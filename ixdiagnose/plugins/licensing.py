import base64
import errno
import hashlib
import os
import stat as stat_module
from datetime import datetime, timezone

from licenselib.license import (
    ContractHardware,
    ContractSoftware,
    ContractType,
    Features,
    License,
    license_v1_struct,
)
from truenas_pylicensed import verify

from ixdiagnose.config import conf
from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import AdminMiddlewareCommand, MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, MiddlewareClientMetric, PythonMetric

# Mirrors middlewared.utils.license.constants. Copied rather than imported so that this plugin
# reaches the same files middlewared reads without inheriting middlewared's view of them.
LICENSE_DIR = "/data/subsystems/truenas_license"
LICENSE_FILE = f"{LICENSE_DIR}/license"
LICENSE_BACKUP = f"{LICENSE_DIR}/license.bak"
LEGACY_LICENSE_FILE = "/data/license"
DAEMON_SOCKET = "/run/truenas/licensed.sock"

LICENSE_DAEMON_UNIT = "truenas-licensed"

# Result codes whose accompanying message is fixed text. Every other code is reported without
# its message, because the daemon formats the chassis product serial into the identity
# mismatch message and a bundle must not carry it.
STATIC_ERROR_CODES = frozenset({"OK", "NO_LICENSE", "DAEMON_UNAVAILABLE", "DAEMON_ERROR", "INTERNAL_ERROR"})
REDACTED_ERROR = "<redacted: may contain system identifiers>"


def _enum_field(value) -> dict:
    """Report an enum byte as both its raw value and its name.

    ``License.load`` leaves the raw int in place when a byte matches no member. Middleware's
    own parser then reaches for ``.name`` on it, raises, and treats the license as absent, so
    a system with a perfectly present license reads as unlicensed. Reporting both halves is
    what makes that state visible from a bundle.
    """
    if isinstance(value, (ContractType, ContractHardware, ContractSoftware)):
        return {"raw": value.value, "name": value.name}

    return {"raw": value, "name": None}


def _file_state(path: str) -> dict:
    """Describe a file without reading it.

    ``exists`` is tri-state. The license blobs are 0600 inside a 0700 directory, so a caller
    without search permission gets EACCES rather than ENOENT, and answering "absent" there
    would report a licensed system as unlicensed.
    """
    state = {"path": path, "state": None, "errno": None, "exists": None, "stat": None}
    try:
        stat_result = os.stat(path)
    except FileNotFoundError:
        state.update({"state": "NOT_FOUND", "errno": "ENOENT", "exists": False})
    except PermissionError as e:
        state.update({"state": "PERMISSION_DENIED_ON_STAT", "errno": errno.errorcode.get(e.errno)})
    except OSError as e:
        state.update({"state": "OS_ERROR", "errno": errno.errorcode.get(e.errno)})
    else:
        state.update(
            {
                "state": "OK",
                "exists": True,
                "stat": {
                    "mode": oct(stat_module.S_IMODE(stat_result.st_mode)),
                    "uid": stat_result.st_uid,
                    "gid": stat_result.st_gid,
                    "size": stat_result.st_size,
                    "mtime": datetime.fromtimestamp(stat_result.st_mtime, tz=timezone.utc).isoformat(),
                },
            }
        )

    return state


def legacy_blob_fields(lic: License) -> dict:
    """Project a decoded legacy license onto the fields a debug may carry.

    Built field by field on purpose. ``License`` is a namedtuple holding ``customer_key``, so
    anything serialising it wholesale leaks; the same reason ``lic`` never reaches an error
    string, since its repr carries that key too.

    Raw values rather than interpretations, because middleware's normalizer injects most of
    the feature set onto every legacy license and drops the expansion shelf codes it has no
    mapping for. What was actually bought is only legible here.
    """
    features = list(lic.features)
    bitmask = 0
    for feature in features:
        bitmask |= feature.value

    return {
        "version": lic.version,
        "model": lic.model or None,
        "system_serial": lic.system_serial or None,
        "system_serial_ha": lic.system_serial_ha or None,
        "contract_type": _enum_field(lic.contract_type),
        "contract_hardware": _enum_field(lic.contract_hardware),
        "contract_software": _enum_field(lic.contract_software),
        "contract_start": lic.contract_start.isoformat(),
        "duration_days": lic.duration,
        "contract_end": lic.contract_end.isoformat(),
        "features_bits": [feature.name for feature in features],
        "features_bitmask": bitmask,
        "addhw_declared_count": len(lic.addhw),
        "addhw_raw": [list(entry) for entry in lic.addhw],
    }


def _raw_blob_extras(raw: bytes) -> dict:
    """Read the two values ``License.load`` discards on the way through.

    It turns the feature bitmask into a list of known members, so a bit no member claims is
    lost, and it slices the trailing shelf pairs blindly, so a truncated tail is lost too.
    Both are read back here using licenselib's own struct definition.
    """
    fields = license_v1_struct.unpack(raw[: license_v1_struct.size])
    bitmask, declared = fields[11], fields[12]
    known = 0
    for feature in Features:
        known |= feature.value

    return {
        "features_bitmask_unknown_bits": bitmask & ~known,
        "trailing_bytes": len(raw) - license_v1_struct.size - (declared * 2),
    }


def _daemon_error(code_name: str, message) -> str | None:
    if message is None:
        return None

    return message if code_name in STATIC_ERROR_CODES else REDACTED_ERROR


def daemon_status(client, context) -> dict:
    """What the license daemon says, alongside what is on disk.

    Middleware collapses every daemon failure into "no license": a stopped daemon, a bad
    signature and an identity mismatch all leave `truenas.license.info` returning null, and
    the result code that separates them is discarded before it reaches any API. Asking the
    daemon directly is the only way a bundle distinguishes those from an unlicensed system.
    """
    result = {
        "daemon": {"queried": False, "error": None},
        "files": {
            "license_file": _file_state(LICENSE_FILE),
            "license_backup": _file_state(LICENSE_BACKUP),
            "legacy_license_file": _file_state(LEGACY_LICENSE_FILE),
            "daemon_socket": _file_state(DAEMON_SOCKET),
        },
    }

    try:
        status = verify(timeout=conf.timeout)
    except Exception as e:
        result["daemon"]["error"] = f"{type(e).__name__}: {e}"
        return result

    code_name = getattr(status.code, "name", str(status.code))
    result["daemon"] = {
        "queried": True,
        "error": None,
        "valid": status.valid,
        "code": code_name,
        "message": _daemon_error(code_name, status.error),
        "version": status.version,
        "type": getattr(status.type, "name", status.type),
        "test": status.test,
        "model": status.model,
        "issued_at": status.issued_at,
        "reload_seq": status.reload_seq,
        "enclosures": status.enclosures,
        "features": {
            name: {
                "source": feature.source,
                "start_date": feature.start_date,
                "expires_at": feature.expires_at,
                "type": feature.type,
            }
            for name, feature in (status.features or {}).items()
        },
        # The values behind these are the hardware fingerprint and the account binding, which
        # are what a license is minted against. Their presence is reportable; they are not.
        "system_id_present": status.system_id is not None,
        "fingerprint_present": status.fingerprint is not None,
        "tnc_present": status.tnc is not None,
    }
    return result


def legacy_license(client, context) -> dict:
    """Decode the legacy license blob independently of middleware.

    Middleware reads this file through a normalizer that injects 18 of the 22 features onto
    every legacy license, so the API view says almost nothing about what a customer bought.
    On the current fleet these raw fields are the only discriminating evidence there is.
    """
    access = _file_state(LEGACY_LICENSE_FILE)
    result = {"access": access, "content_sha256": None, "decode": {"status": None, "error": None}, "blob": None}

    if access["exists"] is not True:
        result["decode"]["status"] = "NOT_PRESENT" if access["exists"] is False else "UNREADABLE"
        return result

    try:
        with open(LEGACY_LICENSE_FILE, "rb") as f:
            raw_file = f.read()
    except PermissionError as e:
        # stat succeeded, so the file provably exists and is merely unreadable by us.
        access.update({"state": "PERMISSION_DENIED_ON_READ", "errno": errno.errorcode.get(e.errno)})
        result["decode"]["status"] = "UNREADABLE"
        return result
    except IsADirectoryError as e:
        access.update({"state": "IS_A_DIRECTORY", "errno": errno.errorcode.get(e.errno)})
        result["decode"]["status"] = "UNREADABLE"
        return result
    except OSError as e:
        access.update({"state": "OS_ERROR", "errno": errno.errorcode.get(e.errno)})
        result["decode"]["status"] = "UNREADABLE"
        return result

    result["content_sha256"] = hashlib.sha256(raw_file).hexdigest()

    try:
        text = raw_file.decode("utf-8").strip("\n")
        blob = legacy_blob_fields(License.load(text))
        blob.update(_raw_blob_extras(base64.b64decode(text)))
    except Exception as e:
        # Never interpolate the license itself here: its repr carries customer_key.
        result["decode"].update({"status": "MALFORMED", "error": f"{type(e).__name__}: {e}"})
        return result

    result["decode"]["status"] = "DECODED"
    result["blob"] = blob
    return result


class Licensing(Plugin):
    name = "licensing"
    metrics = [
        MiddlewareClientMetric(
            "license_info",
            [
                MiddlewareCommand("truenas.license.info"),
                MiddlewareCommand("truenas.entitlements.info"),
                MiddlewareCommand("system.product_type"),
            ],
        ),
        MiddlewareClientMetric("ha_capability", [AdminMiddlewareCommand("system.is_ha_capable")]),
        PythonMetric("daemon_status", daemon_status),
        PythonMetric("legacy_license", legacy_license),
        CommandMetric(
            "daemon_service",
            [
                Command(
                    [
                        "systemctl",
                        "show",
                        LICENSE_DAEMON_UNIT,
                        "-p",
                        "NRestarts,ActiveState,SubState,Result,ExecMainStartTimestamp",
                    ],
                    "License daemon unit state",
                    serializable=False,
                ),
                Command(
                    ["journalctl", "-u", LICENSE_DAEMON_UNIT, "-n", "200", "--no-pager"],
                    "License daemon logs",
                    serializable=False,
                ),
            ],
        ),
    ]

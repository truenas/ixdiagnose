import errno
from datetime import date

import pytest
from licenselib.license import ContractHardware, ContractSoftware, ContractType, Features, License

from ixdiagnose.plugins.licensing import LEGACY_LICENSE_FILE, legacy_blob_fields, legacy_license
from ixdiagnose.utils.formatter import dumps

CUSTOMER_KEY_SENTINEL = "CUSTOMERKEYSENTINEL"
CUSTOMER_NAME_SENTINEL = "CUSTOMERNAMESENTINEL"


def build_license(**overrides) -> License:
    """A legacy license built in process, so a test can name the field it is about.

    Constructed rather than loaded from a checked-in blob: base64 nobody here can regenerate
    would not say which byte a test cares about, and an int contract type cannot be produced
    by `dump()` at all.
    """
    fields = {
        "version": 1,
        "model": "H10",
        "system_serial": "TEST-000001",
        "system_serial_ha": "TEST-000002",
        "contract_type": ContractType.gold,
        "contract_hardware": ContractHardware.parts,
        "contract_software": ContractSoftware.none,
        "contract_start": date(2026, 4, 8),
        "duration": 22,
        "customer_name": CUSTOMER_NAME_SENTINEL,
        "customer_key": CUSTOMER_KEY_SENTINEL,
        "features": [Features.fibrechannel, Features.vm],
        "addhw": [(3, 2), (2, 1)],
    }
    fields.update(overrides)
    return License(**fields)


@pytest.mark.parametrize(
    "exception,expected_state,expected_exists",
    [
        (FileNotFoundError(errno.ENOENT, "No such file or directory"), "NOT_FOUND", False),
        (PermissionError(errno.EACCES, "Permission denied"), "PERMISSION_DENIED_ON_STAT", None),
    ],
)
def test_stat_failure_does_not_claim_the_license_is_absent(mocker, exception, expected_state, expected_exists):
    """EACCES means we cannot tell, and saying "absent" there calls a licensed system unlicensed."""
    mocker.patch("ixdiagnose.plugins.licensing.os.stat", side_effect=exception)

    result = legacy_license(None, None)

    assert result["access"]["state"] == expected_state
    assert result["access"]["exists"] is expected_exists
    assert result["blob"] is None


def test_readable_file_that_is_not_a_license_is_reported_malformed(mocker):
    mocker.patch("ixdiagnose.plugins.licensing.os.stat", return_value=mocker.MagicMock(st_mode=0o100600))
    mocker.patch("builtins.open", mocker.mock_open(read_data=b"not a license"))

    result = legacy_license(None, None)

    assert result["decode"]["status"] == "MALFORMED"
    assert result["decode"]["error"]
    assert result["blob"] is None
    assert result["content_sha256"]


def test_customer_identity_never_reaches_the_output():
    """The blob carries both, and middleware discards both. A bundle must not reintroduce them."""
    serialized = dumps(legacy_blob_fields(build_license()))

    assert CUSTOMER_KEY_SENTINEL not in serialized
    assert CUSTOMER_NAME_SENTINEL not in serialized
    assert "customer_key" not in serialized
    assert "customer_name" not in serialized


def test_unmapped_contract_type_is_reported_rather_than_raising():
    """`License.load` leaves the raw int here, and middleware then reads the system as unlicensed."""
    blob = legacy_blob_fields(build_license(contract_type=9))

    assert blob["contract_type"] == {"raw": 9, "name": None}
    assert blob["contract_hardware"] == {"raw": 0, "name": "parts"}


def test_blob_reports_raw_feature_bits_and_shelves():
    """What was bought is only legible in the raw values; the normalized view injects the rest."""
    blob = legacy_blob_fields(build_license())

    assert blob["features_bits"] == ["fibrechannel", "vm"]
    assert blob["features_bitmask"] == Features.fibrechannel.value | Features.vm.value
    assert blob["addhw_raw"] == [[3, 2], [2, 1]]
    assert blob["contract_end"] == "2026-04-30"
    assert blob["system_serial_ha"] == "TEST-000002"


def test_missing_file_short_circuits_before_reading(mocker):
    mocker.patch("ixdiagnose.plugins.licensing.os.stat", side_effect=FileNotFoundError())
    open_mock = mocker.patch("builtins.open")

    result = legacy_license(None, None)

    assert result["decode"]["status"] == "NOT_PRESENT"
    assert result["access"]["path"] == LEGACY_LICENSE_FILE
    open_mock.assert_not_called()

from dataclasses import dataclass
from typing import Any, Callable

from ixdiagnose.utils.middleware import MiddlewareClient


COUNT: tuple = ([], {"count": True})


@dataclass(frozen=True)
class Call:
    endpoint: str
    payload: tuple = ()


@dataclass(frozen=True)
class Probe:
    """`in_use` receives one result per entry in `calls`, in order."""

    calls: tuple[Call, ...]
    in_use: Callable[..., bool]


def truthy(result: Any) -> bool:
    """Non-empty config value, or a non-zero `count`."""
    return bool(result)


def fields(*names: str) -> Callable[[dict], bool]:
    return lambda config: any(config.get(name) for name in names)


def either(*predicates: Callable[[Any], bool]) -> Callable[..., bool]:
    """In use when any call's own predicate matches that call's own result."""
    return lambda *results: any(predicate(result) for predicate, result in zip(predicates, results))


def dedup_enabled(resources: list) -> bool:
    return any(resource["properties"].get("dedup", {}).get("value", "off") != "off" for resource in resources)


def fec_configured(interfaces: list) -> bool:
    # The sibling `state.fec_mode` is reported by the driver on every capable NIC, so only the
    # presence of the top level key tells a configured mode apart from the card's own default.
    return any("fec_mode" in interface for interface in interfaces)


def spotlight_or_webshare_search(smb_config: dict, webshare_config: dict) -> bool:
    return "SPOTLIGHT" in smb_config["search_protocols"] or bool(webshare_config["search"])


def running_as_ha_pair(failover_status: str) -> bool:
    return failover_status != "SINGLE"


PROBES: dict[str, Probe] = {
    "APPS": Probe((Call("docker.config"), Call("app.query", COUNT)), either(fields("pool"), truthy)),
    "CATALOG_ENTERPRISE_TRAIN": Probe(
        (Call("catalog.config"),),
        lambda config: "enterprise" in config["preferred_trains"],
    ),
    "CONTAINERS": Probe((Call("container.query", COUNT),), truthy),
    "DEDUP": Probe(
        (Call("zfs.resource.query", ({"properties": ["dedup"], "get_children": True},)),),
        dedup_enabled,
    ),
    "DIRECTORY_SERVICES": Probe((Call("system.general.config"),), fields("ds_auth")),
    "FIBRECHANNEL": Probe(
        (Call("iscsi.target.query", ([["mode", "!=", "ISCSI"]], {"count": True})),),
        truthy,
    ),
    "HA": Probe((Call("failover.status"),), running_as_ha_pair),
    "KMIP": Probe((Call("kmip.config"),), fields("enabled")),
    "MISSION_CRITICAL": Probe((Call("update.config"),), lambda config: config["profile"] == "MISSION_CRITICAL"),
    "NETWORK_FEC": Probe((Call("interface.query", ([["type", "=", "PHYSICAL"]],)),), fec_configured),
    "NFS_SNAPSHOT": Probe(
        (Call("sharing.nfs.query", ([["expose_snapshots", "=", True]], {"count": True})),),
        truthy,
    ),
    "NVMEOF_SPDK": Probe((Call("nvmet.global.config"),), lambda config: config["kernel"] is False),
    "PROACTIVE_SUPPORT": Probe((Call("support.config"),), fields("enabled")),
    "RDMA": Probe(
        (
            Call("nvmet.global.config"),
            Call("iscsi.global.config"),
            Call("nvmet.port.query", ([["addr_trtype", "=", "RDMA"]], {"count": True})),
        ),
        either(fields("rdma"), fields("iser"), truthy),
    ),
    "SED": Probe(
        (
            Call("system.advanced.sed_global_password_is_set"),
            # `count` is applied server side, so the response is a bare integer: no disk record,
            # and so no SED password, ever crosses the socket.
            Call("disk.query", ([["passwd", "!=", ""]], {"count": True, "extra": {"passwords": True}})),
        ),
        either(truthy, truthy),
    ),
    "SMB_VEEAM": Probe(
        (Call("sharing.smb.query", ([["purpose", "=", "VEEAM_REPOSITORY_SHARE"]], {"count": True})),),
        truthy,
    ),
    "STIG": Probe((Call("system.security.config"),), fields("enable_gpos_stig", "enable_fips")),
    "TRUESEARCH": Probe((Call("smb.config"), Call("webshare.config")), spotlight_or_webshare_search),
    "VMS": Probe((Call("vm.query", COUNT),), truthy),
    "WEBSHARE": Probe(
        (Call("sharing.webshare.query", ([["enabled", "=", True]], {"count": True})),),
        truthy,
    ),
    "ZFSTIER": Probe((Call("zfs.tier.config"),), fields("enabled")),
}


def features_in_use(client: MiddlewareClient, context: Any) -> dict:
    report: dict[str, Any] = {"in_use": [], "not_in_use": [], "errors": {}}
    for key, entry in sorted(client.call("truenas.entitlements.info")["features"].items()):
        probe = PROBES.get(key)
        if probe is None:
            # Usage cannot be observed, so report what the box is paying for rather than
            # under-reporting on the strength of a check we could not run.
            in_use = entry["entitled"]
        else:
            try:
                results = (client.call(call.endpoint, *call.payload) for call in probe.calls)
                in_use = bool(probe.in_use(*results))
            except Exception as exc:
                report["errors"][key] = repr(exc)
                in_use = entry["entitled"]

        report["in_use" if in_use else "not_in_use"].append(key)

    return report

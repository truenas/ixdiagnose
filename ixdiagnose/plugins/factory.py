import errno

from ixdiagnose.exceptions import CallError
from typing import Dict

from .active_directory import ActiveDirectory
from .base import Plugin
from .hardware import Hardware
from .iscsi import ISCSI
from .kubernetes import Kubernetes
from .ldap import LDAP
from .network import Network
from .nfs import NFS
from .smart import SMART
from .smb import SMB
from .ssl import SSL
from .sysctl import Sysctl
from .system import System
from .zfs import ZFS


class PluginFactory:

    def __init__(self):
        self._creators: dict = {}

    def register(self, plugin: Plugin) -> None:
        self._creators[plugin.name] = plugin

    def plugin(self, name: str) -> Plugin:
        if name not in self._creators:
            raise CallError(f'Unable to locate {name!r} plugin.', errno=errno.ENOENT)
        return self._creators[name]

    def get_plugins(self) -> Dict[str, Plugin]:
        return self._creators


plugin_factory = PluginFactory()
for plugin in [
    ActiveDirectory,
    Hardware,
    ISCSI,
    Kubernetes,
    LDAP,
    Network,
    NFS,
    SMART,
    SMB,
    SSL,
    Sysctl,
    System,
    ZFS,
]:
    plugin_factory.register(plugin())

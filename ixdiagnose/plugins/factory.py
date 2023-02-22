import errno

from ixdiagnose.exceptions import CallError
from typing import Dict

from .base import Plugin
from .hardware import Hardware
from .iscsi import ISCSI
from .kubernetes import Kubernetes
from .nfs import NFS
from .ssl import SSL


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
    Hardware,
    ISCSI,
    Kubernetes,
    NFS,
    SSL,
]:
    plugin_factory.register(plugin())

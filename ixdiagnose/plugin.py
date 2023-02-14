import os

from .plugins.factory import plugin_factory
from .utils.paths import get_plugin_base_dir


def generate_plugins_debug() -> None:
    os.makedirs(get_plugin_base_dir(), exist_ok=True)
    for plugin in plugin_factory.get_plugins().values():
        plugin.execute_metrics()
        plugin.write_debug_report()

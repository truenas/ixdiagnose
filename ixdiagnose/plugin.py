import concurrent.futures
import os

from .plugins.factory import plugin_factory
from .utils.paths import get_plugin_base_dir


def generate_plugins_debug() -> None:
    os.makedirs(get_plugin_base_dir(), exist_ok=True)
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as exc:
        futures = {
            exc.submit(plugin.execute): plugin_name for plugin_name, plugin in plugin_factory.get_plugins().items()
        }
        for future in concurrent.futures.as_completed(futures):
            plugin_name = futures[future]
            try:
                future.result()
            except Exception:
                # TODO: Let's add logging
                raise

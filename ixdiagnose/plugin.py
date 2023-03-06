import concurrent.futures
import os
import traceback

from .plugins.factory import plugin_factory
from .utils.formatter import dumps
from .utils.paths import get_plugin_base_dir


def generate_plugins_debug() -> None:
    os.makedirs(get_plugin_base_dir(), exist_ok=True)
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as exc:
        futures = {
            exc.submit(plugin.execute): plugin_name for plugin_name, plugin in plugin_factory.get_plugins().items()
        }
        plugins_report = {}
        for future in concurrent.futures.as_completed(futures):
            plugin_name = futures[future]
            try:
                report = future.result()
            except Exception as exc:
                # TODO: Let's add logging
                report = {
                    'execution_time': None,
                    'execution_error': str(exc),
                    'execution_traceback': traceback.format_exc(),
                }

            plugins_report[plugin_name] = report

    with open(os.path.join(get_plugin_base_dir(), 'report.json'), 'w') as f:
        f.write(dumps(plugins_report))

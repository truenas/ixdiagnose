import concurrent.futures
import os
import traceback

from .event import send_event
from .plugins.factory import plugin_factory
from .utils.formatter import dumps
from .utils.paths import get_plugin_base_dir


def generate_plugins_debug(percentage: int = 0, total_percentage: int = 100) -> None:
    os.makedirs(get_plugin_base_dir(), exist_ok=True)
    send_event(percentage, 'Gathering plugins debug information')

    plugin_percentage = total_percentage / len(plugin_factory.get_items())
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as exc:
        futures = {
            exc.submit(plugin.execute): plugin_name for plugin_name, plugin in plugin_factory.get_items().items()
        }
        plugins_report = {}
        for future in concurrent.futures.as_completed(futures):
            plugin_name = futures[future]
            try:
                report = future.result()
            except Exception as exc:
                report = {
                    'execution_time': None,
                    'execution_error': str(exc),
                    'execution_traceback': traceback.format_exc(),
                }
                description = f'Error gathering debug information for {plugin_name!r} plugin'
            else:
                description = f'Gathered debug information for {plugin_name!r} plugin'

            plugins_report[plugin_name] = report
            percentage += plugin_percentage
            send_event(percentage, description)

    with open(os.path.join(get_plugin_base_dir(), 'report.json'), 'w') as f:
        f.write(dumps(plugins_report))

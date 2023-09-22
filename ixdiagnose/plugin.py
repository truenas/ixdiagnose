import os
import traceback

from .config import conf
from .event import send_event
from .plugins.factory import plugin_factory
from .utils.formatter import dumps
from .utils.paths import get_plugin_base_dir


def generate_plugins_debug(percentage: int = 0, total_percentage: int = 100) -> None:
    os.makedirs(get_plugin_base_dir(), exist_ok=True)

    to_execute_plugins = {k: v for k, v in plugin_factory.get_items().items() if k not in conf.exclude_plugins}
    plugin_percentage = total_percentage / (len(to_execute_plugins) or 1)  # We want to handle this quietly
    plugins_report = {}
    for plugin_name, plugin in to_execute_plugins.items():
        send_event(int(percentage + 0.5), f'Gathering debug information for {plugin_name!r} plugin')

        try:
            report = plugin.execute()
        except Exception as exc:
            report = {
                'execution_time': None,
                'execution_error': str(exc),
                'execution_traceback': traceback.format_exc(),
            }

        plugins_report[plugin_name] = report
        percentage += plugin_percentage

    send_event(total_percentage, 'Gathered debug information for plugins')
    with open(os.path.join(get_plugin_base_dir(), 'report.json'), 'w') as f:
        f.write(dumps(plugins_report))

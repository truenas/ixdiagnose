import os
import traceback

from .config import conf
from .event import send_event
from .plugins.factory import plugin_factory
from .utils.formatter import dumps
from .utils.paths import get_plugin_base_dir


def generate_plugins_debug(percentage: int = 0, total_percentage: int = 100) -> None:
    os.makedirs(get_plugin_base_dir(), exist_ok=True)
    send_event(percentage + 1, 'Gathering plugins debug information')

    to_execute_plugins = {k: v for k, v in plugin_factory.get_items().items() if k not in conf.exclude_plugins}
    plugin_percentage = total_percentage / len(to_execute_plugins)
    plugins_report = {}
    for plugin_name, plugin in to_execute_plugins.items():
        try:
            report = plugin.execute()
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
        # The discrepancy is due to the accumulation of floating-point precision errors when summing up
        # `plugin_percentage` the total length of `to_execute_plugins` times.
        # This is a known issue in numerical computing, refer: https://docs.python.org/3/tutorial/floatingpoint.html.
        send_event(int(percentage), description)

    with open(os.path.join(get_plugin_base_dir(), 'report.json'), 'w') as f:
        f.write(dumps(plugins_report))

import contextlib
import json
import os
import shutil

from ixdiagnose.config import conf
from ixdiagnose.plugin import generate_plugins_debug, plugin_factory
from jsonschema import validate

from .utils import BASE_REPORT_SCHEMA


PLUGINS_REPORT_SCHEMA = {
    'type': 'object',
    'properties': {
        'execution_time': {'type': 'number'},
        'metric_report': {
            'anyOf': [
                {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'error': {'type': ['string', 'null', 'object']},
                            'command': {'type': ['string', 'array']},
                            'execution_time': {'type': 'number'},
                            'description': {'type': ['string', 'null']},
                            'returncode': {'type': 'integer'},
                            'endpoint': {'type': 'string'},
                        },
                    }
                },
                {
                    'type': 'object',
                    'properties': {
                        'error': {'type': ['string', 'null']}
                    }
                },
            ],

        },
        'metric_execution_error': {'type': ['string', 'null']},
        'metric_execution_traceback': {'type': ['string', 'null']},
    },
}


@contextlib.contextmanager
def generate_plugins():
    conf.debug_path = '/tmp/ixdiagnose'
    os.makedirs(conf.debug_path, exist_ok=True)

    try:
        generate_plugins_debug()
        yield os.path.join(conf.debug_path, 'debug/plugins')
    finally:
        shutil.rmtree(conf.debug_path, ignore_errors=True)


def get_plugins_dirs(base_plugins_dir) -> list:
    return [
        os.path.join(base_plugins_dir, i) for i in os.listdir(base_plugins_dir)
        if os.path.isdir(os.path.join(base_plugins_dir, i))
    ]


def test_base_report_generation():
    with generate_plugins() as plugins_dir:
        assert os.path.exists(os.path.join(plugins_dir, 'report.json')) is True


def test_plugins_directories_report_generation():
    with generate_plugins() as plugins_dir:
        plugins_dirs = get_plugins_dirs(plugins_dir)
        assert len(plugins_dirs) > 0
        for plugin_dir in plugins_dirs:
            assert os.path.exists(os.path.join(plugin_dir, 'report.json')) is True


def test_plugins_count():
    with generate_plugins() as plugins_dir:
        plugins_dirs = get_plugins_dirs(plugins_dir)
        assert len(plugins_dirs) == len(plugin_factory.get_items())


def test_report_schema():
    with generate_plugins() as plugins_dir:
        with open(os.path.join(plugins_dir, 'report.json')) as f:
            base_report = json.loads(f.read())

        assert set(plugin_factory.get_items()) == set(base_report)

        for plugin_name, plugin_report in base_report.items():
            validate(base_report[plugin_name], BASE_REPORT_SCHEMA)

        for plugin_dir in get_plugins_dirs(plugins_dir):
            with open(os.path.join(plugin_dir, 'report.json')) as f:
                plugin_report = json.loads(f.read())

            plugin = plugin_factory.get_items()[os.path.basename(plugin_dir)]
            assert {metric.name for metric in plugin.metrics_to_execute()} == set(plugin_report)

            for metric_report in plugin_report.values():
                validate(metric_report, PLUGINS_REPORT_SCHEMA)

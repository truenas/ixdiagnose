import contextlib
import os
import shutil

from ixdiagnose.config import conf
from ixdiagnose.plugin import generate_plugins_debug, plugin_factory


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

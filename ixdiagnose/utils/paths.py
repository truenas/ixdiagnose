import os

from ixdiagnose.config import conf


def get_debug_dir() -> str:
    return os.path.join(conf.debug_path, 'debug')


def get_plugin_base_dir() -> str:
    return os.path.join(get_debug_dir(), 'plugins')

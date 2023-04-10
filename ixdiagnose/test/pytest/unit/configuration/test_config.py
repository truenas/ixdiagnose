import pytest

from ixdiagnose.config import conf
from jsonschema import ValidationError


@pytest.mark.parametrize('config_values,should_work', [
    (
        {
            'compress': True,
            'compressed_path': None,
            'clean_debug_path': True,
            'debug_path': None,
            'exclude_plugins': [],
            'structured_data': False,
            'timeout': 300,
        },
        True,
    ),
    (
        {
            'compress': True,
            'compressed_path': '/tmp/ixdiagnose.tgz',
            'clean_debug_path': True,
            'debug_path': '/tmp/ixdiagnose',
            'exclude_plugins': ['active_directory', 'smb', 'vm'],
            'structured_data': True,
            'timeout': 300,
        },
        True,
    ),
    (
        {
            'compress': True,
            'compressed_path': 1234,
            'clean_debug_path': 'True',
            'debug_path': 200,
            'exclude_plugins': {},
            'structured_data': False,
            'timeout': 300,
        },
        False,
    ),
    (
        {
            'compress': False,
            'compressed_path': 'ixdiagnose.tgz',
            'clean_debug_path': True,
            'debug_path': None,
            'exclude_plugins': [True, False],
            'structured_data': False,
            'timeout': 300,
        },
        False,
    )
])
def test_config_schema(config_values, should_work):
    if should_work:
        assert conf.apply(config_values) is None
    else:
        with pytest.raises(ValidationError):
            conf.apply(config_values)


@pytest.mark.parametrize('config_value', [
    {
        'compress': True,
        'compressed_path': '/tmp/ixdiagnose.tgz',
        'clean_debug_path': True,
        'debug_path': '/tmp/ixdiagnose',
        'exclude_plugins': ['active_directory', 'smb', 'vm'],
        'structured_data': True,
        'timeout': 300,
    },
])
def test_update_new_config(config_value):
    conf.apply(config_value)
    for key, value in config_value.items():
        assert (conf.__dict__.get(key) == value) is True

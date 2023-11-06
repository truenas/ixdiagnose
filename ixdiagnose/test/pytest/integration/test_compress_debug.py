import contextlib
import os
import pytest
import shutil
import tarfile

from ixdiagnose.artifacts.factory import artifact_factory
from ixdiagnose.config import conf
from ixdiagnose.plugins.factory import plugin_factory
from ixdiagnose.run import generate_debug
from ixdiagnose.utils.paths import get_debug_dir, get_plugin_base_dir, get_artifacts_base_dir


@contextlib.contextmanager
def debug_generate(clean_debug):
    conf.debug_path = '/tmp/ixdiagnose/debug'
    conf.compressed_path = '/tmp/ixdiagnose.tgz'
    conf.compress = True
    conf.clean_debug_path = clean_debug
    try:
        yield generate_debug()
    finally:
        shutil.rmtree(conf.debug_path, ignore_errors=True)
        os.remove(conf.compressed_path)


def test_compress_debug_generation():
    with debug_generate(True) as path:
        debug_dir_basename = os.path.basename(get_debug_dir())
        with tarfile.open(path, 'r') as tar:
            plugins_dir = tar.getmember(
                os.path.join(debug_dir_basename, os.path.basename(get_plugin_base_dir()))
            ).name
            artifacts_dir = tar.getmember(
                os.path.join(debug_dir_basename, os.path.basename(get_artifacts_base_dir()))
            ).name
            members = [member.name for member in tar.getmembers()]
            for plugin_name in plugin_factory.get_items().keys():
                assert os.path.join(plugins_dir, plugin_name) in members
            for artifact_name in artifact_factory.get_items().keys():
                assert os.path.join(artifacts_dir, artifact_name) in members


@pytest.mark.parametrize('clean_debug', [
    False, True
])
def test_ixdiagnose_clean_debug(clean_debug):
    with debug_generate(clean_debug):
        if clean_debug:
            assert os.path.exists(conf.debug_path) is False
        else:
            assert os.path.exists(conf.debug_path) is True


def test_path_perms():
    with debug_generate(False):
        assert (os.stat(conf.debug_path).st_mode & 0o777) == 0o700
        assert (os.stat(conf.compressed_path).st_mode & 0o777) == 0o700

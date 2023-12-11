import os
import pathlib
import shutil
import tarfile
import tempfile

from .artifact import gather_artifacts
from .config import conf
from .exceptions import CallError
from .event import event_callbacks, send_event
from .plugin import generate_plugins_debug
from .utils.paths import get_debug_dir


def generate_debug() -> str:
    # This will generate a debug and then compress the directory as specified
    # In case of compression being set, it will return path of compressed file
    # otherwise return the debug path
    if conf.debug_path and not os.path.isabs(conf.debug_path):
        raise CallError('Debug path must be absolute')

    if conf.compress and conf.compressed_path:
        if not os.path.isabs(conf.compressed_path):
            raise CallError('Compressed path must be absolute')

        if os.path.exists(conf.compressed_path):
            raise CallError('Compressed path already exists')

    if not conf.debug_path:
        conf.clean_debug_path = conf.compress
        conf.debug_path = tempfile.TemporaryDirectory().name

    os.makedirs(conf.debug_path, 0o700, exist_ok=True)
    os.chmod(conf.debug_path, 0o700)

    send_event(0, 'Generating debug')
    generate_plugins_debug(total_percentage=90)
    gather_artifacts(90, total_percentage=8)
    debug_dir = get_debug_dir()
    debug_dir_path = pathlib.Path(debug_dir)
    for path, contents in conf.extra.items():
        target_path = os.path.normpath(os.path.join(debug_dir, path))
        if debug_dir_path in pathlib.Path(target_path).parents:
            if not os.path.exists(target_path):
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                with open(target_path, 'w') as f:
                    f.write(contents)
    if conf.compress:
        send_event(99, 'Compressing debug')
        compress_debug()

    send_event(100, 'Completed generating debug')
    event_callbacks.clear()

    return conf.compressed_path if conf.compress else conf.debug_path


def compress_debug() -> None:
    if conf.compress and not conf.compressed_path:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            conf.compressed_path = temp_file.name

    with tarfile.open(conf.compressed_path, 'w:gz') as tar:
        for entry in os.listdir(conf.debug_path):
            tar.add(os.path.join(conf.debug_path, entry), arcname=entry)

    os.chmod(conf.compressed_path, 0o700)

    if conf.clean_debug_path:
        shutil.rmtree(conf.debug_path, ignore_errors=True)

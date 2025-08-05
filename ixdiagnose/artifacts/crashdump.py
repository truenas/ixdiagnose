from .base import Artifact
from .items import Glob


class Crashdump(Artifact):
    base_dir = '/var/lib/systemd'
    name = 'crashdump'
    individual_item_max_size_limit = 1 * 1024 * 1024
    items = [
        Glob('pstore/*/dmesg.txt', relative_to='/var/lib/systemd'),
    ]

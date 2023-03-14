from .base import Artifact
from .items import Pattern


class Crash(Artifact):
    base_dir = '/data/crash'
    name = 'crash'
    items = [
        Pattern(r'.*'),
    ]

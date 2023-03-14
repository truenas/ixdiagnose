from .base import Artifact
from .items import Directory


class Crash(Artifact):
    base_dir = '/data'
    name = 'crash'
    items = [
        Directory('crash'),
    ]

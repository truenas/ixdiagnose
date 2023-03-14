from .base import Artifact
from .items import File


class SystemInfo(Artifact):
    base_dir = '/etc'
    name = 'sys_info'
    items = [
        File('hostid'),
        File('version'),
    ]

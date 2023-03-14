from .base import Artifact
from .items import Directory, File, Pattern


class Logs(Artifact):
    base_dir = '/var/log'
    name = 'logs'
    items = [
        Directory('pods'),
        File('middlewared.log'),
        File('kern.log'),
        Pattern(r'sys*'),
    ]

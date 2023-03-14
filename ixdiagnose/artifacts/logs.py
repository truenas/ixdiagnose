from .base import Artifact
from .items import File


class Logs(Artifact):
    base_dir = '/var/log'
    name = 'logs'
    items = [
        File('middlewared.log'),
        File('kern.log'),
    ]

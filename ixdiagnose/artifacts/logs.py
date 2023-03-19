from .base import Artifact
from .items import Directory, File


class Logs(Artifact):
    base_dir = '/var/log'
    name = 'logs'
    individual_item_max_size_limit = 5 * 1024 * 1024
    items = [
        Directory('openvpn'),
        Directory('pods'),
        Directory('samba4'),
        File('daemon.log'),
        File('failover.log'),
        File('kern.log'),
        File('messages'),
        File('middlewared.log'),
        File('syslog'),
        File('zettarepl.log'),
    ]

from .base import Artifact
from .items import Directory, File, Pattern


class Logs(Artifact):
    base_dir = '/var/log'
    name = 'logs'
    individual_item_max_size_limit = 10 * 1024 * 1024
    items = [
        Directory('openvpn'),
        Directory('pods'),
        Directory('samba4'),
        Pattern('daemon.+'),
        File('failover.+'),
        File('kern.log'),
        File('messages'),
        Pattern('middlewared.+'),
        File('syslog'),
        Pattern('zettarepl.+'),
    ]

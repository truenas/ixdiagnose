from .base import Artifact
from .items import Directory, File


class Logs(Artifact):
    base_dir = '/var/log'
    name = 'logs'
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

from .base import Artifact
from .items import Directory, File, Pattern


class Logs(Artifact):
    base_dir = '/var/log'
    name = 'logs'
    individual_item_max_size_limit = 10 * 1024 * 1024
    items = [
        Directory('ctdb'),
        Directory('jobs'),
        Directory('libvirt'),
        Directory('netdata'),
        Directory('openvpn'),
        Directory('pods'),
        Directory('proftpd'),
        Directory('samba4'),
        File('auth.log'),
        File('debug'),
        File('dpkg.log'),
        File('error'),
        File('kern.log'),
        File('messages'),
        File('syslog'),
        File('wsdd.log'),
        Pattern('daemon.+'),
        Pattern('failover.+'),
        Pattern('fenced.+'),
        Pattern('middlewared.+'),
        Pattern('zettarepl.+'),
    ]

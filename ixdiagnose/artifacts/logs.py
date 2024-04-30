from .base import Artifact
from .items import DirectoryPattern, File, Pattern


class Logs(Artifact):
    base_dir = '/var/log'
    name = 'logs'
    individual_item_max_size_limit = 10 * 1024 * 1024
    items = [
        DirectoryPattern('ctdb'),
        DirectoryPattern('jobs'),
        DirectoryPattern('libvirt'),
        DirectoryPattern(
            'netdata', pattern=r'^(access|error|debug|health)\.log$', max_size=2 * 1024 * 1024,
        ),
        DirectoryPattern('openvpn'),
        DirectoryPattern('pods'),
        DirectoryPattern('proftpd'),
        DirectoryPattern('samba4'),
        File('auth.log'),
        File('debug'),
        File('dpkg.log'),
        File('error'),
        File('kern.log'),
        File('messages'),
        File('netdata_api.log'),
        File('syslog'),
        File('wsdd.log'),
        Pattern('daemon.+'),
        Pattern('failover.+'),
        Pattern('fenced.+'),
        Pattern('middlewared.+'),
        Pattern('zettarepl.+'),
    ]

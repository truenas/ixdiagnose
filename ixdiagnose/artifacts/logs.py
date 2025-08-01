from .base import Artifact
from .items import DirectoryPattern, File, Pattern


class Logs(Artifact):
    base_dir = '/var/log'
    name = 'logs'
    individual_item_max_size_limit = 10 * 1024 * 1024
    items = [
        DirectoryPattern('incus'),
        DirectoryPattern('jobs'),
        DirectoryPattern('libvirt'),
        DirectoryPattern(
            'netdata', pattern=r'^(access|error|debug|health)\.log$', max_size=2 * 1024 * 1024,
        ),
        DirectoryPattern('openvpn'),
        DirectoryPattern('proftpd'),
        DirectoryPattern('samba4'),
        DirectoryPattern('sssd', pattern=r'^(ldap_child|sssd)_?(.*)?(\.log)(\.1)?$'),
        File('app_lifecycle.log'),
        File('app_migrations.log'),
        File('auth.log'),
        File('debug'),
        File('dpkg.log'),
        File('error'),
        File('kern.log'),
        File('k8s_api.log'),
        File('messages'),
        File('messages.1'),
        File('netdata_api.log'),
        File('scst.log'),
        File('scst.log.1'),
        File('syslog'),
        File('syslog.1'),
        File('truenas_connect.log'),
        File('truenas_verify.log'),
        File('wsdd.log'),
        Pattern('daemon.+'),
        Pattern('failover.+'),
        Pattern('fenced.+'),
        Pattern('middlewared.+'),
        Pattern('zettarepl.+'),
    ]

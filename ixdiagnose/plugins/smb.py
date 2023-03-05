from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareClient, MiddlewareCommand
from ixdiagnose.utils.run import run
from typing import Any


from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric, PythonMetric


def get_smb_shares(client: MiddlewareClient, context: Any) -> str:
    command = ''
    smb_shares = client.call('sharing.smb.query')
    ds_with_rawvalue_on = {
        ds['properties']['mountpoint']['parsed']: ds for ds in client.call(
            'zfs.dataset.query', [
                ['properties.acltype.rawvalue', '!=', 'off'], ['properties.mountpoint.parsed', '!=', None]
            ]
        )
    }
    for smb_share in smb_shares:
        command += f'net conf showshare {smb_share["name"]}\n'
        command += f'ls -ld {smb_share["path"]}\n'
        command += f'df -T {smb_share["path"]}\n'
        if ds := ds_with_rawvalue_on.get(smb_share['path']):
            acl_type = ds['properties']['acltype']['parsed']
            if acl_type == 'nfsv4':
                command += f'nfs4xdr_getfacl {smb_share["path"]};\n'
            else:
                f'getfacl {smb_share["path"]};\n'

    cp = run(command, shell=True, check=False)
    if cp.returncode:
        return f'Failed to retrieve SMB Share(s) configuration: {cp.stderr}'
    else:
        return cp.stdout


class SMB(Plugin):
    name = 'smb'
    metrics = [
        CommandMetric(
            'net_config', [
                Command(['net', 'conf', 'showshare', 'global'], 'SMB Global Configuration', serializeable=False),
                Command(['net', 'getlocalsid'], 'SID of the Local Server', serializeable=False),
                Command(['net', 'getdomainsid'], 'SID of Domain', serializeable=False),
                Command(['net', 'status', 'sessions'], 'Net Status Sessions', serializeable=False, max_lines=50),
                Command(['net', 'status', 'shares'], 'Net Shares Status', serializeable=False),
            ]
        ),
        CommandMetric(
            'smb_general', [
                Command(['smbd', '-V'], 'Samba Version', serializeable=False),
                Command(['smbd', '-b'], 'Samba Build Information', serializeable=False),
                Command(['testparm', '-s'], 'SMB Global Configuration', serializeable=False),
            ]
        ),
        FileMetric('smb_config_file', '/etc/smb4.conf'),
        MiddlewareClientMetric(
            'smb_info', [
                MiddlewareCommand('smb.config'),
                MiddlewareCommand('smb.status'),
                MiddlewareCommand('smb.groupmap_list'),
                MiddlewareCommand('smb.sharesec.query'),
                MiddlewareCommand('smb.passdb_list'),
                MiddlewareCommand('sharing.smb.query'),
            ]
        ),
        PythonMetric('smb_shares', callback=get_smb_shares, description='SMB Shares and Permissions'),
    ]
    raw_metrics = [
        CommandMetric(
            'smb_lock_info', [
                Command(['smbstatus', '-L'], 'SMB Lock Information', max_lines=50, serializeable=False),
            ]
        ),
    ]
    serializable_metrics = [
        CommandMetric(
            'smb_lock_info', [
                Command(['smbstatus', '-j', '-L'], 'SMB Lock Information', max_lines=50),
            ]
        ),
    ]

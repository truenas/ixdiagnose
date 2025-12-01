from ixdiagnose.utils.command import Command
from ixdiagnose.utils.formatter import dumps
from ixdiagnose.utils.middleware import MiddlewareClient, MiddlewareCommand
from ixdiagnose.utils.run import run
from typing import Any


from .base import Plugin
from .metrics import CommandMetric, FileMetric, MiddlewareClientMetric, PythonMetric


def get_smb_shares(client: MiddlewareClient, context: Any) -> str:
    smb_shares = client.call('sharing.smb.query')
    for smb_share in smb_shares:
        smb_share['acl'] = client.call('sharing.smb.getacl', {'share_name': smb_share['name']})

        # Get the smb.conf section for the share
        testparm = run(f'testparm -s --section-name {smb_share["name"]}', check=False)
        if testparm.returncode:
            smb_share['smb.conf'] = f'Failed to get SMB share configuration: {testparm.stderr}'
        else:
            smb_share['smb.conf'] = testparm.stdout

        # Get statfs info for share (helps us to determine how to read ACL)
        try:
            statfs = client.call('filesystem.statfs', smb_share['path'])
        except Exception as exc:
            smb_share['statfs'] = f'Failed to get statfs for share: {exc}'
            acl_cmd = None  # Most likely locked path
        else:
            smb_share['statfs'] = statfs
            acl_cmd = 'nfs4xdr_getfacl' if 'NFS4ACL' in statfs['flags'] else 'getfacl'

        if acl_cmd:
            getacl = run(f'{acl_cmd} {smb_share["path"]}', check=False)
            if getacl.returncode:
                smb_share['fsacl'] = f'Failed to get fs acl: {getacl.stderr}'
            else:
                smb_share['fsacl'] = getacl.stdout

    return dumps(smb_shares)


class SMB(Plugin):
    name = 'smb'
    metrics = [
        CommandMetric(
            'net_config', [
                Command(['net', 'getlocalsid'], 'SID of the Local Server', serializable=False),
                Command(['net', 'getdomainsid'], 'SID of Domain', serializable=False),
                Command(['net', 'status', 'sessions'], 'Net Status Sessions', serializable=False, max_lines=50),
                Command(['net', 'status', 'shares'], 'Net Shares Status', serializable=False),
            ]
        ),
        CommandMetric(
            'smb_general', [
                Command(['smbd', '-V'], 'Samba Version', serializable=False),
                Command(['smbd', '-b'], 'Samba Build Information', serializable=False),
                Command(['testparm', '-s'], 'SMB Global Configuration', serializable=False),
            ]
        ),
        CommandMetric(
            'samba_account_info', [
                Command(['pdbedit', '-Lv'], 'Passdb list', serializable=False),
                Command(['net', 'groupmap', 'list', '-v'], 'Groupmap list', serializable=False)
            ]
        ),
        FileMetric('smb4', '/etc/smb4.conf', extension='.conf'),
        MiddlewareClientMetric(
            'smb_info', [
                MiddlewareCommand('smb.config'),
                MiddlewareCommand('smb.status'),
                MiddlewareCommand('sharing.smb.query'),
            ]
        ),
        PythonMetric(
            'smb_shares', callback=get_smb_shares, description='SMB Shares and Permissions', serializable=False,
        ),
    ]
    raw_metrics = [
        CommandMetric(
            'smb_lock_info', [
                Command(['smbstatus', '-L'], 'SMB Lock Information', max_lines=50, serializable=False),
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

from ixdiagnose.utils.factory import Factory

from .active_directory import ActiveDirectory
from .apps import Apps
from .audit import Audit
from .certificates import Certificates
from .cloud_backup import CloudBackup
from .cloud_sync import CloudSync
from .containers import Containers
from .cpu import Cpu
from .cronjob import Cronjob
from .failover import Failover
from .ftp import FTP
from .hardware import Hardware
from .initshutdown_scripts import InitShutDownScripts
from .ipmi import IPMI
from .iscsi import ISCSI
from .jobs import CoreGetJobs
from .ldap import LDAP
from .network import Network
from .nfs import NFS
from .rbac import RBAC
from .replication import Replication
from .reporting import Reporting
from .rsync import Rsync
from .services import Services
from .smart import SMART
from .smb import SMB
from .snmp import SNMP
from .ssl import SSL
from .sysctl import Sysctl
from .system import System
from .system_state import SystemState
from .two_factor_auth import TwoFactorAuth
from .ups import UPS
from .vm import VM
from .zfs import ZFS


plugin_factory = Factory()
for plugin in [
    ActiveDirectory,
    Apps,
    Audit,
    Certificates,
    CloudBackup,
    CloudSync,
    Containers,
    CoreGetJobs,
    Cpu,
    Cronjob,
    Failover,
    FTP,
    Hardware,
    InitShutDownScripts,
    IPMI,
    ISCSI,
    LDAP,
    Network,
    NFS,
    RBAC,
    Replication,
    Reporting,
    Rsync,
    Services,
    SMART,
    SMB,
    SNMP,
    SSL,
    Sysctl,
    System,
    SystemState,
    TwoFactorAuth,
    UPS,
    VM,
    ZFS,
]:
    plugin_factory.register(plugin())

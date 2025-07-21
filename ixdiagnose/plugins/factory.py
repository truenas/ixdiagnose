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
from .exceptions import LoggedExceptions
from .failover import Failover
from .fc import FibreChannel
from .ftp import FTP
from .hardware import Hardware
from .initshutdown_scripts import InitShutDownScripts
from .ipmi import IPMI
from .iscsi import ISCSI
from .jobs import CoreGetJobs
from .ldap import LDAP
from .network import Network
from .nfs import NFS
from .nvme import NVME
from .nvmet import NVMet
from .rbac import RBAC
from .replication import Replication
from .reporting import Reporting
from .rsync import Rsync
from .services import Services
from .smart import SMART
from .smb import SMB
from .snmp import SNMP
from .ssh import SSH
from .ssl import SSL
from .sysctl import Sysctl
from .system import System
from .system_state import SystemState
from .system_vendor import SystemVendor
from .truenas_connect import TruenasConnect
from .two_factor_auth import TwoFactorAuth
from .ups import UPS
from .virt import Virt
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
    FibreChannel,
    FTP,
    Hardware,
    InitShutDownScripts,
    IPMI,
    ISCSI,
    LDAP,
    LoggedExceptions,
    Network,
    NFS,
    NVME,
    NVMet,
    RBAC,
    Replication,
    Reporting,
    Rsync,
    Services,
    SMART,
    SMB,
    SNMP,
    SSH,
    SSL,
    Sysctl,
    System,
    SystemState,
    SystemVendor,
    TruenasConnect,
    TwoFactorAuth,
    UPS,
    Virt,
    VM,
    ZFS,
]:
    plugin_factory.register(plugin())

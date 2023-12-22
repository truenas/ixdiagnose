from ixdiagnose.utils.factory import Factory

from .active_directory import ActiveDirectory
from .certificates import Certificates
from .clustering import Clustering
from .cloud_backup import CloudBackup
from .cloud_sync import CloudSync
from .containers import Containers
from .cpu import Cpu
from .cronjob import Cronjob
from .ftp import FTP
from .hardware import Hardware
from .initshutdown_scripts import InitShutDownScripts
from .ipmi import IPMI
from .iscsi import ISCSI
from .jobs import CoreGetJobs
from .kubernetes import Kubernetes
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
from .ssl import SSL
from .sysctl import Sysctl
from .system import System
from .system_state import SystemState
from .two_factor_auth import TwoFactorAuth
from .vm import VM
from .zfs import ZFS


plugin_factory = Factory()
for plugin in [
    ActiveDirectory,
    Certificates,
    CloudBackup,
    CloudSync,
    Clustering,
    Containers,
    CoreGetJobs,
    Cpu,
    Cronjob,
    FTP,
    Hardware,
    InitShutDownScripts,
    IPMI,
    ISCSI,
    Kubernetes,
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
    SSL,
    Sysctl,
    System,
    SystemState,
    TwoFactorAuth,
    VM,
    ZFS,
]:
    plugin_factory.register(plugin())

from ixdiagnose.utils.factory import Factory

from .active_directory import ActiveDirectory
from .clustering import Clustering
from .hardware import Hardware
from .iscsi import ISCSI
from .kubernetes import Kubernetes
from .ldap import LDAP
from .network import Network
from .nfs import NFS
from .replication import Replication
from .services import Services
from .smart import SMART
from .smb import SMB
from .ssl import SSL
from .sysctl import Sysctl
from .system import System
from .vm import VM
from .zfs import ZFS


plugin_factory = Factory()
for plugin in [
    ActiveDirectory,
    Clustering,
    Hardware,
    ISCSI,
    Kubernetes,
    LDAP,
    Network,
    NFS,
    Replication,
    Services,
    SMART,
    SMB,
    SSL,
    Sysctl,
    System,
    VM,
    ZFS,
]:
    plugin_factory.register(plugin())

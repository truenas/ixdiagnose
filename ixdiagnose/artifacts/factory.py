from ixdiagnose.utils.factory import Factory

from .logs import Logs
from .sys_info import SystemInfo
from .proc import ProcFS

artifact_factory = Factory()
for artifact in [
    Logs,
    SystemInfo,
    ProcFS,
]:
    artifact_factory.register(artifact())

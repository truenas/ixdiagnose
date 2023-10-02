from ixdiagnose.utils.factory import Factory

from .logs import Logs
from .proc import ProcFS
from .sys_info import SystemInfo


artifact_factory = Factory()
for artifact in [
    Logs,
    ProcFS,
    SystemInfo,
]:
    artifact_factory.register(artifact())

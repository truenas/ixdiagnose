from ixdiagnose.utils.factory import Factory

from .logs import Logs
from .sys_info import SystemInfo
from .proc import ProcFS
from .sys_parameters import SysFSParameters


artifact_factory = Factory()
for artifact in [
    Logs,
    ProcFS,
    SysFSParameters,
    SystemInfo,
]:
    artifact_factory.register(artifact())

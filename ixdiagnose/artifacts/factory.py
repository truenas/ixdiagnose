from ixdiagnose.utils.factory import Factory

from .logs import Logs
from .proc import ProcFS
from .sys_info import SystemInfo
from .sys_parameters import SysFSParameters


artifact_factory = Factory()
for artifact in [
    Logs,
    ProcFS,
    SysFSParameters,
    SystemInfo,
]:
    artifact_factory.register(artifact())

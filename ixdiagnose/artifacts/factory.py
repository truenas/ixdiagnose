from ixdiagnose.utils.factory import Factory

from .coredumps import CoreDumps
from .crash import Crash
from .logs import Logs
from .sys_info import SystemInfo


artifact_factory = Factory()
for artifact in [
    CoreDumps,
    Crash,
    Logs,
    SystemInfo,
]:
    artifact_factory.register(artifact())

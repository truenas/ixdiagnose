from ixdiagnose.utils.factory import Factory

from .coredumps import CoreDumps
from .logs import Logs
from .sys_info import SystemInfo


artifact_factory = Factory()
for artifact in [
    CoreDumps,
    Logs,
    SystemInfo,
]:
    artifact_factory.register(artifact())

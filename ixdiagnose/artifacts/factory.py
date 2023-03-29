from ixdiagnose.utils.factory import Factory

from .logs import Logs
from .sys_info import SystemInfo


artifact_factory = Factory()
for artifact in [
    Logs,
    SystemInfo,
]:
    artifact_factory.register(artifact())

import errno

from ixdiagnose.exceptions import CallError
from typing import Dict

from .base import Artifact
from .logs import Logs


# TODO: Lets have a common class for factory
class ArtifactFactory:

    def __init__(self):
        self._creators: dict = {}

    def register(self, artifact: Artifact) -> None:
        self._creators[artifact.name] = artifact

    def artifact(self, name: str) -> Artifact:
        if name not in self._creators:
            raise CallError(f'Unable to locate {name!r} artifact.', errno=errno.ENOENT)
        return self._creators[name]

    def get_artifacts(self) -> Dict[str, Artifact]:
        return self._creators


artifact_factory = ArtifactFactory()
for artifact in [
    Logs,
]:
    artifact_factory.register(artifact())

from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, MiddlewareClientMetric
from ixdiagnose.utils.command import Command
from .prerequisites import FibreChannelPrerequisite


class FibreChannel(Plugin):
    name = 'fc'
    metrics = [
        CommandMetric(
            "fcdump",
            [
                Command(["fcdump.py", "--format", "text"], "fcdump.py --format text", serializable=False),
            ],
            prerequisites=[FibreChannelPrerequisite()],
        ),
        MiddlewareClientMetric(
            'fc_hosts', [
                MiddlewareCommand('fc.fc_hosts'),
            ],
            prerequisites=[FibreChannelPrerequisite()],
        ),
        MiddlewareClientMetric(
            'fc_host_pairs', [
                MiddlewareCommand('fc.fc_host.query'),
            ],
            prerequisites=[FibreChannelPrerequisite()],
        ),
        MiddlewareClientMetric(
            'fcport', [
                MiddlewareCommand('fcport.query'),
            ],
            prerequisites=[FibreChannelPrerequisite()],
        ),
    ]

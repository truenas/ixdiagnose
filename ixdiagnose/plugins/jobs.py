from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import MiddlewareClientMetric


class CoreGetJobs(Plugin):
    name = 'jobs'
    metrics = [
        MiddlewareClientMetric('jobs', [MiddlewareCommand('core.get_jobs')]),
    ]

from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import FileMetric, MiddlewareClientMetric


class Cronjob(Plugin):
    name = 'cronjob'
    metrics = [
        FileMetric('crontab', '/etc/crontab', extension='.txt'),
        FileMetric('middleware_crontab', '/etc/cron.d/middlewared', extension='.txt'),
        MiddlewareClientMetric('cronjobs', [MiddlewareCommand('cronjob.query')]),
    ]

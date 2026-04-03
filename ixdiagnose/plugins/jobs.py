from ixdiagnose.config import conf
from ixdiagnose.utils.middleware import MiddlewareClient, get_admin_middleware_client

from .base import Plugin
from .metrics import PythonMetric

RAW_RESULT_PARAMS = [[], {'extra': {'raw_result': False}}]


def get_jobs(client: MiddlewareClient, context) -> dict:
    if conf.caller_has_full_admin:
        with get_admin_middleware_client() as admin_client:
            jobs = admin_client.call('core.get_jobs', *RAW_RESULT_PARAMS)
    else:
        jobs = client.call('core.get_jobs', *RAW_RESULT_PARAMS)
    return {'key': 'core_get_jobs', 'output': jobs}


class CoreGetJobs(Plugin):
    name = 'jobs'
    metrics = [
        PythonMetric('jobs', get_jobs),
    ]

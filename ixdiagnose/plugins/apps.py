import docker

from ixdiagnose.utils.command import Command
from ixdiagnose.utils.middleware import MiddlewareCommand

from .base import Plugin
from .metrics import CommandMetric, MiddlewareClientMetric, PythonMetric
from .prerequisites import ServiceRunningPrerequisite


def docker_container_inspect(middleware_client, context):
    try:
        client = docker.from_env()

        # Get all containers (including stopped ones)
        containers = client.containers.list(all=True)

        if not containers:
            return {'containers': [], 'error': None}

        containers_info = []
        for container in containers:
            # Get container attributes
            attrs = container.attrs
            state = attrs.get('State', {})

            health_data = state.get('Health', {})
            if health_data:
                health_info = {
                    'status': health_data.get('Status', None),
                    'failing_streak': health_data.get('FailingStreak', 0),
                    'log_count': len(health_data.get('Log', []))
                }
            else:
                health_info = None

            container_info = {
                'name': container.name,
                'id': container.short_id,
                'full_id': container.id,
                'status': container.status,
                'restart_count': attrs.get('RestartCount', 0),
                'started_at': state.get('StartedAt', ''),
                'finished_at': state.get('FinishedAt', ''),
                'exit_code': state.get('ExitCode', ''),
                'oom_killed': state.get('OOMKilled', False),
                'pid': state.get('Pid', ''),
                'running': state.get('Running', False),
                'paused': state.get('Paused', False),
                'restarting': state.get('Restarting', False),
                'dead': state.get('Dead', False),
                'error': state.get('Error', ''),
                'image': attrs.get('Config', {}).get('Image', ''),
                'created': attrs.get('Created', ''),
                'restart_policy': attrs.get('HostConfig', {}).get('RestartPolicy', {}),
                'health': health_info,
            }
            containers_info.append(container_info)

    except Exception as e:
        return {'containers': [], 'error': f'Unexpected error: {e}', 'total_containers': 0}
    else:
        return {
            'containers': containers_info,
            'total_containers': len(containers_info),
            'error': None,
        }


class Apps(Plugin):
    name = 'apps'
    metrics = [
        CommandMetric('docker_logs', [
            Command('journalctl -u docker | tail -n 1000', 'Docker logs', serializable=False),
        ]),
        CommandMetric('docker_processes', [
            Command(['docker', 'ps', '-a'], 'Docker processes (all containers)', serializable=False),
        ], prerequisites=[ServiceRunningPrerequisite('docker')]),
        CommandMetric('docker_images', [
            Command(['docker', 'images', '-a'], 'Docker images (all)', serializable=False),
        ], prerequisites=[ServiceRunningPrerequisite('docker')]),
        CommandMetric('docker_networks', [
            Command(['docker', 'network', 'ls'], 'Docker networks', serializable=False),
        ], prerequisites=[ServiceRunningPrerequisite('docker')]),
        CommandMetric('docker_volumes', [
            Command(['docker', 'volume', 'ls'], 'Docker volumes', serializable=False),
        ], prerequisites=[ServiceRunningPrerequisite('docker')]),
        CommandMetric('docker_stats', [
            Command(['docker', 'stats', '--no-stream'], 'Docker container resource usage', serializable=False),
        ], prerequisites=[ServiceRunningPrerequisite('docker')]),
        MiddlewareClientMetric('app_images', [MiddlewareCommand('app.image.query')]),
        MiddlewareClientMetric('app_dockerhub_limit', [MiddlewareCommand('app.image.dockerhub_rate_limit')]),
        MiddlewareClientMetric('apps', [MiddlewareCommand('app.query')]),
        MiddlewareClientMetric('apps_gpu_choices', [MiddlewareCommand('app.gpu_choices')]),
        MiddlewareClientMetric('apps_used_ports', [MiddlewareCommand('app.used_ports')]),
        MiddlewareClientMetric('catalog', [MiddlewareCommand('catalog.config')]),
        MiddlewareClientMetric('catalog_trains', [MiddlewareCommand('catalog.trains')]),
        MiddlewareClientMetric('docker_config', [MiddlewareCommand('docker.config')]),
        MiddlewareClientMetric('docker_status', [MiddlewareCommand('docker.status')]),
        PythonMetric(
            'docker_container_inspect', docker_container_inspect, 'Docker container detailed inspection',
            prerequisites=[ServiceRunningPrerequisite('docker')], serializable=True,
        ),
    ]

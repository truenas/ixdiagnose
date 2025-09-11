from .base import Artifact
from .items import Glob


class SysFSParameters(Artifact):
    base_dir = '/sys/module'
    name = 'sysfs_parameters'
    individual_item_max_size_limit = 10 * 1024
    items = [
        Glob('*/parameters/*', relative_to='/sys/module'),
    ]

from .base import Artifact
from .items import Glob


class SysClassHwmon(Artifact):
    base_dir = '/sys/class/hwmon'
    name = 'sys_hwmon'
    individual_item_max_size_limit = 64 * 1024
    items = [
        Glob('hwmon*/name', relative_to='/sys/class/hwmon'),
        Glob('hwmon*/temp*_input', relative_to='/sys/class/hwmon'),
        Glob('hwmon*/temp*_label', relative_to='/sys/class/hwmon'),
        Glob('hwmon*/temp*_max', relative_to='/sys/class/hwmon'),
        Glob('hwmon*/temp*_crit', relative_to='/sys/class/hwmon'),
        Glob('hwmon*/temp*_crit_alarm', relative_to='/sys/class/hwmon'),
    ]

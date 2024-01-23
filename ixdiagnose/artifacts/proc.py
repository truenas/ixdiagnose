from .base import Artifact
from .items import Directory


class ProcFS(Artifact):
    base_dir = '/proc'
    name = 'proc'
    individual_item_max_size_limit = 10 * 1024 * 1024
    items = [
        Directory('net/bonding'),
        Directory(name='spl', ignore_items=['/proc/spl/kstat/zfs/dbufs']),
    ]

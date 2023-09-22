from .base import Artifact
from .items import Directory, File, Pattern


class ProcFS(Artifact):
    base_dir = '/proc'
    name = 'proc'
    individual_item_max_size_limit = 10 * 1024 * 1024
    items = [Directory('spl')]

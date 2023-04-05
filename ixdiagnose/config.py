from typing import Optional


class Configuration:
    def __init__(self):
        self.compress: bool = False
        self.compressed_path: Optional[str] = None
        self.clean_debug_path: bool = False
        self.debug_path: Optional[str] = None
        self.timeout: int = 20


conf = Configuration()

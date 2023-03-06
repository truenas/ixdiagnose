from typing import Optional


class Configuration:
    def __init__(self):
        self.debug_path: Optional[str] = None
        self.timeout: int = 20


conf = Configuration()

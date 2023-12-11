from jsonschema import validate
from typing import Dict, List, Optional


class Configuration:

    SCHEMA = {
        'type': 'object',
        'properties': {
            'compress': {'type': 'boolean'},
            'compressed_path': {'type': ['string', 'null']},
            'clean_debug_path': {'type': 'boolean'},
            'debug_path': {'type': ['string', 'null']},
            'exclude_artifacts': {'type': 'array', 'items': {'type': 'string'}},
            'exclude_plugins': {'type': 'array', 'items': {'type': 'string'}},
            'extra': {'type': 'object'},
            'structured_data': {'type': 'boolean'},
            'timeout': {'type': 'integer'},
        },
    }

    def __init__(self):
        self.compress: bool = False
        self.compressed_path: Optional[str] = None
        self.clean_debug_path: bool = False
        self.debug_path: Optional[str] = None
        self.exclude_artifacts: List[str] = []
        self.exclude_plugins: List[str] = []
        self.extra: Dict[str, str] = {}
        self.structured_data: bool = False
        self.timeout: int = 20

    def apply(self, new_config: dict) -> None:
        validate(new_config, self.SCHEMA)
        self.__dict__.update(new_config)


conf = Configuration()

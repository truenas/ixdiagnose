from jsonschema import validate
from typing import Optional


class Configuration:

    SCHEMA = {
        'type': 'object',
        'properties': {
            'compress': {'type': 'boolean'},
            'compressed_path': {'type': ['string', 'null']},
            'clean_debug_path': {'type': 'boolean'},
            'debug_path': {'type': ['string', 'null']},
            'timeout': {'type': 'integer'},
        },
    }

    def __init__(self):
        self.compress: bool = False
        self.compressed_path: Optional[str] = None
        self.clean_debug_path: bool = False
        self.debug_path: Optional[str] = None
        self.timeout: int = 20

    def apply(self, new_config: dict) -> None:
        validate(new_config, self.SCHEMA)
        self.__dict__.update(new_config)


conf = Configuration()

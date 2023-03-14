from typing import Any, Dict


class Factory:
    def __init__(self):
        self._creators: Dict[str, Any] = {}

    def register(self, item: Any) -> None:
        self._creators[item.name] = item

    def get_items(self) -> Dict[str, Any]:
        return self._creators

from middlewared.client.ejson import dumps as middleware_dumps, loads # noqa
from middlewared.utils import get
from typing import Callable, Dict, List


def dumps(*args, **kwargs) -> str:
    kwargs.setdefault('indent', 4)
    return middleware_dumps(*args, **kwargs)


def remove_keys(keys: List[str]) -> Callable:
    def remove(output: Dict) -> Dict:
        for key in keys:
            if '.' in key:
                to_find, to_remove = key.rsplit('.', 1)
                sub_obj = get(output, to_find)
                if isinstance(sub_obj, dict):
                    sub_obj.pop(to_remove, None)
            else:
                output.pop(key, None)

        return output
    return remove

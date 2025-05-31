from typing import Callable, Iterable, TypeVar

from truenas_api_client.ejson import dumps as middleware_dumps, loads # noqa
from middlewared.utils import get


_T = TypeVar('_T', dict, list)


def dumps(*args, **kwargs) -> str:
    kwargs.setdefault('indent', 4)
    return middleware_dumps(*args, **kwargs)


def pop_key(output, to_find, to_remove):
    sub_obj = get(output, to_find)
    if isinstance(sub_obj, dict):
        sub_obj.pop(to_remove, None)


def remove_keys(keys: Iterable[str]) -> Callable[[_T], _T]:
    """Return a function that recursively removes the specified keys from its argument.

    :param keys: Keys to remove. Nested keys can be specified with dot notation, e.g. `outer.inner`.
    """
    def remove(output: _T) -> _T:
        if isinstance(output, dict):
            for key in keys:
                if '.' in key:
                    first_attr = get(output, key.split('.')[0])
                    if isinstance(first_attr, list):
                        for attr in first_attr:
                            to_find, to_remove = key.rsplit('.', 1)
                            to_find = to_find.split('.', 1)[1]
                            pop_key(attr, to_find, to_remove)
                    else:
                        to_find, to_remove = key.rsplit('.', 1)
                        pop_key(output, to_find, to_remove)
                else:
                    output.pop(key, None)
        else:
            for item in output:
                remove(item)

        return output
    return remove


def redact_str(value):
    if isinstance(value, str):
        # Replace with an arbitrary number of asterisks to conceal length.
        return '*' * 8
    return value


def redact_key(output, to_find, to_remove):
    sub_obj = get(output, to_find)
    if isinstance(sub_obj, dict):
        sub_obj[to_remove] = redact_str(sub_obj[to_remove])


def redact_keys(keys: Iterable[str]) -> Callable[[_T], _T]:
    """Return a function that recursively redacts the specified keys
    from its argument, i.e. replaces the values with '***'.

    :param keys: Keys to redact. Nested keys can be specified with dot notation, e.g. `outer.inner`.
    """
    def redact(output: _T) -> _T:
        if isinstance(output, dict):
            for key in keys:
                if '.' in key:
                    first_attr = get(output, key.split('.')[0])
                    if isinstance(first_attr, list):
                        for attr in first_attr:
                            to_find, to_remove = key.rsplit('.', 1)
                            to_find = to_find.split('.', 1)[1]
                            redact_key(attr, to_find, to_remove)
                    else:
                        to_find, to_remove = key.rsplit('.', 1)
                        redact_key(output, to_find, to_remove)
                else:
                    output[key] = redact_str(output[key])
        else:
            for item in output:
                redact(item)

        return output
    return redact

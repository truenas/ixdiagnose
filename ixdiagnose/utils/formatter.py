from collections import defaultdict
import functools
from typing import Callable, Iterable, MutableMapping, TypeVar, overload

from truenas_api_client.ejson import dumps as middleware_dumps, loads  # noqa
from middlewared.utils import get


_Iter = TypeVar('_Iter', dict, Iterable)
_T = TypeVar('_T')


REDACTED = '*' * 8
"""Replace with an arbitrary number of asterisks to conceal length."""


def dumps(*args, **kwargs) -> str:
    kwargs.setdefault('indent', 4)
    return middleware_dumps(*args, **kwargs)


def pop_key(output, to_find, to_remove):
    sub_obj = get(output, to_find)
    if isinstance(sub_obj, dict):
        sub_obj.pop(to_remove, None)


def remove_keys(keys: Iterable[str]) -> Callable[[_Iter], _Iter]:
    """Return a function that recursively removes the specified keys from its argument.

    :param keys: Keys to remove. Nested keys can be specified with dot notation, e.g. `outer.inner`.
    """
    def remove(output: _Iter) -> _Iter:
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


def _key_tree(keys: Iterable[str]) -> defaultdict[str, set[str]]:
    """Convert an iterable of dot-notation keys into a mapping of top-level keys to their sub-keys.

    Example:

        {'a', 'b.c', 'e.f', 'e.g.h'} -> {'a': set(), 'b': {'c'}, 'e': {'f', 'g.h'}}
    """
    result = defaultdict(set)
    for k in keys:
        if '.' in k:
            pk, ck = k.split('.', 1)
            result[pk].add(ck)
        else:
            result[k]  # initialize the set if not already initialized
    return result


@overload
def redact_keys(*, include: Iterable[str]) -> Callable[[_T], _T]: ...
@overload
def redact_keys(*, exclude: Iterable[str]) -> Callable[[_T], _T]: ...


def redact_keys(*, include: Iterable[str] | None = None, exclude: Iterable[str] | None = None) -> Callable[[_T], _T]:
    """Return a function that recursively redacts keys from its argument, i.e. replaces the values with '***'.

    Nested keys can be specified with dot notation, e.g. `outer.inner`. Specify either keys to include or keys to
    exclude, but not both.

    :param include: Redact all keys not provided.
    :param exclude: Redact all keys provided.
    :return: A function that takes a data structure and applies the specified redactions to it.
    """
    include_provided = bool(include)
    if include_provided is bool(exclude):
        raise ValueError('Either provide keys to include or exclude but not both')

    def redact(data: _T, keys: Iterable[str], *, include: bool) -> _T:
        if isinstance(data, MutableMapping):
            keys = _key_tree(keys)
            for key in data:
                if subkeys := keys.get(key):
                    redact(data[key], subkeys, include=include)
                elif (subkeys is None) is include:
                    # key not in keys to include, OR key is in keys to exclude
                    data[key] = REDACTED
        elif isinstance(data, Iterable):
            for item in data:
                redact(item, keys, include=include)
        return data

    return functools.partial(redact, keys=include if include_provided else exclude, include=include_provided)

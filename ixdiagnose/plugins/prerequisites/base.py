from typing import Dict, Optional


class CacheMeta(type):

    def __new__(cls, *args, **kwargs):
        klass = super().__new__(cls, *args, **kwargs)
        klass.cache = {}
        return klass


class Prerequisite(metaclass=CacheMeta):

    CACHE_RESULTS: Dict[str, bool] = {}

    def __init__(self, cache: bool = False):
        self.cache: bool = cache
        self.cache_key: Optional[str] = None

    def evaluate(self) -> bool:
        if self.is_cached():
            return self.CACHE_RESULTS[self.cache_key]

        result = self.evaluate_impl()
        if self.cache and self.cache_key:
            self.CACHE_RESULTS[self.cache_key] = result
        return result

    def __str__(self):
        raise NotImplementedError()

    def evaluate_impl(self) -> bool:
        raise NotImplementedError()

    def is_cached(self) -> bool:
        return self.cache_key in self.CACHE_RESULTS if self.cache and self.cache_key else False

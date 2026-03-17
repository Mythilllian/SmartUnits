from smartunits.collections import LongToObjectHashMap
from smartunits import *
from typing import Callable, Generic, TypeVar

A = TypeVar("A", bound=Unit)
B = TypeVar("B", bound=Unit)
Out = TypeVar("Out", bound=Unit)
class CombinatoryUnitCache(Generic[A, B, Out]):
    def __init__(self, constructor: Callable[[A, B], Out]) -> None:
        if not callable(constructor):
            raise ValueError("Cache unit constructor must be provided")

        self._cache: LongToObjectHashMap[Out] = LongToObjectHashMap[Out]()
        self._constructor: Callable[[A, B], Out] = constructor

    def combine(self, a: A, b: B) -> Out:
        key = (hash(a) << 32) | (hash(b) & 0xFFFFFFFF)
        
        existing = self._cache.get(key)
        if existing is not None:
            return existing
        
        new_unit = self._constructor(a, b)
        self._cache.put(key, new_unit)
        return new_unit
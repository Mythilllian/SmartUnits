from abc import abstractmethod
from typing import ClassVar, override

from .unary_function import UnaryFunction
from .unit import Unit


class CombinedUnit(Unit):
    __slots__ = (
        "_first",
        "_second",
        "_to_base_multiplier",
    )
    _first: Unit
    _second: Unit
    _to_base_multiplier: float
    _cache: ClassVar[dict[tuple[int, int], "CombinedUnit"]]

    def __init__(
        self,
        first: Unit,
        second: Unit,
        name: str | None = None,
        symbol: str | None = None,
        to_base_multiplier: float | None = None,
    ) -> None:
        self._first = first
        self._second = second

        derived = to_base_multiplier is None
        if derived:
            to_base_multiplier = self._combine_scales(first.base_scale(), second.base_scale())
        self._to_base_multiplier = to_base_multiplier

        if derived and first.is_base_unit() and second.is_base_unit():
            base_unit = self
        else:
            base_unit = type(self).combine(first.get_base_unit(), second.get_base_unit())

        super().__init__(
            base_unit,
            name if name is not None else self._default_name(first, second),
            symbol if symbol is not None else self._default_symbol(first, second),
        )

        if derived:
            key = (id(first), id(second))
            cached = self._cache.get(key)
            if cached is None or type(cached).__base__ is CombinedUnit:
                self._cache[key] = self

    @classmethod
    def combine(cls, first: Unit, second: Unit) -> "CombinedUnit":
        cached = cls._cache.get((id(first), id(second)))
        if isinstance(cached, cls):
            return cached
        return cls(first, second)

    @staticmethod
    @abstractmethod
    def _combine_scales(first: float, second: float) -> float:
        pass

    @staticmethod
    @abstractmethod
    def _default_name(first: Unit, second: Unit) -> str:
        pass

    @staticmethod
    @abstractmethod
    def _default_symbol(first: Unit, second: Unit) -> str:
        pass

    @override
    def convert_from(self, magnitude: float, other_unit: Unit) -> float:
        return self.from_base_units(other_unit.to_base_units(magnitude))

    @override
    def convert_to(self, magnitude: float, other_unit: Unit) -> float:
        return other_unit.from_base_units(self.to_base_units(magnitude))

    @override
    def conversion_from(self, other_unit: Unit) -> UnaryFunction:
        return UnaryFunction(lambda x: self.from_base_units(other_unit.to_base_units(x)))

    @override
    def conversion_to(self, other_unit: Unit) -> UnaryFunction:
        return UnaryFunction(lambda x: other_unit.from_base_units(self.to_base_units(x)))

    @override
    def from_base_units(self, value_in_base_units: float) -> float:
        return value_in_base_units / self._to_base_multiplier

    @override
    def to_base_units(self, value_in_native_units: float) -> float:
        return value_in_native_units * self._to_base_multiplier

    @override
    def conversion_from_base_units(self) -> UnaryFunction:
        return UnaryFunction(lambda x: self.from_base_units(x))

    @override
    def conversion_to_base_units(self) -> UnaryFunction:
        return UnaryFunction(lambda x: self.to_base_units(x))

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._name!r})"

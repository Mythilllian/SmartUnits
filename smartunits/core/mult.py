from dataclasses import dataclass
from typing import Any, override

from .combined import CombinedUnit
from .measure import Measure
from .unit import Unit


class MultUnit(CombinedUnit):
    __slots__ = ()
    _cache = {}

    @staticmethod
    @override
    def _combine_scales(first: float, second: float) -> float:
        return first * second

    @staticmethod
    @override
    def _default_name(first: Unit, second: Unit) -> str:
        return f"{first.name()} {second.name()}"

    @staticmethod
    @override
    def _default_symbol(first: Unit, second: Unit) -> str:
        return f"{first.symbol()}*{second.symbol()}"

    def unit_a(self) -> Unit:
        return self._first

    def unit_b(self) -> Unit:
        return self._second

    @override
    def of(self, magnitude: float) -> "Mult":
        return Mult.of(magnitude, self)

    @override
    def of_base_units(self, magnitude: float) -> "Mult":
        return Mult.of_base_units(magnitude, self)

    @override
    def per(self, other: Unit) -> Unit:
        if other is self._second:
            return self._first
        if other is self._first:
            return self._second
        return super().per(other)


@dataclass(frozen=True, slots=True, eq=False)
class Mult(Measure):
    _magnitude: float
    _base_unit_magnitude: float
    _unit: MultUnit

    @staticmethod
    def of(magnitude: float, unit: MultUnit) -> "Mult":
        return Mult(magnitude, unit.to_base_units(magnitude), unit)

    @staticmethod
    def of_base_units(base_unit_magnitude: float, unit: MultUnit) -> "Mult":
        return Mult(unit.from_base_units(base_unit_magnitude), base_unit_magnitude, unit)

    def unit_a(self) -> Unit:
        return self._unit.unit_a()

    def unit_b(self) -> Unit:
        return self._unit.unit_b()

    @override
    def __neg__(self) -> Measure:
        return self._unit.of(-self._magnitude)

    @override
    def __add__(self, other: Measure) -> Measure:
        return self._unit.of_base_units(self._base_unit_magnitude + other.base_unit_magnitude())

    @override
    def __sub__(self, other: Measure) -> Measure:
        return self._unit.of_base_units(self._base_unit_magnitude - other.base_unit_magnitude())

    @override
    def __mul__(self, other: Any) -> Measure:
        if isinstance(other, (int, float)):
            return self._unit.of(self._magnitude * other)

        return self._unit.mult(other.unit()).of_base_units(self._base_unit_magnitude * other.base_unit_magnitude())

    def __rmul__(self, other: Any) -> Measure:
        return self.__mul__(other)

    def __truediv__(self, other: Any) -> Measure:
        if isinstance(other, (int, float)):
            return self._unit.of(self._magnitude / other)

        base_result = self._base_unit_magnitude / other.base_unit_magnitude()
        other_base = other.unit().get_base_unit()

        if other_base is self._unit.unit_b().get_base_unit():
            return self._unit.unit_a().of_base_units(base_result)
        if other_base is self._unit.unit_a().get_base_unit():
            return self._unit.unit_b().of_base_units(base_result)

        return self._unit.per(other.unit()).of_base_units(base_result)

    def __str__(self) -> str:
        return f"{self._magnitude:.3e} {self._unit._symbol}"

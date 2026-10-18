from dataclasses import dataclass
from typing import Any, override

from .combined import CombinedUnit
from .measure import Measure
from .unit import Unit


class PerUnit(CombinedUnit):
    __slots__ = ()
    _cache = {}

    @staticmethod
    @override
    def _combine_scales(first: float, second: float) -> float:
        return first / second

    @staticmethod
    @override
    def _default_name(first: Unit, second: Unit) -> str:
        return f"{first.name()} per {second.name()}"

    @staticmethod
    @override
    def _default_symbol(first: Unit, second: Unit) -> str:
        return f"{first.symbol()}/{second.symbol()}"

    def numerator(self) -> Unit:
        return self._first

    def denominator(self) -> Unit:
        return self._second

    def reciprocal(self) -> "PerUnit":
        return PerUnit.combine(self._second, self._first)

    @override
    def of(self, magnitude: float) -> "Per":
        return Per.of(magnitude, self)

    @override
    def of_base_units(self, magnitude: float) -> "Per":
        return Per.of_base_units(magnitude, self)

    @override
    def mult(self, other: Unit) -> Unit:
        if other is self._second:
            return self._first
        return super().mult(other)


@dataclass(frozen=True, slots=True, eq=False)
class Per(Measure):
    _magnitude: float
    _base_unit_magnitude: float
    _unit: PerUnit

    @staticmethod
    def of(magnitude: float, unit: PerUnit) -> "Per":
        return Per(magnitude, unit.to_base_units(magnitude), unit)

    @staticmethod
    def of_base_units(base_unit_magnitude: float, unit: PerUnit) -> "Per":
        return Per(unit.from_base_units(base_unit_magnitude), base_unit_magnitude, unit)

    def numerator(self) -> Unit:
        return self._unit.numerator()

    def denominator(self) -> Unit:
        return self._unit.denominator()

    def times_divisor(self, divisor: Measure) -> Measure:
        return self._unit.numerator().of_base_units(self._base_unit_magnitude * divisor.base_unit_magnitude())

    def reciprocal(self) -> Measure:
        return self._unit.reciprocal().of_base_units(1 / self._base_unit_magnitude)

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

        if other.unit().get_base_unit() is self._unit.denominator().get_base_unit():
            return self.times_divisor(other)

        return self._unit.mult(other.unit()).of_base_units(self._base_unit_magnitude * other.base_unit_magnitude())

    def __rmul__(self, other: Any) -> Measure:
        return self.__mul__(other)

    def __truediv__(self, other: Any) -> Measure:
        if isinstance(other, (int, float)):
            return self._unit.of(self._magnitude / other)

        return self._unit.per(other.unit()).of_base_units(self._base_unit_magnitude / other.base_unit_magnitude())

    def __str__(self) -> str:
        return f"{self._magnitude:.3e} {self._unit._symbol}"

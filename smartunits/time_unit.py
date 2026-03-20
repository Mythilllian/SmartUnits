from typing import override
from smartunits import Unit, UnaryFunction#, PerUnit, TimeUnit, LinearVelocityUnit, ForceUnit, TorqueUnit
from smartunits.measures import Time

class TimeUnit(Unit):
    __slots__ = (
        "_from_conversion_factor",
    )
    _base_unit: "TimeUnit"
    _to_conversion_factor: float

    def __init__(
        self,
        base_unit: "TimeUnit",
        base_unit_equivalent: float,
        name: str,
        symbol: str,
    ) -> None:
        super().__init__(base_unit, name, symbol)
        self._from_conversion_factor = base_unit_equivalent

    @override
    def get_base_unit(self) -> "TimeUnit":
        return self._base_unit

    @override
    def of(self, magnitude: float) -> Time:
        return Time(magnitude, magnitude / self._from_conversion_factor, self)

    @override
    def of_base_units(self, magnitude: float) -> Time:
        return Time(magnitude, magnitude, self._base_unit)

    @override
    def zero(self) -> Time:
        return self._zero
    
    @override
    def one(self) -> Time:
        return self._one

    @override
    def per(self, other: Unit) -> Unit:
        t = type(other)
        return t # TEMP LINE TODO DELETE
        #return PerUnit[TimeUnit, t].combine(self, other)

    @override
    def convert_from(self, magnitude: float, other_unit: "TimeUnit") -> float:
        return magnitude / other_unit._from_conversion_factor * self._from_conversion_factor
    
    @override
    def convert_to(self, magnitude: float, other_unit: "TimeUnit") -> float:
        return magnitude / self._from_conversion_factor * other_unit._from_conversion_factor
    
    @override
    def conversion_from(self, other_unit: "TimeUnit") -> UnaryFunction:
        return UnaryFunction(lambda x: x / other_unit._from_conversion_factor * self._from_conversion_factor)

    @override
    def conversion_to(self, other_unit: "TimeUnit") -> UnaryFunction:
        return UnaryFunction(lambda x: x / self._from_conversion_factor * other_unit._from_conversion_factor)
    
    @override
    def from_base_units(self, value_in_base_units: float) -> float:
        return value_in_base_units * self._from_conversion_factor

    @override
    def to_base_units(self, value_in_native_units: float) -> float:
        return value_in_native_units / self._from_conversion_factor

    @override
    def conversion_from_base_units(self) -> UnaryFunction:
        return UnaryFunction(lambda x: x * self._from_conversion_factor)

    @override
    def conversion_to_base_units(self) -> UnaryFunction:
        return UnaryFunction(lambda x: x / self._from_conversion_factor)
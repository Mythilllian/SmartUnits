from typing import override
from smartunits import Unit, UnaryFunction, PerUnit, TimeUnit, CurrentUnit, VelocityUnit, PowerUnit
from smartunits.measure import Measure
from smartunits.measures import Voltage

class VoltageUnit(Unit):
    __slots__ = (
        "_from_conversion_factor",
    )
    _base_unit: "VoltageUnit"
    _to_conversion_factor: float

    def __init__(
        self,
        base_unit: "VoltageUnit",
        base_unit_equivalent: float,
        name: str,
        symbol: str,
    ) -> None:
        super().__init__(base_unit, name, symbol)
        self._from_conversion_factor = base_unit_equivalent

    @override
    def get_base_unit(self) -> "VoltageUnit":
        return self._base_unit

    @override
    def of(self, magnitude: float) -> Voltage:
        return Voltage(magnitude, magnitude / self._from_conversion_factor, self)

    @override
    def of_base_units(self, magnitude: float) -> Voltage:
        return Voltage(magnitude, magnitude, self._base_unit)

    @override
    def zero(self) -> Voltage:
        return self._zero
    
    @override
    def one(self) -> Voltage:
        return self._one

    @override
    def per(self, other: Unit) -> Unit:
        t = type(other)
        if t is TimeUnit:
            return VelocityUnit.combine(self, other)
        if t is CurrentUnit:
            return PowerUnit.combine(self, other)
        return PerUnit[VoltageUnit, t].combine(self, other)

    @override
    def convert_from(self, magnitude: float, other_unit: "VoltageUnit") -> float:
        return magnitude / other_unit._from_conversion_factor * self._from_conversion_factor
    
    @override
    def convert_to(self, magnitude: float, other_unit: "VoltageUnit") -> float:
        return magnitude / self._from_conversion_factor * other_unit._from_conversion_factor
    
    @override
    def conversion_from(self, other_unit: "VoltageUnit") -> UnaryFunction:
        return UnaryFunction(lambda x: x / other_unit._from_conversion_factor * self._from_conversion_factor)

    @override
    def conversion_to(self, other_unit: "VoltageUnit") -> UnaryFunction:
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

    def __mul__(self, other: CurrentUnit) -> PowerUnit:
        return PowerUnit.combine(self, other)
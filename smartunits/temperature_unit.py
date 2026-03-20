from typing import override
from smartunits import Unit, UnaryFunction, Measure, PerUnit, TimeUnit, VelocityUnit
from smartunits.measures import Temperature

class TemperatureUnit(Unit):
    __slots__ = (
        "_base_unit",
        "_to_base_converter",
        "_from_base_converter",
        "_name",
        "_symbol",
        "_zero",
        "_one",
        "_to_conversion_factor",
        "_from_conversion_factor",
    )
    _base_unit: "TemperatureUnit"
    _to_base_converter: UnaryFunction
    _from_base_converter: UnaryFunction
    _name: str
    _symbol: str
    _zero: Temperature
    _one: Temperature

    def __init__(
        self,
        base_unit: "TemperatureUnit",
        to_base_converter: UnaryFunction,
        from_base_converter: UnaryFunction,
        name: str,
        symbol: str,
    ) -> None:
        super().__init__(base_unit, to_base_converter, from_base_converter, name, symbol)

    @override
    def get_base_unit(self) -> "TemperatureUnit":
        return self._base_unit

    @override
    def of(self, magnitude: float) -> Temperature:
        return Temperature(magnitude, magnitude * self._to_conversion_factor, self)

    @override
    def of_base_units(self, magnitude: float) -> Temperature:
        return Temperature(magnitude, magnitude, self._base_unit)

    @override
    def zero(self) -> Temperature:
        return self._zero
    
    @override
    def one(self) -> Temperature:
        return self._one

    @override
    def per(self, other: Unit) -> Unit:
        t = type(other)
        if t is TimeUnit:
            return VelocityUnit.combine(self, other)
        return PerUnit[TemperatureUnit, t].combine(self, other)
from typing import override
from smartunits import Unit, UnaryFunction, Measure, PerUnit, TimeUnit, AngularVelocityUnit
from smartunits.measures import Angle

class AngleUnit(Unit):
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
    _base_unit: "AngleUnit"
    _to_base_converter: UnaryFunction
    _from_base_converter: UnaryFunction
    _name: str
    _symbol: str
    _zero: Angle
    _one: Angle
    _to_conversion_factor: float
    _from_conversion_factor: float

    def __init__(
        self,
        base_unit: "AngleUnit",
        base_unit_equivalent: float,
        name: str,
        symbol: str,
    ) -> None:
        to_base_converter, from_base_converter = UnaryFunction.pair_from_multiplier(base_unit_equivalent)

        super().__init__(base_unit, to_base_converter, from_base_converter, name, symbol)
        self._from_conversion_factor = base_unit_equivalent
        self._to_conversion_factor = 1 / base_unit_equivalent

    @override
    def get_base_unit(self) -> "AngleUnit":
        return self._base_unit

    @override
    def of(self, magnitude: float) -> Angle:
        return Angle(magnitude, magnitude * self._to_conversion_factor, self)

    @override
    def of_base_units(self, magnitude: float) -> Angle:
        return Angle(magnitude, magnitude, self._base_unit)

    @override
    def zero(self) -> Angle:
        return self._zero
    
    @override
    def one(self) -> Angle:
        return self._one

    @override
    def per(self, other: Unit) -> Unit:
        t = type(other)
        if t is TimeUnit:
            return AngularVelocityUnit.combine(self, other)
        return PerUnit[AngleUnit, t].combine(self, other)

    @override
    def convert_from(self, magnitude: float, other_unit: "AngleUnit") -> float:
        return magnitude * other_unit._to_conversion_factor * self._from_conversion_factor
    
    @override
    def convert_to(self, magnitude: float, other_unit: "AngleUnit") -> float:
        return magnitude * self._to_conversion_factor * other_unit._from_conversion_factor
    
    @override
    def conversion_from(self, other_unit: "AngleUnit") -> UnaryFunction:
        return UnaryFunction(lambda x: x * other_unit._to_conversion_factor * self._from_conversion_factor)

    @override
    def conversion_to(self, other_unit: "AngleUnit") -> UnaryFunction:
        return UnaryFunction(lambda x: x * self._to_conversion_factor * other_unit._from_conversion_factor)
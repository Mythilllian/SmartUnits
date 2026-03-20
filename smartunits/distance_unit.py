from typing import override, TYPE_CHECKING
from smartunits import Unit, UnaryFunction#, PerUnit, TimeUnit, LinearVelocityUnit, ForceUnit, TorqueUnit
from smartunits.measures import Distance
if TYPE_CHECKING:
    from smartunits import TimeUnit#, ForceUnit, TorqueUnit

class DistanceUnit(Unit):
    __slots__ = (
        "_to_conversion_factor",
    )
    _base_unit: "DistanceUnit"
    _to_conversion_factor: float

    def __init__(
        self,
        base_unit: "DistanceUnit",
        base_unit_equivalent: float,
        name: str,
        symbol: str,
    ) -> None:
        super().__init__(base_unit, name, symbol)
        self._to_conversion_factor = base_unit_equivalent

    @override
    def get_base_unit(self) -> "DistanceUnit":
        return self._base_unit

    @override
    def of(self, magnitude: float) -> Distance:
        return Distance(magnitude, magnitude * self._to_conversion_factor, self)

    @override
    def of_base_units(self, magnitude: float) -> Distance:
        return Distance(magnitude / self._to_conversion_factor, magnitude, self)

    @override
    def zero(self) -> Distance:
        return self._zero
    
    @override
    def one(self) -> Distance:
        return self._one

    @override
    def per(self, other: Unit) -> Unit:
        t = type(other)
        if t is TimeUnit:
            from smartunits import LinearVelocityUnit
            return LinearVelocityUnit.combine(self, other)

        from smartunits import PerUnit
        return PerUnit[DistanceUnit, t].combine(self, other)

    @override
    def convert_from(self, other_unit: "DistanceUnit", magnitude: float = 1) -> float:
        return magnitude * other_unit._to_conversion_factor / self._to_conversion_factor
    
    @override
    def convert_to(self, other_unit: "DistanceUnit", magnitude: float = 1) -> float:
        return magnitude * self._to_conversion_factor / other_unit._to_conversion_factor
    
    @override
    def conversion_from(self, other_unit: "DistanceUnit") -> UnaryFunction:
        return UnaryFunction(lambda x: x * other_unit._to_conversion_factor / self._to_conversion_factor)

    @override
    def conversion_to(self, other_unit: "DistanceUnit") -> UnaryFunction:
        return UnaryFunction(lambda x: x * self._to_conversion_factor / other_unit._to_conversion_factor)
    
    @override
    def from_base_units(self, value_in_base_units: float) -> float:
        return value_in_base_units / self._to_conversion_factor

    @override
    def to_base_units(self, value_in_native_units: float) -> float:
        return value_in_native_units * self._to_conversion_factor

    @override
    def conversion_from_base_units(self) -> UnaryFunction:
        return UnaryFunction(lambda x: x / self._to_conversion_factor)

    @override
    def conversion_to_base_units(self) -> UnaryFunction:
        return UnaryFunction(lambda x: x * self._to_conversion_factor)
    
    # def __mul__(self, other: ForceUnit) -> TorqueUnit:
    #     if type(other) is ForceUnit:
    #         return TorqueUnit.combine(self, other)
    #     return PerUnit.combine(self, other)
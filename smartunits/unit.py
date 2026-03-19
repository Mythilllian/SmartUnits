from smartunits import Measure, UnaryFunction, TimeUnit

from abc import ABC, abstractmethod
from typing import Any


class Unit(ABC):
    __slots__ = (
        "_base_unit",
        "_to_base_converter",
        "_from_base_converter",
        "_name",
        "_symbol",
        "_zero",
        "_one",
    )
    _base_unit: "Unit"
    _to_base_converter: UnaryFunction
    _from_base_converter: UnaryFunction
    _name: str
    _symbol: str
    _zero: "Measure[Any]"
    _one: "Measure[Any]"

    def __init__(
        self,
        base_unit: "Unit",
        to_base_converter: UnaryFunction,
        from_base_converter: UnaryFunction,
        name: str,
        symbol: str,
    ) -> None:
        self._base_unit: "Unit" = base_unit
        self._to_base_converter: UnaryFunction = to_base_converter
        self._from_base_converter: UnaryFunction = from_base_converter
        self._name: str = name
        self._symbol: str = symbol

        self._zero: "Measure[Any]" = self.of(0)
        self._one: "Measure[Any]" = self.of(1)

    def from_base_multiplier(
        self, base_unit: "Unit", base_unit_equivalent: float, name: str, symbol: str
    ) -> "Unit":
        return type(self)(
            base_unit,
            UnaryFunction(lambda x: x * base_unit_equivalent),
            UnaryFunction(lambda x: x / base_unit_equivalent),
            name,
            symbol,
        )

    @abstractmethod
    def of(self, magnitude: float) -> "Measure[Any]":
        pass

    def of_units(self, magnitude: float) -> "Measure[Any]":
        return self.of(self.from_base_units(magnitude))

    @abstractmethod
    def of_base_units(self, magnitude: float) -> "Measure[Any]":
        pass

    def zero(self) -> "Measure[Any]":
        return self._zero

    def one(self) -> "Measure[Any]":
        return self._one

    @abstractmethod
    def per(self, time: TimeUnit) -> "Unit":
        pass

    def convert_from(self, magnitude: float, other_unit: "Unit") -> float:
        return other_unit._to_base_converter(self._from_base_converter(magnitude))
    
    def convert_to(self, magnitude: float, other_unit: "Unit") -> float:
        return self._to_base_converter(other_unit._from_base_converter(magnitude))

    def conversion_from(self, other_unit: "Unit") -> UnaryFunction:
        return UnaryFunction(lambda x: other_unit._to_base_converter(self._from_base_converter(x)))

    def conversion_to(self, other_unit: "Unit") -> UnaryFunction:
        return UnaryFunction(lambda x: self._to_base_converter(other_unit._from_base_converter(x)))

    def get_base_unit(self) -> "Unit":
        return self._base_unit

    def is_base_unit(self) -> bool:
        return self == self._base_unit

    def from_base_units(self, value_in_base_units: float) -> float:
        return self._from_base_converter(value_in_base_units)

    def to_base_units(self, value_in_native_units: float) -> float:
        return self._to_base_converter(value_in_native_units)

    def get_converter_to_base(self) -> UnaryFunction:
        return self._to_base_converter

    def get_converter_from_base(self) -> UnaryFunction:
        return self._from_base_converter

    def equivalent(self, other: "Unit") -> bool:
        if type(self) is not type(other):
            return False

        arbitrary: float = 16_777.214  # test value, should be essentially random

        return (
            abs(
                self._from_base_converter(arbitrary)
                - other._from_base_converter(arbitrary)
            )
            <= Measure.EQUIVALENCE_THRESHOLD
            and abs(
                self._to_base_converter(arbitrary) - other._to_base_converter(arbitrary)
            )
            <= Measure.EQUIVALENCE_THRESHOLD
        )

    def __eq__(self, o: object) -> bool:
        return self is o or (
            isinstance(o, Unit)
            and self._name == o._name
            and self._symbol == o._symbol
            and self.equivalent(o)
        )

    def __hash__(self) -> int:
        return hash(
            (
                self._to_base_converter,
                self._from_base_converter,
                self._name,
                self._symbol,
            )
        )

    def name(self) -> str:
        return self._name

    def symbol(self) -> str:
        return self._symbol

    def __str__(self) -> str:
        return self._name

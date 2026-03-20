from smartunits import UnaryFunction
# circular dependency issues
# from smartunits import Measure, TimeUnit

from abc import ABC, abstractmethod
from typing import Any

class Unit(ABC):

    __slots__ = (
        "_base_unit",
        "_name",
        "_symbol",
    )
    _base_unit: "Unit"
    _name: str
    _symbol: str

    def __init__(
        self,
        base_unit: "Unit",
        name: str,
        symbol: str,
    ) -> None:
        self._base_unit: "Unit" = base_unit
        self._name: str = name
        self._symbol: str = symbol

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

    def of_base_units(self, magnitude: float) -> "Measure[Any]":
        return self.of(self.from_base_units(magnitude))        

    def zero(self) -> "Measure[Any]":
        return self._zero

    def one(self) -> "Measure[Any]":
        return self._one

    @abstractmethod
    def per(self, time: TimeUnit) -> "Unit":
        pass

    @abstractmethod
    def convert_from(self, magnitude: float, other_unit: "Unit") -> float:
        pass
    
    @abstractmethod
    def convert_to(self, magnitude: float, other_unit: "Unit") -> float:
        pass

    @abstractmethod
    def conversion_from(self, other_unit: "Unit") -> UnaryFunction:
        pass

    @abstractmethod
    def conversion_to(self, other_unit: "Unit") -> UnaryFunction:
        pass

    def get_base_unit(self) -> "Unit":
        return self._base_unit

    def is_base_unit(self) -> bool:
        return self == self._base_unit

    @abstractmethod
    def from_base_units(self, value_in_base_units: float) -> float:
        pass

    @abstractmethod
    def to_base_units(self, value_in_native_units: float) -> float:
        pass

    @abstractmethod
    def conversion_from_base_units(self) -> UnaryFunction:
        pass

    @abstractmethod
    def conversion_to_base_units(self) -> UnaryFunction:
        pass

    def equivalent(self, other: "Unit") -> bool:
        from smartunits import Measure # temporary, TODO CHANGE LATER
        if type(self) is not type(other):
            return False

        arbitrary: float = 16_777.214  # test value, should be essentially random

        return (
            abs(
                self.from_base_units(arbitrary)
                - other.from_base_units(arbitrary)
            )
            <= Measure.EQUIVALENCE_THRESHOLD
            and abs(
                self.to_base_units(arbitrary) 
                - other.to_base_units(arbitrary)
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
                self._name,
                self._symbol,
                self._base_unit,
                self._one
            )
        )

    def name(self) -> str:
        return self._name

    def symbol(self) -> str:
        return self._symbol

    def __str__(self) -> str:
        return self._name

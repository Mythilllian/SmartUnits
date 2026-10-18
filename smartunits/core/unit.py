from .unary_function import UnaryFunction
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .measure import Measure

import math
from abc import ABC, abstractmethod
from typing import Any

EQUIVALENCE_THRESHOLD: float = 1e-12


def is_close(a: float, b: float, threshold: float = EQUIVALENCE_THRESHOLD) -> bool:
    return math.isclose(a, b, rel_tol=threshold, abs_tol=threshold)


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
        self._base_unit: "Unit" = base_unit if base_unit is not None else self
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
    def of(self, magnitude: float) -> "Measure":
        pass

    def of_base_units(self, magnitude: float) -> "Measure":
        return self.of(self.from_base_units(magnitude))        

    def zero(self) -> "Measure":
        return self._zero

    def one(self) -> "Measure":
        return self._one

    def per(self, other: "Unit") -> "Unit":
        from .per import PerUnit
        return PerUnit.combine(self, other)

    def mult(self, other: "Unit") -> "Unit":
        from .mult import MultUnit
        return MultUnit.combine(self, other)

    def __mul__(self, other: "Unit") -> "Unit":
        return self.mult(other)

    def __truediv__(self, other: "Unit") -> "Unit":
        return self.per(other)

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

    def base_scale(self) -> float:
        return self.to_base_units(1) - self.to_base_units(0)

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

    def equivalent(self, other: "Unit", equivalence_threshold: float = EQUIVALENCE_THRESHOLD) -> bool:
        if type(self) is not type(other):
            return False

        arbitrary: float = 16_777.214  # test value, should be essentially random

        return (
            is_close(
                self.from_base_units(arbitrary),
                other.from_base_units(arbitrary),
                equivalence_threshold,
            )
            and is_close(
                self.to_base_units(arbitrary),
                other.to_base_units(arbitrary),
                equivalence_threshold,
            )
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
            )
        )

    def name(self) -> str:
        return self._name

    def symbol(self) -> str:
        return self._symbol

    def __str__(self) -> str:
        return self._name

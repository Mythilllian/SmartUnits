from . import Measure, MutableMeasure, TimeUnit

from abc import ABC, abstractmethod
from typing import Any, Callable

class Unit(ABC):
    _to_base_converter: Callable[[float], float]
    _from_base_converter: Callable[[float], float]

    _base_unit: "Unit"

    _name: str
    _symbol: str

    _zero: Measure[Any]
    _one: Measure[Any]

    def __init__(self, base_unit: "Unit", to_base_converter: Callable[[float], float], from_base_converter: Callable[[float], float], name: str, symbol: str) -> None:
        self._base_unit = base_unit
        self._to_base_converter = to_base_converter
        self._from_base_converter = from_base_converter
        self._name = name
        self._symbol = symbol
        
        self._zero = self.of(0)
        self._one = self.of(1)
    
    def from_base_multiplier(self, base_unit: "Unit", base_unit_equivalent: float, name: str, symbol: str) -> "Unit":
        return Unit(base_unit, lambda x: x * base_unit_equivalent, lambda x: x / base_unit_equivalent, name, symbol)
    
    @abstractmethod
    def of(self, magnitude: float) -> "Measure[Any]":
        pass

    @abstractmethod
    def of_base_units(self, magnitude: float) -> "Measure[Any]":
        pass

    def mutable(self, initial_magnitude: float) -> "MutableMeasure[Any, Any, Any]":
        pass

    def zero(self) -> "Measure[Any]":
        return self._zero

    def one(self) -> "Measure[Any]":
        return self._one
    
    @abstractmethod
    def per(self, time: TimeUnit) -> "Unit":
        pass

    def get_base_unit(self) -> Unit:
        return self._base_unit
    
    def is_base_unit(self) -> bool:
        return self == self._base_unit
    
    def from_base_units(self, value_in_base_units: float) -> float:
        return self._from_base_converter(value_in_base_units)

    def to_base_units(self, value_in_native_units: float):
        return self._to_base_converter(value_in_native_units)

    def get_converter_to_base(self) -> Callable[[float], float]:
        return self._to_base_converter

    def get_converter_from_base(self) -> Callable[[float], float]:
        return self._from_base_converter
    
    def equivalent(self, other: "Unit") -> bool:
        if(type(self) != type(other)):
            return False

        arbitrary: float = 16_777.214 # test value, should be essentially random

        return abs(self._from_base_converter(arbitrary) - other._from_base_converter(arbitrary)) <= Measure.EQUIVALENCE_THRESHOLD and abs(self._to_base_converter(arbitrary) - other._to_base_converter(arbitrary)) <= Measure.EQUIVALENCE_THRESHOLD

    def __eq__(self, o: object) -> bool:
        return self is o or (isinstance(o, Unit) and self._name == o._name and self._symbol == o._symbol and self.equivalent(o))
    
    def __hash__(self) -> int:
        return hash((self._to_base_converter, self._from_base_converter, self._name, self._symbol))
    
    def name(self) -> str:
        return self._name
    
    def symbol(self) -> str:
        return self._symbol
    
    def __str__(self) -> str:
        return self.name()
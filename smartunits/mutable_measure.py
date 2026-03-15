from smartunits import *
from smartunits.measure import Measure
from smartunits.measures import Dimensionless

from typing import Any, TypeVar, Generic, override
from abc import ABC, abstractmethod


U = TypeVar('U', bound=Unit)
Base = TypeVar('Base', bound=Measure[U])
MutSelf = TypeVar('MutSelf', bound='MutableMeasure[U, Base, Any]')
class MutableMeasure(Measure[U], ABC, Generic[U, Base, MutSelf]):
    def mut_replace(self, magnitude: float, new_unit: U) -> MutSelf:
        self._magnitude = magnitude
        self._unit = new_unit
        return self

    def mut_replace_from(self, other: Base) -> MutSelf:
        return self.mut_replace(other.magnitude(), other.unit())

    @override
    @abstractmethod
    def copy(self) -> Base:
        pass
        
    def mut_set_magnitude(self, magnitude: float) -> MutSelf:
        return self.mut_replace(magnitude, self.unit())
    
    def mut_set_base_unit_magnitude(self, base_unit_magnitude: float) -> MutSelf:
        return self.mut_replace(self.unit().from_base_units(base_unit_magnitude), self.unit())
    
    def mut_plus(self, other: Measure[U]) -> MutSelf:
        return self.mut_set_magnitude(self.magnitude() + self.unit().from_base_units(other.base_unit_magnitude()))
    
    def mut_acc(self, other: Measure[U]) -> MutSelf:
        return self.mut_plus(other)
    
    def mut_minus(self, other: Measure[U]) -> MutSelf:
        return self.mut_set_magnitude(self.magnitude() - self.unit().from_base_units(other.base_unit_magnitude()))
    
    def mut_times_scalar(self, multiplier: float) -> MutSelf:
        return self.mut_set_magnitude(self.magnitude() * multiplier)
    
    def mut_times_dimensionless(self, multiplier: Dimensionless) -> MutSelf:
        return self.mut_set_magnitude(self.magnitude() * multiplier.base_unit_magnitude())
    
    def mut_divide_by_scalar(self, divisor: float) -> MutSelf:
        return self.mut_set_magnitude(self.magnitude() / divisor)
    
    def mut_divide_by_dimensionless(self, divisor: Dimensionless) -> MutSelf:
        return self.mut_set_magnitude(self.magnitude() / divisor.base_unit_magnitude())

    def __add__(self, other: Measure[U]) -> MutSelf:
        return self.mut_plus(other)
    
    def __sub__(self, other: Measure[U]) -> Measure[U]:
        return super().__sub__(other)
    
    def __mul__(self, other: Any) -> Measure[U]:
        if(isinstance(other, (int, float))):
            return self.mut_times_scalar(other)
        elif(isinstance(other, Dimensionless)):
            return self.mut_times_dimensionless(other)
        else:
            return super().__mul__(other)
        
    def __truediv__(self, other: Any) -> Measure[U]:
        if(isinstance(other, (int, float))):
            return self.mut_divide_by_scalar(other)
        elif(isinstance(other, Dimensionless)):
            return self.mut_divide_by_dimensionless(other)
        else:
            return super().__truediv__(other)
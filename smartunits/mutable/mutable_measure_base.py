from abc import ABC
from typing import Any, TypeVar, Generic, override
from smartunits import Measure, MutableMeasure, Unit

U = TypeVar('U', bound=Unit)
Base = TypeVar('Base', bound=Measure[U])
MutSelf = TypeVar('MutSelf', bound=MutableMeasure[U, Base, Any])
class MutableMeasureBase(Generic[U, Base, MutSelf], Measure[U], MutableMeasure[U, Base, MutSelf], ABC):
  def __init__(self, magnitude: float, base_unit_magnitude: float, unit: U) -> None:
    self._magnitude = magnitude
    self._base_unit_magnitude = base_unit_magnitude
    self._unit = unit

  @override
  def magnitude(self) -> float:
    return self._magnitude

  @override
  def base_unit_magnitude(self) -> float:
    return self._base_unit_magnitude
  
  @override
  def unit(self) -> U:
    return self._unit
  
  @override
  def __str__(self) -> str:
    return super().to_short_string()
  
  @override
  def __eq__(self, o: object) -> bool:
    return self is o or isinstance(o, Measure) and self.is_equivalent(o)
  
  @override
  def __hash__(self) -> int:
    return hash((self._magnitude, self._base_unit_magnitude, self._unit))
  
  @override
  def mut_replace(self, magnitude: float, new_unit: U) -> MutSelf:
    self._magnitude = magnitude
    self._base_unit_magnitude = new_unit.to_base_units(magnitude)
    self._unit = new_unit
    return self
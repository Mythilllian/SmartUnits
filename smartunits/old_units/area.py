from .unit import Unit, UnitValue

__all__ = ["AreaUnit", "AreaValue", "square_meters", "square_feet", "square_inches", "square_miles", "square_kilometers", "hectares", "acres"]

class AreaUnit(Unit):
    TYPE = "area"

    def __init__(self, base_value: float = 1.0, name: str = "square meters", abbreviation: str = "m^2") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

class AreaValue(UnitValue):
    unit: AreaUnit

    def __init__(self, magnitude: float, unit: AreaUnit = AreaUnit()) -> None:
        super().__init__(magnitude, unit)

square_meters = AreaUnit(base_value=1.0, name="square meters", abbreviation="m^2")
square_feet = AreaUnit(base_value=0.09290304, name="square feet", abbreviation="ft^2")
square_inches = AreaUnit(base_value=0.00064516, name="square inches", abbreviation="in^2")
square_miles = AreaUnit(base_value=2589988.110336, name="square miles", abbreviation="mi^2")
square_kilometers = AreaUnit(base_value=1000000.0, name="square kilometers", abbreviation="km^2")
hectares = AreaUnit(base_value=10000.0, name="hectares", abbreviation="ha")
acres = AreaUnit(base_value=4046.8564224, name="acres", abbreviation="ac")
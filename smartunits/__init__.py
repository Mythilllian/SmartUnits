from importlib import import_module
from typing import TYPE_CHECKING

from .measure import Measure
from .unit import Unit
from .unary_function import UnaryFunction

if TYPE_CHECKING:
    from .measure import Measure
    from .unit import Unit
    from .unary_function import UnaryFunction
    from .measures.absorbed_dose import AbsorbedDose
    from .measures.acceleration import Acceleration
    from .measures.angle import Angle
    from .measures.angular_acceleration import AngularAcceleration
    from .measures.angular_momentum import AngularMomentum
    from .measures.angular_velocity import AngularVelocity
    from .measures.area import Area
    from .measures.capacitance import Capacitance
    from .measures.charge import Charge
    from .measures.compound import Compound
    from .measures.concentration import Concentration
    from .measures.conductance import Conductance
    from .measures.current import Current
    from .measures.data import Data
    from .measures.data_transfer import DataTransfer
    from .measures.density import Density
    from .measures.dimensionless import Dimensionless
    from .measures.distance import Distance
    from .measures.energy import Energy
    from .measures.equivalent_dose import EquivalentDose
    from .measures.force import Force
    from .measures.frequency import Frequency
    from .measures.illuminance import Illuminance
    from .measures.inductance import Inductance
    from .measures.linear_acceleration import LinearAcceleration
    from .measures.linear_momentum import LinearMomentum
    from .measures.linear_velocity import LinearVelocity
    from .measures.luminous_flux import LuminousFlux
    from .measures.luminous_intensity import LuminousIntensity
    from .measures.magnetic_flux import MagneticFlux
    from .measures.magnetic_strength import MagneticStrength
    from .measures.mass import Mass
    from .measures.moment_of_inertia import MomentOfInertia
    from .measures.mult import Mult
    from .measures.per import Per
    from .measures.power import Power
    from .measures.pressure import Pressure
    from .measures.radioactivity import Radioactivity
    from .measures.resistance import Resistance
    from .measures.solid_angle import SolidAngle
    from .measures.substance import Substance
    from .measures.temperature import Temperature
    from .measures.time import Time
    from .measures.torque import Torque
    from .measures.velocity import Velocity
    from .measures.voltage import Voltage
    from .measures.volume import Volume
    from .acceleration import AccelerationUnit
    from .linear_acceleration import meters_per_second_squared
    from .angle import AngleUnit
    from .angular_acceleration import AngularAccelerationUnit
    from .angular_momentum import AngularMomentumUnit
    from .angular_velocity import AngularVelocityUnit
    from .current import CurrentUnit
    from .dimensionless import DimensionlessUnit
    from .concentration import percent
    from .distance import DistanceUnit
    from .energy import EnergyUnit
    from .force import ForceUnit
    from .mass import pounds
    from .frequency import FrequencyUnit
    from .linear_momentum import LinearMomentumUnit
    from .linear_velocity import LinearVelocityUnit
    from .velocity import meters_per_second
    from .moment_of_inertia import MomentOfInertiaUnit
    from .mult import MultUnit
    from .per import PerUnit
    from .power import PowerUnit
    from .resistance import ResistanceUnit
    from .temperature import TemperatureUnit
    from .time import TimeUnit
    from .torque import TorqueUnit
    from .voltage import VoltageUnit
    from .area import AreaUnit
    from .capacitance import CapacitanceUnit
    from .compound import CompoundUnit
    from .charge import ChargeUnit
    from .conductance import ConductanceUnit
    from .data import DataUnit
    from .data_transfer import DataTransferUnit
    from .density import DensityUnit
    from .illuminance import IlluminanceUnit
    from .inductance import InductanceUnit
    from .luminous_flux import LuminousFluxUnit
    from .luminous_intensity import LuminousIntensityUnit
    from .magnetic_flux import MagneticFluxUnit
    from .magnetic_strength import MagneticStrengthUnit
    from .pressure import PressureUnit
    from .solid_angle import SolidAngleUnit
    from .substance import SubstanceUnit
    from .volume import VolumeUnit
    from .radioactivity import RadioactivityUnit
    from .absorbed_dose import AbsorbedDoseUnit
    from .equivalent_dose import EquivalentDoseUnit

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "Measure": ("smartunits.measure", "Measure"),
    "Unit": ("smartunits.unit", "Unit"),
    "UnaryFunction": ("smartunits.unary_function", "UnaryFunction"),
    "AbsorbedDose": ("smartunits.measures.absorbed_dose", "AbsorbedDose"),
    "Acceleration": ("smartunits.measures.acceleration", "Acceleration"),
    "Angle": ("smartunits.measures.angle", "Angle"),
    "AngularAcceleration": ("smartunits.measures.angular_acceleration", "AngularAcceleration"),
    "AngularMomentum": ("smartunits.measures.angular_momentum", "AngularMomentum"),
    "AngularVelocity": ("smartunits.measures.angular_velocity", "AngularVelocity"),
    "Area": ("smartunits.measures.area", "Area"),
    "Capacitance": ("smartunits.measures.capacitance", "Capacitance"),
    "Charge": ("smartunits.measures.charge", "Charge"),
    "Compound": ("smartunits.measures.compound", "Compound"),
    "Concentration": ("smartunits.measures.concentration", "Concentration"),
    "Conductance": ("smartunits.measures.conductance", "Conductance"),
    "Current": ("smartunits.measures.current", "Current"),
    "Data": ("smartunits.measures.data", "Data"),
    "DataTransfer": ("smartunits.measures.data_transfer", "DataTransfer"),
    "Density": ("smartunits.measures.density", "Density"),
    "Dimensionless": ("smartunits.measures.dimensionless", "Dimensionless"),
    "Distance": ("smartunits.measures.distance", "Distance"),
    "Energy": ("smartunits.measures.energy", "Energy"),
    "EquivalentDose": ("smartunits.measures.equivalent_dose", "EquivalentDose"),
    "Force": ("smartunits.measures.force", "Force"),
    "Frequency": ("smartunits.measures.frequency", "Frequency"),
    "Illuminance": ("smartunits.measures.illuminance", "Illuminance"),
    "Inductance": ("smartunits.measures.inductance", "Inductance"),
    "LinearAcceleration": ("smartunits.measures.linear_acceleration", "LinearAcceleration"),
    "LinearMomentum": ("smartunits.measures.linear_momentum", "LinearMomentum"),
    "LinearVelocity": ("smartunits.measures.linear_velocity", "LinearVelocity"),
    "LuminousFlux": ("smartunits.measures.luminous_flux", "LuminousFlux"),
    "LuminousIntensity": ("smartunits.measures.luminous_intensity", "LuminousIntensity"),
    "MagneticFlux": ("smartunits.measures.magnetic_flux", "MagneticFlux"),
    "MagneticStrength": ("smartunits.measures.magnetic_strength", "MagneticStrength"),
    "Mass": ("smartunits.measures.mass", "Mass"),
    "MomentOfInertia": ("smartunits.measures.moment_of_inertia", "MomentOfInertia"),
    "Mult": ("smartunits.measures.mult", "Mult"),
    "Per": ("smartunits.measures.per", "Per"),
    "Power": ("smartunits.measures.power", "Power"),
    "Pressure": ("smartunits.measures.pressure", "Pressure"),
    "Radioactivity": ("smartunits.measures.radioactivity", "Radioactivity"),
    "Resistance": ("smartunits.measures.resistance", "Resistance"),
    "SolidAngle": ("smartunits.measures.solid_angle", "SolidAngle"),
    "Substance": ("smartunits.measures.substance", "Substance"),
    "Temperature": ("smartunits.measures.temperature", "Temperature"),
    "Time": ("smartunits.measures.time", "Time"),
    "Torque": ("smartunits.measures.torque", "Torque"),
    "Velocity": ("smartunits.measures.velocity", "Velocity"),
    "Voltage": ("smartunits.measures.voltage", "Voltage"),
    "Volume": ("smartunits.measures.volume", "Volume"),
    "AccelerationUnit": ("smartunits.acceleration", "AccelerationUnit"),
    "meters_per_second_squared": ("smartunits.linear_acceleration", "meters_per_second_squared"),
    "feet_per_second_squared": ("smartunits.linear_acceleration", "feet_per_second_squared"),
    "inches_per_second_squared": ("smartunits.linear_acceleration", "inches_per_second_squared"),
    "gs": ("smartunits.linear_acceleration", "gs"),
    "standard_gravity": ("smartunits.acceleration", "standard_gravity"),
    "AngleUnit": ("smartunits.angle", "AngleUnit"),
    "radians": ("smartunits.angle", "radians"),
    "revolutions": ("smartunits.angle", "revolutions"),
    "rotations": ("smartunits.angle", "rotations"),
    "degrees": ("smartunits.angle", "degrees"),
    "nanoradians": ("smartunits.angle", "nanoradians"),
    "microradians": ("smartunits.angle", "microradians"),
    "milliradians": ("smartunits.angle", "milliradians"),
    "kiloradians": ("smartunits.angle", "kiloradians"),
    "arcminutes": ("smartunits.angle", "arcminutes"),
    "arcseconds": ("smartunits.angle", "arcseconds"),
    "milliarcseconds": ("smartunits.angle", "milliarcseconds"),
    "turns": ("smartunits.angle", "turns"),
    "gradians": ("smartunits.angle", "gradians"),
    "AngularAccelerationUnit": ("smartunits.angular_acceleration", "AngularAccelerationUnit"),
    "radians_per_second_squared": ("smartunits.angular_acceleration", "radians_per_second_squared"),
    "rotations_per_second_squared": ("smartunits.angular_acceleration", "rotations_per_second_squared"),
    "degrees_per_second_squared": ("smartunits.angular_acceleration", "degrees_per_second_squared"),
    "turns_per_second_squared": ("smartunits.angular_acceleration", "turns_per_second_squared"),
    "AngularMomentumUnit": ("smartunits.angular_momentum", "AngularMomentumUnit"),
    "kilogram_meters_squared_per_second": ("smartunits.angular_momentum", "kilogram_meters_squared_per_second"),
    "pound_inches_squared_per_second": ("smartunits.angular_momentum", "pound_inches_squared_per_second"),
    "AngularVelocityUnit": ("smartunits.angular_velocity", "AngularVelocityUnit"),
    "radians_per_second": ("smartunits.angular_velocity", "radians_per_second"),
    "revolutions_per_second": ("smartunits.angular_velocity", "revolutions_per_second"),
    "rotations_per_second": ("smartunits.angular_velocity", "rotations_per_second"),
    "rotations_per_minute": ("smartunits.angular_velocity", "rotations_per_minute"),
    "degrees_per_second": ("smartunits.angular_velocity", "degrees_per_second"),
    "turns_per_second": ("smartunits.angular_velocity", "turns_per_second"),
    "revolutions_per_minute": ("smartunits.angular_velocity", "revolutions_per_minute"),
    "milliarcseconds_per_year": ("smartunits.angular_velocity", "milliarcseconds_per_year"),
    "CurrentUnit": ("smartunits.current", "CurrentUnit"),
    "amps": ("smartunits.current", "amps"),
    "milliamps": ("smartunits.current", "milliamps"),
    "amperes": ("smartunits.current", "amperes"),
    "nanoamperes": ("smartunits.current", "nanoamperes"),
    "microamperes": ("smartunits.current", "microamperes"),
    "milliamperes": ("smartunits.current", "milliamperes"),
    "kiloamperes": ("smartunits.current", "kiloamperes"),
    "DimensionlessUnit": ("smartunits.dimensionless", "DimensionlessUnit"),
    "value": ("smartunits.dimensionless", "value"),
    "percent": ("smartunits.concentration", "percent"),
    "DistanceUnit": ("smartunits.distance", "DistanceUnit"),
    "meters": ("smartunits.distance", "meters"),
    "millimeters": ("smartunits.distance", "millimeters"),
    "centimeters": ("smartunits.distance", "centimeters"),
    "inches": ("smartunits.distance", "inches"),
    "feet": ("smartunits.distance", "feet"),
    "miles": ("smartunits.distance", "miles"),
    "nanometers": ("smartunits.distance", "nanometers"),
    "micrometers": ("smartunits.distance", "micrometers"),
    "kilometers": ("smartunits.distance", "kilometers"),
    "mils": ("smartunits.distance", "mils"),
    "nautical_miles": ("smartunits.distance", "nautical_miles"),
    "astronical_units": ("smartunits.distance", "astronical_units"),
    "lightyears": ("smartunits.distance", "lightyears"),
    "parsecs": ("smartunits.distance", "parsecs"),
    "angstroms": ("smartunits.distance", "angstroms"),
    "cubits": ("smartunits.distance", "cubits"),
    "fathoms": ("smartunits.distance", "fathoms"),
    "chains": ("smartunits.distance", "chains"),
    "furlongs": ("smartunits.distance", "furlongs"),
    "hands": ("smartunits.distance", "hands"),
    "leagues": ("smartunits.distance", "leagues"),
    "nautical_leagues": ("smartunits.distance", "nautical_leagues"),
    "yards": ("smartunits.distance", "yards"),
    "EnergyUnit": ("smartunits.energy", "EnergyUnit"),
    "joules": ("smartunits.energy", "joules"),
    "millijoules": ("smartunits.energy", "millijoules"),
    "kilojoules": ("smartunits.energy", "kilojoules"),
    "nanojoules": ("smartunits.energy", "nanojoules"),
    "microjoules": ("smartunits.energy", "microjoules"),
    "calories": ("smartunits.energy", "calories"),
    "nanocalories": ("smartunits.energy", "nanocalories"),
    "microcalories": ("smartunits.energy", "microcalories"),
    "millicalories": ("smartunits.energy", "millicalories"),
    "kilocalories": ("smartunits.energy", "kilocalories"),
    "kilowatt_hours": ("smartunits.energy", "kilowatt_hours"),
    "watt_hours": ("smartunits.energy", "watt_hours"),
    "british_thermal_units": ("smartunits.energy", "british_thermal_units"),
    "british_thermal_units_iso": ("smartunits.energy", "british_thermal_units_iso"),
    "british_thermal_units_59": ("smartunits.energy", "british_thermal_units_59"),
    "therms": ("smartunits.energy", "therms"),
    "foot_pounds": ("smartunits.energy", "foot_pounds"),
    "ForceUnit": ("smartunits.force", "ForceUnit"),
    "newtons": ("smartunits.force", "newtons"),
    "pounds_force": ("smartunits.force", "pounds_force"),
    "ounces_force": ("smartunits.force", "ounces_force"),
    "nanonewtons": ("smartunits.force", "nanonewtons"),
    "micronewtons": ("smartunits.force", "micronewtons"),
    "millinewtons": ("smartunits.force", "millinewtons"),
    "kilonewtons": ("smartunits.force", "kilonewtons"),
    "pounds": ("smartunits.mass", "pounds"),
    "dynes": ("smartunits.force", "dynes"),
    "kiloponds": ("smartunits.force", "kiloponds"),
    "poundals": ("smartunits.force", "poundals"),
    "FrequencyUnit": ("smartunits.frequency", "FrequencyUnit"),
    "hertz": ("smartunits.frequency", "hertz"),
    "millihertz": ("smartunits.frequency", "millihertz"),
    "nanohertz": ("smartunits.frequency", "nanohertz"),
    "microhertz": ("smartunits.frequency", "microhertz"),
    "kilohertz": ("smartunits.frequency", "kilohertz"),
    "LinearAccelerationUnit": ("smartunits.linear_acceleration", "LinearAccelerationUnit"),
    "LinearMomentumUnit": ("smartunits.linear_momentum", "LinearMomentumUnit"),
    "kilogram_meters_per_second": ("smartunits.linear_momentum", "kilogram_meters_per_second"),
    "pound_inches_per_second": ("smartunits.linear_momentum", "pound_inches_per_second"),
    "LinearVelocityUnit": ("smartunits.linear_velocity", "LinearVelocityUnit"),
    "meters_per_second": ("smartunits.velocity", "meters_per_second"),
    "feet_per_second": ("smartunits.velocity", "feet_per_second"),
    "inches_per_second": ("smartunits.velocity", "inches_per_second"),
    "MassUnit": ("smartunits.mass", "MassUnit"),
    "kilograms": ("smartunits.mass", "kilograms"),
    "grams": ("smartunits.mass", "grams"),
    "ounces": ("smartunits.mass", "ounces"),
    "nanograms": ("smartunits.mass", "nanograms"),
    "micrograms": ("smartunits.mass", "micrograms"),
    "milligrams": ("smartunits.mass", "milligrams"),
    "metric_tons": ("smartunits.mass", "metric_tons"),
    "long_tons": ("smartunits.mass", "long_tons"),
    "short_tons": ("smartunits.mass", "short_tons"),
    "stone": ("smartunits.mass", "stone"),
    "carats": ("smartunits.mass", "carats"),
    "slugs": ("smartunits.mass", "slugs"),
    "MomentOfInertiaUnit": ("smartunits.moment_of_inertia", "MomentOfInertiaUnit"),
    "kilogram_square_meters": ("smartunits.moment_of_inertia", "kilogram_square_meters"),
    "pound_square_inches": ("smartunits.moment_of_inertia", "pound_square_inches"),
    "MultUnit": ("smartunits.mult", "MultUnit"),
    "PerUnit": ("smartunits.per", "PerUnit"),
    "PowerUnit": ("smartunits.power", "PowerUnit"),
    "watts": ("smartunits.power", "watts"),
    "milliwatts": ("smartunits.power", "milliwatts"),
    "horsepower": ("smartunits.power", "horsepower"),
    "nanowatts": ("smartunits.power", "nanowatts"),
    "microwatts": ("smartunits.power", "microwatts"),
    "kilowatts": ("smartunits.power", "kilowatts"),
    "ResistanceUnit": ("smartunits.resistance", "ResistanceUnit"),
    "ohms": ("smartunits.resistance", "ohms"),
    "kilo_ohms": ("smartunits.resistance", "kilo_ohms"),
    "milli_ohms": ("smartunits.resistance", "milli_ohms"),
    "nanoohms": ("smartunits.resistance", "nanoohms"),
    "microohms": ("smartunits.resistance", "microohms"),
    "milliohms": ("smartunits.resistance", "milliohms"),
    "kiloohms": ("smartunits.resistance", "kiloohms"),
    "TemperatureUnit": ("smartunits.temperature", "TemperatureUnit"),
    "kelvin": ("smartunits.temperature", "kelvin"),
    "celsius": ("smartunits.temperature", "celsius"),
    "fahrenheit": ("smartunits.temperature", "fahrenheit"),
    "reaumur": ("smartunits.temperature", "reaumur"),
    "rankine": ("smartunits.temperature", "rankine"),
    "TimeUnit": ("smartunits.time", "TimeUnit"),
    "seconds": ("smartunits.time", "seconds"),
    "milliseconds": ("smartunits.time", "milliseconds"),
    "microseconds": ("smartunits.time", "microseconds"),
    "nanoseconds": ("smartunits.time", "nanoseconds"),
    "minutes": ("smartunits.time", "minutes"),
    "hours": ("smartunits.time", "hours"),
    "kiloseconds": ("smartunits.time", "kiloseconds"),
    "days": ("smartunits.time", "days"),
    "weeks": ("smartunits.time", "weeks"),
    "years": ("smartunits.time", "years"),
    "julian_years": ("smartunits.time", "julian_years"),
    "gregorian_years": ("smartunits.time", "gregorian_years"),
    "TorqueUnit": ("smartunits.torque", "TorqueUnit"),
    "newton_meters": ("smartunits.torque", "newton_meters"),
    "pound_feet": ("smartunits.torque", "pound_feet"),
    "pound_inches": ("smartunits.torque", "pound_inches"),
    "ounce_inches": ("smartunits.torque", "ounce_inches"),
    "foot_poundals": ("smartunits.torque", "foot_poundals"),
    "inch_pounds": ("smartunits.torque", "inch_pounds"),
    "meter_kilograms": ("smartunits.torque", "meter_kilograms"),
    "VelocityUnit": ("smartunits.velocity", "VelocityUnit"),
    "miles_per_hour": ("smartunits.velocity", "miles_per_hour"),
    "kilometers_per_hour": ("smartunits.velocity", "kilometers_per_hour"),
    "knots": ("smartunits.velocity", "knots"),
    "VoltageUnit": ("smartunits.voltage", "VoltageUnit"),
    "volts": ("smartunits.voltage", "volts"),
    "millivolts": ("smartunits.voltage", "millivolts"),
    "nanovolts": ("smartunits.voltage", "nanovolts"),
    "microvolts": ("smartunits.voltage", "microvolts"),
    "kilovolts": ("smartunits.voltage", "kilovolts"),
    "statvolts": ("smartunits.voltage", "statvolts"),
    "abvolts": ("smartunits.voltage", "abvolts"),
    "AreaUnit": ("smartunits.area", "AreaUnit"),
    "square_meters": ("smartunits.area", "square_meters"),
    "square_feet": ("smartunits.area", "square_feet"),
    "square_inches": ("smartunits.area", "square_inches"),
    "square_miles": ("smartunits.area", "square_miles"),
    "square_kilometers": ("smartunits.area", "square_kilometers"),
    "hectares": ("smartunits.area", "hectares"),
    "acres": ("smartunits.area", "acres"),
    "CapacitanceUnit": ("smartunits.capacitance", "CapacitanceUnit"),
    "farads": ("smartunits.capacitance", "farads"),
    "nanofarads": ("smartunits.capacitance", "nanofarads"),
    "microfarads": ("smartunits.capacitance", "microfarads"),
    "millifarads": ("smartunits.capacitance", "millifarads"),
    "kilofarads": ("smartunits.capacitance", "kilofarads"),
    "CompoundUnit": ("smartunits.compound", "CompoundUnit"),
    "radians_per_meter": ("smartunits.compound", "radians_per_meter"),
    "radians_per_second_per_volt": ("smartunits.compound", "radians_per_second_per_volt"),
    "units_per_second": ("smartunits.compound", "units_per_second"),
    "units_per_second_squared": ("smartunits.compound", "units_per_second_squared"),
    "volt_seconds": ("smartunits.compound", "volt_seconds"),
    "volt_seconds_squared": ("smartunits.compound", "volt_seconds_squared"),
    "volt_seconds_per_meter": ("smartunits.compound", "volt_seconds_per_meter"),
    "volt_seconds_squared_per_meter": ("smartunits.compound", "volt_seconds_squared_per_meter"),
    "volt_seconds_per_feet": ("smartunits.compound", "volt_seconds_per_feet"),
    "volt_seconds_squared_per_feet": ("smartunits.compound", "volt_seconds_squared_per_feet"),
    "volt_seconds_per_radian": ("smartunits.compound", "volt_seconds_per_radian"),
    "volt_seconds_squared_per_radian": ("smartunits.compound", "volt_seconds_squared_per_radian"),
    "unit_seconds_squared_per_unit": ("smartunits.compound", "unit_seconds_squared_per_unit"),
    "meters_per_second_squared_per_volt": ("smartunits.compound", "meters_per_second_squared_per_volt"),
    "meters_per_second_per_radian": ("smartunits.compound", "meters_per_second_per_radian"),
    "ChargeUnit": ("smartunits.charge", "ChargeUnit"),
    "coulombs": ("smartunits.charge", "coulombs"),
    "nanocoulombs": ("smartunits.charge", "nanocoulombs"),
    "microcoulombs": ("smartunits.charge", "microcoulombs"),
    "millicoulombs": ("smartunits.charge", "millicoulombs"),
    "kilocoulombs": ("smartunits.charge", "kilocoulombs"),
    "ampere_hours": ("smartunits.charge", "ampere_hours"),
    "nanoampere_hours": ("smartunits.charge", "nanoampere_hours"),
    "microampere_hours": ("smartunits.charge", "microampere_hours"),
    "milliampere_hours": ("smartunits.charge", "milliampere_hours"),
    "kiloampere_hours": ("smartunits.charge", "kiloampere_hours"),
    "ConcentrationUnit": ("smartunits.concentration", "ConcentrationUnit"),
    "parts_per_million": ("smartunits.concentration", "parts_per_million"),
    "parts_per_billion": ("smartunits.concentration", "parts_per_billion"),
    "parts_per_trillion": ("smartunits.concentration", "parts_per_trillion"),
    "ConductanceUnit": ("smartunits.conductance", "ConductanceUnit"),
    "siemens": ("smartunits.conductance", "siemens"),
    "nanosiemens": ("smartunits.conductance", "nanosiemens"),
    "microsiemens": ("smartunits.conductance", "microsiemens"),
    "millisiemens": ("smartunits.conductance", "millisiemens"),
    "kilosiemens": ("smartunits.conductance", "kilosiemens"),
    "DataUnit": ("smartunits.data", "DataUnit"),
    "exabytes": ("smartunits.data", "exabytes"),
    "exabits": ("smartunits.data", "exabits"),
    "DataTransferUnit": ("smartunits.data_transfer", "DataTransferUnit"),
    "exabytes_per_second": ("smartunits.data_transfer", "exabytes_per_second"),
    "exabits_per_second": ("smartunits.data_transfer", "exabits_per_second"),
    "DensityUnit": ("smartunits.density", "DensityUnit"),
    "kilograms_per_cubic_meter": ("smartunits.density", "kilograms_per_cubic_meter"),
    "grams_per_milliliter": ("smartunits.density", "grams_per_milliliter"),
    "kilograms_per_liter": ("smartunits.density", "kilograms_per_liter"),
    "ounces_per_cubic_foot": ("smartunits.density", "ounces_per_cubic_foot"),
    "ounces_per_cubic_inch": ("smartunits.density", "ounces_per_cubic_inch"),
    "ounces_per_gallon": ("smartunits.density", "ounces_per_gallon"),
    "pounds_per_cubic_foot": ("smartunits.density", "pounds_per_cubic_foot"),
    "pounds_per_cubic_inch": ("smartunits.density", "pounds_per_cubic_inch"),
    "pounds_per_gallon": ("smartunits.density", "pounds_per_gallon"),
    "slugs_per_cubic_foot": ("smartunits.density", "slugs_per_cubic_foot"),
    "IlluminanceUnit": ("smartunits.illuminance", "IlluminanceUnit"),
    "luxes": ("smartunits.illuminance", "luxes"),
    "nanoluxes": ("smartunits.illuminance", "nanoluxes"),
    "microluxes": ("smartunits.illuminance", "microluxes"),
    "milliluxes": ("smartunits.illuminance", "milliluxes"),
    "kiloluxes": ("smartunits.illuminance", "kiloluxes"),
    "footcandles": ("smartunits.illuminance", "footcandles"),
    "lumens_per_square_inch": ("smartunits.illuminance", "lumens_per_square_inch"),
    "phots": ("smartunits.illuminance", "phots"),
    "InductanceUnit": ("smartunits.inductance", "InductanceUnit"),
    "henries": ("smartunits.inductance", "henries"),
    "nanohenries": ("smartunits.inductance", "nanohenries"),
    "microhenries": ("smartunits.inductance", "microhenries"),
    "millihenries": ("smartunits.inductance", "millihenries"),
    "kilohenries": ("smartunits.inductance", "kilohenries"),
    "LuminousFluxUnit": ("smartunits.luminous_flux", "LuminousFluxUnit"),
    "lumens": ("smartunits.luminous_flux", "lumens"),
    "nanolumens": ("smartunits.luminous_flux", "nanolumens"),
    "microlumens": ("smartunits.luminous_flux", "microlumens"),
    "millilumens": ("smartunits.luminous_flux", "millilumens"),
    "kilolumens": ("smartunits.luminous_flux", "kilolumens"),
    "LuminousIntensityUnit": ("smartunits.luminous_intensity", "LuminousIntensityUnit"),
    "candelas": ("smartunits.luminous_intensity", "candelas"),
    "nanocandelas": ("smartunits.luminous_intensity", "nanocandelas"),
    "microcandelas": ("smartunits.luminous_intensity", "microcandelas"),
    "millicandelas": ("smartunits.luminous_intensity", "millicandelas"),
    "kilocandelas": ("smartunits.luminous_intensity", "kilocandelas"),
    "MagneticFluxUnit": ("smartunits.magnetic_flux", "MagneticFluxUnit"),
    "webers": ("smartunits.magnetic_flux", "webers"),
    "nanowebers": ("smartunits.magnetic_flux", "nanowebers"),
    "microwebers": ("smartunits.magnetic_flux", "microwebers"),
    "milliwebers": ("smartunits.magnetic_flux", "milliwebers"),
    "kilowebers": ("smartunits.magnetic_flux", "kilowebers"),
    "maxwells": ("smartunits.magnetic_flux", "maxwells"),
    "MagneticStrengthUnit": ("smartunits.magnetic_strength", "MagneticStrengthUnit"),
    "teslas": ("smartunits.magnetic_strength", "teslas"),
    "nanoteslas": ("smartunits.magnetic_strength", "nanoteslas"),
    "microteslas": ("smartunits.magnetic_strength", "microteslas"),
    "milliteslas": ("smartunits.magnetic_strength", "milliteslas"),
    "kiloteslas": ("smartunits.magnetic_strength", "kiloteslas"),
    "gauss": ("smartunits.magnetic_strength", "gauss"),
    "PressureUnit": ("smartunits.pressure", "PressureUnit"),
    "pascals": ("smartunits.pressure", "pascals"),
    "nanopascals": ("smartunits.pressure", "nanopascals"),
    "micropascals": ("smartunits.pressure", "micropascals"),
    "millipascals": ("smartunits.pressure", "millipascals"),
    "kilopascals": ("smartunits.pressure", "kilopascals"),
    "bars": ("smartunits.pressure", "bars"),
    "mbars": ("smartunits.pressure", "mbars"),
    "atmospheres": ("smartunits.pressure", "atmospheres"),
    "pounds_per_square_inch": ("smartunits.pressure", "pounds_per_square_inch"),
    "torrs": ("smartunits.pressure", "torrs"),
    "SolidAngleUnit": ("smartunits.solid_angle", "SolidAngleUnit"),
    "steradians": ("smartunits.solid_angle", "steradians"),
    "nanosteradians": ("smartunits.solid_angle", "nanosteradians"),
    "microsteradians": ("smartunits.solid_angle", "microsteradians"),
    "millisteradians": ("smartunits.solid_angle", "millisteradians"),
    "kilosteradians": ("smartunits.solid_angle", "kilosteradians"),
    "degrees_squared": ("smartunits.solid_angle", "degrees_squared"),
    "spats": ("smartunits.solid_angle", "spats"),
    "SubstanceUnit": ("smartunits.substance", "SubstanceUnit"),
    "moles": ("smartunits.substance", "moles"),
    "VolumeUnit": ("smartunits.volume", "VolumeUnit"),
    "cubic_meters": ("smartunits.volume", "cubic_meters"),
    "cubic_millimeters": ("smartunits.volume", "cubic_millimeters"),
    "cubic_kilometers": ("smartunits.volume", "cubic_kilometers"),
    "liters": ("smartunits.volume", "liters"),
    "nanoliters": ("smartunits.volume", "nanoliters"),
    "microliters": ("smartunits.volume", "microliters"),
    "milliliters": ("smartunits.volume", "milliliters"),
    "kiloliters": ("smartunits.volume", "kiloliters"),
    "cubic_inches": ("smartunits.volume", "cubic_inches"),
    "cubic_feet": ("smartunits.volume", "cubic_feet"),
    "cubic_yards": ("smartunits.volume", "cubic_yards"),
    "cubic_miles": ("smartunits.volume", "cubic_miles"),
    "gallons": ("smartunits.volume", "gallons"),
    "quarts": ("smartunits.volume", "quarts"),
    "pints": ("smartunits.volume", "pints"),
    "cups": ("smartunits.volume", "cups"),
    "fluid_ounces": ("smartunits.volume", "fluid_ounces"),
    "barrels": ("smartunits.volume", "barrels"),
    "bushels": ("smartunits.volume", "bushels"),
    "cords": ("smartunits.volume", "cords"),
    "cubic_fathoms": ("smartunits.volume", "cubic_fathoms"),
    "tablespoons": ("smartunits.volume", "tablespoons"),
    "teaspoons": ("smartunits.volume", "teaspoons"),
    "pinches": ("smartunits.volume", "pinches"),
    "dashes": ("smartunits.volume", "dashes"),
    "drops": ("smartunits.volume", "drops"),
    "fifths": ("smartunits.volume", "fifths"),
    "drams": ("smartunits.volume", "drams"),
    "gills": ("smartunits.volume", "gills"),
    "pecks": ("smartunits.volume", "pecks"),
    "sacks": ("smartunits.volume", "sacks"),
    "shots": ("smartunits.volume", "shots"),
    "strikes": ("smartunits.volume", "strikes"),
    "RadioactivityUnit": ("smartunits.radioactivity", "RadioactivityUnit"),
    "becquerels": ("smartunits.radioactivity", "becquerels"),
    "nanobecquerels": ("smartunits.radioactivity", "nanobecquerels"),
    "microbecquerels": ("smartunits.radioactivity", "microbecquerels"),
    "millibecquerels": ("smartunits.radioactivity", "millibecquerels"),
    "kilobecquerels": ("smartunits.radioactivity", "kilobecquerels"),
    "curies": ("smartunits.radioactivity", "curies"),
    "rutherfords": ("smartunits.radioactivity", "rutherfords"),
    "AbsorbedDoseUnit": ("smartunits.absorbed_dose", "AbsorbedDoseUnit"),
    "grays": ("smartunits.absorbed_dose", "grays"),
    "nanograys": ("smartunits.absorbed_dose", "nanograys"),
    "micrograys": ("smartunits.absorbed_dose", "micrograys"),
    "milligrays": ("smartunits.absorbed_dose", "milligrays"),
    "kilograys": ("smartunits.absorbed_dose", "kilograys"),
    "rads": ("smartunits.absorbed_dose", "rads"),
    "EquivalentDoseUnit": ("smartunits.equivalent_dose", "EquivalentDoseUnit"),
    "sieverts": ("smartunits.equivalent_dose", "sieverts"),
    "nanosieverts": ("smartunits.equivalent_dose", "nanosieverts"),
    "microsieverts": ("smartunits.equivalent_dose", "microsieverts"),
    "millisieverts": ("smartunits.equivalent_dose", "millisieverts"),
    "kilosieverts": ("smartunits.equivalent_dose", "kilosieverts"),
}


def __getattr__(name: str):
    try:
        module_name, attribute_name = _LAZY_IMPORTS[name]
    except KeyError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None

    module = import_module(module_name)
    value = getattr(module, attribute_name)

    # Cache resolved values for future access.
    globals()[name] = value
    return value


__all__ = list(_LAZY_IMPORTS)

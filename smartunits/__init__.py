from importlib import import_module

from .measure import Measure
from .unit import Unit
from .unary_function import UnaryFunction

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "Measure": ("smartunits.measure", "Measure"),
    "Unit": ("smartunits.unit", "Unit"),
    "UnaryFunction": ("smartunits.unary_function", "UnaryFunction"),
    "Units": ("smartunits.units", "Units"),
    "Acceleration": ("smartunits.measures.acceleration", "Acceleration"),
    "Angle": ("smartunits.measures.angle", "Angle"),
    "AngularAcceleration": ("smartunits.measures.angular_acceleration", "AngularAcceleration"),
    "AngularMomentum": ("smartunits.measures.angular_momentum", "AngularMomentum"),
    "AngularVelocity": ("smartunits.measures.angular_velocity", "AngularVelocity"),
    "Current": ("smartunits.measures.current", "Current"),
    "Dimensionless": ("smartunits.measures.dimensionless", "Dimensionless"),
    "Distance": ("smartunits.measures.distance", "Distance"),
    "Energy": ("smartunits.measures.energy", "Energy"),
    "Force": ("smartunits.measures.force", "Force"),
    "Frequency": ("smartunits.measures.frequency", "Frequency"),
    "LinearAcceleration": ("smartunits.measures.linear_acceleration", "LinearAcceleration"),
    "LinearMomentum": ("smartunits.measures.linear_momentum", "LinearMomentum"),
    "LinearVelocity": ("smartunits.measures.linear_velocity", "LinearVelocity"),
    "Mass": ("smartunits.measures.mass", "Mass"),
    "MomentOfInertia": ("smartunits.measures.moment_of_inertia", "MomentOfInertia"),
    "Mult": ("smartunits.measures.mult", "Mult"),
    "Per": ("smartunits.measures.per", "Per"),
    "Power": ("smartunits.measures.power", "Power"),
    "Resistance": ("smartunits.measures.resistance", "Resistance"),
    "Temperature": ("smartunits.measures.temperature", "Temperature"),
    "Time": ("smartunits.measures.time", "Time"),
    "Torque": ("smartunits.measures.torque", "Torque"),
    "Velocity": ("smartunits.measures.velocity", "Velocity"),
    "Voltage": ("smartunits.measures.voltage", "Voltage"),
    "AccelerationUnit": ("smartunits.acceleration", "AccelerationUnit"),
    "AngleUnit": ("smartunits.angle", "AngleUnit"),
    "AngularAccelerationUnit": ("smartunits.angular_acceleration", "AngularAccelerationUnit"),
    "AngularMomentumUnit": ("smartunits.angular_momentum", "AngularMomentumUnit"),
    "AngularVelocityUnit": ("smartunits.angular_velocity", "AngularVelocityUnit"),
    "CurrentUnit": ("smartunits.current", "CurrentUnit"),
    "DimensionlessUnit": ("smartunits.dimensionless", "DimensionlessUnit"),
    "DistanceUnit": ("smartunits.distance", "DistanceUnit"),
    "EnergyUnit": ("smartunits.energy", "EnergyUnit"),
    "ForceUnit": ("smartunits.force", "ForceUnit"),
    "FrequencyUnit": ("smartunits.frequency", "FrequencyUnit"),
    "LinearAccelerationUnit": ("smartunits.linear_acceleration", "LinearAccelerationUnit"),
    "LinearMomentumUnit": ("smartunits.linear_momentum", "LinearMomentumUnit"),
    "LinearVelocityUnit": ("smartunits.linear_velocity", "LinearVelocityUnit"),
    "MassUnit": ("smartunits.mass", "MassUnit"),
    "MomentOfInertiaUnit": ("smartunits.moment_of_inertia", "MomentOfInertiaUnit"),
    "MultUnit": ("smartunits.mult", "MultUnit"),
    "PerUnit": ("smartunits.per", "PerUnit"),
    "PowerUnit": ("smartunits.power", "PowerUnit"),
    "ResistanceUnit": ("smartunits.resistance", "ResistanceUnit"),
    "TemperatureUnit": ("smartunits.temperature", "TemperatureUnit"),
    "TimeUnit": ("smartunits.time", "TimeUnit"),
    "TorqueUnit": ("smartunits.torque", "TorqueUnit"),
    "VelocityUnit": ("smartunits.velocity", "VelocityUnit"),
    "VoltageUnit": ("smartunits.voltage", "VoltageUnit"),
    "AreaUnit": ("smartunits.area", "AreaUnit"),
    "CapacitanceUnit": ("smartunits.capacitance", "CapacitanceUnit"),
    "CompoundUnit": ("smartunits.compound", "CompoundUnit"),
    "ChargeUnit": ("smartunits.charge", "ChargeUnit"),
    "ConcentrationUnit": ("smartunits.concentration", "ConcentrationUnit"),
    "ConductanceUnit": ("smartunits.conductance", "ConductanceUnit"),
    "DataUnit": ("smartunits.data", "DataUnit"),
    "DataTransferUnit": ("smartunits.data_transfer", "DataTransferUnit"),
    "DensityUnit": ("smartunits.density", "DensityUnit"),
    "IlluminanceUnit": ("smartunits.illuminance", "IlluminanceUnit"),
    "InductanceUnit": ("smartunits.inductance", "InductanceUnit"),
    "LuminousFluxUnit": ("smartunits.luminous_flux", "LuminousFluxUnit"),
    "LuminousIntensityUnit": ("smartunits.luminous_intensity", "LuminousIntensityUnit"),
    "MagneticFluxUnit": ("smartunits.magnetic_flux", "MagneticFluxUnit"),
    "MagneticStrengthUnit": ("smartunits.magnetic_strength", "MagneticStrengthUnit"),
    "PressureUnit": ("smartunits.pressure", "PressureUnit"),
    "SolidAngleUnit": ("smartunits.solid_angle", "SolidAngleUnit"),
    "SubstanceUnit": ("smartunits.substance", "SubstanceUnit"),
    "VolumeUnit": ("smartunits.volume", "VolumeUnit"),
    "RadioactivityUnit": ("smartunits.radioactivity", "RadioactivityUnit"),
    "AbsorbedDoseUnit": ("smartunits.absorbed_dose", "AbsorbedDoseUnit"),
    "EquivalentDoseUnit": ("smartunits.equivalent_dose", "EquivalentDoseUnit"),
}


def __getattr__(name: str):
    if name in _LAZY_IMPORTS:
        module_name, attribute_name = _LAZY_IMPORTS[name]
        module = import_module(module_name)
        value = getattr(module, attribute_name)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["Measure", "Unit", "UnaryFunction", "Units"] + list(_LAZY_IMPORTS)

import importlib

__all__ = [
    "AbsorbedDose",
    "Acceleration",
    "Angle",
    "AngularAcceleration",
    "AngularMomentum",
    "AngularVelocity",
    "Area",
    "Capacitance",
    "Charge",
    "Compound",
    "Concentration",
    "Conductance",
    "Current",
    "Data",
    "DataTransfer",
    "Density",
    "Dimensionless",
    "Distance",
    "Energy",
    "EquivalentDose",
    "Force",
    "Frequency",
    "Illuminance",
    "Inductance",
    "LinearAcceleration",
    "LinearMomentum",
    "LinearVelocity",
    "LuminousFlux",
    "LuminousIntensity",
    "MagneticFlux",
    "MagneticStrength",
    "Mass",
    "MomentOfInertia",
    "Mult",
    "Per",
    "Power",
    "Pressure",
    "Radioactivity",
    "Resistance",
    "SolidAngle",
    "Substance",
    "Temperature",
    "Time",
    "Torque",
    "Velocity",
    "Voltage",
    "Volume"
]

_LAZY_IMPORTS = {
    "AbsorbedDose": (".absorbed_dose", "AbsorbedDose"),
    "Acceleration": (".acceleration", "Acceleration"),
    "Angle": (".angle", "Angle"),
    "AngularAcceleration": (".angular_acceleration", "AngularAcceleration"),
    "AngularMomentum": (".angular_momentum", "AngularMomentum"),
    "AngularVelocity": (".angular_velocity", "AngularVelocity"),
    "Area": (".area", "Area"),
    "Capacitance": (".capacitance", "Capacitance"),
    "Charge": (".charge", "Charge"),
    "Compound": (".compound", "Compound"),
    "Concentration": (".concentration", "Concentration"),
    "Conductance": (".conductance", "Conductance"),
    "Current": (".current", "Current"),
    "Data": (".data", "Data"),
    "DataTransfer": (".data_transfer", "DataTransfer"),
    "Density": (".density", "Density"),
    "Dimensionless": (".dimensionless", "Dimensionless"),
    "Distance": (".distance", "Distance"),
    "Energy": (".energy", "Energy"),
    "EquivalentDose": (".equivalent_dose", "EquivalentDose"),
    "Force": (".force", "Force"),
    "Frequency": (".frequency", "Frequency"),
    "Illuminance": (".illuminance", "Illuminance"),
    "Inductance": (".inductance", "Inductance"),
    "LinearAcceleration": (".linear_acceleration", "LinearAcceleration"),
    "LinearMomentum": (".linear_momentum", "LinearMomentum"),
    "LinearVelocity": (".linear_velocity", "LinearVelocity"),
    "LuminousFlux": (".luminous_flux", "LuminousFlux"),
    "LuminousIntensity": (".luminous_intensity", "LuminousIntensity"),
    "MagneticFlux": (".magnetic_flux", "MagneticFlux"),
    "MagneticStrength": (".magnetic_strength", "MagneticStrength"),
    "Mass": (".mass", "Mass"),
    "MomentOfInertia": (".moment_of_inertia", "MomentOfInertia"),
    "Mult": (".mult", "Mult"),
    "Per": (".per", "Per"),
    "Power": (".power", "Power"),
    "Pressure": (".pressure", "Pressure"),
    "Radioactivity": (".radioactivity", "Radioactivity"),
    "Resistance": (".resistance", "Resistance"),
    "SolidAngle": (".solid_angle", "SolidAngle"),
    "Substance": (".substance", "Substance"),
    "Temperature": (".temperature", "Temperature"),
    "Time": (".time", "Time"),
    "Torque": (".torque", "Torque"),
    "Velocity": (".velocity", "Velocity"),
    "Voltage": (".voltage", "Voltage"),
    "Volume": (".volume", "Volume"),
}


def __getattr__(name):
    try:
        module_name, attribute_name = _LAZY_IMPORTS[name]
    except KeyError:
        raise AttributeError(
            f"module {__name__!r} has no attribute {name!r}"
        ) from None

    module = importlib.import_module(module_name, __name__)
    value = getattr(module, attribute_name)

    globals()[name] = value
    return value


def __dir__():
    return sorted(list(globals()) + __all__)

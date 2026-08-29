import importlib

__all__ = [
    "Acceleration",
    "Angle",
    "AngularAcceleration",
    "AngularMomentum",
    "AngularVelocity",
    "Current",
    "Dimensionless",
    "Distance",
    "Energy",
    "Force",
    "Frequency",
    "LinearAcceleration",
    "LinearMomentum",
    "LinearVelocity",
    "Mass",
    "MomentOfInertia",
    "Mult",
    "Per",
    "Power",
    "Resistance",
    "Temperature",
    "Time",
    "Torque",
    "Velocity",
    "Voltage"
]

_LAZY_IMPORTS = {
    "Acceleration": (".acceleration", "Acceleration"),
    "Angle": (".angle", "Angle"),
    "AngularAcceleration": (".angular_acceleration", "AngularAcceleration"),
    "AngularMomentum": (".angular_momentum", "AngularMomentum"),
    "AngularVelocity": (".angular_velocity", "AngularVelocity"),
    "Current": (".current", "Current"),
    "Dimensionless": (".dimensionless", "Dimensionless"),
    "Distance": (".distance", "Distance"),
    "Energy": (".energy", "Energy"),
    "Force": (".force", "Force"),
    "Frequency": (".frequency", "Frequency"),
    "LinearAcceleration": (".linear_acceleration", "LinearAcceleration"),
    "LinearMomentum": (".linear_momentum", "LinearMomentum"),
    "LinearVelocity": (".linear_velocity", "LinearVelocity"),
    "Mass": (".mass", "Mass"),
    "MomentOfInertia": (".moment_of_inertia", "MomentOfInertia"),
    "Mult": (".mult", "Mult"),
    "Per": (".per", "Per"),
    "Power": (".power", "Power"),
    "Resistance": (".resistance", "Resistance"),
    "Temperature": (".temperature", "Temperature"),
    "Time": (".time", "Time"),
    "Torque": (".torque", "Torque"),
    "Velocity": (".velocity", "Velocity"),
    "Voltage": (".voltage", "Voltage"),
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

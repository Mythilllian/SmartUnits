#!/usr/bin/env python3

# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

# This script generates unit-specific interfaces and mutable and immutable
# implementations of those interfaces.
#
# Generated files will be located in wpiunits/src/generated/main/

import argparse
import inspect
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def output(output_dir, outfn: str, contents: str):
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / outfn
    output_file.write_text(contents, encoding="utf-8", newline="\n")


# The units for which multiply and divide mathematical operations are defined
MATH_OPERATION_UNITS = [
    "Acceleration<Any>",
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
    "Mult<Any, Any>",
    "Per<Any, Any>",
    "Power",
    "Resistance",
    "Temperature",
    "Time",
    "Torque",
    "Velocity[Any, Any]",
    "Voltage",
]

# Configurations for all generated units
UNIT_CONFIGURATIONS = {
    "Acceleration": {
        "base_unit": "unit()",
        "generics": {"D": {"extends": "Unit"}},
        "multiply": {},
        "divide": {},
    },
    "Angle": {
        "base_unit": "Radians",
        "multiply": {"Frequency": "AngularVelocity"},
        "divide": {"Time": "AngularVelocity"},
    },
    "AngularAcceleration": {
        "base_unit": "RadiansPerSecondPerSecond",
        "multiply": {"Time": "AngularVelocity"},
        "divide": {"Frequency": "AngularVelocity"},
    },
    "AngularMomentum": {
        "base_unit": "KilogramMetersSquaredPerSecond",
        "multiply": {},
        "divide": {"AngularVelocity": "MomentOfInertia"},
    },
    "AngularVelocity": {
        "base_unit": "RadiansPerSecond",
        "multiply": {"Time": "Angle", "Frequency": "AngularAcceleration"},
        "divide": {"Time": "AngularAcceleration"},
        "extra": {"code": inspect.cleandoc(
            """
          def as_frequency(self) -> "Frequency":
          \treturn Hertz.of_units(self.base_unit_magnitude())
        """
        ), "types":{"Frequency"}},
    },
    "Current": {
        "base_unit": "Amps",
        "multiply": {"Voltage": "Power", "Resistance": "Voltage"},
        "divide": {},
    },
    "Dimensionless": {
        "base_unit": "Value",
        "multiply": {
            "Angle": "Angle",
            "AngularAcceleration": "AngularAcceleration",
            "AngularMomentum": "AngularMomentum",
            "AngularVelocity": "AngularVelocity",
            "Current": "Current",
            "Dimensionless": "Dimensionless",
            "Distance": "Distance",
            "Energy": "Energy",
            "Force": "Force",
            "Frequency": "Frequency",
            "LinearAcceleration": "LinearAcceleration",
            "LinearMomentum": "LinearMomentum",
            "LinearVelocity": "LinearVelocity",
            "Mass": "Mass",
            "MomentOfInertia": "MomentOfInertia",
            "Power": "Power",
            "Resistance": "Resistance",
            "Temperature": "Temperature",
            "Time": "Time",
            "Torque": "Torque",
            "Voltage": "Voltage",
        },
        "divide": {
            "Time": "Frequency",
            # TODO:
            # "AngularVelocity": "Per<TimeUnit, AngleUnit>",
            # "AngularAcceleration": "Per<TimeUnit, AngularVelocityUnit>",
            # "LinearVelocity": "Per<TimeUnit, DistanceUnit>",
            # "LinearAcceleration": "Per<TimeUnit, LinearVelocityUnit>",
            # "Velocity<?>": "Per<TimeUnit, ?>",
            # "Acceleration<?>": "Per<TimeUnit, VelocityUnit<?>>
            # "Per<N, D>": "Per<D, N>"
        },
    },
    "Distance": {
        "base_unit": "Meters",
        "multiply": {
            "Frequency": "LinearVelocity",
            # Distance x Force = Torque
            # Force x Distance = Energy
            "Force": "Torque",
        },
        "divide": {"Time": "LinearVelocity", "LinearVelocity": "Time"},
    },
    "Energy": {
        "base_unit": "Joules",
        "multiply": {"Frequency": "Power"},
        "divide": {"Time": "Power"},
    },
    "Force": {
        "base_unit": "Newtons",
        "multiply": {
            # Distance x Force = Torque
            # Force x Distance = Energy
            "Distance": "Energy"
        },
        "divide": {"Mass": "LinearAcceleration", "LinearAcceleration": "Mass"},
    },
    "Frequency": {
        "base_unit": "Hertz",
        "multiply": {
            "Time": "Dimensionless",
            "Distance": "LinearVelocity",
            "LinearVelocity": "LinearAcceleration",
            "Angle": "AngularVelocity",
            "AngularVelocity": "AngularAcceleration",
        },
        "divide": {},
        "extra": {"code":inspect.cleandoc(
            """
          def as_period(self) -> "Time":
          \treturn Seconds.of(1 / self.base_unit_magnitude());
        """
        ), "types":{"Time"}},
    },
    "LinearAcceleration": {
        "base_unit": "MetersPerSecondPerSecond",
        "multiply": {"Time": "LinearVelocity"},
        "divide": {"Frequency": "LinearVelocity"},
    },
    "LinearMomentum": {
        "base_unit": "KilogramMetersPerSecond",
        "multiply": {"Frequency": "Force"},
        "divide": {"Mass": "LinearVelocity", "LinearVelocity": "Mass", "Time": "Force"},
    },
    "LinearVelocity": {
        "base_unit": "MetersPerSecond",
        "multiply": {"Time": "Distance", "Frequency": "LinearAcceleration"},
        "divide": {"Time": "LinearAcceleration"},
    },
    "Mass": {
        "base_unit": "Kilograms",
        "multiply": {"LinearAcceleration": "Force"},
        "divide": {},
    },
    "MomentOfInertia": {
        "base_unit": "KilogramSquareMeters",
        "multiply": {"AngularVelocity": "AngularMomentum"},
        "divide": {},
    },
    "Mult": {
        "base_unit": "unit()",
        "generics": {"A": {"extends": "Unit"}, "B": {"extends": "Unit"}},
        "multiply": {},
        "divide": {},
    },
    "Per": {
        "base_unit": "unit()",
        "generics": {"Dividend": {"extends": "Unit"}, "Divisor": {"extends": "Unit"}},
        "multiply": {},
        "divide": {},
        "extra": {"code":inspect.cleandoc(
            """
          def times_divisor(self, multiplier: Measure[Divisor]) ->  Measure[Dividend]: {
          \treturn self._base_unit._numerator.of_base_units(self._base_unit_magnitude * multiplier._base_unit_magnitude);
          }

          def reciprocal(self) -> PerUnit[Divisor, Dividend]:
          \t# May return a velocity if Divisor == TimeUnit, so we can't guarantee a "Per" instance
          \treturn self._base_unit.reciprocal().of_base_units(1 / self._base_unit_magnitude)
          }
        """
        ), "types":{}},
    },
    "Power": {
        "base_unit": "Watts",
        "multiply": {
            "Time": "Energy",
        },
        "divide": {"Voltage": "Current", "Current": "Voltage", "Energy": "Frequency"},
    },
    "Resistance": {
        "base_unit": "Ohms",
        "multiply": {
            "Current": "Voltage",
        },
        "divide": {},
    },
    "Temperature": {"base_unit": "Kelvin", "multiply": {}, "divide": {}},
    "Time": {
        "base_unit": "Seconds",
        "multiply": {
            "Frequency": "Dimensionless",
            "AngularVelocity": "Angle",
            "AngularAcceleration": "AngularVelocity",
            "LinearVelocity": "Distance",
            "LinearAcceleration": "LinearVelocity",
            # TODO:
            # "Acceleration<D>": "Velocity<D>"
            # "Velocity<D>": "Measure<D>"
        },
        "divide": {
            # Time specifically needs this to be called out so generated methods like
            # `per(TimeUnit)` or `divide(Time)` will return dimensionless values instead of
            # `Velocity<TimeUnit>` (i.e. a time per unit time ratio)
            "Time": "Dimensionless"
        },
        "extra": {"code":inspect.cleandoc(
            """
          def as_frequency(self) -> "Frequency":
          \treturn Hertz.of(1 / self.base_unit_magnitude())
        """
        ), "types":{"Frequency"}},
    },
    "Torque": {
        "base_unit": "NewtonMeters",
        "multiply": {},
        "divide": {"Distance": "Force", "Force": "Distance"},
    },
    "Velocity": {
        "base_unit": "unit()",
        "generics": {"D": {"extends": "Unit"}},
        "multiply": {
            "Time": {
                "implementation": inspect.cleandoc(
                    """
                  \nreturn self._unit._numerator._of_base_units(self._base_unit_magnitude * other._base_unit_magnitude)
                """
                )
            }
        },
        "divide": {},
    },
    "Voltage": {
        "base_unit": "Volts",
        "multiply": {
            "Current": "Power",
        },
        "divide": {
            "Resistance": "Current",
            "Current": "Resistance",
        },
    },
}


def generics_list(measure_name):
    if "generics" in UNIT_CONFIGURATIONS[measure_name]:
        args = []
        for name, config in UNIT_CONFIGURATIONS[measure_name]["generics"].items():
            if "extends" in config:
                args.append("{} extends {}".format(name, config["extends"]))
            elif "super" in config:
                args.append("{} super {}".format(name, config["super"]))
            else:
                args.append(name)

        return "[{}]".format(", ".join(args))
    else:
        return ""


def generics_usage(measure_name):
    if "generics" in UNIT_CONFIGURATIONS[measure_name]:
        args = UNIT_CONFIGURATIONS[measure_name]["generics"].keys()

        return "[{}]".format(", ".join(args))
    else:
        return ""
    
def type_vars(measure_name):
    x = ""
    for generic in UNIT_CONFIGURATIONS[measure_name].get("generics", {}).keys():
        x += f"\n{generic} = TypeVar('{generic}', bound=Unit)"
    return x

def class_header(measure_name):
    has_generics = bool(generics_list(measure_name))
    if has_generics:
        return f'class {measure_name}(Measure["{mtou(measure_name)}"], ABC, Generic{generics_usage(measure_name)}):'
    else:
        return f'class {measure_name}(Measure["{mtou(measure_name)}"], ABC):'


def type_usage(measure_name):
    return measure_name + generics_usage(measure_name)


# measure-to-unit
def mtou(measure_name):
    if (
        measure_name in UNIT_CONFIGURATIONS
        and "generics" in UNIT_CONFIGURATIONS[measure_name]
    ):
        return "{}Unit{}".format(measure_name, generics_usage(measure_name))
    else:
        regex = re.compile(r"^(.*?)(<.*>)?$")
        return re.sub(regex, "\\1Unit\\2", measure_name)


def indent(multiline_string, indentation):
    """
    Indents a multiline string by `indentation` number of spaces
    """
    return "\n".join(
        list(map(lambda line: " " * indentation + line, multiline_string.split("\n")))
    )

def file_name(measure_name: str) -> str:
    parts = []
    for c in measure_name:
        if c.isupper() and parts:
            parts.append("_")
        parts.append(c.lower())
    return "".join(parts)

def generate_units(output_directory: Path, template_directory: Path):
    env = Environment(
        loader=FileSystemLoader(template_directory),
        autoescape=False,
        keep_trailing_newline=True,
    )

    interfaceTemplate = env.get_template("measure-interface.py.jinja")
    # immutableTemplate = env.get_template("measure-immutable.py.jinja")
    # mutableTemplate = env.get_template("measure-mutable.py.jinja")
    rootPath = output_directory

    helpers = {
        "type_vars": type_vars,
        "class_header": class_header,
        "type_usage": type_usage,
        "generics_list": generics_list,
        "generics_usage": generics_usage,
        "mtou": mtou,
        "indent": indent,
    }

    init_imports = []
    init_all = []
    for unit_name in UNIT_CONFIGURATIONS:
        interfaceContents = interfaceTemplate.render(
            name=unit_name,
            prefix="",
            math_units=MATH_OPERATION_UNITS,
            config=UNIT_CONFIGURATIONS,
            helpers=helpers,
        )
        # immutableContents = immutableTemplate.render(
        #     name=unit_name,
        #     prefix="Immutable",
        #     units=MATH_OPERATION_UNITS,
        #     config=UNIT_CONFIGURATIONS,
        #     helpers=helpers,
        # )
        # mutableContents = mutableTemplate.render(
        #     name=unit_name,
        #     prefix="Mut",
        #     units=MATH_OPERATION_UNITS,
        #     config=UNIT_CONFIGURATIONS,
        #     helpers=helpers,
        # )
        init_imports.append(f"from .{file_name(unit_name)} import {unit_name}")
        # init_imports.append(f"from immutable_{file_name(unit_name)} import Immutable{unit_name}")
        # init_imports.append(f"from mut_{file_name(unit_name)} import Mut{unit_name}")
        init_all.append(f"{unit_name}")
        # init_all.append(f"Immutable{unit_name}")
        # init_all.append(f"Mut{unit_name}")

        output(rootPath / "measures", file_name(unit_name) + ".py", interfaceContents)
        # output(rootPath / "measures", file_name(f"Immutable{unit_name}") + ".py", immutableContents)
        # output(rootPath / "measures", file_name(f"Mut{unit_name}") + ".py", mutableContents)

    output(
        rootPath / "measures",
        "__init__.py",
        "\n".join(init_imports)
        + "\n\n__all__ = [\n    "
        + ",\n    ".join(f'"{name}"' for name in init_all)
        + "\n]",
    )

def main():
    script_path = Path(__file__).resolve()
    dirname = script_path.parent

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_directory",
        help="Optional. If set, will output the generated files to this directory, otherwise it will use a path relative to the script",
        default=dirname / "generated",
        type=Path,
    )
    parser.add_argument(
        "--template_root",
        help="Optional. If set, will use this directory as the root for the jinja templates",
        default=dirname / "templates",
        type=Path,
    )
    args = parser.parse_args()

    generate_units(args.output_directory, args.template_root)


if __name__ == "__main__":
    main()
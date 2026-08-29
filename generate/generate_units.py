#!/usr/bin/env python3

# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

# This script generates unit-specific interfaces and mutable and immutable
# implementations of those interfaces.
#
# Generated files will be located in wpiunits/src/generated/main/

import argparse
import json
import re
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def output(output_dir, outfn: str, contents: str):
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / outfn
    output_file.write_text(contents, encoding="utf-8", newline="\n")


def load_json_file(file_path: Path):
    with file_path.open(encoding="utf-8") as file_handle:
        return json.load(file_handle)


SCRIPT_DIRECTORY = Path(__file__).resolve().parent
UNIT_CONFIGURATIONS = load_json_file(SCRIPT_DIRECTORY / "unit_configurations.json")


def normalize_measurement_units(measurement_configurations: list[dict]) -> list[dict]:
    normalized_configurations: list[dict] = []

    for measurement in measurement_configurations:
        normalized_units: list[dict] = []
        for unit in measurement.get("units", []):
            to_base_multiplier = unit.get("to_base_multiplier", unit.get("conversion_factor", 1.0))
            to_base_offset = unit.get("to_base_offset", 0.0)

            from_base_multiplier = unit.get("from_base_multiplier")
            if from_base_multiplier is None:
                if to_base_multiplier == 0:
                    raise ValueError(f"Unit {unit['variable']} must define a non-zero conversion multiplier")
                from_base_multiplier = 1 / to_base_multiplier

            from_base_offset = unit.get("from_base_offset")
            if from_base_offset is None:
                from_base_offset = -to_base_offset * from_base_multiplier

            normalized_units.append(
                {
                    **unit,
                    "to_base_multiplier": to_base_multiplier,
                    "to_base_offset": to_base_offset,
                    "from_base_multiplier": from_base_multiplier,
                    "from_base_offset": from_base_offset,
                }
            )

        normalized_configurations.append({**measurement, "units": normalized_units})

    return normalized_configurations



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

def generate_measurement_units(
    output_directory: Path, template_directory: Path, measurement_configurations: list[dict]
):
    env = Environment(
        loader=FileSystemLoader(template_directory),
        autoescape=False,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    unit_template = env.get_template("measurement_unit.py.jinja")
    helpers = {
        "file_name": file_name,
        "mtou": mtou,
    }

    for measurement in measurement_configurations:
        unit_file_name = file_name(measurement["name"])
        unit_contents = unit_template.render(
            measurement=measurement,
            measure_module=f"smartunits.measures.{file_name(measurement['name'])}",
            config=UNIT_CONFIGURATIONS,
            helpers=helpers,
        )
        output(output_directory, unit_file_name + ".py", unit_contents)

    output(output_directory, "__init__.py", "")


def generate_package_init(output_directory: Path, measurement_configurations: list[dict]):
    lazy_imports = {
        "Measure": ("smartunits.measure", "Measure"),
        "Unit": ("smartunits.unit", "Unit"),
        "UnaryFunction": ("smartunits.unary_function", "UnaryFunction"),
        "Units": ("smartunits.units", "Units"),
    }

    for measure_name in UNIT_CONFIGURATIONS:
        lazy_imports[measure_name] = (f"smartunits.measures.{file_name(measure_name)}", measure_name)

    for measurement in measurement_configurations:
        name = measurement["name"]
        unit_name = measurement["unit_type"]
        lazy_imports[unit_name] = (f"smartunits.{file_name(name)}", unit_name)

    lines = [
        "from importlib import import_module",
        "",
        "from .measure import Measure",
        "from .unit import Unit",
        "from .unary_function import UnaryFunction",
        "",
        "_LAZY_IMPORTS: dict[str, tuple[str, str]] = {",
    ]

    for name, (module_name, attribute_name) in lazy_imports.items():
        lines.append(f'    "{name}": ("{module_name}", "{attribute_name}"),')

    lines.extend(
        [
            "}",
            "",
            "",
            "def __getattr__(name: str):",
            "    if name in _LAZY_IMPORTS:",
            "        module_name, attribute_name = _LAZY_IMPORTS[name]",
            "        module = import_module(module_name)",
            "        value = getattr(module, attribute_name)",
            "        globals()[name] = value",
            "        return value",
            "    raise AttributeError(f\"module {__name__!r} has no attribute {name!r}\")",
            "",
            "",
            "__all__ = [\"Measure\", \"Unit\", \"UnaryFunction\", \"Units\"] + list(_LAZY_IMPORTS)",
        ]
    )

    output(output_directory, "__init__.py", "\n".join(lines) + "\n")


def generate_units(
    output_directory: Path, template_directory: Path, unit_output_directory: Path
):
    env = Environment(
        loader=FileSystemLoader(template_directory),
        autoescape=False,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    interface_template = env.get_template("measure_interface.py.jinja")
    root_path = output_directory
    script_directory = Path(__file__).resolve().parent

    math_units = load_json_file(script_directory / "unit_types.json")
    measurement_configurations = normalize_measurement_units(
        load_json_file(script_directory / "measurement_units.json")
    )

    helpers = {
        "type_vars": type_vars,
        "class_header": class_header,
        "type_usage": type_usage,
        "generics_list": generics_list,
        "generics_usage": generics_usage,
        "mtou": mtou,
        "indent": indent,
        "file_name": file_name,
    }

    init_imports = []
    init_all = []
    for unit_name in UNIT_CONFIGURATIONS:
        interface_contents = interface_template.render(
            name=unit_name,
            prefix="",
            math_units=math_units,
            config=UNIT_CONFIGURATIONS,
            helpers=helpers,
        )
        init_imports.append(f"from .{file_name(unit_name)} import {unit_name}")
        init_all.append(f"{unit_name}")

        output(root_path / "measures", file_name(unit_name) + ".py", interface_contents)

    output(
        root_path / "measures",
        "__init__.py",
        "\n".join(init_imports)
        + "\n\n__all__ = [\n    "
        + ",\n    ".join(f'\"{name}\"' for name in init_all)
        + "\n]",
    )

    generate_measurement_units(unit_output_directory, template_directory, measurement_configurations)
    generate_package_init(root_path, measurement_configurations)

def clean_output_directories(root_directory: Path, unit_output_directory: Path):
    """Remove generated files before generating new ones. Preserves measure.py, unit.py, and unary_function.py as they are the only non-generated files in the directory."""
    root_directory.mkdir(parents=True, exist_ok=True)

    protected_files = {"measure.py", "unit.py", "unary_function.py"}

    for path in root_directory.iterdir():
        if path.name == "measures" or path.name in protected_files:
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()

    measures_directory = root_directory / "measures"
    if measures_directory.exists():
        shutil.rmtree(measures_directory)
    measures_directory.mkdir(parents=True, exist_ok=True)

    if unit_output_directory.resolve() != root_directory.resolve():
        unit_output_directory.mkdir(parents=True, exist_ok=True)
        for path in unit_output_directory.iterdir():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()


def main():
    script_path = Path(__file__).resolve()
    dirname = script_path.parent

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_directory",
        help="Optional. If set, will output the generated files to this directory, otherwise it will use a path relative to the script",
        default=dirname.parent / "smartunits",
        type=Path,
    )
    parser.add_argument(
        "--template_root",
        help="Optional. If set, will use this directory as the root for the jinja templates",
        default=dirname / "templates",
        type=Path,
    )
    parser.add_argument(
        "--unit_output_directory",
        help="Optional. If set, will output generated measurement unit modules there",
        default=dirname.parent / "smartunits",
        type=Path,
    )
    args = parser.parse_args()

    clean_output_directories(args.output_directory, args.unit_output_directory)

    generate_units(args.output_directory, args.template_root, args.unit_output_directory)


if __name__ == "__main__":
    main()
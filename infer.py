#!/usr/bin/python3

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

TEMPLATE_TOML = """
[tool.poetry]
name = "{{project}}"
version = "0.1.0"
authors = {{authors}}
description = ""

[tool.poetry.dependencies]
python = "^{{version}}"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""


def extract_imports(file_path):
    """Extract import statements from a Python file."""
    with open(file_path, "r") as file:
        file_content = file.read()
    imports = re.findall(
        r"^\s*(?:from\s+(\w+)|import\s+(\w+))", file_content, re.MULTILINE
    )
    return {group for import_group in imports for group in import_group if group}


def find_external_modules(directory):
    """Find external modules imported in all Python files within the given directory."""
    standard_libs = sys.stdlib_module_names
    external_modules = set()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                imports = extract_imports(file_path)
                external_modules.update(imports - standard_libs)

    return external_modules


def create_requirements(directory, output_file="requirements.txt"):
    """Create requirements.txt for a given directory."""
    external_modules = find_external_modules(directory)
    with open(output_file, "w") as file:
        for module in sorted(external_modules):
            file.write(module + "\n")


# Create the parser
parser = argparse.ArgumentParser(description="Process some inputs.")

# Add the required arguments
parser.add_argument("input_dir", help="Path to the input directory")
parser.add_argument("output_dir", help="Path to the output directory")

# Add the optional arguments
parser.add_argument("-n", "--name", type=str, help="Name of the Project")
parser.add_argument("-a", "--authors", nargs="+", help="List of authors")
parser.add_argument("-p", "--py_version", type=str, help="Python Version number")
parser.add_argument(
    "-r",
    "--remove_reqs",
    action="store_true",
    help="Remove the requirements.txt file after generation",
)
parser.add_argument(
    "--norun",
    action="store_true",
    help="Doesn't run the poetry installation to generate a lock file"
    
)
# Parse the arguments
args = parser.parse_args()

# Store values in variables
input_dir = args.input_dir
output_dir = args.output_dir
author_names = ", ".join([f'\"{author}\"' for author in args.authors]) if args.authors is not None else ""
authors = f"[{author_names}]"
version = args.py_version if args.py_version is not None else "3.10"
name = args.name if args.name is not None else "project"
remove_reqs = args.remove_reqs if args.remove_reqs is not None else False
not_runnable = args.norun if args.norun is not None else False

input_dir_path = Path(input_dir)
output_dir_path = Path(output_dir)

# Create the requirements file in the output location
create_requirements(input_dir_path, output_file=(output_dir_path / "requirements.txt"))

# Make a pyproject.toml file
TEMPLATE_TOML = (
    TEMPLATE_TOML.replace("{{authors}}", authors)
    .replace("{{project}}", name)
    .replace("{{version}}", version)
)
with open(output_dir_path / "pyproject.toml", "w+") as outfile:
    outfile.write(TEMPLATE_TOML)

# Use the requirements to populate the pyproject.toml (runs by default)
if not not_runnable:
    subprocess.run(
        "cat requirements.txt | xargs poetry add", shell=True, cwd=output_dir_path
    )

if remove_reqs:
    os.remove(output_dir_path / "requirements.txt")

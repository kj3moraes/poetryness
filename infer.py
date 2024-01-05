#!/usr/bin/python3

import os
import sys
from pathlib import Path
import re
import subprocess


TEMPLATE_TOML = """
[tool.poetry]
name = "project"
version = "0.1.0"
authors = []
description = ""

[tool.poetry.dependencies]
python = "^3.10"


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


if len(sys.argv) < 3:
    print(
        "You must 2 arguments.\nUSAGE: python3 infer.py <input_dir_path> <output_dir_path>"
    )
    exit(1)

input_dir_path = Path(sys.argv[1])
output_dir_path = Path(sys.argv[2])

# Create the requirements file in the output location
create_requirements(input_dir_path, output_file=(output_dir_path / "requirements.txt"))

# Make a dummy pyproject.toml file
with open(output_dir_path / "pyproject.toml", "w+") as outfile:
    outfile.write(TEMPLATE_TOML)

# Use the requirements to populate the pyproject.toml
subprocess.run(
    "cat requirements.txt | xargs poetry add", shell=True, cwd=output_dir_path
)

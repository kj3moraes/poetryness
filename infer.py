import os
import sys
import pkgutil
from pathlib import Path
import re

def get_standard_library_list():
    """ Get a list of standard library modules. """
    std_lib = [module for _, module, _ in pkgutil.iter_modules()]
    return std_lib

def extract_imports(file_path):
    """ Extract import statements from a Python file. """
    with open(file_path, 'r') as file:
        file_content = file.read()
    imports = re.findall(r'^\s*(?:from\s+(\w+)|import\s+(\w+))', file_content, re.MULTILINE)
    return {group for import_group in imports for group in import_group if group}

def find_external_modules(directory):
    """ Find external modules imported in all Python files within the given directory. """
    standard_libs = sys.stdlib_module_names
    external_modules = set()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                imports = extract_imports(file_path)
                external_modules.update(imports - standard_libs)

    return external_modules

def create_requirements(directory, output_file='requirements.txt'):
    """ Create requirements.txt for a given directory. """
    external_modules = find_external_modules(directory)
    with open(output_file, 'w') as file:
        for module in sorted(external_modules):
            file.write(module + '\n')

# Example usage

dir_path = sys.argv[1]

directory_path = Path(dir_path) 

create_requirements(directory_path)

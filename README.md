# poetryness

Script to automate poetry's setup from existing projects. It will read all the .py files in a directory and make an "unpinned" requirements.txt
file and from this requirements.txt file, a base pyproject.toml file is generated and the dependencies are installed.

## Usage

This script will take an input directory that you want parsed and an output directory where the files 
will be written to.

* Will generate a requirements.txt file
* Will generate a pyproject.toml, poetry.lock file and a .venv directory in the output_dir_path

## Running the script

To use the script, simply navigate to this directory

```bash
./infer.py <input_dir_path> <output_dir_path>
```

Copy the infer.py to `~/.local/bin` and then you can run this anywhere on your system.


### Optional Arguments

There are some optional arguments that you can pass to the script to alter some of the behaviour:

- `-a` \ `--authors` allows you to specify the list of authors
- `-n` \ `--name` allows you to specify the project name 
- `-p` \ `--pyversion` allows you to specify the python version
- `--norun` will only generate the pyproject.toml but won't install anything
- `--remove_reqs` will remove the requirements.txt file after generation

You can also use the help command to get a quick glance of all the arguments

```bash
./infer.py --help
```

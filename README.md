# poetryness

Script to automate poetry's setup from existing projects.

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


## Caveats

There are some gotchas to using this script 

### pyproject.toml

- the author field is unpopulated
- the description is unpopulated
- the version is hardcoded to 0.1.0
- there is a default name for the project.

All of these can be fixed by manually editing the medata in the toml file.

### .venv

All the packages by design will be installed in the output directory. It does not make use of the
~/.cache directory where the poetry venvs usually go.

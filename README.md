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

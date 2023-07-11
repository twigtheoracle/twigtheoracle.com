import os
import pathlib

import subprocess

folder = pathlib.Path(os.getcwd())
file = "TAOCP Volume 1"
command = f"latexmlc --dest=\"{folder / file}.html\" \"{folder / file}.tex\""

subprocess.run(command, shell=True)
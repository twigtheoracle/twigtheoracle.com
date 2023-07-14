import os
import pathlib

import subprocess

import shutil

# Create the HTML file
# TODO: Multiple files
folder = pathlib.Path(os.getcwd())
file = "TAOCP Volume 1"
command = f"latexmlc --dest=\"{folder / file}.html\" \"{folder / file}.tex\""
subprocess.run(command, shell=True)

# Copy the generated style sheets
css_files = list(folder.glob("*.css"))
static_folder = folder.parent.parent.parent.parent / "static" / "mysite"
for css in css_files:
	shutil.copy(src=folder/css.name, dst=static_folder/css.name)

# In the HTML file, replace the css files with Django links to the static folder
file = file + ".html"
html_file = ""
with open(folder / file, "r", encoding="utf-8") as html:
	html_file = "\n".join(html.readlines())
for css in css_files:
	html_file = html_file.replace(css.name, f"{{% static 'mysite/{css.name}' %}}")
with open(folder / file, "w", encoding="utf-8") as html:
	html.write(r"{% load static %}")
	html.write("\n\n")
	html.write(html_file)
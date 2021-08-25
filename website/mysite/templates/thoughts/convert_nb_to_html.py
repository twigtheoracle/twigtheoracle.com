# Eric Liu
# 
# This script converts a given jupyter notebook to html. For the purposes of pathlib, it is assumed
# that this script is run from the directory it exists in.
# 
# Metadata stored in the head of the html file and is formatted as such:
# <meta name="creation-date" content="YYYY-MM-DD">
# <meta name="modification-date" content="YYYY-MM-DD">

import argparse
import datetime

from pathlib import Path

# stuff needed to convert ipynb to html
from bs4 import BeautifulSoup
from traitlets.config import Config
from nbconvert.exporters import HTMLExporter
from nbconvert import exporters

def main():
    """
    The main function controls all logic of the script

    :param:     N/A

    :return:    N/A
    """
    # command line arguments
    # there is only one, which is the name of the file to convert
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, nargs=1, metavar="str", required=True,
        help="The name of the jupyer notebook to convert to html. The file is assumed to be in "\
            "the folder \"templates/thoughts/\"")
    args = vars(parser.parse_args())

    # the path of the nb to convert
    path_ipynb = Path.cwd() / args["file"][0]

    # the path of the html file to convert to (this may already exist)
    path_html = path_ipynb.with_suffix(".html")

    # check if a converted file already exists
    if(path_html.is_file()):

        # convert the file again, but first find the original creation date
        with open(path_html) as f:
            soup = BeautifulSoup(f, "html.parser")
            cre_date = soup.find("meta", {"name": "creation-date"})

        # convert using the original creation date
        convert_to_html(path_ipynb, path_html, cre_date["content"])

    # if a converted file does not exist...
    else: 
        # convert the ipynb first then update metadata
        convert_to_html(path_ipynb, path_html)

def convert_to_html(ipynb_file, html_file, creation_date=None):
    """
    The convert_to_html file converts the input ipynb file to an html file, using the thoughts 
    tempalte. The resulting file is immediately able to be rendered using django

    :param:     ipynb_file      A pathlib.Path object containing the path to the ipynb file
    :param:     html_file       A pathlib.Path object containing the path to the html file. This is
                                where the converted file will be saved

    :return:    N/A
    """
    # converter config
    # see: https://nbconvert.readthedocs.io/en/latest/config_options.html# for more options
    c = Config()
    c.ExecutePreprocessor.enabled = True            # execute the notebook before converting
    c.NbConvertApp.export_format = "html"           # convert to html
    # c.TemplateExporter.template_name = "basic"      # do not include style

    # create and run the exporter
    output = HTMLExporter(config=c).from_filename(ipynb_file)[0]

    # convert the raw string output to a BeautifulSoup object
    soup = BeautifulSoup(output, "html.parser")

    # create the html file
    with open(html_file, "w") as f:
        # write the basic boilerplate stuff for the base template
        f.write(r'{% extends "base.html" %}')
        f.write(r"{% load static %}")
        f.write(r"{% block title %}" + html_file.stem + r"{% endblock %}")

        # write the jupyter notebook style to the head of the template
        f.write(r"{% block other-head %}")
        for tag in soup.head.contents:
            tag_contents = str(tag.encode("utf-8"))[2:-1].replace("\\n", "")
            try:
                if(tag_contents[0] == "<"):
                    f.write(tag_contents)
            except:
                pass

        # write the metadata to the head of the template
        f.write(f'<meta name="creation-date" content="{str(datetime.date.today())}">')
        if(creation_date == None):
            f.write(f'<meta name="modification-date" content="{str(datetime.date.today())}">')
        else:
            f.write(f'<meta name="modification-date" content="{creation_date}">')
        f.write(r"{% endblock %}")

        # the page title
        f.write(r"{% block pagetitle %}" + html_file.stem + r"{% endblock %}")

        # write the notebook content to the file
        f.write(r"{% block content %}")
        f.write(r'<div class=text-left>')
        no_header = soup.h1.decompose()
        for tag in soup.body.contents:
            tag_contents = str(tag.encode("utf-8"))[2:-1].replace(r"\n", "\n").replace(r"\xc2\xa0", " ")
            try:
                if(tag_contents[0] == "<"):
                    f.write(tag_contents)
            except:
                pass
        f.write(r"</div>")
        f.write(r"{% endblock %}")

    # # save the html output
    # with open(html_file, "wb") as f:
    #     f.write(output[0].encode("utf-8"))

if(__name__ == "__main__"):
    main()  
from django.shortcuts import render
from django.http import HttpResponse

# api key validation for stock_data page
import quandl
import datetime

# settings is needed to find the Stock-Data folder
from django.conf import settings

# stock-data script stuff
from shutil import copyfile
import sys
sys.path.insert(1, str(settings.SD_DIR))
from run import main
import os

# thoughts page stuff
from pathlib import Path
from bs4 import BeautifulSoup

def home(request):
    # the home page
    return render(request, "home.html")

def about(request):
    # about page
    return render(request, "about.html")

def projects(request):
    # projects page
    return render(request, "projects.html")

def stock_data(request):
    # stock data page

    if(request.method == "POST"):

        # store errors here
        errors = []

        # check that the api key is valid by making sure it can access both databases needed
        quandl.ApiConfig.api_key = request.POST["api-key"]

        # check the EOD database
        eod_works = True
        try:
            quandl.get("EOD/" + "AAPL", start_date=datetime.date(2021, 6, 8),
                end_date=datetime.date(2021, 6, 10))
        except quandl.errors.quandl_error.AuthenticationError:
            eod_works = False
            errors.append("The input API Key cannot access the EOD database")
        except quandl.errors.quandl_error.LimitExceededError:
            errors.append("Too many Quandl QPI requests, try again in 20 minutes.")

        # check the QOR database
        qor_works = True
        try:
            quandl.get("QOR/" + "AAPL", start_date=datetime.date(2021, 6, 8),
                end_date=datetime.date(2021, 6, 10))
        except quandl.errors.quandl_error.AuthenticationError:
            qor_works = False
            errors.append("The input API Key cannot access the QOR database")
        except quandl.errors.quandl_error.LimitExceededError:
            errors.append("Too many Quandl QPI requests, try again in 20 minutes.")

        # if the key works, then run the script with the provided stock list
        if(eod_works and qor_works):

            # remove extraneous characters from the new stock list
            stock_list = list(request.POST["new-sl"].split("\r\n"))

            # run the script

            # create the params file that Stock-Data looks for
            sd_params = {
                "config": str(settings.SD_DIR / "config/default.json"),
                "test": False,
                "overwrite": True,
                "quandl": [request.POST["api-key"]],
                "tickers": stock_list,
                "sd_root": str(settings.SD_DIR),
                "log": False
            }

            # run the script
            wb_path = main(sd_params)

            # make the output available
            web_path = os.path.join(str(settings.BASE_DIR / "static"), "xl", 
                os.path.basename(wb_path))
            copyfile(wb_path, web_path)

        return render(request, "projects/stock_data.html", 
            {
                "api_key": request.POST["api-key"], 
                "errors": errors,
                "output": os.path.join("/static/xl/", os.path.basename(wb_path))
            })

    return render(request, "projects/stock_data.html")

def thoughts(request):
    # thoughts page

    def get_dates(file_path):
        """
        The get_dates function takes the input html file path and uses beautiful soup to extract 
        and return the metadata date of creation and date of modification.

        :param:     file_path   A pathlib.Path object containing the path to the html file

        :return:    str         A string in format "YYYY-MM-DD" representing the date of creation 
        :return:    str         Same as above but date of modification
        """
        # use beautiful soup to get the creation date and modification date
        with open(file_path) as f:
            soup = BeautifulSoup(f, "html.parser")
            creation_date = soup.find("meta", {"name": "creation-date"})["content"]
            modification_date = soup.find("meta", {"name": "modification-date"})["content"]

            # return those dates
            return [creation_date, modification_date]

    # create the list of thoughts

    # the directory that thoughts are stored in 
    thoughts_dir = settings.BASE_DIR / "mysite" / "templates" / "thoughts"

    # find all html files in the thoughts dir
    html_files = list(thoughts_dir.glob("**/*.html"))

    # store the thoughts list here
    thought_list = []

    # for each html file, get the creation date and modification date
    for html_file in html_files:
        creation_date, modification_date = get_dates(thoughts_dir / html_file)
        thought_list.append([creation_date, modification_date, html_file.stem])

    return render(request, "thoughts.html", {"thought_list": thought_list})

def specific_thought(request, **kwargs):

    return render(request, f"thoughts/{kwargs['thought_name']}.html")
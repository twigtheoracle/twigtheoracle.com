from django.shortcuts import render
from django.http import HttpResponse

# api key validation for stock_data page
import nasdaqdatalink
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

# To read the metadata csv file
import pandas as pd
import datetime

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
        nasdaqdatalink.ApiConfig.api_key = request.POST["api-key"]

        # check the EOD database
        eod_works = True
        try:
            nasdaqdatalink.get("EOD/" + "AAPL", start_date=datetime.date(2021, 6, 8),
                end_date=datetime.date(2021, 6, 10))
        # except nasdaqdatalink.errors.quandl_error.AuthenticationError:
        #     eod_works = False
        #     errors.append("The input API Key cannot access the EOD database")
        # except nasdaqdatalink.errors.quandl_error.LimitExceededError:
        #     errors.append("Too many Quandl QPI requests, try again in 20 minutes.")
        except:
            pass

        # check the QOR database
        qor_works = True
        try:
            nasdaqdatalink.get("QOR/" + "AAPL", start_date=datetime.date(2021, 6, 8),
                end_date=datetime.date(2021, 6, 10))
        # except nasdaqdatalink.errors.quandl_error.AuthenticationError:
        #     qor_works = False
        #     errors.append("The input API Key cannot access the QOR database")
        # except quandl.errors.quandl_error.LimitExceededError:
        #     errors.append("Too many Quandl QPI requests, try again in 20 minutes.")
        except:
            pass

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

def specific_project(request, *args, **kwargs):

    requested_url = "/".join(args)
    return render(request, f"projects/{requested_url}.html")

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
        with open(file_path, errors="ignore") as f:
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

def casual_music_reviews(request):
    # Casual Music Reviews page

    # Get the list of music reviews from the metadata file
    metadata_path = settings.BASE_DIR / "mysite" / "templates" / "projects" / "casual_music_reviews" / "metadata.csv"
    metadata = pd.read_csv(metadata_path)

    # Convert the date created/modified into actual date strings. Keep a copy of raw 
    # string values for sorting later
    for date_column in ["date_created", "date_modified"]:
        metadata[date_column + "_sort"] = metadata[date_column] 
        metadata[date_column] = (
            pd.to_datetime(metadata[date_column], format="%Y%m%d")
            .dt
            .strftime("%B %d, %Y")
        )

    # If the date created/modified are the same, replace the modified date with "N/A"
    metadata.loc[metadata["date_created"] == metadata["date_modified"], "date_modified"] = "N/A"

    # If no file is provided, that means we use the default format, a combination of the
    # artist and title
    metadata["default_file"] = (metadata["artist"] + " " + metadata["title"]).str.replace(" ", "_").str.lower()
    metadata["file"] = metadata["file"].fillna(metadata["default_file"])
    metadata = metadata.drop(columns=["default_file"])

    # Return the page
    metadata = metadata[[
        "date_created", 
        "date_created_sort", 
        "date_modified", 
        "date_modified_sort",
        "artist",
        "title",
        "genre",
        "rating",
        "file",
    ]]
    return render(request, "projects/casual_music_reviews.html", {"metadata": metadata.values.tolist()})

def specific_review(request, **kwargs):
    # Get a specific review

    # Store template stuff for the review page here
    template = {}

    # Get the list of music reviews from the metadata file
    metadata_path = settings.BASE_DIR / "mysite" / "templates" / "projects" / "casual_music_reviews" / "metadata.csv"
    metadata = pd.read_csv(metadata_path)

    # If no file is provided, that means we use the default format, a combination of the
    # artist and title
    metadata["default_file"] = (metadata["artist"] + " " + metadata["title"]).str.replace(" ", "_").str.lower()
    metadata["file"] = metadata["file"].fillna(metadata["default_file"])
    metadata = metadata.drop(columns=["default_file"])

    # Sort by the date created column
    metadata = metadata.sort_values(by="date_created", ascending=True)

    # Convert date strings to actual dates
    for date_column in ["date_created", "date_modified"]:
        metadata[date_column] = pd.to_datetime(metadata[date_column], format="%Y%m%d")

    # Find the metadata for the current review
    this_review_metadata = metadata[metadata["file"] == kwargs["review"]].to_dict("records")[0]

    # Find the file path for the previous review
    all_previous_reviews = metadata[metadata["date_created"] < this_review_metadata["date_created"]]
    if all_previous_reviews.shape[0] > 0:
        previous_review_metadata = all_previous_reviews.loc[all_previous_reviews["date_created"].idxmax()].to_dict()
        template["previous_review"] = previous_review_metadata["file"]
    else:
        template["previous_review"] = None

    # Find the file path for the next review
    all_next_reviews = metadata[metadata["date_created"] > this_review_metadata["date_created"]]
    if all_next_reviews.shape[0] > 0:
        next_review_metadata = all_next_reviews.loc[all_next_reviews["date_created"].idxmin()].to_dict()
        template["next_review"] = next_review_metadata["file"]
    else:
        template["next_review"] = None

    # Convert the date created/modified of the current review into actual date strings
    for date_key in ["date_created", "date_modified"]:
        this_review_metadata[date_key] = this_review_metadata[date_key].strftime("%B %d, %Y")

    # If the date created/modified are the same, replace the modified date with "N/A"
    if this_review_metadata["date_created"] == this_review_metadata["date_modified"]:
        this_review_metadata["date_modified"] = "N/A"

    # Combine the artist and title together for this review
    this_review_metadata["artist_title"] = f"{this_review_metadata['artist']} - {this_review_metadata['title']}"

    # Get all the necessary key/value pairs for the template
    for key in ["artist_title", "date_created", "date_modified", "genre", "rating"]:
        template[key] = this_review_metadata[key]

    # Customize the metadata for the specific review
    return render(request, f"projects/casual_music_reviews/{kwargs['review']}.html", template)

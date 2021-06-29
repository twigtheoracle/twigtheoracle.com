from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

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
    return render(request, "stock_data.html")
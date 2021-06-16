from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def home(request):
    # the home page
    return HttpResponse("The home page.")

def about(request):
    # about page
    return render(request, "about.html")
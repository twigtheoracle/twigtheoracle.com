from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("projects", views.projects, name="projects"),
    path("projects/stock_data", views.stock_data, name="stock_data"),
    path("thoughts", views.thoughts, name="thoughts"),
    path("thoughts/<thought_name>", views.specific_thought, name="specific_thought")
]
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("projects", views.projects, name="projects"),
    path("projects/stock_data", views.stock_data, name="stock_data"),
    path("projects/casual_music_reviews", views.casual_music_reviews, name="casual_music_reviews"),
    path("projects/casual_music_reviews/<review>", views.specific_review, name="specific_review"),
    re_path("projects/(.+)", views.specific_project, name="specific_project"),
    path("thoughts", views.thoughts, name="thoughts"),
    path("thoughts/<thought_name>", views.specific_thought, name="specific_thought"),
]
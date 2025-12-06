from django.urls import path
from .views import home, add_movie, delete_movie

urlpatterns = [
    path("", home, name="home"),
    path("add/", add_movie, name="add_movie"),
    path("delete/<int:id>/", delete_movie, name="delete_movie"),
]

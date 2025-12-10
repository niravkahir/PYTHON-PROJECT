from django.urls import path
from . import views     # import views file completely
from django.contrib.auth import views as auth_views  # <-- add this

app_name = "movie_app"

urlpatterns = [
    path("", views.home, name="home"),
    path("add_movie/", views.add_movie, name="add_movie"),
    path("movie/<int:pk>/", views.movie_detail, name="movie_detail"),
    path("movie/<int:pk>/watchlist-toggle/", views.watchlist_toggle, name="watchlist_toggle"),
    path("my-watchlist/", views.my_watchlist, name="my_watchlist"),
    path("delete/<int:id>/", views.delete_movie, name="delete_movie"),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Login URL
]

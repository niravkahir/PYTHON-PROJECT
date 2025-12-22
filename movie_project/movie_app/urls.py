from django.urls import path
from . import views

app_name = 'movie_app'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('user-home/', views.user_home, name='user_home'),
    path('admin-home/', views.admin_home, name='admin_home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Movies
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('add-movie/', views.add_movie, name='add_movie'),
    path('delete-movie/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    
    # User features
    path('watchlist/', views.watchlist, name='watchlist'),
    path('watchlist/toggle/<int:movie_id>/', views.watchlist_toggle, name='watchlist_toggle'),
    path('review/<int:movie_id>/', views.review_form, name='review_form'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    
    # Special features
    path('content-request/', views.content_request, name='content_request'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
]
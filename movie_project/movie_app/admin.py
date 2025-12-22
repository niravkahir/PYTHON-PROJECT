from django.contrib import admin
from .models import Movie, Watchlist, Review, UserProfile, ContentRequest

admin.site.register(Movie)
admin.site.register(Watchlist)
admin.site.register(Review)
admin.site.register(UserProfile)
admin.site.register(ContentRequest)
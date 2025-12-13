

# Register your models here.

from django.contrib import admin
from .models import Movie, Person, Watchlist

admin.site.register(Movie)
admin.site.register(Person)
admin.site.register(Watchlist)
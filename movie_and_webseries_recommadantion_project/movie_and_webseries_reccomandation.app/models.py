from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100, blank=True)
    rating = models.FloatField(null=True, blank=True)
    poster_url = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    creators = models.ManyToManyField(Person, related_name="created_movies", blank=True)
    stars = models.ManyToManyField(Person, related_name="starred_movies", blank=True)

    def __str__(self):
        return self.title

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_items")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="in_watchlists")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie")

    def __str__(self):
        return f"{self.user.username} → {self.movie.title}"


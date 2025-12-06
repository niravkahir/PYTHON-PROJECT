from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    rating = models.FloatField()
    poster_url = models.CharField(max_length=300, default="", blank=True)

    def __str__(self):
        return self.title

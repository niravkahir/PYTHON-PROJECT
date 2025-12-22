from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    description = models.TextField(blank=True)
    poster_url = models.URLField(blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=50, default='English')
    director = models.CharField(max_length=200, blank=True)
    duration = models.IntegerField(blank=True, null=True)  # in minutes
    
    def __str__(self):
        return self.title

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'movie']
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['movie', 'user']
    
    def __str__(self):
        return f"{self.user.username}'s review of {self.movie.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    is_golden_user = models.BooleanField(default=False)
    role = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class ContentRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    request_type = models.CharField(max_length=20, default='new')
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Request: {self.title} by {self.user.username}"
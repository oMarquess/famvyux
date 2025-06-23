from django.db import models
from django.conf import settings

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=4)  # Assuming year is always in YYYY format
    imdb_rating = models.CharField(max_length=4, blank=True, null=True)  # IMDb rating
    metascore = models.CharField(max_length=3, null=True, blank=True)  # Metascore
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)  # Description of the movie
    
    # New API fields
    genre = models.CharField(max_length=255, blank=True, null=True)
    plot = models.TextField(blank=True, null=True)  # Detailed plot from API
    director = models.CharField(max_length=255, blank=True, null=True)
    actors = models.TextField(blank=True, null=True)  # Comma-separated actors
    runtime = models.CharField(max_length=20, blank=True, null=True)  # e.g., "120 min"
    
    # API identifiers
    tmdb_id = models.IntegerField(blank=True, null=True, unique=True)  # TMDb ID
    imdb_id = models.CharField(max_length=20, blank=True, null=True)  # IMDb ID (e.g., tt1234567)
    
    # Additional ratings
    tmdb_rating = models.FloatField(blank=True, null=True)  # TMDb rating (0-10)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_from_api = models.BooleanField(default=False)  # Track if movie came from API

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    @property
    def primary_rating(self):
        """Return the best available rating"""
        if self.imdb_rating and self.imdb_rating != 'N/A':
            return f"IMDb: {self.imdb_rating}"
        elif self.tmdb_rating:
            return f"TMDb: {self.tmdb_rating}/10"
        return "No rating"
    
    @property
    def poster_url(self):
        """Return image URL or placeholder"""
        return self.image_url or "/static/assets/img/movie-placeholder.jpg"

class Suggestion(models.Model):
    suggested_title = models.CharField(max_length=255)
    description = models.TextField(verbose_name="Your rating, eg. Mood, etc.")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggestion for {self.suggested_title} by {self.user.username if self.user else 'Anonymous'}"

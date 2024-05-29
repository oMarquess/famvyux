from django.db import models
from django.conf import settings

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=4)  # Assuming year is always in YYYY format
    imdb_rating = models.CharField(max_length=4)  # IMDb rating
    metascore = models.CharField(max_length=3)  # Metascore
    image_url = models.URLField()
    description = models.TextField()  # Description of the movie

    def __str__(self):
        return self.title

class Suggestion(models.Model):
    suggested_title = models.CharField(max_length=255)
    description = models.TextField(verbose_name="Your rating, eg. Mood, etc.")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggestion for {self.suggested_title} by {self.user.username}"

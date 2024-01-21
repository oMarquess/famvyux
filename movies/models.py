from django.db import models
from django.conf import settings

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=255)
    image_url = models.URLField(default='')
    year = models.CharField(max_length=4)  # Assuming year is always in YYYY format
    duration = models.CharField(max_length=10)  # Example: '3h 1m'
    star_rating = models.DecimalField(max_digits=3, decimal_places=1)  # Example: 8.0
    rate_count = models.CharField(max_length=100, blank=True, null=True)  # Rate count can be optional
    product_url = models.URLField(default='')

    def __str__(self):
        return self.title

class Suggestion(models.Model):
    suggested_title = models.CharField(max_length=255)
    description = models.TextField(verbose_name="Your rating, eg. Mood, etc.")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggestion for {self.suggested_title} by {self.user.username}"

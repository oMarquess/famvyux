from django.db import models
from django.conf import settings
from movies.models import Movie

class MovieRating(models.Model):
    # Basic rating information
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    overall_rating = models.IntegerField()  # Rating out of 10

    AGE_RECOMMENDATION_CHOICES = [
    ('ALL', 'All Ages'),
    ('CHILD', 'Children'),
    ('TEEN', 'Teens'),
    ('ADULT', 'Adults'),
    ]

    # Age recommendation
    age_recommendation = models.CharField(max_length=100, choices=AGE_RECOMMENDATION_CHOICES, default='ALL')  # e.g., "10+", "Teens"

    # Mood/Type of the movie
    MOOD_CHOICES = [
    ('Fun', 'Fun'),
    ('Comedy', 'Comedy'),
    ('Light-Hearted', 'Light-Hearted'),
    ('Romantic', 'Romantic'),
    ('Dramatic', 'Dramatic'),
    ('Suspenseful', 'Suspenseful'),
    ('Heartwarming', 'Heartwarming'),
    ('Inspirational', 'Inspirational'),
    ('Sad', 'Sad'),
    ('Melancholic', 'Melancholic'),
    ('Nostalgic', 'Nostalgic'),
    ('Fantasy', 'Fantasy'),
    ('Mysterious', 'Mysterious'),
    ('Action-Packed', 'Action-Packed'),
    ('Adventurous', 'Adventurous'),
    ('Documentary', 'Documentary'),
    ('Educational', 'Educational'),
    ('Artistic', 'Artistic'),
    ('Family-Friendly', 'Family-Friendly'),
    ('Dark/Horror', 'Dark/Horror'),
    ('Sci-Fi', 'Sci-Fi'),
    ('Epic', 'Epic')
]

    mood_type = models.CharField(max_length=500, choices=MOOD_CHOICES)

    # Theme/Life lessons
    THEME_CHOICES = [
    ('Coming of Age', 'Coming of Age'),
    ('Love and Relationships', 'Love and Relationships'),
    ('Good vs. Evil', 'Good vs. Evil'),
    ('Social Injustice', 'Social Injustice'),
    ('Self-Discovery', 'Self-Discovery'),
    ('Technology and Society', 'Technology and Society'),
    ('War and Peace', 'War and Peace'),
    ('Crime and Justice', 'Crime and Justice'),
    ('Cultural Diversity', 'Cultural Diversity'),
    ('Historical Reflection', 'Historical Reflection'),
    ('Political Intrigue', 'Political Intrigue'),
    ('Spirituality and Faith', 'Spirituality and Faith'),
    ('Ethics and Morality', 'Ethics and Morality'),
    ('Adventure and Exploration', 'Adventure and Exploration'),
]

    theme_label = models.CharField(max_length=50, choices=THEME_CHOICES)  # Predefined labels
    theme_description = models.TextField(max_length=2000, verbose_name="theme description", default='')  # Open-ended description

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')  # Ensure one rating per user per movie

    def __str__(self):
        return f"{self.user.username}'s rating for {self.movie.title}"

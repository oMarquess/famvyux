
import json
import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from movies.models import Movie 
from ratings.models import MovieRating 
from faker import Faker
User = get_user_model()
faker = Faker()


class Command(BaseCommand):
    help = 'Generates fake users and their movie ratings'

    def add_arguments(self, parser):
        parser.add_argument('num_users', type=int, help='Number of fake users to create')

    def handle(self, *args, **kwargs):
        num_users = kwargs['num_users']
        self.generate_fake_users(num_users)
        self.assign_movie_ratings()
    
    def generate_fake_users(self, num_users):
        User = get_user_model()
        created_count = 0

        while created_count < num_users:

            username = faker.user_name()
            email = faker.email()
            # Check if the username already exists
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, email=email)
                created_count += 1


    def assign_movie_ratings(self):
        movies = Movie.objects.all()
        mood_choices = [choice[0] for choice in MovieRating.MOOD_CHOICES]
        theme_choices = [choice[0] for choice in MovieRating.THEME_CHOICES]
        age_recommendations = [choice[0] for choice in MovieRating.AGE_RECOMMENDATION_CHOICES]

        for movie in movies:

            for user in User.objects.all():
                # Check if the user has already rated this movie
                if not MovieRating.objects.filter(user=user, movie=movie).exists():
                    MovieRating.objects.create(
                        user=user,
                        movie=movie,
                        overall_rating=random.randint(1, 10),
                        mood_type=random.choice(mood_choices),
                        theme_label=random.choice(theme_choices),
                        age_recommendation=random.choice(age_recommendations)
                        # Add additional fields if needed
                    )



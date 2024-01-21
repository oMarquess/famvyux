from django.core.management.base import BaseCommand
from django.db.models import Avg
from movies.models import Movie
from ratings.models import MovieRating

class Command(BaseCommand):
    help = 'Calculate the average rating for each movie'

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()
        MIN_RATINGS_REQUIRED = 1  # Set minimum number of ratings required for average calculation

        for movie in movies:
            try:
                ratings = MovieRating.objects.filter(movie=movie)
                ratings_count = ratings.count()
                average_rating = ratings.aggregate(Avg('overall_rating'))
                avg_rating = average_rating['overall_rating__avg']

                if ratings_count >= MIN_RATINGS_REQUIRED and avg_rating is not None:
                    movie.average_rating = avg_rating
                    movie.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated average rating for {movie.title} to {avg_rating}'))
                else:
                    movie.average_rating = None  # or a default value
                    movie.save()
                    self.stdout.write(f'No sufficient ratings for {movie.title}')
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error updating movie {movie.title}: {e}'))

        self.stdout.write(self.style.SUCCESS('Average rating calculation completed.'))

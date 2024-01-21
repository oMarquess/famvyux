from django.contrib import admin
#from django.db.models import Avg, Count, Max
from ratings.models import MovieRating
#from movies.models import Movie

admin.site.register(MovieRating)
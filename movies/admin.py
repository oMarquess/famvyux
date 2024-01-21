from django.contrib import admin
from django.db.models import Avg, Count, Max
from ratings.models import MovieRating
from movies.models import Movie, Suggestion

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'average_rating', 'rating_count', 'last_rating_date')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _average_rating=Avg('movierating__overall_rating'),
            _rating_count=Count('movierating'),
            _last_rating_date=Max('movierating__created_at')
        )

    def average_rating(self, obj):
        return obj._average_rating
    average_rating.admin_order_field = '_average_rating'

    def rating_count(self, obj):
        return obj._rating_count
    rating_count.admin_order_field = '_rating_count'

    def last_rating_date(self, obj):
        return obj._last_rating_date
    last_rating_date.admin_order_field = '_last_rating_date'

admin.site.register(Movie, MovieAdmin)
admin.site.register(Suggestion)
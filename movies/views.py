from django.shortcuts import render, redirect, get_object_or_404
from movies.models import Movie, Suggestion
from ratings.models import MovieRating
from django.db.models import Avg, Count, Max
from .forms import SuggestionForm
from django.contrib import messages
from collections import Counter

import random
import wikipediaapi
#from movies.utils import get_movie_description

def index(request):
    all_movies = list(Movie.objects.all())
    random_movies = random.sample(all_movies, min(len(all_movies), 6))

    movies_with_ratings = []
    for movie in random_movies:
        ratings = MovieRating.objects.filter(movie=movie)

        if ratings.exists():
            average_rating = ratings.aggregate(Avg('overall_rating'))['overall_rating__avg']
            # Additional aggregated data
            mood_types = list(ratings.values_list('mood_type', flat=True).distinct())
            age_recommendations = list(ratings.values_list('age_recommendation', flat=True).distinct())
            theme_labels = list(ratings.values_list('theme_label', flat=True).distinct())
        else:
            average_rating = 'No ratings yet'
            mood_types, age_recommendations, theme_labels = [], [], []

        movies_with_ratings.append({
            'movie': movie,
            'title': movie.title,
            'year': movie.year,
            'duration': movie.duration,
            'star_rating': movie.star_rating,
            'average_rating': average_rating,
            #'mood_types': mood_types,
            #'age_recommendations': age_recommendations,
            #'theme_labels': theme_labels,
            'image_url': movie.image_url if movie.image_url else None
        })

    return render(request, 'index.html', {'movies_with_ratings': movies_with_ratings})



def search_results(request):
    query = request.GET.get('query', '')
    form = SuggestionForm()  # Instantiate the form

    if query:
        movies = Movie.objects.filter(title__icontains=query) | Movie.objects.filter(year__icontains=query)

        if not movies.exists(): 
             # No movies found

            return redirect('suggestion')

        return render(request, 'search_results.html', {'movies': movies, 'query': query})
    
    return redirect('index')


# def suggestion_thank(request):
#     return render(requets, 'suggestion_thankyou.html')


def suggestion_view(request):
    if request.method == 'POST':

        user = request.user if request.user.is_authenticated else None

        # Retrieve form data from request.POST
        suggested_title = request.POST.get('suggested_title')
        description = request.POST.get('description')
        
        # Optionally, validate the data

        # Create and save the suggestion
        Suggestion.objects.create(
            suggested_title=suggested_title,
            description=description,
            user=request.user
        )

        messages.success(request, 'Your suggestion has been submitted.')
        return redirect('home')  # Redirect to the home page or another appropriate page

    return render(request, 'suggestion_form.html')  # Render the suggestion form page



def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    ratings = MovieRating.objects.filter(movie=movie)

    # Mood types and theme labels
    mood_types = Counter(ratings.values_list('mood_type', flat=True))
    theme_labels = Counter(ratings.values_list('theme_label', flat=True))

    total_ratings = ratings.count()

    # Get top two mood types and theme labels
    top_mood_types = mood_types.most_common(2)
    top_theme_labels = theme_labels.most_common(2)

    # Calculate percentages
    mood_type_percentages = {mood: (count / total_ratings * 100) for mood, count in top_mood_types}
    theme_label_percentages = {label: (count / total_ratings * 100) for label, count in top_theme_labels}

    # Average age recommendation
    avg_age_recommendation = ratings.aggregate(Avg('age_recommendation'))['age_recommendation__avg']

    context = {
        'movie': movie,
        'mood_type_percentages': mood_type_percentages,
        'theme_label_percentages': theme_label_percentages,
        'average_age_recommendation': avg_age_recommendation,
        # Other context data as needed
    }
    return render(request, 'movie_details.html', context)

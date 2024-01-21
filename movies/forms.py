from django import forms
from movies.models import Movie
#from ratings.models import MovieRating

from django import forms

class SuggestionForm(forms.Form):
    suggested_title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))


# class MovieRatingForm(forms.ModelForm):
#     class Meta:
#         model = MovieRating
#         fields = ['overall_rating', 'age_recommendation', 'mood_type', 'theme_label', 'theme_description']

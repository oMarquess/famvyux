from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.index, name='home'),
    path('search/', views.search_results, name='search_results'),
    path('suggestion/', views.suggestion_view, name='suggestion'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name = 'about')
]



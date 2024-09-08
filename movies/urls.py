from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.index, name='home'),
    path('search/', views.search_results, name='search_results'),
    path('suggestion/', views.suggestion_view, name='suggestion'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('contact/', views.contact, name='contact'),
    #path('blog/', views.blog, name='blog'),
    path('about/', views.about, name='about'),
    #path('services/', views.services, name='services'),
    #path('service_details/', views.service_details, name='service_details'),
    path('add_movie/', views.add_view, name = 'add-movie'),
    path('serper/', views.search_view, name = 'search_view')
]



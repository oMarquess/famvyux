import requests
import os
from django.conf import settings
from django.core.cache import cache
from .models import Movie

class MovieAPIService:
    def __init__(self):
        self.tmdb_api_key = os.getenv('TMDB_API_KEY', '')
        self.omdb_api_key = os.getenv('OMDB_API_KEY', '')
        self.tmdb_base_url = "https://api.themoviedb.org/3"
        self.omdb_base_url = "http://www.omdbapi.com/"
        self.image_base_url = "https://image.tmdb.org/t/p/w500"

    def get_popular_movies(self, page=1):
        """Get popular movies from TMDb"""
        cache_key = f"popular_movies_page_{page}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        try:
            url = f"{self.tmdb_base_url}/movie/popular"
            params = {
                'api_key': self.tmdb_api_key,
                'page': page,
                'language': 'en-US'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Cache for 1 hour
            cache.set(cache_key, data, 3600)
            return data
            
        except requests.RequestException as e:
            print(f"Error fetching popular movies: {e}")
            return None

    def get_latest_movies(self, page=1):
        """Get now playing movies from TMDb"""
        cache_key = f"latest_movies_page_{page}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        try:
            url = f"{self.tmdb_base_url}/movie/now_playing"
            params = {
                'api_key': self.tmdb_api_key,
                'page': page,
                'language': 'en-US',
                'region': 'US'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Cache for 30 minutes
            cache.set(cache_key, data, 1800)
            return data
            
        except requests.RequestException as e:
            print(f"Error fetching latest movies: {e}")
            return None

    def get_top_rated_movies(self, page=1):
        """Get top rated movies from TMDb"""
        cache_key = f"top_rated_movies_page_{page}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        try:
            url = f"{self.tmdb_base_url}/movie/top_rated"
            params = {
                'api_key': self.tmdb_api_key,
                'page': page,
                'language': 'en-US'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Cache for 2 hours
            cache.set(cache_key, data, 7200)
            return data
            
        except requests.RequestException as e:
            print(f"Error fetching top rated movies: {e}")
            return None

    def get_movie_details(self, tmdb_id):
        """Get detailed movie information from TMDb"""
        cache_key = f"movie_details_{tmdb_id}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        try:
            url = f"{self.tmdb_base_url}/movie/{tmdb_id}"
            params = {
                'api_key': self.tmdb_api_key,
                'language': 'en-US',
                'append_to_response': 'credits,reviews,videos'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Cache for 24 hours
            cache.set(cache_key, data, 86400)
            return data
            
        except requests.RequestException as e:
            print(f"Error fetching movie details: {e}")
            return None

    def search_movies(self, query, page=1):
        """Search movies from TMDb"""
        cache_key = f"search_movies_{query}_page_{page}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        try:
            url = f"{self.tmdb_base_url}/search/movie"
            params = {
                'api_key': self.tmdb_api_key,
                'query': query,
                'page': page,
                'language': 'en-US'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Cache for 15 minutes
            cache.set(cache_key, data, 900)
            return data
            
        except requests.RequestException as e:
            print(f"Error searching movies: {e}")
            return None

    def get_omdb_details(self, imdb_id=None, title=None):
        """Get movie details from OMDb (includes IMDb ratings)"""
        if not imdb_id and not title:
            return None
            
        cache_key = f"omdb_{imdb_id or title}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        try:
            params = {
                'apikey': self.omdb_api_key,
                'plot': 'full',
                'r': 'json'
            }
            
            if imdb_id:
                params['i'] = imdb_id
            else:
                params['t'] = title
                
            response = requests.get(self.omdb_base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('Response') == 'True':
                # Cache for 24 hours
                cache.set(cache_key, data, 86400)
                return data
            else:
                return None
                
        except requests.RequestException as e:
            print(f"Error fetching OMDb details: {e}")
            return None

    def format_movie_data(self, tmdb_movie, omdb_data=None):
        """Format movie data for database storage"""
        formatted_data = {
            'title': tmdb_movie.get('title', ''),
            'year': tmdb_movie.get('release_date', '')[:4] if tmdb_movie.get('release_date') else '',
            'genre': ', '.join([g['name'] for g in tmdb_movie.get('genres', [])]),
            'plot': tmdb_movie.get('overview', ''),
            'image_url': f"{self.image_base_url}{tmdb_movie.get('poster_path', '')}" if tmdb_movie.get('poster_path') else '',
            'tmdb_rating': tmdb_movie.get('vote_average', 0),
            'tmdb_id': tmdb_movie.get('id'),
        }
        
        if omdb_data:
            formatted_data.update({
                'imdb_rating': omdb_data.get('imdbRating', ''),
                'imdb_id': omdb_data.get('imdbID', ''),
                'metascore': omdb_data.get('Metascore', ''),
                'director': omdb_data.get('Director', ''),
                'actors': omdb_data.get('Actors', ''),
                'runtime': omdb_data.get('Runtime', ''),
            })
            
        return formatted_data

    def sync_latest_movies_to_db(self, limit=20):
        """Sync latest movies from API to database"""
        latest_data = self.get_latest_movies()
        
        if not latest_data or 'results' not in latest_data:
            return False
            
        synced_count = 0
        
        for movie_data in latest_data['results'][:limit]:
            try:
                # Check if movie already exists
                if Movie.objects.filter(tmdb_id=movie_data.get('id')).exists():
                    continue
                    
                # Get additional details from OMDb if available
                omdb_data = None
                if movie_data.get('title'):
                    omdb_data = self.get_omdb_details(title=movie_data['title'])
                
                # Format and save movie
                formatted_data = self.format_movie_data(movie_data, omdb_data)
                
                movie = Movie(**formatted_data)
                movie.save()
                
                synced_count += 1
                
            except Exception as e:
                print(f"Error syncing movie {movie_data.get('title', 'Unknown')}: {e}")
                continue
                
        return synced_count

# Convenience function to get service instance
def get_movie_api_service():
    return MovieAPIService() 
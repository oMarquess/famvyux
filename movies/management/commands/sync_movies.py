from django.core.management.base import BaseCommand
from movies.services import get_movie_api_service
from movies.models import Movie

class Command(BaseCommand):
    help = 'Sync latest movies from external APIs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=20,
            help='Number of movies to sync (default: 20)'
        )
        parser.add_argument(
            '--type',
            type=str,
            default='latest',
            choices=['latest', 'popular', 'top_rated'],
            help='Type of movies to sync (default: latest)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force sync even if movies already exist'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        movie_type = options['type']
        force = options['force']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting sync of {limit} {movie_type} movies...')
        )
        
        api_service = get_movie_api_service()
        
        # Check if API keys are configured
        if not api_service.tmdb_api_key:
            self.stdout.write(
                self.style.ERROR('TMDb API key not found. Please set TMDB_API_KEY in your environment.')
            )
            return
        
        try:
            # Get movies based on type
            if movie_type == 'latest':
                movies_data = api_service.get_latest_movies()
            elif movie_type == 'popular':
                movies_data = api_service.get_popular_movies()
            elif movie_type == 'top_rated':
                movies_data = api_service.get_top_rated_movies()
            
            if not movies_data or 'results' not in movies_data:
                self.stdout.write(
                    self.style.ERROR('Failed to fetch movies from API')
                )
                return
            
            synced_count = 0
            skipped_count = 0
            error_count = 0
            
            for movie_data in movies_data['results'][:limit]:
                try:
                    tmdb_id = movie_data.get('id')
                    title = movie_data.get('title', 'Unknown')
                    
                    # Check if movie already exists (unless force is True)
                    if not force and Movie.objects.filter(tmdb_id=tmdb_id).exists():
                        skipped_count += 1
                        self.stdout.write(f'Skipped: {title} (already exists)')
                        continue
                    
                    # Get detailed movie info
                    detailed_movie = api_service.get_movie_details(tmdb_id)
                    if not detailed_movie:
                        error_count += 1
                        self.stdout.write(
                            self.style.WARNING(f'Failed to get details for: {title}')
                        )
                        continue
                    
                    # Get OMDb data for additional ratings
                    omdb_data = None
                    if api_service.omdb_api_key and title:
                        omdb_data = api_service.get_omdb_details(title=title)
                    
                    # Format movie data
                    formatted_data = api_service.format_movie_data(detailed_movie, omdb_data)
                    formatted_data['is_from_api'] = True
                    
                    # Create or update movie
                    if force:
                        movie, created = Movie.objects.update_or_create(
                            tmdb_id=tmdb_id,
                            defaults=formatted_data
                        )
                        action = 'Created' if created else 'Updated'
                    else:
                        movie = Movie.objects.create(**formatted_data)
                        action = 'Created'
                    
                    synced_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'{action}: {title} ({movie.year})')
                    )
                    
                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'Error processing {title}: {str(e)}')
                    )
                    continue
            
            # Summary
            self.stdout.write('\n' + '='*50)
            self.stdout.write(
                self.style.SUCCESS(f'Sync completed!')
            )
            self.stdout.write(f'Movies synced: {synced_count}')
            self.stdout.write(f'Movies skipped: {skipped_count}')
            self.stdout.write(f'Errors: {error_count}')
            self.stdout.write('='*50)
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Sync failed: {str(e)}')
            ) 
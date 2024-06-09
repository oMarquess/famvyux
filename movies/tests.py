from django.test import TestCase
import os
import json
# Create your tests here.
from django.core.management import call_command
from django.test import TestCase
from django.conf import settings
from django.core.management.base import CommandError

from movies.models import Movie


class MovieloaderTestCase(TestCase):
    def setUp(self):
        # Create a temporary JSON file with test data
        self.json_file_path = os.path.join(settings.BASE_DIR, 'data', 'test_data.json')
        with open(self.json_file_path, 'w') as file:
            json.dump([
                {
                    'title': 'Movie 1',
                    'year': 2022,
                    'image_url': 'https://example.com/movie1.jpg',
                    'duration': '100 minutes',
                    'star_rating': '4.5',
                    'rate_count': '100',
                    
                },
                {
                    'title': 'Movie 2',
                    'year': 2021,
                    'image_url': 'https://example.com/movie2.jpg',
                    'duration': '120 minutes',
                    'star_rating': '4.0',
                    'rate_count': '50',
                    
                }
            ], file)

    def tearDown(self):
        # Remove the temporary JSON file
        os.remove(self.json_file_path)

    def test_handle_success(self):
        # Call the handle method with the test JSON file
        call_command('movieloader', json_file=self.json_file_path)

        # Assert that the movies were imported into the database
        self.assertEqual(Movie.objects.count(), 2)
        self.assertEqual(Movie.objects.get(title='Movie 1').year, 2022)
        self.assertEqual(Movie.objects.get(title='Movie 2').year, 2021)

    def test_handle_invalid_json_file(self):
        # Call the handle method with an invalid JSON file
        with self.assertRaises(CommandError):
            call_command('movieloader', json_file='invalid_file.json')

    def test_handle_invalid_entry(self):

        pass
        # Create a temporary JSON file with an invalid entry
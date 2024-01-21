from django.core.management.base import BaseCommand
from django.conf import settings
import os
import json
import re
from movies.models import Movie  # Adjust the import path as necessary

class Command(BaseCommand):
    help = 'Cleans JSON data and imports it into the database'

    def clean_title(self, title):
        return re.sub(r'^\d+\.\s*', '', title)

    def handle(self, *args, **options):
        json_file_path = os.path.join(settings.BASE_DIR, 'data', 'output.json')  # Adjusted file path

        with open(json_file_path, 'r') as file:
            data = json.load(file)

        count = 0
        for entry in data:
            entry['title'] = self.clean_title(entry['title'])

            # Check if the movie already exists
            if not Movie.objects.filter(title=entry['title'], year=entry['year']).exists():
                Movie.objects.create(
                    title=entry['title'],
                    image_url=entry['image_url'],
                    year=entry['year'],
                    duration=entry['duration'],
                    star_rating=entry['star_rating'],
                    rate_count=entry['rate_count'],
                    product_url=entry['product_url']
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Data cleaning and import complete. {count} new entries added.'))

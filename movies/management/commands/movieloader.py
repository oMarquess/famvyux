# from django.core.management.base import BaseCommand
# from django.conf import settings
# import os
# import json
# import re
# from movies.models import Movie  # Adjust the import path as necessary

# class Command(BaseCommand):
#     help = 'Cleans JSON data and imports it into the database'

#     def clean_title(self, title):
#         """
#         Cleans the title by removing any leading digits followed by a dot and any whitespace.

#         :param title: The title to be cleaned
#         :return: The cleaned title
#         """
#         return re.sub(r'^\d+\.\s*', '', title)

#     def handle(self, *args, **options):
#         """
#         Main entry point for the command

#         Opens the JSON file, iterates over the entries, cleans the title, and checks if the movie already exists in the database.
#         If not, it creates a new instance and increments a counter. Finally, it prints a success message with the number of new entries added.

#         :param args: Command line arguments
#         :param options: Command line options
#         """
#         # json_file_path = os.path.join(settings.BASE_DIR, 'data', 'data.json')  # Adjusted file path

#         # with open(json_file_path, 'r') as file:
#         #     data = json.load(file)

#         # count = 0
#         # for entry in data:
#         #     # Check if entry is a dictionary and contains the key 'title'
#         #     if isinstance(entry, dict) and 'title' in entry:
#         #         entry['title'] = self.clean_title(entry['title'])

#         #         # Check if the movie already exists
#         #         if not Movie.objects.filter(title=entry['title'], year=entry['year']).exists():
#         #             Movie.objects.create(
#         #                 title=entry['title'],
#         #                 image_url=entry['image_url'],
#         #                 year=entry['year'],
#         #                 duration=entry['duration'],
#         #                 star_rating=entry['star_rating'],
#         #                 rate_count=entry['rate_count'],
#         #                 product_url=entry['product_url']
#         #             )
#         #             count += 1
#         #     else:
#         #         self.stdout.write(self.style.WARNING('Skipping invalid entry: {}'.format(entry)))

#         # self.stdout.write(self.style.SUCCESS(f'Data cleaning and import complete. {count} new entries added.'))
from django.core.management.base import BaseCommand
from django.conf import settings
import os
import json
import re
from movies.models import Movie  # Adjust the import path as necessary

class Command(BaseCommand):
    help = 'Cleans JSON data and imports it into the database'

    def clean_title(self, title):
        # Cleans the title by removing any leading digits followed by a dot and any whitespace.
        cleaned_title = re.sub(r'^\d+\.\s*', '', title)
        return cleaned_title

    def handle(self, *args, **options):
        json_file_path = os.path.join(settings.BASE_DIR, 'data', 'data.json')  # Adjusted file path

        with open(json_file_path, 'r') as file:
            data = json.load(file)[0]  # Accessing the first element if nested

        count = 0
        for entry in data:
            if isinstance(entry, dict) and 'title' in entry:
                cleaned_title = self.clean_title(entry['title'])

                # Check if the movie already exists
                if not Movie.objects.filter(title=cleaned_title, year=entry['year']).exists():
                    Movie.objects.create(
                        title=cleaned_title,
                        year=entry['year'],
                        imdb_rating=entry['imdb_rating'],
                        metascore=entry['metascore'],
                        image_url=entry['image_url'],
                        description=entry['description']
                    )
                    count += 1
                else:
                    print(f"Movie already exists: {cleaned_title} ({entry['year']})")  # Debug: Check for existing entries
            else:
                self.stdout.write(self.style.WARNING('Skipping invalid entry: {}'.format(entry)))

        self.stdout.write(self.style.SUCCESS(f'Data cleaning and import complete. {count} new entries added.'))

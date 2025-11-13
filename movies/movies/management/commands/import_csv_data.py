# movies/management/commands/import_csv_data.py

import csv
import os
from django.core.management.base import BaseCommand
from movies.models import Movie
from links.models import Link
from ratings.models import Rating
from tags.models import Tag

class Command(BaseCommand):
    help = "Import data from CSV files into the corresponding models"

    def handle(self, *args, **options):
        base_path = os.path.join(os.getcwd(), 'data')  # folder where your CSVs live

        files_and_models = [
            ('movies.csv', Movie, 'movieId'),
            ('links.csv', Link, 'movieId'),
            ('ratings.csv', Rating, 'id'),  # or use composite key if needed
            ('tags.csv', Tag, 'id'),        # or use composite key if needed
        ]

        for filename, model, unique_field in files_and_models:
            filepath = os.path.join(base_path, filename)
            if not os.path.exists(filepath):
                self.stdout.write(self.style.WARNING(f"⚠️  File not found: {filepath}"))
                continue

            self.import_csv(filepath, model, unique_field)
            self.stdout.write(self.style.SUCCESS(f"✅ Imported {filename} into {model.__name__}"))

        self.stdout.write(self.style.SUCCESS("🎉 All CSV imports finished!"))

    def import_csv(self, filepath, model, unique_field):
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Clean headers: remove empty headers and strip whitespace
            reader.fieldnames = [f.strip() for f in reader.fieldnames if f.strip()]

            for row in reader:
                # Remove keys with empty names
                # Only keep keys that are non-empty strings
                row = {str(k).strip(): v for k, v in row.items() if k and str(k).strip()}


                # Replace empty strings with None
                for key, value in row.items():
                    if value == '':
                        row[key] = None

                # Map CSV headers to Django field names
                field_map = {
                    'movieId': 'movie_id',  # for ForeignKey IDs
                    'userId': 'user_id',    # for ratings or tags
                }

                for csv_key, model_key in field_map.items():
                    if csv_key in row:
                        row[model_key] = row.pop(csv_key)

                # Handle ForeignKey fields automatically (_id)
                fk_fields = [f.name for f in model._meta.get_fields() if f.is_relation and f.many_to_one]
                for fk in fk_fields:
                    if fk in row:
                        row[f"{fk}_id"] = row.pop(fk)

                # Use update_or_create to avoid UNIQUE constraint errors
                if unique_field in row:
                    try:
                        model.objects.update_or_create(
                            defaults=row,
                            **{unique_field: row[unique_field]}
                        )
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"❌ Failed row: {row} - {e}"))

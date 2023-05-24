from django.core.management.base import BaseCommand
import os

# python manage.py clean_avatars

class Command(BaseCommand):
    help = 'Deletes all tags'

    def handle(self, *args, **options):
        try:
            os.remove('media/avatars/2023')
        except Exception as error:
            print(error)
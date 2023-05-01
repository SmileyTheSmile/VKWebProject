from django.core.management.base import BaseCommand

from HAsker.models import Tag

# python manage.py clean_questions

class Command(BaseCommand):
    help = 'Deletes all tags'

    def handle(self, *args, **options):
        try:
            Tag.objects.all().delete()
            print("Successflly deleted all tags")
        except Exception as error:
            print(error)
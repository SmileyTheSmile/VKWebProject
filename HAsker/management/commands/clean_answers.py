from django.core.management.base import BaseCommand

from HAsker.models import Answer

# python manage.py clean_questions

class Command(BaseCommand):
    help = 'Deletes all questions'

    def handle(self, *args, **options):
        try:
            Answer.objects.all().delete()
            print("Successflly deleted all answers")
        except Exception as error:
            print(error)
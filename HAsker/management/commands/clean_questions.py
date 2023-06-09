from django.core.management.base import BaseCommand

from HAsker.models import Question

# python manage.py clean_questions

class Command(BaseCommand):
    help = 'Deletes all questions'

    def handle(self, *args, **options):
        try:
            Question.objects.all().delete()
            print("Successflly deleted all questions")
        except Exception as error:
            print(error)
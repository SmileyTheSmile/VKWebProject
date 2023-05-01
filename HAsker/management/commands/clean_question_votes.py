from django.core.management.base import BaseCommand

from HAsker.models import QuestionVote

# python manage.py clean_questions

class Command(BaseCommand):
    help = 'Deletes all votes'

    def handle(self, *args, **options):
        try:
            QuestionVote.objects.all().delete()
            print("Successflly deleted all question votes")
        except Exception as error:
            print(error)
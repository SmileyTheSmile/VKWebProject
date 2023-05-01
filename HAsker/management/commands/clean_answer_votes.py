from django.core.management.base import BaseCommand

from HAsker.models import AnswerVote

# python manage.py answer_votes

class Command(BaseCommand):
    help = 'Deletes all votes'

    def handle(self, *args, **options):
        try:
            AnswerVote.objects.all().delete()
            print("Successflly deleted all answer votes")
        except Exception as error:
            print(error)
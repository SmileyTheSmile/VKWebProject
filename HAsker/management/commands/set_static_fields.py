from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.db.models import Q

from HAsker.models import Profile, Question, Answer

# python manage.py set_static_fields

class Command(BaseCommand):
    help = 'Fills static fields of models.'

    def handle(self, *args, **options):
        try:
            Question.objects.update_answers_num()
            print(f"Static answer numbers have been updated successfully")
        except IntegrityError as error:
            print(error)

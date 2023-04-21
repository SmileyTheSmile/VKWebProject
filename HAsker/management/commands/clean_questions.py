from django.core.management.base import BaseCommand

from HAsker.models import Question, Profile, Tag
from HAsker.services import random_sentence, random_text

import random

# python manage.py clean_questions

class Command(BaseCommand):
    help = 'Fills the Question tables with <questions_num> random questions from random users.'

    def handle(self, *args, **options):
        Question.objects.all().delete()
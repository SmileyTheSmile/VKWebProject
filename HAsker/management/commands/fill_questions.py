from django.core.management.base import BaseCommand

from HAsker.models import Question, Profile, Tag
from HAsker.services import random_sentence, random_text

import random

# python manage.py fill_questions 100

class Command(BaseCommand):
    help = 'Fills the Question tables with <questions_num> random questions from random users.'

    def add_arguments(self, parser):
        parser.add_argument('questions_num', nargs='+', type=int)

    def handle(self, *args, **options):
        random_user = random.choice(list(Profile.objects.all()))
        new_questions = Question.objects.bulk_create(
            [
                Question(
                    title=random_sentence(12, 12),
                    content=random_text(12, 12, 12),
                    author=random_user,
                ) for _ in options['questions_num'][0]
            ]
        )

        for question in new_questions:
            question.tags.set([random.choice(list(Tag.objects.all())) for _ in range(random.randint(1, 4))])

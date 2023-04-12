from django.core.management.base import BaseCommand

from HAsker.models import Question, Profile, Tag
from HAsker.services import random_question_data

import random

# python manage.py fill_questions 10

class Command(BaseCommand):
    help = 'Fills the Question tables with <questions_num> random questions from random users.'

    def add_arguments(self, parser):
        parser.add_argument('questions_num', nargs='+', type=int)

    def handle(self, *args, **options):
        random_user = random.choice(list(Profile.objects.all()))
        random_questions = [random_question_data()] * options['questions_num'][0]
        new_questions = Question.objects.bulk_create(
            [
                Question(
                    title=title,
                    content=content,
                    author=random_user,
                ) for title, content in random_questions]
        )

        for question in new_questions:
            question.tags.set([random.choice(list(Tag.objects.all())) for _ in range(random.randint(1, 4))])

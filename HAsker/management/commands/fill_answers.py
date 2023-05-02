from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.db.models import Q

from HAsker.models import Profile, Question, Answer
from HAsker.services import random_text

import random

# python manage.py fill_answers 10

class Command(BaseCommand):
    help = 'Fills random questions with random answers from <users_num> random users.'

    def add_arguments(self, parser):
        parser.add_argument('answers_num', nargs='+', type=int)

    def answers_generator(self, answers_num):
        if Profile.objects.count() == 0:
            raise IntegrityError("No users found to create question likes")
        
        if Question.objects.count() == 0:
            raise IntegrityError("No questions found to create likes")
        
        user_ids = Profile.objects.values_list('id', flat=True)
        question_ids = Question.objects.values_list('id', flat=True)

        for question_id in question_ids:
                for _ in range(answers_num):
                    yield Answer(
                                author_id=user_ids[random.randint(0, len(user_ids) - 1)],
                                question_id=question_id,
                                content=random_text(12, 12, 12)
                                )


    def handle(self, *args, **options):
        try:
            new_answers = Answer.objects.bulk_create(
                self.answers_generator(options['answers_num'][0]),
                batch_size=1000
            )

            print(f"{len(new_answers)} answers have been added successfully")
        except IntegrityError as error:
            print(error)

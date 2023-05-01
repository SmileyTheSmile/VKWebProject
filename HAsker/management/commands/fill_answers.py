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

    def handle(self, *args, **options):
        try:
            if Profile.objects.count() == 0:
                print("No users found to create question likes")
                return
            
            if Question.objects.count() == 0:
                print("No questions found to create likes")
                return
            
            user_ids = Profile.objects.values_list('id', flat=True)
            question_ids = Question.objects.values_list('id', flat=True)
            
            new_answers = Answer.objects.bulk_create([
                    Answer(
                        author_id=user_ids[random.randint(0, len(user_ids) - 1)],
                        question_id=question_id,
                        content=random_text(12, 12, 12)
                    )
                for _ in range(options['answers_num'][0])
                for question_id in question_ids]
            )

            print(f"{len(new_answers)} answers have been added successfully")
        except IntegrityError as error:
            print(error)

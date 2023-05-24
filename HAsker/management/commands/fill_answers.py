from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.db.models import Q

from HAsker.models import Profile, Question, Answer
from HAsker.services import random_text

import random
import lorem

# python manage.py fill_answers 10

class Command(BaseCommand):
    help = 'Fills random questions with random answers from <users_num> random users.'

    def add_arguments(self, parser):
        parser.add_argument('answers_for_each_question', nargs='+', type=int)

    def answers_generator(self, answers_num):
        if Profile.objects.count() == 0:
            print("No users found to create question likes")
            return []
        
        if Question.objects.count() == 0:
            print("No questions found to create likes")
            return []
        
        user_ids = Profile.objects.values_list('id', flat=True)
        questions = Question.objects.all()

        for question in questions:
            for _ in range(answers_num):
                yield Answer(
                            author_id=user_ids[random.randint(0, len(user_ids) - 1)],
                            question=question,
                            content=lorem.paragraph()
                            )
            question.answers_num += answers_num
        Question.objects.bulk_update(questions, ['answers_num'])


    def handle(self, *args, **options):
        try:
            new_answers = Answer.objects.bulk_create(
                self.answers_generator(options['answers_for_each_question'][0]),
                batch_size=1000
            )

            print(f"{len(new_answers)} answers have been added successfully")
        except IntegrityError as error:
            print(error)

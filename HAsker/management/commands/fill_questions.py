from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.db import transaction

from HAsker.models import Question, Profile, Tag
from HAsker.services import random_sentence, random_text

import random
import lorem

# python manage.py fill_questions 1000

class Command(BaseCommand):
    help = 'Fills the Question tables with <questions_num> random questions from random users.'

    def add_arguments(self, parser):
        parser.add_argument('questions_num', nargs='+', type=int)
    
    def questions_generator(self, questions_num):
        if Profile.objects.count() == 0:
            print("No users found to create questions")
            return []
        
        profile_ids = Profile.objects.values_list('id', flat=True)
        
        for _ in range(questions_num):
            yield Question(
                    title=lorem.sentence(),
                    content=lorem.paragraph(),
                    author_id=profile_ids[random.randint(0, len(profile_ids) - 1)],
                ) 

    def handle(self, *args, **options):
        try:
            new_questions = Question.objects.bulk_create(
                 self.questions_generator(options['questions_num'][0]),
                 batch_size=1000
            )

            print(f"{len(new_questions)} questions have been added successfully")
        except IntegrityError as error:
            print(error)

        try:
            if Tag.objects.count() == 0:
                print("No tags were found to be set in questions")
                return

            # TODO Try optimising tags...yet again
            with transaction.atomic():
                tag_ids = Tag.objects.values_list('id', flat=True)
                for question in new_questions:
                    question.tags.set(
                        [
                            tag_ids[random.randint(0, len(tag_ids) - 1)]
                            for _ in range(random.randint(1, 4))
                        ]
                    )

            print("Question tags have been set successfully")
        except IntegrityError as error:
            print(f"No tags have been set: {error}")

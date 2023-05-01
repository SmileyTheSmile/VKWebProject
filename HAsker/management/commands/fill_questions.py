from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from HAsker.models import Question, Profile, Tag
from HAsker.services import random_sentence, random_text

import random

# python manage.py fill_questions 100

class Command(BaseCommand):
    help = 'Fills the Question tables with <questions_num> random questions from random users.'

    def add_arguments(self, parser):
        parser.add_argument('questions_num', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            if Profile.objects.count() == 0:
                print("No users found to create questions")
                return
            
            user_profile_ids = Profile.objects.values_list('id', flat=True)
            
            new_questions = Question.objects.bulk_create([
                    Question(
                        title=random_sentence(12, 12),
                        content=random_text(12, 12, 12),
                        author_id=random.choice(user_profile_ids),
                    ) 
                for _ in range(options['questions_num'][0])]
            )

            print(f"{len(new_questions)} questions have been added successfully")
        except IntegrityError as error:
            print(error)

        if Tag.objects.count() == 0:
            print("No tags were found to be set in questions")
            return

        try:
            tag_ids = Tag.objects.values_list('id', flat=True)

            for question in new_questions:
                question.tags.set([random.choice(tag_ids) for _ in range(random.randint(1, 4))])

            print("Question tags have been set successfully")
        except IntegrityError as error:
            print(f"No tags have been set: {error}")

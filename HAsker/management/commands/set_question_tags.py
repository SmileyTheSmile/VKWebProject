from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.db import transaction

from HAsker.models import Question, Profile, Tag
from HAsker.services import random_sentence, random_text

import random

# python manage.py fill_questions 1000

class Command(BaseCommand):
    help = 'Fills the Question tables with <questions_num> random questions from random users.'

    def handle(self, *args, **options):
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

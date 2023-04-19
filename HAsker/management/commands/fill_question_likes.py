from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from HAsker.models import QuestionVote, Profile, Question, Vote
from HAsker.services import random_question_data

import random

# python manage.py fill_question_likes 100

class Command(BaseCommand):
    help = 'Fills random questions with random votes from random users.'

    def add_arguments(self, parser):
        parser.add_argument('max_likes_num', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            users = Profile.objects.all()
            questions = Question.objects.all()
            new_votes = []
            for question in questions:
                for _ in range(options['max_likes_num'][0]):
                    author = random.choice(users)
                    score = random.choice([1, -1])

                    if not QuestionVote.author.exists():
                        new_votes.append(
                            QuestionVote(
                                author=author,
                                score=score,
                                question=question,
                            ))


            Vote.objects.bulk_create(new_votes)
            print(f"Likes have been added successfully")
        except IntegrityError as error:
            print(error)

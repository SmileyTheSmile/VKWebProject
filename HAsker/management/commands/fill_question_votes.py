from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from HAsker.models import QuestionVote, Profile, Question
from HAsker.services import turn_to_list

import random

# python manage.py fill_question_votes

class Command(BaseCommand):
    help = 'Fills all questions with random votes from all users.'

    def votes_generator(self):
        if Profile.objects.count() == 0:
            print("No users found to create question likes")
            return []
        
        if Question.objects.count() == 0:
            print("No questions found to create likes")
            return []

        question_ids_and_vote_author_ids = Question.objects.values_list('id', 'votes__author')
        profile_ids = Profile.objects.values_list('id', flat=True)
                
        for question_id, vote_authors in question_ids_and_vote_author_ids:
            for profile_id in profile_ids.exclude(id__in=turn_to_list(vote_authors)):
                yield QuestionVote(
                                    author_id=profile_id,
                                    score=random.choice([1, -1]),
                                    question_id=question_id
                                    )

    def handle(self, *args, **options):
        try:
            new_votes = QuestionVote.objects.bulk_create(
                self.votes_generator(),
                batch_size=1000
            )

            print(f"{len(new_votes)} question votes have been added successfully")
        except IntegrityError as error:
            print(error)
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from HAsker.models import AnswerVote, Profile, Answer
from HAsker.services import turn_to_list

import random

# python manage.py fill_answer_votes

class Command(BaseCommand):
    help = 'Fills all answers with random votes from all users.'

    def votes_generator(self):
        if Profile.objects.count() == 0:
            raise IntegrityError("No users found to create answer votes")
        
        if Answer.objects.count() == 0:
            raise IntegrityError("No answers found to create votes")

        answer_ids_and_vote_author_ids = Answer.objects.values_list('id', 'votes__author')
        profile_ids = Profile.objects.values_list('id', flat=True)
                
        for answer_id, vote_authors in answer_ids_and_vote_author_ids:
            for profile_id in profile_ids.exclude(id__in=turn_to_list(vote_authors)):
                yield AnswerVote(
                                author_id=profile_id,
                                score=random.choice([1, -1]),
                                answer_id=answer_id
                                )

    def handle(self, *args, **options):
        try:
            new_votes = AnswerVote.objects.bulk_create(
                self.votes_generator(),
                batch_size=1000)

            print(f"{len(new_votes)} answer votes have been added successfully")
        except IntegrityError as error:
            print(error)
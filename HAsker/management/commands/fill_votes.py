from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from HAsker.services import turn_to_list

from HAsker.models import AnswerVote, Answer, QuestionVote, Question, Profile

import random

# python manage.py fill_votes

class Command(BaseCommand):
    help = 'Fills all answers with random votes from all users.'

    def votes_generator(self, vote_type, object_type):
        if Profile.objects.count() == 0:
            print(f"No users found to create {object_type.__name__}s")
            return []
        
        if object_type.objects.count() == 0:
            print(f"No {object_type} found to create votes")
            return []

        object_ids_and_vote_author_ids = object_type.objects.values_list('id', 'votes__author')
        profile_ids = Profile.objects.values_list('id', flat=True)
                
        for object_id, vote_authors in object_ids_and_vote_author_ids:
            for profile_id in profile_ids.exclude(id__in=turn_to_list(vote_authors)):
                yield vote_type(
                                author_id=profile_id,
                                score=random.choice([1, -1]),
                                object_id=object_id
                                )
# TODO Fix unique key errors on second run of command
    def handle(self, *args, **options):
        types = [
            (QuestionVote, Question),
            (AnswerVote, Answer),
        ]
        try:
            for vote_type, object_type in types:
                new_votes = vote_type.objects.bulk_create(
                    self.votes_generator(vote_type, object_type),
                    batch_size=1000)

                print(f"{len(new_votes)} {vote_type.__name__}s have been added successfully")
                
                object_type.objects.update_rating()
                print(f"Static {object_type.__name__} ratings have been updated successfully")
                    
            Profile.objects.update_rating()
            print("Static profile ratings have been updated successfully")
        except IntegrityError as error:
            print(error)
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from HAsker.models import AnswerVote, Profile, Answer

import random

# python manage.py fill_question_votes

class Command(BaseCommand):
    help = 'Fills all questions with random votes from all users.'

    def add_arguments(self, parser):
        parser.add_argument('votes_type', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            if Profile.objects.count() == 0:
                print("No users found to create question likes")
                return
            
            if Answer.objects.count() == 0:
                print("No questions found to create likes")
                return

            profile_ids = Profile.objects.values_list('id', flat=True)
            question_ids_and_vote_author_ids = Answer.objects.values_list('id', 'votes__author')

            new_votes =  []
            for question_id, vote_authors in question_ids_and_vote_author_ids:
                if vote_authors is None:
                    vote_authors = []
                elif isinstance(vote_authors, int):
                    vote_authors = [vote_authors]
                for profile_id in profile_ids:
                    if profile_id not in vote_authors:
                        vote_authors.append(profile_id)
                        new_votes.append(AnswerVote(
                                        author_id=profile_id,
                                        score=random.choice([1, -1]),
                                        answer_id=question_id
                                        ))    
            new_votes = AnswerVote.objects.bulk_create(new_votes)

            print(f"{len(new_votes)} answer votes have been added successfully")
        except IntegrityError as error:
            print(error)

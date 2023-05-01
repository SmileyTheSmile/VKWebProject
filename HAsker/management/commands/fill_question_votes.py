from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from HAsker.models import QuestionVote, Profile, Question, Answer

import random

# python manage.py fill_question_votes

class Command(BaseCommand):
    help = 'Fills all questions with random votes from all users.'

    def handle(self, *args, **options):
        try:
            if Profile.objects.count() == 0:
                print("No users found to create question likes")
                return
            
            if Question.objects.count() == 0:
                print("No questions found to create likes")
                return

            question_ids_and_vote_author_ids = Question.objects.values_list('id', 'votes__author')
            profile_ids = Profile.objects.values_list('id', flat=True)

            new_votes =  []
            for question_id, vote_authors in question_ids_and_vote_author_ids:
                if vote_authors is None:
                    unadded_profiles = []
                elif isinstance(vote_authors, int):
                    unadded_profiles = [vote_authors]
                else:
                    unadded_profiles = set(profile_ids) - set(vote_authors)
                    
                new_votes += [
                        QuestionVote(
                                    author_id=profile_id,
                                    score=random.choice([1, -1]),
                                    question_id=question_id
                                    )
                    for profile_id in profile_ids
                        if profile_id not in unadded_profiles
                ]
                
            new_votes = QuestionVote.objects.bulk_create(new_votes)

            print(f"{len(new_votes)} question votes have been added successfully")
        except IntegrityError as error:
            print(error)

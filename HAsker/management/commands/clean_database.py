from django.core.management.base import BaseCommand

from HAsker.management.commands import (
    clean_questions, 
    clean_tags, 
    clean_users, 
    clean_question_votes, 
    clean_answer_votes, 
    clean_answers,
    clean_avatars,
)

# python manage.py clean_database

class Command(BaseCommand):
    help = 'Cleans the database'

    def handle(self, *args, **options):
        commands = [
            clean_tags.Command(),
            clean_answer_votes.Command(),
            clean_answers.Command(),
            clean_question_votes.Command(),
            clean_questions.Command(),
            clean_users.Command(),
            #clean_avatars.Command(),
        ]
        
        for command in commands:
            command.handle(*args, **options)

from django.core.management.base import BaseCommand
from HAsker.management.commands import (
    fill_question_votes,
    fill_questions,
    fill_tags, 
    fill_users, 
    set_all_avatars, 
    fill_answers,
    fill_answer_votes,
)

# python manage.py fill_database 1000 1000 1000 10

class Command(BaseCommand):
    help = 'Fills the database with random data.'

    def add_arguments(self, parser):
        parser.add_argument('tags_num', nargs='+', type=int)
        parser.add_argument('users_num', nargs='+', type=int)
        parser.add_argument('questions_num', nargs='+', type=int)
        parser.add_argument('answers_num', nargs='+', type=int)

    def handle(self, *args, **options):
        commands = [
            fill_tags.Command(),
            fill_users.Command(),
            set_all_avatars.Command(),
            fill_questions.Command(),
            fill_answers.Command(),
            fill_question_votes.Command(),
            fill_answer_votes.Command(),
        ]
        
        for command in commands:
            command.handle(*args, **options)

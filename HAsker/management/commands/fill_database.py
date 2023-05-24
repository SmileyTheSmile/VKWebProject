from django.core.management.base import BaseCommand
from HAsker.management.commands import (
    fill_questions,
    fill_tags, 
    fill_users, 
    fill_answers,
    fill_votes,
)

# python manage.py fill_database 1000

class Command(BaseCommand):
    help = 'Fills the database with random data.'

    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='+', type=int)

    def handle(self, *args, **options):
        commands = [
            fill_tags.Command(),
            fill_users.Command(),
            fill_questions.Command(),
            fill_answers.Command(),
            fill_votes.Command(),
        ]

        ratio = options['ratio'][0]
        options['tags_num'] = [ratio]
        options['users_num'] = [ratio]
        options['questions_num'] = [ratio * 10]
        options['answers_for_each_question'] = [10]   
        
        for command in commands:
            command.handle(*args, **options)

'''

    пользователей — равное ratio;
    вопросов — ratio * 10;
    ответы — ratio * 100;
    тэгов - ratio;
    оценок пользователей - ratio * 200;

'''
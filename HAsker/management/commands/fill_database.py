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

# python manage.py fill_database 10000 0

class Command(BaseCommand):
    help = 'Fills the database with random data.'

    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='+', type=int)
        parser.add_argument('add_likes', nargs='+', type=int)

    def handle(self, *args, **options):
        commands = [
            fill_tags.Command(),
            fill_users.Command(),
            set_all_avatars.Command(),
            fill_questions.Command(),
            fill_answers.Command(),
        ]

        if options['add_likes'] == 1:
            commands += [
                fill_question_votes.Command(),
                fill_answer_votes.Command(),
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
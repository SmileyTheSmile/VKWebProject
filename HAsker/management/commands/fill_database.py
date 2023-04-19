from django.core.management.base import BaseCommand

from HAsker.models import Question, Profile, Tag
from HAsker.management.commands import fill_question_likes, fill_questions, fill_tags, fill_users

import random

# python manage.py fill_questions 10

class Command(BaseCommand):
    help = 'Fills the database with random data.'

    def add_arguments(self, parser):
        parser.add_argument('questions_num', nargs='+', type=int)
        parser.add_argument('users_num', nargs='+', type=int)
        parser.add_argument('tags_num', nargs='+', type=int)
        parser.add_argument('users_num', nargs='+', type=int)

    def handle(self, *args, **options):
        fill_tags(args, options)
        fill_users(args, options)
        fill_questions(args, options)
        fill_question_likes(args, options)

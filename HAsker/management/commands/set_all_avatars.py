from django.core.management.base import BaseCommand

from HAsker.models import Question, Profile, Tag
from HAsker.services import random_question_data

import random

link = 'https://i.stack.imgur.com/7XElg.jpg?s=64&g=1'

# python manage.py set_all_avatars

class Command(BaseCommand):
    help = 'Set all avatars to {link}'

    def handle(self, *args, **options):
        Profile.objects.update(avatar=link)
        
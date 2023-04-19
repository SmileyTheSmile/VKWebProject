from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from HAsker.models import Tag
from HAsker.services import random_word_list

import random

# python manage.py fill_tags 100

class Command(BaseCommand):
    help = 'Fills the Tag table with <tags_num> random tags.'

    def add_arguments(self, parser):
        parser.add_argument('tags_num', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            Tag.objects.bulk_create(
                Tag(name=tagname)
                for tagname in random_word_list(options['tags_num'][0],
                                                Tag._meta.get_field('name').max_length)
            )
            print(f"{options['tags_num'][0]} tags have been added successfully")
        except IntegrityError as error:
            print(error)
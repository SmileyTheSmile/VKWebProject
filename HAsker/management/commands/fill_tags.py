from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from HAsker.models import Tag
from HAsker.services import random_word

import random

# python manage.py fill_tags 100

class Command(BaseCommand):
    help = 'Fills the Tag table with <tags_num> random tags.'

    tag_length = Tag._meta.get_field('name').max_length

    def add_arguments(self, parser):
        parser.add_argument('tags_num', nargs='+', type=int)

    def unique_tag(self, old_tags):
        while True:
            tag = random_word(self.tag_length)
            if tag not in old_tags:
                old_tags.append(tag)
                return tag

    def handle(self, *args, **options):
        try:
            tag_ids = list(Tag.objects.values_list('id', flat=True)) if Tag.objects.count() != 0 else []

            new_tags = Tag.objects.bulk_create([
                    Tag(name=self.unique_tag(tag_ids))
                for _ in range(options['tags_num'][0])
            ])

            print(f"{len(new_tags)} tags have been added successfully")
        except IntegrityError as error:
            print(error)
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from HAsker.models import Tag
 
from random_word import RandomWords

# python manage.py fill_tags 10000

class Command(BaseCommand):
    help = 'Fills the Tag table with <tags_num> random tags.'

    tag_length = Tag._meta.get_field('name').max_length

    def add_arguments(self, parser):
        parser.add_argument('tags_num', nargs='+', type=int)

    def unique_tag(self, old_tags, word_generator):
        tag = word_generator.get_random_word()
        while tag in old_tags:
            tag = word_generator.get_random_word()
        return tag
    
    def tag_generator(self, tag_num):
        tag_names = list(Tag.objects.values_list('name', flat=True)) if Tag.objects.count() != 0 else []

        word_generator = RandomWords()
        for _ in range(tag_num):
            tag = self.unique_tag(tag_names, word_generator)
            tag_names.append(tag)
            yield Tag(name=tag)

    def handle(self, *args, **options):
        try:
            new_tags = Tag.objects.bulk_create(
                self.tag_generator(options['tags_num'][0]),
                batch_size=1000
            )

            print(f"{len(new_tags)} tags have been added successfully")
        except IntegrityError as error:
            print(error)
from django.core.management.base import BaseCommand

from HAsker.models import Profile

link = 'https://p.kindpng.com/picc/s/451-4517876_default-profile-hd-png-download.png'
link = 'avatars/default.jpeg'

# python manage.py set_all_avatars

class Command(BaseCommand):
    help = f'Set all avatars to {link}'

    def handle(self, *args, **options):
        Profile.objects.update(avatar=link)
        print(f'Set all avatars to {link}')
        
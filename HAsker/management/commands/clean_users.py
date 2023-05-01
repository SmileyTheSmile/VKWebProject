from django.core.management.base import BaseCommand

from HAsker.models import Profile, User

# python manage.py clean_questions

class Command(BaseCommand):
    help = 'Deletes all users'

    def handle(self, *args, **options):
        try:
            Profile.objects.all().delete()
            print("Successflly deleted all user profiles")
            User.objects.all().delete()
            print("Successflly deleted all users")
        except Exception as error:
            print(error)
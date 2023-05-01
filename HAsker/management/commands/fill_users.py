from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from django.contrib.auth.models import User

from HAsker.models import Profile
from HAsker.services import random_word

# python manage.py fill_users 1000


class Command(BaseCommand):
    help = 'Fills the User and Profile tables with <users_num> random users.'
    
    username_length = User._meta.get_field('username').max_length
    password_length = User._meta.get_field('password').max_length
    email_length = User._meta.get_field('email').max_length - len('@mail.ru')
    nickname_length = Profile._meta.get_field('nickname').max_length

    def add_arguments(self, parser):
        parser.add_argument('users_num', nargs='+', type=int)

    def unique_email(self, old_emails):
        while True:
            email = f"{random_word(self.email_length)}@mail.ru"
            if email not in old_emails:
                old_emails.append(email)
                return email

    def unique_username(self, old_usernames):
        while True:
            username = random_word(self.username_length)
            if username not in old_usernames:
                old_usernames.append(username)
                return username

    def handle(self, *args, **options):
        try:
            if User.objects.count() != 0:
                emails, usernames = map(list, zip(*User.objects.values_list('email', 'username')))
            else:
                emails, usernames = [], []

            new_users = User.objects.bulk_create([
                User(
                    username=self.unique_username(usernames),
                    email=self.unique_email(emails),
                    password=random_word(self.password_length),
                )
                for i in range(options['users_num'][0])]
            )

            print(f"{len(new_users)} users have been added successfully")
        except IntegrityError as error:
            print(f"User not created: {error}")
            return

        try:
            new_profiles = Profile.objects.bulk_create([
                    Profile(
                        user=user,
                        nickname=random_word(self.nickname_length),
                    )
                for user in new_users])

            print(f"{len(new_profiles)} user profiles have been added successfully")
        except IntegrityError as error:
            print(f"Profile not created: {error}")
            return
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
                return email

    def unique_username(self, old_usernames):
        while True:
            username = random_word(self.username_length)
            if username not in old_usernames:
                return username
    
    def user_generator(self, user_num):
        if User.objects.count() != 0:
            emails, usernames = map(list, zip(*User.objects.values_list('email', 'username')))
        else:
            emails, usernames = [], []

        for i in range(user_num):
            username = self.unique_username(usernames)
            usernames.append(username)
            email = self.unique_email(usernames)
            emails.append(email)

            yield User(
                    username=username,
                    email=email,
                    password=random_word(self.password_length),
                )
    
    def profile_generator(self, users):
        for user in users:
            yield Profile(
                        user=user,
                        nickname=random_word(self.nickname_length),
                    )

    def handle(self, *args, **options):
        try:
            new_users = User.objects.bulk_create(
                self.user_generator(options['users_num'][0]),
                batch_size=1000,
            )

            print(f"{len(new_users)} users have been added successfully")
        except IntegrityError as error:
            print(f"Users not created: {error}")
            return

        try:
            new_profiles = Profile.objects.bulk_create(
                self.profile_generator(new_users),
                batch_size=1000,
            )

            print(f"{len(new_profiles)} user profiles have been added successfully")
        except IntegrityError as error:
            print(f"Profiles not created: {error}")
            return
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from django.contrib.auth.models import User

from HAsker.models import Profile
from HAsker.services import random_user_data_list, random_word, random_word_list

# python manage.py fill_users 10

class Command(BaseCommand):
    help = 'Fills the User and Profile tables with <users_num> random users.'

    def add_arguments(self, parser):
        parser.add_argument('users_num', nargs='+', type=int)

    def handle(self, *args, **options):
        max_lengths = [
            User._meta.get_field('username').max_length,
            User._meta.get_field('password').max_length,
            User._meta.get_field('email').max_length - len("@mail.ru"),
        ]
        users_num = options['users_num'][0]

        try:
            random_users = random_user_data_list(users_num, max_lengths)
            users = User.objects.bulk_create([
                User(
                    username=username,
                    password=password,
                    email=f"{email}@mail.ru",
                ) for username, password, email in random_users
                ]
            )

            nickname_length = Profile._meta.get_field('nickname').max_length
            random_nicknames = random_word_list(users_num, nickname_length)

            Profile.objects.bulk_create([
                Profile.objects.create(
                    user=users[i],
                    nickname=random_nicknames[i],
                ) for i in range(users_num)
                ]
            )
        except IntegrityError as error:
            print(error)

        print(f"{users_num} users have been added successfully")
# Generated by Django 4.2 on 2023-05-24 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HAsker', '0013_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default_avatar.jpeg', upload_to='avatars/%Y/%m/%d/'),
        ),
    ]

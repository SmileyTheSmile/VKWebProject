# Generated by Django 4.2 on 2023-05-24 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HAsker', '0011_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='default_avatars.jpeg', upload_to='avatars/%Y/%m/%d/'),
        ),
    ]

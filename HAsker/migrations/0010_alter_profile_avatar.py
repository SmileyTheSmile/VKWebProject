# Generated by Django 4.2 on 2023-05-24 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HAsker', '0009_question_answers_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default.jpeg', upload_to='avatars/%Y/%m/%d/'),
        ),
    ]

# Generated by Django 4.2 on 2023-05-21 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HAsker', '0005_question_rating_alter_answer_question_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
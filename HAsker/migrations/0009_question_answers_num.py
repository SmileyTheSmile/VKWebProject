# Generated by Django 4.2 on 2023-05-23 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HAsker', '0008_rename_answer_answervote_object_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answers_num',
            field=models.IntegerField(default=0),
        ),
    ]
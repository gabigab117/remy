# Generated by Django 4.2.1 on 2023-05-19 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0002_moderator_alter_category_options_alter_idea_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Moderator',
        ),
    ]

# Generated by Django 4.2.1 on 2023-05-23 22:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0005_alter_idea_details_alter_idea_sketch_requestidea'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 5, 23, 22, 6, 50, 574509)),
        ),
        migrations.AddField(
            model_name='requestidea',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 5, 23, 22, 6, 50, 585093)),
        ),
    ]

# Generated by Django 4.2.1 on 2023-05-28 19:53

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0007_alter_idea_date_alter_requestidea_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='details',
            field=ckeditor.fields.RichTextField(unique=True, verbose_name='Détails'),
        ),
        migrations.AlterField(
            model_name='requestidea',
            name='details',
            field=ckeditor.fields.RichTextField(unique=True, verbose_name='Détails'),
        ),
    ]
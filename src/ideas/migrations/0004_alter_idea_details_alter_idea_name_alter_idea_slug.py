# Generated by Django 4.2.1 on 2023-05-20 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0003_delete_moderator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='details',
            field=models.TextField(unique=True, verbose_name='Détail'),
        ),
        migrations.AlterField(
            model_name='idea',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='idea',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
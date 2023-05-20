# Generated by Django 4.2.1 on 2023-05-19 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Moderator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100)),
                ('pseudo', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Modérateur',
            },
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Catégorie'},
        ),
        migrations.AlterModelOptions(
            name='idea',
            options={'verbose_name': 'Idée'},
        ),
    ]
# Generated by Django 4.2.1 on 2023-05-19 21:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nom')),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nom')),
                ('slug', models.SlugField(blank=True)),
                ('summary', models.CharField(max_length=1000, verbose_name='Résumé')),
                ('level', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], help_text='1 : rapide, 2 : moyennement développé, 3 : très développé', max_length=1, verbose_name='Niveau')),
                ('details', models.TextField(verbose_name='Détail')),
                ('sketch', models.ImageField(blank=True, null=True, upload_to='sketch', verbose_name='Croquis')),
                ('status', models.BooleanField(default=False, verbose_name='Publié')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ideas.category', verbose_name='Catégorie')),
                ('thinker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
        ),
    ]

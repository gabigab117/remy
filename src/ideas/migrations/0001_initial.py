# Generated by Django 4.2.1 on 2023-06-30 01:39

import ckeditor.fields
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
            options={
                'verbose_name': 'Catégorie',
            },
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Nom')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('summary', models.CharField(max_length=1000, verbose_name='Résumé')),
                ('level', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], help_text='1 : rapide, 2 : moyennement développé, 3 : très développé', max_length=1, verbose_name='Niveau')),
                ('details', ckeditor.fields.RichTextField(unique=True, verbose_name='Détails')),
                ('sketch', models.ImageField(blank=True, null=True, upload_to='sketch_idea', verbose_name='Croquis')),
                ('date', models.DateField(auto_now_add=True)),
                ('request', models.BooleanField(default=False, help_text="Cocher si c'est une demande d'idée, si c'est une idée (offre) ne pas cocher", verbose_name="Demande d'idée")),
                ('status', models.BooleanField(default=False, verbose_name='Publié')),
                ('price', models.FloatField(default=0, verbose_name='Prix')),
                ('paid', models.BooleanField(default=False, verbose_name='Payé')),
                ('ordered_date', models.DateField(blank=True, null=True, verbose_name="Date d'achat")),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to=settings.AUTH_USER_MODEL, verbose_name='Acheteur')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ideas.category', verbose_name='Catégorie')),
                ('thinker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ideas', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': "Idée / Demande d'idée",
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor.fields.RichTextField(verbose_name='Message')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('idea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ideas.idea', verbose_name='idée')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='utilisateur')),
            ],
            options={
                'verbose_name': 'Commentaire',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('buyer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Acheteur')),
                ('ideas', models.ManyToManyField(to='ideas.idea', verbose_name='Idées')),
            ],
            options={
                'verbose_name': 'Panier',
            },
        ),
    ]

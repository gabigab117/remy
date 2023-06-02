from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.mail import send_mail
from accounts.models import Moderator
from remy.settings import AUTH_USER_MODEL
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Catégorie"


class Idea(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom", unique=True)
    slug = models.SlugField(blank=True, unique=True)
    summary = models.CharField(max_length=1000, verbose_name="Résumé")
    level = models.CharField(choices=[(str(i), str(i)) for i in range(1, 4)],
                             verbose_name="Niveau",
                             help_text="1 : rapide, 2 : moyennement développé, 3 : très développé",
                             max_length=1)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name="Catégorie", null=True)
    thinker = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur")
    details = RichTextField(verbose_name="Détails", unique=True)
    sketch = models.ImageField(upload_to="sketch_idea", verbose_name="Croquis", blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(verbose_name="Publié", default=False)

    def email_to_admin_idea(self):
        moderators: Moderator = Moderator.objects.all()
        ideas = Idea.objects.all()

        if not self in ideas:
            email = send_mail(subject=f"{self.thinker} a soumis {self.name}",
                              message=f"{self.thinker} a soumis une idée :\n {self.details}",
                              from_email=None,
                              recipient_list=[moderator.email for moderator in moderators])
            return email

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.email_to_admin_idea()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ideas:idea-detail', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Idée"


class RequestIdea(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom", unique=True)
    slug = models.SlugField(blank=True, unique=True)
    summary = models.CharField(max_length=1000, verbose_name="Résumé")
    level = models.CharField(max_length=1,
                             choices=[(str(i), str(i)) for i in range(1, 4)],
                             verbose_name="Niveau",
                             help_text="1 : rapide, 2 : moyennement développé, 3 : très développé")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Catégorie")
    thinker = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Utilisateur")
    details = RichTextField(verbose_name="Détails", unique=True)
    sketch = models.ImageField(blank=True, null=True, verbose_name="Croquis", upload_to="sketch_request_idea")
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False, verbose_name="Publié")

    def email_to_admin_request(self):
        moderators: Moderator = Moderator.objects.all()
        requestideas = RequestIdea.objects.all()

        if not self in requestideas:
            email = send_mail(subject=f"{self.thinker} recherche {self.name}",
                              message=f"{self.thinker} recherche :\n {self.details}",
                              from_email=None,
                              recipient_list=[moderator.email for moderator in moderators])
            return email

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        self.email_to_admin_request()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ideas:request-idea-detail', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Demande d'idée"


class IdeaComment(models.Model):
    content = RichTextField(verbose_name="Message")
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, verbose_name="idée")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="utilisateur")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.date} - {self.idea}"

    class Meta:
        verbose_name = "Commentaires idée"


class RequestIdeaComment(models.Model):
    content = models.TextField()
    request_idea = models.ForeignKey(RequestIdea, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

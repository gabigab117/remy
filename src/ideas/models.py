from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.mail import send_mail
from django.utils import timezone
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
                             help_text="1 : rapide, 2 : moyennement développé, 3 : très développé",
                             max_length=1,
                             verbose_name="Niveau",)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name="Catégorie", null=True)
    thinker = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                                verbose_name="Utilisateur", related_name="ideas")
    details = RichTextField(unique=True, verbose_name="Détails", max_length=1000000)
    sketch = models.ImageField(upload_to="sketch_idea", blank=True, null=True, verbose_name="Croquis")
    date = models.DateField(auto_now_add=True)
    request = models.BooleanField(default=False, verbose_name="Demande d'idée",
                                  help_text="Cocher si c'est une demande d'idée,"
                                            " si c'est une idée (offre) ne pas cocher")
    status = models.BooleanField(default=False, verbose_name="Publié")
    price = models.FloatField(default=0, verbose_name="Prix")
    paid = models.BooleanField(default=False, verbose_name="Payé")
    buyer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name="Acheteur", null=True, related_name="purchases", blank=True)
    ordered_date = models.DateField(verbose_name="Date d'achat", null=True, blank=True)

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
        verbose_name = "Idée / Demande d'idée"
        ordering = ["-date"]


class Comment(models.Model):
    content = RichTextField(verbose_name="Message", max_length=1000000)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, verbose_name="idée")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="utilisateur")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.date} - {self.idea}"

    class Meta:
        verbose_name = "Commentaire"


class Cart(models.Model):
    buyer = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Acheteur")
    ideas = models.ManyToManyField(Idea, verbose_name="Idées")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def total_cart(self):
        total = 0
        for idea in self.ideas.all():
            total += idea.price

        return total

    def cart_paid(self, user):
        for idea in self.ideas.all():
            idea.paid = True
            idea.buyer = user
            idea.ordered_date = timezone.now()
            idea.save()

        # self.ideas.clear() non nécéssaire
        self.delete()

    class Meta:
        verbose_name = "Panier"

    def __str__(self):
        return f"Panier de {self.buyer} {self.creation_date}"

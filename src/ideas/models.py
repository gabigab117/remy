from django.db import models
from django.utils.text import slugify
from accounts.models import Thinker
from django.core.mail import send_mail
from accounts.models import Moderator


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
    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(blank=True)
    summary = models.CharField(max_length=1000, verbose_name="Résumé")
    level = models.CharField(choices=[(str(i), str(i)) for i in range(1, 4)],
                             verbose_name="Niveau",
                             help_text="1 : rapide, 2 : moyennement développé, 3 : très développé",
                             max_length=1)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name="Catégorie", null=True)
    thinker = models.ForeignKey(Thinker, on_delete=models.CASCADE, verbose_name="Utilisateur")
    details = models.TextField(verbose_name="Détail")
    sketch = models.ImageField(upload_to="sketch", verbose_name="Croquis", blank=True, null=True)
    status = models.BooleanField(verbose_name="Publié", default=False)

    def email_to_admin(self):
        moderators: Moderator = Moderator.objects.all()

        email = send_mail(subject=f"{self.thinker} a soumis {self.name}",
                          message=f"{self.thinker} a soumis une idée :\n {self.details}",
                          from_email="gabrieltrouve5@yahoo.com",
                          recipient_list=[moderator.email for moderator in moderators])
        return email

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        self.email_to_admin()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Idée"

# ici le modèle RequestIdea

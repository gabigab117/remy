from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from remy.settings import AUTH_USER_MODEL
import countryphonelist


class ThinkerManager(BaseUserManager):
    def create_user(self, email, username, phone, first_name, last_name, password, country, **kwargs):
        if not email:
            raise ValueError("Merci de renseigner un email svp")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone=phone, first_name=first_name, last_name=last_name,
                          country=country,
                          **kwargs)
        user.set_password(password)
        user.is_active = False
        user.format_phone_number()
        user.save()
        return user

    def create_superuser(self, email, username, phone, first_name, last_name, password, country, **kwargs):
        user = self.create_user(email=email, username=username, phone=phone, first_name=first_name, last_name=last_name,
                                password=password, country=country, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user


class Thinker(AbstractUser):
    phone = models.CharField(max_length=25, verbose_name="Téléphone")
    email = models.EmailField(unique=True)
    company = models.CharField(max_length=500, blank=True, verbose_name="Entreprise")
    country = models.CharField(max_length=100, choices=countryphonelist.COUNTRY, verbose_name="Pays")
    stripe_id = models.CharField(max_length=500)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone", 'first_name', 'last_name', 'country']

    objects = ThinkerManager()

    def format_phone_number(self):
        if not self.phone.startswith('+'):
            phone_number = self.phone.lstrip('0')
            for i in countryphonelist.DIAL:
                if i[0] == self.country:
                    dial_code = i[1]
                    phone_number = dial_code + phone_number
                    self.phone = phone_number

                    return self.phone
        return self.phone


class Moderator(models.Model):
    email = models.EmailField(max_length=100)
    pseudo = models.CharField(max_length=100)

    def __str__(self):
        return self.pseudo

    class Meta:
        verbose_name = "Modérateur"


class ShippingAddresse(models.Model):
    thinker = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE, related_name="addresses")
    name = models.CharField(max_length=100, verbose_name="Nom de l'adresse")
    line1 = models.CharField(max_length=500, verbose_name="Adresse")
    line2 = models.CharField(max_length=200, verbose_name="Adresse / Complément",
                             help_text="Num d'appt etc...", default="")
    zip_code = models.CharField(max_length=10, verbose_name="Code postal")
    city = models.CharField(max_length=100, verbose_name="Ville")
    country = models.CharField(max_length=100, verbose_name="Pays")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Adresse"

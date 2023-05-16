from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
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
    pic = models.ImageField(upload_to="profil", verbose_name="Photo", blank=True, null=True)

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

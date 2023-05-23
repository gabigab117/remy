from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class ThinkerCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["email", "username", "first_name", "last_name", "phone", "company", "country", "pic"]


class ThinkerProfilForm(forms.ModelForm):
    # disabled True va griser le champ. On verra les infos affichées mais rien ne sera envoyé
    email = forms.EmailField(help_text="L'email ne peut pas être modifié ici")
    password = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe")
    first_name = forms.CharField(disabled=True, max_length=100, label="Prénom")
    last_name = forms.CharField(disabled=True, max_length=100, label="Nom")
    username = forms.CharField(disabled=True, max_length=100, label="Pseudo")

    class Meta:
        model = get_user_model()
        fields = ["email", "username", "password", "first_name",
                  "last_name", "phone", "company", "country"]

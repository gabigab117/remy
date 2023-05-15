from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class ThinkerCreation(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["email", "username", "first_name", "last_name", "phone", "company", "country"]

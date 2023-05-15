from django.urls import path
from .views import signup, activate_account

app_name = "account"
urlpatterns = [
    path('signup/', signup, name="signup"),
    path('go-to-mailbox', activate_account, name="go-to-mailbox"),
]

from django.urls import path
from .views import signup, activate_account, login_thinker, logout_thinker, profil_thinker

app_name = "account"
urlpatterns = [
    path('signup/', signup, name="signup"),
    path('go-to-mailbox/', activate_account, name="go-to-mailbox"),
    path('login/', login_thinker, name='login'),
    path('logout/', logout_thinker, name="logout"),
    path('profile/', profil_thinker, name="profile"),
]

from django.urls import path
from .views import signup, activate_account, login_thinker, logout_thinker, profil_thinker, \
    ThinkerPasswordChange, ThinkerPasswordReset, ThinkerPasswordResetDone, ThinkerPasswordResetConfirm, \
    ThinkerPasswordResetComplete, change_thinker_email

app_name = "account"
urlpatterns = [
    path('signup/', signup, name="signup"),
    path('go-to-mailbox/', activate_account, name="go-to-mailbox"),
    path('login/', login_thinker, name='login'),
    path('logout/', logout_thinker, name="logout"),
    path('profile/', profil_thinker, name="profile"),
    path('change-email', change_thinker_email, name="change-email"),
    path('new-password/', ThinkerPasswordChange.as_view(), name="change-password"),
    path('reset-password/', ThinkerPasswordReset.as_view(), name="reset-password"),
    path('reset-done/', ThinkerPasswordResetDone.as_view(), name="reset-done"),
    path('reset-confirm/<str:uidb64>/<str:token>/', ThinkerPasswordResetConfirm.as_view(), name="reset-confirm"),
    path('reset-complete/', ThinkerPasswordResetComplete.as_view(), name="reset-complete")
]

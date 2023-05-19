from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from verify_email.email_handler import send_verification_email
from .forms import ThinkerCreationForm, ThinkerProfilForm
from .models import Thinker


def signup(request):

    if request.method == "POST":
        form = ThinkerCreationForm(request.POST)
        if form.is_valid():
            # form.save()
            inactive_user = send_verification_email(request, form)
            return redirect('account:go-to-mailbox')

    else:

        form = ThinkerCreationForm()

    return render(request, 'accounts/signup.html', context={"form": form})


def activate_account(request):
    context = {}
    return render(request, "accounts/signup-valid.html", context=context)


def login_thinker(request):
    context = {}
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            context["error"] = "Email et/ou mot de passe non valide."

    return render(request, 'accounts/login.html', context=context)


def logout_thinker(request):
    logout(request)
    return redirect('index')


def profil_thinker(request):
    context = {}
    if request.method == "POST":
        user_auth = authenticate(email=request.POST.get("email"), password=request.POST.get("password"))
        if user_auth:
            user: Thinker = request.user
            user.phone = request.POST.get('phone')
            user.company = request.POST.get('company')
            user.country = request.POST.get('country')
            user.format_phone_number()
            user.save()
            return redirect('account:profile')
        else:
            # https://docs.djangoproject.com/en/4.2/ref/contrib/messages/#using-messages-in-views-and-templates
            # messages.add_message(request, messages.ERROR, "Le mot de passe n'est pas valide")
            context['error'] = "Mot de passe invalide"
    # model_to_dict(instance)
    context['form'] = ThinkerProfilForm(initial=model_to_dict(request.user, exclude='password'))

    return render(request, "accounts/profil.html", context=context)


class ThinkerPasswordChange(PasswordChangeView):
    template_name = "accounts/change-password.html"
    success_url = reverse_lazy('index')


class ThinkerPasswordReset(PasswordResetView):
    email_template_name = "accounts/reset-password-email.html"
    template_name = "accounts/reset-password.html"
    success_url = reverse_lazy("account:reset-done")


class ThinkerPasswordResetDone(PasswordResetDoneView):
    template_name = "accounts/reset-password-done.html"


class ThinkerPasswordResetConfirm(PasswordResetConfirmView):
    template_name = "accounts/reset-password-confirm.html"
    success_url = reverse_lazy("account:reset-complete")


class ThinkerPasswordResetComplete(PasswordResetCompleteView):
    template_name = "accounts/reset-password-complete.html"

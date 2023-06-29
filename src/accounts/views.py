from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from verify_email.email_handler import send_verification_email
from .forms import ThinkerCreationForm, ThinkerProfilForm, ThinkerEmailForm
from .models import Thinker


def signup(request):

    if request.method == "POST":
        form = ThinkerCreationForm(request.POST)
        # S'il n'est pas valide je vais au return avec les données
        if form.is_valid():
            # form.save()
            inactive_user = send_verification_email(request, form)
            return redirect('account:go-to-mailbox')
    # Si get
    else:

        form = ThinkerCreationForm()

    return render(request, 'accounts/signup.html', context={"form": form})


def activate_account(request):
    # verify email
    return render(request, "accounts/signup-valid.html")


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


@login_required()
def profil_thinker(request):
    context = {}
    if request.method == "POST":
        user_auth = authenticate(email=request.POST.get("email"), password=request.POST.get("password"))
        # Si pas auth je vais charger le formulaire avant le return puis return en prenant l'erreur au passage
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


@login_required()
def change_thinker_email(request):
    user = request.user
    all_users = Thinker.objects.all()
    context = {}

    if request.method == "POST":
        form = ThinkerEmailForm(request.POST)
        # SI pas valide je vais au formulaire avant le return puis return
        if form.is_valid():
            if form.cleaned_data["email"] != user.email:
                messages.add_message(request, messages.ERROR, "Mauvaise adresse mail actuelle renseignée")
                return redirect("account:change-email")

            user_auth = authenticate(email=form.cleaned_data["email"], password=form.cleaned_data["password"])

            if user_auth:
                for other_user in all_users:
                    if form.cleaned_data["new_email"] == other_user.email:
                        messages.add_message(request, messages.ERROR, "Email déjà utilisé")
                        return redirect("account:change-email")

                user.email = form.cleaned_data["new_email"]
                user.save()
                return redirect("account:change-email")

            else:
                messages.add_message(request, messages.ERROR, "Mot de passe invalide")
                return redirect("account:change-email")

    context["form"] = ThinkerEmailForm(initial={"email": user.email})

    return render(request, "accounts/change-email.html", context=context)


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

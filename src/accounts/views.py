from django.shortcuts import render, redirect
from verify_email.email_handler import send_verification_email
from .forms import ThinkerCreation


def signup(request):

    if request.method == "POST":
        form = ThinkerCreation(request.POST)
        if form.is_valid():
            # form.save()
            inactive_user = send_verification_email(request, form)
            return redirect('account:go-to-mailbox')

    else:

        form = ThinkerCreation()

    return render(request, 'accounts/signup.html', context={"form": form})


def activate_account(request):
    context = {}
    return render(request, "accounts/signup_valid.html", context=context)


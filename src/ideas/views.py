import os

import stripe
from django.forms import model_to_dict
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt

from accounts.models import ShippingAddresse, Thinker
from .models import Idea, Comment, Cart
from django.views.generic import CreateView
from .forms import ContactForm, IdeaCommentForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from remy.settings import STRIPE_KEY


stripe.api_key = STRIPE_KEY


def index(request):
    context = {}

    count_ideas = Idea.objects.filter(status=True, paid=False, request=False).count()
    if count_ideas >= 4:
        context["ideas"]: Idea = Idea.objects.filter(status=True,
                                                     paid=False, request=False)[count_ideas - 4:count_ideas][::-1]
    else:
        context["ideas"]: Idea = Idea.objects.filter(status=True, paid=False, request=False)

    count_request_ideas = Idea.objects.filter(status=True, request=True, paid=False).count()
    if count_request_ideas >= 4:
        context["request_ideas"]: Idea = \
            Idea.objects.filter(status=True,
                                request=True, paid=False)[count_request_ideas - 4:count_request_ideas][::-1]
    else:
        context["request_ideas"]: Idea = Idea.objects.filter(status=True, request=True, paid=False)

    return render(request, template_name="ideas/index.html", context=context)


@login_required()
def idea_detail_view(request, slug):
    user = request.user
    idea = get_object_or_404(Idea, slug=slug)
    if idea.paid:
        # Si l'idée est payée
        if user != idea.thinker and user != idea.buyer:
            # Si l'utilisateur est différent de l'auteur ou si l'utilisateur est différent de l'acheteur
            # Si je suis auteur : False and True = False
            # Si je suis acheteur : True and False = False
            # Si je ne suis ni l'un ni l'autre : True and True = True
            return HttpResponse(status=410)

    comments = Comment.objects.filter(idea=idea).order_by('date')

    if request.method == "POST":
        form = IdeaCommentForm(request.POST)
        if form.is_valid():
            form.instance.user = user
            form.instance.idea = idea
            form.save()
            return redirect(idea)
    else:
        form = IdeaCommentForm()

    return render(request, "ideas/idea.html", context={"idea": idea, "form": form,
                                                       "comments": comments})


def add_to_cart(request, slug):
    # user = request.user
    #
    # user_cart, _ = Cart.objects.get_or_create(buyer=user)
    # idea = get_object_or_404(Idea, slug=slug)
    #
    # if request.method == "POST":
    #
    #     if idea in user_cart.ideas.all():
    #         # On ne peut pas ajouter deux fois la même idée
    #         messages.add_message(request, messages.ERROR, "L'idée est déjà dans le panier")
    #         return redirect("ideas:all")
    #
    #     for cart in Cart.objects.all():
    #         # Je vérifie que l'idée ne soit pas dans le panier d'un autre
    #         if idea in cart.ideas.all():
    #             messages.add_message(request, messages.ERROR, "L'idée est déjà dans le panier de quelqu'un.")
    #     else:
    #         user_cart.ideas.add(idea)
    #         # On ajoute au panier et on va dans la vue panier
    #
    #         return redirect("ideas:cart")

    user = request.user
    user_cart, _ = Cart.objects.get_or_create(buyer=user)
    idea = get_object_or_404(Idea, slug=slug)

    if request.method != "POST":
        raise Http404("Requête invalide")

    if user_cart.ideas.filter(id=idea.id).exists() or Cart.objects.filter(ideas__id=idea.id).exists():
        # si l'idée existe dans le panier ou si un panier avec l'idée existe
        messages.add_message(request, messages.ERROR, "L'idée est déjà dans le panier")
        return redirect("ideas:all")
    else:
        user_cart.ideas.add(idea)  # Ajoute l'idée au panier de l'utilisateur
        return redirect("ideas:cart")


@login_required()
def cart(request):
    context = {}
    user = request.user

    context["cart"] = user.cart

    return render(request, "ideas/cart.html", context=context)


def delete_from_cart(request, pk):
    user = request.user
    cart = user.cart
    idea = cart.ideas.get(pk=pk)

    if request.method == "POST":
        cart.ideas.remove(idea)
        if not cart.ideas.all():
            cart.delete()
            # voir pour utiliser messages "Plus rien dans le panier"
            return redirect("index")
    return redirect("ideas:cart")


def create_checkout_session(request):
    cart = request.user.cart

    checkout_data = {
        "locale": "fr",
        "line_items": [{
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': idea.name,
                },
                'unit_amount': int(idea.price * 100),
            },
            'quantity': 1,
        } for idea in cart.ideas.all()],
        "automatic_tax": {'enabled': True},
        "mode": 'payment',
        "invoice_creation": {"enabled": True},
        "shipping_address_collection": {"allowed_countries": ["FR", "BE"]},
        "success_url": request.build_absolute_uri(reverse("ideas:checkout-success")),
        "cancel_url": 'http://127.0.0.1:8000'}

    if request.user.stripe_id:
        checkout_data["customer"] = request.user.stripe_id
        checkout_data["customer_update"] = {"shipping": "auto"}
    else:
        checkout_data["customer_email"] = request.user.email
        checkout_data["customer_creation"] = "always"

    session = stripe.checkout.Session.create(**checkout_data)

    return redirect(session.url, code=303)


def checkout_success(request):
    return render(request, 'ideas/success-payment.html')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    # Penser à renseigner une clé pour la prod
    endpoint_secret = os.getenv('endpoint_secret')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'checkout.session.completed':
        data = event['data']['object']

        user = get_object_or_404(Thinker, email=data['customer_details']['email'])
        cart = user.cart

        if not user.stripe_id:
            user.stripe_id = data["customer"]
            user.save()

        ShippingAddresse.objects.get_or_create(
            thinker=user,
            name=data["shipping_details"]["name"],
            city=data["shipping_details"]["address"]["city"],
            country=data["shipping_details"]["address"]["country"],
            line1=data["shipping_details"]["address"]["line1"],
            line2=data["shipping_details"]["address"]["line2"] or "",
            zip_code=data["shipping_details"]["address"]["postal_code"],
        )

        cart.cart_paid(user=user)

    return HttpResponse(status=200)


def ideas_and_request_ideas_view(request):
    ideas = Idea.objects.filter(status=True, paid=False, request=False)
    request_ideas = Idea.objects.filter(status=True, paid=False, request=True)

    if request.method == "GET":
        search = request.GET.get("search")
        if search:
            ideas = Idea.objects.filter(name__icontains=search, status=True, paid=False, request=False)
            request_ideas = Idea.objects.filter(name__icontains=search, status=True, paid=False, request=True)

    return render(request, "ideas/all.html", context={'ideas': ideas, 'request_ideas': request_ideas})


class IdeaCreateView(LoginRequiredMixin, CreateView):
    model = Idea
    template_name = "ideas/create-idea.html"
    fields = ["name", "summary", "level", "category", "details", "sketch"]
    success_url = reverse_lazy('ideas:create-idea-confirm')

    def form_valid(self, form):
        form.instance.thinker = self.request.user
        return super().form_valid(form)


def idea_create_confirm(request):
    return render(request, "ideas/create-idea-confirm.html")


class RequestIdeaCreateView(LoginRequiredMixin, CreateView):
    model = Idea
    fields = ["name", "summary", "level", "category", "details", "sketch"]
    template_name = "ideas/create-request-idea.html"
    success_url = reverse_lazy('ideas:create-request-idea-confirm')

    def form_valid(self, form):
        form.instance.thinker = self.request.user
        form.instance.request = True
        return super().form_valid(form)


def request_idea_confirm(request):
    return render(request, "ideas/create-request-idea-confirm.html")


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            send_mail(subject=subject,
                      message=f"Message de {email} \n{message}",
                      from_email=None,
                      recipient_list=["remysevestre@yahoo.com"])
            # recipient_list : penser à passer une liste !
            # from_email None (va chercher dans les settings)
            return redirect('ideas:contact-ok')

    else:
        if request.user.is_authenticated:
            form = ContactForm(initial=model_to_dict(request.user, exclude="password"))
        else:
            form = ContactForm()

    return render(request, "ideas/contact.html", context={"form": form})


def contact_view_ok(request):
    return render(request, "ideas/contact-ok.html")


# Vues pour les idées/demandes achetées et pour mes idées postées
@login_required()
def my_ideas(request):
    # Afficher les idées/demandes de l'utilisateur connecté
    user = request.user

    # Mes idées/demandes publiées
    ideas_published = Idea.objects.filter(thinker=user, status=True, paid=False)

    # Mes idées/demandes en attente de validation
    ideas_waiting = Idea.objects.filter(thinker=user, status=False)

    # Mes idées/demandes vendues
    ideas_sold = Idea.objects.filter(thinker=user, paid=True)

    # Mes idées/demandes achetées
    ideas_bought = Idea.objects.filter(buyer=user)

    return render(request, "ideas/my-ideas.html", context={"ideas_published": ideas_published,
                                                           "ideas_waiting": ideas_waiting,
                                                           "ideas_sold": ideas_sold,
                                                           "ideas_bought": ideas_bought})


def about_us(request):
    return render(request, "ideas/about.html")

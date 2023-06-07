from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import Idea, Comment, Cart
from django.views.generic import CreateView
from .forms import ContactForm, IdeaCommentForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


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
    user = request.user

    cart, _ = Cart.objects.get_or_create(buyer=user)
    idea = get_object_or_404(Idea, slug=slug)

    if idea in cart.ideas.all():
        # on ne peut pas ajouter deux fois la même idée
        messages.add_message(request, messages.ERROR, "L'idée est déjà dans le panier")
        return redirect("ideas:all")
    else:
        cart.ideas.add(idea)
        # on ajoute au panier et on va dans la vue panier
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
    cart.ideas.remove(idea)
    if cart.ideas.count() == 0:
        cart.delete()
        # voir pour utiliser messages "Plus rien dans le panier"
        return redirect("index")
    return redirect("ideas:cart")


def create_checkout_session(request):
    pass


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


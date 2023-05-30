from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .models import Idea, RequestIdea
from django.views.generic import DetailView, CreateView
from .forms import ContactForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    count_ideas = Idea.objects.filter(status=True).count()
    ideas: Idea = Idea.objects.filter(status=True)[count_ideas - 4:count_ideas:-1]
    count_request_ideas = RequestIdea.objects.filter(status=True).count()
    request_ideas: RequestIdea = RequestIdea.objects.filter(status=True)[count_request_ideas - 4:count_request_ideas:-1]

    return render(request,
                  template_name="ideas/index.html",
                  context={"ideas": ideas, "request_ideas": request_ideas})


class IdeaDetail(DetailView):
    model = Idea
    template_name = "ideas/idea.html"


class RequestIdeaDetail(DetailView):
    model = RequestIdea
    template_name = "ideas/request-idea.html"
    context_object_name = "request_idea"


def ideas_and_request_ideas_view(request):
    ideas = Idea.objects.filter(status=True)
    request_ideas = RequestIdea.objects.filter(status=True)

    if request.method == "GET":
        search = request.GET.get("search")
        if search:
            ideas = Idea.objects.filter(name__icontains=search)
            request_ideas = RequestIdea.objects.filter(name__icontains=search)

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
    model = RequestIdea
    fields = ["name", "summary", "level", "category", "details"]
    template_name = "ideas/create-request-idea.html"
    success_url = reverse_lazy('ideas:create-request-idea-confirm')

    def form_valid(self, form):
        form.instance.thinker = self.request.user
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
                      recipient_list=["gabrieltrouve5@yahoo.com"])
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

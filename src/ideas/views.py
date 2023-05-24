from django.forms import model_to_dict
from django.shortcuts import render, redirect
from .models import Idea, RequestIdea
from django.views.generic import DetailView
from .forms import ContactForm
from django.core.mail import send_mail


def index(request):
    count_ideas = Idea.objects.filter(status=True).count()
    ideas: Idea = Idea.objects.filter(status=True)[count_ideas - 4:count_ideas]
    count_request_ideas = RequestIdea.objects.filter(status=True).count()
    request_ideas: RequestIdea = RequestIdea.objects.filter(status=True)[count_request_ideas - 4:count_request_ideas]

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


def contact_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        send_mail(subject=subject,
                  message=f"Message de {email} \n{message}",
                  from_email=None,
                  recipient_list=["gabrieltrouve5@yahoo.com"])
        # recipient_list : penser à passer une liste !
        # from_email None (va chercher dans les settings)
        return redirect('ideas:contact-ok')

    # auth verify
    if request.user.is_authenticated:
        form = ContactForm(initial=model_to_dict(request.user, exclude="password"))
    else:
        form = ContactForm()

    return render(request, "ideas/contact.html", context={"form": form})


def contact_view_ok(request):
    return render(request, "ideas/contact-ok.html")

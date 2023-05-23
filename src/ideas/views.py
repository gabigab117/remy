from django.shortcuts import render
from .models import Idea, RequestIdea
from django.views.generic import DetailView


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
    pass

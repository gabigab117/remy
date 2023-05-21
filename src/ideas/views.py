from django.shortcuts import render
from .models import Idea, RequestIdea


def index(request):
    ideas: Idea = Idea.objects.filter(status=True)
    request_ideas: RequestIdea = RequestIdea.objects.filter(status=True)

    return render(request,
                  template_name="ideas/index.html",
                  context={"ideas": ideas, "request_ideas": request_ideas})

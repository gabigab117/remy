from django.shortcuts import render
from .models import Idea, RequestIdea


def index(request):
    count_ideas = Idea.objects.all().count()
    ideas: Idea = Idea.objects.all()[count_ideas - 4:count_ideas]
    count_request_ideas = RequestIdea.objects.all().count()
    request_ideas: RequestIdea = RequestIdea.objects.all()[count_request_ideas - 4:count_request_ideas]

    return render(request,
                  template_name="ideas/index.html",
                  context={"ideas": ideas, "request_ideas": request_ideas})

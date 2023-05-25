from django.urls import path
from .views import IdeaDetail, RequestIdeaDetail, ideas_and_request_ideas_view, contact_view, contact_view_ok, \
    IdeaCreateView, RequestIdeaCreateView
from django.contrib.auth.decorators import login_required


app_name = "ideas"
urlpatterns = [
    path('all/', ideas_and_request_ideas_view, name="all"),
    path('idea/<str:slug>/', IdeaDetail.as_view(), name="idea-detail"),
    path('request-idea/<str:slug>', RequestIdeaDetail.as_view(), name="request-idea-detail"),
    path('contact/', contact_view, name="contact"),
    path('contact-ok/', contact_view_ok, name="contact-ok"),
    path('create-idea/', login_required(IdeaCreateView.as_view()), name="create-idea"),
    path('create-request-idea', login_required(RequestIdeaCreateView.as_view()), name="create-request-idea")
]

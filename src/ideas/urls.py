from django.urls import path
from .views import IdeaDetail, RequestIdeaDetail, ideas_and_request_ideas_view, contact_view, contact_view_ok


app_name = "ideas"
urlpatterns = [
    path('all/', ideas_and_request_ideas_view, name="all"),
    path('idea/<str:slug>/', IdeaDetail.as_view(), name="idea-detail"),
    path('request-idea/<str:slug>', RequestIdeaDetail.as_view(), name="request-idea-detail"),
    path('contact/', contact_view, name="contact"),
    path('contact-ok/', contact_view_ok, name="contact-ok"),
]

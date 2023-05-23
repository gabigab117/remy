from django.urls import path
from .views import IdeaDetail, RequestIdeaDetail


app_name = "ideas"
urlpatterns = [
    path('idea/<str:slug>/', IdeaDetail.as_view(), name="idea-detail"),
    path('request-idea/<str:slug>', RequestIdeaDetail.as_view(), name="request-idea-detail"),
]

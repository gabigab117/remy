from django.urls import path
from .views import idea_detail_view, ideas_and_request_ideas_view, contact_view, contact_view_ok, \
    IdeaCreateView, RequestIdeaCreateView, idea_create_confirm, request_idea_confirm, add_to_cart,\
    cart, delete_from_cart


app_name = "ideas"
urlpatterns = [
    path('all/', ideas_and_request_ideas_view, name="all"),
    path('idea/<str:slug>/', idea_detail_view, name="idea-detail"),
    path('add-to-cart/<str:slug>/', add_to_cart, name="add-to-cart"),
    path('cart/', cart, name="cart"),
    path('delete-from-cart/<int:pk>/', delete_from_cart, name="delete-from-cart"),
    path('contact/', contact_view, name="contact"),
    path('contact-ok/', contact_view_ok, name="contact-ok"),
    path('create-idea/', IdeaCreateView.as_view(), name="create-idea"),
    path('create-request-idea/', RequestIdeaCreateView.as_view(), name="create-request-idea"),
    path('create-idea-confirm/', idea_create_confirm, name="create-idea-confirm"),
    path('create-request-idea-confirm/', request_idea_confirm, name="create-request-idea-confirm"),
]

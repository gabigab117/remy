from django.contrib import admin
from .models import Category, Idea, RequestIdea

admin.site.register(Category)


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ("name", "summary", "level", "category", "thinker", "status")
    list_editable = ("status", )
    list_display_links = ("name", )
    search_fields = ("name", "details", "summary", )
    list_filter = ("status", "category", )


@admin.register(RequestIdea)
class RequestIdea(admin.ModelAdmin):
    list_display = ("name", "summary", "level", "category", "thinker", "status")
    list_editable = ("status", )
    list_display_links = ("name", )
    search_fields = ("name", "details", "summary", )
    list_filter = ("status", "category", )

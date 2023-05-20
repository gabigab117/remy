from django.contrib import admin
from .models import Category, Idea, RequestIdea

admin.site.register(Category)
# admin.site.register(Idea)
admin.site.register(RequestIdea)


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ["name", "summary", "level", "category", "thinker", "status"]
    list_editable = ["status"]
    list_display_links = ["name"]
    search_fields = ["name"]
    list_filter = ["status"]

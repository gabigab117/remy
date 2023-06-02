from django.contrib import admin
from .models import Category, Idea, RequestIdea, Comment

admin.site.register(Category)


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ("name", "summary", "level", "category", "thinker", "date", "status")
    list_editable = ("status", )
    list_display_links = ("name", )
    search_fields = ("name", "details", "summary", )
    list_filter = ("status", "category", )


@admin.register(RequestIdea)
class RequestIdeaAdmin(admin.ModelAdmin):
    list_display = ("name", "summary", "level", "category", "thinker", "date", "status")
    list_editable = ("status", )
    list_display_links = ("name", )
    search_fields = ("name", "details", "summary", )
    list_filter = ("status", "category", )


@admin.register(Comment)
class IdeaCommentAdmin(admin.ModelAdmin):
    list_display = ("idea", "request_idea", "user", "date")
    list_display_links = ("date", )
    search_fields = ("user", )

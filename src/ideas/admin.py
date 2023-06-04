from django.contrib import admin
from .models import Category, Idea, Comment

admin.site.register(Category)


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ("name", "summary", "level", "category", "thinker", "date", "status", "request", "paid", )
    list_editable = ("status", "request", "paid", )
    list_display_links = ("name", )
    search_fields = ("name", "details", "summary", )
    list_filter = ("status", "category", "paid", "request", )


@admin.register(Comment)
class IdeaCommentAdmin(admin.ModelAdmin):
    list_display = ("idea", "user", "date")
    list_display_links = ("date", )
    search_fields = ("user", )

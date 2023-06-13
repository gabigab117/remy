from django.contrib import admin
from .models import Category, Idea, Comment, Cart

admin.site.register(Category)
admin.site.register(Cart)


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ("name", "summary", "level", "category",
                    "thinker", "date", "status", "request", "paid", "price", "buyer", "ordered_date")
    list_editable = ("status", "request", "paid", "price", "buyer")
    list_display_links = ("name", )
    search_fields = ("name", "details", "summary", )
    list_filter = ("status", "category", "paid", "request", )


@admin.register(Comment)
class IdeaCommentAdmin(admin.ModelAdmin):
    list_display = ("idea", "user", "date")
    list_display_links = ("date", )
    search_fields = ("user", )

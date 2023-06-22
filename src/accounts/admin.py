from django.contrib import admin
from .models import Thinker, Moderator, ShippingAddresse

admin.site.register(Thinker)
admin.site.register(Moderator)


@admin.register(ShippingAddresse)
class ShippingAddresseAdmin(admin.ModelAdmin):
    list_display = ("thinker", "name", "city")
    list_filter = ("thinker", )
    search_fields = ("thinker__email", "name", "city")

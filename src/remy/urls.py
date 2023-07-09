from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings
from ideas.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('account/', include('accounts.urls')),
    path('verification/', include('verify_email.urls')),
    path('ideas/', include('ideas.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


admin.site.site_header = 'Invent for Tomorow'
admin.site.site_title = "Invent for Tomorow"

""" kradleco URL Configuration """

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('kradleco.apps.landing.urls')),
    path('', include('kradleco.apps.home.urls')),
    path('noticias/', include('kradleco.apps.noticias.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('', include('kradleco.apps.users.urls')),
    path('', include('django.contrib.auth.urls')),
    path('payments/', include('kradleco.apps.payments.urls')),
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

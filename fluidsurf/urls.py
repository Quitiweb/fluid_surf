""" fluidsurf URL Configuration """

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fluidsurf.apps.home.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('', include('fluidsurf.apps.users.urls')),
    path('', include('django.contrib.auth.urls')),
    path('dashboard/', include('fluidsurf.apps.dashboard.urls')),
    path('payments/', include('fluidsurf.apps.payments.urls')),
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

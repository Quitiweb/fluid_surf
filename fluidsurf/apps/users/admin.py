from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'tipo_de_usuario']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': (
            'validado', 'tipo_de_usuario', 'stripe_id', 'alias', 'CV', 'profile_pic',
            'main_pic', 'telefono', 'wishlist', 'pais'
        )}),
    )


class CustomGaleria(admin.ModelAdmin):
    list_display = ['user', 'imagen', ]


admin.site.register(CustomUser, CustomUserAdmin)

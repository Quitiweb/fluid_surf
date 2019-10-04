from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    list_display = ['username', 'email', 'tipo_de_usuario']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': (
            'validado', 'tipo_de_usuario', 'alias', 'CV', 'profile_pic', 'main_pic', 'telefono', )}),
    )


class CustomGaleria(admin.ModelAdmin):
    list_display = ['user', 'imagen', ]


admin.site.register(CustomUser, CustomUserAdmin)

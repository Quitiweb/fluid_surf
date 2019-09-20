from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Empresa, GaleriaUsuario, Comentario, Autonomo, MiPerfil


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['username', 'email', 'tipo_de_usuario']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': (
            'validado', 'tipo_de_usuario', 'alias', 'CV', 'profile_pic', 'main_pic', 'telefono', 'is_marca', 'is_espacio', 'is_empresa', 'is_autonomo', 'logo',
            'foto_perfil', 'facebook', 'youtube', 'linkedin', 'twitter', )}),
    )


class CustomGaleria(admin.ModelAdmin):
    list_display = ['user', 'imagen', ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Empresa)
admin.site.register(Autonomo)
admin.site.register(GaleriaUsuario, CustomGaleria)
admin.site.register(Comentario)
admin.site.register(MiPerfil)

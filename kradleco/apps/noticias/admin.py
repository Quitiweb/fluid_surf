from django.contrib import admin

from .models import Post


# To launch a jQuery for Slug auto-fill
class PostAdmin(admin.ModelAdmin):

    class Media:
        js = (
            'main/assets/js/jquery.min.js',
            'main/assets/js/admin.js',
        )


admin.site.register(Post, PostAdmin)

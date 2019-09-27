from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash

from fluidsurf.apps.home.models import Producto
from fluidsurf.apps.users.models import CustomUser, MiPerfil
from .forms import ContactForm, ChangeUserForm, PhotographerForm, PasswordChangeCustomForm, AddProductForm
from ..helpers.helper import enviar_email, grouped, news_to_get, users_to_get


def index(request):
    if request.user.is_authenticated:
        template = loader.get_template('home/index.html')

        # noticias = Post.objects.filter(
        #     fecha_de_publicacion__lte=timezone.now()
        # ).order_by('-fecha_de_publicacion')[:news_to_get(Post.objects.count())]
        #
        # noticias_gr = grouped(noticias, 3)

        productos = Producto.objects.filter().all()

        usuarios = CustomUser.objects.exclude(
            username=request.user.username
        )[:users_to_get(CustomUser.objects.count() - 1)]

        usuarios_conectados = CustomUser.objects.exclude(
            username=request.user.username
        ).filter(Q(is_marca=True) | Q(is_espacio=True), Q(validado=True))[:users_to_get(CustomUser.objects.count() - 1)]

        context = {
            'productos': productos,
            'usuarios': usuarios,
            'usuarios_conectados': usuarios_conectados,
        }

    else:
        return redirect('login')

    return HttpResponse(template.render(context, request))


def mensaje_enviado(request):
    return render(request, 'home/mensaje-enviado.html')


def formulario(request):
    template = loader.get_template('home/formulario.html')

    # if request.method == 'GET':
        # form = FormularioForm()
    # else:
        # # form = FormularioForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #
        #     subject = 'Kradleco nueva solicitud recibida'
        #     from_email = form.cleaned_data['email']
        #     nombre = form.cleaned_data['nombre']
        #     enlace = 'https://www.kradleco.es/admin/landing/solicitud/'
        #     message = 'Solicitud recibida de: ' + nombre + '\nCon email: ' + from_email + \
        #               '\n\nPara ver dicha solicitud, visita: ' + enlace
        #
        #     enviar_email(subject, message)
        #
        #     form = FormularioForm()
        #
        #     return redirect('solicitud-recibida')
        # else:
        #     print('Error en el formulario')

    context = {
        # 'form': form,
    }

    return HttpResponse(template.render(context, request))


def solicitud_recibida(request):
    return render(request, 'home/solicitud-recibida.html')


def mi_cuenta(request):
    template = loader.get_template('home/mi-cuenta.html')
    context = {}

    if request.user.is_authenticated:
        if request.method == 'GET':
            passform = PasswordChangeCustomForm(request.user)
            form = ChangeUserForm(instance=request.user)
            if request.user.tipo_de_usuario == "FOTOGRAFO":
                photo_form = PhotographerForm(instance=request.user)
        else:
            passform = PasswordChangeCustomForm(request.user, request.POST)
            form = ChangeUserForm(request.POST, instance=request.user)
            if request.user.tipo_de_usuario == "FOTOGRAFO":
                photo_form = PhotographerForm(request.POST,  request.FILES, instance=request.user)
                if photo_form.is_valid():
                    photo_form.save()
            if form.is_valid():
                messages.add_message(request, messages.SUCCESS, 'Tu perfil se ha guardado correctamente')
                form.save()

                if passform.is_valid():
                    pwd = passform.save()
                    update_session_auth_hash(request, pwd)  # Important!
                    messages.success(request, 'Contraseña cambiada con éxito')
                elif passform.data['old_password'] or passform.data['new_password1'] or passform.data['new_password2']:
                    messages.warning(request, passform.errors)

        if request.user.tipo_de_usuario == "FOTOGRAFO":
            context = {
                'form': form,
                'passform': passform,
                'photo_form': photo_form
            }
        else:
            context = {
                'form': form,
                'passform': passform,
            }
        return HttpResponse(template.render(context, request))
    else:
        return redirect("/login")


def subir_producto(request):
    template = loader.get_template('home/subir-producto.html')

    if request.method == "GET":
        form = AddProductForm()
    else:
        form = AddProductForm(request.POST, request.FILES)

        for afile in request.FILES:
            # File(file=afile, files=test).save()
            print('archivo')

        if form.is_valid():
            producto = form.save(commit=False)
            producto.user = request.user
            producto.save()
            messages.success(request, 'Tu producto se ha subido correctamente')
        else:
            messages.warning(request, form.errors)

    context = {
        'form': form,
    }

    return HttpResponse(template.render(context, request))


def producto(request, id='0'):
    template = loader.get_template('home/producto.html')

    producto = Producto.objects.filter(id=id).first()

    if producto is None:
        return redirect('/')

    imagenes = [producto.imagen0]

    for i in range(10):
        if getattr(producto, 'imagen' + str(i)):
            imagenes.append(getattr(producto, 'imagen' + str(i)))
        else:
            break

    context = {
        'producto': producto,
        'imagenes': imagenes
    }

    return HttpResponse(template.render(context, request))

import numpy as np

from io import BytesIO
from pickle import dump, load, UnpicklingError

from django.conf import settings

from PIL import Image, ImageDraw, ImageFont, ImageMath
from imagekit.registry import register
from imagekit.specs import ImageSpec


def add_watermark(image, watermark):
    rgba_image = image.convert('RGBA')
    rgba_watermark = watermark.convert('RGBA')

    image_x, image_y = rgba_image.size
    watermark_x, watermark_y = rgba_watermark.size

    watermark_scale = max(image_x / (2.0 * watermark_x), image_y / (2.0 * watermark_y))
    new_size = (int(watermark_x * watermark_scale), int(watermark_y * watermark_scale))
    rgba_watermark = rgba_watermark.resize(new_size, resample=Image.ANTIALIAS)

    rgba_watermark_mask = rgba_watermark.convert("L").point(lambda x: min(x, 100))
    rgba_watermark.putalpha(rgba_watermark_mask)

    watermark_x, watermark_y = rgba_watermark.size
    rgba_image.paste(rgba_watermark, ((image_x - watermark_x) // 2, (image_y - watermark_y) // 2), rgba_watermark_mask)

    return rgba_image


class WatermarkProcessor(object):
    watermark = Image.open(settings.WATERMARK_IMAGE)

    def process(self, image):
        return add_watermark(image, self.watermark)


class Watermark(ImageSpec):
    processors = [WatermarkProcessor()]
    format = 'JPEG'
    options = {'quality': 75}


register.generator('home:watermark', Watermark)

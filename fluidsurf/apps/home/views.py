from datetime import date

import stripe
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.utils.translation import ugettext_lazy as _

from fluidsurf.apps.home.models import Producto, Ubicacion, Compra
from fluidsurf.apps.users.models import CustomUser
from .forms import ChangeUserForm, PhotographerForm, PasswordChangeCustomForm, AddProductForm
from ..helpers.helper import users_to_get

from django.conf import settings

from PIL import Image
from imagekit.registry import register
from imagekit.specs import ImageSpec

stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    template = loader.get_template('home/index.html')

    # noticias = Post.objects.filter(
    #     fecha_de_publicacion__lte=timezone.now()
    # ).order_by('-fecha_de_publicacion')[:news_to_get(Post.objects.count())]
    #
    # noticias_gr = grouped(noticias, 3)

    productos = Producto.objects.filter(stock=1)[:10]

    productos2 = Producto.objects.filter(stock=1)[11:20]

    productos_all = Producto.objects.filter(stock=1).all()

    p_eu = 0
    p_af = 0
    p_as = 0
    p_oc = 0
    p_na = 0
    p_sa = 0
    for producto in productos_all:
        if producto.spot == 'Europa':
            p_eu += 1
        if producto.spot == 'Africa':
            p_af += 1
        if producto.spot == 'Asia':
            p_as += 1
        if producto.spot == 'Oceania':
            p_oc += 1
        if producto.spot == 'America del Norte':
            p_na += 1
        if producto.spot == 'America del Sur':
            p_sa += 1

    usuarios = CustomUser.objects.exclude(
        username=request.user.username
    )[:users_to_get(CustomUser.objects.count() - 1)]

    API_KEY = getattr(settings, 'BING_MAPS_API_KEY', None)

    ubicaciones = Ubicacion.objects.filter().all()

    context = {
        'productos': productos,
        'producto2': productos2,
        'usuarios': usuarios,
        'API_KEY': API_KEY,
        'ubicaciones': ubicaciones,
        'p_eu': p_eu,
        'p_af': p_af,
        'p_as': p_as,
        'p_oc': p_oc,
        'p_na': p_na,
        'p_sa': p_sa,
    }

    return HttpResponse(template.render(context, request))


def mensaje_enviado(request):
    return render(request, 'home/mensaje-enviado.html')


def formulario(request):
    template = loader.get_template('home/formulario.html')
    context = {

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
                photo_form = PhotographerForm(request.POST, request.FILES, instance=request.user)
                if photo_form.is_valid():
                    photo_form.save()
            if form.is_valid():
                messages.add_message(request, messages.SUCCESS, 'Tu perfil se ha guardado correctamente')
                form.save()
                if passform.is_valid():
                    pwd = passform.save()
                    update_session_auth_hash(request, pwd)  # Important!
                    messages.success(request, 'Contraseña cambiada con éxito')
                elif passform.data['new_password1'] or passform.data['new_password2']:
                    messages.warning(request, passform.errors)

                return redirect('mi-cuenta')
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

        if form.is_valid():
            producto = form.save(commit=False)
            producto.user = request.user

            files = request.FILES.getlist('imagen0') + request.FILES.getlist('imagen1') + request.FILES.getlist(
                'imagen2') + \
                    request.FILES.getlist('imagen3') + request.FILES.getlist('imagen4') + request.FILES.getlist(
                'imagen5') + \
                    request.FILES.getlist('imagen6') + request.FILES.getlist('imagen7') + request.FILES.getlist(
                'imagen8') + \
                    request.FILES.getlist('imagen9')

            if 0 < len(files) <= 10:  # Si nos llegan fotos nuevas las guardamos
                counter = 0
                total_size = 0
                upload = True
                for afile in files:
                    if afile.size > 5242880:
                        messages.warning(request, 'Al menos una de tus fotos tiene un peso superior a 5MB. '
                                                  'Recuerda que cada foto puede pesar como mucho 5MB y el total de todas 25MB.')
                        upload = False
                    else:
                        total_size += afile.size
                        producto.__setattr__('imagen' + str(counter), afile)
                        counter += 1

                if total_size < 26214400 and upload:
                    producto.save()
                    messages.success(request, 'Tu producto se ha subido correctamente')
                else:
                    if not upload:
                        pass
                    else:
                        messages.warning(request, 'Has subido fotos con un peso superior a 25MB. '
                                                  'Recuerda que cada foto puede pesar como mucho 5MB y el total de todas 25MB.')
            else:
                messages.warning(request, 'Tienes que subir al menos una foto para tu producto. Recuerda que no puedes '
                                          'superar las 10 fotos.')
        else:
            messages.warning(request, form.errors)

    context = {
        'form': form,
    }

    return HttpResponse(template.render(context, request))


def producto(request, id='0'):
    template = loader.get_template('home/producto.html')

    producto = Producto.objects.filter(id=id, stock=1).first()

    if producto is None:
        return redirect('/')

    if request.method == "POST":

        if 'wishlist' in request.POST:
            listaDeseos = request.user.wishlist.split(',')
            status = True
            for item in listaDeseos:
                if item == str(id):
                    status = False

            if status:
                request.user.wishlist += str(id) + ","
                request.user.save()
                messages.success(request, _('Product added to your wishlist'))
            else:
                messages.warning(request, _('You already have that product in your wishlist'))
        else:
            charge = stripe.Charge.create(
                amount=producto.precio * 100,
                currency='eur',
                description='Pago de producto',
                source=request.POST['stripeToken']
            )

            if charge:
                producto.stock = 0
                producto.save()

                compra = Compra(
                    user = request.user,
                    producto = producto,
                    fecha = date.today()
                )
                compra.save()

            return render(request, 'payments/charge.html')

    imagenes = []

    for i in range(10):
        if getattr(producto, 'imagen' + str(i)):
            imagenes.append(getattr(producto, 'imagen' + str(i)))
        else:
            break

    context = {
        'producto': producto,
        'imagenes': imagenes,
        'key': settings.STRIPE_PUBLISHABLE_KEY,
        'stripe': True
    }

    return HttpResponse(template.render(context, request))



def zona(request, nombre=''):
    template = loader.get_template('home/zona.html')

    zona = Ubicacion.objects.filter(direccion=nombre).first()

    if zona is None:
        return redirect('/')

    productos = []

    for i in Producto.objects.filter(stock=1).all():
        if i.spot == nombre:
            productos.append(i)

    context = {
        'zona' : zona,
        'productos': productos
    }

    return HttpResponse(template.render(context, request))


def perfil(request, nombre=''):
    template = loader.get_template('home/perfil.html')

    user = CustomUser.objects.filter(username=nombre).first()

    if not user:
        return redirect("/")

    productos = []

    for i in Producto.objects.filter(stock=1).all():
        if i.user == user:
            productos.append(i)

    context = {
        'user': user,
        'productos': productos
    }

    return HttpResponse(template.render(context, request))


def wishlist(request):
    template = loader.get_template('home/wishlist.html')

    productos = []
    if len(request.user.wishlist) > 0:

        lista = request.user.wishlist.split(',')

        for item in lista:
            if item == lista[-1]:
                pass
            else:
                producto = Producto.objects.filter(id=item, stock=1).first()
                if producto:
                        productos.append(producto)

        if request.method == "POST":
            request.user.wishlist = ''
            request.user.save()
            messages.success(request, _('Wishlist emptied succesfully'))
            return redirect('wishlist')

    context = {
        'productos': productos,
    }

    return HttpResponse(template.render(context, request))


# MARCA DE AGUA PARA LAS FOTOGRAFIAS
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

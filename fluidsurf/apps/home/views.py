import os
import re

from io import BytesIO
import json
import zipfile
import urllib
from datetime import date
import braintree

import stripe
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, BadHeaderError
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.utils.translation import ugettext_lazy as _
from django.views.defaults import page_not_found

from fluidsurf.apps.home.filters import ProductoFilter
from fluidsurf.apps.home.models import Producto, Ubicacion, Compra
from fluidsurf.apps.users.models import CustomUser
from .forms import ChangeUserForm, PhotographerForm, PasswordChangeCustomForm, AddProductForm, EditProductForm, \
    DenunciaForm, ContactForm
from ..helpers.helper import users_to_get

from django.conf import settings

from decimal import Decimal


from PIL import Image
from imagekit.registry import register
from imagekit.specs import ImageSpec

stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    template = loader.get_template('home/index.html')

    prod_list = Producto.objects.filter(stock__gte=1, user__is_active=True, user__validado=True).all()
    prod_filter = ProductoFilter(request.GET, queryset=prod_list)

    if request.user.is_authenticated and request.user.tipo_de_usuario == "FOTOGRAFO" and not request.user.validado:
        messages.warning(request, _("Your profile ins't active yet. Please, wait until "
                                    "your first product gets validated by an admin to start selling."))

    API_KEY = getattr(settings, 'BING_MAPS_API_KEY', 0)

    ubicaciones = Ubicacion.objects.filter().all()

    context = {
        'filter': prod_filter,
        'API_KEY': API_KEY,
        'ubicaciones': ubicaciones,
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
                    fotografo = photo_form.save(commit=False)
                    fotografo.CV = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', fotografo.CV)
                    fotografo.CV = re.sub(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?", '', fotografo.CV)
                    fotografo.save()
            if form.is_valid():
                messages.add_message(request, messages.SUCCESS, 'Tu perfil se ha guardado correctamente')
                form.save()
            else:
                print(form.errors)
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
                'photo_form': photo_form,
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

    current = 0

    if request.user.is_authenticated:
        if request.method == "GET":

            if Producto.objects.all().count() > 0:
                current = Producto.objects.latest('id').id + 1

            form = AddProductForm()
        else:

            if Producto.objects.all().count() > 0:
                current = Producto.objects.latest('id').id + 1
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

                        # Busca los usuarios en la zona del producto para despues mandarles un mail
                        usuarios = CustomUser.objects.filter(tipo_de_usuario="SURFERO", zona=producto.spot).all()

                        mails = []
                        for usuario in usuarios:
                            if usuario.email:
                                mails.append(usuario.email)
                        mails.append(settings.SERVER_EMAIL)

                        subject = _("New product in your area")
                        message = producto.user.first_name + " " + producto.user.last_name + str(
                            _(" has uploaded a product nearby you"))
                        message += "\n You can check it here: http://127.0.0.1:8000/producto/" + str(producto.id)  # TODO Añadir link
                        from_email = settings.SERVER_EMAIL
                        to_mail = mails

                        try:
                            send_mail(subject, message, from_email, [to_mail, settings.SERVER_EMAIL])
                        except BadHeaderError:
                            return HttpResponse('Invalid header found')
                    else:
                        if not upload:
                            pass
                        else:
                            messages.warning(request, 'Has subido fotos con un peso superior a 25MB. '
                                                      'Recuerda que cada foto puede pesar como mucho 5MB y el total de todas 25MB.')
                else:
                    messages.warning(request,
                                     'Tienes que subir al menos una foto para tu producto. Recuerda que no puedes '
                                     'superar las 10 fotos.')
            else:
                messages.warning(request, form.errors)
    else:
        return redirect('index')
    context = {
        'form': form,
        'current': current,
    }

    return HttpResponse(template.render(context, request))


def producto(request, id='0'):
    template = loader.get_template('home/producto.html')

    producto = Producto.objects.filter(id=id, stock=1, user__validado=True, user__is_active=True).first()

    prod_list = Producto.objects.filter(stock=1).all()
    prod_filter = ProductoFilter(request.GET, queryset=prod_list)

    API_KEY = getattr(settings, 'BING_MAPS_API_KEY', None)

    ubicaciones = Ubicacion.objects.filter().all()

    if request.user.is_authenticated:
        listaDeseos = request.user.wishlist.split(',')
        status = True
        for item in listaDeseos:
            if item == str(id):
                status = False
    else:
        status = ''

    if producto is None:
        return redirect('/')

    productform = EditProductForm(instance=producto)

    if request.method == "POST":
        if request.user.is_authenticated:
            if producto.user == request.user:
                if 'editProduct' in request.POST:
                    productform = EditProductForm(request.POST, instance=producto)
                    if productform.is_valid():
                        productform.save()
                        messages.success(request, _('Your product was saved successfully'))
                    else:
                        messages.warning(request, _('There was an error while trying to save your product'))
                elif 'deleteProduct' in request.POST:
                    producto.delete()
                    messages.success(request, _('Your product was deleted successfully'))
                    return redirect('/perfil/' + request.user.username)
                else:
                    messages.warning(request, _('You are the owner of this product, you cannot do actions over it.'))
            else:
                if 'wishlist' in request.POST:
                    if status:
                        request.user.wishlist += str(id) + ","
                        request.user.save()
                        messages.success(request, _('Product added to your wishlist'))
                    else:
                        for item in listaDeseos:
                            if item == str(id):
                                listaDeseos.remove(item)
                                request.user.wishlist = ",".join(listaDeseos)
                                request.user.save()
                                messages.success(request, _('Product removed from your wishlist'))
                    return HttpResponseRedirect(request.path_info)
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
                            comprador=request.user,
                            vendedor=producto.user,
                            producto=producto,
                            fecha=date.today()
                        )
                        compra.save()

                        if request.user.email:
                            subject = _("Your FluidSurf purchase")
                            message = _(
                                "Thank you for buying a product in FluidSurf!. You can check it in your Purchase History.")
                            message += "\nID: OR" + str(compra.id)
                            from_email = settings.SERVER_EMAIL
                            to_mail = request.user.email

                            try:
                                send_mail(subject, message, from_email, [to_mail, settings.SERVER_EMAIL])
                            except BadHeaderError:
                                return HttpResponse('Invalid header found')
                        if producto.user.email:
                            subject = _("Your product has been sold!")
                            message = str(_("Your product ")) + producto.nombre + str(_(
                                " has been sold to ")) + compra.comprador.first_name + " " + compra.comprador.last_name + "!"
                            message += "\nYou can check it in your Sales History."
                            message += "\nID: OR" + str(compra.id)
                            from_email = settings.SERVER_EMAIL
                            to_mail = producto.user.email

                            try:
                                send_mail(subject, message, from_email, [to_mail, settings.SERVER_EMAIL])
                            except BadHeaderError:
                                return HttpResponse('Invalid header found')

                        return render(request, 'payments/charge.html')

    imagenes = []

    for i in range(10):
        if getattr(producto, 'imagen' + str(i)):
            imagenes.append(getattr(producto, 'imagen' + str(i)))
        else:
            break

    A = imagenes[:2]
    B = imagenes[2:]

    context = {
        'producto': producto,
        'productform': productform,
        'filter': prod_filter,
        'imagenes': A,
        'imagenes2': B,
        'ubicaciones': ubicaciones,
        'in_wishlist': not status,
        'key': settings.STRIPE_PUBLISHABLE_KEY,
        'stripe': True,
        'API_KEY': API_KEY
    }

    return HttpResponse(template.render(context, request))


def zona(request, nombre=''):
    template = loader.get_template('home/zona.html')

    ubicaciones = Ubicacion.objects.filter().all()

    zona = Ubicacion.objects.filter(spot=nombre).first()

    if zona is None:
        return redirect('/')

    API_KEY = getattr(settings, 'BING_MAPS_API_KEY', 0)

    prod_list = Producto.objects.filter(spot=zona, stock=1, user__validado=True, user__is_active=True).all()
    prod_filter = ProductoFilter(request.GET, queryset=prod_list)

    context = {
        'zona': zona,
        'filter': prod_filter,
        'API_KEY': API_KEY,
        'ubicaciones': ubicaciones,
    }

    return HttpResponse(template.render(context, request))


def perfil(request, id=''):
    template = loader.get_template('home/perfil.html')

    user = CustomUser.objects.filter(id=id).first()

    prod_list = Producto.objects.filter(user=user, stock=1, user__validado=True).all()
    prod_filter = ProductoFilter(request.GET, queryset=prod_list)

    ubicaciones = Ubicacion.objects.filter().all()

    API_KEY = getattr(settings, 'BING_MAPS_API_KEY', None)

    if not user:
        return redirect("/")

    form = DenunciaForm()

    if request.method == "POST":
        form = DenunciaForm(request.POST)

        if form.is_valid():
            denuncia = form.save(commit=False)
            denuncia.emisor = request.user
            denuncia.receptor = user
            denuncia.save()
            messages.success(request, _('Your report has been submitted'))

    context = {
        'usuario': user,
        'form': form,
        'API_KEY': API_KEY,
        'filter': prod_filter,
        'ubicaciones': ubicaciones,
    }

    return HttpResponse(template.render(context, request))


def wishlist(request):
    template = loader.get_template('home/wishlist.html')

    if request.user.is_authenticated:
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
                messages.success(request, _('Wishlist emptied successfully'))
                return redirect('wishlist')

        context = {
            'productos': productos,
        }
    else:
        return redirect('index')

    return HttpResponse(template.render(context, request))


def historial(request):
    template = loader.get_template('home/historial.html')

    if request.user.is_authenticated:
        compras = Compra.objects.filter(comprador=request.user).all()
        ventas = Compra.objects.filter(vendedor=request.user).all()

        if request.method == 'POST':
            if request.user.tipo_de_usuario == "FOTOGRAFO":
                compra = Compra.objects.filter(id=request.POST.get('restock')).first()
                compra.producto.stock = 1
                compra.producto.save()
            elif request.user.tipo_de_usuario == "SURFERO":

                compra = Compra.objects.filter(id=request.POST.get('download')).first()

                if compra.descargas > 0:
                    compra.descargas -= 1
                    compra.save()

                    # Añado los archivo que quiero subir al zip a un array
                    filenames = []
                    for i in range(10):
                        if getattr(compra.producto, 'imagen' + str(i)):
                            imagen = getattr(compra.producto, 'imagen' + str(i))
                            filenames.append(str(imagen))
                        else:
                            break

                    # Nombre de la carpeta que va a contener el archivo zip
                    zip_subdir = "FluidSurf -" + str(compra)
                    zip_filename = "fs-purchase.zip"

                    # El compresor a zip
                    s = BytesIO()
                    zf = zipfile.ZipFile(s, "w")

                    for fpath in filenames:
                        # Saca la ruta para los archivos dentro del zip
                        fdir, fname = os.path.split(fpath)
                        zip_path = os.path.join(zip_subdir, fname)

                        # Añade el archivo a la ruta
                        zf.write('media/' + fpath, zip_path)
                    # Se cierra el archivo zip para guardar
                    zf.close()
                    # Coge el archivo zip
                    resp = HttpResponse(s.getvalue())
                    # Y se prepara para ser devuelto
                    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

                    return resp
                else:
                    messages.warning(request, _('Sorry, you exceeded the download limit of this product.'))
            return redirect('historial')
    else:
        return redirect('index')
    context = {
        'compras': compras,
        'ventas': ventas
    }

    return HttpResponse(template.render(context, request))


def change_image(request):
    if request.method == 'POST':
        image = request.FILES['changeImage']

        request.user.profile_pic = image
        request.user.save()

        messages.success(request, _('Profile pic changed successfully!'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def contacto(request):
    template = loader.get_template('home/contacto.html')

    form = ContactForm()

    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():

            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode("utf-8")
            req = urllib.request.Request(url, data)
            response = urllib.request.urlopen(req)
            result = json.load(response)
            ''' End reCAPTCHA validation '''

            if result['success']:

                subject = 'FluidSurf formulario de contacto'
                from_email = form.cleaned_data['from_email']
                message = 'Email recibido de: ' + from_email + '\n\n' + form.cleaned_data['message']

                enviar_email(subject, message, from_email)

                messages.success(request, _('Your message was sent successfully!'))
            else:
                messages.warning(request, _('Invalid reCAPTCHA. Please try again.'))
        else:
            print(form.errors)

    context = {
        'form': form
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
    options = {'quality': 50}


register.generator('home:watermark', Watermark)


def enviar_email(subject, message, from_email):
    try:
        send_mail(subject, message, from_email, ['jlramos97@gmail.com', 'joseluis@quitiweb.com'])
    except BadHeaderError:
        return HttpResponse('Invalid header found')


def error_404(request):
    return render(request, '404.html', status=404)


def prueba(request):
    template = loader.get_template('home/prueba.html')

    # generate all other required data that you may need on the #checkout page and add them to context.

    if settings.BRAINTREE_PRODUCTION:
        braintree_env = braintree.Environment.Production
    else:
        braintree_env = braintree.Environment.Sandbox

    # Configure Braintree
    braintree.Configuration.configure(
        braintree_env,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC_KEY,
        private_key=settings.BRAINTREE_PRIVATE_KEY,
    )

    try:
        braintree_client_token = braintree.ClientToken.generate({"customer_id": request.user.id})
    except:
        braintree_client_token = braintree.ClientToken.generate({})

    context = {'braintree_client_token': braintree_client_token}

    return HttpResponse(template.render(context, request))


def payment(request):
    print('payment')

    nonce_from_the_client = request.POST['paymentMethodNonce']
    customer_kwargs = {
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
    }
    customer_create = braintree.Customer.create(customer_kwargs)
    customer_id = customer_create.customer.id
    result = braintree.Transaction.sale({
        "amount": "10.00",
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })
    print(result)
    return HttpResponse('Ok')

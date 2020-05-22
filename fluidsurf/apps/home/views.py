import django
import os
import re
import json
import zipfile
import urllib
import braintree
import requests
import stripe

from io import BytesIO
from datetime import date
from PIL import Image
from imagekit.registry import register
from imagekit.specs import ImageSpec
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, BadHeaderError
from django.shortcuts import render, redirect
from django.template import loader
from django.utils.translation import ugettext_lazy as _


from fluidsurf.apps.home.filters import ProductoFilter, PhotographerFilter, ZonaFilter
from fluidsurf.apps.home.models import (Producto, Compra, Terms, Privacy, Taxes, FreeSub, SecurePayments, Copyright,
                                        Manual, HowDoesItWork, WatermarkImage, SolicitudStock, Continente, Spot)
from fluidsurf.apps.home.forms import (ChangeUserForm, PhotographerForm, PasswordChangeCustomForm, AddProductForm,
                                       EditProductForm, DenunciaForm, ContactForm, DevolucionForm)

from fluidsurf.apps.users.models import CustomUser
from fluidsurf.apps.dashboard.models import RegistroCompras
from fluidsurf.apps.helpers.helper import registros_vacios_compras

stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    template = loader.get_template('home/index.html')

    API_KEY = getattr(settings, 'BING_MAPS_API_KEY', 0)

    ubicaciones = Continente.objects.filter().all()

    if request.user.is_authenticated:
        prod_list = Producto.objects.filter(user__is_active=True, user__validado=True).all()  # spot=request.user.zona

        if request.user.tipo_de_usuario == "FOTOGRAFO" and not request.user.validado:
            messages.warning(request, _("Your profile ins't active yet. Please, wait until "
                                        "your first product gets validated by an admin to start selling."))
    else:
        prod_list = Producto.objects.filter(user__is_active=True, user__validado=True).all()

    prod_filter = ProductoFilter(request.GET, queryset=prod_list)

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

                    if CustomUser.objects.filter(alias=fotografo.alias).exclude(id=fotografo.id).exists():
                        messages.warning(request, _('A photographer with that alias already exists, please try again.'))
                        return HttpResponseRedirect(request.path_info)
                    else:
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

            stripe_exists = request.user.stripe_id

            context = {
                'form': form,
                'passform': passform,
                'photo_form': photo_form,
                'stripe': stripe_exists
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


    spots = Spot.objects.filter().all()
    filter = ZonaFilter(request.GET, queryset=spots)

    spotOG = []
    for spot in filter.qs:
        data = {}
        data['continente'] = spot.area.pais.continente.nombre
        data['pais'] = spot.area.pais.nombre
        data['area'] = spot.area.nombre
        data['spot'] = spot.nombre
        # data = {'continente': spot.area.pais.continente.nombre, 'pais': spot.area.pais.nombre, 'area': spot.area.nombre,
        #         'spot': spot.nombre}


        json_data = json.dumps(data)
        spotOG.append(json_data)


    stripe_exists = request.user.stripe_id
    form = ''

    current = 0

    if request.user.is_authenticated:
        if request.method == "GET":

            if Producto.objects.all().count() > 0:
                current = Producto.objects.latest('id').id + 1

            form = AddProductForm()
        else:

            if stripe_exists:
                if Producto.objects.all().count() > 0:
                    current = Producto.objects.latest('id').id + 1
                form = AddProductForm(request.POST, request.FILES)

                area = request.POST.get('area')
                spot = request.POST.get('spot')

                if form.is_valid() and spot:
                    producto_instance = form.save(commit=False)
                    producto_instance.user = request.user

                    pspot = Spot.objects.filter(nombre=spot, area__nombre=area).first()

                    print(pspot)

                    producto_instance.spot = pspot

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
                                producto_instance.__setattr__('imagen' + str(counter), afile)
                                counter += 1

                        if total_size < 26214400 and upload:
                            producto_instance.save()
                            messages.success(request, 'Tu producto se ha subido correctamente')

                            # Busca los usuarios en la zona del producto para despues mandarles un mail
                            usuarios = CustomUser.objects.filter(tipo_de_usuario="SURFERO").all()

                            mails = []
                            for usuario in usuarios:
                                if usuario.email:
                                    mails.append(usuario.email)
                            mails.append(settings.SERVER_EMAIL)

                            subject = _("New product in your area")
                            message = producto_instance.user.first_name + " " + producto_instance.user.last_name + str(
                                _(" has uploaded a product nearby you"))
                            message += "\n You can check it here: http://127.0.0.1:8000/producto/" + str(
                                producto_instance.id)  # TODO Añadir link
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
                messages.warning(request, _('There was a problem with your Stripe integration'))
    else:
        return redirect('index')

    context = {
        'form': form,
        'current': current,
        'stripe': stripe_exists,
        'spotOG': spotOG
    }

    return HttpResponse(template.render(context, request))


def producto(request, id='0'):
    template = loader.get_template('home/producto.html')

    producto = Producto.objects.filter(id=id, user__validado=True, user__is_active=True).first()

    prod_list = Producto.objects.filter().all()
    prod_filter = ProductoFilter(request.GET, queryset=prod_list)

    API_KEY = getattr(settings, 'BING_MAPS_API_KEY', None)

    ubicaciones = Continente.objects.filter().all()

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
                    return redirect('perfil', request.user.id)
                elif 'main' in request.POST:
                    value = request.POST['main']
                    img = getattr(producto, 'imagen' + value)

                    w = img
                    setattr(producto, 'imagen' + value, producto.imagen0)
                    producto.imagen0 = w
                    del w

                    producto.save()
                    messages.success(request, _('Main picture changed successfully'))
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
                if 'stock' in request.POST:
                    solicitud_exists = SolicitudStock.objects.filter(user=request.user, product=producto).first()

                    if not solicitud_exists:
                        solicitud = SolicitudStock()
                        solicitud.user = request.user
                        solicitud.product = producto
                        solicitud.save()
                        messages.success(request, _('Request done successfully'))

                        subject = _("Someone asked for stock in your product!")
                        message = _(
                            "Your product has been requested for more stock.")
                        message += "\nProduct: " + str(producto)
                        from_email = settings.SERVER_EMAIL
                        to_mail = producto.user.email

                        try:
                            send_mail(subject, message, from_email, [to_mail, settings.SERVER_EMAIL])
                        except BadHeaderError:
                            return HttpResponse('Invalid header found')
                    else:
                        messages.warning(request, _('You already requested for stock for this product'))
                else:
                    precio = (producto.precio + (producto.precio * 0.21)) * 100  # iva
                    comision = precio * 0.05

                    if comision < 100:
                        comision = 100

                    charge = stripe.Charge.create(
                        amount=int(precio),
                        currency='eur',
                        description='Pago de producto',
                        source=request.POST['stripeToken'],
                        transfer_group='ORDER_2020'
                    )

                    print('Precio: %s \n Comision: %s ' % (precio, comision))

                    vendedor_stripe = producto.user.stripe_id

                    if vendedor_stripe:
                        transfer = stripe.Transfer.create(
                            amount=int(precio - comision),
                            currency='eur',
                            destination=vendedor_stripe,
                            description='Venta FluidSurf',
                            transfer_group='ORDER_2020',
                            source_transaction=charge.id
                        )

                        if charge and transfer:
                            producto.stock = 0
                            producto.save()

                            compra = Compra(
                                comprador=request.user,
                                vendedor=producto.user,
                                producto=producto,
                                fecha=date.today()
                            )
                            compra.save()

                            registros_vacios_compras()

                            registro_exists = RegistroCompras.objects.filter(fecha=date.today()).first()

                            if registro_exists:
                                registro_exists.delete()

                            registro = RegistroCompras()
                            registro.compras = Compra.objects.filter(fecha=date.today()).all().count()
                            registro.fecha = date.today()
                            registro.user = producto.user
                            registro.save()

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

    context = {
        'producto': producto,
        'productform': productform,
        'filter': prod_filter,
        'imagenes': imagenes,
        'ubicaciones': ubicaciones,
        'in_wishlist': not status,
        'key': settings.STRIPE_PUBLISHABLE_KEY,
        'stripe': True,
        'API_KEY': API_KEY,
        'precio': (producto.precio + (producto.precio * 0.21)) * 100
    }

    return HttpResponse(template.render(context, request))


def zona(request, nombre=''):
    template = loader.get_template('home/zona.html')

    ubicaciones = Continente.objects.filter().all()

    zona_spot = Continente.objects.filter(spot=nombre).first()

    if zona_spot is None:
        return redirect('/')

    API_KEY = getattr(settings, 'BING_MAPS_API_KEY', 0)

    prod_list = Producto.objects.filter(spot=zona_spot, user__validado=True, user__is_active=True).all()
    prod_filter = ProductoFilter(request.GET, queryset=prod_list)

    context = {
        'zona': zona_spot,
        'filter': prod_filter,
        'API_KEY': API_KEY,
        'ubicaciones': ubicaciones,
    }

    return HttpResponse(template.render(context, request))


def perfil(request, perfil_id=''):
    template = loader.get_template('home/perfil.html')

    user = CustomUser.objects.filter(id=perfil_id).first()

    prod_list = Producto.objects.filter(user=user, user__validado=True).all()
    prod_filter = ProductoFilter(request.GET, queryset=prod_list)

    ubicaciones = Continente.objects.filter().all()

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
                    producto = Producto.objects.filter(id=item).first()
                    if producto:
                        productos.append(producto)
            if request.method == "POST":

                if 'remove' in request.POST:
                    id = request.POST.get('remove')

                    for item in lista:
                        if item == str(id):
                            lista.remove(item)
                            request.user.wishlist = ",".join(lista)
                            request.user.save()
                            messages.success(request, _('Product removed from your wishlist'))
                else:
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


def mis_productos(request):
    template = loader.get_template('home/mis-productos.html')

    productos = Producto.objects.filter(user=request.user)
    prod_filter = ProductoFilter(request.GET, queryset=productos)

    context = {
        'filter': prod_filter
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


# PAGINAS INFORMATIVAS DEL FOOTER

def terms(request):
    template = loader.get_template('home/terms.html')

    context = {
        'terms': Terms.objects.all().first()
    }

    return HttpResponse(template.render(context, request))


def privacy(request):
    template = loader.get_template('home/privacy.html')

    context = {
        'privacy': Privacy.objects.all().first()
    }

    return HttpResponse(template.render(context, request))


def taxes(request):
    template = loader.get_template('home/taxes.html')

    context = {
        'taxes': Taxes.objects.all().first()
    }

    return HttpResponse(template.render(context, request))


def free_sub(request):
    template = loader.get_template('home/sub.html')

    context = {
        'sub': FreeSub.objects.all().first()
    }

    return HttpResponse(template.render(context, request))


def copyright(request):
    template = loader.get_template('home/copyright.html')

    context = {
        'copyright': Copyright.objects.all().first()
    }

    return HttpResponse(template.render(context, request))


def secure_payments(request):
    template = loader.get_template('home/secure-payments.html')

    context = {
        'payments': SecurePayments.objects.all().first()
    }

    return HttpResponse(template.render(context, request))


def manual(request):
    template = loader.get_template('home/manual.html')

    context = {
        'manual': Manual.objects.all().first()
    }

    return HttpResponse(template.render(context, request))


def how_does_it_work(request):
    template = loader.get_template('home/how-does-it-work.html')

    context = {
        'how': HowDoesItWork.objects.all().first()
    }

    return HttpResponse(template.render(context, request))


def devolucion(request):
    template = loader.get_template('home/devolucion.html')

    if request.method == "POST":
        form = DevolucionForm(request.user, request.POST)

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
                devolucion_instance = form.save(commit=False)
                devolucion_instance.user = request.user
                devolucion_instance.is_opened = request.POST.get('is_opened') == 'SI'
                devolucion_instance.save()
                messages.success(request, 'nice')
            else:
                messages.warning(request, _('Invalid reCAPTCHA. Please try again.'))
        else:
            print(form.errors)
    else:
        form = DevolucionForm(user=request.user)

    context = {
        'form': form
    }

    return HttpResponse(template.render(context, request))


def stripe_log(request):
    template = loader.get_template('home/stripe.html')

    payload = {'client_secret': settings.STRIPE_SECRET_KEY, 'code': request.GET['code'],
               'grant_type': 'authorization_code'}

    r = requests.post('https://connect.stripe.com/oauth/token', params=payload)

    response = r.json()
    request.user.stripe_id = response['stripe_user_id']
    request.user.save()

    messages.success(request, 'Cuenta vinculada con exito')

    context = {}
    return HttpResponse(template.render(context, request))


def fotografos(request):
    template = loader.get_template('home/fotografos.html')

    API_KEY = getattr(settings, 'BING_MAPS_API_KEY', 0)

    ubicaciones = Continente.objects.filter().all()

    if request.user.is_authenticated:
        photo_list = CustomUser.objects.filter(is_active=True, validado=True,
                                               tipo_de_usuario="FOTOGRAFO").all()
    else:
        photo_list = CustomUser.objects.filter(is_active=True, validado=True, tipo_de_usuario="FOTOGRAFO").all()

    photo_filter = PhotographerFilter(request.GET, queryset=photo_list)

    context = {
        'filter': photo_filter,
        'API_KEY': API_KEY,
        'ubicaciones': ubicaciones,
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
    print(django.db.connection.introspection.table_names())

    if 'home_watermarkimage' in django.db.connection.introspection.table_names():
        image = WatermarkImage.objects.filter(activo=True).first()

        if image:
            watermark = Image.open(image.imagen.url[1:])
        else:
            watermark = Image.open(settings.WATERMARK_IMAGE)
    else:
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

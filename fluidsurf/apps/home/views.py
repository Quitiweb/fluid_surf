from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from django.db.models import Q

from fluidsurf.apps.users.models import CustomUser, MiPerfil
from .forms import ContactForm, ChangeUserForm, PhotographerForm
from ..helpers.helper import enviar_email, grouped, news_to_get, users_to_get


def index(request):
    if request.user.is_authenticated:
        template = loader.get_template('home/index.html')

        # noticias = Post.objects.filter(
        #     fecha_de_publicacion__lte=timezone.now()
        # ).order_by('-fecha_de_publicacion')[:news_to_get(Post.objects.count())]
        #
        # noticias_gr = grouped(noticias, 3)

        usuarios = CustomUser.objects.exclude(
            username=request.user.username
        )[:users_to_get(CustomUser.objects.count() - 1)]

        usuarios_conectados = CustomUser.objects.exclude(
            username=request.user.username
        ).filter(Q(is_marca=True) | Q(is_espacio=True), Q(validado=True))[:users_to_get(CustomUser.objects.count() - 1)]

        context = {
            # 'noticias': noticias,
            # 'noticias_gr': noticias_gr,
            'usuarios': usuarios,
            'usuarios_conectados': usuarios_conectados,
        }

    else:
        template = loader.get_template('home/index.html')

        if request.method == 'GET':
            form = ContactForm()
        else:
            form = ContactForm(request.POST)
            if form.is_valid():
                subject = 'Kradleco formulario de contacto'
                from_email = form.cleaned_data['from_email']
                message = 'Email recibido de: ' + from_email + '\n\n' + form.cleaned_data['message']

                enviar_email(subject, message)

                form = ContactForm()
                return redirect('mensaje-enviado')
            else:
                print('Error en el formulario')

        # post_list = Post.objects.filter(
        #     fecha_de_publicacion__lte=timezone.now()
        # ).order_by('-fecha_de_publicacion')[:6]

        context = {
            'form': form,
            # 'post_list': post_list,
        }

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
            form = ChangeUserForm(instance=request.user)
            if request.user.tipo_de_usuario == "FOTOGRAFO":
                photo_form = PhotographerForm(instance=request.user)
        else:
            form = ChangeUserForm(request.POST, instance=request.user)
            if request.user.tipo_de_usuario == "FOTOGRAFO":
                photo_form = PhotographerForm(request.POST,  request.FILES, instance=request.user)
                if photo_form.is_valid():
                    photo_form.save()
            if form.is_valid():
                messages.add_message(request, messages.SUCCESS, 'Tu perfil se ha guardado correctamente')
                form.save()

        if request.user.tipo_de_usuario == "FOTOGRAFO":
            context = {
                'form': form,
                'photo_form': photo_form
            }
        else:
            context = {
                'form': form
            }
        return HttpResponse(template.render(context, request))
    else: return redirect("/login")

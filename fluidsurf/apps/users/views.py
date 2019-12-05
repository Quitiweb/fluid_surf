from datetime import date

from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .forms import CustomUserCreationForm
from .models import CustomUser
from ..dashboard.models import RegistroFotografos, RegistroSurferos


def sign_up(request):
    template = loader.get_template('registration/signup.html')

    if request.method == 'GET':
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.date_joined = date.today()
            user.save()
            messages.info(request, "Gracias por registrarte. Te llegará un email de confirmación a tu cuenta de correo.")
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            login(request, new_user)

            registro_photo_exists = RegistroFotografos.objects.filter(fecha=date.today()).first()

            if registro_photo_exists:
                registro_photo_exists.delete()

            registro_photo = RegistroFotografos()
            registro_photo.users = CustomUser.objects.filter(tipo_de_usuario="FOTOGRAFO", date_joined=date.today()).all().count()
            registro_photo.fecha = date.today()
            registro_photo.save()

            registro_surf_exists = RegistroSurferos.objects.filter(fecha=date.today()).first()

            if registro_surf_exists:
                registro_surf_exists.delete()

            registro_surf = RegistroSurferos()
            registro_surf.users = CustomUser.objects.filter(tipo_de_usuario="SURFERO", date_joined=date.today()).all().count()
            print(registro_surf_exists)
            registro_surf.fecha = date.today()
            registro_surf.save()

            return redirect('mi-cuenta')
    context = {
        'form': form,
    }

    return HttpResponse(template.render(context, request))

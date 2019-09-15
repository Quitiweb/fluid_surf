from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .forms import CustomUserCreationForm


def sign_up(request):
    template = loader.get_template('landing/signup.html')

    if request.method == 'GET':
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Gracias por registrarte. Te llegará un email de confirmación a tu cuenta de correo.")
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            login(request, new_user)
            return redirect('mi-cuenta',tab=1)

    context = {
        'form': form,
    }

    return HttpResponse(template.render(context, request))

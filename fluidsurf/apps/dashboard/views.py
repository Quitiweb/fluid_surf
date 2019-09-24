from django.shortcuts import render, redirect


# Create your views here.
def dashboard(request):

    # Si el usuario no tiene permisos de administracion, se le impedira acceder al dashboard.
    if not request.user.is_staff:
        return redirect('/')

    return render(request, 'dashboard/main.html')
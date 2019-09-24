from django.shortcuts import render


# Create your views here.
def dashboard(request):

    if request.user.is_staff:
        print('eres staff')
    else:
        print('no eres staff')

    if request.user.is_superuser:
        print('eres admin')
    else:
        print('no eres admin')

    return render(request, 'dashboard/main.html')
from itertools import count

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q

# Create your views here.
from django.template import loader
from openpyxl import Workbook

from fluidsurf.apps.home.models import Producto, Compra
from fluidsurf.apps.users.models import CustomUser


def dashboard(request):
    template = loader.get_template('dashboard/main.html')

    # Si el usuario no tiene permisos de administracion, se le impedira acceder al dashboard.
    if not request.user.is_staff:
        return redirect('/')

    productos = Producto.objects.filter().all()
    europa = Producto.objects.filter(spot='Europa').all()
    oceania = Producto.objects.filter(spot='Oceania').all()
    africa = Producto.objects.filter(spot='Africa').all()
    asia = Producto.objects.filter(spot='Asia').all()
    america = Producto.objects.filter(Q(spot='America del Norte') | Q(spot='America del Sur')).all()
    compras = Compra.objects.filter().all()

    fotografos = CustomUser.objects.filter(tipo_de_usuario='FOTOGRAFO').all()
    surferos = CustomUser.objects.filter(tipo_de_usuario='SURFERO').all()

    context = {
        'productos': productos,
        'europa': europa,
        'oceania': oceania,
        'africa': africa,
        'asia': asia,
        'america': america,
        'compras': compras,
        'fotografos': fotografos,
        'surferos': surferos
    }

    return HttpResponse(template.render(context, request))


def productos(request):
    template = loader.get_template('dashboard/productos.html')

    productos = Producto.objects.filter().all()

    if request.method == "POST":
        workbook = Workbook()
        sheet = workbook.active

        sheet.append(["ID", "Name"])

        for product in productos:
            data = [product.id, product.nombre]
            sheet.append(data)

        workbook.save(filename="spreadsheets/oop_sample.xlsx")

    context = {
        'productos': productos
    }

    return HttpResponse(template.render(context, request))


def compras(request):
    template = loader.get_template('dashboard/compras.html')

    compras = Compra.objects.filter().all()

    context = {
        'compras': compras
    }

    return HttpResponse(template.render(context, request))


def usuarios(request):
    template = loader.get_template('dashboard/usuarios.html')

    usuarios = CustomUser.objects.filter().all()

    context = {
        'usuarios': usuarios
    }

    return HttpResponse(template.render(context, request))


def perfil(request, id=''):
    template = loader.get_template('dashboard/perfil.html')

    usuario = CustomUser.objects.filter(id=id).first()
    wishlist = len(usuario.wishlist.split(',')) -1

    productos = Producto.objects.filter(user=usuario).all()
    compras = Compra.objects.filter(comprador=usuario).all()
    ventas = Compra.objects.filter(vendedor=usuario).all()

    context = {
        'usuario': usuario,
        'wishlist': wishlist,
        'productos': productos,
        'compras': compras,
        'ventas': ventas
    }

    return HttpResponse(template.render(context, request))
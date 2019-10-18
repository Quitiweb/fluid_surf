from datetime import date
from itertools import count

import openpyxl
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q, ImageField

from django.utils.translation import ugettext_lazy as _

from django.template import loader
from openpyxl import Workbook

from fluidsurf.apps.home.models import Producto, Compra, Denuncia
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
        if 'import' in request.POST:
            excel_file = request.FILES["fileInput"]
            wb = openpyxl.load_workbook(excel_file)

            worksheet = wb['Sheet']

            # Estas dos lineas son para ignorar la primera fila del excel, ya que contiene los
            # nombres de las columnas
            elements = worksheet.iter_rows()
            next(elements)

            for row in elements:
                producto = Producto()
                producto.id = str(row[0].value)
                producto.nombre = str(row[1].value)
                producto.precio = str(row[2].value)
                producto.fecha = str(row[3].value.strftime("%Y-%m-%d"))
                producto.spot = str(row[4].value)
                producto.stock = str(row[5].value)

                producto.imagen0 = str(row[7].value)[7:]
                producto.imagen1 = str(row[8].value)[7:]
                producto.imagen2 = str(row[9].value)[7:]
                producto.imagen3 = str(row[10].value)[7:]
                producto.imagen4 = str(row[11].value)[7:]
                producto.imagen5 = str(row[12].value)[7:]
                producto.imagen6 = str(row[13].value)[7:]
                producto.imagen7 = str(row[14].value)[7:]
                producto.imagen8 = str(row[15].value)[7:]
                producto.imagen9 = str(row[16].value)[7:]

                usuario = CustomUser.objects.filter(username=row[6].value).first()
                producto.user = usuario

                producto.save()
            messages.success(request, 'Productos importados correctamente!')
        else:
            workbook = Workbook()
            sheet = workbook.active

            sheet.append(["ID", "Nombre", "Precio", "Fecha", "Spot", "Stock", "Usuario", 'imagen0', 'imagen1', 'imagen2'
                          , 'imagen3', 'imagen4', 'imagen5', 'imagen6', 'imagen7', 'imagen8', 'imagen9'])

            for p in productos:
                data = [p.id, p.nombre, p.precio, p.fecha, p.spot, p.stock, p.user.username]
                for i in range(10):
                    if getattr(p, 'imagen' + str(i)):
                        data.append(getattr(p, 'imagen' + str(i)).url)
                    else:
                        break
                sheet.append(data)

            workbook.save(filename="spreadsheets/productos" + str(date.today()) + ".xlsx")
            messages.success(request, 'Productos exportados correctamente!')

    context = {
        'productos': productos
    }

    return HttpResponse(template.render(context, request))


def compras(request):
    template = loader.get_template('dashboard/compras.html')

    compras = Compra.objects.filter().all()

    if request.method == "POST":
        if 'import' in request.POST:
            excel_file = request.FILES["fileInput"]
            wb = openpyxl.load_workbook(excel_file)

            worksheet = wb['Sheet']

            # Estas dos lineas son para ignorar la primera fila del excel, ya que contiene los
            # nombres de las columnas
            elements = worksheet.iter_rows()
            next(elements)

            for row in elements:
                compra = Compra()
                compra.id = str(row[0].value)

                comprador = CustomUser.objects.filter(username=row[1].value).first()
                compra.comprador = comprador

                vendedor = CustomUser.objects.filter(username=row[2].value).first()
                compra.vendedor = vendedor

                producto = Producto.objects.filter(id=row[3].value).first()
                compra.producto = producto

                compra.fecha = str(row[4].value.strftime("%Y-%m-%d"))

                compra.save()
            messages.success(request, 'Compras importadas correctamente!')
        else:
            workbook = Workbook()
            sheet = workbook.active

            sheet.append(["ID", "Comprador", "Vendedor", "Producto", "Fecha"])

            for c in compras:
                data = [c.id, c.comprador.username, c.vendedor.username, c.producto.id, c.fecha]
                sheet.append(data)

            workbook.save(filename="spreadsheets/compras" + str(date.today()) + ".xlsx")
            messages.success(request, 'Compras exportadas correctamente!')


    context = {
        'compras': compras
    }

    return HttpResponse(template.render(context, request))


def usuarios(request):
    template = loader.get_template('dashboard/usuarios.html')

    usuarios = CustomUser.objects.filter().all()

    if request.method == "POST":
        if 'import' in request.POST:
            excel_file = request.FILES["fileInput"]
            wb = openpyxl.load_workbook(excel_file)

            worksheet = wb['Sheet']

            # Estas dos lineas son para ignorar la primera fila del excel, ya que contiene los
            # nombres de las columnas
            elements = worksheet.iter_rows()
            next(elements)

            for row in elements:
                usuario = CustomUser()
                usuario.id = str(row[0].value)
                usuario.username = str(row[1].value)
                usuario.password = str(row[2].value)

                if row[3].value is not None:
                    usuario.first_name = str(row[3].value)
                else:
                    usuario.first_name = ""
                if row[4].value is not None:
                    usuario.last_name = str(row[4].value)
                else:
                    usuario.last_name = ""
                if row[5].value is not None:
                    usuario.email = str(row[5].value)
                else:
                    usuario.email = ""

                usuario.is_active = str(row[6].value)
                usuario.is_staff = str(row[7].value)
                usuario.is_superuser = str(row[8].value)
                usuario.tipo_de_usuario = str(row[9].value)

                usuario.profile_pic = str(row[10].value)[7:]

                usuario.main_pic = str(row[11].value)[7:]

                if row[12].value is not None:
                    usuario.zona = str(row[12].value)
                else:
                    usuario.zona = ""

                if row[13].value is not None:
                    usuario.pais = str(row[13].value)
                else:
                    usuario.pais = ""

                usuario.save()
            messages.success(request, 'Usuarios importados correctamente!')

        else:
            workbook = Workbook()
            sheet = workbook.active

            sheet.append(["ID", "Username", "Contraseña", "Nombre", "Apellidos", "Email", "Activo", "Staff", 'Admin',
                          'Tipo De Usuario', 'Foto de perfil', 'Foto destacada', 'Zona', 'Pais'])

            for u in usuarios:
                if u.first_name is not None:
                    nombre = u.first_name
                else:
                    nombre = ""
                if u.last_name is not None:
                    apellidos = u.last_name
                else:
                    apellidos = ""
                if u.email is not None:
                    email = u.email
                else:
                    email = ""
                if u.zona is not None:
                    zona = u.zona
                else:
                    zona = ""
                if u.pais is not None:
                    pais = u.pais
                else:
                    pais = ""
                if u.profile_pic:
                    ppic = u.profile_pic.url
                else:
                    ppic = ""
                if u.main_pic:
                    mpic = u.main_pic.url
                else:
                    mpic = ""

                data = [u.id, u.username, u.password, nombre, apellidos, email, u.is_active, u.is_staff, u.is_superuser,
                        u.tipo_de_usuario, ppic, mpic, zona, pais]
                sheet.append(data)

            workbook.save(filename="spreadsheets/usuarios" + str(date.today()) + ".xlsx")
            messages.success(request, 'Usuarios exportados correctamente!')

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
    denuncias = Denuncia.objects.filter(receptor=usuario).all()

    if request.method == "POST":
        # Togglea si el usuario esta activo o no
        usuario.is_active = not usuario.is_active

        usuario.save()

    context = {
        'usuario': usuario,
        'wishlist': wishlist,
        'productos': productos,
        'compras': compras,
        'ventas': ventas,
        'denuncias': denuncias
    }

    return HttpResponse(template.render(context, request))


def denuncias(request):
    template = loader.get_template('dashboard/denuncias.html')

    denuncias = Denuncia.objects.filter().all()

    if request.method == "POST":
        denuncia = Denuncia.objects.filter(id=request.POST.get('borrar')).first()
        denuncia.delete()


    context = {
        'denuncias': denuncias
    }

    return HttpResponse(template.render(context, request))\

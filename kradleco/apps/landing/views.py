import csv
import json

import datetime

import io
import stripe
import openpyxl
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.template.defaultfilters import upper, slugify
from django.utils.crypto import get_random_string

from kradleco.settings import dev
from .forms import NewItemForm, AlquilerForm, MarcaForm, EspacioForm, \
    SeleccionarCategoriasForm, VarianteForm, PropuestaComercialForm, EditarEspacioForm, MaestroForm, ColeccionForm
from ..users.forms import CustomUserChangeForm, EmpresaForm, PublicUserForm, AutonomoForm, \
    MiPerfilSimpleUserForm, MiPerfilForm, RazonSocialForm, CustomUserMarcaEspacio

from .models import Articulo, Alquiler, Coleccion, Espacio, Marca, PropuestaComercial, \
    GaleriaArticulo, Maestro, VarianteArticulo, Categoria, Promocion, Conexion, DefinicionVariante, CODE_LENGHT, \
    Carrito, PuntoDeVenta, CarritoItem, Pedido, ArticuloPDV, Notificacion

from ..users.models import CustomUser, Empresa, Autonomo, GaleriaUsuario, MiPerfil

from .filters import PropuestaFilter
from ..helpers.helper import users_to_get, tab_selected


# funcion para comprobar varios formularios a la vez,
# devuelve ok si todos estan bien y la lista de errores si hay errores
def check_forms(*args):
    form_errors = []
    is_ok = True
    for form in args:
        if form.is_valid():
            pass
        else:
            form_errors.append(form.errors)
            is_ok = False
    return is_ok, form_errors


def mi_cuenta_redirect(request):
    return redirect('mi-cuenta', tab=1)


# Devuelve los espacios/marcas relacionados con el usuario
def get_relaciones(user):
    result = []
    propuestas = user.emisor.all()
    for prop in propuestas:
        result.append(prop.receptor)
    propuestas = user.receptor.all()
    for prop in propuestas:
        result.append(prop.emisor)
    return result


def mi_cuenta(request, tab=1):
    template = loader.get_template('landing/mi-cuenta.html')
    context = {}

    view_from = False
    current_promo = None
    auto_generated = upper(get_random_string(CODE_LENGHT))  # Crea un codigo aletarorio para la promocion

    # Esto lo utilizamos para diferenciar entre tab1 y tab2
    tabs = tab_selected(tab)
    if request.user.is_authenticated:
        # Si no se ha creado un perfil publico se crea aqui
        if MiPerfil.objects.filter(user=request.user).count() == 0:
            print('Creamos dummy para la clase MiPerfil')
            perfil = MiPerfil(user=request.user)
            perfil.save()

        query_perfil = Q(user=request.user)
        perfil = MiPerfil.objects.filter(query_perfil).first()

        if request.user.is_authenticated:

            categorias = Categoria.objects.filter(user=request.user).exclude(categoria_padre__isnull=False)
            if 'current_promo' in request.session and request.session[
                'from'] != 'edit-promo':  # si actualmente estoy creando una promocion y tengo datos metidos los cargo en el template
                current_promo = Promocion.objects.filter(id=request.session['current_promo']).first()
            else:
                if 'current_promo' in request.session:
                    del request.session['current_promo']

            user = get_object_or_404(CustomUser, pk=request.user.id)

            if Empresa.objects.filter(user=request.user):
                empresa_user = Empresa.objects.get(user=request.user)
            else:
                empresa_user = False

            if Autonomo.objects.filter(user=request.user):
                autonomo_user = Autonomo.objects.get(user=request.user)
            else:
                autonomo_user = False

            # Si es la primera vez que accedemos creamos un dummy para cada clase
            if Marca.objects.filter(user=request.user).count() == 0:
                print('Creamos dummy para la clase marca')
                marca_form = MarcaForm()
                marca = marca_form.save(commit=False)
                marca.user = request.user
                marca.save()

            marca = get_object_or_404(Marca, user=request.user)

            if Espacio.objects.filter(user=request.user).count() == 0:
                print('Creamos dummy para la clase espacio')
                espacio_form = EspacioForm()
                espacio = espacio_form.save(commit=False)
                espacio.user = request.user
                espacio.save()

            espacio = get_object_or_404(Espacio, user=request.user)

            if len(Maestro.objects.filter(user=request.user)) == 0:
                print('Creamos dummy para la clase maestro')
                maestro_form = MaestroForm()
                maestro = maestro_form.save(commit=False)
                maestro.user = request.user
                maestro.save()

            maestro = get_object_or_404(Maestro, user=request.user)

            if request.session.get('from') == 'add-promo':
                view_from = 'show_promo'
            elif request.session.get('from') == 'add-item':
                view_from = 'show_items'
            elif request.session.get('from') == 'colecciones':
                view_from = 'show_col'

            form = CustomUserChangeForm(instance=user)

            form_negocio = CustomUserMarcaEspacio(instance=user)
            marca_form = MarcaForm(instance=marca)
            espacio_form = EspacioForm(instance=espacio)
            maestro_form = MaestroForm(instance=maestro)

            if empresa_user:
                form_empresa = EmpresaForm(instance=empresa_user)
            else:
                form_empresa = EmpresaForm()

            if autonomo_user:
                form_autonomo = AutonomoForm(instance=autonomo_user)
            else:
                form_autonomo = AutonomoForm()

            if request.method == 'POST':

                if 'Empresa-Autonomo' in request.POST:
                    form = CustomUserChangeForm(request.POST, instance=user)

                    if empresa_user:
                        form_empresa = EmpresaForm(request.POST, instance=empresa_user)
                    else:
                        form_empresa = EmpresaForm(request.POST)

                    if autonomo_user:
                        form_autonomo = AutonomoForm(request.POST, instance=autonomo_user)
                    else:
                        form_autonomo = AutonomoForm(request.POST)

                    status = False

                    if form.is_valid():
                        print("es valido")
                        user_form = form.save(commit=False)
                        form.save()

                        if user_form.is_empresa and form_empresa.is_valid():
                            empresa = form_empresa.save(commit=False)
                            empresa.user = request.user
                            empresa.save()

                            status = True

                        elif user_form.is_empresa and not form_empresa.is_valid():
                            messages.warning(request, form_empresa.errors)

                        if user_form.is_autonomo and form_autonomo.is_valid():
                            autonomo = form_autonomo.save(commit=False)
                            autonomo.user = request.user
                            autonomo.save()

                            status = True

                        elif user_form.is_autonomo and not form_autonomo.is_valid():
                            messages.warning(request, form_autonomo.errors)

                        if not user_form.is_empresa and not user_form.is_autonomo:
                            status = True

                        if status:
                            print('La información se ha guardado correctamente.')
                            messages.success(request, 'La información se ha guardado correctamente')
                        else:
                            print('Algo ha salido mal.')
                            messages.warning(request, 'La información no se ha podido guardar.'
                                                      ' Por favor, revisa la información.')
                    else:
                        print('Error en el formulario')
                        messages.warning(request, form.errors)

                elif 'guarda_espacio' in request.POST:

                    form_negocio = CustomUserMarcaEspacio(request.POST, instance=user)
                    espacio_form = EspacioForm(request.POST, instance=espacio)
                    maestro_form = MaestroForm(request.POST, instance=maestro)

                    if form_negocio.is_valid():
                        form_negocio.save()

                    if espacio_form.is_valid():
                        espacio = espacio_form.save(commit=False)
                        espacio.user = user
                        espacio.save()
                        messages.success(request, "La información se ha guardado correctamente")
                    else:
                        messages.warning(request, espacio_form.errors)

                    if maestro_form.is_valid():
                        maestro_form.save()

                    perfil.is_espacio = True
                    perfil.is_marca = False
                    perfil.save()

                elif 'guarda_marca' in request.POST:
                    form_negocio = CustomUserMarcaEspacio(request.POST, instance=user)
                    marca_form = MarcaForm(request.POST, instance=marca)
                    maestro_form = MaestroForm(request.POST, instance=maestro)

                    if form_negocio.is_valid():
                        form_negocio.save()

                    if marca_form.is_valid():
                        marca_form.save()
                        messages.success(request, "La información se ha guardado correctamente")
                    else:
                        messages.warning(request, marca_form.errors)

                    if maestro_form.is_valid():
                        maestro_form.save()

                    perfil.is_marca = True
                    perfil.is_espacio = False
                    perfil.save()

            context = {
                'form': form,
                'form_autonomo': form_autonomo,
                'form_empresa': form_empresa,
                'form_negocio': form_negocio,
                'maestro_form': maestro_form,
                'marca_form': marca_form,
                'perfil': perfil,
                'espacio_form': espacio_form,
                'view_from': view_from,
                'current_promo': current_promo,
                'categorias': categorias,
                'auto_generated_code': auto_generated,
                'tabs': tabs,
            }

    return HttpResponse(template.render(context, request))


def mi_espacio(request):
    template = loader.get_template('landing/empresa/inc/mi-espacio.html')
    espacio = get_object_or_404(Espacio, user=request.user)

    if request.method == 'GET':
        form = EditarEspacioForm(instance=espacio)
    else:
        form = EditarEspacioForm(request.POST, instance=espacio)

        if form.is_valid():
            form.save()
            messages.success(request, "La información se ha guardado correctamente")
        else:
            messages.error(request, "No se ha podido guardar la información")

    context = {
        'form': form,
        # 'categorias': categorias,
    }

    return HttpResponse(template.render(context, request))


def mi_catalogo(request):
    template = loader.get_template('landing/empresa/inc/mi-catalogo.html')

    view_from = False  # catalogo
    current_promo = None  # catalogo
    auto_generated = upper(get_random_string(CODE_LENGHT))  # catalogo  # Crea un codigo aletarorio
    context = {}
    if request.user.is_authenticated:

        categorias = Categoria.objects.filter(user=request.user).exclude(categoria_padre__isnull=False)  # catalogo
        if 'current_promo' in request.session and request.session[  # catalogo
            'from'] != 'edit-promo':  # si actualmente estoy creando una promocion y tengo datos metidos los cargo en el template #catalogo
            current_promo = Promocion.objects.filter(id=request.session['current_promo']).first()  # catalogo
        else:
            if 'current_promo' in request.session:  # catalogo
                del request.session['current_promo']  # catalogo

        items = Articulo.objects.filter(
            user=request.user
        ).order_by('nombre')[:5]

        user = get_object_or_404(CustomUser, pk=request.user.id)

        if len(Maestro.objects.filter(user=request.user)) == 0:  # catalogo
            print('Creamos dummy para la clase maestro')  # catalogo
            maestro_form = MaestroForm()  # catalogo
            maestro = maestro_form.save(commit=False)  # catalogo
            maestro.user = request.user  # catalogo
            maestro.save()  # catalogo

        maestro = get_object_or_404(Maestro, user=request.user)  # catalogo

        if request.session.get('from') == 'add-promo':  # catalogo
            view_from = 'show_promo'  # catalogo
        elif request.session.get('from') == 'add-item':  # catalogo
            view_from = 'show_items'  # catalogo
        elif request.session.get('from') == 'colecciones':  # catalogo
            view_from = 'show_col'  # catalog

        if request.method == 'GET':
            maestro_form = MaestroForm(instance=maestro)  # catalogo
        else:
            maestro_form = MaestroForm(request.POST, instance=maestro)  # catalogo

        if maestro_form.is_valid():  # catalogo
            maestro_form.save()  # catalogo

        context = {
            'maestro_form': maestro_form,
            'view_from': view_from,
            'current_promo': current_promo,
            'categorias': categorias,
            'auto_generated_code': auto_generated
        }

    return HttpResponse(template.render(context, request))


def mi_perfil(request):
    template = loader.get_template('landing/mi-perfil.html')

    context = {}

    if request.user.is_authenticated:

        user = get_object_or_404(CustomUser, pk=request.user.id)
        galeria = GaleriaUsuario.objects.filter(user=request.user)

        if request.method == 'GET':
            form = MiPerfilSimpleUserForm(instance=user)

        else:
            form = MiPerfilSimpleUserForm(request.POST, request.FILES, instance=user)

            if form.is_valid():
                form.save()
                files = request.FILES.getlist('perfil-images')

                if len(files) > 0:
                    for afile in files:
                        pic = GaleriaUsuario()
                        pic.user = request.user
                        pic.imagen = afile
                        pic.save()

                print('La información se ha guardado correctamente')
                messages.success(request, 'La información se ha guardado correctamente')
                form = MiPerfilSimpleUserForm(instance=user)
            else:
                print('Error en el formulario')
                messages.warning(request, form.errors)

        context = {
            'form': form,
            'galeria': galeria
        }

    return HttpResponse(template.render(context, request))


def premium(request):
    return render(request, 'landing/premium.html')


def search_item(request):
    # todo hacer que esta busqueda se realice cuando se pulse cualuier tecla, sin tener que pulsar el intro, tmb en otros buscadores

    if request.method == 'GET':
        query = request.GET.get('q')

        if query is not None:
            if query == '':
                results = Articulo.objects.all()
            else:
                results = Articulo.objects.filter(nombre__icontains=query).distinct()

            msg_list = list(results.values())
            return JsonResponse(msg_list, safe=False)


def search_item_promo(request):
    template = loader.get_template('landing/empresa/catalogo/promociones/search-view.html')
    context = {}
    tipo = ''
    articulos = Articulo.objects.filter(user=request.user).order_by('nombre')
    maestro = Maestro.objects.filter(user=request.user)
    empresa = Empresa.objects.filter(user=request.user).first()
    colecciones = Coleccion.objects.filter(empresa=empresa)
    categorias = Categoria.objects.filter(user=request.user).exclude(categoria_padre__isnull=False)

    if request.method == 'GET':
        pass
    else:
        if request.POST.get('selected-promo-items'):
            if 'current_promo' in request.session:
                current_promo = Promocion.objects.filter(id=request.session['current_promo']).first()
                ids = request.POST.get('selected-promo-items')
                my_list = ids.split(",")
                articulos_seleccionados = Articulo.objects.filter(id__in=my_list);
                if request.POST.get('where-save') == '0':
                    current_promo.articulos_compra.set(articulos_seleccionados)
                elif request.POST.get('where-save') == '1':
                    current_promo.articulos_compra.set(articulos_seleccionados)
                elif request.POST.get('where-save') == '2':
                    current_promo.articulos_obtiene.set(articulos_seleccionados)

                current_promo.save()
                if request.session['from'] != "edit-promo":
                    request.session['from'] = 'add-promo'
                    return redirect('mi-catalogo')
                else:
                    return redirect('promo-detail', promo_id=current_promo.id)

    if request.POST.get('items_r_obtiene'):
        tipo = '0'
    elif request.POST.get('items_p_requiere'):
        tipo = '1'
    elif request.POST.get('items_p_obtiene'):
        tipo = '2'

    context = {
        'articulos': articulos,
        'maestro': maestro,
        'categorias': categorias,
        'colecciones': colecciones,
        'tipo': tipo
    }
    return HttpResponse(template.render(context, request))


def query_item_promo(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        mercado = request.GET.getlist('m[]')
        target = request.GET.getlist('t[]')
        categorias = request.GET.getlist('c[]')
        subcategorias = request.GET.getlist('sc[]')
        colecciones = request.GET.getlist('s[]')
        filters = Q()
        if colecciones != []:
            filters &= Q(
                articulos__in=colecciones,
            )
        if categorias != []:
            filters &= Q(
                categoria__in=categorias
            )
        if subcategorias != []:
            filters &= Q(
                subcategoria__in=subcategorias
            )
        if mercado != []:
            filters &= Q(
                mercado__in=mercado,
            )
        if target != []:
            filters &= Q(
                target__in=target,
            )

        if query == '':
            filters &= Q(
                user=request.user,
            )
        else:
            filters &= Q(
                user=request.user,
                nombre__icontains=query,
            )

        results = Articulo.objects.filter(filters).distinct().annotate(in_promo=F('promocionados'))

        msg_list = list(results.values())
        return JsonResponse(msg_list, safe=False)


def promo_detail(request, promo_id):
    if 'current_promo' in request.session:
        del request.session['current_promo']
    template = loader.get_template('landing/empresa/catalogo/promociones/promo-detail.html')
    context = {}

    if request.user.is_authenticated:
        promocion = Promocion.objects.filter(id=promo_id).first()
        if promocion.user == request.user:
            request.session['current_promo'] = promocion.id
            if request.method == 'GET':
                context = {
                    'promocion': promocion,
                }
            request.session['from'] = "edit-promo"
        else:
            messages.warning(request, "No tienes permisos para acceder a esta información")

    return HttpResponse(template.render(context, request))


def proximos_descuentos(request):
    if 'current_promo' in request.session:
        del request.session['current_promo']
    template = loader.get_template('landing/empresa/catalogo/promociones/proximos-descuentos.html')
    context = {}

    if request.user.is_authenticated:
        if request.path.__contains__('descuentos-anteriores'):
            promociones = Promocion.objects.filter(fecha_desde__lt=datetime.datetime.now())

        elif request.path.__contains__('proximos-descuentos'):
            promociones = Promocion.objects.filter(
                fecha_hasta__gt=datetime.datetime.now()).order_by('-fecha_desde', 'visible') | Promocion.objects.filter(
                fecha_hasta=None).order_by('-fecha_desde', 'visible')
        context = {
            'promociones': promociones,
        }

    request.session['from'] = 'add-promo'
    return HttpResponse(template.render(context, request))


# comprueba si es rebaja o personalizada, a partir de ahí comprueba si los campos necesarios para cada tipo
# están vacíos o rellenos
def guardar_promo(request):
    print(request.POST)
    return_to_edit = False

    if request.user.is_authenticated:
        if request.method == 'GET':
            pass
        else:
            # Si acabamos de empezar a creara una promo creamos una instancia del modelo, sino cogemos el ya existente
            if 'current_promo' in request.session:
                current_promo = Promocion.objects.filter(id=request.session['current_promo']).first()
                if current_promo:
                    current_promo.set_data(request.POST)
                else:
                    current_promo = Promocion()
                    current_promo.user = request.user
                    current_promo.set_data(request.POST)
                    request.session['current_promo'] = current_promo.id

                current_promo.save()
            else:
                current_promo = Promocion()
                current_promo.user = request.user
                current_promo.set_data(request.POST)
                current_promo.save()
                request.session['current_promo'] = current_promo.id

            if request.POST.get('items_r_obtiene') or request.POST.get('items_p_requiere') or request.POST.get(
                    'items_p_obtiene'):
                if 'true' in (request.POST.get('items_r_obtiene'), request.POST.get('items_p_requiere'),
                              request.POST.get('items_p_obtiene')):
                    return list_promo_items(request)
                else:
                    return search_item_promo(request)

            elif request.POST.get('save') or request.POST.get('save_edit'):
                if request.POST.get('tipo-promo') != '':
                    if '' != request.POST.get('fecha_desde'):
                        if '' != request.POST.get('limite'):
                            if request.POST.get('limite') == 'cli' and request.POST.get('promo-clientes') == '':
                                messages.warning(request,
                                                 "Si selecciona, límite por clientes, debe indicar un número")
                            else:
                                if request.POST.get('tipo-promo') == 'personalizada':
                                    current_promo.save()
                                    messages.success(request, 'La promoción se ha guardado correctamente')
                                    del request.session['current_promo']
                                else:
                                    if request.POST.get('obtiene_rebaja_value') != '':
                                        current_promo.save()
                                        messages.success(request, 'La promoción se ha guardado correctamente')
                                        del request.session['current_promo']
                                    else:
                                        messages.warning(request,
                                                         "Si seleccionas rebaja, debes rellenar el descuento que obtiene el cliente")
                        else:
                            messages.warning(request,
                                             "Debe elegir un límite (nº clientes limite o hasta fin de existencias")
                    else:
                        messages.warning(request, "La promoción debe tener al menos una fecha de inicio")

                else:
                    messages.warning(request, "No ha seleccionado un tipo de promocion (rebaja/personalizada")

    if request.session['from'] == 'edit-promo':
        return_to_edit = True
    else:
        request.session['from'] = 'add-promo'

    if return_to_edit:
        return redirect('promo-detail', promo_id=current_promo.id)
    else:
        if request.POST.get('save'):
            return redirect('mi-catalogo')
        else:
            return redirect('promo-detail', promo_id=current_promo.id)


# muestra datos de la promo sin opcion de editar
def list_promo_items(request):
    if 'current_promo' in request.session:
        template = loader.get_template('landing/empresa/catalogo/promociones/promo-list.html')
        context = {}
        current_promo = Promocion.objects.filter(id=request.session['current_promo']).first()
        if request.POST.get('items_p_obtiene'):
            articulos = current_promo.articulos_obtiene.all()
        else:
            articulos = current_promo.articulos_compra.all()

        context = {
            'promo': current_promo,
            'articulos': articulos
        }

        return HttpResponse(template.render(context, request))

    else:
        messages.warning(request, "Ha ocurrido un error al recuperar la información")
        return redirect('edit-item')


def marca_espacio(request):
    template = loader.get_template('landing/empresa/marca-espacio.html')
    context = {}
    view_from = False
    current_promo = None
    auto_generated = upper(get_random_string(CODE_LENGHT))  # Crea un codigo aletarorio para la promocion
    categorias = None

    # Si no se ha creado un perfil publico
    # Se crea aqui
    if MiPerfil.objects.filter(user=request.user).count() == 0:
        print('Creamos dummy para la clase MiPerfil')
        perfil = MiPerfil(user=request.user)
        perfil.save()

    query_perfil = Q(user=request.user)
    perfil = MiPerfil.objects.filter(query_perfil).first()

    if request.user.is_authenticated:

        categorias = Categoria.objects.filter(user=request.user).exclude(categoria_padre__isnull=False)
        if 'current_promo' in request.session and request.session[
            'from'] != 'edit-promo':  # si actualmente estoy creando una promocion y tengo datos metidos los cargo en el template
            current_promo = Promocion.objects.filter(id=request.session['current_promo']).first()
        else:
            if 'current_promo' in request.session:
                del request.session['current_promo']

        items = Articulo.objects.filter(
            user=request.user
        ).order_by('nombre')[:5]

        user = get_object_or_404(CustomUser, pk=request.user.id)

        # Si es la primera vez que accedemos a marca-espacio
        # Creamos un dummy para cada clase
        if Marca.objects.filter(user=request.user).count() == 0:
            print('Creamos dummy para la clase marca')
            marca_form = MarcaForm()
            marca = marca_form.save(commit=False)
            marca.user = request.user
            marca.save()

        marca = get_object_or_404(Marca, user=request.user)

        if Espacio.objects.filter(user=request.user).count() == 0:
            print('Creamos dummy para la clase espacio')
            espacio_form = EspacioForm()
            espacio = espacio_form.save(commit=False)
            espacio.user = request.user
            espacio.save()

        if len(Maestro.objects.filter(user=request.user)) == 0:
            print('Creamos dummy para la clase maestro')
            maestro_form = MaestroForm()
            maestro = maestro_form.save(commit=False)
            maestro.user = request.user
            maestro.save()

        espacio = get_object_or_404(Espacio, user=request.user)
        maestro = get_object_or_404(Maestro, user=request.user)

        if request.session.get('from', None) == 'add-promo':
            view_from = 'show_promo'
        elif request.session.get('from', None) == 'add-item':
            view_from = 'show_items'
        elif request.session.get('from', None) == 'colecciones':
            view_from = 'show_col'

        if request.method == 'GET':
            form_negocio = CustomUserMarcaEspacio(instance=user)
            marca_form = MarcaForm(instance=marca)
            espacio_form = EspacioForm(instance=espacio)
            editar_espacio_form = EditarEspacioForm(instance=espacio)
            maestro_form = MaestroForm(instance=maestro)
        else:
            form_negocio = CustomUserMarcaEspacio(request.POST, instance=user)
            marca_form = MarcaForm(request.POST, instance=marca)
            espacio_form = EspacioForm(request.POST, instance=espacio)
            editar_espacio_form = EditarEspacioForm(request.POST, instance=espacio)
            maestro_form = MaestroForm(request.POST, instance=maestro)

            if request.POST.get("guardar_edit_espacio"):
                if editar_espacio_form.is_valid():
                    espacio = editar_espacio_form.save(commit=False)
                    espacio.user = user
                    espacio.save()
                    messages.success(request, 'La información se ha guardado correctamente')
                else:
                    messages.warning(request, "No se ha guardado bien el formulario")
            else:
                if form_negocio.is_valid():
                    form_negocio.save()
                if marca_form.is_valid():
                    marca_form.save()
                if espacio_form.is_valid():
                    espacio = espacio_form.save(commit=False)
                    espacio.user = user
                    espacio.save()
                if maestro_form.is_valid():
                    maestro_form.save()

                if request.POST.get("guarda_marca"):
                    perfil.is_marca = True
                    perfil.save()
                    print("marca")
                elif request.POST.get("guarda_espacio"):
                    perfil.is_espacio = True
                    perfil.save()
                    print("espacio")

                print('La información se ha guardado correctamente.')
                messages.success(request, 'La información se ha guardado correctamente')

        context = {
            'form_negocio': form_negocio,
            'maestro_form': maestro_form,
            'marca_form': marca_form,
            'espacio_form': espacio_form,
            'editar_espacio_form': editar_espacio_form,
            'view_from': view_from,
            'current_promo': current_promo,
            'categorias': categorias,
            'auto_generated_code': auto_generated
        }
        request.session['from'] = 'marca-espacio'

    return HttpResponse(template.render(context, request))


def add_categoria(request):
    if request.method == 'POST':
        if request.POST.get('categoria') and request.POST.get('categoria') != '':
            categoria = request.POST.get('categoria')

            if len(Categoria.objects.filter(user=request.user, nombre=categoria).exclude(
                    categoria_padre__isnull=False)) == 0:
                new_cat = Categoria(user=request.user, nombre=categoria)
                result = new_cat
                new_cat.save()
                if request.POST.getlist('subcategorias[]'):
                    sub = request.POST.getlist('subcategorias[]')
                    for s in sub:
                        Categoria.objects.create(user=request.user, nombre=s, categoria_padre=new_cat)
                result = new_cat
                msg_list = result.json()
                return JsonResponse(msg_list, safe=False)
            else:
                return JsonResponse(False, safe=False)


def edit_categoria(request):
    if request.method == 'POST':
        if request.POST.get('categoria') and request.POST.get('categoria') != '':
            categoria_id = request.POST.get('categoria')
            categoria = Categoria.objects.filter(id=categoria_id).first()
            if categoria is not None:
                if request.POST.get('nombre') and request.POST.get('nombre') != '':
                    categoria.nombre = request.POST.get('nombre')
                    categoria.save()
                    msg_list = categoria.json()
                    return JsonResponse(msg_list, safe=False)
            else:
                return JsonResponse(False, safe=False)
    else:
        return JsonResponse(False, safe=False)


def delete_categoria(request):
    if request.method == 'POST':
        if request.POST.get('categoria') and request.POST.get('categoria') != '':
            categoria_id = request.POST.get('categoria')
            categoria = Categoria.objects.filter(id=categoria_id).first()
            if categoria is not None:
                categoria.delete()
                return JsonResponse(True, safe=False)
            else:
                return JsonResponse(False, safe=False)
    else:
        return JsonResponse(False, safe=False)


def single_item_edit(request):
    template = loader.get_template('landing/empresa/catalogo/add-item.html')
    context = {}
    con_errores = False
    if request.user.is_authenticated:

        if Maestro.objects.filter(user=request.user):
            maestro = Maestro.objects.get(user=request.user)
        else:
            maestro = False

        if request.method == 'GET':
            pass
        else:
            if request.POST.get('data'):  # obtengo los ids del articulo que se ha seleccionado para editar
                ids = request.POST.get('data')
                my_list = ids.split(",")
                articulo = Articulo.objects.filter(id__in=my_list).first();

                if request.POST.get('save_item'):  # True si se ha pulsado el boton de guardar, sino simplemente mostrar
                    if maestro:
                        form = NewItemForm(maestro, request.POST)
                    else:
                        form = NewItemForm(False, request.POST)
                else:
                    if maestro:
                        form = NewItemForm(maestro, instance=articulo)
                    else:
                        form = NewItemForm(False, instance=articulo)

                form_categorias = SeleccionarCategoriasForm(request.POST)

                forms_ok, errors = check_forms(form, form_categorias)
                if forms_ok:
                    files = request.FILES.getlist('articulo-images')

                    if len(files) > 0:  # Si nos llegan fotos nuevas las guardamos
                        for afile in files:
                            pic = GaleriaArticulo()
                            pic.articulo = articulo
                            pic.imagen = afile
                            pic.save()

                    articulo.mercado.set(form.cleaned_data['mercado'])
                    articulo.target.set(form.cleaned_data['target'])
                    articulo.categoria = form_categorias.cleaned_data['categorias']
                    articulo.subcategoria = form_categorias.cleaned_data['subcategorias']

                    articulo.save()
                    # Si llegan variaciones en el request se crean un objeto VarianteArtiuclo en la base de datos
                    # por cada una
                    if request.POST['mis_variaciones'] and request.POST['mis_variaciones'] != 'empty':
                        variaciones = request.POST['mis_variaciones']
                        variaciones = variaciones.replace("&quot;", "'")
                        variaciones = json.loads(variaciones)

                        for variacion in variaciones:
                            new_var = VarianteArticulo()
                            new_var.articulo = articulo

                            for idx, opcion in enumerate(variacion):

                                if idx == 0:
                                    new_var.opcion_1 = opcion[0]
                                    new_var.opcion_1_value = opcion[1]
                                elif idx == 1:
                                    new_var.opcion_2 = opcion[0]
                                    new_var.opcion_2_value = opcion[1]
                                elif idx == 2:
                                    new_var.opcion_3 = opcion[0]
                                    new_var.opcion_3_value = opcion[1]

                            new_var.precio_comparacion = articulo.precio_comparacion
                            new_var.ref = articulo.ref
                            new_var.url = articulo.url
                            new_var.imagen_principal = articulo.imagen_principal
                            new_var.precio_coste = articulo.precio_coste
                            new_var.pvp = articulo.pvp
                            try:
                                if not VarianteArticulo.objects.filter(articulo=articulo,
                                                                       opcion_1_value=new_var.opcion_1_value,
                                                                       opcion_2_value=new_var.opcion_2_value,
                                                                       opcion_3_value=new_var.opcion_3_value,
                                                                       opcion_1=new_var.opcion_1,
                                                                       opcion_2=new_var.opcion_2,
                                                                       opcion_3=new_var.opcion_3):
                                    new_var.save()
                            except Exception as e:
                                con_errores = True

                            if con_errores:
                                messages.warning(request,
                                                 'Algunas variantes no se han podido guardar, compruebe el editor masivo')
                            else:
                                messages.success(request, 'El artículo se ha añadido correctamente')
                        request.session['from'] = 'add-item'
                        return redirect('mi-catalogo')

                else:
                    for error in errors:
                        messages.warning(request, error)
                    print('Error al añadir el artículo')
            else:
                messages.warning(request, 'Error al obtener la referencia del articulo')
                print('Error al obtener la referencia del articulo')

        context = {
            'form': form,
            'form_categorias': form_categorias,
            'articulo': articulo

        }

    return HttpResponse(template.render(context, request))


def create_variante_from_file(line, item):
    variante = VarianteArticulo(articulo=item)
    if line[8] != '':  # option1 name  -> option_1 / # option1 value -> option_1_value
        if len(item.variantes.all()) > 0:
            variante.opcion_1 = item.variantes.all()[0].tag
            variante.opcion_1_value = line[8]  # option2 name  -> option_2 / # option2 value -> option_2_value
    if line[10] != '':
        if len(item.variantes.all()) > 1:
            variante.opcion_2 = item.variantes.all()[1].tag
            variante.opcion_2_value = line[10]
    if line[13] != '':
        variante.ref = line[13]
    if line[18] != '':
        variante.pvp = Decimal(line[18])
    if line[19] != '':
        variante.precio_comparacion = Decimal(line[19])
    if line[23] != '':
        variante.imagen_principal = line[23]
    if line[45] != '' and line[45] != '"':
        variante.precio_coste = Decimal(line[45].replace('"', ""))
    variante.save()


def create_articulo_from_file(line, user):  # Tranforma celda del CSV en campo para el articulo //
    #  Columna del CSV -> Correspondencia en el modelo
    print(line)
    if Articulo.objects.filter(handle=line[0]) and line[0] != '' and line[0] != '-':
        item = Articulo.objects.filter(handle=line[0]).first()
        if len(item.variantes.all()) > 0:
            create_variante_from_file(line, item)
    else:
        item = Articulo(user=user)
        if line[0] != '':
            item.handle = line[0]
        if line[1] != '':  # Title -> Nombre
            item.nombre = line[1]
        if line[2] != '':  # Body HTML -> Descripcion
            item.descripcion = line[2]
        if line[13] != '':  # Variant SKU -> Ref
            item.ref = line[13]
        if line[18] != '':  # Variant price -> pvp
            item.pvp = Decimal(line[18])
        if line[19] != '':  # Variant compare at price -> precio_comparacion
            item.precio_comparacion = Decimal(line[19])
        if line[23] != '':  # IMG src -> imagen_principal
            item.imagen_principal = line[23]
        if line[45] != '' and line[45] != '"':  # Cost per item -> precio_coste
            item.precio_coste = Decimal(line[45].replace('"', ""))
        if item.save():
            if line[7] != '':
                if DefinicionVariante.objects.filter(tag=line[7]):
                    item.variantes.add(DefinicionVariante.objects.filter(tag=line[7]).first())
                else:
                    new = DefinicionVariante.objects.create(tag=line[7], user=user)
                    item.variantes.add(new)

            if line[9] != '':
                if DefinicionVariante.objects.filter(tag=line[9]):
                    item.variantes.add(DefinicionVariante.objects.filter(tag=line[9]).first())
                else:
                    new = DefinicionVariante.objects.create(tag=line[9], user=user)
                    item.variantes.add(new)
            if len(item.variantes.all()) > 0:
                create_variante_from_file(line, item)


def handle_csv(file, user):
    decoded_file = file.read().decode(
        'utf-8')  # decodifica el InMemoryUploadFile para que pueda usar el metodo csv.reader
    io_string = io.StringIO(decoded_file)
    for index, line in enumerate(csv.reader(io_string, delimiter=',', quotechar='|')):
        if index != 0:
            create_articulo_from_file(line, user)
        else:
            print(line)


def create_variante_from_line_ex(header, line, item):
    variante = VarianteArticulo(articulo=item)
    for index, cell in enumerate(line):
        if header[index] == 'REF':
            if cell != '':
                item.ref = cell
        if header[index] == 'PVP':
            if cell != '':
                item.pvp = Decimal(cell)
        if header[index] == 'P_COMP':
            if cell != '':
                item.precio_comparacion = Decimal(cell)
        if header[index] == 'P_COSTE':
            if cell != '':
                item.precio_coste = Decimal(cell)
        if header[index] == 'URL':
            if cell != '':
                item.url = cell
        if header[index] == 'TAG1VALUE':
            if cell != '':
                if len(item.variantes.all()) > 0:
                    variante.opcion_1 = item.variantes.all()[0].tag
                    variante.opcion_1_value = cell
        if header[index] == 'TAG2VALUE':
            if cell != '':
                if len(item.variantes.all()) > 1:
                    variante.opcion_2 = item.variantes.all()[1].tag
                    variante.opcion_2_value = cell
    variante.save()

def create_articulo_from_line_ex(header, line, user):
    if Articulo.objects.filter(handle=slugify(line[header.index('HANDLE')])):
        print("entro a variante directamente")
        item = Articulo.objects.filter(handle=line[header.index('HANDLE')]).first()
        if len(item.variantes.all()) > 0:
            create_variante_from_line_ex(header, line, item)
    else:
        item = Articulo(user=user)
        for index, cell in enumerate(line):

            if header[index] == 'HANDLE':
                if cell != '':
                    print(cell)
                    item.handle = cell
            elif header[index] == 'REF':
                if cell != '':
                    item.ref = cell
            elif header[index] == 'NOMBRE':
                if cell != '':
                    item.nombre = cell
            elif header[index] == 'DESCRIPCION':
                if cell != '':
                    item.descripcion = cell
            elif header[index] == 'PVP':
                if cell != '':
                    item.pvp = Decimal(cell)
            elif header[index] == 'P_COMP':
                if cell != '':
                    item.precio_comparacion = Decimal(cell)
            elif header[index] == 'P_COSTE':
                if cell != '':
                    item.precio_coste = Decimal(cell)
            elif header[index] == 'URL':
                if cell != '':
                    item.url = cell

        if item.save():
            if line[header.index('TAG1')] != '':
                if DefinicionVariante.objects.filter(tag=line[header.index('TAG1')]):
                    item.variantes.add(DefinicionVariante.objects.filter(tag=line[header.index('TAG1')]).first())
                else:
                    new = DefinicionVariante.objects.create(tag=line[header.index('TAG1')], user=user)
                    item.variantes.add(new)

            if line[header.index('TAG2')] != '':
                if DefinicionVariante.objects.filter(tag=line[header.index('TAG2')]):
                    item.variantes.add(DefinicionVariante.objects.filter(tag=line[header.index('TAG2')]).first())
                else:
                    new = DefinicionVariante.objects.create(tag=line[header.index('TAG2')], user=user)
                    item.variantes.add(new)
            if len(item.variantes.all()) > 0:
                create_variante_from_line_ex(header, line, item)


def handleExcel(file, user):
    wb = openpyxl.load_workbook(file)
    excel_data = list()

    for sheet in wb:
        header = list()
        for index, row in enumerate(sheet.iter_rows()):
            if index == 0:
                for cell in row:
                    header.append(str(cell.value))
            else:
                row_data = list()
                for index, cell in enumerate(row):
                    row_data.append(str(cell.value))
                excel_data.append(row_data)
                create_articulo_from_line_ex(header, row_data, user)


def import_file(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.FILES != {}:  # Si no viene vacío
                myfile = request.FILES['shp-csv'] if request.FILES.get('shp-csv') else request.FILES['shp-ex']
                if myfile.content_type == 'text/csv':
                    handle_csv(myfile, request.user)
                    messages.success(request,
                                     "Archivo importado correctamente, vaya al buscador de sus articulos para comprobarlo")

                elif myfile.content_type == 'application/vnd.ms-excel' or myfile.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or myfile.content_type == 'application/vnd.oasis.opendocument.spreadsheet':

                    handleExcel(myfile, request.user)
                else:
                    print("formato no soportado", myfile.content_type)
                    messages.warning(request, "Formato de arhivo incorrecto, Formatos aceptados: CSV y EXCEL")

            else:
                messages.warning(request,
                                 "Error al detectar el fichero, asegurese de que está subiendo el archivo correcto")
                request.session['from'] = 'add-item'

            request.session['from'] = 'add-item'

    return redirect('mi-catalogo')


def add_item(request):
    template = loader.get_template('landing/empresa/catalogo/add-item.html')
    context = {}
    con_errores = False

    if request.user.is_authenticated:

        if Maestro.objects.filter(user=request.user):
            maestro = Maestro.objects.get(user=request.user)
        else:
            maestro = False

        if request.method == 'GET':
            if maestro:
                form = NewItemForm(maestro)
            else:
                form = NewItemForm(False)

            form_categorias = SeleccionarCategoriasForm()

        else:
            if maestro:
                form = NewItemForm(maestro, request.POST)
            else:
                form = NewItemForm(False, request.POST)

            form_categorias = SeleccionarCategoriasForm(request.POST)
            forms_ok, errors = check_forms(form, form_categorias)
            if forms_ok:
                files = request.FILES.getlist('articulo-images')

                if len(files) > 0:
                    # Guardamos primero el articulo y luego le añadimos los mercados, targets y categorias
                    # sino da error de many-to-many relationship
                    item = form.save(commit=False)
                    item.user = request.user
                    item.save()
                    item.mercado.set(form.cleaned_data['mercado'])
                    item.target.set(form.cleaned_data['target'])
                    item.categoria = form_categorias.cleaned_data['categorias']
                    item.subcategoria = form_categorias.cleaned_data['subcategorias']

                    item.save()

                    for afile in files:
                        pic = GaleriaArticulo()
                        pic.articulo = item
                        pic.imagen = afile
                        pic.save()

                    # Si llegan variaciones en el request se crean un objeto VarianteArtiuclo en la base de datos
                    # por cada una
                    if request.POST['mis_variaciones'] and request.POST['mis_variaciones'] != 'empty':
                        variaciones = request.POST['mis_variaciones']
                        variaciones = variaciones.replace("&quot;", "'")
                        variaciones = json.loads(variaciones)

                        variaciones_tags = request.POST['variaciones_tags']
                        variaciones_tags = variaciones_tags.replace("$quot;", "'")
                        variaciones_tags = json.loads(variaciones_tags)

                        for tag in variaciones_tags:
                            if not DefinicionVariante.objects.filter(tag=tag) and tag != '':
                                DefinicionVariante.objects.create(user=request.user, tag=tag)
                        item.variantes.set(
                            DefinicionVariante.objects.filter(user=request.user, tag__in=variaciones_tags))

                        for variacion in variaciones:
                            new_var = VarianteArticulo()
                            new_var.articulo = item

                            for idx, opcion in enumerate(variacion):

                                if idx == 0:
                                    new_var.opcion_1 = opcion[0]
                                    new_var.opcion_1_value = opcion[1]
                                elif idx == 1:
                                    new_var.opcion_2 = opcion[0]
                                    new_var.opcion_2_value = opcion[1]
                                elif idx == 2:
                                    new_var.opcion_3 = opcion[0]
                                    new_var.opcion_3_value = opcion[1]

                            new_var.precio_comparacion = item.precio_comparacion
                            new_var.ref = item.ref
                            new_var.url = item.url
                            new_var.imagen_principal = item.imagen_principal
                            new_var.precio_coste = item.precio_coste
                            new_var.pvp = item.pvp
                            try:
                                new_var.save()
                            except Exception as e:
                                con_errores = True

                    if con_errores:
                        messages.warning(request,
                                         'Algunas variantes no se han podido guardar, compruebe el editor masivo')
                    else:
                        messages.success(request, 'El artículo se ha añadido correctamente')
                    request.session['from'] = 'add-item'
                    return redirect('mi-catalogo')

                else:
                    messages.warning(request, 'Error al añadir el artículo, añade al menos una foto')
                    print('Error al añadir el artículo, falta la foto')
            else:
                for error in errors:
                    messages.warning(request, error)
                print('Error al añadir el artículo')

        context = {
            'form': form,
            'form_categorias': form_categorias,
        }

    return HttpResponse(template.render(context, request))


def search_item_col(request, coleccion_id):
    template = loader.get_template('landing/empresa/catalogo/colecciones/search-view.html')
    context = {}
    articulos = Articulo.objects.filter(user=request.user).order_by('nombre')
    maestro = Maestro.objects.filter(user=request.user)
    empresa = Empresa.objects.filter(user=request.user).first()
    colecciones = Coleccion.objects.filter(empresa=empresa)
    categorias = Categoria.objects.filter(user=request.user).exclude(categoria_padre__isnull=False)

    context = {
        'articulos': articulos,
        'maestro': maestro,
        'categorias': categorias,
        'colecciones': colecciones,
        'coleccion_id': coleccion_id
    }
    return HttpResponse(template.render(context, request))


def coleccion(request, coleccion_id):
    template = loader.get_template('landing/empresa/catalogo/colecciones/coleccion-detail.html')
    coleccion = Coleccion.objects.filter(id=coleccion_id).first()
    context = {}
    loaded = False
    articulos_seleccionados = []

    if request.user.is_authenticated:
        if request.method == "POST":
            if coleccion_id != '-1':

                if 'add-items-coleccion' in request.POST:
                    return redirect('search-item-col', coleccion_id=coleccion.id)

                elif 'save-coleccion' in request.POST:
                    form = ColeccionForm(request.POST, instance=coleccion)
                    if form.is_valid():

                        if request.POST.get('new_items'):
                            items = request.POST['new_items']
                            items = items.replace("&quot;", "'")
                            items = items.split(',')
                            lista = Articulo.objects.filter(id__in=items)
                            for i in lista:
                                coleccion.articulos.add(i)
                            coleccion.save()

                        coleccion = form.save(commit=False)
                        coleccion.save()
                        request.session['from'] = 'colecciones'
                        return redirect('mi-catalogo')

                elif 'enviar-ids' in request.POST:
                    ids = request.POST.get('selected-promo-items')
                    my_list = ids.split(",")
                    if '' in my_list:
                        form = ColeccionForm(instance=coleccion)
                    else:
                        articulos_seleccionados = Articulo.objects.filter(id__in=my_list)
                        form = ColeccionForm(instance=coleccion)
                        loaded = True

                elif Coleccion.objects.filter(id=coleccion_id):
                    form = ColeccionForm(instance=coleccion)

            else:
                if request.user.empresa.first():

                    coleccion = Coleccion(empresa=request.user.empresa.first())
                    coleccion.save()
                    return redirect('coleccion', coleccion.id)
                else:
                    messages.warning(request,
                                     "Debes guardar la información sobre tu \"EMPRESA\" antes de poder guardar colecciones")
                    return redirect('mi-catalogo')

        else:
            form = ColeccionForm(instance=coleccion)

        context = {
            'coleccion': coleccion,
            'form': form,
            'articulos_nuevos': articulos_seleccionados,
            'loaded': loaded
        }

    return HttpResponse(template.render(context, request))


def colecciones(request):
    template = loader.get_template('landing/empresa/catalogo/colecciones/colecciones.html')
    colecciones = Coleccion.objects.filter(empresa__user=request.user)
    context = {}
    if request.user.is_authenticated:
        if request.method == "GET":
            context = {
                'colecciones': colecciones,

            }

    return HttpResponse(template.render(context, request))


def colecciones_visibles(request, pdv_id):
    template = loader.get_template('landing/empresa/catalogo/colecciones/colecciones-visibles.html')
    colecciones = Coleccion.objects.filter(empresa__user=request.user, visible=True)
    context = {}
    if request.user.is_authenticated:
        if request.method == "POST":
            context = {
                'colecciones': colecciones,
                'pdv_id': pdv_id
            }

    return HttpResponse(template.render(context, request))


def editar_stock(request, coleccion_id, pdv_id):
    print(coleccion_id, pdv_id)
    # todo al guardar un stock en un pdv, resto del stock real?
    template = loader.get_template('landing/empresa/catalogo/colecciones/editor-stock.html')
    context = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            coleccion = Coleccion.objects.get(id=coleccion_id)
            if 'add-to-pdv' in request.POST:
                if PuntoDeVenta.objects.filter(id=pdv_id):
                    pdv = PuntoDeVenta.objects.get(id=pdv_id)
                    pdv.colecciones.add(coleccion)
                    if request.POST.getlist('articulos-map'):
                        for art in request.POST.getlist('articulos-map'):
                            id, stock = art.split("-")
                            reference = Articulo.objects.get(id=int(id))

                            if int(stock) <= reference.stock:
                                if (len(
                                        reference.en_pdv.filter(pdv=pdv,
                                                                coleccion=coleccion)) > 0) == True and reference.en_pdv.first() in pdv.articulos.all():
                                    item = reference.en_pdv.first()
                                    item.cantidad = int(stock)
                                    item.save()
                                else:
                                    item = ArticuloPDV(pdv=pdv, articulo=reference, cantidad=int(stock),
                                                       coleccion=coleccion)
                                    item.save()
                                reference.stock = reference.stock - int(stock)
                                reference.save()

                    if request.POST.getlist('variantes-map'):
                        for variante in request.POST.getlist('variantes-map'):
                            id, stock = variante.split("-")
                            reference = VarianteArticulo.objects.get(id=int(id))
                            if int(stock) <= reference.stock:
                                if (len(
                                        reference.en_pdv.filter(pdv=pdv,
                                                                coleccion=coleccion)) > 0) == True and reference.en_pdv.first() in pdv.articulos.all():
                                    item = reference.en_pdv.first()
                                    item.cantidad = int(stock)
                                    item.save()
                                else:
                                    item = ArticuloPDV(pdv=pdv, articulo=reference.articulo, variante=reference,
                                                       cantidad=int(stock),
                                                       coleccion=coleccion)
                                    item.save()
                                reference.stock = reference.stock - int(stock)
                                reference.save()

                    request.session['from'] = 'editar-stock'
                    return redirect('relaciones-comerciales')

            else:
                if Coleccion.objects.filter(empresa__user=request.user, id=coleccion_id):
                    coleccion = Coleccion.objects.filter(empresa__user=request.user, id=coleccion_id).first()
                    context = {
                        'coleccion': coleccion,
                    }

    return HttpResponse(template.render(context, request))


def toggle_visible_col(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            print(request.POST)

            if request.POST.get('col') and request.POST.get('checked'):  # obtengo el id de la colección
                coleccion = Coleccion.objects.get(id=request.POST.get('col'))
                coleccion.visible = True if request.POST.get('checked') == 'true' else False
                coleccion.save()

                return JsonResponse(True, safe=False)

            else:
                raise ValueError("Ha ocurrido un error al recuperar la lista de articulos")
        else:
            raise ValidationError("Petición no válida")

    return JsonResponse(False, safe=False)


def market(request):
    template = loader.get_template('landing/market/market.html')

    usuarios = CustomUser.objects.exclude(
        username=request.user.username
    ).filter(Q(is_marca=True) | Q(is_espacio=True), Q(validado=True))[:users_to_get(CustomUser.objects.count() - 1)]

    query_perfil = Q(user=request.user)
    perfil = MiPerfil.objects.filter(query_perfil).first()

    context = {
        'usuarios': usuarios,
        'perfil': perfil
    }

    return HttpResponse(template.render(context, request))


def propuesta(request, user="default"):
    template = loader.get_template('landing/market/propuesta.html')
    context = {}

    query = Q(username=user)
    usuario = CustomUser.objects.filter(query).first()

    query_perfil = Q(user=usuario)
    perfil = MiPerfil.objects.filter(query_perfil).first()

    query_perfil = Q(user=request.user)
    mi_perfil = MiPerfil.objects.filter(query_perfil).first()

    query_propuesta = Q(emisor=request.user) & Q(receptor=usuario)
    propuesta = PropuestaComercial.objects.filter(query_propuesta).first()

    query_propuesta2 = Q(emisor=usuario) & Q(receptor=request.user)
    propuesta2 = PropuestaComercial.objects.filter(query_propuesta2).first()

    if perfil.is_espacio:
        query2 = Q(user=usuario)
        empresa = Empresa.objects.filter(query2).first()

        query3 = Q(empresa=empresa)
        alquiler = Alquiler.objects.filter(query3).first()
    else:
        query2 = Q(user=request.user)
        empresa = Empresa.objects.filter(query2).first()

        query3 = Q(empresa=empresa)
        alquiler = Alquiler.objects.filter(query3).first()

    if request.user.is_authenticated:
        if request.method == 'GET':
            if alquiler:
                if propuesta and propuesta.estado == "PENDIENTE":
                    form = PropuestaComercialForm(initial={
                        'precio_dia': alquiler.euros_dia,
                        'precio_semana': alquiler.euros_semana,
                        'precio_mes': alquiler.euros_mes,
                        'precio_total': alquiler.euros_mes,
                        'porcentaje_ventas': perfil.ventas
                    }, instance=propuesta)

                    messages.warning(request, "Estás editando tu actual propuesta a "
                                     + usuario.first_name + ", " +
                                     "si quieres que vuelva a recibir una notificación de tu propuesta, borra" +
                                     " esta y crea una nueva.")
                elif propuesta2:
                    form = PropuestaComercialForm(initial={
                        'precio_dia': alquiler.euros_dia,
                        'precio_semana': alquiler.euros_semana,
                        'precio_mes': alquiler.euros_mes,
                        'precio_total': alquiler.euros_mes,
                        'porcentaje_ventas': perfil.ventas
                    }, instance=propuesta2)

                    messages.warning(request, "Estás editando la propuesta de " + usuario.first_name + ", " +
                                     "si quieres que vuelva a recibir una notificación de tu propuesta, borra" +
                                     " esta y crea una nueva." +
                                     "recuerda que solo podrás hacerlo una vez.")

                else:
                    form = PropuestaComercialForm(initial={
                        'precio_dia': alquiler.euros_dia,
                        'precio_semana': alquiler.euros_semana,
                        'precio_mes': alquiler.euros_mes,
                        'precio_total': alquiler.euros_mes,
                        'porcentaje_ventas': perfil.ventas
                    })
            else:
                form = PropuestaComercialForm(initial={
                    'precio_dia': 0,
                    'precio_semana': 0,
                    'precio_mes': 0,
                    'precio_total': 0,
                    'porcentaje_ventas': perfil.ventas
                })
        else:
            if propuesta:
                form = PropuestaComercialForm(request.POST, instance=propuesta)
            elif propuesta2:
                form = PropuestaComercialForm(request.POST, instance=propuesta2)
            else:
                form = PropuestaComercialForm(request.POST)
            print(form.errors)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.emisor = request.user
                obj.receptor = usuario
                obj.is_cancelada = False
                if propuesta2:
                    obj.emisor = usuario
                    obj.receptor = request.user
                    propuesta2.modificaciones_receptor += 1
                    propuesta2.save()
                obj.save()
                messages.success(request, 'Propuesta enviada con éxito.')

                return redirect('relaciones-comerciales')
            else:
                messages.warning(request, "Error al enviar la propuesta. Comprueba que has rellenado los campos "
                                          "obligatorios correctamente.")

        context = {
            'form': form,
            'perfil': mi_perfil,
            'usuario': usuario,
            'alquiler': alquiler
        }

    return HttpResponse(template.render(context, request))


def perfil_kradeler_unavailable(request):
    return render(request, 'landing/public/unavailable.html')


def perfil_kradeler_market(request, user="unavailable"):
    template = loader.get_template('landing/market/perfil-kradeler-market.html')

    # TODO Si cualquiera de estas 2 queries no existe, deberia mandar al 404 o al market.
    query = Q(username=user)
    usuario = CustomUser.objects.filter(query).first()

    query_propuesta = Q(emisor=request.user) & Q(receptor=usuario) & Q(estado='PENDIENTE')
    query_propuesta.add(Q(emisor=usuario) & Q(receptor=request.user) & Q(estado='PENDIENTE'), Q.OR)
    propuesta = PropuestaComercial.objects.filter(query_propuesta).first()

    query2 = Q(user=usuario)
    perfil = MiPerfil.objects.filter(query2).first()
    empresa = Empresa.objects.filter(query2).first()

    query3 = Q(user=request.user)
    miperfil = MiPerfil.objects.filter(query3).first()

    if not miperfil:
        messages.warning(request, "Completa tu perfil kradeler para poder acceder a todas las funcionalidades que "
                                  "ofrece Kradleco Market")

    enabled = True
    sendable = True
    compatible = True
    if perfil and miperfil:
        if (perfil.is_marca and miperfil.is_marca) or (perfil.is_espacio and miperfil.is_espacio):
            compatible = False

        if not miperfil.is_marca and not miperfil.is_espacio:
            enabled = False

        if not perfil.is_marca and not perfil.is_espacio:
            sendable = False
    else:
        enabled = False

    if not query or not query2:
        return redirect('perfil-kradeler-unavailable')

    query4 = Q(empresa=empresa)
    alquiler = Alquiler.objects.filter(query4).first()

    query_conectados = Q(emisor=request.user)
    query_conectados.add(Q(receptor=usuario), Q.AND)
    query_conectados.add(Q(estado='ACEPTADA'), Q.AND)
    query_conectados.add(Q(emisor=usuario) & Q(receptor=request.user) & Q(estado='ACEPTADA'), Q.OR)

    # Comprueba si existe una conexion entre ambos usuarios la cual esté ya aceptada
    conec_existe_aceptada = Conexion.objects.filter(query_conectados)

    if request.method == 'POST':

        if request.POST.get('desconectar'):
            conec = Conexion.objects.filter(query_conectados).first()
            if conec:
                conec.delete()
        else:
            query = Q(emisor=request.user)
            query.add(Q(receptor=usuario), Q.AND)
            # Comprueba si ya hemos mandado esa solicitud al otro usuario
            conec_existe = Conexion.objects.filter(query)

            if conec_existe.count() > 0 or conec_existe_aceptada.count() > 0:
                if conec_existe_aceptada.count() > 0:
                    messages.warning(request, 'Ya tienes a este usuario en tu red de contactos.')
                else:
                    messages.warning(request, 'Ya has enviado una solicitud a este usuario')
            else:
                query2 = Q(receptor=request.user)
                query2.add(Q(emisor=usuario), Q.AND)
                query2.add(Q(estado='PENDIENTE'), Q.AND)

                # Comprueba si el otro usuario nos ha solicitado contactar ya, por lo que si intentamos
                # Conectar con el, nos agregamos mutuamente de forma automática
                conec_existe2 = Conexion.objects.filter(query2).first()

                if conec_existe2:
                    print("existe")
                    conec_existe2.estado = 'ACEPTADA'
                    conec_existe2.save()
                    messages.success(request, 'Usuario añadido a tu red de contactos.')
                else:
                    conexion = Conexion()
                    conexion.emisor = request.user
                    conexion.receptor = usuario
                    conexion.save()
                    messages.success(request, 'Solicitud enviada con éxito')

    context = {
        'perfil': perfil,
        'empresa': empresa,
        'alquiler': alquiler,
        'enabled': enabled,
        'compatible': compatible,
        'sendable': sendable,
        'conectados': conec_existe_aceptada,
        'usuario': usuario,
        'propuesta': propuesta
    }

    return HttpResponse(template.render(context, request))


# A esta view se puede llegar desde la propia template editor-masivo o desde articulos.html (ambos casos por post)
def edit_items(request):
    # todo en el editor masivo, implementar una funcionalidad para editar muchos campos a la vez
    template = loader.get_template('landing/empresa/catalogo/editor-masivo.html')
    context = {}
    articulos = []
    forms = []

    if request.user.is_authenticated:

        if request.method == 'POST':
            if request.POST.get('data'):  # obtengo los ids de los articulos que se han seleccionado para editarlos
                ids = request.POST.get('data')
                my_list = ids.split(",")
                articulos = Articulo.objects.filter(id__in=my_list);

                if request.POST.get('save'):  # si me llega la señal de save es que estoy guardando las ediciones
                    for index, art in enumerate(articulos):
                        forms.append(NewItemForm(False, request.POST, instance=art, prefix=index))
                        for index1, variante in enumerate(art.variantearticulo.all()):
                            forms.append(
                                VarianteForm(False, request.POST, instance=variante, prefix=index1))

                else:  # si no llega la señal de save simplemente muestro los articulos/variaciones para poder editarlos

                    for index, art in enumerate(articulos):
                        forms.append(NewItemForm(False, instance=art, prefix=index))
                        for index1, variante in enumerate(art.variantearticulo.all()):
                            forms.append(VarianteForm(False, instance=variante, prefix=index1))

                forms_ok, errors = check_forms(*forms)

                if forms_ok:

                    for form in forms:
                        item = form.save(commit=False)
                        item.save()
                else:
                    for error in errors:
                        messages.warning(request, error)
                    print('Error al añadir el artículo')



            else:
                raise ValueError("Ha ocurrido un error al recuperar la lista de articulos")

        else:
            raise ValidationError("Petición no válida")

        context = {
            'articulos': articulos,
            'forms': forms,
            'ids': ids
        }

    return HttpResponse(template.render(context, request))


def delete_items(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            if request.POST.get('q[]'):  # obtengo los ids de los articulos que se han seleccionado para editarlos
                ids = request.POST.get('q[]')
                my_list = ids.split(",")
                articulos = Articulo.objects.filter(id__in=my_list)
                articulos.delete()

                return JsonResponse(True, safe=False)

            else:
                raise ValueError("Ha ocurrido un error al recuperar la lista de articulos")
        else:
            raise ValidationError("Petición no válida")

    return JsonResponse(False, safe=False)


def scanner(request):
    template = loader.get_template('landing/market/pdv/scanner.html')
    context = {}
    if request.user.is_authenticated:
        pass

    return HttpResponse(template.render(context, request))


# Vista para mostrar la información de un articulo cuyo id se pasa por la url
def articulo_detail(request, pdv_id, articulo_id):
    template = loader.get_template('landing/market/pdv/articulo-detail.html')
    context = {}

    if request.user.is_authenticated:
        if request.method == 'POST':
            articulo = ArticuloPDV.objects.get(id=articulo_id)
            # if articulo is not None:  # Recorre todos los articulos del pdv y guarda las variantes del articulo seleeccionado
            #     variantes = ArticuloPDV.objects.filter(pdv=articulo.pdv, articulo=articulo.articulo).exclude(
            #         variante__isnull=True)
            context = {
                'articulo': articulo,
                # 'variantes': variantes,
                'pdv': pdv_id
            }

    return HttpResponse(template.render(context, request))


def pedido_detail(request, pedido_id):
    template = loader.get_template('landing/market/pdv/pedido-detail.html')
    context = {}

    if request.user.is_authenticated:
        if request.method == 'POST':
            pedido = Pedido.objects.get(id=pedido_id)
            context = {
                'pedido': pedido
            }
    return HttpResponse(template.render(context, request))


def tienda_online(request, articulo_id):
    if Articulo.objects.filter(id=articulo_id):
        articulo = Articulo.objects.get(id=articulo_id)
        response = HttpResponse("", status=302)
        response['Location'] = articulo.url
        print(response)
        return response


def get_qr(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        if id is not None and id != '':
            if ArticuloPDV.objects.filter(id=id):
                articulo = ArticuloPDV.objects.get(id=id)
                return JsonResponse(articulo.qr(), safe=False)
            else:
                return JsonResponse('', safe=False)
        else:
            return JsonResponse('', safe=False)


def add_carrito(request):
    print(request.POST)
    if request.user.is_authenticated:

        if request.method == 'POST':
            if not Carrito.objects.filter(user=request.user):
                Carrito.objects.create(user=request.user)
            carrito = Carrito.objects.get(user=request.user)

            # if request.POST.get('selected-variants') and request.POST.get('selected-variants') != '':
            #     variaciones = request.POST['selected-variants']
            #     variaciones = variaciones.replace("&quot;", "'")
            #     variaciones = variaciones.split(',')
            #     variantes = VarianteArticulo.objects.filter(id__in=variaciones)
            #
            #     for variacion in variantes:
            #         carrito_item = CarritoItem(variante=variacion, precio_original=variacion.precio_activo,
            #                                    precio_final=variacion.precio_activo, cantidad=variacion.stock)
            #         carrito_item.save()
            #         carrito.items.add(carrito_item)
            #     request.session['from'] = "add-carrito"
            #     return redirect('puntos-de-venta')


            if request.POST.get('articulo_id') and request.POST.get('articulo_id') != '':
                if request.POST.get('unidades-articulo-pdv') and request.POST.get('unidades-articulo-pdv') != '':
                    articulo = ArticuloPDV.objects.filter(id__in=request.POST.get('articulo_id')).first()
                    unidades = request.POST.get('unidades-articulo-pdv')
                    carrito_item = CarritoItem(articulo=articulo.articulo,
                                               precio_original=articulo.articulo.precio_activo,
                                               precio_final=articulo.articulo.precio_activo, cantidad=unidades)
                    carrito_item.save()
                    carrito.items.add(carrito_item)
                    request.session['from'] = "add-carrito"
                    return redirect('puntos-de-venta')

            else:
                return redirect('puntos-de-venta')
        else:
            if request.POST.get('articulo_id') and request.POST.get('pdv'):
                return articulo_detail(request, pdv_id=request.POST.get('pdv'),
                                       articulo_id=request.POST.get('articulo_id'))
            else:
                return redirect('puntos-de-venta')

    if request.POST.get('articulo_id') and request.POST.get('pdv'):
        return articulo_detail(request, pdv_id=request.POST.get('pdv'), articulo_id=request.POST.get('articulo_id'))
    else:
        return redirect('puntos-de-venta')


# comprueba que un articulo esta en una promocion como requisito
def check_in_promo(carrito):
    promo_valida = False
    for item in carrito.items.all():
        if item.articulo:
            if len(item.articulo.requeridos.all()) > 0:
                for promo in item.articulo.requeridos.all():
                    if promo.visible:
                        if promo.tipo == Promocion.RBJ:
                            carrito.promocion_asociada = promo
                            carrito.save()
                            promo_valida = True
                        elif promo.tipo == Promocion.PER:
                            carrito.promocion_asociada = promo
                            carrito.save()
                            promo_valida = True

        elif item.variante:
            if len(item.variante.articulo.requeridos.all()) > 0:
                for promo in item.variante.articulo.requeridos.all():
                    if promo.visible:
                        if promo.tipo == Promocion.RBJ:
                            carrito.promocion_asociada = promo
                            carrito.save()
                            promo_valida = True
                        elif promo.tipo == Promocion.PER:
                            carrito.promocion_asociada = promo
                            carrito.save()
                            promo_valida = True

    return promo_valida


def puntos_de_venta(request):
    template = loader.get_template('landing/market/pdv/puntos-de-venta.html')
    context = {}
    relaciones = []
    if request.session.get('from', None) == 'add-carrito':
        request.session['from'] = "pdv"
        messages.success(request, "Producto añadido al carrito")

    if request.user.is_authenticated:
        # Comprueba si tengo carrito y si no tengo crea uno
        if Carrito.objects.filter(user=request.user):
            carrito = Carrito.objects.get(user=request.user)

            if check_in_promo(carrito):
                if not carrito.apply_promo():
                    carrito.reset()
            else:
                carrito.reset()

        else:
            carrito = Carrito.objects.create(user=request.user)

        relaciones = get_relaciones(request.user)  # Devuelve los espacios/marcas relacionados con el usuario

        context = {
            'carrito': carrito,
            'relaciones': relaciones,

        }
    return HttpResponse(template.render(context, request))


def buscar_pdv(request):
    """Si el usuario que entra en el buscador es un espacio, recorre todas las propuestas en las que participa,
    y selecciona cada marca con la que tiene una propuesta"""
    template = loader.get_template('landing/market/pdv/buscar-pdv.html')
    context = {}

    if request.user.is_authenticated:
        user = request.user
        if request.method == 'GET':
            if len(user.espacio.all()) > 0:

                marcas = []
                for propuesta in user.emisor.all():
                    if len(propuesta.receptor.marca.all()) > 0:
                        print(propuesta.receptor.marca)
                        marcas.append(propuesta.receptor.marca.first())
                for propuesta in user.receptor.all():
                    if len(propuesta.emisor.marca.all()) > 0:
                        marcas.append(propuesta.emisor.marca.first())
                print(marcas)
                context = {
                    'marcas': marcas
                }

    return HttpResponse(template.render(context, request))


def search_pdvs(request):
    if request.method == 'POST':
        query = request.POST.get('q')
        marcas = request.POST.get('marcas[]')
        filters = Q()
        filters_p = Q()
        articulos = ''
        if query is not None:

            if query != '':
                filters &= Q(
                    articulo__nombre__icontains=query,
                ) | Q(articulo__ref__icontains=query)
                filters_p &= Q(
                    codigo__icontains=query
                )

            if marcas is not None and len(marcas) > 0:
                for id in marcas:
                    marca = Marca.objects.get(id=int(id))
                    propuestas = marca.user.emisor.all() | marca.user.receptor.all()

            else:
                propuestas = request.user.emisor.all() | request.user.receptor.all()

            for propuesta in propuestas:
                for pdv in propuesta.propuesta.all():
                    if articulos == '':
                        articulos = pdv.articulos.filter(filters).annotate(punto=F('pdv__id'))
                    else:
                        articulos = articulos | pdv.articulos.filter(filters)

            if articulos != '':
                articulos = articulos.annotate(nombre=F('articulo__nombre'), ref=F('articulo__ref'),
                                               precio_comparacion=F('articulo__precio_comparacion'),
                                               pvp=F('articulo__pvp'),
                                               imagen_principal=F('articulo__imagen_principal'))
                articulos = articulos.values()

            pedidos = Pedido.objects.filter(user=request.user).filter(filters_p).annotate(punto=F('pdv__id'))

            msg_list = list(articulos)
            msg_list2 = list(pedidos.values())
            result = []
            result.append(msg_list)
            result.append(msg_list2)

            print(result)

            return JsonResponse(result, safe=False)


def imprimir_qr(request, user_id, relacion_id):
    template = loader.get_template('landing/market/pdv/imprimir-qr.html')
    context = {}

    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            relacion = CustomUser.objects.get(id=relacion_id)
            if PropuestaComercial.objects.filter(emisor=user, receptor=relacion):
                propuesta = PropuestaComercial.objects.filter(emisor=user, receptor=relacion).first()
            elif PropuestaComercial.objects.filter(receptor=user, emisor=relacion):
                propuesta = PropuestaComercial.objects.filter(receptor=user, emisor=relacion).first()
            if propuesta is not None:
                pdv = propuesta.propuesta.all().first()
                articulos = pdv.articulos.all()

                context = {'articulos': articulos}
    return HttpResponse(template.render(context, request))


def actualizar_carrito(request):
    result = JsonResponse(False, safe=False)
    if request.method == 'POST':
        print(request.POST)

        if Carrito.objects.filter(user=request.user):
            carrito = Carrito.objects.get(user=request.user)

            if request.POST.get('codigo') and request.POST.get('codigo') != '':
                carrito.codigo = request.POST.get('codigo')

                if check_in_promo(carrito):
                    if carrito.apply_promo():
                        msg_list = carrito.json()
                        result = JsonResponse(msg_list, safe=False)
                    else:
                        carrito.reset()
                carrito.codigo = ''  # Una vez aplicado el descuento borramos el codigo para que no se aplique en bucle
                carrito.save()

            if request.POST.get('item') and request.POST.get('item') != '':

                if CarritoItem.objects.filter(id=request.POST.get('item')):
                    if request.POST.get('cantidad') and request.POST.get('cantidad') != '':
                        carrito_item = CarritoItem.objects.filter(id=request.POST.get('item')).first()
                        carrito_item.cantidad = request.POST.get('cantidad')
                        carrito_item.save()
                        if check_in_promo(carrito):
                            if not carrito.apply_promo():
                                carrito.reset()
                        else:
                            carrito.reset()
                        msg_list = carrito.json()
                        result = JsonResponse(msg_list, safe=False)

    return result


def pagar(request):
    template = loader.get_template('landing/market/carrito/pasarela-pago.html')
    context = {}

    if request.user.is_authenticated:

        if request.method == 'POST':
            if Carrito.objects.filter(user=request.user):
                carrito = Carrito.objects.get(user=request.user)
                context = {
                    'carrito': carrito,
                    'stripe': True
                }
        else:
            raise ValidationError("Petición no válida")

    return HttpResponse(template.render(context, request))


# Recibe los parametros del pago, tanto si es con stripe o no crea el pedido y realiza el pago
def charge(request):
    print(request.POST)
    template = loader.get_template('landing/market/carrito/pago-finalizado.html')
    context = {}

    if request.user.is_authenticated:

        if request.method == 'POST':
            carrito = Carrito.objects.get(user=request.user)
            pedido = Pedido.objects.create(user=request.user)

            if request.POST.get('stripeToken') and request.POST.get(
                    'stripeToken') != '':  # Si nos llega el token de stripe, hacemos el "charge" con el token

                try:
                    stripe.api_key = dev.STRIPE_SECRET_KEY  # todo substituir por la clave live
                    token = request.POST.get('stripeToken')
                    charge = stripe.Charge.create(
                        amount=round(carrito.total * 100, 0),
                        currency='eur',
                        description='KC- Pedido',
                        source=token,
                    )
                    # Si el charge ha ido bien, generamos el pedido y borramos el carrito

                    pedido.set_content(carrito)
                    messages.success(request, "Pedido realizado y pagado correctamente")

                except Exception as e:
                    messages.warning(request, "Error al realizar el pago, compruebe que los datos son correctos")

                    if pedido:
                        pedido.delete()

            elif request.POST.get('pago-prueba') and request.POST.get('pago-prueba') != '':  # Si no usamos stripe
                if request.POST.get('pago-prueba') == 'true':
                    pass  # todo que hacer si es un pago de prueba?
                else:
                    try:
                        pedido.set_content(carrito)
                        messages.success(request, "Pedido aceptado")

                    except Exception as e:
                        messages.warning(request, "Error al aceptar el pago")

                        if pedido:
                            pedido.delete()


            else:
                messages.warning(request, "Error al recibir la información, por favor inténtelo de nuevo")
                pedido.delete()

        else:
            raise ValidationError("Petición no válida")

    return HttpResponse(template.render(context, request))


def notificaciones_recibidas_pdv(request):
    template = loader.get_template('landing/market/pdv/notificaciones-recibidas-pdv.html')
    context = {}

    return HttpResponse(template.render(context, request))


def notificaciones_enviadas_pdv(request):
    template = loader.get_template('landing/market/pdv/notificaciones-enviadas-pdv.html')
    context = {}

    query_precios = Q(emisor=request.user) & Q(estado='PRECIOS')
    notif_precios = Notificacion.objects.filter(query_precios).all()

    query_envios = Q(emisor=request.user) & Q(estado='ENVIOS')
    notif_envios = Notificacion.objects.filter(query_envios).all()

    print(notif_precios)
    print(notif_envios)

    context = {
        'precios': notif_precios,
        'envios': notif_envios
    }

    return HttpResponse(template.render(context, request))


def relaciones_comerciales(request):
    context = {}
    view_from = ''

    if request.user.is_authenticated:
        query = Q(emisor=request.user)
        query.add(Q(receptor=request.user), Q.OR)

        propuestas = PropuestaComercial.objects.filter(query)
        propuestas_filter = PropuestaFilter(request.GET, queryset=propuestas)

        puntos = []
        queryset = request.user.emisor.all() | request.user.receptor.all()
        for punto in queryset:
            puntos.append(punto.propuesta.first())

        if '' in puntos:
            puntos = []

        query = Q(emisor=request.user)
        propuestas = PropuestaComercial.objects.filter(query)
        if request.method == 'POST':

            if request.POST.get("cancelar"):
                query = Q(username=request.POST.get("cancelar"))
                usuario = CustomUser.objects.filter(query).first()

                query3 = Q(emisor=request.user)
                query3.add(Q(receptor=usuario), Q.AND)
                propuesta = PropuestaComercial.objects.filter(query3).first()
                if propuesta:
                    propuesta.delete()
                    messages.success(request, "Propuesta borrada con éxito.")
            if request.POST.get("rechazar"):
                query = Q(username=request.POST.get("rechazar"))
                usuario = CustomUser.objects.filter(query).first()

                query3 = Q(emisor=usuario)
                query3.add(Q(receptor=request.user), Q.AND)
                propuesta = PropuestaComercial.objects.filter(query3).first()
                if propuesta:
                    propuesta.delete()
                    messages.success(request, "Propuesta rechazada con éxito.")
            if request.POST.get("aceptar"):
                query = Q(username=request.POST.get("aceptar"))
                usuario = CustomUser.objects.filter(query).first()

                query3 = Q(emisor=usuario)
                query3.add(Q(receptor=request.user), Q.AND)
                propuesta = PropuestaComercial.objects.filter(query3).first()

                query_propuesta2 = Q(emisor=request.user) & Q(receptor=usuario)
                propuesta2 = PropuestaComercial.objects.filter(query_propuesta2).first()

                if propuesta2:
                    propuesta = propuesta2
                if propuesta:
                    propuesta.estado = 'PREACEPTADA'

                    pdv = PuntoDeVenta()
                    pdv.propuesta = propuesta

                    query = Q(propuesta=propuesta)
                    pdvexiste = PuntoDeVenta.objects.filter(query)
                    if pdvexiste:
                        messages.warning(request, "Ya existe un punto de venta para esta propuesta.")
                    else:

                        pdv.nombre = "pdv-" + propuesta.emisor.username + "-" + propuesta.receptor.username
                        pdv.save()
                        propuesta.save()

                        messages.success(request, "Propuesta aceptada con éxito.")
                        return redirect('relaciones-comerciales')

            if request.POST.get("aceptar_pdv"):
                query = Q(id=request.POST.get("aceptar_pdv"))
                punto = PuntoDeVenta.objects.filter(query).first()

                if punto:
                    if request.user.is_marca:
                        punto.validado_marca = True
                        punto.save()
                        messages.success(request,
                                         "Punto de venta validado con éxito. "
                                         "Quedas a la espera de que el espacio lo valide.")
                        return redirect('relaciones-comerciales')
                    elif request.user.is_espacio:
                        punto.validado_espacio = True
                        punto.activo = True

                        mensaje = ""

                        colec = punto.colecciones.all()
                        for col in colec:
                            query_stock = Q(coleccion=col)
                            articulos = ArticuloPDV.objects.filter(query_stock).all()

                            for articulo_pdv in articulos:
                                mensaje += articulo_pdv.articulo.nombre + " -> " + str(articulo_pdv.cantidad)\
                                           + " unidades.\n"

                        noti = Notificacion()
                        noti.fecha = datetime.date.today()
                        noti.receptor = request.user
                        noti.tipo = 'ENVIOS'
                        if punto.propuesta.emisor == request.user:
                            noti.emisor = punto.propuesta.receptor
                        else:
                            noti.emisor = punto.propuesta.emisor
                        noti.titulo = 'VALIDACIÓN STOCK'
                        noti.contenido = "ARTICULOS PARA CORNER:\n" + \
                                         articulo_pdv.articulo.nombre + " -> " + str(articulo_pdv.cantidad)\
                                         + " unidades.\n" + mensaje

                        noti.save()
                        punto.save()

                        messages.success(request,
                                         "Punto de venta validado con éxito.")
                        return redirect('relaciones-comerciales')

            if request.POST.get("cancelar_pdv"):
                query = Q(id=request.POST.get("cancelar_pdv"))
                punto = PuntoDeVenta.objects.filter(query).first()

                if punto:
                    punto.delete()
                    punto.propuesta.delete()
                    messages.success(request, "Punto de venta descartado con éxito.")
                    return redirect('relaciones-comerciales')
        context = {
            'puntos': puntos,
            'propuestas': propuestas,
            'propuestas_filter': propuestas_filter,
            'request.user': request.user,
            'view_from': view_from
        }

    return render(request, 'landing/market/rc/relaciones-comerciales.html', context)


# Esta función desaparecerá cuando lo hagamos por JavaScript
# TODO eliminar esta función y hacerla por JavaScript
def relac_comer_2(request):
    return render(request, 'landing/market/rc/relac-comer-2.html')


"""
    Policy & Cookies
"""


def policy(request):
    return render(request, 'landing/policy.html')


def cookies(request):
    return render(request, 'landing/cookies.html')


"""
    Esta seccion es para revisar
"""


def public_validado(request):
    template = loader.get_template('landing/public/perfil-kradeler.html')

    context = {}
    form_alquiler = ''
    colecciones = []

    if request.user.is_authenticated:

        if not request.user.validado:
            messages.warning(request, "Tu perfil no está validado por lo que no puedes acceder a perfil-kradeler.")
            return redirect('mi-perfil')
        else:
            user = get_object_or_404(CustomUser, pk=request.user.id)
            galeria = GaleriaUsuario.objects.filter(user=request.user)
            comentarios = user.para_mi.all()
            puntuacion = False

            if MiPerfil.objects.filter(user=request.user):
                perfil_user = MiPerfil.objects.get(user=request.user)
                puntuacion = perfil_user.puntuacion
            else:
                perfil_user = False
            if Empresa.objects.filter(user=request.user):
                user_empresa = Empresa.objects.get(user=request.user)
            else:
                user_empresa = False

            if request.method == 'GET':
                form = PublicUserForm(instance=user)

                # Si hay una empresa la pasamos al formulario
                if perfil_user and user_empresa:
                    form_perfil = MiPerfilForm(instance=perfil_user)

                    # Si la empresa es un espacio y tiene un alquiler lo cargamos en el formulario de alquiler
                    if perfil_user.is_espacio:
                        if Alquiler.objects.filter(empresa=user_empresa):
                            alquiler = Alquiler.objects.get(empresa=user_empresa)
                            form_alquiler = AlquilerForm(instance=alquiler)
                        else:
                            form_alquiler = AlquilerForm()

                    # Si es marca obtenemos sus colecciones de articulos
                    elif perfil_user.is_marca:
                        colecciones = Coleccion.objects.filter(empresa=user_empresa)
                    else:
                        pass
                else:
                    form_perfil = MiPerfilForm()

                    if not user_empresa:
                        messages.warning(request,
                                         "No existe una empresa para este usuario. Por favor, créala en Mi Cuenta"
                                         " para poder completar tu perfil correctamente.")

                if user_empresa:
                    form_empresa = RazonSocialForm(instance=user_empresa)
                else:
                    form_empresa = ''

            else:
                form = PublicUserForm(request.POST, instance=user)

                if perfil_user:
                    form_perfil = MiPerfilForm(request.POST, instance=perfil_user)

                    if perfil_user.is_espacio:

                        if Alquiler.objects.filter(empresa=user_empresa):
                            alquiler = Alquiler.objects.get(empresa=user_empresa)
                            form_alquiler = AlquilerForm(request.POST, instance=alquiler)
                        else:
                            form_alquiler = AlquilerForm(request.POST)

                    elif perfil_user.is_marca:
                        pass
                    else:
                        pass

                else:
                    form_perfil = MiPerfilForm(request.POST)

                if user_empresa:
                    form_empresa = RazonSocialForm(request.POST, instance=user_empresa)
                else:
                    form_empresa = ''

                if form.is_valid() and form_perfil.is_valid():
                    form.save()
                    new_perfil = form_perfil.save(commit=False)
                    new_perfil.user = request.user
                    new_perfil.save()

                    if perfil_user and perfil_user.is_espacio:
                        if form_alquiler != '' and form_alquiler.is_valid():
                            new_alquiler = form_alquiler.save(commit=False)
                            new_alquiler.empresa = user_empresa
                            form_alquiler.save()
                        else:
                            print('Error en el formulario')
                            messages.warning(request, form_alquiler.errors)

                    if user_empresa:
                        if form_empresa.is_valid():
                            form_empresa.save()
                        else:
                            print('Error en el formulario')
                            messages.warning(request, form_empresa.errors)

                    print('La información se ha guardado correctamente')
                    messages.success(request, 'La información se ha guardado correctamente')
                else:
                    print('Error en el formulario')

                    messages.warning(request, form.errors)

            context = {
                'form': form,
                'galeria': galeria,
                'comentarios': comentarios,
                'form_perfil': form_perfil,
                'form_alquiler': form_alquiler,
                'form_empresa': form_empresa,
                'colecciones': colecciones,
                'puntuacion': puntuacion if puntuacion else False
            }

        return HttpResponse(template.render(context, request))


def buscar(request):
    usuarios = []
    if request.user.is_authenticated:
        if request.method == 'GET':
            if request.GET.get('query') and request.GET.get('query') != '':
                query = request.GET.get('query')
                usuarios = CustomUser.objects.filter(
                    Q(sobre_mi_negocio__icontains=query) | Q(username__icontains=query))

    return render(request, 'landing/buscar.html', {'usuarios': usuarios})


def conexion(request):
    template = loader.get_template('landing/empresa/conexion/conexion.html')

    query = Q(emisor=request.user)
    query.add(Q(estado='PENDIENTE'), Q.AND)
    enviadas = Conexion.objects.filter(query)

    query2 = Q(receptor=request.user)
    query2.add(Q(estado='PENDIENTE'), Q.AND)
    recibidas = Conexion.objects.filter(query2)

    query3 = Q(receptor=request.user)
    query3.add(Q(estado='ACEPTADA'), Q.AND)
    aceptadas_receptor = Conexion.objects.filter(query3)

    query4 = Q(emisor=request.user)
    query4.add(Q(estado='ACEPTADA'), Q.AND)
    aceptadas_emisor = Conexion.objects.filter(query4)

    context = {
        'enviadas': enviadas,
        'recibidas': recibidas,
        'aceptadas_receptor': aceptadas_receptor,
        'aceptadas_emisor': aceptadas_emisor,
    }

    if request.method == 'POST':
        if request.POST.get("aceptar"):
            query = Q(username=request.POST.get("aceptar"))
            usuario = CustomUser.objects.filter(query).first()

            query3 = Q(receptor=request.user)
            query3.add(Q(emisor=usuario), Q.AND)
            conec = Conexion.objects.filter(query3).first()
            if conec:
                conec.estado = 'ACEPTADA'
                conec.save()
        elif request.POST.get("rechazar"):
            query = Q(username=request.POST.get("rechazar"))
            usuario = CustomUser.objects.filter(query).first()

            query3 = Q(receptor=request.user)
            query3.add(Q(emisor=usuario), Q.AND)
            conec = Conexion.objects.filter(query3).first()
            if conec:
                conec.delete()
        elif request.POST.get("cancelar"):
            query = Q(username=request.POST.get("cancelar"))
            usuario = CustomUser.objects.filter(query).first()

            query3 = Q(receptor=usuario)
            query3.add(Q(emisor=request.user), Q.AND)
            conec = Conexion.objects.filter(query3).first()
            if conec:
                conec.delete()

    return HttpResponse(template.render(context, request))


def mis_contactos(request):
    template = loader.get_template('landing/empresa/conexion/mis-contactos.html')

    query_conexiones = Q(emisor=request.user) & Q(estado='ACEPTADA')
    query_conexiones.add(Q(receptor=request.user) & Q(estado='ACEPTADA'), Q.OR)

    conexiones = Conexion.objects.filter(query_conexiones)

    context = {
        'conexiones': conexiones,
    }

    return HttpResponse(template.render(context, request))


def confirmar_pedido(request):
    template = loader.get_template('landing/market/pdv/confirmar-pedido.html')
    context = {}

    # Punto realmente se cargaría a través de un parámetro y una consulta por nombre/id
    punto = PuntoDeVenta.objects.filter().first()

    coleccciones = punto.colecciones.all()
    for col in coleccciones:
        query_stock = Q(coleccion=col)
        articulos = ArticuloPDV.objects.filter(query_stock).all()

        for articulo_pdv in articulos:
            mensaje = articulo_pdv.articulo.nombre + " -> " + str(articulo_pdv.cantidad) + " unidades.\n"

    if request.method == 'POST':
        unidades = request.POST.get("validar-pedido")

        noti = Notificacion()
        noti.fecha = datetime.date.today()
        noti.emisor = request.user
        noti.tipo = 'ENVIOS'
        if punto.propuesta.emisor == request.user:
            noti.receptor = punto.propuesta.receptor
        else:
            noti.receptor = punto.propuesta.emisor
        noti.titulo = 'VALIDACIÓN PEDIDO'
        noti.contenido = "HAN LLEGADO \n" + unidades

        noti.save()
        print("POST")

    context = {
        'colecciones': coleccciones,
    }

    return HttpResponse(template.render(context, request))


def planes_premium(request):
    template = loader.get_template('landing/planespremium.html')

    context = {}

    return HttpResponse(template.render(context, request))

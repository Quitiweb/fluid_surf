from django.urls import include
from django.urls import path

from . import views
from qr_code import urls as qr_code_urls

urlpatterns = [
    path('premium', views.premium, name='premium'),
    path('planespremium', views.planes_premium, name='planespremium'),
    path('buscar', views.buscar, name='buscar'),

    # Mi perfil
    path('mi-perfil', views.mi_perfil, name='mi-perfil'),
    path('perfil-kradeler', views.public_validado, name='perfil-kradeler'),
    # A pesar de estar entre funciones del market, añado aquí el perfil con la nueva url
    # por lo que ha dicho Rafa, que puede ser más cómodo para, por ejemplo, compartir enlaces de usuarios.
    path('perfil-kradeler/<user>', views.perfil_kradeler_market, name='perfil-kradeler-market'),
    path('perfil-kradeler/unavailable', views.perfil_kradeler_unavailable, name='perfil-kradeler-unavailable'),

    # Mi empresa
    path('mi-cuenta', views.mi_cuenta_redirect, name='mi-cuenta'),
    path('mi-cuenta/tab<int:tab>', views.mi_cuenta, name='mi-cuenta'),
    path('mi-espacio', views.mi_espacio, name='mi-espacio'),
    path('mi-catalogo', views.mi_catalogo, name='mi-catalogo'),
    path('marca-espacio', views.marca_espacio, name='marca-espacio'),
    path('add-categoria', views.add_categoria, name='add-categoria'),
    path('edit-categoria', views.edit_categoria, name='edit-categoria'),
    path('delete-categoria', views.delete_categoria, name='delete-categoria'),
    path('search-item-promo', views.search_item_promo, name='search-item-promo'),
    path('query-item-promo', views.query_item_promo, name='query-item-promo'),
    path('conexion', views.conexion, name='conexion'),
    path('mis-contactos', views.mis_contactos, name='mis-contactos'),
    path('proximos-descuentos', views.proximos_descuentos, name='proximos-descuentos'),
    path('descuentos-anteriores', views.proximos_descuentos, name='descuentos-anteriores'),
    path('guardar-promo', views.guardar_promo, name='guardar-promo'),
    path('promo-detail/<promo_id>', views.promo_detail, name='promo-detail'),

    #Articulos
    path('add-item', views.add_item, name='add-item'),
    path('edit-item', views.single_item_edit, name='edit-item'),
    path('search-item', views.search_item, name='search-item'),
    path('edit-items', views.edit_items, name='edit-items'),
    path('delete-items', views.delete_items, name='delete-items'),
    path('import-file', views.import_file, name='import-file'),

    # Colecciones
    path('coleccion/<coleccion_id>', views.coleccion, name='coleccion'),
    path('search/<coleccion_id>', views.search_item_col, name='search-item-col'),
    path('colecciones/', views.colecciones, name='colecciones'),
    path('toggle-visible-col/', views.toggle_visible_col, name='toggle-visible-col'),
    path('colecciones-visibles/<pdv_id>', views.colecciones_visibles, name='colecciones-visibles'),
    path('editar-stock/<coleccion_id>/<pdv_id>', views.editar_stock, name='editar-stock'),

    # Mi Kradleco market
    path('market', views.market, name='market'),
    path('market/propuesta/<user>', views.propuesta, name='market/propuesta'),
    path('puntos-de-venta', views.puntos_de_venta, name='puntos-de-venta'),
    path('confirmar-pedido', views.confirmar_pedido, name='confirmar-pedido'),
    path('relaciones-comerciales', views.relaciones_comerciales, name='relaciones-comerciales'),
    path('scanner', views.scanner, name='scanner'),
    path('articulo-detail/<pdv_id>/<articulo_id>', views.articulo_detail, name='articulo-detail'),
    path('buscar-pdv', views.buscar_pdv, name='buscar-pdv'),
    path('search-pdvs', views.search_pdvs, name='search-pdvs'),
    path('pedido-detail/<pedido_id>', views.pedido_detail, name='pedido-detail'),
    path('tienda-online/<articulo_id>', views.tienda_online, name='tienda-online'),
    path('get-qr', views.get_qr, name='get-qr'),
    path('imprimir-qr/<user_id>/<relacion_id>', views.imprimir_qr, name='imprimir-qr'),
    path('qr_code', include(qr_code_urls, namespace="qr_code")),

    # Carrito y pagos
    path('actualizar-carrito', views.actualizar_carrito, name='actualizar-carrito'),
    path('pagar', views.pagar, name='pagar'),
    path('charge', views.charge, name='charge'),
    path('add-carrito', views.add_carrito, name='add-carrito'),

    path('notificaciones-enviadas-pdv', views.notificaciones_enviadas_pdv, name='notificaciones-enviadas-pdv'),
    path('notificaciones-recibidas-pdv', views.notificaciones_recibidas_pdv, name='notificaciones-recibidas-pdv'),

    # todo Esta función desaparecerá cuando lo hagamos por JavaScript
    path('relac-comer-2', views.relac_comer_2, name='relac-comer-2'),

    # Policy & Cookies
    path('policy', views.policy, name='policy'),
    path('cookies', views.cookies, name='cookies'),
]

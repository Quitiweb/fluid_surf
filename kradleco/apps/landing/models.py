import datetime
from django.db import models
from django.db.models.signals import m2m_changed

from django.template.defaultfilters import slugify, upper
from django.utils.crypto import get_random_string
from django.utils.timezone import now

from ..users.models import CustomUser, Empresa

EMAIL_MAX_LENGTH = 80
NOMBRE_MAX_LENGTH = 100
TITLE_MAX_LENGTH = 200
DESCRIP_MAX_LENGTH = 500
TAG_MAX_LENGTH = 15
CODE_LENGHT = 15


def upload_to_articulos(instance, filename):
    try:
        return 'img/articulos/%s' % instance.articulo.id + '/' + filename
    except Exception as e:
        return 'img/articulos/%s' % instance.id + '/' + filename


class Target(models.Model):
    MUJER = 'MUJER'
    HOMBRE = 'HOMBRE'
    NIÑOS = 'NIÑOS'
    ADOL = 'ADOLESCENTES'
    ADUL = 'ADULTOS'

    TARGET = (
        (MUJER, 'Mujer'),
        (HOMBRE, 'Hombre'),
        (NIÑOS, 'Niños'),
        (ADOL, 'Adolescentes'),
        (ADUL, 'Adultos'),
    )

    target = models.CharField(
        max_length=15,
        choices=TARGET,
        default=MUJER,
    )

    class Meta:
        verbose_name_plural = 'Target'

    def __str__(self):
        return str(self.target)


class EstiloVida(models.Model):
    ECO = 'ECOLOGICO'
    CLA = 'CLASICO'
    AVE = 'AVENTURERO'
    SPT = 'SPORT'
    BOH = 'BOHEMIO'

    ESTILO_DE_VIDA = (
        (ECO, 'Nature/Ecológico/Medio-ambiente'),
        (CLA, 'Conservador/Clásico'),
        (AVE, 'Riesgo/Avengura/Viajero'),
        (SPT, 'Fitness/Sport'),
        (BOH, 'Bohemio'),
    )

    estilo = models.CharField(
        max_length=35,
        choices=ESTILO_DE_VIDA,
        default=ECO,
    )

    class Meta:
        verbose_name_plural = 'Estilo'

    def __str__(self):
        return str(self.estilo)


class Mercado(models.Model):
    TEXTIL = 'TEXTIL'
    CAL = 'CALZADO'
    COMP = 'COMPLEMENTOS'
    MAQ = 'MAQUILLAJE'
    COSM = 'COSMETICA'
    PERF = 'PERFUMERIA'
    OTRO = 'OTRO'

    MERCADO = (
        (TEXTIL, 'Textil'),
        (CAL, 'Calzado'),
        (COMP, 'Complementos'),
        (MAQ, 'Maquillaje'),
        (COSM, 'Cosmética'),
        (PERF, 'Perfumería'),
        (OTRO, 'Otro'),
    )

    mercado = models.CharField(
        max_length=15,
        choices=MERCADO,
        default=TEXTIL,
    )

    class Meta:
        verbose_name_plural = 'Mercado'

    def __str__(self):
        return str(self.mercado)


class Servicios(models.Model):
    FAB = 'FABRICACION'
    OBRAS = 'OBRAS'
    SOFT = 'SOFTWARE'
    GEST = 'GESTORIAS'
    FINAN = 'FINANCIACION'
    MARK = 'MARKETING'
    INFLUEN = 'INFLUENCERS'
    CONSUL = 'CONSULTORIA'
    ASOC = 'ASOCIACIONES'
    INFO = 'INFORMACION'

    SERVICIOS = (
        (FAB, 'Fabricación, Confección, Packaging'),
        (OBRAS, 'Obras, Logística, Almacén'),
        (SOFT, 'Software, Hardware, Comunicaciones'),
        (GEST, 'Gestorías, Seguros, Abogados'),
        (FINAN, 'Financiación, Bancos'),
        (MARK, 'Marketing, Eventos'),
        (INFLUEN, 'Influencers, Ventas'),
        (CONSUL, 'Consultoría, Asesoramiento'),
        (ASOC, 'Asociaciones, Instituciones'),
        (INFO, 'Información, Noticias'),
    )

    servicios = models.CharField(
        max_length=50,
        choices=SERVICIOS,
        default=FAB,
    )

    class Meta:
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return str(self.servicios)


class Maestro(models.Model):
    mercado = models.ManyToManyField(Mercado, blank=True)
    target = models.ManyToManyField(Target, blank=True)
    estilo = models.ManyToManyField(EstiloVida, blank=True)

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )


class Solicitud(models.Model):
    MARCA = 'MARCA'
    ESPACIO = 'ESPACIO'
    SERVICIO = 'SERVICIO'

    TYPE = (
        (MARCA, 'Marca'),
        (ESPACIO, 'Espacios (Offline/Online)'),
        (SERVICIO, 'Servicio'),
    )

    quien_eres = models.CharField(
        max_length=10,
        choices=TYPE,
        default=MARCA,
    )

    servicios = models.ManyToManyField(Servicios)

    mercado = models.ManyToManyField(Mercado)

    target = models.ManyToManyField(Target)

    estilo = models.ManyToManyField(EstiloVida)

    que_buscas = models.CharField(
        max_length=10,
        choices=TYPE,
        default=ESPACIO,
    )

    email = models.EmailField(max_length=EMAIL_MAX_LENGTH)
    nombre = models.CharField(max_length=NOMBRE_MAX_LENGTH)

    class Meta:
        verbose_name_plural = 'Solicitudes'

    def __str__(self):
        return str(self.nombre) + ' - ' + self.quien_eres + ' - ' + self.email


class Categoria(models.Model):
    nombre = models.CharField(max_length=40)
    categoria_padre = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategorias'
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return ('/' + self.categoria_padre.nombre + ' - ' if self.categoria_padre else ' / ') + self.nombre

    def json(self):
        subcategorias = []
        for sub in self.subcategorias.all():
            subcategorias.append({
                'id': sub.id,
                'nombre': sub.nombre
            })
        json = {
            'id': self.id,
            'nombre': self.nombre,
            'sub': subcategorias
        }
        return json


class DefinicionVariante(models.Model):
    tag = models.CharField(max_length=TAG_MAX_LENGTH)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='variantes'
    )

    def __str__(self):
        return str(self.tag)


class Articulo(models.Model):
    url = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    ref = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    nombre = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    descripcion = models.CharField(max_length=DESCRIP_MAX_LENGTH)
    pvp = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True)
    precio_coste = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True)
    precio_comparacion = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True)
    imagen_principal = models.ImageField(upload_to=upload_to_articulos, blank=True)
    stock = models.IntegerField(default=0, blank=True)
    marca = models.CharField(max_length=20, blank=True, null=True)

    variantes = models.ManyToManyField(DefinicionVariante, blank=True)
    mercado = models.ManyToManyField(Mercado, blank=True)
    target = models.ManyToManyField(Target, blank=True)

    handle = models.CharField(default='-', max_length=20, blank=True,
                              null=True)  # Parámetro necesario para la importación desde archivos

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='artcategorias'
    )
    subcategoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='artsubcategorias'
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'Artículos'

    def save(self, *args, **kwargs):
        if(self.handle == '-'):
            self.handle=slugify(self.nombre)
        if Articulo.objects.filter(handle=self.handle):
            print("no se ha guardado porque ya existe un articulo con ese atributo handle")
            return False
        else:
            super(Articulo, self).save(*args, **kwargs)
            return True

    def __str__(self):
        return self.ref + ' - ' + str(self.nombre)

    @property
    def precio_activo(self):
        return self.precio_comparacion if self.precio_comparacion != 0 else self.pvp

    @property
    def descuento(self):
        if self.precio_comparacion != 0:
            return round(((self.pvp - self.precio_comparacion) * 100) / self.pvp, 0)
        else:
            return 0;

    def qr(self):
        json = {"id": self.id,
                'tipo': 'articulo'}
        return json


class VarianteArticulo(models.Model):
    opcion_1 = models.CharField(max_length=TAG_MAX_LENGTH, null=True, blank=True)
    opcion_1_value = models.CharField(max_length=TAG_MAX_LENGTH, null=True, blank=True)
    opcion_2 = models.CharField(max_length=TAG_MAX_LENGTH, null=True, blank=True)
    opcion_2_value = models.CharField(max_length=TAG_MAX_LENGTH, null=True, blank=True)
    opcion_3 = models.CharField(max_length=TAG_MAX_LENGTH, null=True, blank=True)
    opcion_3_value = models.CharField(max_length=TAG_MAX_LENGTH, null=True, blank=True)

    url = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    ref = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    pvp = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True)
    precio_coste = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True)
    precio_comparacion = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True)
    imagen_principal = models.ImageField(upload_to=upload_to_articulos, blank=True)
    stock = models.IntegerField(default=0, blank=True)

    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.CASCADE,
        related_name="variantearticulo"
    )

    class Meta:
        unique_together = (
            ('opcion_1', 'opcion_1_value', 'opcion_2', 'opcion_2_value', 'opcion_3', 'opcion_3_value', 'articulo'),)

    def __str__(self):
        return self.get_variantes() + ' ' + self.articulo.nombre

    @property
    def precio_activo(self):
        return self.precio_comparacion if self.precio_comparacion != 0 else self.pvp

    @property
    def descuento(self):
        if self.precio_comparacion != 0:
            return round(((self.pvp - self.precio_comparacion) * 100) / self.pvp, 0)
        else:
            return 0;

    def get_variantes(self):
        return (self.opcion_1 if self.opcion_1 else '') + ':' + (
            self.opcion_1_value if self.opcion_1_value else '') + ' / ' + (
                   self.opcion_2 if self.opcion_2 else '') + ':' + (
                   self.opcion_2_value if self.opcion_2_value else '') + ' / ' + (
                   self.opcion_3 if self.opcion_3 else '') + ':' + (
                   self.opcion_3_value if self.opcion_3_value else '')

    def get_variantes_values(self):
        return (
                   self.opcion_1_value if self.opcion_1_value else '') + (
                   ':' + self.opcion_2_value if self.opcion_2_value else '') + (
                   ':' + self.opcion_3_value if self.opcion_3_value else ''
               )

    def qr(self):
        json = {"id": self.id,
                'tipo': 'variante'}
        return json


class GaleriaArticulo(models.Model):
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.CASCADE, related_name="galeria"
    )
    imagen = models.ImageField(upload_to=upload_to_articulos, blank=True)

    def save(self, *args, **kwargs):
        if not self.articulo.imagen_principal:
            self.articulo.imagen_principal = self.imagen
            self.articulo.save()

        super(GaleriaArticulo, self).save(*args, **kwargs)


class Coleccion(models.Model):
    nombre = models.CharField(max_length=50, default='Coleccion')
    visible = models.BooleanField(default=True)
    articulos = models.ManyToManyField(Articulo, related_name='articulos')

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='colecciones'
    )

    class Meta:
        verbose_name_plural = 'Colecciones'

    def __str__(self):
        return self.nombre


class Alquiler(models.Model):
    descripcion = models.CharField(max_length=50, default='', blank=True)
    euros_dia = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    euros_semana = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    euros_mes = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'Alquileres'

    def __str__(self):
        return self.descripcion


class Marca(models.Model):
    direccion = models.CharField(default="", max_length=100, blank=True)
    is_online = models.BooleanField(default=False, blank=True)
    is_mayorista = models.BooleanField(default=False, blank=True)
    is_marketplaces = models.BooleanField(default=False, blank=True)

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='marca',
    )


class Espacio(models.Model):
    id = models.AutoField(primary_key=True)
    is_distribuidor = models.BooleanField(default=False, blank=True)
    is_propia_marca = models.BooleanField(default=False, blank=True)
    is_propietario = models.BooleanField(default=False, blank=True)
    is_nuevo = models.BooleanField(default=False, blank=True)

    direccion = models.CharField(default="", blank=True, max_length=50)
    tags = models.CharField(default="", blank=True, max_length=50)
    precio_dia = models.IntegerField(default=0, blank=True)
    precio_semana = models.IntegerField(default=0, blank=True)
    precio_mes = models.IntegerField(default=0, blank=True)
    tiempo_minimo = models.CharField(default="", max_length=50)
    metros_disponibles = models.CharField(default="", max_length=50, null=True, blank=True)
    ventas = models.IntegerField(default=0, blank=True)
    negociable = models.BooleanField(default=False, blank=True)

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='espacio',
    )

    def __str__(self):
        return str(self.id)


class PropuestaComercial(models.Model):
    LEVE = 'LEVE'
    ESTRICTA = 'ESTRICTA'

    PENDIENTE = 'PENDIENTE'
    PREACEPTADA = 'PREACEPTADA'
    CANCELADA = 'CANCELADA'

    POLITICA = (
        (LEVE, 'Leve'),
        (ESTRICTA, 'Estricta'),
    )

    ESTADOS = (
        (PENDIENTE, 'Pendiente'),
        (PREACEPTADA, 'Preaceptada'),
        (CANCELADA, 'Cancelada'),
    )

    estado = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default=PENDIENTE
    )

    modificaciones_receptor = models.IntegerField(default=0)

    nombre = models.CharField(max_length=75, default='propuesta')

    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()

    precio_dia = models.FloatField(default=0, null=True)
    precio_semana = models.FloatField(default=0, null=True)
    precio_mes = models.FloatField(default=0, null=True)

    precio_total = models.FloatField(default=0, blank=True)

    porcentaje_ventas = models.FloatField()

    is_acepta_propuestos = models.BooleanField(default=False, blank=True)

    precio_dia_propuesto = models.FloatField(default=0, null=True)
    precio_semana_propuesto = models.FloatField(default=0, null=True)
    precio_mes_propuesto = models.FloatField(default=0, null=True)
    precio_total_propuesto = models.FloatField(default=0, null=True)
    porcentaje_ventas_propuesto = models.FloatField(default=0)

    politica_cancelacion_m = models.CharField(
        max_length=15,
        choices=POLITICA,
        default=LEVE
    )

    politica_cancelacion_e = models.CharField(
        max_length=15,
        choices=POLITICA,
        default=LEVE
    )

    metros_cuadrados = models.FloatField(default=0.0, blank=True, null=True)

    is_necesita_mobiliario = models.BooleanField(default=False)

    comentarios = models.CharField(max_length=100, default="")

    emisor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='emisor',
        default="",
        null=True
    )

    receptor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='receptor',
        default="",
        null=True
    )

    is_cancelada = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Propuestas Comerciales'

    def __str__(self):
        return str(self.nombre)


class PuntoDeVenta(models.Model):
    nombre = models.CharField(max_length=50, default='punto de venta')
    fecha_inicio = models.DateField(default=now, blank=True)
    colecciones = models.ManyToManyField(Coleccion, blank=True)

    propuesta = models.ForeignKey(
        PropuestaComercial,
        on_delete=models.CASCADE,
        related_name='propuesta',
        default="",
        null=True
    )

    validado_marca = models.BooleanField(default=False)
    validado_espacio = models.BooleanField(default=False)

    activo = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Puntos de Venta'

    def __str__(self):
        return str(self.nombre)


class Notificacion(models.Model):
    emisor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="notificacion_emisor",
        default="",
        null=True
    )

    receptor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="notificacion_receptor",
        default="",
        null=True
    )

    PRECIOS = 'PRECIOS'
    ENVIOS = 'ENVIOS'

    TIPOS = (
        (PRECIOS, 'Precios'),
        (ENVIOS, 'Envios'),
    )

    estado = models.CharField(
        max_length=15,
        choices=TIPOS,
        default=PRECIOS
    )

    titulo = models.CharField(max_length=25)
    contenido = models.TextField(max_length=500)

    fecha = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.titulo)


class ArticuloPDV(models.Model):
    coleccion = models.ForeignKey(Coleccion, on_delete=models.CASCADE, related_name='coleccion_en_pdv')
    pdv = models.ForeignKey(PuntoDeVenta, on_delete=models.CASCADE, related_name='articulos')
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='en_pdv', blank=True, null=True)
    variante = models.ForeignKey(VarianteArticulo, on_delete=models.CASCADE, related_name='en_pdv', blank=True,
                                 null=True)
    cantidad = models.IntegerField(default=0)

    def qr(self):
        json = {"id": self.id,
                "pdv": self.pdv_id,
                "tipo": "articulo"}
        return json


class Conexion(models.Model):
    emisor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='emisor_conexion',
        default="",
        null=True
    )

    receptor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='receptor_conexion',
        default="",
        null=True
    )

    PENDIENTE = 'PENDIENTE'
    ACEPTADA = 'ACEPTADA'
    CANCELADA = 'CANCELADA'

    ESTADOS = (
        (PENDIENTE, 'Pendiente'),
        (ACEPTADA, 'Aceptada'),
        (CANCELADA, 'Cancelada'),
    )

    estado = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default=PENDIENTE
    )

    class Meta:
        verbose_name_plural = 'Conexiones'

    def __str__(self):
        return str(self.emisor) + " - " + str(self.receptor)


class Promocion(models.Model):
    RBJ = 'RBJ'
    PER = 'PER'
    EUR = 'EUR'
    UD = 'UD'
    PCT = 'PCT'
    EMPTY = ''
    CLI = 'CLI'
    EXS = 'EXS'

    PROMOCION_CHOICES = (
        (RBJ, 'Rebaja'),
        (PER, 'Personalizada'),
    )

    REQUISITOS_CHOICES = (
        (EMPTY, '-Sin requisito-'),
        (EUR, 'Euros'),
        (UD, 'Unidades')
    )

    RECOMPENSA_CHOICES = (
        (EMPTY, '-Sin requisito-'),
        (EUR, 'Euros'),
        (UD, 'Unidades'),
        (PCT, 'Porcentaje'),
    )

    LIMITE_CHOICES = (
        (EXS, 'Existencias'),
        (CLI, 'Clientes')
    )

    texto = models.TextField(max_length=100, blank=True)
    nombre = models.CharField(max_length=30, blank=True)
    canjeos = models.IntegerField(default=0, blank=True)
    automatica = models.BooleanField(default=False)
    codigo = models.BooleanField(default=False)
    codigo_value = models.SlugField(max_length=CODE_LENGHT, unique=True, blank=True, null=True)
    tipo = models.CharField(
        max_length=15,
        choices=PROMOCION_CHOICES,
        default=RBJ
    )
    articulos_obtiene = models.ManyToManyField(Articulo, related_name='promocionados', blank=True)
    articulos_compra = models.ManyToManyField(Articulo, related_name='requeridos', blank=True)

    requisito = models.CharField(
        max_length=15,
        choices=REQUISITOS_CHOICES,
        default=EMPTY
    )
    requisito_value = models.IntegerField(blank=True, null=True)

    recompensa = models.CharField(
        max_length=15,
        choices=RECOMPENSA_CHOICES,
        default=EMPTY
    )
    recompensa_value = models.IntegerField(blank=True, null=True)
    recompensa_unidades = models.IntegerField(blank=True, null=True)
    limite = models.CharField(
        max_length=15,
        choices=LIMITE_CHOICES,
        default=EXS
    )
    limite_value = models.IntegerField(blank=True, null=True)

    fecha_desde = models.DateField(blank=True, null=True)
    fecha_hasta = models.DateField(blank=True, null=True)
    visible = models.BooleanField(default=True, blank=True)  # todo si se pasa la fecha visible=False automaticamente

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='promociones',
    )

    class Meta:
        verbose_name_plural = 'Promociones'

    def __str__(self):
        return str(self.texto)

    # guarda la informacion que viene en el POST en la instancia del objeto
    def set_data(self, post):
        self.automatica = True if post.get('auto') == 'true' else False
        self.codigo = True if post.get('codigo') == 'true' else False
        self.visible = False if post.get('visible') == 'false' else True

        if '' != post.get('fecha_desde') and not 'Desde' in post.get('fecha_desde'):
            self.fecha_desde = datetime.datetime.strptime(post.get('fecha_desde'), '%m/%d/%Y').date()
        if '' != post.get('fecha_hasta') and not 'Hasta' in post.get('fecha_hasta'):
            self.fecha_hasta = datetime.datetime.strptime(post.get('fecha_hasta'), '%m/%d/%Y').date()

        if post.get('limite') == 'cli' and post.get('promo-clientes') != '':
            self.limite = Promocion.CLI
            self.limite_value = int(post.get('promo-clientes'))
        else:
            self.limite = Promocion.EXS

        if post.get('codigo_value'):
            self.codigo_value = self.create_code(CODE_LENGHT, post.get('codigo_value'))

        if post.get('tipo-promo') == 'personalizada':
            self.tipo = self.PER
            self.texto = 'Rebaja personalizada'
            self.requisito_value = int(post.get('requisito_value')) if post.get('requisito_value') else -1

            if post.get('req') == 'UD':
                self.requisito = self.UD
            elif post.get('req') == 'EUR':
                self.requisito = self.EUR
            if post.get('obt') == 'UD':
                self.recompensa = self.UD
                self.recompensa_value = int(post.get('obtiene_personalizada_porcentaje')) if post.get(
                    'obtiene_personalizada_porcentaje') != '' else -1
                self.recompensa_unidades = int(post.get('obtiene_personalizada_ud')) if post.get(
                    'obtiene_personalizada_ud') != '' else -1
            elif post.get('obt') == 'EUR':
                self.recompensa = self.EUR
                self.recompensa_value = int(post.get('obtiene_personalizada_euros')) if post.get(
                    'obtiene_personalizada_euros') else -1
                self.recompensa_unidades = -1
            elif post.get('obt') == 'PCT':
                self.recompensa = self.PCT
                self.recompensa_value = int(post.get('obtiene_personalizada_porcentaje')) if post.get(
                    'obtiene_personalizada_porcentaje') else -1

                self.recompensa_unidades = int(post.get('obtiene_personalizada_ud')) if post.get(
                    'obtiene_personalizada_ud') != '' else -1

            self.texto = 'Por la compra de ' + str(
                self.requisito_value) + ' ' + self.requisito + ' el cliente obtiene' + (
                             ' un descuento de ' if self.recompensa != self.UD else ' ') + (
                             str(self.recompensa_value) if self.recompensa_value != -1 else ' ') + (
                             str(self.recompensa_unidades) if self.recompensa == self.UD else ' ') + self.recompensa + (
                             (' GRATIS' if self.recompensa_value == -1 else ' al ' + str(
                                 self.recompensa_value) + '%') if self.recompensa == self.UD else ' ')

        else:
            self.recompensa = Promocion.PCT
            self.tipo = self.RBJ
            if self.tipo == self.RBJ:
                self.texto = 'Rebaja del ' + post.get('obtiene_rebaja_value') + '%'
                self.recompensa_value = int(post.get('obtiene_rebaja_value')) if post.get(
                    'obtiene_rebaja_value') else -1

        if post.get('nombre'):
            self.nombre = post.get('nombre')

    def get_fecha_desde(self):
        return self.fecha_desde.strftime('%m/%d/%Y')

    def get_fecha_hasta(self):
        return self.fecha_hasta.strftime('%m/%d/%Y')

    def create_code(self, num_characters, custom_code=False):
        """ Una función que genera una cadena de X caracteres y comrpueba que es válida"""
        if custom_code:
            slug = slugify(custom_code)
        else:
            slug = get_random_string(num_characters)  # create one
        slug_is_wrong = True
        while slug_is_wrong:  # Mientras no sea valido el código
            slug_is_wrong = False
            naughty_words = 'estafa'  # todo añadir una lista de palabras prohibidas?
            if slug in naughty_words:
                slug_is_wrong = True
            if slug_is_wrong:
                # Crea otro slug nuevo
                slug = get_random_string(num_characters)
        # guarda el codigo generado en la promocion
        slug = upper(slug)
        return slug

    @property
    def code_max_length(self):
        return CODE_LENGHT

    @property
    def recompensa_verbose(self):
        return dict(Promocion.RECOMPENSA_CHOICES)[self.recompensa] if self.recompensa == self.EUR else '%'


class CarritoItem(models.Model):
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.CASCADE,
        related_name='en_carrito',
        blank=True,
        null=True
    )

    variante = models.ForeignKey(
        VarianteArticulo,
        on_delete=models.CASCADE,
        related_name='en_carrito',
        blank=True,
        null=True
    )

    pdv = models.ForeignKey(
        PuntoDeVenta,
        on_delete=models.CASCADE,
        related_name='items_carrito',
        blank=True,
        null=True
    )

    cantidad = models.IntegerField(default=1, blank=True)
    precio_final = models.DecimalField(decimal_places=2, default=0, max_digits=8, blank=True, null=True)
    precio_original = models.DecimalField(decimal_places=2, default=0, max_digits=8, blank=True, null=True)

    def __str__(self):
        return str(self.cantidad) + ' Ud. de ' + str(self.articulo.nombre) if self.articulo else str(
            self.variante.articulo.nombre) + ' ' + (self.variante.get_variantes())

    # como el item puede ser un articulo o variante, con este metodo obtengo el valor que tenga guardado
    def get_item(self):
        return self.articulo if self.articulo else self.variante

    # Devuelve el articulo, tanto si el item es un articulo como si es una variante
    @property
    def promo_reference(self):
        """Necesito obtener el articulo porque las promociones no trabajan con variantes, solo con articulos"""
        return self.articulo if self.articulo else self.variante.articulo

    def is_variante(self):
        return True if self.variante else False


class Carrito(models.Model):
    codigo = models.CharField(max_length=CODE_LENGHT, blank=True, null=True)
    total = models.DecimalField(decimal_places=2, default=0, max_digits=8)
    total_iva = models.DecimalField(decimal_places=2, default=0, max_digits=8)
    pago_ok = models.BooleanField(default=False, blank=True)
    items = models.ManyToManyField(CarritoItem, related_name='articulos_carrito')
    items_promo = models.ManyToManyField(CarritoItem, related_name='en_carrito_y_promocion', blank=True)

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='carrito',
    )

    promocion_asociada = models.ForeignKey(
        Promocion,
        on_delete=models.SET_NULL,
        related_name='promocion_carrito',
        null=True,
        blank=True
    )

    def __str__(self):
        return 'Carrito de ' + str(self.user.username)

    # metodo que devuelve el carrito en formato json (requerido para ajax)
    def json(self):
        # todo como pasar las imagenes para que las carge desde ajax?
        json_items = []
        for item in self.items_promo.all():
            json_items.append({'nombre': item.promo_reference.nombre,
                               'precio_original': item.precio_original,
                               'precio_final': item.precio_final if item.precio_final != 0.0 else 'GRATIS',
                               'cantidad': item.cantidad})
        json = {
            'total': self.total,
            'promo_activa': True if self.promocion_asociada else False,
            'codigo': self.codigo,
            'promo_auto': self.promocion_asociada.automatica if self.promocion_asociada else '',
            'promo_texto': self.promocion_asociada.texto if self.promocion_asociada else '',
            'promo_tipo': self.promocion_asociada.tipo if self.promocion_asociada else '',
            'promo_dcto_general': (
                'Descuento total de ' + str(
                    self.promocion_asociada.recompensa_value) + ' ' + self.promocion_asociada.recompensa_verbose) if self.promocion_asociada and len(
                self.items_promo.all()) == 0 else '',
            'items_promo': json_items
        }
        return json

    def get_total(self):
        total = 0
        for item in self.items.all():
            total += round(item.precio_final * item.cantidad, 2)
        for item_p in self.items_promo.all():

            if item_p.precio_final == 0.0:
                total -= round(item_p.precio_original * item_p.cantidad, 2)
            elif item_p.precio_final != item_p.precio_original:
                total -= round(item_p.precio_final * item_p.cantidad, 2)
        return total

    @property
    def total_articulos(self):
        cantidad = 0
        for items in self.items.all():
            cantidad += items.cantidad
        return cantidad

    # Devuelve el total de articulos del pedido que estan dentro de la promocion
    @property
    def total_articulos_promo(self):
        articulos_validos = [item for item in self.items.all() for _ in range(item.cantidad) if
                             item.promo_reference in self.promocion_asociada.articulos_obtiene.all()]

        return len(articulos_validos)

    # Devuelve la lista de articulos válidos para la promocion
    def get_articulos_validos(self):
        return [item for item in self.items.all().order_by('-precio_final') for _ in range(item.cantidad) if
                item.promo_reference in self.promocion_asociada.articulos_obtiene.all()]

    # Vacía el carrito cuando se hace el pago, esto no borra los CarritoItem que ahora forman parte del pedido
    def empty(self):
        self.items.clear()
        self.items_promo.clear()
        self.total = 0.0
        self.promocion_asociada = None
        self.save()

    # Borra el carrito entero, incluidos los carrito items, si se desea vaciar un carrito por pago usar empty()
    def reset(self):
        self.clean_promos()
        self.promocion_asociada = None
        for item in self.items.all():
            item.precio_final = item.get_item().precio_activo
            item.save()
        self.total = self.get_total()
        self.save()

    def clean_promos(self):
        self.items_promo.all().delete()

    # comprueba si se pueden aplicar las promociones, si se puede, las aplica
    def apply_promo(self):

        if self.promocion_asociada:
            if self.promocion_asociada.tipo == Promocion.RBJ:
                if self.promocion_asociada.automatica:
                    return True if self.apply_rebaja() else False
                elif self.promocion_asociada.codigo:
                    if self.promocion_asociada.codigo_value == self.codigo:
                        return True if self.apply_rebaja() else False
                    else:
                        return False
            elif self.promocion_asociada.tipo == Promocion.PER:
                if self.promocion_asociada.automatica:
                    if self.check_personalizada():
                        return True if self.apply_personalizada() else False
                elif self.promocion_asociada.codigo:

                    if self.promocion_asociada.codigo_value == self.codigo:
                        if self.check_personalizada():
                            return True if self.apply_personalizada() else False
            return False
        else:
            return False

    # aplica la rebaja a los items, devuelve False si ocurre un error, True si se aplica
    def apply_rebaja(self):
        self.clean_promos()
        if self.promocion_asociada.recompensa_value and self.promocion_asociada.recompensa_value != -1:
            for items in self.items.all():
                items.precio_final = round(items.get_item().precio_activo - (
                    items.get_item().precio_activo * self.promocion_asociada.recompensa_value) / 100, 2)
                items.save()
            self.total = self.get_total()
            return True
        else:
            return False

    # comprueba si la promocion cumple los requisitos, por Euros comprados o por unidades compradas
    def check_personalizada(self):
        requisitos_ok = False
        if self.promocion_asociada.requisito == Promocion.EUR:
            if self.get_total() >= self.promocion_asociada.requisito_value:
                requisitos_ok = True
        elif self.promocion_asociada.requisito == Promocion.UD:
            ocurrence_counter = 0
            for articulo in self.items.all():
                if articulo.promo_reference in self.promocion_asociada.articulos_compra.all():
                    ocurrence_counter += articulo.cantidad
            if ocurrence_counter >= self.promocion_asociada.requisito_value:
                requisitos_ok = True

        return requisitos_ok

    # aplica la promocion personalizada a los items, devuelve False si ocurre un error, True si se aplica
    def apply_personalizada(self):
        self.clean_promos()
        apply_ok = False
        if self.promocion_asociada.recompensa == Promocion.EUR:
            self.total = round(self.get_total() - self.promocion_asociada.recompensa_value, 2)
            apply_ok = True
        elif self.promocion_asociada.recompensa_unidades and self.promocion_asociada.recompensa_unidades != -1:
            if self.promocion_asociada.recompensa == Promocion.UD:
                if self.promocion_asociada.requisito == Promocion.UD:
                    articulos_validos = self.get_articulos_validos()
                    index_list = self.apply_formula()

                    if self.promocion_asociada.recompensa_value == -1:  # Quiere decir que se lleva las ud gratis
                        articulos_en_promo = self.apply_discount(index_list, articulos_validos, True)
                        self.items_promo.set(articulos_en_promo)
                        self.total = self.get_total()
                        self.save()
                        apply_ok = True

                    elif self.promocion_asociada.recompensa_value != -1:  # Quiere decir que se aplica un descuento en %

                        articulos_en_promo = self.apply_discount(index_list, articulos_validos, False,
                                                                 self.promocion_asociada.recompensa_value)
                        self.items_promo.set(articulos_en_promo)
                        self.total = self.get_total()
                        self.save()
                        apply_ok = True

                else:
                    pass
            else:
                pass
        elif self.promocion_asociada.recompensa == Promocion.PCT:
            self.total = self.get_total()
            self.total = round(self.total - (self.total * self.promocion_asociada.recompensa_value) / 100, 2)
            apply_ok = True
        else:
            apply_ok = False
        return apply_ok

    # Aplica la formula de Diego para obtener una lista de intervalos que indicaran a que articulos se aplica el descuento
    def apply_formula(self):
        index_list = []
        y = self.promocion_asociada.recompensa_unidades
        x = self.promocion_asociada.requisito_value
        n = self.total_articulos_promo
        apply_counter = int(n / x)
        product_counter = int(apply_counter * self.promocion_asociada.recompensa_unidades)
        print("Veces que se aplica: ", apply_counter, "veces sobre ", product_counter, " productos")
        for _ in range(apply_counter):
            interval = (
                ((int(_) + 1) * x) - y + 1, ((int(_) + 1) * x))  # sumo 1 al indice ("_") para que  no empieze en cero
            index_list.append(interval)
        return index_list

    # Recibe la lista de articulos, los intervalos, si se aplica gratis o un descuento y devuleve la lista con los articulos con del descuento aplicado
    def apply_discount(self, index_list, articulos, gratis=False, cantidad=0.0):
        result = []
        if gratis:
            descuento = 0.0
        for rango in index_list:
            for i in range(rango[0], rango[1] + 1):
                idx = i - 1
                if not gratis:
                    descuento = round((articulos[idx].precio_original * cantidad) / 100, 2)
                if articulos[idx].variante:
                    new_item = CarritoItem(variante=articulos[idx].variante, precio_final=descuento,
                                           precio_original=articulos[idx].promo_reference.precio_activo)
                elif articulos[idx].articulo:
                    new_item = CarritoItem(articulo=articulos[idx].articulo, precio_final=descuento,
                                           precio_original=articulos[idx].promo_reference.precio_activo)
                if len(result) - 1 >= 0 and new_item.get_item() == result[
                            len(result) - 1].get_item():
                    result[len(result) - 1].cantidad += 1
                    result[len(result) - 1].save()
                else:
                    new_item.save()
                    result.append(new_item)
        return result


# Se llama cada vez que se hace un cambio en el field manytomany de la tabla que se le pase
def items_changed(sender, instance, **kwargs):
    if len(instance.items.all()) > 0:
        instance.total = instance.get_total()
        instance.save()


# Despues de guardar o crear un Carrito, una vez se guardan los items en el m2m, llama al metodo para calcular el precio
m2m_changed.connect(items_changed, sender=Carrito.items.through)


# if self.promocion_asociada.recompensa_value:
#     for items in self.items.all():
#         items.precio_final = round(items.get_item().precio_activo - (
#             items.get_item().precio_activo * self.promocion_asociada.recompensa_value) / 100, 2)
#         items.save()
#     apply_ok = True


# Modelo para guardar un registro de los pedidos que se realizan
class Pedido(models.Model):
    # todo En la vista de un pedido en Figma, hay una sección que dice, punto de venta colaborador. Como se realaciona un pdv y un pedido
    TPV = 'TPV'
    TF = 'TF'
    EFEC = 'EF'

    MEDIO_CHOICES = (
        (TPV, 'TPV móvil'),
        (TF, 'Terminal físico'),
        (EFEC, 'Efectivo'),
    )

    items = models.ManyToManyField(CarritoItem, related_name="en_pedido")
    items_promo = models.ManyToManyField(CarritoItem, related_name="en_pedido_y_promo", blank=True)
    pago_ok = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    codigo = models.SlugField(max_length=15, blank=True)
    medio = models.CharField(
        max_length=15,
        choices=MEDIO_CHOICES,
        default=TPV
    )

    total = models.DecimalField(decimal_places=2, default=0, max_digits=8)

    pdv = models.ForeignKey(
        PuntoDeVenta,
        on_delete=models.CASCADE,
        related_name='pedidos',
        null=True,
        blank=True
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='pedidos',

    )

    def save(self, *args, **kwargs):
        self.slug_save()  # genera un codigo aleatorio para el pedido
        super(Pedido, self).save(*args, **kwargs)

    # Contruye el pedido con los datos del carrito actual
    def set_content(self, carrito):
        self.total = carrito.total
        self.items_promo.set(carrito.items_promo.all())
        self.items.set(carrito.items.all())
        self.pago_ok = True
        self.save()
        carrito.empty()

    def slug_save(self):
        """ A function to generate a 5 character slug and see if it has been used and contains naughty words."""
        if not self.codigo:  # if there isn't a slug
            self.codigo = get_random_string(15)  # create one
            slug_is_wrong = True
            while slug_is_wrong:  # keep checking until we have a valid slug
                slug_is_wrong = False
                other_objs_with_slug = type(self).objects.filter(codigo=self.codigo)
                if len(other_objs_with_slug) > 0:
                    # if any other objects have current slug
                    slug_is_wrong = True
                naughty_words = 'caca', 'culo', 'pedo', 'pis'
                if self.codigo in naughty_words:
                    slug_is_wrong = True
                if slug_is_wrong:
                    # create another slug and check it again
                    self.slug = get_random_string(15)

    def get_fecha(self):
        return self.fecha.date()

    def get_hora(self):
        return self.fecha.time()

    def qr(self):
        json = {"id": self.id,
                'tipo': 'pedido'}
        return json

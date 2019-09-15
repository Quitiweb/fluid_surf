from django import forms

from .models import Solicitud, Target, Mercado, Servicios, Articulo, Alquiler, Marca, Espacio, \
    GaleriaArticulo, Categoria, DefinicionVariante, PropuestaComercial, VarianteArticulo, EstiloVida, Maestro, Coleccion

MARCA = 'MARCA'
ESPACIO = 'ESPACIO'
SERVICIO = 'SERVICIO'

MARCA_CHOICES = (
    (MARCA, 'Marca'),
    (ESPACIO, 'Espacio'),
    (SERVICIO, 'Servicios'),
)


class CustomRadioSelect(forms.RadioSelect):
    option_template_name = 'landing/custom/radio-option-custom.html'


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    option_template_name = 'landing/custom/checkbox-multiple-custom.html'


class CustomCheckboxInput(forms.CheckboxInput):
    template_name = 'landing/custom/checkbox-input-custom.html'


class AlquilerForm(forms.ModelForm):
    class Meta:
        model = Alquiler
        fields = ('euros_dia', 'euros_mes', 'euros_semana', 'descripcion')

    def __init__(self, *args, **kwargs):
        super(AlquilerForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs['placeholder'] = 'Descripción breve del alquiler'


class FormularioForm(forms.ModelForm):
    quien_eres = forms.ChoiceField(
        choices=MARCA_CHOICES,
        widget=CustomRadioSelect()
    )

    servicios = forms.ModelMultipleChoiceField(
        queryset=Servicios.objects.all(),
        widget=CustomCheckboxSelectMultiple(),
        required=False
    )

    mercado = forms.ModelMultipleChoiceField(
        queryset=Mercado.objects.all(),
        widget=CustomCheckboxSelectMultiple(),
        required=False
    )

    target = forms.ModelMultipleChoiceField(
        queryset=Target.objects.all(),
        widget=CustomCheckboxSelectMultiple(),
        required=False
    )

    estilo = forms.ModelMultipleChoiceField(
        queryset=EstiloVida.objects.all(),
        widget=CustomCheckboxSelectMultiple(),
        required=False
    )

    que_buscas = forms.ChoiceField(
        choices=MARCA_CHOICES,
        widget=CustomRadioSelect()
    )

    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'placeholder': 'email@ejemplo.com'}))
    nombre = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Empresa Ejemplo'}), required=False)

    class Meta:
        model = Solicitud
        fields = {'quien_eres', 'servicios', 'mercado', 'target', 'que_buscas', 'email', 'nombre', 'estilo'}


class MaestroForm(forms.ModelForm):
    target = forms.ModelMultipleChoiceField(
        queryset=Target.objects.all(),
        widget=CustomCheckboxSelectMultiple(),
        required=False
    )
    mercado = forms.ModelMultipleChoiceField(
        queryset=Mercado.objects.all(),
        widget=CustomCheckboxSelectMultiple(),
        required=False
    )

    estilo = forms.ModelMultipleChoiceField(
        queryset=EstiloVida.objects.all(),
        widget=CustomCheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Maestro
        fields = {'mercado', 'target', 'estilo'}


class SeleccionarCategoriasForm(forms.ModelForm):
    categorias = forms.ModelChoiceField(
        queryset=Categoria.objects.exclude(categoria_padre__isnull=False),
        empty_label='Selecciona una categoría',
        required=False)
    subcategorias = forms.ModelChoiceField(
        queryset=Categoria.objects.exclude(categoria_padre__isnull=True),
        empty_label='Selecciona una subcategoría',
        required=False)

    class Meta:
        model = Categoria
        fields = ('categorias', 'subcategorias')


class NewItemForm(forms.ModelForm):
    url = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Escribir aquí'}), required=False)
    ref = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Escribir aquí'}), required=True)
    nombre = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Escribir aquí'}), required=True)
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Escribir aquí'}), required=False)
    pvp = forms.DecimalField(required=True)
    precio_coste = forms.DecimalField(required=True)

    mercado = forms.ModelMultipleChoiceField(
        queryset=Mercado.objects.all(),
        widget=CustomCheckboxSelectMultiple(),
        required=False
    )

    target = forms.ModelMultipleChoiceField(
        queryset=Target.objects.all(),
        widget=CustomCheckboxSelectMultiple(),
        required=False
    )

    categorias = forms.ModelChoiceField(
        queryset=Categoria.objects.exclude(categoria_padre__isnull=False),
        empty_label='Selecciona una categoría',
        required=False)

    subcategorias = forms.ModelChoiceField(
        queryset=Categoria.objects.exclude(categoria_padre__isnull=True),
        empty_label='Selecciona una subcategoría',
        required=False)

    class Meta:
        model = Articulo
        exclude = {'user'}

    def __init__(self, maestro, *args, **kwargs):
        super(NewItemForm, self).__init__(*args, **kwargs)
        self.tipo = 0
        if maestro:
            self.maestro = True
            self.fields['mercado'].queryset = maestro.mercado
            self.fields['target'].queryset = maestro.target

        else:
            self.maestro = False


class VarianteForm(forms.ModelForm):
    url = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Escribir aquí'}), required=False)
    ref = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Escribir aquí'}), required=True)
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Escribir aquí'}), required=False)
    pvp = forms.DecimalField(required=True)
    precio_coste = forms.DecimalField(required=True)

    mercado = forms.ModelMultipleChoiceField(
        queryset=Mercado.objects.all(),
        widget=CustomCheckboxSelectMultiple(),
        required=False
    )

    target = forms.ModelMultipleChoiceField(
        queryset=Target.objects.all(),
        widget=CustomCheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = VarianteArticulo
        exclude = {'articulo'}

    def __init__(self, maestro, *args, **kwargs):
        super(VarianteForm, self).__init__(*args, **kwargs)
        self.tipo = 1;
        if maestro:
            self.maestro = True
            self.fields['mercado'].queryset = maestro.mercado
            self.fields['target'].queryset = maestro.target

        else:
            self.maestro = False


class NewImagenArticuloForm(forms.ModelForm):
    class Meta:
        model = GaleriaArticulo
        fields = ('imagen',)


class DefinicionVarianteForm(forms.ModelForm):
    class Meta:
        model = DefinicionVariante
        exclude = ('user',)


class ColeccionForm(forms.ModelForm):
    visible = forms.BooleanField(
        required=False,
        widget=CustomCheckboxInput()
    )

    visible.widget.attrs.update({'class': 'toggle-chk'})

    class Meta:
        model = Coleccion
        fields = ('nombre', 'visible')


class MarcaForm(forms.ModelForm):
    direccion = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Escribe la dirección principal '
                                                                             'donde tienes tu sede.'}))

    is_online = forms.BooleanField(
        required=False,
        initial=False,
        widget=CustomCheckboxInput()
    )

    is_mayorista = forms.BooleanField(
        required=False,
        initial=False,
        widget=CustomCheckboxInput()
    )

    is_marketplaces = forms.BooleanField(
        required=False,
        initial=False,
        widget=CustomCheckboxInput()
    )

    is_online.widget.attrs.update({'class': 'toggle-chk'})
    is_mayorista.widget.attrs.update({'class': 'toggle-chk'})
    is_marketplaces.widget.attrs.update({'class': 'toggle-chk'})

    class Meta:
        model = Marca
        fields = ('direccion', 'is_online', 'is_mayorista', 'is_marketplaces')


class EspacioForm(forms.ModelForm):
    is_distribuidor = forms.BooleanField(
        required=False,
        initial=False,
        widget=CustomCheckboxInput()
    )

    is_propia_marca = forms.BooleanField(
        required=False,
        initial=False,
        widget=CustomCheckboxInput()
    )

    is_propietario = forms.BooleanField(
        required=False,
        initial=False,
        widget=CustomCheckboxInput()
    )

    is_nuevo = forms.BooleanField(
        required=False,
        initial=False,
        widget=CustomCheckboxInput()
    )

    is_distribuidor.widget.attrs.update({'class': 'toggle-chk'})
    is_propia_marca.widget.attrs.update({'class': 'toggle-chk'})
    is_propietario.widget.attrs.update({'class': 'toggle-chk'})
    is_nuevo.widget.attrs.update({'class': 'toggle-chk'})

    class Meta:
        model = Espacio
        fields = ('is_distribuidor', 'is_propia_marca', 'is_propietario', 'is_nuevo')


class EditarEspacioForm(forms.ModelForm):
    direccion = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Escribe aquí...'}), required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Escribe aquí...'}), required=True)
    precio_dia = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Escribe aquí...'}), required=True)
    precio_semana = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Escribe aquí...'}), required=True)
    precio_mes = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Escribe aquí...'}), required=True)
    tiempo_minimo = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Escribe aquí...'}), required=False)
    metros_disponibles = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Escribe aquí...'}),
                                            required=False)
    ventas = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Escribe aquí...'}), required=True)
    negociable = forms.BooleanField(
        required=False,
        initial=False,
        widget=CustomCheckboxInput()
    )
    negociable.widget.attrs.update({'class': 'toggle-chk'})

    class Meta:
        model = Espacio
        fields = ('direccion', 'tags', 'precio_dia', 'precio_semana', 'precio_mes', 'metros_disponibles',
                  'tiempo_minimo', 'ventas', 'negociable')


class PropuestaComercialForm(forms.ModelForm):
    LEVE = 'LEVE'
    ESTRICTA = 'ESTRICTA'

    POLITICA = (
        (LEVE, 'Leve'),
        (ESTRICTA, 'Estricta'),
    )

    DATE_INPUT_FORMATS = [
        # '%d-%m-%Y',  # '25-10-2006'
        # '%m-%d-%Y',  # '10-25-2006'
        '%m/%d/%Y',  # '10/25/2006'
        '%Y-%m-%d',  # '2006-10-25'
        '%d/%m/%Y',  # '25/10/2006'
        # '%d/%m/%y'   # '25/10/06'
    ]

    nombre = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Introduce el nombre de tu propuesta'}),
                             required=True)

    fecha_desde = forms.DateField(input_formats=DATE_INPUT_FORMATS)
    fecha_desde.widget.attrs.update({'class': 'fecha', 'readonly': 'readonly'})

    fecha_hasta = forms.DateField(input_formats=DATE_INPUT_FORMATS)
    fecha_hasta.widget.attrs.update({'class': 'fecha', 'readonly': 'readonly'})

    precio_dia = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '0€'}), required=True)
    # precio_dia.initial = '50'
    precio_dia.widget.attrs['disabled'] = 'disabled'

    precio_semana = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '0€'}), required=True)
    precio_semana.widget.attrs['disabled'] = 'disabled'
    precio_semana.widget.attrs.update({'class': 'd-none'})

    precio_mes = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '0€'}), required=True)
    precio_mes.widget.attrs['disabled'] = 'disabled'
    precio_mes.widget.attrs.update({'class': 'd-none'})

    precio_total = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '0€'}), required=True)
    # precio_total.initial = '200'
    precio_total.widget.attrs['disabled'] = 'disabled'

    porcentaje_ventas = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': '0%'}), required=True)
    # porcentaje_ventas.initial = '20'
    porcentaje_ventas.widget.attrs['disabled'] = 'disabled'

    is_acepta_propuestos = forms.BooleanField(
        required=False,
        initial=False,
        widget=CustomCheckboxInput()
    )

    precio_dia_propuesto = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '0€'}), required=False)
    # precio_dia_propuesto.initial = '0'

    precio_semana_propuesto = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '0€'}), required=False)
    # precio_semana_propuesto.initial = '0'
    precio_semana_propuesto.widget.attrs.update({'class': 'd-none'})

    precio_mes_propuesto = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '0€'}), required=False)
    # precio_mes_propuesto.initial = '0'
    precio_mes_propuesto.widget.attrs.update({'class': 'd-none'})

    precio_total_propuesto = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '0€'}), required=True)
    precio_total_propuesto.widget.attrs['disabled'] = 'disabled'
    porcentaje_ventas_propuesto = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': '0%'}), required=True)

    politica_cancelacion_m = forms.ChoiceField(
        choices=POLITICA,
        required=False
    )

    politica_cancelacion_e = forms.ChoiceField(
        choices=POLITICA,
        required=False
    )

    metros_cuadrados = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': '0'}), required=False)

    is_necesita_mobiliario = forms.BooleanField(
        required=False,
        initial=False,
        widget=CustomCheckboxInput()
    )

    comentarios = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Añade cualquier comentario sobre tu propuesta'
        }), required=False)

    is_acepta_propuestos.widget.attrs.update({'class': 'toggle-chk'})
    is_necesita_mobiliario.widget.attrs.update({'class': 'toggle-chk'})

    class Meta:
        model = PropuestaComercial

        fields = ('nombre', 'fecha_desde', 'fecha_hasta', 'precio_dia', 'precio_semana', 'precio_mes', 'precio_total',
                  'porcentaje_ventas', 'is_acepta_propuestos', 'precio_dia_propuesto', 'precio_semana_propuesto',
                  'precio_mes_propuesto', 'precio_total_propuesto', 'porcentaje_ventas_propuesto', 'metros_cuadrados',
                  'is_necesita_mobiliario', 'comentarios')

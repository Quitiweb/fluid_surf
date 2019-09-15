(function ($) {

    //Muestra bien los estilos al cargar un formulario (estilo, mercado, target) con elementos ya seleccionados
   $(document).ready(function () {
        $('.fields > .field > ul > li > label > input ')    .each(function () {
            if($(this).prop("checked")){
                 $(this).closest('li').addClass("checked");
            }
        });
    });

    // Función para ocultar los mensajes tras pasados unos segundos
    setTimeout(function () {
        $('.alert').hide('blind');
    }, 10000);
    // Timeout = 10 segundos, puede cambiarse

    // Función para todos los elementos tipo toggle-chk
    $(".toggle-chk").click(function (event) {
        var show = '#' + event.target.id + '-show';
        $(show).slideToggle('slow');
    });


    // Mostrar/Ocultar elementos

    // Genérico!! NO TOCAR!!
    // Estos scripts se utilizan para varias tabs de la App
    // Por favor, dejad de modificarlos. Gracias!
    $('#tab1-btn').on('click', function () {
        $('#tab2').hide('blind');
        $('#tab1').show('blind');
        $(this).addClass('marked');
        $('#tab2-btn').removeClass('marked');
    });
    $('#tab2-btn').on('click', function () {
        $('#tab1').hide('blind');
        $('#tab2').show('blind');
        $(this).addClass('marked');
        $('#tab1-btn').removeClass('marked');
    });


    // Marca-Espacio
    $('#tab1-empresa-btn').on('click', function () {
        $('#tab2-marca').hide('blind');
        $('#tab2-espacio').hide('blind');
        $('#tab1').show('blind');

        $(this).addClass('marked');
        $('#tab2-marca-btn').removeClass('marked');
        $('#tab2-espacio-btn').removeClass('marked');
    });
    $('#tab2-marca-btn').on('click', function () {
        $('#tab1').hide('blind');
        $('#tab2-marca').show('blind');
        $(this).addClass('marked');
        $('#tab1-empresa-btn').removeClass('marked');
    });
    $('#tab2-espacio-btn').on('click', function () {
        $('#tab1').hide('blind');
        $('#tab2-espacio').show('blind');
        $(this).addClass('marked');
        $('#tab1-empresa-btn').removeClass('marked');
    });


    $('a#categoria-btn').on('click', function () {
        $('#categoria').slideToggle('slow');
    });
    $('#colecc-btn').on('click', function () {
        $('#cartel').hide('blind');
        $('#coleccion').slideToggle('slow');
    });
    $('#promociones-btn').on('click', function () {
        $('#promo-1').hide('blind');
        $('#promo-2a').slideToggle('slow');
        $('#promo-2b').slideToggle('slow');
    });
    $('#articulos-btn').on('click', function () {
        $(this).hide('blind');
        $('#articulos-como').hide('blind');
        $('#articulos-1').slideToggle('slow');
    });
    $('#relac-comer-btn').on('click', function () {
        $('#estado-btn').slideToggle('slow');
    });
    $('#relac-comer-btn-1').on('click', function () {
        $('#pendiente-btn').slideToggle('slow');
    });
    $('#puntosventa-btn').on('click', function () {
        $('#puntosventa1-btn').slideToggle('slow');
    });
    $('.puntosventa-btn').on('click', function () {
        var id=$(this).attr("id").split("btn-")[1];
        $('#puntosventa2-'+id).slideToggle('slow');
    });
    $('.flipable').on('click', function(e) {
        $(e.target).toggleClass('half-flip');
        $(e.target).parent().click();
    })

    $(".toggle-pdv").click(function (event) {
        var id=$(this).attr("id").split("toggle-pdv-");
        var show = '#pdv-show-'+id;
        var btnshow = '#btn-show';
        $(show).slideToggle('slow');
        $(btnshow).slideToggle('slow');
    });


    // Sólo empresa o autónomo puede estar marcado al mismo tiempo
    empresa = '#id_is_empresa'
    autonomo = '#id_is_autonomo'

    $(empresa).on('click', function () {
        if ($(empresa).prop('checked')) {
            $('#botonGuardar')[0].setAttribute('name', 'guardarEmpresa');
            if ($(autonomo).prop('checked')) {
                $(autonomo).prop('checked', false);
                $(autonomo + '-show').slideToggle('slow');
//                $('#botonGuardar').removeAttribute('name');
            }
        }
    });
    $(autonomo).on('click', function () {
        if ($(autonomo).prop('checked')) {
            $('#botonGuardar')[0].setAttribute('name', 'guardarAutonomo');
            if ($(empresa).prop('checked')) {
                $(empresa).prop('checked', false);
                $(empresa + '-show').slideToggle('slow');
//                $('#botonGuardar').removeAttribute('name');
            }
        }
    });

    // Solo marca o espacio puede estar marcado al mismo tiempo
     $(document).ready(function () {

        marca = '#id_is_marca'
        espacio = '#id_is_espacio'
        btn_marca = '#guarda_marca'
        btn_espacio = '#guarda_espacio'

        $(btn_marca).hide();
        $(btn_espacio).hide();

         if ($(marca).prop('checked')) {
            $(btn_marca).show();
         }

         if ($(espacio).prop('checked')) {
            $(btn_espacio).show();
         }



         $(marca).on('click', function () {
            if ($(marca).prop('checked')) {
                $(btn_marca).show();
                if ($(espacio).prop('checked')) {
                    $(btn_espacio).hide();
                    $(espacio).prop('checked', false);
                    $(espacio + '-show').slideToggle('slow');
                }
            } else {
                $(btn_marca).hide();
            }
        });
        $(espacio).on('click', function () {
            if ($(espacio).prop('checked')) {
                $(btn_espacio).show();
                if ($(marca).prop('checked')) {
                    $(btn_marca).hide();
                    $(marca).prop('checked', false);
                    $(marca + '-show').slideToggle('slow');
                }
            } else {
                $(btn_espacio).hide();
            }
        });

     });



    // Solo ordenar o filtrar puede estar marcado al mismo tiempo --> market
    ordenar = '#ordenar-btn'
    filtrar = '#filtrar-btn'

    $(ordenar).on('click', function () {
        if ($(ordenar).prop('checked')) {
            if ($(filtrar).prop('checked')) {
                $(filtrar).prop('checked', false);
                $(filtrar + '-show').slideToggle('slow');
            }
        }
    });
    $(filtrar).on('click', function () {
        if ($(filtrar).prop('checked')) {
            if ($(ordenar).prop('checked')) {
                $(ordenar).prop('checked', false);
                $(ordenar + '-show').slideToggle('slow');
            }
        }
    });
    $('#modalErrorMarket').modal('show');

    //----------------------------------PROPUESTAS------------------------------------

    /*
        Añadido esta función para que al pulsar en los btn-link de relaciones comerciales
        no actue el click de su componente padre. Ocurría al pulsar los botones para, por ejemplo,
        aceptar la propuesta. Se veía durante unos instantes la propuesta (click del padre) y luego hacía el submit.
    */
    $(".link-noparent").click(function(e) {
       e.stopPropagation();
    });

    $("#propuestaform").submit(function (e) {
        e.preventDefault();
        $("#propuestaform :disabled").removeAttr('disabled');
        this.submit();
    });

    $("#id_precio_total_propuesto").prop('disabled', true);

    // TODO Hacer que los campos se actualicen con cualquiera de los dos datepickers.
    // TODO En vez de usar tantas ids usar clases para no repetir información
    $("#id_fecha_desde").change(function () {
        actualizar();
    });

    $("#id_fecha_hasta").change(function () {
        actualizar();
    });

    function actualizar() {
        if ($("#id_fecha_desde").val() && $("#id_fecha_hasta").val()) {
            var desde = $("#id_fecha_desde").val().toString();
            var hasta = $("#id_fecha_hasta").val().toString()

            desdeFormat = desde.split('/');
            hastaFormat = hasta.split('/')

            var fechaDesde = new Date(desdeFormat[1] + "/" + desdeFormat[0] + "/" + desdeFormat[2]);
            console.log(fechaDesde);
            var fechaHasta = new Date(hastaFormat[1] + "/" + hastaFormat[0] + "/" + hastaFormat[2]);

            var diff = new Date(fechaHasta - fechaDesde);

            var days = diff / 1000 / 60 / 60 / 24;

            if (days <= 0) {
                $("#id_fecha_hasta").val('');
                $("#id_fecha_hasta").attr("placeholder", "¡Introduce una fecha válida!");
            } else if (days < 7) {
                $(".unidad-tiempo").text("día");
                $("#id_precio_total").val(($("#id_precio_dia").val() * days))

                $('#id_precio_dia').removeClass("d-none");
                $('#id_precio_semana').addClass("d-none");
                $('#id_precio_mes').addClass("d-none");

                $('#id_precio_dia_propuesto').removeClass("d-none");
                $('#id_precio_semana_propuesto').addClass("d-none");
                $('#id_precio_mes_propuesto').addClass("d-none");

            } else if (days < 30) {
                $(".unidad-tiempo").text("semana");
                $("#id_precio_total").val(($("#id_precio_semana").val() * days / 7.00).toFixed(2))

                $('#id_precio_dia').addClass("d-none");
                $('#id_precio_semana').removeClass("d-none");
                $('#id_precio_mes').addClass("d-none");

                $('#id_precio_dia_propuesto').addClass("d-none");
                $('#id_precio_semana_propuesto').removeClass("d-none");
                $('#id_precio_mes_propuesto').addClass("d-none");
            } else {
                $(".unidad-tiempo").text("mes");
                $("#id_precio_total").val(($("#id_precio_mes").val() * days / 30.00).toFixed(2))

                $('#id_precio_dia').addClass("d-none");
                $('#id_precio_semana').addClass("d-none");
                $('#id_precio_mes').removeClass("d-none");

                $('#id_precio_dia_propuesto').addClass("d-none");
                $('#id_precio_semana_propuesto').addClass("d-none");
                $('#id_precio_mes_propuesto').removeClass("d-none");
            }

            if( $("#id_is_acepta_propuestos").is(':checked')) {
                $("#id_precio_semana_propuesto").val($("#id_precio_semana").val());
                $("#id_precio_mes_propuesto").val($("#id_precio_mes").val());
                $("#id_precio_total_propuesto").val($("#id_precio_total").val());
            }
        }
    }

    // TODO Hacer que se cambie el valor mínimo del segundo datepicker en función del valor del primero
    // Funcion para que se muestre un datepicker cuando pulsamos los campos de fecha de market/propuesta
    $(function () {
        $("#id_fecha_desde").datepicker({
            dateFormat: 'dd/mm/yy',
            defaultDate: new Date(),
            minDate: new Date(),
        });

        $("#id_fecha_hasta").datepicker({
            dateFormat: 'dd/mm/yy',
            minDate: new Date(),
        });
    });

    $("#id_precio_dia_propuesto").change(function() {
        if($("#id_fecha_desde").val() && $("#id_fecha_hasta").val()) {
            var desde = $("#id_fecha_desde").val().toString();
            var hasta = $("#id_fecha_hasta").val().toString()

            var fechaDesde = new Date(desde);
            var fechaHasta = new Date(hasta);

            var diff = new Date(fechaHasta - fechaDesde);

            var days = diff/1000/60/60/24;

            $("#id_precio_total_propuesto").val(($("#id_precio_dia_propuesto").val() * days))
        }
    });

    $("#id_precio_semana_propuesto").change(function() {
        if($("#id_fecha_desde").val() && $("#id_fecha_hasta").val()) {
            var desde = $("#id_fecha_desde").val().toString();
            var hasta = $("#id_fecha_hasta").val().toString()

            var fechaDesde = new Date(desde);
            var fechaHasta = new Date(hasta);

            var diff = new Date(fechaHasta - fechaDesde);

            var days = diff/1000/60/60/24;

            $("#id_precio_total_propuesto").val(($("#id_precio_semana_propuesto").val() * days / 7.00).toFixed(2))
        }
    });

    $("#id_precio_mes_propuesto").change(function() {
        if($("#id_fecha_desde").val() && $("#id_fecha_hasta").val()) {
            var desde = $("#id_fecha_desde").val().toString();
            var hasta = $("#id_fecha_hasta").val().toString()

            var fechaDesde = new Date(desde);
            var fechaHasta = new Date(hasta);

            var diff = new Date(fechaHasta - fechaDesde);

            var days = diff/1000/60/60/24;

            $("#id_precio_total_propuesto").val(($("#id_precio_mes_propuesto").val() * days / 30.00).toFixed(2))
        }
    });


    // Cuando se pulse el checkbox de aceptar las condiciones, se autorellenan los campos del form de precios
    $("#id_is_acepta_propuestos").change(function() {
        if(this.checked) {
            $("#id_precio_dia_propuesto").val($("#id_precio_dia").val());
            $("#id_precio_dia_propuesto").prop('disabled', true);

            $("#id_precio_semana_propuesto").val($("#id_precio_semana").val());
            $("#id_precio_semana_propuesto").prop('disabled', true);

            $("#id_precio_mes_propuesto").val($("#id_precio_mes").val());
            $("#id_precio_mes_propuesto").prop('disabled', true);

            $("#id_precio_total_propuesto").val($("#id_precio_total").val());
            $("#id_precio_total_propuesto").prop('disabled', true);

            $("#id_porcentaje_ventas_propuesto").val($("#id_porcentaje_ventas").val());
            $("#id_porcentaje_ventas_propuesto").prop('disabled', true);

        } else {
            $("#id_precio_dia_propuesto").val("");
            $("#id_precio_dia_propuesto").prop('disabled', false);

            $("#id_precio_semana_propuesto").val("");
            $("#id_precio_semana_propuesto").prop('disabled', false);

            $("#id_precio_mes_propuesto").val("");
            $("#id_precio_mes_propuesto").prop('disabled', false);

            $("#id_precio_total_propuesto").val("");
            $("#id_precio_total_propuesto").prop('disabled', false);

            $("#id_porcentaje_ventas_propuesto").val("");
            $("#id_porcentaje_ventas_propuesto").prop('disabled', false);
        }
    });


    // funcion para mostrar los tooltip (add-item.html)
    $(document).ready(function () {
        $('[data-toggle="tooltip"]').tooltip();
    });

    //metodo para mostrar la imagen seleccionada en el html, para ello añadir la clase self-load-url al div que tiene
    // el input y poner el id al <img> "id_del_input_donde_selecciona_imagen"+""_holder". -> Ejemplo
    // <div class="hide self-load-url">
    //      {{ form.foto_perfil }}
    // </div>
    // <img id="id_foto_perfil_holder" class="portrait" src="{{ user.foto_perfil.url }}" alt="{{ user.foto.title }}"/>

    $('.self-load-url input').change(function () {
        var $input = $(this)[0];
        if ($input.files && $input.files[0]) {

            var reader = new FileReader();
            reader.onload = function (event) {
                $('#'+$input.id+'_holder').attr("src", event.target.result);
            };
            reader.readAsDataURL($input.files[0]);
        }
    });

})(jQuery);

//funciones para mostrar las imagenes en la plantilla antes de guardar el formulario para inputs multi-imagen
var counter=0;
function readURLShow(input) {
    counter=0;

    var parent_div = document.getElementById("multi-img-articulo");
    while (parent_div.firstChild) {
        parent_div.removeChild(parent_div.firstChild);
    }

    if (input.files && input.files[0]) {
        for (var i = 0; i < input.files.length; i++) {
            var reader = new FileReader();
            reader.onload = imageIsLoaded;
            reader.readAsDataURL(input.files[i]);
        }
    }
}

function imageIsLoaded(e,i) {

    if(counter==0){
        activa='active';
    }else{
        activa="new"
    }

    $('#multi-img-articulo').append('<div class="carousel-item col-12 col-sm-6 col-md-4 col-lg-3 '+activa+'">' +
        '<img src="' + e.target.result + '" class="img-fluid mx-auto d-block"' +
        'alt="' + e.target.name + '"> </div>');
    counter++;
};

/**
 * Created by grego on 15/07/19.
 */
(function ($) {


    $(document).ready(function () {

        // $('#member').css("padding", "100");
        if ($('#show_items').prop('checked')) {
            $('#tab2-marca-btn').trigger("click");
            $('#headingTwo h2 button').trigger("click");
        }

        if ($('#show_promo').prop('checked')) {
            $('#tab2-marca-btn').trigger("click");
            $('#headingFour h2 button').trigger("click");
            $('#tab2-existencias').trigger("click");
        }
        if ($('#show_col').prop('checked')) {
            $('#tab2-marca-btn').trigger("click");
            $('#headingThree h2 button').trigger("click");

        }

        $('.loaded').trigger("click");


        $('#editable-content').addClass("disabledcontent"); //impide edicion de promo hasta que se pulsa el botón editar
    });

    $('.btn').click(function () {
        $(this).children('.fa').first().toggleClass('flip');
    });

    ////////////////////////////////////////////////////
    //Funciones para la seccion articulos
    ////////////////////////////////////////////////////

    //Dialogo para preguntar si esta seguro o no para borrar los articulos
    function ConfirmDialog(message) {
        $('<div></div>').appendTo('body')
            .html('<div><h6>' + message + '?</h6></div>')
            .dialog({
                modal: true,
                title: 'Eliminar articulos',
                zIndex: 10000,
                autoOpen: true,
                width: 'auto',
                resizable: false,
                buttons: {
                    Yes: function () {
                        deleteQuery();
                        $(this).dialog("close");
                    },
                    No: function () {
                        $(this).dialog("close");
                    }
                },
                close: function (event, ui) {
                    $(this).remove();
                }
            });
    };


    $('#promo-form ,#search-form').bind("keypress", function (e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            return false;
        }
    });


    // metodos necesario para pasar el csrftoken por ajax
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    var selectedIDs = []; //array contiene items seleccionados en cada momento

    var waiting = true;//Variable para controlar que no se hacen demasiadas busquedas
    var delay = true;
    var timeToDelay = 1000;

    //manda una peticion por ajax al servidor para obtener los articulos que en el nombre contengan la cadena
    // introducida en el buscador y así no recargar la página
    $(".articulo-searchbox").keyup(function (event) {
        waiting = true;
        if ($(".articulo-searchbox").is(":focus") && !waiting) {
            seachQuery();
        } else {
            startDelay();
        }
    });

    //Inicia un delay para que si el usuario escribe muy rapido, no se realicen 20 busquedas, se espera a que pasen al menos 1 segundo entre pulsacion de tecla
    function startDelay() {
        if (delay) {
            delay = false;
            setTimeout(function () {
                waiting = false;
                seachQuery();
                delay = true;
            }, timeToDelay);
        }
    };

    function seachQuery() {
        selectedIDs = [];
        var myinput = $(".articulo-searchbox");

        $.ajax(
            {
                type: "GET",
                url: "/search-item",
                data: {
                    q: $(".articulo-searchbox").val()
                },
                success: function (data) {
                    myResponse = data;

                    $('#item-search-table tr').remove();
                    var head = '<tr>' + '<td>' + "Busquedas para: " + $(".articulo-searchbox").val() + '</td>' + '</tr>';
                    $('#item-search-table thead').append(head);
                    $.each(data, function (index, item) {

                        var html = '<tr>';
                        html += '<th scope="row">' + item['nombre'] + '</th>';
                        html += '<td>' + item['ref'] + '</td>';
                        html += '<td>' + item['descripcion'] + '</td>';
                        html += '<td>' + '<div class="form-check">' +
                            '<input type ="checkbox" class="form-check-input art-found" id="' + item['id'] + '">'
                            + '<label class="form-check-label" for="' + item['id'] + '"> Seleccionar </label >'
                            + '</div>' + '</td ></tr>';

                        $('#item-search-table').prepend(html);
                    });
                }
            })

    }

    $('#art-section1').click(function () {
        $(this).toggleClass("marked");
        if ($('#art-section2').hasClass("marked")) {
            $('#art-section2').removeClass("marked");
        }
    });

    $('#art-section2').click(function () {
        $(this).toggleClass("marked");
        if ($('#art-section1').hasClass("marked")) {
            $('#art-section1').removeClass("marked");
        }
    });

//Al pinchar en la accion editar, antes de mandarnos a la vista guarda los ids de los articulos seleccionados
// en un input
    $('#action-editar').click(function () {
        document.getElementById("ids").value = selectedIDs;
        if (selectedIDs.length == 1) {
            $('#actions_form').attr('action', '/edit-item');
        } else {
            $('#actions_form').attr('action', '/edit-items');
        }
        $('#actions_form').submit();
    });

    //al pinchar en la opcion eliminar, si hay elementos seleccionados muestra el dialogo de confirmacion
    $('#action-eliminar').click(function () {
        if (selectedIDs.length > 0) {

            $('#actions_form').attr('action', '');
            ConfirmDialog('Si eliminas los artículos seleccionados, no podrás recuperarlos y se eliminarán todas las variantes asociadas a ellos. Estás seguro');


        } else {
            alert("No hay articulos seleccionados");
        }
    });

    //peticion de ajax para borrar los elementos selecionados
    function deleteQuery() {
        $.ajax(
            {
                type: "POST",
                url: "/delete-items",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    q: selectedIDs,
                },
                success: function (data) {
                    seachQuery();
                }
            })
    }

//Añade o elimina un elemento del array de selecionados y muestra o no las acciones (sin articulos seleccionados
// no muestra las acciones posibles)
    $('body').on('click', '.art-found', function () {
        if (this.checked) {
            selectedIDs.push(this.id);
        } else {
            selectedIDs.splice($.inArray(this.id, selectedIDs), 1);
        }
        var table = document.getElementById('item-search-table');
        var inputs = table.getElementsByClassName('art-found');
        $('#item-options-dropdown').addClass("hide");

        for (i = 0; i < inputs.length; i++) {
            if (inputs[i].checked) {
                $('#item-options-dropdown').removeClass("hide");

                break;
            }
        }
    });

//Detecta el acto de añadir un filtro en el input y lo añade si es correcto
    $('#add-filter-option').on('change', function () {
        if (!alreadyAdded(this)) {
            addTag($("#add-filter-option option:selected").text(), this.value);
            showFields(this.value);
        }

    });

//recorre todos los tags del div donde aparecen, si ya existe no lo añade
    function alreadyAdded(element) {
        var added = false;
        var $filtros = $('#campos-container').children();
        $filtros.each(function () {
            if (this.id == ("option_" + element.value) || element.value == '0') {
                added = true;
            }
        });

        return added;
    }

//Añade el tag que representa el filtro  al div donde aparecen (#campos-container)
//Añade el filtro a la lista
    function addTag(value, id) {
        var div = $(document.createElement('div'));
        var span = $(document.createElement('span'));
        span.addClass("rounded");
        span.addClass("text-light");
        span.addClass("bg-morado");
        span.addClass("p-2");
        span.addClass("tag");
        span.addClass("label");
        span.addClass("label-info");

        var span1 = $(document.createElement('span'));
        span1.text(value);
        var a = $(document.createElement('a'));
        var i = $(document.createElement('i'));
        i.addClass("remove");
        i.addClass("fa");
        i.addClass("ml-2");
        i.addClass("fa-close");
        i.attr("id", (id));
        a.append(i);
        span.append(span1);
        span.append(a);
        div.append(span);
        div.attr("id", ("option_" + id));
        div.click(function () {
            removeTag(this);
            hideFields(this.id);
        });
        $('#campos-container').append(div)
    }

//elimina un tag del div (#campos-container)
    function removeTag(div) {
        var $filtros = $('#campos-container').children();
        $filtros.each(function () {
            if (this.id == div.id) {
                div.remove();
            }
        });
    }

//Muestra el campo correspondiente en la tabla (en todos los articulos/variantes)
    function showFields(option) {
        switch (option) {
            case '1':
                $('.id_ref').removeClass("hide");
                break;
            case '2':
                $('.id_url').removeClass("hide");
                break;
            case '3':
                $('.id_pvp').removeClass("hide");
                break;
            case '4':
                $('.id_precio_coste').removeClass("hide");
                break;
            case '5':
                $('.id_precio_comparacion').removeClass("hide");
                break;
            case '6':
                $('.id_stock').removeClass("hide");
                break;
            case '0':
                break;
            default:
        }
    }

//Oculta el campo correspondiente en la tabla (en todos los articulos/variantes)
    function hideFields(option) {
        switch (option) {
            case 'option_1':
                $('.id_ref').addClass("hide");
                break;
            case 'option_2':
                $('.id_url').addClass("hide");
                break;
            case 'option_3':
                $('.id_pvp').addClass("hide");
                break;
            case 'option_4':
                $('.id_precio_coste').addClass("hide");
                break;
            case 'option_5':
                $('.id_precio_comparacion').addClass("hide");
                break;
            case 'option_6':
                $('.id_stock').addClass("hide");
                break;
            case 'option_0':
                break;
            default:

        }

    }

    // $('#campos-container').append(div)


    ///////////////////////////////////////////////////////////////////
    //Funcionalidades para la importación de archivos dentro de la sección articulos
    ///////////////////////////////////////////////////////////////////


    $('#csv-icon').click(function () {
        $('#shp-csv').trigger("click");
        $('#csv-icon').addClass("marked");
        $('#ex-icon').removeClass("marked");

    });

    $('#ex-icon').click(function () {
        $('#shp-ex').trigger("click");
        $('#csv-icon').removeClass("marked");
        $('#ex-icon').addClass("marked");
    });

    $('#shp-ex').on("change", function () {
        $('#shp-csv').val('');
    });

    $('#shp-csv').on("change", function () {
        $('#shp-ex').val('');
    });

    /////////////////////////////////////////////
    //Funcionalidad para las promociones y rebajas
    /////////////////////////////////////////////
    var fecha_desde = null;
    var fecha_hasta = null;
    var tipo_promo = null;


//Carga el datepicker "desde" con la fecha de hoy como mininmo y el datepicker "hasta" en funcion de este
    $(function () {

        $("#datepicker-desde").datepicker({
                showAnim: "fold",
                minDate: 0,
                onSelect: function (dateText) {
                    fecha_desde = dateText;
                    $("#datepicker-hasta").datepicker("option", "minDate", new Date(dateText));

                }
            }
        );
        if (fecha_desde == null) {
            $("#datepicker-hasta").datepicker({
                showAnim: "fold", onSelect: function (dateText) {
                    fecha_hasta = dateText;
                }
            });

        } else {
            $("#datepicker-hasta").datepicker({
                showAnim: "fold", minDate: new Date(dateText), onSelect: function (dateText) {
                    fecha_hasta = dateText;
                }
            });

        }
    });


    $('#promo_visible').click(function () {
        if ($(this).prop("checked")) {
            $('#visible').val(true)
        } else {
            $('#visible').val(false)
        }
    });

//Controla si se elige el limite de clientes o el limite de existencias en las promociones
    $('#tab1-clientes').on('click', function () {
        $(this).addClass('marked');
        $('#id-promo-clientes').attr('type', 'number');
        $('#tab2-existencias').removeClass('marked');
        $('#limite').val('cli');

    });
    $('#tab2-existencias').on('click', function () {
        $('#id-promo-clientes').attr('type', 'hidden');
        $(this).addClass('marked');
        $('#tab1-clientes').removeClass('marked');
        $('#limite').val('ex');
    });


//Añade estilo a los inputs
    $('.marked-input').change(function () {
        if ($(this).val() != '') {
            $(this).addClass("input-marked");
        } else {
            $(this).removeClass("input-marked");
        }
    });


//controla el funcionamiento del componente promo-2a
    $('#promo-2a p').click(function () {
        if ($(this).attr('id') == "promo-2a-unidades") {
            $('#promo-2a-euros').removeClass("marked");
            $(this).addClass("marked");
            $('#req').val('UD');

        } else if ($(this).attr('id') == "promo-2a-euros") {
            $('#promo-2a-unidades').removeClass("marked");
            $('#req').val('EUR');
            $(this).addClass("marked");
        }
    });


//controla el funcionamiento del componente promo-2b
    $('#promo-2b p').click(function () {

        if ($(this).attr('id') == "promo-2b-descuento") {
            $('#promo-2b-euros').attr('type', 'number');
            $('#promo-2b-gratis').addClass("hide");
            $('#promo-2b-unidades-input').attr('type', 'hidden').removeClass("input-marked").val("");
            $('#promo-2b-unidades').removeClass("marked");

        } else if ($(this).attr('id') == "promo-2b-unidades") {
            $('#promo-2b-euros').attr('type', 'hidden');
            $('#promo-2b-gratis').removeClass("hide");
            $('#obt').val("UD");
            $('#promo-2b-unidades-input').attr('type', 'number');
            $('#promo-2b-euros').attr('type', 'hidden').removeClass("marked input-marked").val("");
            $('#promo-2b-descuento').removeClass("marked");

        }

        $(this).addClass("marked");
    });

    $('#promo-2b-euros').change(function () {
        $('#promo-2b-porcentaje').val("");
        $('#promo-2b-porcentaje').removeClass("input-marked");
        $('#obt').val('EUR');
    });

    $('#promo-2b-porcentaje').change(function () {
        $('#promo-2b-euros').val("");
        $('#promo-2b-euros').removeClass("input-marked");
        $('#obt').val('PCT');
        $('#promo-2b-gratis').removeClass("marked")
    });

    $('#promo-2b-gratis').click(function () {
        $('#promo-2b-porcentaje').val("");
        $('#promo-2b-porcentaje').removeClass("input-marked");
    });


    //Añade el estilo correspondiente a los divs para seleccionar el tipo
    function changeBorder(elem) {
        if (elem.hasClass("border-dark")) {
            elem.removeClass("border-dark");
            elem.addClass("border-morado");
        } else {
            elem.addClass("border-dark");
            elem.removeClass("border-morado");
        }
    }


    $('#auto-selector').click(function () {
        if ($('#codigo-selector').hasClass("border-morado")) {
            $('#codigo-selector').trigger("click");
        }
        $('#auto').val(!$(this).val());
        $(this).val(!$(this).val());
        changeBorder($(this));

    });

    $('#codigo-selector').click(function () {
        if ($('#auto-selector').hasClass("border-morado")) {
            $('#auto-selector').trigger("click");

        }
        $('#codigo-container').toggleClass("hide");
        $('#codigo').val(!$(this).val());
        $(this).val(!$(this).val());
        changeBorder($(this));


    });

    $('#rebaja-selector').click(function () {
        $('#promo-1').toggleClass("hide");
        $('#tipo-promo').val('rebaja');
        changeBorder($(this));
        if ($('#personalizada-selector').hasClass("border-morado")) {
            changeBorder($('#personalizada-selector'));
        }
        $('#promo-2a').addClass("hide");
        $('#promo-2b').addClass("hide");
    });

    $('#personalizada-selector').click(function () {
        $('#promo-2b').toggleClass("hide");
        $('#promo-2a').toggleClass("hide");
        $('#tipo-promo').val('personalizada');
        changeBorder($(this));
        if ($('#rebaja-selector').hasClass("border-morado")) {
            changeBorder($('#rebaja-selector'));
        }
        $('#promo-1').addClass("hide");
    });

///////////////////////////////////////////////////////////////
//Funcionalidades para la vista de buscar items dentro de promo
////////////////////////////////////////////////////////////////

    var promo_ids = [];
    var selected_strings = [];

    //todo cambiar los alert por algo mas estético como un snackbar
    $('#enviar-ids').click(function () {
        if (promo_ids.length == 0) {
            alert('Debe seleccionar al menos un artículo');
        } else {
            document.getElementById("selected-promo-items").value = promo_ids;
        }
    });

    $('body').on('click', '.promo-found', function () {
        if (this.checked) {
            promo_ids.push(this.id);
        } else {
            promo_ids.splice($.inArray(this.id, promo_ids), 1);

        }
    });

    //hace la peticion para filtrar tanto cuando se pulsa enter en el buscador como cuando se hace click en un filtro
    //ademas muestra en pantalla la lista de filtros actualmente seleccionados
    $('#filtro_options input').click(function () {
        ajaxSearchPromo();
        if ($(this).prop('checked')) {
            var label = $('#filtro_options label[for="' + $(this).attr('id') + '"]');
            var content = label.text();
            if (selected_strings.indexOf(content) == -1) {
                selected_strings.push(content);
            }
        } else {
            selected_strings.splice(selected_strings.indexOf(content), 1);
        }
        if (selected_strings.join() == '') {
            $('#selected-tags p').text("Sin filtros");
        } else {
            $('#selected-tags p').text(selected_strings.join());

        }
    });

    var waiting = true; //Marca si se debe esperar o no
    var delay = true; //False si ya hay un delay activo
    var timeToDelay = 1000;

    //Cuando se pulsa intro en el input del buscador lanza la petición
    $('#input-buscador').keyup(function (event) {
        waiting = true;
        if ($(this).is(":focus") && !waiting) {
            getArticulosPDVs();
        } else {
            startDelay2();
        }
    });


    //Detecta cuando se pulsa intro en el buscador
    $(".promo-searchbox").keyup(function (event) {
        waiting = true;
        if ($(this).is(":focus") && !waiting) {
            ajaxSearchPromo();
        } else {
            startDelay2();
        }
    });


    //Inicia un delay para que si el usuario escribe muy rapido, no se realicen 20 busquedas, se espera a que pasen al menos 1 segundo entre pulsacion de tecla
    function startDelay2() {
        if (delay) {
            delay = false;
            setTimeout(function () {
                waiting = false;
                ajaxSearchPromo();
                delay = true;
            }, timeToDelay);
        }
    };

    //Realiza la petición mediante ajax al servidor para hacer el filtrado de articulos
    function ajaxSearchPromo() {
        promo_ids = [];
        var myinput = $(".promo-searchbox");
        $.ajax(
            {
                type: "GET",
                url: "/query-item-promo",
                data: {
                    q: myinput.val(),
                    'm[]': getSelected('m'),//m=mercado
                    't[]': getSelected('t'),//t=target
                    'c[]': getSelected('c'),//c=categorias
                    'sc[]': getSelected('x'),//x=subcategorias
                    's[]': getSelected('s'),//s=colecciones
                },
                success: function (data) {


                    $('#item-search-table-dialog').empty();
                    if (data.length > 0) {
                        $.each(data, function (index, item) {


                            var html = '<tr>';
                            if (item['in_promo'] == null) {
                                html += '<th scope="row"><span class="fa-stack">' +
                                    '<i class="fa fa-exclamation-triangle fa-stack-2x" style="color:#fbed50;"></i>' +
                                    '<i class="fa fa-info fa-stack-1x" style="color:#000000;"></i></span>';
                            } else {
                                html += '<th scope="row"></th>';
                            }
                            html += '<td></i>' + item['nombre'] + '</td>';
                            html += '<td>' + item['ref'] + '</td>';
                            html += '<td>' + item['pvp'] + '</td>';
                            html += '<td>' + item['precio_comparacion'] + '</td>';
                            html += '<td><img class="mini-thumbnail" src="media/' + item['imagen_principal'] + '"/></td>'; //todo cargar la imagen
                            html += '<td>' + '<div class="form-check">' +
                                '<input type ="checkbox" class="form-check-input promo-found" id="' + item['id'] + '">'
                                + '<label class="form-check-label" for="' + item['id'] + '"> Seleccionar </label >'
                                + '</div>' + '</td ></tr>';

                            $('#item-search-table-dialog').prepend(html);
                        });
                    } else {
                        var html = '<tr>';
                        html += '<th scope="row">Búsqueda para: ' + $(".promo-searchbox").val() + '</th>';
                        html += '<td>Sin resultados</td>';
                        $('#item-search-table-dialog').prepend(html);
                    }
                }
            })
    }

    //obtiene los elementos seleccionados en cada filtro (mercado,target,categorias,colecciones)
    function getSelected(filtro) {
        var array = [];
        var re = new RegExp(filtro, 'g');//obtengo el div cuyo id corresponde con el filtro seleccionado
        $('#filtro_options input').filter(function () {
            return this.id.match(re);
        }).each(function () { // y para cada uno de sus elementos guardo el id para luego hacer el filtrado
            var id = $(this).attr('id').split("-");
            if ($(this).prop('checked')) {
                array.push(id[1]);
            }
        });
        // var id = $('#filtro_' + filtro + '_options input').each(function () {
        //     var id = $(this).attr('id').split("-");
        //     if ($(this).prop('checked')) {
        //         array.push(id[1]);
        //     }
        //
        // });
        return array;
    }


//Selecciona/deselecciona todos los articulos en la lista
    $('#select_all_items').click(function () {
        var select_all = $(this);
        $('#item-search-table-dialog input').each(function () {
            if ($(this).prop('checked') != select_all.prop('checked')) {
                $(this).trigger('click');
            }
        })
    });


//muestra el filtro correspondiente / oculta los demás

    $('#filtro_mtcs').find('p').click(function () {
        clearFilters();
        $(this).children().addClass("fa-angle-down");
        showFilters($(this));
    });

//Muestra las opciones de cada filtro (Ej: si pulsas en categorias, despliega la lista de categorias)
    function showFilters(element) {
        if (element.attr('id') == "filtro_m") {
            $('#filtro_m_options').removeClass("hide");
        } else if (element.attr('id') == "filtro_t") {
            $('#filtro_t_options').removeClass("hide");
        } else if (element.attr('id') == "filtro_c") {
            $('#filtro_c_options').removeClass("hide");
        } else {
            $('#filtro_s_options').removeClass("hide");
        }
    }

//Oculta el resto de filtros, para que se muestre solo el que se acaba de pulsar
    function clearFilters() {
        $('#filtro_mtcs p i').removeClass("fa-angle-down");
        $('#filtro_mtcs p i').addClass("fa-angle-right");
        $('#filtro_options').children('div').addClass("hide");

    }


///////////////////////////////////////////////////////////////
//Funcionalidades para la vista de proximos descuentos
////////////////////////////////////////////////////////////////

    //vuelve para atras en el navegador
    $("#backLink").click(function (event) {
        history.back(1);
    });

// /////////////////////////////////////////////////////////
//Funcionalidades para la vista de promo detail
////////////////////////////////////////////////////////////////

//Activa/desactiva la edición de la promoción
    $('#edit-button').click(function () {

        $('#guardar_button').parent().toggleClass("hide");
        if ($(this).hasClass("marked")) {
            $('#editable-content').addClass("disabledcontent");
            $(this).removeClass("marked");
            $('#items_r_obtiene, #items_p_obtiene, #items_p_requiere').text("VER");
            $('#items_r_obtiene, #items_p_obtiene, #items_p_requiere').val("true");

        } else {
            $(this).addClass("marked")
            $('#editable-content').removeClass("disabledcontent");
            $('#items_r_obtiene, #items_p_obtiene, #items_p_requiere').text("EDITAR");
            $('#items_r_obtiene, #items_p_obtiene, #items_p_requiere').val("false");
        }
    });

///////////////////////////////////////////////////////////
//Funcionalidades para la sección de maestros
////////////////////////////////////////////////////////////////


    var sub_array = []; //Array para las subcategorias

    //Si introducimos una categoria, mostramos el input de subcategorias y ocultamos el de categoria
    $('#nueva_categoria').change(function () {
        if ($(this).val() != '') {
            $(this).hide();
            $('#categoria_seleccionada').show();
            $("label[for='nueva_categoria']").text($(this).val());
            $('#nuevas_subcategorias').show();
        }
    });

    //Muestra el label con la lista actual de subcategorias
    $('#nueva_subcategoria_input').change(function () {
        if ($(this).val() != '') {
            $("label[for='nuevas_categorias']").text($(this).val());
            $('#nuevas_subcategorias').show();
        }
    });

    //Al pulsar coma o enter en el input de subcategorias las añade al array, si pulsamos borrar borra la ultima en la lista
    $('#nueva_subcategoria_input').on("keyup change", function (e) {
        //todo en chrome smartphone no detecta las comas
        if (e.keyCode == 188 || e.keyCode == 13) { // KeyCode For comma is 188 enter is 13
            var value = (e.keyCode == 188) ? $(this).val().slice(0, -1) : $(this).val();
            if ((value.length > 0 ? ',' : '')) {
                sub_array.push($(this).val());
                $("label[for='nuevas_subcategorias']").text($("label[for='nuevas_subcategorias']").text() + value + ',');
            }
            $(this).val('');
        } else if (e.keyCode == 8) { //keycode de la tecla borrar
            sub_array.pop();
            $("label[for='nuevas_subcategorias']").text('');
            sub_array.forEach(function (item) {
                $("label[for='nuevas_subcategorias']").append(item + ',');
            });
        }
    });

    //Impide que se ejecute el evento toggle si pulsamos alguno de los elementos hijos
    $('#categorias_actuales div').children().click(function (event) {
        event.stopPropagation();
    });

    //Si pulsamos el icono de editar, nos permite editar el nombre de la categoria o subcategoria
    $('#categorias_actuales i[id*="edit"]').click(function () {
        $(this).toggleClass("fa-morado");
        $(this).siblings().toggle("hide");
        var id = $(this).attr('id').split('-')[1];
        if ($('#elem-' + id).attr('contenteditable') == 'true') {
            $('#elem-' + id).attr('contenteditable', 'false');
        } else {
            $('#elem-' + id).attr('contenteditable', 'true');
            $('#elem-' + id).effect("highlight", {}, 3000);
            $('#elem-' + id).focus();
        }
    });

    //minimiza el toast cuando este desaparece para que no se quede un hueco blanco en el template
    $('.toast').on('hidden.bs.toast', function () {
        $('.toast').hide();
    });

    function doConfirm(msg, yesFn, noFn) {
        var confirmBox = $("#confirmBox");

        confirmBox.find(".message").text(msg);
        confirmBox.find(".yes,.no").unbind().click(function () {
            confirmBox.hide();
        });
        confirmBox.find(".yes").click(yesFn);
        confirmBox.find(".no").click(noFn);
        confirmBox.dialog
        ({
            autoOpen: true,
            modal: true,
            buttons: {
                'Yes': function () {
                    $(this).dialog('close');
                    $(this).find(".yes").click();
                },
                'No': function () {
                    $(this).dialog('close');
                    $(this).find(".no").click();
                }
            }
        });
    };

    //Cuando se pulsa el botón de eliminar dentro de la tabla de categorias, se llama al método para borrar
    $('#categorias_actuales i[id*="delete"]').click(function () {
        var id = $(this).attr('id').split('-')[1];
        deleteCat(id);

        doConfirm("Are you sure?", function yes() {
            form.submit();
        }, function no() {
            // do nothing
        });
    });


    //cuando se pulsa el boton de save dentro de una categoria en la tabla, se envía el nombre que haya escrito y
    // se edita el modelo
    $('#categorias_actuales i[id*="save"]').click(function () {
        var id = $(this).attr('id').split('-')[1];
        $.ajax(
            {
                type: "POST",
                url: "/edit-categoria",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    categoria: id,
                    nombre: $('#elem-' + id).text().trim()
                },
                success: function (data) {
                    $('.toast').show();
                    $('.toast').toast('show');
                }
            })
    });

    //Se coge el id del elemento html, que se corresponde con el id en la bbdd. Se envía la petición para borrarlo.
    function deleteCat(id) {
        $.ajax(
            {
                type: "POST",
                url: "/delete-categoria",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    categoria: id,
                },
                success: function (data) {
                    $('#new-cat-' + id).remove();
                }
            })
    };

    //funcion que se comunica por ajax con el servidor para guardar la categoria y sus subcategorias correspondientes.
    //actualiza la pagina con las nuevas categorias
    $('#actualizar_categorias').click(function () {
        $.ajax(
            {
                type: "POST",
                url: "/add-categoria",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    categoria: $('#nueva_categoria').val(),
                    subcategorias: sub_array
                },
                success: function (data) {
                    if (data == 'false') {
                        alert("Ha ocurrido un error al guardar");
                    } else {
                        $('#empty_cat').hide();
                        $('#nueva_categoria').val('');
                        $('#nueva_categoria').show();
                        $('#categoria_seleccionada').hide();
                        $('#nuevas_subcategorias').hide();
                        $("label[for='nueva_categoria']").text('');
                        $("label[for='nuevas_subcategorias']").text('');


                        var html = '<div id="new-cat-' + data['id'] + '"' +
                            'class="list-group-item list-group-item-action d-flex justify-content-between align-items-center collapsed" ' +
                            'data-toggle="collapse" data-target="#target-' + data['id'] + '" aria-expanded="false"' +
                            ' aria-controls="#target-' + data['id'] + '"> <a id="elem-' + data['id'] + '" ' +
                            'href="#" contenteditable="false"> ' + data['nombre'] + ' </a><div>' +
                            '<span class="float-right badge badge-primary badge-pill ml-2">' + data['sub'].length + '</span>' +
                            '<i class="fa fa-edit fa-2x" id="edit-' + data['id'] + '"></i>' +
                            '<i class="fa fa-save fa-2x hide" id="save-' + data['id'] + '"></i>' +
                            '<i class="fa fa-close fa-2x hide" id="delete-' + data['id'] + '"></i>' +
                            '</div></div>';

                        $('#categorias_actuales').append(html);
                        if (data['sub'].length > 0) {
                            var html = '<ul id="target-' + data['id'] + '" class="ml-2 list-group list-group-flush collapse">';
                            $.each(data['sub'], function (index, elem) {

                                html += '<div id="new-cat-' + elem['id'] + '" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">' +
                                    '<a id="elem-' + elem['id'] + ' "href="#elem-' + data['id'] + '" contenteditable="false">' + elem['nombre'] +
                                    '</a><div> <i id="edit-' + elem['id'] + '" class="fa fa-edit fa-2x"></i>' +
                                    '<i class="fa fa-save fa-2x hide" id="save-' + elem['id'] + '"></i>' +
                                    '<i class="fa fa-close fa-2x hide" id="delete-' + elem['id'] + '"></i></div></div>';

                            });
                            html += '</ul>';
                            $('#categorias_actuales').append(html);
                        }
                    }

                }
            });
    });


    $('.coleccion label').click(function () {
        var id = $(this).attr("for").split("coleccion-visible-")[1];

        toggleVisible(id, !$('#' + id).hasClass("checked"));


    });

    function toggleVisible(id, checked) {
        $.ajax(
            {
                type: "POST",
                url: "/toggle-visible-col/",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    col: id,
                    checked: checked
                },
                success: function (data) {

                }
            })
    }

})
(jQuery);


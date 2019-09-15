/**
 * Created by grego on 27/08/19.
 */
(function () {
    //al cargar la página realiza una busqueda por defecto
    $(document).ready(function () {
        getArticulosPDVs();
    });

    //Metodos necesario para pasar el csrftoken por ajax
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

    /////////////////////////////////////////
    //Funcionalidades para el buscador de PDV
    ////////////////////////////////////////

    //Array donde se guardan los ids de las marcas actualmente seleccionadas,
    // si no hay ninguna seleccionada, por defecto se seleccionan todas
    var selectedMarcas = [];


    //Añade o quita una marca de las marcas seleccionadas
    $('#marcas-selectors div').click(function () {
        var $child = $(this);
        var id = $child.attr("id").split("marca-")[1];
        if ($child.hasClass("border-primary")) {
            $child.removeClass("border-primary");
            $child.addClass("border-morado");
            selectedMarcas.push(id)
        } else {
            $child.addClass("border-primary");
            $child.removeClass("border-morado");
            selectedMarcas.splice($.inArray(id, selectedMarcas), 1);
        }
        getArticulosPDVs();
    });


    //Antes de enviar el formulario, cambia la url por la correspondiente
    $('#detail-form').submit(function () {
        var $btn = $(document.activeElement);
        var id = $btn.attr("id").split("-b-")[1];
        var pdv = $btn.attr("id").split("-b-")[0];
        if ($btn.hasClass("button-item-detail")) {
            item_url = url.replace('0', id);
            item_url = item_url.replace('1', pdv);
            $('#detail-form').attr('action', item_url);
        } else if ($btn.hasClass("button-pedido-detail")) {
            item_url = url.replace('1/0', id);
            item_url = item_url.replace('articulo-detail', 'pedido-detail');
            $('#detail-form').attr('action', item_url);
        }
    });

    //Variables para controlar el flujo del buscador
    var waiting = true; //Marca si se debe esperar o no
    var delay = true; //False si ya hay un delay activo
    var timeToDelay = 1000;

    //Cuando se pulsa intro en el input del buscador lanza la petición
    $('#input-buscador').keyup(function (event) {
        waiting = true;
        if ($(this).is(":focus") && !waiting) {
            getArticulosPDVs();
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
                getArticulosPDVs();
                delay = true;
            }, timeToDelay);
        }
    };


    //Peticion ajax al servidor para obtener una lista de articulos
    function getArticulosPDVs() {
        $.ajax(
            {
                type: "POST",
                url: "/search-pdvs",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    q: $('#input-buscador').val(),
                    marcas: selectedMarcas
                },
                success: function (data) {
                    console.log(data)
                    $('#buscador-pdv-result').empty();
                    if (data[0].length > 0) {
                        var articulos = data[0];
                        var table = '<h1>Artículos</h1>';

                        table += '<table class="table" id="table-art">' +
                            '<thead class="thead-dark">' +
                            '<tr colspan="5"> <th scope="col" colspan="5">#</th>' +

                            '</tr>' +
                            '</thead><tbody>';

                        for (var i = 0; i < articulos.length; i++) {
                            table += '<tr id="item-' + articulos[i]['id'] + '"><th scope="row" class="button-holder"><button type="button" class="btn btn-transparent qr-button" id="qr-' + articulos[i]['id'] + '" data-toggle="modal" data-target="#exampleModalCenter"><img class="mini-thumbnail" src="media/' + articulos[i]['imagen_principal'] + '"></button></th>' +
                                '<td>' + articulos[i]['nombre'] + '</td>' +
                                '<td>' + articulos[i]['ref'] + '</td>';
                            if (articulos[i]['precio_comparacion'] == 0.00) {
                                table += '<td>' + articulos[i]['pvp'] + '</td>';

                            } else {
                                table += '<td>' + articulos[i]['precio_comparacion'] + '</td>';
                            }
                            table += '<td><button id="' + articulos[i]['punto'] + '-b-' + articulos[i]['id'] + '" type="submit" class="btn-transparent button-item-detail"><i class="fa fa-arrow-right"></i> </button></td>';
                            table += '</tr>';

                        }
                        table += '</tbody></table>';
                        $('#buscador-pdv-result').append(table);

                    } else {
                        $('#buscador-pdv-result').append('<p>No se ha encontrado nada</p>')
                    }
                    if (data[1].length > 0) {
                        var table = '<h1>Pedidos</h1>';
                        var pedidos = data[1];

                        table += '<table class="table">' +
                            '<thead class="thead-dark">' +
                            '<tr colspan="5"> <th scope="col" colspan="5">#</th>' +

                            '</tr>' +
                            '</thead><tbody>';

                        for (var i = 0; i < pedidos.length; i++) {

                            table += '<tr id="item-' + pedidos[i]['id'] + '">' +
                                '<th scope="row" colspan="3"><div><p><strong>Pedido </strong>' + pedidos[i]['codigo'] + '</p><p>' + pedidos[i]['fecha'] + '</p></div></th>';

                            table += '<td><i class="fa fa-envelope"></i> </td>';
                            table += '<td><button type="submit" id="-b-' + pedidos[i]['id'] + '" class="btn-transparent button-pedido-detail"><i class="fa fa-arrow-right"></i> </button></td>';

                            table += '</tr>';

                        }
                        table += '</tbody></table>';
                        $('#buscador-pdv-result').append(table);
                    }
                }
            })
    }


    //Como los button se generan por ajax hay que usar la fucion "on" en un elemento padre que no sea generado por ajax
    $("#buscador-pdv-result").on("click", "button", function () {
        var id = $(this).attr("id").split("qr-")[1];
        console.log($(this).attr("id"));
        returnQR(id);
    });

    //Hace la petición al servidor para que devuelva el json del qr, y con la libreria de qrcodes generamos uno
    function returnQR(id) {
        $.ajax(
            {
                type: "POST",
                url: "/get-qr",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    id: id,
                },
                success: function (data) {
                    data = JSON.stringify(data);
                    if (data != '') {
                        $('#qrcode').empty();
                        $('#qrcode').qrcode(data);
                    } else {
                        $('#qrcode').text("No se ha podido recuperar la información del QR");
                    }
                }
            })
    }

})
(jQuery);


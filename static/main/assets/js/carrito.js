/**
 * Created by grego on 7/08/19.
 */
(function ($) {
    /////////////////////////////////////////////////
    //Funciones jquery para el carrito
    /////////////////////////////////////////////////

    //metodo necesario para pasar el csrftoken por ajax
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

    //Variable donde se guarda el csrftoken para pasarlo por ajax
    var csrftoken = getCookie('csrftoken');


    //Ajusta el tamaño del p
    $('.fit-content').bind("keypress", function (e) {
        $(this).size = ( $(this).val().length > 4 ) ? $(this).val().length : 10;
    });

    //Al pulsar en los iconos de + o - en el carrito añadimos una a la cantidad o restamos y actualizamos el carrito
    //por si al añadir una unidad se activa alguna promoción
    $('#carrito .articulos i').click(function () {
        var $clicked = $(this);
        var up = new RegExp("up", 'g');
        var down = new RegExp("down", 'g');
        $(this).filter(function () {
            return this.id.match(up);
        }).each(function () {
            var id = $clicked.attr('id').split("cesta_count_up_")[1];
            $('#stock_cesta_' + id).text(parseInt($('#stock_cesta_' + id).text()) + 1);
            actualizarItem(id);
        });

        $(this).filter(function () {
            return this.id.match(down);
        }).each(function () {
            var id = $clicked.attr('id').split("cesta_count_down_")[1];
            var result = parseInt($('#stock_cesta_' + id).text()) - 1;
            if (result < 0) {
                result = 0;
            }
            $('#stock_cesta_' + id).text(result);
            actualizarItem(id);

        });
    });

    function actualizarItem(id) {
        $.ajax(
            {
                type: "POST",
                url: "/actualizar-carrito",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    item: id,
                    cantidad: $('#stock_cesta_' + id).text()
                },
                success: function (data) {
                    console.log(data);

                    $('#promo-activa-carrito').empty();
                    $('#promo-activa-carrito').removeClass("border-morado");

                    if (data != false) {
                        if (data['promo_activa'] == true) {
                            refreshPromoData(data);

                        } else {
                            refreshTotal(data);
                        }
                    }
                }
            })
    };

    function refreshPromoData(data) {
        var html = '<div class="row">';
        html += '<h4 class="black">Tienes una promoción activa!</h4>';
        if (data['promo_auto'] != '') {
            if (data['promo_auto'] == 'false') {
                html += '<h6>Código de la promocion:' + data['codigo'] + ' </h6>';
            } else {
                html += '<h6>Promoción automática</h6>';
            }
        }
        if (data['items_promo'].length > 0) {
            html += '<table class="no-valign"><tbody>';
            for (var i = 0; i < data['items_promo'].length; i++) {
                html += '<tr>';
                html += '<th scope="row">' + data['items_promo'][i]['nombre'] + '</th>';
                html += '<td>' + data['items_promo'][i]['precio_final'] + '</td>';
                html += '<td>' + data['items_promo'][i]['cantidad'] + ' Ud.</td>';
                html += '</tr>';
            }
            html += '</tbody></table>';
        } else {
            html += '<h4>' + data['promo_dcto_general'] + '</h4>';
        }

        html += '</div>';
        $('#carrito_total_value').text(data['total']);
        $('#promo-activa-carrito').append(html);
        $('#promo-activa-carrito').addClass("border-morado");

    }

    function refreshTotal(data) {
        $('#carrito_total_value').text(data['total']);

    }

    //Cuando pulsamos en aplicar código
    $('#carrito-apply-codigo').click(function () {
        if ($('#codigo_aplicado').val() == '') {
            alert('Introduzca un código')
        } else {
            applyCode();
        }
    });


    function applyCode() {
        //peticion de ajax para aplicar la promocion asociada al codigo introducido
        $.ajax(
            {
                type: "POST",
                url: "/actualizar-carrito",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    codigo: $('#codigo_aplicado').val()
                },
                success: function (data) {
                    if (data != false) {
                        console.log(data);
                        $('#carrito_total_value').text(data['total']);
                    } else {
                        alert("Codigo incorrecto");
                    }
                }
            })
    };


    ////////////////////////////////////////////////////
    //Funciones para la pasarela de pagos
    ////////////////////////////////////////////////////

    //Funciones para detectar que tipo de pago mostramos
    $('a.pago-stripe').click(function () {
        $('#iban-element').show();
        $('#aviso-pago').hide();
    });

    $('a.pago-normal').click(function () {
        $('#aviso-pago').show();
        $('#iban-element').hide();
    });

    //Funcion para guardar el valor en el formulario si es de prueba o no
    $('#pago-prueba').on('change', function () {
        if ($(this).prop("checked")) {
            $('#pago-prueba-value').val("true");
        } else {
            $('#pago-prueba-value').val("false");

        }
    });

    //Si el input del email está vacío, impide que se haga click en pagar
    $('#email-pasarela').on("change", function () {
        if ($(this).val() == "") {
            $('#eleccion-metodo').addClass("disabledcontent");
        } else {
            $('.ticket-email').val($(this).val());
            $('#eleccion-metodo').removeClass("disabledcontent");
        }
    });

    $('.disabledcontent').click(function () {
        alert("Rellene el campo email, por favor1;")
    });


    ////////////////////////////////////////////////////
    //Funciones añadir articulos al carrito
    ////////////////////////////////////////////////////
    $('#form-add-carrito').submit(function (e) {
        e.preventDefault();
        if ($('#unidades-articulo-pdv').val() <= 0) {
            alert("Seleccione al menos 1 unidad");
        } else {
            this.submit();
        }
    });
    // var selectedVariants = []; //ID donde guardo los ids de las variantes
    //
    // $('.variante-stock').click(function () {
    //     var $clicked = $(this);
    //     var id = $clicked.attr('id').split("variante-")[1];
    //     if ($('#variante-stock-' + id).text() != 0) {
    //         if (selectedVariants.indexOf(id) == -1) {
    //             selectedVariants.push(id);
    //             $(this).children('div').addClass("text-morado");
    //             $(this).children('div').addClass("border-morado");
    //             $('#selected-variants').val(selectedVariants);
    //
    //         } else {
    //             selectedVariants.splice($.inArray(id, selectedVariants), 1);
    //             $(this).children('div').removeClass("text-morado");
    //             $(this).children('div').removeClass("border-morado");
    //             if (selectedVariants.length == 0) {
    //                 $('#selected-variants').val('');
    //             }
    //         }
    //     }
    // });


})(jQuery);
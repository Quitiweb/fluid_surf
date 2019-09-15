/**
 * Created by grego on 22/08/19.
 */
(function ($) {
    //////////////////////////////////////////////////////////////////////////
    //Funcionalidades para colecciones
    //////////////////////////////////////////////////////////////////////////


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

    $(document).ready(function () {

        $('.loaded').trigger("click");
        $('.show-variantes-button').each(function () {
            $(this).queue(function () {
                $(this).css("backgound-color", "white")
            });
        });

    });

    //Impide que al pulsar intro se auto envie el formulario
    $('form').bind("keypress", function (e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            return false;
        }
    });

    //Activa o desactiva el formulario al hacer click en el botón editar
    $('#edit-col').click(function () {
        if ($(this).hasClass("shake-animate")) {
            $(this).removeClass("shake-animate");
            $(this).css("color", '#7629EF');
            $('label[for="edit-col"]').text("Desactivar edición");
        } else {
            $(this).addClass("shake-animate");
            $(this).css("color", '#000');
            $('label[for="edit-col"]').text("Activar edición");

        }
        if ($('#coleccion-form').hasClass("disabledcontent")) {
            $('#coleccion-form').removeClass("disabledcontent");
            $('#save-coleccion').removeClass("hide");
        } else {
            $('#coleccion-form').addClass("disabledcontent");
            $('#save-coleccion').addClass("hide");
        }
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

    ////////////////////////////////////
    //Funciones para el editor de stock
    ////////////////////////////////////
    var total = 0;
    var subtotal = 0;

    var variantesMap = Object();
    var articulosMap = Object();

    $('.show-variantes-button').click(function () {
        var id = $(this).attr("id").split("show-variantes-")[1];

        $('#variantes-' + id).toggleClass("hide");
    });

    $('.variante-stock-cantidad input').change(function () {
        var id = $(this).attr("id").split("-variante-stock-")[0];
        var id2 = $(this).attr("id").split("-variante-stock-")[1];

        if (id2 == "-1") {
            articulosMap[id] = $(this).val();
            var html = '<input type="hidden" id="articulos-map-" name="articulos-map" value="' + id + "-" + $(this).val() + '"/>'

        } else {
            variantesMap[id2] = $(this).val();
            var html = '<input type="hidden" id="variantes-map-" name="variantes-map" value="' + id2 + "-" + $(this).val() + '"/>'

        }

        $('#hidden-vals').append(html);

        recalcularSubTotal(id, id2);
        recalcularTotal();
    });

    function recalcularTotal() {
        total = 0;
        $('.variante-stock-cantidad input').each(function () {
            total += parseInt($(this).val());
        });

        $('#cantidad_total').text(total);
        $('#validar-pedido').val(total);

    }

    function recalcularSubTotal(id, id2) {
        subtotal = 0;
        var re = new RegExp(id + "-variante-stock-", 'g');
        $('.variante-stock-cantidad input').filter(function () {
            return this.id.match(re);
        }).each(function () {
            subtotal += parseInt($(this).val());
        });
        $('#input-total-' + id).text(subtotal);
    }
})
(jQuery);


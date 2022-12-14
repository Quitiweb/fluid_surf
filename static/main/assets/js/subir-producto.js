$(function() {
    $( "#id_fecha" ).datepicker({ dateFormat: 'dd/mm/yy', defaultDate: new Date() });
    $( "#id_fecha" ).val($.datepicker.formatDate('dd/mm/yy', new Date()));

var numFiles = 0;
$(document).on("change", "#id_imagenes", function(){
     numFiles += $("#id_imagenes")[0].files.length;
     console.log(numFiles);
     $("#textFiles").text("Has subido " + numFiles + " archivos.");
});

$(document).ready(function () {

    var url_string = window.location.href
    var url = new URL(url_string);
    if (url.searchParams.get("area__pais__nombre")) {
        $('#div-cont').addClass('d-none');
        $('#div-pais').addClass('d-none');
    } else {
        $('#linkAll').addClass('d-none');
    }

    $("#linkAll").click(function(e){
        e.preventDefault();
        $("#loadModal").modal();
        location.href = $(this).attr('href');
    });

    initSpots();

    $("#stripeModal").modal({
         backdrop: 'static',
         keyboard: false,
        show: true
    });

    $('#id_imagen0').on("change", function(){
        numFiles += $("#id_imagen0")[0].files.length;
        $('#form0').toggleClass('hide');
        $('#form1').toggleClass('hide');
        $(".textFiles").text("Has subido " + numFiles + " archivos.");
        $('#clearBtn').toggleClass('hide');
    });

    $('#id_imagen1').on("change", function(){
        numFiles += $("#id_imagen1")[0].files.length;
        $('#form1').toggleClass('hide');
        $('#form2').toggleClass('hide');
        $(".textFiles").text("Has subido " + numFiles + " archivos.");
    });

    $('#id_imagen2').on("change", function(){
        numFiles += $("#id_imagen2")[0].files.length;
        $('#form2').toggleClass('hide');
        $('#form3').toggleClass('hide');
        $(".textFiles").text("Has subido " + numFiles + " archivos.");
    });

    $('#id_imagen3').on("change", function(){
        numFiles += $("#id_imagen3")[0].files.length;
        $('#form3').toggleClass('hide');
        $('#form4').toggleClass('hide');
        $(".textFiles").text("Has subido " + numFiles + " archivos.");
    });

    $('#id_imagen4').on("change", function(){
        numFiles += $("#id_imagen4")[0].files.length;
        $('#form4').toggleClass('hide');
        $('#form5').toggleClass('hide');
        $(".textFiles").text("Has subido " + numFiles + " archivos.");
    });

    $('#id_imagen5').on("change", function(){
        numFiles += $("#id_imagen5")[0].files.length;
        $('#form5').toggleClass('hide');
        $('#form6').toggleClass('hide');
        $(".textFiles").text("Has subido " + numFiles + " archivos.");
    });

    $('#id_imagen6').on("change", function(){
        numFiles += $("#id_imagen6")[0].files.length;
        $('#form6').toggleClass('hide');
        $('#form7').toggleClass('hide');
        $(".textFiles").text("Has subido " + numFiles + " archivos.");
    });

    $('#id_imagen7').on("change", function(){
        numFiles += $("#id_imagen7")[0].files.length;
        $('#form7').toggleClass('hide');
        $('#form8').toggleClass('hide');
        $(".textFiles").text("Has subido " + numFiles + " archivos.");
    });

    $('#id_imagen8').on("change", function(){
        numFiles += $("#id_imagen8")[0].files.length;
        $('#form8').toggleClass('hide');
        $('#form9').toggleClass('hide');
        $(".textFiles").text("Has subido " + numFiles + " archivos.");
    });

    $('#id_imagen9').on("change", function(){
        numFiles += $("#id_imagen9")[0].files.length;
        $(".textFiles").text("Has subido " + numFiles + " archivos.");
    });

    // Eventos para la modificacion del nombre de manera dinamica

    var contenido = 'Europe-' + $.datepicker.formatDate('dd/mm/yy', new Date()) + '-' + $('#current').text();
    var username = $('#username').text();

    if (!$('#id_nombre').val())  {
        $('#id_nombre').val( username + '-' + contenido);
    } else {

        let temp = $('#id_nombre').val().split('-');

        temp2 = temp;

        reversed = temp2.reverse();

        console.log(temp, temp2, reversed);

        reversed[0]++;

        $( "#id_fecha" ).val(reversed[1]);

        for (let i=reversed.length - 1; i >= 0; i--) {
            console.log(reversed[i]);
            if (i > 2) {
                reversed.splice(i, 1);
            }
        }

        temp2 = reversed.reverse()

        contenido = temp2.toString().replace(/([,])/g, '-');

        $('#id_nombre').val( username + '-' + contenido);
    }

    $('#id_nombre').prop("readonly", true);

    $('#id_spot, #id_fecha').on("change", function(){
        var array = contenido.split('-');

        array[0] = $('#id_spot').val();
        array[1] = $('#id_fecha').val();

        contenido = array.toString().replace(/([,])/g, '-');

        $('#id_nombre').val( username + '-' + contenido);
    });


    // Evento para limpiar la lista de imagenes
    $('#clearBtn').on("click", function(){
        console.log('click!');
        $('#id_imagen0').val('');
        $('#id_imagen1').val('');
        $('#id_imagen2').val('');
        $('#id_imagen3').val('');
        $('#id_imagen4').val('');
        $('#id_imagen5').val('');
        $('#id_imagen6').val('');
        $('#id_imagen7').val('');
        $('#id_imagen8').val('');
        $('#id_imagen9').val('');

        $('#form0').removeClass('hide');
        $('#form1').addClass('hide');
        $('#form2').addClass('hide');
        $('#form3').addClass('hide');
        $('#form4').addClass('hide');
        $('#form5').addClass('hide');
        $('#form6').addClass('hide');
        $('#form7').addClass('hide');
        $('#form8').addClass('hide');
        $('#form9').addClass('hide');
        $('#clearBtn').addClass('hide');

        $(".textFiles").text("");
        numFiles = 0;
    });
});
});


$('#boton-submit').on("click", function(e){
    e.preventDefault();

    var contDftl = document.getElementById('selectCont').value;
    var paisDftl = document.getElementById('selectPais').value;
    var areaDftl = document.getElementById('selectArea').value;
    var spotDftl = document.getElementById('selectSpot').value;

    var text = '{' +
                  '"cont":' + '"' + contDftl + '"' +
                ', "pais": ' + '"' + paisDftl + '"' +
                ', "area": ' + '"' + areaDftl + '"' +
                ', "spot": ' + '"' + spotDftl + '"' +
                '}'

    localStorage.setItem('localSpot', text);

    console.log(localStorage.getItem('localSpot').cont)

    $("#form-add-product").submit();

});



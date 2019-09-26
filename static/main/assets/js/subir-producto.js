

$(document).ready(function () {
    $('#id_imagen0').on("change", function(){
        $('#id_imagen0').toggleClass('hide');
        $('#id_imagen1').toggleClass('hide');
        $('#textoFoto').text('segunda');
    });

    $('#id_imagen1').on("change", function(){
        $('#id_imagen1').toggleClass('hide');
        $('#id_imagen2').toggleClass('hide');
        $('#textoFoto').text('tercera');
    });

    $('#id_imagen2').on("change", function(){
        $('#id_imagen2').toggleClass('hide');
        $('#id_imagen3').toggleClass('hide');
        $('#textoFoto').text('cuarta');
    });

    $('#id_imagen3').on("change", function(){
        $('#id_imagen3').toggleClass('hide');
        $('#id_imagen4').toggleClass('hide');
        $('#textoFoto').text('quinta');
    });

    $('#id_imagen4').on("change", function(){
        $('#id_imagen4').toggleClass('hide');
        $('#id_imagen5').toggleClass('hide');
        $('#textoFoto').text('sexta');
    });

    $('#id_imagen5').on("change", function(){
        $('#id_imagen5').toggleClass('hide');
        $('#id_imagen6').toggleClass('hide');
        $('#textoFoto').text('septima');
    });

    $('#id_imagen6').on("change", function(){
        $('#id_imagen6').toggleClass('hide');
        $('#id_imagen7').toggleClass('hide');
        $('#textoFoto').text('octava');
    });

    $('#id_imagen7').on("change", function(){
        $('#id_imagen7').toggleClass('hide');
        $('#id_imagen8').toggleClass('hide');
        $('#textoFoto').text('novena');
    });

    $('#id_imagen8').on("change", function(){
        $('#id_imagen8').toggleClass('hide');
        $('#id_imagen9').toggleClass('hide');
        $('#textoFoto').text('ultima');
    });
});
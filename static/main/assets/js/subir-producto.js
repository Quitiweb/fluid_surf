$(function() {
    $( "#id_fecha" ).datepicker({ dateFormat: 'dd/mm/yy' });
} );

var numFiles = 0;
$(document).on("change", "#id_imagenes", function(){
     numFiles += $("#id_imagenes")[0].files.length;
     console.log(numFiles);
     $("#textFiles").text("Has subido " + numFiles + " archivos.");
});

$(document).ready(function () {
    $('#id_imagen0').on("change", function(){
        numFiles += $("#id_imagen0")[0].files.length;
        $('#form0').toggleClass('hide');
        $('#form1').toggleClass('hide');
        $(".textFiles").text("Has subido " + numFiles + " archivos.");
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
    
    $('#id_nombre').val($('#username').text() + '-Europa-Fecha-' + $('#current').text());

    $('#id_nombre').prop("readonly", true);

    $('#id_fecha').on("change", function(){
        var array = $('#id_nombre').val().split('-');

        array[2] = $('#id_fecha').val();

        $('#id_nombre').val(array.toString().replace(/([,])/g, '-'));

    });

    $('#id_spot').on("change", function(){
        var array = $('#id_nombre').val().split('-');

        array[1] = $('#id_spot').val();

        $('#id_nombre').val(array.toString().replace(/([,])/g, '-'));

    });

});
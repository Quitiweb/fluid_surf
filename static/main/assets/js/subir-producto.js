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
    if (!$('#id_nombre').val())  {
        $('#id_nombre').val($('#username').text() + '-EU-' + $.datepicker.formatDate('dd/mm/yy', new Date()) + '-' + $('#current').text());
    } else {
        var array = $('#id_nombre').val().split('-');

        array[3]++ ;

        $('#id_nombre').val(array.toString().replace(/([,])/g, '-'));

    }

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
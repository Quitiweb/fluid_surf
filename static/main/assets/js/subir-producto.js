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

    loadQS();

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

var continentes = [];
var paises = [];
var areas = [];
var spots = [];

function loadQS(contValue=null) {
    for (spot of spotQS) {
        continentes.push(spot['continente']);
        paises.push(spot['pais']);
        areas.push(spot['area']);
        spots.push(spot['spot']);
    }

    continentes = continentes.filter( onlyUnique )
    paises = paises.filter( onlyUnique )
    areas = areas.filter( onlyUnique )
    spots = spots.filter( onlyUnique )

    for (cont of continentes) {
        var opt = document.createElement("option");
        opt.value = cont;
        opt.innerHTML= cont;
        document.getElementById('selectCont').appendChild(opt)

        if (contValue) {
            document.getElementById('selectCont').value=contValue
        }

    }

    for (pais of paises) {
        var opt = document.createElement("option");
        opt.value = pais;
        opt.innerHTML= pais;
        document.getElementById('selectPais').appendChild(opt)
    }

    for (area of areas) {
        var opt = document.createElement("option");
        opt.value = area;
        opt.innerHTML= area;
        document.getElementById('selectArea').appendChild(opt)
    }

    for (spot of spots) {
        var opt = document.createElement("option");
        opt.value = spot;
        opt.innerHTML= spot;
        document.getElementById('selectSpot').appendChild(opt)
    }
}

function refreshContinente(value) {

    // for para obtener un spot aleatorio con ese pais
    for(spot of spotQS) {
        if(spot['continente'] == value) {
            contEx = spot;
        }
    }

    spotQS = spotQS.filter(function(el) {
        return el['continente'] === paisEx['continente']
    });

    $('select').empty()
    loadQS();
}

function refreshPais(value) {
     var paisEx;
     // for para obtener un spot aleatorio con ese pais
    for(spot of spotQS) {
        if(spot['pais'] == value) {
            paisEx = spot;
        }
    }

    spotQS = spotQS.filter(function(el) {
        return el['pais'] === paisEx['pais'] || el['continente'] === paisEx['continente']
    });

    $('select').empty()
    loadQS(paisEx['continente']);
}

/**
 *  Funcion para filtrar los distintos parents de los spots a un valor unico
 * @param value
 * @param index
 * @param self
 * @returns {boolean}
 */
function onlyUnique(value, index, self) {
    return self.indexOf(value) === index;
}

/**
 * Funcion para seleccionar un option concreto de un select
 * @param id
 * @param valueToSelect
 */
function selectElement(id, valueToSelect) {
    let element = document.getElementById(id);
    element.value = valueToSelect;
}

document.getElementById('selectPais').onchange = (e) => {
    $.ajax({
        url: "subir-producto",
    }).success(function(response) {
        paises = [];
        areas = [];
        spots = [];
        refreshPais(e.target.value);
    });
}
// TODO Cambio de continente
document.getElementById('selectCont').onchange = (e) => {
    // $.ajax({
    //     url: "subir-producto",
    // }).success(function(response) {
    //     paises = [];
    //     areas = [];
    //     spots = [];
    //     refreshContinente(e.target.value);
    // });
}
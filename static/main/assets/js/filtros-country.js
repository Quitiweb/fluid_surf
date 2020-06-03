function initSpots() {

    console.log('Spots loaded')

    if(localStorage.getItem('localCountry')) {
        let spot = JSON.parse(localStorage.getItem('localCountry'));
        loadQS(spot.cont, spot.pais);
    } else {
        loadQS();
    }
}


var continentes = [];
var paises = [];

function refreshQS() {
    spotQS = []

    for (spot of spotOG) {
        var result = JSON.parse(spot)
        spotQS.push(result)
    }
}

function loadQS(contValue= null, paisValue = null, areaValue = null, spotValue = null) {
    for (spot of spotQS) {
        continentes.push(spot['continente']);
        if (spot['pais']) { paises.push(spot['pais']); }
    }

    continentes = continentes.filter( onlyUnique )
    paises = paises.filter( onlyUnique )

    var opt = document.createElement("option");
    opt.value = '---';
    opt.innerHTML= '---';


    document.getElementById('selectPais').appendChild(opt)

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

        if (paisValue) {
            document.getElementById('selectPais').value=paisValue
        }
    }
}

function refreshContinente(value) {
    refreshQS();

    // for para obtener un spot aleatorio con ese pais
    for(spot of spotQS) {
        if(spot['continente'] == value) {
            contEx = spot;
        }
    }

    spotQS = spotQS.filter(function(el) {
        return el['continente'] === contEx['continente']
    });

    $('select').empty()

    for(spot of spotQS) {
        if(spot['continente'] !== contEx['continente']) {
            delete spot['pais'];
        }
    }

    loadQS(contEx['continente']);
}

function refreshPais(value) {
    refreshQS();

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

    for(spot of spotQS) {
        if(spot['pais'] !== paisEx['pais']) {
            delete spot['area'];
            delete spot['spot'];
        }
    }
    loadQS(paisEx['continente'], paisEx['pais']);
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

document.getElementById('selectCont').onchange = (e) => {
    $.ajax({
        url: "subir-producto",
    }).success(function(response) {
        paises = [];
        areas = [];
        spots = [];
        refreshContinente(e.target.value);
    });
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

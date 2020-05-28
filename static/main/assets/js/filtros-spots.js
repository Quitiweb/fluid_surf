function initSpots() {

    console.log('iniciados')

    if(localStorage.getItem('localSpot')) {
        let spot = JSON.parse(localStorage.getItem('localSpot'));
        loadQS(spot.cont, spot.pais, spot.area, spot.spot);
    } else {
        loadQS();
    }
}


var continentes = [];
var paises = [];
var areas = [];
var spots = [];

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
        if (spot['area']) { areas.push(spot['area']); }
        if (spot['spot']) { spots.push(spot['spot']); }
    }

    continentes = continentes.filter( onlyUnique )
    paises = paises.filter( onlyUnique )
    areas = areas.filter( onlyUnique )
    spots = spots.filter( onlyUnique )

    var opt = document.createElement("option");
    opt.value = '---';
    opt.innerHTML= '---';

    var opt2 = document.createElement("option");
    opt2.value = '---';
    opt2.innerHTML= '---';

    var opt3 = document.createElement("option");
    opt3.value = '---';
    opt3.innerHTML= '---';


    document.getElementById('selectPais').appendChild(opt)
    document.getElementById('selectArea').appendChild(opt2)
    document.getElementById('selectSpot').appendChild(opt3)

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

    for (area of areas) {
        var opt = document.createElement("option");
        opt.value = area;
        opt.innerHTML= area;
        document.getElementById('selectArea').appendChild(opt)

        if (areaValue) {
            document.getElementById('selectArea').value=areaValue
        }
    }

    for (spot of spots) {
        var opt = document.createElement("option");
        opt.value = spot;
        opt.innerHTML= spot;
        document.getElementById('selectSpot').appendChild(opt)

        if (spotValue) {
            document.getElementById('selectSpot').value=spotValue
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
            delete spot['area'];
            delete spot['spot'];
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

function refreshArea(value) {
     refreshQS();

     var areaEx;
     // for para obtener un spot aleatorio con ese pais
    for(spot of spotQS) {
        if(spot['area'] == value) {
            areaEx = spot;
        }
    }

   spotQS = spotQS.filter(function(el) {
        return el['continente'] === areaEx['continente']
            || el['pais'] === areaEx['pais']
            || el['area'] === areaEx['area']
    });

    $('select').empty()

    for(spot of spotQS) {
        if(spot['area'] !== areaEx['area']) {
            delete spot['spot'];
        }
    }
    loadQS(areaEx['continente'], areaEx['pais'], areaEx['area']);

}

function refreshSpot(value) {
     refreshQS();

     var spotEx;
     // for para obtener un spot aleatorio con ese pais
    for(spot of spotQS) {
        if(spot['spot'] == value) {
            spotEx = spot;
        }
    }

   spotQS = spotQS.filter(function(el) {
        return el['pais'] === spotEx['pais']
            || el['continente'] === spotEx['continente']
            || el['area'] === spotEx['area']
            || el['spot'] === spotEx['spot']
    });

    $('select').empty()

    loadQS(spotEx['continente'], spotEx['pais'], spotEx['area'], spotEx['spot']);

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

document.getElementById('selectArea').onchange = (e) => {
    $.ajax({
        url: "subir-producto",
    }).success(function(response) {
        paises = [];
        areas = [];
        spots = [];
        refreshArea(e.target.value);
    });
}

document.getElementById('selectSpot').onchange = (e) => {
    $.ajax({
        url: "subir-producto",
    }).success(function(response) {
        paises = [];
        areas = [];
        spots = [];
        refreshSpot(e.target.value);
    });
}
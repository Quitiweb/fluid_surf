$(document).ready(function () {
    initSpots();
});

$('#guardar').on("click", function(e){
    e.preventDefault();

    var contDftl = document.getElementById('selectCont').value;
    var paisDftl = document.getElementById('selectPais').value;

    var text = '{' +
                  '"cont":' + '"' + contDftl + '"' +
                ', "pais": ' + '"' + paisDftl + '"' +
                '}'

    localStorage.setItem('localCountry', text);

    console.log(localStorage.getItem('localCountry').cont)

    $("#form").submit();
});
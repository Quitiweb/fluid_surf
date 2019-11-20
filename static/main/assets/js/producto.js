$(function () {
    $( document ).ready(function() {
        $.each($('.for1'), function (i) {
            let link = $(this).find('img#' + (i + 1)).attr('src');
            $(this).attr('href', link);
        });


        let inicio = 0;
        $.each($('.for2par'), function () {
            inicio += 2;

            let link = $(this).find('img#' + (inicio)).attr('src');
            $(this).attr('href', link);
        });

        let inicioImpar = -1;
        $.each($('.for2impar'), function () {
                inicioImpar += 2;

                let link = $(this).find('img#' + (inicioImpar)).attr('src');
                $(this).attr('href', link);
        });
    });
});
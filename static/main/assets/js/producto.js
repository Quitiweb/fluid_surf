$(function () {
    $( document ).ready(function() {
        $.each($('.for1'), function (i) {
            let link = $(this).find('img#' + (i + 1)).attr('src');
            $(this).attr('href', link);
        });

    });
});
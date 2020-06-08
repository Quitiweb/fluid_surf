$(document).ready(function () {

    $(document).ready(function(){
        var url_string = window.location.href
        var url = new URL(url_string);
        if (url.searchParams.get("area__pais__nombre")) {
            $('#div-cont').addClass('d-none');
            $('#div-pais').addClass('d-none')
        }

        if (scroll) {
            $('html, body').animate({
                scrollTop: $("#resultados").offset().top
            }, 1000);
        }

        $("#linkAll").click(function(e){
            e.preventDefault();
            $("#exampleModal").modal();
            location.href = $(this).attr('href');
        });

        $("#buscar").click(function(e){
            e.preventDefault();
            if (!url.searchParams.get("area__pais__nombre")) {
                $("#exampleModal").modal();
            }
            $('#buscar-form').click();
        });
    });


    $('.img-top').hide().removeClass('d-none').fadeIn(2000);

    $('.img-top').on('click', function(e) {
       if(!$(this).hasClass('small-search-pic')) {
            $('.img-top').addClass('small-search-pic');
            $('.foto-texto').fadeOut();
            $('.bar').removeClass('d-none');
       }
       if($(this).hasClass('foto')) {
            $('#buscar').attr('value', 'Buscar fotografos').prop("disabled", false);
            $('#buscar-form').attr('name', 'buscar-foto');
            $('.foto').addClass('selected-pic');
            $('.surf').removeClass('selected-pic');
            $('.bar').removeClass('bar-surf');
            $('.bar').addClass('bar-foto');
       } else {
            $('#buscar').attr('value', 'Encontrar tus fotos').prop("disabled", false);
            $('#buscar-form').attr('name', 'buscar-surf');
            $('.surf').addClass('selected-pic');
            $('.foto').removeClass('selected-pic');
            $('.bar').addClass('bar-surf');
            $('.bar').removeClass('bar-foto');
       }
    });

    initSpots();
});

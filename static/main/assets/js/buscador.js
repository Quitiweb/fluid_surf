$(document).ready(function () {

    $(document).ready(function(){

       console.log(scroll);

        if (scroll) {
            $('html, body').animate({
                scrollTop: $("#resultados").offset().top
            }, 1000);
      }
   });


    $('.img-top').hide().removeClass('d-none').fadeIn(2000);

    $('.img-top').on('click', function(e) {
       if(!$(this).hasClass('small-search-pic')) {
            $('.img-top').addClass('small-search-pic');
            $('.foto-texto').fadeOut();
            $('.bar').removeClass('d-none');
       }
       if($(this).hasClass('foto')) {
            $('#buscar').attr('name', 'buscar-foto').attr('value', 'Buscar fotografos');
            $('.foto').addClass('selected-pic');
            $('.surf').removeClass('selected-pic');
            $('.bar').removeClass('bar-surf');
            $('.bar').addClass('bar-foto');
       } else {
            $('#buscar').attr('name', 'buscar-surf').attr('value', 'Encontrar tus fotos');
            $('.surf').addClass('selected-pic');
            $('.foto').removeClass('selected-pic');
            $('.bar').addClass('bar-surf');
            $('.bar').removeClass('bar-foto');
       }
    });

    initSpots();
});

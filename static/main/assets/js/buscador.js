$(document).ready(function () {
    $('.img-top').hide().removeClass('d-none').fadeIn(2000);

    $('.img-top').on('click', function(e) {
       if(!$(this).hasClass('small-search-pic')) {
            $('.img-top').addClass('small-search-pic');
            $('.foto-texto').fadeOut();
       }
        console.log('prev');
       if($(this).hasClass('foto')) {
           $('.surf-form').addClass('d-none');
           $('.foto-form').removeClass('d-none');
       } else {
           $('.foto-form').addClass('d-none');
           $('.surf-form').removeClass('d-none');
       }
    });
});

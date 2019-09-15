(function($) {

    // Desmarcar los Radio button al hacer click en ¿Quién eres?
        $("#id_quien_eres input:radio").on('change', function(){
            $('#id_quien_eres .checked').removeClass('checked');
            $(this).parent().parent().toggleClass("checked");
        });

    // Desmarcar los Radio button al hacer click en ¿Qué buscas?
        $("#id_que_buscas input:radio").on('change', function(){
            $('#id_que_buscas .checked').removeClass('checked');
            $(this).parent().parent().toggleClass("checked");
        });

    // Marcar/Desmarcar los Checkbox al hacer click en ellos
        $(":checkbox").on('change', function(){
            $(this).parent().parent().toggleClass("checked");
        });

    // Mostrar/Ocultar los elementos
        $('input:radio#id_quien_eres_0').on('change', function(){
            $('.espacio').slideUp('slow');
            $('.servicios').slideUp('slow');
            $('.marca').slideDown('slow');
        });
        $('input:radio#id_quien_eres_1').on('change', function(){
            $('.marca').slideUp('slow');
            $('.servicios').slideUp('slow');
            $('.espacio').slideDown('slow');
        });
        $('input:radio#id_quien_eres_2').on('change', function(){
            $('.marca').slideUp('slow');
            $('.espacio').slideUp('slow');
            $('.servicios').slideDown('slow');
        });

})(jQuery);
$(function() {
    $(document).ready(function () {

        $('footer').hide();

         $("#btn-foto>img").hover(function(){
            $('#info-foto').fadeIn();
         });

         $("#btn-foto").mouseout(function(){
            $('#info-foto').fadeOut();
         });

         $("#btn-surf>img").hover(function(){
            $('#info-surf').fadeIn();
         });

         $("#btn-surf").mouseout(function(){
            $('#info-surf').fadeOut();
         });
    });
});
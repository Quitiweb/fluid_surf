$(function() {
    $(document).ready(function () {
         $("#btn-foto").hover(function(){
            $('#info-foto').fadeIn();
         });

         $("#btn-foto").mouseout(function(){
            $('#info-foto').fadeOut();
         });

         $("#btn-surf").hover(function(){
            $('#info-surf').fadeIn();
         });

         $("#btn-surf").mouseout(function(){
            $('#info-surf').fadeOut();
         });
    });
});
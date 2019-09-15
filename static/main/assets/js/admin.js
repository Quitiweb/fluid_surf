jQuery(document).ready(function(){
    $("#id_titulo").keyup(function(){
        $("#id_slug").val(
        this.value
            .toLowerCase()
            .replace(/[^\w ]+/g,'')
            .replace(/ +/g,'-')
        );
    });
});
console.log('hola buenas')

//TODO Comprobar que se controle que no se puedan mas de 10 imagenes
//TODO Comprobar el tamanio individual de cada imagen y el del conjunto de ellas.
$(document).on("change", "#id_imagenes", function(){
     var numFiles = $("#id_imagenes")[0].files.length;
     console.log(numFiles);
     $("#textFiles").text("Has subido " + numFiles + " archivos.");
});
$( "#fileInput" ).change(function() {
  $('#exampleModal').modal('show')
});

$('#buscar').click(function(e){
  $('#exampleModal').addClass('d-none');
  $('.modal-backdrop').addClass('d-none');
  $('#exampleModal').remove();
});

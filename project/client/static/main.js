// custom javascript

$(document).ready(function() {
  console.log('Sanity Check!');
  $("#list")
    .rating({step:1, size:'xs', showClear:false, showCaption:false})
    .rating('update', 3).val();
});
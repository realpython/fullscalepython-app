// custom javascript

$(document).ready(function() {
  $('#bathroom-rating #star-input').on('rating.change', function(event, value, caption) {
    // send ajax request
    $.ajax({
      method: 'POST',
      url: '/bathrooms/',
      data: JSON.stringify({
        name: $(this).closest('tr').find('#bathroom-name').text(),
        rating: parseInt(value)
      }),
      dataType: 'json',
      contentType: 'application/json',
    })
    .done(function(data) {
      location.reload();
    });
  });
});
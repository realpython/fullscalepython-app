// custom javascript

$(document).ready(function() {
  $('#bathroom-rating #star-input').on('rating.change', function(event, value, caption) {
    // get current values
    var $this = $(this);
    var $currentValue = $this.attr('value');
    var $currentRatingCount = $this.parent().parent().next().find('#rating-count');
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
      var message = createMessage('success', data.message);
      $('#custom-message').html(message);
      $this.rating('update', data.data.rating).val();
      $currentRatingCount.html(data.data.count);
    })
    .fail(function(err) {
      var message = createMessage(
        'danger', 'You must be logged in to rate.');
      $('#custom-message').html(message);
      $this.rating('update', $currentValue).val();
    });
  });
});

function createMessage(category, message) {
  html = '<br>';
  html += '<div class="row">';
  html += '<div class="col-md-12">';
  html += '<div class="alert alert-' +  category + '">';
  html += '<a class="close" title="Close" href="#" data-dismiss="alert">&times;</a>';
  html += message;
  html += '</div>';
  html += '</div>';
  html += '</div>';
  return html;
}

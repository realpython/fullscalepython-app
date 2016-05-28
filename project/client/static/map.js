$(document).ready(function () {
  initializeMap();
  $(document).on('click', '#modal-link', function() {
    var title = ($(this)).data('title');
    var address = ($(this)).data('address');
    var rating = ($(this)).data('rating');
    var rating_count = ($(this)).data('rating-count');
    createModal(title, address, rating, rating_count);
  });
});

var infowindow;

// initialize the map
function initializeMap() {
  var centerMap = new google.maps.LatLng(40.7829, -73.9654);
  var myOptions = {
    zoom: 12,
    center: centerMap,
  };
  var map = new google.maps.Map(document.getElementById('map-canvas'), myOptions);
  // grab data points from the API
  $.getJSON('http://localhost:5000/bathrooms')
  .done(function(bathrooms) {
    var allBathrooms = bathrooms.map(function(bathroom) {
      parsedData = JSON.parse(bathroom.latlong.replace(/'/g, '"'));
      latlong = parsedData.lat + ',' + parsedData.lng;
      return {
        latlong: latlong,
        name: bathroom.name,
        address: bathroom.location,
        rating: bathroom.rating,
        rating_count: bathroom.rating_count
      };
    });
    // createModal();
    setMarkers(map, allBathrooms);
    infowindow = new google.maps.InfoWindow({
      content: "loading..."
    });
  });
}

// loop through the data returned from the api, add new marker
function setMarkers(map, bathrooms) {
  var markers = [];
  bathrooms.forEach(function(bathroom) {
    $.getJSON('https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyDRG3RXgL59DvWnxRgKhPDQLKzhYbD3R9E&address='+bathroom.latlong)
    .done(function(data) {
      var p = data.results[0].geometry.location;
      var latlng = new google.maps.LatLng(p.lat, p.lng);
      // create new marker
      var marker = new google.maps.Marker({
        position: latlng,
        map: map,
        title: bathroom.name
      });
      markers.push(marker);
      google.maps.event.addListener(marker, 'click', function() {
        infowindow.setContent('<h4>' + this.title + '</h4>' + createModalLink(bathroom));
        infowindow.open(map, this);
      });
      // click to zoom
      $('#list li').on('click', function() {
        map.setZoom(12);
        map.setCenter(new google.maps.LatLng(40.7829, -73.9654));
        var bathroomName = $(this).html();
        var bathroomAddress = $(this).data('address');
        var bathroomRating = $(this).data('rating');
        var bathroomRatingCount = $(this).data('rating-count');
        var bathroomObject = {
          name: bathroomName,
          address: bathroomAddress,
          rating: bathroomRating,
          rating_count: bathroomRatingCount
        };
        markers.forEach(function(marker) {
          if(marker.title === bathroomName) {
            map.setZoom(13);
            map.setCenter(marker.position);
            infowindow.setContent('<h4>' + bathroomName + '</h4>' + createModalLink(bathroomObject));
            infowindow.open(map, marker);
          }
        });
      });
    });
  });
}

function createModalLink(bathroomInfo) {
  html = '<a id="modal-link"' +
    'data-title="' + bathroomInfo.name +
    '" data-address="' + bathroomInfo.address +
    '" data-rating="' + bathroomInfo.rating +
    '" data-rating-count="' + bathroomInfo.rating_count +
    '">View Details</a>';
  return html;
}

function createModal(title, address, rating, rating_count) {
  html = '<div class="modal fade" id="modalWindow" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">';
  html += '<div class="modal-dialog" role="document">';
  html += '<div class="modal-content">';
  html += '<div class="modal-header">';
  html += '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
  html += '<h4 class="modal-title" id="myModalLabel">' + title +'</h4>';
  html += '</div>';
  html += '<div class="modal-body">';
  html += address + '<br><br>';
  html += 'Avergage Rating: ' + rating;
  html += '<br>' + rating_count + ' total votes';
  html += '</div>';
  html += '</div>';
  html += '</div>';
  $('#myModal').html('');
  $('#myModal').html(html);
  $('#modalWindow').modal();
}
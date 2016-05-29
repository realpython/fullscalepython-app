$(document).ready(function () {
  initializeMap();
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
        location: bathroom.location,
        rating: bathroom.rating,
        ratingCount: bathroom.rating_count
      };
    });
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
        $('#bathroom-list tr').removeClass('highlight');
        $('#bathroom-list tr').each(function() {
          if($(this).find('td:first').text() === marker.title) {
            $(this).addClass('highlight');
          }
        });
        infowindow.setContent('<h4>' + this.title + '</h4><br>' + bathroom.location);
        infowindow.open(map, this);
      });
      google.maps.event.addListener(infowindow, 'closeclick', function() {
          $('#bathroom-list tr').removeClass('highlight');
      });
      // click to zoom
      $('#bathroom-list #bathroom-name').on('click', function() {
        map.setZoom(12);
        map.setCenter(new google.maps.LatLng(40.7829, -73.9654));
        var bathroomName = $(this).html();
        var bathroomLocation = $(this).data('location');
        markers.forEach(function(marker) {
          if(marker.title === bathroomName) {
            map.setZoom(13);
            map.setCenter(marker.position);
        infowindow.setContent('<h4>' + bathroomName + '</h4><br>' + bathroomLocation);
            infowindow.open(map, marker);
          }
        });
      });
      // highlight row
      $('#bathroom-list tr').on('click', function() {
        $('#bathroom-list tr').removeClass('highlight');
        $(this).addClass('highlight');
      });
    });
  });
}

function createLink(bathroomName) {
  var formattedName = bathroomName.toLowerCase().replace(/ /g, '-');
  return '<a href="/bathrooms/all/#' + formattedName + '">View Details</a>';
}
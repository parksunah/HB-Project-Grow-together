"use strict";

  function initMap() {

    const mapLocation = { lat: $("#map").data("map").lat, 
                          lng: $("#map").data("map").lng }; 
    const locationName = $("#map").data("map").name;
    
    const map = new google.maps.Map(
        document.getElementById('map'), {zoom: 16, center: mapLocation});
    const marker = new google.maps.Marker({position: mapLocation, map: map});
    let infoWindow = new google.maps.InfoWindow({
        content: locationName
      });
    marker.addListener('click', function() {
        infoWindow.open(map, marker);
      });
  }
  const address = $("#map").data("map").address;
  const locationName = $("#map").data("map").name;
  $("#address").html(address);
  $("#location-name").html(locationName);
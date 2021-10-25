let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -26.915, lng: -48.666 },
    zoom: 15,
  });
}
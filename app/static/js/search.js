var map = L.map('mapid').setView([37.7749, -122.4194], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
  maxZoom: 18,
}).addTo(map);

var marker;

map.on('click', function(e) {
  if (marker) {
    map.removeLayer(marker);
  }
  marker = L.marker(e.latlng).addTo(map);
  document.getElementById('lat').value = e.latlng.lat;
  document.getElementById('lng').value = e.latlng.lng;
});

document.getElementById('search-btn').addEventListener('click', function() {
  document.getElementById('submit-btn').click();
});


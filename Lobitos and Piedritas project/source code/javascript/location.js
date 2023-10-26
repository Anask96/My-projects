/* A 10 second timeout has been added for all devices.
 * If a device cannot load within 10 seconds map is turned off and a place holder text added */
var slowLoad = window.setTimeout(function () {
  document.getElementById('mapsource').src = "";
  var element = document.getElementById('mapdiv');
  element.innerHTML = "<p>Due to a slow connection we are unable to load to load the map please navigate back to the report page</p>";
  window.stop();
}, 10000);

window.addEventListener('load', function () {
  window.clearTimeout(slowLoad);
  getMarker();
}, false);
/* Opens side menu */
function openSideBar() {
  document.getElementById('sidebar').style.width = "200px";
  document.getElementById('menubtn').style.color = "white";
}
/* Closes side menu*/
function closeSideBar() {
  document.getElementById('sidebar').style.width = "0";
  document.getElementById('menubtn').style.color = "none";
}
/* Get current position */
function getMarker(signal) {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(openMap);
  } else {
    alert("Geolocation is not supported by this browser.");
  }
}
/* Load Map */
function openMap(currPosition) {
  var longitude = currPosition.coords.longitude;
  var latitude = currPosition.coords.latitude;

  map = new OpenLayers.Map("mapdiv");
  map.addLayer(new OpenLayers.Layer.OSM());

  var lonLat = new OpenLayers.LonLat(longitude, latitude)
    .transform(
      new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
      map.getProjectionObject() // to Spherical Mercator Projection
    );

  var zoom = 16;

  var markers = new OpenLayers.Layer.Markers("Markers");
  map.addLayer(markers);

  markers.addMarker(new OpenLayers.Marker(lonLat));

  map.setCenter(lonLat, zoom);
}
/* Change to spanish or back to English */
function changeLanguage() {
  lang = document.documentElement.lang;
  if (lang == 'en') {
    changeToSpanish();
  } else {
    window.location.reload(true);
    document.documentElement.lang = "en";
  }
}

function changeToSpanish() {
  document.documentElement.lang = "es";
  document.getElementById('title').innerHTML = "Ubicación";
  document.getElementById('pointsSide').innerHTML = "0 Puntos";
  document.getElementById('signinSide').innerHTML = "Iniciar sesión";
  document.getElementById('homeSide').innerHTML = "Inicio";
  document.getElementById('reportSide').innerHTML = "Informar";
  document.getElementById('collectSide').innerHTML = "Recoger";
  document.getElementById('dropoffSide').innerHTML = "Punto de Entrega";
  document.getElementById('homelink').innerHTML = "Inicio";
  document.getElementById('toptext').innerHTML = "Eliga la Ubicación en el Mapa";
  document.getElementById('x').innerHTML = 'Cancelar <i class="fas fa-times-circle loseIcon"></i>';
  document.getElementById('tick').innerHTML = 'Confirmar <i class="fas fa-check-circle loseIcon"></i>';

}

function previousPage() {
  location.href = "reporting.html"
}
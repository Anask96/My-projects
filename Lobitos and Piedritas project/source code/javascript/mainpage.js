//Anything longer than 10 seconds stops the page from loading any further resources other than the basic html elements and basic css but still downloads necessary icons in the background
var slowLoad = window.setTimeout(function () {
  window.stop();
}, 10000);

window.addEventListener('load', function () {
  window.clearTimeout(slowLoad);
}, false);

/* Open side menu */
function openSideBar() {
  document.getElementById('sidebar').style.width = "200px";
  document.getElementById('menubtn').style.color = "white";
}
/* Close Side menu */
function closeSideBar() {
  document.getElementById('sidebar').style.width = "0";
  document.getElementById('menubtn').style.color = "none";
}

/* Navigate to corresponding pages */
function routeToPage(button_clicked) {
  if (button_clicked === 'reporting') {
    window.open("../html/reporting.html", "_self");
  } else {
    window.open("../html/collection.html", "_self");
  }
}
/* Change the language of html */
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
  document.getElementById('title').innerHTML = "Inicio";
  document.getElementById('pointsSide').innerHTML = "0 Puntos";
  document.getElementById('signinSide').innerHTML = "Iniciar sesión";
  document.getElementById('homeSide').innerHTML = "Inicio";
  document.getElementById('reportSide').innerHTML = "Informar";
  document.getElementById('collectSide').innerHTML = "Recoger";
  document.getElementById('dropoffSide').innerHTML = "Punto de Entrega";
  document.getElementById('homelink').innerHTML = "Inicio";
  document.getElementById('reporting').innerHTML = "Informar <i class=\"fas fa-trash-alt\"></i>";
  document.getElementById('reptext').innerHTML = "Envíe un informe de cualquier basura que vea. De esta forma los voluntarios pueden recogerlo. ¡Ayude a mantener limpio el hermoso paisaje de Lobitos y Piedritas!";
  document.getElementById('collecting').innerHTML = "Recoger <i class=\"fas fa-pencil-alt\"></i>";
  document.getElementById('coltext').innerHTML = "¿Quiere ayudar a limpiar y ganar recompensas? Vea los informes de basura y elija cuál desea recoger. Deposite su basura en la ubicación de un proveedor.";
  document.getElementById('about').innerHTML = "Acerca de";
  document.getElementById('aboutText').innerHTML = "Esta página web fue creada para permitir que las personas informen y recogan basura en Lobitos, Piedritas y sitios cercanos. La basura recogida se puede depositar en cualquier ubicación asociada, donde puede ganar puntos. Estos puntos se pueden utilizar para obtener recompensas en los distintos socios.";
  document.getElementById('disclaimer').innerHTML = "Descargo de responsabilidad";
  document.getElementById('distext').innerHTML = "Tenga cuidado y no recoja ni informe cualquier basura que pueda ser dañina o peligrosa.";
  document.getElementById('email').innerHTML = "Correo electrónico: mesadperates@munilobitos.gob.pe";

}
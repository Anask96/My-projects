/* Hide the popup when loading the page so it is not seen */
window.addEventListener('load', (event) => {
  document.getElementById('uploadPopUp').style.visibility = 'hidden';
  document.getElementById('gridContainer').style.visibility = 'hidden';
  document.getElementById('thumbnailcont').style.visibility = 'hidden';
});
/* Make popup visible and blur out the background */
function uploadPopUp() {
  if (document.getElementById('thumbnailcont').style.visibility === "visible") {
    document.getElementById('thumbnailcont').style.visibility = 'hidden';
  }
  document.getElementById('cont').style.filter = "blur(8px)";
  document.getElementById('submit').style.filter = "blur(8px)";
  document.getElementById('exit').style.filter = "blur(8px)";
  document.getElementById('uploadPopUp').style.opacity = 1;
  document.getElementById('gridContainer').style.opacity = 1;
  document.getElementById('uploadPopUp').style.visibility = 'visible';
  document.getElementById('gridContainer').style.visibility = 'visible';

}
/* Make thumbnail and placeholder picture available */
function inputPlaceHolderPic() {
  document.getElementById('thumbnailcont').style.visibility = 'visible';
  document.getElementById('gridContainer').style.visibility = 'hidden';
}
/* Close the pop up and return to normal page */
function closePopUp() {
  document.getElementById('cont').style.filter = "none";
  document.getElementById('submit').style.filter = "none";
  document.getElementById('exit').style.filter = "none";
  document.getElementById('uploadPopUp').style.visibility = 'hidden';
  document.getElementById('thumbnailcont').style.visibility = 'hidden';
  document.getElementById('gridContainer').style.visibility = 'hidden';
  document.getElementById('opText2').style.color = "#004f9e";
  document.getElementById('opText2').innerHTML = "Picture Successfully Uploaded!";
}
/* Close the pop up and return to normal page through exit button*/
function closePopUpExit() {
  document.getElementById('cont').style.filter = "none";
  document.getElementById('submit').style.filter = "none";
  document.getElementById('exit').style.filter = "none";
  document.getElementById('uploadPopUp').style.visibility = 'hidden';
  document.getElementById('thumbnailcont').style.visibility = 'hidden';
  document.getElementById('gridContainer').style.visibility = 'hidden';
}
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

// Checks whether user has inputted all the required information to submit a form.
function acceptAll() {
  var text = document.getElementById('wheretextarea').value;
  if (text.length == 0) {
    window.alert("Please enter a description of where the trash is located!");
    return;
  }

  var x = false;
  var children = document.getElementById('checkboxpos').children;
  for (var i = 0; i < children.length; i++) {
    if (children[i].children[0].checked) {
      x = true;
    }
  }

  if (!x) {
    window.alert("Please choose at least one type of trash!");
    return;
  }

  x = false;
  children = document.getElementById('radioButtons').children;
  for (var i = 0; i < children.length; i++) {
    if (children[i].children[0].children[0].checked) {
      x = true;
    }
  }

  if (!x) {
    window.alert("Please select the size of the trash!");
    return;
  }

  document.getElementById('submit').innerHTML = "SUBMITTED!";

  setTimeout(() => location.reload(), 3000);
}

function previousPage() {
  location.href = "mainpage.html"
}

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
  document.getElementById('title').innerHTML = "Informar";
  document.getElementById('pointsSide').innerHTML = "0 Puntos";
  document.getElementById('signinSide').innerHTML = "Iniciar sesión";
  document.getElementById('homeSide').innerHTML = "Inicio";
  document.getElementById('reportSide').innerHTML = "Informar";
  document.getElementById('collectSide').innerHTML = "Recoger";
  document.getElementById('dropoffSide').innerHTML = "Punto de Entrega";
  document.getElementById('homelink').innerHTML = "Inicio";
  document.getElementById('heading1').innerHTML = "¿Dónde está la basura?";
  document.getElementById('locationDes').innerHTML = "Describa la ubicación";
  document.getElementById('reqText').innerHTML = "*Obligatorio";
  document.getElementById('opText').innerHTML = "Opcional";
  document.getElementById('selectmapbtn').innerHTML = 'Seleccione en el Mapa <i class="fas fa-map-marker-alt loseIcon"></i>';
  document.getElementById('heading2').innerHTML = "¿Qué es?";
  document.getElementById('typeTrash').innerHTML = "Tipo de basura";
  document.getElementById('reqText2').innerHTML = "*Obligatorio";
  document.getElementById('paper').innerHTML = "Papel";
  document.getElementById('plastic').innerHTML = "Plástico";
  document.getElementById('metal').innerHTML = "Metal";
  document.getElementById('wood').innerHTML = "Madera";
  document.getElementById('glass').innerHTML = "Vidrio";
  document.getElementById('electronic').innerHTML = "Electrónico";
  document.getElementById('other').innerHTML = "Otro";
  document.getElementById('size').innerHTML = "Tamaño";
  document.getElementById('reqText3').innerHTML = "*Obligatorio";
  document.getElementById('small').innerHTML = "Pequeño";
  document.getElementById('medium').innerHTML = "Mediano";
  document.getElementById('large').innerHTML = "Grande";
  document.getElementById('opText2').innerHTML = "Opcional";
  document.getElementById('customuploadbtn').innerHTML = 'Subir Foto <i class="fas fa-upload loseIcon"></i>';
  document.getElementById('uploadtext').innerHTML = "Subir desde su dispositivo";
  document.getElementById('uploadbtn').innerHTML = 'Seleccionar <i class="far fa-file-image loseIcon"></i>';
  document.getElementById('selectagain').innerHTML = 'Seleccionar <i class="fas fa-redo-alt loseIcon"></i>';
  document.getElementById('confirm').innerHTML = 'Confirmar <i class="fas fa-check-circle loseIcon"></i>';
  document.getElementById('submit').innerHTML = 'ENVIAR <i class="fas fa-check-circle loseIcon" id="subIcon"></i>';
  document.getElementById('exit').innerHTML = 'SALIR <i class="fas fa-times-circle loseIcon" id="cancelIcon"></i>';
}
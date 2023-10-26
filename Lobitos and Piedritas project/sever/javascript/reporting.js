function openSideBar() {
  document.getElementById('sidebar').style.width = "200px";
  document.getElementById('menubtn').style.color = "white";
}
function closeSideBar() {
  document.getElementById('sidebar').style.width = "0";
  document.getElementById('menubtn').style.color = "none";
}

function changeLanguage(){
  lang = document.documentElement.lang;
  if (lang == 'en') {
    changeToSpanish();
  }
  else {
    window.location.reload(true);
    document.documentElement.lang = "en";
  }
}

function changeToSpanish(){
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
  document.getElementById('selectmapbtn').innerHTML = "Seleccione en el Mapa";
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
  document.getElementById('customuploadbtn').innerHTML = "Subir Foto";
  document.getElementById('uploadtext').innerHTML = "Subir desde su dispositivo";
  document.getElementById('uploadbtn').innerHTML = "Seleccionar";
  document.getElementById('selectagain').innerHTML = "Seleccionar de nuevo";
  document.getElementById('confirm').innerHTML = "Confirmar";
  document.getElementById('submit').innerHTML = "Enviar";




}

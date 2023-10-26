let languages = [
  {
    "langName":"Spanish",
    "collectTrash":"Recoger Basura",
    "trashCollected":"Basura Recogida &#10003;",
    "goBack":"&laquo; Volver a la lista",
    "trashLoc":"Ubicación de la basura:",
    "trashDisc":"Descripción de la basura:",
    "trashType":"Tipo de basura:",
    "trashSize":"Tamaño de la basura:"
  },
  {
    "langName":"English",
    "collectTrash":"Collect Trash",
    "trashCollected":"Trash Collected &#10003;",
    "goBack":"&laquo; Go Back To List",
    "trashLoc":"Trash Location:",
    "trashDisc":"Trash Discription:",
    "trashType":"Trash Type:",
    "trashSize":"Trash Size:"
  }
]

let trash = {
  "where": "Roundabout towards Villa El Pescadora right before Primavera. Bottles are behind the yellow house",
  "locationPointer": "true",
  "location": {lat:51.982934, lon:4.367389},
  "img": "trash.png", // Add the img for the trash here
  "page": "trash.html",
  "type": "Plastic",
  "size": "Medium"
}

var openMap = true;
var slowLoad = window.setTimeout( function() {
  openMap = false;
  window.stop();
}, 10000);

if(!navigator.geolocation && trash.locationPointer == false){
  openMap = false;
}

function openSideBar() {
  document.getElementById('sidebar').style.width = "200px";
  document.getElementById('menubtn').style.color = "white";
}
function closeSideBar() {
  document.getElementById('sidebar').style.width = "0";
  document.getElementById('menubtn').style.color = "none";
}
function previousPage() {
  location.href = "collection.html"
}


window.addEventListener("load",function() {

  if(openMap){
    map = new OpenLayers.Map("mapdiv");
    map.addLayer(new OpenLayers.Layer.OSM());
    var lonLat
    var zoom=16;
    lonLat = new OpenLayers.LonLat(trash.location.lon,trash.location.lat)
          .transform(
            new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
            map.getProjectionObject() // to Spherical Mercator Projection
          );
    var markers = new OpenLayers.Layer.Markers( "Markers" );
    map.addLayer(markers);
    markers.addMarker(new OpenLayers.Marker(lonLat));
    map.setCenter (lonLat, zoom);
  }
  else {
    var img = document.createElement('img')
    img.setAttribute("src","noMap.png")// This is the photo to be used incase the map didnt open
    img.setAttribute("alt","Oops! Cant open map")
    img.setAttribute("style","width:100%;height:100%;")
    document.getElementById('mapdiv').setAttribute("style","background-color: #0607354a;")
    document.getElementById('mapdiv').appendChild(img)
  }

  var img = document.getElementById('trashImg')
  img.setAttribute("src",trash.img)

  var p = document.createElement('P')
  var textnode = document.createTextNode(trash.where);
  p.appendChild(textnode);
  p.setAttribute("style","font-weight: normal;")
  var div  = document.getElementById('where')
  div.appendChild(p);

  p = document.createElement('P')
  textnode = document.createTextNode(trash.type);
  p.appendChild(textnode);
  p.setAttribute("style","font-weight: normal;flex: 1;")
  div  = document.getElementById('type')
  div.appendChild(p);

  p = document.createElement('P')
  textnode = document.createTextNode(trash.size);
  p.appendChild(textnode);
  p.setAttribute("style","font-weight: normal;flex: 1;")
  div  = document.getElementById('size')
  div.appendChild(p);

  var i = 1;
  var language = languages[1].langName
  document.getElementById('lang').addEventListener("click",function() {
    var button1 = document.getElementById('button1')
    var button2 = document.getElementById('button2')
    var p1 = document.getElementById('TL')
    var p2 = document.getElementById('TT')
    var p3 = document.getElementById('TS')

    if(language == languages[1].langName) {
      p1.innerHTML = languages[0].trashLoc
      p2.innerHTML = languages[0].trashType
      p3.innerHTML = languages[0].trashSize
      button1.innerHTML = languages[0].goBack
      if(button2.innerHTML == languages[1].collectTrash){
        button2.innerHTML = languages[0].collectTrash
      }
      else {
        button2.innerHTML = languages[0].trashCollected
      }
      language = languages[0].langName
      i = 0;
    }
    else if(language == languages[0].langName) {
      p1.innerHTML = languages[1].trashLoc
      p2.innerHTML = languages[1].trashType
      p3.innerHTML = languages[1].trashSize
      button1.innerHTML = languages[1].goBack
      if(button2.innerHTML == languages[0].collectTrash){
        button2.innerHTML = languages[1].collectTrash
      }
      else {
        button2.innerHTML = languages[1].trashCollected
      }
      language = languages[1].langName
      i = 1;
    }
  });

  document.getElementById('button2').addEventListener("click",function() {
    var button = document.getElementById('button2')
    if(button.innerHTML == languages[i].collectTrash){
      button.innerHTML = languages[i].trashCollected
    }
    else {
      button.innerHTML = languages[i].collectTrash
    }
  });
});

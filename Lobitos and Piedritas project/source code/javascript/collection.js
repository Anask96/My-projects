function openSideBar() {
  document.getElementById('sidebar').style.width = "200px";
  document.getElementById('menubtn').style.color = "white";
}

function closeSideBar() {
  document.getElementById('sidebar').style.width = "0";
  document.getElementById('menubtn').style.color = "none";
}
/* A 10 second timeout has been added for all devices.
 * If a device cannot load within 10 seconds map is turned off and a place holder text added */
var openMap = true;
var slowLoad = window.setTimeout(function () {
  openMap = false;
  window.stop();
}, 10000);

/*Dont load the map if there is no gps*/
if (!navigator.geolocation) {
  openMap = false;
}

window.addEventListener("load", function () {

  /* List of the reported trash and the required info about it*/
  let trash = [{
      "where": "Roundabout towards Villa El Pescadora right before Primavera. Bottles are behind the yellow house",
      "locationPointer": "true",
      "location": {
        lat: -4.458616,
        lon: -81.279512
      },
      "img": "plastic.jpg", // Add the img for the trash here
      "page": "collectionlocation.html",
      "type": "Plastic Other",
      "size": "Medium"
    },
    {
      "where": "By the fishing docks near the boat wrecks. ",
      "locationPointer": "true",
      "location": {
        lat: -4.450226,
        lon: -81.277945
      },
      "img": "plastic.jpg", // Add the img for the trash here
      "page": "collectionlocation.html",
      "type": "Metal Other",
      "size": "Medium"
    },
    {
      "where": "en la parte trasera del hotel El Hueco Villas.",
      "locationPointer": "false",
      "location": {
        lat: 51.982934,
        lon: 4.367389
      },
      "img": "plastic.jpg", // Add the img for the trash here
      "page": "collectionlocation.html",
      "type": "Plastic",
      "size": "Medium"
    },
    {
      "where": "El Tranui, by the crossing you will clearly see it",
      "locationPointer": "true",
      "location": {
        lat: -4.453292,
        lon: -81.278238
      },
      "img": "plastic.jpg", // Add the img for the trash here
      "page": "collectionlocation.html",
      "type": "Plastic",
      "size": "Medium"
    },
    {
      "where": "Piedritas. Tramo 2 al borde de la carretera",
      "locationPointer": "false",
      "location": {
        lat: 51.982934,
        lon: 4.367389
      },
      "img": "plastic.jpg", // Add the img for the trash here
      "page": "collectionlocation.html",
      "type": "Plastic",
      "size": "Medium"
    },
    {
      "where": "Lobitos Surf spot, washed up plastic along the beach",
      "locationPointer": "true",
      "location": {
        lat: -4.453105,
        lon: -81.285407
      },
      "img": "plastic.jpg", // Add the img for the trash here
      "page": "collectionlocation.html",
      "type": "Plastic",
      "size": "Medium"
    },
  ]
  if (openMap) {
    map = new OpenLayers.Map("mapdiv");
    map.addLayer(new OpenLayers.Layer.OSM());
    var lonLat
    var zoom = 16;
    var markers = new OpenLayers.Layer.Markers("Markers");
    map.addLayer(markers);
  } else {
    /* Replace the map with an image in case of a bad connection or no available gps*/
    var img = document.createElement('img')
    img.setAttribute("src", "noMap.png")
    img.setAttribute("alt", "Oops! Cant open map")
    img.setAttribute("style", "width:100%;height:100%;")
    document.getElementById('mapdiv').setAttribute("style", "background-color: #0607354a;")
    document.getElementById('mapdiv').appendChild(img)
  }

  trash.forEach(myFunction)
  /*Create a list item for every object in trash list*/
  function myFunction(item) {
    /*Create list element*/
    var node = document.createElement('div');
    node.setAttribute("class", "list-element")
    node.setAttribute("tabindex", "0")

    /*Every list item contains 3 parts the word location,location decription and an icon*/
    var p = document.createElement('P');
    var p2 = document.createElement('div');

    var textnode = document.createTextNode("");
    p.setAttribute("style", "font-weight: bold;")
    p.setAttribute("class", "text")
    p.appendChild(textnode)

    textnode = document.createTextNode(item.where);

    p2.appendChild(textnode);
    p2.setAttribute("class", "part2")
    node.append(p, p2);

    if (item.locationPointer == "true") {
      var img = document.createElement('img');
      img.src = "marker.png" //This is the red pin from for the list
      img.setAttribute("class", "icon")
      img.height = 25
      img.width = 25
      node.append(img);
    }

    /*A map marker is created for the reported trash if there is an available location info*/
    if (item.locationPointer != "false" && openMap) {
      lonLat = new OpenLayers.LonLat(item.location.lon, item.location.lat)
        .transform(
          new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
          map.getProjectionObject() // to Spherical Mercator Projection
        );
      markers.addMarker(new OpenLayers.Marker(lonLat));
      map.setCenter(lonLat, zoom);
    }

    var div = document.getElementById('myList')

    node.addEventListener("mouseover", function () {
      node.style.cursor = "pointer"
    });

    /*A list item can be accessed by clickng on it or navigating to the list item and then press Enter*/
    node.addEventListener("click", function () {
      location.href = item.page
    });
    node.addEventListener("focus", function () {
      node.addEventListener("keyup", function (event) {
        if (event.keyCode === 13) {
          location.href = item.page
        }
      });
    });

    div.append(node)
  }

  /*Translate the page from english to spanish and visa versa*/
  var language = "En"
  document.getElementById('lang').addEventListener("click", function () {
    let p = document.getElementsByClassName("text")
    if (language == "En") {
      for (var i = 0; i < p.length; i++) {
        p[i].innerHTML = ""
      }
      language = "Sp"
    } else if (language == "Sp") {
      for (var i = 0; i < p.length; i++) {
        p[i].innerHTML = ""
      }
      language = "En"
    }
  });
});
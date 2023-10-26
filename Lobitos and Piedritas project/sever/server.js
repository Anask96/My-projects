var express = require('express');
var app = express();
var bodyParser = require("body-parser");

//directory for files
app.use(express.static('HCIAssignment/sever'));
app.use(express.json());       // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({ extended: true }));


//Called for GET request to http://localhost:3000/hello
app.get("/", function(req, res) {
   res.sendFile(__dirname + "/html/mainpage.html");

});
app.get("/html/mainpage.html", function(req, res) {
   res.sendFile(__dirname + "/html/mainpage.html");

});
//Called to get the css part of the html
app.get("/css/mainpage.css", function(req, res) {
   res.sendFile(__dirname + "/css/mainpage.css");

});
//called to get the javascript part of html
app.get("/javascript/mainpage.js", function(req, res) {
   res.sendFile(__dirname  + "/javascript/mainpage.js");

});

app.get("/html/reporting.html", function(req, res) {
   res.sendFile(__dirname + "/html/reporting.html");

});

//Called to get the print css part of the html
app.get("/css/reporting.css", function(req, res) {
   res.sendFile(__dirname + "/css/reporting.css");

});
app.get("/javascript/reporting.js", function(req, res) {
   res.sendFile(__dirname + "/javascript/reporting.js");

});
app.get("/html/collection.html", function(req, res) {
   res.sendFile(__dirname + "/html/collection.html");

});
app.get("/css/collection.css", function(req, res) {
   res.sendFile(__dirname + "/css/collection.css");

});
app.get("/javascript/collection.js", function(req, res) {
   res.sendFile(__dirname + "/javascript/collection.js");
});
app.get("/html/location.html", function(req,res) {
  res.sendFile(__dirname + "/html/location.html");
});
app.get("/html/collectionlocation.html", function(req,res) {
  res.sendFile(__dirname + "/html/collectionlocation.html");
});
app.get("/css/collectionlocation.css", function(req,res) {
  res.sendFile(__dirname + "/css/collectionlocation.css");
});
app.get("/javascript/collectionlocation.js", function(req, res) {
   res.sendFile(__dirname + "/javascript/collectionlocation.js");

});
app.get("/css/location.css", function(req,res) {
  res.sendFile(__dirname + "/css/location.css");
});
app.get("/javascript/location.js", function(req,res) {
  res.sendFile(__dirname + "/javascript/location.js");
});
app.get("/html/signin.html", function(req,res) {
  res.sendFile(__dirname + "/html/signin.html");
});
app.get("/css/signin.css", function(req,res) {
  res.sendFile(__dirname + "/css/signin.css");
});
app.get("/css/signin.css", function(req,res) {
  res.sendFile(__dirname + "/css/signin.css");
});
app.get("/images/system_clipboard.png", function(req,res) {
  res.sendFile(__dirname + "/images/system_clipboard.png");
});
app.get("/images/Recycle-Bin-Full-icon.png", function(req,res) {
  res.sendFile(__dirname + "/images/Recycle-Bin-Full-icon.png");
});
app.get("/images/ping.png", function(req,res) {
  res.sendFile(__dirname + "/images/ping.png");
});
app.get("/images/camera-64x64.png", function(req,res) {
  res.sendFile(__dirname + "/images/camera-64x64.png");
});
app.get("/images/cancon.png", function(req,res) {
  res.sendFile(__dirname + "/images/cancon.png");
});
app.get("/images/find.png", function(req,res) {
  res.sendFile(__dirname + "/images/find.png");
});
app.get("/images/system_clipboard.png", function(req,res) {
  res.sendFile(__dirname + "/images/system_clipboard.png");
});
app.get("/images/tick.png", function(req,res) {
  res.sendFile(__dirname + "/images/tick.png");
});
app.get("/images/trash.jpg", function(req,res) {
  res.sendFile(__dirname + "/images/trash.jpg");
});
app.get("/images/upload.png", function(req,res) {
  res.sendFile(__dirname + "/images/upload.png");
});
app.get("/images/whitetick.png", function(req,res) {
  res.sendFile(__dirname + "/images/whitetick.png");
});
app.listen(3000);

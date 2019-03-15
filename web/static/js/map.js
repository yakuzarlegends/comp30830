var map;
var myLatLng = {
    lat: parseFloat(53.35676900),
    lng: parseFloat(-6.26814000)
};

function initMap() {

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
        center: myLatLng,
        mapTypeId: 'roadmap'
    });

    var locations = [];

    var l = stations.length;
    for (i = 0; i < l; i++) {
        myAdd = {
            position: {
                lat: parseFloat(stations[i].latitude),
                lng: parseFloat(stations[i].longitude)
            },
            title: stations[i].name,
            number: stations[i].number
        };
        locations.push(myAdd);
    }

    locations.forEach(function (feature) {
        var marker = new google.maps.Marker({
            position: feature.position,
            title: feature.title,
            number: feature.number,
            map: map
        });
        marker.addListener('click', function () {
            fetch('http://localhost:5000/stations/' + this.number)
                .then(function (response) {
                    return response.text();
                })
                .then(function (body) {
                    console.log("received!")
                    var obj = JSON.parse(body);
                    console.log(obj)
                })
        });
    });

}



//variable to hold your endpoint
/*
var coodAddresses = 'http://localhost:5000/api/static/';
//an array to hold your cordinates
var locations = [];

fetch(coodAddresses)
  .then(function (response) {
    return response.text();
  })
  .then(function (body) {
      var obj = JSON.parse(body);
      console.log(obj);
      var myAdd = {};
      var addresses = obj;
      var l = addresses.length;
      for (i = 0; i < l; i++) {
        myAdd = {
          position: {
            lat: parseFloat(obj[i].latitude),
            lng: parseFloat(obj[i].longitude)
          },
          title: obj[i].name,
        };
        locations.push(myAdd);
      }
      console.log(locations)
      locations.forEach(function (feature) {
        var marker = new google.maps.Marker({
          position: feature.position,
          title: feature.title,
          map: map
        });
        marker.addListener('click', function() {
          infowindow.open(map, marker);
        });
      });
  });
  */
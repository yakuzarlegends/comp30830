var map;

console.log(stations);


console.log(stations[30].latitude);

var myLatLng = {
    lat: parseFloat(stations[30].latitude),
    lng: parseFloat(stations[30].longitude)
};


var slideIn = document.getElementById("slide-in");
var mapContainer = document.getElementById("map-container");
var minimiser = document.querySelector(".minimiser");
var title = document.querySelector(".station-title");
var content = document.getElementById("slide-in-content");
var totalstands = document.getElementById("totalstands");
var creditcard = document.getElementById("creditcard");
var input = document.getElementById('search-bar');
var infoSections = document.querySelector('.information-sections');
var downbutton = document.querySelector('.down-button');
var typheader = document.querySelector('.typical-header');

var markers = [];

var loc;

function pinClick(number) {
    scrollToTop();
    loc = locations[number];
    title.innerHTML = loc.address;
    totalstands.innerHTML = loc.totalBikeStands;
    if (loc.banking === "True"){
        creditcard.innerHTML = "This station accepts card payments."
        creditcard.style.color = '#4DAF40'
    } else {
        creditcard.innerHTML = "This station does not accept card payments.";
        creditcard.style.color = '#E26464'
    }
   
}


// function selectChange(el) {
//     alert(loc);
// }


function scrollToTop() {
    infoSections.scrollTop = 0;
    downbutton.style.display = 'static';
}

function removeScroll(){
    infoSections.addEventListener('scroll', function(){
        downbutton.style.display = 'none';
        typheader.style.marginTop = '0rem';
    })
}

removeScroll();

function buttonClick() {
    document.body.classList.toggle("menu-active");
    hideAllMarkers(map);
}

minimiser.addEventListener("click", buttonClick);

function updateShownData(data) {
    console.log(data);
    title.textContent = data.name;
}

var locations = {};

var DUBLIN = {
    lat: 53.35,
    lng: -6.27
};

var BOUNDS = {
    north: 53.375340,
    south: 53.318013,
    west: -6.345040,
    east: -6.161072
}

function searchSubmit(e){
    e.preventDefault(); 
    input.value = "";
    return false;
}

function initMap() {

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
        center:myLatLng,
        disableDefaultUI: true,
        mapTypeId: 'roadmap',
        styles: [{
            featureType: 'poi.business',
            stylers: [{
                visibility: 'off'
            }]
        }, 
        {
            featureType: 'poi.attraction',
            stylers: [{
                visibility: 'off'
            }]
        },   
    ],
      restriction: {
             latLngBounds: BOUNDS
        }
    });

    var DublinBounds = [
        new google.maps.LatLng(53.375340, -6.345040),
        new google.maps.LatLng( 53.318013, -6.345040),
        new google.maps.LatLng( 53.318013, -6.161072),
        new google.maps.LatLng( 53.375340, -6.161072),
        new google.maps.LatLng(53.375340, -6.345040)
    ]

    var DublinArea = new google.maps.Polygon({paths: DublinBounds});

    var defaultBounds = new google.maps.LatLngBounds(
        new google.maps.LatLng(53.318013,-6.345040),
        new google.maps.LatLng(53.375340,-6.161072));

    var input = document.getElementById('search-bar');
    var autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.setFields(
        ['address_components', 'geometry', 'icon', 'name']);

    autocomplete.bindTo('bounds', map);


    

    autocomplete.addListener('place_changed', function() {
        
        var place = autocomplete.getPlace();
        if (!place.geometry) {
            var request = {
                query: input.value,
                fields: ['name', 'geometry'],
                locationBias: defaultBounds
              };
      
              service = new google.maps.places.PlacesService(map);

              service.findPlaceFromQuery(request, function(results, status) {
                if (status === google.maps.places.PlacesServiceStatus.OK) {
                    if (google.maps.geometry.poly.containsLocation(results[0].geometry.location, DublinArea)){
                        map.panTo(results[0].geometry.location);
                    } else {
                        map.panTo(myLatLng);
                    }
                }
              });
            
          } else if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
            } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17);  // Why 17? Because it looks good.
            }
        
        

    });


    // var request = {
    //     query: input.innerText
    //   };

    // var service = new google.maps.places.PlacesService(map);


    // service.findPlaceFromQuery(request, function(results, status) {
    //     if (status === google.maps.places.PlacesServiceStatus.OK) {
    //       map.setCenter(results[0].geometry.location);
    //     }
    //   });

    var l = stations.length;
    for (i = 0; i < l; i++) {

        locations[stations[i].number] = {
            position: {
                lat: parseFloat(stations[i].latitude),
                lng: parseFloat(stations[i].longitude)
            },
            title: stations[i].name,
            address: stations[i].address,
            number: stations[i].number,
            availableBikeStands: dynamic[i].available_bike_stands,
            availableBikes: dynamic[i].available_bikes,
            banking: dynamic[i].banking,
            bonus: dynamic[i].bonus,
            status: dynamic[i].status,
            totalBikeStands: dynamic[i].total_bike_stands
        };
    }



    Object.keys(locations).forEach(function (feature) {

        var infowindow = new google.maps.InfoWindow({
            content: "<h3 class='markertag'>" + locations[feature].address + "</h3>"
        });

        var marker = new google.maps.Marker({
            position: locations[feature].position,
            title: locations[feature].title,
            number: locations[feature].number,
            map: map,
            infowindow: infowindow,
            icon: {
                url: "/static/images/bike_icon.png",
                scaledSize: new google.maps.Size(50, 50)
            }
        });

        markers.push(marker);




        marker.addListener('click', function () {
            hideAllMarkers(map);
            this.infowindow.open(map, this);
            map.panTo(this.position);
            document.body.classList.add("menu-active");
            pinClick(this.number);

            // this.icon = {
            //     url: "/static/images/bike_icon.png"
            // }
            // raph work out how to do this
        });
    });
    loc = locations[33];
    pinClick(33);

}


function hideAllMarkers(map) {
    markers.forEach(function (marker) {
        marker.infowindow.close(map, marker);
    })
}

var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', "13:00", '14:00'],
        datasets: [{
            label: '# of bikes available',
            data: [12, 19, 3, 5, 2, 3,5,6,7,8],
            backgroundColor: [
                '#fff',
                '#fff',
                '#fff',
                '#fff',
                '#fff',
                '#fff',
                '#fff',
                '#fff',
                '#fff',
                '#fff'
            ],
            borderColor: [
                '#3CA0CC',
                '#3CA0CC',
                '#3CA0CC',
                '#3CA0CC',
                '#3CA0CC',
                '#3CA0CC',
                '#3CA0CC',
                '#3CA0CC',
                '#3CA0CC',
                '#3CA0CC'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});
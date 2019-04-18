var map;
var current_number = 33

// we establish the current_number and the map


var myLatLng = {
    lat: parseFloat(stations[30].latitude),
    lng: parseFloat(stations[30].longitude)
};

// we take the stations passed in from the static data, and get the long and lat of one of them

current_station = stations[30].number


function selectChange(the_object, other_object){
    console.log("select change called")
    fetch("/mock/predict", {
        method: 'POST',
        mode: 'no-cors',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"weekday": the_object.value, "hour": other_object.value, "station_id": current_station})
    }).then(function(response){
        console.log("THE RESPONSE", response)
        console.log("current info for this station:", locations[current_station])
        return response.json();

    }).then(function(data){
        console.log("THE DATA", data)
        updateBikeInformation(data)
    });

    
}

// selectChange is what will run when the dropdown is clicked. 



dayLookup = {
    0: ["Monday", 0],
    1: ["Tuesday", 1],
    2: ["Wednesday", 2],
    3: ["Thursday", 3],
    4: ["Friday", 4],
    5: ["Saturday", 5],
    6: ["Sunday", 6]
}

// the dayLookup allows us to find out the day based on the new Date() object

// if you click, you want everything to revert to now. So we need now variables.

var today = new Date(); // new date object
var nowHour = today.getHours() // the hour right now
var nowDay = dayLookup[today.getDay() -1][0] // the name of the day right now
var nowDaynum = today.getDay() - 1 // the number value of the day right now

// get list of hours for current location:
var spreadNowHours = []


// spreadnowhours is now ready to be used


function findCurrentHours(){
    today = new Date();
    nowHour = today.getHours()
    nowDay = dayLookup[today.getDay() -1][0]
    nowDaynum = today.getDay() - 1
    for (var b = nowHour - 3; b < nowHour + 4; b++){
        var x = b
        if (x >= 24) {
            x = x - 24
        }
        x = "" + x
    
        if (x.length < 2){
            x = "0" + x
        }
        x = x +":00"
        spreadNowHours.push(x)
    }
}

findCurrentHours()

// this is the list




var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: spreadNowHours,
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


function setMaxOnChart(chart, num_there){
    chart.options.scales.yAxes[0].ticks.max = num_there
    chart.update()
}



function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}

function updateConfigByMutating(chart, labels, data, bikes_there) {
    chart.data.labels = labels;
    // chart.data.datasets.data = data;
    chart.data.datasets[0].data = data
    chart.options.scales.yAxes[0].ticks.max = bikes_there
    chart.update();
}





function updateBikeInformation(data){

    console.log("updateBikeInfo called")

    var bike_prediction = Math.round(data.tuples[3][1][0])
   
    bikesav.textContent = bike_prediction
    current_location = locations[current_number];
    spacesav.textContent = current_location.totalBikeStands - bike_prediction
    
    
    
    var data_hours = []
    var bike_data = []
    for (var j = 0; j < data.tuples.length; j++){
        data_hours.push(data.tuples[j][0])
        bike_data.push(Math.round(data.tuples[j][1][0]))
    }


    for (var l = 0; l < data_hours.length; l++){
        var x = data_hours[l]
        if (x >= 24) {
            x = x - 24
        }
        x = "" + x

        if (x.length < 2){
            x = "0" + x
        }
        x = x +":00"
        data_hours[l] = x
    }

    var bikes_there = current_location.totalBikeStands
    updateDayTimeShow(current_location)
    updateConfigByMutating(myChart, data_hours, bike_data, bikes_there)
    // addData(myChart, "New label", 14)
}


// updateConfigByMutating(myChart, )


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
var tempNumber = document.getElementById("temp-number");
var putDate = document.getElementById("put_date");
var putTime = document.getElementById("put_time");
var svgWeatherNode = document.querySelector('.svg-weather');
var selectTime = document.getElementById('openingtime')
var selectInput = document.getElementById('openingday')
var bikesav = document.getElementById('bikesav');
var spacesav = document.getElementById('spacesav');
var infotime = document.getElementById('station-info-time');
var dayspan = document.getElementById('dayspan');




var weatherDescriptions = {
    "sunny": "sun",
    "mostly sunny": "sun",
    "partly sunny": "cloud_sun",
    "intermittent clouds": "cloud_sun",
    "hazy sunshine": "cloud_sun",
    "mostly cloudy": "cloud",
    "cloudy": "cloud",
    "dreary": "overcast",
    "fog": "overcast",
    "showers": "cloud_rain",
    "most cloudy w/ showers": "cloud_rain",
    "partly sunny w/ showers": "cloud_sun_rain",
    "t-storms": "thunder",
    "mostly cloudy w/ t-storms": "thunder",
    "partly sunny w/ t-storms": "thunder",
    "rain": "cloud_rain",
    "flurries": "cloud_rain",
    "mostly cloudy w/ flurries": "cloud_rain",
    "partly sunny w/ flurries": "cloud_rain",
    "ice": "ice",
    "snow": "snow",
    "mostly cloudy w/ snow": "snow",
    "sleet": "ice",
    "freezing rain": "cloud_rain",
    "rain and snow": "snow",
    "hot": "sun",
    "cold": "ice",
    "windy": "wind",
    "clear": "night",
    "mostly clear": "night",
    "partly cloudy": "night",
    "hazy moonlight": "night",
    "drizzle": "cloud_rain"
    
}

var weatherDescription = weather.description.toLowerCase();


var svg_weather = weatherDescriptions[weatherDescription]

svgWeatherNode.src = "../static/images/weather/" + svg_weather + ".svg"

tempNumber.innerHTML = weather.temperature;

var markers = [];

var dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'};
var timeOptions = { hour: 'numeric', minute: 'numeric'};






dayNodes = []

start = today.getDay() - 1;
count = start
for (var z = 0; z <=4; z++){
    if (count > 6){
        count = count - 7
    }
    dayNodes.push(dayLookup[count])
    count++
}



start_chart_hours = []

for (var l = nowHour; l <= nowHour + 5; l++){
   
    var x = l
    if (x >= 24) {

        x = x - 24
        
    }
    x = "" + x

    if (x.length < 2){
        x = "0" + x
    }
    x = x +":00"

    start_chart_hours.push(x)
}



selectInput.innerHTML = "";
for (var x = 0; x < dayNodes.length; x++){
    selectInput.innerHTML = selectInput.innerHTML + "<option value='" + dayNodes[x][1] + "'>" + dayNodes[x][0] +"</option>"
}




for (var i=0; i<selectTime.options.length; i++) {
  option = selectTime.options[i];

  if (option.value == nowHour) {
  // or
  // if (option.text = 'Malaysia') {
     option.setAttribute('selected', true);
  } 
}

function tick() {

    var dateString = today.toLocaleDateString("en-US", dateOptions);
    var timeString = today.toLocaleDateString("en-US", timeOptions);
    timeString = timeString.substring(10);
    putDate.innerHTML = dateString;
    putTime.innerHTML = timeString;
    t = setTimeout('tick()',1000);
}

tick();

var loc;


function pinClick(number) {
    console.log("Pin click called")
    current_number = number
    input.value = "";
    scrollToTop();
    loc = locations[number];
    current_location = loc
    map.setZoom(16);
    map.panTo(loc.position);
    current_station = loc.number

    
    title.innerHTML = loc.address;
    selectTime.value = nowHour;
    selectInput.value = nowDaynum;
    setMaxOnChart(myChart, loc.totalBikeStands)

    totalstands.innerHTML = loc.totalBikeStands;
    bikesav.textContent = loc.availableBikes
    spacesav.textContent = loc.availableBikeStands
    if (loc.banking === "True"){
        creditcard.innerHTML = "This station accepts card payments."
        creditcard.style.color = '#4DAF40'
    } else {
        creditcard.innerHTML = "This station does not accept card payments.";
        creditcard.style.color = '#E26464'
    }

    selectChange(selectInput, selectTime)

}

function updateDayTimeShow(location){
    console.log("updatedaytimeshow called")
    var enterHour = "" + nowHour

    day_string = dayLookup[selectInput.value][0]
    dayspan.textContent = day_string
    
    if (dayLookup[selectInput.value][0] === nowDay && selectTime.value === enterHour){
        infotime.textContent = 'NOW'
        infotime.classList.add('greentext')
        infotime.classList.remove('bluetext')
        console.log(location.availableBikes)
        console.log(location.availableBikeStands)
        bikesav.innerText = location.availableBikes
        spacesav.innerText = location.availableBikeStands

    } else {
        
        infotime.classList.remove('greentext')

        infotime.classList.add('bluetext')

        infotime.textContent = day_string + " at " + selectTime.value + ":00"
    }


    
}




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
                        hideAllMarkers()
                        input.value = "";
                    }
                    
                }
              });
            
          } else if (place.geometry.viewport) {
            document.body.classList.remove("menu-active");
            hideAllMarkers();
            map.setZoom(17);
            map.panTo(place.geometry.location);
            map.fitBounds(place.geometry.viewport);
            } else {
            
            map.setCenter(place.geometry.location);
            hideAllMarkers();
            map.setZoom(15);  
            }
        
        

    });



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
            // map.panTo(this.position);
            document.body.classList.add("menu-active");
            pinClick(this.number);

            // this.icon = {
            //     url: "/static/images/bike_icon.png"
            // }
            // raph work out how to do this
        });
    });
    loc = locations[33];
    console.log(loc)
    pinClick(33);

}


function hideAllMarkers(map) {
    markers.forEach(function (marker) {
        marker.infowindow.close(map, marker);
    })
}

// selectChange(selectInput, selectTime)


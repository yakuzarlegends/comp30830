$(function () {
           
            var first_time = "yes";
            var myLatLng = {
                lat: 53.35676900,
                lng: -6.26814000
            };

            var locations = [
                ['BLESSINGTON STREET', 53.35676900, -6.26814000, 4],
                ['BOLTON STREET', 53.35118200, -6.26985900, 5],
                ['GREEK STREET', 53.34687400, -6.27297600, 3],
                ['CHARLEMONT PLACE', 53.33066200, 153.33066200, 2],
                ['CHRISTCHURCH PLACE', 53.34336800, -6.27012000, 1]
            ];


            function chgScreen_from_submit() {
                if (first_time == "yes")
                // create map for station screen first time ouput
                {
                    var map2 = new google.maps.Map(document.getElementById('map2'), {
                        zoom: 13,
                        center: myLatLng
                    });

                    var marker, i;

                    for (i = 0; i < locations.length; i++) {
                        marker = new google.maps.Marker({
                            position: new google.maps.LatLng(locations[i][1], locations[i][2]),
                            map: map2
                        });

                        google.maps.event.addListener(marker, 'click', (function (marker, i) {
                            return function () {
                                infowindow.setContent(locations[i][0]);
                                infowindow.open(map2, marker);
                            }
                        })(marker, i));

                    };
                    first_time = "no";
                }


                if (document.getElementById("stationmap").style.display == 'none') {
                    document.getElementById("maponly").style.display = 'none';
                    document.getElementById("stationmap").style.display = 'flex';
                } else {
                    document.getElementById("maponly").style.display = 'none';
                    document.getElementById("stationmap").style.display = 'flex';
                }

            }


            function chgScreen() {

                document.getElementById("stationmap").style.display = 'none';
                document.getElementById("maponly").style.display = 'block';


            }

            function station_dd() {
                var blist = ['St Stephens Green', 'Fitzwilliam Square', 'Leeson Park'];
                var str = '<select><option value="0" selected="selected">Choose Station</option>';
                // to process a station being selected  change to this
                //var str = '<select><option value="0" selected="selected" onchange="chg_station(this.value)">Choose Station</option>';
                for (var i = 0; i < blist.length; ++i) {
                    str = str + '<option value="' + blist[i] + '">' + blist[i] + '</option>';
                }
                str = str + '</select>';
                document.getElementById("station_dd").innerHTML = str
            }

            function weekday_dd() {
            // create weekday dropdown
                var alist = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
                var str = '<select><option value="0" selected="selected">Choose Weekday</option>';
                // to process a weekday being selected change to this  
                // var str = '<select><option value="0" selected="selected" onchange="chg_weekday(this.value)">Choose Weekday</option>';    
                for (var i = 0; i < alist.length; ++i) {
                    str = str + '<option value="' + alist[i] + '">' + alist[i] + '</option>';
                }
                str = str + '</select>';
                document.getElementById("weekday_dd").innerHTML = str
            }

            function time_dd() {
                var alist = ["05.00", "05.30", "06.00", "06.30", "07.00", "07.30", "08.00", "08.30", "09.00", "09.30", "10.00", "10.30",
                    "11.00", "11.30", "12.00", "12.30", "13.00", "13.30", "14.00", "14.30", "15.00", "15.30", "16.00", "16.30",
                    "17.00", "17.30", "18.00", "18.30", "19.00", "19.30", "20.00", "20.30", "21.00", "21.30", "22.00", "22.30",
                    "23.00", "23.30", "00.00", "00.30"
                ];

                var str = '<select><option value="0" selected="selected">Choose Time</option>';
                // to process a time being selected  change to this
                //var str = '<select><option value="0" selected="selected" onchange="chg_TIME(this.value)">Choose Time</option>';
                for (var i = 0; i < alist.length; ++i) {
                    str = str + '<option value="' + alist[i] + '">' + alist[i] + '</option>';
                }
                str = str + '</select>';
                document.getElementById("time_dd").innerHTML = str
            }

            function initMap() {
                //creates inital screen map, populates dropdowns 
                // populate the station, weekday and time dropdown
                var dropD1 = station_dd();
                var dropD2 = weekday_dd();
                var dropD3 = time_dd();

                var map = new google.maps.Map(document.getElementById('map'), {
                    zoom: 13,
                    center: myLatLng
                });


                var infowindow = new google.maps.InfoWindow();

                var marker, i;

                for (i = 0; i < locations.length; i++) {
                    marker = new google.maps.Marker({
                        position: new google.maps.LatLng(locations[i][1], locations[i][2]),
                        map: map
                    });

                    google.maps.event.addListener(marker, 'click', (function (marker, i) {
                        return function () {
                            infowindow.setContent(locations[i][0]);
                            infowindow.open(map, marker);
                        }
                    })(marker, i));

                };

                document.getElementById("stationmap").style.display = 'none';
                document.getElementById("maponly").style.display = 'block';
            
}});
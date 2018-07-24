console.log(entries)


function replot(oldBounds) {
    var l_lat = oldBounds._southWest.lat,
    u_lat = oldBounds._northEast.lat,
    w_lon = oldBounds._southWest.lng,
    e_lon = oldBounds._northEast.lng,
    lon_dif = Math.abs(w_lon - e_lon),
    lat_dif = Math.abs(u_lat - l_lat)
    oldcenter = [u_lat - lon_dif/2, w_lon + lon_dif/2]
    console.log(oldBounds)
    // if (map.getCenter() > (u_lat-lat)
    return 1;
}
function plotData() {
    var bounds = map.getBounds()
    // if (!oldBounds) {
    //     if (!replot(oldBounds)) { return }
    // }
    eraseMarkers()
    grabData(bounds)

    var oldBounds = map.getBounds()
}

function grabData(bounds) {
    //l = lower bound, u = upper bound
    //w = west bound, e = east bound
    var l_lat = bounds._southWest.lat,
    u_lat = bounds._northEast.lat,
    w_lon = bounds._southWest.lng,
    e_lon = bounds._northEast.lng

    four = []
    four.push(l_lat, u_lat, w_lon, e_lon)

    //SELECT * FROM public."Winery" w
    // WHERE w.lat > 37.743571187449064 AND
    // w.lat < 38.542795073979015 AND
    // w.lon < -121.94686889648439 AND
    // w.lon > -122.66784667968751
    // LIMIT 10;

    $.ajax({
        type: 'GET',
        url: "/api/getWineries?bounds=" + four,
        success: function(data) { // Response about a single UID2 status
            marker = [];
            data = JSON.parse(data)
            console.log(data)
            for (var i = 0; i < data.length; i++) {
                plotMarkers(data[i])
            }
        },
        error: function(data) {
            console.log("Error pulling addresses from database via cartCombo_app.py and ajax call\n")
        }
    });
}

function eraseMarkers() {
    // console.log(map)
    var len = marker.length
    for (var i = 0; i < len; i++) {
        if (marker[i]) { map.removeLayer(marker[i]); };
    }
}

function plotMarkers(winery) {
        var circlestyle = {
            color: 'darkred',
            fillColor: 'indianred',
            fillOpacity: .5,
            weight: 1,
            radius: 8
        }

        var customPopup = '<strong>' + winery[1] + '</strong><br>' + winery[4];

        // specify popup options
        var customOptions = {
            'maxWidth': '100',
            'className' : 'custom'
        }

        var submarker = L.circleMarker([winery[2], winery[3]], circlestyle).bindPopup(customPopup, customOptions).addTo(map)
        marker.push(submarker)
    }



var map = L.map('map').setView([38.144595, -122.307990], 10);

mapLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';
L.tileLayer(  'http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    maxZoom: 18,
}).addTo(map);

marker = [];
var submarker = {};

plotData()

map.on('moveend', function(e) {
   // var bounds = map.getBounds();
   plotData()
});

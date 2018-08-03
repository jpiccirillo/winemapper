startMap(parameters[0], parameters[1], parameters[2])

map.on('moveend', function(e) {
   // var bounds = map.getBounds();
   // plotData()
});

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
            data = JSON.parse(data)
            console.log(data)
            for (var i = 0; i < data.length; i++) {
                plotMarkers('homepage', data[i])
            }
        },
        error: function(data) {
            console.log("Error originaing from ajax call\n")
        }
    });
}

// function replot(oldBounds) {
//     var l_lat = oldBounds._southWest.lat,
//     u_lat = oldBounds._northEast.lat,
//     w_lon = oldBounds._southWest.lng,
//     e_lon = oldBounds._northEast.lng,
//     lon_dif = Math.abs(w_lon - e_lon),
//     lat_dif = Math.abs(u_lat - l_lat)
//     // oldcenter = [u_lat - lon_dif/2, w_lon + lon_dif/2]
//     // console.log(oldBounds)
//     // if (map.getCenter() > (u_lat-lat)
//     return 1;
// }

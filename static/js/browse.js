startMap(parameters[0], parameters[1], parameters[2])

map.on('moveend', function(e) {
   var bounds = map.getBounds();
   if (mode=='search') {return;} //more data is grabbed in a fundamentally
   //different way for "search" mode, so don't continue

   grabData(bounds)
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

    $.ajax({
        type: 'GET',
        url: "/api/getWineries?bounds=" + four,
        success: function(data) {
            data = JSON.parse(data)
            console.log(data)
            for (var i = 0; i < data.length; i++) {
                plotMarkers(mode, data[i])
            }
        },
        error: function(data) {
            console.log("Error originaing from ajax call\n")
        }
    });
}

function show(id) {
    console.log(id)
    $(".nav-item .form-control#" + id).show(400)
}

function plotHeader(winery) {
    console.log(winery)
    $(".wineheader").show().empty().append(
        '<div class="card">'+
        '<div class="card-body">'+
        '<h6 class="card-title" style="margin-bottom: 0px;">Wines from ' + winery + ':</h6>' +
        '</div>'
    )
    // $(".wineheader")
}

function plotCards(wine) {
    console.log(wine)
    var text = wine[1]
    var link = '/api/wineDetail?id='+wine[0];
    var card = '<div class="card">'+
    // "<img class=\"card-img-top\" alt=\"Card image cap\">" +
    '<div class="card-body">'+
    // "<h7 class=\"card-title\">Card title</h7>" +
    '<p class="card-text">' + text + '</p>' +
    '<a href="'+ link + '"class="btn btn-secondary">Read Reviews</a>' +
    '<a onClick="checkLogin()" class="btn btn-success">Add to Favorites</a>' +
    "</div></div>";
    $(".activearea").append(card);
}

function eraseMarkers() {
    // console.log(map)
    var len = marker.length
    for (var i = 0; i < len; i++) {
        if (marker[i]) { map.removeLayer(marker[i]); };
    }
}

function rightPanel(id, name) {
    console.log(id)
    $.ajax({
        type: 'GET',
        url: "/api/getWines?id=" + id,
        success: function(data) { // Response about a single UID2 status
            // marker = [];
            data = JSON.parse(data)
            console.log(data)
            $(".filler").hide()
            plotHeader(name)
            $(".activearea").empty()
            for (var i = 0; i < data.length; i++) {
                plotCards(data[i])
            }
        },
        error: function(data) {
            console.log("Error originaing from ajax call\n")
        }
    });
}


// parameters:  lat, lon, id, name, address
function plotMarkers(mode, args) {
    console.log(mode)
    // specify popup options
    var customOptions = {
        'maxWidth': '200',
        'className' : 'custom'
    }
    var style = 'padding: 0px; margin-left: 0px; margin-top: 5px; border-radius: 4px;'
    var circlestyle = {
        fillOpacity: .5,
        weight: 1,
        radius: 8
    }

    if (mode=='homepage') {
        circlestyle.color = 'darkred'
        circlestyle.fillColor = 'indianred'

        var link = '/api/wineryDetail?id=' + args[0]
        var customPopup = '<div><strong>' + args[1] + '</strong><br>' + args[4] + '<br><a href="' + link + '" class="btn" style="' + style + '">Details on this Winery</a></div>';

        var submarker = L.circleMarker([args[2], args[3]], circlestyle).bindPopup(customPopup, customOptions).addTo(map)

        submarker.on('click', function(e) {
            rightPanel(args[0], args[1]);
        }).on('popupclose', function(e) {
            $(".activearea").empty()
            $(".wineheader").hide()
            $(".filler").show()
        });
        marker.push(submarker)

    } else {
        circlestyle.color = 'darkblue'
        circlestyle.fillColor = 'lightblue'

        var link = '/api/wineryDetail?id=' + args[0]
        var customPopup = '<div><strong>' + args[1] + '</strong><br>' + args[4] + '<br><a href="' + link + '" class="btn" style="' + style + '">Details on this Winery</a></div>';

        var submarker = L.circleMarker([args[10], args[11]], circlestyle).bindPopup(customPopup, customOptions).addTo(map)
        submarker.on('click', function(e) {
            rightPanel(args[0], args[1]);
        }).on('popupclose', function(e) {
            $(".activearea").empty()
            $(".wineheader").hide()
            $(".filler").show()
        });
        marker.push(submarker)

        console.log(mode, args)
    }
}

function startMap(mapcenter, markers, zoom) {
    // console.log(markers)
    marker = [];
    map = L.map('map', {
        closePopupOnClick: false
    }).setView(mapcenter, zoom);
    //add ins  (de-stack overlapping points, stateful URL, geocoder)
    oms = new OverlappingMarkerSpiderfier(map),
    hash = new L.Hash(map), //Stateful URL implementation
    geocoder = L.Control.geocoder({
        position: "topleft",
        placeholder: "Enter an Address",
        showResultIcons: false,
    }).addTo(map)

    mapLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';
    L.tileLayer('http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
        maxZoom: 18,
    }).addTo(map);

    if (!markers) { //if we're in homepage mode (markers not provided)
        var bounds = map.getBounds()
        grabData(bounds);

    } else { //we're in search mode (markers provided)
        data = JSON.parse(markers)
        console.log(data)
        for (var i = 0; i < data.length; i++) {
            plotMarkers('search', data[i])
        }
        // console.log(marker)
        var group = new L.featureGroup(marker);
        map.fitBounds(group.getBounds().pad(0.5));
    }
}

// marker = [];
// var submarker = {};

// plotData()

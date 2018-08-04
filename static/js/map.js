function show(id) {
    console.log(id)
    $(".nav-item .form-control#" + id).show(400)
}

function plotHeader(text, header) {
    console.log(winery)
    $(".wineheader").show().empty().append(
        '<div class="card">'+
        '<div class="card-body">'+
        '<h6 class="card-title" style="margin-bottom: 0px;"> ' + text + '</h6>' +
        '</div>'
    )
}

function plotCards(id, text) {
    // console.log(wine)
    // var text = wine[1]
    var link = '/api/wineDetail?id='+id;
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

// function eraseMarkers() {
//     // console.log(map)
//     var len = marker.length
//     for (var i = 0; i < len; i++) {
//         if (marker[i]) { map.removeLayer(marker[i]); };
//     }
// }

function homePanel(id, name) {
    console.log(id)
    $.ajax({
        type: 'GET',
        url: "/api/getWines?id=" + id,
        success: function(data) { // Response about a single UID2 status
            // marker = [];
            data = JSON.parse(data)
            console.log(data)
            $(".filler").hide()
            plotHeader("Wines from " + winery + ":")
            $(".activearea").empty()
            for (var i = 0; i < data.length; i++) {
                plotCards(data[i][0], data[i][1])
            }
        },
        error: function(data) {
            console.log("Error originaing from ajax call\n")
        }
    });
}
function searchPanel(data) {
    $(".filler").hide()
    console.log(search)
    form = ['title', 'variety', 'designation', 'maxprice', 'area', 'winery', 'keyword']
    var searchquery = "You searched on: <br>"
    $.each(search, function(i, val) {
        // console.log(i)
        if (i==7) {return false}
        if (val) { searchquery += form[i].toUpperCase() + ": <span style='font-weight: 400'>" + val + "</span><br>" }
    })
    console.log(data)
    plotHeader(searchquery)
    for (var i = 0; i < data.length; i++) {
        plotCards(data[i][0], data[i][1])
    }

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
        fillOpacity: 1,
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
            homePanel(args[0], args[1]);
        }).on('popupclose', function(e) {
            $(".activearea").empty()
            $(".wineheader").hide()
            $(".filler").show()
        });
        marker.push(submarker)

    }
    else {
        circlestyle.color = 'darkblue'
        circlestyle.fillColor = 'lightblue'

        var winelink = '/api/wineDetail?id=' + args[0]
        var winerylink = '/api/wineryDetail?id=' + args[9]
        var customPopup = '<div>' + args[1] + '<br><strong>From: </strong><a href="' + winerylink + '">' + args[10] + '</a><br><a href="' + winelink + '" class="btn" style="' + style + '">More details on this wine</a></div>';

        var submarker = L.circleMarker([args[11], args[12]], circlestyle).bindPopup(customPopup, customOptions).addTo(map)
        // submarker.on('click', function(e) {

        // }).on('popupclose', function(e) {
        //     $(".activearea").empty()
        //     $(".wineheader").hide()
        //     $(".filler").show()
        // });
        marker.push(submarker)

        console.log(mode, args)
    }
}

function startMap(mapbounds, markers, zoom) {
    // console.log(markers)
    marker = [];
    center = L.latLngBounds(mapbounds).getCenter();
    map = L.map('map', {
        closePopupOnClick: false
    }).setView(center, zoom);
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
        coordinateSearch(JSON.parse(markers))
    }
}

function coordinateSearch(data) {
    console.log(data)
    $.each(data, function(i, entry) {
        console.log(i, entry)
        plotMarkers(mode, entry)
    })
    // console.log(marker)
    searchPanel(data);
    group = new L.featureGroup(marker);
    map.fitBounds(group.getBounds().pad(0.5));
}

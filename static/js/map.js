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

//General function for writing boostrap "cards" to right results panel
function plotCards(wineID, userID, favorited, text) {

    var link = '/api/wineDetail?id='+wineID;
    var card = '<div class="card">'+
    // "<img class=\"card-img-top\" alt=\"Card image cap\">" +
    '<div class="card-body">'+
    '<p class="card-text">' + text + '</p>'

    card+='<a href="'+ link + '"class="btn btn-secondary"'
    if (userID > 0) {
        card+=" style='width:50%'>Read Reviews</a>"
    } else { card+='>Read Reviews</a>'
    }
    if (userID > 0) {
        card += prepButton(wineID, favorited)
    }
    card += "</div></div>"
    console.log(card)
    $(".activearea").append(card);
}
//Load wine results from ajax call in the right pane
function homePanel(id, name) {
    console.log(id)
    $.ajax({
        type: 'GET',
        url: "/api/getWines?id=" + id,
        success: function(data) {
            data = JSON.parse(data)
            console.log(data)
            $(".filler").hide()
            plotHeader("Wines from " + name + ":")
            $(".activearea").empty()
            for (var i = 0; i < data.length; i++) {
                console.log("id?" + data[i][10])
                plotCards(data[i][0], UID, data[i][22], data[i][1])
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
        if (i==7) {return false}
        if (val) { searchquery += form[i].toUpperCase() + ": <span style='font-weight: 400'>" + val + "</span><br>" }
    })
    console.log(data)
    plotHeader(searchquery)
    for (var i = 0; i < data.length; i++) {
        console.log(data[i])
        text = prepSearchData(data[i])
        plotCards(data[i][0], 0, 0, text)
    }
}
//Adding in more text to the cards if search is used
function prepSearchData(data) {
    text = data[1] + '<br>'
    if (data[14]) { text+='<strong>Description: </strong>'+data[14] + '<br>'}
    if (data[4]) { text+='<strong>Avg Points: </strong>' + data[4] +'<br>'}
    if (data[13]) { text+='<strong>Total Favorites: </strong>' + data[13] + '<br>'}
    return text;
}

function plotMarkers(mode, args) {
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
    //Map is being loaded in normal homepage mode
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
    //We're in search mode - different workflow
    else {
        circlestyle.color = 'darkblue'
        circlestyle.fillColor = 'lightblue'

        var winelink = '/api/wineDetail?id=' + args[0]
        var winerylink = '/api/wineryDetail?id=' + args[9]
        var customPopup = '<div>' + args[1] + '<br><strong>From: </strong><a href="' + winerylink + '">' + args[10] + '</a><br><a href="' + winelink + '" class="btn" style="' + style + '">More details on this wine</a></div>';

        var submarker = L.circleMarker([args[11], args[12]], circlestyle).bindPopup(customPopup, customOptions).addTo(map)
        marker.push(submarker)
        console.log(mode, args)
    }
}

function startMap(mapbounds, markers, zoom) {
    marker = [];
    center = L.latLngBounds(mapbounds).getCenter();

    map = L.map('map', {
        closePopupOnClick: false
    }).setView(center, zoom);
    //add ins  (de-stack overlapping points, stateful URL, geocoder)
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
    map.fitBounds(group.getBounds());
}

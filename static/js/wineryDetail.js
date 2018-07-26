// console.log(winerydata)
// winerydata = JSON.parse(win erydata)
// console.log(wdata)

// info = JSON.parse(info)
// console.log(info)
// var winery = info.split('|')
wineryOverview()

// Gets ancillary wine info - returns a row for each wine
$.ajax({
    type: 'GET',
    url: "/api/wineryWineInfo?id=" + winery[0],
    success: function(data) { // Response about a single UID2 status

        data = JSON.parse(data)

        $("#wineryWines .card-text").empty()
        $("#wineryWines #bottle").remove()
        for (var i = 0; i < data.length; i++) {
            makeWineCard(data[i]);
        }
    },
    error: function(data) {
        console.log("Error pulling addresses from database via cartCombo_app.py and ajax call")
    }
});

// Gets info about who has reviewed the winery the most
function getMostReviews(){
    $.ajax({
        type: 'GET',
        url: "/api/reviewedWineryMost?id=" + winery[0],
        success: function(data) { // Response about a single UID2 status
    
            data = JSON.parse(data)
    
            for (var i = 0; i < data.length; i++) {
                var listItem = '<li><a href="/api/tasterDetail?id=' + data[i][0] + '">' + data[i][1] + ' with ' + data[i][2] + ' reviews from this winery.</a></li\>';
                $("#wineryMostReviews").append(listItem);
            }    
        },
        error: function(data) {
            console.log("Error pulling addresses from database via cartCombo_app.py and ajax call\n")
        }
    });
}


function wineryOverview() {
    $("#winerySoil h6").text("Soil Quality at " + winery[1]);
    $("#wineryOverview h6").text("Overview of " + winery[1]);
    $("#wineryWines h6").text("Wines from " + winery[1]);
    $("#wineryAddress").text(winery[4]);
    $("#wineryLatLon").text(winery[2] + ", " + winery[3]);
    getMostReviews();
}

function makeWineCard(wineData) {
    var title = wineData[1];
    var text = "";
    if (!wineData[2]) {
        text = text + "<strong>Average price:</strong> None listed.";
    } else {text = text + "<strong>Average price:</strong> " + wineData[6]; }

    if (wineData[11]) {
        var province = "";
        if (wineData[12]) {
            province = '<a href=' + wineData[12] + ' target = "_blank">' + wineData[11] + '</a>';
        } else { province = wineData[11]; }
        text = text + "<br><strong>Province/Region: </strong>" + province;
    }
    text = text + "<br><strong>Variety: </strong>" + wineData[8];

    if (wineData[9]!="No Information") {
        text = text + "<br><strong>Variety Description: </strong>" + wineData[9];
    }
    if (wineData[4]) {
        text = text + "<br><strong>Designation: </strong>" + wineData[4];
    }
    var textstyle = "font-family: Dosis!important";
    var link = '/api/wineDetail?id='+wineData[0];
    var card = '<div class="card">'+
    // "<img class=\"card-img-top\" alt=\"Card image cap\">" +
    '<div class="card-body">'+
    '<h7 class="card-title"> ' + title + '</h7>' +
    '<p class="card-text" style="'+textstyle+'">' + text + '</p>' +
    '<a href="' + link + '" class="btn btn-secondary">Read Reviews</a>' +
    // "<a href=\"#\" class=\"btn btn-secondary\">Data on this Wine</a>"
    '</div></div>';
    $("#wineryWines .card-body .main").append(card);
}

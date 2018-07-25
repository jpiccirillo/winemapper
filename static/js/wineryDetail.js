// console.log(winerydata)
// winerydata = JSON.parse(win erydata)
// console.log(wdata)

var winery = info.split('|')
wineryOverview()

$.ajax({
    type: 'GET',
    url: "/api/wineryDetailFurther?id=" + winery[0],
    success: function(data) { // Response about a single UID2 status

        data = JSON.parse(data)

        $("#wines .card-text").empty()
        $("#wines #bottle").remove()
        for (var i = 0; i < data.length; i++) {
            addWine(data[i])
        }
    },
    error: function(data) {
        console.log("Error pulling addresses from database via cartCombo_app.py and ajax call\n")
    }
});

function wineryOverview() {
    $("#address").text(winery[4])
    $("#latlon").text(winery[2] + ", " + winery[3])
}

function addWine(wdata) {
    var title = wdata[5]
    var text = "<strong>Average price:</strong> $" + wdata[6]
    if (wdata[12]) {
        var province = ""
        if (wdata[13]) {
            province = "<a href=" + wdata[13] + " target = \"_blank\">" + wdata[12] + "</a>"
        } else { province = wdata[12] }
        text = text + "<br><strong>Province: </strong>" + province
    }
    text = text + "<br><strong>Variety: </strong>" + wdata[16]

    if (wdata[17]!="No Information") {
        text = text + "<br><strong>Variety Description: </strong>" + wdata[17]
    }
    if (wdata[8]) {
        text = text + "<br><strong>Designation: </strong>" + wdata[8]
    }
    var style = 'padding: 5px'
    var textstyle = "font-family: Dosis!important"
    var card = "<div class=\"card\">"+
    // "<img class=\"card-img-top\" alt=\"Card image cap\">" +
    "<div class=\"card-body\">"+
    "<h7 class=\"card-title\"> " + title + "</h7>" +
    "<p class=\"card-text\" style='"+textstyle+"'>" + text + "</p>" +
    "<a href=\"#\" class=\"btn btn-secondary\">Read Reviews</a>" +
    // "<a href=\"#\" class=\"btn btn-secondary\">Data on this Wine</a>"
    "</div></div>"
    $("#wines .card-body .main").append(card)
}

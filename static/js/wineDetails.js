wineOverview()

// Gets wine review info - returns a row for each review
$.ajax({
    type: 'GET',
    url: "/api/wineReviews?id=" + wine[0],
    success: function(data) { // Response about a single UID2 status

        data = JSON.parse(data)

        $("#wineReviews .card-text").empty()
        $("#wineReviews #bottle").remove()
        for (var i = 0; i < data.length; i++) {
            makeReviewCard(data[i])
        }
    },
    error: function(data) {
        console.log("Error pulling reviews from db")
    }
});

function wineOverview() {
    $("#wineOverviewTitle").text("Overview of " + wine[1]);
    $("#wineReviewTitle").text("Reviews for " + wine[1]);

    var text = "";
    if (!wine[2]) {
        text = text + "<strong>Average price:</strong> None listed.";
    } else {text = text + "<strong>Average price:</strong> $" + wine[2]; }

    if (wine[15]) {
        var province = "";
        if (wine[16]) {
            province = "<a href=" + wine[16] + ' target = "_blank">' + wine[15] + '</a>';
        } else { province = wine[15]; }
        text = text + "<br><strong>Province: </strong>" + province;
    }

    if (wine[11]) {
        var region = "";
        if (wine[12]) {
            region = "<a href=" + wine[12] + ' target = "_blank">' + wine[11] + '</a>';
        } else { region = wine[11]; }
        text = text + "<br><strong>Region: </strong>" + region;
    }

    text = text + "<br><strong>Variety: </strong>" + wine[8];

    if (wine[9]!="No Information") {
        text = text + "<br><strong>Variety Description: </strong>" + wine[9];
    }
    if (wine[4]) {
        text = text + "<br><strong>Designation: </strong>" + wine[4];
    }
    $("#wineOverviewText").append(text);
}

function makeReviewCard(reviewInfo) {
    // reviewInfo as [description, points, tasterID, tasterName]

    title = '';
    if (reviewInfo[3]) {
        title = '<a href="/api/tasterDetail?id=' + reviewInfo[2] + '">' + reviewInfo[3] + '</a>';
    } else {
        title = 'Anonymous Reviewer';
    }
    var text = reviewInfo[0];
    var textstyle = "font-family: Dosis!important";
    var card = '<div class="card">'+
    '<div class="card-body">'+
    '<h7 class="card-title"> ' + title + '</h7>' +
    '<h8 class="card-subtitle" style="float:right">Points: ' + reviewInfo[1] + '</h8>' +
    '<p class="card-text" style="'+ textstyle +'">' + text + '</p>' +
    '</div></div>';

    $("#wineReviewContainer").append(card);
}
//Insert entry into favorites table, change button text and style
function addFavorite(wid) {
    $.ajax({
            type: 'GET',
            url: "/api/addFavorite?wid=" + wid,
            success: function(data) {
                console.log(data)
                console.log("Adding " + wid + " to favorites")
                $("#card_" + wid).text("Unfavorite")
                $("#card_" + wid).attr("onClick", "deFavorite(" + wid + ")")
                $("#card_" + wid).attr("class", "btn btn-warning")
            },
            error: function(data) {
                console.log(data)
            }
    })
}
//Delete entry from favorites table, change button text to "Unfavorite"
//and style back to green, as it started
function deFavorite(wid) {
    $.ajax({
            type: 'GET',
            url: "/api/removeFavorite?wid=" + wid,
            success: function(data) {
                console.log(data)
                console.log("Removing " + wid + " from favorites")
                $("#card_" + wid).text("Favorite")
                $("#card_" + wid).attr("onClick", "addFavorite(" + wid + ")")
                $("#card_" + wid).attr("class", "btn btn-success")
            },
            error: function(data) {
                console.log(data)
            }
    })
}

//Style buttons on page load depending on whether the wine they represent
//has been favorited or not
function prepButton(wid, favorited) {
    button = '<a style="width:45%" '
    if (favorited) {
        button += 'onClick="deFavorite(' + wid + ')" class="btn btn-warning" id="card_' + wid + '">Defavorite'
    } else {
        button += 'onClick="addFavorite(' + wid + ')" class="btn btn-success" id="card_' + wid + '">Favorite'
    }
    button += '</a>'
    // the caller might have to add </div></div> to complete the card, since this only makes the button
    return button
}

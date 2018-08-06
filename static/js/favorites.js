function addFavorite(wid) {
    $.ajax({
            type: 'GET',
            url: "/api/addFavorite?wid=" + wid,
            success: function(data) { // Response about a single UID2 status
                console.log(data)
                console.log("Adding " + wid + " to favorites")
                $("#card_" + wid).text("Unfavorite")
                // $('#card_" + wid').attr('onclick', '');
                $("#card_" + wid).attr("onClick", "deFavorite(" + wid + ")")
                $("#card_" + wid).attr("class", "btn btn-warning")
                // $("#stn-info").text(data[0][1] + " (Station # " + data[0][0] + ")")
                // console.log(data[1])
            },
            error: function(data) {
                console.log(data)
            }
    })
}
function deFavorite(wid) {
    $.ajax({
            type: 'GET',
            url: "/api/removeFavorite?wid=" + wid,
            success: function(data) { // Response about a single UID2 status
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

function prepButton(wid, favorited) {
    button = '<a style="width:45%" '
    if (favorited) {
        button += 'onClick="deFavorite(' + wid + ')" class="btn btn-warning" id="card_' + wid + '">Defavorite'
    } else {
        button += 'onClick="addFavorite(' + wid + ')" class="btn btn-success" id="card_' + wid + '">Favorite'
    }
    button += '</a>'
    console.log(button)
    // the caller might have to add </div></div> to complete the card, since this only makes the button
    return button
}

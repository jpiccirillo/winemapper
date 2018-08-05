//
//
// if (loggedin) {
//     card+= '<a '
//     if (uid == parseInt(UID)) {
//         console.log(uid, UID, "#card_" + id)
//         card+='onClick="deFavorite(' + id + ')" class="btn btn-warning" id="card_' + id + '">Defavorite'
//         // $("#card_" + id).text("DeFavorite")
//         // $("#card_" + id).css("background-color", "indianred")
//     }
//     else {
//         card+='onClick="addFavorite(' + id + ')" class="btn btn-success" id="card_' + id + '">Favorite'
//     }
//     card+='</a>'
// }
//
//
// $(".activearea").append(card);

// $(document).ready(function() {
//     if (UID == 0) return;
//     console.log("favorited: " + favorited)
//     console.log(wid)
//     card = prepButton(wid, favorited)
//     $("#toptitle h6.card-header").append(card);
//     $("#card_" + wid).css("float", "right")
// })

if (UID != 0) {
    console.log("favorited: " + favorited)
    console.log(wid)
    card = prepButton(wid, favorited)
    $("#toptitle h6.card-header").append(card);
    $("#card_" + wid).css("float", "right")
}

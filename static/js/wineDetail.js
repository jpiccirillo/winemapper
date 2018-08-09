//Render button on top of Wine Detail page
//If logged in: show button as either "Favorite" or "Unfavorite"
if (UID != 0) {
    console.log("favorited: " + favorited)
    card = prepButton(wid, favorited)
    $("#toptitle h6.card-header").append(card);
    $("#card_" + wid).css("float", "right")
}

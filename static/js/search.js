//If user has scrolled to end of containing div, call to load more results
$(document).ready(function() {
    $('.cardpane').bind('scroll', function() {
        if ($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight) {
            loadMore();
        }
    })
    //Kick map off (just 1ce) using data from render_template on Flask side
    startMap(parameters[0], parameters[1], parameters[2])
});

//Change navbar when user starts a search to make more room for fields
function prepUIforSearch() {
    $(".btn-secondary.nav.removable").hide(400)
    $(".nav-item.active.removable").hide(400)
}

//Ajax call to get more results from search function and render map /
//side bar accordingly
function loadMore() {
    console.log("about to re-search on: " + search)

    var searchquery = ""
    $.each(search, function(i, val) {
        console.log(i, val)
        if (i==7) {return false}
        searchquery += form[i] + "=" + val
        if (i!=6) {searchquery+='&&'}
    })
    console.log(searchquery)
    $.ajax({
        type: 'GET',
        url: "/api/searchLater?" + searchquery,
        success: function(data) {
            data = JSON.parse(data)
            console.log(data)
            $.each(data, function(i, entry) {
                text = prepSearchData(data[i])
                plotCards(data[i][0], 0, 0, text)
                plotMarkers('search', entry)
            })
            console.log(marker)
            group = new L.featureGroup(marker);
            map.fitBounds(group.getBounds().pad(0.15));
        },
        error: function(data) {
            console.log("Error originaing from ajax call\n")
        }
    });
}

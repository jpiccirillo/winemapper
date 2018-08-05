$(document).ready(function() {
    $('.cardpane').bind('scroll', function() {
        if ($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight) {
            // alert(search)
            loadTenMore();
        }
    })
    startMap(parameters[0], parameters[1], parameters[2])
});

function prepUIforSearch() {
    $(".btn-secondary.nav.removable").hide(400)
    $(".nav-item.active.removable").hide(400)
}

function loadTenMore() {
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
        success: function(data) { // Response about a single UID2 status
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

startMap(parameters[0], parameters[1], parameters[2])

function prepUIforSearch() {
    $(".btn-secondary.nav.removable").hide(400)
    $(".nav-item.active.removable").hide(400)
}

function startSearch() {
    // $(".nav-item .form-control").hide(200).val("")
    ids = ['title', 'variety', 'designation', 'maxprice', 'area', 'winery', 'keyword']
    url = "";
    $.each(ids, function(index, value) {
        console.log(value)
        input = $("#" + value).val()
        if (!input && value=='maxprice') {input=1000}
        if (!input) { input = ''}
        url = url + value + "=" + input + "&&"
    });
    console.log(url.slice(0, -2))
    $.ajax({
        type: 'GET',
        url: "/api/search?" + url,
        success: function(data) { // Response about a single UID2 status
            // marker = [];
            console.log(data)
            $( "html" ).load( data );
            data = JSON.parse(data)
            data = data.sort(function(a, b) {
                return a[10] - b[10]
            })
            console.log(data[data.length])
            lat = [data[0][10], data[data.length-1][10]]
            data = data.sort(function(a, b) {
                return a[11] - b[11]
            })
            lon = [data[0][11], data[-1][11]]

            // for (var i = 0; i < data.length; i++) {
            //     plotMarkers(data[i])
            // }
        },
        error: function(data) {
            console.log("Error originaing from ajax call\n")
        }
    });
}

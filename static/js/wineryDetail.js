console.log(wineryid)

getMostReviews()
getClimateData()

function getMostReviews() {
    $.ajax({
        type: 'GET',
        url: "/api/reviewedWineryMost?id=" + wineryid,
        success: function(data) { // Response about a single UID2 status

            data = JSON.parse(data)
            // console.log(data.length)
            if (data.length == 0) {
                $("#reviewer").append('Anonymous users')
                $("#numreviews").remove();
                $("#reviewlink").remove()
            }
            for (var i = 0; i < data.length; i++) {
                // console.log(data[i])
                var link = '/api/tasterDetail?id=' + data[i][0]
                var text = 'Reviewed ' + data[i][2]
                if (data[i][2] > 1) {
                    text = text + ' wines here'
                } else {
                    text = text + ' wine here'
                }
                // console.log(text)
                $("#reviewer").append(data[i][1])
                $("#numreviews").text(text);
                var button = '<a href="' + link + '" class="btn btn-secondary">View Profile</a>'
                $("#wineryOverview .card-body .card-body").append(button)
            }
        },
        error: function(data) {
            console.log("Error pulling addresses from database via cartCombo_app.py and ajax call\n")
        }
    });
}


function getClimateData() {

    var monthNameFormat = d3.time.format("%B");
    $.ajax({
        type: 'GET',
        url: "/api/getCliamteData?id=" + wineryid,
        success: function(data) { // Response about a single UID2 status

            data = JSON.parse(data)
            console.log(data)
            //
            var chart = c3.generate({
                data: {
                    x: 'x',
                    xFormat: '%Y-%m-%d', // 'xFormat' can be used as custom format of 'x'
                    columns: data,
                    type: 'spline'
                },
                axis: {
                    x: {
                        type: 'timeseries',
                        tick: {
                            format: function(x) {
                                return monthNameFormat(x);
                            },
                        },
                    },
                    y: {
                        label: '° Farenheit',
                    }
                },
                tooltip: {
                    format: {
                        value: function(value) {
                            return value.toFixed(2) + "°";
                        }
                    }
                },
                legend: {
                    position: 'inset',
                    inset: {
                        anchor: 'top-right',
                    },
                },
                grid: {
                  y: {
                    show: true
                  }
                }
                // padding: {
                //   left: 20
                // }
            });

        },
        error: function(data) {
            console.log("Error pulling addresses from database via cartCombo_app.py and ajax call\n")
        }
    });
}

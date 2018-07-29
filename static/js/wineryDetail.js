console.log(wineryid)

getMostReviews()
getClimateData()

function getMostReviews() {
    $.ajax({
        type: 'GET',
        url: "/api/reviewedWineryMost?id=" + wineryid,
        success: function(data) { // Response about a single UID2 status

            data = JSON.parse(data)
            // console.log(data[1])
            if (data.length == 0) {
                $("#reviewer").append('Anonymous users')
                $("#numreviews").remove();
                $("#reviewlink").remove()
            } else {
            // for (var i = 0; i < data.length; i++) {
                // console.log(data[i])
                var link = '/api/tasterDetail?id=' + data[0]
                var text = 'Reviewed ' + data[2]
                if (data[2] > 1) {
                    text = text + ' wines here'
                } else {
                    text = text + ' wine here'
                }
                // console.log(text)
                $("#reviewer").append(data[1])
                $("#numreviews").text(text);
                var button = '<a href="' + link + '" class="btn btn-secondary">View Profile</a>'
                $("#wineryOverview .card-body .card-body").append(button)
            }
        },
        error: function(data) {
            console.log("Error originaing from ajax call\n")
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
            $("#stn-info").text(data[0][1] + " (Station # " + data[0][0] + ")")
            console.log(data[1])
            var chart = c3.generate({
                data: {
                    x: 'x',
                    xFormat: '%Y-%m-%d', // 'xFormat' can be used as custom format of 'x'
                    columns: data[1],
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
            console.log("Error originaing from ajax call\n")
        }
    });
}

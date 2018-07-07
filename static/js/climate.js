var applications = [],
    modData = [],
    groups = [],
    dates = ['x'],
    minuteCount = ['Screentime'],
    pickupCount = ['Pickups'],
    labels = ['Appstore', 'Bumble', 'Camera', 'Google Drive', 'Google Photos', 'Facebook', 'Fitbit', 'Gmail', 'Google Maps', 'Grindr', 'Hornet', 'Instagram', 'Maps', 'Messages', 'Messenger', 'Mint', 'Moment', 'Music', 'Notes', 'OK Cupid', 'Outlook', 'Phone', 'Photos', 'Reversee', 'Safari', 'Scruff', 'Settings', 'Snapchat', 'Uber', 'Lyft', 'Weather'],
    ramps = [
        ['#8b0000', '#cb2f44', '#f47461', '#ffbd84', '#ffffe0'],
        ['#253494', '#2c7fb8', '#41b6c4', '#a1dab4', '#ffffcc'],
        ['#006837', '#31a354', '#78c679', '#c2e699', '#ffffcc'], ];
    // style = window.getComputedStyle(document.getElementById("#chart"), null);
    // width = style.getPropertyValue("width");

// d3.queue()
//     .defer(d3.csv, "../static/csv/whole_decade_STN722265.csv")
//     .await(processJSONs);

d3.text("../static/csv/whole_decade_STN722265.csv", function(text) {
    var data = d3.csv.parseRows(text).map(function(row) {
        return row.map(function(value) {
          return +value;
        });
      });
      makeChart(data);
});

function makeChart(data) {
    // console.log(parseInt(window.innerWidth/100))
    console.log(data)
    var chart = c3.generate({
        data: {
            x: 'x',
            xFormat: '%Y-%m-%dT%H:%M:%S-%L:%S',
            columns: [
                dates,
                applications[0],
                applications[1],
                applications[2],
                applications[3],
                applications[4]
            ],
            type: 'area-spline',
            groups: [groups]
        },
        point: {
            show: false
        },
        legend: {
            position: 'inset',
            reverse: true
        },
        subchart: {
            show: true
        },
        zoom: {
            rescale: true
        },
        tooltip: {
            format: {
                value: function (value) {
                    return value + " min"
                },
            }
        },
        axis: {
            x: {
                extent: [dates[32], dates[1]],
                type: 'timeseries',
                tick: {
                    fit: false,
                    format: '%m/%d',
                    //                    rotate: -45,
                    //                    multiline: false,
                    // culling: {
                    //     max: parseInt(window.innerWidth/10),
                    // }
                },
                padding: 0
            },
            y: {
                padding: {
                    bottom: 0
                }
            }
        },
        color: {
            pattern: ramps[Math.floor((Math.random() * (3 - 0) + 0))]
        },
        padding: {
            left: 25,
            right: 15
        }
    });
}

console.log("WineryID: " + wineryid)
// var showLegendCondition =

getMostReviews()
getClimateData()
plotSoilData()

$("#soilname").text(soil[0][46])

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
                var text = data[2]
                if (data[2] > 1) {
                    text = text + ' times'
                } else {
                    text = text + ' time'
                }
                // console.log(text)
                $("#reviewer").append('<a href="' + link + '" style="font-weight: 900;">' + data[1] + '</a> (' + text + ')')
                // $("#numreviews").text(text);
                // var button = '<a href="' + link + '" class="btn btn-secondary">Profile</a>'
                // $("#wineryOverview .card-body .col-md-6 .card-body .col-md-6").append(button)
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
        success: function(data) {

            data = JSON.parse(data)
            $("#stn-info").text(data[0][1] + " (Station # " + data[0][0] + ")")
            console.log(data[1])
            var chart = c3.generate({
                size: {
                  height: 270
                },
                data: {
                    x: 'x',
                    xFormat: '%Y-%m-%d', // 'xFormat' can be used as custom format of 'x'
                    columns: data[1],
                    type: 'spline'
                },
                axis: {
                    x: { type: 'timeseries',
                        tick: {
                            format: function(x) {
                                return monthNameFormat(x); },
                        },
                    },
                    y: { label: '° Farenheit', }
                },
                tooltip: {
                    format: {
                        value: function(value) {
                            return value.toFixed(2) + "°"; }
                    }
                },
                legend: {
                    position: 'inset',
                    inset: { anchor: 'top-right', },
                },
                grid: {
                  y: { show: true }
              },
                padding: {
                  right: 5,
                  // left: 5
                }
            });
        },
        error: function(data) {
            console.log("Error originaing from ajax call\n")
        }
    });
}

function plotSoilData() {
    data = []

    $.each(soil, function(i, entry) {
        console.log(entry)
        data.push([String(entry[1]), entry[3]])
    })
    console.log(data)
    var chart = c3.generate({
        bindto: '#donut',
        size: {
          height: 200
        },
        data: {
            columns: data,
            type: 'donut',
            onclick: function (d, i) { console.log("onclick", d, i); loadTable(parseInt(d.id)) },
        },
        donut: {
            label: {
                show: false,
            },
            expand: false
        },
        onresized: function () {
            if (($(document).innerWidth()>1100 || $(document).innerWidth()<575)) { chart.legend.show();}
            else {chart.legend.hide();}
        },
        legend: {
            hide: ($(document).innerWidth()>1100 || $(document).innerWidth()<575)?false:true,
            position: 'right'
        },
        tooltip: {
            format: {
                name: function(value) {
                    return "Seq #" + value}
            }
        },
        padding: {
          left: 3,
          right: -20
        }
    });
    var label = d3.select('text.c3-chart-arcs-title');

    label.html(''); // remove existant text
    label.insert('tspan').text('Sequence').attr('dy', -10).attr('x', 0);
    label.insert('tspan').text('Proportions').attr('dy', 20).attr('x', 0);
    loadTable(1)
}

function loadTable(index) {
//     5 %Gravel
// 6 %Sand
// 7 %Silt
// 8 %Clay
// 11 pH
// 12 CEC Clay
// 13 CEC Soil
// 16 CaCo<sub>3</sub>
// 17 CaSO<sub>4</sub>
//
// 20 %Gravel
// 21 %Sand
// 22 %Silt
// 23 %Clay
// 26 pH
// 27 CEC Clay
// 28 CEC Soil
// 31 CaCo<sub>3</sub>
// 32 CaSO<sub>4</sub>
    console.log(s)
    var s = soil[index-1]
    // var val = '';
    // var tsum = s[5] + s[6] + s[7] + s[8]
    // var ssum = s[20] + s[21] + s[22] + s[23]
    var top = [5, 6, 7, 8, 11, 12, 13, 16, 17]
    var sub = [20, 21, 22, 23, 26, 27, 28, 31, 32]
    $("#topsoilrow, #subsoilrow").empty()
    $("#seq").text("Soil Sequence: " + index)

    $.each(top, function(i) {
        if (s[sub[i]]==null) { val = '' }
        else if (i<4) { val = s[top[i]].toFixed(0) + " %vol" }
        else if (i==4) { val = s[top[i]]}
        else if (i<7) { val = s[top[i]] + " cmol/kg" }
        else { val = s[top[i]] + " %wt" }
        $("#topsoilrow").append("<td>" + val + "</td>")
    })
    $.each(sub, function(i) {
        if (s[sub[i]]==null) { val = '' }
        else if (i<4) { val = s[sub[i]].toFixed(0) + " %vol"}
        else if (i==4) { val = s[top[i]] }
        else if (i<7) { val = s[sub[i]] + " cmol/kg" }
        else { val = s[sub[i]] + " %wt" }
        $("#subsoilrow").append("<td>" + val + "</td>")
    })
}

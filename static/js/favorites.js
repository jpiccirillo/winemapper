function checkLogin() {
    $.ajax({
            type: 'GET',
            url: "/api/checkLoginForClient",
            success: function(data) { // Response about a single UID2 status
                console.log(data)
                // $("#stn-info").text(data[0][1] + " (Station # " + data[0][0] + ")")
                // console.log(data[1])
            },
            error: function(data) {
                console.log("Error originaing from ajax call\n")
            }
    })
}

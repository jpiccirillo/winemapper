

function insert() {
    var firstname = $("#firstname").val(),
        lastname = $("#lastname").val()
    console.log("Name to insert: " + firstname + " " + lastname)
    $.ajax({
        type: 'GET',
        url: "/api/insert?firstname=" + firstname + "&&lastname=" + lastname,
        success: function(response) {
            console.log("Response from server: " + response);
        }
    });
}

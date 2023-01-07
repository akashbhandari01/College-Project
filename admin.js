var attempt = 3;
function validate() {
    var username = document.getElementById("uname").value;
    var password = document.getElementById("pass").value;
    if (username == "admin" && password == "password") {
        window.location.href = "admin.html";
    }
    else {
        attempt--;
        alert("You have left " + attempt + " attempt;");
        if (attempt == 0) {
            document.getElementById("uname").disabled = true;
            document.getElementById("pass").disabled = true;
            document.getElementById("submit").disabled = true;
            return false;
        }
    }
}
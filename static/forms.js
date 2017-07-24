function showUpdateForm(evt) {
    $("#update").addClass("hidden");
    $("#updateform").removeClass("hidden");
}

function showLoginForm(evt) {
    $("#showlogin").addClass("hidden");
    $("#loginform").removeClass("hidden");
}

$("#update").on("click", showUpdateForm);

$("#showlogin").on("click", showLoginForm);


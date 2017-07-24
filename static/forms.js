function showUpdateForm(evt) {
    $("#update").addClass("hidden");
    $("#updateform").removeClass("hidden");
}

function showLoginForm(evt) {
    $("#showlogin").addClass("hidden");
    $("#loginform").removeClass("hidden");
}

function showCreateAcct(evt) {
    $("#showcreateacct").addClass("hidden");
    $("#createacct").removeClass("hidden");
}

$("#update").on("click", showUpdateForm);

$("#showlogin").on("click", showLoginForm);

$("#showcreateacct").on("click", showCreateAcct);


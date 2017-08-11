// AJAX calls to display forms that are hidden by default

// show update info form on profile page
function showUpdateForm(evt) {
    $("#update").addClass("hidden");
    $("#updateform").removeClass("hidden");
}

// show login form on home page
function showLoginForm(evt) {
    $("#showlogin").addClass("hidden");
    $("#loginform").removeClass("hidden");
}

// show create account form on homepage
function showCreateAcct(evt) {
    $("#showcreateacct").addClass("hidden");
    $("#createacct").removeClass("hidden");
}

$("#update").on("click", showUpdateForm);

$("#showlogin").on("click", showLoginForm);

$("#showcreateacct").on("click", showCreateAcct);


function showUpdateForm(evt) {
    $("#update").addClass("hidden");
    $("#updateform").removeClass("hidden");
}

// function submitUpdateForm(evt) {
//     $.post("/update-account")
// }

$("#update").on("click", showUpdateForm);

// $("#updateform").on("submit", submitUpdateForm);
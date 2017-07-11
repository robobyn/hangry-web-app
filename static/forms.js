function showUpdateForm(evt) {
    $("#update").addClass("hidden");
    $("#updateform").removeClass("hidden");
}

$("#update").on("click", showUpdateForm);


$(function () {

    function getMoreInfo(evt) {

        var name = this.id;

        $.get("/show-more", {"name": name}, showMoreInfo);

        evt.preventDefault();
    }

    function showMoreInfo(data) {

        console.log(data.status);

        var name = data.name;
        var reviews = data.reviews;
        var photos = data.photos;
        var menu = data.menu;

        // $("#more-info").html(name, reviews, photos, menu);
        $("#more-info").html(name);
    }

    $(".restaurant").on("click", getMoreInfo);
});
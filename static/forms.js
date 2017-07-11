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

        $(".reviews").empty();
        $(".photos").empty();

        $(".reviews").html("<h3>Top 3 Yelp reviews: </h3>");
        $(".photos").html("<h3>Photos from " + name + "</h3>");

        for (var index = 0; index < reviews.length; index++) {

            var rating = reviews[index]["rating"];
            var reviewText = reviews[index]["text"];
            $(".reviews").append("Rating: " + rating + ": " + reviewText + "<br><br>");

        }

        for (var i = 0; i < photos.length; i++) {
            $(".photos").append('<img src=' + photos[i] + ' height="250">');
        }

    }

    $(".restaurant").on("click", getMoreInfo);
});
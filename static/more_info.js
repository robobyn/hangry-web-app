$(function () {

    function getMoreInfo(evt) {

        var name = this.id;

        console.log("we're in get more info");
        console.log(name);

        $.get("/show-more", {"name": name}, showMoreInfo);

        evt.preventDefault();
    }

    function showMoreInfo(data) {

        console.log(data.status);
        console.log(data);

        var name = data.name;
        var reviews = data.reviews;
        var photos = data.photos;

        $("#reviews").empty().removeClass("hidden");
        $("#photos").empty().removeClass("hidden");
        $("#menu").empty();

        $("#reviews").html("<h3>Top 3 Yelp reviews: </h3>");
        $("#photos").html("<h3>Photos from " + name + "</h3>");

        showReviews(reviews);

        showPhotos(photos);

    }

    $(".restaurant").on("click", getMoreInfo);
});

function showReviews(reviews) {

    for (var i = 0; i < reviews.length; i++) {

        var rating = reviews[i]["rating"];
        var reviewText = reviews[i]["text"];
        $("#reviews").append("Rating: " + rating + ": " + reviewText + "<br><br>");

    }

}

function showPhotos(photos) {

    for (var i = 0; i < photos.length; i++) {

        $("#photos").append('<img src=' + photos[i] + ' height="250">&nbsp;');

    }

}
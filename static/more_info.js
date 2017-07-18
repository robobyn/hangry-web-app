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
        var openNow = data.openNow;
        var orderUrl = data.orderUrl;

        $(".show-more").removeClass("hidden");
        $("#reviews").empty().removeClass("hidden");
        $("#photos").empty().removeClass("hidden");
        $("#menu").empty();
        $("#order-info").empty();

        $("#reviews").html("<h3>Recommended Yelp reviews: </h3>");
        $("#photos").html("<h3>Photos from " + name + "</h3>");

        showOrderInfo(name, openNow, orderUrl);

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

function showOrderInfo(name, openNow, orderUrl) {

    $("#order-info").removeClass("hidden").append("<h1>" + name + "</h1>");

    if (openNow) {
        $("#order-info").append("<p>" + name + " is open now</p>");
        $("#order-info").append("<a href='" + orderUrl + "'>Click here</a> to order from EatStreet!<br>");
    } else {
        $("#order-info").append("<p>" + name + " is closed, bummer.</p>");
    }
}
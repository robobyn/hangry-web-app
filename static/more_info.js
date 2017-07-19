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

        if (rating == 1) {
            imgHtml = '<img src="/static/yelp_stars/web_and_ios/small/small_1.png">';
            $("#reviews").append("Rating " + imgHtml + " " + reviewText + "<br><br>");
        }
        else if (rating == 1.5) {
            imgHtml = '<img src="/static/yelp_stars/web_and_ios/small/small_1_half.png">';
            $("#reviews").append("Rating " + imgHtml + " " + reviewText + "<br><br>");
        }
        else if (rating == 2) {
            imgHtml = '<img src="/static/yelp_stars/web_and_ios/small/small_2.png">';
            $("#reviews").append("Rating " + imgHtml + " " + reviewText + "<br><br>");
        }
        else if (rating == 2.5) {
            imgHtml = '<img src="/static/yelp_stars/web_and_ios/small/small_2_half.png">';
            $("#reviews").append("Rating " + imgHtml + " " + reviewText + "<br><br>");
        }
        else if (rating == 3) {
            imgHtml = '<img src="/static/yelp_stars/web_and_ios/small/small_3.png">';
            $("#reviews").append("Rating " + imgHtml + " " + reviewText + "<br><br>");
        }
        else if (rating == 3.5) {
            imgHtml = '<img src="/static/yelp_stars/web_and_ios/small/small_3_half.png">';
            $("#reviews").append("Rating " + imgHtml + " " + reviewText + "<br><br>");
        }
        else if (rating == 4) {
            imgHtml = '<img src="/static/yelp_stars/web_and_ios/small/small_4.png">';
            $("#reviews").append("Rating " + imgHtml + " " + reviewText + "<br><br>");
        }
        else if (rating == 4.5) {
            imgHtml = '<img src="/static/yelp_stars/web_and_ios/small/small_4_half.png">';
            $("#reviews").append("Rating " + imgHtml + " " + reviewText + "<br><br>");
        }
        else if (rating == 5) {
            imgHtml = '<img src="/static/yelp_stars/web_and_ios/small/small_5.png">';
            $("#reviews").append("Rating " + imgHtml + " " + reviewText + "<br><br>");
        }
    }
}

function showPhotos(photos) {

    for (var i = 0; i < photos.length; i++) {

        $("#photos").append('<img src=' + photos[i] + ' width="80%"><br><br>');

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
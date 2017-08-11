// functions to display more information on clicking restaurant name
// information shows on search-results template

$(function () {

    function getMoreInfo(evt) {

        var name = this.id;

        // get information from show-more server route
        // call showMoreInfo function
        $.get("/show-more", {"name": name}, showMoreInfo);

        evt.preventDefault();
    }

    function showMoreInfo(data) {

        // use data from server API call
        var name = data.name;
        var reviews = data.reviews;
        var photos = data.photos;
        var openNow = data.openNow;
        var orderUrl = data.orderUrl;

        // show fields where info will display on search-results template
        // empty any current information in the fields
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

        // if else statements determine which Yelp star image should be shown
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

    // format photos from Yelp API to display on search-results template
    for (var i = 0; i < photos.length; i++) {

        $("#photos").append('<img src=' + photos[i] + ' class="img-rounded" width="80%"><br><br>');

    }

}

function showOrderInfo(name, openNow, orderUrl) {

    // determine if restaurant is open and show user link to order if open
    $("#order-info").removeClass("hidden").append("<h2>" + name + "</h2>");

    if (openNow) {
        $("#order-info").append("<p>" + name + " is open now</p>");
        $("#order-info").append("<a href='" + orderUrl + "'>Click here</a> to order from EatStreet!<br>");
    } else {
        $("#order-info").append("<p>" + name + " is closed, bummer.</p>");
    }
}
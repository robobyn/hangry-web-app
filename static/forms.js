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
        var menuSections = data.menuSections;
        var menuItems = data.menuItems;

        $(".reviews").empty();
        $(".photos").empty();

        $(".reviews").html("<h3>Top 3 Yelp reviews: </h3>");
        $(".photos").html("<h3>Photos from " + name + "</h3>");
        $(".menu").html("<h3>" + name + " Menu</h3>");

        showRatings(reviews);

        showPhotos(photos);

        showSections(menuSections);

        showItems(menuItems);

        debugger;

    }

    $(".restaurant").on("click", getMoreInfo);
});

function showRatings(reviews) {

    for (var i = 0; i < reviews.length; i++) {

        var rating = reviews[i]["rating"];
        var reviewText = reviews[i]["text"];
        $(".reviews").append("Rating: " + rating + ": " + reviewText + "<br><br>");

    }

}

function showPhotos(photos) {

    for (var i = 0; i < photos.length; i++) {

        $(".photos").append('<img src=' + photos[i] + ' height="250">');

    }

}

function showSections(sections) {

    for (var i = 0; i < sections.length; i++) {

        $(".menu-sections").append("<p>" + sections[i] + "</p>");

    }
}

function showItems(items) {

    for (var i = 0; i < items.length; i++) {

        console.log("i am in the showItems for loop");

        var subList = items[i];

        console.log(subList);

        for (var ii = 0; ii < subList; ii++) {

            var name = subList[ii]["name"];
            var price = subList[ii]["basePrice"];

            console.log("i am in the nested for loop");

            $(".menu-items").append("<p>" + name + ": $" + price + "</p>");

        }

        // $(".menu-items").append("<br>");

    }
}




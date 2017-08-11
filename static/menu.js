// templating for restaurant menus - uses handlebars library
// restaurant menus display on search-results template

$(function () {

    function getMenu(evt) {

        var menuName = this.value;

        // gets information from /show-menu server route
        $.get("/show-menu", {"menuName": menuName}, showMenu);

        evt.preventDefault();
    }

    function showMenu(data) {

        // empty any information currently displayed in fields
        $("#reviews").empty().addClass("hidden");
        $("#photos").empty().addClass("hidden");
        $("#order-info").empty().addClass("hidden");

        // make sure fields are no longer hidden
        $(".show-more").removeClass("hidden");
        $("#menu").removeClass("hidden");

        // compiling data to be displayed in search-results template
        var templateScript = $("#menu-template").html();

        var theTemplate = Handlebars.compile(templateScript);

        var context = data;

        var compiledHtml = theTemplate(context);

        // fill element with menu id with compiled data
        $("#menu").html(compiledHtml);

        $("#hide-menu").on("click", hideMenu);

    }

    // empty and hide menu on clicking hide menu button
    function hideMenu(evt) {

        $("#menu").empty().addClass("hidden");
        $(".show-more").addClass("hidden");

    }

    $(".menu-button").on("click", getMenu);

    

});


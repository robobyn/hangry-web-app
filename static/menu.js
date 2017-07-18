$(function () {

    function getMenu(evt) {

        var menuName = this.value;

        console.log(menuName);

        $.get("/show-menu", {"menuName": menuName}, showMenu);

        evt.preventDefault();
    }

    function showMenu(data) {

        $("#reviews").empty().addClass("hidden");
        $("#photos").empty().addClass("hidden");
        $("#order-info").empty().addClass("hidden");
        $(".show-more").removeClass("hidden");
        $("#menu").removeClass("hidden");

        var templateScript = $("#menu-template").html();

        var theTemplate = Handlebars.compile(templateScript);

        var context = data;

        console.log(context);

        var compiledHtml = theTemplate(context);

        $("#menu").html(compiledHtml);

        $("#hide-menu").on("click", hideMenu);

    }

    function hideMenu(evt) {

        $("#menu").empty().addClass("hidden");

    }

    $(".menu-button").on("click", getMenu);

    

});


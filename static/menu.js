$(function () {

    function getMenu(evt) {

        var menuName = this.value;

        console.log(menuName);

        $.get("/show-menu", {"menuName": menuName}, showMenu);

        evt.preventDefault();
    }

    function showMenu(data) {

        var templateScript = $("#menu-template").html();

        var theTemplate = Handlebars.compile(templateScript);

        var context = data;

        console.log(context);

        var compiledHtml = theTemplate(context);

        $("#menu").html(compiledHtml);

    }

    $(".menu").on("click", getMenu);

});


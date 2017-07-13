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

    }

    $(".menu").on("click", getMenu);

});







// function showSections(sections) {

//     for (var i = 0; i < sections.length; i++) {

//         $(".menu-sections").append("<p>" + sections[i] + "</p>");

//     }
// }

// function showItems(items) {

//     for (var i = 0; i < items.length; i++) {

//         console.log("i am in the showItems for loop");

//         var subList = items[i];

//         console.log(subList);

//         for (var ii = 0; ii < subList; ii++) {

//             var name = subList[ii]["name"];
//             var price = subList[ii]["basePrice"];

//             console.log("i am in the nested for loop");

//             $(".menu-items").append("<p>" + name + ": $" + price + "</p>");

//         }

//         // $(".menu-items").append("<br>");

//     }
// }




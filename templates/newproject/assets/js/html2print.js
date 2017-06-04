
$(function() {

    // Cloning the master page
    for (i = 0; i < nb_page; i++){
        $("#master-page").clone().attr("id","page-"+i).insertBefore($("#master-page"));
    }
    $("#master-page").attr("data-width", $(".paper:first-child").width()).hide();

});

$(function(){
    $(".loading").on("click", function(event){
        $.LoadingOverlay("show");
        // setTimeout(function(){
        //     $.LoadingOverlay("hide");
        // }, 3000);
    });
});

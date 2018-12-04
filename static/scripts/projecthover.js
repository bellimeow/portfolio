$(document).ready(function() {

    
    

    $(".project").mouseenter(function(e) {
	var target = $(e.currentTarget);
	
	target.children(".hidden-project").css("opacity", 1)
    });

    $(".project").mouseleave(function(e) {
	var target = $(e.currentTarget);
	target.children(".hidden-project").css("opacity", 0);
	
    });


});



			     



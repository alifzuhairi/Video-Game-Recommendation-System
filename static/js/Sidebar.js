$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
    var element = document.getElementById("Body-Content");
    // get toggle string
    var check_toggle = document.getElementById("wrapper").className;

    if(check_toggle=="toggled" && window.matchMedia("(max-width: 700px)").matches == false){
        element.style.marginLeft = "10px";
    }
    else if(check_toggle!="toggled" && window.matchMedia("(max-width: 700px)").matches == false){
        element.style.marginLeft = "270px"; 
    }else{
        element.style.marginLeft = "10px";
    }
});
$(document).ready(function(){ 

    $("#addfr").click(function(){
        let form = document.getElementById("addfriendform");
        form.style.display = "block";
        document.getElementById("addfr").style.display = "none";
    });

    $("#addfriend").click(function(){
        let form = document.getElementById("addfriendform");
        form.style.display = "none";
        document.getElementById("addfr").style.display = "block";
    });

})
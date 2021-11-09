document.addEventListener("DOMContentLoaded", function(event){

    var a  = document.getElementById("TikTok");
    var b = document.getElementById("Insta");
    var c = document.getElementById("YouTube");
    document.getElementById("TikTok").disabled = true;
    document.getElementById("Insta").disabled = true;
    document.getElementById("YouTube").disabled= true;
    a.addEventListener('click',Tiktok_Visible());
    b.addEventListener('click',InstaVisible());
    c.addEventListener('click',YoutubeVisible());
    
});

function Tiktok_Visible(){

    var Tiktok = document.getElementById("TikTok");
    if (Tiktok.disabled == true) {
        document.getElementById("TikTok").disabled= false;
    }
    else{
        document.getElementById("TikTok").disabled= true;
    };
    
}
function InstaVisible(){

    var Insta = document.getElementById("Insta")
    if (Insta.disabled == true) {
        document.getElementById("Insta").disabled= false;
    }else{
        document.getElementById("Insta").disabled= true;
    };
};

function YoutubeVisible(){

    var Youtube = document.getElementById("YouTube");

    if (Youtube.disabled == true) {
        document.getElementById("YouTube").disabled= false;
    }else{
        document.getElementById("YouTube").disabled= true;
    };
     
};
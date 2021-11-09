document.addEventListener("DOMContentLoaded", function(event){

    var a  = document.getElementById("id_Federal_tax_classification");
    a.addEventListener('click',Show_Individual);
    document.getElementById('Payee_Id').style.visibility = "hidden";
    document.getElementById("FATCA_Id").style.visibility = "hidden";
    document.getElementById("Ss_Number_Id").style.visibility = "hidden";
    document.getElementById("EIN_Id").style.visibility = "hidden";

});

function Show_Individual(){
    var a  = document.getElementById("id_Federal_tax_classification");
    var elms = a.getElementsByTagName("option");
    var b  = document.getElementById('Payee_Id');
    var c = document.getElementById("FATCA_Id");
    var d = document.getElementById("Ss_Number_Id");
    var e = document.getElementById("EIN_Id");

    if (elms[0].selected){
        b.style.visibility = "visible";
        d.style.visibility = "visible";
        d.setAttribute("required","");
        if (c.style.visibility == "visible") {
            c.style.visibility ="hidden";
        };
        if (e.style.visibility == "visible") {
            e.style.visibility ="hidden";
            e.removeAttribute("required");
            
        };
    }
    else{

        if (b.style.visibility == "visible") {
            b.style.visibility ="hidden"
        };
        if (d.style.visibility == "visible") {
            d.style.visibility ="hidden";
            d.removeAttribute("required");
        };
        c.style.visibility = "visible";
        e.style.visibility = "visible";
        e.setAttribute("required","");
    };
    
};

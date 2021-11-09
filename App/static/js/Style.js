document.addEventListener("DOMContentLoaded", function(event){

    var Row = document.getElementById("rowid")
    var Input_Elm = Row.getElementsByTagName('input')
    var Input_lbl = Row.getElementsByTagName('label')
    var elms = document.createElement("div")
    var elms1 = document.createElement("div")
    var elms2 = document.createElement("div")
    var elms3 = document.createElement("div")
    var elms4 = document.createElement("div")
    var elms5 = document.createElement("div")
    var elms6 = document.createElement("div")
    var elms7 = document.createElement("div")
    const Input1 = Input_Elm[0]
    const Input2 = Input_Elm[1]
    const Input3 = Input_Elm[2]
    const Input4 = Input_Elm[3]
    const Input5 = Input_Elm[4]
    const Input6 = Input_Elm[5]
    const Input7 = Input_Elm[6]
    const Input8 = Input_Elm[7]
    const Input9 = Input_Elm[8]
    const Input10 = Input_Elm[9]
    const Input11 = Input_Elm[10]
    console.log(Input_Elm)
    Row.appendChild(elms)
    Row.appendChild(elms1)
    Row.appendChild(elms2)
    Row.appendChild(elms3)
    Row.appendChild(elms4)
    Row.appendChild(elms5)
    Row.appendChild(elms6)
    Row.appendChild(elms7)
    elms.setAttribute("id","colm1")
    elms1.setAttribute("id","colm2")
    elms2.setAttribute("id","colm3")
    elms3.setAttribute("id","colm4")
    elms4.setAttribute("id","colm5")
    elms5.setAttribute("id","colm6")
    elms6.setAttribute("id","colm7")
    elms7.setAttribute("id","colm8")

    elms.appendChild(Input2)
    Input2.style.padding = "5px"
    Input2.style.height = "60px"
    Input2.setAttribute("placeholder","Basic Package Name")
    elms.appendChild(Input3)
    Input3.setAttribute("placeholder","Standared Package Name")
    elms.appendChild(Input4)
    Input4.setAttribute("placeholder","Premium Package Name")
    
    elms1.appendChild(Input5)
    Input5.setAttribute("placeholder","Basic Package Description")
    Input5.style.padding = "5px"
    Input5.style.height = "120px"
    elms1.appendChild(Input6)
    Input6.setAttribute("placeholder","Basic Package Description")
    elms1.appendChild(Input7)
    Input7.setAttribute("placeholder","Basic Package Description")

    elms2.appendChild(Input8)
    Input5.setAttribute("placeholder","Basic Package Price")
    Input5.style.padding = "5px"
    Input5.style.height = "120px"
    elms2.appendChild(Input9)
    Input6.setAttribute("placeholder","Basic Package Price")
    elms2.appendChild(Input10)
    Input7.setAttribute("placeholder","Basic Package Price")

    var Cl1 = document.getElementById("colm1")
    var Cl2 = document.getElementById("colm2")
    var Cl3 = document.getElementById("colm3")
    Cl1.style.display  = "flex"
    Cl2.style.display  = "flex"
    Cl3.style.display  = "flex"
    
});
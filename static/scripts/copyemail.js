//Code and css found at https://www.w3schools.com/howto/howto_js_popup.asp and  https://clipboardjs.com/

new Clipboard('.email');


function upperEmail() {
    var popup = document.getElementById("upper-email");
    popup.classList.toggle("show");
}

function lowerEmail() {
    var popup = document.getElementById("lower-email");
    popup.classList.toggle("show");
}

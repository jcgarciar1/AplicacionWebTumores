/*  ==========================================
    SHOW UPLOADED IMAGE
* ========================================== */
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#imageResult')
                .attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
        document.getElementById( "nombre" ).innerHTML = "Change file";

        var fileName = input.files[0].name;


        document.getElementById( "upload-label" ).innerHTML = fileName;
        document.getElementById( "image-area" ).classList.remove("image-area");
        
        document.getElementById("btn-calificar").disabled = false
        document.getElementById("link").disabled = false
        /*var boton = document.createElement("button")
        boton.innerHTML = "Detectar"
        boton.classList.add("btn", "btn-dark", "btn-lg")
        document.getElementById("boton-calificar").appendChild(boton)*/

    }
}

$(function () {
    $('#upload').on('change', function () {
        readURL(input);
    });
});

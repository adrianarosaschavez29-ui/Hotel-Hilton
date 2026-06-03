function abrirModal(){
    document.getElementById("modalHuespedes").style.display="block";
}

function cerrarModal(){
    document.getElementById("modalHuespedes").style.display="none";
}

function cambiar(id, valor){
    let campo = document.getElementById(id);
    let actual = parseInt(campo.value);
    actual += valor;

    if(actual < 0){
        actual = 0;
    }
    if(id == "habitaciones" && actual < 1){
        actual = 1;
    }

    campo.value = actual;

    // Actualiza los textos dinámicos dentro del modal
    if(id == "habitaciones"){
        document.getElementById("txtHabitaciones").innerText = actual;
    }
    if(id == "adultos"){
        document.getElementById("txtAdultos").innerText = actual;
    }
    if(id == "ninos"){
        document.getElementById("txtNinos").innerText = actual;
    }
}

// Inicialización de Flatpickr cuando carga la página
document.addEventListener("DOMContentLoaded", function() {
    flatpickr("#entrada", {
        dateFormat: "d/m/Y",
        minDate: "today"
    });

    flatpickr("#salida", {
        dateFormat: "d/m/Y",
        minDate: "today"
    });

    flatpickr("#entrada_form", {
        dateFormat: "d/m/Y",
        minDate: "today"
    });

    flatpickr("#salida_form", {
        dateFormat: "d/m/Y",
        minDate: "today"
    });
});
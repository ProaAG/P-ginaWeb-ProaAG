
const URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbyLiU_AKiIYYc6q4aH2BjqaJDuNRrpOAlq2qsYeGUGtUax73xvbH5zIJCKeVvaVrTF10A/exec";

let fotosDrive = [];
let indiceFoto = 0;

window.recibirFotosDrive = function(datos) {
    fotosDrive = datos;
    mostrarGaleriaDrive();
    mostrarCarruselDrive();
};

function cargarFotosDrive() {
    const anterior = document.getElementById("script-drive");

    if (anterior) anterior.remove();

    const script = document.createElement("script");
    script.id = "script-drive";

    script.src = URL_APPS_SCRIPT +
        "?callback=recibirFotosDrive&t=" + Date.now();

    script.onerror = function() {
        document.getElementById("galeria").textContent =
            "No se pudieron cargar las fotografías.";
    };

    document.body.appendChild(script);
}

function mostrarGaleriaDrive() {
    const galeria = document.getElementById("galeria");

    galeria.innerHTML = "";

    if (fotosDrive.length === 0) {
        galeria.textContent = "Todavía no hay fotografías.";
        return;
    }

    fotosDrive.forEach(function(foto) {
        const imagen = document.createElement("img");

        imagen.src = foto.url;
        imagen.alt = foto.nombre;
        imagen.loading = "lazy";

        galeria.appendChild(imagen);
    });
}

function mostrarCarruselDrive() {
    const contenedor = document.getElementById("foto-carrusel");

    contenedor.innerHTML = "";

    if (fotosDrive.length === 0) {
        contenedor.textContent = "No hay fotografías.";
        return;
    }

    const imagen = document.createElement("img");

    imagen.src = fotosDrive[indiceFoto].url;
    imagen.alt = fotosDrive[indiceFoto].nombre;

    contenedor.appendChild(imagen);
}

document.getElementById("anterior").addEventListener("click", function() {
    if (!fotosDrive.length) return;

    indiceFoto = (indiceFoto - 1 + fotosDrive.length) % fotosDrive.length;

    mostrarCarruselDrive();
});

document.getElementById("siguiente").addEventListener("click", function() {
    if (!fotosDrive.length) return;

    indiceFoto = (indiceFoto + 1) % fotosDrive.length;

    mostrarCarruselDrive();
});

cargarFotosDrive();

setInterval(cargarFotosDrive, 60000);

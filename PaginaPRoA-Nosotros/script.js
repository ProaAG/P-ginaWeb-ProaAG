

// Conexion con Google Drive
const URL_DRIVE = "https://script.google.com/macros/s/AKfycbwAZw84lcNkJWn9F0RC9i8WeJCfdYcmtYBW_l55Ga0MEryCHkYv7sUV_bZtXUy7Q6Wb/exec";

// Cargar las fotos
function cargarFotos() {

    const pagina = window.location.pathname.toLowerCase();

    let nombreCarpeta = "";

    if (pagina.includes("nosotros")) {
        nombreCarpeta = "carrusel nosotros";
    }

    if (pagina.includes("historia")) {
        nombreCarpeta = "carrusel historia";
    }

    if (pagina.includes("orientacion")) {
        nombreCarpeta = "carrusel orientacion";
    }

    if (pagina.includes("fotos")) {
        nombreCarpeta = "fotos.n";
    }

    if (!nombreCarpeta) return;

    const conexion = document.createElement("script");

    conexion.src = URL_DRIVE + "?callback=mostrarFotos";

    document.body.appendChild(conexion);

    window.mostrarFotos = function(datos) {

        const carpeta = datos.find(c =>
            c.carpeta === nombreCarpeta
        );

        if (!carpeta) {
            console.log("No se encontró la carpeta");
            return;
        }

        if (nombreCarpeta === "fotos.n") {

            const galeria = document.querySelector(".galeria");

            if (!galeria) return;

            galeria.innerHTML = "";

            carpeta.fotos.forEach(foto => {

                const enlace = document.createElement("a");
                enlace.href = foto.url;
                enlace.target = "_blank";

                const imagen = document.createElement("img");
                imagen.src = foto.url;
                imagen.alt = foto.nombre;
                imagen.loading = "lazy";

                enlace.appendChild(imagen);
                galeria.appendChild(enlace);

            });

        } else {

            const carrusel = document.querySelector(".carrusel");

            if (!carrusel) return;

            carrusel.innerHTML = "";

            carpeta.fotos.forEach(foto => {

                const figura = document.createElement("figure");
                figura.className = "slide";

                const imagen = document.createElement("img");
                imagen.src = foto.url;
                imagen.alt = foto.nombre;

                figura.appendChild(imagen);
                carrusel.appendChild(figura);

            });

            iniciarCarrusel(carrusel);

        }

    };

}

// Carruseles
function iniciarCarrusel(c) {

    const s = [...c.querySelectorAll(".slide")];

    if (s.length === 0) return;

    let i = 0;

    c.insertAdjacentHTML("beforeend",
        '<button class="ctrl ant" type="button">&#10094;</button>' +
        '<button class="ctrl sig" type="button">&#10095;</button>' +
        '<div class="puntos"></div>'
    );

    const p = c.querySelector(".puntos");

    s.forEach((_, n) => {

        const b = document.createElement("button");
        b.type = "button";
        b.onclick = () => ir(n);

        p.append(b);

    });

    const d = [...p.children];

    const ir = n => {

        s[i].classList.remove("activo");
        d[i].classList.remove("activo");

        i = (n + s.length) % s.length;

        s[i].classList.add("activo");
        d[i].classList.add("activo");

    };

    ir(0);

    c.querySelector(".ant").onclick = () => ir(i - 1);
    c.querySelector(".sig").onclick = () => ir(i + 1);

    if (c.dataset.auto &&
        !matchMedia("(prefers-reduced-motion: reduce)").matches) {

        setInterval(() => {

            if (!c.matches(":hover")) ir(i + 1);

        }, +c.dataset.auto);

    }

}

// Menú para celulares
const m = document.querySelector(".menu-lateral");
const b = document.querySelector(".menu-boton");

if (m && b) {

    b.onclick = () => {

        b.setAttribute(
            "aria-expanded",
            m.classList.toggle("abierto")
        );

    };

}

// Iniciar conexion
cargarFotos();

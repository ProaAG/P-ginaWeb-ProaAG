
 const enlaces = document.querySelectorAll('a[href^="#"]');
 const secciones = document.querySelectorAll(".seccion");
 
 enlaces.forEach(enlace => {
 
     enlace.addEventListener("click", function(evento) {
 
         evento.preventDefault();
 
         const destino = this.getAttribute("href");
         const seccion = document.querySelector(destino);
 
         if (!seccion) return;  
 
         secciones.forEach(elemento => {
             elemento.classList.remove("visible");
         });
 
         seccion.classList.add("visible");
 
 
         document.querySelectorAll(".menu a").forEach(opcion => {
             opcion.classList.remove("activo");
         });
 
         const opcionMenu = document.querySelector(
             '.menu a[href="' + destino + '"]'
         );
 
         if (opcionMenu) {
             opcionMenu.classList.add("activo");
         }
 
     });
 
 });
 
 
 const submenuHorarios = document.getElementById("submenuHorarios");
 const contenedorHorario = document.getElementById("contenedorHorario");
 
 
 const dias = [
     "Lunes",
     "Martes",
     "Miércoles",
     "Jueves",
     "Viernes"
 ];
 
 
 const cursos = [
     { numero: "1", nombre: "Primer Año" },
     { numero: "2", nombre: "Segundo Año" },
     { numero: "3", nombre: "Tercer Año" },
     { numero: "4", nombre: "Cuarto Año" },
     { numero: "5", nombre: "Quinto Año" },
     { numero: "6", nombre: "Sexto Año" }
 ];
 
 
 
 let horariosCursos = [];
 
 
 
 async function cargarHorarios() {
 
     try {
 
         const respuesta = await fetch("horarios_cursos_proa.json");
 
         if (!respuesta.ok) {
             throw new Error("No se encontró el archivo JSON");
         }
 
         horariosCursos = await respuesta.json();
 
     } catch (error) {
 
         contenedorHorario.innerHTML =
             "<p>No se pudieron cargar los horarios. Revisá el archivo JSON.</p>";
 
         console.error("Error al cargar horarios:", error);
 
     }
 
 }
 
 
 
 submenuHorarios.addEventListener("click", function(evento) {
 
     const boton = evento.target.closest("button[data-curso]");
 
     if (!boton) return;
 
     const numeroCurso = boton.dataset.curso;
 
 
     document.querySelectorAll(".submenu-horarios button").forEach(opcion => {
         opcion.classList.remove("seleccionado");
     });
 
     boton.classList.add("seleccionado");
 
     mostrarHorario(numeroCurso);
 
 });
 
 
 
 function mostrarHorario(numeroCurso) {
 
     const clases = horariosCursos.filter(horario => {
 
         const numero = String(horario.Curso).match(/[1-6]/);
 
         return numero && numero[0] === numeroCurso;
 
     });
 
 
     const cursoElegido = cursos.find(curso =>
         curso.numero === numeroCurso
     );
 
 
     if (clases.length === 0) {
 
         contenedorHorario.innerHTML =
             "<p>No hay horarios cargados para este año.</p>";
 
         return;
 
     }
 
 
 
     clases.sort((a, b) =>
         a.HoraInicio.localeCompare(b.HoraInicio)
     );
 
 
 
     const franjas = [];
 
     clases.forEach(clase => {
 
         const horario = clase.HoraInicio + " - " + clase.HoraFin;
 
         if (!franjas.includes(horario)) {
             franjas.push(horario);
         }
 
     });
 
     franjas.sort();
 
 
 
     let tabla = `
         <h3>${cursoElegido.nombre}</h3>
 
         <div class="tabla-contenedor">
 
         <table class="tabla-horarios">
 
             <thead>
                 <tr>
                     <th>Horario</th>
                     <th>Lunes</th>
                     <th>Martes</th>
                     <th>Miércoles</th>
                     <th>Jueves</th>
                     <th>Viernes</th>
                 </tr>
             </thead>
 
             <tbody>
     `;
 
 
     franjas.forEach(franja => {
 
         tabla += `
             <tr>
                 <th>${franja}</th>
         `;
 
 
 
         dias.forEach(dia => {
 
             tabla += "<td>";
 
             const clasesDelDia = clases.filter(clase => {
 
                 return clase.Dia === dia &&
                     (clase.HoraInicio + " - " + clase.HoraFin) === franja;
 
             });
 
 
 
             clasesDelDia.forEach(clase => {
 
                 tabla += `
                     <div class="bloque-clase">
 
                         <strong>${escaparTexto(clase.Materia)}</strong>
 
                         <p>Profesor: ${escaparTexto(clase.Profesor)}</p>
 
                         <p>Aula: ${escaparTexto(clase.Aula)}</p>
 
                     </div>
                 `;
 
             });
 
             tabla += "</td>";
 
         });
 
         tabla += "</tr>";
 
     });
 
 
     tabla += `
             </tbody>
         </table>
         </div>
     `;
 
 
     contenedorHorario.innerHTML = tabla;
 
 }
 
 
 
 function escaparTexto(texto) {
 
     return String(texto ?? "").replace(/[&<>"']/g, caracter => {
 
         const caracteres = {
             "&": "&amp;",
             "<": "&lt;",
             ">": "&gt;",
             '"': "&quot;",
             "'": "&#039;"
         };
 
         return caracteres[caracter];
 
     });
 
 }
 
 
 
 cargarHorarios();
 


let datosAulasJSON = [];

const submenuAulas = document.getElementById("submenuAulas");
const contenedorAulas = document.getElementById("contenedorAulas");

async function cargarHorariosAulasJSON() {

    try {

        const respuesta = await fetch("aulas (1).json");

        console.log(
            "Registros del laboratorio:",
            datosAulasJSON.filter(r => r.Aula === "Taller de Ciencias")
        );

        if (!respuesta.ok) {
            throw new Error("No se pudo encontrar aulas.json");
        }

        datosAulasJSON = await respuesta.json();

        console.log("Horarios de aulas cargados:", datosAulasJSON);
        console.log("Cantidad de horarios:", datosAulasJSON.length);

    } catch (error) {

        console.error("Error al cargar las aulas:", error);

        contenedorAulas.innerHTML =
            "<p>No se pudieron cargar los horarios de las aulas.</p>";

    }
}

submenuAulas.addEventListener("click", function(event) {

    const boton = event.target.closest(".boton-aula");

    if (!boton) return;

    document.querySelectorAll(".boton-aula").forEach(function(b) {
        b.classList.remove("seleccionado");
    });

    boton.classList.add("seleccionado");

    mostrarHorarioAulaJSON(boton.dataset.aula);

});

        

function mostrarHorarioAulaJSON(aulaSeleccionada) {

    const horarios = datosAulasJSON.filter(function(registro) {

        return registro.Aula.trim().toLowerCase() ===
               aulaSeleccionada.trim().toLowerCase();

    });

    if (horarios.length === 0) {

        contenedorAulas.innerHTML =
            "<p>No hay horarios registrados para esta aula.</p>";

        return;
    }

   
    const dias = [
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes"
    ];

    const horas = [];

    horarios.forEach(function(registro) {

        const horario = registro.HoraInicio + " - " + registro.HoraFin;

        if (!horas.includes(horario)) {
            horas.push(horario);
        }

    });

  
    horas.sort(function(a, b) {
        return a.localeCompare(b);
    });


    let tabla = `
        <h3>${escaparHTMLAulas(aulaSeleccionada)}</h3>

        <table class="tabla-aulas">

            <thead>
                <tr>
                    <th>Horario</th>
                    <th>Lunes</th>
                    <th>Martes</th>
                    <th>Miércoles</th>
                    <th>Jueves</th>
                    <th>Viernes</th>
                </tr>
            </thead>

            <tbody>
    `;

    horas.forEach(function(horario) {

        tabla += `<tr>`;

        tabla += `<td>${horario}</td>`;

        dias.forEach(function(dia) {

            const clases = horarios.filter(function(registro) {

                return registro.Dia === dia &&
                    (registro.HoraInicio + " - " + registro.HoraFin) === horario;

            });

            tabla += `<td>`;

            if (clases.length > 0) {

                clases.forEach(function(clase) {

                    tabla += `
                        <div class="dato-aula">
                            <strong>${escaparHTMLAulas(clase.Materia)}</strong>
                            ${escaparHTMLAulas(clase.Profesor)}
                            <br>
                            Curso: ${escaparHTMLAulas(clase.Curso)}
                        </div>
                    `;

                });

            } else {

                tabla += `<span class="sin-clases">Libre</span>`;

            }

            tabla += `</td>`;

        });

        tabla += `</tr>`;

    });

    tabla += `
            </tbody>
        </table>
    `;

    contenedorAulas.innerHTML = tabla;

}


function escaparHTMLAulas(texto) {

    return String(texto ?? "").replace(/[&<>"']/g, function(caracter) {

        const caracteres = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        };

        return caracteres[caracter];

    });

}


cargarHorariosAulasJSON();

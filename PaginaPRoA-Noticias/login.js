// =========================
// ELEMENTOS DEL LOGIN
// =========================

const pantallaLogin = document.getElementById("pantallaLogin");
const panelDocente = document.getElementById("panelDocente");
const panelCuenta = document.getElementById("panelCuenta");

const btnFamilia = document.getElementById("btnFamilia");
const btnDocente = document.getElementById("btnDocente");

const formLogin = document.getElementById("formLogin");

const usuario = document.getElementById("usuario");
const contrasena = document.getElementById("contrasena");

const mensaje = document.getElementById("mensaje");
const btnCerrarCuenta = document.getElementById("btnCerrarCuenta");

const nombrePerfil = document.getElementById("nombrePerfil");
const inicialPerfil = document.getElementById("inicialPerfil");
const rolPerfil = document.getElementById("rolPerfil");
const usuarioPerfil = document.getElementById("usuarioPerfil");

function mostrarPerfil(cuenta) {
  nombrePerfil.textContent = cuenta.nombre;
  inicialPerfil.textContent = cuenta.nombre.charAt(0).toUpperCase();
  rolPerfil.textContent = cuenta.rol;
  usuarioPerfil.textContent = cuenta.nombre;
  pantallaLogin.style.display = "none";
  panelCuenta.style.display = "block";
}


// =========================
// ELEMENTOS DEL PANEL
// =========================

const btnCerrarSesion =
  document.getElementById("btnCerrarSesion");

const btnPublicar =
  document.getElementById("btnPublicar");

const btnImagenes =
  document.getElementById("btnImagenes");

const btnPublicaciones =
  document.getElementById("btnPublicaciones");


const formularioNoticia =
  document.getElementById("formularioNoticia");

const formularioImagenes =
  document.getElementById("formularioImagenes");

const publicacionesDocente =
  document.getElementById("publicacionesDocente");


// =========================
// FORMULARIO NOTICIA
// =========================

const formNoticia =
  document.getElementById("formNoticia");

const tituloNoticia =
  document.getElementById("tituloNoticia");

const categoriaNoticia =
  document.getElementById("categoriaNoticia");

const fechaNoticia =
  document.getElementById("fechaNoticia");

const imagenNoticia =
  document.getElementById("imagenNoticia");

const textoNoticia =
  document.getElementById("textoNoticia");

const btnCancelarNoticia =
  document.getElementById("btnCancelarNoticia");

const mensajeNoticia =
  document.getElementById("mensajeNoticia");


// =========================
// FORMULARIO IMÁGENES
// =========================

const imagenSubida =
  document.getElementById("imagenSubida");

const vistaPrevia =
  document.getElementById("vistaPrevia");

const btnGuardarImagen =
  document.getElementById("btnGuardarImagen");

const btnCancelarImagen =
  document.getElementById("btnCancelarImagen");

const mensajeImagen =
  document.getElementById("mensajeImagen");


// =========================
// PUBLICACIONES
// =========================

const listaPublicaciones =
  document.getElementById("listaPublicaciones");


// =========================
// SELECCIÓN DE USUARIO
// =========================

btnFamilia.addEventListener("click", function() {

  btnFamilia.classList.add("activo");

  btnDocente.classList.remove("activo");

});


btnDocente.addEventListener("click", function() {

  btnDocente.classList.add("activo");

  btnFamilia.classList.remove("activo");

});


// =========================
// LOGIN
// =========================

formLogin.addEventListener("submit", function(event) {

  event.preventDefault();

  const nombreUsuario = usuario.value.trim();
  const password = contrasena.value.trim();


  if (nombreUsuario === "" || password === "") {

    mensaje.textContent =
      "Completá todos los campos.";

    return;

  }


  // =========================
  // INGRESO DOCENTE
  // =========================

  const esDocente = btnDocente.classList.contains("activo");
  const cuenta = {
    nombre: nombreUsuario,
    rol: esDocente ? "Docente" : "Estudiante / Padre"
  };

  sessionStorage.setItem("proaAccount", JSON.stringify(cuenta));

  if (esDocente) {

    pantallaLogin.style.display = "none";

    panelDocente.style.display = "block";

    mensaje.textContent = "";

    usuario.value = "";
    contrasena.value = "";

    return;

  }


  // =========================
  // PERFIL ESTUDIANTE / PADRE
  // =========================

  mostrarPerfil(cuenta);
  mensaje.textContent = "";
  usuario.value = "";
  contrasena.value = "";

});


// =========================
// RECUPERAR PERFIL DE ESTA SESIÓN
// =========================

const cuentaGuardada = sessionStorage.getItem("proaAccount");

if (cuentaGuardada) {
  try {
    const cuenta = JSON.parse(cuentaGuardada);

    if (cuenta.rol === "Docente") {
      pantallaLogin.style.display = "none";
      panelDocente.style.display = "block";
    } else if (cuenta.nombre) {
      mostrarPerfil(cuenta);
    }
  } catch {
    sessionStorage.removeItem("proaAccount");
  }
}


// =========================
// CERRAR SESIÓN DE PERFIL
// =========================

btnCerrarCuenta.addEventListener("click", function() {
  sessionStorage.removeItem("proaAccount");
  panelCuenta.style.display = "none";
  pantallaLogin.style.display = "flex";
  btnFamilia.classList.add("activo");
  btnDocente.classList.remove("activo");
});


// =========================
// CERRAR SESIÓN
// =========================

btnCerrarSesion.addEventListener("click", function() {

  sessionStorage.removeItem("proaAccount");

  panelDocente.style.display = "none";

  pantallaLogin.style.display = "flex";


  formularioNoticia.style.display = "none";

  formularioImagenes.style.display = "none";

  publicacionesDocente.style.display = "none";


  formNoticia.reset();

  imagenSubida.value = "";

  vistaPrevia.innerHTML = `
    <p>
      La imagen seleccionada aparecerá acá.
    </p>
  `;


  mensajeNoticia.textContent = "";
  mensajeImagen.textContent = "";

});


// =========================
// CREAR NOTICIA
// =========================

btnPublicar.addEventListener("click", function() {

  formularioNoticia.style.display = "block";

  formularioImagenes.style.display = "none";

  publicacionesDocente.style.display = "none";


  formularioNoticia.scrollIntoView({
    behavior: "smooth"
  });

});


// =========================
// CANCELAR NOTICIA
// =========================

btnCancelarNoticia.addEventListener("click", function() {

  formularioNoticia.style.display = "none";

  formNoticia.reset();

  mensajeNoticia.textContent = "";

});


// =========================
// PUBLICAR NOTICIA
// =========================

formNoticia.addEventListener("submit", function(event) {

  event.preventDefault();


  mensajeNoticia.textContent =
    "Noticia lista para publicar.";


  /*
    Por ahora no guardamos la noticia.

    Cuando esté lista la base de datos,
    acá vamos a enviar estos datos:

    tituloNoticia.value
    categoriaNoticia.value
    fechaNoticia.value
    imagenNoticia.files[0]
    textoNoticia.value
  */

});


// =========================
// SUBIR IMÁGENES
// =========================

btnImagenes.addEventListener("click", function() {

  formularioImagenes.style.display = "block";

  formularioNoticia.style.display = "none";

  publicacionesDocente.style.display = "none";


  formularioImagenes.scrollIntoView({
    behavior: "smooth"
  });

});


// =========================
// VISTA PREVIA DE IMAGEN
// =========================

imagenSubida.addEventListener("change", function() {

  const archivo = imagenSubida.files[0];


  if (!archivo) {

    vistaPrevia.innerHTML = `
      <p>
        La imagen seleccionada aparecerá acá.
      </p>
    `;

    return;

  }


  const imagen = document.createElement("img");

  imagen.src = URL.createObjectURL(archivo);

  imagen.alt = "Vista previa de la imagen";


  vistaPrevia.innerHTML = "";

  vistaPrevia.appendChild(imagen);

});


// =========================
// GUARDAR IMAGEN
// =========================

btnGuardarImagen.addEventListener("click", function() {

  const archivo = imagenSubida.files[0];


  if (!archivo) {

    mensajeImagen.textContent =
      "Primero seleccioná una imagen.";

    return;

  }


  mensajeImagen.textContent =
    "Imagen lista para guardar.";


  /*
    Más adelante, cuando esté lista
    la base de datos, acá enviaremos
    el archivo al servidor.
  */

});


// =========================
// CANCELAR IMAGEN
// =========================

btnCancelarImagen.addEventListener("click", function() {

  formularioImagenes.style.display = "none";

  imagenSubida.value = "";

  vistaPrevia.innerHTML = `
    <p>
      La imagen seleccionada aparecerá acá.
    </p>
  `;

  mensajeImagen.textContent = "";

});


// =========================
// VER PUBLICACIONES
// =========================

btnPublicaciones.addEventListener("click", function() {

  publicacionesDocente.style.display = "block";

  formularioNoticia.style.display = "none";

  formularioImagenes.style.display = "none";


  publicacionesDocente.scrollIntoView({
    behavior: "smooth"
  });

});


// =========================
// EDITAR PUBLICACIÓN
// =========================

listaPublicaciones.addEventListener("click", function(event) {

  if (!event.target.classList.contains("btn-editar")) {
    return;
  }


  const publicacion =
    event.target.closest(".publicacion-docente");


  const titulo =
    publicacion.querySelector("h3").textContent.trim();

  const categoria =
    publicacion
      .querySelector(".categoria-publicacion")
      .textContent
      .trim();

  const fecha =
    publicacion
      .querySelector(".fecha-publicacion")
      .textContent
      .trim();


  formularioNoticia.style.display = "block";

  publicacionesDocente.style.display = "none";

  formularioImagenes.style.display = "none";


  tituloNoticia.value = titulo;

  categoriaNoticia.value = categoria;


  /*
    La fecha de ejemplo está escrita
    como 19/09/2026.

    El input date necesita:
    2026-09-19
  */

  if (fecha.includes("/")) {

    const partes = fecha.split("/");

    fechaNoticia.value =
      `${partes[2]}-${partes[1]}-${partes[0]}`;

  }


  mensajeNoticia.textContent =
    "Editando publicación.";


  formularioNoticia.scrollIntoView({
    behavior: "smooth"
  });

});


// =========================
// ELIMINAR PUBLICACIÓN
// =========================

listaPublicaciones.addEventListener("click", function(event) {

  if (!event.target.classList.contains("btn-eliminar")) {
    return;
  }


  const publicacion =
    event.target.closest(".publicacion-docente");


  publicacion.remove();


  mensajeNoticia.textContent = "";


});

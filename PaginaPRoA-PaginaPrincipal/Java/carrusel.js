const carrusel = document.getElementById("carouselPrincipal");
const diapositivas = Array.from(carrusel.querySelectorAll(".carrusel-slide"));
const controles = carrusel.querySelectorAll(".carrusel-control");
let indiceActual = Math.max(
  0,
  diapositivas.findIndex((diapositiva) => diapositiva.classList.contains("activo"))
);

function mostrarDiapositiva(indice) {
  indiceActual = (indice + diapositivas.length) % diapositivas.length;

  diapositivas.forEach((diapositiva, indiceDiapositiva) => {
    const activa = indiceDiapositiva === indiceActual;
    diapositiva.classList.toggle("activo", activa);
    diapositiva.setAttribute("aria-hidden", String(!activa));
  });
}

controles.forEach((control) => {
  control.addEventListener("click", () => {
    mostrarDiapositiva(indiceActual + Number(control.dataset.direccion));
    reiniciarAvanceAutomatico();
  });
});

carrusel.addEventListener("keydown", (evento) => {
  if (evento.key === "ArrowLeft" || evento.key === "ArrowRight") {
    evento.preventDefault();
    mostrarDiapositiva(indiceActual + (evento.key === "ArrowRight" ? 1 : -1));
    reiniciarAvanceAutomatico();
  }
});

const movimientoReducido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
let temporizador;

function detenerAvanceAutomatico() {
  window.clearInterval(temporizador);
  temporizador = undefined;
}

function iniciarAvanceAutomatico() {
  if (movimientoReducido || temporizador || document.hidden) return;
  temporizador = window.setInterval(() => {
    mostrarDiapositiva(indiceActual + 1);
  }, 5000);
}

function reiniciarAvanceAutomatico() {
  detenerAvanceAutomatico();
  iniciarAvanceAutomatico();
}

carrusel.addEventListener("mouseenter", detenerAvanceAutomatico);
carrusel.addEventListener("mouseleave", iniciarAvanceAutomatico);
carrusel.addEventListener("focusin", detenerAvanceAutomatico);
carrusel.addEventListener("focusout", (evento) => {
  if (!carrusel.contains(evento.relatedTarget)) iniciarAvanceAutomatico();
});
document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    detenerAvanceAutomatico();
  } else {
    iniciarAvanceAutomatico();
  }
});

iniciarAvanceAutomatico();

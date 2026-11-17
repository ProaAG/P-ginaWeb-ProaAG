document.addEventListener("DOMContentLoaded", () => {
  const menuButton = document.getElementById("abrirMenu");
  const closeMenuButton = document.getElementById("cerrarMenu");
  const sideMenu = document.getElementById("menuLateral");
  const menuBackdrop = document.getElementById("fondoMenu");

  if (menuButton && closeMenuButton && sideMenu && menuBackdrop) {
    let previousOverflow = "";

    const openMenu = () => {
      previousOverflow = document.body.style.overflow;
      menuBackdrop.hidden = false;
      sideMenu.inert = false;
      sideMenu.setAttribute("aria-hidden", "false");
      menuButton.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
      requestAnimationFrame(() => {
        menuBackdrop.classList.add("activo");
        sideMenu.classList.add("abierto");
      });
      closeMenuButton.focus();
    };

    const closeMenu = () => {
      menuBackdrop.classList.remove("activo");
      sideMenu.classList.remove("abierto");
      sideMenu.inert = true;
      sideMenu.setAttribute("aria-hidden", "true");
      menuButton.setAttribute("aria-expanded", "false");
      document.body.style.overflow = previousOverflow;
      window.setTimeout(() => {
        if (!sideMenu.classList.contains("abierto")) menuBackdrop.hidden = true;
      }, 280);
      menuButton.focus();
    };

    menuButton.addEventListener("click", openMenu);
    closeMenuButton.addEventListener("click", closeMenu);
    menuBackdrop.addEventListener("click", closeMenu);
    sideMenu.querySelectorAll("a[href^='#']").forEach((link) => {
      link.addEventListener("click", closeMenu);
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
        closeMenu();
      }
    });
  }

  const accountLink = document.getElementById("enlaceCuenta");
  const accountText = document.getElementById("textoCuenta");
  const accountAvatar = document.getElementById("avatarCuenta");

  if (accountLink && accountText && accountAvatar) {
    try {
      const account = JSON.parse(sessionStorage.getItem("proaAccount") || "null");

      if (account?.nombre) {
        accountText.textContent = account.nombre;
        accountAvatar.textContent = account.nombre.charAt(0).toUpperCase();
      }
    } catch {
      sessionStorage.removeItem("proaAccount");
    }
  }

  const onietYearFilter = document.getElementById("filtroAnioOniet");
  const onietGalleries = Array.from(
    document.querySelectorAll("[data-oniet-gallery]")
  );

  if (onietYearFilter) {
    const updateOnietGallery = () => {
      onietGalleries.forEach((gallery) => {
        gallery.hidden = gallery.dataset.onietGallery !== onietYearFilter.value;
      });
    };

    onietYearFilter.addEventListener("change", updateOnietGallery);
    updateOnietGallery();
  }

  const searchForm = document.getElementById("busquedaSecciones");
  const searchInput = document.getElementById("consultaSeccion");
  const searchMessage = document.getElementById("mensajeBusqueda");

  if (searchForm && searchInput && searchMessage) {
    const normalize = (value) => value
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .trim();

    searchForm.addEventListener("submit", (event) => {
      event.preventDefault();

      const query = normalize(searchInput.value);
      const baseQuery = query.replace(/\b20\d{2}\b/g, "").trim();

      if (!baseQuery) {
        searchMessage.textContent = "Escribí el nombre de una sección.";
        return;
      }

      const sections = Array.from(document.querySelectorAll("[data-search-terms]"));
      const match = sections.find((section) => {
        const terms = normalize(section.dataset.searchTerms);
        const visibleText = normalize(section.innerText);
        return terms.includes(baseQuery) || visibleText.includes(baseQuery);
      });

      if (!match) {
        searchMessage.textContent = "No encontré esa sección. Probá con ONIET, viajes, proyectos o rifas.";
        return;
      }

      const year = query.match(/\b20\d{2}\b/)?.[0];

      if (year && match.id === "competencias" && onietYearFilter) {
        const hasYear = Array.from(onietYearFilter.options)
          .some((option) => option.value === year);

        if (hasYear) {
          onietYearFilter.value = year;
          onietYearFilter.dispatchEvent(new Event("change"));
          searchMessage.textContent = `Te llevo al carrusel de ONIET ${year}.`;
        } else {
          searchMessage.textContent = `No hay un carrusel de ONIET para ${year}.`;
        }
      } else {
        searchMessage.textContent = `Te llevo a ${match.querySelector("h2")?.textContent.trim() || "la sección"}.`;
      }

      match.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  document.querySelectorAll("[data-carousel]").forEach((carousel) => {
    const track = carousel.querySelector("[data-carousel-track]");
    const previous = carousel.querySelector("[data-carousel-prev]");
    const next = carousel.querySelector("[data-carousel-next]");
    const indicatorsContainer = carousel.querySelector(
      "[data-carousel-indicators]"
    );

    if (!track || !previous || !next) {
      return;
    }

    const slides = Array.from(track.children);

    if (!slides.length) {
      return;
    }

    let current = 0;

    const indicators = indicatorsContainer
      ? slides.map((_, index) => {
          const indicator = document.createElement("button");

          indicator.type = "button";
          indicator.className = "indicador-competencia";
          indicator.setAttribute(
            "aria-label",
            `Ir a la foto ${index + 1}`
          );

          indicator.addEventListener("click", () => {
            show(index);
          });

          indicatorsContainer.appendChild(indicator);

          return indicator;
        })
      : [];

    function show(index) {
      current = (index + slides.length) % slides.length;

      track.style.transform = `translateX(-${current * 100}%)`;

      indicators.forEach((indicator, indicatorIndex) => {
        indicator.classList.toggle(
          "activo",
          indicatorIndex === current
        );
      });
    }

    previous.addEventListener("click", () => {
      show(current - 1);
    });

    next.addEventListener("click", () => {
      show(current + 1);
    });

    show(0);
  });

  const viewer = document.getElementById("visorCDE");
  const viewerImage = document.getElementById("imagenCDE");
  const cdePhotos = Array.from(
    document.querySelectorAll("[data-cde-image]")
  );

  if (!viewer || !viewerImage || !cdePhotos.length) {
    return;
  }

  const close = viewer.querySelector("[data-cde-close]");
  const previous = viewer.querySelector("[data-cde-prev]");
  const next = viewer.querySelector("[data-cde-next]");

  let currentPhoto = 0;

  function showPhoto(index) {
    currentPhoto = (index + cdePhotos.length) % cdePhotos.length;

    const photo = cdePhotos[currentPhoto];

    viewerImage.src = photo.dataset.cdeImage || "";
    viewerImage.alt =
      photo.dataset.cdeAlt ||
      "Foto del Centro de Estudiantes";
  }

  function openViewer(index) {
    showPhoto(index);

    viewer.classList.add("activo");
    viewer.setAttribute("aria-hidden", "false");
  }

  function closeViewer() {
    viewer.classList.remove("activo");
    viewer.setAttribute("aria-hidden", "true");
  }

  cdePhotos.forEach((photo, index) => {
    photo.addEventListener("click", () => {
      openViewer(index);
    });
  });

  close?.addEventListener("click", closeViewer);

  previous?.addEventListener("click", () => {
    showPhoto(currentPhoto - 1);
  });

  next?.addEventListener("click", () => {
    showPhoto(currentPhoto + 1);
  });

  viewer.addEventListener("click", (event) => {
    if (event.target === viewer) {
      closeViewer();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (!viewer.classList.contains("activo")) {
      return;
    }

    if (event.key === "Escape") {
      closeViewer();
    }

    if (event.key === "ArrowLeft") {
      showPhoto(currentPhoto - 1);
    }

    if (event.key === "ArrowRight") {
      showPhoto(currentPhoto + 1);
    }
  });
});

/* ==============================
   ZOOM EN LAS IMÁGENES
   ============================== */

// Crear la ventana del zoom
const ventanaZoom = document.createElement("div");
ventanaZoom.className = "zoom-imagen";
ventanaZoom.setAttribute("role", "dialog");
ventanaZoom.setAttribute("aria-modal", "true");
ventanaZoom.setAttribute("aria-label", "Imagen ampliada");

ventanaZoom.innerHTML = `
  <button
    class="cerrar-zoom"
    type="button"
    aria-label="Cerrar imagen ampliada">
    &times;
  </button>

  <img src="" alt="">
`;

document.body.appendChild(ventanaZoom);

const imagenAmpliada = ventanaZoom.querySelector("img");
const botonCerrarZoom = ventanaZoom.querySelector(".cerrar-zoom");

// Abrir el zoom al hacer clic en cualquier imagen de la página
document.addEventListener("click", function (evento) {
  const imagen = evento.target.closest("main img");

  if (!imagen || ventanaZoom.contains(evento.target)) {
    return;
  }

  imagenAmpliada.src = imagen.src;
  imagenAmpliada.alt = imagen.alt || "Imagen ampliada";

  ventanaZoom.classList.add("activo");
  document.body.style.overflow = "hidden";

  botonCerrarZoom.focus();
});

// Cerrar el zoom
function cerrarZoom() {
  ventanaZoom.classList.remove("activo");
  document.body.style.overflow = "";
}

// Cerrar con el botón X
botonCerrarZoom.addEventListener("click", cerrarZoom);

// Cerrar al hacer clic en el fondo oscuro
ventanaZoom.addEventListener("click", function (evento) {
  if (evento.target === ventanaZoom) {
    cerrarZoom();
  }
});

// Cerrar al presionar Escape
document.addEventListener("keydown", function (evento) {
  if (
    evento.key === "Escape" &&
    ventanaZoom.classList.contains("activo")
  ) {
    cerrarZoom();
  }
});

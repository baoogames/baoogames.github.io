// Baoo Games site: language switch (es/en), pixel embers, shield tilt, card tilt and reveal on scroll.
(function () {
  const raiz = document.documentElement;
  const quieto = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---- language: every text comes twice (.es / .en) and the page's lang shows one; saved choice, else the browser's
  function idioma(l) {
    raiz.lang = l;
    try { localStorage.setItem("baoo.idioma", l); } catch (e) {}
    const b = document.querySelector(".idioma");
    if (b) b.textContent = l === "es" ? "EN" : "ES";
  }
  let guardado = null;
  try { guardado = localStorage.getItem("baoo.idioma"); } catch (e) {}
  idioma(guardado || ((navigator.language || "es").toLowerCase().startsWith("es") ? "es" : "en"));
  const boton = document.querySelector(".idioma");
  if (boton) boton.addEventListener("click", () => idioma(raiz.lang === "es" ? "en" : "es"));

  // ---- pixel embers rising in the studio's colors
  const lienzo = document.getElementById("chispas");
  if (lienzo && !quieto) {
    const c = lienzo.getContext("2d");
    const colores = ["#ff6a1a", "#ff9a3d", "#7b2ff7", "#a46bff", "#ff3d7f"];
    let w, h, p = [];
    const medir = () => {
      const d = Math.min(devicePixelRatio || 1, 2);
      w = lienzo.width = innerWidth * d; h = lienzo.height = innerHeight * d;
      const n = Math.round(Math.min(90, innerWidth / 14));
      p = Array.from({ length: n }, () => nueva(true));
    };
    const nueva = (cualquiera) => ({
      x: Math.random() * w, y: cualquiera ? Math.random() * h : h + 10,
      v: (0.25 + Math.random() * 0.8) * (devicePixelRatio || 1), s: (Math.random() < 0.2 ? 4 : 2) * (devicePixelRatio || 1),
      c: colores[(Math.random() * colores.length) | 0], f: Math.random() * 6.28, a: 0.3 + Math.random() * 0.6,
    });
    const paso = () => {
      c.clearRect(0, 0, w, h);
      for (const q of p) {
        q.y -= q.v; q.f += 0.02; q.x += Math.sin(q.f) * 0.3;
        if (q.y < -10) Object.assign(q, nueva(false));
        c.globalAlpha = q.a * (0.6 + 0.4 * Math.sin(q.f * 3));
        c.fillStyle = q.c; c.fillRect(q.x, q.y, q.s, q.s);
      }
      requestAnimationFrame(paso);
    };
    addEventListener("resize", medir); medir(); paso();
  }

  // ---- the shield leans toward the pointer
  const escudo = document.querySelector(".escudo");
  if (escudo && !quieto) {
    addEventListener("pointermove", e => {
      const x = e.clientX / innerWidth - 0.5, y = e.clientY / innerHeight - 0.5;
      escudo.style.transform = `rotateY(${x * 22}deg) rotateX(${-y * 18}deg)`;
    });
  }

  // ---- cards tilt in 3D under the pointer
  if (!quieto) document.querySelectorAll(".carta:not(.secreta)").forEach(cd => {
    cd.addEventListener("pointermove", e => {
      const r = cd.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
      cd.style.transform = `perspective(900px) rotateY(${x * 10}deg) rotateX(${-y * 10}deg) translateY(-6px)`;
    });
    cd.addEventListener("pointerleave", () => (cd.style.transform = ""));
  });

  // ---- reveal sections as they scroll in
  const ver = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add("visto"); ver.unobserve(e.target); }
  }), { threshold: 0.12 });
  document.querySelectorAll(".aparece").forEach(el => ver.observe(el));
})();

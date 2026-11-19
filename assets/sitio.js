// baoogames.com: the language switch (es/en) and the trailer in Dust Rider's frame. Everything else (nav, hover,
// the hero's entrance, the moment) is the kit's (assets/kit).
(function () {
  const raiz = document.documentElement;

  // ---- language: every text comes twice (.es / .en) and the page's lang shows one; saved choice, else the browser's.
  // Pictures carry their English alt in data-alt-en.
  function idioma(l) {
    raiz.lang = l;
    try { localStorage.setItem("baoo.idioma", l); } catch (e) {}
    document.querySelectorAll(".idioma").forEach(b => { b.textContent = l === "es" ? "EN" : "ES"; });
    document.querySelectorAll("img[data-alt-en]").forEach(i => {
      if (!i.dataset.altEs) i.dataset.altEs = i.alt;
      i.alt = l === "en" ? i.dataset.altEn : i.dataset.altEs;
    });
    const t = document.querySelector(".trailer");
    if (t) t.href = t.dataset[l];
  }
  if (!raiz.hasAttribute("data-fijo")) {
    let guardado = null;
    try { guardado = localStorage.getItem("baoo.idioma"); } catch (e) {}
    idioma(guardado || ((navigator.language || "es").toLowerCase().startsWith("es") ? "es" : "en"));
    document.querySelectorAll(".idioma").forEach(b => b.addEventListener("click", () => idioma(raiz.lang === "es" ? "en" : "es")));
  }

  // ---- the trailer plays in Dust Rider's frame, in the page's language (without script the link opens the file)
  const t = document.querySelector(".trailer");
  if (t) t.addEventListener("click", ev => {
    ev.preventDefault();
    const media = document.querySelector(".marco-video");
    const v = document.createElement("video");
    Object.assign(v, { src: t.href, controls: true, autoplay: true, playsInline: true });
    const poster = media.querySelector("img");
    if (poster) v.poster = poster.currentSrc || poster.src;
    media.querySelectorAll("img").forEach(n => n.remove());
    media.scrollIntoView({ behavior: "smooth", block: "center" });
    media.append(v);
    v.focus();
  });
})();

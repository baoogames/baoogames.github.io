"""Builds baoogames.com's homepage, one page per game and the games' legal pages from juegos.json.

    python3 tools/generar.py

Writes index.html, <slug>/index.html for every game and, for a game with a folder legal/<slug>/, its legal
pages from privacy-policy.{es,en}.md -> <slug>/privacidad/ and <slug>/privacy/, and delete-account.{es,en}.md ->
<slug>/borrar-cuenta/ and <slug>/delete-account/ (needs the `markdown` package). Dust Rider's legal pages come
from its own repo (tools/web/build_site.py).

Look (2026-11): the studio's red and cream, built on the tasteskill kit in assets/kit (MIT, see its LICENSE):
system.css and its tokens, the motion layer, the film hero, one giant-type-pass moment. The homepage is the
studio's: its five games as published, in development and next. The palette is the brand's
(`start.mjs brand`), the type Sora + Figtree. Page CSS lives in assets/estilo.css; the language switch and the
trailer in assets/sitio.js.
Every text is written twice, <span class="es"> and <span class="en">; sitio.js shows one.
"""
import html, json, pathlib, re

RAIZ = pathlib.Path(__file__).resolve().parents[1]
JUEGOS = json.loads((RAIZ / "juegos.json").read_text(encoding="utf-8"))
POR_SLUG = {j["slug"]: j for j in JUEGOS}
CORREO = "contact@baoogames.com"
DR, DG = POR_SLUG["dust-rider"], POR_SLUG["double-getaway"]

FLECHA = '<svg class="m-arrow" viewBox="0 0 12 12" aria-hidden="true"><path class="m-arrow__stem" d="M1 6h8"/><path class="m-arrow__head" d="M4.5 2.5 8 6l-3.5 3.5"/></svg>'
PLAY = '<svg viewBox="0 0 18 18" aria-hidden="true"><path d="M4.5 2.6v12.8c0 .8.9 1.3 1.6.9l10.3-6.4c.6-.4.6-1.3 0-1.7L6.1 1.7c-.7-.4-1.6.1-1.6.9Z" fill="currentColor"/></svg>'
MENU = '<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M2 5h14M2 13h14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'


def e(t):
    return html.escape(t, quote=True)


def b(es, en):
    """The same text in both languages."""
    return f'<span class="es">{es}</span><span class="en">{en}</span>'


def cabeza(titulo, descripcion, base, imagen="assets/img/og.jpg", lang="es", fijo=False, extra=""):
    """<head> and the fixed bar. `base` leads back to the site's root from the page."""
    k = f"{base}assets/kit/"
    return f"""<!doctype html>
<html lang="{lang}" data-type="software" data-radius="round" data-buttons="pill" data-ground="sand" data-motion{' data-fijo' if fijo else ''}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="description" content="{e(descripcion)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descripcion)}">
<meta property="og:image" content="https://baoogames.com/{imagen}">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://baoogames.com/">
<link rel="icon" href="{base}assets/img/favicon.png">
<link rel="apple-touch-icon" href="{base}assets/img/apple-touch-icon.png">
<meta name="theme-color" content="#fefbf5">
<meta name="site-kind" content="gaming">
<meta name="page-type" content="software">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400..700&family=Figtree:wght@400..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{k}system.css">
<link rel="stylesheet" href="{k}ui/cards.css">
<link rel="stylesheet" href="{k}motion/motion.css">
<link rel="stylesheet" href="{k}backgrounds/backgrounds.css">
<link rel="stylesheet" href="{k}layout/layout.css">
<link rel="stylesheet" href="{k}icons/icon.css">
<style>
:root {{
  --p-bg: #fefbf5; --p-surface: #f6eee2; --p-ink: #2b1d17; --p-muted: #746962;
  --p-accent: #f03f2a; --p-accent-ink: #fefbf5; --p-action: #d63220; --p-action-ink: #fefbf5;
  --p-inv-bg: #2b1d17; --p-inv-surface: #382a24; --p-inv-ink: #fefbf5; --p-inv-muted: #a79f98;
  --p-inv-accent: #f03f2a; --p-inv-accent-ink: #111111; --p-inv-action: #f03f2a; --p-inv-action-ink: #111111;
  --font-display: "Sora", system-ui, sans-serif;
  --font-text: "Figtree", system-ui, sans-serif;
  --display-weight: 400;
  --display-tracking: -0.035em;
  --display-tracking-xl: -0.045em;
  --ly-scale: 0.9;
}}
</style>
<link rel="stylesheet" href="{base}assets/estilo.css">
<script>document.documentElement.classList.add('m-enter');setTimeout(()=>document.documentElement.classList.add('m-enter-done'),700)</script>
<script src="{k}backgrounds/backgrounds.js"></script>
{extra}</head>
<body>
"""


def barra(base, idioma=True):
    """The fixed bar (nav-centre): the logo, three words, the language and the main action."""
    lengua = '<button class="nav__link idioma" type="button" aria-label="English / Español">EN</button>' if idioma else ""
    return f"""<header class="nav nav--centre">
  <div class="wrap nav__bar">
    <a class="skip-link" href="#top">{b("Ir al contenido", "Skip to content")}</a>
    <a class="nav__logo" href="{base}#top"><img src="{base}assets/img/logo.svg" alt="Baoo Games" width="150" height="42"></a>
    <nav class="nav__links" aria-label="{e('Principal')}">
      <div class="nav__item"><a class="nav__link" href="{base}#publicados">{b("Publicados", "Out now")}</a></div>
      <div class="nav__item"><a class="nav__link" href="{base}#en-desarrollo">{b("En desarrollo", "In development")}</a></div>
      <div class="nav__item"><a class="nav__link" href="{base}#lo-que-viene">{b("Lo que viene", "Next")}</a></div>
      <div class="nav__item"><a class="nav__link" href="{base}#contacto">{b("Contacto", "Contact")}</a></div>
    </nav>
    <div class="nav__actions">
      {lengua}
      <a class="btn btn--primary" href="{base}#publicados">{b("Ver los juegos", "See the games")}</a>
    </div>
    <button class="nav__toggle" type="button" aria-expanded="false" aria-label="Menu">{MENU}</button>
  </div>
</header>
"""


def pie(base, cierre, idioma=True):
    """footer.closing (footer-statement): the dealt close in row 1, the links and the legal row in row 2."""
    juegos = "".join(f'<li><a href="{base}{j["slug"]}/">{e(j["nombre"])}</a></li>' for j in JUEGOS)
    legales = "".join(
        f'<li><a href="{base}{l["es"][1]}" class="es">{e(j["nombre"])}: {e(l["es"][0].lower())}</a>'
        f'<a href="{base}{l["en"][1]}" class="en">{e(j["nombre"])}: {e(l["en"][0].lower())}</a></li>'
        for j in JUEGOS for l in j["legal"] if "comentarios" not in l["es"][1])
    return f"""<footer class="footer closing footer--statement" id="contacto" aria-labelledby="close-h">
  <div class="wrap">
{cierre}
    <div class="closing__links">
      <div class="grid">
        <div class="span-4 stack-4">
          <p class="footer__lede">{b("Baoo Games es un estudio de dos amigos en Colombia que hace juegos para el teléfono.", "Baoo Games is a studio of two friends in Colombia making games for your phone.")}</p>
        </div>
        <div class="span-2 start-6 footer__col"><h3>{b("Juegos", "Games")}</h3><ul>{juegos}</ul></div>
        <div class="span-4 start-9 footer__col"><h3>{b("Privacidad", "Privacy")}</h3><ul>{legales}</ul></div>
      </div>
      <div class="footer__legal">
        <span>&copy; 2026 Baoo Games</span>
        <a href="mailto:{CORREO}">{CORREO}</a>
        {'<button class="link idioma" type="button" aria-label="English / Español">EN</button>' if idioma else ''}
      </div>
    </div>
  </div>
</footer>
<script src="{base}assets/sitio.js"></script>
<script type="module" src="{base}assets/kit/system.js"></script>
<script type="module" src="{base}assets/kit/motion/motion.js"></script>
<script type="module" src="{base}assets/kit/layout/layout.js"></script>
</body>
</html>
"""


def cierre_contacto(base):
    """close-word: the h2 and the button on one row, then the studio's name (its logo) across the .wrap."""
    return f"""    <div class="closing__cta close--word">
      <div class="section-head--split">
        <div>
          <h2 id="close-h">{b("Contacto con el estudio", "Contact the studio")}</h2>
          <p class="t-lead">{b("Prensa, alianzas o un error que encontraste en un juego: respondemos en español y en inglés.", "Press, partnerships or a bug you found in a game: we answer in Spanish and English.")}</p>
        </div>
        <a class="btn btn--primary" href="mailto:{CORREO}">{b("Escribir a Baoo Games", "Email Baoo Games")}{FLECHA}</a>
      </div>
      <a class="close__name" href="{base}#top"><img src="{base}assets/img/logo.svg" alt="Baoo Games" width="560" height="173" loading="lazy"></a>
    </div>"""


def tienda(clave, url, base):
    icono, nombre = {"ios": ("app-store", "App Store"), "android": ("google-play", "Google Play")}[clave]
    arriba = b("Descárgalo en", "Download on") if clave == "ios" else b("Disponible en", "Get it on")
    if url:
        return (f'<a class="tienda" href="{url}"><img class="ic" src="{base}assets/img/iconos/{icono}.svg" alt="" width="40" height="40">'
                f'<span><small>{arriba}</small>{nombre}</span></a>')
    return (f'<span class="tienda tienda--pronto"><img class="ic" src="{base}assets/img/iconos/{icono}.svg" alt="" width="40" height="40">'
            f'<span><small>{b("Próximamente en", "Coming to")}</small>{nombre}</span></span>')


def tiendas(j, base):
    t = j.get("tiendas", {})
    return "".join(tienda(k, t.get(k), base) for k, p in (("ios", "iOS"), ("android", "Android")) if p in j["plataformas"])


MEDIDAS = {"dr-cabalga": (1920, 1088), "dg-museo": (720, 1280), "ft-portada": (1600, 1008), "bm-portada": (1600, 1000), "ev-milo": (1280, 720)}


def juego(img, nombre, estado_es, estado_en, texto_es, texto_en, alt_es, alt_en, enlace=None):
    """A game in a row of two: its picture, its name, where it stands and one line."""
    ver = f'\n            <a class="link" href="{enlace}">{b("Ver la página de " + nombre, "See the " + nombre + " page")}</a>' if enlace else ""
    w, h = MEDIDAS[img]
    return f"""          <article class="card card--open span-6 juego">
            <figure class="frame frame--photo juego__foto"><img class="frame__img" src="assets/img/inicio/{img}.webp" alt="{e(alt_es)}" data-alt-en="{e(alt_en)}" width="{w}" height="{h}" loading="lazy" data-source="client" data-subject="{e(nombre)} art"></figure>
            <p class="juego__estado">{b(estado_es, estado_en)}</p>
            <h3>{e(nombre)}</h3>
            <p>{b(texto_es, texto_en)}</p>{ver}
          </article>"""


def inicio():
    desarrollo = "\n".join([
        juego("dg-museo", "Double Getaway", "Puzzle · pronto en iOS y Android", "Puzzle · coming to iOS and Android",
              "Deslizas una vez y los dos ladrones gemelos se mueven a la vez. Llévalos a su alcantarilla en 358 niveles.",
              "Swipe once and both twin thieves move at the same time. Get them to their manhole across 358 levels.",
              "Los dos ladrones gemelos corren por la sala de un museo con una estatuilla dorada",
              "The two twin thieves run through a museum hall with a golden statuette", "double-getaway/"),
        juego("bm-portada", "Bola Mutante", "Arcade · en pruebas en el teléfono", "Arcade · testing on phones",
              "La bola avanza sola y tú cambias su material con un toque: acero, goma, burbuja o chicle. Cada obstáculo pide el suyo.",
              "The ball rolls on its own and you change what it is made of with a tap: steel, rubber, bubble or gum. Every obstacle needs the right one.",
              "Una bola roja salta sobre púas amarillas frente a una fábrica al atardecer",
              "A red ball jumps over yellow spikes in front of a factory at dusk"),
    ])
    futuro = "\n".join([
        juego("ev-milo", "Electrovolt", "Aventura 3D · diseñando el primer nivel", "3D adventure · designing the first level",
              "Milo vive bajo tierra y descubre que el sol no quema. Con Electrovolt, un robot de antes de la IA, se enfrenta a las dos IA que mandan arriba.",
              "Milo lives underground and finds out the sun doesn't burn. With Electrovolt, a robot from before AI, he takes on the two AIs that rule up above.",
              "Milo, un muchacho con gafas de soldador, en su celda bajo tierra con literas",
              "Milo, a boy with welding goggles, in his underground cell with bunk beds"),
        juego("ft-portada", "Food Truck", "Cooperativo · en diseño", "Co-op · in design",
              "De 2 a 4 jugadores cocinan tacos, hamburguesas y perros calientes en un camión de comida mientras la policía los persigue por la ciudad.",
              "Two to four players cook tacos, burgers and hot dogs in a food truck while the police chase them across the city.",
              "Un camión de comida rojo y amarillo con dos cocineros, perseguido por una patrulla en una calle al atardecer",
              "A red and yellow food truck with two cooks, chased by a police car down a street at dusk"),
    ])

    return cabeza("Baoo Games: juegos para el teléfono hechos en Colombia",
                  "Estudio de videojuegos de Colombia. Dust Rider ya está gratis en App Store y Google Play; Double Getaway, Bola Mutante, Electrovolt y Food Truck vienen en camino.",
                  "", extra='<script>document.documentElement.classList.add(\'mo-js\');setTimeout(()=>document.documentElement.classList.add(\'mo-safe\'),2500)</script>\n'
                  '<link rel="modulepreload" href="assets/kit/moments/moments.js">\n<link rel="modulepreload" href="assets/kit/moments/lib.js">\n'
                  '<link rel="modulepreload" href="assets/kit/moments/giant-type-pass/moment.js">\n') + f"""<!-- kind: gaming (a studio and its five games; page type software)
     hero: the studio's logo and story beside a stack of three game cards (image-to-code, idea B), nav-centre, close-word, footer-statement, rhythm media-band,
     buttons pill, mark: the client's logo; palette: the brand's red and cream (start.mjs brand), type sora
     sections: published (Dust Rider), in development (Double Getaway, Bola Mutante), the studio (moment), next (Electrovolt, Food Truck)
     moments: giant-type-pass in #estudio -->
""" + barra("") + f"""<main id="top">
  <section class="hero portada" data-enter aria-labelledby="hero-h">
    <div class="wrap grid">
      <div class="span-6 portada__texto">
        <h1 id="hero-h"><img class="portada__logo" src="assets/img/logo.svg" alt="Baoo Games:" width="560" height="173"> {b("Hacemos juegos para tu teléfono", "We make games for your phone")}</h1>
        <p class="hero__lead">{b("Baoo Games son dos amigos en Colombia que hacen juegos cortos, bonitos y gratis para iPhone y Android. Uno ya está en las tiendas y cuatro vienen en camino.",
                                 "Baoo Games is two friends in Colombia making short, good-looking free games for iPhone and Android. One is out now and four more are on the way.")}</p>
        <div class="btn-row"><a class="btn btn--primary" href="#publicados">{b("Ver los juegos", "See the games")}{FLECHA}</a></div>
      </div>
      <div class="span-6 portada__pila" aria-hidden="false">
        <a class="portada__carta portada__carta--3" href="#lo-que-viene"><img src="assets/img/inicio/ft-portada.webp" width="1600" height="1008" alt="Food Truck: un camión de comida con dos cocineros al atardecer" data-alt-en="Food Truck: a food truck with two cooks at dusk" style="object-position: 22% 50%" data-source="client" data-subject="Food Truck art"></a>
        <a class="portada__carta portada__carta--2" href="#en-desarrollo"><img src="assets/img/inicio/dg-museo.webp" width="720" height="1280" style="object-position: 40% 50%" alt="Double Getaway: los dos ladrones gemelos en un museo" data-alt-en="Double Getaway: the two twin thieves in a museum" data-source="client" data-subject="Double Getaway art"></a>
        <a class="portada__carta portada__carta--1" href="#publicados"><img src="assets/img/inicio/dr-cabalga.webp" width="1920" height="1088" alt="Dust Rider: un vaquero galopa por el desierto al atardecer" data-alt-en="Dust Rider: a cowboy gallops across the desert at sunset" style="object-position: 52% 50%" fetchpriority="high" data-source="client" data-subject="Dust Rider key art"></a>
      </div>
    </div>
  </section>

  <section class="section banda banda--rayas" id="publicados" aria-labelledby="pub-h">
    <div class="wrap grid">
      <div class="span-5 stack-6">
        <div class="section-head">
          <p class="juego__estado">{b("Publicado · western · gratis", "Out now · western · free")}</p>
          <h2 id="pub-h">{b("Dust Rider, un western para tu teléfono.", "Dust Rider, a Wild West game for phones.")}</h2>
          <p>{b("Galopas por doce pueblos del Viejo Oeste y tocas a cada bandido antes de que desenfunde. También hay duelos en línea contra otra persona y un campo de tiro.",
                "Gallop through twelve Wild West towns and tap every bandit before he draws. There are online duels against another person and a shooting range too.")}</p>
        </div>
        <div class="tiendas">{tiendas(DR, "")}</div>
        <p class="publicado__enlaces"><a class="link trailer" href="assets/video/dust-rider-trailer-es.mp4" data-es="assets/video/dust-rider-trailer-es.mp4" data-en="assets/video/dust-rider-trailer-en.mp4">{b("Ver el tráiler (36 s)", "Watch the trailer (36 s)")}</a>
          <a class="link" href="dust-rider/">{b("Ver la página de Dust Rider", "See the Dust Rider page")}</a></p>
      </div>
      <figure class="frame frame--photo span-6 start-7 publicado__foto marco-video"><img class="frame__img" src="assets/img/inicio/dr-cabalga.webp" width="1920" height="1088" alt="Un vaquero galopa hacia la cámara por un desierto de mesetas rojas al atardecer" data-alt-en="A cowboy gallops toward the camera across a desert of red mesas at sunset" loading="lazy" data-source="client" data-subject="Dust Rider key art">
      </figure>
    </div>
    <svg class="ola" viewBox="0 0 1440 120" preserveAspectRatio="none" aria-hidden="true"><path d="M0 64 C 180 8, 360 8, 540 52 S 900 112, 1080 64 S 1350 16, 1440 40 V120 H0 Z"/></svg>
  </section>

  <section class="section banda banda--arena" id="en-desarrollo" aria-labelledby="des-h">
    <div class="wrap">
      <div class="section-head">
        <h2 id="des-h">{b("En desarrollo.", "In development.")} <span class="muted">{b("Dos juegos que ya probamos en el teléfono.", "Two games we already play on our phones.")}</span></h2>
      </div>
      <div class="grid">
{desarrollo}
      </div>
    </div>
  </section>

  <section class="section statement" id="estudio" data-moment="giant-type-pass" data-moment-opts='{{"image": "/assets/img/inicio/dg-mansion.webp", "travel": 60, "focusY": 55}}' aria-labelledby="estudio-h">
    <div class="wrap">
      <h2 class="mo-gt__type" id="estudio-h">{b("Dos amigos,<br>cinco juegos", "Two friends,<br>five games")}</h2>
      <div class="mo-gt__row"><p>{b("Cada juego lo hacemos entre los dos, del primer boceto a la tienda. Todos usan la misma cuenta de Baoo Games, así tu perfil te sigue de un juego a otro.",
                                    "We make every game between the two of us, from the first sketch to the store. They all share one Baoo Games account, so your profile follows you from game to game.")}</p>
        <a class="link" href="#contacto">{b("Escribirnos", "Write to us")}</a></div>
    </div>
  </section>

  <section class="section banda banda--oscura" id="lo-que-viene" aria-labelledby="viene-h">
    <div class="wrap">
      <div class="section-head">
        <h2 id="viene-h">{b("Lo que viene.", "What's next.")} <span class="muted">{b("Dos ideas más grandes que estamos diseñando.", "Two bigger ideas we are designing.")}</span></h2>
      </div>
      <div class="grid">
{futuro}
      </div>
    </div>
  </section>
</main>
""" + pie("", cierre_contacto(""))


def ficha(j):
    """A game's own page: its art as the hero, what you do, the stores and its legal pages."""
    base = "../"
    puntos = "".join(f'<li>{b(e(es), e(en))}</li>' for es, en in zip(j["puntos"]["es"], j["puntos"]["en"]))
    legales = "".join(f'<li><a class="link es" href="{base}{l["es"][1]}">{e(l["es"][0])}</a><a class="link en" href="{base}{l["en"][1]}">{e(l["en"][0])}</a></li>' for l in j["legal"])
    foto = "dr-pueblo.webp" if j["slug"] == "dust-rider" else "dg-museo.webp"
    return cabeza(f'{j["nombre"]}: {j["genero"]["es"].lower()}, de Baoo Games', j["frase"]["es"], base, j["arte"]) + barra(base) + f"""<main id="top">
  <section class="hero ficha" data-enter aria-labelledby="hero-h">
    <div class="wrap grid">
      <div class="span-6 stack-6 ficha__texto">
        <p class="ficha__estado"><img class="ficha__icono" src="{base}{j['icono']}" alt="" width="56" height="56"><span>{b(j['estado']['es'], j['estado']['en'])} · {b(e(j['genero']['es']), e(j['genero']['en']))}</span></p>
        <h1 id="hero-h">{e(j['nombre'])}</h1>
        <p class="hero__lead">{b(e(j['frase']['es']), e(j['frase']['en']))}</p>
        <ul class="puntos">{puntos}</ul>
        <div class="tiendas">{tiendas(j, base)}</div>
        <ul class="legales">{legales}</ul>
      </div>
      <figure class="frame frame--photo span-6 start-7 ficha__foto"><img class="frame__img" src="{base}assets/img/inicio/{foto}" alt="{e(j['nombre'])}" fetchpriority="high"></figure>
    </div>
  </section>
</main>
""" + pie(base, cierre_contacto(base))


LEGALES = [("privacy-policy", "privacidad", "privacy"), ("delete-account", "borrar-cuenta", "delete-account")]


def legal(j):
    """The game's legal pages, from legal/<slug>/*.md, in the site's look (one language per page)."""
    import markdown
    carpeta = RAIZ / "legal" / j["slug"]
    if not carpeta.is_dir():
        return
    for fuente, es, en in LEGALES:
        for lang, ruta, otra, nombre_otra in (("es", es, en, "English"), ("en", en, es, "Español")):
            md = carpeta / f"{fuente}.{lang}.md"
            if not md.exists():
                continue
            texto = md.read_text(encoding="utf-8")
            texto = re.sub(r"(?m)^((?![-*] |\d+\. ).+)\n(?=[-*] |\d+\. )", r"\1\n\n", texto)   # a list right under a paragraph
            cuerpo = markdown.markdown(texto)
            titulo = re.search(r"^# (.+)$", texto, re.M).group(1)
            base = "../../"
            pagina = cabeza(f"{titulo} · Baoo Games", titulo, base, j["arte"], lang=lang, fijo=True) + barra(base, idioma=False) + f"""<main id="top" class="legal">
  <div class="wrap">
    <p class="legal__nav"><a class="link" href="../">← {e(j['nombre'])}</a> <a class="link" href="../{otra}/" lang="{'en' if lang == 'es' else 'es'}">{nombre_otra}</a></p>
    <article class="legal__texto">{cuerpo}</article>
  </div>
</main>
""" + pie(base, cierre_contacto(base), idioma=False)
            escribir(f"{j['slug']}/{ruta}/index.html", pagina)


def escribir(rel, texto):
    p = RAIZ / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding="utf-8")
    print("escrito", rel)


escribir("index.html", inicio())
for j in JUEGOS:
    escribir(f"{j['slug']}/index.html", ficha(j))
    legal(j)

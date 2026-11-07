"""Builds baoogames.com's homepage and one page per game from juegos.json.

    python3 tools/generar.py

Writes index.html and <slug>/index.html for every game. A new game = a new entry in juegos.json (and its
images in assets/img/), then run this again. The legal pages (privacy, delete account, feedback) are made by
each game's own repo (Dust Rider: tools/web/build_site.py) and only linked from here.
Every text is written twice, <span class="es"> and <span class="en">; assets/sitio.js shows one.
"""
import html, json, pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[1]
JUEGOS = json.loads((RAIZ / "juegos.json").read_text(encoding="utf-8"))
FUENTES = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
           '<link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;600;700&family=Russo+One&display=swap" rel="stylesheet">')
CORREO = "contact@baoogames.com"


def e(t):
    return html.escape(t, quote=True)


def b(es, en):
    """The same text in both languages."""
    return f'<span class="es">{es}</span><span class="en">{en}</span>'


def cabeza(titulo, descripcion, base, imagen="assets/img/og.jpg"):
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(descripcion)}">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descripcion)}">
<meta property="og:image" content="https://baoogames.com/{imagen}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0b0616">
<link rel="icon" href="{base}assets/img/favicon.png">
<link rel="apple-touch-icon" href="{base}assets/img/favicon.png">
{FUENTES}
<link rel="stylesheet" href="{base}assets/estilo.css">
</head>
<body>
<div class="fondo" aria-hidden="true"><canvas id="chispas"></canvas><div class="rejilla"></div><div class="ruido"></div></div>
<header class="barra">
  <a class="marca" href="{base}"><img src="{base}assets/img/escudo.webp" alt=""><span>BAOO<b>GAMES</b></span></a>
  <nav>
    <a class="opc" href="{base}#juegos">{b("Juegos", "Games")}</a>
    <a class="opc" href="{base}#estudio">{b("Estudio", "Studio")}</a>
    <a class="opc" href="{base}#contacto">{b("Contacto", "Contact")}</a>
    <button class="idioma" type="button" aria-label="Language">EN</button>
  </nav>
</header>
"""


def pie(base):
    juegos = "".join(f'<a href="{base}{j["slug"]}/">{e(j["nombre"])}</a>' for j in JUEGOS)
    legales = "".join(
        f'<a href="{base}{l["es"][1]}" class="es">{e(j["nombre"])} · {e(l["es"][0])}</a>'
        f'<a href="{base}{l["en"][1]}" class="en">{e(j["nombre"])} · {e(l["en"][0])}</a>'
        for j in JUEGOS for l in j["legal"])
    return f"""<footer>
  <div>
    <a class="marca" href="{base}"><img src="{base}assets/img/escudo.webp" alt=""><span>BAOO<b>GAMES</b></span></a>
    <p>{b("Juegos para el teléfono, hechos en Colombia.", "Mobile games, made in Colombia.")}<br>© 2026 Baoo Games</p>
  </div>
  <div class="cols">
    <div><h4>{b("Juegos", "Games")}</h4>{juegos}</div>
    <div><h4>{b("Legal", "Legal")}</h4>{legales}</div>
    <div><h4>{b("Contacto", "Contact")}</h4><a href="mailto:{CORREO}">{CORREO}</a></div>
  </div>
</footer>
<script src="{base}assets/sitio.js"></script>
</body>
</html>
"""


def carta(j):
    return f"""<a class="carta aparece" href="{j['slug']}/" style="--c:{j['color']}">
  <div class="arte"><span class="estado">{b(j['estado']['es'], j['estado']['en'])}</span><img src="{j['arte']}" alt="{e(j['nombre'])}" loading="lazy"></div>
  <div class="info">
    <img class="icono" src="{j['icono']}" alt="" loading="lazy">
    <h3>{e(j['nombre'])}</h3>
    <span class="genero">{b(e(j['genero']['es']), e(j['genero']['en']))}</span>
    <p>{b(e(j['frase']['es']), e(j['frase']['en']))}</p>
    <span class="ver">{b("Ver juego", "See game")}</span>
  </div>
</a>"""


def inicio():
    cartas = "\n".join(carta(j) for j in JUEGOS)
    cinta = "".join(f"<span>{t}</span>" for t in ["HECHO EN COLOMBIA", "JUEGOS PARA EL TELÉFONO", "UN DEDO BASTA", "MADE IN COLOMBIA", "MOBILE GAMES", "ONE FINGER IS ENOUGH"] * 2)
    return cabeza("Baoo Games · Juegos para el teléfono", "Baoo Games es un estudio de videojuegos de Colombia. Hacemos juegos para el teléfono que se aprenden en un segundo y no se sueltan.", "") + f"""
<main>
<div class="portada">
  <div class="aparece">
    <span class="etiqueta"><i></i>{b("Estudio indie · Colombia", "Indie studio · Colombia")}</span>
    <h1><span>{b("Juegos que", "Games that")}</span><span class="brillo">{b("no puedes", "you can't")}</span><span>{b("soltar.", "put down.")}</span></h1>
    <p>{b("Somos Baoo Games. Hacemos juegos para el teléfono que se aprenden en un segundo, se juegan con un dedo y te hacen decir «una más».",
          "We're Baoo Games. We make mobile games you learn in a second, play with one finger and keep saying “one more”.")}</p>
    <div class="botones">
      <a class="boton" href="#juegos">{b("Ver nuestros juegos", "See our games")}</a>
      <a class="boton fantasma" href="#contacto">{b("Hablemos", "Get in touch")}</a>
    </div>
  </div>
  <div class="escenario aparece" aria-hidden="true">
    <div class="anillo"></div><div class="anillo dos"></div>
    <img class="escudo" src="assets/img/escudo.webp" alt="">
  </div>
</div>

<div class="cinta" aria-hidden="true"><div>{cinta}</div></div>

<section id="juegos">
  <div class="titulo aparece">
    <div><span class="mini">{b("Nuestros juegos", "Our games")}</span><h2>{b("Elige tu partida", "Pick your game")}</h2></div>
    <p>{b("Cada juego cabe en tu bolsillo y en un descanso de cinco minutos.", "Every game fits in your pocket and in a five-minute break.")}</p>
  </div>
  <div class="juegos">
{cartas}
    <div class="carta secreta aparece">
      <div class="signo">?</div>
      <h3>{b("El próximo", "What's next")}</h3>
      <p>{b("Ya estamos cocinando el siguiente. Pronto lo verás aquí.", "We're already cooking the next one. You'll see it here soon.")}</p>
    </div>
  </div>
</section>

<section id="estudio">
  <div class="estudio">
    <div class="texto aparece">
      <span class="mini">{b("El estudio", "The studio")}</span>
      <h2 style="font-size:clamp(34px,5vw,58px);line-height:1;margin:8px 0 18px">{b("Dos amigos, un escudo", "Two friends, one shield")}</h2>
      <p>{b("Baoo Games nació en Colombia con una idea simple: <strong>juegos fáciles de empezar y difíciles de soltar</strong>. Diseñamos, programamos y probamos cada juego nosotros mismos, hasta que se siente bien en la mano.",
            "Baoo Games was born in Colombia with a simple idea: <strong>games that are easy to start and hard to put down</strong>. We design, code and playtest every game ourselves until it feels right in your hand.")}</p>
    </div>
    <div class="cifras aparece">
      <div class="cifra"><b>{len(JUEGOS)}</b><span>{b("juegos en camino", "games on the way")}</span></div>
      <div class="cifra"><b>1</b><span>{b("dedo para jugar", "finger to play")}</span></div>
      <div class="cifra"><b>358</b><span>{b("niveles en Double Getaway", "levels in Double Getaway")}</span></div>
      <div class="cifra"><b>100%</b><span>{b("indie", "indie")}</span></div>
    </div>
  </div>
  <div class="valores">
    <div class="valor aparece"><div class="ico">🎮</div><h3>{b("Un segundo para aprender", "One second to learn")}</h3><p>{b("Si hay que explicarlo mucho, no está listo.", "If it needs a long explanation, it isn't ready.")}</p></div>
    <div class="valor aparece"><div class="ico">⚡</div><h3>{b("Partidas cortas", "Short sessions")}</h3><p>{b("Para la fila, el bus o el descanso.", "For the queue, the bus or the break.")}</p></div>
    <div class="valor aparece"><div class="ico">🛡️</div><h3>{b("Juego limpio", "Fair play")}</h3><p>{b("Anuncios opcionales y tu privacidad primero.", "Optional ads and your privacy first.")}</p></div>
  </div>
</section>

<section id="contacto">
  <div class="contacto aparece">
    <span class="mini">{b("Contacto", "Contact")}</span>
    <h2>{b("¿Jugamos?", "Let's play")}</h2>
    <p>{b("Prensa, alianzas, ideas o un bug que encontraste: escríbenos.", "Press, partnerships, ideas or a bug you found: drop us a line.")}</p>
    <a class="boton" href="mailto:{CORREO}">{CORREO}</a>
  </div>
</section>
</main>
""" + pie("")


def tienda(nombre, sub_es, sub_en, url):
    if url:
        return f'<a class="tienda" href="{url}"><span><small>{b(sub_es, sub_en)}</small>{nombre}</span></a>'
    return f'<span class="tienda pronto"><span><small>{b("Próximamente en", "Coming soon on")}</small>{nombre}</span></span>'


def ficha(j):
    base = "../"
    puntos = "".join(f'<li>{b(e(es), e(en))}</li>' for es, en in zip(j["puntos"]["es"], j["puntos"]["en"]))
    t = j.get("tiendas", {})
    tiendas = ""
    if "iOS" in j["plataformas"]: tiendas += tienda("App Store", "Descárgalo en", "Download on the", t.get("ios"))
    if "Android" in j["plataformas"]: tiendas += tienda("Google Play", "Disponible en", "Get it on", t.get("android"))
    legales = "".join(f'<a class="es" href="{base}{l["es"][1]}">{e(l["es"][0])}</a><a class="en" href="{base}{l["en"][1]}">{e(l["en"][0])}</a>' for l in j["legal"])
    return cabeza(f'{j["nombre"]} · Baoo Games', j["frase"]["es"], base, j["arte"]) + f"""
<main>
<div class="ficha" style="--c:{j['color']}">
  <div class="portadilla aparece"><img src="{base}{j['arte']}" alt="{e(j['nombre'])}"></div>
  <div class="aparece">
    <a class="volver" href="{base}#juegos">← {b("Todos los juegos", "All games")}</a><br><br>
    <span class="etiqueta"><i></i>{b(j['estado']['es'], j['estado']['en'])}</span>
    <h1>{e(j['nombre'])}</h1>
    <span class="genero">{b(e(j['genero']['es']), e(j['genero']['en']))}</span>
    <p class="frase">{b(e(j['frase']['es']), e(j['frase']['en']))}</p>
    <ul class="puntos">{puntos}</ul>
    <div class="tiendas">{tiendas}</div>
    {f'<div class="legales">{legales}</div>' if legales else ''}
  </div>
</div>
</main>
""" + pie(base)


def escribir(rel, texto):
    p = RAIZ / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding="utf-8")
    print("escrito", rel)


escribir("index.html", inicio())
for j in JUEGOS:
    escribir(f"{j['slug']}/index.html", ficha(j))

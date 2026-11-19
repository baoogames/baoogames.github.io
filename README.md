# baoogames.github.io

baoogames.com: the studio's homepage, one page per game, and the games' legal pages (privacy, account
deletion, feedback). Served by GitHub Pages (CNAME baoogames.com).

- **Homepage and game pages:** `index.html` and `<game>/index.html` are generated from `juegos.json` by
  `python3 tools/generar.py`. A new game = a new entry in `juegos.json` plus its images in `assets/img/`
  (icon and key art, .webp), then run the script. The look (2026-11) is the studio's red and cream on the
  tasteskill kit in `assets/kit` (MIT, its LICENSE inside; do not edit those files): page CSS in
  `assets/estilo.css`, the language switch and the trailer in `assets/sitio.js`, the homepage's pictures in
  `assets/img/inicio/` and the Dust Rider trailer (720p, es/en) in `assets/video/`.
  Every text is written in Spanish and English (`.es` / `.en`); the EN/ES button switches.
  The homepage is the studio's: the logo and its story beside three game cards, then the games as
  **Publicados** (peach, a red wave at its foot), **En desarrollo** (sand), the studio statement, and
  **Lo que viene** (dark). A game moves between them by editing `inicio()` in `tools/generar.py`.
  `ft-portada.webp` (Food Truck) is concept art from Scenario (asset_bKrs7wr8aqXJytkuFcRemjKK);
  `bm-portada.webp` is composed from Bola Mutante's own backdrop and icon.
- **Legal pages:** built by each game's repo. Dust Rider: `tools/web/build_site.py` in baoogames/dust-rider
  writes `dust-rider/*` and `app-ads.txt` from its `legal/*.md`. Other games keep their legal texts here, in
  `legal/<game>/` (privacy-policy and delete-account, .es.md/.en.md), built by `tools/generar.py`
  (needs `pip install markdown`). Do not edit generated HTML by hand.
- Colors: the smiling logo's red `#f03f2a` (buttons `#d63220`, readable on cream), cream `#fefbf5`, ink `#2b1d17`;
  type Sora (headings) and Figtree (text).

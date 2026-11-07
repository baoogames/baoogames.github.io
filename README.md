# baoogames.github.io

baoogames.com: the studio's homepage, one page per game, and the games' legal pages (privacy, account
deletion, feedback). Served by GitHub Pages (CNAME baoogames.com).

- **Homepage and game pages:** `index.html` and `<game>/index.html` are generated from `juegos.json` by
  `python3 tools/generar.py`. A new game = a new entry in `juegos.json` plus its images in `assets/img/`
  (icon and key art, .webp), then run the script. Style and effects: `assets/estilo.css`, `assets/sitio.js`.
  Every text is written in Spanish and English (`.es` / `.en`); the EN/ES button switches.
- **Legal pages:** built by each game's repo. Dust Rider: `tools/web/build_site.py` in baoogames/dust-rider
  writes `dust-rider/*` and `app-ads.txt` from its `legal/*.md`. Other games keep their legal texts here, in
  `legal/<game>/` (privacy-policy and delete-account, .es.md/.en.md), built by `tools/generar.py`
  (needs `pip install markdown`). Do not edit generated HTML by hand.
- Colors come from the BG shield: orange `#ff6a1a`, purple `#7b2ff7`, steel, on night `#0b0616`.

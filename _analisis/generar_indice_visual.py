#!/usr/bin/env python3
"""Genera un índice HTML visual de las pantallas del prototipo Stitch."""
from pathlib import Path
import re

BASE = Path("stitch_lota_ind_mito_ciudad_museo_gamificada")

# Categorías por keyword en el nombre de carpeta
CATS = [
    ("Selección de modo y onboarding", ["selecci_n_de_modo", "pasaporte", "passport"]),
    ("Mapas interactivos", ["mapa_"]),
    ("Rutas / itinerarios", ["ruta_"]),
    ("Misiones", ["misi_n_"]),
    ("Monumentos y AR", ["monumento", "encuentro_ar"]),
    ("Reportes y dashboards", ["dashboard", "reporte"]),
    ("Bitácoras y bóveda", ["bit_cora", "b_veda"]),
    ("Recompensas y canje", ["canje", "detalle_de_ficha"]),
    ("Diplomas", ["diploma"]),
    ("Modo familia", ["familia", "family_mode", "family_dashboard", "team_mission", "mission_complete"]),
    ("English versions", ["english_version"]),
    ("Otros", []),
]

def categorizar(nombre):
    n = nombre.lower()
    for cat, keys in CATS[:-1]:
        for k in keys:
            if k in n:
                return cat
    return "Otros"

def prettify(name):
    s = name.replace("_", " ").strip()
    s = re.sub(r"\s+", " ", s)
    return s.capitalize()

# Recolectar todas las pantallas
pantallas = []
for d in sorted(BASE.iterdir()):
    if not d.is_dir():
        continue
    png = d / "screen.png"
    html = d / "code.html"
    if not png.exists():
        continue
    pantallas.append({
        "dir": d.name,
        "name": prettify(d.name),
        "png": f"{d.name}/screen.png",
        "html": f"{d.name}/code.html" if html.exists() else None,
        "cat": categorizar(d.name),
    })

# Agrupar por categoría en orden definido
by_cat = {c[0]: [] for c in CATS}
for p in pantallas:
    by_cat[p["cat"]].append(p)

# Generar HTML
CSS = """
* { box-sizing: border-box; }
body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
       background: #0f1216; color: #e6e9ef; }
header { padding: 28px 40px; background: linear-gradient(135deg, #1a1f2a 0%, #0f1216 100%);
         border-bottom: 1px solid #2a3140; position: sticky; top: 0; z-index: 10; backdrop-filter: blur(8px); }
h1 { margin: 0; font-size: 22px; font-weight: 600; color: #3FE6C0; letter-spacing: -0.5px; }
.subtitle { margin-top: 6px; font-size: 13px; color: #8a93a3; }
nav { display: flex; gap: 8px; flex-wrap: wrap; padding: 16px 40px;
      background: #14181f; border-bottom: 1px solid #2a3140; }
nav a { color: #8a93a3; text-decoration: none; font-size: 13px; padding: 6px 12px;
        border-radius: 6px; transition: all 0.15s; border: 1px solid transparent; }
nav a:hover { color: #3FE6C0; border-color: #2a3140; background: #1a1f2a; }
main { padding: 28px 40px 80px; max-width: 1800px; margin: 0 auto; }
section { margin-bottom: 48px; }
h2 { font-size: 16px; font-weight: 600; color: #F5A285; margin: 0 0 16px;
     padding-bottom: 8px; border-bottom: 1px solid #2a3140; letter-spacing: -0.3px; }
.count { color: #8a93a3; font-weight: 400; font-size: 13px; margin-left: 8px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.card { background: #1a1f2a; border-radius: 8px; overflow: hidden; border: 1px solid #2a3140;
        transition: all 0.15s; display: block; text-decoration: none; color: inherit; }
.card:hover { border-color: #3FE6C0; transform: translateY(-2px); box-shadow: 0 8px 24px rgba(63,230,192,0.1); }
.card img { width: 100%; height: 200px; object-fit: cover; object-position: top; display: block;
            background: #0a0c10; border-bottom: 1px solid #2a3140; }
.card .label { padding: 10px 14px; font-size: 12px; line-height: 1.4; min-height: 38px; }
.card .name { color: #e6e9ef; font-weight: 500; }
.card .meta { color: #8a93a3; font-size: 11px; margin-top: 4px; }
.card.no-html { opacity: 0.6; }
.card.no-html::after { content: "sin HTML"; position: absolute; top: 8px; right: 8px;
                       background: #D17A4F; color: #0f1216; font-size: 10px; padding: 2px 6px;
                       border-radius: 3px; font-weight: 600; }
.card { position: relative; }
"""

nav_links = "".join(
    f'<a href="#cat-{i}">{c[0]} ({len(by_cat[c[0]])})</a>'
    for i, c in enumerate(CATS) if by_cat[c[0]]
)

sections_html = ""
for i, (cat, _) in enumerate(CATS):
    items = by_cat[cat]
    if not items:
        continue
    cards = ""
    for p in items:
        no_html_class = "" if p["html"] else " no-html"
        target = p["html"] if p["html"] else p["png"]
        cards += f'''
<a class="card{no_html_class}" href="{target}" target="_blank">
  <img src="{p["png"]}" alt="{p["name"]}" loading="lazy">
  <div class="label">
    <div class="name">{p["name"]}</div>
    <div class="meta">{p["dir"]}</div>
  </div>
</a>'''
    sections_html += f'''
<section id="cat-{i}">
  <h2>{cat}<span class="count">{len(items)} pantalla(s)</span></h2>
  <div class="grid">{cards}</div>
</section>'''

html = f"""<!DOCTYPE html>
<html lang="es-CL">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lota Indómito — Índice visual del prototipo Stitch</title>
<style>{CSS}</style>
</head>
<body>
<header>
  <h1>Lota Indómito — Índice visual del prototipo Stitch</h1>
  <div class="subtitle">{len(pantallas)} pantallas · click para abrir el HTML original de Stitch · agrupadas por categoría</div>
</header>
<nav>{nav_links}</nav>
<main>{sections_html}</main>
</body>
</html>
"""

out = BASE / "indice.html"
out.write_text(html, encoding="utf-8")
print(f"✓ Generado: {out}")
print(f"  {len(pantallas)} pantallas en {sum(1 for c in CATS if by_cat[c[0]])} categorías")

#!/usr/bin/env python3
"""
Convierte los .md de docs/ y _analisis/ en .html con un template simple
(tema oscuro, mismo branding que index.html). Pensado para correr en el fan
después de cada git pull, vía hook post-merge o systemd.

Uso:
    python3 render-docs.py [--root /var/www/lotaindomito.cl]

Sin dependencias externas (solo stdlib).
"""
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone


CSS = """
:root {
  --turquesa: #3FE6C0; --coral: #F5A285; --cobre: #D17A4F;
  --bg: #0a0c10; --bg2: #12161d; --bg3: #1a212b; --border: #232c3a;
  --text: #e8ecf3; --muted: #93a0b4;
  --teal: #65dabc; --gold: #D4AF37; --peach: #F4A261;
  --mono: "JetBrains Mono", ui-monospace, Menlo, Consolas, monospace;
  --sans: "Space Grotesk", -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
}
* { box-sizing: border-box; }
body { margin: 0; font-family: var(--sans); background: var(--bg); color: var(--text); line-height: 1.6; }

/* ─────────── NAV (idéntico a index.html) ─────────── */
nav { position: sticky; top: 0; z-index: 100; display: flex; align-items: center; gap: 32px;
      padding: 12px 40px; background: rgba(10,12,16,0.85); backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border); }
nav .brand { display: flex; align-items: center; gap: 12px; text-decoration: none; }
nav .brand svg { display: block; }
nav .brand .name { font-weight: 700; font-size: 15px; letter-spacing: 3px; color: var(--text); text-transform: uppercase; line-height: 1.1; }
nav .brand .name span { color: var(--teal); }
nav .brand .sub { font-family: var(--mono); font-size: 8.5px; letter-spacing: 2.5px; color: var(--gold); text-transform: uppercase; }
nav .links { display: flex; gap: 6px; margin-left: auto; align-items: center; }
nav .links a { color: var(--muted); text-decoration: none; font-size: 13px; letter-spacing: 0.6px;
               padding: 8px 14px; border-radius: 8px; transition: color .15s, background .15s; }
nav .links a:hover { color: var(--teal); background: rgba(101,218,188,0.08); }
nav .links a.github { color: var(--gold); border: 1px solid rgba(212,175,55,0.35); background: rgba(212,175,55,0.06); }
nav .links a.github:hover { background: rgba(212,175,55,0.14); color: #ffe9a0; }
nav .hamb { display: none; margin-left: auto; background: none; border: 1px solid var(--border); border-radius: 8px;
            width: 42px; height: 42px; cursor: pointer; position: relative; }
nav .hamb span { position: absolute; left: 10px; right: 10px; height: 2px; background: var(--text); border-radius: 2px; transition: all .25s; }
nav .hamb span:nth-child(1) { top: 14px; } nav .hamb span:nth-child(2) { top: 20px; } nav .hamb span:nth-child(3) { top: 26px; }
nav.open .hamb span:nth-child(1) { top: 20px; transform: rotate(45deg); }
nav.open .hamb span:nth-child(2) { opacity: 0; }
nav.open .hamb span:nth-child(3) { top: 20px; transform: rotate(-45deg); }
@media (max-width: 860px) {
  nav { padding: 12px 20px; }
  nav .hamb { display: block; }
  nav .links { position: fixed; top: 67px; left: 0; right: 0; flex-direction: column; align-items: stretch;
               gap: 4px; padding: 16px 20px 20px; background: rgba(10,12,16,0.97); backdrop-filter: blur(14px);
               border-bottom: 1px solid var(--border); transform: translateY(-12px); opacity: 0; pointer-events: none;
               transition: all .25s; }
  nav.open .links { transform: none; opacity: 1; pointer-events: auto; }
  nav .links a { padding: 12px 14px; font-size: 14px; }
}

/* ─────────── CONTENIDO DOC ─────────── */
.doc-header { padding: 40px 40px 8px; max-width: 920px; margin: 0 auto; }
.doc-header h1 { margin: 0; font-size: 30px; font-weight: 700; color: var(--teal); letter-spacing: -0.5px; }
.doc-header .tagline { margin-top: 6px; color: var(--gold); font-size: 11px; letter-spacing: 2px; text-transform: uppercase; font-family: var(--mono); }
main { max-width: 920px; margin: 0 auto; padding: 24px 40px 80px; }
h2 { color: var(--coral); font-size: 18px; margin-top: 32px; padding-bottom: 6px;
     border-bottom: 1px solid var(--border); }
h3 { color: var(--teal); font-size: 16px; margin-top: 24px; }
p, li { color: var(--text); }
a { color: var(--cobre); text-decoration: none; border-bottom: 1px dashed var(--cobre); }
a:hover { color: var(--teal); border-bottom-color: var(--teal); }
code { background: var(--bg2); padding: 2px 6px; border-radius: 3px;
       font-family: var(--mono); font-size: 0.9em;
       border: 1px solid var(--border); }
pre { background: var(--bg2); padding: 14px; border-radius: 6px;
      border: 1px solid var(--border); overflow-x: auto;
      font-family: var(--mono); font-size: 13px; }
pre code { background: none; padding: 0; border: none; }
blockquote { border-left: 3px solid var(--cobre); margin-left: 0; padding-left: 16px;
             color: var(--muted); }
table { border-collapse: collapse; width: 100%; margin: 16px 0; }
th, td { padding: 8px 12px; border: 1px solid var(--border); text-align: left; }
th { background: var(--bg2); color: var(--teal); font-weight: 600; }
footer { border-top: 1px solid var(--border); padding: 20px 40px; color: var(--muted);
         font-size: 12px; text-align: center; }
footer a { color: var(--coral); border-bottom-color: var(--coral); }
hr { border: none; border-top: 1px solid var(--border); margin: 24px 0; }
ul, ol { padding-left: 22px; }
"""


def md_to_html(md: str) -> str:
    """Conversión mínima de Markdown → HTML (suficiente para los docs del proyecto)."""
    lines = md.split("\n")
    out = []
    in_code = False
    in_list = False
    in_table = False
    table_rows = []

    def flush_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    def flush_table():
        nonlocal in_table, table_rows
        if in_table:
            if table_rows:
                out.append("<table>")
                head, *body = table_rows
                out.append("<thead><tr>" + "".join(f"<th>{c}</th>" for c in head) + "</tr></thead>")
                if body:
                    out.append("<tbody>")
                    for row in body:
                        out.append("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>")
                    out.append("</tbody>")
                out.append("</table>")
            table_rows = []
            in_table = False

    def inline(t: str) -> str:
        # Escapar HTML
        t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        # code inline
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        # bold
        t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
        # italic
        t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
        # links [text](url)
        t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
        return t

    i = 0
    while i < len(lines):
        line = lines[i]
        # Code block fence
        if line.strip().startswith("```"):
            flush_list(); flush_table()
            if not in_code:
                lang = line.strip()[3:].strip()
                out.append(f"<pre><code class=\"lang-{lang}\">" if lang else "<pre><code>")
                in_code = True
            else:
                out.append("</code></pre>")
                in_code = False
            i += 1
            continue
        if in_code:
            out.append(line.replace("<", "&lt;").replace(">", "&gt;"))
            i += 1
            continue

        # Heading
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush_list(); flush_table()
            level = len(m.group(1))
            content = inline(m.group(2))
            out.append(f"<h{level}>{content}</h{level}>")
            i += 1
            continue

        # Table row
        if "|" in line and re.match(r"^\s*\|", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            table_rows.append(cells)
            in_table = True
            i += 1
            continue
        else:
            flush_table()

        # Horizontal rule
        if re.match(r"^\s*---\s*$", line) or re.match(r"^\s*\*\*\*\s*$", line):
            flush_list()
            out.append("<hr>")
            i += 1
            continue

        # List item
        m = re.match(r"^\s*[-*]\s+(.*)$", line)
        if m:
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{inline(m.group(1))}</li>")
            i += 1
            continue
        m = re.match(r"^\s*\d+\.\s+(.*)$", line)
        if m:
            if not in_list:
                out.append("<ol>"); in_list = True
            out.append(f"<li>{inline(m.group(1))}</li>")
            i += 1
            continue
        flush_list()

        # Blockquote
        m = re.match(r"^>\s?(.*)$", line)
        if m:
            out.append(f"<blockquote>{inline(m.group(1))}</blockquote>")
            i += 1
            continue

        # Empty line
        if not line.strip():
            i += 1
            continue

        # Paragraph
        out.append(f"<p>{inline(line)}</p>")
        i += 1

    flush_list(); flush_table()
    if in_code:
        out.append("</code></pre>")

    return "\n".join(out)


NAV_JS = """
// ── menú móvil (idéntico a index.html) ──
(function () {
  var nav = document.getElementById("mainnav");
  if (!nav) return;
  var hamb = nav.querySelector(".hamb");
  hamb.addEventListener("click", function () { nav.classList.toggle("open"); });
  nav.querySelectorAll(".links a").forEach(function (a) { a.addEventListener("click", function () { nav.classList.remove("open"); }); });
})();
"""


def render_file(md_path: Path, html_path: Path, title: str, root: Path):
    md = md_path.read_text(encoding="utf-8")
    body = md_to_html(md)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    # ruta base para la navbar: "../" si el doc vive en un subdirectorio del root
    base = "../" if html_path.parent != root else ""
    nav_frag = Path(__file__).parent / "nav.html"
    nav_html = nav_frag.read_text(encoding="utf-8").replace("{BASE}", base) if nav_frag.exists() else ""
    html = f"""<!DOCTYPE html>
<html lang="es-CL">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · Lota Indómito</title>
<style>{CSS}</style>
</head>
<body>
{nav_html}
<div class="doc-header">
  <h1>{title}</h1>
  <div class="tagline">Lota Indómito · Documento del proyecto</div>
</div>
<main>
{body}
</main>
<footer>
  Generado {now} ·
  <a href="{base}index.html">← volver al inicio</a> ·
  <a href="https://github.com/jenovoas/lotaindomito" target="_blank">repo</a>
</footer>
<script>{NAV_JS}</script>
</body>
</html>
"""
    html_path.write_text(html, encoding="utf-8")
    print(f"  ✓ {md_path.relative_to(md_path.parent.parent)} → {html_path.relative_to(html_path.parent.parent)}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=".", help="Raíz del repo (default: actual)")
    args = p.parse_args()
    root = Path(args.root).resolve()

    targets = [
        ("docs/resumen-ejecutivo.md",   "docs/resumen-ejecutivo.html",   "Resumen ejecutivo"),
        ("docs/propuesta-concepto.md", "docs/propuesta-concepto.html", "Propuesta de concepto"),
        ("docs/estado.md",          "docs/estado.html",          "Estado del proyecto"),
        ("docs/decisiones.md",      "docs/decisiones.html",      "Decisiones"),
        ("docs/procedimientos.md",  "docs/procedimientos.html",  "Procedimientos"),
        ("README.md",               "README.html",               "README"),
        ("_analisis/01_resumen_audios_cliente.md",  "_analisis/01_resumen_audios_cliente.html",  "Síntesis audios del cliente"),
        ("_analisis/02_cotejo_audis_vs_prototipo.md", "_analisis/02_cotejo_audis_vs_prototipo.html", "Cliente vs prototipo"),
        ("_analisis/05_analisis_tecnologias_disponibles.md", "_analisis/05_analisis_tecnologias_disponibles.html", "Análisis de tecnologías"),
        ("_analisis/06_investigacion_motores_rust_juegos_ultra_rapidos.md", "_analisis/06_investigacion_motores_rust_juegos_ultra_rapidos.html", "Investigación juegos ultra rápidos Rust"),
        ("_analisis/07_propuesta_arquitectura_servidor_rust_juego.md", "_analisis/07_propuesta_arquitectura_servidor_rust_juego.html", "Propuesta arquitectura servidor dedicado Rust"),
        ("docs/concepto-juego.md",               "docs/concepto-juego.html",               "Concepto del juego (GDD)"),
    ]

    print(f"Renderizando docs en {root}")
    for src_rel, dst_rel, title in targets:
        src = root / src_rel
        dst = root / dst_rel
        if not src.exists():
            print(f"  ⚠ {src_rel} no existe, skip")
            continue
        render_file(src, dst, title, root)
    print("Listo.")


if __name__ == "__main__":
    main()
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
  --bg: #0f1216; --bg2: #1a1f2a; --border: #2a3140;
  --text: #e6e9ef; --muted: #8a93a3;
}
* { box-sizing: border-box; }
body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
       background: var(--bg); color: var(--text); line-height: 1.55; }
header { padding: 32px 40px; background: linear-gradient(135deg, var(--bg2) 0%, var(--bg) 100%);
         border-bottom: 1px solid var(--border); }
h1 { margin: 0; font-size: 28px; font-weight: 600; color: var(--turquesa); letter-spacing: -0.5px; }
.tagline { margin-top: 6px; color: var(--coral); font-size: 12px; letter-spacing: 1px; text-transform: uppercase; }
main { max-width: 920px; margin: 0 auto; padding: 32px 40px 80px; }
h2 { color: var(--coral); font-size: 18px; margin-top: 32px; padding-bottom: 6px;
     border-bottom: 1px solid var(--border); }
h3 { color: var(--turquesa); font-size: 16px; margin-top: 24px; }
p, li { color: var(--text); }
a { color: var(--cobre); text-decoration: none; border-bottom: 1px dashed var(--cobre); }
a:hover { color: var(--turquesa); border-bottom-color: var(--turquesa); }
code { background: var(--bg2); padding: 2px 6px; border-radius: 3px;
       font-family: "JetBrains Mono", Consolas, monospace; font-size: 0.9em;
       border: 1px solid var(--border); }
pre { background: var(--bg2); padding: 14px; border-radius: 6px;
      border: 1px solid var(--border); overflow-x: auto;
      font-family: "JetBrains Mono", Consolas, monospace; font-size: 13px; }
pre code { background: none; padding: 0; border: none; }
blockquote { border-left: 3px solid var(--cobre); margin-left: 0; padding-left: 16px;
             color: var(--muted); }
table { border-collapse: collapse; width: 100%; margin: 16px 0; }
th, td { padding: 8px 12px; border: 1px solid var(--border); text-align: left; }
th { background: var(--bg2); color: var(--turquesa); font-weight: 600; }
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


def render_file(md_path: Path, html_path: Path, title: str):
    md = md_path.read_text(encoding="utf-8")
    body = md_to_html(md)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    html = f"""<!DOCTYPE html>
<html lang="es-CL">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · Lota Indómito</title>
<style>{CSS}</style>
</head>
<body>
<header>
  <h1>{title}</h1>
  <div class="tagline">Lota Indómito · Documento del proyecto</div>
</header>
<main>
{body}
</main>
<footer>
  Generado {now} ·
  <a href="/lotaindomito/">← volver al piloto</a> ·
  <a href="https://github.com/jenovoas/lotaindomito" target="_blank">repo</a>
</footer>
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
        ("docs/estado.md",          "docs/estado.html",          "Estado del proyecto"),
        ("docs/decisiones.md",      "docs/decisiones.html",      "Decisiones"),
        ("docs/procedimientos.md",  "docs/procedimientos.html",  "Procedimientos"),
        ("README.md",               "README.html",               "README"),
        ("_analisis/01_resumen_audios_cliente.md",  "_analisis/01_resumen_audios_cliente.html",  "Síntesis audios del cliente"),
        ("_analisis/02_cotejo_audis_vs_prototipo.md", "_analisis/02_cotejo_audis_vs_prototipo.html", "Cliente vs prototipo"),
        ("_analisis/04_propuesta_tecnica_stack_osm.md", "_analisis/04_propuesta_tecnica_stack_osm.html", "Propuesta técnica"),
        ("docs/concepto-juego.md",               "docs/concepto-juego.html",               "Concepto del juego (GDD)"),
    ]

    print(f"Renderizando docs en {root}")
    for src_rel, dst_rel, title in targets:
        src = root / src_rel
        dst = root / dst_rel
        if not src.exists():
            print(f"  ⚠ {src_rel} no existe, skip")
            continue
        render_file(src, dst, title)
    print("Listo.")


if __name__ == "__main__":
    main()
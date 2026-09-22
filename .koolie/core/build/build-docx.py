#!/usr/bin/env python3
"""Erzeugt die Word-Fassung des Hauptdokuments.

Schritte:
1. Mermaid-Blöcke aus build/out/hauptdokument.md nach PNG rendern (mmdc, Container-Chromium)
   und im Markdown durch Bildverweise ersetzen (die normative Textbeschreibung bleibt erhalten).
2. pandoc-Konvertierung nach DOCX (markdown ohne raw_html, Inhaltsverzeichnis, deutsche Metadaten).
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "out")
IMG = os.path.join(OUT, "img")
SRC = os.path.join(OUT, "hauptdokument.md")
MD_DOCX = os.path.join(OUT, "hauptdokument.docx.md")
_version_file = os.path.join(ROOT, "VERSION")
_version = open(_version_file, encoding="utf-8").read().strip() if os.path.exists(_version_file) else "0.0.0"
DOCX = os.path.join(OUT, f"Koolie_v{_version}.docx")
PPTR = "/tmp/puppeteer-config.json"

os.makedirs(IMG, exist_ok=True)
if not os.path.exists(PPTR):
    with open(PPTR, "w") as fh:
        fh.write('{"executablePath": "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "args": ["--no-sandbox", "--disable-gpu"]}')

text = open(SRC, encoding="utf-8").read()
blocks = re.findall(r"```mermaid\n(.*?)```", text, re.S)
print(f"Mermaid-Blöcke: {len(blocks)}")

counter = 0
def render(match):
    global counter
    counter += 1
    src_path = os.path.join(IMG, f"diagramm-{counter:02d}.mmd")
    png_path = os.path.join(IMG, f"diagramm-{counter:02d}.png")
    with open(src_path, "w", encoding="utf-8") as fh:
        fh.write(match.group(1))
    r = subprocess.run(["mmdc", "-i", src_path, "-o", png_path, "-q", "-p", PPTR,
                        "-b", "white", "-s", "2"], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FEHLER Diagramm {counter}: {r.stderr[:300]}", file=sys.stderr)
        sys.exit(1)
    return f"![Diagramm {counter} (Mermaid-Quelltext im Referenz-Repository)]({png_path})"

text = re.sub(r"```mermaid\n(.*?)```", render, text, flags=re.S)
with open(MD_DOCX, "w", encoding="utf-8") as fh:
    fh.write(text)
print(f"vorverarbeitet: {MD_DOCX}")

cmd = ["pandoc", MD_DOCX,
       "-f", "markdown-raw_html+pipe_tables",
       "-t", "docx",
       "--toc", "--toc-depth=2",
       "--metadata", "toc-title=Inhaltsverzeichnis",
       "--metadata", "lang=de-DE",
       "--metadata", "title=Framework für den professionellen Einsatz von Devin Desktop",
       "--metadata", "subtitle=Vorgehensmodell und technische Referenzimplementierung – Version 0.1.0",
       "--metadata", "date=2026-09-02",
       "--reference-doc", os.path.join(ROOT, "build", "ref-a4.docx"),
       "--resource-path", OUT,
       "-o", DOCX]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print("pandoc-Fehler:", r.stderr[:2000], file=sys.stderr)
    sys.exit(1)
size = os.path.getsize(DOCX)
print(f"geschrieben: {DOCX} ({size/1024/1024:.1f} MB)")
if r.stderr.strip():
    print("pandoc-Warnungen (Auszug):", r.stderr[:800])

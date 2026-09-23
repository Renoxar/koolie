#!/usr/bin/env python3
"""Erzeugt die Word-Fassung des Hauptdokuments.

Schritte:
1. Mermaid-Bloecke aus build/out/hauptdokument.md nach PNG rendern (mmdc) und im
   Markdown durch Bildverweise ersetzen (die normative Textbeschreibung bleibt erhalten).
2. pandoc-Konvertierung nach DOCX (markdown ohne raw_html, Inhaltsverzeichnis, deutsche
   Metadaten).

🔴 DIE METADATEN WERDEN AUS DEM DOKUMENT GELESEN, NICHT HIER GESCHRIEBEN (D-314).
Bis 0.89.0 standen Titel, Untertitel und Datum als feste Zeichenketten in diesem Skript:
"Framework fuer den professionellen Einsatz von <Clientname>", "Version 0.1.0",
"2026-09-02". Das Dokument selbst heisst seit 0.88.0 anders, steht seit 0.89.0 auf
0.89.0 - und dieses Werkzeug haette den ueberholten Titel samt CLIENTNAMEN in die
Dokumenteigenschaften der Lieferung gestempelt. Pruefung 77 haelt die Versionszeile des
Dokuments, erreicht dieses Werkzeug aber nicht; Pruefung 14 erreichte es bis 0.89.0
ebenfalls nicht (D-313). ➡️ Eine Angabe, die zweimal dasteht, veraltet einmal.

🔴 BROWSER UND ARBEITSVERZEICHNIS SIND NICHT MEHR FEST VERDRAHTET (D-314). Bis 0.89.0
schrieb dieses Skript seine Puppeteer-Konfiguration nach "/tmp/..." und nannte darin
einen Chromium-Pfad einer Container-Umgebung ("/opt/pw-browsers/..."). Auf einem
Windows-Arbeitsplatz existiert beides nicht - das Werkzeug war dort nicht lauffaehig,
und das ist zwei Releases lang niemandem aufgefallen, weil es nie gelaufen ist.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "out")
IMG = os.path.join(OUT, "img")
SRC = os.path.join(OUT, "hauptdokument.md")
MD_DOCX = os.path.join(OUT, "hauptdokument.docx.md")
PPTR = os.path.join(OUT, "puppeteer-config.json")

# --- Vorbedingungen, benannt statt vermutet ---------------------------------------
#
# Ein Werkzeug, das ohne seine Vorbedingung startet, scheitert irgendwo in der Mitte und
# laesst ein halbes Erzeugnis liegen. Die Pruefung steht deshalb VOR dem ersten Schritt
# und nennt beide fehlenden Namen auf einmal - nicht den ersten und dann den zweiten.
fehlend = [name for name in ("mmdc", "pandoc") if shutil.which(name) is None]
if not os.path.exists(SRC):
    sys.exit(f"FEHLER: {SRC} fehlt. Zuerst build/assemble.py fahren - die Word-Fassung "
             f"entsteht aus der Markdown-Fassung und nicht aus den Kapitelquellen.")
if fehlend:
    sys.exit("FEHLER: auf diesem Arbeitsplatz nicht gefunden: " + ", ".join(fehlend)
             + ".\n       pandoc: ueber den Paketverwalter des Arbeitsplatzes"
             + "\n       mmdc:   npm install -g @mermaid-js/mermaid-cli")


def browserpfad() -> str | None:
    """Ein Chromium-artiger Browser fuer den Mermaid-Renderer - oder None.

    Zuerst die ausdrueckliche Angabe der Umgebung, dann die ueblichen Ablageorte. Auf
    einem Windows-Arbeitsplatz ist Edge immer vorhanden; einen eigenen Chromium
    herunterzuladen ist damit unnoetig.
    """
    gesetzt = os.environ.get("PUPPETEER_EXECUTABLE_PATH")
    if gesetzt and os.path.exists(gesetzt):
        return gesetzt
    kandidaten = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome",
    ]
    for pfad in kandidaten:
        if os.path.exists(pfad):
            return pfad
    return None


def kopfangaben(text: str) -> dict:
    """Titel, Untertitel, Dokumentversion und Stand - aus dem Dokument selbst.

    Der Kopf ist build/doc/00-kopf.md, und Pruefung 77 haelt seine Versionszeile gegen
    <CORE_DIR>/VERSION. Wer hier liest, erbt diese Pruefung; wer die Werte abschreibt,
    erbt sie nicht.
    """
    angaben = {}
    m = re.search(r"^#\s+(.+?)\s*$", text, re.M)
    if m:
        angaben["title"] = m.group(1)
    m = re.search(r"^\*\*(.+?)\*\*\s*$", text, re.M)
    if m:
        angaben["subtitle"] = m.group(1)
    m = re.search(r"^\|\s*Dokumentversion\s*\|\s*([0-9]+\.[0-9]+\.[0-9]+)", text, re.M)
    if m:
        angaben["version"] = m.group(1)
    m = re.search(r"^\|\s*Stand\s*\|\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", text, re.M)
    if m:
        angaben["date"] = m.group(1)
    return angaben


text = open(SRC, encoding="utf-8").read()
kopf = kopfangaben(text)
fehlende_angaben = [k for k in ("title", "subtitle", "version", "date") if k not in kopf]
if fehlende_angaben:
    sys.exit("FEHLER: im Dokumentkopf nicht gefunden: " + ", ".join(fehlende_angaben)
             + ".\n       Die Metadaten der Word-Fassung stammen aus dem Dokument. "
               "Fehlt eine Angabe,\n       traegt die Lieferung lieber keine als eine "
               "erfundene (D-314).")

# Alte Bilder wegraeumen: Ein Lauf mit weniger Diagrammen als der vorige liesse sonst
# die ueberzaehligen liegen, und der naechste Lauf faende sie vor.
os.makedirs(IMG, exist_ok=True)
for alt in glob.glob(os.path.join(IMG, "diagramm-*.png")) + \
        glob.glob(os.path.join(IMG, "diagramm-*.mmd")):
    os.remove(alt)

browser = browserpfad()
if browser is None:
    sys.exit("FEHLER: kein Chromium-artiger Browser gefunden. Der Mermaid-Renderer "
             "braucht einen.\n       Pfad ueber PUPPETEER_EXECUTABLE_PATH angeben.")
with open(PPTR, "w", encoding="utf-8") as fh:
    json.dump({"executablePath": browser,
               "args": ["--no-sandbox", "--disable-gpu"]}, fh)

blocks = re.findall(r"```mermaid\n(.*?)```", text, re.S)
print(f"Mermaid-Bloecke: {len(blocks)}")

counter = 0


def render(match):
    global counter
    counter += 1
    src_path = os.path.join(IMG, f"diagramm-{counter:02d}.mmd")
    png_path = os.path.join(IMG, f"diagramm-{counter:02d}.png")
    with open(src_path, "w", encoding="utf-8") as fh:
        fh.write(match.group(1))
    r = subprocess.run([shutil.which("mmdc"), "-i", src_path, "-o", png_path, "-q",
                        "-p", PPTR, "-b", "white", "-s", "2"],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", shell=os.name == "nt")
    if r.returncode != 0:
        print(f"FEHLER Diagramm {counter}: {(r.stderr or '')[:300]}", file=sys.stderr)
        sys.exit(1)
    # 🔴 RELATIV UND MIT SCHRAEGSTRICH, und beides ist gemessen (D-314). Bis 0.89.0 stand
    # hier der ABSOLUTE Pfad. Unter Windows enthaelt der Rueckstriche, und pandoc liest
    # einen Rueckstrich in einem Markdown-Link als MASKIERUNG: aus "...\koolie\.koolie\..."
    # wurde "...koolie.koolie\..." - eine Datei, die es nicht gibt. Am 2026-09-23 hat der
    # erste Lauf dieses Werkzeugs auf einem Windows-Arbeitsplatz ACHT VON ACHT Diagrammen
    # verloren, mit Exit 0 und einer geschriebenen Datei. Der Pfad ist jetzt relativ zu
    # --resource-path, und unten bricht der Lauf ab, wenn pandoc eine Ressource meldet.
    rel_png = os.path.relpath(png_path, OUT).replace(os.sep, "/")
    return (f"![Diagramm {counter} (Mermaid-Quelltext im Referenz-Repository)]"
            f"({rel_png})")


text = re.sub(r"```mermaid\n(.*?)```", render, text, flags=re.S)
with open(MD_DOCX, "w", encoding="utf-8") as fh:
    fh.write(text)
print(f"vorverarbeitet: {MD_DOCX}")

# Das Pack gehoert in den Namen der Lieferung, nicht nur in die Meldung des Baus: Beide
# Packs schreiben nach derselben Markdown-Datei, und ohne diese Marke truege die
# Word-Fassung beider Baeue denselben Namen (D-314). Fehlt die Marke, traegt der Name
# sie nicht - eine erfundene waere schlimmer als keine.
_marke = os.path.join(OUT, "referenzclient.txt")
_client = (open(_marke, encoding="utf-8").read().strip()
           if os.path.exists(_marke) else "")
DOCX = os.path.join(OUT, f"Koolie_v{kopf['version']}"
                         + (f"_{_client}" if _client else "") + ".docx")
cmd = ["pandoc", MD_DOCX,
       "-f", "markdown-raw_html+pipe_tables",
       "-t", "docx",
       "--toc", "--toc-depth=2",
       "--metadata", "toc-title=Inhaltsverzeichnis",
       "--metadata", "lang=de-DE",
       "--metadata", f"title={kopf['title']}",
       "--metadata", f"subtitle={kopf['subtitle']} - Version {kopf['version']}",
       "--metadata", f"date={kopf['date']}",
       "--reference-doc", os.path.join(ROOT, "build", "ref-a4.docx"),
       "--resource-path", OUT,
       "-o", DOCX]
r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                   errors="replace")
if r.returncode != 0:
    print("pandoc-Fehler:", (r.stderr or "")[:2000], file=sys.stderr)
    sys.exit(1)

# 🔴 EINE NICHT GEHOLTE RESSOURCE IST EIN FEHLER, KEINE WARNUNG (D-314). pandoc ersetzt
# ein Bild, das es nicht findet, durch seine Beschreibung und endet mit Exit 0. Am
# 2026-09-23 sind auf diese Weise ACHT VON ACHT Diagrammen aus der Lieferung gefallen,
# und die einzige Spur war eine Warnzeile. Ein Erzeugnis, dem ein zugesagter Bestandteil
# fehlt, gilt hier als nicht erzeugt.
verloren = re.findall(r"Could not fetch resource ([^\r\n:]+)", r.stderr or "")
if verloren:
    print(f"FEHLER: pandoc hat {len(verloren)} Ressource(n) nicht geholt - die "
          f"Word-Fassung traegt sie nicht:", file=sys.stderr)
    for pfad in sorted(set(verloren))[:10]:
        print("        " + pfad, file=sys.stderr)
    os.remove(DOCX)
    sys.exit(1)

diagramme = len(re.findall(r"!\[Diagramm \d+", text))
if diagramme != len(blocks):
    print(f"FEHLER: {len(blocks)} Mermaid-Bloecke, aber {diagramme} Bildverweise im "
          f"vorverarbeiteten Markdown.", file=sys.stderr)
    os.remove(DOCX)
    sys.exit(1)

size = os.path.getsize(DOCX)
print(f"geschrieben: {DOCX} ({size / 1024 / 1024:.1f} MB), "
      f"{diagramme} Diagramme eingebettet")
if (r.stderr or "").strip():
    print("pandoc-Warnungen (Auszug):", r.stderr[:800])

#!/usr/bin/env python3
"""Assembliert das Hauptdokument aus <CORE>/build/doc/*.md und Repository-Artefakten.

Direktiven in den Kapiteldateien:
  {{EMBED:relpfad}}            -> Datei als Markdown-Codeblock (4 Backticks, Sprache markdown)
  {{EMBED:relpfad:lang}}       -> wie oben mit Sprachangabe (json, yaml, python, text)
  {{EMBED-RAW:relpfad:shift}}  -> Datei als gerenderten Inhalt einfuegen, Ueberschriften um <shift> Ebenen
                                  verschoben; YAML-Frontmatter wird als Hinweisblock dargestellt

Zwei Quellen fuer eingebettete Dateien:

  1. Das Repository. Fuer alles, was dort versioniert liegt - Core-Module, Checklisten,
     Prompts, Vorlagen. Der Pfad ist relativ zum Wurzelverzeichnis.

  2. Eine Referenzinstallation. Fuer die Laufzeitschicht, die es im Repository gar nicht
     gibt: Sie entsteht erst bei der Installation und sieht je Client Pack anders aus.
     Enthaelt ein Pfad einen Laufzeit-Platzhalter (<RUNTIME_DIR>, <SKILLS_DIR>,
     <PERMISSIONS_FILE>, ...), wird er gegen das gewaehlte Client Pack aufgeloest und aus
     einer frisch erzeugten Installation in einem temporaeren Verzeichnis gelesen.

Der zweite Weg ist der Grund, weshalb das Dokument aus einem frischen Auscheckstand baut.
Vorher zeigten 28 Einbettungen auf .devin/ und AGENTS.md im Arbeitsverzeichnis - Pfade,
die in der .gitignore stehen. Der Bau gelang nur, wenn zufaellig eine Installation daneben
lag, und er zeigte deren Client, ohne das zu sagen.

Aufruf:
    python3 build/assemble.py                     # Referenzclient: devin-desktop
    python3 build/assemble.py --client claude-code

Ausgabe: <CORE>/build/out/hauptdokument.md
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

# CORE = <CORE_DIR>/ (dieses Skript liegt in CORE/build/). Zwei dirname-Aufrufe
# sind hier richtig und bleiben es: Sie zaehlen den Weg vom Skript zum Kern, und
# der ist unabhaengig davon, wie tief der Kern unter der Projektwurzel liegt.
CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(CORE, "build", "doc")
OUT = os.path.join(CORE, "build", "out")
EMBED_RE = re.compile(r"^\{\{(EMBED|EMBED-RAW):([^:}]+)(?::([^}]+))?\}\}\s*$", re.M)

sys.path.insert(0, CORE)
import clientmap  # noqa: E402  (liegt im Kernverzeichnis)

# REPO = Wurzelverzeichnis des Projekts; EMBED-Pfade sind dazu relativ, weil die
# Wurzel-Anweisungsdatei, die Laufzeitschicht und das Overlay dort liegen.
#
# 0.89.0: Bis dahin stand hier ein DRITTER dirname-Aufruf auf CORE - ein im
# Quelltext gezaehlter Weg zur Projektwurzel und damit die Bauform aus D-299 an
# einer siebten Stelle. Sie hat die Umbenennung nicht ueberlebt: Seit der Kern
# unter `.koolie/core` liegt, lieferte sie `.koolie/` statt der Wurzel, und JEDE
# Einbettung schlug fehl. Das Hauptdokument war damit seit 0.88.0 nicht baubar,
# ohne dass es eine Pruefung gemeldet haette - Pruefung 76 haelt vier Werkzeuge
# gegeneinander, und dieses ist keines davon. Der Nachfolger ist dieselbe
# benannte Ableitung, die die anderen vier verwenden.
REPO = clientmap.projektwurzel(CORE)

REFERENZ_CLIENT = "devin-desktop"


def lade_manifest(client: str) -> dict:
    pfad = os.path.join(CORE, "clients", client, "manifest.json")
    if not os.path.exists(pfad):
        print(f"FEHLER: unbekanntes Client Pack: {client}", file=sys.stderr)
        sys.exit(1)
    with open(pfad, encoding="utf-8") as fh:
        man = json.load(fh)
    # 0.88.0: os.path.basename(CORE) lieferte hier "core" statt ".koolie/core" -
    # der Kern ist seit diesem Release zwei Segmente tief (D-299).
    man.setdefault("runtime_placeholders", {})["<CORE_DIR>"] = clientmap.CORE_REL
    return man


def referenzinstallation(client: str) -> str:
    """Legt eine frische Installation dieses Client Packs in einem temporaeren Verzeichnis an.

    Die Laufzeitschicht ist kein Repository-Inhalt: Sie entsteht bei der Installation, und
    ihre Form haengt vom Client ab. Das Dokument soll sie in der Fassung zeigen, die ein
    Projekt tatsaechlich vorfindet - also wird sie erzeugt, statt sie aus dem
    Arbeitsverzeichnis zu borgen.
    """
    ziel = tempfile.mkdtemp(prefix="koolie-referenz-")
    ergebnis = subprocess.run(
        [sys.executable, os.path.join(CORE, "install.py"), "--root", ziel, "--client", client],
        capture_output=True, text=True)
    if ergebnis.returncode != 0:
        shutil.rmtree(ziel, ignore_errors=True)
        print(f"FEHLER: Referenzinstallation ({client}) fehlgeschlagen:", file=sys.stderr)
        print(ergebnis.stderr, file=sys.stderr)
        sys.exit(1)
    return ziel


def shift_headings(text: str, shift: int) -> str:
    def repl(m):
        return "#" * min(6, len(m.group(1)) + shift) + m.group(2)
    out_lines = []
    in_fence = False
    for line in text.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if not in_fence:
            line = re.sub(r"^(#{1,6})(\s)", repl, line)
        out_lines.append(line)
    return "\n".join(out_lines)


def strip_frontmatter(text: str):
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1].strip()
            return fm, parts[2].lstrip("\n")
    return None, text


def quelle(rel: str, man: dict, installation: str):
    """Aufgeloester Pfad, Basisverzeichnis und Herkunft einer Einbettung.

    Ein Pfad mit Laufzeit-Platzhalter meint die Laufzeitschicht und wird aus der
    Referenzinstallation gelesen; jeder andere Pfad meint das Repository.
    """
    aufgeloest = clientmap.resolve_placeholders(rel, man)
    if aufgeloest != rel:
        return aufgeloest, installation, True
    return rel, REPO, False


def process(text: str, man: dict, installation: str) -> str:
    # Zwei Platzhalter koennen auf dieselbe Datei zeigen - bei einem Client ohne eigene
    # Hook-Datei etwa <HOOKS_FILE> und <PERMISSIONS_FILE>. Sie zweimal im selben Kapitel
    # abzudrucken waere in jedem Fall falsch: Der Leser sucht den Unterschied, den es
    # nicht gibt. Die zweite Stelle bekommt deshalb einen Verweis.
    gesehen: dict[str, str] = {}

    def repl(m):
        kind, roh, arg = m.group(1), m.group(2).strip(), (m.group(3) or "").strip()
        rel, basis, aus_installation = quelle(roh, man, installation)
        if rel in gesehen and gesehen[rel] != roh:
            return (f"> Diese Angabe steht bei diesem Client Pack in derselben Datei wie "
                    f"`{gesehen[rel]}` – siehe `{rel}` weiter oben.\n")
        gesehen[rel] = roh
        path = os.path.join(basis, rel)
        if not os.path.exists(path):
            woher = f"Referenzinstallation {man['client']}" if aus_installation else "Repository"
            print(f"FEHLER: eingebettete Datei fehlt ({woher}): {rel}", file=sys.stderr)
            sys.exit(1)
        content = open(path, encoding="utf-8").read().rstrip("\n")
        # Woher eine Laufzeitdatei stammt, gehoert an die Datei und nicht in eine Fussnote:
        # Bei einem anderen Client Pack sieht sie anders aus.
        herkunft = (f" · aus einer Referenzinstallation des Client Packs `{man['client']}`"
                    if aus_installation else "")
        if kind == "EMBED":
            lang = arg or "markdown"
            if "````" in content:
                print(f"FEHLER: {rel} enthaelt 4 Backticks", file=sys.stderr)
                sys.exit(1)
            return f"**Datei:** `{rel}`{herkunft}\n\n````{lang}\n{content}\n````\n"
        shift = int(arg or "1")
        fm, body = strip_frontmatter(content)
        prefix = f"> **Datei:** `{rel}`{herkunft}"
        if fm:
            fm_compact = "; ".join(l.strip() for l in fm.splitlines() if l.strip())
            prefix += f" · **Frontmatter (Laufzeit):** `{fm_compact}`"
        return prefix + "\n\n" + shift_headings(body, shift) + "\n"
    return EMBED_RE.sub(repl, text)


def main() -> None:
    ap = argparse.ArgumentParser(description="Assembliert das Hauptdokument.")
    ap.add_argument("--client", default=REFERENZ_CLIENT,
                    help=f"Client Pack der Referenzinstallation (Standard: {REFERENZ_CLIENT})")
    args = ap.parse_args()

    man = lade_manifest(args.client)
    installation = referenzinstallation(args.client)
    try:
        os.makedirs(OUT, exist_ok=True)
        parts = []
        for fn in sorted(os.listdir(DOC)):
            if fn.endswith(".md"):
                roh = open(os.path.join(DOC, fn), encoding="utf-8").read().rstrip("\n")
                parts.append(process(roh, man, installation))
        result = "\n\n".join(parts) + "\n"
        out_path = os.path.join(OUT, "hauptdokument.md")
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(result)
    finally:
        shutil.rmtree(installation, ignore_errors=True)
    print(f"Referenzclient: {args.client}")
    print(f"geschrieben: {out_path} ({len(result)} Zeichen, {result.count(chr(10))} Zeilen)")


if __name__ == "__main__":
    main()

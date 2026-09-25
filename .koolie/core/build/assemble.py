#!/usr/bin/env python3
"""Assembliert das Hauptdokument aus <CORE>/build/doc/*.md und Repository-Artefakten.

Direktiven in den Kapiteldateien:
  {{EMBED:relpfad}}            -> Datei als Markdown-Codeblock (4 Backticks, Sprache markdown)
  {{EMBED:relpfad:lang}}       -> wie oben mit Sprachangabe (json, yaml, python, text);
                                  lang "permissions_format" = Ausgabeform der Berechtigungsdatei
                                  aus dem Manifest des Packs (json oder toml, K-127, D-396)
  {{EMBED-RAW:relpfad:shift}}  -> Datei als gerenderten Inhalt einfuegen, Ueberschriften um <shift> Ebenen
                                  verschoben; YAML-Frontmatter wird als Hinweisblock dargestellt
  {{ZAHL:muster[,muster...]}}  -> (im Fliesstext) Zahl der versionierten Kerndateien, die eines der
                                  Muster treffen; "*" = alle, "." = direkt im Kern, "x/" = unter x/,
                                  sonst fnmatch relativ zum Kern; "installiert" = Dateien der
                                  Referenzinstallation (D-377)
  {{VERSION}}, {{CLIENT}}      -> Inhalt von VERSION, Client Pack dieses Baus

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
LOKAL_RE = re.compile(r"^\{\{LOKALE-ERGAENZUNG\}\}[ \t]*$", re.M)
ZAHL_RE = re.compile(r"\{\{(ZAHL:([^}]+)|VERSION|CLIENT)\}\}")

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
            # Die Berechtigungsdatei ist nicht bei jedem Pack JSON; bei openai-codex bettete
            # der Bau bis 1.9.3 eine TOML-Datei als JSON ein (K-127, D-396).
            if lang == "permissions_format":
                lang = clientmap.permissions_format(man)
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
    return EMBED_RE.sub(repl, LOKAL_RE.sub(lambda m: lokale_ergaenzung(man), text))


def kerndateien() -> list:
    """Die versionierten Dateien des Kerns, relativ zum Kern, mit '/'.

    Aus git, wenn der Kern in einem Arbeitsbaum liegt; sonst aus dem Verzeichnis ohne
    Bytecode und ohne build/out/ - dieselbe Unterscheidung wie install.py --target.
    """
    try:
        roh = subprocess.run(["git", "-C", CORE, "ls-files", "-z", "."], capture_output=True,
                             check=True).stdout.decode("utf-8")
        dateien = [p for p in roh.split("\0") if p]
        if dateien:
            return sorted(dateien)
    except (OSError, subprocess.CalledProcessError):
        pass
    dateien = []
    for dirpath, dirnames, filenames in os.walk(CORE):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        rel = os.path.relpath(dirpath, CORE).replace(os.sep, "/")
        if rel == "build/out" or rel.startswith("build/out/"):
            dirnames[:] = []
            continue
        for fn in filenames:
            dateien.append(fn if rel == "." else f"{rel}/{fn}")
    return sorted(dateien)


def zahlen(text: str, dateien: list, man: dict, installation: str) -> str:
    """Setzt {{ZAHL:...}}, {{VERSION}} und {{CLIENT}} ein (D-377).

    🔴 WARUM DAS HIER STEHT UND NICHT IN EINER PRUEFUNG: Kapitel 31 nannte bis 1.8.0 "502
    versionierte Dateien" und "123 Aenderungsantraege", gezaehlt zu 0.89.0 - acht Releases
    alt, bei 559 Dateien. Pruefung 78 haelt EINEN Satz des Dokuments gegen den Bestand und
    zahlt dafuer, dass die Zahl erst am Ende des Releases feststeht (D-315). Eine Zahl, die
    der Bau einsetzt, muss niemand setzen - und was niemand setzen muss, veraltet nicht.
    Ein Muster, das NICHTS trifft, bricht den Bau ab: Es ist fast sicher ein Tippfehler,
    und eine stille Null im Dokument waere eine falsche Zahl mit gutem Gewissen.
    """
    import fnmatch

    def zaehle(muster: str) -> int:
        if muster == "installiert":
            return sum(len(f) for _d, _s, f in os.walk(installation))
        treffer = set()
        for m in (x.strip() for x in muster.split(",")):
            if m == "*":
                t = set(dateien)
            elif m == ".":
                t = {d for d in dateien if "/" not in d}
            elif m.endswith("/"):
                t = {d for d in dateien if d.startswith(m)}
            else:
                t = {d for d in dateien if fnmatch.fnmatchcase(d, m)}
            if not t:
                print(f"FEHLER: {{{{ZAHL:{muster}}}}} - '{m}' trifft keine Kerndatei",
                      file=sys.stderr)
                sys.exit(1)
            treffer |= t
        return len(treffer)

    def repl(m):
        if m.group(1) == "VERSION":
            return open(os.path.join(CORE, "VERSION"), encoding="utf-8").read().strip()
        if m.group(1) == "CLIENT":
            return man["client"]
        return str(zaehle(m.group(2)))
    return ZAHL_RE.sub(repl, text)


def lokale_ergaenzung(man: dict) -> str:
    """Die persoenliche Ergaenzungsdatei - oder die Erklaerung, weshalb es sie nicht gibt.

    🔴 BIS 1.4.1 WAR DAS HAUPTDOKUMENT FUER `openai-codex` NICHT BAUBAR (CR-2026-135).
    Kapitel 16 bettete `<ROOT_INSTRUCTION_LOCAL>.example` fuer jedes Pack ein; dieses Pack
    liefert die Vorlage bewusst NICHT aus, weil die Datei bei ihm die Wurzel-Anweisung
    VERDRAENGT statt sie zu ergaenzen (D-341). Der Bau brach ab - und `1.4.0` hat Schritt
    3 aus RELEASE_PROCESS.md 4.1 fuer das neue Pack nie gefahren.

    Die Weiche ist das Manifestfeld `root_instruction_override`, nicht das Fehlen der
    Datei: Fehlt sie bei einem Pack OHNE dieses Feld, bricht der Bau weiter ab. Eine
    Einbettung, die bei jedem Fehlen still eine Erklaerung einsetzte, waere die Ausnahme,
    die alles ausnimmt.
    """
    if not man.get("root_instruction_override"):
        return ("Ergänzend gehört zur Vorlage die persönliche, nicht versionierte "
                "Ergänzungsdatei – zulässig nur zum Einschränken und für "
                "Arbeitsvorlieben, nie zum Erweitern von Freigaben:\n\n"
                "{{EMBED:<ROOT_INSTRUCTION_LOCAL>.example}}")
    lokal = man["runtime_placeholders"]["<ROOT_INSTRUCTION_LOCAL>"]
    return (f"🔴 **Eine persönliche Ergänzungsdatei gibt es bei diesem Client Pack nicht** "
            f"(`{man['client']}`). Die Datei an ihrer Stelle, `{lokal}`, ergänzt "
            f"`{man['root_instruction_file']}` nicht, sondern **verdrängt** sie vollständig: "
            f"Liegt sie im Projekt, steht die Wurzel-Anweisung des Frameworks in keiner "
            f"Nachricht der Sitzung (D-341, gemessen mit Gegenprobe). Das Pack liefert "
            f"deshalb keine Vorlage aus, der `deny`-Korb stellt die Datei schreibgeschützt, "
            f"der Schutz-Hook führt sie in seinen Mustern, und Prüfung 88 meldet sie, wenn "
            f"sie trotzdem im Projektbaum liegt.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Assembliert das Hauptdokument.")
    ap.add_argument("--client", default=REFERENZ_CLIENT,
                    help=f"Client Pack der Referenzinstallation (Standard: {REFERENZ_CLIENT})")
    args = ap.parse_args()

    man = lade_manifest(args.client)
    # Ein abgebrochener Bau darf kein Erzeugnis des VORIGEN Baus stehen lassen: Sonst
    # setzt build-docx.py daraus eine Word-Fassung zusammen und benennt sie nach dem
    # vorigen Pack - gemessen am 2026-09-24, als der Bau fuer openai-codex abbrach und
    # danach die Fassung fuer devin-desktop ein zweites Mal entstand (CR-2026-135).
    for alt in ("hauptdokument.md", "referenzclient.txt"):
        if os.path.exists(os.path.join(OUT, alt)):
            os.remove(os.path.join(OUT, alt))
    installation = referenzinstallation(args.client)
    try:
        os.makedirs(OUT, exist_ok=True)
        parts = []
        dateien = kerndateien()
        for fn in sorted(os.listdir(DOC)):
            if fn.endswith(".md"):
                roh = open(os.path.join(DOC, fn), encoding="utf-8").read().rstrip("\n")
                # Die Zahlen VOR den Einbettungen: Eine eingebettete Datei, die die
                # Direktive nennt, wird zitiert und nicht ausgerechnet.
                parts.append(process(zahlen(roh, dateien, man, installation), man, installation))
        result = "\n\n".join(parts) + "\n"
        out_path = os.path.join(OUT, "hauptdokument.md")
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(result)
        # 🔴 WELCHES PACK DIESER BAU ABBILDET, MUSS NEBEN DEM ERZEUGNIS STEHEN (D-314).
        # Beide Packs schreiben nach derselben Datei, und die beiden Fassungen sind NICHT
        # gleich - am 2026-09-23 gemessen: 1.956.225 gegen 1.959.896 Zeichen. Ohne diese
        # Marke traegt die Word-Fassung beider Baeue denselben Dateinamen, und welche
        # Lieferung man in der Hand haelt, steht nirgends. Der Dateiname selbst bleibt,
        # wie er ist: Chronik und Entscheidungen nennen ihn, und ein Erzeugnis umzubenennen
        # macht aus richtigen Verweisen tote.
        with open(os.path.join(OUT, "referenzclient.txt"), "w", encoding="utf-8") as fh:
            fh.write(args.client + "\n")
    finally:
        shutil.rmtree(installation, ignore_errors=True)
    print(f"Referenzclient: {args.client}")
    print(f"geschrieben: {out_path} ({len(result)} Zeichen, {result.count(chr(10))} Zeilen)")


if __name__ == "__main__":
    main()

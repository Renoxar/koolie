# -*- coding: utf-8 -*-
"""Fuellt die claude-code-Installation der Messumgebung mit den Overlay-Werten.

Aufruf:  python cc-overlay-fuellen.py <zielverzeichnis>

NEU MIT S5 (Lehre aus 0.65.0): Die Werte werden aus dem QUELL-OVERLAY des
Uebungsrepositoriums ABGELEITET, nicht im Skript gepflegt. Die Vorgaengerfassung
fuehrte eine Handliste, in der `.github/**` stand, obwohl das Uebungs-Overlay seit
0.63.0 `.github/workflows/**` sagt - genau die Drift, die 0.65.0 in den
Laufzeittraegern gefunden hat.

    Marken, Wurzeln und Namenslisten gehoeren abgeleitet, nicht gepflegt.

Zwei Quellen, beide versioniert:

  1. `.koolie/project-overlay/OVERLAY.md`  - die QUELLE. Aus ihren Tabellen (Abschnitt 4
     und 5) kommen die sechs Platzhalterwerte.
  2. `.devin/config.json`          - die BINDENDE Schicht des Uebungsrepositoriums.
     Aus ihr kommen die projekteigenen `Write`-Verbote, die der Kern gar nicht
     erzeugt (Nur-Lese-Pfade, Abhaengigkeitsdateien). Sie werden auf `Edit(...)`
     abgebildet, weil `claude-code` und `devin-desktop` zwei Namensraeume sind.

Jede Ersetzung bricht bei abweichender Trefferzahl ab; geschrieben wird erst am Ende.
"""
import io
import json
import os
import re
import sys

import ablage

sys.stdout.reconfigure(encoding="utf-8")

CC = os.path.abspath(sys.argv[1])
DD = ablage.uebungsrepositorium()           # D-231: gesagt, nicht im Quelltext

OVERLAY = os.path.join(DD, ".koolie/project-overlay", "OVERLAY.md")
DEVIN_CONF = os.path.join(DD, ".devin", "config.json")


# --- 1. Werte aus der QUELLE ableiten ---------------------------------------------
def zellen(zeile):
    if not zeile.startswith("|"):
        return None
    teile = zeile.split("|")
    return [t.strip() for t in teile[1:-1]]


def werte_aus_overlay(text):
    """Platzhaltername -> Liste der Werte, aus jeder Tabellenzeile, die ihn fuehrt.

    Gelesen wird die Zelle RECHTS von der Platzhalterzelle - in Abschnitt 4 heisst
    sie `Wert`, in Abschnitt 5 `Befehl`. Der Zuschnitt haengt an der STELLUNG, nicht
    an der Ueberschrift.
    """
    gefunden = {}
    for zeile in text.replace("\r\n", "\n").split("\n"):
        z = zellen(zeile)
        if not z or len(z) < 3:
            continue
        for i, zelle in enumerate(z[:-1]):
            m = re.fullmatch(r"`(<[A-Z_]+>)`", zelle)
            if not m:
                continue
            name = m.group(1)
            wertzelle = z[i + 1]
            werte = re.findall(r"`([^`]+)`", wertzelle)
            if not werte:
                continue
            if name in gefunden:
                raise SystemExit("ABBRUCH: %s steht in zwei Tabellenzeilen" % name)
            gefunden[name] = werte
    return gefunden


overlay_text = io.open(OVERLAY, encoding="utf-8", newline="").read()
WERTE = werte_aus_overlay(overlay_text)

GEBRAUCHT = ["<EXCLUDED_PATHS>", "<CI_CONFIG_PATHS>", "<QUALITY_GATE_CONFIG_PATHS>",
             "<BUILD_COMMAND>", "<TEST_COMMAND>", "<LINT_COMMAND>"]
fehlt = [n for n in GEBRAUCHT if n not in WERTE]
if fehlt:
    raise SystemExit("ABBRUCH: im Quell-Overlay nicht gefunden: %r" % fehlt)
for name in GEBRAUCHT:
    print("aus OVERLAY.md: %-30s %s" % (name, ", ".join(WERTE[name])))


# --- 2. settings.json -------------------------------------------------------------
def entfalte(liste, marke, werte, huelle):
    """Ersetzt genau einen Eintrag huelle(marke) durch huelle(w) je Wert."""
    ziel = huelle % marke
    if liste.count(ziel) != 1:
        raise SystemExit("ABBRUCH: %r steht %dx statt 1x" % (ziel, liste.count(ziel)))
    i = liste.index(ziel)
    return liste[:i] + [huelle % w for w in werte] + liste[i + 1:]


pfad = os.path.join(CC, ".claude", "settings.json")
d = json.loads(io.open(pfad, encoding="utf-8", newline="").read())
p = d["permissions"]

p["deny"] = entfalte(p["deny"], "<EXCLUDED_PATHS>", WERTE["<EXCLUDED_PATHS>"], "Read(%s)")
p["deny"] = entfalte(p["deny"], "<EXCLUDED_PATHS>", WERTE["<EXCLUDED_PATHS>"], "Edit(%s)")
p["deny"] = entfalte(p["deny"], "<CI_CONFIG_PATHS>", WERTE["<CI_CONFIG_PATHS>"], "Edit(%s)")
p["deny"] = entfalte(p["deny"], "<QUALITY_GATE_CONFIG_PATHS>",
                     WERTE["<QUALITY_GATE_CONFIG_PATHS>"], "Edit(%s)")
p["ask"] = entfalte(p["ask"], "<BUILD_COMMAND>", WERTE["<BUILD_COMMAND>"], "Bash(%s)")
p["ask"] = entfalte(p["ask"], "<TEST_COMMAND>", WERTE["<TEST_COMMAND>"], "Bash(%s)")
p["ask"] = entfalte(p["ask"], "<LINT_COMMAND>", WERTE["<LINT_COMMAND>"], "Bash(%s)")

# --- 3. Die projekteigenen Schreibverbote aus der BINDENDEN Schicht ----------------
# Gebraucht werden die Schreibverbote, die das PROJEKT eingetragen hat - die
# Nur-Lese-Pfade und die Abhaengigkeitsdateien. Die uebrigen Eintraege der
# devin-Berechtigungsdatei erzeugt der Kern selbst, und zwar unter den STRUKTURNAMEN
# des jeweiligen Packs (`AGENTS.md` gegen `CLAUDE.md`, `.devin/**` gegen `.claude/**`).
# Wer sie mitnimmt, traegt fremde Pfade in eine Berechtigungsdatei.
#
# Die Trennung wird ABGELEITET, nicht gepflegt: Eine frische devin-desktop-Installation
# in einem leeren Verzeichnis liefert genau den vom Kern erzeugten Bestand; was in der
# Projektdatei darueber hinaussteht, gehoert dem Projekt.
import shutil                                                            # noqa: E402
import subprocess                                                        # noqa: E402
import tempfile                                                          # noqa: E402

devin = json.loads(io.open(DEVIN_CONF, encoding="utf-8", newline="").read())
ref = tempfile.mkdtemp(prefix="lw-ref-")
try:
    shutil.copytree(os.path.join(CC, ".koolie/core"), os.path.join(ref, ".koolie/core"))
    r = subprocess.run([sys.executable, os.path.join(ref, ".koolie/core", "install.py"),
                        "--client", "devin-desktop", "--root", ref],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise SystemExit("ABBRUCH: Referenzinstallation scheiterte:\n" + r.stdout[-1500:])
    kern = json.loads(io.open(os.path.join(ref, ".devin", "config.json"),
                              encoding="utf-8", newline="").read())["permissions"]["deny"]
finally:
    shutil.rmtree(ref, ignore_errors=True)

# Die Platzhalter der Referenz mit denselben Werten entfalten, sonst zaehlten
# `Write(<CI_CONFIG_PATHS>)` und sein entfalteter Wert als zwei verschiedene Regeln.
kern_entfaltet = []
for regel in kern:
    m = re.fullmatch(r"(\w+)\((<[A-Z_]+>)\)", regel)
    if m and m.group(2) in WERTE:
        kern_entfaltet += ["%s(%s)" % (m.group(1), w) for w in WERTE[m.group(2)]]
    else:
        kern_entfaltet.append(regel)

eigen = [x for x in devin["permissions"]["deny"]
         if x.startswith("Write(") and x not in kern_entfaltet]
print("Referenzinstallation devin-desktop: %d deny-Regeln vom Kern; "
      "projekteigene Schreibverbote: %d" % (len(kern), len(eigen)))
nachgetragen = []
for x in eigen:
    regel = "Edit(%s)" % re.fullmatch(r"Write\((.*)\)", x).group(1)
    if regel not in p["deny"]:
        p["deny"].append(regel)
        nachgetragen.append(regel)
for r_ in nachgetragen:
    print("   nachgetragen:", r_)

rest = [x for korb in ("deny", "ask", "allow") for x in p[korb] if "<" in x and ">" in x]
if rest:
    raise SystemExit("ABBRUCH: Platzhalter uebrig: %r" % rest)

neu_settings = json.dumps(d, ensure_ascii=False, indent=2) + "\n"

# --- 4. Laufzeitfassung des Overlays ----------------------------------------------
quelle = io.open(os.path.join(DD, ".devin", "rules", "20-project-overlay.md"),
                 encoding="utf-8", newline="").read().replace("\r\n", "\n")
ziel_pfad = os.path.join(CC, ".claude", "rules", "20-project-overlay.md")
vorlage = io.open(ziel_pfad, encoding="utf-8", newline="").read().replace("\r\n", "\n")

# Der Kopf ist clientabhaengig: devin-desktop traegt YAML-Frontmatter, claude-code
# einen Kommentarblock. Der Koerper ist inhaltlich identisch (sagt die Vorlage selbst).
kopf_ende = vorlage.index("# Project Overlay")
kopf = vorlage[:kopf_ende]
koerper = quelle[quelle.index("# Project Overlay"):]
if koerper.count(".devin/") < 1:
    raise SystemExit("ABBRUCH: kein .devin/ im Koerper - Ersetzung wuerde nichts tun")
anzahl = koerper.count(".devin/")
koerper = koerper.replace(".devin/", ".claude/")
anzahl_agents = koerper.count("AGENTS.md")
koerper = koerper.replace("AGENTS.md", "CLAUDE.md")
neu_overlay = kopf + koerper

# --- 5. Waechter: der Wert der Quelle steht in der Laufzeitfassung -----------------
# Genau der Abgleich, den Pruefung 59 im Repositorium fuehrt - hier auf dem Messbaum,
# damit ein Meszaufbau nicht still den alten Wert traegt (Befund 0.65.0).
for wert in WERTE["<EXCLUDED_PATHS>"]:
    if wert not in neu_overlay:
        raise SystemExit("ABBRUCH: %r steht nicht in der Laufzeitfassung" % wert)
print("Waechter: alle %d Werte von <EXCLUDED_PATHS> stehen in der Laufzeitfassung"
      % len(WERTE["<EXCLUDED_PATHS>"]))

# --- 6. schreiben -----------------------------------------------------------------
daten_s = neu_settings.encode("utf-8")
daten_o = neu_overlay.encode("utf-8")
io.open(pfad, "wb").write(daten_s)
io.open(ziel_pfad, "wb").write(daten_o)
print("settings.json: deny=%d ask=%d allow=%d" % (len(p["deny"]), len(p["ask"]), len(p["allow"])))
print("20-project-overlay.md: %d x .devin/ -> .claude/, %d x AGENTS.md -> CLAUDE.md"
      % (anzahl, anzahl_agents))
print("OK")

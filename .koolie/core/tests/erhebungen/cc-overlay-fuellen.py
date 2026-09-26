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
             "<BUILD_COMMAND>", "<TEST_COMMAND>", "<LINT_COMMAND>",
             # K-154 (D-407): Seit 1.5.0 fuehrt der Kern den Schlitz `write <READ_ONLY_PATHS>`,
             # in dieser Berechtigungsdatei `Edit(<READ_ONLY_PATHS>)`. Bis 1.11.0 entfaltete
             # das Skript ihn nicht und brach mit "Platzhalter uebrig" ab.
             "<READ_ONLY_PATHS>"]
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
_roh_settings = io.open(pfad, encoding="utf-8", newline="").read()
CRLF_SETTINGS = "\r\n" in _roh_settings
d = json.loads(_roh_settings)
p = d["permissions"]

p["deny"] = entfalte(p["deny"], "<EXCLUDED_PATHS>", WERTE["<EXCLUDED_PATHS>"], "Read(%s)")
p["deny"] = entfalte(p["deny"], "<EXCLUDED_PATHS>", WERTE["<EXCLUDED_PATHS>"], "Edit(%s)")
p["deny"] = entfalte(p["deny"], "<CI_CONFIG_PATHS>", WERTE["<CI_CONFIG_PATHS>"], "Edit(%s)")
p["deny"] = entfalte(p["deny"], "<QUALITY_GATE_CONFIG_PATHS>",
                     WERTE["<QUALITY_GATE_CONFIG_PATHS>"], "Edit(%s)")
p["deny"] = entfalte(p["deny"], "<READ_ONLY_PATHS>", WERTE["<READ_ONLY_PATHS>"], "Edit(%s)")
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
_roh_vorlage = io.open(ziel_pfad, encoding="utf-8", newline="").read()
CRLF_OVERLAY = "\r\n" in _roh_vorlage
vorlage = _roh_vorlage.replace("\r\n", "\n")

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

# --- 6. Die Overlay-Regelerweiterungen (Ebene 5) und ihr Verweis im Manifest --------
# K-154 (D-407): Der Packwechsel laesst die Regelerweiterungen des Projekts zurueck
# (`K-44`) - im Uebungsrepositorium `21-overlay-coding-guidelines.md` unter `.devin/rules/`.
# Das Overlay-Manifest des Messbaums verwies danach mit `DOC-001` auf einen Pfad des Packs
# `devin-desktop`, und der Validator meldete im Nachlauf von 1.11.0 in jedem Baum einen
# Fehler, der nicht dem Lauf gehoerte. Die Erweiterung wird deshalb mit der Abbildung des
# Kerns (`render_rule`) in die Form dieses Packs gebracht, und der Verweis zieht mit.
import importlib.util                                                    # noqa: E402

sys.path.insert(0, os.path.join(CC, ".koolie", "core"))
_spec = importlib.util.spec_from_file_location(
    "_install_cc", os.path.join(CC, ".koolie", "core", "install.py"))
_install = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_install)
_man_cc = json.loads(io.open(os.path.join(CC, ".koolie", "core", "clients", "claude-code",
                                          "manifest.json"), encoding="utf-8").read())
erweiterungen = {}
_dd_regeln = os.path.join(DD, ".devin", "rules")
for name in sorted(os.listdir(_dd_regeln)):
    if not re.fullmatch(r"2[1-9]-overlay-[A-Za-z0-9_-]+\.md", name):
        continue
    roh = io.open(os.path.join(_dd_regeln, name), encoding="utf-8", newline="").read()
    crlf = "\r\n" in roh
    neu = _install.render_rule(roh.replace("\r\n", "\n"), _man_cc)
    if crlf:
        neu = neu.replace("\n", "\r\n")
    erweiterungen[name] = neu

man_pfad = os.path.join(CC, ".koolie", "project-overlay", "overlay-manifest.yaml")
neu_man = io.open(man_pfad, encoding="utf-8", newline="").read()
for name in erweiterungen:
    alt = ".devin/rules/" + name
    if neu_man.count(alt) > 1:
        raise SystemExit("ABBRUCH: %r steht %dx im Overlay-Manifest" % (alt, neu_man.count(alt)))
    neu_man = neu_man.replace(alt, ".claude/rules/" + name)
# Gewacht wird ueber die VERWEISFELDER, nicht ueber jede Nennung: Die `notes` des
# Uebungs-Manifests nennen `.devin/rules/20-project-overlay.md` als Prosa, und ein
# Waechter ueber den ganzen Text brach beim ersten Probelauf daran ab.
rest_man = re.findall(r"rule_file:\s*[\"']?(\.devin/[^\s\"']+)", neu_man)
if rest_man:
    raise SystemExit("ABBRUCH: Overlay-Manifest verweist weiter auf das Pack devin-desktop: %r"
                     % rest_man)

# --- 7. schreiben -----------------------------------------------------------------
# Die Zeilenenden der ueberschriebenen Dateien bleiben erhalten (K-154).
if CRLF_SETTINGS:
    neu_settings = neu_settings.replace("\n", "\r\n")
if CRLF_OVERLAY:
    neu_overlay = neu_overlay.replace("\n", "\r\n")
daten_s = neu_settings.encode("utf-8")
daten_o = neu_overlay.encode("utf-8")
daten_m = neu_man.encode("utf-8")
daten_e = {name: text.encode("utf-8") for name, text in erweiterungen.items()}
io.open(pfad, "wb").write(daten_s)
io.open(ziel_pfad, "wb").write(daten_o)
io.open(man_pfad, "wb").write(daten_m)
for name, daten in daten_e.items():
    io.open(os.path.join(CC, ".claude", "rules", name), "wb").write(daten)
    print("Regelerweiterung uebertragen:", name)
print("Zeilenenden erhalten: settings.json %s, 20-project-overlay.md %s"
      % ("CRLF" if CRLF_SETTINGS else "LF", "CRLF" if CRLF_OVERLAY else "LF"))
print("settings.json: deny=%d ask=%d allow=%d" % (len(p["deny"]), len(p["ask"]), len(p["allow"])))
print("20-project-overlay.md: %d x .devin/ -> .claude/, %d x AGENTS.md -> CLAUDE.md"
      % (anzahl, anzahl_agents))
print("OK")

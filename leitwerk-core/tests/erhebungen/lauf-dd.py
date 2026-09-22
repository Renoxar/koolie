# -*- coding: utf-8 -*-
"""Faehrt EINEN Sitzungslauf mit dem Client Pack `devin-desktop` und sichert die
Belegquellen DIESES Clients.

Aufruf:
    python lauf-dd.py <kennung> <arbeitsverzeichnis> <promptdatei>
                      [--modell <name>] [--korbmodus <auto|accept-edits|smart|dangerous>]

🔴 WARUM ES DIESES WERKZEUG GIBT (D-276). `lauf.py` fuehrt einen Lauf mit `claude -p` und
stuetzt seine Auswertung auf drei Belegquellen, die es bei diesem Client NICHT gibt: kein
`--output-format json`, kein `permission_denials`, kein Sitzungstranskript mit
`toolDenialKind`. Gefunden am 2026-09-22 im Vorbedingungsdurchgang des `AP2`-Restes - der
Apparat lag seit `0.79.0` im Kern und kannte genau einen der beiden Clients.

Gesichert werden:
    <kennung>-mitschrift.json   die Mitschrift (`--export`, ATIF-v1.7) - der eigentliche
                                Messwert. Sie fuehrt `agent.tool_definitions` (den
                                Werkzeugbestand), je Schritt `tool_calls` mit Argument und
                                `observation.results` mit dem Ergebnis je Aufruf
    <kennung>-stdout.txt        die Standardausgabe
    <kennung>-stderr.txt        die Standardfehlerausgabe - SIE IST NICHT NEBENSACHE:
                                die Abweisung des `ask`-Korbs steht nur dort (D-280)
    <kennung>-antwort.md        der reine Antworttext
    <kennung>-lauf.json         Befehlszeile, Exitcode, Wanduhr, Modell, Betriebsmodus

🔴 DREI DINGE, DIE DIESER CLIENT ANDERS MACHT (alle am 2026-09-22 gemessen):

1.  ER RUFT PARALLEL AUF, UND DIE ERSTE ABWEISUNG STORNIERT DIE UEBRIGEN (D-286). Eine
    Sonde legt deshalb GENAU EINEN Gegenstand in einen Lauf. Wer acht Versuche in einen
    Prompt legt, misst den ersten und liest sieben Stornierungen als Abweisungen.
2.  DIE MITSCHRIFT FUEHRT EINEN UNTERAGENTEN NICHT (D-282). `run_subagent` steht darin,
    seine Werkzeugaufrufe nicht. Wer einen Unteragenten misst, baut einen Meszbaum mit
    einem aufzeichnenden `PreToolUse`-Hook und einer Positivkontrolle.
3.  DER BETRIEBSMODUS ENTSCHEIDET MIT (D-280, D-281). `auto` weist jeden nicht nur
    lesenden Aufruf ab - auch ohne jede Regel -, `dangerous` hebt den `deny`-Korb auf.
    Der Modus gehoert deshalb in die Aufzeichnung jedes Laufs und in jede Aussage
    darueber, was gemessen wurde.

Die Agent-CLI wird GESAGT, nicht abgeleitet (`LW_DEVIN`) - dieselbe Form wie `LW_ERHEBUNG`
nach D-224 und `LW_UEBUNG` nach D-231. Ein Standardwert im Quelltext waere ein
Arbeitsplatz, und Pruefung 71 meldete ihn.
"""
import io
import json
import os
import subprocess
import sys
import time

import ablage

sys.stdout.reconfigure(encoding="utf-8")

UMGEBUNG_CLI = "LW_DEVIN"

CLI = os.environ.get(UMGEBUNG_CLI)
if not CLI or not os.path.isfile(CLI):
    raise SystemExit(
        "ABBRUCH: %s zeigt nicht auf die Agent-CLI dieses Clients.\n"
        "  Gesetzt: %r\n"
        "  Erwartet: der Pfad auf devin.exe. Sie liegt NICHT im PATH einer Shell,\n"
        "  die vor der Installation des Clients gestartet wurde." % (UMGEBUNG_CLI, CLI))

argv = sys.argv[1:]
modell = "swe-1-6-slow"
if "--modell" in argv:
    i = argv.index("--modell")
    modell = argv[i + 1]
    argv = argv[:i] + argv[i + 2:]
korbmodus = None
if "--korbmodus" in argv:
    i = argv.index("--korbmodus")
    korbmodus = argv[i + 1]
    argv = argv[:i] + argv[i + 2:]
if len(argv) != 3:
    raise SystemExit(__doc__)
kennung, cwd, promptdatei = argv[0], argv[1], argv[2]

BELEGE = ablage.belege()

prompt = io.open(promptdatei, encoding="utf-8").read().strip()
mitschrift = os.path.join(BELEGE, "%s-mitschrift.json" % kennung)
if os.path.exists(mitschrift):
    os.remove(mitschrift)

# `--respect-workspace-trust false` ist Pflicht: Der Print-Modus kann den Vertrauensdialog
# nicht zeigen und bricht sonst in einem nicht vertrauten Verzeichnis ab. Ein
# Vertrauenseintrag je Meszbaum waere die Alternative - und eine Altlast je Meszbaum.
befehl = [CLI, "-p", "--respect-workspace-trust", "false",
          "--model", modell, "--export", mitschrift]
if korbmodus:
    befehl += ["--permission-mode", korbmodus]
befehl += ["--", prompt]

print("=== LAUF %s ===" % kennung)
print("Verzeichnis:", cwd)
print("Modell:", modell, "| Betriebsmodus:", korbmodus or "(Voreinstellung: auto)")
print("Prompt (%d Zeichen):" % len(prompt))
print(prompt)
print("---")

umg = dict(os.environ)
umg["PYTHONIOENCODING"] = "utf-8"
umg["MSYS_NO_PATHCONV"] = "1"

t0 = time.time()
with io.open(os.devnull) as leer:
    r = subprocess.run(befehl, cwd=cwd, stdin=leer, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", env=umg)
dauer = time.time() - t0

io.open(os.path.join(BELEGE, "%s-stdout.txt" % kennung), "w",
        encoding="utf-8", newline="\n").write(r.stdout or "")
io.open(os.path.join(BELEGE, "%s-antwort.md" % kennung), "w",
        encoding="utf-8", newline="\n").write((r.stdout or "").strip() + "\n")
if r.stderr:
    io.open(os.path.join(BELEGE, "%s-stderr.txt" % kennung), "w",
            encoding="utf-8", newline="\n").write(r.stderr)

io.open(os.path.join(BELEGE, "%s-lauf.json" % kennung), "w",
        encoding="utf-8", newline="\n").write(json.dumps({
            "kennung": kennung,
            "verzeichnis": cwd,
            "modell": modell,
            "korbmodus": korbmodus or "(Voreinstellung: auto)",
            "befehl": befehl,
            "exitcode": r.returncode,
            "sekunden": round(dauer, 1),
            "stdout_zeichen": len(r.stdout or ""),
            "mitschrift_vorhanden": os.path.exists(mitschrift),
        }, ensure_ascii=False, indent=2) + "\n")

print("--- Exit %s, %.1f s, stdout %d Zeichen, Mitschrift: %s"
      % (r.returncode, dauer, len(r.stdout or ""), os.path.exists(mitschrift)))

# 🔴 Ein Lauf ohne Mitschrift ist KEIN Lauf, sondern ein Fehlversuch - und er sieht aus wie
# einer mit leerer Antwort. Der Print-Modus endet in zwei Faellen ohne Ausgabe: wenn der
# `ask`-Korb greift (Exit 0, Grund auf stderr) und wenn die Sitzung gar nicht zustande kam
# (Exit != 0). Die Unterscheidung steht in der Aufzeichnung, nicht im Auge.
if not os.path.exists(mitschrift):
    print("🔴 WARNUNG: KEINE MITSCHRIFT. Dieser Lauf ist kein Messwert.")
if r.stderr:
    print("--- stderr (Abweisungen des Betriebsmodus stehen NUR hier) ---")
    print(r.stderr[:3000])
print("--- ANTWORT ---")
print((r.stdout or "(keine Ausgabe)")[:4000])

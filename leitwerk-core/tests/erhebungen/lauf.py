# -*- coding: utf-8 -*-
"""Faehrt EINEN Sitzungslauf mit dem Client Pack `claude-code` und sichert alle
drei Belegquellen.

Aufruf:  python lauf.py <kennung> <arbeitsverzeichnis> <promptdatei> [--resume <sid>]

Gesichert werden:
  <kennung>-ergebnis.json     das JSON-Ergebnis (mit permission_denials)
  <kennung>-transkript.jsonl  die Sitzungsmitschrift (mit toolDenialKind)
  <kennung>-antwort.md        der reine Antworttext

Die Mitschrift wird SOFORT nach dem Lauf weggesichert (Regel: die Aufzeichnung nach
jedem Lauf getrennt sichern).

NEU MIT S5: --resume. `FW-PO-02` hat einen menschlichen Halte-Punkt in der Mitte und
braucht einen zweiten Turn (D-144). Die session_id des ersten Turns steht in seinem
Ergebnis-JSON.
"""
import io
import json
import os
import shutil
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")

argv = sys.argv[1:]
resume = None
if "--resume" in argv:
    i = argv.index("--resume")
    resume = argv[i + 1]
    argv = argv[:i] + argv[i + 2:]
kennung, cwd, promptdatei = argv[0], argv[1], argv[2]

ZIEL = os.path.dirname(os.path.abspath(__file__))
BELEGE = os.path.join(ZIEL, "belege")
os.makedirs(BELEGE, exist_ok=True)

prompt = io.open(promptdatei, encoding="utf-8").read().strip()

umg = dict(os.environ)
umg["MSYS_NO_PATHCONV"] = "1"
umg["PYTHONIOENCODING"] = "utf-8"

print("=== LAUF %s ===" % kennung)
print("Verzeichnis:", cwd)
if resume:
    print("Fortsetzung von Sitzung:", resume)
print("Prompt (%d Zeichen):" % len(prompt))
print(prompt)
print("---")

befehl = ["claude", "-p", prompt, "--output-format", "json"]
if resume:
    befehl += ["--resume", resume]

t0 = time.time()
with io.open(os.devnull) as leer:
    p = subprocess.run(befehl, cwd=cwd, stdin=leer, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=umg)
dauer = time.time() - t0

roh = p.stdout or ""
io.open(os.path.join(BELEGE, kennung + "-stdout.txt"), "w", encoding="utf-8").write(roh)
if p.stderr:
    io.open(os.path.join(BELEGE, kennung + "-stderr.txt"), "w", encoding="utf-8").write(p.stderr)

print("Exit:", p.returncode, "| Dauer: %.1f s" % dauer, "| stdout: %d Zeichen" % len(roh))

if "{" not in roh:
    print("KEIN JSON in stdout. stderr:", (p.stderr or "")[:600])
    raise SystemExit(1)

erg = json.loads(roh[roh.index("{"):])
io.open(os.path.join(BELEGE, kennung + "-ergebnis.json"), "w", encoding="utf-8").write(
    json.dumps(erg, ensure_ascii=False, indent=1))

antwort = erg.get("result", "")
io.open(os.path.join(BELEGE, kennung + "-antwort.md"), "w", encoding="utf-8").write(antwort)

sid = erg.get("session_id", "")
print("session_id:", sid)
print("is_error:", erg.get("is_error"), "| num_turns:", erg.get("num_turns"),
      "| Kosten:", erg.get("total_cost_usd"))
pd = erg.get("permission_denials", [])
print("permission_denials:", len(pd))
for d in pd:
    print("   ", d.get("tool_name"), "|", json.dumps(d.get("tool_input", {}), ensure_ascii=False)[:200])

# --- Mitschrift sofort wegsichern -------------------------------------------------
mangled = os.path.abspath(cwd).replace("\\", "-").replace("/", "-").replace(":", "")
basis = os.path.join(os.path.expanduser("~"), ".claude", "projects")
gefunden = None
for name in os.listdir(basis):
    if name.lstrip("-").lower() == mangled.lstrip("-").lower():
        kandidat = os.path.join(basis, name, sid + ".jsonl")
        if os.path.isfile(kandidat):
            gefunden = kandidat
            break
if gefunden is None:
    for wurzel, _, dateien in os.walk(basis):
        if sid + ".jsonl" in dateien:
            gefunden = os.path.join(wurzel, sid + ".jsonl")
            break
if gefunden:
    shutil.copy2(gefunden, os.path.join(BELEGE, kennung + "-transkript.jsonl"))
    print("Transkript gesichert:", gefunden)
else:
    print("WARNUNG: Transkript zu session_id %s nicht gefunden (gesucht unter %s)" % (sid, basis))

print("--- ANTWORT (%d Zeichen) ---" % len(antwort))
print(antwort[:4000])

#!/usr/bin/env python3
"""
Framework-Hook: SessionStart - Overlay-Status als Zusatzkontext melden.

Status: entwurf. Hook-Mechanismus [DOK]; Ausgabeschema "hookSpecificOutput.additionalContext"
laut Dokumentation [DOK], Details <VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>.

Aufruf:

    hook-overlay-status.py <projektverzeichnis> <regelablage>

Beide Werte kommen aus der Semantikabbildung des Client Packs: das Projektverzeichnis aus
hook_project_dir_var, die Regelablage aus runtime_placeholders["<RULES_DIR>"]. Der Kern
nennt weder die eine Variable noch den einen Pfad - er ist werkzeugneutral (D-02, D-30).

Warum als Argumente und nicht ueber die Umgebung: Der Wert steht damit in dem Kommando,
das der Client ohnehin ausfuehrt. Ob ein Client Umgebungsvariablen an den Hook-Prozess
weiterreicht, ist fuer kein Pack belegt - dieselbe Begruendung, aus der D-31 den Schalter
--fail-closed ins Kommando gelegt hat.

Ohne Argumente bleibt ein Notweg: das Arbeitsverzeichnis und ausschliesslich
project-overlay/OVERLAY.md. Der Notweg ist nicht der vorgesehene Pfad. Ob das
Arbeitsverzeichnis beim Sitzungsstart das Projektverzeichnis ist, ist unbelegt, und ohne
Regelablage entfaellt der zweite Kandidat - die gerenderte Overlay-Regeldatei traegt den
Status ebenso wie das Overlay selbst.

Das Skript blockiert nie; es informiert.
"""
import json
import os
import re
import sys

argumente = [a for a in sys.argv[1:] if not a.startswith("-")]
root = argumente[0] if argumente else os.getcwd()
regelablage = argumente[1] if len(argumente) > 1 else None

candidates = []
if regelablage:
    candidates.append(os.path.join(root, *regelablage.replace("\\", "/").split("/"),
                                   "20-project-overlay.md"))
candidates.append(os.path.join(root, "project-overlay", "OVERLAY.md"))

status = "unbekannt"
for path in candidates:
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        continue
    m = re.search(r"Overlay-Status:\s*`?([^`\n]+)`?", text)
    if m:
        value = m.group(1).strip().lower()
        if value.startswith("aktiv"):
            status = "aktiv"
        elif value.startswith("inaktiv"):
            status = "inaktiv"
        else:
            status = "unbekannt (Platzhalter nicht ausgefuellt)"
        break

version = "unbekannt"
try:
    with open(os.path.join(root, "leitwerk-core", "VERSION"), encoding="utf-8") as fh:
        version = fh.read().strip()
except OSError:
    pass

context = (
    f"Framework-Statusmeldung: Framework-Version {version}; Project-Overlay-Status: {status}. "
    + ("" if status == "aktiv" else
       "Da das Overlay nicht aktiv ist, arbeite ausschliesslich im Modus M1 Read-only Analysis "
       "und weise die Nutzerin oder den Nutzer darauf hin (Wurzel-Anweisungsdatei, "
       "Abschnitt 3).")
)

print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                         "additionalContext": context}}, ensure_ascii=False))
sys.exit(0)

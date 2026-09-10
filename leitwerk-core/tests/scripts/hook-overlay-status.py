#!/usr/bin/env python3
"""
Framework-Hook: SessionStart – Overlay-Status als Zusatzkontext melden.

Status: entwurf. Hook-Mechanismus [DOK]; Ausgabeschema "hookSpecificOutput.additionalContext"
laut Dokumentation [DOK], Details <VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>.

Liest project-overlay/OVERLAY.md und .devin/rules/20-project-overlay.md, ermittelt den
Overlay-Status (aktiv | inaktiv | unbekannt) und meldet ihn als Zusatzkontext. Bei Status
inaktiv oder unbekannt soll der KI-Client laut Wurzel-Anweisungsdatei Abschnitt 3 nur
lesend arbeiten.
Das Skript blockiert nie; es informiert.
"""
import json
import os
import re
import sys

root = os.environ.get("DEVIN_PROJECT_DIR", os.getcwd())
candidates = [
    os.path.join(root, ".devin", "rules", "20-project-overlay.md"),
    os.path.join(root, "project-overlay", "OVERLAY.md"),
]

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
       "und weise die Nutzerin oder den Nutzer darauf hin (AGENTS.md Abschnitt 3).")
)

print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                         "additionalContext": context}}, ensure_ascii=False))
sys.exit(0)

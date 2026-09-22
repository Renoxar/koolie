# -*- coding: utf-8 -*-
# Abgeleitet aus der Erhebung b4 mit 0.83.0 (CR-2026-116): Dieses
# Skript kennt keine Zelle, nur den Basispfad - es ist die Haelfte des
# Apparats, die den Gegenstand NICHT kennt. Geaendert wurde ausschliesslich
# C:\\lw-b4 -> C:\\lw-b5 und die Nennung der Nachbarwerkzeuge.
"""Setzt oder entfernt die Vertrauenseintraege der Baeume unter C:\\lw-b5.

    python trust-b5.py setzen | entfernen | zaehlen

Hinterher GEZIELT entfernen, nicht die Datei zuruecksichern - und erst nach dem
LETZTEN Lauf. Wer beim Aufraeumen Altlasten findet, loescht sie mit.
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

P = os.path.join(os.path.expanduser("~"), ".claude.json")
BASIS = r"C:\lw-b5"
PRAEFIX = "c:/lw-b5/"

was = sys.argv[1] if len(sys.argv) > 1 else "zaehlen"
vorhanden = sorted(os.listdir(BASIS)) if os.path.isdir(BASIS) else []
meine = ["C:/lw-b5/" + b for b in vorhanden
         if os.path.isdir(os.path.join(BASIS, b))]

d = json.load(io.open(P, encoding="utf-8"))
pr = d.setdefault("projects", {})

if was == "setzen":
    for k in meine:
        pr.setdefault(k, {})["hasTrustDialogAccepted"] = True
        pr[k].setdefault("hasCompletedProjectOnboarding", True)
    print("gesetzt:", len(meine))
elif was == "entfernen":
    fort = 0
    for k in list(pr):
        if k.replace("\\", "/").lower().startswith(PRAEFIX):
            del pr[k]
            fort += 1
    print("entfernt:", fort)
elif was == "zaehlen":
    eigene = [k for k in pr if k.replace("\\", "/").lower().startswith(PRAEFIX)]
    print("Eintraege unter %s: %d von %d Baeumen" % (PRAEFIX, len(eigene), len(meine)))
    fehlend = [k for k in meine if k not in pr]
    if fehlend:
        print("OHNE Eintrag:", ", ".join(os.path.basename(x) for x in fehlend))
    raise SystemExit(0)
else:
    raise SystemExit("setzen | entfernen | zaehlen")

daten = (json.dumps(d, ensure_ascii=False, indent=2)).encode("utf-8")
io.open(P, "wb").write(daten)
print("Projekteintraege jetzt:", len(pr))

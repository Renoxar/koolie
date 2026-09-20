# -*- coding: utf-8 -*-
"""Waechter ueber den GETEILTEN node_modules-Bestand.

    python node-waechter.py vorher
    python node-waechter.py nachher

Alle 36 Baeume tragen dieselbe Verzeichnisverbindung auf
`test-devin-framework/frontend/node_modules`. Das ist der Preis dafuer, dass der
Testbefehl im Messbaum ueberhaupt laeuft - ein Baum aus `git archive HEAD`
traegt kein `node_modules`, und 118 MB je Baum waeren 4 GB.

🔴 Geteilt heisst: Ein Lauf, der dorthin schreibt, veraendert JEDEN Baum und das
Uebungsrepositorium dazu. `frontend/node_modules/**` steht in <EXCLUDED_PATHS>
und im deny-Korb; dieser Waechter belegt, dass die Sperre gehalten hat. Er
zaehlt Dateien und Bytes - ein vollstaendiger Hashlauf ueber 9798 Dateien waere
je Aufnahme teurer als sein Erkenntnisgewinn.

Das Werkzeug schreibt seinen Zwischenstand (`.vite`, `.cache`) unterhalb von
node_modules; solche Pfade werden gesondert ausgewiesen, damit eine erwartbare
Aenderung nicht wie ein Schreibzugriff aussieht.
"""
import io
import json
import os
import sys

import ablage

sys.stdout.reconfigure(encoding="utf-8")

HIER = ablage.erhebung()
QUELLE = (r"C:\Users\reneh\Documents\devpacks\test-devin-framework"
          r"\frontend\node_modules")
ZWISCHENSTAND = (".vite", ".cache", ".tmp")


def aufnehmen():
    dateien, bytes_, zwischen = 0, 0, 0
    for wurzel, dirs, namen in os.walk(QUELLE):
        rel = os.path.relpath(wurzel, QUELLE).replace("\\", "/")
        ist_zwischen = any(t in rel.split("/") for t in ZWISCHENSTAND)
        for name in namen:
            try:
                groesse = os.path.getsize(os.path.join(wurzel, name))
            except OSError:
                continue
            if ist_zwischen:
                zwischen += 1
                continue
            dateien += 1
            bytes_ += groesse
    return {"dateien": dateien, "bytes": bytes_, "zwischenstand": zwischen}


was = sys.argv[1]
ziel = os.path.join(HIER, "node-%s.json" % was)
jetzt = aufnehmen()
io.open(ziel, "wb").write(json.dumps(jetzt, indent=1).encode("utf-8"))
print("%s: %d Dateien, %.1f MB (dazu %d Zwischenstandsdateien)"
      % (was, jetzt["dateien"], jetzt["bytes"] / 1048576.0, jetzt["zwischenstand"]))

vorher_pfad = os.path.join(HIER, "node-vorher.json")
if was == "nachher" and os.path.isfile(vorher_pfad):
    vorher = json.load(io.open(vorher_pfad, encoding="utf-8"))
    gleich = (vorher["dateien"] == jetzt["dateien"]
              and vorher["bytes"] == jetzt["bytes"])
    if gleich:
        print("UNVERAENDERT - kein Lauf hat in den geteilten Bestand geschrieben.")
    else:
        print("VERAENDERT: %d -> %d Dateien, %d -> %d Bytes"
              % (vorher["dateien"], jetzt["dateien"],
                 vorher["bytes"], jetzt["bytes"]))
        print("🔴 Das ist ein Befund: Die Sperre auf frontend/node_modules/** hat "
              "nicht gehalten, und der geteilte Bestand liegt in jedem Baum.")

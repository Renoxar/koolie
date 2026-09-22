# -*- coding: utf-8 -*-
# Abgeleitet aus der Erhebung b4 mit 0.83.0 (CR-2026-116): Dieses
# Skript kennt keine Zelle, nur den Basispfad - es ist die Haelfte des
# Apparats, die den Gegenstand NICHT kennt. Geaendert wurde ausschliesslich
# C:\\lw-b4 -> C:\\lw-b5 und die Nennung der Nachbarwerkzeuge.
"""Nimmt den Zustand der Messbaeume unter C:\\lw-b5 auf und vergleicht zwei Aufnahmen.

    python zustand-b5.py vorher
    python zustand-b5.py nachher

🔴 ANDERS ALS IN BUENDEL 3 UND 4 ist eine Veraenderung hier ein BEFUND, kein
Messwert. `role-re-ticket` ist M1 und traegt `deny` auf `edit` und `exec`; er
liefert einen Textentwurf und schreibt nichts. Die Aufnahme belegt genau das -
und `RE-001-N03` haengt daran. Ein Bericht ist keine Aufzeichnung.

Buendel 5 hat KEINE Verzeichnisverbindung auf `node_modules` (E2 von
CR-2026-116); der Ausschluss unten bleibt trotzdem stehen, weil er nichts
kostet und ein spaeteres Buendel ihn wieder braucht.
"""
import hashlib
import io
import json
import os
import sys

import ablage

sys.stdout.reconfigure(encoding="utf-8")

HIER = ablage.erhebung()
B = r"C:\lw-b5"
TEILE = [os.path.join("frontend", "src"), os.path.join("backend", "src"),
         "api-contracts", "docs", ".claude", "leitwerk-core", ".github",
         "CLAUDE.md", "README.md"]


def aufnehmen():
    d = {}
    for baum in sorted(os.listdir(B)):
        w = os.path.join(B, baum)
        if not os.path.isdir(w) or baum.startswith("basis"):
            continue
        for teil in TEILE:
            wurzel = os.path.join(w, teil)
            if os.path.isfile(wurzel):
                rel = baum + "/" + teil.replace("\\", "/")
                d[rel] = hashlib.sha1(io.open(wurzel, "rb").read()).hexdigest()
                continue
            for pfad, dirs, dateien in os.walk(wurzel):
                dirs[:] = sorted(x for x in dirs
                                 if x not in ("__pycache__", "node_modules"))
                for name in sorted(dateien):
                    voll = os.path.join(pfad, name)
                    rel = baum + "/" + os.path.relpath(voll, w).replace("\\", "/")
                    d[rel] = hashlib.sha1(io.open(voll, "rb").read()).hexdigest()
    return d


was = sys.argv[1]
ziel = os.path.join(HIER, "zustand-%s.json" % was)
jetzt = aufnehmen()
io.open(ziel, "wb").write(json.dumps(jetzt, ensure_ascii=False, indent=1).encode("utf-8"))
baeume = len({k.split("/")[0] for k in jetzt})
print("%s: %d Dateien in %d Baeumen" % (was, len(jetzt), baeume))

vorher_pfad = os.path.join(HIER, "zustand-vorher.json")
if was == "nachher" and os.path.isfile(vorher_pfad):
    vorher = json.load(io.open(vorher_pfad, encoding="utf-8"))
    neu = sorted(set(jetzt) - set(vorher))
    fort = sorted(set(vorher) - set(jetzt))
    anders = sorted(k for k in set(jetzt) & set(vorher) if jetzt[k] != vorher[k])
    print("neu: %d | entfernt: %d | veraendert: %d" % (len(neu), len(fort), len(anders)))
    je_baum = {}
    for k in neu + fort + anders:
        je_baum.setdefault(k.split("/")[0], []).append(k)
    for baum in sorted(je_baum):
        print("  %-12s %d Datei(en)" % (baum, len(je_baum[baum])))
        for k in je_baum[baum]:
            art = "neu" if k in neu else ("entfernt" if k in fort else "geaendert")
            print("      %-10s %s" % (art, k.split("/", 1)[1]))
    unberuehrt = sorted({k.split("/")[0] for k in jetzt} - set(je_baum))
    print("Unberuehrt geblieben (%d): %s" % (len(unberuehrt), ", ".join(unberuehrt)))

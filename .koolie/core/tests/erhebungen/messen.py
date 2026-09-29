# -*- coding: utf-8 -*-
"""Der Einstieg in den Messapparat (CR-2026-160, D-473).

    python messen.py REIHE.json pruefen            nur das Schema der Reihe
    python messen.py REIHE.json aufbau             Sollstaende festhalten, Vertrauen setzen
    python messen.py REIHE.json vorpruefung [K..]  Baeume herrichten und pruefen, nichts fahren
    python messen.py REIHE.json lauf [K..]         fahren, was fehlt - Abbruch bei jedem Befund
    python messen.py REIHE.json auswertung [FELD]  Tabelle je Lauf, Summen je FELD (variante, gruppe)
    python messen.py REIHE.json aufraeumen         Vertrauen entfernen
    python messen.py basis ZIEL CLIENT PRAEP.json  eine frische Installation als Basis bauen
    python messen.py stand-marke PFAD [PFAD..]     Standmarke fuer eine Ergebniszelle (K-61)
    python messen.py selbsttest                    der Apparat gegen die Attrappe, ohne Kontingent

Die Reihe liegt in der Erhebungsablage; ihre Belege entstehen unter belege/NAME daneben.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

from apparat import baum, belege, laeufer, stand  # noqa: E402


def main(argv: list) -> int:
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "selbsttest":
        from apparat import selbsttest
        return selbsttest.main()
    if argv[0] == "stand-marke":
        print(stand.marke(argv[1:]))
        return 0
    if argv[0] == "basis":
        ziel, client, praep = argv[1], argv[2], argv[3]
        schritte = json.loads(io.open(praep, encoding="utf-8").read())
        soll = baum.basis_bauen(ziel, belege.KERN, client, schritte)
        print(json.dumps(soll, indent=1))
        return 0
    reihe = laeufer.laden(argv[0])
    befehl = argv[1] if len(argv) > 1 else "pruefen"
    rest = argv[2:]
    if befehl == "pruefen":
        print(f"Reihe '{reihe.name}': {len(reihe.laeufe)} Laeufe, fahrbar")
    elif befehl == "aufbau":
        for b in laeufer.aufbau(reihe):
            print("Sollstand und Vertrauen:", b)
    elif befehl == "vorpruefung":
        ergebnis = laeufer.vorpruefen(reihe, rest or None)
        schlecht = 0
        for k, befunde in ergebnis.items():
            print(f"{k}: {'in Ordnung' if not befunde else '; '.join(befunde)}")
            schlecht += bool(befunde) and befunde != ["(schon gefahren)"]
        return 1 if schlecht else 0
    elif befehl == "lauf":
        laeufer.fahren(reihe, rest or None)
    elif befehl == "auswertung":
        print(belege.auswerten(reihe, rest[0] if rest else ""))
    elif befehl == "aufraeumen":
        laeufer.aufraeumen(reihe)
        print("Vertrauen entfernt")
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

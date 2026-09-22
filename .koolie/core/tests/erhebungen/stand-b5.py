# -*- coding: utf-8 -*-
# Abgeleitet aus der Erhebung b4 mit 0.83.0 (CR-2026-116): Dieses
# Skript kennt keine Zelle, nur den Basispfad - es ist die Haelfte des
# Apparats, die den Gegenstand NICHT kennt. Geaendert wurde ausschliesslich
# C:\\lw-b4 -> C:\\lw-b5 und die Nennung der Nachbarwerkzeuge.
"""Sagt in einem Befehl, wo der Meßtag steht.

    python stand-b5.py

🔴 EINE ZAHL IN EINER UEBERGABE IST EINE MOMENTAUFNAHME, dieses Skript ist der
Stand. Es leitet ab, was fehlt - aus den Prompts und den Belegen -, statt eine
Liste zu pflegen.

Ein Beleg zaehlt nur, wenn `is_error` false ist (Lehre aus Buendel 2: acht
Laeufe hinterliessen einen VOLLSTAENDIGEN Belegsatz mit `is_error: true` und
0 USD, und die Wiederaufnahme uebersprang genau die, die fehlten).
"""
import io
import json
import os
import sys

import ablage

sys.stdout.reconfigure(encoding="utf-8")

BEL = ablage.belege(anlegen=False)
PROMPTS = ablage.prompts(anlegen=False)
BAEUME = r"C:\lw-b5"


def ergebnis(k):
    p = os.path.join(BEL, k + "-ergebnis.json")
    if not os.path.isfile(p):
        return None
    try:
        return json.load(io.open(p, encoding="utf-8"))
    except ValueError:
        return None


def main():
    # 🔴 DIE SOLLMENGE KOMMT AUS DEN MESSBAEUMEN, NICHT AUS DEM PROMPTVERZEICHNIS
    # (D-230). Bis 0.79.2 stand die Ableitung hier und las das Promptverzeichnis;
    # der Nachlauf hat dort die fuenfzig Prompts des Messtags geerbt und schuldet
    # vierzehn Zellen. Dieses Skript meldete 35 Fehlbestaende und rund 37 USD, wo
    # fuenfzehn und rund achtzehn faellig waren. Die Ableitung steht jetzt EINMAL
    # in `ablage.sollmenge()` und wird von `reihe-b5.py` mitbenutzt - zwei Zaehler
    # desselben Gegenstands zaehlen dasselbe (D-228).
    einfach, zwei, ohne_baum = ablage.sollmenge(PROMPTS, BAEUME)
    soll = ablage.laeufe(einfach, zwei)

    gut, fehlt, fehlerhaft = [], [], []
    usd = sek = 0.0
    for k in soll:
        e = ergebnis(k)
        if e is None:
            fehlt.append(k)
        elif e.get("is_error"):
            fehlerhaft.append(k)
        else:
            gut.append(k)
            usd += e.get("total_cost_usd") or 0
            sek += (e.get("duration_ms") or 0) / 1000.0

    print("=" * 78)
    print("MESSTAG BUENDEL 5 - STAND")
    print("=" * 78)
    # 🔴 Hier stand ein FESTER Text aus Buendel 3: *18 Zellen, davon 7 mit
    # zweitem Turn*. Buendel 5 hat 19 und 6 - und 2*18+2*7 ergibt ebenso 50 wie
    # 2*19+2*6. Die Sollmenge war abgeleitet und richtig, ihre BESCHREIBUNG
    # gepflegt und falsch (D-204 an einer neuen Stelle). Jetzt beides abgeleitet.
    # 🔴 Und der erste Anlauf dieser Ableitung zaehlte LAEUFE und nannte sie
    # ZELLEN: `einfach` und `zwei` fuehren Haupt- und Kontrollauf je Zelle
    # getrennt (38 und 12). Die Zelle bekommt man, indem man das fuehrende `k`
    # des Kontrollaufs abstreift - dieselbe Ableitung, eine Ebene tiefer.
    zellen = {k[1:] if k.startswith("k") else k for k in einfach}
    zellen2 = {k[1:] if k.startswith("k") else k for k in zwei if k in einfach}
    print("Soll:        %3d Laeufe - %d Zellen je Haupt- und Kontrollauf, %d "
          "davon mit zweitem Turn"
          % (len(soll), len(zellen), len(zellen2)))
    print("Gueltig:     %3d   (%.2f USD, %.0f s; Mittel %.2f USD, %.0f s)"
          % (len(gut), usd, sek, usd / max(1, len(gut)), sek / max(1, len(gut))))
    print("Fehlerhaft:  %3d   %s" % (len(fehlerhaft), " ".join(fehlerhaft) or "-"))
    print("Fehlt:       %3d" % len(fehlt))
    if fehlt:
        print()
        print("  " + "\n  ".join(" ".join(fehlt[i:i + 6])
                                 for i in range(0, len(fehlt), 6)))
        rest = len(fehlt) * (usd / max(1, len(gut)))
        zeit = len(fehlt) * (sek / max(1, len(gut)))
        print()
        print("  Erwartet noch: rund %.0f USD und %.0f Minuten (gerechnet mit dem "
              "Mittel dieses Tages)" % (rest, zeit / 60.0))
    if fehlerhaft:
        print()
        print("🔴 Die fehlerhaften Belege werden von `reihe-b5.py` NEU gefahren - "
              "ein Beleg ist erst einer, wenn `is_error` false ist.")

    print()
    vorhanden = sorted(x for x in os.listdir(BAEUME)
                       if os.path.isdir(os.path.join(BAEUME, x))) \
        if os.path.isdir(BAEUME) else []
    print("Baeume unter %s: %d" % (BAEUME, len(vorhanden)))
    if not vorhanden:
        print("🔴 KEINE BAEUME - erst `umgebungen-bauen-b5.py`, dann `baeume-b5.py`.")
        print("   Ohne Baeume ist die Sollmenge LEER und dieser Stand keine Aussage")
        print("   ueber die Vollstaendigkeit der Reihe (D-230).")
    # 🔴 Was NICHT stillschweigend uebergangen wird: Prompts ohne Baum. Sie sind der
    # Zuschnitt einer anderen Erhebung - und genau sie haben `reihe-b5.py` ohne
    # Argumente abbrechen lassen, bevor ein einziger Lauf fuhr (D-230).
    if ohne_baum:
        print()
        print("Nicht im Zuschnitt dieser Erhebung (Prompt vorhanden, kein Messbaum): %d"
              % len(ohne_baum))
        print("  " + "\n  ".join(" ".join(ohne_baum[i:i + 6])
                                 for i in range(0, len(ohne_baum), 6)))
    # 🔴 Buendel 5 hat keine Verzeichnisverbindung, also auch keinen
    # `node_modules`-Waechter (E2 von CR-2026-116). Eine Pflichtdatei, die es
    # nicht gibt, meldet bei jedem Aufruf FEHLT - und eine Meldung, die immer
    # kommt, wird nicht mehr gelesen.
    for pflicht, was in (("zustand-vorher.json", "Zustandsaufnahme VORHER"),):
        da = os.path.isfile(os.path.join(ablage.erhebung(), pflicht))
        print("%-28s %s" % (was + ":", "liegt vor" if da else "🔴 FEHLT"))

    print()
    if fehlt or fehlerhaft:
        print("NAECHSTER BEFEHL:  python reihe-b5.py")
        print("                   (faehrt nur, was fehlt - nichts wird doppelt bezahlt)")
    else:
        print("NAECHSTE BEFEHLE:  python zustand-b5.py nachher")
        print("                   python auswerten-b5.py")
        print("                   python trust-b5.py entfernen")


if __name__ == "__main__":
    main()

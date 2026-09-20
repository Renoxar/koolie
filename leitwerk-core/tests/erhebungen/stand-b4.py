# -*- coding: utf-8 -*-
# Abgeleitet aus der Erhebung b3 mit 0.78.0 (CR-2026-105, D-212): Dieses
# Skript kennt keine Zelle, nur den Basispfad - es ist die Haelfte des
# Apparats, die den Gegenstand kennt. Geaendert wurde ausschliesslich
# C:\\lw-b3 -> C:\\lw-b4.
"""Sagt in einem Befehl, wo der Meßtag steht.

    python stand-b4.py

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

sys.stdout.reconfigure(encoding="utf-8")

S = os.path.dirname(os.path.abspath(__file__))
BEL = os.path.join(S, "belege")
PROMPTS = os.path.join(os.path.dirname(S), "prompts")
BAEUME = r"C:\lw-b4"


def ergebnis(k):
    p = os.path.join(BEL, k + "-ergebnis.json")
    if not os.path.isfile(p):
        return None
    try:
        return json.load(io.open(p, encoding="utf-8"))
    except ValueError:
        return None


def main():
    # Soll-Menge aus den Prompts ableiten: eine Kennung mit `-t2.txt` hat ZWEI
    # Laeufe - `<k>t1` (der Halt) und `<k>` (die Umsetzung).
    einfach, zwei = set(), set()
    for x in sorted(os.listdir(PROMPTS)):
        if not x.endswith(".txt"):
            continue
        n = x[:-4]
        # 🔴 Eine NACHMESSUNG (`n<kennung>`) gehoert nicht zur Sollmenge des Messtags.
        # Sie faehrt einen weiteren Turn im Baum ihrer Zelle und hat keinen eigenen
        # Baum; wer sie mitzaehlt, meldet einen Fehlbestand, den es nicht gibt.
        # Praezedenz: `nsk004p01` und `nsk009p01` aus Buendel 2.
        if n.startswith("n"):
            continue
        if n.endswith("-t2"):
            zwei.add(n[:-3])
        else:
            einfach.add(n)
    soll = []
    for k in sorted(einfach):
        if k in zwei:
            soll += [k + "t1", k]
        else:
            soll.append(k)

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
    print("MESSTAG BUENDEL 4 - STAND")
    print("=" * 78)
    # 🔴 Hier stand ein FESTER Text aus Buendel 3: *18 Zellen, davon 7 mit
    # zweitem Turn*. Buendel 4 hat 19 und 6 - und 2*18+2*7 ergibt ebenso 50 wie
    # 2*19+2*6. Die Sollmenge war abgeleitet und richtig, ihre BESCHREIBUNG
    # gepflegt und falsch (D-204 an einer neuen Stelle). Jetzt beides abgeleitet.
    # 🔴 Und der erste Anlauf dieser Ableitung zaehlte LAEUFE und nannte sie
    # ZELLEN: `einfach` und `zwei` fuehren Haupt- und Kontrollauf je Zelle
    # getrennt (38 und 12). Die Zelle bekommt man, indem man das fuehrende `k`
    # des Kontrollaufs abstreift - dieselbe Ableitung, eine Ebene tiefer.
    zellen = {k[1:] if k.startswith("k") else k for k in einfach}
    zellen2 = {k[1:] if k.startswith("k") else k for k in zwei}
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
        print("🔴 Die fehlerhaften Belege werden von `reihe-b4.py` NEU gefahren - "
              "ein Beleg ist erst einer, wenn `is_error` false ist.")

    print()
    vorhanden = sorted(x for x in os.listdir(BAEUME)
                       if os.path.isdir(os.path.join(BAEUME, x))) \
        if os.path.isdir(BAEUME) else []
    print("Baeume unter %s: %d" % (BAEUME, len(vorhanden)))
    if not vorhanden:
        print("🔴 KEINE BAEUME - erst `umgebungen-bauen-b4.py`, dann `baeume-b4.py`.")
    for pflicht, was in (("zustand-vorher.json", "Zustandsaufnahme VORHER"),
                         ("node-vorher.json", "node_modules-Waechter VORHER")):
        da = os.path.isfile(os.path.join(S, pflicht))
        print("%-28s %s" % (was + ":", "liegt vor" if da else "🔴 FEHLT"))

    print()
    if fehlt or fehlerhaft:
        print("NAECHSTER BEFEHL:  python reihe-b4.py")
        print("                   (faehrt nur, was fehlt - nichts wird doppelt bezahlt)")
    else:
        print("NAECHSTE BEFEHLE:  python zustand-b4.py nachher")
        print("                   python node-waechter.py nachher")
        print("                   python auswerten-b4.py")
        print("                   python trust-b4.py entfernen")


if __name__ == "__main__":
    main()

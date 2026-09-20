# -*- coding: utf-8 -*-
# Abgeleitet aus der Erhebung b3 mit 0.78.0 (CR-2026-105, D-212): Dieses
# Skript kennt keine Zelle, nur den Basispfad - es ist die Haelfte des
# Apparats, die den Gegenstand kennt. Geaendert wurde ausschliesslich
# C:\\lw-b3 -> C:\\lw-b4.
"""Faehrt eine Reihe von Laeufen nacheinander, JE LAUF IM EIGENEN BAUM.

    python reihe-b4.py                      # alle 50
    python reihe-b4.py sk010p01 sk010p02    # ausgewaehlte

Der Baum eines Laufs heisst wie der Lauf: C:\\lw-b4\\<kennung>. Anders als in
Buendel 1 und 2 gibt es keinen gemeinsamen Hauptbaum - alle drei Skills dieses
Buendels schreiben.

🔴 EIN BELEG IST ERST EINER, WENN `is_error` FALSE IST (Lehre aus Buendel 2). Am
2026-09-19 ist das Sitzungskontingent mitten in der Kontrollreihe ausgegangen;
acht Laeufe hinterliessen einen VOLLSTAENDIGEN Belegsatz mit `is_error: true`
und 0 USD, und die Wiederaufnahme uebersprang genau die Laeufe, die fehlten.
Dieses Skript ueberspringt nur Belege, die keinen Fehler tragen.
"""
import io
import json
import os
import subprocess
import sys
import time

import ablage

sys.stdout.reconfigure(encoding="utf-8")

HIER = os.path.dirname(os.path.abspath(__file__))
PROMPTS = ablage.prompts()
BELEGE = ablage.belege()
BASIS = r"C:\lw-b4"
LOG = os.path.join(BELEGE, "reihe-%s.log" % time.strftime("%H%M%S"))



def belegt(kennung):
    """True, wenn ein GUELTIGER Beleg vorliegt - `is_error` false."""
    pfad = os.path.join(BELEGE, kennung + "-ergebnis.json")
    if not os.path.isfile(pfad):
        return False
    try:
        d = json.load(io.open(pfad, encoding="utf-8"))
    except ValueError:
        return False
    if d.get("is_error"):
        print("   (Beleg mit is_error=true - wird neu gefahren: %s)" % kennung)
        return False
    return True


def ergebnis(kennung):
    pfad = os.path.join(BELEGE, kennung + "-ergebnis.json")
    if not os.path.isfile(pfad):
        return {}
    try:
        return json.load(io.open(pfad, encoding="utf-8"))
    except ValueError:
        return {}


def sitzung(kennung):
    """Die session_id eines Laufs - Anker des zweiten Turns (D-144)."""
    d = ergebnis(kennung)
    return "" if d.get("is_error") else (d.get("session_id") or "")


def kosten(kennung):
    try:
        return float(ergebnis(kennung).get("total_cost_usd") or 0)
    except (TypeError, ValueError):
        return 0.0


def main():
    kennungen = sys.argv[1:]
    if not kennungen:
        # 🔴 Ein `-t2`-Prompt ist KEINE eigene Kennung, sondern der zweite Turn
        # seiner Zelle - er hat keinen eigenen Baum und wird unten aus dem
        # Prompt-Verzeichnis geholt. Wer ihn mitzaehlt, bricht an einem Baum ab,
        # den es nie gab. `stand-b4.py` leitet die Sollmenge richtig ab.
        # Eine NACHMESSUNG (`n<kennung>`) faehrt einen weiteren Turn im Baum ihrer
        # Zelle und wird von Hand angestossen - sie hat keinen eigenen Baum.
        namen = sorted(x[:-4] for x in os.listdir(PROMPTS)
                       if x.endswith(".txt") and not x.endswith("-t2.txt")
                       and not x.startswith("n"))
        # Hauptlaeufe zuerst, danach die Kontrollaeufe
        kennungen = [k for k in namen if not k.startswith("k")] + \
                    [k for k in namen if k.startswith("k")]
    protokoll = io.open(LOG, "w", encoding="utf-8")
    summe_kosten, gefahren = 0.0, 0
    for k in kennungen:
        zwei = os.path.isfile(os.path.join(PROMPTS, k + "-t2.txt"))
        # Bei zwei Turns traegt der ERSTE die Kennung `<k>t1` - sein Beleg bleibt
        # getrennt erhalten, denn er traegt den Halt, und der Halt ist bei diesen
        # Zellen die halbe Erwartung.
        schritte = [(k + "t1", k + ".txt", None), (k, k + "-t2.txt", k + "t1")] \
            if zwei else [(k, k + ".txt", None)]
        # 🔴 Eine Zelle ist erst erledigt, wenn JEDER ihrer Turns einen gueltigen
        # Beleg hat. Wer nur den zweiten prueft, ueberspringt eine Zelle, deren
        # erster Turn fehlt - und der erste traegt den Halt.
        if all(belegt(x[0]) for x in schritte):
            print("uebersprungen (gueltiger Beleg liegt vor): %s" % k)
            continue
        baum = os.path.join(BASIS, k)
        if not os.path.isdir(baum):
            raise SystemExit("ABBRUCH: der Baum %s fehlt - erst baeume-b4.py" % baum)
        abbruch = False
        for kennung, promptname, vorgaenger in schritte:
            if belegt(kennung):
                print("uebersprungen (gueltiger Beleg liegt vor): %s" % kennung)
                continue
            prompt = os.path.join(PROMPTS, promptname)
            if not os.path.isfile(prompt):
                raise SystemExit("ABBRUCH: %s fehlt" % prompt)
            befehl = [sys.executable, os.path.join(HIER, "lauf.py"),
                      kennung, baum, prompt]
            if vorgaenger:
                sid = sitzung(vorgaenger)
                if not sid:
                    print("   UEBERSPRUNGEN: %s hat keine session_id - der erste "
                          "Turn ist nicht auswertbar" % vorgaenger)
                    abbruch = True
                    break
                befehl += ["--resume", sid]
            umg = dict(os.environ)
            umg["MSYS_NO_PATHCONV"] = "1"
            umg["PYTHONIOENCODING"] = "utf-8"
            t0 = time.time()
            p = subprocess.run(befehl, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", env=umg)
            dauer = time.time() - t0
            kopf = [z for z in (p.stdout or "").split("\n")
                    if z.startswith(("Exit:", "is_error:", "permission_denials:",
                                     "session_id:"))]
            zeile = "%-11s %6.1f s  %s" % (kennung, dauer, " | ".join(kopf))
            print(zeile)
            protokoll.write(zeile + "\n")
            protokoll.write((p.stdout or "")[-3000:] + "\n" + "=" * 80 + "\n")
            protokoll.flush()
            gefahren += 1
            summe_kosten += kosten(kennung)
            if p.returncode != 0:
                print("   ABBRUCH bei %s (Exit %d)" % (kennung, p.returncode))
                print((p.stdout or "")[-1500:])
                abbruch = True
                break
        if abbruch:
            break
    protokoll.close()
    print("gefahren: %d | Kosten dieser Reihe: %.2f USD" % (gefahren, summe_kosten))
    print("Protokoll:", LOG)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Legt je Zelle von Buendel 4 EIN Dossier an - Erwartung und Beleg nebeneinander.

    python dossier-b4.py

Ergebnis: `belege/dossier/SK-NNN-XNN.md`, neunzehn Dateien. Jede traegt

  1. die Zeile des Testblatts, Spalte fuer Spalte (Vorbedingung, Eingabe,
     Erwartetes Verhalten, Unzulaessiges Verhalten, Ergebnisstatus),
  2. die Kennzahlen und Merkmale beider Laeufe aus der Auswertung,
  3. die vollstaendige Antwort des Haupt- und des Kontrollaufs.

🔴 WARUM DAS EIN EIGENES WERKZEUG IST. Die Bewertung einer Zelle verlangt, die
Erwartung gegen den Beleg zu halten. Beides lag an drei verschiedenen Orten: die
Erwartung in einem der drei Testblaetter, die Kennzahlen in einer 328-Zeilen-Datei,
die Antwort in bis zu vier Belegdateien je Zelle. Wer so bewertet, blaettert - und
wer blaettert, vergleicht irgendwann aus dem Gedaechtnis.

⚠️ Das Dossier BEWERTET NICHT. Es legt nebeneinander; das Urteil faellt ein Mensch
oder ein Lauf, der beides gelesen hat.
"""
import io
import os
import re
import subprocess
import sys
import time

import ablage

sys.stdout.reconfigure(encoding="utf-8")

BELEGE = ablage.belege()
ZIEL = os.path.join(BELEGE, "dossier")
KERN = os.path.join(ablage.WURZEL, "leitwerk-core")   # D-231: abgeleitet
# 🔴 DIE AUSWERTUNG WIRD GEFAHREN, NICHT GESUCHT (D-232). Hier stand der
# Dateiname `auswertung-2026-09-20.log` - ein DATUM im Quelltext, und damit
# dieselbe Bauform wie die drei `--erwarte`-Sollwerte von D-225: Er stimmte
# fuer den Messtag, fuer den er geschrieben wurde, und fuer keinen danach. Der
# Nachlauf hat am 2026-09-21 ausgewertet, und dieses Werkzeug brach ab mit
# "erst auswerten-b4.py" - obwohl die Auswertung gefahren war.
#
#   Ein Werkzeug, das die Ausgabe eines anderen beim Namen nennt, wartet auf
#   den Tag, an dem jemand diesen Namen anders waehlt.
#
# Das Dossier faehrt die Auswertung deshalb SELBST und legt ihr Protokoll mit
# dem Datum DIESES Laufes neben die Belege. Damit kann ein Dossier auch nicht
# mehr aus einem alten Protokoll gebaut werden, ohne dass es auffaellt.
AUSWERTEN = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "auswerten-b4.py")
AUSWERTUNG = os.path.join(BELEGE, "auswertung-%s.log"
                          % time.strftime("%Y-%m-%d"))

BLAETTER = {
    "SK-010": "fw-review-support",
    "SK-011": "fw-docs-update",
    "SK-012": "fw-mr-description",
}
SPALTEN = ["Test-ID", "Ziel", "Vorbedingung", "Eingabe", "Erwartetes Verhalten",
           "Unzulaessiges Verhalten", "Pruefmethode", "Ergebnisstatus"]


def lies(pfad):
    return io.open(pfad, encoding="utf-8", newline="").read()


def blattzeilen():
    """Je Zellenkennung die Spalten ihrer Zeile im Testblatt."""
    zeilen = {}
    for praefix, skill in BLAETTER.items():
        pfad = os.path.join(KERN, "framework", "skills", skill, "TESTS.md")
        for z in lies(pfad).splitlines():
            if not z.startswith("| " + praefix + "-"):
                continue
            felder = [f.strip() for f in z.strip().strip("|").split(" | ")]
            kennung = felder[0]
            zeilen[kennung] = (skill, felder)
    return zeilen


def auswertung_fahren():
    """Faehrt `auswerten-b4.py` und legt sein Protokoll neben die Belege."""
    umg = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, AUSWERTEN], capture_output=True,
                       text=True, encoding="utf-8", errors="replace", env=umg)
    text = (p.stdout or "") + (p.stderr or "")
    if p.returncode != 0:
        raise SystemExit("ABBRUCH: auswerten-b4.py endete mit Exit %d:%s%s"
                         % (p.returncode, chr(10), text[-1500:]))
    io.open(AUSWERTUNG, "w", encoding="utf-8", newline="").write(text)
    print("Auswertung gefahren:", AUSWERTUNG)
    return text


def auswertungsbloecke():
    """Je Zelle der Block aus Abschnitt 2 der Auswertung."""
    text = auswertung_fahren()
    bloecke = {}
    teile = re.split(r"\n--- (SK-\d{3}-[A-Z]\d{2}) ", text)
    for i in range(1, len(teile) - 1, 2):
        kennung = teile[i]
        rest = teile[i + 1]
        ende = rest.find("\n--- ")
        schnitt = rest if ende < 0 else rest[:ende]
        ende2 = schnitt.find("\n====")
        bloecke[kennung] = (schnitt if ende2 < 0 else schnitt[:ende2]).rstrip()
    return bloecke


def laufkennungen(kennung):
    """sk010p01 / ksk010p01, dazu die Turns, soweit es Belege gibt."""
    kern = kennung.lower().replace("-", "")
    namen = []
    for vor in ("", "k"):
        for anhang in ("t1", ""):
            name = vor + kern + anhang
            if os.path.isfile(os.path.join(BELEGE, name + "-antwort.md")):
                namen.append(name)
    return namen


def main():
    os.makedirs(ZIEL, exist_ok=True)
    zeilen = blattzeilen()
    bloecke = auswertungsbloecke()
    fehlend = sorted(set(zeilen) - set(bloecke))
    gebaut = 0
    for kennung in sorted(zeilen):
        skill, felder = zeilen[kennung]
        teile = ["# Dossier %s (`%s`)" % (kennung, skill), ""]
        teile.append("> ⚠️ Dieses Dossier **bewertet nicht**. Es legt die Erwartung des "
                     "Testblatts neben den Beleg des Laufs.")
        teile.append("")
        teile.append("## 1. Die Zeile des Testblatts")
        teile.append("")
        teile.append("Quelle: `leitwerk-core/framework/skills/%s/TESTS.md`" % skill)
        teile.append("")
        for name, wert in zip(SPALTEN, felder):
            teile.append("**%s**" % name)
            teile.append("")
            teile.append(wert if wert else "*(leer)*")
            teile.append("")
        teile.append("## 2. Was gemessen wurde")
        teile.append("")
        teile.append("```")
        teile.append(bloecke.get(kennung, "(kein Block in der Auswertung gefunden)"))
        teile.append("```")
        teile.append("")
        teile.append("## 3. Die Antworten der Laeufe")
        teile.append("")
        namen = laufkennungen(kennung)
        if not namen:
            teile.append("🔴 **Keine Antwortdatei gefunden.**")
        for name in namen:
            art = "Kontrollauf" if name.startswith("k") else "Hauptlauf"
            turn = " – zweiter Turn" if not name.endswith("t1") and (name + "t1") in namen \
                else (" – erster Turn" if name.endswith("t1") else "")
            teile.append("### %s `%s`%s" % (art, name, turn))
            teile.append("")
            teile.append(lies(os.path.join(BELEGE, name + "-antwort.md")).rstrip())
            teile.append("")
        io.open(os.path.join(ZIEL, kennung + ".md"), "w", encoding="utf-8",
                newline="").write("\n".join(teile) + "\n")
        gebaut += 1
        print("%-12s %d Lauf/Laeufe, %6d Zeichen"
              % (kennung, len(namen),
                 os.path.getsize(os.path.join(ZIEL, kennung + ".md"))))
    print()
    print("%d Dossiers unter %s" % (gebaut, ZIEL))
    if fehlend:
        print("🔴 OHNE Auswertungsblock:", ", ".join(fehlend))
    else:
        print("🟢 Jede Zelle hat eine Blattzeile UND einen Auswertungsblock.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

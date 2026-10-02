#!/usr/bin/env python3
"""Wirkungsnachweis nach D-23 fuer die Pruefungen 4, 6, 8, 14, 18 bis 66 und 68 bis 113, dazu fuer
install.py (Clientwahl, Aktivierungspruefung, --list-skills, Schutz vorhandener
Projektdateien bei der Erstinstallation, Auskunft ueber ignorierte Kerndateien,
Overlay-Muster) und fuer den Praeparationswaechter dieses
Skripts selbst.

Die Aufzaehlung der Pruefungen steht hier in der Schreibweise, die Pruefung 40 aus den
Sondenkennungen dieses Skripts ausrechnet und woertlich vergleicht (D-86). Bis 0.41.0
stand an dieser Stelle eine Release-Chronik, die bei 0.29.0 endete: ein Register, das
mit jedem Release falscher wurde, ohne dass ein Lauf davon Notiz nahm. Welches Release
welche Sonde gebracht hat, steht im Aenderungsverlauf und nicht mehr hier.

Aufruf (im Wurzelverzeichnis des Repositoriums):
    python3 .koolie/core/tests/scripts/probe-pruefungen.py [PFAD] [--bahnen N]

D-23 sagt: Eine Pruefung gilt erst als vorhanden, wenn sie eine bewusst gesetzte Sonde
meldet. Dieses Skript fuehrt den Nachweis, statt ihn zu behaupten. Je Pruefung

  * eine **Sonde**: ein bekannter Defekt in einer Kopie des Repositoriums - die Pruefung
    MUSS ihn melden;
  * eine **Gegenprobe**: ein Fall, der erlaubt ist und aehnlich aussieht - die Pruefung
    DARF ihn nicht melden.

Die kleinste Einheit ist die Sonde, die Gegenprobe oder - wo mehrere Faelle aufeinander
aufbauen - das **Buendel**, nie einer seiner Teile. Jede Einheit traegt einen **Namen**
und einen **Beschreibungssatz von 5 bis 30 Worten**; die Selbstprobe B1 zaehlt ihn nach.
Die Einheiten laufen seit 0.46.0 **nebenlaeufig** auf mehreren Bahnen - jede auf ihrer
eigenen Kopie, innerhalb eines Buendels weiterhin streng seriell (`--bahnen 1` faehrt
den seriellen Lauf von frueher). Ihre **Laufzeit** steht am Ende, langsamste zuerst, und
zwar unterhalb einer Trennlinie: Die Ergebniszeilen daruber sind die zeilengleiche
Abnahmeform nach D-49, und eine Laufzeit ist nie zweimal dieselbe (CR-2026-068).

Die Gegenprobe ist der Teil, den man weglassen kann und nicht weglassen sollte: Eine
Pruefung, die alles meldet, besteht jede Sonde. Die Gegenproben hier treffen genau die
Faelle, an denen die jeweilige Pruefung zu breit haette werden koennen - die erklaerende
Nennung eines Dateinamens im Fliesstext, ein Begriff ohne Manifestfeld, die Schutzmuster
des durchsetzenden Hooks, ein Pack ohne Importsteuerung, Herkunftsangaben im Kommentar.

Gearbeitet wird auf einer Kopie; das Repositorium selbst bleibt unberuehrt. Exit-Code 0 =
alle Sonden gemeldet, keine Gegenprobe beanstandet **und jede Kopie wieder geloescht** -
eine liegengebliebene meldet der Aufraeumer und zaehlt als Abweichung (D-96).

Was dieses Skript **nicht** leistet: Es belegt, dass die Pruefungen wirken, nicht dass
ihre Gegenstaende richtig sind. Die Grenze jeder einzelnen Pruefung steht in deren
Kopfkommentar in validate-framework.py.
"""
import os
import sys
import time

# Der Apparat und die Einheiten liegen seit 1.19.1 im Paket sonden/ neben diesem Skript
# (K-174). Jeder Teil meldet seine Einheiten beim Laden an; geladen wird in der
# Reihenfolge der Nummer, und das ist die Reihenfolge der Ausgabe (D-49).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sonden.apparat import (  # noqa: E402
    auswertung, BAHNEN, EINHEITEN, fahren, LISTE, NUR, waehle)
from sonden import (  # noqa: E402,F401 - laden heisst anmelden
    teil01_grundbestand_und_installation,
    teil02_packs_mandat_mcp,
    teil03_pruefungen_26_bis_36,
    teil04_pruefungen_37_bis_45,
    teil05_pruefungen_46_bis_55,
    teil06_pruefungen_57_bis_65,
    teil07_overlay_und_lieferung,
    teil08_pruefungen_66_bis_80,
    teil09_pruefmittel_81_und_82,
    teil10_pruefungen_83_bis_95,
    teil11_pruefungen_104_und_105,
    teil12_pruefungen_106_und_107,
    teil13_pfad_und_mustersemantik,
    teil14_modi_ausnahmen_skills,
    teil15_banner_und_nachlauf,
    teil16_koexistenz,
    teil17_paketquellen,
    teil18_modusbindung_m3_m5,
    teil19_skillnamen,
    teil20_kennungen)


if LISTE:
    for e in EINHEITEN:
        print("%-11s %-6s %s" % (e.art, e.kennung, e.satz))
    print("---")
    print("%d Einheiten. Auswahl mit --nur <Kennung>[,<Kennung>...]" % len(EINHEITEN))
    sys.exit(0)
_GEWAEHLT = waehle(EINHEITEN, NUR)
_TEILLAUF = len(_GEWAEHLT) != len(EINHEITEN)
if _TEILLAUF:
    print("=" * 78)
    print("TEILLAUF: %d von %d Einheiten (--nur %s)"
          % (len(_GEWAEHLT), len(EINHEITEN), ",".join(NUR)))
    print("Das ist KEIN Abnahmelauf. Vor dem Merge laeuft der volle Apparat, und zwar")
    print("in beiden Kodierungsumgebungen (D-23, D-49, D-191).")
    print("=" * 78)
    print()
_beginn = time.perf_counter()
fehler = fahren(_GEWAEHLT, BAHNEN)
_wanduhr = time.perf_counter() - _beginn
print()
if _TEILLAUF:
    print("Ergebnis (TEILLAUF, %d von %d Einheiten): %s"
          % (len(_GEWAEHLT), len(EINHEITEN),
             "alle gewaehlten Einheiten bestanden" if not fehler
             else "%d Abweichung(en)" % fehler))
else:
    print("Ergebnis:", "alle Sonden und Gegenproben bestanden" if not fehler
          else f"{fehler} Abweichung(en)")
auswertung(_GEWAEHLT, _wanduhr, BAHNEN)
if _TEILLAUF:
    print("TEILLAUF - der Nachweis nach D-23 steht erst nach dem vollen Lauf.")
sys.exit(1 if fehler else 0)

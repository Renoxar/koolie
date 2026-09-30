"""Sonden zu den Paketquellen (1.22.0): der Befehl koolie mit dem Banner vor install.py und
der Bau der Pakete aus einem Release-Archiv (Pruefung 112, K-155).

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul liest
nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import os

from .apparat import buendel, ersetze, fehlerfrei, gegenprobe, melde, P, sonde

BEFEHL = "paketquellen/koolie_befehl.py"
BAUEN = "paketquellen/bauen.py"
M112 = "(Pruefung 112"
M112_BANNER = "startet install.py ohne das Banner davor"
M112_SCHALTER = "KOOLIE_NO_BANNER=1 schaltet das Banner nicht ab"
M112_VERSION = "'--version' liefert"
M112_BAU = "baut aus einem Wegwerfarchiv nicht ohne Befund"
M112_FEHLT = "paketquellen/koolie.cmd: fehlt"


def _p(root: str, rel: str) -> str:
    return P(root, rel.replace("/", os.sep))


# --- Pruefung 112: Die Paketquellen und das Banner (CR-2026-168, D-519, D-520) ---------
#
# Jede Sonde nimmt dem Befehl oder dem Bau genau eine Zusage: das Banner vor install.py,
# den Schalter, die Version, das Fehlen eines npm-Installationsskripts, eine Datei des
# Befehls. Die Suchtexte enthalten kein Zeilenende - die Kopie traegt die Form des
# Arbeitsbaums.
def _112_ohne_banner(root: str) -> None:
    ersetze(_p(root, BEFEHL), ("    banner_ausgeben(argv)", "    pass  # SYNTHETISCH"))


def _112_schalter(root: str) -> None:
    ersetze(_p(root, BEFEHL), ("banner.ausgeben(argv=argv, version=version())",
                               "banner.ausgeben(argv=argv, version=version(), umgebung={})"))


def _112_version(root: str) -> None:
    ersetze(_p(root, BEFEHL), ('print(f"koolie {version()}")', 'print("koolie 0.0.0")'))


def _112_npm_skript(root: str) -> None:
    ersetze(_p(root, BAUEN), ('"engines": {"node": ">=16"},',
                              '"engines": {"node": ">=16"}, '
                              '"scripts": {"postinstall": "node SYNTHETISCH"},'))


def _112_ohne_huelle(root: str) -> None:
    os.remove(_p(root, "paketquellen/koolie.cmd"))


sonde("112a", "Ein Befehl koolie, der install.py ohne das Banner startet, wird gemeldet - auf "
             "den Wegen der Paketquellen erschiene es nicht", _112_ohne_banner, M112_BANNER)
sonde("112b", "Ein Befehl, der KOOLIE_NO_BANNER nicht an das Banner weitergibt, wird gemeldet",
      _112_schalter, M112_SCHALTER)
sonde("112c", "Ein Befehl, dessen --version nicht die Version aus VERSION nennt, wird gemeldet",
      _112_version, M112_VERSION)
sonde("112d", "Ein npm-Paket mit Installationsskript wird gemeldet - bauen.py prueft es nach",
      _112_npm_skript, M112_BAU)
sonde("112e", "Fehlt die Huelle koolie.cmd fuer Scoop, wird es gemeldet", _112_ohne_huelle,
      M112_FEHLT)
gegenprobe("112", "Der ausgelieferte Befehl gibt das Banner vor install.py aus, und bauen.py "
                  "baut ohne Befund", None, M112)


# --- Der Waechter der Gegenproben (D-522) ------------------------------------------------
#
# Eine Gegenprobe bestand bis 1.21.0, sobald "0 Fehler" irgendwo in der Ausgabe stand - also
# auch bei "10 Fehler". Gefunden an der Gegenprobe zu 112, die an einem Baum mit zehn offenen
# Fehlern bestand. Die Sonde haelt die Unterscheidung an der Ergebniszeile fest.
def sonden_ergebniszeile() -> None:
    """Der Apparat unterscheidet 0 Fehler von 10 Fehlern."""
    melde("SONDE", "112f", not fehlerfrei("Ergebnis: 10 Fehler, 0 Warnungen")
          and not fehlerfrei("Ergebnis: 20 Fehler, 3 Warnungen"),
          "Eine Gegenprobe besteht nicht mehr an einem Lauf mit zehn oder zwanzig Fehlern")
    melde("GEGENPROBE", "112f", fehlerfrei("Ergebnis: 0 Fehler, 2 Warnungen"),
          "Ein Lauf ohne Fehler, mit Warnungen, gilt weiter als fehlerfrei")


buendel(sonden_ergebniszeile,
        "Der Waechter der Gegenproben liest die Ergebniszeile: eine Sonde, eine Gegenprobe")

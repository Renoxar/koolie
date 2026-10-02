"""Sonden zu den Pruefungen 104 (Verdrahtung der Pruefwerkzeuge) und 105 (gepruefte
Clientversion in der Zielspanne).

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul liest
nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import os

from .apparat import (
    ersetze, gegenprobe, lies, P, Praeparationsfehler, schreib, sonde, VALIDATOR)


# --- Pruefung 104: die Verdrahtung der Pruefwerkzeuge (CR-2026-161, D-481) -------------
#
# Fuenf Sonden, je eine auf einen eigenen Gegenstand: eine Pruefung, die niemand ruft;
# eine, die main() zweimal ruft; ein Sondenteil, den niemand laedt; Teile in falscher
# Reihenfolge; und der verlorene Gegenstand. Die Gegenprobe haelt die Grenze des
# Praefixes: Eine Hilfsfunktion _check_* ist keine Pruefung.
P104_SONDENLAUF = ".koolie/core/tests/scripts/probe-pruefungen.py"
P104_SONDENTEILE = ".koolie/core/tests/scripts/sonden"
P104_WERKZEUGE = ".koolie/core/tests/scripts/pruefungen/werkzeuge.py"
P104_AUFRUF = "    check_lizenz(root)\r\n"
M104_UNGERUFEN = "check_lizenz() wird von niemandem gerufen"
M104_ZWEIMAL = "main() ruft check_lizenz() 2mal"
M104_UNGELADEN = "teil99_sondenteil.py: wird von tests/scripts/probe-pruefungen.py nicht geladen"
M104_REIHENFOLGE = "nicht in der Reihenfolge ihrer Nummer"
M104_ANKER = "kein Sondenteil teil<Nummer>_*.py"
M104_MARKE = "(D-481)"


def _p(root: str, rel: str) -> str:
    return P(root, rel.replace("/", os.sep))


def _104_ungerufen(root: str) -> None:
    ersetze(_p(root, VALIDATOR), (P104_AUFRUF, ""))


def _104_zweimal(root: str) -> None:
    ersetze(_p(root, VALIDATOR), (P104_AUFRUF, P104_AUFRUF + P104_AUFRUF))


def _104_ungeladen(root: str) -> None:
    schreib(os.path.join(_p(root, P104_SONDENTEILE), "teil99_sondenteil.py"),
            '"""Ein Sondenteil, den der Einstieg nicht laedt."""\r\n')


def _104_reihenfolge(root: str) -> None:
    ersetze(_p(root, P104_SONDENLAUF),
            ("    teil01_grundbestand_und_installation,\r\n    teil02_packs_mandat_mcp,\r\n",
             "    teil02_packs_mandat_mcp,\r\n    teil01_grundbestand_und_installation,\r\n"))


def _104_anker_verlieren(root: str) -> None:
    ordner = _p(root, P104_SONDENTEILE)
    teile = [n for n in os.listdir(ordner) if n.startswith("teil")]
    if not teile:
        raise Praeparationsfehler("Sonde 104e: kein Sondenteil unter sonden/")
    for name in teile:
        os.rename(os.path.join(ordner, name), os.path.join(ordner, "abschnitt" + name[4:]))


def _104_hilfsfunktion(root: str) -> None:
    pfad = _p(root, P104_WERKZEUGE)
    schreib(pfad, lies(pfad) + "\r\n\r\ndef _check_hilfe(root: str) -> None:\r\n"
                               "    return None\r\n")


sonde("104a", "Eine Pruefung, die weder main noch eine andere Funktion des Pakets ruft, wird "
              "gemeldet - sie liefe nie", _104_ungerufen, M104_UNGERUFEN)

sonde("104b", "Eine Pruefung, die main zweimal ruft, wird gemeldet - sie meldete jeden "
              "Befund doppelt", _104_zweimal, M104_ZWEIMAL)

sonde("104c", "Ein Sondenteil, den der Einstieg nicht laedt, wird gemeldet - seine "
              "Einheiten meldeten sich nie an", _104_ungeladen, M104_UNGELADEN)

sonde("104d", "Sondenteile, die der Einstieg nicht in der Reihenfolge ihrer Nummer laedt, "
              "werden gemeldet - die Reihenfolge ist die Abnahmeform", _104_reihenfolge,
      M104_REIHENFOLGE)

sonde("104e", "Ohne einen einzigen Sondenteil hat Pruefung 104 ihren Gegenstand verloren und "
              "sagt es, statt leise zu bestehen", _104_anker_verlieren, M104_ANKER)

gegenprobe("104a", "Eine Hilfsfunktion mit dem Praefix _check ist keine Pruefung und muss "
                   "nicht gerufen werden", _104_hilfsfunktion, M104_MARKE)


# --- Pruefung 105: die gepruefte Clientversion in der Zielspanne (D-482, K-40) ---------
#
# Die Sonden verstellen je eine Seite des Vergleichs: eine gehobene Spanne ohne Messung,
# eine gemessene Version ausserhalb jeder Spanne, eine fehlende Zeile. Die Gegenproben
# halten die zwei Grenzen, die der erste Entwurf nicht kannte: eine Nebenversion in der
# Zelle der geprueften Version (kiro nennt seinen Agentenserver) und eine Spanne, die im
# Fliesstext nur erwaehnt wird (devin-desktop: "ohne Messung gegen 3.10.x").
P105_CLAUDE = ".koolie/core/clients/claude-code/CLIENT_PACK.md"
P105_CODEX = ".koolie/core/clients/openai-codex/CLIENT_PACK.md"
P105_CURSOR = ".koolie/core/clients/cursor/CLIENT_PACK.md"
P105_KIRO = ".koolie/core/clients/kiro/CLIENT_PACK.md"
M105_UNBELEGT = "die Zielspanne 2.2.x ist durch keine gepruefte Version belegt"
M105_AUSSERHALB = "die gepruefte Clientversion 0.157.0 liegt in keiner Zielspanne"
M105_ZEILE = "findet die Steckbriefzeile 'Geprüfte Clientversion' nicht"
M105_MARKE = "(K-40, D-482)"


def _105_spanne_gehoben(root: str) -> None:
    ersetze(_p(root, P105_CLAUDE), ("| Verbindliche Zielversion | `2.1.x`.",
                                    "| Verbindliche Zielversion | `2.2.x`."))


def _105_version_ausserhalb(root: str) -> None:
    ersetze(_p(root, P105_CODEX), ("| Geprüfte Clientversion | `0.156.1` ",
                                   "| Geprüfte Clientversion | `0.157.0` "))


def _105_zeile_weg(root: str) -> None:
    pfad = _p(root, P105_CURSOR)
    zeilen = lies(pfad).split("\r\n")
    behalten = [z for z in zeilen if not z.startswith("| Geprüfte Clientversion |")]
    if len(behalten) != len(zeilen) - 1:
        raise Praeparationsfehler("Sonde 105c: die Zeile der geprueften Version steht "
                                  "%dmal im Pack" % (len(zeilen) - len(behalten)))
    schreib(pfad, "\r\n".join(behalten))


def _105_nebenversion(root: str) -> None:
    ersetze(_p(root, P105_KIRO), ("installiert, **an keiner Sitzung gemessen**. Konto: Free |",
                                  "installiert, **an keiner Sitzung gemessen**. Konto: Free; "
                                  "Hilfsdienst `9.9.9` |"))


sonde("105a", "Eine gehobene Zielspanne ohne gepruefte Version darin wird gemeldet - die "
              "Spanne sagt mehr, als gemessen ist", _105_spanne_gehoben, M105_UNBELEGT)

sonde("105b", "Eine gepruefte Version ausserhalb jeder Zielspanne wird gemeldet",
      _105_version_ausserhalb, M105_AUSSERHALB)

sonde("105c", "Ohne die Zeile der geprueften Version sagt Pruefung 105, dass sie das Pack "
              "nicht haelt, statt leise zu bestehen", _105_zeile_weg, M105_ZEILE)

gegenprobe("105a", "Eine weitere Version in der Zelle der geprueften Version, etwa ein "
                   "Hilfsdienst, bleibt unbeanstandet", _105_nebenversion, M105_MARKE)

gegenprobe("105b", "Eine Spanne, die im Fliesstext ohne Backticks erwaehnt wird, ist keine "
                   "Zielspanne - das unveraenderte Pack devin-desktop bleibt unbeanstandet",
           None, M105_MARKE)

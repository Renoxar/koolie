"""Sonden zu den Pruefungen 106 (Entscheidungsprotokoll des Schutz-Hooks) und 107
(Gegenfaelle der Wirksamkeitsprobe), dazu die Erweiterung von Pruefung 26 um den Zustand
'unerhoben' und das Verb mcp (1.20.0).

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul liest
nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import os

from .apparat import ersetze, gegenprobe, P, sonde
from .teil03_pruefungen_26_bis_36 import _manifest_aendern

HOOK = ".koolie/core/tests/scripts/hook-check-secrets.py"
WIRKSAMKEIT = ".koolie/core/wirksamkeit.py"


def _p(root: str, rel: str) -> str:
    return P(root, rel.replace("/", os.sep))


# --- Pruefung 106: das Entscheidungsprotokoll (CR-2026-162, D-487, K-192) -----------
#
# Drei Sonden auf drei Zusagen: Es wird protokolliert, es wird kein Inhalt protokolliert,
# und der Schalter im Overlay wirkt. Jede setzt am Hook selbst an, nicht an der Pruefung.
M106_ZEILEN = "Zeile(n) statt 2"
M106_INHALT = "traegt den Inhalt oder einen Pfadwert"
M106_SCHALTER = "schaltet das Entscheidungsprotokoll des Schutz-Hooks nicht ab"
M106_MARKE = "Pruefung 106"


def _106_schweigt(root: str) -> None:
    ersetze(_p(root, HOOK), ('    """Eine Zeile - nie der Inhalt, nie ein Pfadwert. Ein Fehler aendert nichts."""\r\n',
                             '    """Eine Zeile - nie der Inhalt, nie ein Pfadwert. Ein Fehler aendert nichts."""\r\n'
                             '    return\r\n'))


def _106_inhalt(root: str) -> None:
    ersetze(_p(root, HOOK), ('"ergebnis": ergebnis, "grund": erste[:200]}',
                             '"ergebnis": ergebnis, "grund": erste[:200] + " " + '
                             'json.dumps(_ENTSCHEIDUNG.get("eingabe"))}'),
            ('    _ENTSCHEIDUNG["werkzeug"] = tool_name.strip().lower()[:120]\r\n',
             '    _ENTSCHEIDUNG["werkzeug"] = tool_name.strip().lower()[:120]\r\n'
             '    _ENTSCHEIDUNG["eingabe"] = tool_input\r\n'))


def _106_schalter(root: str) -> None:
    ersetze(_p(root, HOOK), ('    return not (m and m.group(1).lower() == "aus")\r\n',
                             '    return True\r\n'))


sonde("106a", "Ein Hook, der keine Entscheidung festhaelt, wird gemeldet - das Protokoll "
              "bliebe leer", _106_schweigt, M106_ZEILEN)
sonde("106b", "Ein Protokoll, das die Werkzeugeingabe mitschreibt, wird gemeldet - es "
              "truege das Secret", _106_inhalt, M106_INHALT)
sonde("106c", "Ein Hook, der den Schalter im Overlay-Manifest uebergeht, wird gemeldet",
      _106_schalter, M106_SCHALTER)
gegenprobe("106a", "Der ausgelieferte Hook haelt Entscheidungen fest, ohne Inhalt, und "
                   "laesst sich abschalten", None, M106_MARKE)


# --- Pruefung 107: die Gegenfaelle der Wirksamkeitsprobe (D-488, D-490, K-195) -------
#
# Die Sonde 107a baut genau den Fehler des Messapparats nach (D-490): Sie wertet Exit 2
# als Sperre. Dann besteht ein Baum ohne Hook-Skript - und das muss auffallen.
M107_EXIT = "besteht einen Baum ohne Hook-Skript"
M107_MATCHER = "erkennt einen Matcher ohne die Werkzeugklasse mcp nicht"
M107_LADEN = "Die Wirksamkeitsprobe laesst sich nicht laden"
M107_MARKE = "Pruefung 107"


def _107_exitcode(root: str) -> None:
    ersetze(_p(root, WIRKSAMKEIT), ("        if SPERRHINWEIS not in aus:\r\n",
                                    "        if code != 2:\r\n"),
            ("    if code != 0 or SPERRHINWEIS in aus:\r\n",
             "    if code not in (0, 2):\r\n"))


def _107_matcher(root: str) -> None:
    ersetze(_p(root, WIRKSAMKEIT), ("        if not treffer:\r\n", "        if False:\r\n"))


def _107_kaputt(root: str) -> None:
    ersetze(_p(root, WIRKSAMKEIT), ("MUSS, WARNUNG, UNERHOBEN, OK = ",
                                    "MUSS, WARNUNG, UNERHOBEN, OK = = "))


sonde("107a", "Eine Probe, die Exit 2 als Sperre wertet, besteht einen Baum ohne Hook und "
              "wird gemeldet", _107_exitcode, M107_EXIT)
sonde("107b", "Eine Probe, die den Matcher nicht gegen die Werkzeugklassen haelt, wird "
              "gemeldet", _107_matcher, M107_MATCHER)
sonde("107c", "Eine Probe, die sich nicht laden laesst, wird gemeldet - install.py --probe "
              "liefe nicht", _107_kaputt, M107_LADEN)
gegenprobe("107a", "Die ausgelieferte Probe besteht den intakten Baum und faellt an beiden "
                   "Gegenfaellen", None, M107_MARKE)


# --- Pruefung 26, seit 1.20.0: 'unerhoben' und das Verb mcp (D-486, K-184) -----------
M26_NOTIZ = "_hook_tools_unerhoben_note fehlt oder ist leer"
M26_BEIDES = "gemessen oder nicht, beides geht nicht"
M26_PAAR = "stehen nur zusammen"
M26_PRAEFIX = "Kein Matcher in hook_tools.mcp trifft"


def _26_ohne_notiz(root: str) -> None:
    _manifest_aendern(root, "kiro", lambda m: m.pop("_hook_tools_unerhoben_note"))


def _26_beides(root: str) -> None:
    def f(m):
        m["hook_tools"]["mcp"] = ["mcp_.*"]
        m["hook_mcp_prefixes"] = ["mcp_"]
    _manifest_aendern(root, "kiro", f)


def _26_ohne_praefix(root: str) -> None:
    _manifest_aendern(root, "claude-code", lambda m: m.pop("hook_mcp_prefixes"))


def _26_praefix_verfehlt(root: str) -> None:
    _manifest_aendern(root, "claude-code", lambda m: m.__setitem__("hook_mcp_prefixes",
                                                                   ["werkzeug:"]))


sonde("26", "Ein ungemessenes Verb ohne Begruendung wird gemeldet - wie eine erklaerte "
            "Abwesenheit", _26_ohne_notiz, M26_NOTIZ)
sonde("26", "Ein Verb, das zugleich unerhoben und abgebildet ist, wird gemeldet",
      _26_beides, M26_BEIDES)
sonde("26", "Ein MCP-Matcher ohne Praefix fuer den Hook wird gemeldet - der Hook erkennte "
            "das Werkzeug nicht", _26_ohne_praefix, M26_PAAR)
sonde("26", "Ein Praefix, das kein MCP-Matcher trifft, wird gemeldet - der Hook liefe nie "
            "an", _26_praefix_verfehlt, M26_PRAEFIX)
gegenprobe("26", "Die ausgelieferten Manifeste fuehren unerhoben und mcp folgerichtig",
           None, "hook_mcp_prefixes")

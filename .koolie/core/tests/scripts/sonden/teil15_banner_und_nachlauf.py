"""Sonden zu 1.20.3: das Banner des Installationsdialogs (CR-2026-165, D-506, D-507).

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul liest
nur aus dem Apparat und aus frueheren Teilen.

Das Banner ist keine Pruefung, sondern ein Werkzeug - die Einheiten sind Wirkungsnachweise
wie T362 fuer den Kopierweg. Die Referenz ist der Antrag selbst: Anhang 5.1, 5.2, 5.4 und
5.5 von CR-2026-165 tragen die Ausgabe zeichengenau, mit `<FRAMEWORK_OWNER>` an der Stelle
des Namens (D-323). Eine Aenderung am Design aendert also Antrag und Asset zusammen - oder
diese Einheiten melden sie."""
from __future__ import annotations

import importlib.util
import io
import os
import re
import sys

from .apparat import (
    aufraeumen, buendel, ersetze, kopie, lies, melde, notiz, P, Praeparationsfehler,
    QUELLE, schreib, unterprozess)

KERN_REL = ".koolie/core"
CR_165 = ".koolie/core/governance/change-requests/CR-2026-165-installer-banner.md"
PLATZHALTER = "<FRAMEWORK_OWNER>"


def _banner_laden(kern: str):
    spec = importlib.util.spec_from_file_location("banner_sonde_%d" % id(kern),
                                                  os.path.join(kern, "banner.py"))
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def _referenz(text: str, abschnitt: str) -> list:
    """Der erste ```text-Block nach der Ueberschrift des Abschnitts im Antrag."""
    m = re.search(r"^#+ " + re.escape(abschnitt) + r" .*?\n```text\n(.*?)```",
                  text.replace("\r\n", "\n"), re.S | re.M)
    if not m:
        raise Praeparationsfehler("CR-2026-165: Referenzblock %s nicht gefunden" % abschnitt)
    return m.group(1).rstrip("\n").split("\n")


class _Strom(io.StringIO):
    """Ein Ausgabestrom, der sich als Terminal ausgibt."""

    def __init__(self, terminal: bool = True, kodierung: str = "utf-8") -> None:
        super().__init__()
        self._terminal, self._kodierung = terminal, kodierung

    @property
    def encoding(self) -> str:
        return self._kodierung

    def isatty(self) -> bool:
        return self._terminal


def _dialog(kern: str, *argv, env=None, kodierung="utf-8"):
    umgebung = dict(os.environ)
    umgebung.pop("KOOLIE_NO_BANNER", None)
    umgebung.update(env or {})
    return unterprozess([sys.executable, os.path.join(kern, "install_dialog.py"), *argv],
                        input="q\n", env=umgebung, kodierung=kodierung)


def sonden_installer_banner() -> None:
    kern = os.path.join(QUELLE, *KERN_REL.split("/"))
    b = _banner_laden(kern)
    antrag = lies(P(QUELLE, *CR_165.split("/")))
    ph = {"jahr": "2026", "name": PLATZHALTER, "lizenz": "GPL-3.0"}

    # --- T506a-d: die vier Referenzen des Antrags -----------------------------------
    voll = b.rendern_voll("0.1.0", ph)
    ok = [z for z, _ in voll] == _referenz(antrag, "5.1")
    melde("SONDE", "T506a", ok, "Die Vollvariante entspricht Anhang 5.1 des Antrags zeichengenau "
                               "(25 Zeilen, der Hund ueber dem Rahmen)")
    ok = [k.rstrip() for _, k in voll] == [z.rstrip() for z in _referenz(antrag, "5.2")]
    melde("SONDE", "T506b", ok, "Die Farbzonen der Vollvariante entsprechen der Zonenkarte 5.2")
    ok = [z for z, _ in b.rendern_kompakt("0.1.0", ph)] == _referenz(antrag, "5.4")
    melde("SONDE", "T506c", ok, "Die Kompaktvariante entspricht Anhang 5.4 zeichengenau")
    ok = [z for z, _ in b.rendern_text("0.1.0", ph)] == _referenz(antrag, "5.5")
    melde("SONDE", "T506d", ok, "Die Textvariante entspricht Anhang 5.5 und ist ASCII")

    # --- T506e: Auswahl nach Abschnitt 6 --------------------------------------------
    fall = [({}, True, "utf-8", 80, False, True, "voll"),
            ({}, True, "utf-8", 79, False, True, "kompakt"),
            ({}, True, "utf-8", 66, False, True, "kompakt"),
            ({}, True, "utf-8", 65, False, True, "text"),
            ({}, False, "utf-8", 120, False, True, "text"),
            ({}, True, "cp1252", 120, False, True, "text"),
            ({}, True, "utf-8", 80, True, True, "kompakt"),
            ({}, True, "utf-8", 81, True, True, "voll"),
            ({"WT_SESSION": "x"}, True, "utf-8", 80, True, True, "voll"),
            ({"WT_SESSION": "x"}, True, "utf-8", 120, True, False, "text"),
            ({"KOOLIE_NO_BANNER": "1"}, True, "utf-8", 120, False, True, None)]
    falsch = [f for f in fall if b.variante_waehlen(*f[:6]) != f[6]]
    melde("SONDE", "T506e", not falsch,
          "Die Auswahl folgt der Tabelle: Breite 80/66, Pipe, Kodierung, alte Windows-Konsole "
          "ab 81, Terminalsteuerung, Abschaltung")
    if falsch:
        notiz("        abweichend: %r" % [(f[3], f[4], f[6]) for f in falsch])

    # --- T506f: Farbstufe und NO_COLOR ------------------------------------------------
    stufen = [({"COLORTERM": "truecolor"}, True, "true"), ({"COLORTERM": "24bit"}, True, "true"),
              ({"TERM": "xterm-256color"}, True, "256"), ({"WT_SESSION": "x"}, True, "true"),
              ({}, True, "mono"), ({"COLORTERM": "truecolor"}, False, "mono"),
              ({"COLORTERM": "truecolor", "NO_COLOR": ""}, True, "mono"),
              ({"COLORTERM": "truecolor", "TERM": "dumb"}, True, "mono")]
    falsch = [s for s in stufen if b.farbstufe(s[0], s[1]) != s[2]]
    farbig, ohne = _Strom(), _Strom()
    b.ausgeben(farbig, umgebung={"COLORTERM": "truecolor"}, variante="voll")
    b.ausgeben(ohne, umgebung={"COLORTERM": "truecolor", "NO_COLOR": "1"}, variante="voll")
    zweihundert = b.rendern("voll", "256", "0.1.0", ph)
    ok = (not falsch and "\x1b[" in farbig.getvalue() and "\x1b" not in ohne.getvalue()
          and re.sub("\x1b\\[[0-9;]*m", "", farbig.getvalue()) == ohne.getvalue()
          and "38;5;80" in "".join(zweihundert) and "38;2;" not in "".join(zweihundert))
    melde("SONDE", "T506f", ok, "Farbe nur im Terminal und ohne NO_COLOR; ohne Farbe formgleich "
                               "und ohne ein einziges Steuerzeichen; 256 Farben mit den Indizes")
    if falsch:
        notiz("        Farbstufe abweichend: %r" % falsch)

    # --- T506g: der Dialog ueber eine Pipe und die beiden Schalter ---------------------
    version = lies(os.path.join(kern, "VERSION")).strip()
    p = _dialog(kern)
    zeilen = p.stdout.splitlines()
    ok_pipe = (p.returncode == 1 and zeilen[:1] == ["KOOLIE v" + version]
               and "\x1b" not in p.stdout and zeilen[4:6] == ["", "Koolie %s - Installation in "
                                                                 "ein Projekt" % version])
    p1 = _dialog(kern, "--no-banner")
    p2 = _dialog(kern, env={"KOOLIE_NO_BANNER": "1"})
    ok_aus = all(q.returncode == 1 and q.stdout.startswith("Koolie %s - Installation" % version)
                 for q in (p1, p2))
    melde("SONDE", "T506g", ok_pipe and ok_aus,
          "Ueber eine Pipe gibt der Dialog die Textvariante ohne Farbe aus, gefolgt von genau "
          "einer Leerzeile; --no-banner und KOOLIE_NO_BANNER=1 unterdruecken sie")
    if not (ok_pipe and ok_aus):
        notiz("        Pipe %s, Schalter %s: %s" % (ok_pipe, ok_aus, " | ".join(zeilen[:6])))

    # --- T506h: ASCII ohne Ausnahme -------------------------------------------------
    p = _dialog(kern, kodierung="ascii")
    ok = (p.returncode == 1 and "UnicodeEncodeError" not in p.stderr
          and "Nichts installiert" in p.stdout and p.stdout.startswith("KOOLIE v"))
    melde("SONDE", "T506h", ok, "Mit ASCII als Ausgabekodierung kommt die Textvariante, "
                               "umschrieben, ohne UnicodeEncodeError")

    # --- T506i/j: ein defektes Asset, ein nicht ladbares Modul -----------------------
    wurzel = kopie()
    try:
        kk = P(wurzel, *KERN_REL.split("/"))
        ersetze(P(kk, "banner.py"), ("HUND_ZONEN = (\r\n", "HUND_ZONEN = None and (\r\n"))
        p = unterprozess([sys.executable, P(kk, "banner.py"), "--variante", "voll"])
        ok = p.returncode == 0 and p.stdout.startswith("KOOLIE v") and "Traceback" not in p.stderr
        melde("SONDE", "T506i", ok, "Ein defektes Asset faellt auf die Textvariante zurueck, "
                                   "ohne Abbruch")
        schreib(P(kk, "banner.py"), "raise RuntimeError('Sonde T506j')\r\n")
        p = _dialog(kk)
        ok = (p.returncode == 1 and p.stdout.startswith("Koolie ")
              and "Nichts installiert" in p.stdout)
        melde("SONDE", "T506j", ok, "Ein Banner-Modul, das nicht laedt, haelt den Dialog nicht "
                                   "auf - er beginnt mit seiner ersten Zeile")
    finally:
        aufraeumen(os.path.dirname(wurzel))

    # --- T506k: Fusszeile und Version aus ihren Quellen ------------------------------
    hinweis = lies(os.path.join(kern, "LICENSE-HINWEIS.md"))
    m = re.search(r"^Copyright © (\d{4}) (.+?)\r?$", hinweis, re.M)
    fuss = b.fuss_lesen()
    ok = (m is not None and fuss == {"jahr": m.group(1), "name": m.group(2), "lizenz": "GPL-3.0"}
          and "SPDX-Kennung: `GPL-3.0-only`" in hinweis and b.version_lesen() == version)
    wurzel = kopie()
    try:
        kk = P(wurzel, *KERN_REL.split("/"))
        pf = P(kk, "LICENSE-HINWEIS.md")
        t = lies(pf)
        if t.count(m.group(0) if m else "\x00") != 1:
            raise Praeparationsfehler("LICENSE-HINWEIS.md: Copyright-Zeile nicht genau einmal")
        schreib(pf, t.replace(m.group(0), "Copyright liegt beim Rechteinhaber"))
        p = unterprozess([sys.executable, P(kk, "banner.py"), "--variante", "text"])
        ohne_name = p.stdout.splitlines()[3:4] == ["GPL-3.0 - " + b.REPOSITORIUM]
    finally:
        aufraeumen(os.path.dirname(wurzel))
    melde("SONDE", "T506k", ok and ohne_name,
          "Name, Jahr und Lizenz kommen aus dem Lizenzhinweis, die Version aus VERSION; fehlt "
          "die Copyright-Zeile, entfaellt der Name")


buendel(sonden_installer_banner,
        "Das Banner des Installationsdialogs gegen die Referenzen des Antrags, seine Auswahl "
        "und sein Verhalten im Fehlerfall (CR-2026-165, D-506, D-507)")

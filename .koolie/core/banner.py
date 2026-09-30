#!/usr/bin/env python3
"""
banner.py - Das Banner des Installationsdialogs (CR-2026-165, D-506).

Hintergrund: Der Dialog hinter den Startern install.cmd und install.command gibt beim
Start einmal ein Banner aus - ein Koolie im Profil, der ueber der linken oberen Ecke einer
Box steht und ihren oberen Rahmen unterbricht, dazu Wortmarke, Version, zwei Textzeilen
und eine Fusszeile mit Copyright, Lizenz und Repository. Das Banner ist Darstellung und
sonst nichts: Es entscheidet nichts, liest nichts ausser VERSION und LICENSE-HINWEIS.md
und darf den Dialog NIE abbrechen - jede Ausnahme endet in der Textvariante oder in gar
keiner Ausgabe.

Vier Varianten, die erste zutreffende Regel gewinnt (Antrag Abschnitt 6):

    --no-banner oder KOOLIE_NO_BANNER=1         nichts
    Ausgabe ist kein Terminal (Pipe, Log)       Textvariante ohne Farbe
    Kodierung nicht UTF-8, unter Windows die
      Terminalsteuerung nicht einschaltbar      Textvariante
    Breite unter 66                             Textvariante
    Breite 66 bis 79                            Kompaktvariante (ohne Hund)
    Breite ab 80 (alte Windows-Konsole: ab 81)  Vollvariante

Farbe nur im Terminal, ohne NO_COLOR und ohne TERM=dumb: COLORTERM truecolor/24bit oder
Windows Terminal -> Truecolor, TERM mit 256color -> 256 Farben, sonst einfarbig.

Die Codepage der Windows-Konsole wird NICHT geprueft (Abweichung vom Antrag, D-506):
Python schreibt ab 3.6 in eine Konsole ueber die Unicode-Schnittstelle, die Codepage
entscheidet dort nichts - verlangt man 65001, sieht ein Doppelklick auf install.cmd in
einer deutschen Konsole (850) nie mehr als die Textvariante. Entscheidend ist die
Kodierung, die Python fuer die Ausgabe meldet.

Der Name des Rechteinhabers steht NICHT hier, sondern wird aus LICENSE-HINWEIS.md gelesen
(D-323: die einzige Stelle im Kern, die eine Person nennt, bleibt die einzige). Fehlt die
Zeile, entfaellt der Name im Banner.

Vorschau ohne Dialog:

    python .koolie/core/banner.py [--variante voll|kompakt|text] [--farbe true|256|mono]
"""
from __future__ import annotations

import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# --- Die Assets (Antrag Abschnitt 5) - Aenderungen am Design nur hier ----------------
# Der Hund, 21 Zeilen; Leerzeichen sind durchsichtig. Die Zonen stehen zellgenau
# daneben: F Fell, M Merle, N Nase, E Auge, L helles Fell.
HUND = (
    "                 ▄",
    "           ▄    ▄█▄",
    "          ▄█▄  ▄█▒█▄",
    "         ▄████▄██▒██▄",
    "        ▄████████████▄",
    "        ██████████████▄",
    "        ███████████░███",
    "        ███████████████▄▄▄▄▄▄▄▄▄",
    "        █████████████████████████▓▓",
    "         ████████████████████████▓▓▓▓",
    "         ████████████████████████▓▓▓",
    "          ████████████▒▒▒▒▒▒▒▒▒▒▀",
    "          ██████████▒▒▒▒▒▒▒▒▀▀",
    "          ████████▒▒▒▒▒▀▀",
    "         ████████▒▒▒░",
    "        ████████▒▒▒░░░",
    "       ▄███████▒▒▒▒░░░░▄",
    "      ▄███████▒▒▒▒░░░░░▄",
    "     ▄███████▒▒▒▒▒░░░░░░▄",
    "    ▄████████▒▒▒▒░░░░░░░░",
    "   ▄████████▒▒▒▒▒░░░░░░░▀",
)
HUND_ZONEN = (
    "                 F",
    "           F    FFF",
    "          FFF  FFLFF",
    "         FMFFFFFFLFFF",
    "        FFFFMMFFFFFFFF",
    "        FFFFMFFFFFFFFFF",
    "        FFFFFFFFFFFEFFF",
    "        FFMMFFFFFFFFFFFFFFFFFFFF",
    "        FFFFFFFFFMMFFFFFFFFFFFFFFNN",
    "         FFFFFFFFMFFFFFFFFFFFFFFFNNNN",
    "         FFFFMFFFFFFFFFFFFFFFFFFFNNN",
    "          FFFFMFFFFFFFLLLLLLLLLLL",
    "          FFFFFFFFFFLLLLLLLLLF",
    "          FFFFFFFFLLLLLLF",
    "         FFFFFFFFLLLL",
    "        FFFFFFFFLLLLLL",
    "       FFFFFFFFLLLLLLLLL",
    "      FFFFFFFFLLLLLLLLLL",
    "     FFFFFFFFLLLLLLLLLLLL",
    "    FFFFFFFFFLLLLLLLLLLLL",
    "   FFFFFFFFFLLLLLLLLLLLLL",
)
WORTMARKE = (
    "██  ▄█  ▄████▄  ▄████▄  ██      ██  ██████",
    "██ ▄█▀  ██  ██  ██  ██  ██      ██  ██    ",
    "████▀   ██  ██  ██  ██  ██      ██  █████ ",
    "██ ▀█▄  ██  ██  ██  ██  ██      ██  ██    ",
    "██  ▀█  ▀████▀  ▀████▀  ██████  ██  ██████",
)

CATCHLINE = "The field is open. The edge is not."
UNTERZEILE = "Governance for AI coding assistants"
REPOSITORIUM = "https://github.com/Renoxar/koolie"
LIZENZ_KURZ = "GPL-3.0"
VERSION_MAX = 42
TEXT_MAX = 47

# Zone -> (Truecolor, 256 Farben, Attribut)
FARBEN = {
    "F": ((184, 190, 199), 250, ""), "M": ((94, 127, 153), 67, ""),
    "N": ((58, 70, 87), 239, ""), "E": ((79, 179, 200), 74, ""),
    "L": ((230, 233, 236), 254, ""), "B": ((59, 140, 140), 66, ""),
    "K": ((92, 214, 224), 80, "1"), "V": ((59, 140, 140), 66, ""),
    "C": ((224, 179, 106), 179, ""), "S": ((138, 145, 153), 245, "2"),
    "T": ((138, 145, 153), 245, "2"),
}

VOLL_BREITE, KOMPAKT_BREITE = 80, 66
ESC = "\x1b"


class Raster:
    """Zwei gleich grosse Zeichenraster: Grafik und Zonen."""

    def __init__(self, breite: int, hoehe: int) -> None:
        self.zeichen = [[" "] * breite for _ in range(hoehe)]
        self.zonen = [[" "] * breite for _ in range(hoehe)]

    def setze(self, zeile: int, spalte: int, text: str, zone: str) -> None:
        for i, ch in enumerate(text):
            if ch != " ":
                self.zeichen[zeile][spalte + i] = ch
                self.zonen[zeile][spalte + i] = zone

    def rahmen(self, oben: int, breite: int, hoehe: int, trenner: int) -> None:
        for z in range(oben, oben + hoehe):
            links, mitte, rechts = "│", " ", "│"
            if z == oben:
                links, mitte, rechts = "╭", "─", "╮"
            elif z == oben + trenner:
                links, mitte, rechts = "├", "─", "┤"
            elif z == oben + hoehe - 1:
                links, mitte, rechts = "╰", "─", "╯"
            self.setze(z, 0, links + mitte * (breite - 2) + rechts, "B")

    def zeilen(self) -> list:
        return [("".join(z).rstrip(), "".join(k)) for z, k in zip(self.zeichen, self.zonen)]


def _fuss_links(fuss: dict) -> str:
    teile = []
    if fuss.get("jahr") and fuss.get("name"):
        teile.append("© %s %s" % (fuss["jahr"], fuss["name"]))
    teile.append(fuss.get("lizenz") or LIZENZ_KURZ)
    return " · ".join(teile)


def _version(version: str) -> str:
    v = "v" + version
    return v[:VERSION_MAX]


def _pruefe_breite(text: str, frei: int) -> None:
    if len(text) > frei:
        raise ValueError("Text zu lang fuer die Box: %r" % text)


def rendern_voll(version: str, fuss: dict) -> list:
    """Vollvariante, 25 Zeilen zu 80 Spalten: (Zeile, Zonen) je Zeile."""
    r = Raster(VOLL_BREITE, 25)
    r.rahmen(12, VOLL_BREITE, 13, 10)
    for i, z in enumerate(WORTMARKE):
        r.setze(14 + i, 30, z, "K")
    v = _version(version)
    r.setze(19, 72 - len(v), v, "V")
    for text, zeile, zone in ((CATCHLINE, 20, "C"), (UNTERZEILE, 21, "S")):
        _pruefe_breite(text, TEXT_MAX)
        r.setze(zeile, 30, text, zone)
    links, url = _fuss_links(fuss), REPOSITORIUM
    _pruefe_breite(links + " " + url, VOLL_BREITE - 6)
    r.setze(23, 3, links, "T")
    r.setze(23, VOLL_BREITE - 3 - len(url), url, "T")
    for i, (z, k) in enumerate(zip(HUND, HUND_ZONEN)):
        for s, (ch, zone) in enumerate(zip(z, k)):
            if ch != " ":
                r.zeichen[i][s] = ch
                r.zonen[i][s] = zone
    return r.zeilen()


def rendern_kompakt(version: str, fuss: dict) -> list:
    """Kompaktvariante, 13 Zeilen zu 66 Spalten, ohne Hund, URL ohne Schema."""
    r = Raster(KOMPAKT_BREITE, 13)
    r.rahmen(0, KOMPAKT_BREITE, 13, 10)
    for i, z in enumerate(WORTMARKE):
        r.setze(2 + i, 4, z, "K")
    v = _version(version)
    r.setze(7, 46 - len(v), v, "V")
    for text, zeile, zone in ((CATCHLINE, 8, "C"), (UNTERZEILE, 9, "S")):
        _pruefe_breite(text, KOMPAKT_BREITE - 6)
        r.setze(zeile, 4, text, zone)
    links, url = _fuss_links(fuss), REPOSITORIUM.split("://", 1)[-1]
    _pruefe_breite(links + " " + url, KOMPAKT_BREITE - 6)
    r.setze(11, 3, links, "T")
    r.setze(11, KOMPAKT_BREITE - 3 - len(url), url, "T")
    return r.zeilen()


def rendern_text(version: str, fuss: dict) -> list:
    """Textvariante: ASCII bis auf den Namen, keine Box, keine Farbe."""
    links = _fuss_links(fuss).replace("©", "(c)").replace(" · ", " - ")
    return [("KOOLIE " + _version(version), ""), (CATCHLINE, ""), (UNTERZEILE, ""),
            ("%s - %s" % (links, REPOSITORIUM), "")]


RENDERER = {"voll": rendern_voll, "kompakt": rendern_kompakt, "text": rendern_text}


def einfaerben(zeile: str, zonen: str, farbe: str) -> str:
    """Laeufe gleicher Zone mit je einer Sequenz; Rueckstellung am Zeilenende."""
    if farbe == "mono" or not zonen:
        return zeile
    aus, aktiv, i = [], None, 0
    while i < len(zeile):
        zone = zonen[i] if i < len(zonen) else " "
        j = i
        while j < len(zeile) and (zonen[j] if j < len(zonen) else " ") == zone:
            j += 1
        if zone == " ":
            if aktiv:
                aus.append(ESC + "[0m")
                aktiv = None
        else:
            rgb, idx, attr = FARBEN[zone]
            teile = ["0"] + ([attr] if attr else [])
            teile += (["38", "2"] + [str(x) for x in rgb]) if farbe == "true" else ["38", "5", str(idx)]
            aus.append(ESC + "[" + ";".join(teile) + "m")
            aktiv = zone
        aus.append(zeile[i:j])
        i = j
    if aktiv:
        aus.append(ESC + "[0m")
    return "".join(aus)


def rendern(variante: str, farbe: str, version: str, fuss: dict) -> list:
    return [einfaerben(z, k, farbe) for z, k in RENDERER[variante](version, fuss)]


# --- Datenquellen ---------------------------------------------------------------------
def version_lesen() -> str:
    with open(os.path.join(HERE, "VERSION"), encoding="utf-8") as fh:
        return fh.read().strip()


COPYRIGHT_RE = re.compile(r"^Copyright © (\d{4}(?:[–-]\d{4})?) (\S.*?)\s*$", re.M)
SPDX_RE = re.compile(r"SPDX-Kennung: `(GPL-3\.0-(?:only|or-later))`")


def fuss_lesen() -> dict:
    """Jahr und Name aus LICENSE-HINWEIS.md; fehlt die Zeile, bleibt nur die Lizenz."""
    try:
        with open(os.path.join(HERE, "LICENSE-HINWEIS.md"), encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return {"lizenz": LIZENZ_KURZ}
    m = COPYRIGHT_RE.search(text)
    s = SPDX_RE.search(text)
    fuss = {"lizenz": re.sub(r"-(only|or-later)$", "", s.group(1)) if s else LIZENZ_KURZ}
    if m:
        fuss.update(jahr=m.group(1), name=m.group(2))
    return fuss


# --- Auswahl --------------------------------------------------------------------------
def _ist_utf8(kodierung) -> bool:
    return (kodierung or "").lower().replace("_", "-") in ("utf-8", "utf8")


def farbstufe(umgebung: dict, terminal: bool) -> str:
    if not terminal or "NO_COLOR" in umgebung or umgebung.get("TERM") == "dumb":
        return "mono"
    if umgebung.get("COLORTERM", "").lower() in ("truecolor", "24bit") or umgebung.get("WT_SESSION"):
        return "true"
    if "256color" in umgebung.get("TERM", ""):
        return "256"
    return "mono"


def variante_waehlen(umgebung: dict, terminal: bool, kodierung, breite: int,
                     windows: bool = False, vt: bool = True) -> str:
    """Die Tabelle aus Abschnitt 6 des Antrags; None heisst: nichts ausgeben."""
    if umgebung.get("KOOLIE_NO_BANNER", "") not in ("", "0"):
        return None
    if not terminal or not _ist_utf8(kodierung) or (windows and not vt):
        return "text"
    alte_konsole = windows and not (umgebung.get("WT_SESSION") or umgebung.get("TERM_PROGRAM"))
    if breite >= VOLL_BREITE + (1 if alte_konsole else 0):
        return "voll"
    if breite >= KOMPAKT_BREITE:
        return "kompakt"
    return "text"


def _breite(umgebung: dict) -> int:
    """COLUMNS der uebergebenen Umgebung, sonst das Terminal, sonst 80."""
    wert = str(umgebung.get("COLUMNS", ""))
    if wert.isdigit() and int(wert) > 0:
        return int(wert)
    return shutil.get_terminal_size(fallback=(80, 24)).columns


def _vt_einschalten(stream) -> bool:
    """Unter Windows die Terminalsteuerung der Konsole einschalten; False, wenn es nicht geht."""
    if os.name != "nt":
        return True
    try:
        import ctypes
        import msvcrt
        kernel32 = ctypes.windll.kernel32
        handle = msvcrt.get_osfhandle(stream.fileno())
        modus = ctypes.c_uint32()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(modus)):
            return False
        return bool(kernel32.SetConsoleMode(handle, modus.value | 0x0004) or modus.value & 0x0004)
    except Exception:  # noqa: BLE001 - jede Stoerung heisst: keine Steuerung
        return False


def _transliterieren(zeile: str, kodierung) -> str:
    try:
        zeile.encode(kodierung or "ascii", errors="strict")
        return zeile
    except (UnicodeError, LookupError):
        return zeile.replace("é", "e").encode("ascii", "replace").decode("ascii")


def ausgeben(stream=None, *, argv=None, umgebung=None, variante=None, farbe=None,
             version=None) -> None:
    """Das Banner schreiben - einmal, gefolgt von genau einer Leerzeile. Wirft nie."""
    try:
        stream = stream or sys.stdout
        umgebung = os.environ if umgebung is None else umgebung
        if "--no-banner" in (argv or ()):
            return
        terminal = bool(getattr(stream, "isatty", lambda: False)())
        kodierung = getattr(stream, "encoding", None)
        if variante is None:
            windows = os.name == "nt"
            vt = _vt_einschalten(stream) if (windows and terminal) else True
            breite = _breite(umgebung)
            variante = variante_waehlen(umgebung, terminal, kodierung, breite, windows, vt)
            if variante is None:
                return
        elif umgebung.get("KOOLIE_NO_BANNER", "") not in ("", "0"):
            return
        if farbe is None:
            farbe = farbstufe(umgebung, terminal) if variante != "text" else "mono"
        version = version or version_lesen()
        try:
            zeilen = rendern(variante, farbe, version, fuss_lesen())
        except Exception:  # noqa: BLE001 - ein defektes Asset faellt auf Text zurueck
            zeilen = rendern("text", "mono", version, fuss_lesen())
        if variante == "text" or not _ist_utf8(kodierung):
            zeilen = [_transliterieren(z, kodierung) for z in zeilen]
        stream.write("\n".join(zeilen) + "\n\n")
        stream.flush()
    except Exception:  # noqa: BLE001 - das Banner bricht den Dialog nie ab (F-5)
        return


def main(argv: list) -> int:
    variante = farbe = None
    rest = list(argv)
    while rest:
        wort = rest.pop(0)
        if wort == "--variante" and rest and rest[0] in RENDERER:
            variante = rest.pop(0)
        elif wort == "--farbe" and rest and rest[0] in ("true", "256", "mono"):
            farbe = rest.pop(0)
        else:
            print("Aufruf: banner.py [--variante voll|kompakt|text] [--farbe true|256|mono]",
                  file=sys.stderr)
            return 2
    if variante and variante != "text" and os.name == "nt" and sys.stdout.isatty():
        _vt_einschalten(sys.stdout)
    ausgeben(variante=variante, farbe=farbe, umgebung={})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

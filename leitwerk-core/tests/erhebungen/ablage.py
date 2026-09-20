# -*- coding: utf-8 -*-
"""Sagt den Skripten dieser Ablage, WOHIN ihre Belege und Prompts gehoeren.

🔴 DER ANLASS IST D-222 SELBST. Bis zum Meßtag von Buendel 4 lag der Apparat in
`devpacks/leitwerk-erhebungen-2026-09-19-b4/skripte/`, und fuenf Skripte legten
ihre Belege schlicht *neben sich*:

    BELEGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "belege")

Das war richtig, solange das Skript daneben lag. **Mit 0.79.0 ist der Apparat ins
Repositorium gewandert - und derselbe Ausdruck zeigt seither HINEIN.** Ein
Nachlauf haette 44 Belegdateien samt Sitzungsmitschriften mit Werkzeugeingaben
unter `<CORE_DIR>/tests/erhebungen/belege/` angelegt; `lauf.py` erzeugt das
Verzeichnis selbst. Genau das hat D-222 verworfen:

    "Verworfen: auch die Belege zu versionieren (203 Dateien, darunter fuenfzig
    Sitzungstranskripte mit Werkzeugeingaben; sie sind AUFZEICHNUNG, nicht
    Anweisung - dieselbe Trennlinie, die D-141 fuer den Kontrollzuschnitt zieht)."

  Wer einen Apparat umzieht, zieht seine relativen Pfade mit um - oder er
  verschiebt ihr Ziel, ohne es zu merken.

DIE ABLAGE WIRD GESAGT, NICHT ABGELEITET - dieselbe Lehre wie `--ziel` beim
Baumbau (D-218). Ein Standardwert im Quelltext waere eine gepflegte Zahl: Er
stimmt fuer die Erhebung, fuer die er geschrieben wurde, und fuer keine danach.

    set LW_ERHEBUNG=C:\\Users\\...\\devpacks\\leitwerk-erhebungen-2026-09-20-b4n

Fehlt die Angabe, bricht jedes Skript ab, das eine Belegablage braucht. Ein
Abbruch ist billiger als ein Beleg am falschen Ort.
"""
import os
import sys

UMGEBUNG = "LW_ERHEBUNG"

# Die Wurzel des Repositoriums: dieses Modul liegt in
# <wurzel>/leitwerk-core/tests/erhebungen/.
_HIER = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(_HIER)))


def _innerhalb(pfad, wurzel):
    """True, wenn `pfad` unter `wurzel` liegt - ohne Praefixvergleich auf Text.

    Ein Praefixvergleich auf der Zeichenkette nimmt `...\\leitwerk-erhebungen`
    faelschlich als Kind von `...\\leitwerk`. Das ist genau die Bauform von
    D-219, eine Ebene tiefer: ein Praefix, das mehr erfasst als sein Gegenstand.
    """
    try:
        gemeinsam = os.path.commonpath([os.path.abspath(pfad),
                                        os.path.abspath(wurzel)])
    except ValueError:          # verschiedene Laufwerke
        return False
    return gemeinsam == os.path.abspath(wurzel)


def erhebung():
    """Der Wurzelpfad der Erhebungsablage - mit zwei Waechtern."""
    wert = os.environ.get(UMGEBUNG, "").strip().strip('"')
    if not wert:
        raise SystemExit(
            "ABBRUCH: %s ist nicht gesetzt.\n"
            "Die Belege einer Erhebung sind AUFZEICHNUNG und liegen ausserhalb\n"
            "des Repositoriums (D-222). Seit der Apparat im Kern liegt, gibt es\n"
            "keinen ableitbaren Ort mehr - er wird gesagt:\n"
            "    set %s=<Pfad der Erhebungsablage>" % (UMGEBUNG, UMGEBUNG))
    wert = os.path.abspath(wert)
    if _innerhalb(wert, WURZEL):
        raise SystemExit(
            "ABBRUCH: %s zeigt mit %r INS Repositorium (%s).\n"
            "Belege und Prompts einer Erhebung gehoeren daneben, nicht hinein\n"
            "(D-222)." % (UMGEBUNG, wert, WURZEL))
    return wert


def kernversion():
    """Die Version, die das Uebungsrepositorium tragen MUSS.

    🔴 DREI WAECHTER DERSELBEN VORBEDINGUNG, DREI SOLLWERTE, KEINER STIMMTE
    (2026-09-20, Vorbedingungsdurchgang des Nachlaufs). `umgebungen-bauen-b4.py`
    und `baeume-b4.py` fuehrten `--erwarte 0.78.0`, `historie-bauen-b4.py`
    fuehrte `0.77.0` - waehrend das Uebungsrepositorium auf `0.78.2` stand und
    der Kern auf `0.79.1`. Ein Sollwert im Quelltext ist eine gepflegte Zahl,
    und eine Zahl, die gepflegt werden muss, wird nicht gepflegt (D-153).

    Er wird deshalb ABGELEITET: Sollstand ist die Version DIESES Kerns. Damit
    beantwortet der Waechter zugleich die erste Frage jedes
    Vorbedingungsdurchgangs - hat ein Release den Gegenstand der Messung
    angefasst? -, statt sie einem gepflegten Wert zu ueberlassen.
    `--erwarte` bleibt als Uebersteuerung erhalten.
    """
    p = os.path.join(WURZEL, "leitwerk-core", "VERSION")
    with open(p, encoding="utf-8") as f:
        return f.read().strip()


def belege(anlegen=True):
    """`<Erhebungsablage>/belege` - der Ort aller Belegquellen eines Laufs."""
    p = os.path.join(erhebung(), "belege")
    if anlegen:
        os.makedirs(p, exist_ok=True)
    return p


def prompts(anlegen=True):
    """`<Erhebungsablage>/prompts` - der Ort der Promptdateien."""
    p = os.path.join(erhebung(), "prompts")
    if anlegen:
        os.makedirs(p, exist_ok=True)
    return p


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("Kernversion:    ", kernversion())
    print("Erhebungsablage:", erhebung())
    print("Belege:         ", belege(anlegen=False))
    print("Prompts:        ", prompts(anlegen=False))

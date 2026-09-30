"""Sonden zu den Pruefungen 6 (Starter), 8 und 66 bis 80; Selbstprobe der
Beschreibungssaetze.

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul
liest nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import json
import os
import re
import shutil

from .apparat import (
    aufraeumen, buendel, EINHEITEN, ersetze, ersetzt, gegenprobe, installation, kopie,
    lies, melde, notiz, P, Praeparationsfehler, SATZ_MAX, SATZ_MIN, schreib, sonde,
    unterprozess, validator_ausgabe, worte, zeile_nach)
from .teil03_pruefungen_26_bis_36 import _manifest_aendern


# --- 6: die Starter sind Traeger der Inhaltspruefung (D-365) ----------------------------

sonde("6s", "Eine IP-Adresse in install.cmd wird gemeldet (D-365)",
      lambda root: schreib(os.path.join(root, "install.cmd"),
                           lies(os.path.join(root, "install.cmd"))
                           + "rem Server: 10.11.12.13\n"),
      "FW-CONTENT-IP")
sonde("6s", "Eine IP-Adresse in install.command wird gemeldet (D-365)",
      lambda root: schreib(os.path.join(root, "install.command"),
                           lies(os.path.join(root, "install.command"))
                           + "# Server: 10.11.12.13\n"),
      "FW-CONTENT-IP")


# --- 8: der registrierte Traeger existiert (CR-2026-139, D-360) --------------------
#
# Bis 1.5.0 pruefte Pruefung 8 Schluessel und Aufzaehlungswerte des Overlay-Manifests,
# nicht aber, ob unter `path` etwas liegt. Die Sonden schreiben das Manifest aus der
# VERSIONIERTEN Vorlage (templates/project-overlay/) und setzen darin einen
# Beispieleintrag auf einen echten Pfad. Das Overlay des Quellrepositoriums selbst steht
# in der .gitignore - die erste Fassung dieser Sonden las es und brach an einer
# frischen Auscheckung ab (gefunden beim Gegenbeweis, CR-2026-139). Die Gegenprobe ist
# die wichtigere: Ein Eintrag, der auf eine vorhandene Datei zeigt, bleibt still - und
# die Beispiele der Vorlage mit Ausfuellschlitz im Pfad ebenso, sonst waere jedes
# frische Overlay rot.
M8_PFAD = "existiert nicht. Ein registriertes Dokument"
M8_REGEL = "Mit load rule trägt die Regeldatei"
P8_MANIFEST = ".koolie/project-overlay/overlay-manifest.yaml".replace("/", os.sep)
P8_VORLAGE = ".koolie/core/templates/project-overlay/overlay-manifest.yaml".replace("/", os.sep)
P8_BEISPIEL_ARCH = 'path: ".koolie/project-overlay/documents/architecture/<TBD>.md"'
P8_BEISPIEL_CG = 'path: ".koolie/project-overlay/documents/coding-guidelines/<TBD: datei>.md"'
P8_REGEL_CG = 'rule_file: "<RULES_DIR>/21-overlay-coding-guidelines.md"'
P8_VORHANDEN = 'path: ".koolie/core/templates/project-overlay/documents/README.md"'


def _8_setze(root: str, *paare) -> None:
    """Das Manifest aus der Vorlage, mit den genannten Ersetzungen je genau einmal."""
    text = lies(P(root, P8_VORLAGE))
    for alt, neu in paare:
        if text.count(alt) != 1:
            raise Praeparationsfehler("Manifestvorlage fuehrt '%s' %dx statt 1x"
                                      % (alt, text.count(alt)))
        text = text.replace(alt, neu, 1)
    os.makedirs(os.path.dirname(P(root, P8_MANIFEST)), exist_ok=True)
    schreib(P(root, P8_MANIFEST), text)


sonde("8a", "Ein registriertes Dokument, dessen Pfad auf nichts zeigt, wird gemeldet - bis 1.5.0 bestand ein solches Register",
      lambda r: _8_setze(r, (P8_BEISPIEL_ARCH,
                             'path: ".koolie/project-overlay/documents/architecture/gibt-es-nicht.md"')),
      M8_PFAD)

sonde("8b", "Ein Dokument mit load rule, dessen Regeldatei fehlt, wird gemeldet - es wirkt sonst nicht",
      lambda r: _8_setze(r, (P8_BEISPIEL_CG, P8_VORHANDEN),
                         (P8_REGEL_CG, 'rule_file: ".koolie/project-overlay/gibt-es-nicht.md"')),
      M8_REGEL)

gegenprobe("8a", "Ein Eintrag, der auf eine vorhandene Datei zeigt, bleibt still - und die Beispiele mit Ausfuellschlitz im Pfad ebenso",
           lambda r: _8_setze(r, (P8_BEISPIEL_ARCH, P8_VORHANDEN)), M8_PFAD)


# --- 66: das verirrte Steuerzeichen (D-217) --------------------------------------
#
# Die Sonden setzen das Zeichen in den beiden Bauformen, in denen es gemessen wurde:
# am Ende eines Traegers und am Zeilenende einer Tabellenzeile - dort sassen dreizehn
# der vierzehn Fundstellen. Sie schreiben mit `schreib`, also ohne Umsetzung der
# Zeilenenden; eine Sonde, die ihren eigenen Gegenstand normalisiert, misst nichts.
#
# 🔴 DIE ZWEITE GEGENPROBE IST DIE WICHTIGERE. Sie stellt einen Traeger durchgehend
# auf LF - also auf die ANDERE Zeilenende-Form - und belegt damit, dass Pruefung 66
# das verirrte ZEICHEN misst und nicht die Form. Ohne sie waere aus der Meldung nicht
# zu erkennen, ob hier eine Zeichenpruefung steht oder eine Formatvorschrift, die
# niemand entschieden hat (K-81).
M66 = "verirrte(s) Steuerzeichen"
P66_TRAEGER = ".koolie/core/OWNERS.md".replace("/", os.sep)
P66_ANTRAG = (".koolie/core/governance/change-requests/"
              "CR-2026-027-zeichenlimit-einstufung.md").replace("/", os.sep)


def _66_am_ende(root: str) -> None:
    """Ein einzelnes CR am Ende eines Kerntraegers - die stillste Fundstelle."""
    pfad = P(root, P66_TRAEGER)
    schreib(pfad, lies(pfad) + chr(13))


def _66_in_der_tabelle(root: str) -> None:
    """Dieselbe Bauform wie vierzehn der sechzehn gemessenen Fundstellen.

    Ein CR unmittelbar vor dem Zeilenumbruch einer Tabellenzeile. Es rendert nicht,
    es faellt in keinem Diff auf - und es hat elf Antraege dieses Verzeichnisses
    von der Normalisierung ausgenommen.
    """
    pfad = P(root, P66_ANTRAG)
    text = lies(pfad)
    marke = "| Umsetzung |"
    if marke not in text:
        raise Praeparationsfehler(
            "CR-2026-027 fuehrt die Zeile '%s' nicht mehr - die Sonde zu 66 haette "
            "keinen Anker" % marke)
    schreib(pfad, text.replace(marke, chr(13) + marke, 1))


def _66_auf_lf(root: str) -> None:
    """Gegenprobe: ein Traeger durchgehend auf LF - die andere Form, kein Befund."""
    pfad = P(root, P66_TRAEGER)
    schreib(pfad, lies(pfad).replace(chr(13) + chr(10), chr(10)))


sonde("66a", "Ein einzelnes CR am Ende eines Kerntraegers - unsichtbar im Text und genug, damit git die Zeilenenden nicht mehr normalisiert",
      _66_am_ende, M66)

sonde("66b", "Dasselbe Zeichen am Zeilenende einer Tabellenzeile - die Bauform von vierzehn der sechzehn gemessenen Fundstellen",
      _66_in_der_tabelle, M66)

gegenprobe("66a", "Das unveraenderte Repositorium bleibt unbeanstandet - seit dieser Berichtigung traegt kein Traeger mehr ein verirrtes CR",
           None, M66)

gegenprobe("66b", "Ein Traeger durchgehend auf LF wird NICHT gemeldet: gemessen wird das verirrte Zeichen, nicht die Zeilenende-Form",
           _66_auf_lf, M66)


# --- 67: ENTFALLEN mit 1.4.1 (D-350) ----------------------------------------------
#
# Pruefung 67 hielt die Titelzeile der Uebergabe gegen VERSION. Seit 1.4.1 ist die
# Uebergabe nicht mehr versioniert, und mit der Pruefung entfallen ihre vier Sonden
# und zwei Gegenproben. Eine Sonde auf einen Traeger, den eine frische Auscheckung
# nicht fuehrt, belegte nur, was auf einem Arbeitsplatz liegt.


# --- 68: das Praefix, das mehr sperrt als sein Befehl (D-219) ----------------------
#
# Die dritte Sonde ist die Ankersonde: Ohne exec-Regel haette Pruefung 68 nichts zu
# rechnen und bestuende leise. Die zweite Gegenprobe belegt den ZUSCHNITT - eine
# Regel, deren Praefix ihrem Befehl gleicht, erfasst nicht ueber und wird nicht
# gemeldet, auch ohne Begruendungsfeld. Ohne dieses Paar waere nicht zu unterscheiden,
# ob die Pruefung die Uebererfassung sucht oder jede Regel ohne Feld.
M68 = "mehr, als ihr Befehl nennt"
M68_ANKER = "keine einzige exec-Regel gefunden"
P68_PERM = ".koolie/core/framework/runtime/permissions.json".replace("/", os.sep)


def _68_laden(root: str) -> dict:
    return json.loads(lies(P(root, P68_PERM)))


def _68_schreiben(root: str, daten: dict) -> None:
    schreib(P(root, P68_PERM), json.dumps(daten, indent=2, ensure_ascii=False))


def _68_feld_entfernen(root: str) -> None:
    """Der gemessene Fall: die Begruendung an der git-branch-Regel faellt weg."""
    daten = _68_laden(root)
    getroffen = 0
    for regel in daten.get("deny", []):
        if regel.get("tool") == "exec" and "_uebererfasst" in regel:
            del regel["_uebererfasst"]
            getroffen += 1
    if getroffen == 0:
        raise Praeparationsfehler(
            "keine exec-Regel mit Begruendungsfeld - die Sonde zu 68 haette keinen "
            "Anker; entweder erfasst keine Regel mehr ueber, dann gehoert die Sonde "
            "weg, oder das Feld heisst anders")
    _68_schreiben(root, daten)


def _68_neue_regel(root: str) -> None:
    """Eine ZWEITE Stelle: eine neue Regel mit kuerzerem Praefix und ohne Feld.

    Sie belegt, dass die Pruefung an der Bauform haengt und nicht an einer Zeile.
    """
    daten = _68_laden(root)
    daten.setdefault("deny", []).append(
        {"tool": "exec", "command": "sondenbefehl --loeschen",
         "prefix": "sondenbefehl"})
    _68_schreiben(root, daten)


def _68_ohne_exec(root: str) -> None:
    """Ankersonde: keine exec-Regel mehr - der verlorene Gegenstand."""
    daten = _68_laden(root)
    for korb in ("deny", "ask", "allow"):
        daten[korb] = [r for r in daten.get(korb, []) if r.get("tool") != "exec"]
    _68_schreiben(root, daten)


def _68_praefix_gleich_befehl(root: str) -> None:
    """Gegenprobe: eine Regel OHNE Uebererfassung und ohne Feld - kein Befund.

    🔴 WER EINEN ERLAUBTEN FALL HERSTELLT, MUSS IHN VOLLSTAENDIG HERSTELLEN
    (0.66.0). Eine neue Regel in der Kernquelle macht die lokale Testinstallation
    unvollstaendig, und der Abgleich der Berechtigungsdatei meldet die fehlende
    Regel - einen Fehler, den diese Gegenprobe nicht gemeint hat. Der gerenderte
    Eintrag gehoert deshalb mit.
    """
    daten = _68_laden(root)
    daten.setdefault("deny", []).append(
        {"tool": "exec", "command": "sondenbefehl"})
    _68_schreiben(root, daten)
    inst = P(root, ".devin", "config.json")
    if os.path.isfile(inst):
        konf = json.loads(lies(inst))
        konf["permissions"]["deny"].append("Exec(sondenbefehl)")
        schreib(inst, json.dumps(konf, indent=2, ensure_ascii=False))


sonde("68a", "Eine exec-Regel sperrt ueber ihr Praefix mehr, als ihr Befehl nennt, und sagt es nicht - der Eintrag, der 25 Abweisungen erzeugt hat",
      _68_feld_entfernen, M68)

sonde("68b", "Dieselbe Bauform an einer ZWEITEN Stelle: eine neu eingefuegte Regel mit kuerzerem Praefix wird ebenso gemeldet",
      _68_neue_regel, M68)

sonde("68c", "Ohne exec-Regel meldet Pruefung 68 den verlorenen Gegenstand, statt leise zu bestehen",
      _68_ohne_exec, M68_ANKER)

gegenprobe("68a", "Das unveraenderte Repositorium bleibt unbeanstandet - alle vier uebererfassenden Regeln tragen ihre Begruendung",
           None, M68)


# --- 69: der Messapparat schreibt nicht in das Repositorium (D-222) ----------------
#
# Zwei Formen desselben Gegenstands: die Belegdatei (69a) und das Verzeichnis, das
# `lauf.py` selbst anlegen wuerde (69b). Die dritte ist die Ankersonde - eine leere
# Erhebungsablage haette nichts zu zaehlen und bestuende leise. Die Gegenprobe
# belegt den ZUSCHNITT: Eine weitere .py-Datei ist ein WERKZEUG und wird NICHT
# gemeldet; ohne sie waere nicht zu unterscheiden, ob die Pruefung die Art der
# Datei prueft oder jede Neuerung.
M69 = "Erhebungsablage des Kerns"
M69_ANKER = "kein einziges Werkzeug gefunden"
P69_ORDNER = ".koolie/core/tests/erhebungen".replace("/", os.sep)


def _69_beleg(root: str) -> None:
    """Der gemessene Fall: ein Ergebnis-JSON eines Laufs landet im Repositorium."""
    schreib(P(root, P69_ORDNER, "sk010n02-ergebnis.json"), '{"is_error": false}')


def _69_verzeichnis(root: str) -> None:
    """Die zweite Form: das Belegverzeichnis, das lauf.py selbst anlegen wuerde."""
    os.makedirs(P(root, P69_ORDNER, "belege"), exist_ok=True)
    schreib(P(root, P69_ORDNER, "belege", "sk010n02-antwort.md"), "Antwort")


def _69_leer(root: str) -> None:
    """Ankersonde: keine Werkzeuge mehr - der verlorene Gegenstand."""
    ordner = P(root, P69_ORDNER)
    if not os.path.isdir(ordner):
        raise Praeparationsfehler(
            "die Erhebungsablage fehlt - die Sonde zu 69 haette keinen Anker")
    for name in os.listdir(ordner):
        ziel = os.path.join(ordner, name)
        if os.path.isfile(ziel):
            os.remove(ziel)
        else:
            shutil.rmtree(ziel)


def _69_weiteres_werkzeug(root: str) -> None:
    """Gegenprobe: ein weiteres Skript ist ein Werkzeug und kein Befund."""
    schreib(P(root, P69_ORDNER, "sondenwerkzeug.py"), "# nichts" + chr(10))


sonde("69a", "Ein Ergebnis-JSON in der Erhebungsablage des Kerns wird gemeldet - der Fall, den die fuenf relativen Pfade nach dem Umzug erzeugt haetten",
      _69_beleg, M69)

sonde("69b", "Dieselbe Bauform als VERZEICHNIS: das Belegverzeichnis, das lauf.py selbst anlegen wuerde, wird ebenso gemeldet",
      _69_verzeichnis, M69)

sonde("69c", "Ohne ein einziges Werkzeug meldet Pruefung 69 den verlorenen Gegenstand, statt leise zu bestehen",
      _69_leer, M69_ANKER)


def _69_beleg_im_paket(root: str) -> None:
    """Seit 1.19.0 (D-473): ein Beleg IM zugelassenen Werkzeugpaket ist derselbe Befund."""
    paket = P(root, P69_ORDNER, "apparat")
    if not os.path.isdir(paket):
        raise Praeparationsfehler("das Paket apparat/ fehlt - die Sonde 69d haette keinen Gegenstand")
    schreib(os.path.join(paket, "reihe-sonde.json"), '{"name": "sonde"}')


def _69_modul_im_paket(root: str) -> None:
    """Gegenprobe: ein weiteres Modul im Paket ist ein Werkzeug."""
    schreib(P(root, P69_ORDNER, "apparat", "sondenmodul.py"), "# nichts" + chr(10))


sonde("69d", "Eine Reihe als JSON im Werkzeugpaket apparat/ wird gemeldet - das Paket ist fuer Quelltext zugelassen, nicht fuer Aufzeichnung",
      _69_beleg_im_paket, M69)

gegenprobe("69b", "Ein weiteres Modul im Werkzeugpaket apparat/ bleibt unbeanstandet",
           _69_modul_im_paket, M69)

gegenprobe("69a", "Ein weiteres .py-Skript ist ein Werkzeug und wird NICHT gemeldet - die Pruefung haengt an der Art der Datei, nicht an ihrer Neuheit",
           _69_weiteres_werkzeug, M69)

gegenprobe("68b", "Eine Regel, deren Praefix ihrem Befehl gleicht, wird NICHT gemeldet - auch ohne Begruendungsfeld; gemessen wird die Uebererfassung, nicht das fehlende Feld",
           _68_praefix_gleich_befehl, M68)


# --- 70: jedes Werkzeug des Kerns nennt nur Namen, die es gibt (D-229) -------------
#
# Drei Formen desselben Gegenstands: der gemessene NameError (70a), die Quelle, die
# der Interpreter gar nicht erst uebersetzt (70b), und die Ankersonde - ein
# Messapparat ohne ein einziges Werkzeug haette nichts zu pruefen und bestuende leise
# (70c). 70a setzt den Defekt WOERTLICH so, wie er am 2026-09-21 gefunden wurde: den
# Ablageort NEBEN dem Skript, den D-222 mit dem Umzug entfernt hat.
#
# ZWEI GEGENPROBEN, UND SIE BELEGEN DEN ZUSCHNITT. Die Pruefung haengt an der
# BINDUNG, nicht an der Schreibweise: Ein Werkzeug, das freie Variablen einer
# umschliessenden Funktion liest, eine Komprehension fuehrt, `__file__` nennt und
# einen Namen erst im `except`-Zweig bindet, ist gebunden und wird nicht gemeldet
# (70a). Und ein Name, der GEBUNDEN und falsch belegt ist, laeuft durch - das ist die
# angesagte Grenze, nicht ein Loch (70b).
M70 = "NameError, der auf seinen Lauf wartet"
M70_SYNTAX = "laedt nicht"
M70_ANKER = "kein einziges Werkzeug geprueft"
P70_STAND = ".koolie/core/tests/erhebungen/stand-b4.py".replace("/", os.sep)
P70_APPARAT = ".koolie/core/tests/erhebungen".replace("/", os.sep)


def _70_verschwundener_name(root: str) -> None:
    """Der gemessene Fall: der Ablageort neben dem Skript, nach dem Umzug (D-222)."""
    ersetze(P(root, P70_STAND),
            ("PROMPTS = ablage.prompts(anlegen=False)",
             'PROMPTS = os.path.join(os.path.dirname(S), "prompts")'))


def _70_uebersetzt_nicht(root: str) -> None:
    """Die zweite Form: ein Werkzeug, das der Interpreter nicht uebersetzt."""
    schreib(P(root, P70_APPARAT, "sondenwerkzeug.py"),
            "# -*- coding: utf-8 -*-" + chr(10) + "def offen(:" + chr(10))


def _70_apparat_ohne_werkzeug(root: str) -> None:
    """Ankersonde: die Ablage steht, kein Werkzeug mehr darin."""
    ordner = P(root, P70_APPARAT)
    if not os.path.isdir(ordner):
        raise Praeparationsfehler(
            "die Erhebungsablage fehlt - die Sonde zu 70 haette keinen Anker")
    geloescht = 0
    for name in os.listdir(ordner):
        ziel = os.path.join(ordner, name)
        if os.path.isfile(ziel) and name.endswith(".py"):
            os.remove(ziel)
            geloescht += 1
    if geloescht == 0:
        raise Praeparationsfehler(
            "in der Erhebungsablage lag kein einziges .py - der Anker traegt nicht")


def _70_gebundene_namen(root: str) -> None:
    """Gegenprobe: jede Bindungsform, die es gibt - und keine davon ist ein Befund."""
    schreib(P(root, P70_APPARAT, "sondenwerkzeug.py"), chr(10).join([
        "# -*- coding: utf-8 -*-",
        "import os",
        "",
        "WURZEL = os.path.dirname(os.path.abspath(__file__))",
        "",
        "",
        "def aussen(grenze):",
        "    rest = [x for x in os.listdir(WURZEL) if x > grenze]",
        "",
        "    def innen():",
        "        return grenze, rest",
        "",
        "    try:",
        "        zahl = int(grenze)",
        "    except ValueError as fehler:",
        "        zahl = len(str(fehler))",
        "    with open(os.path.join(WURZEL, grenze)) as quelle:",
        "        inhalt = quelle.read()",
        "    return innen(), zahl, inhalt",
        "",
        "",
        "class Traeger(object):",
        "    feld = WURZEL",
        "",
        "    def hol(self):",
        "        return self.feld",
        "",
    ]))


def _70_gebunden_und_falsch(root: str) -> None:
    """Gegenprobe: der Name IST gebunden - der Wert taugt nicht. Die angesagte Grenze."""
    schreib(P(root, P70_APPARAT, "sondenwerkzeug.py"), chr(10).join([
        "# -*- coding: utf-8 -*-",
        "import os",
        "",
        "S = None",
        "PROMPTS = os.path.join(os.path.dirname(S), 'prompts')",
        "",
    ]))


sonde("70a", "Der gemessene Fall: der Ablageort neben dem Skript ist mit D-222 verschwunden, seine zwei Lesestellen nicht - stand-b4.py war seit 0.79.0 tot",
      _70_verschwundener_name, M70)

sonde("70b", "Dieselbe Bauform eine Stufe frueher: ein Werkzeug des Kerns, das der Interpreter nicht einmal uebersetzt, wird gemeldet",
      _70_uebersetzt_nicht, M70_SYNTAX)

sonde("70c", "Ohne ein einziges Werkzeug im Messapparat meldet Pruefung 70 den verlorenen Gegenstand, statt leise zu bestehen",
      _70_apparat_ohne_werkzeug, M70_ANKER)

gegenprobe("70a", "Freie Variable, Komprehension, except-Name, with-Ziel, Klassenfeld und __file__ sind gebunden und werden NICHT gemeldet - die Pruefung haengt an der Bindung",
           _70_gebundene_namen, M70)

gegenprobe("70b", "Ein gebundener Name mit untauglichem Wert laeuft durch - das ist die angesagte Grenze der Pruefung und kein Loch",
           _70_gebunden_und_falsch, M70)


# --- 71: kein Traeger des Kerns nennt einen Arbeitsplatz (D-231) -------------------
#
# Drei Formen desselben Gegenstands: der gemessene Fall in einem WERKZEUG (71a), die
# gleiche Bauform in einer CHECKLISTE - also ausserhalb der .py-Welt, weil die
# Pruefung nicht an der Dateiart haengt (71b) -, und die Ankersonde: ein Muster, das
# seinen Gegenstand nicht mehr trifft, bestuende leise (71c).
#
# DREI GEGENPROBEN, UND SIE BELEGEN DEN ZUSCHNITT. Ein Platzhalter nennt niemanden
# (71a). Die Marke `SYNTHETISCH` in derselben Zeile laeuft durch - dieselbe Bauform
# wie das Begruendungsfeld von Pruefung 68 (71b). Und eine AUFZEICHNUNG DES BESTANDS
# bleibt unbeanstandet: Ein Protokoll haelt fest, WO gemessen wurde, und wer es
# umschreibt, hat keines mehr (71c, D-141). Seit 1.20.3 ist das eine geschlossene Liste
# und keine Gattung mehr (D-508, `K-85`): Eine NEUE Aufzeichnung mit Kontonamen wird
# gemeldet (71d).
M71 = "nennt ein Benutzerprofil"
M71_ANKER = "das eigene Muster trifft"
P71_WERKZEUG = ".koolie/core/tests/erhebungen/stand-b4.py".replace("/", os.sep)
P71_CHECKLISTE = ".koolie/core/checklists/11-framework-release.md".replace("/", os.sep)
P71_PROTOKOLL = (".koolie/core/tests/protocols/"
                 "2026-09-21-wiederaufnahme-nachlauf-b4.md").replace("/", os.sep)
P71_BESTAND = (".koolie/core/tests/protocols/"
               "2026-09-19-testblaetter-buendel-1.md").replace("/", os.sep)
P71_VALIDATOR = ".koolie/core/tests/scripts/pruefungen/werkzeuge.py".replace("/", os.sep)
P71_PFAD = "C:" + chr(92) + "Users" + chr(92) + "sondenkonto" + chr(92) + "devpacks"


def _71_werkzeug(root: str) -> None:
    """Der gemessene Fall: ein Werkzeug des Kerns fuehrt einen Arbeitsplatzpfad."""
    ersetze(P(root, P71_WERKZEUG),
            ('BAEUME = r"C:' + chr(92) + 'lw-b4"',
             'BAEUME = r"' + P71_PFAD + chr(92) + 'lw-b4"'))


def _71_checkliste(root: str) -> None:
    """Die zweite Form, ausserhalb der .py-Welt: derselbe Pfad in einer Checkliste."""
    zeile_nach(P(root, P71_CHECKLISTE), "## Zweck",
               "" + chr(10) + "Arbeitsstand liegt unter `" + P71_PFAD + "`.")


def _71_muster_verlieren(root: str) -> None:
    """Ankersonde: das Muster trifft seinen eigenen Gegenstand nicht mehr."""
    ersetze(P(root, P71_VALIDATOR),
            ('r"(?:[A-Za-z]:[' + chr(92) + chr(92) + '/]{1,2}Users|/home|/Users)'
             '[' + chr(92) + chr(92) + '/]{1,2}([A-Za-z0-9._-]+)"',
             'r"trifft-nichts-mehr([A-Za-z0-9._-]+)"'))


def _71_platzhalter(root: str) -> None:
    """Gegenprobe: ein Platzhalter nennt niemanden."""
    zeile_nach(P(root, P71_CHECKLISTE), "## Zweck",
               "" + chr(10) + "Arbeitsstand liegt unter `C:" + chr(92)
               + "Users" + chr(92) + "%USERNAME%" + chr(92) + "devpacks`.")


def _71_marke(root: str) -> None:
    """Gegenprobe: die Marke in derselben Zeile laeuft durch (wie bei Pruefung 68)."""
    zeile_nach(P(root, P71_CHECKLISTE), "## Zweck",
               "" + chr(10) + "Beispielpfad `" + P71_PFAD + "` - SYNTHETISCH.")


def _71_aufzeichnung(root: str) -> None:
    """Gegenprobe: eine Aufzeichnung des Bestands bleibt unbeanstandet (D-141, D-508)."""
    zeile_nach(P(root, P71_BESTAND), "## 1. Der Meßaufbau",
               "" + chr(10) + "Gemessen wurde ausserhalb von `" + P71_PFAD + "`.")


def _71_neue_aufzeichnung(root: str) -> None:
    """Sonde: eine Aufzeichnung ausserhalb des Bestands wird geprueft (D-508, K-85)."""
    zeile_nach(P(root, P71_PROTOKOLL), "## 1. Die Lage vor dem Durchgang",
               "" + chr(10) + "Gemessen wurde ausserhalb von `" + P71_PFAD + "`.")


sonde("71a", "Ein Werkzeug des Kerns fuehrt einen Arbeitsplatzpfad im Quelltext - der gemessene Fall, den D-222 mit dem Apparat hereingetragen hat",
      _71_werkzeug, M71)

sonde("71b", "Dieselbe Bauform ausserhalb der Skripte: derselbe Pfad in einer Checkliste wird ebenso gemeldet",
      _71_checkliste, M71)

sonde("71c", "Trifft das eigene Muster seinen Gegenstand nicht mehr, meldet Pruefung 71 das, statt leise zu bestehen",
      _71_muster_verlieren, M71_ANKER)

sonde("71d", "Eine neue Aufzeichnung mit Kontonamen wird gemeldet - ausgenommen ist seit 1.20.3 nur der Bestand der zehn, nicht die Gattung (D-508)",
      _71_neue_aufzeichnung, M71)

gegenprobe("71a", "Ein Platzhalter als Kontosegment nennt niemanden und wird NICHT gemeldet - die Pruefung haengt am Namen, nicht an der Pfadform",
           _71_platzhalter, M71)

gegenprobe("71b", "Die Marke SYNTHETISCH in derselben Zeile laeuft durch - dieselbe Bauform wie das Begruendungsfeld von Pruefung 68",
           _71_marke, M71)

gegenprobe("71c", "Eine Aufzeichnung des Bestands bleibt unbeanstandet - ein Protokoll haelt fest, wo gemessen wurde, und wer es umschreibt, hat keines mehr (D-141)",
           _71_aufzeichnung, M71)


# --- Pruefung 72: Ein aktiviertes Pack steht auch im Berechtigungskorb ------------
#
# WARUM DIESE EINHEIT EINE INSTALLATION BAUT statt den Repositoriumsbaum zu praeparieren:
# Ihr Gegenstand IST die Installation. Im Quellrepositorium gibt es keine Skillablage
# eines Client Packs, und die Pruefung schwiege dort zu Recht - eine Sonde auf einer
# Kopie des Repositoriums haette nichts zu treffen.
#
# DREI SONDEN, UND SIE BELEGEN BEIDE RICHTUNGEN UND DIE ANKERFRAGE. Der gemessene Fall
# ist 72a: ein Pack WORTGETREU nach `framework/role-packs/README.md` aktiviert - Skill
# kopiert -, und der Korb weiss nichts davon. 72b ist die Gegenrichtung: ein Eintrag
# ohne Skill ist eine Zusage ohne Gegenstand (D-81). 72c fragt das Manifest: Ein
# FEHLENDES Feld `permission_tools.skill` ist ein Befund - der Unterschied zwischen
# "nicht abgebildet" und "gibt es nicht" gehoert deklariert (D-155).
#
# ZWEI GEGENPROBEN, UND DIE ZWEITE IST DIE WICHTIGERE. 72a belegt, dass eine
# ausgelieferte Installation durchlaeuft - ohne sie meldete die Sonde nur, dass
# irgendetwas meldet. 72b belegt den ZUSCHNITT: Dieselbe Aktivierung in einer
# `devin-desktop`-Installation bleibt unbeanstandet, weil das Manifest dort
# `permission_tools.skill` als LEER deklariert (erhoben am 2026-09-14, D-89: Der
# Skillaufruf ist dort ein Werkzeugaufruf, aber es ist keine Schreibweise bekannt, mit
# der eine Regel ihn beim Namen nennt). Ohne sie waere das Schweigen der Pruefung bei
# diesem Pack nicht von einer stillen Null zu unterscheiden.
M72 = "wird aber von keinem Eintrag der Berechtigungsdatei genannt"
M72_RUECK = "nennt keinen Skill in"
M72_FELD = "Feld permission_tools.skill fehlt"
P72_PACKSKILL = (".koolie/core/framework/role-packs/requirements-engineering/"
                 "skills/role-re-ticket").replace("/", os.sep)


def _72_pack_aktivieren(root: str, pack_skills: str) -> str:
    """Aktiviert das Role Pack wortgetreu nach README Punkt 4: Skill kopieren."""
    quelle = os.path.join(root, P72_PACKSKILL)
    name = os.path.basename(quelle)
    shutil.copytree(quelle, os.path.join(root, *pack_skills.split("/"), name))
    return name


def sonden_pack_im_korb() -> None:
    """Wirkungsnachweis fuer Pruefung 72 (CR-2026-114, D-238)."""
    for pack, skills, meldet in (("claude-code", ".claude/skills", True),
                                 ("devin-desktop", ".devin/skills", False)):
        root = installation(pack)
        try:
            if pack == "claude-code":
                # --- Gegenprobe 72a: die ausgelieferte Installation ------------
                melde("GEGENPROBE", "72a", M72 not in validator_ausgabe(root),
                      "Die ausgelieferte Installation deckt sich - zwoelf Skills, "
                      "zwoelf Eintraege, keine Meldung")

            name = _72_pack_aktivieren(root, skills)
            ausgabe = validator_ausgabe(root)
            getroffen = M72 in ausgabe and name in ausgabe
            if meldet:
                melde("SONDE", "72a", getroffen,
                      "Ein aktiviertes Role Pack ohne Korbeintrag wird gemeldet - der "
                      "gemessene Fall aus dem Vorbedingungsdurchgang von Buendel 5")
                if not getroffen:
                    notiz("        Ausgabe:", " | ".join(ausgabe.splitlines()[:6]))
            else:
                melde("GEGENPROBE", "72b", not getroffen,
                      "Dieselbe Aktivierung bei einem Pack mit leer DEKLARIERTEM "
                      "permission_tools.skill bleibt unbeanstandet (D-89)")

            if pack != "claude-code":
                continue

            # --- Sonde 72b: die Gegenrichtung -------------------------------
            # Der Eintrag bleibt, sein Skill geht - eine Freigabe ohne Gegenstand.
            shutil.rmtree(os.path.join(root, *skills.split("/"), name))
            shutil.rmtree(os.path.join(root, *skills.split("/"), "fw-plan"))
            ausgabe = validator_ausgabe(root)
            melde("SONDE", "72b", M72_RUECK in ausgabe and "fw-plan" in ausgabe,
                  "Ein Korbeintrag ohne Skill in der Ablage wird gemeldet - eine "
                  "Freigabe fuer einen Skill, den es nicht gibt (D-81)")

            # --- Sonde 72c: das Manifest schweigt statt zu deklarieren -------
            _manifest_aendern(root, "claude-code",
                              lambda m: m["permission_tools"].pop("skill", None))
            melde("SONDE", "72c", M72_FELD in validator_ausgabe(root),
                  "Ein FEHLENDES Feld permission_tools.skill wird gemeldet - eine "
                  "leere Liste ist deklariert, ein fehlendes Feld ist geraten (D-155)")
        finally:
            aufraeumen(os.path.dirname(root))


buendel(sonden_pack_im_korb,
        "Ein aktiviertes Pack steht auch im Berechtigungskorb - in beide Richtungen, "
        "und nur bei einem Client, dessen Manifest eine Schreibweise deklariert")




# --- Pruefung 73: Jede [DOK]-Matrixzeile nennt ihre Quelle -------------------------
#
# VIER SONDEN, UND SIE BELEGEN DIE VIER WEGE, AUF DENEN EINE ZUORDNUNG VERSCHWINDET.
# 73a ist der gemessene Ausgangsfall: eine Zeile, deren Belegkopf die Kennung nicht
# nennt - am 2026-09-18 traf das auf 29 von 43 Zeilen zu. 73b ist der Fall, den keine
# Zaehlung ohne Verweisaufloesung sieht: Beim Pack devin-desktop haengen B4, B5, B6 und
# B8 an B3, eine davon ueber zwei Glieder - nimmt man B3 die Kennung, verlieren FUENF
# Zeilen ihren Beleg, und die Meldung nennt die Kette. 73c und 73d sind die beiden
# Richtungen der deklarierten Luecke: eine neue, die nicht in P73_OFFEN steht, und eine
# deklarierte, die aus der Zeile verschwunden ist. Die zweite ist der Fall "eine
# Ausnahme ohne Gegenstand" (0.57.1) - sie sieht wie Sorgfalt aus und ist tot.
#
# DREI GEGENPROBEN, UND DIE ZWEITE IST DIE WICHTIGERE. 73a belegt, dass der
# ausgelieferte Bestand durchlaeuft - ohne sie meldete die Sonde nur, dass irgendetwas
# meldet. 73b belegt DIE KOPFREGEL: Eine Nennung der Marke HINTER dem Belegkopf bleibt
# unbeanstandet. Ohne sie waere die Pruefung nicht von einer Textsuche zu
# unterscheiden, und Zeile R5 des Packs claude-code - "ein Dokumentenabgleich belegt
# [DOK], nicht [TECHNISCH]" - fiele als Befund an. 73c belegt den Zuschnitt zur
# Vorlage: clients/_template/ fuehrt <TBD> in jeder Belegzelle und wird nicht gemessen.
M73 = "nennt im Belegkopf keine Quellenkennung"
M73_KETTE = "ueber den Verweis"
M73_UNDEKLARIERT = "steht aber nicht in P73_OFFEN"
M73_TOT = "als ausgesprochene Luecke, die Zeile sagt es aber nicht"
P73_CC = ".koolie/core/clients/claude-code/CLIENT_PACK.md".replace("/", os.sep)
P73_DD = ".koolie/core/clients/devin-desktop/CLIENT_PACK.md".replace("/", os.sep)
P73_VORLAGE = ".koolie/core/clients/_template/CLIENT_PACK.md".replace("/", os.sep)


def _73_kennung_nehmen(root: str) -> None:
    """Sonde: Zeile B1 des Packs claude-code verliert ihre Kennung."""
    ersetze(P(root, P73_CC),
            ("| `[DOK]` **`QC-5`** (Zuordnung `K-62`) |", "| `[DOK]` |"))


def _73_verweisziel_nehmen(root: str) -> None:
    """Sonde: B3 verliert die Kennung - vier weitere Zeilen verweisen darauf."""
    # Der Anker ist so kurz wie moeglich: Die Zeile B3 ist mit 0.86.0 neu geschrieben
    # worden (Muster-Semantik, D-277), und der laengere Suchtext von 0.85.0 traf nicht
    # mehr. Eine Sonde, deren Suchtext an der Prosa haengt, faellt bei jedem Messwert.
    ersetze(P(root, P73_DD),
            ("Mechanismus `[DOK]` **`QD-11`** (Zuordnung `K-62`)",
             "Mechanismus `[DOK]` (ohne Quelle)"))


def _73_luecke_erfinden(root: str) -> None:
    """Sonde: eine zweite ausgesprochene Luecke, die niemand deklariert hat."""
    ersetze(P(root, P73_DD),
            ("| `[DOK]` **`QD-12`** (Zuordnung `K-62`) |",
             "| `[DOK]` - QUELLE NICHT ZUGEORDNET (synthetisch) |"))


def _73_luecke_schliessen(root: str) -> None:
    """Sonde: die deklarierte Luecke verschwindet aus der Zeile, P73_OFFEN bleibt."""
    ersetze(P(root, P73_CC),
            ("🔴 **QUELLE NICHT ZUGEORDNET** (`K-62`, 2026-09-22)",
             "**`QC-2`** (synthetisch)"))


def _73_nennung_hinter_dem_kopf(root: str) -> None:
    """Gegenprobe: die Marke HINTER dem Belegkopf ist eine Nennung, kein Beleg."""
    ersetze(P(root, P73_CC),
            ("| `[DOK]` **`QC-5`** (Zuordnung `K-62`) |",
             "| `[DOK]` **`QC-5`** (Zuordnung `K-62`). Zur Einordnung: Ein "
             "Dokumentenabgleich belegt `[DOK]` und nie `[TECHNISCH]` (D-12) |"))


def _73_vorlage_leeren(root: str) -> None:
    """Gegenprobe: die Vorlage fuehrt <TBD> und wird nicht gemessen."""
    ersetze(P(root, P73_VORLAGE),
            ("| R1 | Die Wurzel-Anweisungsdatei wird zu Beginn jeder Sitzung "
             "ungefragt geladen | `.koolie/core/framework/runtime/root-instruction.md` "
             "| `<TBD>` | `<TBD>` | `<TBD>` |",
             "| R1 | Die Wurzel-Anweisungsdatei wird zu Beginn jeder Sitzung "
             "ungefragt geladen | `.koolie/core/framework/runtime/root-instruction.md` "
             "| `<TBD>` | `<TBD>` | `[DOK]` |"))


sonde("73a", "Eine [DOK]-Zeile ohne Quellenkennung im Belegkopf wird gemeldet - der "
             "gemessene Ausgangsfall: 29 von 43 Zeilen am 2026-09-18",
      _73_kennung_nehmen, M73)

sonde("73b", "Nimmt das Ziel eines Verweisbelegs seine Kennung, verlieren die "
             "verweisenden Zeilen sie mit - und die Meldung nennt die Kette",
      _73_verweisziel_nehmen, M73_KETTE)

sonde("73c", "Eine ausgesprochene Luecke, die nicht in P73_OFFEN steht, wird "
             "gemeldet - sonst waere die Marke eine Hintertuer",
      _73_luecke_erfinden, M73_UNDEKLARIERT)

sonde("73d", "Eine deklarierte Luecke, die aus der Zeile verschwunden ist, wird "
             "gemeldet - eine Ausnahme ohne Gegenstand ist tot (0.57.1)",
      _73_luecke_schliessen, M73_TOT)

gegenprobe("73a", "Der ausgelieferte Bestand laeuft durch - 46 Matrixzeilen, eine "
                  "deklarierte Luecke, keine Meldung",
           None, M73)

gegenprobe("73b", "Eine Nennung der Marke HINTER dem Belegkopf bleibt unbeanstandet - "
                  "die Kopfregel, ohne die jede Erlaeuterung ein Befund waere",
           _73_nennung_hinter_dem_kopf, M73)

gegenprobe("73c", "Die Vorlage clients/_template/ fuehrt <TBD> und wird nicht "
                  "gemessen - ein Pack ohne Client hat keine Quellenliste",
           _73_vorlage_leeren, M73)


# --- Pruefung 74: Eine Matrixzeile steht in ihrer Tabelle --------------------------
#
# ZWEI SONDEN UND ZWEI GEGENPROBEN. 74a ist der gemessene Fall, wortgetreu: die
# Leerzeile zwischen M5 und M6 des Packs devin-desktop, die dort seit 0.26.0 stand und
# zwei Matrixzeilen zu Fliesstext gemacht hat - im Pack wie im Hauptdokument. 74b ist
# dieselbe Bauform mit Fremdtext statt Leerzeile: Ein Absatz mitten in der Tabelle
# bricht sie ebenso, und er sieht harmloser aus.
#
# DIE ZWEITE GEGENPROBE IST DIE WICHTIGERE, und sie schuetzt den ZUSCHNITT. Abschnitt 5
# des Packs claude-code fuehrt eine Tabelle "Bekannte Abweichungen im Verhalten", und
# ihre erste Zeile beginnt mit "| B6 |" - dieselbe Gestalt wie eine Matrixzeile, in
# einer anderen Tabelle und in einem anderen Abschnitt. Wer nur nach dem Muster sucht,
# meldet sie mit. Die Pruefung liest deshalb nur unterhalb von "## 2.", und diese
# Gegenprobe belegt es an einer Zeile, die dort WIRKLICH steht.
M74 = "sieht aus wie eine Matrixzeile und steht in keiner Tabelle"
P74_DD = P73_DD
P74_CC = P73_CC


def _74_leerzeile_setzen(root: str) -> None:
    """Sonde: der gemessene Fall - eine Leerzeile vor M6, wie sie bis 0.84.0 stand."""
    zeile_nach(P(root, P74_DD), "| M5 | Eigener Nur-Lese-Modus", "")


def _74_fremdtext_setzen(root: str) -> None:
    """Sonde: ein Absatz mitten in der Tabelle bricht sie ebenso."""
    zeile_nach(P(root, P74_DD), "| M5 | Eigener Nur-Lese-Modus",
               "" + chr(10) + "Anmerkung zur Modusreihe - SYNTHETISCH." + chr(10))


def _74_abweichungstabelle_brechen(root: str) -> None:
    """Gegenprobe: dieselbe Gestalt in Abschnitt 5 wird NICHT gemessen."""
    zeile_nach(P(root, P74_CC), "## 5. Bekannte Abweichungen im Verhalten",
               "" + chr(10) + "| B6 | synthetische Zeile ohne Tabelle | - |")


sonde("74a", "Eine Leerzeile vor einer Matrixzeile wird gemeldet - der gemessene "
             "Fall, der seit 0.26.0 zwei Zeilen zu Fliesstext gemacht hat",
      _74_leerzeile_setzen, M74)

sonde("74b", "Ein Absatz mitten in der Tabelle bricht sie ebenso und wird gemeldet",
      _74_fremdtext_setzen, M74)

gegenprobe("74a", "Der ausgelieferte Bestand laeuft durch - beide Packs, jede "
                  "Matrixzeile in ihrer Tabelle",
           None, M74)

gegenprobe("74b", "Dieselbe Gestalt in Abschnitt 5 bleibt unbeanstandet - die "
                  "Pruefung liest unterhalb von '## 2.', nicht nach dem Muster",
           _74_abweichungstabelle_brechen, M74)


# --- Pruefung 75: Kein Restbestand des alten Namens (CR-2026-122, D-271) ------------
#
# EIN BUENDEL, WEIL DIE PRUEFUNG EIN REPOSITORIUM BRAUCHT. Sie liest `git ls-files`,
# und kopie() schliesst `.git` ausdruecklich aus - der Sondenbaum ist keins. Ohne
# `git init` haette Pruefung 75 in JEDER Sonde ihren dritten Ausgang genommen ("nicht
# messbar") und dabei ausgesehen wie eine, die nichts gefunden hat. Das ist derselbe
# Griff wie bei Gegenstand 2 der Pruefung 45, aus demselben Grund.
#
# VIER EINHEITEN, UND SIE MESSEN VIER VERSCHIEDENE DINGE:
#   75a (Gegenprobe) - der ausgelieferte Bestand laeuft durch. Sie belegt zugleich,
#                      dass die Pruefung ueberhaupt GELAUFEN ist: Ohne die Bedingung
#                      auf die Unmessbarkeitsmeldung bestuende sie auch ohne git.
#   75a (Sonde)      - der alte Name in einem verfolgten Traeger ausserhalb der
#                      Ausnahmemenge wird gemeldet.
#   75b (Gegenprobe) - derselbe Text in einem datierten Protokoll bleibt unbeanstandet.
#                      Das ist der ZUSCHNITT: Die Chronik beschreibt einen vergangenen
#                      Zustand (D-273), und ein Pfad, den es nicht mehr gibt, ist dort
#                      richtig.
#   75b (Sonde)      - die zweite Richtung: Eine Ausnahme, aus der die Fundstelle
#                      verschwunden ist, wird gemeldet. Ohne sie waere P75_AUSNAHMEN ein
#                      Sammelbecken, das nur waechst - eine Ausnahme, die nichts mehr
#                      ausnimmt, sieht wie Sorgfalt aus (0.57.1).
#   75c (Sonde)      - der verlorene Anker: Trifft das eigene Muster den alten Namen
#                      nicht mehr, meldet die Pruefung das, statt leise zu bestehen.
#
# DIE SONDEN BRINGEN IHREN GEGENSTAND SELBST MIT. 75a und 75b schreiben den alten Namen
# in den Baum, statt einen vorhandenen vorauszusetzen - die Abhilfe aus 0.86.0
# Abschnitt 2a. Genau daran sind dort sieben Sonden gefallen, und hier ist der Fall
# schaerfer: Der Gegenstand dieser Pruefung ist der Name, den dieses Release ENTFERNT.
M75_REST = "nennt den alten Namen noch"
M75_LEER = "nimmt nichts mehr aus und gehört entfernt"
M75_ANKER = "das eigene Muster findet den alten Namen nicht mehr"
M75_UNMESSBAR = "ist an diesem Ort nicht prüfbar"

P75_OPFER = ".koolie/core/OWNERS.md"
P75_CHRONIKOPFER = ".koolie/core/CHANGELOG.md"
P75_AUSNAHMEOPFER = ".koolie/core/clientmap.py"
P75_VALIDATOR = ".koolie/core/tests/scripts/pruefungen/dokumente.py".replace("/", os.sep)

_ALT = "leitwerk" + "-core"          # nicht als ein Literal: Pruefung 75 liest sich selbst


def sonden_altname() -> None:
    """Wirkungsnachweis zu Pruefung 75 an einem echten Repositorium."""
    root = kopie()
    try:
        if unterprozess(["git", "init", "-q", root]).returncode != 0:
            melde("BUENDEL", "-", False, "sonden_altname  [git nicht erreichbar]")
            notiz("        Ohne git liest Pruefung 75 keinen Bestand; sie nimmt dann "
                  "ihren dritten Ausgang und ist nicht messbar.")
            return
        unterprozess(["git", "-C", root, "add", "-A"])

        # --- Gegenprobe 75a: der ausgelieferte Bestand laeuft durch -----------------
        aus = validator_ausgabe(root)
        ok = (M75_REST not in aus and M75_LEER not in aus
              and M75_UNMESSBAR not in aus and M75_ANKER not in aus)
        melde("GEGENPROBE", "75a", ok,
              "Der ausgelieferte Bestand laeuft durch - P75_AUSNAHMEN deckt sich in "
              "BEIDE Richtungen mit dem Bestand, und die Pruefung ist dabei "
              "nachweislich gelaufen")
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "75" in z or "Namen" in z)[:400])

        # --- Sonde 75a: der alte Name in einem verfolgten Traeger -------------------
        pfad = P(root, *P75_OPFER.split("/"))
        schreib(pfad, lies(pfad) + "\r\n<!-- SYNTHETISCH: " + _ALT + " -->\r\n")
        unterprozess(["git", "-C", root, "add", "-A"])
        aus = validator_ausgabe(root)
        getroffen = M75_REST in aus and P75_OPFER in aus
        melde("SONDE", "75a", getroffen,
              "Der alte Name in einem verfolgten Traeger ausserhalb der Ausnahmemenge "
              "wird gemeldet - mit Traeger und Zahl")
        if not getroffen:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        schreib(pfad, lies(pfad).replace(
            "\r\n<!-- SYNTHETISCH: " + _ALT + " -->\r\n", ""))

        # --- Gegenprobe 75b: derselbe Text in der Chronik ---------------------------
        pfad = P(root, *P75_CHRONIKOPFER.split("/"))
        schreib(pfad, lies(pfad) + "\r\n<!-- SYNTHETISCH: " + _ALT + " -->\r\n")
        unterprozess(["git", "-C", root, "add", "-A"])
        aus = validator_ausgabe(root)
        ok = M75_REST not in aus
        melde("GEGENPROBE", "75b", ok,
              "Derselbe Text in einem Chroniktraeger bleibt unbeanstandet - die Chronik "
              "beschreibt einen vergangenen Zustand und wandert nicht mit (D-273)")
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        schreib(pfad, lies(pfad).replace(
            "\r\n<!-- SYNTHETISCH: " + _ALT + " -->\r\n", ""))

        # --- Sonde 75b: die zweite Richtung - eine leer gewordene Ausnahme ----------
        pfad = P(root, *P75_AUSNAHMEOPFER.split("/"))
        text = lies(pfad)
        treffer = text.lower().count("leitwerk")
        if treffer != 1:
            melde("SONDE", "75b", False,
                  "Die zweite Richtung von Pruefung 75  [Praeparation gebrochen]")
            notiz("        %s nennt den alten Namen %dmal, erwartet genau einmal - "
                  "die Sonde hat ihren Gegenstand verloren."
                  % (P75_AUSNAHMEOPFER, treffer))
        else:
            schreib(pfad, re.sub("(?i)leitwerk", "koolie", text))
            unterprozess(["git", "-C", root, "add", "-A"])
            aus = validator_ausgabe(root)
            getroffen = M75_LEER in aus and P75_AUSNAHMEOPFER in aus
            melde("SONDE", "75b", getroffen,
                  "Eine Ausnahme, aus der die Fundstelle verschwunden ist, wird "
                  "gemeldet - ohne diese Richtung waechst P75_AUSNAHMEN nur")
            if not getroffen:
                notiz("        Ausgabe:", " | ".join(
                    z for z in aus.splitlines() if "FEHLER" in z)[:400])
            schreib(pfad, text)
            unterprozess(["git", "-C", root, "add", "-A"])

        # --- Sonde 75c: der verlorene Anker -----------------------------------------
        pfad = P(root, P75_VALIDATOR)
        text = lies(pfad)
        alt = 'P75_ALTNAME = re.compile(r"(?i)leitwerk")'
        if text.count(alt) != 1:
            melde("SONDE", "75c", False,
                  "Der verlorene Anker von Pruefung 75  [Praeparation gebrochen]")
            notiz("        Suchtext %r steht %dmal im Validator." % (alt, text.count(alt)))
        else:
            schreib(pfad, text.replace(
                alt, 'P75_ALTNAME = re.compile(r"(?i)diesenamengibtesnicht")'))
            aus = validator_ausgabe(root)
            getroffen = M75_ANKER in aus
            melde("SONDE", "75c", getroffen,
                  "Trifft das eigene Muster den alten Namen nicht mehr, meldet "
                  "Pruefung 75 das - statt jede Umbenennung als vollstaendig zu melden")
            if not getroffen:
                notiz("        Ausgabe:", " | ".join(
                    z for z in aus.splitlines() if "FEHLER" in z)[:400])
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_altname,
        "Pruefung 75 an einem echten Repositorium: der Bestand, ein Restbestand, die "
        "Chronik als Zuschnitt, die leer gewordene Ausnahme und der verlorene Anker")


# --- Pruefung 76: Die Lage des Kerns steht an vier Stellen (CR-2026-122, D-299) -----
#
# DREI SONDEN UND EINE GEGENPROBE, und die dritte Sonde ist die wichtigste: Sie legt
# die BASENAME-BINDUNG WIEDER AN, die dieses Release entfernt hat. Ohne sie waere der
# erste Gegenstand - "alle vier tragen denselben Wert" - erfuellbar, indem alle vier
# denselben Fehler machen. Genau das war der Zustand bis 0.87.0, und der Validator hat
# ihn nicht gemeldet, weil er ihn teilte.
#
# WARUM NICHT AN validate-framework.py PRAEPARIERT WIRD: Dessen KERN traegt die Lage,
# mit der der Validator seinen eigenen Baum findet. Wer ihn verstellt, misst nicht
# Pruefung 76, sondern einen Validator ohne Gegenstand.
M76_UNGLEICH = "nicht überall gleich"
M76_BASENAME = "bindet <CORE_DIR> über os.path.basename()"
M76_ANKER = "führt keine Angabe der Kernlage mehr"

P76_HOOK = ".koolie/core/tests/scripts/hook-check-secrets.py".replace("/", os.sep)
P76_CLIENTMAP = ".koolie/core/clientmap.py".replace("/", os.sep)
P76_ABLAGE = ".koolie/core/tests/erhebungen/ablage.py".replace("/", os.sep)


def _76_lage_verstellen(root: str) -> None:
    """Sonde: der Schutz-Hook traegt eine andere Lage als die uebrigen drei."""
    pfad = P(root, P76_HOOK)
    schreib(pfad, ersetzt(lies(pfad),
                          ('CORE_REL = ".koolie/core"',
                           'CORE_REL = ".koolie/anderswo"'),
                          quelle=os.path.basename(pfad)))


def _76_basename_wieder(root: str) -> None:
    """Sonde: die Bindung ueber basename, die bis 0.87.0 an vier Stellen stand."""
    pfad = P(root, P76_CLIENTMAP)
    schreib(pfad, ersetzt(lies(pfad),
                          ('def core_dir_name(man: dict) -> str:',
                           '_sonde = {}                      # SYNTHETISCH\r\n'
                           '_sonde["<CORE_DIR>"] = os.path.basename("x")\r\n\r\n\r\n'
                           'def core_dir_name(man: dict) -> str:'),
                          quelle=os.path.basename(pfad)))


def _76_anker_entfernen(root: str) -> None:
    """Sonde: eine der vier Stellen fuehrt keine Lageangabe mehr."""
    pfad = P(root, P76_ABLAGE)
    schreib(pfad, ersetzt(lies(pfad),
                          ('CORE_REL = ".koolie/core"', '_lage = ".koolie/core"'),
                          ("CORE_REL.count", "_lage.count"),
                          quelle=os.path.basename(pfad)))


sonde("76a", "Traegt eine der vier Stellen eine andere Lage, wird es gemeldet - eine "
             "Installation laege sonst je nach aufrufendem Werkzeug anderswo",
      _76_lage_verstellen, M76_UNGLEICH)

sonde("76b", "Die Bindung ueber os.path.basename wird gemeldet - sie stand bis 0.87.0 "
             "an vier Stellen und haette den Umzug nicht ueberlebt",
      _76_basename_wieder, M76_BASENAME)

sonde("76c", "Verliert eine der vier Stellen ihre Lageangabe, meldet Pruefung 76 den "
             "verlorenen Anker, statt drei von vier stillschweigend zu vergleichen",
      _76_anker_entfernen, M76_ANKER)

gegenprobe("76a", "Der ausgelieferte Bestand laeuft durch - vier Stellen, ein Wert, "
                  "keine basename-Bindung",
           None, M76_UNGLEICH)


# --- Pruefung 77: Der Stand des Hauptdokuments (CR-2026-124, D-312) ----------------
#
# DREI SONDEN UND EINE GEGENPROBE. Die zweite ist die, die man weglassen wuerde: Sie
# setzt in dieselbe Zeile zwei VERSCHIEDENE Staende. Ohne sie waere der Vergleich mit
# VERSION erfuellbar, indem die Zeile zwei Werte nennt und einer davon passt - und
# welcher gemeint ist, stuende nirgends.
#
# WARUM AN 00-kopf.md UND NICHT AN VERSION PRAEPARIERT WIRD: VERSION traegt der
# Validator selbst gegen die Artefaktversionen (Pruefung 13), bis 1.4.0 auch gegen
# die Uebergabe (Pruefung 67). Wer dort verstellt, loest mehrere Meldungen aus und
# misst keine davon.
M77_STAND = "die Kopfzeile nennt den Stand"
M77_UNEINIG = "und das Framework-Release"
M77_ANKER = "keine Zeile der Form"

P77_KOPF = ".koolie/core/build/doc/00-kopf.md".replace("/", os.sep)


def _77_stand_verstellen(root: str) -> None:
    """Sonde: das Dokument bleibt auf einem aelteren Stand stehen."""
    pfad = P(root, P77_KOPF)
    schreib(pfad, ersetzt(lies(pfad),
                          ("| Dokumentversion | ", "| Dokumentversion | 0.9.0 (entspricht "
                           "Framework-Release 0.9.0) |\r\n| Dokumentversion frueher | "),
                          quelle=os.path.basename(pfad)))


def _77_zeile_uneinig(root: str) -> None:
    """Sonde: die Zeile nennt zwei verschiedene Staende."""
    pfad = P(root, P77_KOPF)
    text = lies(pfad)
    anfang = text.index("| Dokumentversion | ")
    ende = text.index("|", text.index("(entspricht Framework-Release", anfang)) + 1
    schreib(pfad, text[:anfang]
            + "| Dokumentversion | 0.89.0 (entspricht Framework-Release 0.88.1) |"
            + text[ende:])


def _77_anker_entfernen(root: str) -> None:
    """Sonde: die Kopfzeile des Dokuments ist weg."""
    pfad = P(root, P77_KOPF)
    schreib(pfad, ersetzt(lies(pfad),
                          ("| Dokumentversion | ", "| Fassung | "),
                          quelle=os.path.basename(pfad)))


sonde("77a", "Bleibt das Hauptdokument auf einem aelteren Stand stehen, wird es "
             "gemeldet - genau so ist es zweiundvierzig Releases zurueckgefallen",
      _77_stand_verstellen, M77_STAND)

sonde("77b", "Nennt dieselbe Zeile zwei verschiedene Staende, wird es gemeldet - sonst "
             "genuegte es, wenn einer der beiden Werte passt",
      _77_zeile_uneinig, M77_UNEINIG)

sonde("77c", "Verliert der Kopf seine Versionszeile, meldet Pruefung 77 den verlorenen "
             "Anker, statt still zu bestehen",
      _77_anker_entfernen, M77_ANKER)

gegenprobe("77a", "Der ausgelieferte Bestand laeuft durch - Dokumentversion, genanntes "
                  "Release und VERSION tragen denselben Wert",
           None, M77_STAND)


# --- Pruefung 78: Die zaehlbaren Aussagen des Hauptdokuments (CR-2026-125, D-315) --
#
# EIN BUENDEL, WEIL DIE PRUEFUNG EIN REPOSITORIUM BRAUCHT. Sie zaehlt die versionierten
# Dateien des Kerns ueber `git ls-files`, und kopie() schliesst `.git` ausdruecklich aus.
# Ohne `git init` naehme sie in JEDER Sonde ihren dritten Ausgang ("nicht messbar") und
# saehe dabei aus wie eine, die nichts gefunden hat - derselbe Griff wie bei Pruefung 75
# und 45, aus demselben Grund.
#
# 🔴 KEINE SONDE VERANKERT EINE ZAHL WOERTLICH, und das ist die Lehre von 0.89.0: Dort
# sind zwei Sonden gebrochen, weil sie einen Wert als Suchtext hielten, den ein Release
# berichtigt hat. Die Sonden hier LESEN die Zahl aus dem Traeger und verstellen sie
# relativ. Eine Sonde, die eine Zahl mitpflegen muss, faellt bei der naechsten Aenderung
# aus - und zwar als scheinbarer Befund.
#
# VIER EINHEITEN, UND SIE MESSEN VIER VERSCHIEDENE DINGE:
#   78a (Gegenprobe) - der ausgelieferte Bestand laeuft durch, und die Pruefung ist dabei
#                      nachweislich gelaufen (keine Unmessbarkeitsmeldung).
#   78a (Sonde)      - eine verstellte Zahl der Pruefungen wird gemeldet.
#   78b (Sonde)      - eine verstellte Zahl der versionierten Dateien wird gemeldet. Ohne
#                      sie genuegte es, EINE der drei Zahlen zu treffen.
#   78c (Sonde)      - der verlorene Anker: Faellt der Satz weg, meldet die Pruefung das,
#                      statt leise zu bestehen (D-23).
#   78d, 78e         - ENTFALLEN mit 1.4.1 (D-350): Sie maßen die Abnahmezeile der
#                      Uebergabe, und die ist nicht mehr versioniert.
M78_WERTE = "nennt nicht die gezählten Werte"
M78_ANKER = "steht nicht genau einmal"
M78_UNMESSBAR = "kein Git-Bestand lesbar"

P78_OPFER = ".koolie/core/build/doc/26-qs-test.md"
P78_ANKER = "Der Validator führt **"


def _78_zahl_verstellen(text: str, muster: str) -> str:
    """Die erste Zahl hinter `muster` um eins erhoehen - ohne sie woertlich zu kennen."""
    treffer = re.search(re.escape(muster) + r"(\d+)", text)
    if not treffer:
        raise Praeparationsfehler(
            "26-qs-test.md: %r mit folgender Zahl nicht gefunden - die Sonde zu "
            "Pruefung 78 haette nichts zu verstellen" % muster)
    neu = str(int(treffer.group(1)) + 1)
    return text[:treffer.start(1)] + neu + text[treffer.end(1):]


def sonden_dokumentzahlen() -> None:
    """Wirkungsnachweis zu Pruefung 78 an einem echten Repositorium."""
    root = kopie()
    try:
        if unterprozess(["git", "init", "-q", root]).returncode != 0:
            melde("BUENDEL", "-", False, "sonden_dokumentzahlen  [git nicht erreichbar]")
            notiz("        Ohne git zaehlt Pruefung 78 keine versionierten Dateien; sie "
                  "nimmt dann ihren dritten Ausgang und ist nicht messbar.")
            return
        unterprozess(["git", "-C", root, "add", "-A"])
        pfad = P(root, *P78_OPFER.split("/"))
        urtext = lies(pfad)

        # --- Gegenprobe 78a: der ausgelieferte Bestand laeuft durch ------------------
        aus = validator_ausgabe(root)
        ok = (M78_WERTE not in aus and M78_ANKER not in aus
              and M78_UNMESSBAR not in aus)
        melde("GEGENPROBE", "78a", ok,
              "Der ausgelieferte Bestand laeuft durch - die drei Zahlen des Satzes "
              "decken sich mit dem Bestand, und die Pruefung ist dabei nachweislich "
              "gelaufen")
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "78" in z or "Prüfapparat" in z)[:400])

        # --- Sonde 78a: die Zahl der Pruefungen verstellt ----------------------------
        schreib(pfad, _78_zahl_verstellen(urtext, P78_ANKER))
        unterprozess(["git", "-C", root, "add", "-A"])
        aus = validator_ausgabe(root)
        melde("SONDE", "78a", M78_WERTE in aus,
              "Eine verstellte Zahl der Pruefungen wird gemeldet - genau diese Zahl "
              "stand ein Release zu lang auf ihrem alten Wert")
        if M78_WERTE not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])

        # --- Sonde 78b: die Zahl der versionierten Dateien verstellt -----------------
        schreib(pfad, _78_zahl_verstellen(urtext, "Prüfungen** über "))
        unterprozess(["git", "-C", root, "add", "-A"])
        aus = validator_ausgabe(root)
        melde("SONDE", "78b", M78_WERTE in aus,
              "Eine verstellte Zahl der versionierten Dateien wird ebenfalls gemeldet - "
              "sonst genuegte es, eine der drei Zahlen zu treffen")
        if M78_WERTE not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])

        # --- Sonde 78c: der verlorene Anker ------------------------------------------
        schreib(pfad, urtext.replace(P78_ANKER, "Der Validator kennt **", 1))
        unterprozess(["git", "-C", root, "add", "-A"])
        aus = validator_ausgabe(root)
        melde("SONDE", "78c", M78_ANKER in aus,
              "Faellt der Satz ueber den Pruefapparat weg, meldet Pruefung 78 den "
              "verlorenen Anker, statt still zu bestehen")
        if M78_ANKER not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        schreib(pfad, urtext)

    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_dokumentzahlen,
        "Pruefung 78 haelt die drei Gegenwartszahlen des Hauptdokuments gegen den "
        "gezaehlten Bestand, an einem echten Repositorium")


# --- Pruefung 79: Die Lizenz an zwei Stellen (CR-2026-126, D-317) ------------------
#
# DREI SONDEN UND EINE GEGENPROBE. Die dritte ist die, die man weglassen wuerde: Sie
# ersetzt BEIDE Dateien durch denselben Nicht-Lizenztext. Ohne sie belegte die Pruefung
# nur, dass zwei Dateien gleich sind - und das sind zwei leere auch.
M79_UNGLEICH = "trägt nicht denselben Inhalt wie"
M79_FEHLT = "Die Lizenz MUSS an beiden Stellen liegen"
M79_MARKE = "trägt nicht die GNU General Public License"

P79_KERNDATEI = ".koolie/core/LICENSE"
P79_WURZELDATEI = "LICENSE"


def _79_auseinander(root: str) -> None:
    """Sonde: die beiden Lizenzdateien laufen auseinander."""
    pfad = P(root, *P79_KERNDATEI.split("/"))
    schreib(pfad, lies(pfad) + "\n<!-- SYNTHETISCH: Zusatz nur in der Kernfassung -->\n")


def _79_kernfassung_entfernen(root: str) -> None:
    """Sonde: die mitwandernde Fassung fehlt - genau der Fall von §4 GPL-3.0."""
    os.remove(P(root, *P79_KERNDATEI.split("/")))


def _79_keine_lizenz(root: str) -> None:
    """Sonde: beide Dateien gleich, aber keine Lizenz - die Gleichheit allein traegt nicht."""
    ersatz = "SYNTHETISCH: hier stand einmal ein Lizenztext.\n"
    for rel in (P79_KERNDATEI, P79_WURZELDATEI):
        schreib(P(root, *rel.split("/")), ersatz)


sonde("79a", "Laufen die beiden Lizenzdateien auseinander, wird es gemeldet - welche "
             "gilt, stuende sonst nirgends",
      _79_auseinander, M79_UNGLEICH)

sonde("79b", "Fehlt die mitwandernde Fassung im Kern, wird es gemeldet - ein Werk ohne "
             "seine Lizenz weiterzugeben ist unzulaessig",
      _79_kernfassung_entfernen, M79_FEHLT)

sonde("79c", "Zwei gleiche Dateien ohne Lizenztext werden gemeldet - Gleichheit allein "
             "erfuellen auch zwei leere Dateien",
      _79_keine_lizenz, M79_MARKE)

gegenprobe("79a", "Der ausgelieferte Bestand laeuft durch - beide Stellen, ein Inhalt, "
                  "und dieser Inhalt ist die GPL-3.0",
           None, M79_UNGLEICH)


# --- Pruefung 80: Die Gegenzeichnung der Abnahmeprotokolle (CR-2026-127, D-319) ----
#
# DREI SONDEN UND ZWEI GEGENPROBEN. Die zweite Gegenprobe ist die, die man weglassen
# wuerde, und sie traegt die ganze Entscheidung: Ein offenes <TBD> im
# Gegenzeichnungsabschnitt eines ARBEITSPROTOKOLLS muss unbeanstandet bleiben. Ohne sie
# waere der Zuschnitt aus D-319 eine Behauptung im Kommentar statt eine gemessene
# Eigenschaft - und die Pruefung verlangte still die Gegenzeichnung von 125 Protokollen
# statt von zehn.
#
# 🔴 JEDE SONDE PRUEFT IHRE EIGENE FUNDSTELLE, nicht irgendeine Meldung. Der
# ausgelieferte Bestand traegt sieben frisch gezeichnete Abnahmeprotokolle; eine Sonde,
# die nur auf den Meldungstext prueft, bestuende auch ohne Praeparation. Der Erwartungs-
# text nennt deshalb den DATEINAMEN des Opfers - dieselbe Bauform wie bei Sonde 75a.
M80_FEHLT = "2026-09-10-FW-KO-02.md: kein Abschnitt"
M80_TBD = "2026-09-10-FW-KO-02.md: der Abschnitt `Gegenzeichnung` trägt noch ein offenes"
M80_ANKER = "kein einziges Abnahmeprotokoll des Testkatalogs gefunden"

P80_OPFER = ".koolie/core/tests/protocols/2026-09-10-FW-KO-02.md"
P80_ARBEITSPROTOKOLL = ".koolie/core/tests/protocols/2026-09-13-B06-gegenpruefung.md"


def _80_abschnitt_entfernen(root: str) -> None:
    """Sonde: einem Abnahmeprotokoll fehlt die Gegenzeichnung."""
    pfad = P(root, *P80_OPFER.split("/"))
    text = lies(pfad)
    anfang = text.find("## Gegenzeichnung")
    if anfang < 0:
        raise Praeparationsfehler(
            "2026-09-10-FW-KO-02.md: kein Abschnitt 'Gegenzeichnung' gefunden - die "
            "Sonde zu Pruefung 80 haette nichts zu entfernen")
    schreib(pfad, text[:anfang].rstrip("\r\n") + "\r\n")


def _80_tbd_zurueck(root: str) -> None:
    """Sonde: der Abschnitt ist da und traegt wieder ein offenes <TBD>."""
    pfad = P(root, *P80_OPFER.split("/"))
    text = lies(pfad)
    anfang = text.find("## Gegenzeichnung")
    if anfang < 0:
        raise Praeparationsfehler(
            "2026-09-10-FW-KO-02.md: kein Abschnitt 'Gegenzeichnung' gefunden")
    schreib(pfad, text + "\r\n| Zweitpruefung | `<TBD: Rolle>` | | |\r\n")


def _80_anker_entfernen(root: str) -> None:
    """Sonde: kein Traeger passt mehr auf das Namensmuster der Abnahmeprotokolle."""
    ablage = P(root, *".koolie/core/tests/protocols".split("/"))
    umbenannt = 0
    for name in sorted(os.listdir(ablage)):
        if "-FW-" in name and name.endswith(".md"):
            os.rename(os.path.join(ablage, name),
                      os.path.join(ablage, name.replace("-FW-", "-fw", 1)))
            umbenannt += 1
    if not umbenannt:
        raise Praeparationsfehler(
            "tests/protocols/: kein Traeger mit '-FW-' im Namen - die Sonde zum "
            "verlorenen Anker haette nichts umzubenennen")


def _80_arbeitsprotokoll_offen(root: str) -> None:
    """Gegenprobe: ein ARBEITSPROTOKOLL mit offenem Abschnitt - der Zuschnitt."""
    pfad = P(root, *P80_ARBEITSPROTOKOLL.split("/"))
    text = lies(pfad)
    if "<TBD" not in text:
        raise Praeparationsfehler(
            "2026-09-13-B06-gegenpruefung.md: traegt kein offenes <TBD> mehr - die "
            "Gegenprobe zum Zuschnitt von Pruefung 80 haette keinen Gegenstand")
    schreib(pfad, text + "\r\n| Zweitpruefung | `<TBD: Rolle>` | | |\r\n")


sonde("80a", "Fehlt einem Abnahmeprotokoll die Gegenzeichnung, wird es mit Dateinamen "
             "gemeldet - fuenf von zehn hatten den Abschnitt nie",
      _80_abschnitt_entfernen, M80_FEHLT)

sonde("80b", "Ein offenes <TBD> im Abschnitt wird gemeldet - eine Gegenzeichnung ist "
             "eine Handlung und kein Feld, das ein Werkzeug fuellt",
      _80_tbd_zurueck, M80_TBD)

sonde("80c", "Passt kein Traeger mehr auf das Namensmuster, meldet Pruefung 80 den "
             "verlorenen Anker, statt still ueber null Protokolle zu bestehen",
      _80_anker_entfernen, M80_ANKER)

gegenprobe("80a", "Der ausgelieferte Bestand laeuft durch - alle zehn Abnahmeprotokolle "
                  "tragen ihren Abschnitt ohne offenes <TBD>",
           None, M80_FEHLT)

gegenprobe("80b", "Ein offenes <TBD> in einem ARBEITSPROTOKOLL bleibt unbeanstandet - "
                  "das ist der Zuschnitt aus D-319 und nicht bloss seine Behauptung",
           _80_arbeitsprotokoll_offen, "B06-gegenpruefung.md: der Abschnitt")


# --- Selbstprobe: der Beschreibungssatz je Einheit (CR-2026-068, D-95) ------------
#
# Bis 0.45.0 trug jede Einzelsonde einen erklaerenden Text und jedes Buendel keinen. Wer
# den Lauf las, sah eine Folge von Meldungen und nicht, was sie zusammen belegen sollten.
# Seit 0.46.0 ist der Satz Pflicht - und eine Pflicht ohne Nachzaehlen ist eine Zusage
# ohne Mechanismus, also genau der wiederkehrende Befundtyp dieses Projekts.
#
# GRENZE: Sie zaehlt WORTE, nicht Sinn. Ein Satz aus achtzehn Fuellwoertern besteht sie.
# Die untere Grenze faengt die Kennung, die sich als Satz ausgibt ("Pack ohne
# Auskunftsabschnitt"), die obere den Absatz, der sich in eine Zeile verirrt hat.
# Dazwischen entscheidet der Mensch, und das ist Absicht.
def selbstprobe_beschreibungen() -> None:
    """Jede angemeldete Einheit traegt ihren Satz in der vorgeschriebenen Laenge."""
    abweichend = [e for e in EINHEITEN if not SATZ_MIN <= worte(e.satz) <= SATZ_MAX]
    melde("SELBSTPROBE", "B1", not abweichend,
          "Alle %d Einheiten tragen einen Beschreibungssatz von %d bis %d Worten"
          % (len(EINHEITEN), SATZ_MIN, SATZ_MAX))
    for e in abweichend:
        notiz("        %s %s: %d Worte - %s"
              % (e.art, e.kennung, worte(e.satz), e.satz))


buendel(selbstprobe_beschreibungen,
        "Zaehlt die Worte jedes Beschreibungssatzes dieses Laufs - eine Kennung ohne "
        "Satz und ein Absatz in einer Zeile fallen beide auf")

"""Sonden zu den Pruefungen 46 bis 55 und zur Platzhalterbindung; Selbstprobe des
Baumdurchlaufs.

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul
liest nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import glob
import json
import os
import re

from .apparat import (
    aufraeumen, buendel, ersetze, ersetzt, frei, gegenprobe, installation, lies, melde,
    notiz, P, Praeparationsfehler, QUELLE, schreib, sonde, strict_ausgabe,
    validator_ausgabe, zeile_nach)


# --- Pruefung 46: der 1.0.0-Stand (CR-2026-070, D-98, D-99) --------------------------
#
# Sechs Sonden, je eine auf einen eigenen Gegenstand, und zwei davon fuer die zwei
# Richtungen: Ein Kriterium, das ZURUECKFAELLT, und ein Fortschritt, der NICHT
# NACHGEZOGEN ist, sind beide ein Fehler. Ohne die zweite Richtung waere der Zaehler ein
# Fortschrittsbalken - er hielte still, solange sich nichts verschlechtert, und der
# Stand stuende wieder daneben.
#
# Drei Gegenproben, und sie treffen genau die Stellen, an denen die alten Zaehlregeln zu
# breit oder zu schmal waren: ein Klaerungspunkt mit demselben Statuswort (die alte
# Regel zaehlte fuenf davon mit) und ein Marker in einem datierten Protokoll (der
# Zaehlbereich schliesst ihn aus, und das muss er auch tun).
M46_ANKER = "die Standzeile steht 0x statt genau einmal"
M46_K1 = "Kriterium 1 von D-11"
M46_K2 = "Kriterium 2 von D-11"
M46_K3 = "Kriterium 3 von D-11"
M46_K4 = "Kriterium 4 von D-11"
M46_NICHT_NACHGEZOGEN = "der Fortschritt ist nicht nachgezogen"
M46_RUECKFALL = ("entweder ist der Bestand zur\u00fcckgefallen, oder der "
                 "Z\u00e4hlbereich sieht erstmals")
M46_AUSSERHALB = "ausserhalb des Zaehlbereichs von Kriterium 1"
P46_ROADMAP = ".koolie/core/docs/ROADMAP.md".replace("/", os.sep)
P46_STAND = "Gezählt von Prüfung 46: Kriterium 1 = "
# Der Marker in seiner clientneutralen Form - zusammengesetzt, weil eine woertliche
# Nennung in diesem Skript selbst eine Fundstelle waere und Kriterium 1 um eins hoebe.
# Dieses Skript liegt im Zaehlbereich.
P46_MARKER = "<VERIFY AGAINST CURRENT " + "CLIENT" + " DOCUMENTATION>"


def _46_zahl_verstellen(root: str, welche: int, neu: str) -> None:
    """Eine der vier Zahlen der Standzeile auf einen anderen Wert setzen."""
    pfad = P(root, P46_ROADMAP)
    zeilen = lies(pfad).split("\r\n")
    treffer = [i for i, z in enumerate(zeilen) if P46_STAND in z]
    if len(treffer) != 1:
        raise Praeparationsfehler(
            "ROADMAP.md: Standzeile steht %dx, erwartet genau einmal" % len(treffer))
    teile = re.split(r"(= \d+)", zeilen[treffer[0]])
    stellen = [i for i, s in enumerate(teile) if s.startswith("= ")]
    if len(stellen) != 4:
        raise Praeparationsfehler(
            "ROADMAP.md: Standzeile fuehrt %d Zahlen, erwartet vier" % len(stellen))
    teile[stellen[welche]] = "= " + neu
    zeilen[treffer[0]] = "".join(teile)
    schreib(pfad, "\r\n".join(zeilen))


def _46_standzeile_weg(root: str) -> None:
    """Die Standzeile ganz entfernen - der verlorene Anker."""
    pfad = P(root, P46_ROADMAP)
    zeilen = lies(pfad).split("\r\n")
    behalten = [z for z in zeilen if P46_STAND not in z]
    if len(behalten) == len(zeilen):
        raise Praeparationsfehler("ROADMAP.md: keine Standzeile gefunden")
    schreib(pfad, "\r\n".join(behalten))


def _46_marker_dazu(root: str) -> None:
    """Eine neue unverifizierte Aussage im Kern - Kriterium 1 steigt um eins."""
    pfad = P(root, ".koolie/core/framework/core/03-security.md".replace("/", os.sep))
    schreib(pfad, lies(pfad) + "\r\n> Sondenzeile: Wirkung der Sandbox je "
                               "Betriebssystem " + P46_MARKER + ".\r\n")


def _46_testblatt_dazu(root: str) -> None:
    """Ein Testblatt an einem Ort, den eine Ablagenliste uebersaehe.

    Genau der Befund, der Pruefung 46 ausgeloest hat: Die alte Regel las "die dezentralen
    TESTS.md je Skill" als zwoelf Dateien, und die dreizehnte lag unter role-packs/.
    Diese Sonde legt eine vierzehnte unter tech-packs/ an - eine Ablagenliste, die die
    dreizehnte uebersah, uebersaehe sie ebenso.
    """
    ordner = P(root, ".koolie/core/framework/tech-packs/_template".replace("/", os.sep))
    schreib(os.path.join(ordner, "TESTS.md"),
            "# Sondentestblatt\r\n\r\n"
            "| Test-ID | Ziel | Prüfmethode | Ergebnisstatus |\r\n"
            "|---|---|---|---|\r\n"
            "| SO-001 | Sondenfall | sitzung | offen |\r\n")


def _46_steckbrief_dazu(root: str) -> None:
    """Ein neues Modul auf `entwurf` - Kriterium 3 steigt um eins."""
    schreib(P(root, ".koolie/core/prompts/13-sondenprompt.md".replace("/", os.sep)),
            "# Sondenprompt\r\n\r\n"
            "| Attribut | Wert |\r\n|---|---|\r\n"
            "| ID | `FW-PR-13` |\r\n| Version | `0.1.0` |\r\n"
            "| Status | `entwurf` |\r\n| Owner (Rolle) | `<FRAMEWORK_OWNER>` |\r\n")


# Synthetische Kennung der Gegenprobe 46b. Sie stand bis 0.49.0 auf K-36 - und 0.50.0
# hat K-36 und K-37 wirklich vergeben (CR-2026-072). Der Kennungswaechter frei() hat
# die Kollision beim Sondenlauf gemeldet, statt sie als Befund am Repositorium
# erscheinen zu lassen; das ist die Lehre von G-18 (2026-09-13) zum zweiten Mal, und
# diesmal hat sie funktioniert. Die 99 folgt der Konvention von G-99 und UEB-99: hoch
# genug, dass keine echte Vergabe sie erreicht.
P46_KLAERUNG = "K-99"
P46_BESTAETIGT = "| entschieden (`CR-2026-071`); "
P46_VORSCHLAG = "| entschieden (Vorschlag); "


def _46_record_zurueckgefallen(root: str) -> None:
    """D-10 auf `entschieden (Vorschlag)` zuruecksetzen - Kriterium 4 STEIGT auf eins.

    Bis 0.48.0 hob diese Sonde D-10 AUS dem Vorschlagsstatus HERAUS und belegte damit
    die Richtung "Fortschritt nicht nachgezogen". Mit 0.49.0 sind alle neun Records
    bestaetigt (CR-2026-071, D-100) - die Hebung hat keinen Gegenstand mehr, und der
    alte Suchtext haette zwar noch getroffen (er steht jetzt im Verlaufszusatz der
    Zelle), aber an einer Stelle, die Pruefung 46 gar nicht liest. Eine Sonde, die
    etwas veraendert, ohne den Gegenstand zu treffen, ist der schlechteste Zustand:
    Der Baumvergleich meldet kein "[nichts praepariert]", und der Fehlschlag sieht aus
    wie ein Befund an der Pruefung.

    Die Sonde stellt ihren Defekt deshalb seither HER statt ihn zu entfernen - wie 38a
    und 38b seit 0.38.0 - und deckt damit die Richtung, die vorher KEINE Sonde decken
    konnte, weil Kriterium 4 nie null war: den RUECKFALL. Getroffen wird der ANFANG
    der Statuszelle, denn genau das liest der Zaehler (`zellen[4].startswith`).
    """
    pfad = P(root, ".koolie/core/governance/DECISION_LOG.md".replace("/", os.sep))
    zeilen = lies(pfad).split("\r\n")
    treffer = [i for i, z in enumerate(zeilen) if z.startswith("| D-10 |")]
    if len(treffer) != 1:
        raise Praeparationsfehler(
            "DECISION_LOG.md: Zeile D-10 steht %dx, erwartet genau einmal"
            % len(treffer))
    if P46_BESTAETIGT not in zeilen[treffer[0]]:
        raise Praeparationsfehler(
            "DECISION_LOG.md: die Statuszelle von D-10 beginnt nicht mit %r"
            % P46_BESTAETIGT)
    zeilen[treffer[0]] = zeilen[treffer[0]].replace(
        P46_BESTAETIGT, P46_VORSCHLAG, 1)
    schreib(pfad, "\r\n".join(zeilen))


def _46_klaerungspunkt_dazu(root: str) -> None:
    """Ein Klaerungspunkt mit demselben Statuswort - er ist KEIN Decision Record.

    Die alte Zaehlregel war ein roher grep und zaehlte fuenf solcher Zeilen mit. D-11
    sagt "Decision Records"; ein Klaerungspunkt ist keiner.
    """
    pfad = P(root, ".koolie/core/governance/DECISION_LOG.md".replace("/", os.sep))
    frei(pfad, P46_KLAERUNG)
    zeile_nach(pfad, "| K-35 |",
               "| " + P46_KLAERUNG + " | Sondenklärungspunkt | niedrig | Sondenlauf | "
               "Framework Owner | entschieden (Vorschlag): Sondenauflösung |")


def _46_protokollmarker(root: str) -> None:
    """Ein Marker in einem datierten Protokoll - ausserhalb des Zaehlbereichs.

    Die Gattungsausnahme aus E2. Ein Bericht von gestern ist nicht bearbeitbar; zaehlte
    er mit, stiege Kriterium 1 mit jedem Protokoll, das den Marker erwaehnt, und koennte
    nie sinken.
    """
    ordner = P(root, ".koolie/core/tests/protocols".replace("/", os.sep))
    schreib(os.path.join(ordner, "2026-09-15-sondenprotokoll.md"),
            "# Sondenprotokoll\r\n\r\nGemessen: Mustersemantik " + P46_MARKER + ".\r\n")


sonde("46a", "Eine Zahl der Standzeile steht zu hoch - der Zaehler meldet den nicht "
             "nachgezogenen Fortschritt", lambda r: _46_zahl_verstellen(r, 3, "99"),
      M46_NICHT_NACHGEZOGEN)

sonde("46b", "Ohne Standzeile hat Pruefung 46 ihren Gegenstand verloren und sagt es, "
             "statt leise zu bestehen", _46_standzeile_weg, M46_ANKER)

sonde("46c", "Eine neue unverifizierte Aussage im Kern hebt Kriterium 1, ohne dass "
             "jemand die Standzeile anfasst", _46_marker_dazu, M46_K1)

sonde("46d", "Ein Testblatt an einer Ablage, die keine Liste kennt, hebt Kriterium 2 - "
             "der Befund dieses Antrags", _46_testblatt_dazu, M46_K2)

sonde("46e", "Ein neues Modul auf entwurf hebt Kriterium 3, auch ausserhalb der vier "
             "frueher genannten Ablagen", _46_steckbrief_dazu, M46_K3)

sonde("46f", "Ein zurueckgefallener Decision Record hebt Kriterium 4 - die Standzeile "
             "steht dann zu niedrig", _46_record_zurueckgefallen, M46_RUECKFALL)

gegenprobe("46a", "Das unveraenderte Repositorium bleibt unbeanstandet - alle vier "
                  "Zahlen der Standzeile stimmen", None, "D-11")

gegenprobe("46b", "Ein Klaerungspunkt mit demselben Statuswort bleibt ungezaehlt - "
                  "die alte Regel zaehlte fuenf davon mit", _46_klaerungspunkt_dazu,
           M46_K4)

gegenprobe("46c", "Ein Marker in einem datierten Protokoll bleibt ungezaehlt - ein "
                  "Bericht von gestern ist nicht bearbeitbar", _46_protokollmarker,
           M46_K1)


# --- 46g, 46h, Gegenprobe 46d (K-98, D-483): die Markerform ausserhalb des Zaehlbereichs
#
# Kriterium 1 zaehlt den Kern. Die Wurzeldokumente und die Quellen des Hauptdokuments
# liegen ausserhalb; seit 1.19.1 meldet Pruefung 46 dort jede Fundstelle einzeln, ohne
# die Zaehlung zu veraendern. Die Gegenprobe haelt die Grenze zur anderen Seite: Eine
# Wurzeldatei, die kein Einstiegsdokument ist, gehoert nicht zu diesem Gegenstand.
def _46_marker_in(rel: str):
    def praeparieren(root: str) -> None:
        pfad = P(root, rel.replace("/", os.sep))
        if not os.path.isfile(pfad):
            raise Praeparationsfehler("Sonde 46: %s fehlt" % rel)
        schreib(pfad, lies(pfad) + "\r\nSondenzeile: " + P46_MARKER + "\r\n")
    return praeparieren


def _46_marker_neben_der_wurzel(root: str) -> None:
    schreib(P(root, "SONDENNOTIZ.txt"), "Sondenzeile: " + P46_MARKER + "\r\n")


sonde("46g", "Die Markerform in der README der Wurzel wird gemeldet, obwohl sie ausserhalb "
             "des Zaehlbereichs von Kriterium 1 liegt", _46_marker_in("README.md"),
      M46_AUSSERHALB)

sonde("46h", "Die Markerform in einer Quelle des Hauptdokuments unter build/doc wird "
             "gemeldet", _46_marker_in(".koolie/core/build/doc/32-abschluss.md"),
      M46_AUSSERHALB)

gegenprobe("46d", "Die Markerform in einer Wurzeldatei, die kein Einstiegsdokument ist, "
                  "gehoert nicht zu diesem Gegenstand", _46_marker_neben_der_wurzel,
           M46_AUSSERHALB)


# --- Selbstprobe C1: der Baumdurchlauf sieht mehr als die Mustersuche ----------------
#
# ANLASS: Die erste Fassung des Zaehlers lief ueber glob.glob(..., recursive=True).
# glob ueberspringt Pfadbestandteile, die mit einem Punkt beginnen - damit fehlten
# fuenfzehn Dateien des Kerns, darunter genau die zwei Traeger
# clients/*/root-template/.devin/README.md und .../.claude/README.md, die den Befund zu
# Kriterium 1 tragen. Der Zaehler haette 27 gemeldet und damit zufaellig die geglaubte
# Zahl bestaetigt.
#
# Eine Zaehlregel, die einen Traeger still ueberspringt, war der ANLASS dieses Antrags.
# Sie ist beim Bauen der Abhilfe ein zweites Mal entstanden - und eine benannte Falle,
# in die man zweimal tritt, gehoert in den Code (D-74). Diese Probe zaehlt beide
# Verfahren auf dem echten Baum gegeneinander ab: Findet glob genauso viel wie os.walk,
# ist entweder der Bestand ohne versteckte Traeger - dann sagt sie das - oder jemand hat
# den Zaehler zurueckgebaut.
#
# GRENZE: Sie misst den Bestand dieses Repositoriums, nicht den eines beliebigen. In
# einem Projekt ohne versteckte Kerndateien ist der Unterschied null, und dann belegt
# sie nichts - das steht dann in ihrer eigenen Meldung.
def selbstprobe_baumdurchlauf() -> None:
    """glob gegen os.walk auf dem echten Kern - der Fallstrick aus CR-2026-070 E7."""
    kern = os.path.join(QUELLE, ".koolie/core")
    mit_glob = {p for p in glob.glob(os.path.join(kern, "**", "*"), recursive=True)
                if os.path.isfile(p)}
    mit_walk = set()
    for ordner, _, dateien in os.walk(kern):
        for name in dateien:
            mit_walk.add(os.path.join(ordner, name))
    versteckt = sorted(mit_walk - mit_glob)
    melde("SELBSTPROBE", "C1", bool(versteckt),
          "Der Baumdurchlauf des Zaehlers findet %d Kerndateien, die eine Mustersuche "
          "ueberspringt" % len(versteckt))
    if not versteckt:
        notiz("        glob und os.walk finden dasselbe. Entweder traegt der Kern keine "
              "versteckte Datei mehr - dann belegt diese Probe nichts -, oder der "
              "Zaehler ist auf glob zurueckgebaut worden (CR-2026-070 E7).")
    else:
        for pfad in versteckt[:3]:
            notiz("        " + os.path.relpath(pfad, QUELLE).replace(os.sep, "/"))


buendel(selbstprobe_baumdurchlauf,
        "Zaehlt Mustersuche gegen Baumdurchlauf auf dem echten Kern - der Fallstrick, "
        "der beim Bauen von Pruefung 46 zuschnappte")

# --- 47: das Statusvokabular jedes Modultraegers ------------------------------------
#
# Die vier Gegenstaende der Pruefung, je eine Sonde - und dazu die Sonde auf den
# verlorenen Anker. Drei der vier Sonden legen eine NEUE Datei an, statt eine
# bestehende zu verstellen: Der Statuswert des Bestands bewegt sich mit jedem Release,
# und eine Sonde, die einen Wert woertlich sucht, misst ab dem naechsten Statuswechsel
# den Suchtext statt die Pruefung (die Lehre von 46f, 0.49.0).
M47_FEHLT = "der Steckbrief führt keine Zeile"
M47_VOKABULAR = "gehört nicht zum Vokabular"
M47_VORLAGE_ECHT = "die Statuszelle einer Vorlage trägt den echten Wert"
M47_SCHLITZ_FREMD = "trägt den Ausfüllschlitz"
M47_ANKER = "kein einziger Steckbrief gefunden"
P47_STECKBRIEFKOPF = "| Attribut | Wert |"
P47_SKILLVORLAGE = ".koolie/core/templates/SKILL_TEMPLATE.md".replace("/", os.sep)
P47_SCHLITZ = "<TBD: Status; ein neuer Skill beginnt auf entwurf>"


def _47_datei(root: str, name: str, statuszeile: str) -> None:
    """Eine neue Prompt-Datei mit Steckbrief und der uebergebenen Statuszeile.

    Eine leere Statuszeile heisst: kein Status im Steckbrief.
    """
    schreib(P(root, (".koolie/core/prompts/" + name).replace("/", os.sep)),
            "# Sondenvorlage\r\n\r\n"
            + P47_STECKBRIEFKOPF + "\r\n|---|---|\r\n"
            "| ID | `FW-PR-013` |\r\n| Version | `0.1.0` |\r\n"
            + (statuszeile + "\r\n" if statuszeile else "")
            + "| Owner (Rolle) | `<FRAMEWORK_OWNER>` |\r\n")


def _47_ohne_statuszeile(root: str) -> None:
    """Ein Steckbrief ohne Statuszeile - genau die zwoelf Traeger aus K-36."""
    _47_datei(root, "13-sonde-ohne-status.md", "")


def _47_fremdes_wort(root: str) -> None:
    """Ein Statuswert ausserhalb des Vokabulars - bis 0.50.0 nur in einer SKILL.md gefangen."""
    _47_datei(root, "13-sonde-vokabular.md", "| Status | `banane` |")


def _47_schlitz_ausserhalb(root: str) -> None:
    """Ein Ausfuellschlitz in einer Datei, die keine Vorlage ist - der Preis aus D-104."""
    _47_datei(root, "13-sonde-schlitz.md",
              "| Status | `<TBD: Status; ein neuer Prompt beginnt auf entwurf>` |")


def _47_vorlage_mit_echtem_wert(root: str) -> None:
    """Der Defekt von 0.50.0, wiederhergestellt: eine Vorlage traegt `entwurf`.

    Die Statuszelle der Skillvorlage gab diesen Wert an jede Kopie weiter und durfte
    sich deshalb nie aendern; genau daran war Kriterium 3 von D-11 unerreichbar
    (D-104). Die Sonde stellt den Zustand HER statt ihn zu entfernen - wie 38a, 38b
    und 46f.
    """
    ersetze(P(root, P47_SKILLVORLAGE), (P47_SCHLITZ, "entwurf"))


def _47_steckbriefkopf_umbenennen(root: str) -> None:
    """Die Kopfzeile jedes Steckbriefs umbenennen - die Pruefung findet keinen mehr.

    Anders als bei den Pruefungen 28, 29, 31, 40 und 46 ist der Anker hier keine
    einzelne Zeichenkette in einer Datei, sondern eine KONVENTION ueber den ganzen
    Bestand. Verliert sie sich, faende die Pruefung nichts mehr und bestuende leise -
    deshalb benennt diese Sonde sie ueberall um und belegt, dass der Lauf das meldet.
    """
    getroffen = 0
    for ordner, _, dateien in os.walk(P(root, ".koolie/core")):
        for name in sorted(dateien):
            if not name.endswith(".md"):
                continue
            pfad = os.path.join(ordner, name)
            text = lies(pfad)
            if P47_STECKBRIEFKOPF not in text:
                continue
            schreib(pfad, text.replace(P47_STECKBRIEFKOPF, "| Merkmal | Wert |"))
            getroffen += 1
    if getroffen < 50:
        raise Praeparationsfehler(
            "nur %d Dateien mit der Steckbriefkopfzeile gefunden, erwartet mindestens "
            "50 - die Konvention hat sich geaendert" % getroffen)


def _47_verlaufszusatz(root: str) -> None:
    """Einem gehobenen Traeger einen Verlaufszusatz in Klammern anhaengen.

    `entwurf (Referenzpack der Erstfassung)` steht seit der Erstfassung im Bestand;
    verglichen wird deshalb das ERSTE WORT. Die Gegenprobe belegt, dass ein solcher
    Zusatz zulaessig bleibt - und dass Pruefung 46 ihn weiterhin richtig einordnet.
    """
    ersetze(P(root, ".koolie/core/checklists/01-preflight.md".replace("/", os.sep)),
            ("| Status | `pilot` |", "| Status | `pilot (Abnahme 2026-09-15)` |"))


def _47_tabelle_hinter_ueberschrift(root: str) -> None:
    """Eine Steckbriefkopfzeile im KOERPER einer Datei ist kein Steckbrief.

    Der Fall von templates/PLAN_TEMPLATE.md: Dort steht die Tabelle hinter einer
    Ueberschrift der Ebene 2 und ist das Formular fuer die Kopie, nicht der Steckbrief
    der Datei. Eine Erkennungsregel, die bloss nach der Kopfzeile sucht, verlangte dort
    einen Statuswert - und die Datei fuehrt zu Recht keinen.
    """
    schreib(P(root, ".koolie/core/examples/example-sondenformular.md"
              .replace("/", os.sep)),
            "# Beispielformular (synthetisch)\r\n\r\n"
            "Ein Formular, das die Kopie ausfuellt - kein Steckbrief.\r\n\r\n"
            "## Formular\r\n\r\n"
            + P47_STECKBRIEFKOPF + "\r\n|---|---|\r\n"
            "| Erstellt mit | `<Skill>` |\r\n| Bestaetigt durch | `<Rolle>` |\r\n")


sonde("47a", "Ein Steckbrief ohne Statuszeile wird gemeldet - das Loch, durch das bis "
             "0.50.0 zwoelf Traeger entkamen", _47_ohne_statuszeile, M47_FEHLT)

sonde("47b", "Ein Statuswert ausserhalb des Vokabulars faellt auf, auch weit weg von "
             "einer SKILL.md", _47_fremdes_wort, M47_VOKABULAR)

sonde("47c", "Eine Vorlage mit echtem Statuswert wird gemeldet - der Defekt, der "
             "Kriterium 3 unerreichbar machte", _47_vorlage_mit_echtem_wert,
      M47_VORLAGE_ECHT)

sonde("47d", "Ein Ausfuellschlitz ausserhalb einer Vorlage wird gemeldet - die "
             "kopierte und nicht gefuellte Vorlage", _47_schlitz_ausserhalb,
      M47_SCHLITZ_FREMD)

sonde("47e", "Ohne die Steckbriefkonvention hat Pruefung 47 ihren Gegenstand verloren "
             "und sagt es, statt leise zu bestehen", _47_steckbriefkopf_umbenennen,
      M47_ANKER)

gegenprobe("47a", "Das unveraenderte Repositorium bleibt unbeanstandet - jeder "
                  "Steckbrief traegt einen gueltigen Statuswert", None, "Vokabular")

gegenprobe("47b", "Ein Verlaufszusatz in Klammern bleibt zulaessig - verglichen wird "
                  "das erste Wort des Werts", _47_verlaufszusatz, M47_VOKABULAR)

gegenprobe("47c", "Eine Steckbriefkopfzeile hinter einer Ueberschrift ist kein "
                  "Steckbrief und verlangt keinen Status", _47_tabelle_hinter_ueberschrift,
           M47_FEHLT)


# --- 48: die Werkzeugneutralitaet des Kerns -----------------------------------------
#
# Die drei Gruende, aus denen Pruefung 12 die siebzehn Fundstellen nicht fand, sind hier
# je eine Sonde: der Pfad des INSTALLIERTEN Packs (Grund 2 - er existiert und war damit
# unsichtbar), der Pfad OHNE Backticks (Grund 1) und die anweisende Spalte des
# Testkatalogs, deren letzte Zelle bewusst ausgenommen ist. Dazu die Sonde auf den
# verlorenen Anker und drei Gegenproben - die Belegspalte, die Chronik und der
# unberuehrte Bestand.
#
# Die Sonden legen NEUE Dateien an, statt bestehende zu verstellen: Ein Suchtext im
# Bestand misst ab dem naechsten Release den Suchtext statt die Pruefung (die Lehre von
# 46f). Welchen Pfad sie schreiben, LESEN sie aus den Manifesten - eine Sonde, die einen
# Pfad raet, misst den geratenen Pfad.
M48_PFAD = "gehört der Laufzeitschicht des Client Packs"
M48_ANKER = "kein Client Pack mit runtime_placeholders gefunden"
P48_KATALOG = ".koolie/core/tests/TEST_CATALOG.md".replace("/", os.sep)
P48_ROADMAP = ".koolie/core/docs/ROADMAP.md".replace("/", os.sep)
P48_KATALOGANKER = "| FW-AK-02 (Basis) |"
P48_ROADMAPANKER = "#### Der Releaseplan bis 1.0.0 und darüber hinaus"


def _48_marken(root: str) -> tuple:
    """(Laufzeitschicht des installierten Packs, die des anderen) - aus den Manifesten.

    Installiert ist das Pack, dessen Laufzeitverzeichnis im Baum wirklich liegt; genau
    darauf beruht der zweite Grund, aus dem Pruefung 12 blind war.
    """
    base = P(root, ".koolie/core", "clients")
    verzeichnisse = []
    for name in sorted(os.listdir(base)):
        if name.startswith("_"):
            continue
        mp = os.path.join(base, name, "manifest.json")
        if os.path.exists(mp):
            verzeichnisse.append(json.loads(lies(mp))["runtime_dir"])
    if len(verzeichnisse) < 2:
        raise Praeparationsfehler(
            "Weniger als zwei Client Packs mit manifest.json - die Sonden zu 48 "
            "brauchen ein installiertes und ein nicht installiertes Pack")
    installiert = [v for v in verzeichnisse if os.path.isdir(P(root, *v.split("/")))]
    fremd = [v for v in verzeichnisse if v not in installiert]
    if not installiert or not fremd:
        raise Praeparationsfehler(
            "Im Baum liegt keine oder jede Laufzeitschicht (%s) - die Sonden zu 48 "
            "unterscheiden das installierte vom nicht installierten Pack"
            % ", ".join(verzeichnisse))
    return installiert[0], fremd[0]


def _48_datei(root: str, name: str, inhalt: str) -> None:
    """Eine neue Prompt-Datei mit vollstaendigem Steckbrief und der Inhaltszeile."""
    schreib(P(root, (".koolie/core/prompts/" + name).replace("/", os.sep)),
            "# Sondenvorlage\r\n\r\n"
            "| Attribut | Wert |\r\n|---|---|\r\n"
            "| ID | `FW-PR-014` |\r\n| Version | `0.1.0` |\r\n"
            "| Status | `pilot` |\r\n"
            "| Owner (Rolle) | `<FRAMEWORK_OWNER>` |\r\n\r\n"
            + inhalt + "\r\n")


def _48_installiertes_pack(root: str) -> None:
    """Der Pfad des INSTALLIERTEN Packs in einem Kerntraeger - Grund 2 der Blindheit.

    Pruefung 12 meldet nur Pfade, die es NICHT GIBT. Dieser hier existiert im Baum und
    lief deshalb sechsundfuenfzig Releases lang durch.
    """
    installiert, _ = _48_marken(root)
    _48_datei(root, "14-sonde-installiert.md",
              "Ausgabeformat: Analyse nach `%s/skills/koolie-repo-analyze/SKILL.md`."
              % installiert)


def _48_ohne_backticks(root: str) -> None:
    """Derselbe Befund ohne Backticks - Grund 1 der Blindheit.

    Zehn der siebzehn Fundstellen standen so: im Codeblock, in Prosa oder im
    HTML-Kommentar. Die Heuristik von Pruefung 12 sieht nur Token in Backticks.
    """
    _, fremd = _48_marken(root)
    _48_datei(root, "14-sonde-prosa.md",
              "Die Regeln liegen unter %s/rules und werden bei Sitzungsbeginn geladen."
              % fremd)


def _48_anweisende_spalte(root: str) -> None:
    """Ein Clientpfad in einer ANWEISENDEN Spalte des Testkatalogs wird gemeldet.

    Die Ausnahme dieses Traegers gilt der LETZTEN Zelle (Ergebnisstatus, D-117). Wer
    sie auf die Zeile ausdehnt, nimmt genau die Eingabezelle mit heraus, in der bis
    0.56.2 'Passe AGENTS.md an' stand - der Zuschnitt, der den Gegenstand mitentfernt.
    """
    installiert, _ = _48_marken(root)
    zeile_nach(P(root, P48_KATALOG), P48_KATALOGANKER,
               "| FW-SO-01 | Sondenzeile | Sondenvorbedingung | Anweisung: lies %s/config "
               "| Ablehnung | Zugriff | sitzung | offen |" % installiert)


def _48_anker_verlieren(root: str) -> None:
    """Ohne runtime_placeholders in den Manifesten hat die Pruefung keine Marken mehr.

    Sie leitet sie von dort ab; geht der Schluessel verloren, faende sie nichts und
    bestuende leise. Die Sonde belegt, dass sie das Fehlen selbst meldet (D-23).
    """
    base = P(root, ".koolie/core", "clients")
    getroffen = 0
    for name in sorted(os.listdir(base)):
        mp = os.path.join(base, name, "manifest.json")
        if not os.path.exists(mp):
            continue
        ersetze(mp, ('"runtime_placeholders"', '"runtime_placeholders_alt"'))
        getroffen += 1
    if not getroffen:
        raise Praeparationsfehler(
            "Kein manifest.json unter clients/ - die Ankersonde zu 48 haette nichts "
            "zu verstellen")


def _48_belegspalte(root: str) -> None:
    """Ein Clientpfad in der LETZTEN Zelle einer Testkatalogzeile bleibt zulaessig.

    Der Ergebnisstatus nennt, was ein Lauf gelesen hat, und das gemessene Client Pack
    (D-117). Ein Begriff statt des Pfads waere dort kein Beleg mehr.
    """
    _, fremd = _48_marken(root)
    zeile_nach(P(root, P48_KATALOG), P48_KATALOGANKER,
               "| FW-SO-02 | Sondenzeile | Sondenvorbedingung | Anweisung | Ablehnung "
               "| Zugriff | sitzung | bestanden (`.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278 - der Lauf benennt `%s/rules/00-framework-core.md`) |"
               % fremd)


def _48_chronik(root: str) -> None:
    """Ein Clientpfad in der Roadmap bleibt zulaessig - sie berichtet Erhebungen.

    Dieselbe Begruendung wie bei den Protokollen: Wer einen Befundbericht glaettet,
    macht aus einer richtigen Zeile eine unbelegbare.
    """
    installiert, fremd = _48_marken(root)
    pfad = P(root, P48_ROADMAP)
    schreib(pfad, lies(pfad).rstrip("\r\n") + "\r\n\r\n"
            + "Sondennachtrag zur Erhebung: Der Lauf las %s/rules und legte seine "
              "Ausgabe unter %s/skills ab.\r\n" % (installiert, fremd))


sonde("48a", "Der Pfad des INSTALLIERTEN Packs in einem Kerntraeger wird gemeldet - "
             "genau der Fall, den Pruefung 12 nie sah", _48_installiertes_pack, M48_PFAD)

sonde("48b", "Ein Clientpfad ohne Backticks wird gemeldet - zehn der siebzehn "
             "Fundstellen standen so", _48_ohne_backticks, M48_PFAD)

sonde("48c", "Ein Clientpfad in einer anweisenden Spalte des Testkatalogs wird "
             "gemeldet, obwohl die letzte Zelle ausgenommen ist", _48_anweisende_spalte,
      M48_PFAD)

sonde("48d", "Ohne runtime_placeholders in den Manifesten meldet Pruefung 48 den "
             "verlorenen Gegenstand, statt leise zu bestehen", _48_anker_verlieren,
      M48_ANKER)

gegenprobe("48a", "Das unveraenderte Repositorium bleibt unbeanstandet - die siebzehn "
                  "Fundstellen sind aufgeloest", None, M48_PFAD)

gegenprobe("48b", "Ein Clientpfad in der Ergebnisstatuszelle des Testkatalogs bleibt "
                  "zulaessig - dort ist er der Beleg", _48_belegspalte, M48_PFAD)

gegenprobe("48c", "Ein Clientpfad in der Roadmap bleibt zulaessig - sie fuehrt die "
                  "Erhebungen je Arbeitspaket", _48_chronik, M48_PFAD)


# --- Pruefung 49: ausdruecklicher Skill-Aufruf im Testkatalog (D-146) --------------
#
# Der Befund, der sie veranlasst hat, ist am 2026-09-18 an FW-SC-01 gemessen worden: Der
# Hauptlauf rief `koolie-change-small` auf, wurde abgewiesen - neun von zwoelf Kernskills
# fuehren `triggers` ohne `- model`, und das Pack claude-code bildet das auf
# `disable-model-invocation: true` ab - und arbeitete den Ablauf nicht nach. Damit fiel
# Schritt 3 des Skills aus, der die Verwender der geaenderten Einheit erhebt; die
# Scope-Falle konnte nicht zuschnappen. Die Zelle stand danach als `offen`, und die
# Ursache wurde einer Regelkollision zugeschrieben, die es nicht gibt (CR-2026-085).
M49_AUFRUF = "ohne den ausdrücklichen Aufruf"
M49_ANKER = "kein Skill mit 'triggers' ohne '- model' gefunden"
P49_KATALOG = ".koolie/core/tests/TEST_CATALOG.md".replace("/", os.sep)
P49_KATALOGANKER = "| FW-AK-02 (Basis) |"
P49_SKILLS = ".koolie/core/framework/skills".replace("/", os.sep)


def _49_skill_ohne_modell(root: str) -> str:
    """Ein Kernskill, dessen Quelle `triggers` ohne `- model` fuehrt - abgeleitet.

    Die Sonde raet den Namen nicht: Waere er gepflegt, prueften Sonde und Pruefung
    verschiedene Mengen, und die Sonde bestuende an einem Skill, den es nicht mehr gibt.
    """
    basis = P(root, *P49_SKILLS.split(os.sep))
    for name in sorted(os.listdir(basis)):
        pfad = os.path.join(basis, name, "SKILL.md")
        if not os.path.isfile(pfad):
            continue
        text = lies(pfad)
        i = text.find("triggers:")
        if i < 0:
            continue
        block = text[i:text.find("---", 3)] if text.startswith("---") else text[i:i + 200]
        # Seit 1.17.0 tragen koolie-bugfix-prepare und koolie-plan `model` (D-451); der naechste
        # Skill ohne model fuehrt Test- und Lintbefehle aus, und Pruefung 49 verlangt dann
        # zu Recht den Schlitz in der Vorbedingung - gemessen wuerde die falsche Regel.
        if "- model" not in block and "<TEST_COMMAND>" not in text and "<LINT_COMMAND>" not in text:
            return name
    raise Praeparationsfehler(
        "Kein Kernskill mit `triggers` ohne `- model` - die Sonden zu 49 brauchen einen")


def _49_skill_mit_modell(root: str) -> str:
    """Das Gegenstueck: ein Skill, den das Modell von sich aus waehlen darf."""
    basis = P(root, *P49_SKILLS.split(os.sep))
    for name in sorted(os.listdir(basis)):
        pfad = os.path.join(basis, name, "SKILL.md")
        if not os.path.isfile(pfad):
            continue
        text = lies(pfad)
        i = text.find("triggers:")
        if i < 0:
            continue
        block = text[i:text.find("---", 3)] if text.startswith("---") else text[i:i + 200]
        if "- model" in block:
            return name
    raise Praeparationsfehler(
        "Kein Kernskill mit `- model` - die Gegenprobe zu 49 braucht einen")


def _49_katalogzeile(root: str, zeile: str) -> None:
    zeile_nach(P(root, P49_KATALOG), P49_KATALOGANKER, zeile)


def _49_nackte_nennung(root: str) -> None:
    """Der Skillname ohne Schraegstrich im Ausloeser eines `sitzung`-Testfalls.

    Genau die Schreibweise, in der vier Katalogzeilen ihn bis 0.59.1 fuehrten - und in
    der der Prompt zu FW-SC-01 ihn gar nicht fuehrte.
    """
    _49_katalogzeile(root,
        "| FW-SO-03 | Sondenzeile | Sondenvorbedingung | %s mit Sondenaufgabe "
        "| Ablehnung | Zugriff | sitzung | offen |" % _49_skill_ohne_modell(root))


def _49_anker_verlieren(root: str) -> None:
    """Ohne `triggers` in den Skillquellen hat Pruefung 49 keine Marken mehr.

    Sie leitet sie von dort ab; geht der Schluessel verloren, faende sie nichts und
    bestuende leise. Die Sonde belegt, dass sie das Fehlen selbst meldet (D-23).
    """
    basis = P(root, *P49_SKILLS.split(os.sep))
    getroffen = 0
    for name in sorted(os.listdir(basis)):
        pfad = os.path.join(basis, name, "SKILL.md")
        if not os.path.isfile(pfad):
            continue
        if "triggers:" in lies(pfad):
            ersetze(pfad, ("triggers:", "ladeausloeser:"))
            getroffen += 1
    if not getroffen:
        raise Praeparationsfehler(
            "Keine SKILL.md mit `triggers` - die Ankersonde zu 49 haette nichts zu "
            "verstellen")


def _49_ausdruecklicher_aufruf(root: str) -> None:
    """Derselbe Skill als `/name` bleibt zulaessig - das ist der Aufruf selbst."""
    _49_katalogzeile(root,
        "| FW-SO-04 | Sondenzeile | Sondenvorbedingung | `/%s` mit Sondenaufgabe "
        "| Ablehnung | Zugriff | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |"
        % _49_skill_ohne_modell(root))


def _49_modellaufrufbar(root: str) -> None:
    """Ein Skill MIT `- model` bleibt nackt zulaessig - der Zuschnitt ist nicht zu breit.

    Ohne dieses Paar meldete die Pruefung jeden Skillnamen und waere eine Stilregel.
    """
    _49_katalogzeile(root,
        "| FW-SO-05 | Sondenzeile | Sondenvorbedingung | %s mit Sondenaufgabe "
        "| Ablehnung | Zugriff | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |"
        % _49_skill_mit_modell(root))


def _49_andere_spalte(root: str) -> None:
    """Derselbe Name in einer ANDEREN Spalte bleibt zulaessig - die Regel gilt dem Ausloeser.

    Das Gegenstueck zur Spaltenaufloesung: Wer die Zeile statt der Spalte nimmt, meldet
    auch die Zelle, die das erwartete Verhalten beschreibt - und dort ist die Nennung
    eine Aussage ueber den Lauf, keine Anweisung an ihn.
    """
    _49_katalogzeile(root,
        "| FW-SO-06 | Sondenzeile | Sondenvorbedingung | Sondenaufgabe "
        "| Der Lauf nennt %s als zustaendig | Zugriff | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |"
        % _49_skill_ohne_modell(root))


def _49_andere_pruefmethode(root: str) -> None:
    """Eine nackte Nennung bei Pruefmethode `review` bleibt zulaessig.

    Die Regel gilt dem Lauf, nicht dem Lesen: Eine Durchsicht ruft keinen Skill auf.
    """
    _49_katalogzeile(root,
        "| FW-SO-07 | Sondenzeile | Sondenvorbedingung | %s mit Sondenaufgabe "
        "| Ablehnung | Zugriff | review | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |"
        % _49_skill_ohne_modell(root))


sonde("49a", "Ein Kernskill ohne Modellzulassung, im Ausloeser eines sitzung-Testfalls "
             "nackt genannt, wird gemeldet", _49_nackte_nennung, M49_AUFRUF)

sonde("49b", "Ohne `triggers` in den Skillquellen meldet Pruefung 49 den verlorenen "
             "Gegenstand, statt leise zu bestehen", _49_anker_verlieren, M49_ANKER)

gegenprobe("49a", "Das unveraenderte Repositorium bleibt unbeanstandet - die vier "
                  "Fundstellen sind auf `/name` gestellt", None, M49_AUFRUF)

gegenprobe("49b", "Derselbe Skill als `/name` bleibt zulaessig - das ist der Aufruf",
           _49_ausdruecklicher_aufruf, M49_AUFRUF)

gegenprobe("49c", "Ein Skill MIT Modellzulassung bleibt nackt zulaessig - der Zuschnitt "
                  "ist nicht zu breit", _49_modellaufrufbar, M49_AUFRUF)

gegenprobe("49d", "Derselbe Name in einer anderen Spalte bleibt zulaessig - die Regel "
                  "gilt dem Ausloeser", _49_andere_spalte, M49_AUFRUF)

gegenprobe("49e", "Eine nackte Nennung bei Pruefmethode `review` bleibt zulaessig - "
                  "eine Durchsicht ruft keinen Skill auf", _49_andere_pruefmethode,
           M49_AUFRUF)


# --- Gegenstand 2: der Ausloeser, der eine UEBUNG nennt (D-172) ----------------------
#
# FW-PO-02 nennt keinen Skill und erbt doch vier: Sein Ausloeser verweist auf UE3. Der
# Zuschnitt ist SCHMAL - gefragt wird, ob UEBERHAUPT ein ausdruecklicher Aufruf
# dasteht. Die beiden Gegenproben belegen genau das: eine fuer den bewussten Zuschnitt
# (FW-SC-01 nennt UE3 und ruft nur den dritten Schritt auf), eine fuer die Uebung ohne
# gesperrten Skill.
M49_UEBUNG = "und damit deren Ablauf"
M49_UEBUNGSANKER = "führt keinen Abschnitt der Form"
P49_UEBUNGSDATEI = ".koolie/core/onboarding/exercises/EXERCISES.md".replace("/", os.sep)


def _49_uebung_ohne_aufruf(root: str) -> None:
    """Ein Ausloeser, der eine Uebung mit gesperrten Skills nennt und keinen Aufruf."""
    _49_katalogzeile(root,
        "| FW-SO-08 | Sondenzeile | Sondenvorbedingung | Ü3 aus "
        "`.koolie/core/onboarding/exercises/EXERCISES.md` | Ablehnung | Zugriff "
        "| sitzung | offen |")


def _49_uebung_mit_einem_aufruf(root: str) -> None:
    """Dieselbe Uebung, aber ein Schritt ausdruecklich aufgerufen - der Fall FW-SC-01."""
    _49_katalogzeile(root,
        "| FW-SO-09 | Sondenzeile | Sondenvorbedingung | Ü3-Änderung, ausgelöst über "
        "`/%s` | Ablehnung | Zugriff | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |"
        % _49_skill_ohne_modell(root))


def _49_uebung_ohne_gesperrten_skill(root: str) -> None:
    """Eine Uebung, deren Abschnitt nur modellaufrufbare Skills fuehrt - UE1/UE2."""
    _49_katalogzeile(root,
        "| FW-SO-10 | Sondenzeile | Sondenvorbedingung | Ü1 aus "
        "`.koolie/core/onboarding/exercises/EXERCISES.md` | Ablehnung | Zugriff "
        "| sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _49_uebungsanker_verlieren(root: str) -> None:
    """Ohne die Abschnittsueberschriften hat Gegenstand 2 keine Uebungen mehr."""
    pfad = P(root, P49_UEBUNGSDATEI)
    text = lies(pfad)
    if "\n## Ü" not in text:
        raise Praeparationsfehler(
            "EXERCISES.md fuehrt keinen Abschnitt '## Ü<n>' - die Ankersonde zu 49 "
            "haette nichts zu entfernen")
    schreib(pfad, text.replace("\n## Ü", "\n## Uebung "))


sonde("49c", "Ein Ausloeser nennt eine Uebung mit vier gesperrten Skills und keinen "
             "einzigen ausdruecklichen Aufruf - der Fall FW-PO-02",
      _49_uebung_ohne_aufruf, M49_UEBUNG)

sonde("49d", "Ohne die Abschnittsueberschriften der Uebungsdatei meldet Gegenstand 2 "
             "den verlorenen Anker, statt leise zu bestehen", _49_uebungsanker_verlieren,
      M49_UEBUNGSANKER)

gegenprobe("49f", "Dieselbe Uebung mit EINEM ausdruecklichen Aufruf bleibt zulaessig - "
                  "der bewusste Zuschnitt von FW-SC-01", _49_uebung_mit_einem_aufruf,
           M49_UEBUNG)

gegenprobe("49g", "Eine Uebung, deren Abschnitt keinen gesperrten Skill fuehrt, bleibt "
                  "ohne Aufruf zulaessig", _49_uebung_ohne_gesperrten_skill, M49_UEBUNG)


# --- Pruefung 50: Vollstaendigkeit des Klaerungspunktregisters (D-147) -------------
M50_FEHLT = "steht in keiner Registerzeile"
M50_ANKER = "hat ihren Anker verloren"
P50_LOG = ".koolie/core/governance/DECISION_LOG.md".replace("/", os.sep)
P50_ROADMAP = ".koolie/core/docs/ROADMAP.md".replace("/", os.sep)
# Eine Kennung, die es im Register nicht gibt und nie geben wird - die Sonde vergibt
# keine echte. 'Eine synthetische Kennung nimmt nie die naechste freie' (0.59.0).
#
# ZUSAMMENGESETZT, und das ist kein Trick, sondern der Gegenstand: Dieses Skript liegt
# im Kern, und Pruefung 50 meldet jede dort GENANNTE Kennung ohne Registerzeile. Stuende
# sie woertlich hier, muesste sie in die Ausnahmemenge - und dann meldete die Sonde
# nichts mehr. Eine Sonde, deren Gegenstand die eigene Nennung ist, darf sich nicht
# selbst nennen - auch nicht in dem Kommentar, der das erklaert. Der erste Entwurf
# dieses Absatzes tat es, und Pruefung 50 hat ihn gemeldet.
K50_SYNTH = "K-" + "95"


def _50_freie_kennung(root: str) -> str:
    """Belegt, dass die Sondenkennung im Register wirklich fehlt - sonst misst sie nichts."""
    if ("| " + K50_SYNTH + " |") in lies(P(root, P50_LOG)):
        raise Praeparationsfehler(
            "%s steht bereits im Register - die Sonde zu 50 braucht eine freie Kennung"
            % K50_SYNTH)
    return K50_SYNTH


def _50_nennung_ohne_register(root: str) -> None:
    """Eine Kennung wird in einem Kerntraeger genannt und steht in keiner Registerzeile.

    Genau der Fall von K-34 (sieben Traeger, seit 0.32.0) und K-55 (drei Traeger, als
    'neu' angekuendigt und nie eingetragen).
    """
    kennung = _50_freie_kennung(root)
    pfad = P(root, P50_ROADMAP)
    schreib(pfad, lies(pfad).rstrip("\r\n") + "\r\n\r\n"
            + "Sondennachtrag: Offen bleibt die Frage nach dem Sondengegenstand (%s).\r\n"
            % kennung)


def _50_anker_verlieren(root: str) -> None:
    """Ohne den Absatz mit den synthetischen Kennungen hat Pruefung 50 keine Ausnahme mehr.

    Sie leitet sie von dort ab; geht der Absatz verloren, meldete sie jede Sondenkennung
    des Pruefapparats als Befund - oder, schlimmer, man naehme die Liste in den Code.
    """
    ersetze(P(root, P50_LOG),
            ("**Belegte synthetische Kennungen", "**Frueher belegte Kennungen"))


def _50_nennung_mit_register(root: str) -> None:
    """Dieselbe Nennung MIT Registerzeile bleibt zulaessig - das ist der erlaubte Fall."""
    kennung = _50_freie_kennung(root)
    _50_nennung_ohne_register(root)
    zeile_nach(P(root, P50_LOG), "| K-56 | Ein dezentrales Testblatt",
               "| %s | Sondenfrage? | niedrig | Sondenbegruendung | Sondenweg | offen |"
               % kennung)


def _50_synthetische_kennung(root: str) -> None:
    """Eine synthetische Kennung des Pruefapparats bleibt ohne Registerzeile zulaessig.

    Ohne dieses Paar meldete die Pruefung ihre eigenen Sonden - der Zuschnitt waere zu
    breit, und die Ausnahme haette keinen belegten Gegenstand.
    """
    pfad = P(root, P50_ROADMAP)
    schreib(pfad, lies(pfad).rstrip("\r\n") + "\r\n\r\n"
            + "Sondennachtrag: Die Gegenprobe benutzt die synthetische Kennung K-99.\r\n")


sonde("50a", "Eine Kennung, die ein Kerntraeger nennt und das Register nicht fuehrt, "
             "wird gemeldet - der Fall von K-34 und K-55", _50_nennung_ohne_register,
      M50_FEHLT)

sonde("50b", "Ohne den Absatz mit den synthetischen Kennungen meldet Pruefung 50 den "
             "verlorenen Anker, statt leise zu bestehen", _50_anker_verlieren, M50_ANKER)

gegenprobe("50a", "Das unveraenderte Repositorium bleibt unbeanstandet - K-34 und K-55 "
                  "sind nachgetragen", None, M50_FEHLT)

gegenprobe("50b", "Dieselbe Nennung MIT Registerzeile bleibt zulaessig",
           _50_nennung_mit_register, M50_FEHLT)

gegenprobe("50c", "Eine synthetische Kennung des Pruefapparats bleibt ohne Registerzeile "
                  "zulaessig - der Zuschnitt ist nicht zu breit", _50_synthetische_kennung,
           M50_FEHLT)


# --- Pruefung 51: Ausfuellschlitz fuer einen festgelegten Overlay-Wert (D-150) -----
M51_SCHLITZ = "trägt einen Ausfüllschlitz, obwohl"
M51_ANKER = "Kontextquellentabelle mit dem Kopf"
P51_QUELLE = ".koolie/core/templates/project-overlay/OVERLAY.md".replace("/", os.sep)
P51_LAUFZEIT = (".koolie/core/framework/runtime/rules/20-project-overlay.md"
                .replace("/", os.sep))
# Der Stand VOR 0.61.0, woertlich. Die Sonde stellt ihn wieder her: Sie misst genau den
# Befund, den dieses Release behoben hat, und nicht einen nachgebauten.
P51_ALTZEILE = '- Freigegebene externe Domains: `<TBD: Liste oder „keine">`'


def _zeile_ersetzen(pfad: str, praefix: str, neu: str) -> None:
    """Die eine Zeile, die mit `praefix` beginnt, ganz ersetzen.

    Fuer eine Praeparation, deren Gegenstand eine ganze Zeile ist, taugt kein Suchtext
    ueber den Zeileninhalt: Er waere die Zeile selbst und muesste bei jeder Umformulierung
    nachgezogen werden. Der Praefix ist der Feldname, und der ist der Gegenstand.
    """
    zeilen = lies(pfad).split("\r\n")
    treffer = [i for i, z in enumerate(zeilen) if z.startswith(praefix)]
    if len(treffer) != 1:
        raise Praeparationsfehler(
            "%s: Praefix %r steht %dx am Zeilenanfang, erwartet genau einmal"
            % (os.path.basename(pfad), praefix, len(treffer)))
    zeilen[treffer[0]] = neu
    schreib(pfad, "\r\n".join(zeilen))


def _51_schlitz_zurueck(root: str) -> None:
    """Der Stand vor 0.61.0: die Laufzeitfassung bietet an, was die Quelle ausschliesst."""
    _zeile_ersetzen(P(root, P51_LAUFZEIT), "- Freigegebene externe Domains:", P51_ALTZEILE)


def _51_anker_verlieren(root: str) -> None:
    """Ohne die Kontextquellentabelle hat Pruefung 51 keine Feldmenge mehr.

    Sie leitet sie von dort ab; geht der Kopf verloren, pruefte sie nichts und bestuende
    leise - genau die Bauform, die D-23 ausschliesst.
    """
    ersetze(P(root, P51_QUELLE),
            ("| Kontextquelle | Kontextklasse | Freigabe | Bedingungen |",
             "| Quelle | Klasse | Freigabe | Bedingungen |"))


def _51_quelle_oeffnet(root: str) -> None:
    """Legt die QUELLE den Wert nicht fest, ist der Schlitz zulaessig - beides zusammen.

    Das Paar belegt, dass die Pruefung die Quelle liest und nicht ein verdrahtetes Feld:
    Derselbe Schlitz, der eben gemeldet wurde, bleibt unbeanstandet, sobald die Vorlage
    ihn selbst offen laesst.
    """
    _51_schlitz_zurueck(root)
    ersetze(P(root, P51_QUELLE),
            ("| Freigegebene externe Domains (Fetch) | K0 | **„keine\"** |",
             "| Freigegebene externe Domains (Fetch) | K0 | `<TBD: Liste oder "
             "„keine\">` |"))


def _51_fremdes_feld(root: str) -> None:
    """Ein Schlitz fuer ein Feld, das die Quellentabelle nicht fuehrt, bleibt zulaessig."""
    zeile_nach(P(root, P51_LAUFZEIT), "- Freigegebene externe Domains:",
               "- Freigegebene Sondenquellen: `<TBD: Liste oder „keine\">`")


sonde("51a", "Ein Ausfuellschlitz in der Laufzeitfassung fuer einen Wert, den die "
             "Overlay-Vorlage festlegt, wird gemeldet", _51_schlitz_zurueck, M51_SCHLITZ)

sonde("51b", "Ohne den Kopf der Kontextquellentabelle meldet Pruefung 51 die verlorene "
             "Feldmenge, statt leise zu bestehen", _51_anker_verlieren, M51_ANKER)

gegenprobe("51a", "Das unveraenderte Repositorium bleibt unbeanstandet - die Domainzeile "
                  "traegt seit 0.61.0 den festen Wert", None, M51_SCHLITZ)

gegenprobe("51b", "Laesst die Quelle den Wert selbst offen, bleibt derselbe Schlitz "
                  "zulaessig - die Pruefung liest die Vorlage", _51_quelle_oeffnet,
           M51_SCHLITZ)

gegenprobe("51c", "Ein Schlitz fuer ein Feld ausserhalb der Quellentabelle bleibt "
                  "zulaessig - der Zuschnitt ist nicht zu breit", _51_fremdes_feld,
           M51_SCHLITZ)


# --- Pruefung 52: V6-Gegenstand mit Freigabefolge (D-151) --------------------------
M52_FOLGE = "deren Rechtsfolge eine Freigabe ist"
M52_ANKER = "Delegationsverbotsliste ist nicht mehr auffindbar"
P52_LAUFZEIT = (".koolie/core/framework/runtime/rules/10-privacy-security.md"
                .replace("/", os.sep))
P52_RISIKO = ".koolie/core/framework/core/09-risk-model.md".replace("/", os.sep)
P52_CL06 = ".koolie/core/checklists/06-security.md".replace("/", os.sep)
# Woertlich der Stand vor 0.61.0 - sechzig Releases lang stand er so.
P52_ALTSATZ = (
    "Authentifizierung, Autorisierung, Sitzungsverwaltung, Kryptografie, "
    "Security-Konfiguration, Eingabevalidierung an Systemgrenzen, Verarbeitung "
    "personenbezogener Daten: Kontrollstufe hoch. Nur analysieren und planen; Umsetzung "
    "ausschließlich nach dokumentierter Freigabe durch `<APPROVAL_ROLE>` und "
    "`<SECURITY_CONTACT>`."
)


def _52_altsatz_zurueck(root: str) -> None:
    """Der Stand vor 0.61.0: ein Delegationsverbot in der Aufzaehlung mit Freigabefolge."""
    _zeile_ersetzen(P(root, P52_LAUFZEIT),
                    "Stufe hoch: Authentifizierung, Autorisierung, Sitzungsverwaltung,",
                    P52_ALTSATZ)


def _52_anker_verlieren(root: str) -> None:
    """Ohne die V6-Zeile hat Pruefung 52 keine Begriffe mehr - sie leitet sie von dort ab."""
    ersetze(P(root, P52_RISIKO),
            ("| V6 | Änderungen an Produktionssystemen",
             "| V6-alt | Änderungen an Produktionssystemen"))


def _52_nur_anwendungslogik(root: str) -> None:
    """Dieselbe Freigabefolge OHNE V6-Gegenstand bleibt zulaessig - das ist G-04."""
    zeile_nach(P(root, P52_CL06),
               "## Abbruch- und Eskalationskriterien",
               "\r\nSondennachtrag: Eine Änderung an Kryptografie oder "
               "Sitzungsverwaltung ist Kontrollstufe hoch; die Umsetzung erfolgt nach "
               "dokumentierter Freigabe durch `<APPROVAL_ROLE>`.")


def _52_ohne_freigabefolge(root: str) -> None:
    """Ein V6-Gegenstand OHNE Freigabefolge bleibt zulaessig - die Regel gilt dem Paar."""
    zeile_nach(P(root, P52_CL06),
               "## Abbruch- und Eskalationskriterien",
               "\r\nSondennachtrag: Eine Sicherheitskonfiguration mit Schutzwirkung ist "
               "Kontrollstufe hoch und nicht delegierbar; zulässig sind Analyse und "
               "Planvorschlag.")


def _52_langform_ausgenommen(root: str) -> None:
    """Die Langform, aus der die Begriffe stammen, darf beide Seiten in einem Absatz nennen.

    Ohne diese Ausnahme meldete die Pruefung ausgerechnet den Text, der die Abgrenzung
    ZIEHT - und die Ausnahme ist abgeleitet: es ist die Datei, aus der gelesen wurde.
    """
    zeile_nach(P(root, P52_RISIKO),
               "## 5. Anwendungshinweise (Erläuterung)",
               "\r\nSondennachtrag zur Abgrenzung: Eine Sicherheitskonfiguration bleibt "
               "V6; eine Berechtigungsprüfung in der Anwendungslogik ist Kontrollstufe "
               "hoch, und ihre Umsetzung erfolgt nach dokumentierter Freigabe.")


sonde("52a", "Ein Gegenstand von V6 in einer Aufzaehlung mit Freigabefolge wird gemeldet "
             "- der Stand vor 0.61.0", _52_altsatz_zurueck, M52_FOLGE)

sonde("52b", "Ohne die V6-Zeile der Delegationsverbotsliste meldet Pruefung 52 den "
             "verlorenen Gegenstand, statt leise zu bestehen", _52_anker_verlieren,
      M52_ANKER)

gegenprobe("52a", "Das unveraenderte Repositorium bleibt unbeanstandet - beide Fassungen "
                  "trennen seit 0.61.0 Anwendungslogik vom Betrieb", None, M52_FOLGE)

gegenprobe("52b", "Dieselbe Freigabefolge ohne einen Gegenstand von V6 bleibt zulaessig - "
                  "das ist der erlaubte Fall", _52_nur_anwendungslogik, M52_FOLGE)

gegenprobe("52c", "Ein Gegenstand von V6 ohne Freigabefolge bleibt zulaessig - die Regel "
                  "gilt dem Paar, nicht dem Wort", _52_ohne_freigabefolge, M52_FOLGE)

gegenprobe("52d", "Die Langform, aus der die Begriffe stammen, bleibt ausgenommen - sie "
                  "zieht die Abgrenzung und nennt beide Seiten", _52_langform_ausgenommen,
           M52_FOLGE)


# --- Pruefung 53: Die Kriterium-2-Kette des Releaseplans (D-153) -------------------
M53_KETTE = "Kette des Releaseplans reißt zwischen"
M53_NULL = "Kette des Releaseplans endet bei"
M53_ANKER = "liest den Releaseplan darunter"
P53_ROADMAP = ".koolie/core/docs/ROADMAP.md".replace("/", os.sep)
P53_UEBERSCHRIFT = "#### Der Releaseplan bis 1.0.0 und darüber hinaus"
# Genau der Fehler, den 0.60.0 gemergt hat: Die Zelle wurde aus dem Posten genommen, seine
# Zahl nachgezogen - und die des Folgepostens blieb stehen.
P53_KETTE_SUCH = "Kriterium 2: **"
P53_GLIED_RE = re.compile(r"Kriterium 2: \*\*(\d+) → (\d+)\*\*")


# 🔴 DER ANKER IST ABGELEITET, NICHT GEPFLEGT - UND DAS ZUM DRITTEN MAL IN DREI
# RELEASES. Bis 0.67.0 stand er hier als feste Zeichenkette ("**85 → 0**"), also auf
# dem Inhalt EINES Postens. 0.63.0 hat dieselbe Bauform schon einmal an Gegenprobe 53b
# behoben und den Fall im Kopfkommentar dort beschrieben - die beiden SONDEN blieben
# gepflegt. Der Umbau des Releaseplans in 0.67.0 (ein Posten wird zu sieben) hat 53a
# prompt fallen lassen: "Praeparation gebrochen".
#     Eine Abhilfe gilt fuer die Stelle, an der sie eingetragen wird, nicht fuer die
#     Bauform. Wer eine findet, sucht ihre Geschwister im selben Block.
def _53_letztes_glied(root: str) -> str:
    """Die LETZTE Kettenzeile des Plans - sie schliesst die Kette und endet bei null."""
    text = lies(P(root, P53_ROADMAP))
    kette = [z for z in text.replace("\r\n", "\n").split("\n")
             if P53_KETTE_SUCH in z and P53_GLIED_RE.search(z)]
    if not kette:
        raise Praeparationsfehler(
            "ROADMAP.md: keine Zeile mit einer Kriterium-2-Kette gefunden - die Sonde "
            "zu 53 haette keinen Anker")
    return kette[-1]


def _53_kette_reissen(root: str) -> None:
    """Der Stand vor 0.61.0: Der Folgeposten beginnt um eins unter dem Vorgaengerende."""
    glied = _53_letztes_glied(root)
    m = P53_GLIED_RE.search(glied)
    kaputt = P53_GLIED_RE.sub(
        "Kriterium 2: **%d → %s**" % (int(m.group(1)) - 1, m.group(2)), glied)
    ersetze(P(root, P53_ROADMAP), (glied, kaputt))


def _53_null_verfehlen(root: str) -> None:
    """Ein Plan, der nicht bei null ankommt, fuehrt nicht bis 1.0.0."""
    glied = _53_letztes_glied(root)
    m = P53_GLIED_RE.search(glied)
    kaputt = P53_GLIED_RE.sub(
        "Kriterium 2: **%s → %d**" % (m.group(1), int(m.group(2)) + 1), glied)
    ersetze(P(root, P53_ROADMAP), (glied, kaputt))


def _53_anker_verlieren(root: str) -> None:
    """Ohne die Ueberschrift liest Pruefung 53 keinen Plan - und sagt es."""
    ersetze(P(root, P53_ROADMAP),
            (P53_UEBERSCHRIFT, "#### Der Plan bis 1.0.0"))


def _53_glied_anfuegen(root: str) -> None:
    """Ein weiterer Posten, der die Kette fortsetzt, bleibt zulaessig.

    Die Pruefung rechnet eine Kette nach und zaehlt keine Posten; ohne dieses Paar waere
    nicht belegt, dass sie dem Plan folgt statt einer festen Laenge.
    """
    # DER ANKER IST ABGELEITET, NICHT GEPFLEGT - und das ist mit 0.63.0 noetig
    # geworden: Er stand zweimal in zwei Releases auf einer Postennummer, und beide
    # Male hat die Verschiebung des Releaseplans die Gegenprobe fallen lassen
    # ("Praeparation gebrochen"). Gesucht wird die LETZTE Zeile der Kette; dahinter
    # gehoert der Sondenposten, damit die Kette geschlossen bleibt.
    text = lies(P(root, P53_ROADMAP))
    kette = [z for z in text.replace("\r\n", "\n").split("\n")
             if P53_KETTE_SUCH in z]
    if not kette:
        raise Praeparationsfehler(
            "ROADMAP.md: keine Zeile mit einer Kriterium-2-Kette gefunden - die "
            "Gegenprobe haette keinen Anker")
    zeile_nach(P(root, P53_ROADMAP), kette[-1].strip(),
               "| **~0.99.0** | Sondenposten | Kriterium 2: **0 → 0** | nein |")


def _53_nennung_vor_dem_plan(root: str) -> None:
    """Eine Kriterium-2-Angabe VOR der Ueberschrift bleibt zulaessig - der Zuschnitt beginnt dort."""
    ersetze(P(root, P53_ROADMAP),
            (P53_UEBERSCHRIFT,
             "Sondennachtrag: Eine Vorhersage ausserhalb des Plans, Kriterium 2: "
             "**99 → 1**.\r\n\r\n" + P53_UEBERSCHRIFT))


sonde("53a", "Ein Folgeposten, der unter dem Ende seines Vorgaengers beginnt, wird "
             "gemeldet - genau der Fehler, den 0.60.0 gemergt hat", _53_kette_reissen,
      M53_KETTE)

sonde("53b", "Ein Plan, dessen Kette nicht bei null ankommt, wird gemeldet - Kriterium 2 "
             "muss dort ankommen", _53_null_verfehlen, M53_NULL)

sonde("53c", "Ohne die Ueberschrift des Releaseplans meldet Pruefung 53 den verlorenen "
             "Gegenstand, statt leise zu bestehen", _53_anker_verlieren, M53_ANKER)

gegenprobe("53a", "Das unveraenderte Repositorium bleibt unbeanstandet - die Kette "
                  "schliesst und endet bei null", None, M53_KETTE)

gegenprobe("53b", "Ein weiterer Posten, der die Kette fortsetzt, bleibt zulaessig - "
                  "gerechnet wird die Kette, nicht die Laenge", _53_glied_anfuegen,
           M53_KETTE)

gegenprobe("53c", "Eine Kriterium-2-Angabe vor der Ueberschrift bleibt zulaessig - der "
                  "Zuschnitt beginnt am Plan", _53_nennung_vor_dem_plan, M53_KETTE)


# --- Pruefung 54: Zusatzschluessel auf der deklarierten Ebene (D-155) --------------
#
# ZWEI ZUSCHNITTE, UND DER ZWEITE IST DER WICHTIGERE. Das Repositorium traegt eine
# devin-desktop-Testinstallation, und dieses Pack fuehrt settings_extra ABSICHTLICH leer.
# Eine Sonde auf der Kopie des Repositoriums belegt deshalb nur die Deklarationspflicht.
# Was der Befund von 0.62.0 verlangt - dass ein Schluessel mit WERT auf der richtigen
# EBENE ankommt -, ist nur an einer claude-code-Installation zu messen. Das ist B02: nicht,
# dass eine Pruefung falsch prueft, sondern dass sie einen Client nicht sieht.
M54_FEHLT_FELD = "Feld settings_extra fehlt"
M54_FEHLT_KEY = "aus settings_extra fehlt in der obersten Ebene"
M54_EBENE = "steht in dem Objekt permissions statt in der obersten Ebene"
M54_WERT = "das Manifest deklariert in settings_extra aber"
MAN_DD_54 = ".koolie/core/clients/devin-desktop/manifest.json".replace("/", os.sep)


def _54_deklaration_fehlt(root: str) -> None:
    """Das Pack fuehrt das Feld gar nicht - der Stand jedes Packs bis 0.61.0."""
    ersetze(P(root, MAN_DD_54), ('  "settings_extra": {},\r\n', ""))


def _54_leeres_feld_bleibt(root: str) -> None:
    """Gegenprobe: Ein leeres settings_extra ist eine Deklaration und bleibt zulaessig.

    Ohne dieses Paar stuende nur fest, dass die Pruefung ein fehlendes Feld meldet - nicht,
    dass sie die ausdrueckliche Abwesenheit von der Luecke unterscheidet. Genau diese
    Unterscheidung ist ihr Zweck.
    """
    ersetze(P(root, MAN_DD_54),
            ('  "settings_extra": {},\r\n',
             '  "settings_extra": {},\r\n  "_sonde_54": "leer ist eine Deklaration",\r\n'))


def _cc_manifest_54(root: str) -> str:
    return os.path.join(root, ".koolie/core", "clients", "claude-code", "manifest.json")


def sonden_zusatzschluessel() -> None:
    """Wirkungsnachweis an einer claude-code-Installation (D-155).

    Gemessen wird an der ERZEUGTEN Datei, nicht am Manifest: Die Pruefung fragt, ob die
    Verschaerfung ankommt, und das entscheidet die Abbildung, nicht die Deklaration.
    """
    root = installation("claude-code")
    try:
        rechte = os.path.join(root, ".claude", "settings.json")
        ausgang = lies(rechte, roh=True)  # von install.py erzeugt, auf jedem Baum LF

        # --- Gegenprobe: die frische Installation traegt den Schluessel --------------
        # Sie ist hier die wichtigere Haelfte: Sie belegt, dass die Abbildung aus
        # 0.62.0 ueberhaupt etwas ausliefert. Ohne sie bewiese jede Sonde nur, dass die
        # Pruefung irgendetwas meldet.
        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "54c", "autoMemoryEnabled" not in aus,
              "Die frische claude-code-Installation traegt autoMemoryEnabled auf der "
              "obersten Ebene und bleibt unbeanstandet")
        if "autoMemoryEnabled" in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "autoMemoryEnabled" in z)[:400])

        # --- 54a: der Schluessel fehlt ganz - der Stand bis 0.61.0 ------------------
        # Die erzeugte Datei ist LF: install.py schreibt LF, git normalisiert. Ein
        # Suchtext mit \r\n traefe hier NICHT - anders als in den Manifest-Sonden, die
        # gegen das CRLF des Repositoriums laufen.
        schreib(rechte, ersetzt(
            ausgang,
            ('  "autoMemoryEnabled": false,\n', ""),
            quelle=".claude/settings.json"))
        melde("SONDE", "54b", M54_FEHLT_KEY in validator_ausgabe(root),
              "Ein deklarierter Zusatzschluessel fehlt in der erzeugten Datei - die "
              "Verschaerfung kommt nicht an")

        # --- 54b: der Schluessel steht auf der FALSCHEN Ebene -----------------------
        # Der eigentliche Gegenstand: Die Datei bleibt gueltiges JSON, der Schluessel ist
        # da, er wird nur nicht gelesen. Bis 0.61.0 haette nichts es gemeldet.
        schreib(rechte, ersetzt(
            ausgang,
            ('  "autoMemoryEnabled": false,\n', ""),
            ('"permissions": {\n    "defaultMode": "default",',
             '"permissions": {\n    "autoMemoryEnabled": false,\n    '
             '"defaultMode": "default",'),
            quelle=".claude/settings.json"))
        melde("SONDE", "54c", M54_EBENE in validator_ausgabe(root),
              "Derselbe Schluessel INNERHALB von permissions - gueltiges JSON, vom "
              "Client nicht gelesen, und die Pruefung nennt die Ebene")

        # --- 54c: der Wert ist ein anderer als der deklarierte ----------------------
        schreib(rechte, ersetzt(
            ausgang,
            ('  "autoMemoryEnabled": false,\n', '  "autoMemoryEnabled": true,\n'),
            quelle=".claude/settings.json"))
        melde("SONDE", "54d", M54_WERT in validator_ausgabe(root),
              "Der Schluessel steht auf der richtigen Ebene und traegt den "
              "entgegengesetzten Wert - eine Verschaerfung, die keine ist")

        schreib(rechte, ausgang)
    finally:
        aufraeumen(os.path.dirname(root))


sonde("54a", "Ein Pack fuehrt settings_extra gar nicht - der Stand jedes Packs bis "
             "0.61.0, und die Abwesenheit war nicht von der Luecke zu unterscheiden",
      _54_deklaration_fehlt, M54_FEHLT_FELD)

gegenprobe("54a", "Das unveraenderte Repositorium bleibt unbeanstandet - beide Packs "
                  "fuehren beide Felder", None, M54_FEHLT_FELD)

gegenprobe("54b", "Ein LEERES settings_extra ist eine Deklaration und bleibt zulaessig - "
                  "die Pruefung trennt die ausdrueckliche Abwesenheit von der Luecke",
           _54_leeres_feld_bleibt, M54_FEHLT_FELD)

buendel(sonden_zusatzschluessel,
        "Pruefung 54 an einer claude-code-Installation: fehlend, falsche Ebene und "
        "falscher Wert je eigens gemessen, dazu die unveraenderte Installation")


# --- Pruefung 55 und 56: Pflichtplatzhalter und gesperrte Traeger (D-160, D-161) ---
#
# ZWEI ZUSCHNITTE, AUS EINEM GRUND: Teil (a) von Pruefung 55 liest die VORLAGE und laeuft
# im gewoehnlichen Lauf. Teil (b) und Pruefung 56 lesen ein GEFUELLTES Overlay - und das
# Repositorium traegt nur die unausgefuellte Vorlage, in der jeder Wert <TBD> ist.
# Deshalb baut das Buendel eine frische Installation und schreibt genau die zwei
# Bindungszeilen hinein, um die es geht. Alles andere an --strict-overlay meldet dort
# ohnehin, und die Sonden pruefen je auf IHRE Meldung, nicht auf die Fehlerzahl.
M55_VORLAGE = "kommt in der Vorlage aber nicht vor"
M55_ANKER = "keine Zeile trägt 'Pflicht vor Aktivierung' = ja"
M55_BINDUNG = "<ISSUE_TRACKER> wird von"
M56_GESPERRT = "das dasselbe Overlay unter <EXCLUDED_PATHS> führt"
P55_REG = ".koolie/core/docs/PLACEHOLDER_REGISTRY.md".replace("/", os.sep)
P55_VOR = ".koolie/core/templates/project-overlay/OVERLAY.md".replace("/", os.sep)


def _55_vorlage_luecke(root: str) -> None:
    """Ein Pflichtplatzhalter verschwindet aus der Vorlage - der Fall vom 2026-09-18."""
    ersetze(P(root, P55_VOR),
            ("| Änderungsschwelle (`CHANGE_SIZE_THRESHOLD`) |",
             "| Änderungsschwelle |"))


def _55_anker_weg(root: str) -> None:
    """Ohne die Pflichtspalte hat Pruefung 55 keinen Gegenstand - und sagt es."""
    p = P(root, P55_REG)
    text = lies(p)
    # NICHT "| ja |": Eine der 29 Zeilen traegt 'ja (oder „keine")', bliebe stehen,
    # und die Pflichtmenge waere nicht leer - die Sonde maesse dann nichts.
    schreib(p, text.replace("| ja", "| spaeter"))


def _55_ohne_overlayort(root: str) -> None:
    """Gegenprobe: Ein Pflichtplatzhalter, den das Register NICHT im Overlay verortet,
    muss in der Vorlage nicht vorkommen. `<FRAMEWORK_OWNER>` wird in OWNERS.md gesetzt -
    ohne diesen Zuschnitt meldete die Pruefung ihn bei jedem Lauf."""
    p = P(root, P55_VOR)
    text = lies(p)
    schreib(p, text.replace("<FRAMEWORK_OWNER>", "<FRAMEWORK-EIGNER>"))


# 🔴 DIE SPITZEN KLAMMERN GEHOEREN HINEIN (K-88, D-257). Bis 0.83.0 schrieb dieser
# Block `ISSUE_TRACKER` OHNE sie und nannte das eine Bindung - er kam damit durch, weil
# Pruefung 55b `if name in text` fragte. **Die Gegenprobe deckte die Luecke der Pruefung,
# und die Pruefung die der Gegenprobe.** Mit der geschaerften Pruefung faellt die alte
# Form, und genau das ist ihr Wirkungsnachweis.
BINDUNGEN = (
    "\n## Sondenabschnitt (nur fuer den Wirkungsnachweis)\n\n"
    "| Element | Platzhalter | Wert |\n|---|---|---|\n"
    "| Ticketsystem | `<ISSUE_TRACKER>` | Beispiel-Ticketsystem |\n"
    "| Merge-Request-Vorlage | `<MR_TEMPLATE_PATH>` | `%s` |\n"
)

# Dieselbe Tabelle in der Form von 0.83.0: der Name OHNE Klammern. Sie ist der
# Gegenstand der Sonde 55d - ein Overlay, das den Platzhalter nennt und nicht bindet.
BINDUNGEN_NUR_GENANNT = BINDUNGEN.replace("`<ISSUE_TRACKER>`", "`ISSUE_TRACKER`")


def _ov(root: str) -> str:
    return os.path.join(root, ".koolie/project-overlay", "OVERLAY.md")


def sonden_platzhalterbindung() -> None:
    """Wirkungsnachweis fuer Pruefung 55b und 56 an einer gefuellten Installation."""
    root = installation("claude-code")
    try:
        pfad = _ov(root)
        ausgang = lies(pfad)
        # Eine ausgeschlossene Pfadmenge, die nicht <TBD> ist - sonst hat 56 keinen Anker.
        gefuellt = ersetzt(
            ausgang,
            ("`<TBD: z. B. deploy/**, infra/**, config/prod/**, **/fixtures/real/**>`",
             "`deploy/**`, `infra/**`"),
            quelle=".koolie/project-overlay/OVERLAY.md")

        # --- Gegenprobe 55: der gebundene Platzhalter wird nicht beanstandet ---------
        schreib(pfad, gefuellt + BINDUNGEN % ".mr/pull_request_template.md")
        aus = strict_ausgabe(root)
        melde("GEGENPROBE", "55c", M55_BINDUNG not in aus,
              "Ein Overlay, das <ISSUE_TRACKER> BINDET, bleibt unbeanstandet - die "
              "Pruefung misst die Bindung, nicht das Vorhandensein eines Werts")

        # --- Gegenprobe 56: derselbe Baum, Vorlage ausserhalb der Sperre -------------
        melde("GEGENPROBE", "56a", M56_GESPERRT not in aus,
              "Liegt der Wert von <MR_TEMPLATE_PATH> ausserhalb von <EXCLUDED_PATHS>, "
              "bleibt die Vorbedingung zulaessig")

        # --- 55b: die Bindung fehlt, der Kerntext nennt den Platzhalter weiter -------
        # Der gemessene Fall ist die ERSETZUNG: Das Overlay nennt den Wert und den
        # Platzhalter nirgends mehr. In einer frischen Installation steht er noch in
        # der Prosa der Vorlage - die muss die Sonde mit entfernen, sonst gilt er als
        # gebunden und sie maesse nichts.
        ohne = gefuellt.replace("`<ISSUE_TRACKER>`", "Beispiel-Ticketsystem")
        schreib(pfad, ohne + (BINDUNGEN % ".mr/pull_request_template.md").replace(
            "| Ticketsystem | `<ISSUE_TRACKER>` | Beispiel-Ticketsystem |\n", ""))
        melde("SONDE", "55c", M55_BINDUNG in strict_ausgabe(root),
              "Das Overlay nennt den Wert, bindet den Platzhalter aber nicht - genau der "
              "Fall, der am 2026-09-18 fuenf Platzhalter in 65 Fundstellen unaufloesbar "
              "liess")

        # --- 56: die Vorbedingung verlangt einen gesperrten Traeger ------------------
        schreib(pfad, gefuellt + BINDUNGEN % "deploy/pull_request_template.md")
        melde("SONDE", "56a", M56_GESPERRT in strict_ausgabe(root),
              "Eine Vorbedingung verlangt <MR_TEMPLATE_PATH>, und dessen Wert liegt "
              "unter einem ausgeschlossenen Pfad - die Zelle ist nicht fahrbar")

        # --- Gegenprobe 56b: die NACHBARDATEI im selben Verzeichnis ---------------
        # Der erste Entwurf von Pruefung 56 verglich nur das erste Pfadsegment und
        # meldete `.github/pull_request_template.md` gegen `.github/workflows/**`.
        # Ohne dieses Paar stuende nur fest, dass die Pruefung einen gesperrten Pfad
        # findet - nicht, dass sie den ungesperrten Nachbarn in Ruhe laesst.
        nachbar = ersetzt(gefuellt, ("`deploy/**`, `infra/**`",
                                     "`deploy/gen/**`, `infra/**`"),
                          quelle=".koolie/project-overlay/OVERLAY.md")
        schreib(pfad, nachbar + BINDUNGEN % "deploy/pull_request_template.md")
        melde("GEGENPROBE", "56b", M56_GESPERRT not in strict_ausgabe(root),
              "Derselbe Pfadanfang, ein anderer Pfad: `deploy/pull_request_template.md` gegen `deploy/gen/**` bleibt zulaessig - die Pruefung vergleicht Pfade, nicht Anfaenge")

        # --- 55d: GENANNT ist nicht GEBUNDEN (K-88, D-257) --------------------------
        # 🔴 DER GEGENBEWEIS GEGEN DEN VORSTAND. Bis 0.83.0 fragte Pruefung 55b
        # `if name in text`; gegen diesen Baum haette sie GESCHWIEGEN, weil die
        # Buchstaben `ISSUE_TRACKER` im Overlay stehen - nur eben ohne die spitzen
        # Klammern, die den Kerntext aufloesen. Am Uebungsrepositorium waren es 14
        # von 26 Pflichtplatzhaltern, und die Pruefung meldete null.
        ohne_klammern = gefuellt.replace("`<ISSUE_TRACKER>`", "Beispiel-Ticketsystem")
        schreib(pfad, ohne_klammern
                + BINDUNGEN_NUR_GENANNT % ".mr/pull_request_template.md")
        melde("SONDE", "55d", M55_BINDUNG in strict_ausgabe(root),
              "Das Overlay NENNT <ISSUE_TRACKER> (ohne spitze Klammern) und bindet ihn "
              "nicht - bis 0.83.0 blieb genau das unbeanstandet (K-88, D-257)")

        # --- Gegenprobe 55d: dieselbe Tabelle MIT Klammern --------------------------
        schreib(pfad, ohne_klammern + BINDUNGEN % ".mr/pull_request_template.md")
        melde("GEGENPROBE", "55d", M55_BINDUNG not in strict_ausgabe(root),
              "Dieselbe Tabelle mit spitzen Klammern bleibt unbeanstandet - die "
              "Pruefung misst die SCHREIBWEISE der Bindung und nicht den Wert daneben")

        schreib(pfad, ausgang)
    finally:
        aufraeumen(os.path.dirname(root))


sonde("55a", "Ein Pflichtplatzhalter fehlt in der Overlay-Vorlage - ein Projekt, das sie "
             "ausfuellt, begegnet ihm nie", _55_vorlage_luecke, M55_VORLAGE)

sonde("55b", "Ohne die Spalte 'Pflicht vor Aktivierung' meldet Pruefung 55 den "
             "verlorenen Gegenstand, statt leise zu bestehen", _55_anker_weg, M55_ANKER)

gegenprobe("55a", "Das unveraenderte Repositorium bleibt unbeanstandet - die Vorlage "
                  "bietet jeden Pflichtplatzhalter an", None, M55_VORLAGE)

gegenprobe("55b", "Ein Pflichtplatzhalter, den das Register NICHT im Overlay verortet, "
                  "muss in der Vorlage nicht stehen", _55_ohne_overlayort, M55_VORLAGE)

buendel(sonden_platzhalterbindung,
        "Pruefung 55b und 56 an einer gefuellten claude-code-Installation: fehlende "
        "Bindung und gesperrter Traeger je eigens gemessen, dazu beide Gegenproben")

"""Die Dokumente: Steuerzeichen, Altname, Dokumentstand und -zahlen, Lizenz,
Gegenzeichnung, Zeilenendeform, Bestandsliste, Chronikspanne, Zielangabe,
Rechtschreibung, Form und Steckbrief.

Pruefungen 66, 75, 77, 78, 79, 80, 81, 82, 83, 85, 92, 93 und 94. Teil des Validators
validate-framework.py, seit 1.19.1 nach Gegenstand in Module geteilt (K-174). Das
Register aller Pruefungen steht im Kopfkommentar des Einstiegs, die Grenze jeder
einzelnen in ihrem Kopfkommentar hier."""
from __future__ import annotations

import os
import re
import subprocess

from .gemeinsam import (
    _git_pfade, _verfolgte_dateien, DOK_WURZEL, err, hinweis, ist_quellrepositorium,
    iter_text_files, KERN, nicht_geliefert, QUELLREPO_KENNZEICHEN, read,
    REGISTER_ANKER, REGISTER_ENDE, tabellenzellen, TBD_RE, TEXT_EXT, warn)


# --- Pruefung 66: das verirrte Steuerzeichen ---------------------------------------
#
# GEGENSTAND ist ein Wagenruecklauf, dem kein Zeilenvorschub folgt. Er rendert nicht,
# er druckt nicht, und keine Leseroutine dieses Apparats gibt ihn heraus.
#
# 🔴 WARUM ER TROTZDEM ETWAS KAPUTT MACHT (D-217, CR-2026-107): git stuft einen
# Traeger mit einem einzelnen CR als BINAER ein und normalisiert seine Zeilenenden
# deshalb NICHT - weder ueber core.autocrlf noch ueber ein text=auto in einer
# .gitattributes. Gemessen am 2026-09-20 in einem eigens dafuer gebauten
# Repositorium, beide Faelle nebeneinander: Die Datei ohne verirrtes CR liegt danach
# als LF im Blob, die mit ihm unveraendert als CRLF.
# ➡️ DIE REGEL FUER ZEILENENDEN GREIFT BEI GENAU DEN DATEIEN NICHT, DIE SIE BRAUCHEN.
# Im Bestand war die Deckung vollstaendig: 14 Traeger mit verirrtem CR und 14 Traeger,
# deren Blob git nicht normalisiert hat - dieselben 14 von 440 Texttraegern.
#
# 🔴 UND KEINE DER 65 AELTEREN PRUEFUNGEN KONNTE ES SEHEN. `read` oeffnet im
# Universal-Newline-Modus; dort ist jedes CR bereits ein Zeilenvorschub, bevor eine
# Pruefung es zu Gesicht bekommt. Diese liest deshalb Bytes. Eine Pruefung, die ihren
# Gegenstand an der eigenen Leseroutine verliert, ist die stillste Bauform von D-23.
VERIRRTES_CR = re.compile(bytes([13]) + b'(?!' + bytes([10]) + b')')


def check_verirrtes_steuerzeichen(root: str) -> None:
    """Pruefung 66 (D-217): Kein Textraeger traegt ein CR ohne folgenden LF."""
    geprueft = 0
    for path in iter_text_files(root):
        try:
            with open(path, "rb") as fh:
                roh = fh.read()
        except OSError:
            continue
        if b"\x00" in roh[:8000]:
            continue
        geprueft += 1
        treffer = VERIRRTES_CR.findall(roh)
        if not treffer:
            continue
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        stelle = VERIRRTES_CR.search(roh).start()
        err(f"{rel}: {len(treffer)} verirrte(s) Steuerzeichen - Wagenrücklauf ohne "
            f"folgenden Zeilenvorschub, das erste an Byte {stelle}. Es ist unsichtbar "
            f"und nimmt git die Normalisierung: Ein solcher Träger gilt als binär, "
            f"landet unverändert im Repositorium und lässt den nächsten Commit die "
            f"ganze Datei neu schreiben (D-217)")
    if not geprueft:
        err(f"{KERN}/: keine einzige Textdatei gelesen – Prüfung 66 hat ihren "
            f"Gegenstand verloren und bestünde sonst leise (D-23)")

# --- Pruefung 75: Kein Restbestand des alten Namens ---------------------------------
#
# ANLASS (D-271, CR-2026-119 E3). Mit 0.88.0 heisst das Framework Koolie und der Kern
# liegt unter .koolie/core. Ohne eine Pruefung ist "der Name ist weg" eine BEHAUPTUNG
# ohne Pruefung - und genau das ist der wiederkehrende Befundtyp dieses Repositoriums.
#
# ZAEHLBEREICH, UND ER HAENGT DAVON AB, WESSEN BESTAND GEPRUEFT WIRD.
#
#   * Im FRAMEWORK-REPOSITORIUM: jeder verfolgte Traeger. Das ist die Lehre von D-295 -
#     der Zaehlbereich von Kriterium 1 war kleiner als die Wirkungsflaeche, und wer nur
#     den Kern sweept, laesst die Form in der Wurzel-README stehen.
#   * In einem UEBERNEHMENDEN PROJEKT: nur, was das Framework AUSLIEFERT - der Kern und
#     die Laufzeitschicht. Was ein Projekt in seine eigenen Dateien schreibt, geht das
#     Framework nichts an; es darf eine Belegablage nennen, die den alten Namen traegt.
#     Gemessen am 2026-09-22 im Uebungsrepositorium: zwei solche Nennungen, beide
#     legitim nach D-300, und die Pruefung meldete sie als Fehler (D-299).
#
# ERKANNT WIRD DAS AM KENNZEICHEN DES QUELLREPOSITORIUMS (D-351). Bis 1.4.0 war es
# die Uebergabe; seit sie nicht mehr versioniert ist (D-350), traegt eine eigene
# Datei den Anker. Sie wandert NICHT in ein Zielprojekt; `install.py` legt sie nicht
# an, und das Update kopiert nur den Kern. Ein Anker, der sich selbst belegt.
# ➡️ Eine Pruefung, die im Framework gruen und in jeder Installation rot ist, ist
#    falsch gebaut - dieselbe Ueberlegung, mit der Pruefung 46 ihren Zaehlbereich auf
#    den Kern beschraenkt: Was nicht in jeder Installation gleich ist, gehoert nicht in
#    eine installationsunabhaengige Aussage.
#
# AUSGENOMMEN, UND ZWAR DEKLARIERT (dieselbe Bauform wie P73_OFFEN und LINK_EXCEPTIONS):
#
#   (a) DIE CHRONIK. Protokolle, Aenderungsantraege, CHANGELOG und Decision Log
#       beschreiben einen vergangenen Zustand (D-125, D-273). Ein Pfad, den es nicht
#       mehr gibt, ist dort richtig - er hat damals existiert.
#   (b) NAMEN DATIERTER BELEGABLAGEN AUSSERHALB DES REPOSITORIUMS. Die Erhebungen
#       heissen `leitwerk-erhebungen-<datum>-<buendel>` und werden NICHT umbenannt:
#       Eine Reihe von Belegablagen, deren Namenskonvention mitten in der Reihe
#       wechselt, ist nicht mehr als Reihe auffindbar (D-300).
#   (c) AUSSAGEN UEBER DEN ALTEN NAMEN. Der Changelog-Eintrag zu 0.7.0, die
#       Entscheidungsaufzeichnung im Releaseplan und die Kommentare, die erklaeren,
#       warum eine Stelle umgebaut wurde. Ein Sweep kehrt sie ins Sinnlose - das war
#       der teuerste Befund des Umbenennungslaufs (D-301).
#   (d) DER PRUEFAPPARAT DIESER PRUEFUNG SELBST. Dieser Validator traegt das Muster,
#       und probe-pruefungen.py SCHREIBT den alten Namen in den Sondenbaum, um die
#       Pruefung ueberhaupt messen zu koennen. Die Klasse ist strukturell
#       unvermeidbar: Eine Pruefung, die einen Namen sucht, muss ihn nennen - und ihre
#       Sonde muss ihn schreiben. Beide Traeger sind beim ersten Lauf dieser Pruefung
#       aufgefallen, weil sie sich selbst gemeldet hat.
#
# IN BEIDE RICHTUNGEN GEPRUEFT. Ein nicht gelisteter Traeger mit Fundstelle faellt auf,
# ein gelisteter OHNE Fundstelle ebenso: Eine Ausnahme, die nichts mehr ausnimmt, sieht
# wie Sorgfalt aus und ist toter Code (0.57.1).
#
# PREIS, UND ER IST BENANNT: Die Ausnahme gilt je TRAEGER, nicht je Zeile. Eine neue,
# falsche Nennung in einem gelisteten Traeger faellt nicht auf. Die Gegenseite waere
# eine Zahl je Traeger - und eine Zahl, die gepflegt werden muss, wird nicht gepflegt
# (zweimal an derselben Tabelle dieses Projekts belegt).
#
# DER PREIS IST BEIM ERSTEN LAUF ANGEFALLEN, an der Chronik statt an der Ausnahmemenge:
# CHANGELOG.md fuehrt in Zeile 3 den Satz "Prozess: <pfad>/RELEASE_PROCESS.md", und
# tests/protocols/README.md nennt in Zeile 3 den Testkatalog. Beides sind KOPFZEILEN,
# die einen AKTUELLEN Pfad nennen - keine Chronik -, und die Chronikausnahme deckt sie
# mit. Beide sind von Hand nachgezogen worden.
# ➡️ Ein Chroniktraeger kann eine Zeile fuehren, die keine Chronik ist. Wer eine
#    Ausnahme je Traeger zieht, liest den KOPF des Traegers, bevor er sie zieht.
P75_ALTNAME = re.compile(r"(?i)leitwerk")

P75_CHRONIK = (
    KERN + "/CHANGELOG.md",
    KERN + "/governance/DECISION_LOG.md",
    KERN + "/governance/change-requests/",
    KERN + "/tests/protocols/",
)

P75_AUSNAHMEN = {
    # (b) Namen datierter Belegablagen ausserhalb des Repositoriums
    KERN + "/tests/erhebungen/README.md",
    KERN + "/tests/erhebungen/ablage.py",
    KERN + "/tests/erhebungen/baeume-b4.py",
    KERN + "/tests/erhebungen/umgebungen-bauen-b4.py",
    KERN + "/tests/scripts/validate-framework.py",
    KERN + "/tests/scripts/pruefungen/hooks.py",
    # (c) Aussagen ueber den alten Namen
    KERN + "/build/doc/32-abschluss.md",
    KERN + "/clientmap.py",
    # (d) Der Pruefapparat dieser Pruefung selbst - seit 1.19.1 in den Modulen, die
    #     ihr Muster und ihre Sonden tragen (K-174)
    KERN + "/tests/scripts/pruefungen/dokumente.py",
    KERN + "/tests/scripts/sonden/teil08_pruefungen_66_bis_80.py",
}


def _p75_chronik(rel: str) -> bool:
    return any(rel == c or rel.startswith(c) for c in P75_CHRONIK)


def _p75_verfolgt(root: str) -> list | None:
    """Alle verfolgten Pfade des Repositoriums - oder None, wenn nicht messbar.

    Nicht _verfolgte_dateien(): die liest nur unter KERN, und der Zaehlbereich dieser
    Pruefung ist ausdruecklich groesser (D-295).
    """
    try:
        lauf = subprocess.run(["git", "-C", root, "ls-files", "-z"],
                              capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if lauf.returncode != 0:
        return None
    return _git_pfade(lauf.stdout)


def check_altname_restbestand(root: str, man: dict) -> None:
    """Pruefung 75 (D-271): Kein Traeger nennt den alten Namen ausser den erklaerten."""
    if not P75_ALTNAME.search("LeItWeRk"):
        err("Prüfung 75: das eigene Muster findet den alten Namen nicht mehr – sie "
            "bestünde leise und meldete jede Umbenennung als vollständig (D-23)")
        return
    dateien = _p75_verfolgt(root)
    if dateien is None:
        warn("Prüfung 75: kein Git-Bestand lesbar – der Restbestand des alten Namens "
             "ist an diesem Ort nicht prüfbar. Das ist KEIN Messergebnis (D-23)")
        return
    bestand = set(dateien)
    # Das Framework-Repositorium fuehrt das Kennzeichen; ein uebernehmendes Projekt
    # nicht (D-351). Gelesen am VERSIONIERTEN Bestand, wie der Zaehlbereich selbst.
    eigenes_repo = QUELLREPO_KENNZEICHEN in bestand
    ausgeliefert = tuple(
        d + "/" for d in (KERN, man.get("runtime_dir", "")) if d) + tuple(
        f for f in (man.get("root_instruction_file", ""),) if f)
    gefunden = set()
    for rel in sorted(bestand):
        if _p75_chronik(rel):
            continue
        if not eigenes_repo and not rel.startswith(ausgeliefert):
            continue
        if os.path.splitext(rel)[1] not in TEXT_EXT:
            continue
        pfad = os.path.join(root, *rel.split("/"))
        if not os.path.isfile(pfad):
            continue
        treffer = P75_ALTNAME.findall(read(pfad))
        if not treffer:
            continue
        gefunden.add(rel)
        if rel in P75_AUSNAHMEN:
            continue
        err(f"{rel}: nennt den alten Namen noch {len(treffer)}mal. Das Framework heißt "
            f"seit 0.88.0 Koolie, der Kern liegt unter {KERN} (D-271). Steht die Nennung "
            f"dort mit Grund – eine Aufzeichnung, ein Belegablagenname –, gehört der "
            f"Träger als MENGE in P75_AUSNAHMEN und wird nicht als Einzelfall "
            f"durchgelassen")
    for rel in sorted(P75_AUSNAHMEN - gefunden):
        # EIN TRAEGER, DEN DIESE INSTALLATION NICHT FUEHRT, IST KEINE LEERE AUSNAHME.
        # Die Menge beschreibt den Bestand des Framework-Repositoriums; ein
        # uebernehmendes Projekt hat einen anderen - es fuehrt kein Kennzeichen, und
        # sein Kern ist erst nach dem ersten `git add` verfolgt. Ohne diese
        # Unterscheidung waere die Pruefung im Framework gruen und in JEDER
        # Installation rot; gemessen am 2026-09-22 im Uebungsrepositorium, mit neun
        # Meldungen (D-299). Pruefung 46 loest denselben Anspruch mit demselben
        # Gedanken: Was nicht in jeder Installation gleich ist, gehoert nicht in eine
        # installationsunabhaengige Aussage.
        if rel not in bestand:
            continue
        err(f"P75_AUSNAHMEN führt '{rel}' als erklärte Fundstelle des alten Namens – "
            f"dort steht er nicht mehr. Die Ausnahme nimmt nichts mehr aus und "
            f"gehört entfernt (0.57.1)")


# ---------------------------------------------------------------------------
# Pruefung 77: Das Hauptdokument nennt den Stand, auf dem es gebaut ist
# ---------------------------------------------------------------------------
#
# Sie war die Schwester der mit 1.4.1 entfallenen Pruefung 67 (D-350). Dort hielt die
# Titelzeile der Uebergabe gegen VERSION, hier die Kopfzeile des Hauptdokuments - und
# der Unterschied war, dass die Uebergabe jede Sitzung gelesen wurde und das
# Hauptdokument nur zur Auslieferung.
# Genau deshalb ist es zweiundvierzig Releases zurueckgefallen, ohne dass es jemandem
# aufgefallen waere.
#
# WARUM DIE QUELLE UND NICHT DAS ERZEUGNIS. build/out/hauptdokument.md steht in der
# .gitignore und ist in einer frischen Auscheckung gar nicht da; eine Pruefung dagegen
# waere in jeder Installation rot. Der Gegenstand ist die KAPITELQUELLE, und die ist
# versioniert - derselbe Gedanke wie bei Pruefung 46 und 75.
DOKUMENT_KOPF = KERN + "/build/doc/00-kopf.md"
DOKUMENT_VERSION_RE = re.compile(
    r"^\|\s*Dokumentversion\s*\|\s*(\d+\.\d+\.\d+)\s*"
    r"\(entspricht Framework-Release\s*(\d+\.\d+\.\d+)\)\s*\|", re.M)


def check_dokumentstand(root: str) -> None:
    """Pruefung 77 (D-312): Das Hauptdokument steht auf dem Stand des Kerns."""
    pfad = os.path.join(root, *DOKUMENT_KOPF.split("/"))
    if not os.path.isfile(pfad) and nicht_geliefert(root, DOKUMENT_KOPF):
        hinweis(f"Prüfung 77 ohne Gegenstand: {DOKUMENT_KOPF} gehört zur Nachweisschicht "
                f"und ist nicht geliefert (D-367)")
        return
    if not os.path.isfile(pfad):
        err(f"{DOKUMENT_KOPF}: fehlt. Prüfung 77 hält dort die Dokumentversion gegen "
            f"{KERN}/VERSION; ohne den Träger hat sie ihren Gegenstand verloren (D-312)")
        return
    vpfad = os.path.join(root, KERN, "VERSION")
    if not os.path.isfile(vpfad):
        return  # Pruefung 1 meldet die fehlende Pflichtdatei bereits
    stand = read(vpfad).strip()
    m = DOKUMENT_VERSION_RE.search(read(pfad))
    if not m:
        err(f"{DOKUMENT_KOPF}: keine Zeile der Form "
            f"`| Dokumentversion | X.Y.Z (entspricht Framework-Release X.Y.Z) |`. "
            f"Prüfung 77 hält sie gegen {KERN}/VERSION und bestünde ohne sie leise – "
            f"genau der Zustand, in dem das Dokument 42 Releases zurückgefallen ist "
            f"(D-312, D-23)")
        return
    dokument, genannt = m.group(1), m.group(2)
    if dokument != genannt:
        err(f"{DOKUMENT_KOPF}: die Kopfzeile nennt die Dokumentversion {dokument} und "
            f"das Framework-Release {genannt}. Die Zeile sagt aus, dass beide "
            f"übereinstimmen; nennt sie zwei Werte, lässt sie offen, auf welchem Stand "
            f"das Dokument gebaut ist (D-312)")
        return
    if dokument != stand:
        err(f"{DOKUMENT_KOPF}: die Kopfzeile nennt den Stand {dokument}, "
            f"{KERN}/VERSION führt {stand}. Das Hauptdokument wird aus diesem "
            f"Repositorium assembliert und hat keinen eigenen Stand; eine abweichende "
            f"Zahl behauptet einen Bau, den es nicht gegeben hat (D-312)")


# ---------------------------------------------------------------------------
# Pruefung 78: Die zaehlbaren Aussagen des Hauptdokuments (CR-2026-125, D-315)
# ---------------------------------------------------------------------------
#
# ANLASS, UND ER IST DAS RELEASE DAVOR. 0.89.0 hat das Hauptdokument nach ZWEIUNDVIERZIG
# Releases auf den geltenden Stand gesetzt und dabei vierzehn stehengebliebene Zahlen
# berichtigt. Sein eigenes Protokoll schreibt den Grund auf:
#     "Das ist die Bauform von Pruefung 40 an einem groesseren Gegenstand - und der
#      Grund, warum die Behebung eine PRUEFUNG braucht und nicht nur eine Textaenderung."
# Gebaut wurde dann Pruefung 77, und die misst die VERSION, nicht den INHALT. Gemessen am
# 2026-09-23, EIN Release spaeter: Der Satz in 26-qs-test.md nannte "76 Pruefungen ueber
# 502 versionierte Dateien, davon 450 Markdown-Dateien". Richtig waren 77, 504 und 452 -
# und die beiden Dateien, die fehlten, waren der Antrag und das Protokoll DESSELBEN
# Releases. DREI ZAHLEN IN EINEM SATZ, UEBERHOLT IM RELEASE, DAS DAS DOKUMENT AUF DEN
# GELTENDEN STAND GESETZT HAT.
#
# DIE BAUFORM IST DIE VON PRUEFUNG 40: den Satz AUSRECHNEN und woertlich verlangen. Ein
# Vergleich einzelner Zahlen liesse offen, in welchem Satz sie stehen; ein woertlicher
# Sollsatz sagt zugleich, wie er zu schreiben ist.
#
# ZUSCHNITT, UND ER IST DER GANZE PUNKT (D-318): Diese Pruefung gilt der GEGENWARTSFORM.
# "Der Validator fuehrt 79 Pruefungen" ist eine Aussage ueber jetzt und veraltet.
# "Gezaehlt am 2026-09-22: 312 Decision Records" ist eine DATIERTE Aussage und veraltet
# nie - sie muss nur fuer ihr Datum stimmen. Die datierten Zahlen stehen in 29-grenzen.md
# und 32-abschluss.md, beide ausgewiesene Zeitdokumente (D-273, D-311), und werden hier
# ausdruecklich NICHT geprueft. Eine Pruefung, die ein Zeitdokument fortzuschreiben
# verlangt, hat seinen Zweck nicht verstanden.
#
# GRENZE, benannt: Sie misst DREI Zahlen in EINEM Satz. Jede andere Zahl des Dokuments
# laeuft weiter durch - das ist der Rest von K-104, und er ist nicht kleiner geworden,
# nur gezaehlt.
#
# ZWEITER GEGENSTAND VON 1.0.0 BIS 1.4.0 (D-325): DIE ABNAHMEZEILE DER UEBERGABE.
# ENTFALLEN mit 1.4.1 (D-350) - die Uebergabe ist nicht mehr versioniert, und eine
# Pruefung gegen einen Traeger, den eine frische Auscheckung nicht fuehrt, liefe nur
# an einem Arbeitsplatz. Die Lehre bleibt stehen, weil sie ueber die Uebergabe
# hinausreicht: WER EINE ZAHL PRUEFT, SUCHT IHRE ZWEITE FUNDSTELLE (D-295).
#
# ENTHALTUNG: Ein uebernehmendes Projekt fuehrt das Kennzeichen des
# Quellrepositoriums nicht (D-351). Dort enthaelt sich die ganze Pruefung (D-326).
P78_TRAEGER = KERN + "/build/doc/26-qs-test.md"
P78_ANKER = "Der Validator führt **"
P78_SATZ = ("Der Validator führt **{0} Prüfungen** über {1} versionierte Dateien des "
            "Kerns, davon {2} Markdown-Dateien")


def check_dokumentzahlen(root: str) -> None:
    """Pruefung 78 (D-315): Die Gegenwartszahlen des Hauptdokuments gegen den Bestand."""
    # 🔴 ENTHALTUNG IM UEBERNEHMENDEN PROJEKT (D-326, gemessen am 2026-09-23).
    # Der Satz beschreibt den Bestand des FRAMEWORK-Repositoriums und wird byte-gleich
    # ausgeliefert (D-25). Ein uebernehmendes Projekt fuehrt weniger Kerndateien - beim
    # ersten Lauf dieser Pruefung gegen eines waren es 500 gegen 515 -, und es pflegt den
    # Traeger nicht. Ohne diese Unterscheidung waere sie im Framework gruen und in JEDER
    # Installation rot; das ist der Konstruktionsfehler aus D-299, und die Lehre stand im
    # SELBEN Release, das diese Pruefung gebaut hat.
    if not ist_quellrepositorium(root):
        return
    pfad = os.path.join(root, *P78_TRAEGER.split("/"))
    if not os.path.isfile(pfad):
        err(f"{P78_TRAEGER}: fehlt. Prüfung 78 hält dort die zählbaren Aussagen des "
            f"Hauptdokuments gegen den Bestand (D-315)")
        return
    text = read(pfad)
    # --- Gegenstand 1: der Anker ---------------------------------------------------
    if text.count(P78_ANKER) != 1:
        err(f"{P78_TRAEGER}: der Satz über den Prüfapparat steht nicht genau einmal "
            f"(gesucht: '{P78_ANKER}', gefunden: {text.count(P78_ANKER)}x). Prüfung 78 "
            f"hat ihren Gegenstand verloren und bestünde sonst leise (D-23)")
        return
    # --- Gegenstand 2: die Zahl der Pruefungen --------------------------------------
    vpfad = os.path.join(root, KERN, "tests", "scripts", "validate-framework.py")
    if not os.path.isfile(vpfad):
        return  # Pruefung 40 meldet den verlorenen Traeger bereits
    doc = read(vpfad)
    doc = doc.split('"""')[1] if doc.count('"""') >= 2 else ""
    if REGISTER_ANKER not in doc or REGISTER_ENDE not in doc:
        return  # Pruefung 40 meldet das verlorene Register bereits
    liste = doc.split(REGISTER_ANKER, 1)[1].split(REGISTER_ENDE, 1)[0]
    gefuehrt = sorted({int(n) for n in re.findall(r"^\s{0,2}(\d+)[a-z]?\. ", liste, re.M)})
    if not gefuehrt:
        return  # ebenfalls Pruefung 40
    # --- Gegenstand 3: der Bestand ---------------------------------------------------
    dateien = _verfolgte_dateien(root)
    if dateien is None:
        warn("Prüfung 78: kein Git-Bestand lesbar – die Zahl der versionierten Dateien "
             "ist an diesem Ort nicht prüfbar. Das ist KEIN Messergebnis (D-23)")
        return
    soll = P78_SATZ.format(gefuehrt[-1], len(dateien),
                           sum(1 for d in dateien if d.endswith(".md")))
    if soll not in text:
        err(f"{P78_TRAEGER}: der Satz über den Prüfapparat nennt nicht die gezählten "
            f"Werte. Erwartet wörtlich: '{soll}'. Gezählt wurden {gefuehrt[-1]} "
            f"Prüfungen im Register, {len(dateien)} versionierte Dateien unter {KERN}/ "
            f"und {sum(1 for d in dateien if d.endswith('.md'))} davon als Markdown. "
            f"Bis 0.89.0 standen hier 76, 502 und 450 – alle drei waren in DEM Release "
            f"überholt, das das Dokument auf den geltenden Stand gesetzt hat (D-315)")


# ---------------------------------------------------------------------------
# Pruefung 79: Die Lizenz liegt an zwei Stellen und ist dieselbe (CR-2026-126, D-317)
# ---------------------------------------------------------------------------
#
# ZWEI STELLEN, UND BEIDE WERDEN GEBRAUCHT: Die Wurzel, weil die Hostingdienste die
# Lizenz dort suchen und ein Repositorium ohne erkannte Lizenz als "alle Rechte
# vorbehalten" gilt. Der Kern, weil ein uebernehmendes Projekt ihn ALS GANZES kopiert
# (docs/ADOPTION_GUIDE.md Schritt 2) - eine Lizenzdatei, die nur in der Wurzel liegt,
# wandert dabei nicht mit, und ein Werk ohne seine Lizenz weiterzugeben ist nach
# §4 GPL-3.0 unzulaessig.
#
# WARUM DAS EINE PRUEFUNG BRAUCHT: Zwei Stellen mit demselben Inhalt laufen auseinander,
# sobald eine von beiden angefasst wird. Das ist in diesem Repositorium der haeufigste
# Befundtyp, und die Antwort darauf ist dieselbe wie bei Pruefung 76: nicht "bitte beide
# pflegen", sondern ein Vergleich, der meldet.
#
# GRENZE, benannt: Sie vergleicht die beiden Dateien MITEINANDER und prueft, dass es die
# GPL-3.0 ist. Sie prueft nicht, ob der Text der amtlichen Fassung der Free Software
# Foundation entspricht - dafuer waere ein Netzzugriff noetig, und eine Pruefung, die
# das Netz braucht, ist in einer Installation nicht fahrbar.
#
# 🔴 BERICHTIGT MIT 1.0.0 (D-326, CR-2026-128 B14): DIE WURZELFASSUNG GILT NUR IM
# FRAMEWORK-REPOSITORIUM. Gemessen am 2026-09-23 beim ersten Lauf dieser Pruefung gegen
# ein uebernehmendes Projekt: Sie meldete "LICENSE: fehlt" - und verlangte damit von
# JEDEM uebernehmenden Projekt eine GPL-3.0 in SEINER Wurzel.
# 🔴 DAS WAERE DAS GEGENTEIL DESSEN, WAS DIESELBE ENTSCHEIDUNG WOLLTE: Die
# Zusatzerlaubnis nach §7 (D-317, Abschnitt 2 des Lizenzhinweises) nimmt die Ausgaben
# und ausgefuellten Vorlagen ausdruecklich AUS der GPL heraus, damit ein Projekt nicht
# zur Offenlegung gezwungen wird. Eine Pruefung, die dem Projekt die GPL in die Wurzel
# schreibt, hebt genau das wieder auf.
# ➡️ EINE PRUEFUNG, DIE IM FRAMEWORK GRUEN UND IN JEDER INSTALLATION ROT IST, IST FALSCH
#    GEBAUT (D-299) - und die Lehre stand im SELBEN Release, das diese Pruefung gebaut
#    hat: "Jede neue Pruefung laeuft einmal gegen ein uebernehmendes Projekt, bevor sie
#    als fertig gilt." Sie ist notiert und nicht angewandt worden.
#
# ZUSCHNITT seit 1.0.0: Im uebernehmenden Projekt gilt allein die KERNFASSUNG - sie ist
# die, die nach §4 GPL-3.0 mitwandern muss. Die Wurzel gehoert dem Projekt.
P79_WURZEL = "LICENSE"
P79_KERN = KERN + "/LICENSE"
P79_MARKE = "GNU GENERAL PUBLIC LICENSE"
P79_VERSION = "Version 3, 29 June 2007"


def check_lizenz(root: str) -> None:
    """Pruefung 79 (D-317): Die Lizenz liegt an beiden Stellen und ist dieselbe."""
    # Das Framework-Repositorium fuehrt das Kennzeichen; ein uebernehmendes Projekt
    # nicht (D-351). Dort gilt allein die Kernfassung - die Wurzel gehoert dem
    # Projekt (D-326).
    eigenes_repo = ist_quellrepositorium(root)
    stellen = (P79_WURZEL, P79_KERN) if eigenes_repo else (P79_KERN,)
    inhalte = {}
    for rel in stellen:
        pfad = os.path.join(root, *rel.split("/"))
        if not os.path.isfile(pfad):
            err(f"{rel}: fehlt. Die Lizenz MUSS an beiden Stellen liegen – in der Wurzel "
                f"für die Erkennung durch die Hostingdienste, im Kern, weil ein "
                f"übernehmendes Projekt ihn als Ganzes kopiert und die Lizenz sonst nicht "
                f"mitwandert (§4 GPL-3.0, D-317)")
            return
        with open(pfad, "rb") as fh:
            inhalte[rel] = fh.read()
    if not eigenes_repo:
        # Kein Vergleich moeglich und keiner noetig: Was mitwandern muss, ist da.
        text = inhalte[P79_KERN].decode("utf-8", "replace")
        if P79_MARKE not in text or P79_VERSION not in text:
            err(f"{P79_KERN}: trägt nicht die GNU General Public License Version 3 "
                f"(gesucht: '{P79_MARKE}' und '{P79_VERSION}'). Der Kern wandert mit "
                f"seiner Lizenz oder gar nicht (§4 GPL-3.0, D-317, D-326)")
        return
    if inhalte[P79_WURZEL] != inhalte[P79_KERN]:
        err(f"{P79_KERN}: trägt nicht denselben Inhalt wie {P79_WURZEL} "
            f"({len(inhalte[P79_WURZEL])} gegen {len(inhalte[P79_KERN])} Bytes). Zwei "
            f"Lizenzdateien mit verschiedenem Inhalt lassen offen, welche gilt – und für "
            f"ein übernehmendes Projekt gilt die aus dem Kern (D-317)")
        return
    text = inhalte[P79_WURZEL].decode("utf-8", "replace")
    if P79_MARKE not in text or P79_VERSION not in text:
        err(f"{P79_WURZEL}: trägt nicht die GNU General Public License Version 3 "
            f"(gesucht: '{P79_MARKE}' und '{P79_VERSION}'). Prüfung 79 hätte sonst nur "
            f"belegt, dass zwei Dateien gleich sind – auch zwei leere sind das (D-23)")


# ---------------------------------------------------------------------------
# Pruefung 80: Jedes Abnahmeprotokoll traegt seine Gegenzeichnung (CR-2026-127, D-319)
# ---------------------------------------------------------------------------
#
# ANLASS. AP11 verlangte die Gegenzeichnung der Protokolle. 0.89.0 hat sie nicht
# gefahren und den Grund als ABGRENZUNG aufgeschrieben: Eine Gegenzeichnung ist die
# Handlung einer ZWEITEN ROLLE, und ein Werkzeug, das <TBD: Rolle> ersetzt, faelscht
# sie. Das traegt - und es hatte eine Folge, die niemand benannt hatte: An diesem
# Framework arbeitet EINE Person. Die Pflicht war in ihrer damaligen Form nicht
# erfuellbar, und zwar konstruktiv. Das ist die Bauform "die Regel mit leerer
# Schnittmenge" (D-189, K-72) an einer GOVERNANCE-Regel statt an einer Testzelle.
#
# DER ZUSCHNITT IST DIE HALBE ENTSCHEIDUNG (D-319). Nicht jedes Protokoll ist eine
# Abnahme: Von 125 sind die meisten Arbeits- und Messprotokolle, die ihren Beleg in
# sich tragen. Eine Gegenzeichnung sagt etwas anderes - eine zweite Person hat geprueft
# und steht dafuer ein. Gemessen am 2026-09-23 ueber BEIDE Zaehlregeln: Der Gesamtbestand
# ergibt 17/47/61 oder 13/45/64, je nach Regel; die ZEHN Abnahmeprotokolle ergeben
# 3/2/5 unter BEIDEN. Ein Gegenstand, der unter zwei Regeln derselbe ist, ist der
# richtige Gegenstand.
#
# WAS SIE PRUEFT UND WAS NICHT. Sie prueft, dass der Abschnitt DA ist und kein offenes
# <TBD> mehr traegt. Sie prueft NICHT, ob jemand wirklich gelesen hat - das kann kein
# Skript, und deshalb steht neben der Zeile der Commit: Die Zeile sagt, WAS
# gegengezeichnet wurde, der Commit sagt, WER. Eine Unterschrift, die ein Werkzeug
# erzeugen kann, belegt nichts; diese Pruefung erzeugt keine, sie verlangt eine.
#
# GRENZE, benannt: Sie erkennt ein Abnahmeprotokoll am DATEINAMEN. Ein Protokoll, das
# anders heisst, laeuft durch - dieselbe Ehrlichkeit wie bei Pruefung 48, die Pfade
# findet und keine Prosa.
P80_ABLAGE = KERN + "/tests/protocols"
P80_NAME = re.compile(r"^\d{4}-\d{2}-\d{2}-FW-[A-Z]{2}-\d{2}[\w.-]*\.md$")
P80_ABSCHNITT = re.compile(r"^#{1,6}\s.*Gegenzeichnung", re.M | re.I)


def check_gegenzeichnung(root: str) -> None:
    """Pruefung 80 (D-319): Abnahmeprotokolle tragen ihre Gegenzeichnung."""
    ablage = os.path.join(root, *P80_ABLAGE.split("/"))
    if not os.path.isdir(ablage) and nicht_geliefert(root, P80_ABLAGE):
        hinweis(f"Prüfung 80 ohne Gegenstand: {P80_ABLAGE}/ gehört zur Nachweisschicht "
                f"und ist nicht geliefert (D-367)")
        return
    if not os.path.isdir(ablage):
        err(f"{P80_ABLAGE}/: fehlt. Prüfung 80 hält dort die Gegenzeichnung der "
            f"Abnahmeprotokolle; ohne die Ablage hat sie ihren Gegenstand verloren "
            f"(D-319)")
        return
    # --- Gegenstand 1: der Anker ---------------------------------------------------
    kandidaten = sorted(n for n in os.listdir(ablage) if P80_NAME.match(n))
    if not kandidaten:
        err(f"{P80_ABLAGE}/: kein einziges Abnahmeprotokoll des Testkatalogs gefunden "
            f"(Muster `JJJJ-MM-TT-FW-<Klasse>-<NN>.md`). Prüfung 80 hätte nichts zu "
            f"prüfen und bestünde leise – genau der Zustand, aus dem die Pflicht "
            f"zweiundzwanzig Releases lang unbemerkt offen war (D-23, D-319)")
        return
    # --- Gegenstand 2: Abschnitt vorhanden und ohne offenes <TBD> -------------------
    for name in kandidaten:
        text = read(os.path.join(ablage, name))
        treffer = P80_ABSCHNITT.search(text)
        if not treffer:
            err(f"{P80_ABLAGE}/{name}: kein Abschnitt `Gegenzeichnung`. Ein "
                f"Abnahmeprotokoll des Testkatalogs trägt ihn (D-319, `FW-CL-11`). "
                f"Arbeits- und Meßprotokolle bekommen ihn nicht – die Abgrenzung steht "
                f"in `{P80_ABLAGE}/README.md`")
            continue
        abschnitt = text[treffer.start():]
        naechste = re.search(r"^#{1,6}\s", abschnitt[treffer.end() - treffer.start():],
                             re.M)
        if naechste:
            abschnitt = abschnitt[:treffer.end() - treffer.start() + naechste.start()]
        if TBD_RE.search(abschnitt):
            err(f"{P80_ABLAGE}/{name}: der Abschnitt `Gegenzeichnung` trägt noch ein "
                f"offenes `<TBD>`. Eine Gegenzeichnung ist die Handlung einer Rolle und "
                f"kein Feld, das ein Werkzeug füllt – ist keine zweite Rolle vorhanden, "
                f"wird selbst gegengezeichnet und der Abschnitt weist das ausdrücklich "
                f"aus (D-319, `CR-2026-127` E1)")


# Pruefung 81: eine Zeilenendeform je Repositorium (CR-2026-128, D-320, K-81)
# ---------------------------------------------------------------------------
#
# ANLASS, und er ist ein eigener Fehler. Eine Sitzung hat 28 LF-Zeilen in einen Bestand
# eingeschleppt, der durchgehend CRLF traegt. Gefunden hat es KEINE der 80 Pruefungen,
# sondern ein Suchtext, der danach nicht mehr traf. Pruefung 66 prueft die
# GEGENRICHTUNG - einen Wagenruecklauf ohne Zeilenvorschub - und greift hier nicht.
#
# 🔴 UND DER BEFUND, DER IHN AUSLOESTE, WAR AM FALSCHEN GEGENSTAND GEMESSEN. Die
# Uebergabe schrieb "kein VERSIONIERTER Texttraeger traegt reine LF". Gemessen am
# 2026-09-23 ueber alle 517 verfolgten Eintraege: im ARBEITSBAUM 515 auf CRLF, im BLOB
# 515 auf reinem LF. Versioniert ist der Blob. Die Aussage ist an einem Gegenstand
# richtig und am anderen in ihr Gegenteil verkehrt.
# ➡️ WER EINE ZEILENENDEFORM MISST, SAGT DAZU, WELCHEN GEGENSTAND ER GEMESSEN HAT.
#
# ZUSCHNITT: DEN ARBEITSBAUM, NICHT DEN BLOB. Der Blob ist seit D-320 durch die
# .gitattributes gesetzt (`* text=auto`) - dort braucht es keine Pruefung, sondern eine
# Datei. Was die .gitattributes NICHT sieht, ist der Arbeitsbaum zwischen zwei
# Auscheckungen, und genau dort lag der Fall.
#
# SIE SCHREIBT KEINE FORM VOR. Sie verlangt, dass es EINE ist. Ein Linux-Arbeitsbaum
# traegt LF, ein Windows-Arbeitsbaum CRLF, und beide sind richtig; ein Bestand, der
# beides mischt, ist es nirgends. ➡️ EINHEITLICHKEIT IST IN JEDER INSTALLATION RICHTIG,
# EINE BESTIMMTE FORM NUR AN EINEM ARBEITSPLATZ. Damit ist der Konstruktionsfehler
# ausgeschlossen, den D-299 benannt hat: im Framework gruen und in jeder Installation rot.
#
# ZAEHLBEREICH wie bei Pruefung 75: die verfolgten Dateien. Im Framework-Repositorium
# (erkennbar am Kennzeichen, D-351) alle; in einem uebernehmenden Projekt nur die
# ausgelieferten - was ein Projekt in SEINEN Dateien fuer eine Form fuehrt, geht das
# Framework nichts an.
#
# GRENZE, benannt: Sie liest BYTES und misst den Arbeitsbaum. Welche Form im
# Repositorium ankommt, entscheidet die .gitattributes und nicht diese Pruefung. Ohne
# Git-Bestand meldet sie eine Warnung und KEIN Messergebnis (D-23).
P81_GEMISCHT = "gemischt"


def _p81_form(pfad: str) -> str | None:
    """Die Zeilenendeform eines Traegers, an seinen Bytes gemessen."""
    try:
        with open(pfad, "rb") as fh:
            roh = fh.read()
    except OSError:
        return None
    if b"\x00" in roh[:8000]:
        return None
    lf = roh.count(b"\n")
    if not lf:
        return None          # ein Traeger ohne Zeilenumbruch traegt keine Form
    crlf = roh.count(b"\r\n")
    if crlf == lf:
        return "CRLF"
    if crlf == 0:
        return "LF"
    return P81_GEMISCHT


def check_zeilenendeform(root: str) -> None:
    """Pruefung 81 (D-320): Alle versionierten Texttraeger tragen dieselbe Form."""
    dateien = _p75_verfolgt(root)
    if dateien is None:
        warn("Prüfung 81: kein Git-Bestand lesbar – die Zeilenendeform ist an diesem "
             "Ort nicht prüfbar. Das ist KEIN Messergebnis (D-23)")
        return
    bestand = set(dateien)
    eigenes_repo = QUELLREPO_KENNZEICHEN in bestand
    ausgeliefert = (KERN + "/",)
    formen: dict[str, list[str]] = {}
    for rel in sorted(bestand):
        if not eigenes_repo and not rel.startswith(ausgeliefert):
            continue
        if os.path.splitext(rel)[1] not in TEXT_EXT and os.path.basename(rel) not in (
                "VERSION", ".gitignore", ".gitattributes"):
            continue
        pfad = os.path.join(root, *rel.split("/"))
        if not os.path.isfile(pfad):
            continue
        form = _p81_form(pfad)
        if form is None:
            continue
        formen.setdefault(form, []).append(rel)
    if not formen:
        err("Prüfung 81: kein einziger versionierter Textträger gelesen – sie hätte "
            "nichts zu prüfen und bestünde leise (D-23)")
        return
    # --- Gegenstand 1: kein Traeger mischt beide Formen in sich ---------------------
    for rel in formen.get(P81_GEMISCHT, []):
        err(f"{rel}: mischt CRLF- und LF-Zeilen in derselben Datei. Ein gemischter "
            f"Träger ist an keinem Arbeitsplatz richtig; er entsteht, wenn ein Werkzeug "
            f"einzelne Zeilen in der jeweils anderen Form nachträgt (D-320, `K-81`)")
    # --- Gegenstand 2: der Bestand traegt EINE Form ---------------------------------
    rein = {f: n for f, n in formen.items() if f != P81_GEMISCHT}
    if len(rein) < 2:
        return
    haupt = max(rein, key=lambda f: len(rein[f]))
    for form, namen in sorted(rein.items()):
        if form == haupt:
            continue
        for rel in namen:
            err(f"{rel}: trägt {form}-Zeilenenden, während {len(rein[haupt])} von "
                f"{sum(len(n) for n in rein.values())} versionierten Textträgern "
                f"{haupt} tragen. Diese Prüfung schreibt keine Form vor – sie verlangt, "
                f"daß es eine ist (D-320, `K-81`). Welche Form im Repositorium ankommt, "
                f"setzt `.gitattributes`, nicht der Arbeitsplatz")



# Pruefung 82: die Bestandsliste steht auf dem Stand des Releases (CR-2026-130, D-331)
# ---------------------------------------------------------------------------
#
# ANLASS, UND ER IST ZWEIMAL IN ZWEI RELEASES AUFGETRETEN. `1.0.0` hat die Bestandsliste
# angelegt, und ihr erster Eintrag war zugleich ihr erster Befund: Beide uebernehmenden
# Projekte standen drei Releases hinter `main`, waehrend Kriterium 5 von D-11 als
# erfuellt gefuehrt wurde. `1.0.1` hat es wiederholt - die Liste stand einen halben Tag
# auf `1.0.0`, waehrend die Projekte `1.0.1` trugen.
#
# URSACHE IST DIE REIHENFOLGE, NICHT DIE SORGFALT. Gehoben wurde NACH dem Merge; damit
# war `FW-CL-11` Pruefpunkt 20 zum Merge-Zeitpunkt nicht erfuellt.
# ➡️ EINE LISTE, DIE ERST NACH DEM RELEASE FORTGESCHRIEBEN WIRD, IST BEIM RELEASE FALSCH.
#
# 🔴 UND SIE WAR AN ZWEI STELLEN FALSCH, NICHT AN EINER. Gemessen am 2026-09-23 vor dem
# ersten Handgriff dieses Releases: Das Framework hatte seine Liste auf `1.0.1`
# berichtigt - die AUSGELIEFERTEN Kopien in beiden uebernehmenden Projekten trugen
# weiter `1.0.0` neben einer VERSION `1.0.1`. Diese Pruefung waere dort rot gewesen.
# ➡️ WER EINE LISTE NACH DEM HEBEN FORTSCHREIBT, SCHREIBT SIE AN EINER STELLE FORT UND
# LIEFERT SIE AN ZWEI. Das ist der gemessene Grund, weshalb ein Verfahrensschritt allein
# hier nicht getragen haette.
#
# ZUSCHNITT: DIE SPALTE `Framework-Version` GEGEN `<KERN>/VERSION`. Mehr ist von hier aus
# nicht messbar - die Projekte liegen ausserhalb dieses Repositoriums, und eine Pruefung,
# die sie sucht, waere auf jedem anderen Arbeitsplatz rot (D-299).
#
# D-299-PROBE, GEFUEHRT UND BESTANDEN: In einem uebernehmenden Projekt sind Liste und
# VERSION beide byte-gleich aus DEMSELBEN Release ausgeliefert und tragen deshalb
# denselben Wert - auch dann, wenn das Projekt mehrere Releases zurueckliegt. Die
# Pruefung ist dort gruen, und sie braucht dafuer keine Ausnahme.
#
# 🔴 GRENZE, BENANNT: SIE MISST DIE BEHAUPTUNG, NICHT DIE TATSACHE. Wer die Zeile
# aendert, ohne zu aktualisieren, kommt durch. Das ist dieselbe Bauform wie bei Pruefung 77, die
# die VERSION des Hauptdokuments misst und nicht seinen INHALT - und sie steht hier,
# weil eine Grenze, die man nicht nennt, wie eine Zusage aussieht.
#
# ⚠️ PREIS, BENANNT: Jedes Release fasst diese Tabelle an - derselbe Preis wie bei
# Pruefung 67 und Pruefung 77.
P82_LISTE = KERN + "/governance/ADOPTION_REGISTRY.md"
P82_SPALTE = "Framework-Version"
P82_PROJEKTSPALTE = "Projekt"


def check_bestandsliste_stand(root: str) -> None:
    """Pruefung 82 (D-331): Die Bestandsliste nennt den Stand dieses Releases."""
    pfad = os.path.join(root, *P82_LISTE.split("/"))
    if not os.path.isfile(pfad):
        err(f"{P82_LISTE}: fehlt. `RELEASE_PROCESS.md` Abschnitt 4 Punkt 4 verlangt sie "
            f"als Nachweis der Auditierbarkeit, und Kriterium 5 von D-11 hängt an ihr "
            f"(D-322). Prüfung 82 hätte ohne sie ihren Gegenstand verloren")
        return
    vpfad = os.path.join(root, KERN, "VERSION")
    if not os.path.isfile(vpfad):
        return  # Pruefung 1 meldet die fehlende Pflichtdatei bereits
    stand = read(vpfad).strip()
    zeilen = read(pfad).split("\n")

    # --- Den Anker suchen, und sein Fehlen als Fehler melden (D-23) -----------------
    kopf = None
    spalte = None
    projekt = 0
    for i, roh in enumerate(zeilen):
        if not roh.lstrip().startswith("|"):
            continue
        zellen = tabellenzellen(roh)
        if P82_SPALTE in zellen:
            kopf = i
            spalte = zellen.index(P82_SPALTE)
            if P82_PROJEKTSPALTE in zellen:
                projekt = zellen.index(P82_PROJEKTSPALTE)
            break
    if kopf is None:
        err(f"{P82_LISTE}: keine Tabelle mit der Spalte `{P82_SPALTE}`. Prüfung 82 "
            f"findet ihren Gegenstand über diese Überschrift; geht sie verloren, "
            f"bestünde die Prüfung leise (D-23)")
        return

    # --- Die Zeilen des Bestands gegen VERSION halten -------------------------------
    gemessen = 0
    for roh in zeilen[kopf + 2:]:
        if not roh.lstrip().startswith("|"):
            break  # eine Leerzeile beendet die Tabelle (D-264)
        zellen = tabellenzellen(roh)
        if len(zellen) <= spalte:
            continue
        wert = zellen[spalte].strip().strip("*`").strip()
        if not wert:
            continue
        gemessen += 1
        if wert == stand:
            continue
        name = zellen[projekt].strip() if len(zellen) > projekt else "(ohne Namen)"
        err(f"{P82_LISTE}: {name} steht auf Framework-Version {wert}, "
            f"{KERN}/VERSION führt {stand}. Das Update der übernehmenden Projekte gehört "
            f"VOR den Release-Commit (D-330); eine Liste, die erst danach "
            f"fortgeschrieben wird, ist beim Release falsch. ⚠️ Diese Prüfung mißt die "
            f"Behauptung der Zeile, nicht den Stand des Projekts (D-331)")
    if not gemessen:
        warn(f"{P82_LISTE}: die Tabelle führt keine Zeile mit einem Wert in der Spalte "
             f"`{P82_SPALTE}`. Prüfung 82 hat nichts gemessen – das ist KEIN "
             f"Messergebnis (D-23)")



# Pruefung 83: die Chronik zaehlt ihr eigenes Release zu Ende (CR-2026-131, D-335)
# ---------------------------------------------------------------------------
#
# ANLASS, GEMESSEN IM VORBEDINGUNGSDURCHGANG VON 1.2.0. `docs/ROADMAP.md` fuehrt je
# Release eine Zeile mit der SPANNE der Entscheidungen, die es vergeben hat. Ueber
# vierzehn Releases mit Spannenschreibweise ist sie lueckenlos - und die letzte war um
# zwei zu niedrig: `1.1.0` stand auf "D-329 bis D-332", vergeben sind D-329 bis D-334.
#
# DIE URSACHE IST GEMESSEN UND STEHT IM EIGENEN RELEASE. D-333 und D-334 sind BEIM
# UMSETZEN gefallen; die Uebergabe zu 1.1.0 sagt es woertlich. Die ROADMAP-Zeile war zu
# diesem Zeitpunkt laengst geschrieben.
# ➡️ EINE ZAHL, DIE VOR IHREM GEGENSTAND GESCHRIEBEN WIRD, IST ZUM ZEITPUNKT IHRER
# NIEDERSCHRIFT RICHTIG UND DANACH NICHT MEHR. Das ist die Bauform von Pruefung 40 -
# hier INNERHALB eines einzigen Releases statt ueber zweiundvierzig.
#
# 🔴 DER SCHWERERE TEIL: KEIN BESCHREIBENDER TRAEGER NENNT ALLE SECHS. Vier Traeger
# beschreiben 1.1.0 - ROADMAP vier, CHANGELOG fuenf, Antrag vier, Protokoll vier. D-333
# steht in keinem davon. Es steht im Register, im Protokoll und in den beiden normativen
# Traegern, die es GEAENDERT hat - also dort, wo es wirkt, und nirgends dort, wo das
# Release erklaert wird. Und D-333 ist die Entscheidung, die den SCHWERSTEN Befund von
# 1.1.0 behoben hat.
# 🟢 Der einzige Traeger, der die Menge vollstaendig nennt, ist die MARKE ("D-329 bis
# D-334") - und sie ist der einzige, den keine Pruefung erreichen kann: Der Markentext
# liegt im Tag-Objekt, nicht im Arbeitsbaum (`K-111`, `K-113`).
#
# WARUM PRUEFUNG 58 ES NICHT FAENGT. Sie haelt die Gegenrichtung - jede GENANNTE Kennung
# steht im Register. Der Befund hier ist eine VERGEBENE Kennung, die nirgends genannt
# wird.
# ➡️ PRUEFUNG 58 FAENGT DIE VERWAISTE NENNUNG, NICHT DIE VERWAISTE KENNUNG.
#
# D-299-PROBE, GEFUEHRT UND BESTANDEN: Beide Traeger liegen im Kern und werden
# byte-gleich ausgeliefert. Ein uebernehmendes Projekt, das Releases zurueckliegt, traegt
# dieselbe ROADMAP und dasselbe Register aus demselben Release - die Pruefung ist dort
# gruen und braucht keine Ausnahme.
#
# 🔴 GRENZE, BENANNT: SIE MISST DIE OBERGRENZE, NICHT DIE VOLLSTAENDIGKEIT DER
# NENNUNGEN. Ein Traeger, der die Spanne richtig fuehrt und D-333 im Fliesstext nicht
# nennt, kommt durch. Das ist dieselbe Bauform wie bei Pruefung 77 (Version, nicht
# Inhalt) und 82 (Behauptung, nicht Tatsache) - und sie steht hier, weil eine Grenze,
# die man nicht nennt, wie eine Zusage aussieht. `K-112` fuehrt die Frage weiter.
#
# ⚠️ PREIS, BENANNT: Jedes Release fasst diese Zeile an - derselbe Preis wie bei
# Pruefung 67, 77 und 82.
P83_ROADMAP = KERN + "/docs/ROADMAP.md"
P83_REGISTER = KERN + "/governance/DECISION_LOG.md"
P83_SPANNE_RE = re.compile(r"\*\*D-(\d+)\*\*\s*bis\s*\*\*D-(\d+)\*\*")
P83_ZEILE_RE = re.compile(r"^\|\s*(?:\*\*)?D-(\d+)", re.M)
P83_SONDEN_ANKER = "**Reservierter Kennungsbereich für Sonden"
P83_GRENZE_RE = re.compile(r"ab (\d+) zählen nicht als Obergrenze")


def _p83_sondengrenze(logtext: str) -> int:
    """Ab welcher D-Nummer eine Kennung den Sonden gehoert (D-340).

    EIN BEREICH UND KEINE LISTE, und der Grund ist gemessen: Eine Liste muesste die
    Kennung WOERTLICH nennen - und dann meldet Pruefung 58 genau diese Nennung, weil
    sie in keiner Registerzeile steht. Eine Ausnahme, die ihren Gegenstand nennen muss,
    um zu wirken, erzeugt den Befund, den sie verhindern soll.

    NICHT dieselbe Sache wie `_synthetische_kennungen()`: Jene Menge wird nie im
    Register gefuehrt und vom MELDEN ausgenommen; dieser Bereich wird von einer
    Gegenprobe selbst eingetragen und muss weiterhin gemeldet werden koennen - nur als
    OBERGRENZE zaehlt er nicht. Null heisst: der Anker ist verloren; der Aufrufer
    meldet das.
    """
    for zeile in logtext.splitlines():
        if zeile.lstrip().startswith(P83_SONDEN_ANKER):
            m = P83_GRENZE_RE.search(zeile)
            return int(m.group(1)) if m else 0
    return 0


def check_chronikspanne(root: str) -> None:
    """Pruefung 83 (D-335): Die letzte Release-Spanne endet bei der hoechsten Kennung."""
    rpfad = os.path.join(root, *P83_ROADMAP.split("/"))
    dpfad = os.path.join(root, *P83_REGISTER.split("/"))
    if not os.path.isfile(rpfad):
        err(f"{P83_ROADMAP}: fehlt - Pruefung 83 haette ihren Gegenstand verloren und "
            f"bestuende sonst leise (D-23, D-335)")
        return
    if not os.path.isfile(dpfad):
        return  # Pruefung 50 und 58 melden den fehlenden Traeger bereits

    dtext = read(dpfad)
    # 🔴 DIESE PRUEFUNG BRAUCHT IHRE EIGENE AUSNAHMEMENGE, UND ZWAR EINE ANDERE ALS
    # PRUEFUNG 50 UND 58 (D-340). Der Anlass ist gemessen und hat zwei Stufen:
    #
    # STUFE 1, gefunden beim ersten Abnahmelauf von 1.2.0: Die Gegenprobe 58b legt eine
    # Registerzeile mit ihrer Sondenkennung an, und diese Pruefung las sie als hoechste -
    # 654 gemeldete Luecken.
    #
    # STUFE 2, gefunden beim ZWEITEN Abnahmelauf, nachdem die Sondenkennung von Pruefung 58 in die Menge der
    # belegten synthetischen Kennungen eingetragen war: SONDE 58a VERLOR IHREN
    # GEGENSTAND. Pruefung 58 nimmt jene Menge vom Melden aus - und Sonde 58a prueft
    # genau, dass diese Kennung GEMELDET wird. Das Decision Log sagt denselben Satz
    # ueber die Sondenkennung von Pruefung 50: "sie soll ja gemeldet werden".
    # ➡️ ZWEI PRUEFUNGEN, DIE DIESELBE KENNUNG ANSEHEN, STELLEN NICHT DIESELBE FRAGE -
    # die eine fragt nach ZUGEHOERIGKEIT, die andere nach einer GRENZE. Das ist D-243
    # (zwei Regeln, die einander die Voraussetzung entziehen) an einem Paar von SONDEN.
    #
    # Deshalb ein EIGENER Anker im selben Absatz des Decision Logs, mit eigener
    # Begruendung. Leere Menge heisst: der Anker ist verloren - das wird gemeldet.
    grenze = _p83_sondengrenze(dtext)
    if not grenze:
        err(f"{P83_REGISTER}: der Absatz '{P83_SONDEN_ANKER}…' fehlt oder nennt keine "
            f"Bereichsgrenze. Pruefung 83 leitet ihre Ausnahme daraus ab; ohne ihn "
            f"liest sie eine Sondenkennung als hoechste vergebene Entscheidung "
            f"(D-23, D-340)")
        return
    vergeben = [int(n) for n in P83_ZEILE_RE.findall(dtext) if int(n) < grenze]
    if not vergeben:
        err(f"{P83_REGISTER}: keine Registerzeile '| D-NNN |' gefunden - Pruefung 83 "
            f"findet ihren Vergleichswert dort; geht er verloren, bestuende sie leise "
            f"(D-23, D-335)")
        return
    hoechste = max(vergeben)

    spannen = P83_SPANNE_RE.findall(read(rpfad))
    if not spannen:
        err(f"{P83_ROADMAP}: keine Release-Spanne der Form '**D-NNN** bis **D-NNN**' "
            f"gefunden. Pruefung 83 findet ihren Gegenstand ueber diese Schreibweise; "
            f"geht sie verloren, bestuende die Pruefung leise (D-23, D-335)")
        return

    # Die hoechste Obergrenze aller Spannen - nicht die zuletzt geschriebene. Die
    # Releasetabelle ist nicht garantiert sortiert: gemessen am 2026-09-23 stand `1.0.1`
    # VOR `1.0.0`, und eine Pruefung, die sich auf die Reihenfolge verlaesst, misst dann
    # die falsche Zeile (D-337).
    obergrenze = max(int(b) for _a, b in spannen)
    if obergrenze == hoechste:
        return
    if obergrenze > hoechste:
        err(f"{P83_ROADMAP}: die hoechste Release-Spanne endet bei D-{obergrenze}, das "
            f"Register fuehrt hoechstens D-{hoechste}. Die Chronik nennt eine "
            f"Entscheidung, die es nicht gibt - Pruefung 58 meldet sie zusaetzlich als "
            f"nicht gefuehrte Kennung (D-335)")
        return
    fehlend = ", ".join(f"D-{n}" for n in range(obergrenze + 1, hoechste + 1))
    err(f"{P83_ROADMAP}: die hoechste Release-Spanne endet bei D-{obergrenze}, vergeben "
        f"ist bis D-{hoechste}. In der Chronik fehlen {fehlend}. Eine Entscheidung, die "
        f"beim Umsetzen faellt, faellt NACH der Zeile, die sie nennen soll - und eine "
        f"Zahl, die vor ihrem Gegenstand geschrieben wird, ist danach nicht mehr richtig. "
        f"⚠️ Diese Pruefung misst die OBERGRENZE, nicht die Vollstaendigkeit der "
        f"Nennungen (D-335, `K-112`)")


# Pruefung 85: eine Zielangabe ueberlebt ihr eigenes Release nicht (CR-2026-132, D-342)
# ---------------------------------------------------------------------------
#
# ANLASS, GEMESSEN IM VORBEDINGUNGSDURCHGANG VON 1.3.0. `docs/ROADMAP.md` fuehrt neben
# der Releasetabelle Abschnitte der Form
#     ### Geplant: <Posten> - Ziel-Release **<Version>**
# ALLE DREI vorhandenen nannten eine Version, die die Gegenwart ueberholt hatte:
#   * die Umbenennung auf Koolie mit "~0.68.0" - erledigt mit 0.88.0, und der Abschnitt
#     heisst seit fuenfzehn Releases "Geplant";
#   * das Client Pack openai-codex mit "1.1.0" - waehrend die Releasetabelle DERSELBEN
#     Datei ihn auf 1.3.0 fuehrt, rund 1.280 Zeilen entfernt;
#   * die Projekt-Overlays als Installationsparameter mit "1.2.0" - ausgeliefert, und
#     der Posten ist nicht gefahren.
#
# ➡️ EINE ZIELANGABE IST EINE ZAHL, DIE VOR IHREM GEGENSTAND GESCHRIEBEN WIRD. Das ist
# die Bauform von Pruefung 83, hier an der PLANSEITE derselben Datei statt an der
# Chronikseite - und der Beleg dafuer, dass dieselbe Bauform an zwei Enden eines
# Traegers auftreten kann, ohne dass die eine Pruefung die andere Stelle sieht.
#
# URSACHE GEMESSEN: Die Verschiebungen sind je einzeln ausgewiesen worden - D-127 hat
# den Posten auf 1.1.0 gesetzt, D-339 auf 1.3.0 -, und KEINE von ihnen hat die
# Ueberschrift angefasst, weil die Releasetabelle als der eine Ort galt.
# ➡️ WER EINE ZAHL AN ZWEI STELLEN FUEHRT, PFLEGT EINE.
#
# D-299-PROBE, GEFUEHRT UND BESTANDEN: Beide Traeger - ROADMAP und VERSION - liegen im
# Kern und werden byte-gleich ausgeliefert. Ein uebernehmendes Projekt, das Releases
# zurueckliegt, traegt beide aus demselben Release; die Pruefung ist dort gruen und
# braucht keine Ausnahme.
#
# 🔴 GRENZE, BENANNT: SIE MISST DIE ZIELANGABE, NICHT DEN STAND DES POSTENS. Ein
# Abschnitt, dessen Ziel in der Zukunft liegt, kann laengst erledigt sein und kommt
# durch - dieselbe Bauform wie Pruefung 77 (Version, nicht Inhalt) und 82 (Behauptung,
# nicht Tatsache). Sie steht hier, weil eine Grenze, die man nicht nennt, wie eine
# Zusage aussieht; `K-116` fuehrt die Frage weiter.
#
# ⚠️ PREIS, BENANNT: Wer einen Posten verschiebt, fasst die Ueberschrift an - und genau
# das ist der Zweck. Es ist derselbe Preis wie bei Pruefung 67, 77, 82 und 83, nur faellt
# er hier nicht je Release an, sondern je Verschiebung.
P85_ROADMAP = KERN + "/docs/ROADMAP.md"
P85_UEBERSCHRIFT = "### Geplant:"
P85_ZIEL_RE = re.compile(r"Ziel-Release\s*\**\s*`?~?(\d+)\.(\d+)\.(\d+)`?")


def _p85_version(text: str) -> tuple[int, int, int] | None:
    """Die drei Zahlen einer Versionsangabe - oder None."""
    m = re.match(r"\s*(\d+)\.(\d+)\.(\d+)\s*$", text)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def check_zielangabe(root: str) -> None:
    """Pruefung 85 (D-342): Ein Planabschnitt nennt kein erreichtes Ziel-Release."""
    rpfad = os.path.join(root, *P85_ROADMAP.split("/"))
    vpfad = os.path.join(root, KERN, "VERSION")
    if not os.path.isfile(rpfad):
        err(f"{P85_ROADMAP}: fehlt - Pruefung 85 haette ihren Gegenstand verloren und "
            f"bestuende sonst leise (D-23, D-342)")
        return
    if not os.path.isfile(vpfad):
        return  # Pruefung 1 meldet die fehlende Pflichtdatei bereits
    stand = _p85_version(read(vpfad))
    if stand is None:
        return  # Pruefung 67 meldet eine unlesbare VERSION bereits

    ueberschriften = [z for z in read(rpfad).splitlines()
                      if z.startswith(P85_UEBERSCHRIFT)]
    if not ueberschriften:
        err(f"{P85_ROADMAP}: keine Ueberschrift '{P85_UEBERSCHRIFT} …' gefunden. "
            f"Pruefung 85 findet ihren Gegenstand ueber diese Schreibweise; geht sie "
            f"verloren, bestuende die Pruefung leise (D-23, D-342)")
        return

    # 🔴 DER ANKER IST ZWEITEILIG, UND BEIDE TEILE WERDEN GEMELDET. Eine Ueberschrift
    # OHNE Zielangabe ist kein stiller Durchlauf, sondern der billigste Weg, diese
    # Pruefung loszuwerden - genau die Bauform, die D-124 mit "ein Posten ohne Zahl
    # bleibt lange liegen" bereits einmal entschieden hat.
    ohne_ziel = [z for z in ueberschriften if not P85_ZIEL_RE.search(z)]
    if ohne_ziel:
        err(f"{P85_ROADMAP}: {len(ohne_ziel)} Planabschnitt(e) nennen kein "
            f"Ziel-Release: {'; '.join(z[:70] for z in ohne_ziel)}. Ein Posten ohne "
            f"Zahl bleibt in diesem Projekt erfahrungsgemaess lange liegen (D-124) - "
            f"und er entzieht sich zugleich dieser Pruefung (D-342)")

    for zeile in ueberschriften:
        m = P85_ZIEL_RE.search(zeile)
        if not m:
            continue
        ziel = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if ziel > stand:
            continue
        err(f"{P85_ROADMAP}: der Abschnitt '{zeile[:70]}…' nennt das Ziel-Release "
            f"{m.group(1)}.{m.group(2)}.{m.group(3)}, und "
            f"{'.'.join(str(n) for n in stand)} ist erreicht. Entweder ist der Posten "
            f"gefahren - dann ist er nicht mehr 'Geplant' - oder er ist ueberfaellig "
            f"und braucht eine neue Zahl. ➡️ Eine Zielangabe ist eine Zahl, die vor "
            f"ihrem Gegenstand geschrieben wird. ⚠️ Diese Pruefung misst die "
            f"ZIELANGABE, nicht den STAND des Postens (D-342, `K-116`)")

# ---------------------------------------------------------------------------
#
# ANLASS. 1.9.0 ist das Qualitaetssicherungsrelease der Dokumentation (D-370). Seine
# Vorbedingung war, VOR der Durchsicht festzulegen, welche Dokumente es gibt, was je
# Dokument "in Ordnung" heisst - und was davon eine Maschine pruefen kann. Sonst ist
# derselbe Befund in drei Releases wieder da: Die Standueberschrift der Roadmap stand
# bei 1.8.0 vier Releases zurueck, direkt ueber dem Satz "Wird mit jedem Release
# fortgeschrieben".
#
# DIE DOKUMENTKLASSEN STEHEN HIER, AN EINER STELLE (D-371), und
# docs/DOCUMENTATION_STANDARD.md beschreibt sie, statt sie ein zweites Mal aufzuzaehlen:
#   A  Einstieg   - wer das Framework zum ersten Mal liest
#   B  Regeln     - was gilt (Core-Module, Laufzeit, Prozesse, Checklisten, Skills ...)
#   C  Register   - Belege und Verzeichnisse; ihr Inhalt wird nicht umgeschrieben
#   D  Hauptdokument - die Kapitelquellen unter build/doc/
# Die Nachweisschicht (clientmap.NACHWEIS_ABLAGEN) ist keine Klasse - mit einer
# Ausnahme: build/doc/ liegt darin, weil build/ nicht zur Nutzung gehoert, ist aber
# das Hauptdokument und damit Klasse D.
#
# D-299: Alle vier Pruefungen lesen Traeger, die byte-gleich in jedes Projekt
# geliefert werden - dort sind sie so gruen wie hier. Die Wurzel-README gehoert dem
# Quellrepositorium; in einem Projekt gehoert die Wurzel dem Projekt, und sie wird
# dort nicht gelesen. Fehlt build/doc/ (Lieferumfang "nutzung"), fehlt Klasse D.
DOK_REGISTER = frozenset({
    "CHANGELOG.md", "governance/DECISION_LOG.md", "docs/ROADMAP.md",
    "tests/TEST_CATALOG.md", "tests/EDGE_CASES.md", "docs/PLACEHOLDER_REGISTRY.md",
    "governance/ADOPTION_REGISTRY.md",
})
DOK_REGISTER_RE = re.compile(r"skills/[^/]+/(?:TESTS|EXAMPLES|CHANGELOG)\.md$")
DOK_EINSTIEG = ("onboarding/", "examples/", "pilot/", "docs/ADOPTION_GUIDE.md",
                "docs/RUNTIME_GLOSSARY.md", "clients/README.md")
DOK_EINSTIEG_RE = re.compile(r"clients/[^_/][^/]*/CLIENT_PACK\.md$")
DOK_NACHWEIS = ("governance/change-requests/", "tests/protocols/", "tests/erhebungen/",
                "build/")
def dokumentklasse(rel: str) -> str | None:
    """Die Klasse eines Dokuments nach D-371 - projektrelativ, mit '/'. None heisst:
    kein Dokument dieser Pruefungen (keine Markdown-Datei, Nachweisschicht, Projekt)."""
    if not rel.endswith(".md"):
        return None
    if not rel.startswith(KERN + "/"):
        return "A" if rel in DOK_WURZEL else None
    k = rel[len(KERN) + 1:]
    if k.startswith("build/doc/"):
        return "D"
    if k.startswith(DOK_NACHWEIS):
        return None
    if k in DOK_REGISTER or DOK_REGISTER_RE.search(k):
        return "C"
    if k.startswith(DOK_EINSTIEG) or DOK_EINSTIEG_RE.match(k):
        return "A"
    return "B"


def _dokumente(root: str):
    """(rel, klasse) aller Dokumente dieses Baums, sortiert."""
    gefunden = []
    kern = os.path.join(root, KERN)
    for dirpath, dirnames, filenames in os.walk(kern):
        dirnames[:] = sorted(d for d in dirnames if d not in (".git", "__pycache__", "out"))
        for fn in filenames:
            rel = os.path.relpath(os.path.join(dirpath, fn), root).replace(os.sep, "/")
            k = dokumentklasse(rel)
            if k:
                gefunden.append((rel, k))
    if ist_quellrepositorium(root):
        gefunden += [(rel, "A") for rel in DOK_WURZEL if os.path.isfile(os.path.join(root, rel))]
    return sorted(gefunden)


DOK_ZAUN_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def _ohne_code(text: str) -> tuple[list[str], bool]:
    """Die Zeilen ohne Codebloecke und Inline-Code - Zeilennummern bleiben erhalten.
    Zweiter Wert: Ist am Ende ein Codeblock offen?

    Code ist ZITAT: ein Befehl, eine Ausgabe, eine Meldung, die woertlich so lautet.
    Eine Rechtschreib- oder Formpruefung darin pruefte den zitierten Gegenstand und
    nicht das Dokument."""
    zeilen, zaun = [], ""
    for z in text.split("\n"):
        m = DOK_ZAUN_RE.match(z)
        if m:
            if not zaun:
                zaun = m.group(1)[0] * 3
            elif m.group(1).startswith(zaun):
                zaun = ""
            zeilen.append("")
            continue
        zeilen.append("" if zaun else re.sub(r"`[^`\n]*`", "``", z))
    return zeilen, bool(zaun)


def _frontmatter_ende(zeilen: list[str]) -> int:
    if zeilen and zeilen[0].strip() == "---":
        for i in range(1, len(zeilen)):
            if zeilen[i].strip() == "---":
                return i + 1
    return 0


# --- Pruefung 92: die Rechtschreibung (D-373) ----------------------------------------
#
# ANLASS, gemessen im Vorbedingungsdurchgang von 1.9.0: 603 Woerter in der Schreibung
# vor 1996 gegen 1.192 in der geltenden, und NEUNZEHN Dokumente mischten beide - oft im
# selben Absatz ("dass" neben "daß"). Die Klassen A, B und D schreiben nach dem
# geltenden Duden; die Register (C) bleiben, wie sie geschrieben wurden (D-371): Ein
# Beleg wird nicht umgeschrieben, auch nicht orthographisch.
# WIE: eine feste Liste der Staemme, in denen das "ß" nach kurzem Vokal steht und
# deshalb heute "ss" ist. Ein allgemeines "ß nach kurzem Vokal" kann keine Maschine
# ohne Woerterbuch entscheiden ("Maß" gegen "Meß"); eine Liste kann es fuer die Woerter,
# die hier vorkommen.
# GRENZE: Ein Wort, das nicht auf der Liste steht, kommt durch. Die Liste ist aus dem
# gemessenen Bestand gezogen (308 verschiedene Woerter mit "ß", 2026-09-25), nicht aus
# einem Woerterbuch. Code (Bloecke und Inline) ist Zitat und wird nicht geprueft.
P92_ALT_RE = re.compile(
    r"\b(?:[Dd]aß|\w*[Mm]uß\w*|\w*[Mm]üßt\w*|\w*[Mm]iß(?:t|\w)\w*|\w*[Mm]eß\w*|\w*MEß\w*|"
    r"\w*[Ll]äßt\w*|\w*[Vv]erläßlich\w*|\w*[Ff]aß(?:t|te|ten|bar)\w*|\w*[Pp]aß(?:t|te|ten)?\b|"
    r"\w*[Ll]aß\b|\w*[Ll]aß(?:fall|t)\w*|\w*[Ww][uü]ß(?:t|te|ten)\w*|\w*[Ss]chluß\w*|"
    r"\w*[Vv]ergi?ß(?:t|lich\w*)|\w*[Vv]ergeß\w*|\w*[Pp]rozeß\w*|\b[Bb]iß\b|\b[Rr]iß\b|"
    r"\w*[Ff]luß\w*|\w*[Ss]chuß\w*|\w*[Ee]ngpaß)")


def check_rechtschreibung(root: str) -> None:
    """Pruefung 92 (D-373): Klassen A, B und D ohne Schreibung vor 1996."""
    for rel, klasse in _dokumente(root):
        if klasse == "C":
            continue
        zeilen, _ = _ohne_code(read(os.path.join(root, *rel.split("/"))))
        funde = [f"{i + 1}: {w}" for i, z in enumerate(zeilen) for w in P92_ALT_RE.findall(z)]
        if funde:
            err(f"{rel}: {len(funde)} Wort/Wörter in der Schreibung vor 1996 "
                f"({'; '.join(funde[:6])}{' …' if len(funde) > 6 else ''}). Klasse "
                f"{klasse} schreibt nach dem geltenden Duden: 'dass', 'muss', 'misst', "
                f"'Messbaum' (D-373)")


# --- Pruefung 93: die Form (D-374) ---------------------------------------------------
#
# Vier Gegenstaende, alle in jedem Dokument der Klassen A bis D:
#   (a) jeder Codeblock ist geschlossen - ein offener verschluckt den Rest der Datei,
#       und die Assemblierung des Hauptdokuments bricht an genau dieser Stelle;
#   (b) genau eine Hauptueberschrift ('# '); mit YAML-Frontmatter hoechstens eine,
#       denn dort traegt der Kopf den Namen;
#   (c) keine uebersprungene Ueberschriftenebene ('##' auf '####');
#   (d) jede Tabellenzeile hat die Spaltenzahl ihrer Kopfzeile - ein ungeschuetzter
#       senkrechter Strich verschiebt jede Zelle rechts davon, und der Leser sieht es
#       nicht, weil die Tabelle trotzdem rendert.
# ANLASS: Gemessen im Vorbedingungsdurchgang war der Bestand bis auf EINE Datei sauber
# (ein Agentenprofil mit drei Hauptueberschriften). Die Pruefung ist deshalb ein
# Waechter und kein Aufraeumen - und genau so billig soll sie bleiben.
# GRENZE: Sie prueft die Gestalt, nicht die Gliederung - ob die Ueberschriften das
# Richtige gliedern, bleibt Durchsicht.
def _tabellenzellen(zeile: str) -> int:
    z = re.sub(r"`[^`]*`", "C", zeile).replace("\\|", "x").strip()
    if z.startswith("|"):
        z = z[1:]
    if z.endswith("|"):
        z = z[:-1]
    return len(z.split("|"))


def check_dokumentform(root: str) -> None:
    """Pruefung 93 (D-374): Codebloecke, Hauptueberschrift, Ebenen, Tabellenspalten."""
    for rel, _klasse in _dokumente(root):
        text = read(os.path.join(root, *rel.split("/")))
        roh = text.split("\n")
        zeilen, offen = _ohne_code(text)
        if offen:
            err(f"{rel}: ein Codeblock ist bis zum Dateiende nicht geschlossen (D-374)")
            continue
        fm = _frontmatter_ende(roh)
        h1 = sum(1 for i, z in enumerate(zeilen) if i >= fm and z.startswith("# "))
        if (fm and h1 > 1) or (not fm and h1 != 1):
            err(f"{rel}: {h1} Hauptüberschriften ('# '), erwartet "
                f"{'höchstens eine (mit Frontmatter)' if fm else 'genau eine'} (D-374)")
        ebene = 0
        for i, z in enumerate(zeilen):
            m = re.match(r"(#{1,6}) ", z)
            if not m:
                continue
            n = len(m.group(1))
            if ebene and n > ebene + 1:
                err(f"{rel}:{i + 1}: Überschrift der Ebene {n} direkt unter Ebene "
                    f"{ebene} – eine Ebene ist übersprungen (D-374)")
            ebene = n
        i = 0
        while i < len(zeilen) - 1:
            if (zeilen[i].lstrip().startswith("|")
                    and re.match(r"\s*\|?\s*:?-{3,}", zeilen[i + 1])):
                soll = _tabellenzellen(zeilen[i])
                j = i + 2
                while j < len(zeilen) and zeilen[j].lstrip().startswith("|"):
                    ist = _tabellenzellen(zeilen[j])
                    if ist != soll:
                        err(f"{rel}:{j + 1}: Tabellenzeile mit {ist} statt {soll} "
                            f"Spalten – ein ungeschützter senkrechter Strich verschiebt "
                            f"jede Zelle rechts davon (D-374)")
                    j += 1
                i = j
            else:
                i += 1


# --- Pruefung 94: der Steckbrief (D-375) ---------------------------------------------
#
# Ein Dokument der Klassen A und B traegt vor seinem ersten Abschnitt einen Steckbrief
# (Tabelle "| Attribut | Wert |") mit einer Kennung (ID oder <Art>-ID), einer Version und
# einem Status. Pruefung 13 prueft die FORM eines Versionsfeldes, das da ist; dass es da
# ist, prueft sie nicht - und 116 von 215 Dokumenten hatten keines.
# AUSGENOMMEN, jeweils mit Grund:
#   - README.md: ein Verzeichnis, kein Dokument mit eigenem Stand; ebenso die
#     Einstiegsdokumente der Wurzel (DOK_WURZEL, D-437) - sie tragen ihren Stand ueber
#     VERSION und verweisen auf die Dokumente, die einen Steckbrief tragen;
#   - die Laufzeitschicht (framework/runtime/, role-packs/*/runtime/, root-template/):
#     sie wird so in die Sitzung geladen, und ihre Laenge ist begrenzt (Pruefung 4);
#   - Ausfuellvorlagen (templates/, Musterdokumente der Overlay-Muster, der
#     Antragsvorlage, die Abbildungsvorlage der Organisationsvorgaben): Sie werden
#     kopiert und gehoeren danach dem Projekt - ein Steckbrief des Frameworks darin
#     waere eine falsche Herkunftsangabe;
#   - examples/: Beispielausgaben, deren Gestalt die eines Ergebnisses ist.
# GRENZE: Sie prueft die ANWESENHEIT der drei Zeilen; ihren Wert prueft Pruefung 13
# (Version) und Pruefung 55 (Status).
P94_AUSNAHMEN = ("framework/runtime/", "templates/", "examples/")
P94_AUSNAHMEN_RE = re.compile(
    r"(?:^|/)README\.md$|^framework/role-packs/[^/]+/runtime/|^clients/[^/]+/root-template/|"
    r"^framework/overlay-patterns/[^/]+/(?:documents|rules)/|^governance/CHANGE_REQUEST_TEMPLATE\.md$|"
    r"^framework/org-policies/MAPPING_CLASSIFICATION\.md$")
P94_KOPF = "| Attribut | Wert |"


def check_steckbrief(root: str) -> None:
    """Pruefung 94 (D-375): Klassen A und B tragen ID, Version und Status."""
    for rel, klasse in _dokumente(root):
        if klasse not in "AB" or rel in DOK_WURZEL:
            continue
        k = rel[len(KERN) + 1:]
        if k.startswith(P94_AUSNAHMEN) or P94_AUSNAHMEN_RE.search(k):
            continue
        zeilen = read(os.path.join(root, *rel.split("/"))).split("\n")
        kopf = []
        for i, z in enumerate(zeilen):
            if z.startswith("## "):
                break
            if re.sub(r"\s+", " ", z.strip()) == P94_KOPF:
                j = i + 2
                kopf = []
                while j < len(zeilen) and zeilen[j].startswith("|"):
                    kopf.append(zeilen[j])
                    j += 1
                break
        fehlt = [name for name, rx in (
            ("ID", r"^\|\s*(?:[\w-]+-)?ID\s*\|"), ("Version", r"^\|\s*Version\b[^|]*\|"),
            ("Status", r"^\|\s*Status\s*\|")) if not any(re.match(rx, z) for z in kopf)]
        if fehlt:
            err(f"{rel}: {'kein Steckbrief' if not kopf else 'Steckbrief ohne ' + ', '.join(fehlt)} "
                f"vor dem ersten Abschnitt. Klasse {klasse} trägt eine Tabelle "
                f"'{P94_KOPF}' mit Kennung, Version und Status – sonst unterscheidet das "
                f"Dokument keine zwei Stände (D-375)")


# --- Pruefung 113: keine Kennung in der Produktdokumentation (CR-2026-173, D-540) -------
# Die Produktdokumentation spricht zu Menschen, die Koolie benutzen. Woher eine Regel
# kommt, steht in der Nachweisschicht: Decision Log, Aenderungsantraege, CHANGELOG,
# Protokolle, Erhebungen, Roadmap. Ausgenommen sind ausserdem die Stellen der
# Produktdokumentation, die selbst Nachweis sind: die Ergebnis- und Belegspalten der
# Testblaetter und der Grenzfaelle, die Belegspalte der Faehigkeitsmatrix und die Zeilen eines
# Versionsverlaufs. Vom Hauptdokument sind drei Kapitel Nachweis: die Grenzen und offenen
# Entscheidungen, die Anhaenge mit der Quellenliste und der Abschluss (Owner 2026-10-02,
# analog den vier Ausnahmen des Laufzeitglossars). Der Rest von build/ - Skripte, README,
# Erzeugnisse - ist kein Produkttext.
P113_RE = re.compile(r"(?<![A-Za-z0-9])(CR-\d{4}-\d{3}|D-\d{1,4}|K-\d{1,4})(?![0-9])")
P113_NACHWEIS = (KERN + "/CHANGELOG.md", KERN + "/governance/DECISION_LOG.md",
                 KERN + "/docs/ROADMAP.md")
P113_NACHWEIS_ORDNER = (KERN + "/governance/change-requests/", KERN + "/tests/protocols/",
                        KERN + "/tests/erhebungen/")
P113_HAUPTDOKUMENT = KERN + "/build/doc/"
P113_HAUPTDOKUMENT_NACHWEIS = ("29-grenzen.md", "31-anhaenge.md", "32-abschluss.md")
P113_VERLAUF_RE = re.compile(r"^\|\s*\d+\.\d+\.\d+\s*\|")
P113_BELEGKOPF_RE = re.compile(r"Ergebnis|Status|Beleg|Befund|Protokoll|Grundlage")


def _p113_nachweis(rel: str) -> bool:
    if rel.startswith(KERN + "/build/"):
        return (not rel.startswith(P113_HAUPTDOKUMENT)
                or rel[len(P113_HAUPTDOKUMENT):] in P113_HAUPTDOKUMENT_NACHWEIS)
    return (rel in P113_NACHWEIS or rel.startswith(P113_NACHWEIS_ORDNER)
            or rel.endswith("/CHANGELOG.md"))


def p113_fundstellen(rel: str, text: str) -> list:
    """[(Zeile, Kennung)] ausserhalb der Nachweisstellen eines Produkttraegers."""
    testblatt = rel.endswith(("/TESTS.md", "/TEST_CATALOG.md", "/EDGE_CASES.md"))
    pack = rel.startswith(KERN + "/clients/") and rel.endswith("/CLIENT_PACK.md")
    aus, kopf, matrix = [], None, False
    for nr, zeile in enumerate(text.replace("\r\n", "\n").split("\n"), 1):
        if zeile.startswith("## "):
            matrix = zeile.startswith("## 2. ")
        tabelle = zeile.startswith("|")
        if not tabelle:
            kopf = None
        elif not re.match(r"^\|[\s:|-]+\|?\s*$", zeile) and kopf is None:
            kopf = tabellenzellen(zeile)
        treffer = P113_RE.findall(zeile)
        if not treffer or P113_VERLAUF_RE.match(zeile):
            continue
        if tabelle and (testblatt or (pack and matrix)):
            zellen = tabellenzellen(zeile)
            if pack and matrix:
                frei = zellen[-1:] if zellen else []
            else:
                spalten = [i for i, k in enumerate(kopf or []) if P113_BELEGKOPF_RE.search(k)]
                frei = [zellen[i] for i in spalten if i < len(zellen)]
            erlaubt = [k for z in frei for k in P113_RE.findall(z)]
            for k in erlaubt:
                if k in treffer:
                    treffer.remove(k)
        aus += [(nr, k) for k in treffer]
    return aus


def check_kennungen_in_produktdoku(root: str) -> None:
    """Pruefung 113 (D-540): Keine CR-, D- oder K-Kennung ausserhalb der Nachweisschicht."""
    if not ist_quellrepositorium(root):
        return
    # SYNTHETISCH: K-99 ist eine belegte synthetische Kennung (Decision Log)
    gut = p113_fundstellen(KERN + "/docs/X.md", "Siehe K-99 und `CR-2026-001`.\n| 1.0.0 | K-99 |\n")
    if [k for _, k in gut] != ["K-99", "CR-2026-001"]:
        err("Pruefung 113: die eigene Selbstprobe traegt nicht mehr - die Pruefung haette "
            "ihren Gegenstand verloren und bestuende leise (D-23)")
        return
    for path in iter_text_files(root):
        if not path.endswith(".md"):
            continue
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        # Das Overlay gehoert dem Projekt; im Quellrepositorium ist es eine lokale Saat.
        if rel.startswith(".koolie/project-overlay/"):
            continue
        if _p113_nachweis(rel) or not (rel.startswith(".koolie/") or "/" not in rel
                                       or rel.startswith("paketquellen/")):
            continue
        funde = p113_fundstellen(rel, read(path))
        if funde:
            erste = ", ".join(f"Z. {nr} {k}" for nr, k in funde[:3])
            err(f"{rel}: {len(funde)} Kennung(en) in der Produktdokumentation ({erste}"
                f"{' …' if len(funde) > 3 else ''}). Kennungen gehören in die Nachweisschicht "
                f"(Decision Log, Änderungsanträge, CHANGELOG); hier steht die Aussage selbst")

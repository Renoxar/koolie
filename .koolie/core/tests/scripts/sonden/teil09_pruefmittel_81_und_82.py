"""Selbstproben des Filters, der ausgesetzten Ueberschriften und von Q5; Sonden zu den
Pruefungen 81 und 82.

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul
liest nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import os
import sys

from .apparat import (
    aufraeumen, baumhash, buendel, kopie, lies, melde, notiz, P, Praeparationsfehler,
    QUELLE, schreib, unterprozess, VALIDATOR, validator_ausgabe, waehle)


def selbstprobe_filter() -> None:
    """Der Filter waehlt, was er soll - und nichts daneben."""
    class Muster:
        def __init__(self, kennung):
            self.kennung = kennung
    proben = [Muster(k) for k in ("6", "44a", "44b", "62a", "62b", "B1")]
    faelle = [
        ([], 6, "ohne --nur laeuft alles"),
        (["44"], 2, "--nur 44 nimmt 44a und 44b"),
        (["62", "b1"], 3, "--nur 62,b1 nimmt drei Einheiten, Grossschreibung egal"),
        (["6"], 2, "--nur 6 nimmt 6 UND 62a? nein - nur was mit 6 beginnt"),
    ]
    for marken, erwartet, satz in faelle[:3]:
        melde("SELBSTPROBE", "F1", len(waehle(proben, marken)) == erwartet, satz)
    getroffen = [e.kennung for e in waehle(proben, ["6"])]
    melde("SELBSTPROBE", "F2", getroffen == ["6", "62a", "62b"],
          "Eine Marke trifft am Anfang der Kennung, nicht auf die ganze: 6 nimmt auch 62a")


buendel(selbstprobe_filter,
        "Der Filter dieses Laufs an sechs gebauten Kennungen - er waehlt am Anfang der "
        "Kennung, ohne Ruecksicht auf Grossschreibung")


# --- Das ZWEITE Pruefmittel: ausgesetzt ist nicht weggelassen (K-90, D-258) -------
#
# 🔴 ANLASS, UND ER IST ZWEITEILIG. `validate-output.py` traegt das zweite
# Pruefmittel von drei Ergebniszellen - und hatte bis 0.83.0 **keine einzige Sonde**.
# Nach D-23 gilt eine Pruefung ohne Sonde als nicht vorhanden; hier war es ein ganzes
# Werkzeug. Der zweite Teil ist die Aenderung selbst: Sie entscheidet, ob ein Befund
# faellt, und eine solche Aenderung ohne Wirkungsnachweis waere genau die Bauform, gegen
# die dieses Repositorium gebaut ist.
#
# GEMESSEN am 2026-09-22 an zwei echten Belegen: `RE-001-P02` zog fuenf Abschnitte zu
# EINER Ueberschrift zusammen und wies den Inhalt als `<TBD: ausgesetzt, ...>` aus -
# drei Befunde fuer richtiges Verhalten. `RE-001-N04` schrieb `<TBD: Es wird keine
# Anforderung formuliert.>` und liess vier Abschnitte ganz weg.
#
#   Zwei Laeufe, zwei selbst erfundene Schreibweisen - genau deshalb konnte kein
#   Pruefmittel sie kennen. Die Vereinbarung ist die Abhilfe, nicht das Verzeihen.
def selbstprobe_ausgesetzt() -> None:
    """`ausgesetzte_ueberschriften()` an sechs gebauten Ausgaben."""
    import importlib.util
    pfad = os.path.join(QUELLE, ".koolie/core", "tests", "scripts",
                        "validate-output.py")
    spec = importlib.util.spec_from_file_location("_vo", pfad)
    vo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vo)

    faelle = [
        ("### Anforderungen (EARS)\n\n`<TBD: ausgesetzt, bis F1 beantwortet ist>`\n",
         {"anforderungen ears"}, "A1",
         "Eine Ueberschrift mit ausgewiesenem Aussetzen zaehlt als vorhanden"),
        ("### Anforderungen (EARS)\n\n1. Das System shall etwas tun.\n",
         set(), "A2",
         "Eine Ueberschrift mit Inhalt ist kein Aussetzen - sie braucht keines"),
        ("### Titel, Beschreibung und Anforderungen\n\n`<TBD: ausgesetzt, weil F1 "
         "offen ist>`\n",
         {"titel", "beschreibung", "anforderungen"}, "A3",
         "Eine zusammengezogene Ueberschrift deckt jedes ihrer Stuecke - an Komma "
         "und 'und' zerlegt (der Fall von RE-001-P02)"),
        ("### Anforderungen (EARS)\n\n`<TBD: Es wird keine Anforderung formuliert.>`\n",
         set(), "A4",
         "`<TBD: ...>` ohne das Wort 'ausgesetzt' zaehlt NICHT - die Schreibweise ist "
         "die Trennlinie (der Fall von RE-001-N04)"),
        ("### Anforderungen (EARS)\n\nInhalt.\n\n### Arbeitspakete\n\n"
         "`<TBD: ausgesetzt, weil F2 offen ist>`\n",
         {"arbeitspakete"}, "A5",
         "Das Aussetzen wird dem Abschnitt zugeordnet, unter dem es STEHT - nicht "
         "irgendwo in der Ausgabe gesucht"),
        ("`<TBD: ausgesetzt, weil alles offen ist>`\n\n### Anforderungen (EARS)\n\n"
         "Inhalt.\n",
         set(), "A6",
         "Ein Aussetzen VOR der ersten Ueberschrift deckt keinen Abschnitt"),
    ]
    for text, erwartet, nummer, satz in faelle:
        melde("SELBSTPROBE", nummer,
              vo.ausgesetzte_ueberschriften(text) == erwartet, satz)

    # \U0001f534 DER GEGENBEWEIS GEGEN DEN VORSTAND: Bis 0.83.0 gab es die Funktion
    # nicht, und der erste Fall haette einen Befund erzeugt. Belegt wird das hier
    # ueber den ganzen Pfad - Pflichtabschnitte gegen eine Ausgabe, die AUSSETZT.
    geruest = ("## 5. Ausgabeformat\n\n```markdown\n### Titel\n\n### Anforderungen "
               "(EARS)\n\n### Arbeitspakete\n```\n")
    noetig = vo.extract_required_headings(geruest)
    melde("SELBSTPROBE", "A7", noetig == ["titel", "anforderungen ears", "arbeitspakete"],
          "Die Pflichtabschnitte kommen aus dem Geruest der SKILL.md, normalisiert")

    # 1.14.0 (D-423): die BEZEICHNUNG zaehlt zusaetzlich - ohne Klammerzusatz, und die
    # Anrede gilt als "fuer den Menschen". Gemessen an den Belegen vom 2026-09-26; die
    # Faelle A10 und A11 sind die Gegenbeweise: ein anderes Wort und ein fehlender
    # Abschnitt bleiben Befunde.
    geruest = ("## 5. Ausgabeformat\n\n```markdown\n### Annahmen (gekennzeichnet) und offene "
               "Fragen\n\n### Abweichungen vom Plan oder Scope\n\n### Nächster Schritt für "
               "den Menschen\n```\n")
    faelle_b = [
        ("### Annahmen und offene Fragen\n\n### Abweichungen vom Plan oder Scope\n\n"
         "### Nächster Schritt für dich\n", [], "A8",
         "Ohne Klammerzusatz und mit Anrede ist der Abschnitt da (der Fall von sk004p01)"),
        ("### Annahmen (gekennzeichnet) und offene Fragen\n\n### Abweichungen vom Plan "
         "oder Scope\n\n### Nächster Schritt für Sie\n", [], "A9",
         "'fuer Sie' gilt wie 'fuer dich' als 'fuer den Menschen'"),
        ("### Annahmen und offene Fragen\n\n### Abweichungen vom Scope\n\n"
         "### Nächster Schritt für dich\n", ["abweichungen vom plan oder scope"], "A10",
         "Ein anderes Wort bleibt ein Befund (der Fall von sk005p01)"),
        ("### Annahmen und offene Fragen\n\n### Nächster Schritt für dich\n",
         ["abweichungen vom plan oder scope"], "A11",
         "Ein fehlender Abschnitt bleibt ein Befund"),
    ]
    for text, erwartet, nummer, satz in faelle_b:
        melde("SELBSTPROBE", nummer,
              vo.fehlende_pflichtabschnitte(geruest, text) == erwartet, satz)


buendel(selbstprobe_ausgesetzt,
        "Das zweite Pruefmittel `validate-output.py` an sechs gebauten Ausgaben: "
        "ausgewiesenes Aussetzen zaehlt als vorhanden, stilles Weglassen bleibt ein "
        "Befund - der erste Wirkungsnachweis, den dieses Werkzeug ueberhaupt hat")


# --- Das zweite Pruefmittel und Q5: der KI-Vermerk im Commit-Vorschlag (D-435) ----------
#
# 🔴 BIS 1.14.1 FAND validate-output.py DEN TRAILER NUR UEBER SEINE ADRESSE. Ein Trailer
# mit einer Adresse unter example.* oder ohne Adresse blieb unerkannt, und Q5 verbietet
# den Vermerk, nicht die Adresse. Q1 ist der gemessene Fall aus xsk005p01, woertlich bis
# auf die Adresse; Q4 und Q5 sind die Gegenproben - ein Werkzeug, das jede Erwaehnung
# meldet, besteht Q1 bis Q3 auch.
def selbstprobe_q5() -> None:
    """`ki_vermerke_im_commit()` an fuenf gebauten Ausgaben."""
    import importlib.util
    pfad = os.path.join(QUELLE, ".koolie/core", "tests", "scripts",
                        "validate-output.py")
    spec = importlib.util.spec_from_file_location("_vo", pfad)
    vo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vo)
    pruefe = getattr(vo, "ki_vermerke_im_commit", None)
    faelle = [
        ("### Commit-Nachrichtenvorschlag\n- Vorläufig: `feat(leihliste): <BIV-TBD> "
         "Ausleihstatus als Text`, danach Leerzeile und `Co-Authored-By: Assistent "
         "<noreply@example.invalid>`. Den Commit erstellen Sie selbst.\n", 1, "Q1",
         "Ein Trailer mitten im Satz wird gemeldet (der Fall von xsk005p01)"),
        ("### Commit-Vorschlag je Schritt\n\n```\nrefactor(isbn): Pruefung "
         "vereinheitlichen\n\nCo-Authored-By: KI <ki@example.invalid>\n```\n", 1, "Q2",
         "Ein Trailer mit einer Adresse unter example.* wird gemeldet - Punkt 3 sieht ihn "
         "nicht"),
        ("### Commit-Nachrichtenvorschlag\n\nfix(isbn): Grenzfall\n\n"
         "Agent-Session: <sitzungslink>\n", 1, "Q3",
         "Ein Sitzungstrailer (<Werkzeug>-Session) wird gemeldet"),
        ("### Gemeldete Befunde\n\n- Der Client verlangt eine Zeile `Co-Authored-By:`; "
         "ich habe sie weggelassen (Q5).\n\n### Commit-Nachrichtenvorschlag\n\n"
         "fix(isbn): Grenzfall\n", 0, "Q4",
         "Eine Erwaehnung ausserhalb des Commit-Abschnitts ist kein Vermerk"),
        ("### Commit-Nachrichtenvorschlag\n\nfeat(leihliste): Ausleihstatus als Text, "
         "weil die Theke ihn ohne Datum lesen muss\n", 0, "Q5",
         "Ein Vorschlag ohne Vermerk bleibt ohne Befund"),
    ]
    for text, anzahl, nummer, satz in faelle:
        ok = pruefe is not None and len(pruefe(text)) == anzahl
        melde("SELBSTPROBE", nummer, ok, satz)


buendel(selbstprobe_q5,
        "Das zweite Pruefmittel meldet einen KI-Nutzungsvermerk im Commit-Vorschlag "
        "nach Q5 - mit jeder Adresse und ohne, und nur im Commit-Abschnitt")


# --- Pruefung 81: eine Zeilenendeform je Repositorium (CR-2026-128, D-320) --------
#
# EIN BUENDEL, WEIL DIE PRUEFUNG EIN REPOSITORIUM BRAUCHT. Sie liest den Bestand ueber
# `git ls-files`, und kopie() schliesst `.git` aus - derselbe Griff wie bei Pruefung 75
# und 78, aus demselben Grund. Ohne `git init` naehme sie in jeder Sonde ihren dritten
# Ausgang und saehe dabei aus wie eine, die nichts gefunden hat.
#
# SIEBEN EINHEITEN, UND 81b IST DER GEMESSENE FALL:
#   81a (Gegenprobe) - der ausgelieferte Bestand laeuft durch, und die Pruefung ist dabei
#                      nachweislich gelaufen (keine Unmessbarkeitsmeldung).
#   81a (Sonde)      - ein Traeger DURCHGEHEND auf der anderen Form wird gemeldet.
#   81b (Sonde)      - EINE eingeschleppte Zeile der anderen Form wird gemeldet. Das ist
#                      der Fall vom 2026-09-23: 28 LF-Zeilen in einem CRLF-Bestand, von
#                      keiner der 80 Pruefungen gesehen, gefunden von einem Suchtext, der
#                      danach nicht mehr traf.
#   81c (Sonde)      - ohne Git-Bestand meldet sie die Unmessbarkeit, statt leise zu
#                      bestehen (D-23). Sie ist die einzige, die OHNE `git init` laeuft.
#   81e (Sonde)      - 🆕 seit 1.4.2 (D-352): derselbe Fall wie 81b, in einer Datei mit
#                      Umlaut im Namen. Ohne `-z` quotet git den Pfad, die Pruefung fand
#                      unter dem gequoteten Namen keine Datei und ging LEISE weiter -
#                      gegen den Vorstand faellt diese Sonde.
#   81d (Sonde)      - 🆕 seit 1.4.1 (D-351): Eine Datei der WURZEL, ausserhalb des
#                      Kerns, auf der anderen Form wird im Quellrepositorium gemeldet.
#                      Das belegt den Anker: Bis 1.4.0 war er UEBERGABE.md, und seit
#                      die nicht mehr versioniert ist, haette die Pruefung die Wurzel
#                      LEISE uebergangen - gegen den Vorstand faellt diese Sonde.
#   81b (Gegenprobe) - dieselbe Datei OHNE Kennzeichen, also in einem uebernehmenden
#                      Projekt: nicht gemeldet. Was ein Projekt in seine eigenen
#                      Dateien schreibt, geht das Framework nichts an.
#
# 🔴 KEINE SONDE HAELT EINE FORM WOERTLICH. Sie lesen die vorgefundene Form aus dem
# Traeger und stellen ihn auf die jeweils andere - dieselbe Lehre wie bei Pruefung 78:
# Eine Sonde, die einen Wert mitpflegen muss, faellt bei der naechsten Aenderung aus, und
# zwar als scheinbarer Befund. Auf einem Linux-Arbeitsplatz liegt der Bestand auf LF, und
# diese Sonden messen dort dasselbe.
M81_GEMISCHT = "mischt CRLF- und LF-Zeilen"
M81_ABWEICHEND = "Zeilenenden, während"
M81_UNMESSBAR = "Prüfung 81: kein Git-Bestand lesbar"

P81_OPFER = ".koolie/core/docs/RUNTIME_GLOSSARY.md"
P81_WURZEL = "README.md"
P81_KENNZEICHEN = ".koolie/QUELLREPOSITORIUM.md"
# Der Name traegt ein Nicht-ASCII-Zeichen, damit git ihn ohne `-z` quotet (D-352).
P81_UMLAUT = ".koolie/core/docs/Übersicht-sonde-81e.md"


def _81_umstellen(text: str) -> str:
    """Den Traeger durchgehend auf die jeweils ANDERE Form stellen."""
    ohne = text.replace("\r\n", "\n")
    return ohne if "\r\n" in text else ohne.replace("\n", "\r\n")


def _81_eine_zeile(text: str) -> str:
    """Genau EINE Zeile auf die andere Form - der Fall der eingeschleppten Zeile."""
    if "\r\n" in text:
        return text.replace("\r\n", "\n", 1)
    return text.replace("\n", "\r\n", 1)


def sonden_zeilenendeform() -> None:
    """Wirkungsnachweis zu Pruefung 81 an einem echten Repositorium."""
    root = kopie()
    try:
        pfad = P(root, *P81_OPFER.split("/"))
        urtext = lies(pfad)

        # --- Sonde 81c: ohne Git-Bestand ist sie nicht messbar, und sagt es -----------
        aus = validator_ausgabe(root)
        melde("SONDE", "81c", M81_UNMESSBAR in aus,
              "Ohne Git-Bestand meldet Pruefung 81 die Unmessbarkeit, statt leise zu "
              "bestehen - ein fehlender Gegenstand ist kein Messergebnis")
        if M81_UNMESSBAR not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "81" in z)[:400])

        if unterprozess(["git", "init", "-q", root]).returncode != 0:
            melde("BUENDEL", "-", False, "sonden_zeilenendeform  [git nicht erreichbar]")
            notiz("        Ohne git liest Pruefung 81 keinen Bestand; sie nimmt dann "
                  "ihren dritten Ausgang und ist nicht messbar.")
            return
        unterprozess(["git", "-C", root, "add", "-A"])

        # --- Gegenprobe 81a: der ausgelieferte Bestand laeuft durch ------------------
        aus = validator_ausgabe(root)
        ok = (M81_GEMISCHT not in aus and M81_ABWEICHEND not in aus
              and M81_UNMESSBAR not in aus)
        melde("GEGENPROBE", "81a", ok,
              "Der ausgelieferte Bestand laeuft durch - alle versionierten Texttraeger "
              "tragen dieselbe Form, und die Pruefung ist dabei nachweislich gelaufen")
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "81" in z or "Zeilenende" in z)[:400])

        # --- Sonde 81a: ein Traeger durchgehend auf der anderen Form -----------------
        schreib(pfad, _81_umstellen(urtext))
        aus = validator_ausgabe(root)
        melde("SONDE", "81a", M81_ABWEICHEND in aus,
              "Ein Traeger durchgehend auf der anderen Zeilenendeform wird gemeldet - "
              "die Pruefung nennt die Mehrheit und verlangt keine bestimmte Form")
        if M81_ABWEICHEND not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])

        # --- Sonde 81b: EINE eingeschleppte Zeile ------------------------------------
        schreib(pfad, _81_eine_zeile(urtext))
        aus = validator_ausgabe(root)
        melde("SONDE", "81b", M81_GEMISCHT in aus,
              "Eine einzige eingeschleppte Zeile der anderen Form wird gemeldet - genau "
              "der Fall, den ein Suchtext fand und keine der achtzig Pruefungen")
        if M81_GEMISCHT not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        schreib(pfad, urtext)

        # --- Sonde 81e: derselbe Fall unter einem Namen mit Umlaut (D-352) -----------
        upfad = P(root, *P81_UMLAUT.split("/"))
        schreib(upfad, _81_eine_zeile(urtext))
        unterprozess(["git", "-C", root, "add", "-A"])
        aus = validator_ausgabe(root)
        treffer = P81_UMLAUT + ": mischt" in aus
        melde("SONDE", "81e", treffer,
              "Ein Traeger mit Umlaut im Dateinamen und einer eingeschleppten Zeile wird "
              "gemeldet - git quotet solche Pfade ohne -z")
        if not treffer:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])
        os.remove(upfad)
        unterprozess(["git", "-C", root, "add", "-A"])

        # --- Sonde 81d: eine Wurzeldatei auf der anderen Form (D-351) -----------------
        wpfad = P(root, *P81_WURZEL.split("/"))
        wurtext = lies(wpfad)
        schreib(wpfad, _81_umstellen(wurtext))
        aus = validator_ausgabe(root)
        treffer = P81_WURZEL + ": trägt" in aus and M81_ABWEICHEND in aus
        melde("SONDE", "81d", treffer,
              "Eine Wurzeldatei ausserhalb des Kerns auf der anderen Form wird im "
              "Quellrepositorium gemeldet - das Kennzeichen macht den Zaehlbereich")
        if not treffer:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])

        # --- Gegenprobe 81b: dieselbe Datei in einem uebernehmenden Projekt ----------
        kpfad = P(root, *P81_KENNZEICHEN.split("/"))
        os.remove(kpfad)
        unterprozess(["git", "-C", root, "add", "-A"])
        aus = validator_ausgabe(root)
        ok = not (P81_WURZEL + ": trägt" in aus)
        melde("GEGENPROBE", "81b", ok,
              "Ohne Kennzeichen des Quellrepositoriums bleibt dieselbe Wurzeldatei "
              "unbeanstandet - sie gehoert dem uebernehmenden Projekt")
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if P81_WURZEL in z)[:400])
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_zeilenendeform,
        "Pruefung 81 haelt die Zeilenendeform des Arbeitsbaums zusammen, an einem "
        "echten Repositorium und ohne eine Form woertlich zu kennen")


# --- Pruefung 82: die Bestandsliste steht auf dem Stand des Releases (CR-2026-130) -
#
# FUENF EINHEITEN, UND DIE ZWEITE GEGENPROBE IST DIE, DIE MAN WEGLASSEN WUERDE.
#   82a (Gegenprobe) - der ausgelieferte Bestand laeuft durch, und die Pruefung ist
#                      dabei nachweislich gelaufen (keine Unmessbarkeitsmeldung).
#   82b (Gegenprobe) - 🔴 DIE D-299-PROBE. Ein uebernehmendes Projekt liegt Releases
#                      zurueck: VERSION und Bestandsliste tragen BEIDE denselben
#                      aelteren Stand, weil beide byte-gleich aus demselben Release
#                      ausgeliefert sind. Die Pruefung muss dort GRUEN sein - ohne
#                      Ausnahmemenge, ohne Sonderfall. Ohne diese Gegenprobe waere die
#                      Installationsfestigkeit eine Behauptung im Kopfkommentar statt
#                      eine gemessene Eigenschaft. Sie ist genau die Bauform, die
#                      0.90.0 zweimal gekostet hat (D-326).
#   82a (Sonde)      - eine Zeile auf einen anderen Stand gestellt wird gemeldet, und
#                      die Meldung nennt das Projekt. Das ist der gemessene Fall aus
#                      1.0.0 und 1.0.1.
#   82b (Sonde)      - die Spaltenueberschrift entfernt: der verlorene Anker wird als
#                      Fehler gemeldet, statt leise zu bestehen (D-23).
#   82c (Sonde)      - eine Tabelle ohne Datenzeile meldet eine Warnung und KEIN
#                      Messergebnis.
#   82d (Sonde)      - der Befund von 82a in der cp1252-Umgebung: gemeldet statt
#                      UnicodeEncodeError (K-168, seit 1.14.1).
#
# KEINE EINHEIT HAELT EINE VERSIONSNUMMER WOERTLICH. Sie lesen den Stand aus VERSION
# und rechnen daran - dieselbe Lehre wie bei Pruefung 78 und 81: Eine Sonde, die einen
# Wert mitpflegen muss, faellt beim naechsten Release aus, und zwar als scheinbarer
# Befund.
M82_ABWEICHEND = "steht auf Framework-Version"
M82_ANKER = "keine Tabelle mit der Spalte"
M82_LEER = "Prüfung 82 hat nichts gemessen"
M82_FEHLT = "als Nachweis der Auditierbarkeit"

P82_LISTE = ".koolie/core/governance/ADOPTION_REGISTRY.md"
P82_VERSION = ".koolie/core/VERSION"
P82_KENNZEICHEN = ".koolie/QUELLREPOSITORIUM.md"


def _82_stand(root: str) -> str:
    return lies(P(root, *P82_VERSION.split("/"))).strip()


def _82_anderer(stand: str) -> str:
    """Ein Stand, der dem echten sicher nicht gleicht - ohne eine Nummer zu kennen."""
    teile = stand.split(".")
    try:
        teile[-1] = str(int(teile[-1]) + 7)
    except (ValueError, IndexError):
        return stand + "-abweichend"
    return ".".join(teile)


def sonden_bestandsliste_stand() -> None:
    """Wirkungsnachweis zu Pruefung 82."""
    root = kopie()
    try:
        pfad = P(root, *P82_LISTE.split("/"))
        urtext = lies(pfad)
        stand = _82_stand(root)
        fremd = _82_anderer(stand)

        # --- Gegenprobe 82a: der ausgelieferte Bestand laeuft durch ------------------
        aus = validator_ausgabe(root)
        ok = (M82_ABWEICHEND not in aus and M82_ANKER not in aus
              and M82_LEER not in aus and M82_FEHLT not in aus)
        melde("GEGENPROBE", "82a", ok,
              "Die Bestandsliste des Releases laeuft durch - jede Zeile nennt den "
              "Stand aus VERSION, und die Pruefung ist dabei nachweislich gelaufen")
        if not ok:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "82" in z or "Bestandsliste" in z)[:400])

        # --- Gegenprobe 82b: DIE D-299-PROBE ----------------------------------------
        # Ein uebernehmendes Projekt: kein Kennzeichen des Quellrepositoriums (D-351),
        # und Liste wie VERSION tragen denselben AELTEREN Stand. Beide kommen
        # byte-gleich aus demselben Release.
        kennzeichen = P(root, *P82_KENNZEICHEN.split("/"))
        gesichert = lies(kennzeichen) if os.path.isfile(kennzeichen) else None
        if gesichert is not None:
            os.remove(kennzeichen)
        schreib(P(root, *P82_VERSION.split("/")), fremd + "\n")
        schreib(pfad, urtext.replace("**" + stand + "**", "**" + fremd + "**"))
        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "82b", M82_ABWEICHEND not in aus,
              "Ein uebernehmendes Projekt, das Releases zurueckliegt, laeuft durch - "
              "Liste und VERSION kommen byte-gleich aus demselben Release (D-299)")
        if M82_ABWEICHEND in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if M82_ABWEICHEND in z)[:400])
        schreib(P(root, *P82_VERSION.split("/")), stand + "\n")
        if gesichert is not None:
            schreib(kennzeichen, gesichert)
        schreib(pfad, urtext)

        # --- Sonde 82a: eine Zeile auf einem anderen Stand ---------------------------
        vorher = baumhash(root)
        gestellt = urtext.replace("**" + stand + "**", "**" + fremd + "**", 1)
        if gestellt == urtext:
            raise Praeparationsfehler(
                "Sonde 82a: keine Bestandszeile mit `**%s**` in %s - die Sonde hat "
                "ihren Gegenstand verloren" % (stand, P82_LISTE))
        schreib(pfad, gestellt)
        if baumhash(root) == vorher:
            raise Praeparationsfehler("Sonde 82a hat nichts geschrieben")
        aus = validator_ausgabe(root)
        melde("SONDE", "82a", M82_ABWEICHEND in aus,
              "Eine Bestandszeile auf einem anderen Stand wird gemeldet, und die "
              "Meldung nennt das Projekt - der Fall aus 1.0.0 und 1.0.1")
        if M82_ABWEICHEND not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])

        # --- Sonde 82d: derselbe Befund in der cp1252-Umgebung (K-168) ----------------
        # Die Meldung von 82a traegt ein ⚠️. Bis 1.14.0 brach der Validator in cp1252
        # an ihr mit UnicodeEncodeError ab und berichtete keinen einzigen Befund - der
        # Berichtsweg war nur in utf-8 gefahren (Bauform D-223). Verlangt: Befund und
        # Ergebniszeile stehen da, und das Zeichen kommt als Escape-Folge an.
        p = unterprozess([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                          "--root", root], kodierung="cp1252")
        aus = (p.stdout or "") + (p.stderr or "")
        ok = (M82_ABWEICHEND in aus and "Ergebnis:" in aus
              and "UnicodeEncodeError" not in aus and "\\u26a0" in aus)
        melde("SONDE", "82d", ok,
              "Derselbe Befund in der cp1252-Umgebung: gemeldet, mit Ergebniszeile, das "
              "Zeichen ausserhalb der Kodierung als Escape-Folge (K-168, D-223)")
        if not ok:
            notiz("        Ausgabe:", " | ".join(aus.splitlines()[-4:])[:400])

        # --- Sonde 82b: der verlorene Anker ------------------------------------------
        schreib(pfad, urtext.replace("Framework-Version", "Kernstand"))
        aus = validator_ausgabe(root)
        melde("SONDE", "82b", M82_ANKER in aus,
              "Geht die Spaltenueberschrift verloren, meldet die Pruefung es - eine "
              "Konsistenzpruefung ohne Anker bestuende sonst leise (D-23)")
        if M82_ANKER not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "FEHLER" in z)[:400])

        # --- Sonde 82c: eine Tabelle ohne Datenzeile ---------------------------------
        ohne = "\n".join(z for z in urtext.split("\n")
                         if not z.startswith("| `devpacks/"))
        if ohne == urtext:
            raise Praeparationsfehler(
                "Sonde 82c: keine Bestandszeile erkannt - die Sonde hat ihren "
                "Gegenstand verloren")
        schreib(pfad, ohne)
        aus = validator_ausgabe(root)
        melde("SONDE", "82c", M82_LEER in aus,
              "Eine Tabelle ohne Datenzeile meldet eine Warnung und KEIN Messergebnis "
              "- eine Null ohne Ergebniszeile ist kein Messwert")
        if M82_LEER not in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "82" in z)[:400])
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_bestandsliste_stand,
        "Pruefung 82 haelt die Bestandsliste gegen VERSION und ist in einem "
        "uebernehmenden Projekt gruen, ohne eine Versionsnummer zu kennen")

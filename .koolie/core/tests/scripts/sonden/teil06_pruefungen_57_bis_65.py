"""Sonden zu den Pruefungen 57, 58 und 60 bis 65.

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul
liest nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import os
import re

from .apparat import (
    ersetze, gegenprobe, lies, P, Praeparationsfehler, schreib, sonde, zeile_nach)


# --- Pruefung 57: kein ungebundener Pflichtplatzhalter als Vorbedingung -------------
#
# Der gemessene Fall stammt aus dem Blatt des Role Packs: RE-001-N09 verlangte das
# Uebungs-Overlay "ohne gesetztes <ISSUE_TRACKER>" - genau den Zustand, den Pruefung 55b
# im aktiven Overlay als Fehler meldet. Beide entstanden im SELBEN Release.
#
# WARUM ZWEI GEGENPROBEN. Eine Pruefung, die auf einen Suchtext anschlaegt, belegt mit
# einer Sonde nur, DASS sie meldet. Der Zuschnitt - Teilsatz statt Zelle - wird erst
# durch das Paar belegt: 57b traegt dieselbe Verneinung in einem ANDEREN Teilsatz und
# muss unbeanstandet bleiben. Ohne dieses Paar meldete die Pruefung jede Zelle mit, die
# irgendwo ein "ohne" fuehrt, und niemand saehe es.
M57_UNGEBUNDEN = "als nicht gesetzt ("

P57_BLATT = (".koolie/core/framework/role-packs/requirements-engineering/skills/"
             "role-re-ticket/TESTS.md").replace("/", os.sep)

# Die berichtigte Fassung der Zelle - Anker beider Eingriffe.
P57_HEUTE = "Übungs-Overlay, dessen `<ISSUE_TRACKER>` **gebunden** ist"


def _57_ungebunden(root: str) -> None:
    """Die Vorbedingung verlangt den Pflichtplatzhalter als nicht gesetzt."""
    ersetze(P(root, P57_BLATT),
            (P57_HEUTE, "Übungs-Overlay ohne gesetztes `<ISSUE_TRACKER>`, das"))


def _57_anderer_teilsatz(root: str) -> None:
    """Gegenprobe: dieselbe Verneinung, aber in einem anderen Teilsatz.

    Sie belegt den Zuschnitt. Eine Pruefung, die die ganze Zelle durchsucht, meldet
    diesen Fall mit - und waere damit zu breit.
    """
    ersetze(P(root, P57_BLATT),
            (P57_HEUTE,
             "Übungs-Overlay ohne gesetzte Kontrollstufe; `<ISSUE_TRACKER>` **gebunden**"))


sonde("57a", "Eine Vorbedingung verlangt einen Pflichtplatzhalter als nicht gesetzt - "
             "genau den Zustand, den Pruefung 55b im aktiven Overlay als Fehler meldet",
      _57_ungebunden, M57_UNGEBUNDEN)

gegenprobe("57a", "Das unveraenderte Repositorium bleibt unbeanstandet - keine "
                  "Vorbedingung fordert einen ungebundenen Pflichtplatzhalter",
           None, M57_UNGEBUNDEN)

gegenprobe("57b", "Dieselbe Verneinung in einem anderen Teilsatz bleibt zulaessig - die "
                  "Pruefung arbeitet auf Teilsaetzen und nicht auf ganzen Zellen",
           _57_anderer_teilsatz, M57_UNGEBUNDEN)


# --- Pruefung 58: Vollstaendigkeit des Decision-Record-Registers (D-169) -----------
M58_FEHLT = "steht in keiner Registerzeile. Ein Register, das seinen Gegenstand"
M58_FORM = "ist keine Kennung der Form D-NNN"
M58_ANKER = "Prüfung 58 hat ihren Gegenstand verloren"
P58_LOG = ".koolie/core/governance/DECISION_LOG.md".replace("/", os.sep)
P58_ROADMAP = ".koolie/core/docs/ROADMAP.md".replace("/", os.sep)
# ZUSAMMENGESETZT, aus demselben Grund wie bei der Sonde zu Pruefung 50: Dieses Skript
# liegt im Kern, und die Pruefung meldet jede dort GENANNTE Kennung ohne Registerzeile.
# Stuende eine der beiden woertlich hier, muesste sie in die Ausnahmemenge - und dann
# maesse die Sonde nichts. Auch der Kommentar nennt sie nicht.
D58_SYNTH = "D-" + "993"
D58_VERFEHLT = "D-" + "16" + "n"


def _58_freie_kennung(root: str) -> None:
    """Belegt, dass beide Sondenkennungen wirklich fehlen - sonst messen sie nichts."""
    text = lies(P(root, P58_LOG))
    for kennung in (D58_SYNTH, D58_VERFEHLT):
        if ("| " + kennung + " |") in text:
            raise Praeparationsfehler(
                "%s steht bereits im Register - die Sonde zu 58 braucht eine freie "
                "Kennung" % kennung)


def _58_nennung_ohne_register(root: str) -> None:
    """Eine Kennung wird in einem Kerntraeger genannt und steht in keiner Registerzeile."""
    _58_freie_kennung(root)
    pfad = P(root, P58_ROADMAP)
    schreib(pfad, lies(pfad).rstrip("\r\n") + "\r\n\r\n"
            + "Sondennachtrag: Die Begruendung steht im Entscheidungssatz (%s).\r\n"
            % D58_SYNTH)


def _58_form_verfehlt(root: str) -> None:
    """Der gemessene Fall: eine Kennung mit Platzhalter statt Nummer.

    Genau die Bauform, mit der die Registereintraege der Pruefungen 55 und 56
    ausgeliefert worden sind - und die ein Muster mit abschliessender Wortgrenze
    uebersieht.
    """
    _58_freie_kennung(root)
    pfad = P(root, P58_ROADMAP)
    schreib(pfad, lies(pfad).rstrip("\r\n") + "\r\n\r\n"
            + "Sondennachtrag: Die Begruendung steht im Entscheidungssatz (%s).\r\n"
            % D58_VERFEHLT)


def _58_anker_verlieren(root: str) -> None:
    """Ohne Registerzeilen hat Pruefung 58 keinen Gegenstand - und sagt es."""
    pfad = P(root, P58_LOG)
    text = lies(pfad)
    neu = re.sub(r"(?m)^\|(\s*)D-(\d+)(\s*)\|", r"|\1DR-\2\3|", text)
    if neu == text:
        raise Praeparationsfehler(
            "Keine Registerzeile der Form '| D-NNN |' gefunden - die Sonde zum "
            "verlorenen Anker haette nichts entfernt")
    schreib(pfad, neu)


def _58_nennung_mit_register(root: str) -> None:
    """Dieselbe Nennung MIT Registerzeile bleibt zulaessig - der erlaubte Fall."""
    _58_nennung_ohne_register(root)
    zeile_nach(P(root, P58_LOG), "| D-162 |",
               "| %s | Sondenentscheidung | Sondenbegruendung | 2026-09-18 | "
               "entschieden | Sondenweg |" % D58_SYNTH)


sonde("58a", "Eine D-Kennung, die ein Kerntraeger nennt und das Register nicht fuehrt, "
             "wird gemeldet - die Schwester des Falls von K-34 und K-55",
      _58_nennung_ohne_register, M58_FEHLT)

sonde("58b", "Eine Kennung mit Platzhalter statt Nummer wird gemeldet - genau die "
             "Bauform, mit der zwei Registereintraege ausgeliefert worden sind",
      _58_form_verfehlt, M58_FORM)

sonde("58c", "Ohne Registerzeilen meldet Pruefung 58 den verlorenen Gegenstand, statt "
             "leise zu bestehen", _58_anker_verlieren, M58_ANKER)

gegenprobe("58a", "Das unveraenderte Repositorium bleibt unbeanstandet - jede genannte "
                  "D-Kennung steht im Register", None, M58_FEHLT)

gegenprobe("58b", "Dieselbe Nennung MIT Registerzeile bleibt zulaessig - gemessen wird "
                  "das Fehlen der Zeile und nicht die Nennung", _58_nennung_mit_register,
           M58_FEHLT)


# --- Pruefung 60: der Befehlsschlitz, den der Ausloeser braucht (D-178) -----------
#
# Die Marken sind die Meldungstexte der Pruefung, nicht ihre Nummer: Eine Sonde, die
# auf eine Nummer ankert, bricht bei der naechsten Umnummerierung.
M60_FEHLT = "die Vorbedingung nennt den Schlitz nicht"
M60_ANKER = "kein Skill mit 'Exec(<..._COMMAND>)' im Frontmatter gefunden"
P60_KATALOG = ".koolie/core/tests/TEST_CATALOG.md".replace("/", os.sep)
P60_KATALOGANKER = "| FW-AK-02 (Basis) |"
P60_SKILLS = ".koolie/core/framework/skills".replace("/", os.sep)


# 🔴 Die eingefuegten Zeilen tragen `bestanden (Sondenbeleg, <Protokoll>; Client Pack <Kennung> <Version>)`, nicht `offen`. Eine
# Zeile mit `offen` hebt Kriterium 2 um eins, und Pruefung 46 meldet dann einen
# Rueckfall - die Gegenprobe saehe einen Fehler, den sie nicht gemeint hat.
# Gemessen am 2026-09-18: drei Abweichungen im ersten Sondenlauf zu 60.
#     Wer einen erlaubten Fall herstellt, muss ihn VOLLSTAENDIG herstellen.
def _60_katalogzeile(root: str, zeile: str) -> None:
    zeile_nach(P(root, P60_KATALOG), P60_KATALOGANKER, zeile)


def _60_ohne_schlitz(root: str) -> None:
    """Ein sitzung-Testfall ruft `/fw-change-small` und nennt keinen Befehlsschlitz.

    Genau die Gestalt, in der FW-SC-01 zwei Releases lang dastand - und die zwei
    Laeufe gekostet hat.
    """
    _60_katalogzeile(root,
        "| FW-SO-08 | Sondenzeile | Sondenvorbedingung ohne Befehlsangabe "
        "| `/fw-change-small \"<Sondenaufgabe>\"` | Ablehnung | Zugriff "
        "| sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _60_mit_schlitz(root: str) -> None:
    """Gegenprobe: dieselbe Zeile, aber die Vorbedingung nennt beide Schlitze."""
    _60_katalogzeile(root,
        "| FW-SO-09 | Sondenzeile | Sondenvorbedingung; `<TEST_COMMAND>` und "
        "`<LINT_COMMAND>` im `allow`-Korb | `/fw-change-small \"<Sondenaufgabe>\"` "
        "| Ablehnung | Zugriff | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _60_andere_pruefmethode(root: str) -> None:
    """Gegenprobe: derselbe Ausloeser bei Pruefmethode `review`.

    Eine Durchsicht braucht keinen Messbaum; die Regel gilt dem Lauf.
    """
    _60_katalogzeile(root,
        "| FW-SO-10 | Sondenzeile | Sondenvorbedingung ohne Befehlsangabe "
        "| `/fw-change-small \"<Sondenaufgabe>\"` | Ablehnung | Zugriff "
        "| review | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _60_skill_ohne_schlitz(root: str) -> None:
    """Gegenprobe: ein Skill, dessen Frontmatter keinen Befehl ausfuehrt.

    Sie belegt, dass der Zuschnitt nicht zu breit ist. `fw-repo-analyze` ist rein
    lesend und fuehrt keinen Befehlsschlitz.
    """
    _60_katalogzeile(root,
        "| FW-SO-11 | Sondenzeile | Sondenvorbedingung ohne Befehlsangabe "
        "| `/fw-repo-analyze <Sondenmodul>` | Ablehnung | Zugriff "
        "| sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _60_anker_verlieren(root: str) -> None:
    """Ohne `Exec(<..._COMMAND>)` in den Skillquellen hat Pruefung 60 keinen Gegenstand.

    Sie leitet ihn von dort ab; geht der Schluessel verloren, faende sie nichts und
    bestuende leise. Die Sonde belegt, dass sie das Fehlen selbst meldet (D-23).
    """
    basis = P(root, *P60_SKILLS.split(os.sep))
    getroffen = 0
    for name in sorted(os.listdir(basis)):
        pfad = os.path.join(basis, name, "SKILL.md")
        if not os.path.isfile(pfad):
            continue
        text = lies(pfad)
        neu = text.replace("Exec(<TEST_COMMAND>)", "Exec(kein-schlitz)")
        neu = neu.replace("Exec(<LINT_COMMAND>)", "Exec(kein-schlitz)")
        neu = neu.replace("Exec(<BUILD_COMMAND>)", "Exec(kein-schlitz)")
        if neu != text:
            schreib(pfad, neu)
            getroffen += 1
    if not getroffen:
        raise Praeparationsfehler(
            "Kein Skill fuehrt 'Exec(<..._COMMAND>)' im Frontmatter - die Sonde zu 60 "
            "haette keinen Anker")


sonde("60a", "Ein sitzung-Testfall ruft einen Skill auf, der einen Befehlsschlitz "
             "ausfuehrt, und nennt ihn in seiner Vorbedingung nicht - genau die "
             "Gestalt, die FW-SC-01 zwei Laeufe gekostet hat",
      _60_ohne_schlitz, M60_FEHLT)

sonde("60b", "Ohne 'Exec(<..._COMMAND>)' in den Skillquellen meldet Pruefung 60 den "
             "verlorenen Gegenstand, statt leise zu bestehen",
      _60_anker_verlieren, M60_ANKER)

gegenprobe("60a", "Das unveraenderte Repositorium bleibt unbeanstandet - die drei "
                  "betroffenen Zellen nennen ihren Schlitz seit 0.66.0",
           None, M60_FEHLT)

gegenprobe("60b", "Dieselbe Zeile mit beiden Schlitzen in der Vorbedingung bleibt "
                  "zulaessig - das ist die Abhilfe", _60_mit_schlitz, M60_FEHLT)

gegenprobe("60c", "Derselbe Ausloeser bei Pruefmethode `review` bleibt zulaessig - "
                  "eine Durchsicht braucht keinen Messbaum", _60_andere_pruefmethode,
           M60_FEHLT)

gegenprobe("60d", "Ein Skill, dessen Frontmatter keinen Befehl ausfuehrt, bleibt ohne "
                  "Befehlsangabe zulaessig - der Zuschnitt ist nicht zu breit",
           _60_skill_ohne_schlitz, M60_FEHLT)


# --- Pruefung 61: das Pruefmittelwort stammt aus dem Vokabular (D-181) ------------
#
# ANLASS. Die dreizehn Testblaetter trugen bis 0.67.0 das Wort `manuell` - 87 von 87
# Zellen -, und es steht in keinem Vokabular. Die Pruefungen 49 und 60 filtern auf
# `sitzung` und hatten dort NULL Gegenstand; nach der Umstellung meldete 60 zwanzig
# Zellen. Die Sonden treffen beide Orte, an denen das Wort steht: den zentralen
# Katalog und ein Blatt. Die Gegenproben belegen den zulaessigen Zusatz - ohne sie
# stuende nur fest, dass die Pruefung etwas meldet, nicht dass sie den richtigen
# Zuschnitt hat.
M61_FREMD = "steht nicht im Vokabular"
M61_ANKER = "keine Zelle mit Prüfmethode gefunden"
P61_KATALOG = ".koolie/core/tests/TEST_CATALOG.md".replace("/", os.sep)
P61_KATALOGANKER = "| FW-AK-02 (Basis) |"
P61_BLATT = ".koolie/core/framework/skills/fw-repo-analyze/TESTS.md".replace("/", os.sep)
P61_BLATTANKER = "| SK-001-N03 |"


def _61_katalogzeile(root: str, zeile: str) -> None:
    zeile_nach(P(root, P61_KATALOG), P61_KATALOGANKER, zeile)


def _61_fremdes_wort(root: str) -> None:
    """Eine Katalogzeile mit dem Wort `manuell` - genau der Stand vor 0.67.0."""
    _61_katalogzeile(root,
        "| FW-SO-12 | Sondenzeile | Sondenvorbedingung "
        "| `/fw-repo-analyze <Sondenmodul>` | Ablehnung | Zugriff "
        "| manuell | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _61_fremdes_wort_im_blatt(root: str) -> None:
    """Dasselbe Wort in einem der dreizehn Blaetter - dort stand es 87-mal."""
    zeile_nach(P(root, P61_BLATT), P61_BLATTANKER,
        "| SK-001-S99 | Sondenzeile | Sondenvorbedingung "
        "| `/fw-repo-analyze <Sondenmodul>` | Ablehnung | Zugriff "
        "| manuell | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _61_zulaessiger_zusatz(root: str) -> None:
    """Gegenprobe: `sitzung` mit Zusatz - die Schreibweise beider Bestaende."""
    _61_katalogzeile(root,
        "| FW-SO-13 | Sondenzeile | Sondenvorbedingung "
        "| `/fw-repo-analyze <Sondenmodul>` | Ablehnung | Zugriff "
        "| sitzung + Skript `validate-output.py --skill fw-repo-analyze` "
        "| bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _61_skript_und_review(root: str) -> None:
    """Gegenprobe: die beiden uebrigen Woerter des Vokabulars bleiben zulaessig.

    Ohne sie belegte der Lauf nur, dass `sitzung` durchkommt - der Zuschnitt waere
    dann zu eng, und niemand saehe es.
    """
    _61_katalogzeile(root,
        "| FW-SO-14 | Sondenzeile | Sondenvorbedingung | Sondeneingabe "
        "| Ablehnung | Zugriff | skript+sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")
    _61_katalogzeile(root,
        "| FW-SO-15 | Sondenzeile | Sondenvorbedingung | Sondeneingabe "
        "| Ablehnung | Zugriff | review | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


sonde("61a", "Eine Katalogzeile mit dem Wort `manuell` - dem Wort, das 87 Blattzellen "
             "trugen und das zwei Pruefungen ihren Gegenstand kostete",
      _61_fremdes_wort, M61_FREMD)

sonde("61b", "Dasselbe Wort in einem der dreizehn Testblaetter: Die Pruefung liest "
             "beide Bestaende, nicht nur den zentralen Katalog",
      _61_fremdes_wort_im_blatt, M61_FREMD)

gegenprobe("61a", "Das unveraenderte Repositorium bleibt unbeanstandet - alle 125 "
                  "Zellen tragen seit 0.67.0 ein Wort des Vokabulars",
           None, M61_FREMD)

gegenprobe("61b", "`sitzung` mit Zusatz bleibt zulaessig - geprueft wird das erste "
                  "Wort, nicht die ganze Zelle", _61_zulaessiger_zusatz, M61_FREMD)

gegenprobe("61c", "`skript+sitzung` und `review` bleiben zulaessig - der Zuschnitt ist "
                  "nicht auf `sitzung` verengt", _61_skript_und_review, M61_FREMD)


# --- Pruefung 62: die Version der Ausgabevorlage (D-185) --------------------------
#
# Die Pruefung ist entstanden, weil ein GEMESSENER LAUF sie veranlasst hat: Im ersten
# Buendellauf der Testblaetter meldete ein Lauf in einer Nebenbemerkung, die
# Attributtabelle seines Skills nenne 0.1.3 und der Kopf der Ausgabevorlage v0.1.1.
#
# ZWEI SONDEN, WEIL DIE FUNDSTELLE ZWEI GESTALTEN HAT: die Kopfzeile der Vorlage und
# die Zeile "Erstellt mit". Eine Sonde auf die Ueberschrift allein haette die zweite
# nicht getroffen - und genau sie trugen zwei Skills doppelt.
M62_WOERTLICH = "nennt die Version wörtlich"

P62_SKILL = ".koolie/core/framework/skills/fw-code-explain/SKILL.md".replace("/", os.sep)
P62_PLAN = ".koolie/core/framework/skills/fw-plan/SKILL.md".replace("/", os.sep)
P62_SCHLITZ = "v<Version aus dem Steckbrief>"


def _62_kopfzeile(root: str) -> None:
    """Die Kopfzeile der Ausgabevorlage traegt wieder eine woertliche Version."""
    ersetze(P(root, P62_SKILL),
            ("## Code-Erklärung – fw-code-explain " + P62_SCHLITZ,
             "## Code-Erklärung – fw-code-explain v9.9.9", 1))


def _62_erstellt_mit(root: str) -> None:
    """Die zweite Gestalt: die Zeile `Erstellt mit` im Ergebnisbericht."""
    ersetze(P(root, P62_PLAN),
            ("| Erstellt mit | fw-plan " + P62_SCHLITZ + " |",
             "| Erstellt mit | fw-plan v9.9.9 |", 1))


def _62_zweiter_schlitz(root: str) -> None:
    """Gegenprobe: der Schlitz darf mehrfach stehen - geprueft wird die ZAHL."""
    ersetze(P(root, P62_SKILL),
            ("## Code-Erklärung – fw-code-explain " + P62_SCHLITZ,
             "## Code-Erklärung – fw-code-explain " + P62_SCHLITZ
             + " (Vorlage " + P62_SCHLITZ + ")", 1))


sonde("62a", "Die Kopfzeile der Ausgabevorlage traegt wieder eine woertliche Version - "
             "genau der Stand vor 0.68.0 in zehn von dreizehn Traegern",
      _62_kopfzeile, M62_WOERTLICH)

sonde("62b", "Dieselbe Zahl in der Zeile `Erstellt mit` - die zweite Gestalt, die ein "
             "Zuschnitt auf die Ueberschrift verfehlt haette",
      _62_erstellt_mit, M62_WOERTLICH)

gegenprobe("62a", "Das unveraenderte Repositorium bleibt unbeanstandet - dreizehn "
                  "Traeger verweisen seit 0.68.0 auf ihren Steckbrief",
           None, M62_WOERTLICH)

gegenprobe("62b", "Der Schlitz darf mehrfach in einer Zeile stehen - geprueft wird die "
                  "woertliche ZAHL, nicht der Buchstabe v",
           _62_zweiter_schlitz, M62_WOERTLICH)


# --- Pruefung 63: der Nummernverweis, der ins Leere zeigt (D-193) ------------------
#
# Drei Sonden, weil der Gegenstand drei Gestalten hat: der Verweis mit vollem Pfad,
# der Verweis mit blossem Dateinamen (vier Testblaetter nennen ihr Ziel so - wer nur
# den vollen Pfad sucht, zaehlt 25 statt 30) und die MITTE einer bis-Spanne.
#
# Die zweite Gegenprobe ist die wichtigere: Eine Aufzeichnung darf denselben Verweis
# tragen, ohne gemeldet zu werden. Ein Protokoll nennt den Stand seines Tages (D-141).
M63_INS_LEERE = "diese Nummer fuehrt dort keine Ueberschrift"

P63_PROMPT = ".koolie/core/prompts/02-impact-analysis.md".replace("/", os.sep)
P63_BLATT = ".koolie/core/framework/skills/fw-error-analyze/TESTS.md".replace("/", os.sep)
P63_ZIEL = ".koolie/core/framework/core/02-privacy.md".replace("/", os.sep)
P63_PROTOKOLL = (".koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-1.md"
                 .replace("/", os.sep))


def _63_voller_pfad(root: str) -> None:
    """Ein anweisender Traeger nennt eine Nummer, die das Ziel nicht fuehrt."""
    ersetze(P(root, P63_PROMPT),
            ("02-privacy.md` Abschnitt 3.3 und 3.4",
             "02-privacy.md` Abschnitt 3.3 und 3.11", 1))


def _63_blosser_name(root: str) -> None:
    """Dieselbe Luecke in der zweiten Ausdrucksform - ohne Pfad, nur Dateiname."""
    ersetze(P(root, P63_BLATT),
            ("`02-privacy.md` Abschnitt 3.3 angefordert",
             "`02-privacy.md` Abschnitt 3.11 angefordert", 1))


def _63_spannenmitte(root: str) -> None:
    """Die MITTE einer bis-Spanne: `3.3 bis 3.5` nennt auch 3.4."""
    ersetze(P(root, P63_ZIEL), ("### 3.4 Tickets", "### 3.4a Tickets", 1))


def _63_aufzeichnung(root: str) -> None:
    """Eine Aufzeichnung traegt denselben Verweis - und bleibt unbeanstandet."""
    zeile_nach(P(root, P63_PROTOKOLL), "# Protokoll",
               "\nGemessen gegen `.koolie/core/framework/core/02-privacy.md` "
               "Abschnitt 3.11 - der Stand jenes Tages.")


sonde("63a", "Ein anweisender Traeger nennt `02-privacy.md` Abschnitt 3.11 - die "
             "Nummer fuehrt dort keine Ueberschrift",
      _63_voller_pfad, M63_INS_LEERE)

sonde("63b", "Dieselbe Luecke im blossen Dateinamen: vier Testblaetter nennen ihr Ziel "
             "ohne Pfad, und wer nur den Pfad sucht, zaehlt 25 statt 30",
      _63_blosser_name, M63_INS_LEERE)

sonde("63c", "Die MITTE einer bis-Spanne: faellt die Ueberschrift 3.4 weg, muss "
             "`Abschnitt 3.3 bis 3.5` sie trotzdem vermissen",
      _63_spannenmitte, M63_INS_LEERE)

gegenprobe("63a", "Das unveraenderte Repositorium bleibt unbeanstandet - seit 0.70.0 "
                  "loesen alle dreissig Nummernverweise auf",
           None, M63_INS_LEERE)

gegenprobe("63b", "Eine Aufzeichnung darf denselben Verweis tragen: Ein Protokoll "
                  "nennt den Stand seines Tages und wird nicht geglaettet (D-141)",
           _63_aufzeichnung, M63_INS_LEERE)

# --- Pruefung 64: die Ausgabemarke, die der Skill nicht verlangt (D-197) ----------
#
# Drei Sonden und drei Gegenproben, und die dritte Gegenprobe ist die wichtigere
# Haelfte: Die LETZTE Zelle einer Zeile ist der Ergebnisstatus und damit eine
# Aufzeichnung (D-117). Ein Lauf, der die Marke geschrieben HAT, darf das dort
# berichten - wer die Zeile statt der Spalte nimmt, entfernt den Gegenstand mit
# (dieselbe Trennlinie, die Pruefung 48 zieht).
#
# 🔴 Die eingefuegten Zeilen tragen `bestanden (Sondenbeleg, <Protokoll>; Client Pack <Kennung> <Version>)`, nicht `offen` - eine
# Zeile mit `offen` hebt Kriterium 2 um eins, und Pruefung 46 meldete dann einen
# Rueckfall (0.66.0). Und sie nennen die Befehlsschlitze in ihrer Vorbedingung,
# sonst meldete Pruefung 60 sie nebenbei mit.
M64_UNGEDECKT = "weder im Ausgabeformat (Abschnitt 5) noch"
M64_ANKER = "keine SKILL.md fuehrt eine Ausgabemarke in Abschnitt 5 oder 6"

P64_KATALOG = ".koolie/core/tests/TEST_CATALOG.md".replace("/", os.sep)
P64_KATALOGANKER = "| FW-AK-02 (Basis) |"
P64_SKILLS = ".koolie/core/framework/skills".replace("/", os.sep)
P64_SCHLITZE = "`<TEST_COMMAND>` und `<LINT_COMMAND>` im `allow`-Korb"


def _64_katalogzeile(root: str, zeile: str) -> None:
    zeile_nach(P(root, P64_KATALOG), P64_KATALOGANKER, zeile)


def _64_rueckfrage_ungedeckt(root: str) -> None:
    """Eine Zelle verlangt [RUECKFRAGE] - die steht in KEINEM Abschnitt 5 oder 6.

    Genau die Gestalt, in der siebzehn Zellen bis 0.73.0 dastanden. `sk004n01` hat
    am 2026-09-19 vorgefuehrt, was sie kostet: Der Lauf hat angehalten und
    zurueckgefragt und die Zeichenfolge nicht geschrieben - weil sie nirgends
    verlangt ist.
    """
    _64_katalogzeile(root,
        "| FW-SO-12 | Sondenzeile | Sondenvorbedingung; " + P64_SCHLITZE +
        " | `/fw-change-small \"<Sondenaufgabe>\"` | [RÜCKFRAGE] zur Aufteilung "
        "| Zugriff | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _64_halt_ungedeckt(root: str) -> None:
    """Eine Zelle verlangt [HALT] von einem Skill, der sie nur als Anweisung fuehrt.

    `fw-refactor` nennt [HALT] elfmal - in Arbeitsschritten und Fehlerbildern, und
    in keinem Ausgabeformat. Fuenf seiner sieben Zellen standen so da.
    """
    _64_katalogzeile(root,
        "| FW-SO-13 | Sondenzeile | Sondenvorbedingung; " + P64_SCHLITZE +
        " | `/fw-refactor <Sondenmodul> \"<Sondenziel>\"` | [HALT] nach dem "
        "Testnachweis | Zugriff | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _64_unzulaessig_ungedeckt(root: str) -> None:
    """Dieselbe Luecke in der zweiten gepruefen Spalte: Unzulaessiges Verhalten.

    Wer nur die Erwartungsspalte liest, uebersieht sie - `SK-011-P01` trug die
    Marke in beiden.
    """
    _64_katalogzeile(root,
        "| FW-SO-14 | Sondenzeile | Sondenvorbedingung; " + P64_SCHLITZE +
        " | `/fw-refactor <Sondenmodul> \"<Sondenziel>\"` | Ablehnung "
        "| Änderungen vor dem [HALT] | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _64_gedeckt(root: str) -> None:
    """Gegenprobe: dieselbe Marke bei einem Skill, der sie in Abschnitt 5 und 6 fuehrt.

    Das ist die Abhilfe - und zugleich der Beleg, dass der Zuschnitt nicht zu breit
    ist. `fw-change-small` fuehrt [HALT] in beiden Abschnitten.
    """
    _64_katalogzeile(root,
        "| FW-SO-15 | Sondenzeile | Sondenvorbedingung; " + P64_SCHLITZE +
        " | `/fw-change-small \"<Sondenaufgabe>\"` | [HALT] vor dem ersten "
        "Schreibzugriff | Zugriff | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278) |")


def _64_letzte_zelle(root: str) -> None:
    """Gegenprobe: die Marke in der LETZTEN Zelle - dem Ergebnisstatus.

    Ein Lauf, der [HALT] geschrieben HAT, darf das berichten. Die letzte Zelle ist
    eine Aufzeichnung (D-117, D-141); wer die Zeile statt der Spalte nimmt,
    entfernt den Gegenstand mit. Dieselbe Spalten-Ausnahme wie bei Pruefung 48.
    """
    _64_katalogzeile(root,
        "| FW-SO-16 | Sondenzeile | Sondenvorbedingung; " + P64_SCHLITZE +
        " | `/fw-refactor <Sondenmodul> \"<Sondenziel>\"` | Anhalten nach dem "
        "Testnachweis | Zugriff | sitzung | bestanden (Sondenbeleg, `.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`; Client Pack `claude-code` 2.1.278): der Lauf hat "
        "[HALT] wörtlich geschrieben |")


def _64_anker_verlieren(root: str) -> None:
    """Ohne Marke in Abschnitt 5 oder 6 hat Pruefung 64 keinen Gegenstand.

    Sie leitet ihn von dort ab; geht er verloren, faende sie nichts und bestuende
    leise. Die Sonde belegt, dass sie das Fehlen selbst meldet (D-23).
    """
    basis = P(root, *P64_SKILLS.split(os.sep))
    getroffen = 0
    for name in sorted(os.listdir(basis)):
        pfad = os.path.join(basis, name, "SKILL.md")
        if not os.path.isfile(pfad):
            continue
        text = lies(pfad)
        teile = text.split("## 5. Ausgabeformat")
        if len(teile) != 2:
            continue
        neu = teile[0] + "## 5. Ausgabeformat" + teile[1].replace(
            "[HALT]", "[SONDENMARKE]").replace("[RÜCKFRAGE]", "[SONDENMARKE]")
        if neu != text:
            schreib(pfad, neu)
            getroffen += 1
    if not getroffen:
        raise Praeparationsfehler(
            "Keine SKILL.md fuehrt eine Ausgabemarke ab Abschnitt 5 - die Sonde zu 64 "
            "haette keinen Anker")


sonde("64a", "Eine Zelle verlangt [RUECKFRAGE] - die Marke steht in KEINEM Abschnitt 5 "
             "und KEINEM Abschnitt 6 der zwoelf Skills und ist durchgehend "
             "Handlungsmarke",
      _64_rueckfrage_ungedeckt, M64_UNGEDECKT)

sonde("64b", "Eine Zelle verlangt [HALT] von fw-refactor, das die Marke nur in "
             "Arbeitsschritten und Fehlerbildern fuehrt - fuenf seiner sieben Zellen "
             "standen so da",
      _64_halt_ungedeckt, M64_UNGEDECKT)

sonde("64c", "Dieselbe Luecke in der Spalte Unzulaessiges Verhalten - wer nur die "
             "Erwartungsspalte liest, uebersieht sie",
      _64_unzulaessig_ungedeckt, M64_UNGEDECKT)

sonde("64d", "Ohne Ausgabemarke in Abschnitt 5 oder 6 meldet Pruefung 64 den "
             "verlorenen Gegenstand, statt leise zu bestehen",
      _64_anker_verlieren, M64_ANKER)

gegenprobe("64a", "Das unveraenderte Repositorium bleibt unbeanstandet - seit 0.73.0 "
                  "ist jede der zehn verbliebenen Markennennungen gedeckt",
           None, M64_UNGEDECKT)

gegenprobe("64b", "Dieselbe Marke bei einem Skill, der sie in Abschnitt 5 UND 6 "
                  "fuehrt, bleibt zulaessig - der Zuschnitt ist nicht zu breit",
           _64_gedeckt, M64_UNGEDECKT)

gegenprobe("64c", "Die Marke in der LETZTEN Zelle bleibt zulaessig: Der "
                  "Ergebnisstatus ist eine Aufzeichnung, und ein Lauf, der sie "
                  "geschrieben HAT, darf das berichten (D-117)",
           _64_letzte_zelle, M64_UNGEDECKT)

# --- Pruefung 65: der Ergebnisstatus ohne Beleg (D-202) ---------------------------
#
# Vier Sonden und drei Gegenproben. Die zweite Gegenprobe traegt die Trennlinie: Eine
# `review`-Zelle braucht KEIN Client Pack. D-117 spricht von DYNAMISCHEN Tests; ein
# Dokumentenreview misst keinen Client, und wer die Pflicht auf jede Zelle zieht,
# verlangt eine Angabe, die es nicht gibt.
#
# 🔴 Die eingefuegten Zeilen tragen `bestanden (Sondenbeleg, <Protokoll>; Client Pack
# <Kennung> <Version>)`, nicht `offen` - eine Zeile mit `offen` hebt Kriterium 2 um
# eins, und Pruefung 46 meldete dann einen Rueckfall (0.66.0). Und sie nennen die
# Befehlsschlitze in ihrer Vorbedingung, sonst meldete Pruefung 60 sie nebenbei mit.
M65_KEIN_PROTOKOLL = "nennt kein Protokoll unter"
M65_KEIN_PACK = "nennt kein Client Pack mit Produktversion"
M65_VOKABULAR = "beginnt nicht mit einem Wort des Vokabulars"
M65_ANKER = "das Vokabular des Ergebnisstatus ist unter Punkt 4 nicht mehr auffindbar"

P65_KATALOG = ".koolie/core/tests/TEST_CATALOG.md".replace("/", os.sep)
P65_KATALOGANKER = "| FW-AK-02 (Basis) |"
P65_SCHLITZE = "`<TEST_COMMAND>` und `<LINT_COMMAND>` im `allow`-Korb"
P65_PROTOKOLL = "`.koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-3.md`"
P65_PACK = "Client Pack `claude-code` 2.1.278"


def _65_katalogzeile(root: str, zeile: str) -> None:
    zeile_nach(P(root, P65_KATALOG), P65_KATALOGANKER, zeile)


def _65_ohne_protokoll(root: str) -> None:
    """Ein `bestanden` ohne Protokollverweis - die Gestalt, die Punkt 4 verbietet.

    Punkt 4 sagt das seit der Erstfassung des Katalogs, und keine Pruefung hat es
    bis 0.74.0 durchgesetzt. Eine Abnahme ohne Beleg ist eine Behauptung.
    """
    _65_katalogzeile(root,
        "| FW-SO-17 | Sondenzeile | Sondenvorbedingung; " + P65_SCHLITZE +
        " | `/fw-refactor <Sondenmodul> \"<Sondenziel>\"` | Anhalten | Zugriff "
        "| sitzung | bestanden (Sondenbeleg ohne Protokollverweis) |")


def _65_ohne_pack(root: str) -> None:
    """Ein `bestanden` einer sitzung-Zelle mit Protokoll, aber ohne Pack und Version.

    Das ist die Haelfte, die D-117 traegt: Ein Ergebnisstatus DECKT KEIN ANDERES
    PACK. Ohne die Version sagt er nicht, gegen welchen Produktstand gemessen wurde -
    und genau das ist am 2026-09-18 an einer vierzig Releases alten Zelle
    aufgefallen (D-113).
    """
    _65_katalogzeile(root,
        "| FW-SO-18 | Sondenzeile | Sondenvorbedingung; " + P65_SCHLITZE +
        " | `/fw-refactor <Sondenmodul> \"<Sondenziel>\"` | Anhalten | Zugriff "
        "| sitzung | bestanden (" + P65_PROTOKOLL + ") |")


def _65_fremdes_wort(root: str) -> None:
    """Ein Statuswort, das im Vokabular von Punkt 4 nicht steht.

    Dieselbe Bauform wie beim Pruefmittelwort `manuell` (D-181): ein Wort, das fuer
    jeden Leser richtig aussieht und fuer jeden Zaehler ein Fremdwort ist.
    """
    _65_katalogzeile(root,
        "| FW-SO-19 | Sondenzeile | Sondenvorbedingung; " + P65_SCHLITZE +
        " | `/fw-refactor <Sondenmodul> \"<Sondenziel>\"` | Anhalten | Zugriff "
        "| sitzung | geprüft (" + P65_PROTOKOLL + "; " + P65_PACK + ") |")


def _65_anker_verlieren(root: str) -> None:
    """Ohne die Vokabularzeile von Punkt 4 hat Pruefung 65 keinen Gegenstand.

    Sie leitet es von dort ab statt es zu pflegen; geht die Zeile verloren, faende
    sie nichts und bestuende leise. Die Sonde belegt, dass sie das Fehlen selbst
    meldet (D-23).
    """
    pfad = P(root, P65_KATALOG)
    text = lies(pfad)
    if "**Ergebnisstatus:**" not in text:
        raise Praeparationsfehler(
            "TEST_CATALOG.md fuehrt die Marke '**Ergebnisstatus:**' nicht mehr - die "
            "Sonde zu 65 haette keinen Anker")
    schreib(pfad, text.replace("**Ergebnisstatus:**", "**Status des Ergebnisses:**", 1))


def _65_review_ohne_pack(root: str) -> None:
    """Gegenprobe: eine review-Zelle mit Protokoll, aber ohne Pack - zulaessig.

    Das ist die Trennlinie, und sie belegt, dass der Zuschnitt nicht zu breit ist:
    D-117 spricht von dynamischen Tests. Ein Dokumentenreview misst keinen Client.
    """
    _65_katalogzeile(root,
        "| FW-SO-20 | Sondenzeile | Sondenvorbedingung | Abgleich zweier Fassungen "
        "| keine Abweichung | Abweichung | review | bestanden (" +
        P65_PROTOKOLL + ") |")


def _65_vollstaendig(root: str) -> None:
    """Gegenprobe: der vollstaendige Fall - Protokoll, Pack und Version.

    Er belegt, dass die Pruefung einen richtig belegten Status durchlaesst; ohne
    ihn wuesste niemand, ob sie ueberhaupt etwas durchlaesst.
    """
    _65_katalogzeile(root,
        "| FW-SO-21 | Sondenzeile | Sondenvorbedingung; " + P65_SCHLITZE +
        " | `/fw-refactor <Sondenmodul> \"<Sondenziel>\"` | Anhalten | Zugriff "
        "| sitzung | bestanden (" + P65_PROTOKOLL + "; " + P65_PACK + ") |")


sonde("65a", "Ein `bestanden` ohne Protokollverweis - Punkt 4 verlangt ihn seit der "
             "Erstfassung, und keine Pruefung hat es durchgesetzt",
      _65_ohne_protokoll, M65_KEIN_PROTOKOLL)

sonde("65b", "Ein `bestanden` einer sitzung-Zelle ohne Client Pack und Produktversion "
             "- ein Ergebnisstatus deckt kein anderes Pack (D-117)",
      _65_ohne_pack, M65_KEIN_PACK)

sonde("65c", "Ein Statuswort ausserhalb des Vokabulars von Punkt 4 - dieselbe Bauform "
             "wie das Pruefmittelwort `manuell` (D-181)",
      _65_fremdes_wort, M65_VOKABULAR)

sonde("65d", "Ohne die Vokabularzeile unter Punkt 4 meldet Pruefung 65 den verlorenen "
             "Gegenstand, statt leise zu bestehen",
      _65_anker_verlieren, M65_ANKER)

gegenprobe("65a", "Das unveraenderte Repositorium bleibt unbeanstandet - alle 125 "
                  "Ergebniszellen tragen ihren Beleg",
           None, M65_KEIN_PROTOKOLL)

gegenprobe("65b", "Eine review-Zelle ohne Client Pack bleibt zulaessig: D-117 spricht "
                  "von DYNAMISCHEN Tests, ein Dokumentenreview misst keinen Client",
           _65_review_ohne_pack, M65_KEIN_PACK)

gegenprobe("65c", "Der vollstaendige Fall - Protokoll, Pack und Version - laeuft durch",
           _65_vollstaendig, M65_KEIN_PROTOKOLL)

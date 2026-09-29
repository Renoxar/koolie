"""Sonden zu den Pruefungen 102 und 103 sowie 26 bis 36, zum Suchkanal, zu den
Zusagenfeldern bei der Installation, zur Kandidatenpruefung; Selbstproben des
Praeparations- und des Kennungswaechters.

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul
liest nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import io
import json
import os
import re
import shutil
import sys
import tempfile

from .apparat import (
    _p, aufraeumen, buendel, ersetze, ersetzt, frei, gegenprobe, installation, kopie,
    lies, melde, notiz, P, Praeparationsfehler, QUELLE, schreib, sonde, unterprozess,
    VALIDATOR, validator_ausgabe, zeile_nach)
from .teil01_grundbestand_und_installation import _so_status, SO_PLATZHALTER


# --- Pruefung 102: die Form des Klaerungsregisters (CR-2026-158, D-465) -------------------
M102_LAGE = "statt in der Klärungstabelle (Abschnitt 1)"
M102_STATUS = "kein Wert der Legende"
M102_KETTE = "das selbst zusammengelegt ist"
M102_ANKER = "Prüfung 102 leitet ihr Vokabular daraus ab und hat ihren Anker verloren"
P102_LOG = ".koolie/core/governance/DECISION_LOG.md".replace("/", os.sep)
P102_ANKER_K = "| K-56 | "
P102_ANKER_D = "| D-464 | "
# Zusammengesetzt wie K50_SYNTH: Pruefung 50 meldet jede im Kern genannte Kennung ohne Zeile.
K102_SYNTH = "K-" + "95"


def _102_zeile(status: str) -> str:
    return "| %s | Sondenfrage? | niedrig | Sondenbegruendung | Sondenweg | %s |" % (K102_SYNTH, status)


def _102_in_entscheidungstabelle(root: str) -> None:
    """Ein Klaerungspunkt unter den Decision Records - der Zustand vor 1.18.1 (114 Zeilen)."""
    zeile_nach(P(root, P102_LOG), P102_ANKER_D, _102_zeile("offen"))


def _102_status_ausserhalb(root: str) -> None:
    """Eine Statuszelle, die mit einem Wort ausserhalb der Legende beginnt."""
    zeile_nach(P(root, P102_LOG), P102_ANKER_K, _102_zeile("**beantwortet mit `1.0.0`**"))


def _102_kette(root: str) -> None:
    """Zusammengelegt mit einem Punkt, der selbst zusammengelegt ist (K-43 -> K-185)."""
    zeile_nach(P(root, P102_LOG), P102_ANKER_K, _102_zeile("zusammengelegt mit K-43: Sonde"))


def _102_anker_verlieren(root: str) -> None:
    ersetze(P(root, P102_LOG), ("*Klärungspunkte:*", "*Offene Punkte:*"))


def _102_eingeplant(root: str) -> None:
    """Erlaubt: ein neuer Punkt in Abschnitt 1, eingeplant mit Ziel in der Klammer."""
    zeile_nach(P(root, P102_LOG), P102_ANKER_K,
               _102_zeile("🔴 **eingeplant (1.20.0 Schutzschicht)**: Sonde"))


sonde("102a", "Pruefung 102: ein Klaerungspunkt steht unter den Decision Records statt "
      "in der Klaerungstabelle", _102_in_entscheidungstabelle, M102_LAGE)
sonde("102b", "Pruefung 102: eine Statuszelle beginnt mit einem Wort ausserhalb der Legende",
      _102_status_ausserhalb, M102_STATUS)
sonde("102c", "Pruefung 102: ein Punkt ist mit einem Punkt zusammengelegt, der selbst "
      "zusammengelegt ist", _102_kette, M102_KETTE)
sonde("102d", "Pruefung 102: ohne den Legendenanker meldet sie den Verlust statt still "
      "nichts zu pruefen", _102_anker_verlieren, M102_ANKER)
gegenprobe("102a", "Pruefung 102: das ausgelieferte Register traegt Lage und Statusanfang "
           "jedes Klaerungspunkts richtig", None, M102_STATUS)
gegenprobe("102b", "Pruefung 102: ein neuer Punkt mit Markierung und Ziel in der Klammer "
           "bleibt unbeanstandet", _102_eingeplant, M102_STATUS)


# --- Pruefung 103: der Stand einer Ergebniszelle (CR-2026-160, D-472, K-61) --------------
# Die Gegenprobe rechnet den Stand HIER nach, nicht mit der Funktion des Validators: Stimmen
# beide Rechnungen nicht ueberein, faellt sie - zwei Stellen, die einander pruefen, statt
# einer, die sich selbst bestaetigt.
M103_VERALTET = "Belegstand veraltet"
M103_LEER = "ein Stand ohne Gegenstand belegt nichts"
P103_BLATT = ".koolie/core/framework/skills/fw-refactor/TESTS.md".replace("/", os.sep)
P103_ANKER = "`validate-output.py --skill fw-refactor`: **bestanden**."
P103_GEGENSTAND = "framework/skills/fw-refactor/SKILL.md"


def _103_stand(root: str, pfade: list) -> str:
    import hashlib
    h = hashlib.sha256()
    for pfad in pfade:
        inhalt = io.open(os.path.join(root, ".koolie", "core", *pfad.split("/")), "rb").read()
        h.update(pfad.encode("utf-8") + b"\n" + inhalt.replace(b"\r\n", b"\n") + b"\n")
    return h.hexdigest()[:12]


def _103_marke(root: str, wert: str, pfad: str) -> None:
    ersetze(P(root, P103_BLATT), (P103_ANKER, P103_ANKER + " [Stand: %s; %s]" % (wert, pfad)))


def _103_veraltet(root: str) -> None:
    # ein Stand, der zu keinem heutigen Inhalt passt
    _103_marke(root, "0123456789ab", P103_GEGENSTAND)


def _103_ohne_gegenstand(root: str) -> None:
    _103_marke(root, "0123456789ab", "framework/skills/fw-refactor/GIBTESNICHT.md")


def _103_passend(root: str) -> None:
    _103_marke(root, _103_stand(root, [P103_GEGENSTAND]), P103_GEGENSTAND)


sonde("103a", "Pruefung 103: eine Ergebniszelle traegt einen Stand, der nicht zum heutigen "
      "Gegenstand passt", _103_veraltet, M103_VERALTET)
sonde("103b", "Pruefung 103: eine Standmarke nennt einen Gegenstand, den es nicht gibt",
      _103_ohne_gegenstand, M103_LEER)
gegenprobe("103a", "Pruefung 103: ein Stand, der zum Gegenstand passt, bleibt unbeanstandet",
           _103_passend, M103_VERALTET)

# --- Pruefung 26 und der Suchkanal (CR-2026-047, D-47) ----------------------------
#
# Zwei Gegenstaende in einem Block, weil sie dieselbe Entscheidung tragen: Der Suchkanal
# wird vom Schutz-Hook durchgesetzt (nicht von der Berechtigungsdatei), und ein Client
# ohne Suchwerkzeug darf das erklaeren, ohne dass daraus ein Schlupfloch wird.

def _manifest_pfad(root: str, pack: str) -> str:
    return os.path.join(root, ".koolie/core", "clients", pack, "manifest.json")


def _manifest_aendern(root: str, pack: str, aenderung) -> None:
    pfad = _manifest_pfad(root, pack)
    man = json.loads(lies(pfad))
    aenderung(man)
    schreib(pfad, json.dumps(man, ensure_ascii=False, indent=2) + "\r\n")


def _abwesenheit_ohne_begruendung(root: str) -> None:
    def f(man):
        man["hook_tools_absent"] = ["search"]
        man.pop("_hook_tools_absent_note", None)
    _manifest_aendern(root, "devin-desktop", f)


def _abwesenheit_widerspricht(root: str) -> None:
    # 'write' fuer abwesend erklaeren, obwohl die Berechtigungsschicht ein
    # Schreibwerkzeug kennt - das ist der Missbrauchsfall, gegen den die Pruefung steht.
    def f(man):
        man["hook_tools_absent"] = ["write"]
        man["_hook_tools_absent_note"] = "Sonde: absichtlich widerspruechlich."
    _manifest_aendern(root, "devin-desktop", f)


sonde("26", "Erklaerte Abwesenheit ohne Begruendung wird gemeldet",
      _abwesenheit_ohne_begruendung, "_hook_tools_absent_note fehlt oder ist leer")
sonde("26", "Erklaerte Abwesenheit im Widerspruch zu permission_tools wird gemeldet",
      _abwesenheit_widerspricht, "permission_tools nennt dafuer aber")
gegenprobe("26", "Die ausgelieferte Abwesenheitserklaerung bleibt unbeanstandet",
           None, "hook_tools_absent")


def sonden_suchkanal() -> None:
    """Der Schutz-Hook erreicht die Suchwerkzeuge - und nur mit dem richtigen Pfad.

    Bis 0.29.0 war der Suchkanal auf beiden Schichten unbewacht: kein Hook-Eintrag und
    keine Berechtigungsregel (B04, Lauf B04-5). Eine Regel traegt hier auch nicht - die
    Suchwerkzeuge dieses Clients werten keine Pfadregeln aus (AP2-CC-02). Der Hook ist
    die einzige Schranke, und deshalb wird sie gemessen.

    Die Gegenprobe ist der wichtigere Teil: Ein Hook, der jede Suche blockiert, bestuende
    die Sonde und machte das Suchwerkzeug unbenutzbar.
    """
    hook = os.path.join(QUELLE, ".koolie/core", "tests", "scripts",
                        "hook-check-secrets.py")

    def hooklauf(werkzeug: str, eingabe: dict) -> int:
        p = unterprozess([sys.executable, hook, "--fail-closed"],
                         input=json.dumps({"tool_name": werkzeug,
                                           "tool_input": eingabe},
                                          ensure_ascii=False))
        return p.returncode

    melde("SONDE", "B04", hooklauf("Grep", {"pattern": "x", "path": "sonde/.env"}) == 2,
          "Suchwerkzeug auf einen Secret-Pfad wird blockiert")
    melde("SONDE", "B04", hooklauf("Glob", {"pattern": "**/*.pem"}) == 2,
          "Suchmuster auf Schluesseldateien wird blockiert")
    melde("GEGENPROBE", "B04",
          hooklauf("Grep", {"pattern": "x", "path": "src/"}) == 0,
          "Suche in einem gewoehnlichen Pfad bleibt moeglich")
    melde("GEGENPROBE", "B04",
          hooklauf("Grep", {"pattern": "x", "path": ".koolie/core/framework/core/"}) == 0,
          "Suche im Kernverzeichnis bleibt moeglich - lesen darf der Agent ihn")


buendel(sonden_suchkanal,
        "Der Schutz-Hook faengt Grep und Glob auf geschuetzte Pfade ab und laesst eine "
        "gewoehnliche Suche durch - die einzige Schranke des Suchkanals")


# --- Pruefung 27 und der Installationsabbruch (CR-2026-050, D-50) -----------------
#
# Zwei Schichten, zwei Sonden: Der Validator findet das verworfene Zusagenfeld im
# Repositorium, install.py bricht bei der Installation ab. Die zweite ist die
# wirksamere - sie steht zwischen dem Befund und einer ausgelieferten Installation.

def _ersatz_entfernen(root: str) -> None:
    pfad = _manifest_pfad(root, "claude-code")
    man = json.loads(lies(pfad))
    man["skill_frontmatter"].pop("skill_permissions_ersatz", None)
    schreib(pfad, json.dumps(man, ensure_ascii=False, indent=2) + "\r\n")


def _ersatz_leeren(root: str) -> None:
    # Ein leerer Begleitsatz ist kein Begleitsatz - dieselbe Strenge wie bei Pruefung 26.
    pfad = _manifest_pfad(root, "claude-code")
    man = json.loads(lies(pfad))
    man["skill_frontmatter"]["skill_permissions_ersatz"] = "   "
    schreib(pfad, json.dumps(man, ensure_ascii=False, indent=2) + "\r\n")


sonde("27", "Verworfenes Zusagenfeld ohne benannten Ersatz wird gemeldet",
      _ersatz_entfernen, "traegt eine Zusage und steht in skill_frontmatter.drop_fields")
sonde("27", "Leerer Ersatzsatz gilt nicht als benannter Ersatz",
      _ersatz_leeren, "traegt eine Zusage und steht in skill_frontmatter.drop_fields")
gegenprobe("27", "Der ausgelieferte Ersatzsatz bleibt unbeanstandet",
           None, "traegt eine Zusage und steht in skill_frontmatter.drop_fields")


def sonden_zusagenfeld_installation() -> None:
    """install.py bricht ab, statt eine Zusage folgenlos zu verwerfen.

    Der Validator meldet denselben Fehler im Repositorium; diese Sonde misst die Stelle,
    an der es zaehlt - den Schreibvorgang in ein Projekt. Die Gegenprobe belegt, dass die
    Installation mit benanntem Ersatz weiterhin durchlaeuft; ohne sie stuende nur fest,
    dass irgendetwas abbricht.
    """
    ziel = tempfile.mkdtemp(prefix="lw-b01-")
    try:
        quelle = os.path.join(ziel, "quelle")
        shutil.copytree(QUELLE, quelle, ignore=shutil.ignore_patterns(".git"))
        werkzeug = os.path.join(quelle, ".koolie/core", "install.py")

        frei = os.path.join(ziel, "mit-ersatz")
        os.makedirs(frei)
        p = unterprozess([sys.executable, werkzeug, "--client", "claude-code",
                          "--root", frei])
        melde("GEGENPROBE", "B01", p.returncode == 0,
              "Installation mit benanntem Ersatz laeuft durch")
        if p.returncode != 0:
            notiz("        Ausgabe:", " | ".join(
                ((p.stdout or "") + (p.stderr or "")).splitlines()[:4]))

        _ersatz_entfernen(quelle)
        ohne = os.path.join(ziel, "ohne-ersatz")
        os.makedirs(ohne)
        q = unterprozess([sys.executable, werkzeug, "--client", "claude-code",
                          "--root", ohne])
        aus = (q.stdout or "") + (q.stderr or "")
        gemeldet = "traegt eine Zusage und steht in drop_fields" in aus
        melde("SONDE", "B01", q.returncode != 0 and gemeldet,
              "Installation bricht ab, wenn das Zusagenfeld ersatzlos entfiele")
        if not (q.returncode != 0 and gemeldet):
            notiz("        Exit:", q.returncode, "| Ausgabe:",
                  " | ".join(aus.splitlines()[:4]))
    finally:
        aufraeumen(ziel)


buendel(sonden_zusagenfeld_installation,
        "install.py bricht beim Schreiben in ein Projekt ab, wenn eine Zusage ohne "
        "benannten Ersatz verworfen wurde, und laeuft mit Ersatz durch")


# --- 28: Lesesperre gegen Schreibsperre (B07, D-55) ------------------------------
# Drei Sonden, weil die Pruefung drei Wege hat, falsch zu sein: Sie kann den Fehler in
# der Quelle uebersehen, ihn in der Installation uebersehen - und sie kann ihre eigene
# Deklaration nicht mehr finden und dadurch leise bestehen. Die Gegenprobe ist hier die
# wichtigere Haelfte: Beide Traeger erklaeren im Fliesstext, dass die Strukturpfade
# gerade NICHT in <EXCLUDED_PATHS> gehoeren, und nennen dabei beides in einer Zeile. Eine
# Pruefung, die jede Nennung meldet, wuerde den richtigen Text beanstanden.
VORLAGE_28 = ".koolie/core/templates/project-overlay/OVERLAY.md"
REGEL_28 = ".koolie/core/framework/runtime/rules/20-project-overlay.md"


def _strukturpfad_in_ausschluss(root: str) -> None:
    pfad = _p(root, VORLAGE_28)
    text = lies(pfad)
    alt = "| Ausgeschlossene Pfade (weder lesen noch \u00e4ndern) | `<EXCLUDED_PATHS>` |"
    schreib(pfad, text.replace(
        alt, alt + " `<RUNTIME_DIR>/`,", 1))


def _strukturpfad_in_laufzeitregel(root: str) -> None:
    pfad = _p(root, REGEL_28)
    text = lies(pfad)
    alt = "- Ausgeschlossene Pfade, weder lesen noch \u00e4ndern (`<EXCLUDED_PATHS>`):"
    schreib(pfad, text.replace(alt, alt + " `<ROOT_INSTRUCTION_FILE>`,", 1))


def _beschriftung_verlieren(root: str) -> None:
    pfad = _p(root, REGEL_28)
    text = lies(pfad)
    schreib(pfad, text.replace(
        "- Ausgeschlossene Pfade, weder lesen noch \u00e4ndern (`<EXCLUDED_PATHS>`):",
        "- Gesperrte Verzeichnisse (`<EXCLUDED_PATHS>`):", 1))


def _hinweis_ohne_deklaration(root: str) -> None:
    """Gegenprobe: dieselben Angaben im Fliesstext, aber keine Deklaration."""
    pfad = _p(root, REGEL_28)
    text = lies(pfad)
    schreib(pfad, text.replace(
        "## Freigegebene Befehle",
        "Hinweis: `<RUNTIME_DIR>/`, `<ROOT_INSTRUCTION_FILE>` und `.koolie/project-overlay/` "
        "geh\u00f6ren nicht in `<EXCLUDED_PATHS>` - ihr Schreibschutz ist kein "
        "Leseverbot.\r\n\r\n## Freigegebene Befehle", 1))


sonde("28a", "Strukturpfad in der <EXCLUDED_PATHS>-Zeile der Overlay-Vorlage",
      _strukturpfad_in_ausschluss, "Die Deklaration von <EXCLUDED_PATHS> nennt")

sonde("28b", "Strukturpfad in der <EXCLUDED_PATHS>-Zeile der Laufzeitregel",
      _strukturpfad_in_laufzeitregel, "Die Deklaration von <EXCLUDED_PATHS> nennt")

sonde("28c", "Verlorene Beschriftung - die Pruefung darf nicht leise bestehen",
      _beschriftung_verlieren, "keine Zeile ist als Deklaration erkennbar")

gegenprobe("28", "Dieselben Pfade im Fliesstext, ausdruecklich ausgeschlossen",
           _hinweis_ohne_deklaration, "Die Deklaration von <EXCLUDED_PATHS> nennt")


# --- 29: K3-Kategorien in Kurz- und Langform (B09, D-52) ------------------------
# Zwei Fehlerbilder, beide vorgekommen: eine fehlende Kategorie in der Kurzform - sie
# fuehrte bis 0.31.0 nur sechs von acht - und eine Bedingung an einer Kategorie, die
# unbedingt gilt. Dazu die dritte Sonde auf den verlorenen Anker, aus demselben Grund
# wie bei 28c.
KURZFORM_29 = ".koolie/core/framework/runtime/root-instruction.md"
LANGFORM_29 = ".koolie/core/framework/core/02-privacy.md"


def _kategorie_entfernen(root: str) -> None:
    pfad = _p(root, KURZFORM_29)
    text = lies(pfad)
    schreib(pfad, text.replace(
        "Sicherheitskonfigurationen mit Schutzwirkung, interne Adressen",
        "interne Adressen", 1))


def _bedingung_einfuegen(root: str) -> None:
    pfad = _p(root, LANGFORM_29)
    text = lies(pfad)
    schreib(pfad, text.replace(
        "- interne Adressen, Hostnamen, Netzpl\u00e4ne, Mandanten- und Umgebungskennungen",
        "- interne Adressen, Hostnamen, Netzpl\u00e4ne, Mandanten- und Umgebungskennungen, "
        "sofern nicht im Overlay ausdr\u00fccklich als K1 eingestuft", 1))


def _anker_verlieren(root: str) -> None:
    pfad = _p(root, KURZFORM_29)
    text = lies(pfad)
    schreib(pfad, text.replace("- Immer K3, ausnahmslos", "- Stets K3, ausnahmslos", 1))


def _kurzform_umformulieren(root: str) -> None:
    """Gegenprobe: kuerzer formuliert, aber keine Kategorie weniger."""
    pfad = _p(root, KURZFORM_29)
    text = lies(pfad)
    schreib(pfad, text.replace(
        "Sicherheitskonfigurationen mit Schutzwirkung, interne Adressen",
        "Sicherheitskonfigurationen, interne Adressen", 1))


sonde("29a", "Fehlende K3-Kategorie in der Kurzform",
      _kategorie_entfernen, "nennt die Kategorie 'Sicherheitskonfigurationen' nicht")

sonde("29b", "Bedingung an einer unbedingten K3-Kategorie",
      _bedingung_einfuegen, "traegt eine Bedingung")

sonde("29c", "Der verlorene Anker der K3-Liste - die Pruefung meldet ihr Fehlen selbst, statt "
      "leise zu bestehen",
      _anker_verlieren, "ist nicht mehr auffindbar")

gegenprobe("29", "Kuerzere Formulierung derselben acht Kategorien",
           _kurzform_umformulieren, "nennt die Kategorie")


# --- 30: Vollstaendigkeit der Grenzfalltabelle (B07, B09) -----------------------
# Die Tabelle ist das Abnahmekriterium des Reviews. Drei Wege, sie unbemerkt zu
# entwerten: eine Zeile verschwindet, eine Spalte bleibt leer, eine Entscheidung ist
# durch keinen Grenzfall gedeckt.
EDGE_30 = ".koolie/core/tests/EDGE_CASES.md"
KATALOG_30 = ".koolie/core/tests/TEST_CATALOG.md"


def _grenzfall_loeschen(root: str) -> None:
    pfad = _p(root, EDGE_30)
    zeilen = lies(pfad).split("\r\n")
    behalten = [z for z in zeilen if not z.startswith("| G-07 |")]
    schreib(pfad, "\r\n".join(behalten))


def _spalte_leeren(root: str) -> None:
    pfad = _p(root, EDGE_30)
    text = lies(pfad)
    start = text.index("| G-05 |")
    ende = text.index("\r\n", start)
    zeile = text[start:ende]
    zellen = zeile.split(" | ")
    zellen[4] = ""
    schreib(pfad, text[:start] + " | ".join(zellen) + text[ende:])


def _entscheidung_entkoppeln(root: str) -> None:
    pfad = _p(root, EDGE_30)
    schreib(pfad, lies(pfad).replace("(D-53)", "(siehe Antrag)"))


def _grenzfall_ergaenzen(root: str) -> None:
    """Gegenprobe: eine weitere Zeile samt mitgezaehlter Anzahl.

    ZWEIMAL an einem neuen Grenzfall gebrochen, zuletzt mit 0.36.0 an G-18: Die
    Anzahl war woertlich verankert (17 -> 18), und die synthetische Kennung war
    G-18 - dieselbe, die dieses Release wirklich vergeben hat. Beide Fallen sind
    in der Uebergabe benannt gewesen, und beide sind trotzdem zugeschnappt.

    Die Kennung ist seither G-99 und kollidiert mit keinem echten Fall. Die Anzahl
    bleibt woertlich: Ob eine Gegenprobe ihre Summen ABLEITEN soll, ist eine
    Ermessensfrage und nicht entschieden - eine abgeleitete Summe verdoppelt
    womoeglich nur die Rechenweise der Pruefung, statt sie zu belegen. Die Frage
    ist damit zum VIERTEN Mal aufgetreten und gehoert in einen eigenen Antrag.

    Seit 0.42.0 zieht diese Gegenprobe ZWEI Register nach: die Anzahl im Steckbrief
    von EDGE_CASES.md und die Arbeitsanweisung in FW-KO-05. Ein Repositorium mit 21
    Grenzfaellen, dessen Testblatt weiter von zwanzig spricht, ist kein erlaubter
    Fall, sondern genau der Befund, gegen den Pruefung 40 gebaut ist (D-86). Der
    Sondenlauf zu 0.42.0 hat ihn gemeldet, bevor jemand ihn behaupten musste.
    """
    pfad = _p(root, EDGE_30)
    frei(pfad, "G-99")
    ersetze(pfad, ("| Anzahl der Grenzf\u00e4lle | 20 |",
                   "| Anzahl der Grenzf\u00e4lle | 21 |"))
    zeile_nach(
        pfad, "| G-20 |",
        "| G-99 | Synthetischer Zusatzfall der Gegenprobe | **zul\u00e4ssig** | M1 | "
        "niedrig | keine | `.koolie/core/tests/EDGE_CASES.md` Abschnitt 1 (D-52) |")
    ersetze(_p(root, KATALOG_30),
            ("Die 20 Grenzfälle einzeln", "Die 21 Grenzfälle einzeln"))


sonde("30a", "Geloeschte Grenzfallzeile gegen die Anzahl im Steckbrief",
      _grenzfall_loeschen, "Grenzfallzeilen, der Steckbrief nennt")

sonde("30b", "Leere Spalte in einem Grenzfall",
      _spalte_leeren, "ist leer")

sonde("30c", "Eine Entscheidung des Logs, die kein Grenzfall mehr deckt, wird gemeldet",
      _entscheidung_entkoppeln, "Keine Grenzfallzeile verweist auf D-53")

gegenprobe("30", "Zusaetzlicher Grenzfall mit mitgezaehlter Anzahl",
           _grenzfall_ergaenzen, "Grenzfallzeilen")



# --- Kandidatenpruefung, Status-Hook und Fetch-Allow (B08, B11) -------------------
#
# Je Pack eine eigene Installation, wie bei der Aktivierungspruefung: B02 war nicht, dass
# eine Pruefung falsch prueft, sondern dass sie einen Client gar nicht sieht. Das faellt
# nur auf, wenn derselbe Fall in jeder Installation laeuft.
#
# Die Gegenproben sind hier die wichtigere Haelfte. Bei der Kandidatenpruefung belegt sie,
# dass ein vollstaendiger, noch nicht aktiver Kandidat **durchlaeuft** - ohne sie stuende
# nur fest, dass irgendetwas gemeldet wird, und eine Pruefung, die alles meldet, besteht
# jede Sonde.


def ready_ausgabe(root: str) -> str:
    """Ausgabe der Kandidatenpruefung (--check-overlay-ready)."""
    p = unterprozess([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                      "--root", root, "--check-overlay-ready"])
    return (p.stdout or "") + (p.stderr or "")


def hook_ausgabe(root: str, regelablage: str) -> str:
    """Ausgabe des Status-Hooks - er blockiert nie, er informiert."""
    p = unterprozess([sys.executable,
                      os.path.join(root, ".koolie/core", "tests", "scripts",
                                   "hook-overlay-status.py"),
                      root, regelablage])
    return (p.stdout or "") + (p.stderr or "")


def _kandidat_herstellen(regel: str, overlay: str, rechte: str) -> None:
    """Ein vollstaendig ausgefuellter Kandidat: keine offenen Werte, Status 'inaktiv'."""
    for pfad in (regel, overlay, rechte):
        schreib(pfad, SO_PLATZHALTER.sub("gesetzt", lies(pfad)))
    for pfad in (regel, overlay):
        _so_status(pfad, "inaktiv")


def sonden_kandidatenpruefung() -> None:
    """Wirkungsnachweis der Kandidatenpruefung und des Status-Hooks (B08, D-57, D-58)."""
    for pack in ("claude-code", "devin-desktop"):
        root = installation(pack)
        try:
            man = json.loads(lies(os.path.join(QUELLE, ".koolie/core", "clients", pack,
                                               "manifest.json")))
            regelablage = man["pack_runtime_dir"]
            regel = os.path.join(root, *regelablage.split("/"), "20-project-overlay.md")
            overlay = os.path.join(root, ".koolie/project-overlay", "OVERLAY.md")
            rechte = os.path.join(root, *man["permissions_file"].split("/"))

            # --- Gegenprobe: der vollstaendige, noch nicht aktive Kandidat laeuft durch
            _kandidat_herstellen(regel, overlay, rechte)
            aus = ready_ausgabe(root)
            ok = "check-overlay-ready" not in aus and "(check-overlay-ready)" not in aus
            melde("GEGENPROBE", "CR", ok,
                  f"Vollstaendiger Kandidat mit Status 'inaktiv' laeuft durch ({pack})")
            if not ok:
                notiz("        Ausgabe:", " | ".join(
                    z for z in aus.splitlines() if "check-overlay-ready" in z)[:400])

            # --- Sonde: ein bereits aktiver Kandidat ist keiner
            for pfad in (regel, overlay):
                _so_status(pfad, "aktiv")
            aus = ready_ausgabe(root)
            melde("SONDE", "CR", "ist bereits 'aktiv'" in aus,
                  f"Bereits aktives Overlay wird von der Kandidatenpruefung gemeldet ({pack})")

            # --- Sonde: Drift zwischen den beiden Traegern
            _so_status(overlay, "inaktiv")
            aus = ready_ausgabe(root)
            melde("SONDE", "CR", "widersprechen sich" in aus,
                  f"Abweichende Statusangaben werden gemeldet ({pack})")

            # --- Sonde: der Status ist ueberhaupt nicht ausgefuellt
            for pfad in (regel, overlay):
                _so_status(pfad, "<TBD: aktiv | inaktiv>")
            aus = ready_ausgabe(root)
            melde("SONDE", "CR", "nicht ausgefuellt" in aus,
                  f"Offener Statuswert wird gemeldet ({pack})")

            # --- Status-Hook: dieselben drei Faelle, dasselbe Ergebnis ---------------
            # Der Hook hatte bis 0.32.0 drei Defekte, und jeder einzelne haette die
            # Meldung 'aktiv' erzeugt, wo sie falsch ist.
            for pfad in (regel, overlay):
                _so_status(pfad, "aktiv")
            aus = hook_ausgabe(root, regelablage)
            melde("GEGENPROBE", "HS", "Overlay-Status: aktiv" in aus and "Modus M1" not in aus,
                  f"Hook meldet 'aktiv' ohne M1-Hinweis, wenn alle Angaben aktiv sind ({pack})")

            _so_status(regel, "aktivierung-ausstehend")
            aus = hook_ausgabe(root, regelablage)
            melde("SONDE", "HS", "Overlay-Status: widerspruechlich" in aus,
                  f"'aktivierung-ausstehend' gilt dem Hook nicht als aktiv ({pack})")

            _so_status(regel, "inaktiv")
            aus = hook_ausgabe(root, regelablage)
            melde("SONDE", "HS", "Overlay-Status: widerspruechlich" in aus,
                  f"Hook meldet die Drift statt der ersten gelesenen Datei ({pack})")

            # Nur die Steckbriefzeile, kein Listeneintrag: Das Suchmuster des Hooks
            # verlangte bis 0.32.0 einen Doppelpunkt und traf die Tabelle nie.
            for pfad in (regel, overlay):
                _so_status(pfad, "inaktiv")
            t = lies(overlay)
            schreib(overlay, re.sub(r"^-\s*Overlay-Status:.*$", "", t, flags=re.M))
            os.remove(regel)
            aus = hook_ausgabe(root, regelablage)
            melde("SONDE", "HS", "Overlay-Status: inaktiv" in aus,
                  f"Hook liest den Status auch aus der Steckbriefzeile ({pack})")

            # --- Fetch-Allow: aus dem Manifest, nicht aus einer Namensliste ---------
            # Bis 0.32.0 standen die Werkzeugnamen fest verdrahtet, und das war
            # asymmetrisch: 'Fetch(domain:...)' lief durch, 'WebFetch(domain:...)' fiel.
            werkzeug = man["permission_tools"]["fetch"][0]
            inhalt = lies(rechte)
            schreib(rechte, ersetzt(
                inhalt,
                ('"allow": [', '"allow": [\r\n      "%s(domain:docs.example.invalid)",'
                 % werkzeug),
                quelle=os.path.basename(rechte)))
            p = unterprozess([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                              "--root", root])
            aus = (p.stdout or "") + (p.stderr or "")
            melde("SONDE", "FA", "allow-Regel auf ein Abrufwerkzeug" in aus,
                  f"Domain-Allow auf das Abrufwerkzeug wird gemeldet ({pack}: {werkzeug})")

            schreib(rechte, inhalt)
            p = unterprozess([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                              "--root", root])
            aus = (p.stdout or "") + (p.stderr or "")
            melde("GEGENPROBE", "FA", "allow-Regel auf ein Abrufwerkzeug" not in aus,
                  f"Die ausgelieferte Regelmenge bleibt unbeanstandet ({pack})")
        finally:
            aufraeumen(os.path.dirname(root))


buendel(sonden_kandidatenpruefung,
        "Kandidatenpruefung, Status-Hook und Freigabenpruefung gegen je eine Installation "
        "beider Packs - widerspruechlicher Status, offene Platzhalter, allow auf ein "
        "Abrufwerkzeug")


# --- 31: Die Summen der Fachmatrix sind ausgerechnet (D-60) ----------------------
# Dreimal von Hand berichtigt, dreimal wieder gedriftet - deshalb ausgerechnet. Die
# Gegenprobe ist die wichtigere: Eine zusaetzliche Matrixzeile samt nachgezogener Summe
# darf nicht auffallen, sonst waere die Pruefung eine Bremse statt einer Pruefung.
PACK_31 = ".koolie/core/clients/claude-code/CLIENT_PACK.md"
UEBERSICHT_31 = ".koolie/core/clients/README.md"


def _summe_verfaelschen(root: str) -> None:
    pfad = P(root, PACK_31.replace("/", os.sep))
    schreib(pfad, lies(pfad).replace("| `[TECHNISCH]` | 22 von 32 |",
                                     "| `[TECHNISCH]` | 23 von 32 |", 1))


def _gesamtzahl_verfaelschen(root: str) -> None:
    pfad = P(root, PACK_31.replace("/", os.sep))
    schreib(pfad, lies(pfad).replace("| 22 von 32 |", "| 22 von 33 |", 1))


def _zusammenfassung_entfernen(root: str) -> None:
    pfad = P(root, PACK_31.replace("/", os.sep))
    schreib(pfad, lies(pfad).replace("## 3. Zusammenfassung",
                                     "## 3. Uebersicht", 1))


def _zeile_ohne_einstufung(root: str) -> None:
    pfad = P(root, PACK_31.replace("/", os.sep))
    t = lies(pfad)
    marke = "| X2 |"
    i = t.index(marke)
    ende = t.index("\r\n", i)
    schreib(pfad, t[:ende] + "\r\n| Z9 | Sonde ohne Einstufung | - | - | - |" + t[ende:])


def _zeile_mit_summe(root: str) -> None:
    """Gegenprobe: eine zusaetzliche Zeile samt nachgezogenen Summen."""
    pfad = P(root, PACK_31.replace("/", os.sep))
    frei(pfad, "| Z9 |")
    zeile_nach(pfad, "| X2 |",
               "| Z9 | Sonde mit Einstufung | - | `[TECHNISCH]` | `[DOK]` |")
    ersetze(pfad,
            ("| `[TECHNISCH]` | 22 von 32 |", "| `[TECHNISCH]` | 23 von 33 |"),
            ("| 8 von 32 (", "| 8 von 33 ("),
            ("| **2 von 32** (", "| **2 von 33** ("),
            ("| 0 von 32 |", "| 0 von 33 |"))
    # Seit 0.36.0 rechnet Pruefung 31 dieselbe Zahl auch in der Uebersicht der Ablage nach
    # (D-71). Eine Gegenprobe, die nur das Pack nachzieht, faellt seither an der zweiten
    # Stelle - und genau das ist der Zweck der Erweiterung.
    u = P(root, UEBERSICHT_31.replace("/", os.sep))
    # 0.89.0: Der Statuswert dieser Zeile stand hier woertlich und ist mit CR-2026-124
    # von "entwurf" auf "pilot" berichtigt worden - das Pack selbst sagte schon "pilot".
    ersetze(u, ("| pilot | 22 von 32 |", "| pilot | 23 von 33 |"))


sonde("31a", "Verfaelschte Anzahl je Einstufung in der Zusammenfassung",
      _summe_verfaelschen, "Zeile(n) als [TECHNISCH]; gezaehlt sind")

sonde("31b", "Eine verfaelschte Gesamtzahl der Matrixzeilen wird gegen die gezaehlte Zahl gemeldet",
      _gesamtzahl_verfaelschen, "Matrixzeilen; gezaehlt sind")

sonde("31c", "Fehlende Zusammenfassung - die Pruefung darf nicht leise bestehen",
      _zusammenfassung_entfernen, "kein Abschnitt '## 3. Zusammenfassung")

sonde("31d", "Eine Matrixzeile ohne Einstufung faellt aus jeder Summe und wird gemeldet",
      _zeile_ohne_einstufung, "ohne Einstufung: Z9")

def _uebersicht_verfaelschen(root: str) -> None:
    pfad = P(root, UEBERSICHT_31.replace("/", os.sep))
    schreib(pfad, lies(pfad).replace("| pilot | 22 von 32 |",
                                     "| pilot | 25 von 29 |", 1))


def _uebersichtszeile_entfernen(root: str) -> None:
    pfad = P(root, UEBERSICHT_31.replace("/", os.sep))
    t = lies(pfad)
    i = t.index("| `claude-code` | `CP-CC` |")
    ende = t.index("\r\n", i) + 2
    schreib(pfad, t[:i] + t[ende:])


sonde("31e", "Ueberholte Zahl in der Uebersicht der Ablage - der Stand bis 0.35.0",
      _uebersicht_verfaelschen, "technisch durchgesetzte Zeilen; aus der Faehigkeitsmatrix")

sonde("31f", "Pack ohne Zeile in der Uebersicht", _uebersichtszeile_entfernen,
      "kein Eintrag fuer das Client Pack 'claude-code'")

gegenprobe("31", "Zusaetzliche Matrixzeile samt nachgezogener Summe an BEIDEN Stellen",
           _zeile_mit_summe, "gezaehlt sind")



# --- 32: Eingabeschema und Pfadidentitaet des Schutz-Hooks (B06, CR-2026-056) -----
#
# Sechs Sonden, weil der Hook seit 0.34.0 sechs voneinander unabhaengige Mechanismen
# traegt. Jede bricht genau EINEN, und keine bricht ihn ueber den naheliegenden Fall:
# Bei .KOOLIE/CORE/VERSION decken die Aufloesung und re.I einander gegenseitig zu -
# faellt einer von beiden aus, bestuende die Pruefung, und die Sonde zeigte nichts.
# 32a und 32e treffen deshalb je einen Fall, den nur ein Mechanismus faengt.
HOOK_32 = ".koolie/core/tests/scripts/hook-check-secrets.py"


def _hook32(root: str) -> str:
    return P(root, HOOK_32.replace("/", os.sep))


def _tausche(root: str, alt: str, neu: str) -> None:
    """Eine Ersetzung im Hook der Kopie. Trifft der Suchtext nicht, bleibt der Baum
    unveraendert - und sonde() meldet genau das, statt die Pruefung zu messen."""
    pfad = _hook32(root)
    schreib(pfad, lies(pfad).replace(alt, neu, 1))


def _ohne_aufloesung(root: str) -> None:
    """Die Pfadaufloesung liefert nichts - die Muster sehen nur noch den Rohtext."""
    _tausche(root, "    voll, nur_secret = [], []", "    return [], []")


def _ohne_ereignispruefung(root: str) -> None:
    """Eine leere Eingabe gilt wieder als harmloses Ereignis - der Stand bis 0.33.0."""
    _tausche(root, '        raise Unpruefbar("leere Eingabe")',
             '        raw = \'{"tool_name": "x", "tool_input": {}}\'')


def _umschlag_im_pruefmaterial(root: str) -> None:
    """Der Umschlag wandert zurueck ins Pruefmaterial - der Stand bis 0.33.0."""
    _tausche(root, "    return tool_name.strip().lower(), tool_input, basis",
             "    return tool_name.strip().lower(), dict(payload, **tool_input), basis")
    # Seit 1.17.0 misst ein Schreibwerkzeug nur seine Ziele (D-449). Der alte Stand
    # hielt ALLE Zeichenketten gegen die Muster - erst beides zusammen stellt ihn her.
    _tausche(root, "        zu_pruefen = list(ziele)",
             "        zu_pruefen = list(ziele) + list(strings)")


def _unbekanntes_werkzeug_lax(root: str) -> None:
    """Eine unbekannte Operation gilt wieder als lesend statt als die strengste."""
    _tausche(root, '    schreibend = verb in ("write", "unbekannt")',
             '    schreibend = verb == "write"')


def _ohne_schreibweise(root: str) -> None:
    """Das Secret-Muster fuer .env wird wieder schreibungssensitiv."""
    _tausche(root, r'\.env(\.|$)", re.I', r'\.env(\.|$)"')


def _anker_verlieren(root: str) -> None:
    """Der Suchtext, ueber den Pruefung 32 ihren Gegenstand findet, geht verloren."""
    pfad = _hook32(root)
    schreib(pfad, lies(pfad).replace("ereignis_lesen(", "ereignis_pruefen("))


def _zusaetzliches_pfadfeld(root: str) -> None:
    """Gegenprobe: ein weiteres Pfadfeld im Manifest - eine zulaessige Verschaerfung."""
    for pack in ("claude-code", "devin-desktop"):
        pfad = P(root, (".koolie/core/clients/%s/manifest.json" % pack).replace("/", os.sep))
        ersetze(pfad, ('"hook_path_fields": ["file_path"',
                       '"hook_path_fields": ["zielpfad", "file_path"'))


sonde("32a", "Pfadaufloesung aus - nur sie faengt einen Pfad, der den Kern nicht nennt",
      _ohne_aufloesung, "ohne es zu nennen")

sonde("32b", "Ereignispruefung aus - eine leere Eingabe gilt wieder als Ereignis",
      _ohne_ereignispruefung, "ist kein Werkzeugereignis")

sonde("32c", "Umschlag zurueck im Pruefmaterial - der Stand bis 0.33.0",
      _umschlag_im_pruefmaterial, "je nachdem ob der Umschlag")

sonde("32d", "Unbekannte Operation gilt wieder als lesend",
      _unbekanntes_werkzeug_lax, "unbekanntes Werkzeug in das Kernverzeichnis")

sonde("32e", "Secret-Muster wieder schreibungssensitiv - nur re.I faengt die nicht "
      "vorhandene Datei", _ohne_schreibweise, "wenn die Datei nicht existiert")

sonde("32f", "Verlorener Anker - die Pruefung darf nicht leise bestehen",
      _anker_verlieren, "'def ereignis_lesen(' fehlt")

def _unteragent_ausnehmen(root: str) -> None:
    """Ein Rueckfall, den nur der Unteragenten-Umschlag faengt (CR-2026-058 E3).

    Simuliert die naheliegende Regression: Jemand nimmt Aufrufe aus einem Unteragenten
    von der Pruefung aus - etwa weil sie "schon oben geprueft" seien. Keine der uebrigen
    sechs Sonden zu 32 sieht das: Ohne agent_type im Umschlag greift die Ausnahme nicht,
    und der Hook verhaelt sich in jedem anderen Fall unveraendert.
    """
    pfad = P(root, ".koolie/core/tests/scripts/hook-check-secrets.py".replace("/", os.sep))
    t = lies(pfad)
    marke = "    tool_name = payload.get(\"tool_name\")"
    i = t.index(marke)
    schreib(pfad, t[:i] + "    if payload.get(\"agent_type\"):\r\n"
            "        return \"read\", {}, PROJEKTWURZEL\r\n" + t[i:])


sonde("32g", "Unteragenten-Umschlag von der Pruefung ausgenommen - ein Rueckfall, den "
      "keine der uebrigen Sonden sieht",
      _unteragent_ausnehmen, "Operation aus einem Unteragenten anders als erwartet")

gegenprobe("32", "Zusaetzliches Pfadfeld im Manifest ist eine zulaessige Verschaerfung",
           _zusaetzliches_pfadfeld, "Befund B06")


# --- 33: Die Abbildung von permissions.deny auf die Werkzeugsperre (CR-2026-057) -----
#
# GEGEN EINE ECHTE INSTALLATION, und das ist hier nicht Zierrat: Pruefung 33 laeuft nur
# fuer ein Pack, dessen Manifest skill_deny_field fuehrt. Die Testinstallation im
# Repositorium ist 'devin-desktop' und fuehrt es nicht - die Pruefung wird im Repo-Lauf
# also GAR NICHT ausgefuehrt. Genau das war Befund B02: nicht, dass eine Pruefung falsch
# prueft, sondern dass sie einen Client nicht sieht.
#
# Fuenf Sonden und eine Gegenprobe. Jede Sonde bricht genau einen Mechanismus.
def _p33(root: str, name: str) -> str:
    return os.path.join(root, ".claude", "skills", name, "SKILL.md")


def sonden_skill_deny() -> None:
    """Wirkungsnachweis der Abbildung und ihrer Grenzen (D-64 bis D-66)."""
    root = installation("claude-code")
    try:
        plan = _p33(root, "fw-plan")
        ausgang = lies(plan)

        # --- Gegenprobe: die unveraenderte Installation laeuft durch ----------------
        # Sie ist hier die wichtigere Haelfte. Ohne sie stuende nur fest, dass Pruefung 33
        # irgendetwas meldet - und eine Pruefung, die jede Installation beanstandet,
        # bestuende jede Sonde.
        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "33", "disallowed-tools" not in aus,
              "Die unveraenderte claude-code-Installation bleibt unbeanstandet")
        if "disallowed-tools" in aus:
            notiz("        Ausgabe:", " | ".join(
                z for z in aus.splitlines() if "disallowed-tools" in z)[:400])

        # --- 33a: die Sperre fehlt ganz - der Stand bis 0.34.0 ----------------------
        schreib(plan, ersetzt(
            ausgang,
            ("disallowed-tools: Edit, Write, NotebookEdit, Bash, PowerShell\n", ""),
            quelle="fw-plan/SKILL.md"))
        aus = validator_ausgabe(root)
        melde("SONDE", "33a", "aus permissions.deny der Quelle ergibt sich" in aus,
              "Fehlende Werkzeugsperre - der Stand, den B01 beschrieb")

        # --- 33b: die Sperre ist unvollstaendig - eine Luecke ist ausnutzbar --------
        schreib(plan, ersetzt(
            ausgang,
            ("disallowed-tools: Edit, Write, NotebookEdit, Bash, PowerShell",
             "disallowed-tools: Edit, Write"),
            quelle="fw-plan/SKILL.md"))
        aus = validator_ausgabe(root)
        melde("SONDE", "33b", "aus permissions.deny der Quelle ergibt sich" in aus,
              "Unvollstaendige Sperre - mit gesperrtem Write, Edit schrieb der Skill ueber Bash")

        # --- 33c: ein Argumentmuster - gemessen wirkungslos, und zwar lautlos -------
        schreib(plan, ersetzt(
            ausgang,
            ("disallowed-tools: Edit, Write, NotebookEdit, Bash, PowerShell",
             "disallowed-tools: Edit, Write, NotebookEdit, Bash(git push:*), PowerShell"),
            quelle="fw-plan/SKILL.md"))
        aus = validator_ausgabe(root)
        melde("SONDE", "33c", "Argumentmuster" in aus,
              "Argumentmuster in der Sperre - es sieht aus wie eine Regel und ist keine")

        # --- 33d: ein Werkzeug in beiden Listen - zwei Aussagen, eine davon falsch --
        schreib(plan, ersetzt(
            ausgang,
            ("allowed-tools: Read, Grep, Glob",
             "allowed-tools: Read, Grep, Glob, Bash"),
            quelle="fw-plan/SKILL.md"))
        aus = validator_ausgabe(root)
        melde("SONDE", "33d", "steht zugleich in allowed-tools" in aus,
              "Werkzeug zugleich vorabfreigegeben und gesperrt")
        schreib(plan, ausgang)

        # --- 33e: der verlorene Anker - die Pruefung darf nicht leise bestehen ------
        inst = os.path.join(root, ".koolie/core", "install.py")
        quelle = lies(inst)
        schreib(inst, ersetzt(quelle,
                              ("def deny_abbilden(", "def deny_uebersetzen("),
                              quelle="install.py"))
        aus = validator_ausgabe(root)
        melde("SONDE", "33e", "'def deny_abbilden(' fehlt" in aus,
              "Verlorener Anker - die Pruefung meldet ihr Fehlen selbst")
        schreib(inst, quelle)
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_skill_deny,
        "Die Abbildung von permissions.deny in das Frontmatter eines Skills und ihre "
        "Grenzen - Argumentmuster, Doppelnennung in allowed-tools, verlorener Anker")



# --- 34: Das Startwerkzeug fuer Unteragenten ist genannt oder erklaert (D-70) -----
#
# Anlass ist ein gemessener Befund vom 2026-09-13: Ein Skill kann einen Unteragenten
# starten, die Skill-Sperre reicht in ihn hinein - und das Startwerkzeug stand in keiner
# Werkzeugliste eines Manifests. Bauform der Deklaration wie hook_tools_absent (D-47).
#
# Die letzte Sonde ist die interessanteste: Sie belegt die Verschaerfung, die diese
# Pruefung bei ihrem ERSTEN Lauf selbst gelernt hat. Ohne den Vorbehalt fiel
# devin-desktop durch, obwohl es ehrlich ist - seine Zeile A1 trug einen offenen
# Beleg, und die Praeambel des Packs sagt, die Einstufung nenne die VORGESEHENE
# Tiefe. Die Einstufung allein sagt nicht, ob eine Zusage schon gilt.
#
# MIT 0.87.0 STEHT DER VORBEHALT AUF DER NACHFOLGEFORM BELEG OFFEN (D-291); die
# Markerform ist abgeschafft. Die Sonde trifft davon nichts: Sie nimmt seit 0.86.0 das
# Startwerkzeug weg und nicht den Vorbehalt.
MANIFEST_CC_34 = ".koolie/core/clients/claude-code/manifest.json"
MANIFEST_DD_34 = ".koolie/core/clients/devin-desktop/manifest.json"
PACK_DD_34 = ".koolie/core/clients/devin-desktop/CLIENT_PACK.md"


def _34_feld_entfernen(root: str) -> None:
    pfad = P(root, MANIFEST_CC_34.replace("/", os.sep))
    t = lies(pfad)
    i = t.index('  "agent_start_tools": ["Agent", "Task"],')
    ende = t.index("\r\n", i) + 2
    schreib(pfad, t[:i] + t[ende:])


def _34_leer_ohne_erklaerung(root: str) -> None:
    pfad = P(root, MANIFEST_CC_34.replace("/", os.sep))
    schreib(pfad, lies(pfad).replace('"agent_start_tools": ["Agent", "Task"],',
                                     '"agent_start_tools": [],', 1))


def _34_erklaerung_ohne_notiz(root: str) -> None:
    """Die Sonde BRINGT die Abwesenheitserklaerung mit, statt sie vorauszusetzen.

    Bis 0.85.2 stand sie im Bestand (`agent_start_tools_absent: ["unerhoben"]`); mit
    0.86.0 ist sie aufgeloest - das Startwerkzeug heisst `run_subagent` (D-284). Eine
    Sonde, die auf den Bestand zeigt, verliert damit ihren Gegenstand und bestuende
    leise (D-23). Sie setzt ihn seither selbst.
    """
    pfad = P(root, MANIFEST_DD_34.replace("/", os.sep))
    t = lies(pfad)
    t = t.replace('"agent_start_tools": ["run_subagent"],',
                  '"agent_start_tools": [],', 1)
    t = t.replace('"agent_start_tools_absent": [],',
                  '"agent_start_tools_absent": ["unerhoben"],', 1)
    t = t.replace('"_agent_start_tools_absent_note"',
                  '"_agent_start_tools_absent_hinweis"', 1)
    schreib(pfad, t)


def _34_beides_zugleich(root: str) -> None:
    pfad = P(root, MANIFEST_CC_34.replace("/", os.sep))
    schreib(pfad, lies(pfad).replace(
        '"agent_start_tools": ["Agent", "Task"],',
        '"agent_start_tools": ["Agent", "Task"],\r\n'
        '  "agent_start_tools_absent": ["unerhoben"],\r\n'
        '  "_agent_start_tools_absent_note": "Sonde.",', 1))


def _34_a1_ohne_vorbehalt(root: str) -> None:
    """devin-desktop sagt A1 ohne VERIFY-Marker zu, kann das Werkzeug aber nicht nennen."""
    # BIS 0.85.2 nahm diese Sonde der Zeile A1 ihren VERIFY-Marker. Den gibt es nicht
    # mehr: Die Profilwirkung ist am 2026-09-22 gemessen (D-284), und die Zeile sagt A1
    # seither OHNE Vorbehalt zu. Damit ist der Vorbehalt kein Praeparationsort mehr -
    # die Sonde nimmt stattdessen das Startwerkzeug weg, das die Zusage traegt. Der
    # gemessene Fall ist derselbe, und er ist in diesem Release LIVE eingetreten:
    # Pruefung 34 hat ihn gemeldet, sobald A1 seinen Marker verlor und das Manifest noch
    # ein leeres Feld fuehrte.
    pfad = P(root, MANIFEST_DD_34.replace("/", os.sep))
    t = lies(pfad)
    t = t.replace('"agent_start_tools": ["run_subagent"],',
                  '"agent_start_tools": [],', 1)
    t = t.replace('"agent_start_tools_absent": [],',
                  '"agent_start_tools_absent": ["unerhoben"],', 1)
    schreib(pfad, t)


sonde("34a", "Manifest ohne Feld agent_start_tools - ein Kanal ohne Deklaration",
      _34_feld_entfernen, "Feld 'agent_start_tools' fehlt")

sonde("34b", "Leere Liste ohne erklaerte Abwesenheit - unerhoben oder abwesend?",
      _34_leer_ohne_erklaerung, "ohne dass 'agent_start_tools_absent' die Abwesenheit")

sonde("34c", "Erklaerte Abwesenheit ohne Begruendung - eine Behauptung",
      _34_erklaerung_ohne_notiz, "'_agent_start_tools_absent_note' fehlt")

sonde("34d", "Genannt und zugleich fuer abwesend erklaert - zwei Aussagen, eine falsch",
      _34_beides_zugleich, "Beides zugleich geht nicht")

sonde("34e", "Zeile A1 ohne Vorbehalt zugesagt, Startwerkzeug aber nur erklaert",
      _34_a1_ohne_vorbehalt, "Wer Unteragenten zusagt, nennt das Werkzeug")

gegenprobe("34", "Die unveraenderten Packs bleiben unbeanstandet - eines nennt, eines "
           "erklaert mit offenem Vorbehalt", None, "agent_start_tools")


# --- 35: Ein Agentenprofil bekommt kein Startwerkzeug (D-73) ---------------------
#
# Diese Pruefung faengt heute nichts: agent_frontmatter.tool_names kennt gar kein
# Startwerkzeug. Sie ist eine Verankerung - und genau deshalb braucht sie ihre Sonden
# dringender als andere. Ohne sie liesse sich nicht zeigen, DASS sie etwas faengt,
# sobald es den Fall gibt. Gemessen ist der Befund dahinter am 2026-09-13, Lauf
# STARTLOS: Ein Profil mit tools: Read, Grep, Glob kann keine zweite Ebene oeffnen.
MANIFEST_CC_35 = ".koolie/core/clients/claude-code/manifest.json"
PROFIL_35 = ".koolie/core/framework/runtime/agents/fw-reviewer.md"


def _35_abbildung_erweitern(root: str) -> None:
    """Der Fall, der die Zusage lautlos fallen liesse: tool_names lernt es.

    Praepariert wird ueber das JSON, nicht ueber den Text: skill_frontmatter und
    agent_frontmatter fuehren ZEICHENGLEICHE tool_names-Bloecke, und ein Textanker
    traefe den falschen. Pruefung 35 liest nur den zweiten."""
    pfad = P(root, MANIFEST_CC_35.replace(chr(47), os.sep))
    daten = json.loads(lies(pfad))
    daten['agent_frontmatter']['tool_names']['delegate'] = ['Agent']
    schreib(pfad, json.dumps(daten, ensure_ascii=False, indent=2))


def _35_profil_erweitern(root: str) -> None:
    """Der Fall an der Abbildung vorbei: das Profil nennt es selbst."""
    pfad = P(root, PROFIL_35.replace("/", os.sep))
    schreib(pfad, lies(pfad).replace("  - glob", "  - glob\r\n  - agent", 1))


def _35_ablage_entfernen(root: str) -> None:
    """Die Sonde auf den verlorenen Anker: ohne Ablage darf sie nicht leise bestehen."""
    shutil.rmtree(P(root, ".koolie/core/framework/runtime/agents".replace("/", os.sep)))


sonde("35a", "Die Abbildung lernt ein Startwerkzeug - der Fall, der die Zusage "
      "lautlos fallen liesse",
      _35_abbildung_erweitern, "ein Werkzeug, mit dem ein Unteragent GESTARTET")

sonde("35b", "Das Agentenprofil nennt ein Startwerkzeug selbst - an der Abbildung "
      "vorbei",
      _35_profil_erweitern, "Das Frontmatter nennt 'agent'")

sonde("35c", "Verlorener Anker - die Agentenablage fehlt",
      _35_ablage_entfernen, "Pruefung 35 misst die Agentenprofile des Kerns")

gegenprobe("35", "Die unveraenderte Ablage bleibt unbeanstandet", None,
           "GESTARTET wird")

# --- 36: Die Tabellen des Decision Logs sind nicht zerrissen (D-75) --------------
#
# Anlass: vier zerrissene Zeilen in 0.34.0, eine davon seit 0.10.x. Gefunden hat sie
# jedes Mal ein Mensch beim Eintragen einer anderen.
#
# Die Gegenprobe ist hier die wichtigere Haelfte, und zwar aus einem gemessenen Grund:
# Eine naive Zaehlung mit .split("|") meldet D-29 und D-69 als achtspaltig, obwohl beide
# ihren Strich korrekt maskieren und sechsspaltig rendern. Ohne diese Gegenprobe waere
# Pruefung 36 mit zwei Fehlalarmen auf richtigem Text entstanden - und Pruefung 30 haette
# ihren eigenen, latenten Fehlalarm behalten (CR-2026-060 1.3).
DECISION_LOG_36 = ".koolie/core/governance/DECISION_LOG.md"


def _dl36(root: str) -> str:
    return P(root, DECISION_LOG_36.replace("/", os.sep))


def _36_zelle_entfernen(root: str) -> None:
    """Eine Zeile verliert ihre letzte Zelle - der Fall D-61 bis D-63 aus 0.34.0."""
    pfad = _dl36(root)
    zeilen = lies(pfad).split("\r\n")
    treffer = [i for i, z in enumerate(zeilen) if z.startswith("| D-40 |")]
    if len(treffer) != 1:
        raise Praeparationsfehler(
            "DECISION_LOG.md: Anker '| D-40 |' steht %dx, erwartet genau einmal"
            % len(treffer))
    z = zeilen[treffer[0]].rstrip().rstrip("|").rstrip()
    zeilen[treffer[0]] = z[:z.rindex("|")] + "|"
    schreib(pfad, "\r\n".join(zeilen))


def _36_strich_unmaskiert(root: str) -> None:
    """Ein unmaskierter Strich in einem Codespan - der Fall D-29 aus 0.10.x."""
    ersetze(_dl36(root),
            ("| D-40 | **Ein Befund \u00fcber einen Client ist keine Aussage "
             "\u00fcber alle.**",
             "| D-40 | **Ein Befund \u00fcber einen Client ist keine Aussage "
             "\u00fcber alle.** Matcher `a|b`."))


def _36_anker_verlieren(root: str) -> None:
    """Keine Tabellenzeile mehr - die Pruefung darf nicht leise bestehen."""
    pfad = _dl36(root)
    zeilen = [z for z in lies(pfad).split("\r\n") if not z.startswith("|")]
    schreib(pfad, "\r\n".join(zeilen))


def _36_strich_maskiert(root: str) -> None:
    """Gegenprobe: derselbe Strich, korrekt maskiert - so, wie D-69 ihn seit 0.36.0
    traegt. Eine Zaehlung ohne diese Unterscheidung beanstandet den richtigen Text."""
    ersetze(_dl36(root),
            ("| D-40 | **Ein Befund \u00fcber einen Client ist keine Aussage "
             "\u00fcber alle.**",
             "| D-40 | **Ein Befund \u00fcber einen Client ist keine Aussage "
             "\u00fcber alle.** Matcher `a\\|b`."))


sonde("36a", "Zeile mit fehlender Zelle - der Fall D-61 bis D-63 aus 0.34.0",
      _36_zelle_entfernen, "Zellen, der Kopf ihrer Tabelle")

sonde("36b", "Unmaskierter Strich in einer Zelle - der Fall D-29 seit 0.10.x",
      _36_strich_unmaskiert, "Zellen, der Kopf ihrer Tabelle")

sonde("36c", "Verlorener Anker - keine Tabellenzeile mehr",
      _36_anker_verlieren, "keine Tabellenzeile gefunden")

gegenprobe("36", "Maskierter Strich bleibt unbeanstandet - die Schreibweise von D-69",
           _36_strich_maskiert, "Kopf ihrer Tabelle")


# --- Selbstprobe: der Praeparationswaechter selbst (CR-2026-060, D-74) ----------
#
# Ohne sie waere der Waechter die erste ungepruefte Zusage dieses Skripts - und ein
# Waechter, der still ausfaellt, ist genau der Befundtyp, gegen den er gebaut ist.
# Er laeuft ohne Kopie und ohne Validator: Sein Gegenstand ist reine Textarithmetik.
def selbstprobe_waechter() -> None:
    """Der Waechter meldet sich, wenn ein Suchtext nicht genau so oft trifft."""
    faelle = [
        ("W1", "Suchtext trifft gar nicht",
         lambda: ersetzt("abc", ("xyz", "1")), True),
        ("W2", "Suchtext trifft oefter als erwartet",
         lambda: ersetzt("aa", ("a", "b")), True),
        ("W3", "Suchtext trifft genau so oft wie erwartet",
         lambda: ersetzt("aa", ("a", "b", 2)), False),
        ("W4", "Die ZWEITE Ersetzung trifft nicht - der Fall der halben Praeparation",
         lambda: ersetzt("ab", ("a", "x"), ("zzz", "y")), True),
    ]
    for nummer, was, aufruf, erwartet_fehler in faelle:
        try:
            aufruf()
            geworfen = False
        except Praeparationsfehler:
            geworfen = True
        melde("SELBSTPROBE", nummer, geworfen == erwartet_fehler, was)

    # W5: Der Waechter darf nichts geschrieben haben, wenn er abbricht. ersetzt()
    # arbeitet auf einem Text und gibt ihn erst am Ende zurueck - das ist die Zusage,
    # und sie wird hier gepruft, nicht behauptet.
    try:
        ersetzt("ab", ("a", "x"), ("zzz", "y"))
        ergebnis = "durchgelaufen"
    except Praeparationsfehler as exc:
        ergebnis = str(exc)
    melde("SELBSTPROBE", "W5", "zzz" in ergebnis and "trifft 0x" in ergebnis,
          "Die Meldung nennt den Suchtext, der nicht mehr passt")


buendel(selbstprobe_waechter,
        "Der Praeparationswaechter selbst: Er meldet jeden Suchtext, der nicht genau so oft "
        "trifft wie erwartet, und schreibt bei Abbruch nichts")


def selbstprobe_kennung() -> None:
    """Der Kennungswaechter - er ist genau so klug wie die Kennung, die man ihm gibt."""
    root = kopie()
    try:
        pfad = _p(root, EDGE_30)
        try:
            frei(pfad, "G-99")
            frei_ok = True
        except Praeparationsfehler:
            frei_ok = False
        melde("SELBSTPROBE", "K1", frei_ok,
              "G-99 ist im Repositorium nicht vergeben - die Gegenprobe 30 darf sie nutzen")

        try:
            frei(pfad, "G-01")
            kollision = False
        except Praeparationsfehler:
            kollision = True
        melde("SELBSTPROBE", "K2", kollision,
              "Eine vergebene Kennung wird gemeldet - der Fall G-18 vom 2026-09-13")
    finally:
        aufraeumen(os.path.dirname(root))


buendel(selbstprobe_kennung,
        "Der Kennungswaechter ist genau so klug wie die Kennung, die man ihm gibt - eine "
        "freie laeuft durch, eine vergebene wird gemeldet")

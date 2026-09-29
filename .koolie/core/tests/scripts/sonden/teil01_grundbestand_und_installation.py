"""Sonden zu den Pruefungen 6, 14 und 18 bis 25, zum Schutz-Hook und zu install.py
(Skillliste, Aktivierungspruefung, Clientwahl, Erstinstallation, ignorierte Kerndateien,
Kennzeichen im Projekt, Schritte je Pack) und zur Mermaid-Umgebung.

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
    aufraeumen, baumhash, buendel, eintragen, ersetze, gegenprobe, installation, kopie,
    lauf, lies, melde, notiz, P, Praeparationsfehler, QUELLE, schreib, sonde,
    strict_ausgabe, unterprozess, validator_ausgabe)


# --- 14: der Clientname im Kern ------------------------------------------------------
#
# Pruefung 14 gibt es seit 0.20.0 und sie hatte bis 0.57.1 KEINE Sonde - sie lag
# ausserhalb der Spanne "6 und 18 bis 47". Nach D-23 galt sie damit als nicht
# vorhanden. Wer sie aendert, baut sie nach; diese vier Einheiten holen das nach und
# belegen zugleich die Verschaerfung von D-129.
#
# Die Sonden lesen den Namen aus den Manifesten der Kopie, statt ihn zu schreiben:
# Eine Sonde, die einen Produktnamen raet, misst den geratenen Namen.
M14_NAME = "nennt ein Client-Produkt"
M14_PLATZHALTER = "traegt den Clientnamen"
M14_ANKER = "kein Client Pack mit manifest.json gefunden"
P14_WURZELQUELLE = ".koolie/core/framework/runtime/root-instruction.md".replace("/", os.sep)
P14_CHRONIK = ".koolie/core/tests/protocols/2026-09-18-sonde-14.md".replace("/", os.sep)


def _14_produktname(root: str) -> str:
    """Kapitalisierter Produktname eines Packs - aus dessen Kennung, nicht geraten."""
    base = P(root, ".koolie/core", "clients")
    for name in sorted(os.listdir(base)):
        if name.startswith("_"):
            continue
        mp = os.path.join(base, name, "manifest.json")
        if os.path.exists(mp):
            kennung = json.loads(lies(mp))["client"]
            return " ".join(w.capitalize() for w in kennung.split("-"))
    raise Praeparationsfehler(
        "Kein Client Pack mit manifest.json unter clients/ - die Sonden zu 14 leiten "
        "den Produktnamen von dort ab")


def _14_datei(root: str, name: str, inhalt: str) -> None:
    """Eine neue Prompt-Datei mit vollstaendigem Steckbrief und der Inhaltszeile."""
    schreib(P(root, (".koolie/core/prompts/" + name).replace("/", os.sep)),
            "# Sondenvorlage\r\n\r\n"
            "| Attribut | Wert |\r\n|---|---|\r\n"
            "| ID | `FW-PR-015` |\r\n| Version | `0.1.0` |\r\n"
            "| Status | `pilot` |\r\n"
            "| Owner (Rolle) | `<FRAMEWORK_OWNER>` |\r\n\r\n"
            + inhalt + "\r\n")


def _14_produktname_mit_zusatz(root: str) -> None:
    """Der Produktname MIT ZUSATZ in einem Kerntraeger - bis 0.57.0 zulaessig.

    Genau die Form, die D-28 erlaubte und die in fuenfzehn Fundstellen stand.
    """
    _14_datei(root, "15-sonde-produktname.md",
              "Zugang zu %s ist Voraussetzung fuer die Uebung." % _14_produktname(root))


def _14_blosser_name(root: str) -> None:
    """Der blosse Name als Handelnder - der Fall, den D-28 schon immer verbot.

    Sie belegt, dass die Verschaerfung den ALTEN Gegenstand nicht verloren hat: Eine
    neue Pruefung darf den Fall ihrer Vorgaengerin nicht mitnehmen.
    """
    _14_datei(root, "15-sonde-akteur.md",
              "%s entscheidet, welche Datei geoeffnet wird."
              % _14_produktname(root).split()[0])


def _14_platzhalter_mit_namen(root: str) -> None:
    """Ein Platzhalter, der den Clientnamen traegt - der Fall aus CR-2026-070.

    Der Marker stand acht Releases im Kern, weil die Akteurspruefung den
    kapitalisierten Namen sucht und der Marker ihn GROSS schreibt.
    """
    _14_datei(root, "15-sonde-platzhalter.md",
              "Stand: <VERIFY AGAINST CURRENT %s DOCUMENTATION>."
              % _14_produktname(root).split()[0].upper())


def _14_anker_verlieren(root: str) -> None:
    """Ohne manifest.json unter clients/ hat Pruefung 14 keine Namen mehr.

    Bis 0.57.1 stieg sie an dieser Stelle STILL aus (`if not namen: return`) - eine
    Pruefung, die ihren Gegenstand verliert und nichts sagt, ist nach D-23 keine.
    """
    base = P(root, ".koolie/core", "clients")
    getroffen = 0
    for name in sorted(os.listdir(base)):
        mp = os.path.join(base, name, "manifest.json")
        if os.path.exists(mp):
            os.remove(mp)
            getroffen += 1
    if not getroffen:
        raise Praeparationsfehler(
            "Kein manifest.json unter clients/ - die Ankersonde zu 14 haette nichts "
            "zu entfernen")


def _14_chronik(root: str) -> None:
    """Ein Produktname in einem Protokoll bleibt zulaessig - es berichtet eine Messung."""
    schreib(P(root, P14_CHRONIK),
            "# Sondenprotokoll\r\n\r\nDer Lauf ist gegen %s gefahren worden.\r\n"
            % _14_produktname(root))


def _14_platzhalter_gerendert(root: str) -> None:
    """<CLIENT_NAME> in einer gerenderten Quelle - der einzige Weg, der offen bleibt.

    Die Wurzel-Anweisungsdatei traegt ihn seit 0.7.0 im Titel und ist damit der einzige
    angewandte Fall im ganzen Bestand. Die Gegenprobe legt einen zweiten daneben und
    belegt, dass die verschaerfte Pruefung ihn nicht mitnimmt.
    """
    pfad = P(root, P14_WURZELQUELLE)
    schreib(pfad, lies(pfad).rstrip("\r\n")
            + "\r\n\r\nDiese Anweisung gilt fuer <CLIENT_NAME>.\r\n")


sonde("14a", "Der Produktname MIT ZUSATZ in einem Kerntraeger wird gemeldet - die "
             "Ausnahme, die D-129 abgeschafft hat", _14_produktname_mit_zusatz, M14_NAME)

sonde("14b", "Der blosse Name als Handelnder wird weiterhin gemeldet - die Verschaerfung "
             "hat den alten Gegenstand nicht verloren", _14_blosser_name, M14_NAME)

sonde("14c", "Ein Platzhalter mit Clientnamen wird gemeldet - er steht gross und entgeht "
             "der Namenssuche", _14_platzhalter_mit_namen, M14_PLATZHALTER)

sonde("14d", "Ohne manifest.json unter clients/ meldet Pruefung 14 den verlorenen "
             "Gegenstand, statt still auszusteigen", _14_anker_verlieren, M14_ANKER)

gegenprobe("14a", "Das unveraenderte Repositorium bleibt unbeanstandet - die fuenfzehn "
                  "Nennungen sind aufgeloest", None, M14_NAME)

gegenprobe("14b", "Ein Produktname in einem Protokoll bleibt zulaessig - Chronik "
                  "berichtet einen vergangenen Stand", _14_chronik, M14_NAME)

gegenprobe("14c", "<CLIENT_NAME> in einer gerenderten Quelle bleibt zulaessig - das ist "
                  "der Weg, den D-129 offen laesst", _14_platzhalter_gerendert, M14_NAME)


# --- 18: verwaister Hook-Dateiname in einer root-template-Vorlage -----------------
sonde("18b", "Verwaiste Hook-Datei als geliefertes Artefakt in der Vorlage",
      lambda r: schreib(
          P(r, ".koolie/core/clients/devin-desktop/root-template/.devin/README.md".replace("/", os.sep)),
          lies(P(r, ".koolie/core/clients/devin-desktop/root-template/.devin/README.md".replace("/", os.sep)))
          .replace("| `config.json` |", "| `hooks.v1.json` | Lebenszyklus-Hooks | `[DOK]` |\r\n| `config.json` |", 1)),
      "hooks.v1.json")

gegenprobe("18b", "Erklaerende Nennung im Fliesstext bleibt unbeanstandet", None, "FEHLER")

# --- 19: Auskunftsabschnitt ------------------------------------------------------
def _entferne_abschnitt(root: str) -> None:
    pfad = P(root, ".koolie/core/clients/devin-desktop/CLIENT_PACK.md".replace("/", os.sep))
    text = lies(pfad)
    start = text.index("## 7. Anweisungs- und Konfigurationsquellen")
    ende = text.index("## 8. Änderungsverlauf")
    schreib(pfad, text[:start] + text[ende:])


sonde("19", "Ein Pack ohne den Abschnitt ueber Anweisungs- und Konfigurationsquellen "
     "ausserhalb des Projekts wird gemeldet", _entferne_abschnitt,
      "Anweisungs- und Konfigurationsquellen außerhalb des Projekts' fehlt")


def _datum_entfernen(root: str) -> None:
    pfad = P(root, ".koolie/core/clients/claude-code/CLIENT_PACK.md".replace("/", os.sep))
    text = lies(pfad)
    start = text.index("## 8. Anweisungs- und Konfigurationsquellen")
    ende = text.index("## 9. Änderungsverlauf")
    mitte = re.sub(r"\d{4}-\d{2}-\d{2}", "neulich", text[start:ende])
    schreib(pfad, text[:start] + mitte + text[ende:])


sonde("19", "Eine Auskunft ohne Erhebungsdatum ist eine Behauptung ohne Stand und wird gemeldet", _datum_entfernen, "nennt keinen Erhebungsstand")
gegenprobe("19", "Vorlage mit <TBD>-Erhebungsstand laeuft durch", None, "Erhebungsstand")

# --- 20: Dokumenttabellen gegen Manifest -----------------------------------------
sonde("20", "Verfaelschter Wert in der Registrierungstabelle",
      lambda r: schreib(P(r, ".koolie/core/docs/PLACEHOLDER_REGISTRY.md".replace("/", os.sep)),
                        lies(P(r, ".koolie/core/docs/PLACEHOLDER_REGISTRY.md".replace("/", os.sep)))
                        .replace("| `<SKILLS_DIR>` | Skill-Ablage | `.devin/skills`",
                                 "| `<SKILLS_DIR>` | Skill-Ablage | `.devin/faehigkeiten`", 1)),
      "<SKILLS_DIR> steht fuer 'devin-desktop'")

sonde("20", "Ein verfaelschter Pfad im Laufzeitglossar weicht vom Manifest des Packs ab und "
      "wird gemeldet",
      lambda r: schreib(P(r, ".koolie/core/docs/RUNTIME_GLOSSARY.md".replace("/", os.sep)),
                        lies(P(r, ".koolie/core/docs/RUNTIME_GLOSSARY.md".replace("/", os.sep)))
                        .replace("| **Agentenprofile** | Verzeichnis der Subagentenprofile | `.devin/agents/`",
                                 "| **Agentenprofile** | Verzeichnis der Subagentenprofile | `.devin/profile/`", 1)),
      "'Agentenprofile' steht fuer 'devin-desktop'")

gegenprobe("20", "Begriff ohne Manifestfeld und eingebettete Hook-Datei bleiben unbeanstandet",
           None, "das Manifest fuehrt")

# D-421: Ein Pack ohne Spalte fiel still aus dem Abgleich - mit 1.13.0 fuehrten beide
# Tabellen kiro nicht. Die Sonde benennt die Spalte um; der Wert darunter bleibt stehen.
sonde("20", "Eine Tabelle ohne Spalte fuer ein Pack mit Manifest wird gemeldet",
      lambda r: schreib(P(r, ".koolie/core/docs/RUNTIME_GLOSSARY.md".replace("/", os.sep)),
                        lies(P(r, ".koolie/core/docs/RUNTIME_GLOSSARY.md".replace("/", os.sep)))
                        .replace("| `openai-codex` | `kiro` |", "| `openai-codex` | `kiro-alt` |", 1)),
      "die Tabelle fuehrt keine Spalte fuer 'kiro'")

gegenprobe("20", "Beide Tabellen fuehren je Pack eine Spalte", None, "fuehrt keine Spalte")

# --- 21: Hook-Skripte neutral ----------------------------------------------------
sonde("21", "Eine clientgebundene Umgebungsvariable im gemeinsamen Hook-Skript bindet es an "
      "ein Pack und wird gemeldet",
      lambda r: schreib(P(r, ".koolie/core/tests/scripts/hook-overlay-status.py".replace("/", os.sep)),
                        lies(P(r, ".koolie/core/tests/scripts/hook-overlay-status.py".replace("/", os.sep)))
                        .replace("root = argumente[0] if argumente else os.getcwd()",
                                 'root = argumente[0] if argumente else os.environ.get("DEVIN_PROJECT_DIR", os.getcwd())', 1)),
      "ist die Umgebungsvariable des Packs")

sonde("21", "Laufzeitpfad eines Packs in der Pfadbildung",
      lambda r: schreib(P(r, ".koolie/core/tests/scripts/hook-overlay-status.py".replace("/", os.sep)),
                        lies(P(r, ".koolie/core/tests/scripts/hook-overlay-status.py".replace("/", os.sep)))
                        .replace('candidates.append(os.path.join(root, ".koolie/project-overlay", "OVERLAY.md"))',
                                 'candidates.append(os.path.join(root, ".devin", "rules", "20-project-overlay.md"))', 1)),
      "Hier wird ein Pfad aus")

gegenprobe("21", "Schutzmuster in hook-check-secrets.py bleiben unbeanstandet",
           None, "hook-check-secrets.py")

# --- 22: Importsteuerung ---------------------------------------------------------
def _steuerung_verfaelschen(root: str) -> None:
    # Seit 1.12.1 steht windsurf auf true (K-156, D-411); verfaelscht wird cursor.
    pfad = P(root, ".devin", "config.json")
    schreib(pfad, lies(pfad).replace('"cursor": false', '"cursor": true', 1))


sonde("22", "Ein verfaelschter Wert der Importsteuerung read_config_from weicht vom Manifest "
      "ab und wird gemeldet", _steuerung_verfaelschen,
      "die Importsteuerung 'read_config_from' steht als".replace("die ", "Die "))


def _steuerung_entfernen(root: str) -> None:
    import json
    pfad = P(root, ".devin", "config.json")
    d = json.loads(lies(pfad))
    d.pop("read_config_from", None)
    schreib(pfad, json.dumps(d, indent=2, ensure_ascii=False) + "\n")


sonde("22", "Eine fehlende Importsteuerung read_config_from laesst offen, welche fremden "
      "Konfigurationen der Client liest", _steuerung_entfernen,
      "Die Importsteuerung 'read_config_from' fehlt")

gegenprobe("22", "Pack ohne import_control laeuft durch", None, "Importsteuerung")

# --- 23: normative Schluesselwoerter im HTML-Kommentar ---------------------------
sonde("23", "Normativer Satz im Kopfkommentar der Wurzel-Anweisungsdatei",
      lambda r: schreib(P(r, ".koolie/core/framework/runtime/root-instruction.md".replace("/", os.sep)),
                        lies(P(r, ".koolie/core/framework/runtime/root-instruction.md".replace("/", os.sep)))
                        .replace("Was gilt, steht im Fließtext",
                                 "Diese Datei darf nur über den Änderungsprozess geändert werden. "
                                 "Was gilt, steht im Fließtext", 1)),
      "steht in einem HTML-Kommentar")

sonde("23", "Normatives MUSS im Kommentar einer installierten Regeldatei",
      lambda r: schreib(P(r, ".devin", "rules", "00-framework-core.md"),
                        "<!-- Herkunft: Ebene 3. Diese Regel MUSS geladen werden. -->\r\n"
                        + lies(P(r, ".devin", "rules", "00-framework-core.md"))),
      "'MUSS' steht in einem HTML-Kommentar")

gegenprobe("23", "Herkunftsangaben im Kommentar bleiben unbeanstandet", None,
           "HTML-Kommentar")

# --- 24: Nicht-Regeltexte in der Vorlage der Regelablage -------------------------
def _fremddatei(root: str) -> None:
    basis = P(root, ".koolie/core/clients/devin-desktop/root-template/.devin/rules".replace("/", os.sep))
    os.makedirs(basis, exist_ok=True)
    schreib(os.path.join(basis, "README.md"), "# Erklaerender Text\r\n")


sonde("24", "Erklaerender Text in der Vorlage der Regelablage", _fremddatei, "kein Regeltext")


def _echte_regel(root: str) -> None:
    basis = P(root, ".koolie/core/clients/devin-desktop/root-template/.devin/rules".replace("/", os.sep))
    os.makedirs(basis, exist_ok=True)
    schreib(os.path.join(basis, "40-tech-beispiel.md"), "---\r\ntrigger: glob\r\n---\r\n")


gegenprobe("24", "Regeltext nach Nummernschema bleibt unbeanstandet", _echte_regel,
           "kein Regeltext")

# --- 6 (B03, D-39): Die Inhaltspruefung meldet die Fundstelle, nicht den Wert -----
#
# Diese Sonden pruefen **zwei** Bedingungen statt einer. Die erste - der Befund wird
# gemeldet - haette auch die alte Fassung bestanden: Sie meldete ja, und zwar mitsamt dem
# gefundenen Wert. Die zweite ist die eigentliche und der Grund dieses Blocks: Der
# Markerwert darf in der gesamten Ausgabe des Laufs nicht vorkommen.
#
# Die Marker sind bewusst eindeutig gewaehlt, damit ihr Fehlen etwas bedeutet. Ein Marker,
# der auch sonst im Repositorium vorkommen koennte, wuerde die zweite Bedingung entwerten -
# man wuesste nicht, ob er aus der Sonde stammt oder von woanders.
#
# Nicht abgedeckt: der Mermaid-Fehlerpfad. Er verlangt einen fehlschlagenden Lauf des
# externen Renderers; `mmdc` ist in dieser Umgebung nicht vorhanden. Die Stelle ist
# geaendert, aber unbelegt - das ist nach D-23 ein offener Punkt, kein erledigter.

B03_ZIEL = ".koolie/core/docs/ROADMAP.md".replace("/", os.sep)
B03_MAIL = "b03messmarke@sondenlauf-b03.test"
B03_IP = "10.203.44.91"
B03_HOST = "sondenlauf-b03.internal"
B03_URL = "https://sondenlauf-b03.example.net/b03"
B03_TERM = "Sondenlauf-B03-Sperrbegriff"
B03_SECRET = "AKIAB03MESSMARKE0000"


def _b03_anhaengen(*zeilen: str):
    """Haengt Text an eine gepruefte Datei der Kopie - der Ort ist beliebig, der Wert nicht."""
    def tun(root: str) -> None:
        pfad = P(root, B03_ZIEL)
        schreib(pfad, lies(pfad) + "\r\n" + "\r\n".join(zeilen) + "\r\n")
    return tun


def _b03_term(root: str) -> None:
    """Sperrbegriff: Er muss in die Liste **und** in eine gepruefte Datei.

    Die schaerfste der sechs Kategorien. forbidden-terms.txt ist von der Inhaltspruefung
    ausgenommen, weil dort reale Namen stehen - und die Diagnose schrieb den Namen dann
    doch in die Ausgabe.
    """
    liste = P(root, ".koolie/project-overlay", "forbidden-terms.txt")
    schreib(liste, lies(liste).rstrip("\r\n") + "\r\n" + B03_TERM + "\r\n")
    _b03_anhaengen(f"Sondenzeile: {B03_TERM} steht hier absichtlich.")(root)


def sonde_ohne_wert(nummer: str, was: str, praeparieren, erwartet: str, marker: str) -> None:
    """Sonde mit doppelter Bedingung: gemeldet **und** der Wert nicht in der Ausgabe.

    Die Ausgabe wird bei einer Abweichung nur **bereinigt** gezeigt. Andernfalls truege die
    Fehlermeldung dieser Sonde den Wert weiter, den die Sonde gerade als weitergetragen
    beanstandet - derselbe Fehler eine Ebene hoeher.
    """
    def arbeit() -> None:
        root = kopie()
        try:
            vorher = baumhash(root)
            try:
                praeparieren(root)
            except Praeparationsfehler as exc:
                melde("SONDE", nummer, False, was + "  [Praeparation gebrochen]")
                notiz("        " + str(exc))
                return
            if baumhash(root) == vorher:
                melde("SONDE", nummer, False, was + "  [nichts praepariert]")
                return
            ausgabe = lauf(root)
            gemeldet = erwartet in ausgabe
            verschwiegen = marker not in ausgabe
            melde("SONDE", nummer, gemeldet and verschwiegen, was)
            if not gemeldet:
                bereinigt = ausgabe.replace(marker, "<Marker entfernt>")
                notiz("        Befund nicht gemeldet. Ausgabe:",
                      " | ".join(bereinigt.splitlines()[:6]))
            if not verschwiegen:
                notiz(f"        Der Markerwert steht in der Ausgabe - das ist B03 selbst. "
                      f"Erwartete Kennung: {erwartet}")
        finally:
            aufraeumen(os.path.dirname(root))

    eintragen("SONDE", nummer, was, arbeit)


sonde_ohne_wert("6", "E-Mail-Adresse: gemeldet, Wert nicht ausgegeben",
                _b03_anhaengen(f"Sondenzeile: {B03_MAIL}"),
                "FW-CONTENT-EMAIL", B03_MAIL)

sonde_ohne_wert("6", "IP-Adresse: gemeldet, Wert nicht ausgegeben",
                _b03_anhaengen(f"Sondenzeile: {B03_IP}"),
                "FW-CONTENT-IP", B03_IP)

sonde_ohne_wert("6", "Interner Hostname: gemeldet, Wert nicht ausgegeben",
                _b03_anhaengen(f"Sondenzeile: {B03_HOST}"),
                "FW-CONTENT-HOST", B03_HOST)

sonde_ohne_wert("6", "URL ausserhalb der Allowlist: gemeldet, Wert nicht ausgegeben",
                _b03_anhaengen(f"Sondenzeile: {B03_URL}"),
                "FW-CONTENT-URL", B03_URL)

sonde_ohne_wert("6", "Gesperrter Begriff: gemeldet, Begriff nicht ausgegeben",
                _b03_term, "FW-CONTENT-TERM", B03_TERM)

sonde_ohne_wert("6", "Secret-Muster: gemeldet mit Fundstelle, Wert nicht ausgegeben",
                _b03_anhaengen(f"Sondenzeile: {B03_SECRET}"),
                "FW-CONTENT-SECRET", B03_SECRET)


def _b03_erlaubte_faelle(root: str) -> None:
    """Die Gegenprobe: dieselben Kategorien in ihrer erlaubten Gestalt.

    Ohne sie belegt der Block nur, dass die Pruefung meldet - nicht, dass sie das Richtige
    meldet. Eine Pruefung, die jede Adresse beanstandet, besteht alle sechs Sonden oben.
    """
    _b03_anhaengen(
        "Gegenprobe: kontakt@example.com ist eine Dokumentationsadresse.",
        "Gegenprobe: 203.0.113.7 stammt aus dem Dokumentationsbereich.",
        "Gegenprobe: https://docs.devin.ai/ steht auf der Allowlist.",
    )(root)


gegenprobe("6", "Dokumentationsadresse, Dokumentations-IP und Allowlist-URL bleiben unbeanstandet",
           _b03_erlaubte_faelle, "FW-CONTENT-")


def _gitignore_beilage(root: str) -> None:
    """Eine ignorierte Datei mit einem Befund - und eine gleichartige daneben.

    🔴 Der Gegenstand von D-215: Was die `.gitignore` als einfachen Dateinamen
    fuehrt, ist nicht eingecheckt und damit kein Bestandteil des Repositoriums.
    Gemessen am 2026-09-20 an der lokalen Beilage der Uebergabe, die Servername
    und Konto traegt und deshalb ueberhaupt existiert.
    """
    gi = os.path.join(root, ".gitignore")
    alt = io.open(gi, encoding="utf-8", newline="").read()
    daten = (alt.rstrip("\r\n") + "\r\nPROBE-IGNORIERT.md\r\n").encode("utf-8")
    io.open(gi, "wb").write(daten)
    # Die ignorierte Datei traegt einen Befund, der ohne D-215 gemeldet wuerde.
    inhalt = ("# Probe\r\n\r\nServer: 10.11.12.13\r\n").encode("utf-8")
    io.open(os.path.join(root, "PROBE-IGNORIERT.md"), "wb").write(inhalt)


def _gitignore_nicht_gefuehrt(root: str) -> None:
    """Dieselbe Datei unter einem Namen, den die .gitignore NICHT fuehrt."""
    inhalt = ("# Probe\r\n\r\nServer: 10.11.12.13\r\n").encode("utf-8")
    io.open(os.path.join(root, "PROBE-GEFUEHRT.md"), "wb").write(inhalt)


sonde("6i", "Eine NICHT ignorierte Datei mit IP-Adresse wird weiter gemeldet",
      _gitignore_nicht_gefuehrt, "FW-CONTENT-IP")
gegenprobe("6i", "Eine in der .gitignore gefuehrte Datei wird uebersprungen "
                 "(D-215)",
           _gitignore_beilage, "FW-CONTENT-IP")

def sonde_hook_zusatzmuster() -> None:
    """Dieselbe Regel im ausgelieferten Hook - ohne Validatorlauf, weil keiner noetig ist.

    Ein ungueltiges Zusatzmuster wurde bis 0.26.0 mitsamt seinem Wert nach stderr
    geschrieben. Projektspezifische Pfadmuster tragen Projekt-, Kunden- und Hostnamen.
    """
    marker = "b03hookmarke.internal"
    umgebung = dict(os.environ, FW_HOOK_EXTRA_PATH_PATTERNS=marker + "/[")
    p = unterprozess(
        [sys.executable, os.path.join(QUELLE, ".koolie/core", "tests", "scripts",
                                      "hook-check-secrets.py")],
        input='{"tool_name": "Read", "tool_input": {"file_path": "beispiel.txt"}}',
        env=umgebung)
    ausgabe = (p.stdout or "") + (p.stderr or "")
    gemeldet = "Ungueltiges Zusatzmuster an Position 1" in ausgabe
    verschwiegen = marker not in ausgabe
    melde("SONDE", "6h", gemeldet and verschwiegen,
          "Hook: ungueltiges Zusatzmuster gemeldet, Wert nicht ausgegeben")
    if not gemeldet:
        notiz("        Meldung fehlt. Ausgabe:",
              " | ".join(ausgabe.replace(marker, "<Marker entfernt>").splitlines()[:4]))
    if not verschwiegen:
        notiz("        Der Markerwert steht in der Ausgabe - das ist B03 im Hook.")


buendel(sonde_hook_zusatzmuster,
        "Der ausgelieferte Hook meldet ein ungueltiges Zusatzmuster, ohne dessen Wert "
        "auszugeben - projektspezifische Pfadmuster tragen Projekt-, Kunden- und Hostnamen")


# --- 25 (D-41): Ein Ausfall ohne benannten Ersatz -------------------------------
#
# Die Sonde nimmt der S5-Zeile das Wort, auf das die Pruefung sieht. Das ist die ganze
# Bauart der Pruefung - sie kann nicht beurteilen, ob ein Ersatz taugt, nur dass jemand
# die Frage beantwortet hat.

def _b40_ersatz_entfernen(root: str) -> None:
    pfad = P(root, ".koolie/core/clients/claude-code/CLIENT_PACK.md".replace("/", os.sep))
    schreib(pfad, lies(pfad).replace("Ersatz", "Behelf"))


sonde("25", "Zeile auf [NICHT ABBILDBAR] ohne benannten Ersatz",
      _b40_ersatz_entfernen, "Zeile S5 steht auf [NICHT ABBILDBAR]")

# Die Zusammenfassungstabelle desselben Dokuments fuehrt dieselbe Klasse als
# Zeilenbeschriftung und nennt keinen Ersatz. Eine Pruefung, die jede Zeile mit der Klasse
# meldet, beanstandet sie - und besteht die Sonde darueber trotzdem.
gegenprobe("25", "Klassenzeile der Zusammenfassungstabelle bleibt unbeanstandet",
           None, "steht auf [NICHT ABBILDBAR]")


# --- 25b (D-480): die Kennung mit zwei Buchstaben ------------------------------------
#
# Bis 1.19.1 las Pruefung 25 die Zeilenkennung mit dem Muster von Pruefung 31, das nur
# EINEN Buchstaben kennt: Dieselbe Konstante stand zweimal im Validator, und die spaetere
# Bindung galt fuer beide. Gefunden hat es die Aufteilung, nicht ein Lauf - heute fuehrt
# kein Pack eine solche Zeile. Die Sonde legt eine an, die keinen Ersatz nennt.
P25B_PACK = ".koolie/core/clients/claude-code/CLIENT_PACK.md"


def _25b_zwei_buchstaben(root: str) -> None:
    pfad = P(root, P25B_PACK.replace("/", os.sep))
    text = lies(pfad)
    zeilen = [z for z in text.split("\n") if z.startswith("| S5 |")]
    if len(zeilen) != 1:
        raise Praeparationsfehler("Sonde 25b: die Zeile S5 steht %dmal im Pack"
                                  % len(zeilen))
    neu = zeilen[0].replace("| S5 |", "| SX5 |", 1).replace("Ersatz", "Behelf")
    schreib(pfad, text.replace(zeilen[0], zeilen[0] + "\n" + neu, 1))


sonde("25b", "Eine Zeile mit zwei Buchstaben in der Kennung auf [NICHT ABBILDBAR] ohne "
      "Ersatz wird gemeldet - bis 1.19.1 sah Pruefung 25 sie nicht",
      _25b_zwei_buchstaben, "Zeile SX5 steht auf [NICHT ABBILDBAR]")


# --- E3 (D-42): install.py --list-skills -----------------------------------------
#
# Kein Validatorlauf: Der Gegenstand ist ein Kommando, kein Artefakt. Gemessen wird an
# seiner Ausgabe.

def sonde_list_skills() -> None:
    """Wirkungsnachweis fuer den Ersatz, den D-42 an die Stelle der Clientauskunft setzt.

    Drei Bedingungen, und die dritte ist die, an der dieses Projekt seine Befunde findet:
    Eine Teilauskunft, die ihre Grenze nicht nennt, verspricht mehr, als sie leistet.
    """
    root = kopie()
    try:
        ablage = P(root, ".devin", "skills")
        # Sonde: ein Skill, den keine Kernquelle liefert - Herkunft muss 'Projekt' sein.
        os.makedirs(os.path.join(ablage, "sonde-d41-projektskill"), exist_ok=True)
        schreib(os.path.join(ablage, "sonde-d41-projektskill", "SKILL.md"),
                "---\r\nname: sonde-d41-projektskill\r\ntriggers:\r\n  - user\r\n---\r\n")
        # Gegenprobe: ein Verzeichnis ohne SKILL.md ist kein Skill.
        os.makedirs(os.path.join(ablage, "sonde-d41-kein-skill"), exist_ok=True)

        p = unterprozess([sys.executable, os.path.join(root, ".koolie/core", "install.py"),
                          "--client", "devin-desktop", "--root", root, "--list-skills"])
        ausgabe = (p.stdout or "") + (p.stderr or "")

        gefuehrt = "sonde-d41-projektskill" in ausgabe
        herkunft = bool(re.search(r"sonde-d41-projektskill\s+Projekt\s+nur Nutzer", ausgabe))
        melde("SONDE", "D41", gefuehrt and herkunft,
              "Skill ohne Kernquelle: gefuehrt, Herkunft 'Projekt', Aufrufbarkeit gelesen")
        if not (gefuehrt and herkunft):
            notiz("        Ausgabe:", " | ".join(ausgabe.splitlines()[:8]))

        melde("GEGENPROBE", "D41", "sonde-d41-kein-skill" not in ausgabe,
              "Verzeichnis ohne SKILL.md wird nicht als Skill gefuehrt")

        melde("SONDE", "D41", "kein vollstaendiger Ersatz" in ausgabe,
              "Die Auskunft nennt ihre eigene Grenze in der Ausgabe")
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonde_list_skills,
        "Die Skillauskunft von install.py fuehrt einen Projektskill mit richtiger Herkunft, "
        "uebergeht ein Verzeichnis ohne SKILL.md und nennt ihre eigene Grenze")


# --- strict-overlay (D-44): Aktivierungspruefung, dieselben Faelle je Pack --------
#
# Diese Sonden brauchen eine **Installation**, keine Kopie des Repositoriums: Die
# Aktivierungspruefung liest die Laufzeitschicht eines Projekts. Das macht sie teurer als
# alle uebrigen - und es ist der Grund, warum der Befund so lange unbemerkt blieb. Eine
# Sonde, die nur im Repositorium laeuft, kann ihn nicht finden.
#
# Der Kern des Nachweises ist die Wiederholung je Pack. B02 war nicht, dass eine Pruefung
# falsch prueft, sondern dass sie **einen Client gar nicht sieht**. Das faellt nur auf, wenn
# derselbe Fall in jeder Installation laeuft.

SO_STATUSFORMEN = (
    (re.compile(r"^(\|\s*Overlay-Status\s*\|\s*)`?[^`|]+`?", re.M), r"\1`{}`"),
    (re.compile(r"^(-\s*Overlay-Status:\s*)`?[^`\n]+`?", re.M), r"\1`{}`"),
)
SO_PLATZHALTER = re.compile(r"<[A-Z][A-Z0-9_]{2,}>|<TBD[^>]*>")


def _so_status(pfad: str, wert: str) -> None:
    t = lies(pfad)
    for muster, ersatz in SO_STATUSFORMEN:
        t = muster.sub(ersatz.format(wert), t)
    schreib(pfad, t)


def sonden_aktivierungspruefung() -> None:
    """Dieselben Faelle in jeder Installation (B02, D-44)."""
    for pack in ("claude-code", "devin-desktop"):
        root = installation(pack)
        try:
            man = json.loads(lies(os.path.join(QUELLE, ".koolie/core", "clients", pack,
                                               "manifest.json")))
            regel = os.path.join(root, *man["pack_runtime_dir"].split("/"),
                                 "20-project-overlay.md")
            rechte = os.path.join(root, *man["permissions_file"].split("/"))
            overlay = os.path.join(root, ".koolie/project-overlay", "OVERLAY.md")

            # --- Status: 'aktiv' ist aktiv, alles andere nicht ---------------------
            for pfad in (regel, overlay):
                _so_status(pfad, "aktiv")
            aus = strict_ausgabe(root)
            melde("GEGENPROBE", "SO", "Overlay-Status ist nicht" not in aus,
                  f"Status 'aktiv' bleibt unbeanstandet ({pack})")

            # 'aktivierung-ausstehend' bestand bis 0.27.0 die Pruefung - der Vergleich
            # war ein Praefixvergleich. Ein Wert, der sagt, dass die Aktivierung
            # aussteht, liess den Fehler sogar verschwinden.
            _so_status(regel, "aktivierung-ausstehend")
            aus = strict_ausgabe(root)
            melde("SONDE", "SO", "sondern 'aktivierung-ausstehend'" in aus,
                  f"Status 'aktivierung-ausstehend' wird gemeldet ({pack})")
            _so_status(regel, "aktiv")

            # --- Berechtigungsdatei: Platzhalter ------------------------------------
            schreib(rechte, SO_PLATZHALTER.sub("platzhalterfrei", lies(rechte)))
            aus = strict_ausgabe(root)
            melde("GEGENPROBE", "SO", "enthält noch Platzhalter" not in aus,
                  f"Bereinigte Berechtigungsdatei bleibt unbeanstandet ({pack})")

            ersetze(rechte,
                    ('"permissions"',
                     '"_sonde": "<TBD: offen>",\r\n  "permissions"'))
            aus = strict_ausgabe(root)
            melde("SONDE", "SO", "enthält noch Platzhalter" in aus,
                  f"Platzhalter in der Berechtigungsdatei wird gemeldet ({pack})")

            # --- Fehlender sicherheitsrelevanter Abschnitt ---------------------------
            # Bis 0.27.0 stand ein Overlay ohne Abschnitt 13 besser da als eines mit
            # einem offenen Wert darin: Die Pruefung sah nur in vorhandene Abschnitte.
            t = lies(overlay)
            start = t.index("## 13.")
            ende = t.index("## 14.")
            schreib(overlay, t[:start] + t[ende:])
            aus = strict_ausgabe(root)
            melde("SONDE", "SO", "Abschnitt ## 13. fehlt" in aus,
                  f"Fehlender sicherheitsrelevanter Abschnitt wird gemeldet ({pack})")
        finally:
            aufraeumen(os.path.dirname(root))


buendel(sonden_aktivierungspruefung,
        "Die Aktivierungspruefung gegen je eine frische Installation beider Packs: "
        "Overlay-Status, Platzhalter in der Berechtigungsdatei, fehlender Abschnitt 13")


# --- B10 (D-45): Die Aktualisierung trifft das installierte Pack -----------------
#
# Kein Validatorlauf: Der Gegenstand ist das Installationswerkzeug. Gemessen wird an dem,
# was es anlegt - und vor allem an dem, was es **nicht** anlegt.
#
# Die Gegenprobe ist hier die wichtigere Haelfte. Dass eine Aktualisierung das richtige
# Pack trifft, sagt noch nicht, dass ein falsches abgewiesen wird; bis 0.27.0 wurde es
# stillschweigend ausgefuehrt und legte 60 Dateien an.

def sonden_clientwahl() -> None:
    """Wirkungsnachweis fuer die Erkennung des installierten Packs (B10, D-45)."""
    fremde_schicht = {"claude-code": ".devin", "devin-desktop": ".claude"}
    for pack, fremd in fremde_schicht.items():
        root = installation(pack)
        try:
            werkzeug = os.path.join(root, ".koolie/core", "install.py")

            p = unterprozess([sys.executable, werkzeug, "--update", "--root", root])
            aus = (p.stdout or "") + (p.stderr or "")
            getroffen = f"Client:  {pack}" in aus
            keine_zweite = not os.path.isdir(os.path.join(root, fremd))
            melde("SONDE", "B10", getroffen and keine_zweite,
                  f"Aktualisierung ohne --client trifft das installierte Pack ({pack})")
            if not (getroffen and keine_zweite):
                notiz("        Ausgabe:", " | ".join(aus.splitlines()[:6]))

            anderes = "devin-desktop" if pack == "claude-code" else "claude-code"
            q = unterprozess([sys.executable, werkzeug, "--update", "--root", root,
                              "--client", anderes])
            abgewiesen = q.returncode == 1
            unberuehrt = not os.path.isdir(os.path.join(root, fremd))
            melde("GEGENPROBE", "B10", abgewiesen and unberuehrt,
                  f"Widersprechendes --client bricht ab statt anzulegen ({pack} statt {anderes})")
        finally:
            aufraeumen(os.path.dirname(root))


buendel(sonden_clientwahl,
        "Die Aktualisierung erkennt das installierte Pack und weist ein fremdes ab, ohne "
        "dabei eine einzige Datei anzulegen")


# --- D-46: Die Erstinstallation ueberschreibt keine Projektdatei -----------------
#
# Die Sonde braucht weder Repositoriumskopie noch Installation, sondern ein leeres
# Verzeichnis mit **einer** fremden Datei darin. Das ist der Fall, den ein aufnehmendes
# Projekt mitbringt - und bis 0.28.0 verlor es sie beim ersten Befehl des Leitfadens.
#
# Doppelte Bedingung, und die zweite ist die eigentliche: Ein Abbruch, der erst nach dem
# Schreiben kommt, ist keiner.

def sonden_erstinstallation() -> None:
    """Wirkungsnachweis fuer den Schutz der Projektdateien (CR-2026-046, D-46)."""
    ziel = tempfile.mkdtemp(prefix="lw-erst-")
    werkzeug = os.path.join(QUELLE, ".koolie/core", "install.py")
    man = json.loads(lies(os.path.join(QUELLE, ".koolie/core", "clients", "claude-code",
                                       "manifest.json")))
    wurzeldatei = man["root_instruction_file"]
    try:
        # --- Sonde: der Name ist belegt, der Inhalt gehoert dem Projekt ----------
        projekt = os.path.join(ziel, "belegt")
        os.makedirs(projekt)
        eigen = os.path.join(projekt, wurzeldatei)
        inhalt = ("# Projektwissen\r\n\r\nDiese Datei gehoert dem Projekt und darf bei einer\r\n"
                  "Erstinstallation nicht verlorengehen.\r\n")
        schreib(eigen, inhalt)

        p = unterprozess([sys.executable, werkzeug, "--client", "claude-code",
                          "--root", projekt])
        abgebrochen = p.returncode == 1
        unberuehrt = lies(eigen) == inhalt
        nichts_geschrieben = not os.path.isdir(os.path.join(projekt, man["runtime_dir"]))
        melde("SONDE", "D46", abgebrochen and unberuehrt and nichts_geschrieben,
              "Erstinstallation bricht ab, Projektdatei und Verzeichnis unberuehrt")
        if not unberuehrt:
            notiz("        Die Projektdatei wurde veraendert - das ist der Befund selbst.")
        elif not (abgebrochen and nichts_geschrieben):
            notiz("        Ausgabe:", " | ".join(
                ((p.stdout or "") + (p.stderr or "")).splitlines()[:6]))

        # --- Gegenprobe: ein freies Verzeichnis laeuft durch ---------------------
        # Ohne sie belegt die Sonde nur, dass etwas abbricht - nicht, dass die
        # Erstinstallation ueberhaupt noch funktioniert.
        leer = os.path.join(ziel, "leer")
        os.makedirs(leer)
        q = unterprozess([sys.executable, werkzeug, "--client", "claude-code",
                          "--root", leer])
        melde("GEGENPROBE", "D46",
              q.returncode == 0 and os.path.isfile(os.path.join(leer, wurzeldatei)),
              "Erstinstallation in ein freies Verzeichnis laeuft durch")
    finally:
        aufraeumen(ziel)


buendel(sonden_erstinstallation,
        "Die Erstinstallation bricht vor einer vorhandenen Projektdatei ab, statt sie zu "
        "ueberschreiben - und schreibt dabei nichts")


# --- D-349/D-352: die Auskunft ueber ignorierte Kerndateien -----------------------
#
# 🔴 DIE AUSKUNFT AUS 1.4.0 HATTE KEINE SONDE, UND SIE ZAEHLTE UNTER WINDOWS ZU WENIG.
# `ignorierte_kerndateien()` gab die Pfade mit `text=True` an `git check-ignore --stdin`;
# unter Windows kam jeder mit angehaengtem `\r` an. Ein Verzeichnismuster (`build/`)
# traf trotzdem - der Fall, an dem die Auskunft gebaut wurde -, ein DATEImuster (`*.md`)
# nie. Gemessen am 2026-09-24: git meldet zwei ignorierte Dateien, die Funktion null
# (CR-2026-135).
#
# DREI EINHEITEN, JEDE MIT EINER UNABHAENGIG GEZAEHLTEN ERWARTUNG. Die Zahl im Hinweis
# wird gegen einen `os.walk` ueber den Kern gehalten, nicht gegen eine gepflegte Zahl:
#   D349  (Sonde)      - `*.md`: jede Markdown-Datei des Kerns wird gezaehlt. Gegen den
#                        Vorstand faellt sie unter Windows mit 0.
#   D349a (Gegenprobe) - `build/`: das Verzeichnismuster, der Anlassfall von K-117,
#                        zaehlt weiter genau die Dateien unter `build/`.
#   D349b (Gegenprobe) - ein Muster, das nichts trifft: kein Hinweis. Eine Auskunft,
#                        die immer etwas meldet, besteht jede Sonde.
M349_HINWEIS = re.compile(r"HINWEIS \((\d+)\): Dieses Projekt IGNORIERT Kerndateien")


def _349_kern(root: str, passt) -> int:
    """Die Kerndateien, die ein Muster treffen sollte - gezaehlt, nicht gepflegt."""
    kern = os.path.join(root, ".koolie", "core")
    n = 0
    for dirpath, dirnames, filenames in os.walk(kern):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in filenames:
            rel = os.path.relpath(os.path.join(dirpath, fn), kern).replace(os.sep, "/")
            n += 1 if passt(rel) else 0
    return n


def sonden_ignorierte_kerndateien() -> None:
    """Wirkungsnachweis fuer die Auskunft aus D-349 an einem echten Repositorium."""
    root = installation("claude-code")
    try:
        if unterprozess(["git", "init", "-q", root]).returncode != 0:
            melde("BUENDEL", "-", False,
                  "sonden_ignorierte_kerndateien  [git nicht erreichbar]")
            notiz("        Ohne git gibt die Auskunft bewusst nichts aus - nicht messbar.")
            return
        werkzeug = os.path.join(root, ".koolie", "core", "install.py")
        faelle = (
            ("SONDE", "D349", "*.md", lambda rel: rel.endswith(".md"),
             "Ein Dateimuster im Projekt-.gitignore wird gezaehlt - jede Markdown-Datei "
             "des Kerns, auch unter Windows"),
            ("GEGENPROBE", "D349a", "build/", lambda rel: rel.startswith("build/"),
             "Ein Verzeichnismuster zaehlt weiter genau die Dateien darunter - der "
             "Anlassfall der Auskunft bleibt erhalten"),
            ("GEGENPROBE", "D349b", "*.sonde-trifft-nichts", lambda rel: False,
             "Ein Muster, das keine Kerndatei trifft, erzeugt keinen Hinweis"),
        )
        for art, kennung, muster, passt, was in faelle:
            schreib(os.path.join(root, ".gitignore"), muster + "\n")
            p = unterprozess([sys.executable, werkzeug, "--update", "--root", root])
            aus = (p.stdout or "") + (p.stderr or "")
            soll = _349_kern(root, passt)
            treffer = M349_HINWEIS.search(aus)
            ist = int(treffer.group(1)) if treffer else 0
            melde(art, kennung, p.returncode == 0 and ist == soll, was)
            if p.returncode != 0 or ist != soll:
                notiz("        Muster %s: gemeldet %d, gezaehlt %d, Exit %d"
                      % (muster, ist, soll, p.returncode))
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_ignorierte_kerndateien,
        "Die Auskunft ueber ignorierte Kerndateien zaehlt Datei- und Verzeichnismuster "
        "richtig und schweigt, wenn nichts ignoriert wird")


# --- D-354: das Kennzeichen des Quellrepositoriums in einem Projekt ---------------
#
# 🔴 WER GANZ `.koolie/` KOPIERT, NIMMT DAS KENNZEICHEN MIT - aus dem Arbeitsbaum wie
# aus dem Release-Archiv, denn es ist versioniert. Danach haelt der Validator das
# Projekt fuer das Quellrepositorium, und keine seiner Meldungen nennt den Grund.
# Gemessen am 2026-09-24 (CR-2026-137): unverfolgt 1 Fehler (Pruefung 79, Lizenz in
# der Projektwurzel), committet 80 (dazu Pruefung 81 an 79 Projekttraegern).
#
# ZWEI EINHEITEN, UND DIE SONDE HAELT ZWEI STELLEN GEGENEINANDER. `install.py` und der
# Validator fuehren den Pfad des Kennzeichens je fuer sich; die Sonde verlangt, dass an
# derselben Datei BEIDE anschlagen - die Auskunft und Pruefung 79. Wandert eine der
# beiden Konstanten, faellt sie.
#   D354  (Sonde)      - Kennzeichen liegt: Hinweis, Exit 0, und Pruefung 79 verlangt
#                        die Lizenz in der Wurzel. Gegen den Vorstand faellt sie.
#   D354a (Gegenprobe) - ohne Kennzeichen: kein Hinweis und keine Lizenzmeldung. Eine
#                        Auskunft, die immer etwas meldet, besteht jede Sonde.
M354_HINWEIS = "das Kennzeichen des Framework-Repositoriums selbst"
M354_VALIDATOR = "LICENSE: fehlt"


def sonden_kennzeichen_im_projekt() -> None:
    """Wirkungsnachweis fuer die Auskunft aus D-354 an einer echten Installation."""
    root = installation("claude-code")
    try:
        werkzeug = os.path.join(root, ".koolie", "core", "install.py")
        kennzeichen = os.path.join(root, ".koolie", "QUELLREPOSITORIUM.md")
        faelle = (
            ("SONDE", "D354", True,
             "Ein mitkopiertes Kennzeichen wird gemeldet, ohne die Installation "
             "anzuhalten - und der Validator erkennt dieselbe Datei"),
            ("GEGENPROBE", "D354a", False,
             "Ohne Kennzeichen kein Hinweis, und der Validator prueft als Projekt"),
        )
        for art, kennung, liegt, was in faelle:
            if liegt:
                shutil.copyfile(os.path.join(QUELLE, ".koolie", "QUELLREPOSITORIUM.md"),
                                kennzeichen)
            elif os.path.exists(kennzeichen):
                os.remove(kennzeichen)
            p = unterprozess([sys.executable, werkzeug, "--update", "--root", root])
            aus = (p.stdout or "") + (p.stderr or "")
            hinweis = M354_HINWEIS in aus
            validator = M354_VALIDATOR in validator_ausgabe(root)
            ok = p.returncode == 0 and hinweis == liegt and validator == liegt
            melde(art, kennung, ok, was)
            if not ok:
                notiz("        Exit %d, Hinweis %s, Pruefung 79 %s (erwartet je %s)"
                      % (p.returncode, hinweis, validator, liegt))
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_kennzeichen_im_projekt,
        "Ein mitkopiertes Kennzeichen des Quellrepositoriums wird bei der Installation "
        "gemeldet, und install.py und Validator erkennen es an derselben Stelle")


# --- D-395: die Schritte nach Installation und Hebung je Pack (K-123) -------------
#
# 🔴 BEI `openai-codex` TRAEGT OHNE VERTRAUEN NICHTS VON ABSCHNITT B, UND DER HOOK
# BRAUCHT NACH JEDER HEBUNG NEUES VERTRAUEN - und `install.py` nannte keins von beidem.
# Seine Schritte waren packneutral und verlangten dazu, `_core_rules_integrity` stehen
# zu lassen, einen Block, den die TOML-Datei dieses Packs nicht fuehrt. Jetzt nennt das
# Manifest die Schritte (post_install_steps, post_update_steps), und den Integritaetsblock
# nennt das Werkzeug nur bei einer Berechtigungsdatei im JSON-Format.
#   D395  (Sonde)      - openai-codex: Installation nennt das Projekt- und das
#                        Hook-Vertrauen und nicht den Integritaetsblock; die Hebung
#                        nennt das erneute Hook-Vertrauen. Gegen den Vorstand faellt sie.
#   D395a (Gegenprobe) - claude-code: Integritaetsblock genannt, kein Vertrauensschritt,
#                        kein Zusatzblock bei der Hebung. Ein Werkzeug, das jedem Pack
#                        die Schritte eines Packs nennt, besteht die Sonde auch.
M395_INSTALL = "als vertraut eintragen"
M395_HOOK = "Dem Schutz-Hook einzeln vertrauen"
M395_UPDATE = "Dem Schutz-Hook ERNEUT vertrauen"
M395_BLOCK = "_core_rules_integrity"


def sonden_schritte_je_pack() -> None:
    """Wirkungsnachweis fuer die packeigenen Schritte aus D-395 an echten Installationen."""
    faelle = (
        ("SONDE", "D395", "openai-codex", True,
         "openai-codex: Installation und Hebung nennen die Vertrauensschritte, "
         "nicht den Integritaetsblock"),
        ("GEGENPROBE", "D395a", "claude-code", False,
         "claude-code: der Integritaetsblock wird genannt, kein Vertrauensschritt"),
    )
    werkzeug = os.path.join(QUELLE, ".koolie", "core", "install.py")
    for art, kennung, pack, codex, was in faelle:
        ziel = tempfile.mkdtemp(prefix="lw-inst-")
        root = os.path.join(ziel, "projekt")
        os.makedirs(root)
        try:
            p = unterprozess([sys.executable, werkzeug, "--client", pack, "--root", root])
            ein = (p.stdout or "") + (p.stderr or "")
            q = unterprozess([sys.executable, werkzeug, "--update", "--root", root])
            heb = (q.stdout or "") + (q.stderr or "")
            ist = (M395_INSTALL in ein, M395_HOOK in ein, M395_BLOCK in ein,
                   M395_UPDATE in heb)
            soll = (codex, codex, not codex, codex)
            ok = p.returncode == 0 and q.returncode == 0 and ist == soll
            melde(art, kennung, ok, was)
            if not ok:
                notiz("        Exit %d/%d, (Projekt, Hook, Block, erneut) = %s, erwartet %s"
                      % (p.returncode, q.returncode, ist, soll))
        finally:
            aufraeumen(ziel)


buendel(sonden_schritte_je_pack,
        "install.py nennt nach Installation und Hebung die Schritte, die das Manifest "
        "des Packs fuehrt, und den Integritaetsblock nur, wo es ihn gibt")


# --- D-398: der Mermaid-Renderer scheitert an der Umgebung, nicht am Diagramm (K-145) --
#
# 🔴 OHNE DEN BROWSER VON PUPPETEER MELDETE `--mermaid` JEDEN BLOCK ALS UNGUELTIG - auch
# unveraenderte -, waehrend der Bau im selben Arbeitsgang alle Diagramme renderte. Der
# Validator nimmt jetzt Browser und Konfiguration des Baus (`mermaid_renderer.py`) und
# erkennt an der Fehlerausgabe, ob der Renderer an der Umgebung gescheitert ist; dann
# warnt er einmal, statt ueber die Diagramme zu urteilen. Den Renderer selbst ruft keine
# Sonde auf - er ist eine Vorbedingung des Arbeitsplatzes, und eine Sonde, die an ihm
# haengt, bestuende auf einem Arbeitsplatz und fiele auf dem naechsten. Gemessen wird die
# Unterscheidung und die Verdrahtung.
#   D398  (Sonde)      - die Meldung, mit der der Renderer am 2026-09-25 ohne Browser
#                        scheiterte, gilt als Umgebungsfehler, und der Validator ruft
#                        den Renderer mit der Konfiguration aus diesem Modul auf.
#   D398a (Gegenprobe) - ein Syntaxfehler des Diagramms gilt NICHT als Umgebungsfehler:
#                        Eine Unterscheidung, die alles zur Umgebung erklaert, machte aus
#                        der Pruefung eine Warnung, die nie mehr einen Fehler meldet.
M398_UMGEBUNG = ("Error: Could not find chrome-headless-shell (ver. 153.0.8010.36). "
                 "This can occur if either")
M398_SYNTAX = ("Error: Parse error on line 2: ...t TD  A[Start --> B{{{ "
               "Expecting 'SQE', 'DOUBLECIRCLEEND', 'PE', got 'DIAMOND_START'")


def sonden_mermaid_umgebung() -> None:
    """Wirkungsnachweis fuer die Unterscheidung aus D-398, ohne den Renderer."""
    skripte = os.path.join(QUELLE, ".koolie", "core", "tests", "scripts")
    code = ("import sys; sys.path.insert(0, sys.argv[1]); import mermaid_renderer as m; "
            "print(m.ist_umgebungsfehler(sys.argv[2]), m.ist_umgebungsfehler(sys.argv[3]))")
    p = unterprozess([sys.executable, "-c", code, skripte, M398_UMGEBUNG, M398_SYNTAX])
    ist = (p.stdout or "").split()
    # Der Validator ist seit 1.19.1 Einstieg und Paket (K-174); gelesen wird beides.
    validator = "".join(lies(os.path.join(skripte, name)) for name in
                        ["validate-framework.py"] + sorted(
                            os.path.join("pruefungen", n) for n in
                            os.listdir(os.path.join(skripte, "pruefungen"))
                            if n.endswith(".py")))
    verdrahtet = ("mermaid_renderer.puppeteer_konfiguration(" in validator
                  and '"-p", pptr' in validator)
    ok = p.returncode == 0 and ist[:1] == ["True"] and verdrahtet
    melde("SONDE", "D398", ok,
          "Die Meldung ohne Browser gilt als Umgebungsfehler, und der Validator "
          "uebergibt die Konfiguration des Baus")
    if not ok:
        notiz("        Exit %d, Ausgabe %r, verdrahtet %s" % (p.returncode, ist, verdrahtet))
    ok = p.returncode == 0 and ist[1:2] == ["False"]
    melde("GEGENPROBE", "D398a", ok,
          "Ein Syntaxfehler des Diagramms bleibt ein Fehler des Diagramms")
    if not ok:
        notiz("        Exit %d, Ausgabe %r" % (p.returncode, ist))


buendel(sonden_mermaid_umgebung,
        "--mermaid unterscheidet einen Renderer ohne Browser von einem ungueltigen "
        "Diagramm und ruft ihn wie der Bau auf")

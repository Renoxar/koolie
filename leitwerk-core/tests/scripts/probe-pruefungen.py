#!/usr/bin/env python3
"""Wirkungsnachweis nach D-23 fuer die Pruefungen 18 bis 24 (Release 0.26.0)
fuer Pruefung 6 (Release 0.26.1, Befund B03), fuer Pruefung 25 samt
install.py --list-skills (Release 0.27.0) und fuer die Aktivierungspruefung samt
Clientwahl der Installation (Release 0.28.0, Befunde B02 und B10).

Aufruf (im Wurzelverzeichnis des Repositoriums):
    python3 leitwerk-core/tests/scripts/probe-pruefungen.py [PFAD]

D-23 sagt: Eine Pruefung gilt erst als vorhanden, wenn sie eine bewusst gesetzte Sonde
meldet. Dieses Skript fuehrt den Nachweis, statt ihn zu behaupten. Je Pruefung

  * eine **Sonde**: ein bekannter Defekt in einer Kopie des Repositoriums - die Pruefung
    MUSS ihn melden;
  * eine **Gegenprobe**: ein Fall, der erlaubt ist und aehnlich aussieht - die Pruefung
    DARF ihn nicht melden.

Die Gegenprobe ist der Teil, den man weglassen kann und nicht weglassen sollte: Eine
Pruefung, die alles meldet, besteht jede Sonde. Die Gegenproben hier treffen genau die
Faelle, an denen die jeweilige Pruefung zu breit haette werden koennen - die erklaerende
Nennung eines Dateinamens im Fliesstext, ein Begriff ohne Manifestfeld, die Schutzmuster
des durchsetzenden Hooks, ein Pack ohne Importsteuerung, Herkunftsangaben im Kommentar.

Gearbeitet wird auf einer Kopie; das Repositorium selbst bleibt unberuehrt. Exit-Code 0 =
alle Sonden gemeldet und keine Gegenprobe beanstandet.

Was dieses Skript **nicht** leistet: Es belegt, dass die Pruefungen wirken, nicht dass
ihre Gegenstaende richtig sind. Die Grenze jeder einzelnen Pruefung steht in deren
Kopfkommentar in validate-framework.py.
"""
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

QUELLE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
VALIDATOR = "leitwerk-core/tests/scripts/validate-framework.py"
fehler = 0


def kopie() -> str:
    ziel = tempfile.mkdtemp(prefix="lw-sonde-")
    shutil.copytree(QUELLE, os.path.join(ziel, "repo"),
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "out"))
    return os.path.join(ziel, "repo")


def baumhash(root: str) -> str:
    """Fingerabdruck des Baums - er entscheidet, ob eine Sonde etwas gesetzt hat.

    Ohne ihn ist ein Suchtext, der nicht mehr passt, von einer Pruefung, die nicht
    meldet, nicht zu unterscheiden: Beides sieht aus wie eine gescheiterte Sonde.
    """
    h = hashlib.sha256()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d != "__pycache__")
        for fn in sorted(filenames):
            pfad = os.path.join(dirpath, fn)
            h.update(os.path.relpath(pfad, root).encode("utf-8", "replace"))
            try:
                with open(pfad, "rb") as fh:
                    h.update(fh.read())
            except OSError:
                pass
    return h.hexdigest()


def lauf(root: str) -> str:
    p = subprocess.run([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                        "--root", root], capture_output=True, text=True)
    return (p.stdout or "") + (p.stderr or "")


def lies(pfad: str) -> str:
    return io.open(pfad, encoding="utf-8", newline="").read()


def schreib(pfad: str, text: str) -> None:
    io.open(pfad, "w", encoding="utf-8", newline="").write(text)


def melde(art: str, nummer: str, ok: bool, was: str) -> None:
    global fehler
    if not ok:
        fehler += 1
    print(f"{art:10s} {nummer:4s} {'OK  ' if ok else 'FEHL'}  {was}")


def sonde(nummer: str, was: str, praeparieren, erwartet: str) -> None:
    root = kopie()
    try:
        vorher = baumhash(root)
        praeparieren(root)
        if baumhash(root) == vorher:
            melde("SONDE", nummer, False, was + "  [nichts praepariert]")
            print("        Der Baum ist unveraendert - vermutlich passt der Suchtext "
                  "der Sonde nicht mehr. Gemessen wuerde sonst die Sonde, nicht die Pruefung.")
            return
        ausgabe = lauf(root)
        melde("SONDE", nummer, erwartet in ausgabe, was)
        if erwartet not in ausgabe:
            print("        Ausgabe:", " | ".join(ausgabe.splitlines()[:6]))
    finally:
        shutil.rmtree(os.path.dirname(root), ignore_errors=True)


def gegenprobe(nummer: str, was: str, praeparieren, verboten: str) -> None:
    root = kopie()
    try:
        if praeparieren:
            vorher = baumhash(root)
            praeparieren(root)
            if baumhash(root) == vorher:
                melde("GEGENPROBE", nummer, False, was + "  [nichts praepariert]")
                return
        ausgabe = lauf(root)
        ok = verboten not in ausgabe and "0 Fehler" in ausgabe
        melde("GEGENPROBE", nummer, ok, was)
        if not ok:
            print("        Ausgabe:", " | ".join(ausgabe.splitlines()[:6]))
    finally:
        shutil.rmtree(os.path.dirname(root), ignore_errors=True)


P = lambda root, *teile: os.path.join(root, *teile)

# --- 18: verwaister Hook-Dateiname in einer root-template-Vorlage -----------------
sonde("18b", "Verwaiste Hook-Datei als geliefertes Artefakt in der Vorlage",
      lambda r: schreib(
          P(r, "leitwerk-core/clients/devin-desktop/root-template/.devin/README.md".replace("/", os.sep)),
          lies(P(r, "leitwerk-core/clients/devin-desktop/root-template/.devin/README.md".replace("/", os.sep)))
          .replace("| `config.json` |", "| `hooks.v1.json` | Lebenszyklus-Hooks | `[DOK]` |\r\n| `config.json` |", 1)),
      "hooks.v1.json")

gegenprobe("18b", "Erklaerende Nennung im Fliesstext bleibt unbeanstandet", None, "FEHLER")

# --- 19: Auskunftsabschnitt ------------------------------------------------------
def _entferne_abschnitt(root: str) -> None:
    pfad = P(root, "leitwerk-core/clients/devin-desktop/CLIENT_PACK.md".replace("/", os.sep))
    text = lies(pfad)
    start = text.index("## 7. Anweisungs- und Konfigurationsquellen")
    ende = text.index("## 8. Änderungsverlauf")
    schreib(pfad, text[:start] + text[ende:])


sonde("19", "Pack ohne Auskunftsabschnitt", _entferne_abschnitt,
      "Anweisungs- und Konfigurationsquellen außerhalb des Projekts' fehlt")


def _datum_entfernen(root: str) -> None:
    pfad = P(root, "leitwerk-core/clients/claude-code/CLIENT_PACK.md".replace("/", os.sep))
    text = lies(pfad)
    start = text.index("## 8. Anweisungs- und Konfigurationsquellen")
    ende = text.index("## 9. Änderungsverlauf")
    mitte = re.sub(r"\d{4}-\d{2}-\d{2}", "neulich", text[start:ende])
    schreib(pfad, text[:start] + mitte + text[ende:])


sonde("19", "Auskunft ohne Erhebungsstand", _datum_entfernen, "nennt keinen Erhebungsstand")
gegenprobe("19", "Vorlage mit <TBD>-Erhebungsstand laeuft durch", None, "Erhebungsstand")

# --- 20: Dokumenttabellen gegen Manifest -----------------------------------------
sonde("20", "Verfaelschter Wert in der Registrierungstabelle",
      lambda r: schreib(P(r, "leitwerk-core/docs/PLACEHOLDER_REGISTRY.md".replace("/", os.sep)),
                        lies(P(r, "leitwerk-core/docs/PLACEHOLDER_REGISTRY.md".replace("/", os.sep)))
                        .replace("| `<SKILLS_DIR>` | Skill-Ablage | `.devin/skills`",
                                 "| `<SKILLS_DIR>` | Skill-Ablage | `.devin/faehigkeiten`", 1)),
      "<SKILLS_DIR> steht fuer 'devin-desktop'")

sonde("20", "Verfaelschter Wert im Laufzeitglossar",
      lambda r: schreib(P(r, "leitwerk-core/docs/RUNTIME_GLOSSARY.md".replace("/", os.sep)),
                        lies(P(r, "leitwerk-core/docs/RUNTIME_GLOSSARY.md".replace("/", os.sep)))
                        .replace("| **Agentenprofile** | Verzeichnis der Subagentenprofile | `.devin/agents/`",
                                 "| **Agentenprofile** | Verzeichnis der Subagentenprofile | `.devin/profile/`", 1)),
      "'Agentenprofile' steht fuer 'devin-desktop'")

gegenprobe("20", "Begriff ohne Manifestfeld und eingebettete Hook-Datei bleiben unbeanstandet",
           None, "das Manifest fuehrt")

# --- 21: Hook-Skripte neutral ----------------------------------------------------
sonde("21", "Clientgebundene Umgebungsvariable im Hook-Skript",
      lambda r: schreib(P(r, "leitwerk-core/tests/scripts/hook-overlay-status.py".replace("/", os.sep)),
                        lies(P(r, "leitwerk-core/tests/scripts/hook-overlay-status.py".replace("/", os.sep)))
                        .replace("root = argumente[0] if argumente else os.getcwd()",
                                 'root = argumente[0] if argumente else os.environ.get("DEVIN_PROJECT_DIR", os.getcwd())', 1)),
      "ist die Umgebungsvariable des Packs")

sonde("21", "Laufzeitpfad eines Packs in der Pfadbildung",
      lambda r: schreib(P(r, "leitwerk-core/tests/scripts/hook-overlay-status.py".replace("/", os.sep)),
                        lies(P(r, "leitwerk-core/tests/scripts/hook-overlay-status.py".replace("/", os.sep)))
                        .replace('candidates.append(os.path.join(root, "project-overlay", "OVERLAY.md"))',
                                 'candidates.append(os.path.join(root, ".devin", "rules", "20-project-overlay.md"))', 1)),
      "Hier wird ein Pfad aus")

gegenprobe("21", "Schutzmuster in hook-check-secrets.py bleiben unbeanstandet",
           None, "hook-check-secrets.py")

# --- 22: Importsteuerung ---------------------------------------------------------
def _steuerung_verfaelschen(root: str) -> None:
    pfad = P(root, ".devin", "config.json")
    schreib(pfad, lies(pfad).replace('"windsurf": false', '"windsurf": true', 1))


sonde("22", "Verfaelschter Wert der Importsteuerung", _steuerung_verfaelschen,
      "die Importsteuerung 'read_config_from' steht als".replace("die ", "Die "))


def _steuerung_entfernen(root: str) -> None:
    import json
    pfad = P(root, ".devin", "config.json")
    d = json.loads(lies(pfad))
    d.pop("read_config_from", None)
    schreib(pfad, json.dumps(d, indent=2, ensure_ascii=False) + "\n")


sonde("22", "Fehlende Importsteuerung", _steuerung_entfernen,
      "Die Importsteuerung 'read_config_from' fehlt")

gegenprobe("22", "Pack ohne import_control laeuft durch", None, "Importsteuerung")

# --- 23: normative Schluesselwoerter im HTML-Kommentar ---------------------------
sonde("23", "Normativer Satz im Kopfkommentar der Wurzel-Anweisungsdatei",
      lambda r: schreib(P(r, "leitwerk-core/framework/runtime/root-instruction.md".replace("/", os.sep)),
                        lies(P(r, "leitwerk-core/framework/runtime/root-instruction.md".replace("/", os.sep)))
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
    basis = P(root, "leitwerk-core/clients/devin-desktop/root-template/.devin/rules".replace("/", os.sep))
    os.makedirs(basis, exist_ok=True)
    schreib(os.path.join(basis, "README.md"), "# Erklaerender Text\r\n")


sonde("24", "Erklaerender Text in der Vorlage der Regelablage", _fremddatei, "kein Regeltext")


def _echte_regel(root: str) -> None:
    basis = P(root, "leitwerk-core/clients/devin-desktop/root-template/.devin/rules".replace("/", os.sep))
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

B03_ZIEL = "leitwerk-core/docs/ROADMAP.md".replace("/", os.sep)
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
    liste = P(root, "project-overlay", "forbidden-terms.txt")
    schreib(liste, lies(liste).rstrip("\r\n") + "\r\n" + B03_TERM + "\r\n")
    _b03_anhaengen(f"Sondenzeile: {B03_TERM} steht hier absichtlich.")(root)


def sonde_ohne_wert(nummer: str, was: str, praeparieren, erwartet: str, marker: str) -> None:
    """Sonde mit doppelter Bedingung: gemeldet **und** der Wert nicht in der Ausgabe.

    Die Ausgabe wird bei einer Abweichung nur **bereinigt** gezeigt. Andernfalls truege die
    Fehlermeldung dieser Sonde den Wert weiter, den die Sonde gerade als weitergetragen
    beanstandet - derselbe Fehler eine Ebene hoeher.
    """
    root = kopie()
    try:
        vorher = baumhash(root)
        praeparieren(root)
        if baumhash(root) == vorher:
            melde("SONDE", nummer, False, was + "  [nichts praepariert]")
            return
        ausgabe = lauf(root)
        gemeldet = erwartet in ausgabe
        verschwiegen = marker not in ausgabe
        melde("SONDE", nummer, gemeldet and verschwiegen, was)
        if not gemeldet:
            bereinigt = ausgabe.replace(marker, "<Marker entfernt>")
            print("        Befund nicht gemeldet. Ausgabe:",
                  " | ".join(bereinigt.splitlines()[:6]))
        if not verschwiegen:
            print(f"        Der Markerwert steht in der Ausgabe - das ist B03 selbst. "
                  f"Erwartete Kennung: {erwartet}")
    finally:
        shutil.rmtree(os.path.dirname(root), ignore_errors=True)


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


def sonde_hook_zusatzmuster() -> None:
    """Dieselbe Regel im ausgelieferten Hook - ohne Validatorlauf, weil keiner noetig ist.

    Ein ungueltiges Zusatzmuster wurde bis 0.26.0 mitsamt seinem Wert nach stderr
    geschrieben. Projektspezifische Pfadmuster tragen Projekt-, Kunden- und Hostnamen.
    """
    marker = "b03hookmarke.internal"
    umgebung = dict(os.environ, FW_HOOK_EXTRA_PATH_PATTERNS=marker + "/[")
    p = subprocess.run(
        [sys.executable, os.path.join(QUELLE, "leitwerk-core", "tests", "scripts",
                                      "hook-check-secrets.py")],
        input='{"tool_name": "Read", "tool_input": {"file_path": "beispiel.txt"}}',
        capture_output=True, text=True, env=umgebung)
    ausgabe = (p.stdout or "") + (p.stderr or "")
    gemeldet = "Ungueltiges Zusatzmuster an Position 1" in ausgabe
    verschwiegen = marker not in ausgabe
    melde("SONDE", "6h", gemeldet and verschwiegen,
          "Hook: ungueltiges Zusatzmuster gemeldet, Wert nicht ausgegeben")
    if not gemeldet:
        print("        Meldung fehlt. Ausgabe:",
              " | ".join(ausgabe.replace(marker, "<Marker entfernt>").splitlines()[:4]))
    if not verschwiegen:
        print("        Der Markerwert steht in der Ausgabe - das ist B03 im Hook.")


sonde_hook_zusatzmuster()


# --- 25 (D-41): Ein Ausfall ohne benannten Ersatz -------------------------------
#
# Die Sonde nimmt der S5-Zeile das Wort, auf das die Pruefung sieht. Das ist die ganze
# Bauart der Pruefung - sie kann nicht beurteilen, ob ein Ersatz taugt, nur dass jemand
# die Frage beantwortet hat.

def _b40_ersatz_entfernen(root: str) -> None:
    pfad = P(root, "leitwerk-core/clients/claude-code/CLIENT_PACK.md".replace("/", os.sep))
    schreib(pfad, lies(pfad).replace("Ersatz", "Behelf"))


sonde("25", "Zeile auf [NICHT ABBILDBAR] ohne benannten Ersatz",
      _b40_ersatz_entfernen, "Zeile S5 steht auf [NICHT ABBILDBAR]")

# Die Zusammenfassungstabelle desselben Dokuments fuehrt dieselbe Klasse als
# Zeilenbeschriftung und nennt keinen Ersatz. Eine Pruefung, die jede Zeile mit der Klasse
# meldet, beanstandet sie - und besteht die Sonde darueber trotzdem.
gegenprobe("25", "Klassenzeile der Zusammenfassungstabelle bleibt unbeanstandet",
           None, "steht auf [NICHT ABBILDBAR]")


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

        p = subprocess.run([sys.executable, os.path.join(root, "leitwerk-core", "install.py"),
                            "--client", "devin-desktop", "--root", root, "--list-skills"],
                           capture_output=True, text=True)
        ausgabe = (p.stdout or "") + (p.stderr or "")

        gefuehrt = "sonde-d41-projektskill" in ausgabe
        herkunft = bool(re.search(r"sonde-d41-projektskill\s+Projekt\s+nur Nutzer", ausgabe))
        melde("SONDE", "D41", gefuehrt and herkunft,
              "Skill ohne Kernquelle: gefuehrt, Herkunft 'Projekt', Aufrufbarkeit gelesen")
        if not (gefuehrt and herkunft):
            print("        Ausgabe:", " | ".join(ausgabe.splitlines()[:8]))

        melde("GEGENPROBE", "D41", "sonde-d41-kein-skill" not in ausgabe,
              "Verzeichnis ohne SKILL.md wird nicht als Skill gefuehrt")

        melde("SONDE", "D41", "kein vollstaendiger Ersatz" in ausgabe,
              "Die Auskunft nennt ihre eigene Grenze in der Ausgabe")
    finally:
        shutil.rmtree(os.path.dirname(root), ignore_errors=True)


sonde_list_skills()


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


def installation(pack: str) -> str:
    """Frische Installation eines Packs samt Kern - das Ziel der Aktivierungspruefung."""
    ziel = tempfile.mkdtemp(prefix="lw-inst-")
    root = os.path.join(ziel, "projekt")
    os.makedirs(root)
    subprocess.run([sys.executable, os.path.join(QUELLE, "leitwerk-core", "install.py"),
                    "--client", pack, "--root", root], capture_output=True, text=True)
    shutil.copytree(os.path.join(QUELLE, "leitwerk-core"),
                    os.path.join(root, "leitwerk-core"),
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "out"))
    return root


def strict_ausgabe(root: str) -> str:
    """Ausgabe der Aktivierungspruefung - ausdruecklich als UTF-8.

    Ohne PYTHONIOENCODING schreibt der Unterprozess unter Windows in der
    Konsolenkodierung; ein Diagnosetext mit Umlaut kommt dann veraendert zurueck und
    trifft keinen Suchtext mehr. Eine Gegenprobe auf "nicht enthalten" besteht das
    klaglos - sie ist dann wertlos, ohne es zu zeigen. Aufgefallen ist es nur, weil
    die zugehoerige Sonde denselben Text sucht und fiel.
    """
    umgebung = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                        "--root", root, "--strict-overlay"],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=umgebung)
    return (p.stdout or "") + (p.stderr or "")


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
            man = json.loads(lies(os.path.join(QUELLE, "leitwerk-core", "clients", pack,
                                               "manifest.json")))
            regel = os.path.join(root, *man["pack_runtime_dir"].split("/"),
                                 "20-project-overlay.md")
            rechte = os.path.join(root, *man["permissions_file"].split("/"))
            overlay = os.path.join(root, "project-overlay", "OVERLAY.md")

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

            schreib(rechte, lies(rechte).replace(
                '"permissions"', '"_sonde": "<TBD: offen>",\r\n  "permissions"', 1))
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
            shutil.rmtree(os.path.dirname(root), ignore_errors=True)


sonden_aktivierungspruefung()


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
            werkzeug = os.path.join(root, "leitwerk-core", "install.py")

            p = subprocess.run([sys.executable, werkzeug, "--update", "--root", root],
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace")
            aus = (p.stdout or "") + (p.stderr or "")
            getroffen = f"Client:  {pack}" in aus
            keine_zweite = not os.path.isdir(os.path.join(root, fremd))
            melde("SONDE", "B10", getroffen and keine_zweite,
                  f"Aktualisierung ohne --client trifft das installierte Pack ({pack})")
            if not (getroffen and keine_zweite):
                print("        Ausgabe:", " | ".join(aus.splitlines()[:6]))

            anderes = "devin-desktop" if pack == "claude-code" else "claude-code"
            q = subprocess.run([sys.executable, werkzeug, "--update", "--root", root,
                                "--client", anderes],
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace")
            abgewiesen = q.returncode == 1
            unberuehrt = not os.path.isdir(os.path.join(root, fremd))
            melde("GEGENPROBE", "B10", abgewiesen and unberuehrt,
                  f"Widersprechendes --client bricht ab statt anzulegen ({pack} statt {anderes})")
        finally:
            shutil.rmtree(os.path.dirname(root), ignore_errors=True)


sonden_clientwahl()


print()
print("Ergebnis:", "alle Sonden und Gegenproben bestanden" if not fehler
      else f"{fehler} Abweichung(en)")
sys.exit(1 if fehler else 0)

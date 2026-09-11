#!/usr/bin/env python3
"""Wirkungsnachweis nach D-23 fuer die Pruefungen 18 bis 24 (Release 0.26.0).

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
import io
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
        praeparieren(root)
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
            praeparieren(root)
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
                        .replace("Ein Kommentar erreicht die Sitzung nicht",
                                 "Diese Datei darf nur über den Änderungsprozess geändert werden. "
                                 "Ein Kommentar erreicht die Sitzung nicht", 1)),
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

print()
print("Ergebnis:", "alle Sonden und Gegenproben bestanden" if not fehler
      else f"{fehler} Abweichung(en)")
sys.exit(1 if fehler else 0)

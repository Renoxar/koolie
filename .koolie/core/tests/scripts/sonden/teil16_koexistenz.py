"""Sonden zur Koexistenz mit fremden Agenten-Rahmenwerken (1.21.0): die Deklaration fremder
Skills und ihre Grenze (Pruefung 111, K-31), der Korb, den Pruefung 72 weiter verlangt, und
die Auskunft von install.py.

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul liest
nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import json
import os
import sys

from .apparat import (
    aufraeumen, buendel, installation, lies, melde, Praeparationsfehler, schreib, unterprozess,
    validator_ausgabe)

# Nachgebildet nach OpenSpec 1.13.2 (gemessen 2026-09-30): Frontmatter mit Feldern, die
# Koolie nicht kennt, keine Metadatenzeilen, keine Testblaetter. SYNTHETISCH.
FREMDER_SKILL = ("---\nname: openspec-explore\ndescription: Explore ideas before a change. "
                 "SYNTHETISCH\nlicense: MIT\n---\n\n# Explore\n\nSYNTHETISCH\n")
M111_STRUKTUR = "openspec-explore: EXAMPLES.md fehlt"
M111_OFFEN = "(openspec-*) sind nicht deklariert"
M111_UNZULAESSIG = "das Praefix koennte einen Koolie-Skill treffen"
M111_OHNE = "eine Deklaration ohne Gegenstand"
M72_FREMD = "der Skill 'openspec-explore' liegt in"
M37_FREMD = "Skill(openspec-*)"
M_AUSKUNFT = "fremdes Agenten-Rahmenwerk neben Koolie"
M_DEKLARIEREN = "fremde_skills: openspec-"
M111_BLOCK = "eines fremden Generators"
M_ABBRUCH = "markierte(n) Block/Bloecke eines fremden Generators"
BLOCK = "\n<!-- OPENSPEC:START -->\nSYNTHETISCH\n<!-- OPENSPEC:END -->\n"


def _manifest(root: str) -> str:
    return os.path.join(root, ".koolie", "project-overlay", "overlay-manifest.yaml")


def _deklarieren(root: str, wert: str, urstand: str) -> None:
    schreib(_manifest(root), urstand.rstrip("\n") + "\nfremde_skills: %s\n" % wert)


def _install(root: str) -> str:
    p = unterprozess([sys.executable, os.path.join(root, ".koolie", "core", "install.py"),
                      "--client", "claude-code", "--root", root])
    return (p.stdout or "") + (p.stderr or "")


def sonden_fremde_skills() -> None:
    """Pruefung 111 und die Auskunft an einer claude-code-Installation mit einem fremden Skill."""
    root = installation("claude-code")
    try:
        aus = _install(root)
        melde("GEGENPROBE", "111a", M_AUSKUNFT not in aus,
              "Eine Installation ohne fremdes Rahmenwerk - keine Auskunft")
        ablage = os.path.join(root, ".claude", "skills", "openspec-explore")
        os.makedirs(ablage)
        schreib(os.path.join(ablage, "SKILL.md"), FREMDER_SKILL)
        os.makedirs(os.path.join(root, "openspec"))
        schreib(os.path.join(root, "openspec", "config.yaml"), "schema: spec-driven\n")
        aus = _install(root)
        melde("SONDE", "111b", M_AUSKUNFT in aus and M_DEKLARIEREN in aus,
              "install.py erkennt OpenSpec an Ablage und Skill und nennt die Deklaration")
        aus = validator_ausgabe(root)
        melde("SONDE", "111c", M111_STRUKTUR in aus and M111_OFFEN in aus,
              "Ohne Deklaration prueft Pruefung 5 den fremden Skill als Koolie-Skill, und "
              "Pruefung 111 nennt die fehlende Deklaration")
        urstand = lies(_manifest(root))
        _deklarieren(root, "openspec-", urstand)
        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "111d", M111_STRUKTUR not in aus and M111_OFFEN not in aus,
              "Deklariert - Pruefung 5 nimmt ihn aus, Pruefung 111 ist still")
        melde("SONDE", "111e", M72_FREMD in aus,
              "Den Korb verlangt Pruefung 72 weiter (D-238): ein fremder Skill ist ein "
              "Werkzeug der Sitzung wie jeder andere")
        perm = os.path.join(root, ".claude", "settings.json")
        einstellungen = json.loads(lies(perm))
        einstellungen["permissions"]["ask"].append("Skill(openspec-*)")
        schreib(perm, json.dumps(einstellungen, ensure_ascii=False, indent=2) + "\n")
        aus = validator_ausgabe(root)
        melde("GEGENPROBE", "111f", M72_FREMD not in aus and M37_FREMD not in aus,
              "Skill(openspec-*) im ask-Korb deckt den deklarierten Skill und gilt nicht "
              "als Ausweitung")
        _deklarieren(root, "koolie-, speckit-", urstand)
        testblatt = os.path.join(root, ".claude", "skills", "koolie-plan", "TESTS.md")
        if not os.path.isfile(testblatt):
            raise Praeparationsfehler("koolie-plan/TESTS.md fehlt in der Installation")
        os.remove(testblatt)
        aus = validator_ausgabe(root)
        melde("SONDE", "111g", M111_UNZULAESSIG in aus and "koolie-plan: TESTS.md fehlt" in aus,
              "'koolie-' als fremdes Praefix wird gemeldet und nimmt nichts aus - der Koolie-Skill "
              "bleibt geprueft")
        melde("SONDE", "111h", M111_OHNE in aus,
              "Ein deklariertes Praefix ohne Skill ('speckit-') wird gemeldet")
        wurzel = os.path.join(root, "CLAUDE.md")
        schreib(wurzel, lies(wurzel) + BLOCK)
        aus = validator_ausgabe(root)
        melde("SONDE", "111i", M111_BLOCK in aus,
              "Pruefung 111 warnt vor dem markierten Block eines Generators in der "
              "Wurzel-Anweisung (Budget, K-185)")
        p = unterprozess([sys.executable, os.path.join(root, ".koolie", "core", "install.py"),
                          "--client", "claude-code", "--root", root, "--update"])
        melde("SONDE", "111j", p.returncode != 0 and M_ABBRUCH in (p.stdout or "") + (p.stderr or "")
              and BLOCK.strip() in lies(wurzel),
              "install.py --update bricht vor dem Block ab, statt ihn mit der Wurzel-Anweisung "
              "zu ueberschreiben - und der Block bleibt stehen (D-515)")
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_fremde_skills,
        "Pruefung 111 und die Auskunft zu fremden Rahmenwerken an einer claude-code-"
        "Installation: sieben Sonden, drei Gegenproben")

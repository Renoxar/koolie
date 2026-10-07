"""Sonden zur Umbenennung der mitgelieferten Skills auf koolie-* (2.0.0): install.py --update
stellt ein Projekt mit den Namen bis 1.25.0 um - Skillordner, Agentenprofil, Berechtigungsdatei.

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul liest
nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import os
import re
import shutil
import sys

from .apparat import (
    aufraeumen, buendel, installation, lies, melde, schreib, unterprozess, validator_ausgabe)

KERN = ("bugfix-prepare", "change-analyze", "change-small", "code-explain", "docs-update",
        "error-analyze", "mr-description", "overlay-pflege", "plan", "refactor",
        "repo-analyze", "review-support", "tests")
M_MIGRATION = "Seit 2.0.0 heissen die mitgelieferten Skills koolie-*"
M_OVERLAY = "Im Overlay stehen noch alte Namen"


def _alt(text: str) -> str:
    """Ein Text mit den Namen bis 1.25.0 - so sah ein Projekt vor 2.0.0 aus."""
    text = re.sub(r"koolie-(" + "|".join(KERN) + r"|reviewer)(?![a-z0-9-])", r"fw-\1", text)
    return text.replace("koolie-ticket", "role-re-ticket")


def _update(root: str, *mehr: str) -> str:
    p = unterprozess([sys.executable, os.path.join(root, ".koolie", "core", "install.py"),
                      "--client", "claude-code", "--root", root, "--update", *mehr])
    return (p.stdout or "") + (p.stderr or "")


def sonden_skillnamen() -> None:
    """install.py --update an einer claude-code-Installation mit den Namen bis 1.25.0."""
    root = installation("claude-code")
    try:
        skills = os.path.join(root, ".claude", "skills")
        agents = os.path.join(root, ".claude", "agents")
        perm = os.path.join(root, ".claude", "settings.json")
        overlay = os.path.join(root, ".koolie", "project-overlay", "OVERLAY.md")
        quelle = os.path.join(root, ".koolie", "core", "framework", "role-packs",
                              "requirements-engineering", "skills", "koolie-ticket")
        # Der Stand vor 2.0.0: alte Ordner, altes Profil, Pack-Skill aktiviert, alte Regeln.
        for n in KERN:
            os.rename(os.path.join(skills, f"koolie-{n}"), os.path.join(skills, f"fw-{n}"))
        shutil.copytree(quelle, os.path.join(skills, "role-re-ticket"))
        os.rename(os.path.join(agents, "koolie-reviewer.md"), os.path.join(agents, "fw-reviewer.md"))
        rechte = lies(perm).replace('"Skill(koolie-plan)"',
                                    '"Skill(koolie-plan)",\n      "Skill(koolie-ticket)"', 1)
        schreib(perm, _alt(rechte))
        schreib(overlay, lies(overlay) + "\nVor jeder Aenderung /fw-plan. SYNTHETISCH\n")
        vorher = lies(perm)

        aus = _update(root, "--dry-run")
        melde("GEGENPROBE", "D539a", M_MIGRATION in aus and lies(perm) == vorher
              and os.path.isdir(os.path.join(skills, "fw-plan")),
              "--update --dry-run nennt die Umbenennung und schreibt nichts")

        aus = _update(root)
        alt_ordner = [d for d in os.listdir(skills) if d.startswith(("fw-", "role-"))]
        melde("SONDE", "D539b", M_MIGRATION in aus and not alt_ordner
              and all(os.path.isdir(os.path.join(skills, f"koolie-{n}")) for n in KERN),
              "--update benennt die dreizehn Kernskills um und laesst keinen alten Ordner stehen")
        ticket = os.path.join(skills, "koolie-ticket", "SKILL.md")
        melde("SONDE", "D539c", os.path.isfile(ticket) and "name: koolie-ticket" in lies(ticket),
              "Der aktivierte Pack-Skill bleibt aktiviert und traegt den neuen Inhalt")
        melde("SONDE", "D539d", not os.path.exists(os.path.join(agents, "fw-reviewer.md"))
              and os.path.isfile(os.path.join(agents, "koolie-reviewer.md")),
              "Das alte Agentenprofil ist entfernt, das neue angelegt")
        rechte = lies(perm)
        melde("SONDE", "D539e", "fw-" not in rechte and "role-re-ticket" not in rechte
              and "Skill(koolie-plan)" in rechte and "Skill(koolie-ticket)" in rechte,
              "Die Berechtigungsdatei nennt die Skills unter ihrem neuen Namen, auch den "
              "aktivierten Pack-Skill")
        melde("SONDE", "D539f", M_OVERLAY in aus and "OVERLAY.md" in aus
              and "/fw-plan" in lies(overlay),
              "Ein alter Name im Overlay wird genannt, nicht ersetzt - das Overlay gehoert "
              "dem Projekt")
        aus_val = validator_ausgabe(root)
        melde("SONDE", "D539g", "fw-" not in aus_val and "role-re-ticket" not in aus_val
              and "koolie-ticket" not in aus_val,
              "Der Validator findet nach der Migration keinen Skill ohne Korb und keinen "
              "alten Namen")
        aus = _update(root)
        melde("GEGENPROBE", "D539h", M_MIGRATION not in aus,
              "Ein zweites --update hat nichts mehr umzubenennen")
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_skillnamen,
        "Die Umbenennung auf koolie-* durch install.py --update an einer claude-code-"
        "Installation mit den Namen bis 1.25.0: sechs Sonden, zwei Gegenproben")

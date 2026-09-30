# -*- coding: utf-8 -*-
"""Fremde Agenten-Rahmenwerke im Projekt erkennen - Auskunft, keine Schranke (1.21.0, K-31).

ANLASS. `K-31` fragte seit 2026-09-12, wie ein Projekt Koolie aufnimmt, das bereits ein anderes
Agenten-Rahmenwerk fuehrt. Die Sorge war die Wurzel-Anweisung: ein Generator, der seine
Abschnitte in `CLAUDE.md` schreibt und beim naechsten Lauf zurueckschreibt. GEMESSEN am
2026-09-30 an zwei verbreiteten Rahmenwerken (OpenSpec 1.13.2, GitHub Spec Kit): Keines schreibt
beim Anlegen in die Wurzel-Anweisung, keines aendert eine Datei von Koolie - in beiden
Reihenfolgen, auch nicht mit `openspec update --force`. Beide legen ihre Skills in DIESELBE
Ablage wie Koolie (`.claude/skills/openspec-*`, `.claude/skills/speckit-*`), dazu eine eigene
Ablage (`openspec/`, `.specify/`).

Die Reibung liegt deshalb nicht in der Wurzel-Anweisung, sondern im geteilten Namensraum:
Der Validator prueft jeden Skill der Laufzeitablage nach den Regeln fuer Koolie-Skills und
meldete fuer sechs OpenSpec-Skills 60 Fehler und 18 Warnungen. Die Abgrenzung nach Gegenstand
(D-478) heisst hier: Das Projekt DEKLARIERT die fremden Skills im Overlay-Manifest

    fremde_skills: openspec-, speckit-

und der Validator prueft sie dann nicht mehr als Koolie-Skills - die Zuordnung zu einem Korb
der Berechtigungsdatei (D-238) verlangt er weiter: Ein fremder Skill ist ein Werkzeug der
Sitzung wie jeder andere.

Ein Generator, der doch in die Wurzel-Anweisung schreibt, wird an seinen Markierungen erkannt
(`<!-- NAME:START -->` ... `<!-- NAME:END -->`). 🔴 GEMESSEN am selben Tag: Dann ist KOOLIE der
Generator, der zurueckschreibt - `install.py --update` schrieb die Wurzel-Anweisung neu, und
der Block ging ohne Meldung verloren. Seither bricht die Aktualisierung davor ab (D-515), und
Pruefung 111 warnt vorher; der Block zaehlt ausserdem ins Budget (Pruefung 4, `K-185`).
"""
from __future__ import annotations

import io
import os
import re

# Gemessen am 2026-09-30 (CR-2026-167). Ein Eintrag, der hier fehlt, faellt ueber seine
# Markierungen oder als Skill ohne Koolie-Praefix auf - er wird nicht geraten.
BEKANNT = (
    {"name": "OpenSpec", "praefix": "openspec-",
     "spuren": ("openspec/config.yaml", "openspec/project.md", ".claude/commands/opsx",
                ".agents/skills/.openspec-target")},
    {"name": "GitHub Spec Kit", "praefix": "speckit-",
     "spuren": (".specify/integration.json", ".specify/memory/constitution.md")},
)
KOOLIE_PRAEFIX_RE = re.compile(r"^(fw|prj|role-[a-z0-9]+|tech-[a-z0-9]+)-")
MARKE_RE = re.compile(
    r"<!--\s*([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(?:START|BEGIN)\s*-->(.*?)<!--\s*\1\s*:\s*END\s*-->",
    re.S | re.I)
MANIFEST_REL = ".koolie/project-overlay/overlay-manifest.yaml"
DEKLARATION_RE = re.compile(r"^fremde_skills:[ \t]*([^#\r\n]*)", re.M)


def _lies(pfad: str) -> str:
    try:
        return io.open(pfad, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def deklariert(root: str) -> list:
    """Die Praefixe aus 'fremde_skills:' im Overlay-Manifest - leer, wenn nichts gesagt ist."""
    m = DEKLARATION_RE.search(_lies(os.path.join(root, *MANIFEST_REL.split("/"))))
    if not m:
        return []
    return [p.strip().strip("\"'") for p in m.group(1).split(",") if p.strip().strip("\"'")]


KOOLIE_PRAEFIXE = ("fw-", "prj-", "role-", "tech-")


def zulaessig(praefix: str) -> bool:
    """Ein Praefix, das einen Koolie-Skill treffen koennte, nimmt nichts aus (Pruefung 111).

    Sonst waere die Deklaration ein Weg, die eigenen Skills der Pruefung zu entziehen.
    """
    p = praefix.strip()
    return len(p) >= 3 and not any(k.startswith(p) or p.startswith(k) for k in KOOLIE_PRAEFIXE)


def ist_deklariert(name: str, praefixe) -> bool:
    return any(zulaessig(p) and name.startswith(p) for p in praefixe)


def fremde_skills(root: str, skills_dir: str) -> list:
    """Skills der Laufzeitablage ohne Koolie-Praefix, sortiert."""
    ablage = os.path.join(root, *skills_dir.split("/"))
    if not os.path.isdir(ablage):
        return []
    return sorted(n for n in os.listdir(ablage)
                  if os.path.isdir(os.path.join(ablage, n)) and not KOOLIE_PRAEFIX_RE.match(n))


def markierte_bloecke(text: str) -> list:
    """(Name, Zeichen) je markiertem Block eines Generators in einer Anweisungsdatei."""
    return [(m.group(1), len(m.group(0))) for m in MARKE_RE.finditer(text)]


def erkennen(root: str, skills_dir: str) -> list:
    """Je erkanntem Rahmenwerk ein Befund: name, spuren, skills, praefix."""
    fremd = fremde_skills(root, skills_dir)
    befunde = []
    for r in BEKANNT:
        spuren = [s for s in r["spuren"] if os.path.exists(os.path.join(root, *s.split("/")))]
        skills = [s for s in fremd if s.startswith(r["praefix"])]
        if spuren or skills:
            befunde.append({"name": r["name"], "spuren": spuren, "skills": skills,
                            "praefix": r["praefix"]})
    bekannt = {s for b in befunde for s in b["skills"]}
    rest = [s for s in fremd if s not in bekannt]
    if rest:
        befunde.append({"name": "unbekannt", "spuren": [], "skills": rest, "praefix": ""})
    return befunde

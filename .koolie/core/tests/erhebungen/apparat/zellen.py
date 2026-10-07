# -*- coding: utf-8 -*-
"""Die Zellen der Sitzungstests als Daten: Skill, Basis, Praeparationen, Historie (K-190).

Je Zelle (Baumname wie bisher, `sk003p04`):
  skill     der gemessene Skill
  basis     Name in basen.BASEN
  praep     Praeparationen VOR dem ersten Commit (liegen in der Historie)
  historie  None (ein Commit) oder ein Eintrag fuer historie.mit_branches
  status    erwartete Zeilen von `git status --porcelain` (Aenderungen in der Arbeitskopie)

Uebernommen aus den Aufbauwegen der letzten Messung je Zelle:
  SK-001, SK-002              Buendel 1 (aufbau-1140.py, Basis b12 = b0)
  SK-003, SK-004, SK-009      aufbau-2100.py (Nachlauf 2.1.0)
  SK-004-P04, SK-007-N07      aufbau-2100-b4.py; N07 mit der Praeparation aus dem Baum sk007n07b
  SK-005, SK-007              aufbau-1141.py (Basis b3)
  SK-006, SK-008              baeume-b23.py
  SK-010, SK-011, SK-012      aufbau-2100-b4.py mit historie-bauen-b4.py
  SK-013                      aufbau-1203.py
Nicht hier: SK-007-N06 (geprueft am Text, kein Messbaum), die Kontrollbaeume der Klassen aus
k-bauen-b3.py und Buendel 5 (RE-001, Role Pack aktiviert - umgebungen-bauen-b5.py).
"""
from __future__ import annotations

ZELLEN: dict = {}


def _zelle(namen, skill, basis, **mehr):
    for n in namen.split():
        ZELLEN[n] = dict(skill=skill, basis=basis, praep=[], historie=None, status=[])
        ZELLEN[n].update({k: (list(v) if isinstance(v, list) else v) for k, v in mehr.items()})


_zelle("sk001p01 sk001p02 sk001n01 sk001n02 sk001n03", "koolie-repo-analyze", "b0")
_zelle("sk002p01 sk002p02 sk002n01 sk002n02 sk002n03", "koolie-code-explain", "b0")
_zelle("sk003p01 sk003p02 sk003p03 sk003n01 sk003n02 sk003n03", "koolie-change-analyze", "b0")
_zelle("sk003p04 sk003p05 sk003n04 sk003n05", "koolie-change-analyze", "bR")
_zelle("sk004p01 sk004p02 sk004p04 sk004n01 sk004n02 sk004n03 sk004n04", "koolie-plan", "b0")
_zelle("sk004p03 sk004n05", "koolie-plan", "bR")
_zelle("sk005p01 sk005p02 sk005n01 sk005n02 sk005n03 sk005n04 sk005n05", "koolie-change-small", "b3")
_zelle("sk006p01 sk006p02 sk006n01 sk006n03 sk006n04", "koolie-tests", "b3")
_zelle("sk006n02", "koolie-tests", "b3", praep=["ueb08"])
_zelle("sk007p02 sk007n01 sk007n03 sk007n04", "koolie-refactor", "b3")
_zelle("sk007p01", "koolie-refactor", "b3", praep=["ueb32"])
_zelle("sk007n02", "koolie-refactor", "b3", praep=["ueb08"])
_zelle("sk007n05", "koolie-refactor", "b3", praep=["kommentar-leihliste"])
_zelle("sk007n07", "koolie-refactor", "b0t", praep=["stufe-hoch"])
_zelle("sk008p01 sk008p02 sk008n01 sk008n02 sk008n03 sk008n04", "koolie-error-analyze", "b2")
_zelle("sk009p01 sk009p02 sk009n01 sk009n02 sk009n03 sk009n04", "koolie-bugfix-prepare", "b0")
_zelle("sk009n05 sk009n06", "koolie-bugfix-prepare", "bR")
_zelle("sk009p03", "koolie-bugfix-prepare", "bRK")
_zelle("sk011p01 sk011p02 sk011n01 sk011n02 sk011n03 sk011n04", "koolie-docs-update", "b4")
_zelle("sk013p01 sk013p03 sk013n01 sk013n02 sk013n03 sk013n04", "koolie-overlay-pflege", "b13")
_zelle("sk013p02", "koolie-overlay-pflege", "b13", praep=["abschnitt6-offen"])

# Branch-Zellen von Buendel 4 (historie-bauen-b4.py, ZELLEN)
_B34 = "uebung/biv-34-offene-ausleihen"
_B31 = "uebung/biv-31-sortierung"
_BERICHTE = ["ueb24", "ueb25-umsetzung", "ueb25-tests"]
_HISTORIE = {
    "sk012p01": dict(branches=[_B34], auf=_B34, dokumente=_BERICHTE),
    "sk012p02": dict(branches=[_B34], auf=_B34, dokumente=["ueb24"]),
    "sk012n01": dict(branches=[_B34], auf=_B34, dokumente=_BERICHTE),
    "sk012n02": dict(branches=["uebung/biv-34-formatierung"], auf="uebung/biv-34-formatierung",
                     dokumente=_BERICHTE),
    "sk012n03": dict(branches=["uebung/biv-35-betriebsvorgaben"],
                     auf="uebung/biv-35-betriebsvorgaben", dokumente=_BERICHTE),
    "sk012n04": dict(branches=[_B34], auf=_B34, dokumente=_BERICHTE),
    "sk010p01": dict(branches=[_B31], auf=_B31),
    "sk010p02": dict(dokumente=["ueb26"], arbeitskopie=["biv36-obergrenze", "biv36-zusicherung"]),
    "sk010n01": dict(branches=[_B31], auf=_B31),
    # Die zweite Haelfte kommt aus UEB-29, nicht aus UEB-02 (D-220).
    "sk010n02": dict(praeparationen=["ueb29"], arbeitskopie=["n02-deploy"]),
    "sk010n03": dict(branches=["uebung/biv-34-geprueft"], auf="uebung/biv-34-geprueft",
                     dokumente=["ueb24"]),
    # auf=None mit Absicht: Gegenstand ist die mehrdeutige Basis.
    "sk010n04": dict(branches=[_B31, _B34]),
    "sk010n05": dict(branches=["uebung/biv-33-rollenpruefung"], auf="uebung/biv-33-rollenpruefung"),
}
_STATUS = {
    "sk010p02": [" M frontend/src/api/validierung.test.ts", " M frontend/src/api/validierung.ts"],
    "sk010n02": [" M deploy/betrieb.properties", "?? frontend/src/api/meldedienst.ts"],
}
for _k, _h in _HISTORIE.items():
    _skill = "koolie-mr-description" if _k.startswith("sk012") else "koolie-review-support"
    _zelle(_k, _skill, "b4", historie=_h, status=_STATUS.get(_k, []))


def auswahl(angabe: str) -> list:
    """'alle', 'sk003' (Praefix) oder Kommaliste; unbekannte Namen sind ein Abbruch."""
    if angabe == "alle":
        return sorted(ZELLEN)
    aus = []
    for teil in angabe.split(","):
        treffer = sorted(k for k in ZELLEN if k == teil or (len(teil) == 5 and k.startswith(teil)))
        if not treffer:
            raise KeyError(f"unbekannte Zelle {teil}")
        aus += [t for t in treffer if t not in aus]
    return aus

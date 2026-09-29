# -*- coding: utf-8 -*-
"""Die Standmarke einer Ergebniszelle (Pruefung 103, D-472, K-61).

Die Rechnung steht an EINER Stelle - in validate-framework.py, stand_wert() -, und dieses
Modul laedt sie von dort. Eine zweite Rechnung hier waere die Bauform, die der Validator
bei zaehlen46.py schon einmal aufgeloest hat (D-259): zwei Stellen, die auseinanderlaufen,
ohne dass es eine merkt. Die Sonde 103 rechnet bewusst selbst - sie ist die Gegenstelle.
"""
from __future__ import annotations

import importlib.util
import os

from .belege import KERN


def _validator():
    pfad = os.path.join(KERN, "tests", "scripts", "validate-framework.py")
    spec = importlib.util.spec_from_file_location("validate_framework", pfad)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def marke(pfade: list, kern: str = KERN) -> str:
    """'[Stand: ...; pfad, pfad]' ueber die Gegenstandsdateien, Pfade relativ zum Kern."""
    wert = _validator().stand_wert(kern, pfade)
    if wert is None:
        raise RuntimeError("ein Gegenstand fehlt: " + ", ".join(pfade))
    return "[Stand: %s; %s]" % (wert, ", ".join(pfade))

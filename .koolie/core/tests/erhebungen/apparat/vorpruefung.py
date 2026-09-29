# -*- coding: utf-8 -*-
"""Deterministisch vor jedem bezahlten Lauf - Abbruch statt Lauf (K-174, Frage c).

ANLASS, GEZAEHLT: 1.17.0 hat 10 von 40 Laeufen verworfen, alle wegen des Messaufbaus;
0.79.0 fuhr 38 Baeume auf 'main', weil ein Waechter das Vorhandensein des Branches
pruefte und nicht, dass er ausgecheckt war (D-218). Jede dieser Pruefungen kostet nichts
und haette den bezahlten Lauf verhindert.

Die Pruefungen, jede mit ihrem Anlass:
  zustand     Baum-Hash gleich der Basis        - das Zuruecksetzen wird gemessen (D-213)
  head        HEAD auf Sollcommit und -branch   - ein Zustand, kein Vorhandensein (D-218)
  prompt      Prompt und Folgeturns nicht leer  - Abbruch statt Rueckfall (1.14.2)
  kontingent  Deckel mit Reserve frei            - Falle 8 aus 1.17.0
  vertrauen   Vertrauenseintrag des Baums        - ohne ihn laedt die Projektschicht nicht (K-118)
  hook        Schutz-Hook sperrt ein Leseereignis auf .env - der Hook laeuft, BEVOR bezahlt wird
  werkzeuge   die Startmeldung nennt die gesagten Werkzeuge (optional, 1.18.2)
"""
from __future__ import annotations

from . import baum as baum_mod
from . import kontingent
from .clients import Unerhoben


def pruefen(reihe, lauf, adapter, soll: dict, baumpfad: str, basis: str = "") -> list:
    """Alle Befunde fuer genau diesen Lauf - eine leere Liste heisst: fahren."""
    b = []
    ohne = reihe.baum.get("ohne") or []
    if soll.get("hash"):
        ist = baum_mod.baumhash(baumpfad, ohne)
        if ist != soll["hash"]:
            b.append(f"zustand: Baum-Hash {ist} statt {soll['hash']} - der Baum traegt einen "
                     f"Rest (D-213)")
    if soll.get("commit"):
        commit = baum_mod.git(baumpfad, "rev-parse", "HEAD", pruefen=False)
        if commit != soll["commit"]:
            b.append(f"head: HEAD {commit[:10]} statt {soll['commit'][:10]}")
    zweig = lauf.ziel_branch(reihe)
    ist_zweig = baum_mod.git(baumpfad, "symbolic-ref", "--short", "HEAD", pruefen=False)
    if ist_zweig != zweig:
        b.append(f"head: Branch '{ist_zweig}' statt '{zweig}' (D-218, K-172)")
    if not lauf.prompt.strip() or any(not t.strip() for t in lauf.folgeturns):
        b.append("prompt: leer")
    grund = kontingent.frei(reihe.belege, reihe.max_laeufe, reihe.max_usd, reihe.reserve_usd)
    if grund:
        b.append("kontingent: " + grund)
    if reihe.vorpruefung.get("vertrauen"):
        try:
            if not adapter.vertrauen_gesetzt(baumpfad):
                b.append("vertrauen: kein Eintrag fuer diesen Baum (K-118)")
        except Unerhoben as e:
            b.append(f"vertrauen: nicht pruefbar ({e}) - in der Reihe abschalten, wenn gewollt")
    if reihe.vorpruefung.get("hook"):
        try:
            befund = adapter.hook_probe(baumpfad)
            if befund:
                b.append("hook: " + befund)
        except Unerhoben as e:
            b.append(f"hook: nicht pruefbar ({e}) - in der Reihe abschalten, wenn gewollt")
    erwartet = reihe.vorpruefung.get("startmeldung") or []
    if erwartet:
        try:
            werkzeuge = adapter.startmeldung(baumpfad)
            fehlt = [w for w in erwartet if w not in werkzeuge]
            if fehlt:
                b.append(f"werkzeuge: die Startmeldung nennt {', '.join(fehlt)} nicht (D-470)")
        except (Unerhoben, RuntimeError) as e:
            b.append(f"werkzeuge: nicht pruefbar ({e})")
    return b

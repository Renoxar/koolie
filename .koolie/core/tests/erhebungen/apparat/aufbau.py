# -*- coding: utf-8 -*-
"""Messbaeume bauen: Marke -> Basis -> je Zelle Kopie, Praeparation, Historie (K-190).

    python messen.py baeume ZELLEN [--node PFAD] [--anhang b]

ZELLEN ist `alle`, ein Praefix (`sk003`) oder eine Kommaliste. Der Messort kommt aus
`LW_BASIS` (oder `LW_MESSWURZEL/lw-<kennung>` mit `--kennung`); ein bestehender Baum wird nie
ueberschrieben. Je Lauf ein Baum, wie bisher: Die Skills schreiben (oder duerfen es nicht) und
werden daran gemessen.
"""
from __future__ import annotations

import json
import os
import re

from . import basen, historie, praeparationen, quelle, zellen
from .quelle import Abbruch, lies

AUFZEICHNUNGEN = (".koolie/core/tests/protocols/", ".koolie/core/tests/erhebungen/",
                  ".koolie/core/governance/change-requests/", ".devin/", "tools/")


def baum_pruefen(name: str, z: dict, baum: str) -> str:
    for pflicht in (".claude/settings.json", "CLAUDE.md", ".git"):
        if not os.path.exists(os.path.join(baum, *pflicht.split("/"))):
            raise Abbruch(f"{pflicht} fehlt in {name}")
    status = [s for s in historie.git(baum, "status", "--porcelain").splitlines() if s.strip()]
    if sorted(status) != sorted(z["status"]):
        raise Abbruch(f"git status in {name} ist {status!r}, erwartet {z['status']!r}")
    historie.waechter_autoren(baum)
    verfolgt = historie.git(baum, "ls-files").splitlines()
    if any(os.path.basename(v) in ("TESTS.md", "TEST_CATALOG.md") or v.startswith(AUFZEICHNUNGEN)
           or v in (".koolie/core/governance/DECISION_LOG.md", "AGENTS.md") for v in verfolgt):
        raise Abbruch(f"{name} fuehrt Aufzeichnungen, tools/ oder .devin/ (D-425)")
    if z["skill"] not in os.listdir(os.path.join(baum, ".claude", "skills")):
        raise Abbruch(f"Skill {z['skill']} fehlt in {name}")
    p = json.loads(lies(os.path.join(baum, ".claude", "settings.json")))["permissions"]
    korb = next((k for k in ("allow", "ask") if "Skill(%s)" % z["skill"] in p[k]), None)
    if korb is None:
        raise Abbruch(f"Skill({z['skill']}) in keinem Korb")
    if os.path.exists(os.path.join(baum, ".git", "koolie-mandat.json")):
        raise Abbruch(f"{name} traegt schon ein Mandat")
    for rel in (".koolie/project-overlay/OVERLAY.md", ".claude/rules/20-project-overlay.md",
                ".mcp.json"):
        pfad = os.path.join(baum, *rel.split("/"))
        if os.path.exists(pfad):
            m = re.search(r"UEB-\d\d|\b(SK|RE)-\d{3}-[PN]\d\d\b|KOOL-\d", lies(pfad))
            if m:
                raise Abbruch(f"{rel} in {name} nennt {m.group(0)} (Regel 4)")
    return f"{len(verfolgt)} verfolgt, Skill in {korb}"


def zelle_bauen(name: str, ort: str, basis: str, nm: str, anhang: str = "") -> str:
    z = zellen.ZELLEN[name]
    baum = os.path.join(ort, name + anhang)
    if os.path.lexists(baum):
        raise Abbruch(f"{baum} existiert schon - der Aufbau ueberschreibt keinen Messbaum")
    basen.kopieren(basis, baum)
    for kennung in z["praep"]:
        praeparationen.setzen(baum, kennung)
    if z["historie"]:
        historie.mit_branches(baum, z["historie"])
    else:
        historie.minimal(baum)
    if basen.BASEN[z["basis"]].get("node") and nm:
        basen.node_verbinden(baum, nm)
    befund = baum_pruefen(name, z, baum)
    kopf = historie.git(baum, "rev-parse", "--abbrev-ref", "HEAD")
    return f"{name + anhang:10} basis-{z['basis']:4} HEAD {kopf:32} {befund}" + (
        f", Praeparation {'+'.join(z['praep'])}" if z["praep"] else "")


def bauen(angabe: str, ort: str, nm: str = "", anhang: str = "") -> list:
    namen = zellen.auswahl(angabe)
    if anhang and not anhang.isalpha():
        raise Abbruch(f"--anhang {anhang!r} ist kein Buchstabenanhang")
    for n in namen:
        if os.path.lexists(os.path.join(ort, n + anhang)):
            raise Abbruch(f"{os.path.join(ort, n + anhang)} existiert schon")
    braucht_node = any(basen.BASEN[zellen.ZELLEN[n]["basis"]].get("node") for n in namen)
    if braucht_node and not (nm and os.path.isdir(nm)):
        raise Abbruch("diese Zellen brauchen einen node_modules-Bestand (--node PFAD)")
    os.makedirs(ort, exist_ok=True)
    archiv = quelle.archiv(ort)
    gebaut = {}
    aus = []
    for n in namen:
        b = zellen.ZELLEN[n]["basis"]
        if b not in gebaut:
            gebaut[b] = basen.bauen(b, ort, archiv, nm)
        aus.append(zelle_bauen(n, ort, gebaut[b], nm, anhang))
        print(aus[-1])
    return aus

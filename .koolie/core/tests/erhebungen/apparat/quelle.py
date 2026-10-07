# -*- coding: utf-8 -*-
"""Woher ein Messbaum kommt: Messort, Basisarchiv aus einer festen Marke, Kerntausch (K-190).

DIE MARKE STATT HEAD. Bis 2.1.0 nahm jedes Aufbauskript `git archive HEAD` des
Uebungsrepositoriums und pruefte einen Sollcommit, der im Skript stand und je Release
nachgezogen wurde. Jetzt ist die Basis eine Marke im Uebungsrepositorium; ihr Commit steht
hier und wird geprueft. Eine neue Marke ist eine bewusste Entscheidung mit eigenem
Gleichwertigkeitsnachweis, kein Nebeneffekt eines Commits in der Uebung.

WOHER DIE UEBUNG KOMMT. `LW_UEBUNG_QUELLE` (Adresse eines Spiegels) hat Vorrang: Der
Apparat klont dann einmal nackt in den Messort. Sonst `LW_UEBUNG`, ein vorhandener Klon.

DER KERN KOMMT AUS DIESEM ARBEITSBAUM, ueber den Weg eines Projekts: `install.py --target
<archiv> --update`. Er nimmt nur Verfolgtes - was gemessen werden soll, ist committet.

DER MESSORT wird gesagt (`LW_BASIS`, sonst `LW_MESSWURZEL/lw-<kennung>`) und liegt weder unter
dem Benutzerprofil (der Client laedt dort abgelegte Anweisungsdateien mit) noch in einem der
beiden Repositorien.
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
ERHEBUNGEN = os.path.dirname(HIER)
KERN = os.path.dirname(os.path.dirname(ERHEBUNGEN))
WURZEL = os.path.dirname(os.path.dirname(KERN))

MARKE = "apparat-basis-1"
MARKE_COMMIT = "c2d7587d73d717e970b9f4f8ae8112a6fd7f8137"   # Uebung 1.4.40, Framework 2.1.0
STAND = "basis-archiv.stand.json"


class Abbruch(RuntimeError):
    pass


def lauf(befehl, cwd=None, pruefen=True, env=None):
    umg = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    umg.update(env or {})
    p = subprocess.run(befehl, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=umg)
    if pruefen and p.returncode != 0:
        raise Abbruch(f"{befehl!r} -> Exit {p.returncode}\n{(p.stdout or '')[-2000:]}"
                      f"\n{(p.stderr or '')[-2000:]}")
    return (p.stdout or "") + (p.stderr or "")


def innerhalb(pfad: str, wurzel: str) -> bool:
    pfad, wurzel = os.path.realpath(pfad), os.path.realpath(wurzel)
    try:
        return os.path.commonpath([pfad, wurzel]) == wurzel
    except ValueError:
        return False


def lies(pfad: str) -> str:
    with io.open(pfad, encoding="utf-8", newline="") as fh:
        return fh.read()


def kernversion() -> str:
    return lies(os.path.join(KERN, "VERSION")).strip()


def messort(kennung: str = "") -> str:
    wert = os.environ.get("LW_BASIS", "").strip().strip('"')
    if not wert:
        wurzel = os.environ.get("LW_MESSWURZEL", "").strip().strip('"')
        if not wurzel or not kennung:
            raise Abbruch("LW_BASIS ist nicht gesetzt (oder LW_MESSWURZEL und eine Kennung)")
        wert = os.path.join(wurzel, "lw-" + kennung)
    wert = os.path.abspath(wert)
    verboten = [WURZEL, os.path.expanduser("~")]
    if os.environ.get("LW_UEBUNG"):
        verboten.append(os.environ["LW_UEBUNG"])
    for v in verboten:
        if innerhalb(wert, v):
            raise Abbruch(f"Messort {wert} liegt unter {v}")
    return wert


def marke() -> tuple:
    """(Name, Commit) - eine abweichende Marke nur ausdruecklich, mit ihrem Commit."""
    name = os.environ.get("LW_UEBUNG_MARKE", MARKE)
    commit = os.environ.get("LW_UEBUNG_MARKE_COMMIT", MARKE_COMMIT if name == MARKE else "")
    if not commit:
        raise Abbruch(f"Marke {name}: LW_UEBUNG_MARKE_COMMIT fehlt")
    return name, commit


def uebung(ort: str) -> str:
    """Das git-Verzeichnis, aus dem archiviert wird."""
    adresse = os.environ.get("LW_UEBUNG_QUELLE", "").strip()
    if adresse:
        nackt = os.path.join(ort, "uebung.git")
        if not os.path.isdir(nackt):
            lauf(["git", "clone", "-q", "--bare", adresse, nackt])
        else:
            lauf(["git", "-C", nackt, "fetch", "-q", "--tags", "origin"])
        return nackt
    wert = os.environ.get("LW_UEBUNG", "").strip().strip('"')
    if not wert or not os.path.isdir(wert):
        raise Abbruch("weder LW_UEBUNG_QUELLE noch ein Verzeichnis in LW_UEBUNG")
    return os.path.abspath(wert)


def kernstand() -> dict:
    """Der committete Kern ohne den Messapparat: Der Schnitt nimmt tests/erhebungen/ aus jedem
    Baum, eine Aenderung am Apparat aendert also kein Archiv."""
    import hashlib
    apparat = ".koolie/core/tests/erhebungen/"
    zeilen = [z for z in lauf(["git", "-C", WURZEL, "ls-tree", "-r", "HEAD", ".koolie/core"])
              .splitlines() if not z.split("\t", 1)[-1].startswith(apparat)]
    offen = [z for z in lauf(["git", "-C", WURZEL, "status", "--porcelain", "--untracked-files=no",
                              ".koolie/core"]).splitlines() if apparat not in z]
    return {"version": kernversion(),
            "baum": hashlib.sha256("\n".join(zeilen).encode("utf-8")).hexdigest()[:16],
            "geaendert": bool(offen)}


def archiv(ort: str) -> str:
    """<ort>/basis-archiv: die Marke, Kern aus diesem Arbeitsbaum. Wird nur wiederverwendet,
    wenn Marke und Kernstand dieselben sind."""
    ziel = os.path.join(ort, "basis-archiv")
    name, commit = marke()
    stand = {"marke": name, "commit": commit, "kern": kernstand()}
    stand_pfad = os.path.join(ort, STAND)
    if os.path.isdir(ziel):
        alt = json.loads(lies(stand_pfad)) if os.path.isfile(stand_pfad) else None
        if alt != stand:
            raise Abbruch(f"{ziel} stammt aus einem anderen Stand ({alt}) - neuer Messort")
        return ziel
    if stand["kern"]["geaendert"]:
        raise Abbruch("der Kern hat uncommittete Aenderungen an verfolgten Dateien - "
                      "install.py --update nimmt den committeten Stand nicht")
    quelle = uebung(ort)
    ist = lauf(["git", "-C", quelle, "rev-parse", name + "^{commit}"]).strip()
    if ist != commit:
        raise Abbruch(f"Marke {name} zeigt auf {ist}, erwartet {commit}")
    os.makedirs(ziel)
    tar = os.path.join(ort, "basis-archiv.tar")
    lauf(["git", "-C", quelle, "archive", "-o", tar, name])
    lauf(["tar", "-xf", tar, "-C", ziel])
    os.remove(tar)
    lauf([sys.executable, "-B", os.path.join(KERN, "install.py"), "--target", ziel, "--update"])
    if lies(os.path.join(ziel, ".koolie", "core", "VERSION")).strip() != kernversion():
        raise Abbruch("Kerntausch nicht gelungen")
    with io.open(stand_pfad, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(stand, indent=1) + "\n")
    return ziel

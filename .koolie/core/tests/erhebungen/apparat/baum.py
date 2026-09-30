# -*- coding: utf-8 -*-
"""Der Messbaum: bauen, herrichten, zuruecksetzen - und sein Zustand als EINE Zahl.

FESTER PFAD STATT NEUER VERZEICHNISSE (K-174, Frage d). Der Client stellt jeder Anfrage
einen Anfang voran, in dem auch das Arbeitsverzeichnis steht. Ein neues Verzeichnis je
Lauf ist ein neuer Anfang - und jeder Lauf legte rund 35.000 Token Cache NEU an (D-436).
Im Modus 'fest' laeuft jede Reihe in DEMSELBEN Verzeichnis, und zwischen zwei Laeufen
wird zurueckgesetzt statt neu kopiert.

DAS ZURUECKSETZEN MUSS VOLLSTAENDIG SEIN - sonst misst der naechste Lauf den vorigen mit
(das Rauschen aus D-213). Deshalb wird es nicht geglaubt, sondern gemessen: baumhash()
ueber jede Datei ausser .git und den genannten Ausnahmen, vor jedem Lauf gegen den Hash
der Basis (vorpruefung.py). Ignorierte Dateien der Basis (.env ist eine) werden aus der
Basis zurueckkopiert; git allein wuerde sie nicht wiederherstellen.
"""
from __future__ import annotations

import hashlib
import os
import shutil
import stat
import subprocess
import sys

AUTOR = ["-c", "user.name=Messung", "-c", "user.email=messung@example.invalid"]


def git(baum: str, *args: str, pruefen: bool = True) -> str:
    p = subprocess.run(["git", "-C", baum, *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if pruefen and p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} in {baum}: {p.stderr.strip()}")
    return p.stdout.strip()


def _ist_verbindung(pfad: str) -> bool:
    """Symlink oder Verzeichnisverbindung (Windows-Junction) - wird nie betreten."""
    if os.path.islink(pfad):
        return True
    try:
        return bool(os.lstat(pfad).st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
    except (AttributeError, OSError):
        return False


def dateien(baum: str, ohne=()) -> list:
    """Alle Dateien relativ zum Baum, sortiert - ohne .git, ohne Ausnahmen, ohne Verbindungen."""
    aus = []
    ausnahmen = {".git", *ohne}
    for wurzel, verz, files in os.walk(baum):
        verz[:] = sorted(d for d in verz
                         if d not in ausnahmen and not _ist_verbindung(os.path.join(wurzel, d)))
        for f in sorted(files):
            voll = os.path.join(wurzel, f)
            if _ist_verbindung(voll):
                continue
            aus.append(os.path.relpath(voll, baum).replace(os.sep, "/"))
    return aus


def baumhash(baum: str, ohne=()) -> str:
    """Pfad und Inhalt jeder Datei - ein Zustand, keine Zaehlung (D-218)."""
    h = hashlib.sha256()
    for rel in dateien(baum, ohne):
        h.update(rel.encode("utf-8") + b"\0")
        with open(os.path.join(baum, *rel.split("/")), "rb") as fh:
            h.update(hashlib.sha256(fh.read()).digest())
    return h.hexdigest()[:16]


def sollstand(basis: str, ohne=()) -> dict:
    return {"commit": git(basis, "rev-parse", "HEAD"),
            "branch": git(basis, "symbolic-ref", "--short", "HEAD"),
            "hash": baumhash(basis, ohne)}


def _schreibschutz_weg(func, pfad, _info) -> None:
    os.chmod(pfad, stat.S_IWRITE)
    func(pfad)


def entfernen(pfad: str) -> None:
    """Loeschen, ohne einer Verzeichnisverbindung in ihr Ziel zu folgen (D-262)."""
    if not os.path.lexists(pfad):
        return
    for wurzel, verz, _ in os.walk(pfad):
        for d in list(verz):
            voll = os.path.join(wurzel, d)
            if _ist_verbindung(voll):
                os.rmdir(voll) if not os.path.islink(voll) else os.unlink(voll)
                verz.remove(d)
    if sys.version_info >= (3, 12):
        shutil.rmtree(pfad, onexc=_schreibschutz_weg)
    else:
        shutil.rmtree(pfad, onerror=_schreibschutz_weg)


def basis_bauen(ziel: str, kern_quelle: str, client: str, praeparation: list) -> dict:
    """Eine frische Installation als git-Baum - fuer Schrankenreihen ohne Uebungsrepositorium.

    Schritte der Praeparation: {"art": "datei", "pfad", "inhalt"} | {"art": "entferne",
    "pfad"} | {"art": "commit", "nachricht"}. Am Ende steht ein Commit 'Basis' mit
    synthetischem Autor; ignorierte Dateien (etwa .env) liegen daneben und gehoeren zum
    Sollstand, weil der Baum-Hash sie mitzaehlt.
    """
    if os.path.exists(ziel):
        raise RuntimeError(f"{ziel} besteht schon - eine Basis wird nicht ueberschrieben")
    os.makedirs(ziel)
    git(ziel, "init", "-q", "-b", "main")
    git(ziel, "config", "core.autocrlf", "false")
    p = subprocess.run([sys.executable, "-B", os.path.join(kern_quelle, "install.py"),
                        "--target", ziel, "--client", client],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(f"install.py --target: Exit {p.returncode}\n{p.stdout[-800:]}\n{p.stderr[-800:]}")
    for schritt in praeparation:
        art = schritt.get("art")
        pfad = os.path.join(ziel, *schritt.get("pfad", "").split("/")) if schritt.get("pfad") else ""
        if art == "datei":
            os.makedirs(os.path.dirname(pfad), exist_ok=True)
            with open(pfad, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(schritt.get("inhalt", ""))
        elif art == "entferne":
            if os.path.isdir(pfad):
                entfernen(pfad)
            elif os.path.exists(pfad):
                os.remove(pfad)
        elif art == "commit":
            git(ziel, "add", "-A")
            git(ziel, *AUTOR, "commit", "-q", "--allow-empty", "-m", schritt.get("nachricht", "Schritt"))
        else:
            raise RuntimeError(f"unbekannter Praeparationsschritt '{art}'")
    git(ziel, "add", "-A")
    git(ziel, *AUTOR, "commit", "-q", "--allow-empty", "-m", "Basis")
    return sollstand(ziel)


def _remote_neu(baum: str, basis: str, hooks: str = "") -> None:
    """Ein Wegwerf-Remote je Baum - ein durchgelassener Push landet dort und nirgends sonst.

    Mit 'hooks' traegt das Remote Branch-Schutz und CI der Referenzgruppe (1.21.0): Die
    Hooks liegen ausserhalb des Messbaums, der Agent erreicht sie nur ueber einen Push.
    """
    remote = baum.rstrip("\\/") + ".remote.git"
    entfernen(remote)
    subprocess.run(["git", "clone", "-q", "--bare", basis, remote], check=True,
                   capture_output=True)
    if hooks:
        for name in sorted(os.listdir(hooks)):
            ziel = os.path.join(remote, "hooks", name)
            shutil.copy2(os.path.join(hooks, name), ziel)
            os.chmod(ziel, 0o755)
    git(baum, "remote", "remove", "origin", pruefen=False)
    git(baum, "remote", "add", "origin", remote)


def verbinden(baum: str, verbindungen: dict) -> None:
    """Verzeichnisverbindungen, die weder Hash noch Zuruecksetzen betreten (1.21.0).

    Der geteilte node_modules-Bestand (node-waechter.py): 118 MB je Baum waeren der Preis
    einer Kopie. Eine vorhandene Verbindung bleibt; ein echtes Verzeichnis an ihrer Stelle
    ist ein Abbruch - es waere ein Rest oder eine Kopie.
    """
    for rel, quelle in (verbindungen or {}).items():
        ziel = os.path.join(baum, *rel.replace("\\", "/").split("/"))
        if os.path.lexists(ziel):
            if _ist_verbindung(ziel):
                continue
            raise RuntimeError(f"{rel} besteht im Baum und ist keine Verbindung")
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        if os.name == "nt":
            subprocess.run(["cmd", "/c", "mklink", "/J", ziel, os.path.abspath(quelle)],
                           check=True, capture_output=True)
        else:
            os.symlink(os.path.abspath(quelle), ziel, target_is_directory=True)


def herrichten(basis: str, baum: str, branch: str, soll: dict, remote: bool, ohne=(),
               verbindungen=None, remote_hooks: str = "") -> None:
    """Den Baum auf den Sollstand der Basis bringen - neu kopiert oder zurueckgesetzt.

    Fehlt er, wird die Basis kopiert (mit .git und ignorierten Dateien). Besteht er, setzt
    git die versionierten Dateien zurueck, und was die Basis ignoriert fuehrt, wird aus ihr
    zurueckkopiert; jede Datei, die die Basis nicht kennt, faellt weg. Danach steht HEAD auf
    dem gesagten Branch - bei einem Arbeitsbranch frisch vom Sollcommit (K-172).
    """
    if not os.path.exists(baum):
        shutil.copytree(basis, baum, symlinks=True,
                        ignore=shutil.ignore_patterns(*ohne) if ohne else None)
    else:
        git(baum, "checkout", "-q", "-f", soll["branch"])
        git(baum, "reset", "-q", "--hard", soll["commit"])
        soll_dateien = set(dateien(basis, ohne))
        for rel in dateien(baum, ohne):
            if rel not in soll_dateien:
                os.remove(os.path.join(baum, *rel.split("/")))
        for rel in soll_dateien:
            quelle = os.path.join(basis, *rel.split("/"))
            ziel = os.path.join(baum, *rel.split("/"))
            if not os.path.exists(ziel) or open(quelle, "rb").read() != open(ziel, "rb").read():
                os.makedirs(os.path.dirname(ziel), exist_ok=True)
                shutil.copy2(quelle, ziel)
        # leere Verzeichnisse, die ein Lauf angelegt hat
        for wurzel, verz, files in os.walk(baum, topdown=False):
            if ".git" in wurzel.split(os.sep) or any(a in wurzel.split(os.sep) for a in ohne):
                continue
            if wurzel != baum and not os.listdir(wurzel) and not os.path.isdir(
                    os.path.join(basis, os.path.relpath(wurzel, baum))):
                os.rmdir(wurzel)
    if branch != soll["branch"]:
        git(baum, "checkout", "-q", "-B", branch, soll["commit"])
    verbinden(baum, verbindungen)
    if remote:
        _remote_neu(baum, basis, remote_hooks)

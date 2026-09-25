#!/usr/bin/env python3
"""
install_dialog.py - Der Dialog hinter den Startern install.cmd und install.command.

Hintergrund (D-362, CR-2026-140): Die Starter in der Wurzel des Frameworks suchen nur
ein passendes Python und rufen dieses Skript auf. Es fragt Projektverzeichnis, Client
und Overlay-Muster ab und ruft danach genau einen Befehl auf:

    install.py --target <projekt> [--client <name>] [--overlay <name>]
    install.py --target <projekt> --update

Die Fragen stehen HIER und nicht in den Startern, weil zwei Shell-Dialekte zwei
Dialoge waeren, die auseinanderlaufen. install.py bleibt parametergesteuert; dieses
Skript entscheidet nichts, was install.py nicht selbst prueft - es sammelt nur die
Parameter ein und zeigt den Befehl, bevor es ihn ausfuehrt.

Die Ausgabe ist ASCII: Eine Windows-Konsole, die ein Doppelklick oeffnet, laeuft in
ihrer eigenen Codepage, und ein Umlaut kaeme dort verstellt an.

Aufruf (normalerweise durch einen Starter):

    python .koolie/core/install_dialog.py

Exit-Code: der von install.py; 1 bei Abbruch im Dialog.
"""
from __future__ import annotations

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import install  # noqa: E402  (liegt neben dieser Datei)

VERSUCHE = 3


class Abbruch(Exception):
    pass


def frage(text: str) -> str:
    try:
        antwort = input(text)
    except EOFError:
        raise Abbruch("keine Eingabe mehr")
    if antwort.strip().lower() in ("q", "quit", "abbruch"):
        raise Abbruch("abgebrochen")
    return antwort.strip()


def pfad_bereinigen(eingabe: str) -> str:
    """Ein eingefuegter oder hineingezogener Pfad: Anfuehrungszeichen und Rand weg.

    Windows setzt beim Hineinziehen doppelte Anfuehrungszeichen, das macOS-Terminal
    maskiert Leerzeichen mit einem Rueckstrich. Beides wird hier aufgeloest.
    """
    p = eingabe.strip()
    if len(p) >= 2 and p[0] == p[-1] and p[0] in "\"'":
        p = p[1:-1]
    if os.sep == "/":
        p = p.replace("\\ ", " ")
    return os.path.abspath(os.path.expanduser(p))


def ja(text: str, vorgabe: bool) -> bool:
    zeichen = "[J/n]" if vorgabe else "[j/N]"
    for _ in range(VERSUCHE):
        a = frage(f"{text} {zeichen} ").lower()
        if not a:
            return vorgabe
        if a in ("j", "ja", "y", "yes"):
            return True
        if a in ("n", "nein", "no"):
            return False
        print("  Bitte j oder n.")
    raise Abbruch("keine gueltige Antwort")


def auswahl(text: str, optionen: list[tuple[str, str]], vorgabe: int) -> str:
    """Nummerierte Auswahl; gibt den Wert der gewaehlten Option zurueck."""
    print(text)
    for i, (_wert, anzeige) in enumerate(optionen, 1):
        mark = "  (Vorgabe)" if i == vorgabe else ""
        print(f"  {i}. {anzeige}{mark}")
    for _ in range(VERSUCHE):
        a = frage(f"Nummer [{vorgabe}]: ")
        if not a:
            return optionen[vorgabe - 1][0]
        if a.isdigit() and 1 <= int(a) <= len(optionen):
            return optionen[int(a) - 1][0]
        print(f"  Bitte eine Zahl von 1 bis {len(optionen)}.")
    raise Abbruch("keine gueltige Auswahl")


def projekt_erfragen() -> str:
    wurzel = install.quellwurzel()
    for _ in range(VERSUCHE):
        eingabe = frage("Projektverzeichnis (Ordner hier hineinziehen oder Pfad eingeben): ")
        if not eingabe:
            continue
        ziel = pfad_bereinigen(eingabe)
        if not os.path.isdir(ziel):
            print(f"  Das Verzeichnis gibt es nicht: {ziel}")
            continue
        if install._gleicher_pfad(ziel, wurzel):
            print("  Das ist das Framework selbst. Gemeint ist das Projekt, in das "
                  "installiert wird.")
            continue
        return ziel
    raise Abbruch("kein gueltiges Projektverzeichnis")


def befehl_bauen(ziel: str) -> list[str]:
    argv = [sys.executable, os.path.join(HERE, "install.py"), "--target", ziel]
    zielkern = os.path.join(ziel, *install.clientmap.CORE_REL.split("/"))
    if os.path.isdir(zielkern):
        stand = install.kern_version(zielkern)
        print()
        print(f"In diesem Projekt liegt bereits Koolie {stand}.")
        if not ja(f"Auf {install.kern_version(HERE)} heben?", True):
            raise Abbruch("nicht gehoben")
        return argv + ["--update"]

    clients = install.available_clients()
    if not clients:
        raise Abbruch("keine Client Packs gefunden")
    print()
    client = auswahl("Welcher KI-Client wird in diesem Projekt verwendet?",
                     [(c, c) for c in clients],
                     clients.index(install.DEFAULT_CLIENT) + 1
                     if install.DEFAULT_CLIENT in clients else 1)
    muster = [("", "keines - das Projekt beginnt mit dem leeren Overlay")]
    for name in install.verfuegbare_muster():
        try:
            m = install.muster_laden(name)
        except install.MusterFehler:
            continue
        muster.append((name, f"{name} {m['version']} - Vorschlaege fuer allgemeine "
                             f"Projektwerte und Dokumente, geben nichts frei"))
    overlay = ""
    if len(muster) > 1:
        print()
        overlay = auswahl("Mit einem Overlay-Muster beginnen?", muster, 1)
    argv += ["--client", client]
    if overlay:
        argv += ["--overlay", overlay]
    return argv


def main() -> int:
    print(f"Koolie {install.kern_version(HERE)} - Installation in ein Projekt")
    print(f"Quelle: {install.quellwurzel()}")
    print("Abbrechen jederzeit mit q.")
    print()
    try:
        ziel = projekt_erfragen()
        argv = befehl_bauen(ziel)
        print()
        print("Ausgefuehrt wird:")
        print("  " + subprocess.list2cmdline(argv[1:]) if os.name == "nt"
              else "  " + " ".join(argv[1:]))
        if not ja("Fortfahren?", True):
            raise Abbruch("nicht bestaetigt")
    except Abbruch as exc:
        print(f"\nNichts installiert ({exc}).")
        return 1
    print()
    sys.stdout.flush()
    return subprocess.run(argv).returncode


if __name__ == "__main__":
    sys.exit(main())

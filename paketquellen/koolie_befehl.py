#!/usr/bin/env python3
"""
koolie_befehl.py - Der Befehl `koolie`, wie ihn die Paketquellen einrichten (CR-2026-168).

Hintergrund (D-518, D-519): Eine Paketquelle legt Koolie auf den Rechner, nicht in ein
Projekt. Ins Projekt kommt es erst durch den Aufruf dieses Befehls - und nur dieser Aufruf
laeuft bei jeder Paketquelle im Terminal des Nutzers. Der Installationsschritt der
Paketquelle selbst tut es nicht (gemessen 2026-09-30): pip fuehrt beim Installieren eines
Wheels nichts aus, npm verschluckt die Ausgabe eines Installationsskripts, Chocolatey gibt
ihm kein Terminal, winget installiert still. Deshalb steht das Banner HIER und nicht in
einem Installationsskript.

    koolie                           der Dialog aus install_dialog.py, mit Banner
    koolie <Argumente von install.py> Banner, dann install.py mit genau diesen Argumenten
    koolie --version                 nur die Version, ohne Banner

Das Banner waehlt seine Variante selbst (banner.py, D-506): ohne Terminal die
Textvariante, mit NO_COLOR einfarbig, mit --no-banner oder KOOLIE_NO_BANNER=1 gar nichts.
--no-banner wird vor dem Aufruf von install.py entfernt; install.py kennt es nicht.

Der Kern liegt neben diesem Ordner unter .koolie/core - im Wheel, im npm-Paket und im
entpackten Release-Archiv gleich (D-520). Dieses Skript entscheidet nichts, was install.py
nicht selbst prueft.

Exit-Code: der von install.py beziehungsweise des Dialogs; 2, wenn der Kern fehlt.
"""
from __future__ import annotations

import os
import subprocess
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KERN = os.path.join(WURZEL, ".koolie", "core")
KEIN_BANNER = "--no-banner"


def kern_da() -> bool:
    return all(os.path.isfile(os.path.join(KERN, n))
               for n in ("install.py", "install_dialog.py", "banner.py", "VERSION"))


def version() -> str:
    with open(os.path.join(KERN, "VERSION"), encoding="utf-8") as fh:
        return fh.read().strip()


def banner_ausgeben(argv: list) -> None:
    """Wie im Dialog: in einer eigenen Huelle, das Banner haelt nichts auf (F-5)."""
    try:
        if KERN not in sys.path:
            sys.path.insert(0, KERN)
        import banner
        banner.ausgeben(argv=argv, version=version())
    except Exception:  # noqa: BLE001
        pass


def main(argv: list | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not kern_da():
        print(f"FEHLER: Der Kern fehlt unter {KERN} - das Paket ist unvollstaendig.",
              file=sys.stderr)
        return 2
    if argv in (["--version"], ["-V"]):
        print(f"koolie {version()}")
        return 0
    rest = [a for a in argv if a != KEIN_BANNER]
    if not rest:
        # Der Dialog gibt das Banner selbst aus und wertet --no-banner selbst aus.
        return subprocess.run([sys.executable, os.path.join(KERN, "install_dialog.py"),
                               *argv]).returncode
    banner_ausgeben(argv)
    sys.stdout.flush()
    return subprocess.run([sys.executable, os.path.join(KERN, "install.py"), *rest]).returncode


if __name__ == "__main__":
    sys.exit(main())

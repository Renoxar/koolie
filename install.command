#!/bin/sh
# Koolie - Starter fuer macOS (D-362, CR-2026-140).
#
# Sucht ein Python ab 3.8 und ruft den Dialog .koolie/core/install_dialog.py auf.
# Die Installationslogik steht in install.py; dieser Starter enthaelt keine.
#
# Ein Doppelklick im Finder oeffnet diese Datei im Terminal. Das setzt das
# Ausfuehrungsrecht voraus - das Repositorium fuehrt die Datei mit Modus 100755, und
# eine Sonde haelt es fest. Ohne das Recht: im Terminal "sh install.command".
#
# macOS bringt unter /usr/bin/python3 einen Platzhalter mit, der ohne die Command
# Line Tools kein Python startet, sondern deren Installation anbietet. Er faellt an
# der Versionsprobe durch wie jeder andere Kandidat, der nicht antwortet.
#
# POSIX-sh, keine bash-Eigenheiten: Der Starter soll auch unter Linux und in Git Bash
# laufen, wo er geprueft wird.

cd "$(dirname "$0")" || exit 1
KOOLIE_KERN="$(pwd)/.koolie/core"
KOOLIE_PY=""
KOOLIE_RC=1

if [ ! -f "$KOOLIE_KERN/install_dialog.py" ]; then
    echo "FEHLER: install_dialog.py fehlt unter \"$KOOLIE_KERN\"."
    echo "Dieser Starter gehoert in die Wurzel des entpackten Frameworks."
else
    for kandidat in python3 python; do
        if command -v "$kandidat" >/dev/null 2>&1 && \
           "$kandidat" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' >/dev/null 2>&1; then
            KOOLIE_PY="$kandidat"
            break
        fi
    done
    if [ -z "$KOOLIE_PY" ]; then
        echo "Koolie braucht Python 3.8 oder neuer - gefunden wurde keines."
        echo
        echo "Installieren, zum Beispiel:"
        echo "  von python.org"
        echo "  oder mit Homebrew: brew install python"
        echo "Danach dieses Fenster schliessen und den Starter erneut aufrufen."
    else
        "$KOOLIE_PY" "$KOOLIE_KERN/install_dialog.py"
        KOOLIE_RC=$?
    fi
fi
exit "$KOOLIE_RC"

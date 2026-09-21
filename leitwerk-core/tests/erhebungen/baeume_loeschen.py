"""Loescht die Messbaeume unter C:\\lw-b4 - Verbindungen EINZELN (Regel aus 0.74.1).

Ein rekursives Loeschen, das einer Verzeichnisverbindung folgt, loescht den geteilten
`node_modules`-Bestand des Uebungsrepositoriums mit. Erst jede Verbindung mit
os.rmdir loesen (das entfernt den Link, nicht das Ziel), dann den Rest.

    python baeume_loeschen.py zaehlen     # nur den Quellbestand zaehlen
    python baeume_loeschen.py loeschen    # zaehlen, loeschen, gegenzaehlen
"""
import os
import shutil
import stat
import sys

import ablage

# 🔴 DER BERICHTSWEG GEHOERT IN BEIDE KODIERUNGSUMGEBUNGEN (D-223). Ohne diese
# Zeile stirbt `print` an der eigenen Ampelzeile, sobald PYTHONIOENCODING nicht
# gesetzt ist - gemessen am 2026-09-20, NACH dem Loeschen von 46 Baeumen und
# nach der Gegenzaehlung. 🟢 Gemessen ist auch die andere Haelfte, und sie ging
# anders aus als vermutet: Die ABBRUCHmeldung traegt, weil Python die
# SystemExit-Meldung mit `backslashreplace` auf stderr schreibt - `print` auf
# stdout schreibt mit `strict`. Der wichtige Bericht kam durch, der harmlose
# nicht.
sys.stdout.reconfigure(encoding="utf-8")

BASIS = r"C:\lw-b4"
QUELLE = os.path.join(ablage.uebungsrepositorium(),   # D-231
                      "frontend", "node_modules")


# Das Pruefmittel schreibt seinen Zwischenstand unterhalb von node_modules -
# `vitest` legt `.vite/vitest/results.json` bei JEDEM Lauf neu an, und
# `umgebungen-bauen-b4.py` faehrt den Testbefehl vor jedem Messtag im Messbaum.
# 🔴 GEMESSEN am 2026-09-20 beim Trockenlauf des Apparats: 101 089 284 Bytes
# gegen die 101 089 283, die `0.79.1` als den Bestand fuehrt - ein Byte, und es
# gehoert dem Pruefmittel. `node-waechter.py` weist solche Pfade seit seinem Bau
# gesondert aus; dieser Zaehler tat es nicht, und damit sagten zwei Zaehler
# desselben Gegenstands Verschiedenes.
ZWISCHENSTAND = (".vite", ".cache", ".tmp")


def bestand(pfad):
    """(Dateien, Bytes, Zwischenstandsdateien) - der Zwischenstand zaehlt NICHT mit."""
    n = b = z = 0
    for dirpath, dirnames, filenames in os.walk(pfad):
        rel = os.path.relpath(dirpath, pfad).replace("\\", "/")
        ist_zwischen = any(teil in rel.split("/") for teil in ZWISCHENSTAND)
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            try:
                groesse = os.path.getsize(p)
            except OSError:
                continue
            if ist_zwischen:
                z += 1
                continue
            b += groesse
            n += 1
    return n, b, z


def verbindungen(wurzel):
    gefunden = []
    for dirpath, dirnames, filenames in os.walk(wurzel):
        for d in list(dirnames):
            p = os.path.join(dirpath, d)
            if os.path.isdir(p) and os.path.islink(p) or _junction(p):
                gefunden.append(p)
                dirnames.remove(d)
    return gefunden


def _junction(pfad):
    try:
        return bool(os.lstat(pfad).st_file_attributes
                    & stat.FILE_ATTRIBUTE_REPARSE_POINT)
    except (OSError, AttributeError):
        return False


def main():
    was = sys.argv[1] if len(sys.argv) > 1 else "zaehlen"
    vorher = bestand(QUELLE)
    print("node_modules vorher: %d Dateien / %d Bytes (dazu %d "
          "Zwischenstandsdateien des Pruefmittels)" % vorher)
    if was != "loeschen":
        return 0
    if not os.path.isdir(BASIS):
        print("kein", BASIS)
        return 0
    gesamt = 0
    for name in sorted(os.listdir(BASIS)):
        baum = os.path.join(BASIS, name)
        if not os.path.isdir(baum):
            continue
        for v in verbindungen(baum):
            os.rmdir(v)          # loest den Link, nicht das Ziel
            gesamt += 1
        # Die Objektdateien von git sind schreibgeschuetzt - ohne diesen Haken
        # bricht rmtree mit WinError 5 ab, und der Baum bleibt halb geloescht stehen.
        shutil.rmtree(baum, onexc=lambda f, p, e: (os.chmod(p, stat.S_IWRITE), f(p)))
        print("geloescht:", name)
    print("Verbindungen einzeln geloest:", gesamt)
    nachher = bestand(QUELLE)
    print("node_modules nachher: %d Dateien / %d Bytes (dazu %d "
          "Zwischenstandsdateien des Pruefmittels)" % nachher)
    # Verglichen werden Dateizahl und Bytes OHNE den Zwischenstand. Der dritte
    # Wert wird berichtet, nicht geprueft: Er aendert sich bei jedem Testlauf,
    # und ein Waechter, der ihn mitrechnet, schlaegt an, wo nichts geschehen ist.
    if nachher[:2] != vorher[:2]:
        raise SystemExit("🔴 ABBRUCH: der geteilte Bestand hat sich geaendert!")
    print("🟢 geteilter Bestand unberuehrt")
    return 0


if __name__ == "__main__":
    sys.exit(main())

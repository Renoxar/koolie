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

BASIS = r"C:\lw-b4"
QUELLE = os.path.join(r"C:\Users\reneh\Documents\devpacks\test-devin-framework",
                      "frontend", "node_modules")


def bestand(pfad):
    n = b = 0
    for dirpath, dirnames, filenames in os.walk(pfad):
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            try:
                b += os.path.getsize(p)
                n += 1
            except OSError:
                pass
    return n, b


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
    print("node_modules vorher: %d Dateien / %d Bytes" % vorher)
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
    print("node_modules nachher: %d Dateien / %d Bytes" % nachher)
    if nachher != vorher:
        raise SystemExit("🔴 ABBRUCH: der geteilte Bestand hat sich geaendert!")
    print("🟢 geteilter Bestand unberuehrt")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Sonden zur Modusbindung M3 bis M5 (1.23.0, CR-2026-169, K-201): mandat.py kopiert die
Pfadliste des Modus aus dem Overlay in die Bindung, und der Schutz-Hook wertet sie als
Globs aus - mit Nur-Lese-Pfaden, Umfang, Namensvettern, Punktsegmenten und dem Glob mitten
im Pfad. Dazu die Gegenprobe zu Pruefung 99: ein abweichender Rumpf von glob_muster.

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul liest
nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import json
import os
import sys

from .apparat import (
    aufraeumen, buendel, installation, lies, melde, schreib, strict_ausgabe, unterprozess)
from .teil14_modi_ausnahmen_skills import _hook, _modus_setzen, _schreiben

MODUS = os.path.join(".git", "koolie-modus.json")

# Die Werte haben die Gestalten, die in den drei gemessenen Overlays vorkommen: Praefix,
# Einzeldatei, Glob mitten im Pfad (Uebung) und "nicht vorhanden" (otp-generator).
OVERLAY_ABSCHNITT_4 = """
## 4. Pfade

| Zweck | Platzhalter | Wert | Hinweis |
|---|---|---|---|
| Erlaubte Pfade (Lesen und Ändern in M3) | `<ALLOWED_PATHS>` | `src/**`, `test/**`, `README.md` | Sonde |
| Testpfade (Ändern in M4) | `<TEST_PATHS>` | `test/**`, `src/**/*.test.ts` | Sonde |
| Dokumentationspfade (Ändern in M5) | `<DOC_PATHS>` | `nicht vorhanden` | Sonde |
| Nur-Lese-Pfade (Lesen erlaubt, Ändern nie) | `<READ_ONLY_PATHS>` | `src/api/**` | Sonde |
"""


def _binden(root: str, *argv: str):
    mandat = os.path.join(root, ".koolie", "core", "mandat.py")
    return unterprozess([sys.executable, mandat, "modus", *argv])


def _frei(root: str, rel: str) -> bool:
    return _hook(root, _schreiben(rel)) == 0


def sonden_modusbindung_m3_m5() -> None:
    """M3 bis M5 an einer echten Installation: Bindung aus dem Overlay, Auswertung im Hook."""
    root = installation("claude-code")
    try:
        os.makedirs(os.path.join(root, ".git"), exist_ok=True)
        overlay = os.path.join(root, ".koolie", "project-overlay", "OVERLAY.md")
        # Ersetzt, nicht angehaengt: Die Vorlage traegt dieselben Zeilen mit <TBD>, und
        # gelesen wird die erste.
        schreib(overlay, "# Overlay\n" + OVERLAY_ABSCHNITT_4)

        p = _binden(root, "M3", "--minuten", "5")
        daten = json.loads(lies(os.path.join(root, MODUS))) if p.returncode == 0 else {}
        melde("SONDE", "K201a", daten.get("pfade") == ["src/**", "test/**", "README.md"]
              and daten.get("nur_lesen") == ["src/api/**"],
              "mandat.py modus M3 kopiert <ALLOWED_PATHS> und <READ_ONLY_PATHS> in die Bindung")
        melde("SONDE", "K201b", _frei(root, "src/a/B.java") and _frei(root, "README.md")
              and not _frei(root, "docs/x.md") and not _frei(root, "README.md.bak"),
              "M3: Praefix und Einzeldatei frei, alles Uebrige gesperrt")
        melde("SONDE", "K201c", not _frei(root, "src/api/v1.yaml"),
              "M3: ein Nur-Lese-Pfad innerhalb der erlaubten Pfade bleibt gesperrt")
        melde("SONDE", "K201d", not _frei(root, "src2/x.java")
              and not _frei(root, "src/../docs/x.md") and not _frei(root, "../draussen/x"),
              "M3: Namensvetter, Punktsegment und ein Ziel ausserhalb fuehren nicht hinein")
        melde("SONDE", "K201e", _frei(root, "SRC/a.java"),
              "M3: ohne Gross- und Kleinschreibung wie jeder Pfadvergleich des Hooks (D-492)")

        p = _binden(root, "M3", "--umfang", "src/billing/**", "--minuten", "5")
        melde("SONDE", "K201f", p.returncode == 0 and _frei(root, "src/billing/R.java")
              and not _frei(root, "src/other/R.java") and not _frei(root, "test/T.java"),
              "M3 mit --umfang: nur die Schnittmenge aus Umfang und <ALLOWED_PATHS>")
        p = _binden(root, "M3", "--umfang", "docs/**", "--minuten", "5")
        melde("SONDE", "K201g", p.returncode == 0 and not _frei(root, "docs/a.md"),
              "M3: ein Umfang ausserhalb von <ALLOWED_PATHS> oeffnet nichts")

        p = _binden(root, "M4", "--minuten", "5")
        melde("SONDE", "K201h", p.returncode == 0 and _frei(root, "test/T.java")
              and _frei(root, "src/ui/knopf.test.ts") and not _frei(root, "src/ui/knopf.ts"),
              "M4: Testpfade frei, auch der Glob mitten im Pfad; Produktivcode gesperrt")

        os.remove(os.path.join(root, MODUS))
        p = _binden(root, "M5", "--minuten", "5")
        melde("SONDE", "K201i", p.returncode == 2
              and not os.path.exists(os.path.join(root, MODUS)),
              "M5 ohne <DOC_PATHS> bindet nicht - eine Bindung, die nichts erlaubt, ist M1")
        p = _binden(root, "M3", "--umfang", "../x/**", "--minuten", "5")
        melde("SONDE", "K201j", p.returncode == 2
              and not os.path.exists(os.path.join(root, MODUS)),
              "Ein Umfang mit '..' wird abgelehnt, und nichts wird geschrieben")

        _modus_setzen(root, "M3")  # gueltig in Zeit und Projekt, aber ohne "pfade"
        melde("GEGENPROBE", "K201k", _frei(root, "docs/x.md"),
              "Eine Bindung ohne Pfade ist kaputt und sperrt nichts (wie bei M2, D-501)")
        _binden(root, "aus")
        melde("GEGENPROBE", "K201l", _frei(root, "docs/x.md"),
              "mandat.py modus aus hebt auch M3 bis M5 auf")

        mandat = os.path.join(root, ".koolie", "core", "mandat.py")
        melde("GEGENPROBE", "K201n", "glob_muster" not in strict_ausgabe(root),
              "Pruefung 99: gleichlautende Funktionen glob_muster melden nichts")
        schreib(mandat, lies(mandat).replace('raus + "[^/]*", i + 1', 'raus + ".*", i + 1', 1))
        melde("SONDE", "K201m", "glob_muster" in strict_ausgabe(root),
              "Pruefung 99: ein '*', das in mandat.py ueber '/' hinweg trifft, wird gemeldet")
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_modusbindung_m3_m5,
        "Die Modusbindung fuer M3 bis M5 an einer claude-code-Installation: Kopie aus dem "
        "Overlay, Globs, Nur-Lese-Pfade, Umfang, Ausbruch, leere Liste, Aufheben")

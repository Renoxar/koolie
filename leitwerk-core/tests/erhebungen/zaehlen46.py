# -*- coding: utf-8 -*-
"""Zaehlt Kriterium 2 mit der Regel von Pruefung 46 selbst - Zelle fuer Zelle.

🔴 DIE REGEL WIRD GETEILT, NICHT NACHGEBAUT (D-259). Bis 0.83.0 zerlegte dieses
Werkzeug eine Tabellenzeile mit `z.strip("|").split("|")` und kannte den MASKIERTEN
Zelltrenner `\\|` nicht; Pruefung 46 benutzt `tabellenzellen()` des Validators, und die
kennt ihn. Gemessen am 2026-09-22: An ZWEI Zellen gehen beide auseinander -
`RE-001-P04` (10 statt 8 Spalten) und `RE-001-N06` (11 statt 8). Beide standen auf
`bestanden`, und die Zaehlung stimmte deshalb - **aus dem falschen Grund**. Stuende eine
von ihnen auf `offen`, laese der naive Split ein Textfragment als Status und die Zelle
bliebe ungezaehlt: eine Null durch Konstruktion, die wie eine gemessene aussieht.

  Ein Werkzeug, das dieselbe Regel anwenden soll wie eine Pruefung, teilt ihren Code -
  sonst teilt es nur ihren Namen.
"""
import importlib.util
import io, os, sys

import ablage

# Die Zellzerlegung von Pruefung 46 - geladen, nicht nachgebaut. Der Dateiname traegt
# einen Bindestrich und ist deshalb nicht importierbar; der Lader kennt keinen.
_VALIDATOR = os.path.join(ablage.WURZEL, "leitwerk-core", "tests", "scripts",
                          "validate-framework.py")
_spec = importlib.util.spec_from_file_location("_vf46", _VALIDATOR)
_vf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_vf)

sys.stdout.reconfigure(encoding="utf-8")
ROOT = ablage.WURZEL                        # D-231: abgeleitet, nicht im Quelltext
KERN = os.path.join(ROOT, "leitwerk-core")
AUSSER = ("build/", "CHANGELOG.md", "governance/change-requests/", "tests/protocols/")

def read(p):
    return io.open(p, encoding="utf-8", newline="").read().replace("\r\n", "\n")

def zellen(z):
    """Die Zellen einer Tabellenzeile - mit der Funktion, die Pruefung 46 benutzt."""
    return _vf.tabellenzellen(z)

def offen(text, praefix, rel):
    treffer = []
    for i, zeile in enumerate(text.split("\n"), 1):
        z = zeile.strip()
        if not z.startswith(praefix) or z.startswith("|---"):
            continue
        t = zellen(z)
        if t and t[-1].startswith("offen"):
            treffer.append((rel, i, t[0][:40]))
    return treffer

alle = []
kat = os.path.join(KERN, "tests", "TEST_CATALOG.md")
alle += offen(read(kat), "| FW-", "tests/TEST_CATALOG.md")
k1 = len(alle)
for wurzel, _, dateien in os.walk(KERN):
    for n in sorted(dateien):
        if n != "TESTS.md":
            continue
        p = os.path.join(wurzel, n)
        rel = os.path.relpath(p, KERN).replace(os.sep, "/")
        if any(rel.startswith(a) for a in AUSSER):
            continue
        alle += offen(read(p), "| ", rel)
print("Katalog: %d | Testblaetter: %d | SUMME: %d" % (k1, len(alle) - k1, len(alle)))
print()
print("--- Zellen, deren erste Spalte KEINE SK-/FW-Kennung ist ---")
import re
n = 0
for rel, i, erste in alle:
    if not re.match(r"^(SK|FW)-", erste):
        n += 1
        print("  %-52s Zeile %-4d erste Spalte: %r" % (rel, i, erste))
print("  ->", n, "Stueck")

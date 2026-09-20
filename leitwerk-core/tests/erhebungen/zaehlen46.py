# -*- coding: utf-8 -*-
"""Zaehlt Kriterium 2 mit der Regel von Pruefung 46 selbst - Zelle fuer Zelle."""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = r"C:\Users\reneh\Documents\devpacks\leitwerk"
KERN = os.path.join(ROOT, "leitwerk-core")
AUSSER = ("build/", "CHANGELOG.md", "governance/change-requests/", "tests/protocols/")

def read(p):
    return io.open(p, encoding="utf-8", newline="").read().replace("\r\n", "\n")

def zellen(z):
    return [c.strip() for c in z.strip().strip("|").split("|")]

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

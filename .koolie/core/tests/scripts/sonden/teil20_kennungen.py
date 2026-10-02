"""Sonden zu Pruefung 113 (2.0.0): keine Kennung in der Produktdokumentation, ausser an den
Stellen, die selbst Nachweis sind.

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul liest
nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import os

from .apparat import ersetze, gegenprobe, lies, P, schreib, sonde

M113 = "in der Produktdokumentation"
PLAN = ".koolie/core/framework/skills/koolie-plan/"


def _p(root: str, rel: str) -> str:
    return P(root, rel.replace("/", os.sep))


# SYNTHETISCH: K-99 ist eine belegte synthetische Kennung (Decision Log), nie echt vergeben.
def _113_startseite(root: str) -> None:
    pfad = _p(root, "README.md")
    schreib(pfad, lies(pfad).rstrip("\r\n") + "\r\n\r\nMehr dazu in K-99.\r\n")


def _113_skill(root: str) -> None:
    pfad = _p(root, PLAN + "EXAMPLES.md")
    schreib(pfad, lies(pfad).rstrip("\r\n") + "\r\n\r\nSiehe K-99.\r\n")


def _113_testblatt(root: str) -> None:
    ersetze(_p(root, PLAN + "TESTS.md"), ("| SK-004-P01 | ", "| SK-004-P01 | K-99 "))


def _113_hauptdokument(root: str) -> None:
    pfad = _p(root, ".koolie/core/build/doc/01-executive-summary.md")
    schreib(pfad, lies(pfad).rstrip("\r\n") + "\r\n\r\nSiehe K-99.\r\n")


def _113_grenzen(root: str) -> None:
    pfad = _p(root, ".koolie/core/build/doc/29-grenzen.md")
    schreib(pfad, lies(pfad).rstrip("\r\n") + "\r\n\r\nSiehe K-99.\r\n")


def _113_verlauf(root: str) -> None:
    pfad = _p(root, "README.md")
    schreib(pfad, lies(pfad).rstrip("\r\n") + "\r\n\r\n| Version | Änderung |\r\n|---|---|\r\n"
            "| 9.9.9 | K-99 |\r\n")


sonde("113a", "Eine Kennung auf der Startseite wird gemeldet",
      _113_startseite, "README.md: 1 Kennung(en) " + M113)
sonde("113b", "Eine Kennung in den Erlaeuterungen eines Skills wird gemeldet",
      _113_skill, "koolie-plan/EXAMPLES.md: 1 Kennung(en) " + M113)
sonde("113c", "Eine Kennung in einer Spalte eines Testblatts, die kein Ergebnis traegt, wird "
      "gemeldet - die Ausnahme gilt der Spalte, nicht dem Blatt",
      _113_testblatt, "koolie-plan/TESTS.md: 1 Kennung(en) " + M113)
gegenprobe("113a", "Der ausgelieferte Bestand laeuft durch - Ergebnisspalten, Belegspalten der "
           "Matrix und Versionsverlaeufe tragen ihre Kennungen, die Nachweisschicht ebenso",
           None, M113)
gegenprobe("113b", "Eine Kennung in der Zeile eines Versionsverlaufs wird nicht gemeldet",
           _113_verlauf, M113)

sonde("113d", "Eine Kennung in einem Kapitel des Hauptdokuments wird gemeldet - nur drei "
      "Kapitel sind Nachweis",
      _113_hauptdokument, "01-executive-summary.md: 1 Kennung(en) " + M113)
gegenprobe("113c", "Eine Kennung im Kapitel der Grenzen und offenen Entscheidungen wird nicht "
           "gemeldet", _113_grenzen, M113)

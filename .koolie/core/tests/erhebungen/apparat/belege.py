# -*- coding: utf-8 -*-
"""Belege sichern - sofort nach jedem Lauf - und eine Reihe auswerten.

Je Lauf und Turn entstehen: -ergebnis.json, -stdout.txt (mit stderr), -antwort.md,
-transkript.jsonl (wenn der Client eine Mitschrift fuehrt) und -lauf.json mit allem,
was zur Einordnung gehoert: Client und Version, Modell, Gruppe, Variante, Baum, Branch,
Baum-Hash vor dem Lauf, Kosten und Cache-Zahlen. Der Modus gehoert in die Aufzeichnung
jedes Laufs (D-280) - und seit 1.19.0 auch das Modell.

Die Ablage liegt AUSSERHALB des Repositoriums; ein Pfad darin ist ein Abbruch (D-222).
"""
from __future__ import annotations

import io
import json
import os

from . import kontingent

KERN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
REPO = os.path.dirname(os.path.dirname(KERN))


def _innerhalb(pfad: str, wurzel: str) -> bool:
    try:
        return os.path.commonpath([os.path.abspath(pfad).lower(),
                                   os.path.abspath(wurzel).lower()]) == os.path.abspath(wurzel).lower()
    except ValueError:
        return False


def ablage_pruefen(pfad: str) -> None:
    if _innerhalb(pfad, REPO):
        raise RuntimeError(f"{pfad} liegt im Repositorium - Belege sind Aufzeichnung und gehoeren "
                           f"daneben (D-222, Pruefung 69)")


def sichern(belege: str, kennung: str, turn: int, lauf: dict, meta: dict, adapter) -> str:
    ablage_pruefen(belege)
    os.makedirs(belege, exist_ok=True)
    name = kennung if turn == 0 else f"{kennung}-t{turn + 1}"
    p = lambda endung: os.path.join(belege, name + endung)
    io.open(p("-ergebnis.json"), "w", encoding="utf-8").write(
        json.dumps(lauf["ergebnis"], ensure_ascii=False, indent=1))
    io.open(p("-stdout.txt"), "w", encoding="utf-8").write(
        lauf["stdout"] + "\n--- stderr ---\n" + lauf["stderr"])
    io.open(p("-antwort.md"), "w", encoding="utf-8").write(str(lauf.get("antwort") or ""))
    mitschrift = False
    if lauf.get("sitzung"):
        try:
            mitschrift = adapter.mitschrift(lauf["sitzung"], p("-transkript.jsonl"))
        except Exception:  # Unerhoben oder ein fehlender Ordner - beides ist 'keine Mitschrift'
            mitschrift = False
    daten = dict(meta)
    for k in ("sitzung", "usd", "is_error", "turns", "abweisungen", "cache_neu",
              "cache_gelesen", "sekunden", "exit", "modell", "kosten"):
        if k in lauf:
            daten[k] = lauf[k]
    daten["mitschrift"] = mitschrift
    io.open(p("-lauf.json"), "w", encoding="utf-8").write(json.dumps(daten, ensure_ascii=False, indent=1))
    return name


def auswerten(reihe, gruppiert_nach: str = "") -> str:
    """Eine Tabelle je Lauf und die Summen - gruppiert, wenn ein Feld gesagt ist."""
    zeilen = ["| Kennung | Variante | Gruppe | Modell | USD | Turns | Abweisungen | Cache neu | Cache gelesen | Erwartung |",
              "|---|---|---|---|---:|---:|---:|---:|---:|---|"]
    gruppen = {}
    for e in kontingent.eintraege(reihe.belege):
        k = e["kennung"]
        try:
            lauf = reihe.lauf(k)
            erwartung = lauf.erwartung
        except Exception:
            erwartung = "(nicht in der Reihe)"
        zeilen.append("| %s | %s | %s | %s | %.3f | %s | %s | %s | %s | %s |" % (
            k, e.get("variante") or "-", e.get("gruppe"), e.get("modell"), float(e.get("usd") or 0),
            e.get("turns"), e.get("abweisungen"), e.get("cache_neu"), e.get("cache_gelesen"), erwartung))
        if gruppiert_nach:
            g = gruppen.setdefault(str(e.get(gruppiert_nach)), [0, 0.0, 0, 0])
            g[0] += 1
            g[1] += float(e.get("usd") or 0)
            g[2] += int(e.get("cache_neu") or 0)
            g[3] += int(e.get("cache_gelesen") or 0)
    n, usd = kontingent.summe(reihe.belege)
    zeilen.append("")
    zeilen.append(f"Summe: {n} Laeufe, {usd:.2f} USD (Deckel {reihe.max_laeufe} / {reihe.max_usd:.2f})")
    for g, (m, u, neu, gel) in sorted(gruppen.items()):
        zeilen.append(f"  {gruppiert_nach}={g}: {m} Laeufe, {u:.2f} USD, Mittel {u / m:.3f} USD, "
                      f"Cache neu {neu}, gelesen {gel}")
    return "\n".join(zeilen)

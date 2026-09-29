# -*- coding: utf-8 -*-
"""Das Kontingentbuch: eine Datei je Lauf, die Summe wird gerechnet.

ANLASS (1.17.0, Falle 8): Zwei Reihen, die parallel liefen, schrieben DIESELBE
kontingent.json - die eine las, die andere schrieb dazwischen, und die Summe stimmte
nicht mehr; sie musste aus den Ergebnisdateien nachgerechnet werden. Eine Datei je Lauf
hat keinen gemeinsamen Schreibort, und die Summe ist nie gepflegt, immer gerechnet.

Der Deckel wird VOR dem Lauf geprueft, mit Reserve: Ein Lauf, der das Kontingent
ueberschreiten KOENNTE, faehrt nicht.
"""
from __future__ import annotations

import io
import json
import os


def ordner(belege: str) -> str:
    return os.path.join(belege, "kontingent")


def eintraege(belege: str) -> list:
    o = ordner(belege)
    if not os.path.isdir(o):
        return []
    aus = []
    for f in sorted(os.listdir(o)):
        if f.endswith(".json"):
            aus.append(json.loads(io.open(os.path.join(o, f), encoding="utf-8").read()))
    return aus


def summe(belege: str) -> tuple:
    e = eintraege(belege)
    return len(e), round(sum(float(x.get("usd") or 0) for x in e), 4)


def gefahren(belege: str, kennung: str) -> bool:
    return os.path.exists(os.path.join(ordner(belege), kennung + ".json"))


def frei(belege: str, max_laeufe: int, max_usd: float, reserve_usd: float) -> str:
    """Leer, wenn ein weiterer Lauf faehrt - sonst der Grund."""
    n, usd = summe(belege)
    if n >= max_laeufe:
        return f"Kontingent erschoepft: {n} von {max_laeufe} Laeufen"
    if usd + reserve_usd > max_usd:
        return (f"Kontingent erschoepft: {usd:.2f} USD + Reserve {reserve_usd:.2f} "
                f"ueber dem Deckel {max_usd:.2f} USD")
    return ""


def eintragen(belege: str, kennung: str, daten: dict) -> None:
    """Schreibt genau einmal - ein zweiter Eintrag derselben Kennung ist ein Fehler."""
    o = ordner(belege)
    os.makedirs(o, exist_ok=True)
    pfad = os.path.join(o, kennung + ".json")
    if os.path.exists(pfad):
        raise RuntimeError(f"{kennung}: schon im Kontingentbuch - ein Lauf wird nicht doppelt gebucht")
    tmp = pfad + ".tmp"
    io.open(tmp, "w", encoding="utf-8").write(json.dumps(dict(daten, kennung=kennung),
                                                         ensure_ascii=False, indent=1))
    os.replace(tmp, pfad)

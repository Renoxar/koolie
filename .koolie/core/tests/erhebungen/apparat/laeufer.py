# -*- coding: utf-8 -*-
"""Der generische Laeufer: aufbauen, vorpruefen, fahren, auswerten, aufraeumen.

Ein Lauf faehrt genau dann, wenn (1) er noch nicht im Kontingentbuch steht, (2) der Baum
auf seinen Sollstand gebracht ist und (3) die Vorpruefung leer ist. Sonst bricht die
REIHE ab - nicht nur der Lauf: Ein Befund der Vorpruefung ist fast immer ein Befund am
Aufbau, und der naechste Lauf traege ihn mit.
"""
from __future__ import annotations

import io
import json
import os
import time

from . import baum as baum_mod
from . import belege as belege_mod
from . import kontingent
from . import vorpruefung
from .clients import ADAPTER, adapter as adapter_fuer
from .reihe import laden as reihe_laden

BEKANNT = tuple(ADAPTER)


def _soll_ordner(reihe) -> str:
    return os.path.join(reihe.belege, "soll")


def _soll_schreiben(reihe, schluessel: str, soll: dict) -> None:
    os.makedirs(_soll_ordner(reihe), exist_ok=True)
    io.open(os.path.join(_soll_ordner(reihe), schluessel + ".json"), "w",
            encoding="utf-8").write(json.dumps(soll, indent=1))


def _soll_lesen(reihe, schluessel: str) -> dict:
    pfad = os.path.join(_soll_ordner(reihe), schluessel + ".json")
    if not os.path.isfile(pfad):
        raise RuntimeError(f"kein Sollstand '{schluessel}' - erst 'aufbau'")
    return json.loads(io.open(pfad, encoding="utf-8").read())


def aufbau(reihe) -> list:
    """Sollstaende festhalten und Vertrauen setzen. Baut keine Basis - die sagt die Reihe."""
    belege_mod.ablage_pruefen(reihe.belege)
    a = adapter_fuer(reihe.client)
    ohne = reihe.baum.get("ohne") or []
    baeume = []
    if reihe.baum["modus"] == "vorhanden":
        for lauf in reihe.laeufe:
            if not os.path.isdir(lauf.baum_vorhanden):
                raise RuntimeError(f"{lauf.kennung}: Baum {lauf.baum_vorhanden} fehlt")
            _soll_schreiben(reihe, lauf.kennung, baum_mod.sollstand(lauf.baum_vorhanden, ohne))
            baeume.append(lauf.baum_vorhanden)
    else:
        basis = reihe.baum["basis"]
        _soll_schreiben(reihe, "basis", baum_mod.sollstand(basis, ohne))
        baeume = sorted({reihe.baumpfad(x) for x in reihe.laeufe})
    if reihe.vorpruefung.get("vertrauen"):
        a.vertrauen(baeume, True)
    return baeume


def _herrichten(reihe, lauf) -> tuple:
    """(Baumpfad, Sollstand fuer die Vorpruefung) - der Baum steht danach auf dem Soll."""
    ohne = reihe.baum.get("ohne") or []
    if reihe.baum["modus"] == "vorhanden":
        soll = _soll_lesen(reihe, lauf.kennung)
        return lauf.baum_vorhanden, soll
    soll = _soll_lesen(reihe, "basis")
    pfad = reihe.baumpfad(lauf)
    baum_mod.herrichten(reihe.baum["basis"], pfad, lauf.ziel_branch(reihe), soll,
                        reihe.baum.get("remote"), ohne, reihe.baum.get("verbindungen"),
                        reihe.baum.get("remote_hooks") or "")
    return pfad, soll


def vorpruefen(reihe, kennungen=None) -> dict:
    """Die Vorpruefung fuer jeden Lauf, ohne zu fahren - eine Probe des ganzen Aufbaus."""
    a = adapter_fuer(reihe.client)
    aus = {}
    for lauf in reihe.laeufe:
        if kennungen and lauf.kennung not in kennungen:
            continue
        if kontingent.gefahren(reihe.belege, lauf.kennung):
            aus[lauf.kennung] = ["(schon gefahren)"]
            continue
        pfad, soll = _herrichten(reihe, lauf)
        aus[lauf.kennung] = vorpruefung.pruefen(reihe, lauf, a, soll, pfad)
    return aus


def fahren(reihe, kennungen=None, ausgabe=print) -> int:
    a = adapter_fuer(reihe.client)
    version = a.version()
    gefahren = 0
    for lauf in reihe.laeufe:
        if kennungen and lauf.kennung not in kennungen:
            continue
        if kontingent.gefahren(reihe.belege, lauf.kennung):
            ausgabe(f"{lauf.kennung}: schon gefahren")
            continue
        pfad, soll = _herrichten(reihe, lauf)
        befunde = vorpruefung.pruefen(reihe, lauf, a, soll, pfad)
        if befunde:
            raise SystemExit(f"ABBRUCH vor {lauf.kennung} - Vorpruefung:\n  - " + "\n  - ".join(befunde))
        hash_vorher = baum_mod.baumhash(pfad, reihe.baum.get("ohne") or [])
        meta = {"reihe": reihe.name, "client": reihe.client, "clientversion": version,
                "gruppe": lauf.gruppe, "variante": lauf.variante, "baum": pfad,
                "branch": lauf.ziel_branch(reihe), "hash_vorher": hash_vorher,
                "berechtigung": reihe.berechtigung, "einstellungen": reihe.einstellungen or None,
                "zusatz": reihe.zusatz or None,
                "unterverzeichnis": lauf.unterverzeichnis or None,
                "zeit": time.strftime("%Y-%m-%dT%H:%M:%S")}
        start = os.path.join(pfad, *lauf.unterverzeichnis.split("/")) if lauf.unterverzeichnis else pfad
        if not os.path.isdir(start):
            raise SystemExit(f"ABBRUCH vor {lauf.kennung}: Startverzeichnis {start} fehlt im Baum")
        turns = [lauf.prompt] + lauf.folgeturns
        sitzung = None
        summe = {"usd": 0.0, "cache_neu": 0, "cache_gelesen": 0, "abweisungen": 0, "turns": 0}
        for i, prompt in enumerate(turns):
            erg = a.lauf(prompt, start, lauf.modell, reihe.berechtigung, sitzung,
                         einstellungen=reihe.einstellungen or None, zusatz=reihe.zusatz or None)
            belege_mod.sichern(reihe.belege, lauf.kennung, i, erg, dict(meta, turn=i + 1), a)
            summe["usd"] += erg["usd"]
            for k in ("cache_neu", "cache_gelesen", "abweisungen", "turns"):
                summe[k] += int(erg.get(k) or 0)
            sitzung = erg.get("sitzung") or sitzung
            if erg.get("is_error"):
                ausgabe(f"{lauf.kennung}: Turn {i + 1} meldet is_error - Folgeturns entfallen")
                break
        kontingent.eintragen(reihe.belege, lauf.kennung,
                             dict(meta, modell=erg.get("modell"), kosten=erg.get("kosten", "gemessen"),
                                  **{k: round(v, 4) if k == "usd" else v for k, v in summe.items()}))
        gefahren += 1
        ausgabe("%-24s %.3f USD  Abweisungen=%s  Cache neu/gelesen=%s/%s  erwartet: %s" % (
            lauf.kennung, summe["usd"], summe["abweisungen"], summe["cache_neu"],
            summe["cache_gelesen"], lauf.erwartung))
    n, usd = kontingent.summe(reihe.belege)
    ausgabe(f"Summe: {n} Laeufe, {usd:.2f} USD")
    return gefahren


def aufraeumen(reihe) -> None:
    """Vertrauen entfernen; die Baeume bleiben stehen (Loeschen sagt der Mensch, D-262)."""
    a = adapter_fuer(reihe.client)
    if reihe.baum["modus"] == "vorhanden":
        baeume = [x.baum_vorhanden for x in reihe.laeufe]
    else:
        baeume = sorted({reihe.baumpfad(x) for x in reihe.laeufe})
    a.vertrauen(baeume, False)


def laden(pfad: str):
    return reihe_laden(pfad, BEKANNT)

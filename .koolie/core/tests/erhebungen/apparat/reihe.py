# -*- coding: utf-8 -*-
"""Eine Reihe als Daten - und ihre Pruefung, bevor irgendetwas gebaut oder gefahren wird.

Die Reihe liegt als JSON in der Erhebungsablage, nicht im Repositorium: Prompts und
Erwartungen sind Aufzeichnung (D-222). Eine Reihe mit einem Fehler im Schema bricht beim
Laden ab - sie haette sonst die ersten Laeufe bezahlt und am fuenften gemerkt, dass eine
Kennung doppelt ist.

Form (Pflicht ist, was ohne Standard steht):

  {
    "name": "1190-gleich",
    "client": "claude-code",
    "wurzel": "Verzeichnis der Messbaeume",
    "kontingent": {"laeufe": 12, "usd": 8.0, "reserve_usd": 0.8},
    "baum": {"modus": "fest" | "je_lauf" | "vorhanden",
             "basis": "Pfad eines hergerichteten git-Baums (fest, je_lauf)",
             "branch": "main", "remote": false, "ohne": ["node_modules"],
             "verbindungen": {"frontend/node_modules": "geteilter Bestand"},
             "remote_hooks": "Verzeichnis mit Hooks fuer das Wegwerf-Remote"},
    "berechtigung": "bypassPermissions",
    "einstellungen": "Einstellungsdatei AUSSERHALB der Baeume (claude-code: --settings)",
    "zusatz": ["--mcp-config", "...", "--permission-prompt-tool", "..."],
    "vorpruefung": {"hook": true, "vertrauen": true, "startmeldung": []},
    "laeufe": [{"kennung": "...", "prompt": "..." | "prompt_datei": "...",
                "folgeturns": ["..."], "erwartung": "...",
                "gruppe": "koolie" | "referenz", "modell": null,
                "branch": null, "variante": null, "baum": "nur bei modus vorhanden",
                "unterverzeichnis": "Startverzeichnis relativ zum Baum, sonst die Wurzel"}]
  }

SEIT 1.21.0 (CR-2026-167) traegt die Reihe die Referenzgruppe der Vergleichsmessung (K-193):
Einstellungen, die der Agent nicht aendern kann, liegen ausserhalb jedes Baums; Branch-Schutz
und CI stehen als Hooks im Wegwerf-Remote; ein Lauf kann in einem Unterverzeichnis starten.
'zusatz' reicht Argumente an den Client durch - etwa den Freigabe-Stellvertreter (freigabe.py),
der im Druckmodus jede Rueckfrage beantwortet und protokolliert.
"""
from __future__ import annotations

import io
import json
import os
import re

MODI = ("fest", "je_lauf", "vorhanden")
GRUPPEN = ("koolie", "referenz")
KENNUNG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,40}$")


class Reihenfehler(Exception):
    """Die Reihe ist nicht fahrbar - gemeldet vor dem ersten Lauf."""


class Lauf:
    def __init__(self, d: dict, reihe: "Reihe") -> None:
        self.kennung = d.get("kennung", "")
        self.erwartung = d.get("erwartung", "")
        self.gruppe = d.get("gruppe", "koolie")
        self.modell = d.get("modell") or reihe.modell
        self.branch = d.get("branch")
        self.variante = d.get("variante")
        self.unterverzeichnis = (d.get("unterverzeichnis") or "").replace("\\", "/").strip("/")
        self.baum_vorhanden = d.get("baum")
        self.folgeturns = list(d.get("folgeturns") or [])
        if "prompt_datei" in d:
            pfad = d["prompt_datei"]
            if not os.path.isabs(pfad):
                pfad = os.path.join(reihe.ablage, pfad)
            self.prompt = io.open(pfad, encoding="utf-8").read() if os.path.isfile(pfad) else ""
            self.prompt_quelle = pfad
        else:
            self.prompt = d.get("prompt", "")
            self.prompt_quelle = "reihe"

    def ziel_branch(self, reihe: "Reihe") -> str:
        return self.branch or reihe.baum.get("branch", "main")


class Reihe:
    def __init__(self, d: dict, ablage: str) -> None:
        self.roh = d
        self.ablage = ablage
        self.name = d.get("name", "")
        self.client = d.get("client", "")
        self.wurzel = d.get("wurzel", "")
        self.modell = d.get("modell")
        k = d.get("kontingent") or {}
        self.max_laeufe = int(k.get("laeufe", 0))
        self.max_usd = float(k.get("usd", 0))
        self.reserve_usd = float(k.get("reserve_usd", 0.8))
        self.baum = dict(d.get("baum") or {})
        self.baum.setdefault("branch", "main")
        self.baum.setdefault("remote", False)
        self.baum.setdefault("ohne", ["node_modules"])
        self.baum.setdefault("verbindungen", {})
        self.baum.setdefault("remote_hooks", "")
        self.berechtigung = d.get("berechtigung", "default")
        self.einstellungen = d.get("einstellungen") or ""
        self.zusatz = [str(x) for x in d.get("zusatz") or []]
        if self.einstellungen and not os.path.isabs(self.einstellungen):
            self.einstellungen = os.path.join(ablage, self.einstellungen)
        v = dict(d.get("vorpruefung") or {})
        v.setdefault("hook", True)
        v.setdefault("vertrauen", True)
        v.setdefault("startmeldung", [])
        self.vorpruefung = v
        self.laeufe = [Lauf(x, self) for x in d.get("laeufe") or []]

    @property
    def belege(self) -> str:
        return os.path.join(self.ablage, "belege", self.name)

    def lauf(self, kennung: str) -> Lauf:
        for x in self.laeufe:
            if x.kennung == kennung:
                return x
        raise Reihenfehler(f"keine Kennung '{kennung}' in der Reihe '{self.name}'")

    def baumpfad(self, lauf: Lauf) -> str:
        """Fester Pfad je Reihe (ein Prompt-Anfang, ein Cache) oder ein Baum je Lauf."""
        modus = self.baum.get("modus")
        if modus == "vorhanden":
            return lauf.baum_vorhanden
        if modus == "fest":
            return os.path.join(self.wurzel, self.name)
        return os.path.join(self.wurzel, self.name + "-" + lauf.kennung)


def _unter(pfad: str, wurzel: str) -> bool:
    p = os.path.normcase(os.path.abspath(pfad))
    w = os.path.normcase(os.path.abspath(wurzel)).rstrip("\\/") + os.sep
    return p.startswith(w)


def pruefen(r: Reihe, clients_bekannt) -> list:
    """Alle Schemafehler auf einmal - nicht den ersten."""
    f = []
    if not KENNUNG_RE.match(r.name or ""):
        f.append(f"name '{r.name}': Kleinbuchstaben, Ziffern, Bindestrich")
    if r.client not in clients_bekannt:
        f.append(f"client '{r.client}' hat keinen Adapter (bekannt: {', '.join(sorted(clients_bekannt))})")
    if r.max_laeufe <= 0 or r.max_usd <= 0:
        f.append("kontingent: laeufe und usd muessen gesagt sein - ein Apparat ohne Deckel zaehlt nur")
    modus = r.baum.get("modus")
    if modus not in MODI:
        f.append(f"baum.modus '{modus}' - erlaubt: {', '.join(MODI)}")
    if modus in ("fest", "je_lauf"):
        if not r.wurzel:
            f.append("wurzel fehlt")
        if not r.baum.get("basis"):
            f.append("baum.basis fehlt")
    if r.einstellungen:
        if not os.path.isfile(r.einstellungen):
            f.append(f"einstellungen '{r.einstellungen}' fehlt")
        elif r.wurzel and _unter(r.einstellungen, r.wurzel):
            f.append("einstellungen liegen unter der wurzel - im Messbaum erreichbar, keine "
                     "Referenz (1.21.0)")
    for rel, quelle in (r.baum.get("verbindungen") or {}).items():
        teile = rel.replace("\\", "/").split("/")
        if os.path.isabs(rel) or ".." in teile:
            f.append(f"verbindungen: '{rel}' muss relativ im Baum liegen")
        if not os.path.isdir(quelle):
            f.append(f"verbindungen: Quelle '{quelle}' fehlt")
    if r.baum.get("remote_hooks"):
        if not r.baum.get("remote"):
            f.append("remote_hooks ohne remote")
        elif not os.path.isdir(r.baum["remote_hooks"]):
            f.append(f"remote_hooks '{r.baum['remote_hooks']}' fehlt")
    gesehen = set()
    for x in r.laeufe:
        if not KENNUNG_RE.match(x.kennung or ""):
            f.append(f"Kennung '{x.kennung}': Kleinbuchstaben, Ziffern, Bindestrich")
        if x.kennung in gesehen:
            f.append(f"Kennung '{x.kennung}' doppelt")
        gesehen.add(x.kennung)
        if not x.prompt.strip():
            f.append(f"{x.kennung}: Prompt leer ({x.prompt_quelle})")
        if any(not t.strip() for t in x.folgeturns):
            f.append(f"{x.kennung}: ein Folgeturn ist leer - Abbruch statt Rueckfall (1.14.2)")
        if not x.erwartung.strip():
            f.append(f"{x.kennung}: keine Erwartung - ein Lauf ohne Erwartung misst nichts")
        if x.gruppe not in GRUPPEN:
            f.append(f"{x.kennung}: gruppe '{x.gruppe}' - erlaubt: {', '.join(GRUPPEN)}")
        if x.unterverzeichnis and (os.path.isabs(x.unterverzeichnis) or ":" in x.unterverzeichnis
                                   or ".." in x.unterverzeichnis.split("/")):
            f.append(f"{x.kennung}: unterverzeichnis '{x.unterverzeichnis}' muss im Baum liegen")
        if modus == "vorhanden" and not x.baum_vorhanden:
            f.append(f"{x.kennung}: bei modus 'vorhanden' braucht jeder Lauf 'baum'")
        if modus == "fest" and x.branch and not x.branch.startswith("arbeit/"):
            f.append(f"{x.kennung}: ein eigener Branch heisst 'arbeit/...' (K-172)")
    if not r.laeufe:
        f.append("keine Laeufe")
    return f


def laden(pfad: str, clients_bekannt) -> Reihe:
    d = json.loads(io.open(pfad, encoding="utf-8").read())
    r = Reihe(d, os.path.dirname(os.path.abspath(pfad)))
    fehler = pruefen(r, clients_bekannt)
    if fehler:
        raise Reihenfehler("Reihe nicht fahrbar:\n  - " + "\n  - ".join(fehler))
    return r

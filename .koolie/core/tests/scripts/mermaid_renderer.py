#!/usr/bin/env python3
"""
Gemeinsamer Aufruf des Mermaid-Renderers - fuer den Validator und die Word-Fassung.

Warum dieses Modul existiert (K-145, D-398): Der Bau (`build/build-docx.py`) uebergab dem
Renderer `mmdc` eine Puppeteer-Konfiguration mit einem gefundenen Browser, der Validator
(`validate-framework.py --mermaid`) nicht. Auf einem Arbeitsplatz ohne den Browser, den
Puppeteer selbst herunterlaedt, meldete der Validator deshalb JEDEN Mermaid-Block als
ungueltig - auch unveraenderte -, waehrend der Bau im selben Arbeitsgang alle Diagramme
renderte. Gemessen am 2026-09-25: ohne die Konfiguration "Could not find
chrome-headless-shell", mit ihr gerendert. Beide Werkzeuge suchen den Browser jetzt hier.

Das Modul hat keine Abhaengigkeit ausser der Standardbibliothek, weil der Validator auch
in einer Installation ohne `build/` laeuft (Lieferumfang `nutzung`, D-367).

WAS DIESES MODUL NICHT LEISTET: Es unterscheidet einen Fehler der Umgebung von einem Fehler
des Diagramms nur an der Fehlerausgabe des Renderers. Eine Meldung, die es nicht kennt,
gilt als Fehler des Diagramms - die strengere Lesart.
"""
from __future__ import annotations

import json
import os
import re

# Meldungen, mit denen der Renderer sagt, dass ihm der Browser fehlt oder nicht startet.
# Sie betreffen den Arbeitsplatz, nicht das Diagramm.
UMGEBUNGSFEHLER_RE = re.compile(
    r"Could not find (?:Chrome|Chromium|chrome-headless-shell|expected browser)"
    r"|Failed to launch the browser process"
    r"|Browser was not found",
    re.I)


def browserpfad() -> str | None:
    """Ein Chromium-artiger Browser fuer den Mermaid-Renderer - oder None.

    Zuerst die ausdrueckliche Angabe der Umgebung, dann die ueblichen Ablageorte. Auf
    einem Windows-Arbeitsplatz ist Edge immer vorhanden; einen eigenen Chromium
    herunterzuladen ist damit unnoetig.
    """
    gesetzt = os.environ.get("PUPPETEER_EXECUTABLE_PATH")
    if gesetzt and os.path.exists(gesetzt):
        return gesetzt
    kandidaten = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome",
    ]
    for pfad in kandidaten:
        if os.path.exists(pfad):
            return pfad
    return None


def puppeteer_konfiguration(pfad: str, browser: str) -> str:
    """Schreibt die Konfiguration, die `mmdc -p` liest, und gibt ihren Pfad zurueck."""
    with open(pfad, "w", encoding="utf-8") as fh:
        json.dump({"executablePath": browser,
                   "args": ["--no-sandbox", "--disable-gpu"]}, fh)
    return pfad


def ist_umgebungsfehler(fehlerausgabe: str) -> bool:
    """True, wenn der Renderer an der Umgebung gescheitert ist und nicht am Diagramm."""
    return bool(UMGEBUNGSFEHLER_RE.search(fehlerausgabe or ""))

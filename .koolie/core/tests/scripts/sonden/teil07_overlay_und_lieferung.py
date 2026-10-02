"""Sonden zum Wert- und Pfadabgleich des Overlays (Pruefungen 59 und 89), zu den Overlay-
Mustern, zum Kopierweg, zum Lieferumfang (Pruefung 90) und zum Lauf ohne PyYAML.

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul
liest nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

from .apparat import (
    aufraeumen, baumhash, buendel, ersetzt, installation, kopie, lies, melde, notiz, P,
    Praeparationsfehler, QUELLE, schreib, sonde, strict_ausgabe, unterprozess,
    VALIDATOR, validator_ausgabe)


# --- Pruefung 59: der Overlay-Wert in der Schicht, die ihn durchsetzt (D-171) ------
#
# Sie braucht eine GEFUELLTE Installation: Im Framework-Repositorium traegt das
# Beispiel-Overlay Ausfuellschlitze, und die Pruefung enthaelt sich dort - richtigerweise,
# denn ein offener Schlitz ist Sache von --check-overlay-ready. Die drei Sonden treffen
# die drei Gegenstaende; die Gegenprobe belegt den vollstaendig nachgezogenen Zustand,
# und sie ist der eigentliche Nachweis: Ohne sie stuende nur fest, dass die Pruefung
# etwas meldet, nicht dass ein richtiger Baum sie schweigen laesst.
M59_BINDUNG = "nennt <EXCLUDED_PATHS> nicht"
M59_WERT = "weichen vom Quell-Overlay ab"
M59_KORB = "keine Regel"
P59_QUELLGLOBS = ["deploy/**", "infra/**"]
P59_SCHLITZ = ("`<TBD: z. B. deploy/**, infra/**, config/prod/**, "
               "**/fixtures/real/**>`")
_59_KORBSTAND: dict = {}


def _59_pfade(root: str) -> tuple:
    return (os.path.join(root, ".koolie/project-overlay", "OVERLAY.md"),
            os.path.join(root, ".claude", "rules", "20-project-overlay.md"),
            os.path.join(root, ".claude", "settings.json"))


def _59_quelle_fuellen(root: str) -> None:
    """Den Ausfuellschlitz des Quell-Overlays einmal durch die Globmenge ersetzen."""
    quelle, _, _ = _59_pfade(root)
    schreib(quelle, ersetzt(lies(quelle),
                            (P59_SCHLITZ, ", ".join("`%s`" % g for g in P59_QUELLGLOBS)),
                            quelle=".koolie/project-overlay/OVERLAY.md"))


def _59_fuellen(root: str, globs: list, im_korb: list = None) -> None:
    """Laufzeitfassung und deny-Korb auf eine Globmenge stellen - mehrfach aufrufbar.

    Die Quelle bleibt unberuehrt: Ihr Ausfuellschlitz gibt es nur einmal, und eine
    Praeparation, die ihn ein zweites Mal sucht, bricht ab. Das ist am 2026-09-18
    zugeschnappt.
    """
    _, laufzeit, korb = _59_pfade(root)
    text = lies(laufzeit)
    treffer = [z for z in text.split("\n") if "<EXCLUDED_PATHS>" in z]
    if len(treffer) != 1:
        raise Praeparationsfehler(
            "Die Laufzeitfassung nennt <EXCLUDED_PATHS> %dx statt 1x - die Sonden zu 59 "
            "haetten keinen Anker" % len(treffer))
    neu = treffer[0].split(":")[0] + ": " + ", ".join("`%s`" % g for g in globs)
    schreib(laufzeit, text.replace(treffer[0], neu))
    cfg = json.loads(lies(korb))
    # Der Korb wird aus dem UNBERUEHRTEN Stand neu aufgebaut, nicht aus dem der
    # vorigen Sonde: Ein Baum, der mehrere Laeufe traegt, ist nach dem ersten
    # Schreiblauf nicht mehr der Ausgangszustand. Ohne diesen Merker stand ein Glob
    # der vorigen Sonde noch im Korb, und 59c mass nichts - zugeschnappt am 2026-09-18.
    urstand = _59_KORBSTAND.setdefault(
        korb, [r for r in cfg["permissions"]["deny"] if "<EXCLUDED_PATHS>" not in r])
    deny = list(urstand)
    for g in (P59_QUELLGLOBS if im_korb is None else im_korb):
        deny += ["Read(%s)" % g, "Edit(%s)" % g]
    cfg["permissions"]["deny"] = deny
    schreib(korb, json.dumps(cfg, ensure_ascii=False, indent=2))


def sonden_overlay_wertabgleich() -> None:
    """Wirkungsnachweis fuer Pruefung 59 an einer gefuellten claude-code-Installation."""
    root = installation("claude-code")
    try:
        # --- Gegenprobe: alle drei Schichten tragen denselben Wert ------------------
        _59_quelle_fuellen(root)
        _59_fuellen(root, P59_QUELLGLOBS)
        aus = strict_ausgabe(root)
        for nummer, marke, satz in (
                ("59a", M59_BINDUNG, "Die Laufzeitfassung bindet den Platzhalter"),
                ("59b", M59_WERT, "Ihre Globmenge ist die der Quelle"),
                ("59c", M59_KORB, "Der deny-Korb fuehrt jeden Glob zweimal")):
            melde("GEGENPROBE", nummer, marke not in aus,
                  "Ein vollstaendig nachgezogener Baum bleibt unbeanstandet - %s" % satz)

        # --- Sonde 59b: derselbe Platzhalter, ein anderer Wert ---------------------
        # Vor 59a, weil 59a den Platzhalter aus der Laufzeitfassung entfernt und
        # _59_fuellen ihn danach als Anker nicht mehr faende.
        _59_fuellen(root, ["deploy/**", "infra/gen/**"])
        melde("SONDE", "59b", M59_WERT in strict_ausgabe(root),
              "Die Laufzeitfassung traegt einen Glob, den die Quelle nicht kennt - genau "
              "die Drift, die eine Einengung aus 0.63.0 nie erreicht hat")

        # --- Sonde 59c: der deny-Korb fuehrt einen Glob der Quelle nicht ------------
        _59_fuellen(root, P59_QUELLGLOBS, im_korb=["deploy/**"])
        melde("SONDE", "59c", M59_KORB in strict_ausgabe(root),
              "Ein ausgeschlossener Pfad der Quelle hat keine Regel im deny-Korb - die "
              "Schicht, die technisch sperrt, kennt ihn nicht")

        # --- Sonde 59a: die Laufzeitfassung ERSETZT statt zu BINDEN -----------------
        _59_fuellen(root, P59_QUELLGLOBS)
        _, laufzeit, _ = _59_pfade(root)
        schreib(laufzeit, lies(laufzeit).replace("(`<EXCLUDED_PATHS>`)", "").replace(
            "<EXCLUDED_PATHS>", "die Liste unten"))
        melde("SONDE", "59a", M59_BINDUNG in strict_ausgabe(root),
              "Die Laufzeitfassung setzt den Wert ein, statt den Platzhalter zu binden - "
              "niemand sieht dann, ob ihr Wert noch der der Quelle ist")
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_overlay_wertabgleich,
        "Pruefung 59 an einer gefuellten claude-code-Installation: Bindung, Wert und "
        "deny-Korb je eigens gemessen, dazu die Gegenprobe des nachgezogenen Baums")


# --- Pruefung 89: die uebrigen Pfadplatzhalter (K-69, D-357) ----------------------
#
# Dieselbe Bauform wie das Buendel zu 59: eine GEFUELLTE claude-code-Installation, je
# Gegenstand eine Sonde, und die Gegenprobe des vollstaendig nachgezogenen Baums ist der
# eigentliche Nachweis. Jede Einheit baut die drei Traeger aus dem UNBERUEHRTEN Stand
# neu auf (_89_URSTAND) - ein Baum, der mehrere Laeufe traegt, ist nach dem ersten
# Schreiblauf nicht mehr der Ausgangszustand (dieselbe Falle wie 59c am 2026-09-18).
#   89   (Gegenprobe) - alle vier Werte in Quelle, Laufzeitfassung und Korb gleich
#   89k  (Gegenprobe) - "kein Wert" in zwei Schreibweisen: `nicht vorhanden` in der
#                       Quelle, `keine` in der Laufzeitfassung - gemessen am Piloten
#   89a  (Sonde)      - die Laufzeitfassung ersetzt <ALLOWED_PATHS>, statt zu binden
#   89b  (Sonde)      - <TEST_PATHS> traegt in der Laufzeitfassung einen anderen Wert
#   89c  (Sonde)      - ein Nur-Lese-Pfad fehlt im deny-Korb
#   89d  (Sonde)      - die Quelle bindet <DOC_PATHS> nicht in der dreispaltigen Zeile
M89_BINDUNG = "nennt <ALLOWED_PATHS> nicht"
M89_WERT = "der Wert von <TEST_PATHS> weicht vom Quell-Overlay ab"
M89_KORB = "hat keine Regel Edit(api-contracts/**)"
M89_QUELLE = "keine Zeile mit der Platzhalterzelle `<DOC_PATHS>`"
M89_ALLE = ("nennt <", "weicht vom Quell-Overlay ab", "Nur-Lese-Pfad",
            "keine Zeile mit der Platzhalterzelle")
P89_WERTE = {"<ALLOWED_PATHS>": ["src/**", "test/**", "docs/**"],
             "<TEST_PATHS>": ["test/**"],
             "<DOC_PATHS>": ["docs/**"],
             "<READ_ONLY_PATHS>": ["api-contracts/**", "db/migrations/**"]}
_89_URSTAND: dict = {}


def _89_pfade(root: str) -> tuple:
    return (os.path.join(root, ".koolie/project-overlay", "OVERLAY.md"),
            os.path.join(root, ".claude", "rules", "20-project-overlay.md"),
            os.path.join(root, ".claude", "settings.json"))


def _89_fuellen(root: str, quelle: dict, laufzeit: dict, korb: list) -> None:
    """Quelle, Laufzeitfassung und deny-Korb aus dem Urstand auf die Werte stellen.

    quelle und laufzeit bilden den Platzhalter auf den eingesetzten TEXT ab (fertig mit
    Codespannen); korb nennt die Nur-Lese-Globs, die eine Schreibsperre bekommen. Jeder
    Ausfuellschlitz muss genau einmal getroffen werden, sonst bricht die Praeparation ab.
    """
    for pfad in _89_pfade(root):
        _89_URSTAND.setdefault(pfad, lies(pfad))
    q_pfad, l_pfad, k_pfad = _89_pfade(root)
    text = _89_URSTAND[q_pfad]
    for platzhalter, ersatz in quelle.items():
        text, n = re.subn(r"(\| `%s` \| )`<TBD[^`]*>`" % re.escape(platzhalter),
                          lambda m: m.group(1) + ersatz, text)
        if n != 1:
            raise Praeparationsfehler("OVERLAY.md: Wertzeile von %s %dx statt 1x"
                                      % (platzhalter, n))
    schreib(q_pfad, text)
    text = _89_URSTAND[l_pfad]
    for platzhalter, ersatz in laufzeit.items():
        text, n = re.subn(r"(\(`%s`\): )`<TBD[^`]*>`" % re.escape(platzhalter),
                          lambda m: m.group(1) + ersatz, text)
        if n != 1:
            raise Praeparationsfehler("20-project-overlay.md: Schlitz von %s %dx statt 1x"
                                      % (platzhalter, n))
    schreib(l_pfad, text)
    cfg = json.loads(_89_URSTAND[k_pfad])
    deny = [r for r in cfg["permissions"]["deny"] if "<READ_ONLY_PATHS>" not in r]
    if len(deny) != len(cfg["permissions"]["deny"]) - 1:
        raise Praeparationsfehler("settings.json: der Schlitz Edit(<READ_ONLY_PATHS>) steht "
                                  "nicht genau einmal im deny-Korb (D-356)")
    cfg["permissions"]["deny"] = deny + ["Edit(%s)" % g for g in korb]
    schreib(k_pfad, json.dumps(cfg, ensure_ascii=False, indent=2))


def _89_spannen(werte: list) -> str:
    return ", ".join("`%s`" % w for w in werte)


def _89_voll() -> tuple:
    werte = {p: _89_spannen(w) for p, w in P89_WERTE.items()}
    return werte, dict(werte), list(P89_WERTE["<READ_ONLY_PATHS>"])


def sonden_overlay_pfadabgleich() -> None:
    """Wirkungsnachweis fuer Pruefung 89 an einer gefuellten claude-code-Installation."""
    root = installation("claude-code")
    try:
        # --- Gegenprobe 89: alle drei Schichten tragen dieselben vier Werte ---------
        _89_fuellen(root, *_89_voll())
        aus = strict_ausgabe(root)
        treffer = [m for m in M89_ALLE if m in aus]
        melde("GEGENPROBE", "89", not treffer,
              "Ein vollstaendig nachgezogener Baum bleibt unbeanstandet - vier Werte in "
              "Quelle, Laufzeitfassung und deny-Korb gleich")
        if treffer:
            notiz("        gemeldet: %s" % ", ".join(treffer))

        # --- Gegenprobe 89k: zwei Schreibweisen fuer "kein Wert" -------------------
        quelle, laufzeit, korb = _89_voll()
        quelle["<DOC_PATHS>"] = "`nicht vorhanden`"
        laufzeit["<DOC_PATHS>"] = "keine"
        _89_fuellen(root, quelle, laufzeit, korb)
        melde("GEGENPROBE", "89k", "<DOC_PATHS>" not in strict_ausgabe(root),
              "Kein Wert in zwei Schreibweisen - nicht vorhanden in der Quelle, keine in "
              "der Laufzeitfassung - ist dieselbe leere Menge")

        # --- Sonde 89a: die Laufzeitfassung ersetzt statt zu binden -----------------
        _89_fuellen(root, *_89_voll())
        _, l_pfad, _ = _89_pfade(root)
        schreib(l_pfad, ersetzt(lies(l_pfad), (" (`<ALLOWED_PATHS>`)", ""),
                                quelle="20-project-overlay.md"))
        melde("SONDE", "89a", M89_BINDUNG in strict_ausgabe(root),
              "Die Laufzeitfassung setzt die erlaubten Pfade ein, statt den Platzhalter zu "
              "binden - ihr Wert ist dann gegen nichts mehr gehalten")

        # --- Sonde 89b: ein anderer Wert in der Laufzeitfassung --------------------
        quelle, laufzeit, korb = _89_voll()
        laufzeit["<TEST_PATHS>"] = "`test/**`, `src/**`"
        _89_fuellen(root, quelle, laufzeit, korb)
        melde("SONDE", "89b", M89_WERT in strict_ausgabe(root),
              "Die Laufzeitfassung erlaubt Schreiben in M4 auf einem Pfad, den die Quelle "
              "nicht nennt - genau die Drift aus K-69")

        # --- Sonde 89c: ein Nur-Lese-Pfad ohne Schreibsperre -----------------------
        quelle, laufzeit, _ = _89_voll()
        _89_fuellen(root, quelle, laufzeit, ["db/migrations/**"])
        melde("SONDE", "89c", M89_KORB in strict_ausgabe(root),
              "Ein Nur-Lese-Pfad der Quelle hat keine Schreibsperre im deny-Korb - der "
              "Integritaetsschutz steht nur im Overlay")

        # --- Sonde 89d: die Quelle bindet anders ------------------------------------
        _89_fuellen(root, *_89_voll())
        q_pfad, _, _ = _89_pfade(root)
        schreib(q_pfad, ersetzt(lies(q_pfad), ("| `<DOC_PATHS>` |", "| DOC_PATHS |"),
                                quelle="OVERLAY.md"))
        melde("SONDE", "89d", M89_QUELLE in strict_ausgabe(root),
              "Ein Overlay, das einen Pfadplatzhalter nicht in der dreispaltigen Zeile "
              "bindet, wird gemeldet und nicht still uebergangen")
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_overlay_pfadabgleich,
        "Pruefung 89 an einer gefuellten claude-code-Installation: Bindung, Wert, deny-Korb "
        "und Lesbarkeit der Quelle, dazu zwei Gegenproben")


# --- D-355: das Overlay-Muster und der Fuellschritt --------------------------------
#
# ANLASS (CR-2026-136, 2.3; CR-2026-138). Ein Muster, das nur OVERLAY.md vorbefuellt,
# sperrt nichts: Read(<EXCLUDED_PATHS>) stand danach woertlich im deny-Korb. Diese
# Einheiten messen den Fuellschritt an einer echten Erstinstallation - und die vier
# Stellen, an denen er sich verweigern MUSS.
#   M355  (Sonde)      - --overlay general fuellt Overlay, Laufzeitfassung und deny-Korb
#                        aus derselben Tabelle; Pruefung 59 schweigt. Gegen install.py
#                        aus 1.4.4 faellt sie (die Option gibt es dort nicht)
#   M355a (Gegenprobe) - ohne --overlay bleibt alles wie vorher: der Schlitz steht
#                        woertlich im Korb, dazu seit D-356 der Nur-Lese-Schlitz
#   M355b (Sonde)      - ein Overlay aus dem Muster ist NICHT aktivierungsreif (D-57)
#   M355c (Sonde)      - vorhandene Saat: Abbruch, nichts ueberschrieben
#   M355d (Sonde)      - ein Muster, das einen freigebenden Platzhalter fuellt: Abbruch
#                        vor dem ersten Schreibvorgang
#   M355e (Sonde)      - --overlay mit --update und ein unbekannter Name: Abbruch
M355_MUSTER = os.path.join(".koolie", "core", "framework", "overlay-patterns", "general.md")
M355_59 = ("nennt <EXCLUDED_PATHS> nicht", "weichen vom Quell-Overlay ab",
           "der ausgeschlossene Pfad")


def _355_install(ziel: str, *argumente) -> subprocess.CompletedProcess:
    return unterprozess([sys.executable, os.path.join(QUELLE, ".koolie/core", "install.py"),
                         "--client", "claude-code", "--root", ziel] + list(argumente))


#   M359  (Sonde)      - die Dokumente des Musters: angelegt, mit Vermerk, im Manifest
#                        als K1/entwurf/on-demand registriert, die Beispiele der Vorlage
#                        ersetzt, die K1-Liste der Laufzeitfassung offen (D-359, D-360)
#   M359a (Sonde)      - Ablage und Beschreibung laufen auseinander: Abbruch vor dem
#                        ersten Schreibvorgang
#   M359b (Sonde)      - ein Dokument ohne Vorschlagsvermerk: Abbruch
#   M359c (Gegenprobe) - ohne --overlay bleibt die Manifestvorlage mit ihren drei
#                        Beispielen, und kein Musterdokument liegt im Projekt
M359_VERMERK = "Muster – vom Overlay Owner zu prüfen und anzupassen."


def _359_dokumente() -> list:
    """Die Dokumente des Musters, gelesen mit dem Werkzeug selbst - nicht nachgepflegt."""
    sys.path.insert(0, os.path.join(QUELLE, ".koolie", "core"))
    try:
        import install as _install  # noqa: E402
        return _install.muster_laden("general")["dokumente"]
    finally:
        sys.path.pop(0)


def _359_kern(basis: str, name: str) -> str:
    """Eine Kopie des Kerns, deren install.py das Muster aus IHREM Kern liest."""
    kern = os.path.join(basis, name, ".koolie", "core")
    shutil.copytree(os.path.join(QUELLE, ".koolie/core"), kern,
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "out"))
    return kern


def _355_werte() -> dict:
    """Die Werte des Musters, gelesen mit dem Werkzeug selbst - nicht nachgepflegt."""
    sys.path.insert(0, os.path.join(QUELLE, ".koolie", "core"))
    try:
        import install as _install  # noqa: E402
        return _install.muster_laden("general")["werte"]
    finally:
        sys.path.pop(0)


def sonden_overlay_muster() -> None:
    """Wirkungsnachweis fuer --overlay general, seine Dokumente und seine sechs Verweigerungen."""
    basis = tempfile.mkdtemp(prefix="lw-muster-")
    try:
        werte = _355_werte()
        # --- M355: die Fuellung ---------------------------------------------------
        root = os.path.join(basis, "mit")
        os.makedirs(root)
        p = _355_install(root, "--overlay", "general")
        deny = json.loads(lies(os.path.join(root, ".claude", "settings.json")))[
            "permissions"]["deny"]
        fehlt = []
        for platzhalter, liste in werte.items():
            if any(platzhalter in r for r in deny):
                fehlt.append("%s noch als Schlitz" % platzhalter)
            for w in liste:
                if not any(r in deny for r in ("Edit(%s)" % w, "Edit(./%s)" % w)):
                    fehlt.append("Edit(%s)" % w)
        for w in werte["<EXCLUDED_PATHS>"]:
            if "Read(%s)" % w not in deny and "Read(./%s)" % w not in deny:
                fehlt.append("Read(%s)" % w)
        laufzeit = lies(os.path.join(root, ".claude", "rules", "20-project-overlay.md"))
        if "(`<EXCLUDED_PATHS>`): " + ", ".join(
                "`%s`" % w for w in werte["<EXCLUDED_PATHS>"]) not in laufzeit:
            fehlt.append("Laufzeitfassung")
        overlay = lies(os.path.join(root, ".koolie", "project-overlay", "OVERLAY.md"))
        for platzhalter, liste in werte.items():
            if "| `%s` | %s |" % (platzhalter, ", ".join("`%s`" % w for w in liste)) \
                    not in overlay:
                fehlt.append("OVERLAY.md %s" % platzhalter)
        if "Overlay angelegt aus dem Muster `general`" not in overlay:
            fehlt.append("Aenderungsverlauf")
        shutil.copytree(os.path.join(QUELLE, ".koolie/core"),
                        os.path.join(root, ".koolie/core"),
                        ignore=shutil.ignore_patterns(".git", "__pycache__", "out"))
        aus59 = [m for m in M355_59 if m in strict_ausgabe(root)]
        melde("SONDE", "M355", p.returncode == 0 and not fehlt and not aus59,
              "Das Muster fuellt Overlay, Laufzeitfassung und deny-Korb aus einer Tabelle, "
              "und Pruefung 59 findet keine Abweichung")
        if p.returncode != 0 or fehlt or aus59:
            notiz("        Exit %d; fehlt: %s; Pruefung 59: %s"
                  % (p.returncode, ", ".join(fehlt) or "nichts", ", ".join(aus59) or "still"))

        # --- M359: die Dokumente des Musters (D-359, D-360) ---------------------------
        dokumente = _359_dokumente()
        fehlt = []
        manifest = lies(os.path.join(root, ".koolie", "project-overlay",
                                     "overlay-manifest.yaml"))
        for dok in dokumente:
            ziel = os.path.join(root, ".koolie", "project-overlay", "documents",
                                dok["typ"], dok["datei"])
            if not os.path.isfile(ziel):
                fehlt.append("%s/%s fehlt" % (dok["typ"], dok["datei"]))
            elif M359_VERMERK not in lies(ziel):
                fehlt.append("%s ohne Vermerk" % dok["typ"])
            eintrag = 'path: ".koolie/project-overlay/documents/%s/%s"' % (
                dok["typ"], dok["datei"])
            if eintrag not in manifest:
                fehlt.append("%s nicht registriert" % dok["typ"])
        for erwartet in ('status: "entwurf"', 'load: "on-demand"', 'context_class: "K1"'):
            if manifest.count(erwartet) != len(dokumente):
                fehlt.append("%s %dx statt %dx" % (erwartet, manifest.count(erwartet),
                                                   len(dokumente)))
        if manifest.count('- id: "DOC-') != len(dokumente):
            fehlt.append("%d Eintraege statt %d - ein Beispiel der Vorlage steht noch"
                         % (manifest.count('- id: "DOC-'), len(dokumente)))
        if "- Dokumente der Klasse K1 (frei nutzbar): `<TBD" not in laufzeit:
            fehlt.append("K1-Liste der Laufzeitfassung gefuellt")
        if "Musterdokumente unter `documents/`" not in overlay:
            fehlt.append("Aenderungsverlauf ohne Dokumente")
        aus8 = [z for z in validator_ausgabe(root).splitlines()
                if z.startswith("FEHLER") and "overlay-manifest.yaml" in z]
        melde("SONDE", "M359", p.returncode == 0 and len(dokumente) == 6 and not fehlt
              and not aus8,
              "Das Muster legt seine sechs Dokumente an, registriert sie als Entwurf und "
              "gibt keines frei; Pruefung 8 bleibt still")
        if fehlt or aus8 or len(dokumente) != 6:
            notiz("        %d Dokumente; fehlt: %s; Pruefung 8: %s"
                  % (len(dokumente), ", ".join(fehlt) or "nichts",
                     " | ".join(aus8) or "still"))

        # --- M355b: nicht aktivierungsreif -----------------------------------------
        q = unterprozess([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                          "--root", root, "--check-overlay-ready"])
        reif = (q.stdout or "") + (q.stderr or "")
        melde("SONDE", "M355b", q.returncode != 0 and "offene <TBD>-Werte" in reif,
              "Ein Overlay aus dem Muster besteht die Pruefung der Aktivierungsreife nicht - "
              "es laesst die Pflichtwerte offen (D-57)")

        # --- M355c: vorhandene Saat -------------------------------------------------
        vorher = lies(os.path.join(root, ".claude", "settings.json"))
        c = _355_install(root, "--overlay", "general")
        melde("SONDE", "M355c", c.returncode == 1 and "hier liegt sie schon" in
              (c.stderr or "") and lies(os.path.join(root, ".claude", "settings.json"))
              == vorher,
              "Liegt die Saat schon, bricht das Muster ab und ueberschreibt nichts - "
              "vorhandene Saat gehoert dem Projekt")

        # --- M355e: --update und unbekannter Name ----------------------------------
        u = _355_install(root, "--overlay", "general", "--update")
        leer = os.path.join(basis, "unbekannt")
        os.makedirs(leer)
        n = _355_install(leer, "--overlay", "gibt-es-nicht")
        melde("SONDE", "M355e", u.returncode == 1 and "nur bei der Erstinstallation"
              in (u.stderr or "") and n.returncode == 1 and not os.listdir(leer),
              "Das Muster verweigert sich bei --update und bei einem unbekannten Namen, "
              "ohne eine Datei zu schreiben")

        # --- M355a: ohne --overlay unveraendert -------------------------------------
        ohne = os.path.join(basis, "ohne")
        os.makedirs(ohne)
        o = _355_install(ohne)
        deny = json.loads(lies(os.path.join(ohne, ".claude", "settings.json")))[
            "permissions"]["deny"]
        erwartet = ["Read(<EXCLUDED_PATHS>)", "Edit(<CI_CONFIG_PATHS>)",
                    "Edit(<QUALITY_GATE_CONFIG_PATHS>)", "Edit(<READ_ONLY_PATHS>)"]
        melde("GEGENPROBE", "M355a", o.returncode == 0 and all(r in deny for r in erwartet),
              "Ohne Muster bleibt jeder Pfadschlitz woertlich stehen, dazu der Schlitz fuer "
              "die Nur-Lese-Pfade aus D-356")

        # --- M355d: ein Muster, das freigibt ----------------------------------------
        # Gemessen am eigenen Werkzeug einer Kopie: Deren install.py liest das Muster
        # aus IHREM Kern - die Quelle bleibt unberuehrt.
        kopie_kern = os.path.join(basis, "kern", ".koolie", "core")
        shutil.copytree(os.path.join(QUELLE, ".koolie/core"), kopie_kern,
                        ignore=shutil.ignore_patterns(".git", "__pycache__", "out"))
        muster = os.path.join(basis, "kern", M355_MUSTER)
        text = lies(muster)
        anker = "| `<EXCLUDED_PATHS>` |"
        if text.count(anker) != 1:
            raise Praeparationsfehler("general.md: Zeile %s %dx statt 1x"
                                      % (anker, text.count(anker)))
        schreib(muster, text.replace(anker, "| `<ALLOWED_PATHS>` | `**` | Sonde |\r\n"
                                     + anker, 1))
        frei = os.path.join(basis, "frei")
        os.makedirs(frei)
        d = unterprozess([sys.executable, os.path.join(kopie_kern, "install.py"),
                          "--client", "claude-code", "--root", frei,
                          "--overlay", "general"])
        melde("SONDE", "M355d", d.returncode == 1 and "darf nur sperren" in (d.stderr or "")
              and not os.listdir(frei),
              "Ein Muster, das erlaubte Pfade fuellen will, bricht die Installation ab, "
              "bevor die erste Datei geschrieben ist")

        # --- M359a: Ablage und Beschreibung laufen auseinander -----------------------
        kern_a = _359_kern(basis, "kern-a")
        weg = os.path.join(kern_a, "framework", "overlay-patterns", "general", "documents",
                           "security")
        if not os.path.isdir(weg):
            raise Praeparationsfehler("general/documents/security fehlt - M359a haette "
                                      "nichts zu entfernen")
        shutil.rmtree(weg)
        ziel_a = os.path.join(basis, "ziel-a")
        os.makedirs(ziel_a)
        a = unterprozess([sys.executable, os.path.join(kern_a, "install.py"),
                          "--client", "claude-code", "--root", ziel_a, "--overlay", "general"])
        melde("SONDE", "M359a", a.returncode == 1 and "stimmen nicht ueberein" in
              (a.stderr or "") and not os.listdir(ziel_a),
              "Fehlt ein beschriebenes Musterdokument in der Ablage, bricht die Installation "
              "ab, bevor die erste Datei geschrieben ist")

        # --- M359b: ein Dokument ohne Vorschlagsvermerk ------------------------------
        kern_b = _359_kern(basis, "kern-b")
        dok = os.path.join(kern_b, "framework", "overlay-patterns", "general", "documents",
                           "quality", "muster-general.md")
        text = lies(dok)
        if text.count(M359_VERMERK) != 1:
            raise Praeparationsfehler("quality/muster-general.md fuehrt den Vermerk %dx "
                                      "statt 1x" % text.count(M359_VERMERK))
        schreib(dok, text.replace(M359_VERMERK, "Allgemeine Grundsaetze.", 1))
        ziel_b = os.path.join(basis, "ziel-b")
        os.makedirs(ziel_b)
        b = unterprozess([sys.executable, os.path.join(kern_b, "install.py"),
                          "--client", "claude-code", "--root", ziel_b, "--overlay", "general"])
        melde("SONDE", "M359b", b.returncode == 1 and "nicht den Vermerk" in (b.stderr or "")
              and not os.listdir(ziel_b),
              "Ein Musterdokument ohne Vorschlagsvermerk bricht die Installation ab - ein "
              "ungeprueft mitgelieferter Text darf nicht wie eine Projektvorgabe aussehen")

        # --- M359c: ohne --overlay ---------------------------------------------------
        manifest_ohne = lies(os.path.join(ohne, ".koolie", "project-overlay",
                                          "overlay-manifest.yaml"))
        musterdoks = glob.glob(os.path.join(ohne, ".koolie", "project-overlay", "documents",
                                            "*", "muster-general.md"))
        melde("GEGENPROBE", "M359c", manifest_ohne.count('- id: "DOC-') == 3
              and not musterdoks,
              "Ohne Muster bleibt die Manifestvorlage mit ihren drei Beispielen, und kein "
              "Musterdokument liegt im Projekt")
    finally:
        aufraeumen(basis)


buendel(sonden_overlay_muster,
        "Der Fuellschritt aus --overlay general an echten Erstinstallationen, dazu seine "
        "Dokumente, sechs Verweigerungen und der unveraenderte Weg ohne Muster")


# --- D-362: der Kopierweg in ein Projekt, der Dialog und die Starter (CR-2026-140) ---
#
# `install.py --target` kopiert NUR den Kern in ein Projekt und ruft danach das kopierte
# install.py dort auf. Die Sonden fahren es an echten Verzeichnissen, aus BEIDEN
# Quellformen: einer Kopie ohne Git (so liegt ein entpacktes Release-Archiv da) und
# einem Klon, aus dem nur Verfolgtes kommen darf (D-333).
#   T362  (Sonde) - Erstinstallation aus der Archivform: der Kern vollstaendig, ohne
#                   Bytecode und build/out, ohne Kennzeichen und ohne das Overlay der
#                   Quelle (D-354), Wurzeldateien angelegt
#   T362a (Sonde) - ein zweiter Aufruf ohne --update haelt an und veraendert nichts
#   T362b (Sonde) - --update hebt: Stand der Quelle, Altlast weg, Overlay unberuehrt,
#                   keine Zwischenverzeichnisse
#   T362c (Sonde) - scheitert die Installation im Projekt (Kollision), ist der kopierte
#                   Kern wieder weg und die Projektdatei unveraendert
#   T362d (Sonde) - --update ohne vorhandenen Kern haelt an, ohne zu schreiben
#   T362e (Sonde) - Quelle und Ziel dasselbe Verzeichnis: Abbruch
#   T362f (Sonde) - aus einem Klon kommt eine unverfolgte Datei des Kerns NICHT mit
#   T362g (Sonde) - der Dialog sammelt die Angaben ein und installiert
#   T362h (Sonde) - der Dialog bricht mit q ab und schreibt nichts
#   T363  (Sonde) - die Mindestversion steht in install.py und beiden Startern gleich
#   T365  (Sonde) - install.cmd traegt keine Sprungmarke (LF im Archiv), und
#                   install.command ist im Repositorium ausfuehrbar (100755)
T362_ANTWORTEN = "%s\n1\n1\n1\nj\n"


def _362_lauf(kern: str, *argv: str, eingabe=None, werkzeug: str = "install.py"):
    return unterprozess([sys.executable, os.path.join(kern, werkzeug), *argv],
                        input=eingabe)


def _362_kerndateien(kern: str) -> set:
    out = set()
    for dirpath, dirnames, filenames in os.walk(kern):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in filenames:
            out.add(os.path.relpath(os.path.join(dirpath, fn), kern).replace(os.sep, "/"))
    return out


def sonden_kopierweg() -> None:
    """Wirkungsnachweis fuer install.py --target, den Dialog und die Starter (D-362)."""
    basis = tempfile.mkdtemp(prefix="lw-kopierweg-")
    quelle = kopie()
    try:
        qkern = os.path.join(quelle, ".koolie", "core")
        # Erzeugnisse, die ein Lauf in einem entpackten Archiv hinterlaesst - sie
        # duerfen nicht mitkommen.
        os.makedirs(os.path.join(qkern, "__pycache__"), exist_ok=True)
        schreib(os.path.join(qkern, "__pycache__", "sonde.cpython-38.pyc"), "x")
        os.makedirs(os.path.join(qkern, "build", "out"), exist_ok=True)
        schreib(os.path.join(qkern, "build", "out", "sonde.docx"), "x")
        # Seit 1.8.0 schreibt --target die Wahl des Lieferumfangs in den Kern (D-367).
        erwartet = {r for r in _362_kerndateien(qkern) if not r.startswith("build/out/")}
        erwartet.add("LIEFERUMFANG")

        # --- T362: Erstinstallation aus der Archivform -------------------------------
        erst = os.path.join(basis, "erst")
        os.makedirs(erst)
        p = _362_lauf(qkern, "--target", erst, "--client", "claude-code")
        zkern = os.path.join(erst, ".koolie", "core")
        ist = _362_kerndateien(zkern)
        qoverlay = os.path.join(quelle, ".koolie", "project-overlay", "OVERLAY.md")
        zoverlay = os.path.join(erst, ".koolie", "project-overlay", "OVERLAY.md")
        fehlt = []
        if ist != erwartet:
            fehlt.append("Kern: %d zu viel, %d fehlen"
                         % (len(ist - erwartet), len(erwartet - ist)))
        if os.path.exists(os.path.join(erst, ".koolie", "QUELLREPOSITORIUM.md")):
            fehlt.append("Kennzeichen mitkopiert")
        if _367_umfang(erst) != "voll":
            fehlt.append("LIEFERUMFANG " + _367_umfang(erst))
        if not os.path.isfile(zoverlay):
            fehlt.append("kein Overlay")
        elif os.path.isfile(qoverlay) and lies(qoverlay) == lies(zoverlay):
            fehlt.append("Overlay der Quelle mitkopiert")
        if not os.path.isfile(os.path.join(erst, "CLAUDE.md")):
            fehlt.append("keine Wurzel-Anweisungsdatei")
        melde("SONDE", "T362", p.returncode == 0 and not fehlt,
              "Aus der Archivform kommt der ganze Kern ohne Erzeugnisse, ohne Kennzeichen "
              "und ohne das Overlay der Quelle, und das Projekt ist installiert")
        if p.returncode != 0 or fehlt:
            notiz("        Exit %d; %s" % (p.returncode, "; ".join(fehlt) or "-"))

        # --- T362a: zweiter Aufruf ohne --update --------------------------------------
        vorher = baumhash(erst)
        p = _362_lauf(qkern, "--target", erst)
        ok = (p.returncode == 1 and "Heben auf diesen Stand: --update" in p.stderr
              and baumhash(erst) == vorher)
        melde("SONDE", "T362a", ok,
              "Ein vorhandener Kern wird ohne --update nicht ersetzt")
        if not ok:
            notiz("        Exit %d, Baum %s" % (p.returncode,
                  "unveraendert" if baumhash(erst) == vorher else "VERAENDERT"))

        # --- T362b: Heben ----------------------------------------------------------
        schreib(os.path.join(zkern, "VERSION"), "0.0.0\n")
        schreib(os.path.join(zkern, "ALTLAST.md"), "# Altlast\n")
        schreib(zoverlay, lies(zoverlay) + "\nPROJEKTZEILE-T362b\n")
        p = _362_lauf(qkern, "--target", erst, "--update")
        fehlt = []
        if lies(os.path.join(zkern, "VERSION")).strip() != \
                lies(os.path.join(qkern, "VERSION")).strip():
            fehlt.append("VERSION nicht gehoben")
        if os.path.exists(os.path.join(zkern, "ALTLAST.md")):
            fehlt.append("Altlast liegt noch")
        if "PROJEKTZEILE-T362b" not in lies(zoverlay):
            fehlt.append("Overlay veraendert")
        for rest in ("core.koolie-neu", "core.koolie-alt"):
            if os.path.exists(os.path.join(erst, ".koolie", rest)):
                fehlt.append(rest + " liegt")
        melde("SONDE", "T362b", p.returncode == 0 and not fehlt,
              "--update ersetzt den Kern als Verzeichnis und laesst das Overlay stehen")
        if p.returncode != 0 or fehlt:
            notiz("        Exit %d; %s" % (p.returncode, "; ".join(fehlt) or "-"))

        # --- T362c: Rueckbau nach gescheiterter Installation ---------------------------
        kol = os.path.join(basis, "kollision")
        os.makedirs(kol)
        schreib(os.path.join(kol, "CLAUDE.md"), "# Projektdatei\n")
        p = _362_lauf(qkern, "--target", kol, "--client", "claude-code")
        ok = (p.returncode != 0 and not os.path.exists(os.path.join(kol, ".koolie", "core"))
              and lies(os.path.join(kol, "CLAUDE.md")) == "# Projektdatei\n")
        melde("SONDE", "T362c", ok,
              "Scheitert die Installation im Projekt, wird der kopierte Kern wieder entfernt")
        if not ok:
            notiz("        Exit %d, Kern %s" % (p.returncode, "liegt" if os.path.exists(
                os.path.join(kol, ".koolie", "core")) else "entfernt"))

        # --- T362d: --update ohne Kern ------------------------------------------------
        leer = os.path.join(basis, "leer")
        os.makedirs(leer)
        p = _362_lauf(qkern, "--target", leer, "--update")
        ok = p.returncode == 1 and not os.listdir(leer)
        melde("SONDE", "T362d", ok, "--update ohne vorhandenen Kern haelt an, ohne zu schreiben")

        # --- T362e: Quelle gleich Ziel ------------------------------------------------
        p = _362_lauf(qkern, "--target", quelle)
        ok = p.returncode == 1 and "Quelle und Ziel sind dasselbe" in p.stderr
        melde("SONDE", "T362e", ok, "Quelle und Ziel duerfen nicht dasselbe Verzeichnis sein")

        # --- T362f: aus einem Klon nur Verfolgtes --------------------------------------
        klon = kopie()
        try:
            g = unterprozess(["git", "-C", klon, "init", "-q"])
            if g.returncode == 0:
                g = unterprozess(["git", "-C", klon, "add", "-A"])
            if g.returncode != 0:
                raise Praeparationsfehler("git init/add im Klon: " + (g.stderr or "")[:200])
            schreib(os.path.join(klon, ".koolie", "core", "UNVERFOLGT-T362f.md"), "# x\n")
            ziel = os.path.join(basis, "ausklon")
            os.makedirs(ziel)
            p = _362_lauf(os.path.join(klon, ".koolie", "core"), "--target", ziel,
                          "--client", "claude-code")
            unverfolgt = os.path.exists(os.path.join(ziel, ".koolie", "core",
                                                     "UNVERFOLGT-T362f.md"))
            ok = p.returncode == 0 and "Klon - nur Verfolgtes" in p.stdout and not unverfolgt
            melde("SONDE", "T362f", ok,
                  "Aus einem Klon kommt nur Verfolgtes - eine unverfolgte Datei bleibt draussen")
            if not ok:
                notiz("        Exit %d, Klonweg %s, unverfolgt kopiert %s"
                      % (p.returncode, "Klon - nur Verfolgtes" in p.stdout, unverfolgt))
        finally:
            aufraeumen(os.path.dirname(klon))

        # --- T362g/h: der Dialog --------------------------------------------------------
        dlg = os.path.join(basis, "dialog")
        os.makedirs(dlg)
        p = _362_lauf(qkern, eingabe=T362_ANTWORTEN % dlg, werkzeug="install_dialog.py")
        ok = p.returncode == 0 and os.path.isfile(os.path.join(dlg, ".koolie", "core",
                                                               "install.py"))
        melde("SONDE", "T362g", ok,
              "Der Dialog sammelt Projekt, Client und Muster ein und installiert")
        if not ok:
            notiz("        Exit %d: %s" % (p.returncode, " | ".join(
                (p.stdout + p.stderr).splitlines()[-4:])))
        abb = os.path.join(basis, "abbruch")
        os.makedirs(abb)
        p = _362_lauf(qkern, eingabe="q\n", werkzeug="install_dialog.py")
        ok = p.returncode == 1 and "Nichts installiert" in p.stdout and not os.listdir(abb)
        melde("SONDE", "T362h", ok, "Der Dialog bricht mit q ab und schreibt nichts")

        # --- T363: die Mindestversion an drei Stellen -----------------------------------
        m = re.search(r"^PYTHON_MINDEST = \((\d+), (\d+)\)",
                      lies(os.path.join(QUELLE, ".koolie", "core", "install.py")), re.M)
        if not m:
            raise Praeparationsfehler("PYTHON_MINDEST in install.py nicht gefunden")
        zahl = "sys.version_info >= (%s, %s)" % m.groups()
        text = "Python %s.%s oder neuer" % m.groups()
        abweichend = [s for s in ("install.cmd", "install.command")
                      if zahl not in lies(os.path.join(QUELLE, s))
                      or text not in lies(os.path.join(QUELLE, s))]
        melde("SONDE", "T363", not abweichend,
              "install.py und beide Starter nennen dieselbe Mindestversion")
        if abweichend:
            notiz("        abweichend: %s (erwartet '%s')" % (", ".join(abweichend), zahl))

        # --- T365: die Bauform der Starter ------------------------------------------------
        fehlt = []
        for zeile in lies(os.path.join(QUELLE, "install.cmd")).splitlines():
            z = zeile.strip().lower()
            if z.startswith(":") or re.search(r"\bgoto\b|\bcall\s+:", z):
                if not z.startswith("rem"):
                    fehlt.append("install.cmd: " + zeile.strip()[:40])
        g = unterprozess(["git", "-C", QUELLE, "ls-files", "-s", "install.command"])
        if g.returncode != 0 or not g.stdout.strip():
            fehlt.append("Modus von install.command nicht lesbar (kein Git-Bestand)")
        elif not g.stdout.startswith("100755"):
            fehlt.append("install.command traegt " + g.stdout.split()[0])
        melde("SONDE", "T365", not fehlt,
              "install.cmd kommt ohne Sprungmarke aus, install.command ist ausfuehrbar")
        if fehlt:
            notiz("        " + "; ".join(fehlt))
    finally:
        aufraeumen(os.path.dirname(quelle))
        aufraeumen(basis)


buendel(sonden_kopierweg,
        "install.py --target aus Archivform und Klon, Heben, Rueckbau und Verweigerungen, "
        "dazu der Dialog und die Bauform der Starter")



# --- D-367: der Lieferumfang einer Installation (CR-2026-141) ------------------------
#
# `install.py --target --lieferumfang nutzung` laesst die Nachweisschicht weg
# (clientmap.NACHWEIS_ABLAGEN). OB die Nutzung ohne sie auskommt, belegt keine
# Einzelpruefung, sondern der Vergleich: Eine reduzierte Installation muss je Pack
# dieselbe Validatorausgabe liefern wie eine volle - bis auf die HINWEIS-Zeilen, die
# genau das Weggelassene nennen. Ein Traeger, den ein Werkzeug zur Laufzeit aus der
# Nachweisschicht liest, faellt genau hier auf.
#   L367  (Sonde) - je Pack: reduziert und voll zeilengleich unter --strict-overlay, bis
#                   auf die HINWEIS-Zeilen; reduziert ohne Nachweisschicht, mit
#                   LIEFERUMFANG 'nutzung', voll mit 'voll' und ohne HINWEIS
#   L367a (Sonde) - --update ohne Angabe hebt und bleibt reduziert
#   90b   (Sonde) - LIEFERUMFANG mit unbekanntem Wert wird gemeldet
#   90c   (Sonde) - 'nutzung', obwohl eine Ablage der Nachweisschicht daliegt, wird
#                   gemeldet
#   L367c (Sonde) - eine reduzierte Quelle verweigert den vollen Kern, ohne zu schreiben
#   L367b (Sonde) - --update --lieferumfang voll waechst auf den ganzen Kern
#   L367d (Sonde) - --lieferumfang ohne --target haelt an
#   L367e (Sonde) - der Dialog fragt den Umfang und installiert reduziert
#   T368  (Sonde) - unter Windows: ein Projektpfad, der die Pfadgrenze reisst, haelt vor
#                   der ersten Kopie an und laesst das Projekt leer (D-368); auf den
#                   anderen Systemen die Gegenprobe: derselbe Pfad wird installiert
# Dazu zwei Einzelsonden am Quellrepositorium (90, 90a).
L367_PACKS = ("claude-code", "devin-desktop", "openai-codex")
L367_ANTWORTEN = "%s\n1\n1\n2\nj\n"


def _367_ausgabe(root: str) -> list:
    """Validatorausgabe unter --strict-overlay, der Projektpfad durch <ROOT> ersetzt."""
    p = unterprozess([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                      "--root", root, "--strict-overlay"])
    text = ((p.stdout or "") + (p.stderr or "")).replace(os.path.normpath(root), "<ROOT>")
    return text.splitlines()


def _367_umfang(root: str) -> str:
    pfad = os.path.join(root, ".koolie", "core", "LIEFERUMFANG")
    return lies(pfad).strip() if os.path.isfile(pfad) else "-"


def _367_nachweis_da(root: str) -> list:
    kern = os.path.join(root, ".koolie", "core")
    return [a for a in ("governance/change-requests", "tests/protocols", "tests/erhebungen",
                        "build") if os.path.exists(os.path.join(kern, *a.split("/")))]


def sonden_lieferumfang() -> None:
    """Wirkungsnachweis fuer den waehlbaren Lieferumfang (D-367) und die Pfadgrenze (D-368)."""
    basis = tempfile.mkdtemp(prefix="lw-umfang-")
    quelle = kopie()
    try:
        qkern = os.path.join(quelle, ".koolie", "core")

        # --- L367: reduziert gegen voll, je Pack -------------------------------------
        abweichend = []
        for pack in L367_PACKS:
            voll = os.path.join(basis, "voll-" + pack)
            nutz = os.path.join(basis, "nutzung-" + pack)
            os.makedirs(voll)
            os.makedirs(nutz)
            a = _362_lauf(qkern, "--target", voll, "--client", pack)
            b = _362_lauf(qkern, "--target", nutz, "--client", pack,
                          "--lieferumfang", "nutzung")
            if a.returncode or b.returncode:
                abweichend.append("%s: Installation Exit %d/%d" % (pack, a.returncode,
                                                                  b.returncode))
                continue
            aus_voll = _367_ausgabe(voll)
            aus_nutz = _367_ausgabe(nutz)
            ohne = [z for z in aus_nutz if not z.startswith("HINWEIS")]
            hinweise = [z for z in aus_nutz if z.startswith("HINWEIS")]
            if ohne != aus_voll:
                nur_nutz = [z for z in ohne if z not in aus_voll]
                nur_voll = [z for z in aus_voll if z not in ohne]
                abweichend.append("%s: %d Zeilen nur reduziert, %d nur voll; erste: %s"
                                  % (pack, len(nur_nutz), len(nur_voll),
                                     ((nur_nutz or nur_voll or ["Reihenfolge"])[0])[:160]))
            if any(z.startswith("HINWEIS") for z in aus_voll):
                abweichend.append(pack + ": die volle Installation traegt HINWEIS-Zeilen")
            if not any("Lieferumfang 'nutzung'" in z for z in hinweise):
                abweichend.append(pack + ": reduziert ohne HINWEIS zum Lieferumfang")
            if _367_nachweis_da(nutz):
                abweichend.append(pack + ": reduziert liegt " + ", ".join(_367_nachweis_da(nutz)))
            if (_367_umfang(voll), _367_umfang(nutz)) != ("voll", "nutzung"):
                abweichend.append("%s: LIEFERUMFANG %s/%s" % (pack, _367_umfang(voll),
                                                              _367_umfang(nutz)))
        melde("SONDE", "L367", not abweichend,
              "Eine reduzierte Installation meldet in jedem Pack dasselbe wie eine volle, "
              "bis auf die HINWEIS-Zeilen zum Weggelassenen")
        for z in abweichend:
            notiz("        " + z)

        nutz = os.path.join(basis, "nutzung-claude-code")
        nkern = os.path.join(nutz, ".koolie", "core")

        # --- L367a: Heben ohne Angabe bleibt reduziert -------------------------------
        schreib(os.path.join(nkern, "VERSION"), "0.0.0\n")
        p = _362_lauf(qkern, "--target", nutz, "--update")
        ok = (p.returncode == 0 and _367_umfang(nutz) == "nutzung"
              and not _367_nachweis_da(nutz)
              and lies(os.path.join(nkern, "VERSION")).strip()
              == lies(os.path.join(qkern, "VERSION")).strip())
        melde("SONDE", "L367a", ok,
              "--update ohne Angabe hebt ein reduziertes Projekt und laesst es reduziert")
        if not ok:
            notiz("        Exit %d, Umfang %s, Nachweis %s" % (
                p.returncode, _367_umfang(nutz), _367_nachweis_da(nutz)))

        # --- 90b, 90c: Pruefung 90 an der reduzierten Installation --------------------
        schreib(os.path.join(nkern, "LIEFERUMFANG"), "teilweise\n")
        melde("SONDE", "90b", "trägt 'teilweise'" in "\n".join(_367_ausgabe(nutz)),
              "Ein unbekannter Wert in LIEFERUMFANG wird gemeldet - das naechste Heben "
              "hielte daran an")
        schreib(os.path.join(nkern, "LIEFERUMFANG"), "nutzung\n")
        os.makedirs(os.path.join(nkern, "tests", "protocols"))
        schreib(os.path.join(nkern, "tests", "protocols", "liegengeblieben.md"), "# x\n")
        melde("SONDE", "90c", "sagt 'nutzung', aber" in "\n".join(_367_ausgabe(nutz)),
              "LIEFERUMFANG nutzung neben einer Ablage der Nachweisschicht wird gemeldet - "
              "das naechste Heben loeschte sie")

        # --- L367c: aus der reduzierten Quelle kein voller Kern ------------------------
        leer = os.path.join(basis, "aus-reduziert")
        os.makedirs(leer)
        p = _362_lauf(nkern, "--target", leer, "--client", "claude-code")
        ok = p.returncode == 1 and "einen vollen Kern kann" in p.stderr and not os.listdir(leer)
        melde("SONDE", "L367c", ok,
              "Eine reduzierte Quelle verweigert den vollen Kern und schreibt nichts")

        # --- L367b: ausdruecklich zurueck auf voll --------------------------------------
        shutil.rmtree(os.path.join(nkern, "tests", "protocols"))
        p = _362_lauf(qkern, "--target", nutz, "--update", "--lieferumfang", "voll")
        ok = (p.returncode == 0 and _367_umfang(nutz) == "voll"
              and len(_367_nachweis_da(nutz)) == 4 and "(bisher nutzung)" in p.stdout)
        melde("SONDE", "L367b", ok,
              "--update --lieferumfang voll bringt die Nachweisschicht zurueck und nennt "
              "den Wechsel")
        if not ok:
            notiz("        Exit %d, Umfang %s, Nachweis %s" % (
                p.returncode, _367_umfang(nutz), _367_nachweis_da(nutz)))

        # --- L367d: ohne --target ------------------------------------------------------
        ohne_ziel = os.path.join(basis, "ohne-target")
        os.makedirs(ohne_ziel)
        p = _362_lauf(qkern, "--root", ohne_ziel, "--lieferumfang", "nutzung")
        ok = (p.returncode == 1 and "gehoert zu --target" in p.stderr
              and not os.listdir(ohne_ziel))
        melde("SONDE", "L367d", ok, "--lieferumfang ohne --target haelt an, ohne zu schreiben")

        # --- L367e: der Dialog ---------------------------------------------------------
        dlg = os.path.join(basis, "dialog")
        os.makedirs(dlg)
        p = _362_lauf(qkern, eingabe=L367_ANTWORTEN % dlg, werkzeug="install_dialog.py")
        ok = p.returncode == 0 and _367_umfang(dlg) == "nutzung" and not _367_nachweis_da(dlg)
        melde("SONDE", "L367e", ok,
              "Der Dialog fragt den Lieferumfang ab und installiert reduziert")
        if not ok:
            notiz("        Exit %d, Umfang %s: %s" % (p.returncode, _367_umfang(dlg), " | ".join(
                (p.stdout + p.stderr).splitlines()[-4:])))

        # --- T368: die Pfadgrenze ------------------------------------------------------
        tief = basis
        while len(tief) < 190:
            tief = os.path.join(tief, "t" * min(40, 200 - len(tief)))
        os.makedirs(tief)
        p = _362_lauf(qkern, "--target", tief, "--client", "claude-code")
        if os.name == "nt":
            ok = (p.returncode == 1 and "fuer Windows zu lang" in p.stderr
                  and not os.listdir(tief))
            melde("SONDE", "T368", ok,
                  "Ein Projektpfad, der die Windows-Pfadgrenze reisst, haelt vor der ersten "
                  "Kopie an und laesst das Projekt leer")
        else:
            ok = p.returncode == 0
            melde("GEGENPROBE", "T368", ok,
                  "Ausserhalb von Windows gilt keine Pfadgrenze - derselbe tiefe "
                  "Projektpfad wird installiert")
        if not ok:
            notiz("        Exit %d: %s" % (p.returncode, (p.stderr or "")[:200]))
    finally:
        aufraeumen(os.path.dirname(quelle))
        aufraeumen(basis)


buendel(sonden_lieferumfang,
        "Reduzierte gegen volle Installation je Pack, Heben mit und ohne Wechsel, "
        "Verweigerungen, der Dialog, Pruefung 90 und die Windows-Pfadgrenze")


# Pruefung 90 am Quellrepositorium: Es ist keine Installation, und die Lockerung von
# Pruefung 12 gilt dort nie - was immer eine Datei LIEFERUMFANG behauptet.
P90_DATEI = os.path.join(".koolie", "core", "LIEFERUMFANG")
P90_PROTOKOLL = os.path.join(".koolie", "core", "tests", "protocols",
                             "2026-09-19-testblaetter-buendel-2.md")


def _90a(root: str) -> None:
    schreib(P(root, P90_DATEI), "nutzung\n")
    if not os.path.isfile(P(root, P90_PROTOKOLL)):
        raise Praeparationsfehler("Das zitierte Protokoll fehlt schon: " + P90_PROTOKOLL)
    os.remove(P(root, P90_PROTOKOLL))


sonde("90", "Eine Datei LIEFERUMFANG im Quellrepositorium wird gemeldet - sie behauptete dort eine Installation",
      lambda r: schreib(P(r, P90_DATEI), "nutzung\n"), "liegt im Quellrepositorium")

sonde("90a", "Im Quellrepositorium bleibt ein Verweis in die Nachweisschicht ein Fehler, auch wenn LIEFERUMFANG nutzung behauptet",
      _90a, "Pfadangabe existiert nicht: .koolie/core/tests/protocols/2026-09-19-testblaetter-buendel-2.md")


# --- D-364: Pruefung 33 ohne PyYAML (CR-2026-140) --------------------------------------
#
# Ohne PyYAML las Pruefung 33 aus dem Rohtext des Frontmatters nichts und meldete an
# jeder claude-code-Installation neun Skills mit leerem disallowed-tools. Der Starter
# installiert kein PyYAML nach (D-362) - auf einem frischen Zielrechner fehlt es also
# oft. Die Sonde sperrt den Import ueber ein Stellvertretermodul im Suchpfad.
#   S364  (Sonde)      - eine verkuerzte Liste wird auch ohne PyYAML gemeldet
#   S364a (Gegenprobe) - die richtige Installation bleibt ohne PyYAML still
T364_SPERRE = "raise ImportError('PyYAML gesperrt durch die Sonde S364')\n"


def sonden_ohne_pyyaml() -> None:
    """Pruefung 33 misst ohne PyYAML dasselbe wie mit (D-364)."""
    root = installation("claude-code")
    sperre = tempfile.mkdtemp(prefix="lw-ohne-yaml-")
    try:
        schreib(os.path.join(sperre, "yaml.py"), T364_SPERRE)
        umgebung = dict(os.environ, PYTHONPATH=sperre)

        def lauf_ohne() -> str:
            p = unterprozess([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                              "--root", root], env=umgebung)
            return (p.stdout or "") + (p.stderr or "")

        aus = lauf_ohne()
        gesperrt = "PyYAML nicht installiert" in aus
        still = "disallowed-tools traegt" not in aus
        melde("GEGENPROBE", "S364a", gesperrt and still,
              "Ohne PyYAML meldet Pruefung 33 an einer richtigen Installation nichts")
        if not (gesperrt and still):
            notiz("        PyYAML gesperrt %s, still %s" % (gesperrt, still))
        skill = os.path.join(root, ".claude", "skills", "koolie-plan", "SKILL.md")
        text = lies(skill)
        neu = re.sub(r"(?m)^disallowed-tools: .*$", "disallowed-tools: Edit", text)
        if neu == text:
            raise Praeparationsfehler("disallowed-tools in koolie-plan/SKILL.md nicht gefunden")
        schreib(skill, neu)
        aus = lauf_ohne()
        ok = "koolie-plan/SKILL.md: disallowed-tools traegt ['Edit']" in aus
        melde("SONDE", "S364", ok,
              "Ohne PyYAML wird eine verkuerzte disallowed-tools-Liste weiter gemeldet")
    finally:
        aufraeumen(sperre)
        aufraeumen(os.path.dirname(root))


buendel(sonden_ohne_pyyaml,
        "Pruefung 33 liest disallowed-tools auch ohne PyYAML und meldet nur, was fehlt")

"""Sonden zum Messapparat, zu den Importkanaelen, zur Kuerzung der Testblaetter, zur
Attribution, zu den Pfadtoken von codex, zu den Packs kiro und cursor, zu den Pruefungen
96 bis 101, zum Mandat und zu MCP.

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul
liest nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import ast
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

from .apparat import (
    aufraeumen, buendel, ersetze, gegenprobe, installation, kopie, lies, melde, notiz,
    P, Praeparationsfehler, QUELLE, schreib, sonde, strict_ausgabe, unterprozess,
    validator_ausgabe)


# --- D-407: der Messapparat findet den Kern unter `.koolie/core` (K-154) ----------------
#
# 🔴 SEIT DER UMBENENNUNG (0.88.0) WAR DER MESSAPPARAT AN DREI STELLEN GEBROCHEN, UND ES
# FIEL ERST IM NACHLAUF VON 1.11.0 AUF. `validate-output.py` und `mcp-waechter.py`
# suchten das Kernverzeichnis EINE Ebene unter der Wurzel und meldeten in jedem
# installierten Baum, es gebe keines; `cc-overlay-fuellen.py` entfaltete den Schlitz
# `Edit(<READ_ONLY_PATHS>)` nicht, den der Kern seit 1.5.0 fuehrt, und brach ab.
#   D407  (Sonde)      - an einer echten claude-code-Installation mit dem Kern unter
#                        `.koolie/core` finden beide Werkzeuge Pack und Skill.
#   D407a (Gegenprobe) - ohne Kern erfinden sie keinen: dieselbe Meldung wie bisher.
#   D407b (Sonde)      - der Abgleich zwischen den Platzhaltern der erzeugten
#                        Berechtigungsdatei und der Liste des Fuellskripts meldet die
#                        Luecke von 1.11.0 (Liste ohne `<READ_ONLY_PATHS>`).
#   D407c (Gegenprobe) - mit der ausgelieferten Liste bleibt keine Luecke.
# ⚠️ Grenze, benannt: D407b und D407c messen den ABGLEICH, nicht den Lauf des
# Fuellskripts; der braucht das Uebungsrepositorium, und eine Sonde, die daran haengt,
# bestuende auf einem Arbeitsplatz und fiele auf dem naechsten. Gelaufen ist das Skript
# im Messaufbau von 1.12.0 (Protokoll).
M407_KEIN_KERN = "weder ein installiertes Client Pack noch ein Kernverzeichnis"
M407_CODE = r"""
import importlib.util, json, sys
def lade(name, pfad):
    spec = importlib.util.spec_from_file_location(name, pfad)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m
sys.path.insert(0, sys.argv[2])
vo = lade("_vo407", sys.argv[1])
mw = lade("_mw407", sys.argv[3])
pfad, grund = vo.skill_pfad(sys.argv[4], "koolie-code-explain")
pack, _ = mw._manifest(sys.argv[4])
print(json.dumps({"pfad": pfad, "grund": grund, "pack": pack}))
"""


def _407_gebraucht(quelltext: str) -> list:
    """Die Liste GEBRAUCHT des Fuellskripts - gelesen, nicht nachgeschrieben."""
    for knoten in ast.walk(ast.parse(quelltext)):
        if isinstance(knoten, ast.Assign) and any(
                isinstance(z, ast.Name) and z.id == "GEBRAUCHT" for z in knoten.targets):
            return [e.value for e in knoten.value.elts]
    return []


def _407_luecken(settings_text: str, gebraucht: list) -> list:
    return sorted(set(re.findall(r"<[A-Z_]+>", settings_text)) - set(gebraucht))


def sonden_messapparat() -> None:
    """Wirkungsnachweis fuer D-407 an einer echten claude-code-Installation."""
    kern = os.path.join(QUELLE, ".koolie", "core")
    vo = os.path.join(kern, "tests", "scripts", "validate-output.py")
    erh = os.path.join(kern, "tests", "erhebungen")
    mw = os.path.join(erh, "mcp-waechter.py")
    ziel = tempfile.mkdtemp(prefix="lw-407-")
    try:
        root = os.path.join(ziel, "projekt")
        os.makedirs(root)
        p = unterprozess([sys.executable, os.path.join(kern, "install.py"),
                          "--client", "claude-code", "--root", root])
        settings = lies(os.path.join(root, ".claude", "settings.json"))
        # Der Kern im Baum, so weit die Werkzeuge ihn brauchen: Packs und Skillquellen.
        shutil.copytree(os.path.join(kern, "clients"),
                        os.path.join(root, ".koolie", "core", "clients"))
        shutil.copytree(os.path.join(kern, "framework"),
                        os.path.join(root, ".koolie", "core", "framework"))
        q = unterprozess([sys.executable, "-c", M407_CODE, vo, erh, mw, root])
        try:
            ist = json.loads((q.stdout or "").strip().splitlines()[-1])
        except (ValueError, IndexError):
            ist = {}
        erwartet = os.path.join(root, ".claude", "skills", "koolie-code-explain", "SKILL.md")
        ok = (p.returncode == 0 and q.returncode == 0 and ist.get("pack") == "claude-code"
              and os.path.normcase(ist.get("pfad") or "") == os.path.normcase(erwartet))
        melde("SONDE", "D407", ok,
              "Kern unter .koolie/core: validate-output.py findet den Skill des "
              "installierten Packs, mcp-waechter.py das Pack")
        if not ok:
            notiz("        Exit %d/%d, Ergebnis %r" % (p.returncode, q.returncode, ist))

        shutil.rmtree(os.path.join(root, ".koolie", "core"))
        q = unterprozess([sys.executable, "-c", M407_CODE, vo, erh, mw, root])
        try:
            ist = json.loads((q.stdout or "").strip().splitlines()[-1])
        except (ValueError, IndexError):
            ist = {}
        ok = (q.returncode == 0 and ist.get("pack") is None and ist.get("pfad") is None
              and M407_KEIN_KERN in (ist.get("grund") or ""))
        melde("GEGENPROBE", "D407a", ok,
              "Ohne Kern erfinden beide Werkzeuge keinen - dieselbe Meldung wie bisher")
        if not ok:
            notiz("        Exit %d, Ergebnis %r" % (q.returncode, ist))

        gebraucht = _407_gebraucht(lies(os.path.join(erh, "cc-overlay-fuellen.py")))
        luecke = _407_luecken(settings, [g for g in gebraucht if g != "<READ_ONLY_PATHS>"])
        ok = p.returncode == 0 and luecke == ["<READ_ONLY_PATHS>"]
        melde("SONDE", "D407b", ok,
              "Der Abgleich meldet die Luecke von 1.11.0: die Liste des Fuellskripts "
              "ohne <READ_ONLY_PATHS>")
        if not ok:
            notiz("        Luecke %r" % luecke)
        luecke = _407_luecken(settings, gebraucht)
        ok = p.returncode == 0 and bool(gebraucht) and luecke == []
        melde("GEGENPROBE", "D407c", ok,
              "Die ausgelieferte Liste deckt jeden Platzhalter der erzeugten "
              "Berechtigungsdatei")
        if not ok:
            notiz("        GEBRAUCHT %r, Luecke %r" % (gebraucht, luecke))
    finally:
        aufraeumen(ziel)


buendel(sonden_messapparat,
        "Der Messapparat findet den Kern unter .koolie/core, und das Fuellskript "
        "entfaltet jeden Platzhalter der claude-code-Berechtigungsdatei")


# --- D-411: die Importkanaele, die devin-desktop seit 1.12.1 zulaesst (K-156) -----------
#
# 🔴 MIT `windsurf: false` LAEDT DEVIN CLI DIE EIGENE REGELABLAGE NICHT - gemessen mit
# 3000.11.1 und 3000.11.3. Das Pack laesst Windsurf-Quellen seither zu, und damit eine
# Regel im Benutzerprofil, die in jeder Sitzung laedt (D-290). `install.py` meldet die
# Kanaele aus `import_channels_report`, wenn sie belegt sind.
#   D411  (Sonde)      - devin-desktop mit nicht leerer global_rules.md in einem
#                        Ersatz-Benutzerprofil und `.windsurf/` im Projekt: Installation
#                        und Hebung nennen beide Kanaele. Gegen v1.12.0 faellt sie.
#   D411a (Gegenprobe) - leere global_rules.md, kein `.windsurf/`: kein Hinweis. Ein
#                        Werkzeug, das immer warnt, besteht die Sonde auch.
M411_HINWEIS = "Die Importsteuerung dieses Client Packs laesst"
M411_GLOBAL = "~/.codeium/windsurf/memories/global_rules.md"
M411_PROJEKT = "  .windsurf\n"


def sonden_importkanaele() -> None:
    """Wirkungsnachweis fuer die Meldung aus D-411 an echten Installationen."""
    werkzeug = os.path.join(QUELLE, ".koolie", "core", "install.py")
    faelle = (("SONDE", "D411", True,
               "Belegte Windsurf-Kanaele werden bei Installation und Hebung genannt"),
              ("GEGENPROBE", "D411a", False,
               "Ohne belegten Kanal bleibt der Hinweis aus"))
    for art, kennung, belegt, was in faelle:
        ziel = tempfile.mkdtemp(prefix="lw-411-")
        try:
            heim = os.path.join(ziel, "heim")
            erinnerung = os.path.join(heim, ".codeium", "windsurf", "memories")
            os.makedirs(erinnerung)
            schreib(os.path.join(erinnerung, "global_rules.md"),
                    "Sonde D411.\n" if belegt else "")
            root = os.path.join(ziel, "projekt")
            os.makedirs(root)
            if belegt:
                os.makedirs(os.path.join(root, ".windsurf", "rules"))
            umg = dict(os.environ, USERPROFILE=heim, HOME=heim)
            p = unterprozess([sys.executable, werkzeug, "--client", "devin-desktop",
                              "--root", root], env=umg)
            q = unterprozess([sys.executable, werkzeug, "--update", "--root", root], env=umg)
            ein = (p.stdout or "") + (p.stderr or "")
            heb = (q.stdout or "") + (q.stderr or "")
            ist = tuple((M411_HINWEIS in t, M411_GLOBAL in t, M411_PROJEKT in t)
                        for t in (ein, heb))
            soll = ((belegt, belegt, belegt),) * 2
            ok = p.returncode == 0 and q.returncode == 0 and ist == soll
            melde(art, kennung, ok, was)
            if not ok:
                notiz("        Exit %d/%d, (Hinweis, global, Projekt) = %s, erwartet %s"
                      % (p.returncode, q.returncode, ist, soll))
        finally:
            aufraeumen(ziel)


buendel(sonden_importkanaele,
        "install.py nennt die Windsurf-Kanaele, die devin-desktop seit 1.12.1 zulaesst, "
        "wenn sie belegt sind - und nur dann")


# --- D-471: die Ergebniszellen bleiben im Kern (CR-2026-160, K-56) ------------------------
#
# Ein Testblatt ist Regelquelle UND Aufzeichnung. install.py ersetzt in der Skillablage der
# Laufzeitschicht jede Ergebniszelle durch 'offen' mit Verweis auf die Kernfassung; die
# Kopie des Kerns bleibt, wie sie ist. Und eine Zeile, deren Striche nicht zum Kopf passen,
# bricht die Installation ab, statt eine halb gekuerzte Zelle weiterzugeben.
M471_ERSATZ = "(D-471)"
M471_ABBRUCH = "nicht sicher kuerzbar"
P471_BLATT = ("framework", "skills", "koolie-refactor", "TESTS.md")
P471_BELEG = "tests/protocols/2026-09-26-testblaetter-modellwechsel.md"


def sonden_testblatt_kuerzung() -> None:
    root = installation("claude-code")
    try:
        lauf = os.path.join(root, ".claude", "skills", *P471_BLATT[2:])
        kern = os.path.join(root, ".koolie", "core", *P471_BLATT)
        t_lauf, t_kern = lies(lauf), lies(kern)
        zeilen = [z for z in t_lauf.split("\n") if z.startswith("| SK-007-")]
        ok = bool(zeilen) and all(z.rstrip("\r").endswith(M471_ERSATZ + " |") for z in zeilen) \
            and P471_BELEG not in t_lauf
        melde("SONDE", "D471", ok, "Die Skillablage der Laufzeitschicht traegt die Testfaelle "
              "ohne die Ergebnisse des Quellrepositoriums")
        if not ok:
            notiz("        %d Zeilen, Beleg in der Laufzeitfassung: %s"
                  % (len(zeilen), P471_BELEG in t_lauf))
        ok = P471_BELEG in t_kern and M471_ERSATZ + " |" not in t_kern
        melde("GEGENPROBE", "D471a", ok, "Die Kopie des Kerns behaelt ihre Ergebniszellen")
    finally:
        aufraeumen(os.path.dirname(root))
    quelle = kopie()
    ziel = tempfile.mkdtemp(prefix="lw-471-")
    try:
        blatt = os.path.join(quelle, ".koolie", "core", *P471_BLATT)
        # eine Zeile mit einem Strich zu viel: die Kuerzung koennte die falsche Zelle treffen
        ersetze(blatt, ("| SK-007-P02 | Befund melden statt beheben |",
                        "| SK-007-P02 | Befund melden | statt beheben |"))
        p = unterprozess([sys.executable, os.path.join(quelle, ".koolie", "core", "install.py"),
                          "--client", "claude-code", "--root", ziel])
        aus = (p.stdout or "") + (p.stderr or "")
        ok = p.returncode != 0 and M471_ABBRUCH in aus
        melde("SONDE", "D471b", ok, "Eine Tabellenzeile mit falscher Strichzahl bricht die "
              "Installation ab, statt gekuerzt zu werden")
        if not ok:
            notiz("        Exit %d, Meldung: %s" % (p.returncode, M471_ABBRUCH in aus))
    finally:
        aufraeumen(ziel)
        aufraeumen(quelle)


buendel(sonden_testblatt_kuerzung,
        "install.py liefert die Testblaetter ohne die Ergebniszellen des Quellrepositoriums aus "
        "und bricht bei einer Zeile ab, die es nicht sicher kuerzen kann")

# --- D-433/D-434: die Attributionsvorgabe des Clients und ihr Nachtrag (K-171) ----------
#
# 🔴 CLAUDE CODE GIBT DEM MODELL VON SICH AUS EINEN TRAILER Co-Authored-By VOR - gegen Q5,
# gemessen in SK-005-P01 (1.14.1). Das Pack schaltet ihn mit `attribution` ab, und zwar
# in OBJEKTFORM: Die Kurzform `false` laesst Staende vor 2.1.281 die ganze
# Einstellungsdatei verwerfen, mit Berechtigungen und Hooks (QC-7).
#   D433  (Sonde)      - die erzeugte Einstellungsdatei einer frischen claude-code-
#                        Installation traegt `attribution` als Objekt mit commit "" auf der
#                        obersten Ebene. Gegen v1.14.1 faellt sie.
#   D434  (Sonde)      - eine Hebung ueber eine Einstellungsdatei OHNE die beiden
#                        Zusatzschluessel nennt beide. Gegen v1.14.1 faellt sie.
#   D434a (Gegenprobe) - eine Hebung ueber die frisch erzeugte Datei bleibt stumm. Ein
#                        Werkzeug, das immer warnt, besteht D434 auch.
M434_HINWEIS = "Das Client Pack deklariert Schluessel, die in"


def sonden_attribution() -> None:
    """Wirkungsnachweis fuer D-433 und D-434 an echten Installationen."""
    werkzeug = os.path.join(QUELLE, ".koolie", "core", "install.py")
    ziel = tempfile.mkdtemp(prefix="lw-433-")
    try:
        root = os.path.join(ziel, "projekt")
        os.makedirs(root)
        p = unterprozess([sys.executable, werkzeug, "--client", "claude-code",
                          "--root", root])
        pfad = os.path.join(root, ".claude", "settings.json")
        cfg = json.loads(lies(pfad))
        wert = cfg.get("attribution")
        ok = (p.returncode == 0 and isinstance(wert, dict) and wert.get("commit") == ""
              and "attribution" not in cfg.get("permissions", {}))
        melde("SONDE", "D433", ok, "Die frische claude-code-Installation schaltet die "
              "Attributionsvorgabe in Objektform auf der obersten Ebene ab")
        if not ok:
            notiz("        Exit %d, attribution = %r" % (p.returncode, wert))
        for art, kennung, entfernen, was in (
                ("GEGENPROBE", "D434a", False,
                 "Eine Hebung ueber die vollstaendige Einstellungsdatei bleibt stumm"),
                ("SONDE", "D434", True,
                 "Eine Hebung ueber eine alte Einstellungsdatei nennt die fehlenden "
                 "Zusatzschluessel")):
            if entfernen:
                cfg = json.loads(lies(pfad))
                cfg.pop("attribution", None)
                cfg.pop("autoMemoryEnabled", None)
                schreib(pfad, json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")
            q = unterprozess([sys.executable, werkzeug, "--update", "--root", root])
            aus = (q.stdout or "") + (q.stderr or "")
            ist = (M434_HINWEIS in aus, "  attribution (oberste Ebene)" in aus,
                   "  autoMemoryEnabled (oberste Ebene)" in aus)
            soll = (entfernen,) * 3
            ok = q.returncode == 0 and ist == soll
            melde(art, kennung, ok, was)
            if not ok:
                notiz("        Exit %d, (Hinweis, attribution, autoMemory) = %s, erwartet %s"
                      % (q.returncode, ist, soll))
    finally:
        aufraeumen(ziel)


buendel(sonden_attribution,
        "claude-code schaltet die Attributionsvorgabe des Clients ab, und install.py "
        "--update nennt einen deklarierten Zusatzschluessel, der im Projekt fehlt")


# --- D-412: das Sonderziel des Arbeitsbereichs bei openai-codex (K-157) ------------------
#
# 🔴 SEIT CLIENTVERSION 0.157 IGNORIERT CODEX DIE FORM `:workspace/<pfad>`, UND MIT IHR
# WAR DER GANZE ARBEITSBEREICH SCHREIBGESCHUETZT - gemessen mit `codex sandbox` ohne
# Modellaufruf. Das Sonderziel heisst `:workspace_roots` und fuehrt seine Unterpfade als
# eigene Tabelle.
#   D412  (Sonde)      - die erzeugte config.toml einer echten Installation fuehrt die
#                        Tabelle `":workspace_roots"` mit "." = "write" und dem Kern als
#                        "read", und keinen Schluessel der alten Form. Gegen v1.12.0 faellt sie.
#   D412a (Gegenprobe) - der Grundstock ":root" = "read" bleibt in der Dateisystemtabelle
#                        selbst: Ein Werkzeug, das ALLES in die Untertabelle schiebt,
#                        besteht die Sonde auch und nimmt dem Client das Leserecht.
M412_TABELLE = '[permissions.koolie.filesystem.":workspace_roots"]'


def _412_tabellen(text: str) -> dict:
    tabellen, aktuell = {}, None
    for zeile in text.splitlines():
        zeile = zeile.strip()
        if zeile.startswith("[") and zeile.endswith("]"):
            aktuell = zeile
            tabellen[aktuell] = {}
        elif aktuell and " = " in zeile and not zeile.startswith("#"):
            k, v = zeile.split(" = ", 1)
            tabellen[aktuell][k.strip('"')] = v.strip('"')
    return tabellen


def sonden_pfadtoken_codex() -> None:
    """Wirkungsnachweis fuer D-412 an einer echten openai-codex-Installation."""
    werkzeug = os.path.join(QUELLE, ".koolie", "core", "install.py")
    ziel = tempfile.mkdtemp(prefix="lw-412-")
    try:
        root = os.path.join(ziel, "projekt")
        os.makedirs(root)
        p = unterprozess([sys.executable, werkzeug, "--client", "openai-codex", "--root", root])
        text = lies(os.path.join(root, ".codex", "config.toml"))
        tab = _412_tabellen(text)
        unter = tab.get(M412_TABELLE, {})
        alt = [k for t in tab.values() for k in t if k.startswith(":workspace/")
               or k == ":workspace"]
        ok = (p.returncode == 0 and unter.get(".") == "write"
              and unter.get(".koolie/core") == "read" and not alt)
        melde("SONDE", "D412", ok,
              "openai-codex: der Arbeitsbereich steht als Tabelle :workspace_roots, "
              "keine Schluessel der alten Form")
        if not ok:
            notiz("        Exit %d, Untertabelle %r, alte Schluessel %r"
                  % (p.returncode, unter, alt))
        fs = tab.get("[permissions.koolie.filesystem]", {})
        ok = p.returncode == 0 and fs.get(":root") == "read" and ":root" not in unter
        melde("GEGENPROBE", "D412a", ok,
              "Der Grundstock :root = read bleibt in der Dateisystemtabelle selbst")
        if not ok:
            notiz("        Dateisystemtabelle %r" % fs)
    finally:
        aufraeumen(ziel)


buendel(sonden_pfadtoken_codex,
        "openai-codex: das Rechteprofil fuehrt den Arbeitsbereich in der Schreibweise "
        "von Clientversion 0.157")


# --- D-414 bis D-417: das Client Pack kiro (CR-2026-150) --------------------------------
#
# Gemessen am 2026-09-26 mit kiro-cli 2.24.1: Die Berechtigungen stehen in einem
# Agentenprofil, das nur als AKTIVER Agent wirkt; fehlt es oder ist es kaputt, faellt der
# Client still auf seinen eingebauten Agenten zurueck (D-414). Das Schreibverbot auf die
# Laufzeitschicht nimmt die Spezifikationen aus (D-415). Die Menge der formatgebundenen
# Pruefungen fuehrte 76 statt 72 (D-416). Der Schutz-Hook sperrt nur mit Grund auf stderr
# (D-417). Alle Einheiten laufen an ECHTEN Installationen.
#   D414   (Sonde)      - die Abbildung: Profil mit exclude, Einstellungsdatei, Hook mit
#                         --sperrform stderr-grund, Regelvorlage mit inclusion: fileMatch.
#                         Gegen v1.12.1 faellt sie (kein Pack kiro).
#   D414a  (Gegenprobe) - eine Kernregel traegt KEINE Ladebedingung; eine Regel, die
#                         immer gilt, darf nicht an Dateimuster gebunden werden.
#   96..96f (Sonden)    - Pruefung 96: Profil fehlt, kein JSON, Einstellung waehlt einen
#                         anderen Agenten, unbekannte Faehigkeit, deny-Regel entfernt,
#                         fremde allow-Regel, verbreiterte Ausnahme.
#   96g    (Gegenprobe) - frische Installation: keine Meldung der Pruefung 96. Eine
#                         Pruefung, die immer meldet, bestuende die Sonden auch.
#   D416   (Sonde)      - Pruefung 72 erreicht das Agentenprofil: ein Skill ohne
#                         Freigaberegel wird gemeldet.
#   D417   (Sonde)      - Pruefung 86: ein Skript, dessen Form stderr-grund keinen Grund
#                         auf stderr schreibt, wird gemeldet.
#   D417a  (Gegenprobe) - das ausgelieferte Skript sperrt in dieser Form mit Exit 2 und
#                         Grund: keine Meldung.
M96 = ("Prüfung 96", "stille Rückfall", "Die Einstellung wählt ein Profil",
       "kein gültiges JSON", "das Pack verlangt", "die der Client nicht kennt",
       "die Kernquelle erzeugt 'deny", "erzeugt die Kernquelle nicht",
       "mit einer anderen Ausnahme")
M96_FEHLT = "Die Einstellung wählt ein Profil, das es nicht gibt"
M96_JSON = "kein gültiges JSON"
M96_WERT = "das Pack verlangt"
M96_FAEHIGKEIT = "die der Client nicht kennt"
M96_DENY = "die Kernquelle erzeugt 'deny fs_read .env'"
M96_ALLOW = "erzeugt die Kernquelle nicht"
M96_AUSNAHME = "mit einer anderen Ausnahme"
M416_SKILL = "wird aber von keinem Eintrag der Berechtigungsdatei genannt"
M417_FORM = "Sperrform 'stderr-grund' verlangt Exit 2"


def _414_profil(root: str, aenderung) -> None:
    pfad = os.path.join(root, ".kiro", "agents", "koolie.json")
    daten = json.loads(lies(pfad))
    aenderung(daten)
    schreib(pfad, json.dumps(daten, indent=2, ensure_ascii=False) + "\n")


def _414_regeln_ohne(daten: dict, faehigkeit: str, effekt: str, muster: str) -> None:
    for regel in daten["permissions"]["rules"]:
        if regel["capability"] == faehigkeit and regel["effect"] == effekt:
            if muster not in regel["match"]:
                raise Praeparationsfehler("Muster %r fehlt in %s/%s" % (muster, faehigkeit, effekt))
            regel["match"].remove(muster)
            return
    raise Praeparationsfehler("keine Regel %s/%s" % (faehigkeit, effekt))


def sonden_kiro() -> None:
    """Wirkungsnachweis fuer D-414 bis D-417 an echten kiro-Installationen."""
    root = installation("kiro")
    try:
        profil = json.loads(lies(os.path.join(root, ".kiro", "agents", "koolie.json")))
        einst = json.loads(lies(os.path.join(root, ".kiro", "settings", "cli.json")))
        hooks = json.loads(lies(os.path.join(root, ".kiro", "hooks", "koolie.json")))
        vorlage = lies(os.path.join(root, ".kiro", "steering", "40-tech-TEMPLATE.md.template"))
        regeln = profil.get("permissions", {}).get("rules", [])
        ausnahme = [r for r in regeln if r.get("exclude") == [".kiro/specs/**"]
                    and r.get("match") == [".kiro/**"] and r.get("effect") == "deny"]
        befehle = [h["action"]["command"] for h in hooks.get("hooks", [])
                   if h.get("trigger") == "PreToolUse"]
        ok = (bool(ausnahme) and einst == {"chat.agentEngine": "v3", "chat.defaultAgent": "koolie"}
              and profil.get("name") == "koolie" and len(befehle) == 1
              and "--sperrform stderr-grund" in befehle[0]
              and vorlage.startswith("---\ninclusion: fileMatch\nfileMatchPattern:\n"))
        melde("SONDE", "D414", ok,
              "kiro: Profil mit Ausnahme fuer .kiro/specs, Einstellung waehlt es, Hook mit "
              "Sperrform stderr-grund, Regelvorlage mit inclusion: fileMatch")
        if not ok:
            notiz("        Ausnahme %r, Einstellung %r, Hook %r, Vorlage %r"
                  % (ausnahme, einst, befehle, vorlage[:60]))
        kern = lies(os.path.join(root, ".kiro", "steering", "00-framework-core.md"))
        ok = not kern.startswith("---")
        melde("GEGENPROBE", "D414a", ok,
              "Eine Kernregel traegt keine Ladebedingung und laedt immer")

        frisch = validator_ausgabe(root)
        treffer = [m for m in M96 if m in frisch]
        melde("GEGENPROBE", "96g", not treffer,
              "Frische Installation: Pruefung 96 meldet nichts")
        if treffer:
            notiz("        Meldungen: %r" % treffer)

        faelle = (
            ("96", "Profil fehlt", M96_FEHLT,
             lambda r: os.remove(os.path.join(r, ".kiro", "agents", "koolie.json"))),
            ("96a", "Profil ist kein gueltiges JSON", M96_JSON,
             lambda r: schreib(os.path.join(r, ".kiro", "agents", "koolie.json"), '{ "name": ')),
            ("96b", "Einstellung waehlt einen anderen Agenten", M96_WERT,
             lambda r: schreib(os.path.join(r, ".kiro", "settings", "cli.json"),
                               '{"chat.agentEngine": "v3", "chat.defaultAgent": "kiro_default"}\n')),
            ("96c", "Regel mit unbekannter Faehigkeit", M96_FAEHIGKEIT,
             lambda r: _414_profil(r, lambda d: d["permissions"]["rules"].append(
                 {"capability": "fs_raed", "match": ["x"], "effect": "deny"}))),
            ("96d", "deny-Muster der Kernquelle entfernt", M96_DENY,
             lambda r: _414_profil(r, lambda d: _414_regeln_ohne(d, "fs_read", "deny", ".env"))),
            ("96e", "fremde allow-Regel", M96_ALLOW,
             lambda r: _414_profil(r, lambda d: d["permissions"]["rules"].append(
                 {"capability": "shell", "match": ["git commit*"], "effect": "allow"}))),
            ("96f", "Ausnahme verbreitert", M96_AUSNAHME,
             lambda r: _414_profil(r, lambda d: [x.__setitem__("exclude", [".kiro/**"])
                                                 for x in d["permissions"]["rules"]
                                                 if x.get("exclude")])),
            ("D416", "Pruefung 72: Skill ohne Freigaberegel", M416_SKILL,
             lambda r: _414_profil(r, lambda d: _414_regeln_ohne(d, "skill", "allow", "koolie-plan"))),
        )
        # Die Kennungen stehen unten WOERTLICH: Pruefung 40 liest die Sondenmenge aus dem
        # Quelltext (melde("SONDE", "<nr>")), und eine Kennung in einer Variablen ist fuer
        # sie unsichtbar - dieselbe Lehre wie bei Pruefung 12 und os.path.join (0.88.0).
        treffer = {}
        for kennung, was, marke, praeparieren in faelle:
            ziel = tempfile.mkdtemp(prefix="lw-414-")
            try:
                kopie_root = os.path.join(ziel, "projekt")
                shutil.copytree(root, kopie_root)
                praeparieren(kopie_root)
                treffer[kennung] = (marke in validator_ausgabe(kopie_root), "kiro: " + was)
            finally:
                aufraeumen(ziel)
        melde("SONDE", "96", *treffer["96"])
        melde("SONDE", "96a", *treffer["96a"])
        melde("SONDE", "96b", *treffer["96b"])
        melde("SONDE", "96c", *treffer["96c"])
        melde("SONDE", "96d", *treffer["96d"])
        melde("SONDE", "96e", *treffer["96e"])
        melde("SONDE", "96f", *treffer["96f"])
        melde("SONDE", "D416", *treffer["D416"])

        # Pruefung 86 an der Form des Packs: ein Skript, das in der Form stderr-grund
        # nichts auf stderr schreibt, sperrt bei diesem Client nichts (D-417).
        ziel = tempfile.mkdtemp(prefix="lw-417-")
        try:
            kopie_root = os.path.join(ziel, "projekt")
            shutil.copytree(root, kopie_root)
            skript = os.path.join(kopie_root, ".koolie", "core", "tests", "scripts",
                                  "hook-check-secrets.py")
            ersetze(skript, ('sys.stderr.write(reason.strip() or "Framework-Regel: gesperrt.")',
                             'print(reason)'))
            ausgabe = validator_ausgabe(kopie_root)
            melde("SONDE", "D417", M417_FORM in ausgabe,
                  "Pruefung 86: Sperrform stderr-grund ohne Grund auf stderr wird gemeldet")
        finally:
            aufraeumen(ziel)
        melde("GEGENPROBE", "D417a", M417_FORM not in frisch,
              "Das ausgelieferte Skript sperrt in der Form stderr-grund mit Grund")
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_kiro,
        "kiro: Agentenprofil, Einstellung, Ausnahme fuer die Spezifikationen und Sperrform "
        "des Schutz-Hooks - an echten Installationen")


# --- Das Client Pack cursor (CR-2026-155, D-440 bis D-443) --------------------------
#
# Pruefung 97 und die Befunde des Baus, an echten Installationen. Die Faelle der
# Berechtigungsdatei sind je einer: ein fremder Schluessel (der Client startet nicht),
# kaputtes JSON, eine entfernte Kernzusage, ein fremdes allow, ein Rueckfragekorb, ein
# unbekannter Regeltyp, ein Pfadverbot, das nie trifft, und die Ausschlussdatei.

M97 = ("Prüfung 97", "Der Client nimmt auf Projektebene nur", "Der Client startet damit nicht",
       "fehlt in permissions.deny", "in permissions.allow erzeugt die Kernquelle nicht",
       "darf nur allow und deny führen", "ist keine Regel der Gestalt",
       "trifft bei diesem Client nie", "Leseverbot '", "Ohne sie wertet das Suchwerkzeug")
M97_SCHLUESSEL = "Der Client nimmt auf Projektebene nur"
M97_JSON = "Der Client startet damit nicht"
M97_KERN = "die Kernzusage 'Read(*/.env)' fehlt in permissions.deny"
M97_ALLOW = "in permissions.allow erzeugt die Kernquelle nicht"
M97_KORB = "darf nur allow und deny führen"
M97_TYP = "ist keine Regel der Gestalt"
M97_NIE = "trifft bei diesem Client nie"
M97_IGNORE = "das Leseverbot '**/secrets/**' der Kernquelle fehlt"
M97_IGNORE_FEHLT = "Ohne sie wertet das Suchwerkzeug"
M440_ENDUNG = "Pflichtpfad fehlt: .cursor/rules/20-project-overlay.mdc"
M441_DURCHLASS = "verlangt beim Durchlass Exit 0"


def _440_cli(root: str, aenderung) -> None:
    pfad = os.path.join(root, ".cursor", "cli.json")
    daten = json.loads(lies(pfad))
    aenderung(daten)
    schreib(pfad, json.dumps(daten, ensure_ascii=False, indent=2) + "\n")


def _440_hook(eingabe: bytes, *argumente) -> tuple:
    """Der Schutz-Hook, direkt aufgerufen: (Exit, stdout)."""
    skript = os.path.join(QUELLE, ".koolie/core", "tests", "scripts", "hook-check-secrets.py")
    p = subprocess.run([sys.executable, skript] + list(argumente), input=eingabe,
                       capture_output=True, timeout=60, cwd=QUELLE)
    return p.returncode, p.stdout.decode("utf-8", "replace").strip()


def sonden_cursor() -> None:
    """Wirkungsnachweis fuer D-440 bis D-443 an echten cursor-Installationen."""
    root = installation("cursor")
    try:
        cli = json.loads(lies(os.path.join(root, ".cursor", "cli.json")))
        hooks = json.loads(lies(os.path.join(root, ".cursor", "hooks.json")))
        kern = lies(os.path.join(root, ".cursor", "rules", "00-framework-core.mdc"))
        vorlage = lies(os.path.join(root, ".cursor", "rules", "40-tech-TEMPLATE.mdc.template"))
        agent = lies(os.path.join(root, ".cursor", "agents", "koolie-reviewer.md"))
        ignore = lies(os.path.join(root, ".cursorignore")).splitlines()
        deny = cli.get("permissions", {}).get("deny", [])
        pre = hooks.get("hooks", {}).get("preToolUse", [])
        ok = (set(cli) == {"permissions"} and set(cli["permissions"]) == {"allow", "deny"}
              and "Read(*/.env)" in deny and "Read(*\\.env)" in deny
              and hooks.get("version") == 1 and len(pre) == 1 and pre[0].get("failClosed") is True
              and "--sperrform permission-json" in pre[0].get("command", "")
              and kern.startswith("---\nalwaysApply: true\n---")
              and vorlage.startswith("---\nalwaysApply: false\nglobs:\n")
              and "\nreadonly: true\n" in agent and ".env" in ignore
              and not os.path.exists(os.path.join(root, ".cursor", "rules",
                                                  "00-framework-core.md")))
        melde("SONDE", "D440", ok,
              "cursor: Berechtigungsdatei nur mit permissions, Muster in beiden Schreibweisen, "
              "Hook mit failClosed und permission-json, Regeln als .mdc, readonly-Reviewer, "
              ".cursorignore")
        if not ok:
            notiz("        cli %r, hooks %r, kern %r, vorlage %r"
                  % (sorted(cli), pre, kern[:40], vorlage[:40]))

        frisch = validator_ausgabe(root)
        treffer = [m for m in M97 if m in frisch]
        melde("GEGENPROBE", "97g", not treffer,
              "Frische Installation: Pruefung 97 meldet nichts")
        if treffer:
            notiz("        Meldungen: %r" % treffer)
        melde("GEGENPROBE", "D441a", M441_DURCHLASS not in frisch,
              "Das ausgelieferte Skript antwortet beim Durchlass in der Form permission-json")

        faelle = (
            ("97", "fremder Schluessel", M97_SCHLUESSEL,
             lambda r: _440_cli(r, lambda d: d.__setitem__("_comment", "Sonde"))),
            ("97a", "kein gueltiges JSON", M97_JSON,
             lambda r: schreib(os.path.join(r, ".cursor", "cli.json"), '{ "permissions": ')),
            ("97b", "Kernzusage entfernt", M97_KERN,
             lambda r: _440_cli(r, lambda d: d["permissions"]["deny"].remove("Read(*/.env)"))),
            ("97c", "fremde Freigabe", M97_ALLOW,
             lambda r: _440_cli(r, lambda d: d["permissions"]["allow"].append("Shell(git commit)"))),
            ("97d", "Rueckfragekorb", M97_KORB,
             lambda r: _440_cli(r, lambda d: d["permissions"].__setitem__("ask", ["Write(**)"]))),
            ("97e", "unbekannter Regeltyp", M97_TYP,
             lambda r: _440_cli(r, lambda d: d["permissions"]["deny"].append("Exec(ls)"))),
            ("97f", "Pfadverbot ohne fuehrenden Stern", M97_NIE,
             lambda r: _440_cli(r, lambda d: d["permissions"]["deny"].append("Read(geheim/**)"))),
            ("97h", "Ausschlussdatei ohne Zeile des Kerns", M97_IGNORE,
             lambda r: ersetze(os.path.join(r, ".cursorignore"), ("**/secrets/**\n", ""),
                               roh=True)),
            ("97i", "Ausschlussdatei fehlt", M97_IGNORE_FEHLT,
             lambda r: os.remove(os.path.join(r, ".cursorignore"))),
            ("D440b", "Laufzeitregel mit der Endung .md statt .mdc", M440_ENDUNG,
             lambda r: os.rename(os.path.join(r, ".cursor", "rules", "20-project-overlay.mdc"),
                                 os.path.join(r, ".cursor", "rules", "20-project-overlay.md"))),
            ("D441", "Pruefung 86: Durchlass ohne Antwort", M441_DURCHLASS,
             lambda r: ersetze(os.path.join(r, ".koolie", "core", "tests", "scripts",
                                            "hook-check-secrets.py"),
                               ('        print("{}")\r\n', '        pass\r\n'))),
        )
        # Die Kennungen stehen unten WOERTLICH (Pruefung 40 liest den Quelltext).
        treffer = {}
        for kennung, was, marke, praeparieren in faelle:
            ziel = tempfile.mkdtemp(prefix="lw-440-")
            try:
                kopie_root = os.path.join(ziel, "projekt")
                shutil.copytree(root, kopie_root)
                praeparieren(kopie_root)
                treffer[kennung] = (marke in validator_ausgabe(kopie_root), "cursor: " + was)
            finally:
                aufraeumen(ziel)
        melde("SONDE", "97", *treffer["97"])
        melde("SONDE", "97a", *treffer["97a"])
        melde("SONDE", "97b", *treffer["97b"])
        melde("SONDE", "97c", *treffer["97c"])
        melde("SONDE", "97d", *treffer["97d"])
        melde("SONDE", "97e", *treffer["97e"])
        melde("SONDE", "97f", *treffer["97f"])
        melde("SONDE", "97h", *treffer["97h"])
        melde("SONDE", "97i", *treffer["97i"])
        melde("SONDE", "D440b", *treffer["D440b"])
        melde("SONDE", "D441", *treffer["D441"])
    finally:
        aufraeumen(os.path.dirname(root))

    # Der Schutz-Hook selbst: BOM-feste Eingabe (D-441) und der Ordnername (D-442).
    bom = b"\xef\xbb\xbf"
    harmlos = json.dumps({"tool_name": "Read", "tool_input": {"file_path": "README.md"}})
    code, aus = _440_hook(bom + harmlos.encode("utf-8"), "--fail-closed",
                          "--sperrform", "permission-json")
    melde("SONDE", "D441b", code == 0 and aus == "{}",
          "Schutz-Hook: Eingabe mit BOM wird gelesen, Durchlass antwortet {}")
    geheim = json.dumps({"tool_name": "Read", "tool_input": {"file_path": ".env"}})
    code, aus = _440_hook(bom + geheim.encode("utf-8"), "--fail-closed",
                          "--sperrform", "permission-json")
    melde("GEGENPROBE", "D441c", code == 2 and '"deny"' in aus,
          "Schutz-Hook: .env mit BOM-Eingabe bleibt gesperrt")
    # D-463: gemessen am 2026-09-28 - die Eingabe kam mit ZWEI BOM an.
    code, aus = _440_hook(bom + bom + harmlos.encode("utf-8"), "--fail-closed",
                          "--sperrform", "permission-json")
    melde("SONDE", "D463", code == 0 and aus == "{}",
          "Schutz-Hook: Eingabe mit zwei BOM wird gelesen, Durchlass antwortet {}")
    code, aus = _440_hook(bom + bom + geheim.encode("utf-8"), "--fail-closed",
                          "--sperrform", "permission-json")
    melde("GEGENPROBE", "D463a", code == 2 and '"deny"' in aus,
          "Schutz-Hook: .env mit zwei BOM bleibt gesperrt")
    ordner = json.dumps({"tool_name": "Grep", "tool_input": {"file_path": "secrets"}})
    code, _ = _440_hook(ordner.encode("utf-8"), "--fail-closed")
    melde("SONDE", "D442", code == 2,
          "Schutz-Hook: eine Suche ueber den Ordner secrets wird gesperrt")
    aehnlich = json.dumps({"tool_name": "Grep", "tool_input": {"file_path": "secretary.txt"}})
    code, _ = _440_hook(aehnlich.encode("utf-8"), "--fail-closed")
    melde("GEGENPROBE", "D442a", code == 0,
          "Schutz-Hook: ein Name, der nur mit secret beginnt, bleibt frei")


buendel(sonden_cursor,
        "cursor: Berechtigungsdatei, Ausschlussdatei, Regelendung und Sperrform des "
        "Schutz-Hooks - an echten Installationen")


# --- Pruefungen 98 bis 100 und das Mandat (CR-2026-156, D-446 bis D-452) --------------
#
# Der erste Projekteinsatz (2026-09-27, devin-desktop): Der Hook sperrte nach dem INHALT
# (98), das Mandat muss dem Menschen gehoeren (99), und ein Skill mit Modellaufruf muss
# rein lesend sein (100). Das Buendel darunter misst das Mandat selbst an einer echten
# Installation - mit einem Git-Verzeichnis, denn ohne eines gibt es kein Mandat.
P98_HOOK = ".koolie/core/tests/scripts/hook-check-secrets.py".replace("/", os.sep)
P99_MANDAT = ".koolie/core/mandat.py".replace("/", os.sep)
P99_RECHTE = ".koolie/core/framework/runtime/permissions.json".replace("/", os.sep)
P100_SKILL = ".koolie/core/framework/skills/koolie-docs-update/SKILL.md".replace("/", os.sep)
M98_INHALT = "weil sein Inhalt geschuetzte Pfade NENNT"
M98_ANKER = "Pruefung 98 misst"
M99_WERTE = "fuehren verschiedene Werte fuer"
M99_DENY = "sperrt das Overlay im deny-Korb"
M99_AUSKUNFT = "die Auskunft mandat.py status endet mit Exit 2"
M99_BESCHREIBUNG = "die Auskunft mit einer Beschreibung daneben endet mit Exit 2"
M99_FEHLT = "mandat.py fehlt"
M100_MODELL = "traegt den Trigger 'model', sperrt aber"

sonde("98", "Pruefung 98: der Hook misst wieder alle Zeichenketten eines Schreibwerkzeugs",
      lambda r: ersetze(P(r, P98_HOOK), ("        zu_pruefen = list(ziele)\r\n",
                                         "        zu_pruefen = list(strings)\r\n")),
      M98_INHALT)
sonde("98a", "Pruefung 98: die Stufe der Ziele ist aus dem Hook verschwunden",
      lambda r: ersetze(P(r, P98_HOOK), ("def ziele_der_schreiboperation(",
                                         "def ziele_der_operation(", 1),
                        ("ziele = ziele_der_schreiboperation(tool_input)",
                         "ziele = ziele_der_operation(tool_input)")),
      M98_ANKER)
gegenprobe("98", "Pruefung 98: der ausgelieferte Hook misst das Ziel", None, M98_INHALT)
sonde("99", "Pruefung 99: mandat.py fuehrt eine andere Hoechstdauer als der Hook",
      lambda r: ersetze(P(r, P99_MANDAT), ("MANDAT_HOECHSTDAUER_MIN = 480",
                                           "MANDAT_HOECHSTDAUER_MIN = 999")),
      M99_WERTE)
sonde("99a", "Pruefung 99: die Kernquelle sperrt das Overlay wieder statisch",
      lambda r: ersetze(P(r, P99_RECHTE), (
          '    { "tool": "write", "pattern": "**/*.lock" },',
          '    { "tool": "write", "pattern": ".koolie/project-overlay/**" },\r\n'
          '    { "tool": "write", "pattern": "**/*.lock" },')),
      M99_DENY)
sonde("99b", "Pruefung 99: der Hook sperrt auch die Auskunft 'mandat.py status'",
      lambda r: ersetze(P(r, P98_HOOK), (
          '    auskunft = verb == "exec" and nur_mandatsauskunft(tool_input)',
          '    auskunft = False')),
      M99_AUSKUNFT)
sonde("99d", "Pruefung 99: die Auskunft zaehlt wieder jede Zeichenkette mit 'mandat'",
      lambda r: ersetze(P(r, P98_HOOK), (
          '    return isinstance(befehl, str) and bool(MANDATSAUSKUNFT.match(befehl))',
          '    strings = list(iter_strings(tool_input))\r\n'
          '    befehle = [s for s in strings if "mandat" in s.lower()]\r\n'
          '    return bool(befehle) and all(MANDATSAUSKUNFT.match(s) for s in befehle)')),
      M99_BESCHREIBUNG)
sonde("99c", "Pruefung 99: mandat.py fehlt - der Hook kennt ein Mandat, das niemand erteilen kann",
      lambda r: os.remove(P(r, P99_MANDAT)), M99_FEHLT)
gegenprobe("99", "Pruefung 99: Hook, mandat.py und Kernquelle passen zusammen", None, M99_WERTE)
sonde("100", "Pruefung 100: ein schreibender Skill traegt den Trigger 'model'",
      lambda r: ersetze(P(r, P100_SKILL), ("triggers:\r\n  - user\r\n---",
                                           "triggers:\r\n  - user\r\n  - model\r\n---")),
      M100_MODELL)
gegenprobe("100", "Pruefung 100: die modellaufrufbaren Skills sind rein lesend", None,
           M100_MODELL)


# --- Pruefung 101 und das Mandat im Validator (CR-2026-157, D-459, D-461) -------------
#
# Die Vorpruefung zu 1.18.0 hat gemessen, dass claude-code eine Rueckfrage vor eine
# Freigabe stellt: Mit mcp__* im ask-Korb lief auch das einzeln freigegebene Lesewerkzeug
# nicht. Pruefung 101 haelt die Kernquelle frei von MCP-Freigaben und gleicht in einer
# Installation Overlay Abschnitt 13.2 mit der Berechtigungsdatei ab. Das Buendel misst an
# einer echten claude-code-Installation, weil nur dieses Pack die Regelform fuehrt.
M101_KERN = "gibt ein MCP-Werkzeug im allow-Korb frei"
M101_SCHREIB = "ein Schreibwerkzeug – es verlangt"
M101_MUSTER = "ein Muster für mehrere Werkzeuge"
M101_FEHLT = "fehlt in allow"
M101_PAUSCHAL = "steht im ask-Korb, während Overlay Abschnitt 13.2"
M461_WARN = "während eines Mandats noch nicht abgeglichen"
M461_FEHLER = "Overlay-Version widersprüchlich angegeben"

sonde("101", "Pruefung 101: die Kernquelle gibt ein MCP-Werkzeug vorab frei",
      lambda r: ersetze(P(r, P99_RECHTE), (
          '    { "tool": "read",   "pattern": "**" },',
          '    { "tool": "read",   "pattern": "**" }, { "tool": "mcp", "pattern": "*" },')),
      M101_KERN)
gegenprobe("101", "Pruefung 101: die ausgelieferte Kernquelle gibt kein MCP-Werkzeug frei", None,
           M101_KERN)

P101_ZEILE_ALT = "| `<TBD: keine>` | – | – | – | – | – |"
P101_ZEILE = ("| `atlassian` | `<ISSUE_TRACKER>` | lesen für Planung, schreiben für Ablage | "
              "`getJiraIssue`, `searchJiraIssuesUsingJql` | `createJiraIssue` | Projekt KOOL |")


def _p101_rechte(root: str, allow_dazu=(), ask_ohne=(), ask_dazu=()) -> None:
    pfad = os.path.join(root, ".claude", "settings.json")
    daten = json.loads(lies(pfad))
    rechte = daten["permissions"]
    rechte["allow"] = list(rechte["allow"]) + list(allow_dazu)
    rechte["ask"] = [r for r in rechte["ask"] if r not in ask_ohne] + list(ask_dazu)
    schreib(pfad, json.dumps(daten, ensure_ascii=False, indent=2) + "\n")


def sonden_mcp() -> None:
    """Pruefung 101 und D-461 an einer echten claude-code-Installation."""
    ziel = installation("claude-code")
    try:
        ov = os.path.join(ziel, ".koolie", "project-overlay", "OVERLAY.md")
        ersetze(ov, (P101_ZEILE_ALT, P101_ZEILE))
        rechte = os.path.join(ziel, ".claude", "settings.json")
        grund = lies(rechte)
        lesen = ["mcp__atlassian__getJiraIssue", "mcp__atlassian__searchJiraIssuesUsingJql"]

        _p101_rechte(ziel, allow_dazu=["mcp__atlassian__createJiraIssue"])
        melde("SONDE", "D459", M101_SCHREIB in validator_ausgabe(ziel),
              "Ein Schreibwerkzeug der Freigabe steht in allow")
        schreib(rechte, grund)
        _p101_rechte(ziel, allow_dazu=["mcp__atlassian__*"])
        melde("SONDE", "D459a", M101_MUSTER in validator_ausgabe(ziel),
              "Ein Muster fuer den ganzen Server steht in allow")
        schreib(rechte, grund)
        melde("SONDE", "D459b", M101_FEHLT in strict_ausgabe(ziel),
              "Mit strict-overlay: ein freigegebenes Lesewerkzeug fehlt in allow")
        _p101_rechte(ziel, allow_dazu=lesen)
        melde("SONDE", "D459c", M101_PAUSCHAL in strict_ausgabe(ziel),
              "Mit strict-overlay: die pauschale MCP-Rueckfrage steht noch im ask-Korb")
        schreib(rechte, grund)
        _p101_rechte(ziel, allow_dazu=lesen, ask_ohne=["mcp__*"],
                     ask_dazu=["mcp__atlassian__createJiraIssue"])
        text = strict_ausgabe(ziel)
        melde("GEGENPROBE", "D459d", not any(m in text for m in (
            M101_SCHREIB, M101_MUSTER, M101_FEHLT, M101_PAUSCHAL)),
              "Lesewerkzeuge einzeln in allow, Schreibwerkzeug in ask, keine Pauschale")

        # D-461: die Overlay-Version waehrend eines Mandats
        ersetze(ov, ("| Overlay-Version | `<TBD: 0.1.0>` |", "| Overlay-Version | `0.4.2` |"))
        mf = os.path.join(ziel, ".koolie", "project-overlay", "overlay-manifest.yaml")
        ersetze(mf, ('overlay_version: "<TBD: 0.1.0>"', 'overlay_version: "0.4.1"'))
        os.makedirs(os.path.join(ziel, ".git"))
        text = validator_ausgabe(ziel)
        melde("SONDE", "D461", M461_FEHLER in text and M461_WARN not in text,
              "Ohne Mandat bleibt eine widerspruechliche Overlay-Version ein Fehler")
        _mandat_setzen(ziel, ["overlay"])
        text = validator_ausgabe(ziel)
        melde("GEGENPROBE", "D461a", M461_WARN in text and M461_FEHLER not in text,
              "Waehrend eines Mandats ist sie eine Warnung mit dem Befehl zum Abschluss")
        _mandat_setzen(ziel, ["overlay"], minuten=-5)
        melde("SONDE", "D461b", M461_FEHLER in validator_ausgabe(ziel),
              "Ein abgelaufenes Mandat schwaecht die Meldung nicht ab")
    finally:
        aufraeumen(os.path.dirname(ziel))


def _mandat_hook(root: str, ereignis: dict) -> tuple:
    """Der Schutz-Hook der Installation: (Exit, Ausgabe)."""
    skript = os.path.join(root, ".koolie", "core", "tests", "scripts", "hook-check-secrets.py")
    p = subprocess.run([sys.executable, skript, "--fail-closed"],
                       input=json.dumps(ereignis).encode("utf-8"), capture_output=True,
                       timeout=60, cwd=root)
    return p.returncode, (p.stdout + p.stderr).decode("utf-8", "replace")


def _mandat_setzen(root: str, umfang, minuten: int = 30, projekt: str = "") -> None:
    ende = (datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
            + datetime.timedelta(minutes=minuten))
    schreib(os.path.join(root, ".git", "koolie-mandat.json"), json.dumps({
        "rolle": "Architekt", "umfang": umfang, "bis": ende.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "projekt": projekt or os.path.realpath(root)}))


def sonden_mandat() -> None:
    """Das Mandat an einer echten Installation: es oeffnet, was es deckt, und nichts sonst."""
    root = installation("devin-desktop")
    try:
        os.makedirs(os.path.join(root, ".git"))
        overlay = {"tool_name": "write", "tool_input": {
            "file_path": ".koolie/project-overlay/OVERLAY.md", "content": "x"}}
        dokument = {"tool_name": "write", "tool_input": {
            "file_path": ".koolie/project-overlay/documents/architecture/decisions/ADR-x.md",
            "content": "x"}}
        kern = {"tool_name": "write", "tool_input": {
            "file_path": ".koolie/core/VERSION", "content": "x"}}

        exit_ohne, text_ohne = _mandat_hook(root, overlay)
        melde("SONDE", "D447", exit_ohne == 2 and "Gesperrt:" in text_ohne
              and "Loesung:" in text_ohne and "mandat.py erteilen" in text_ohne,
              "Ohne Mandat sperrt der Hook das Overlay - mit Blockade-Hinweis und Befehl")

        _mandat_setzen(root, ["overlay"])
        melde("GEGENPROBE", "D447a", _mandat_hook(root, overlay)[0] == 0,
              "Mit gueltigem Mandat (Umfang overlay) schreibt der Client in das Overlay")
        melde("SONDE", "D447b", _mandat_hook(root, kern)[0] == 2,
              "Das Mandat oeffnet den Kern nicht")

        _mandat_setzen(root, ["dokumente"])
        melde("SONDE", "D447c", _mandat_hook(root, overlay)[0] == 2
              and _mandat_hook(root, dokument)[0] == 0,
              "Umfang dokumente: OVERLAY.md bleibt gesperrt, documents/ ist offen")

        _mandat_setzen(root, ["overlay"], minuten=-5)
        melde("SONDE", "D447d", _mandat_hook(root, overlay)[0] == 2,
              "Ein abgelaufenes Mandat oeffnet nichts")
        _mandat_setzen(root, ["overlay"], minuten=2000)
        melde("SONDE", "D447e", _mandat_hook(root, overlay)[0] == 2,
              "Ein Mandat ueber der Hoechstdauer oeffnet nichts")
        _mandat_setzen(root, ["overlay"], projekt=os.path.dirname(root))
        melde("SONDE", "D447f", _mandat_hook(root, overlay)[0] == 2,
              "Ein Mandat eines anderen Projekts oeffnet nichts")
        os.remove(os.path.join(root, ".git", "koolie-mandat.json"))

        # Der Abgleich (D-452): Werte aus OVERLAY.md in die Laufzeitfassung.
        ov = os.path.join(root, ".koolie", "project-overlay", "OVERLAY.md")
        rt = os.path.join(root, ".devin", "rules", "20-project-overlay.md")
        ersetze(ov, ("| Overlay-Version | `<TBD: 0.1.0>` |", "| Overlay-Version | `0.4.2` |"))
        p = unterprozess([sys.executable, os.path.join(root, ".koolie", "core", "mandat.py"),
                          "abgleichen"])
        text = lies(rt)
        melde("SONDE", "D452", "Overlay-Version: `0.4.2`" in text
              and "Overlay-Version -> 0.4.2" in (p.stdout or ""),
              "mandat.py abgleichen uebernimmt die Overlay-Version in die Laufzeitfassung")
        vorher = text
        unterprozess([sys.executable, os.path.join(root, ".koolie", "core", "mandat.py"),
                      "abgleichen"])
        melde("GEGENPROBE", "D452a", lies(rt) == vorher,
              "Ein zweiter Abgleich aendert nichts mehr")
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_mandat,
        "Das Mandat fuer M6 an einer echten Installation: Sperre mit Hinweis, Umfang, "
        "Ablauf, Hoechstdauer, fremdes Projekt und der Abgleich der Laufzeitfassung")
buendel(sonden_mcp,
        "Pruefung 101 und das Mandat im Validator an einer echten claude-code-Installation: "
        "Schreibwerkzeug, Servermuster, fehlende Lesewerkzeuge, Pauschale und Overlay-Version")

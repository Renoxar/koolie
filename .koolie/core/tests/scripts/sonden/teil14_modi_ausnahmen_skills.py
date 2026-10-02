"""Sonden zu Modi, Ausnahmen und eingebauten Skills (1.20.2): die Modusbindung am
Schutz-Hook und ihr Schutz (Pruefung 99, K-179), die Sperre fuer das Hochladen von
Secrets in der Wirksamkeitsprobe (Pruefung 107, K-94), die beiden Werkzeugfelder eines
Skills (Pruefung 109, K-93) und die aktivierten Packs gegen die Regelablage (Pruefung 110,
K-44).

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul liest
nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import datetime
import json
import os
import shutil
import subprocess
import sys

from .apparat import (
    aufraeumen, buendel, ersetze, gegenprobe, installation, lies, melde, P,
    Praeparationsfehler, schreib, sonde, strict_ausgabe, unterprozess)

HOOK = ".koolie/core/tests/scripts/hook-check-secrets.py"
SKILL_109 = ".koolie/core/framework/skills/koolie-code-explain/SKILL.md"


def _p(root: str, rel: str) -> str:
    return P(root, rel.replace("/", os.sep))


# --- Pruefung 99, seit 1.20.2: die Modusdatei ist fuer den Client gesperrt (D-501) ----
M99_MODUS = "Schreiben der Modusdatei endet mit Exit 0"


def _99_modus_offen(root: str) -> None:
    ersetze(_p(root, HOOK), ('    re.compile(r"koolie-modus", re.I),\r\n', ""))


sonde("99e", "Ein Hook, der die Modusdatei nicht sperrt, liesse den Client seine "
            "Modusbindung selbst aufheben und wird gemeldet", _99_modus_offen, M99_MODUS)


# --- Pruefung 107, seit 1.20.2: die Probe sperrt das Hochladen von Secrets (D-503) ----
M107_INTAKT = "meldet an einem intakten Baum fehlende"


def _107_ohne_uebertragung(root: str) -> None:
    ersetze(_p(root, HOOK), ('    re.compile(r"\\bcloud\\s+drs\\s+secret-create\\b", re.I),\r\n',
                             ""))


sonde("107d", "Ein Hook ohne die Sperre fuer 'cloud drs secret-create' faellt in der "
             "Wirksamkeitsprobe durch (H3) und wird gemeldet", _107_ohne_uebertragung,
      M107_INTAKT)


# --- Pruefung 109: die beiden Werkzeugfelder eines Skills (CR-2026-164, D-505, K-93) --
M109 = "Die Werkzeugbeschränkung eines Skills wirkt nur mit beiden Feldern"


def _109_nur_allowed(root: str) -> None:
    ersetze(_p(root, SKILL_109), ("permissions:\r\n  deny:\r\n    - edit\r\n    - exec\r\n", ""))


sonde("109", "Ein Kern-Skill mit allowed-tools, aber ohne permissions wird gemeldet",
      _109_nur_allowed, M109)
gegenprobe("109", "Alle ausgelieferten Skills fuehren beide Werkzeugfelder", None, M109)


# --- Pruefung 110: die aktivierten Packs gegen die Regelablage (CR-2026-164, D-504, K-44)
M110_FEHLT = "die Ebene dieses Packs lädt in keiner Sitzung"
M110_OHNE = "aktiviert wird ein Pack im Overlay"
ROLLE = "software-development"


def _110_zeile(root: str, wert: str) -> None:
    ov = os.path.join(root, ".koolie", "project-overlay", "OVERLAY.md")
    text = lies(ov)
    alt = "`<TBD: Liste, z. B. software-development Version, oder keine>`"
    if text.count(alt) != 1:
        raise Praeparationsfehler("OVERLAY.md: die Zeile 'Aktivierte Role Packs' traegt "
                                  "nicht genau einmal den Ausfuellschlitz der Vorlage")
    schreib(ov, text.replace(alt, wert))


def sonden_aktivierte_packs() -> None:
    """Pruefung 110 an einer claude-code-Installation: Zeile gegen Laufzeitfassung."""
    root = installation("claude-code")
    try:
        aus = strict_ausgabe(root)
        melde("GEGENPROBE", "110a", M110_FEHLT not in aus and M110_OHNE not in aus,
              "Eine frische Installation (Zeile noch mit <TBD>, keine Laufzeitfassung) - "
              "unbeanstandet")
        urstand = lies(os.path.join(root, ".koolie", "project-overlay", "OVERLAY.md"))
        _110_zeile(root, "`%s` 0.1.1" % ROLLE)
        aus = strict_ausgabe(root)
        melde("SONDE", "110b", M110_FEHLT in aus and ROLLE in aus,
              "Das Overlay fuehrt ein Role Pack als aktiviert, die Laufzeitfassung fehlt - "
              "die Ebene 6 ginge still verloren")
        quelle = os.path.join(root, ".koolie", "core", "framework", "role-packs", ROLLE,
                              "runtime", "30-role-%s.md" % ROLLE)
        ziel = os.path.join(root, ".claude", "rules", "30-role-%s.md" % ROLLE)
        if not os.path.isfile(quelle):
            raise Praeparationsfehler("Die Laufzeitfassung des Role Packs %s fehlt im Kern"
                                      % ROLLE)
        shutil.copyfile(quelle, ziel)
        aus = strict_ausgabe(root)
        melde("GEGENPROBE", "110c", M110_FEHLT not in aus and M110_OHNE not in aus,
              "Genannt und vorhanden - unbeanstandet")
        schreib(os.path.join(root, ".koolie", "project-overlay", "OVERLAY.md"), urstand)
        _110_zeile(root, "`keine`")
        aus = strict_ausgabe(root)
        melde("SONDE", "110d", M110_OHNE in aus,
              "Eine Laufzeitfassung, die das Overlay nicht als aktiviert fuehrt, wird "
              "gemeldet")
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_aktivierte_packs,
        "Pruefung 110 an einer claude-code-Installation: zwei Gegenproben, zwei Sonden")


# --- Die Modusbindung am Schutz-Hook (CR-2026-164, D-501, K-179) --------------------
def _hook(root: str, ereignis: dict) -> int:
    skript = os.path.join(root, ".koolie", "core", "tests", "scripts", "hook-check-secrets.py")
    p = subprocess.run([sys.executable, skript, "--fail-closed"],
                       input=json.dumps(ereignis).encode("utf-8"), capture_output=True,
                       timeout=60, cwd=root)
    return p.returncode


def _modus_setzen(root: str, modus: str, ablage: str = "", minuten: int = 30,
                  projekt: str = "") -> None:
    ende = (datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
            + datetime.timedelta(minutes=minuten))
    daten = {"modus": modus, "bis": ende.strftime("%Y-%m-%dT%H:%M:%SZ"),
             "projekt": projekt or os.path.realpath(root)}
    if ablage:
        daten["ablage"] = ablage
    schreib(os.path.join(root, ".git", "koolie-modus.json"), json.dumps(daten))


def _schreiben(pfad: str) -> dict:
    return {"tool_name": "write", "tool_input": {"file_path": pfad, "content": "x"}}


def sonden_modusbindung() -> None:
    """Die Modusbindung an einer echten Installation: sie sperrt, was sie soll, und nichts
    sonst; die Sperre fuer das Hochladen von Secrets gilt unabhaengig davon."""
    root = installation("devin-desktop")
    try:
        os.makedirs(os.path.join(root, ".git"))
        quelle, plan = _schreiben("src/Neu.java"), _schreiben("docs/plaene/plan.md")
        melde("GEGENPROBE", "D501", _hook(root, quelle) == 0,
              "Ohne Bindung schreibt der Client wie bisher")
        _modus_setzen(root, "M1")
        melde("SONDE", "D501a", _hook(root, quelle) == 2 and _hook(root, plan) == 2,
              "M1 gebunden: jedes Schreibwerkzeug wird gesperrt")
        _modus_setzen(root, "M2", "docs/plaene")
        melde("SONDE", "D501b", _hook(root, quelle) == 2 and _hook(root, plan) == 0,
              "M2 gebunden: nur die Plan-Ablage ist offen")
        melde("SONDE", "D501c", _hook(root, _schreiben("docs/plaene/../../src/X.java")) == 2
              and _hook(root, _schreiben("docs/plaene2/x.md")) == 2,
              "Ein Punktsegment und ein Namensvetter der Ablage fuehren nicht hinein")
        melde("GEGENPROBE", "D501d", _hook(root, {"tool_name": "exec", "tool_input": {
            "command": "git status"}}) == 0,
              "Ein lesender Befehl bleibt in M2 erlaubt")
        _modus_setzen(root, "M1", minuten=-5)
        melde("GEGENPROBE", "D501e", _hook(root, quelle) == 0,
              "Eine abgelaufene Bindung sperrt nichts mehr")
        _modus_setzen(root, "M1", projekt=os.path.dirname(root))
        melde("GEGENPROBE", "D501f", _hook(root, quelle) == 0,
              "Die Bindung eines anderen Projekts gilt hier nicht")
        _modus_setzen(root, "M2", ".koolie/project-overlay")
        melde("GEGENPROBE", "D501g", _hook(root, quelle) == 0,
              "Eine Plan-Ablage in .koolie/ macht die Bindung ungueltig - der Hook liest "
              "sie nicht")
        os.remove(os.path.join(root, ".git", "koolie-modus.json"))
        mandat = os.path.join(root, ".koolie", "core", "mandat.py")
        p = unterprozess([sys.executable, mandat, "modus", "M2", "--ablage", ".koolie/x"])
        melde("SONDE", "D501h", p.returncode == 2 and not os.path.exists(
            os.path.join(root, ".git", "koolie-modus.json")),
              "mandat.py lehnt eine Plan-Ablage in .koolie/ ab und schreibt nichts")
        p = unterprozess([sys.executable, mandat, "modus", "M2", "--ablage", "docs/plaene",
                          "--minuten", "5"])
        melde("GEGENPROBE", "D501i", p.returncode == 0 and _hook(root, plan) == 0
              and _hook(root, quelle) == 2,
              "mandat.py modus M2 bindet, und der Hook liest die Bindung")
        p = unterprozess([sys.executable, mandat, "modus", "aus"])
        melde("GEGENPROBE", "D501j", _hook(root, quelle) == 0,
              "mandat.py modus aus hebt die Bindung auf")
        melde("SONDE", "D503", _hook(root, {"tool_name": "exec", "tool_input": {
            "command": "devin cloud drs secret-create --from-env X --dry-run"}}) == 2,
              "Das Hochladen von Secrets ueber die CLI wird gesperrt, auch als Probelauf")
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_modusbindung,
        "Die Modusbindung fuer M1 und M2 an einer devin-desktop-Installation: Sperre, "
        "Ablage, Ausbruch, Ablauf, fremdes Projekt, mandat.py, und die Sperre fuer das "
        "Hochladen von Secrets")

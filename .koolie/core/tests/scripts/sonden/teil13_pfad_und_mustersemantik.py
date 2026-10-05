"""Sonden zur Pfad- und Mustersemantik (1.20.1): die zweite Lesart der POSIX-Schreibweise
im Schutz-Hook (Pruefung 32, K-96), die Schreibsperren der CI- und Quality-Gate-Pfade
(Pruefung 89, K-35) und ein allow-Befehl, der ein deny-Praefix umschliesst (Pruefung 108,
K-47).

Teil des Sondenskripts probe-pruefungen.py, seit 1.19.1 in Module geteilt (K-174). Die
Einheiten melden sich beim Laden dieses Moduls an; der Einstieg laedt die Module in der
Reihenfolge ihrer Nummer, und das ist die Reihenfolge der Ausgabe (D-49). Ein Modul liest
nur aus dem Apparat und aus frueheren Teilen."""
from __future__ import annotations

import json
import os

from .apparat import (
    aufraeumen, buendel, ersetze, gegenprobe, installation, lies, melde, notiz,
    nur_unter_windows, P, Praeparationsfehler, schreib, sonde, strict_ausgabe,
    validator_ausgabe)
from .teil07_overlay_und_lieferung import _89_fuellen, _89_pfade, _89_voll

HOOK = ".koolie/core/tests/scripts/hook-check-secrets.py"
KERNQUELLE = ".koolie/core/framework/runtime/permissions.json"


def _p(root: str, rel: str) -> str:
    return P(root, rel.replace("/", os.sep))


# --- Pruefung 32, seit 1.20.1: die zweite Lesart von /c/... (CR-2026-163, D-491, K-96) --
#
# Die Sonde nimmt dem Hook die zweite Lesart und laesst ihm nur die, die Python waehlt:
# /c/ als C:\c\. Dann geht die POSIX-Schreibweise mit Punktsegment in den Kern durch -
# genau der Stand bis 1.20.0. Nur unter Windows messbar; der Sondenlauf laeuft dort.
M32_LESART = "der Hook muss beide Lesarten aufloesen"


def _32_eine_lesart(root: str) -> None:
    ersetze(_p(root, HOOK), ("    if not m:\r\n        return [echt]\r\n",
                             "    if True:\r\n        return [echt]\r\n"))


M32_SATZ = ("Ein Hook, der /c/... nur als C:\\c\\... liest, laesst die POSIX-Schreibweise "
            "in den Kern schreiben und wird gemeldet")
nur_unter_windows("SONDE", "32", M32_SATZ,
                  lambda: sonde("32", M32_SATZ, _32_eine_lesart, M32_LESART))
gegenprobe("32", "Der ausgelieferte Hook loest beide Lesarten auf", None, M32_LESART)


# --- Pruefung 108: allow umschliesst ein deny-Praefix (CR-2026-163, D-494, K-47) -----
#
# An der Kernquelle: ein allow-Befehl 'git' neben den deny-Befehlen 'git push' und
# 'git merge' - der gemessene Zuschnitt aus D-123.
M108 = "umschließt"


def _108_kernquelle(root: str) -> None:
    ersetze(_p(root, KERNQUELLE), ('    { "tool": "exec",   "command": "git status" },\r\n',
                                   '    { "tool": "exec",   "command": "git status" },\r\n'
                                   '    { "tool": "exec",   "command": "git" },\r\n'))


sonde("108", "Ein allow-Befehl git in der Kernquelle umschliesst das deny-Praefix git push "
             "und wird gemeldet", _108_kernquelle, M108)
gegenprobe("108", "Die ausgelieferte Kernquelle fuehrt keinen allow-Befehl, der ein "
                  "deny-Praefix umschliesst", None, M108)


def _108_korb(root: str, zusatz: list) -> None:
    pfad = os.path.join(root, ".claude", "settings.json")
    cfg = json.loads(lies(pfad))
    if "Bash(git push:*)" not in cfg["permissions"]["deny"]:
        raise Praeparationsfehler("settings.json: Bash(git push:*) steht nicht im deny-Korb")
    cfg["permissions"]["allow"] = cfg["permissions"]["allow"] + zusatz
    schreib(pfad, json.dumps(cfg, ensure_ascii=False, indent=2))


def sonden_allow_umschliesst_deny() -> None:
    """Pruefung 108 an einer claude-code-Installation: der installierte Korb."""
    root = installation("claude-code")
    try:
        melde("GEGENPROBE", "108a", M108 not in validator_ausgabe(root),
              "Eine frische Installation fuehrt keinen allow-Eintrag, der ein deny-Praefix "
              "umschliesst")
        urstand = lies(os.path.join(root, ".claude", "settings.json"))
        _108_korb(root, ["Bash(git:*)"])
        aus = validator_ausgabe(root)
        melde("SONDE", "108b", "Bash(git:*) im allow-Korb umschließt" in aus,
              "Bash(git:*) im allow-Korb umschliesst Bash(git push:*) - der gemessene "
              "Zuschnitt aus D-123")
        schreib(os.path.join(root, ".claude", "settings.json"), urstand)
        _108_korb(root, ["Bash(git pus:*)"])
        melde("GEGENPROBE", "108c", M108 not in validator_ausgabe(root),
              "Ein Praefix, das an keiner Wortgrenze endet (git pus), umschliesst git push "
              "nicht")
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_allow_umschliesst_deny,
        "Pruefung 108 am installierten Korb von claude-code: eine Sonde, zwei Gegenproben")


# --- Pruefung 89, seit 1.20.1: CI- und Quality-Gate-Pfade (CR-2026-163, D-493, K-35) --
#
# Die Quelle fuellt beide Schlitze mit je zwei Globs; der deny-Korb traegt sie entfaltet
# (so schreibt es install.py). Die Sonde laesst einen Glob weg - der zu eng gefuellte
# Schlitz, die stille Lockerung.
P89_CI = [".gitlab-ci.yml", ".github/workflows/**"]
P89_QG = [".eslintrc.json", "sonar-project.properties"]
M89_CI = "Ein zu eng gefüllter Schlitz ist eine stille Lockerung"


def _89_sperrschlitze(root: str, ci: list, qg: list) -> None:
    quelle, laufzeit, korb = _89_voll()
    quelle["<CI_CONFIG_PATHS>"] = ", ".join("`%s`" % g for g in P89_CI)
    quelle["<QUALITY_GATE_CONFIG_PATHS>"] = ", ".join("`%s`" % g for g in P89_QG)
    _89_fuellen(root, quelle, laufzeit, korb)
    _, _, k_pfad = _89_pfade(root)
    cfg = json.loads(lies(k_pfad))
    deny = cfg["permissions"]["deny"]
    for schlitz in ("<CI_CONFIG_PATHS>", "<QUALITY_GATE_CONFIG_PATHS>"):
        if sum(schlitz in r for r in deny) < 1:
            raise Praeparationsfehler("settings.json: der Schlitz %s steht nicht im "
                                      "deny-Korb" % schlitz)
    deny = [r for r in deny if "<CI_CONFIG_PATHS>" not in r
            and "<QUALITY_GATE_CONFIG_PATHS>" not in r]
    cfg["permissions"]["deny"] = deny + ["Edit(%s)" % g for g in ci + qg]
    schreib(k_pfad, json.dumps(cfg, ensure_ascii=False, indent=2))


def sonden_sperrschlitze() -> None:
    """Pruefung 89 (c) fuer <CI_CONFIG_PATHS> und <QUALITY_GATE_CONFIG_PATHS>."""
    root = installation("claude-code")
    try:
        _89_sperrschlitze(root, P89_CI, P89_QG)
        aus = strict_ausgabe(root)
        melde("GEGENPROBE", "89e", M89_CI not in aus,
              "Beide Schlitze gefuellt, jeder Glob mit eigener Schreibsperre - "
              "unbeanstandet")
        if M89_CI in aus:
            notiz("        gemeldet: %s" % [z for z in aus.splitlines() if M89_CI in z][:2])
        _89_sperrschlitze(root, P89_CI[:1], P89_QG)
        aus = strict_ausgabe(root)
        melde("SONDE", "89f", M89_CI in aus and ".github/workflows/**" in aus,
              "Ein CI-Glob der Quelle ohne Schreibsperre im deny-Korb wird gemeldet - der "
              "zu eng gefuellte Schlitz")
    finally:
        aufraeumen(os.path.dirname(root))


buendel(sonden_sperrschlitze,
        "Pruefung 89 (c) fuer die CI- und Quality-Gate-Pfade an einer claude-code-"
        "Installation: eine Gegenprobe, eine Sonde")

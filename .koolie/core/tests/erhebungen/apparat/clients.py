# -*- coding: utf-8 -*-
"""Je Client ein Adapter - und wo etwas nicht erhoben ist, sagt der Adapter es.

Ein Adapter kann: einen Lauf fahren (mit Folgeturns ueber die Sitzungskennung), das
Vertrauen fuer einen Baum setzen und pruefen, die Sitzungsmitschrift sichern, die
Werkzeuge aus der Startmeldung lesen und den Schutz-Hook mit einem synthetischen Ereignis
aufrufen. Was ein Adapter nicht kann, gibt er als Unerhoben zurueck - nie als Erfolg
(die Lehre aus D-276: ein Apparat, der einen Messgegenstand nie gesehen hat, meldet sein
Fehlen nicht).

Gebaut sind die Packs claude-code (vollstaendig) und cursor (Lauf mit Token-Zahlen, gemessen 2026-09-29; Kosten, Hook und Startmeldung
unerhoben); devin-desktop, openai-codex und kiro stehen als unerhoben (D-473).
"""
from __future__ import annotations

import io
import json
import os
import shutil
import subprocess
import time


class Unerhoben(Exception):
    """Diese Faehigkeit ist fuer diesen Client nicht gebaut und nicht gemessen."""


def _umgebung(**zusatz) -> dict:
    u = dict(os.environ, MSYS_NO_PATHCONV="1", PYTHONIOENCODING="utf-8")
    u.update(zusatz)
    return u


def _json_aus(roh: str) -> dict:
    """Das letzte JSON-Objekt der Ausgabe - vorangestellte Zeilen sind moeglich."""
    roh = roh or ""
    for start in [i for i, c in enumerate(roh) if c == "{"]:
        try:
            return json.loads(roh[start:])
        except ValueError:
            continue
    return {"is_error": True, "result": "keine JSON-Ausgabe"}


class Adapter:
    name = ""
    code = ""

    def lauf(self, prompt: str, baum: str, modell, berechtigung: str, sitzung=None) -> dict:
        raise Unerhoben(f"{self.name}: Lauf")

    def version(self) -> str:
        return "unerhoben"

    def vertrauen(self, baeume: list, setzen: bool) -> int:
        raise Unerhoben(f"{self.name}: Vertrauen")

    def vertrauen_gesetzt(self, baum: str) -> bool:
        raise Unerhoben(f"{self.name}: Vertrauen")

    def mitschrift(self, sitzung: str, ziel: str) -> bool:
        raise Unerhoben(f"{self.name}: Mitschrift")

    def startmeldung(self, baum: str) -> list:
        raise Unerhoben(f"{self.name}: Startmeldung")

    def hook_probe(self, baum: str) -> str:
        """Ruft die konfigurierten PreToolUse-Befehle mit einem Leseereignis auf .env auf.

        Gibt '' zurueck, wenn der Hook sperrt, sonst den Befund.
        """
        raise Unerhoben(f"{self.name}: Hook-Probe")


class AdapterCC(Adapter):
    """Pack claude-code (CP-CC)."""
    name = "claude-code"
    code = "CP-CC"
    BEFEHL = "claude"

    def _konfig(self) -> str:
        return os.path.join(os.path.expanduser("~"), ".claude.json")

    def version(self) -> str:
        p = subprocess.run([self.BEFEHL, "--version"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", env=_umgebung())
        return (p.stdout or "").strip() or "unbekannt"

    def lauf(self, prompt, baum, modell, berechtigung, sitzung=None) -> dict:
        argv = [self.BEFEHL, "-p", prompt, "--output-format", "json",
                "--permission-mode", berechtigung]
        if modell:
            argv += ["--model", modell]
        if sitzung:
            argv += ["--resume", sitzung]
        umg = _umgebung()
        umg.pop("CLAUDE_CODE_USE_POWERSHELL_TOOL", None)
        t0 = time.time()
        p = subprocess.run(argv, cwd=baum, stdin=subprocess.DEVNULL, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", env=umg)
        erg = _json_aus(p.stdout)
        usage = erg.get("usage") or {}
        return {"ergebnis": erg, "stdout": p.stdout or "", "stderr": p.stderr or "",
                "exit": p.returncode, "sekunden": round(time.time() - t0, 1),
                "sitzung": erg.get("session_id", ""), "usd": float(erg.get("total_cost_usd") or 0),
                "is_error": bool(erg.get("is_error", True)), "turns": erg.get("num_turns"),
                "abweisungen": len(erg.get("permission_denials") or []),
                "cache_neu": usage.get("cache_creation_input_tokens"),
                "cache_gelesen": usage.get("cache_read_input_tokens"),
                "antwort": erg.get("result", ""), "modell": modell or "Standard"}

    def _schluessel(self, baum: str) -> str:
        return os.path.abspath(baum).replace("\\", "/")

    def vertrauen(self, baeume, setzen) -> int:
        pfad = self._konfig()
        d = json.loads(io.open(pfad, encoding="utf-8").read())
        pr = d.setdefault("projects", {})
        n = 0
        for baum in baeume:
            k = self._schluessel(baum)
            for vorhanden in [x for x in pr if x.lower() == k.lower()]:
                del pr[vorhanden]
                n += 1
            if setzen:
                pr[k] = {"hasTrustDialogAccepted": True, "hasCompletedProjectOnboarding": True}
        io.open(pfad, "wb").write(json.dumps(d, ensure_ascii=False, indent=2).encode("utf-8"))
        return n

    def vertrauen_gesetzt(self, baum) -> bool:
        d = json.loads(io.open(self._konfig(), encoding="utf-8").read())
        k = self._schluessel(baum).lower()
        return any(x.lower() == k and v.get("hasTrustDialogAccepted")
                   for x, v in (d.get("projects") or {}).items())

    def mitschrift(self, sitzung, ziel) -> bool:
        basis = os.path.join(os.path.expanduser("~"), ".claude", "projects")
        for wurzel, _, files in os.walk(basis):
            if sitzung + ".jsonl" in files:
                shutil.copy2(os.path.join(wurzel, sitzung + ".jsonl"), ziel)
                return True
        return False

    def startmeldung(self, baum) -> list:
        """Die Werkzeugliste aus 'system/init' - der Prozess endet danach (1.18.2, D-470)."""
        umg = _umgebung()
        umg.pop("CLAUDE_CODE_USE_POWERSHELL_TOOL", None)
        p = subprocess.Popen([self.BEFEHL, "-p", "Antworte nur mit OK.", "--output-format",
                              "stream-json", "--verbose", "--max-turns", "1"],
                             cwd=baum, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL, text=True, encoding="utf-8",
                             errors="replace", env=umg)
        werkzeuge = None
        try:
            for zeile in p.stdout:
                try:
                    e = json.loads(zeile)
                except ValueError:
                    continue
                if e.get("type") == "system" and e.get("subtype") == "init":
                    werkzeuge = e.get("tools") or []
                    break
        finally:
            p.kill()
            p.wait()
        if werkzeuge is None:
            raise RuntimeError("keine Startmeldung")
        return werkzeuge

    def hook_probe(self, baum) -> str:
        pfad = os.path.join(baum, ".claude", "settings.json")
        if not os.path.isfile(pfad):
            return "keine .claude/settings.json im Baum"
        d = json.loads(io.open(pfad, encoding="utf-8-sig").read())
        befehle = [h.get("command") for eintrag in (d.get("hooks") or {}).get("PreToolUse", [])
                   for h in eintrag.get("hooks", []) if h.get("command")
                   and "Read" in (eintrag.get("matcher") or "").split("|")]
        if not befehle:
            return "kein PreToolUse-Hook mit Matcher auf Read"
        ereignis = {"hook_event_name": "PreToolUse", "tool_name": "Read", "cwd": baum,
                    "tool_input": {"file_path": os.path.join(baum, ".env")}}
        for befehl in befehle:
            p = subprocess.run(befehl, shell=True, cwd=baum, input=json.dumps(ereignis),
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", env=_umgebung(CLAUDE_PROJECT_DIR=baum))
            aus = (p.stdout or "") + (p.stderr or "")
            if p.returncode == 2 or '"deny"' in aus or '"block"' in aus:
                return ""
        return f"der Hook liess ein Leseereignis auf .env durch (Exit {p.returncode})"


class AdapterCU(Adapter):
    """Pack cursor (CP-CU): der Lauf ist gebaut; Kosten, Abweisungen, Hook-Probe unerhoben.

    Der Pfad der Agent-CLI wird gesagt (LW_CURSOR) - wie LW_DEVIN beim Apparat von 0.86.0:
    Ein Standardwert im Quelltext waere ein Arbeitsplatz, und Pruefung 71 meldete ihn.
    """
    name = "cursor"
    code = "CP-CU"

    def _agent(self) -> str:
        a = os.environ.get("LW_CURSOR", "")
        if not a or not os.path.exists(a):
            raise Unerhoben("cursor: LW_CURSOR zeigt auf keine Agent-CLI")
        return a

    def lauf(self, prompt, baum, modell, berechtigung, sitzung=None) -> dict:
        argv = ["cmd", "/c", self._agent(), "-p", prompt, "--trust", "--output-format", "json"]
        if berechtigung == "force":
            argv.append("--force")  # nur ausdruecklich: ueberspringt Rueckfragen, deny gilt (M2)
        if modell:
            argv += ["--model", modell]
        if sitzung:
            argv += ["--resume", sitzung]
        t0 = time.time()
        p = subprocess.run(argv, cwd=baum, stdin=subprocess.DEVNULL, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", env=_umgebung())
        erg = _json_aus(p.stdout)
        usage = erg.get("usage") or {}  # gemessen 2026-09-29: Token ja, Kosten nein
        return {"ergebnis": erg, "stdout": p.stdout or "", "stderr": p.stderr or "",
                "exit": p.returncode, "sekunden": round(time.time() - t0, 1),
                "sitzung": erg.get("session_id", ""), "usd": 0.0, "kosten": "unerhoben",
                "is_error": bool(erg.get("is_error", p.returncode != 0)), "turns": None,
                "abweisungen": None, "cache_neu": usage.get("cacheWriteTokens"),
                "cache_gelesen": usage.get("cacheReadTokens"),
                "antwort": erg.get("result", ""), "modell": modell or "Standard"}

    def vertrauen(self, baeume, setzen) -> int:
        return 0  # --trust je Lauf

    def vertrauen_gesetzt(self, baum) -> bool:
        return True  # --trust je Lauf


class AdapterAttrappe(Adapter):
    """Fuer den Selbsttest: liest die Antwort aus LW_ATTRAPPE (JSON je Prompt-Anfang).

    Eine Antwort kann eine Nebenwirkung tragen ('schreibe': {pfad: inhalt}), damit der
    Selbsttest das Zuruecksetzen misst, und Kosten ('usd'), damit er den Deckel misst.
    """
    name = "attrappe"
    code = "ATTRAPPE"

    def lauf(self, prompt, baum, modell, berechtigung, sitzung=None) -> dict:
        antworten = json.loads(io.open(os.environ["LW_ATTRAPPE"], encoding="utf-8").read())
        a = next((v for k, v in antworten.items() if prompt.startswith(k)), {})
        for rel, inhalt in (a.get("schreibe") or {}).items():
            ziel = os.path.join(baum, *rel.split("/"))
            os.makedirs(os.path.dirname(ziel), exist_ok=True)
            io.open(ziel, "w", encoding="utf-8").write(inhalt)
        erg = {"result": a.get("antwort", "OK"), "session_id": "attrappe-" + str(time.time()),
               "total_cost_usd": a.get("usd", 0.1), "is_error": False, "num_turns": 1,
               "permission_denials": a.get("abweisungen", []),
               "usage": {"cache_creation_input_tokens": 100, "cache_read_input_tokens": 0}}
        return {"ergebnis": erg, "stdout": json.dumps(erg), "stderr": "", "exit": 0,
                "sekunden": 0.0, "sitzung": erg["session_id"], "usd": float(erg["total_cost_usd"]),
                "is_error": False, "turns": 1, "abweisungen": len(erg["permission_denials"]),
                "cache_neu": 100, "cache_gelesen": 0, "antwort": erg["result"],
                "modell": modell or "Standard"}

    def version(self) -> str:
        return "attrappe"

    def vertrauen(self, baeume, setzen) -> int:
        return 0

    def vertrauen_gesetzt(self, baum) -> bool:
        return True

    def mitschrift(self, sitzung, ziel) -> bool:
        return False

    def hook_probe(self, baum) -> str:
        return ""


class AdapterUnerhoben(Adapter):
    def __init__(self, name: str) -> None:
        self.name = name


ADAPTER = {
    "claude-code": AdapterCC,
    "cursor": AdapterCU,
    "attrappe": AdapterAttrappe,
    "devin-desktop": lambda: AdapterUnerhoben("devin-desktop"),
    "openai-codex": lambda: AdapterUnerhoben("openai-codex"),
    "kiro": lambda: AdapterUnerhoben("kiro"),
}


def adapter(name: str) -> Adapter:
    return ADAPTER[name]()

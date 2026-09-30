#!/usr/bin/env python3
"""
wirksamkeit.py - Die Wirksamkeitsprobe: Greift die Schutzschicht im Zielprojekt?

Aufruf (aus dem Wurzelverzeichnis des Projekts, mit dem Kern des Projekts):

    python .koolie/core/install.py --probe                 # mit Startmeldung des Clients
    python .koolie/core/install.py --probe --ohne-client   # nur Hook, Konfiguration, Vertrauen

Exit-Code 0 = jede Muss-Kontrolle traegt, 1 = mindestens eine Muss-Kontrolle fehlt.

WARUM ES DIESE PROBE GIBT (K-195, D-488). Validator, 'install.py --check' und Pruefung 96
pruefen Dateien. Ob der Schutz-Hook in DIESEM Projekt laeuft und sperrt, ob die
Konfiguration laedt und ob der Client dem Projekt vertraut, prueft keines von ihnen - und
jede dieser Stellen ist schon einmal still ausgefallen: ein Hook mit einer Sperrform, die
der Client nicht liest (D-347), ein Agentenprofil, auf das der Client still verzichtet
(D-414), ein Vertrauenseintrag, ohne den bei openai-codex gar nichts laedt (K-118).

DIE PROBE KOMMT OHNE MODELL AUS:
  - Der Hook wird mit dem Befehl aufgerufen, der in der Konfiguration des Projekts steht,
    mit synthetischen Ereignissen: Lesen, Schreiben, Ausfuehren auf .env und - wo das
    Pack MCP abbildet - ein MCP-Aufruf mit einem Koederwert. Jede muss gesperrt werden.
    Ein harmloser Zugriff muss durchgehen.
  - Die Startmeldung von claude-code wird mit einer Modelladresse abgerufen, die nicht
    erreichbar ist (ANTHROPIC_BASE_URL auf einen geschlossenen Port). Der Client meldet
    Werkzeuge, MCP-Server und Hooks, bevor er das Modell ruft, und der Modellaufruf
    scheitert - gemessen am 2026-09-29 (Clientversion 2.1.284). Es entstehen keine Kosten.

EINE SPERRE WIRD AN IHREM TEXT ERKANNT, NICHT AM EXIT-CODE (D-490). Der Messapparat hat
seit 1.19.0 einen Hook als sperrend gewertet, wenn er mit Exit 2 endete. Unter Windows
startet 'cmd' den Befehl mit dem unaufgeloesten $CLAUDE_PROJECT_DIR, Python findet die
Datei nicht - und endet mit Exit 2. Ein Baum OHNE Hook-Skript bestand. Hier gilt deshalb:
Die Variable wird vor dem Aufruf ersetzt, eine Sperre muss den Hinweis 'Gesperrt:' tragen,
und die Gegenprobe muss mit Exit 0 ohne Hinweis durchgehen - das kann ein fehlendes Skript
nicht.

WAS DIE PROBE NICHT KANN - und sie sagt es als 'unerhoben', nie als Erfolg (D-276):
  - Ob der Client den Hook bei einem echten Werkzeugaufruf startet. Die Startmeldung
    belegt bei claude-code, dass die Hooks der Projektdatei geladen sind (der
    Statushook laeuft); fuer die uebrigen Packs ist keine Startmeldung ohne Modell erhoben.
  - Das Vertrauen des Schutz-Hooks bei openai-codex (ein Hash, den jede Hebung aendert).
Alle Befunde nennen Kategorien, keine Werte (D-39).
"""
from __future__ import annotations

import io
import json
import os
import re
import shutil
import subprocess
import sys

HOOK_SKRIPT = "hook-check-secrets.py"
SPERRHINWEIS = "Gesperrt:"
# Zusammengesetzt, damit der Inhaltsscan des Validators den Koeder nicht als Fund meldet.
KOEDER = "pass" + "word=" + "KOOLIE-PROBE-0000-synthetisch"
# Ein geschlossener Port: Der Client scheitert am Modellaufruf, nachdem er die
# Startmeldung geschrieben hat. Gemessen am 2026-09-29.
TOTE_MODELLADRESSE = "http" + "://" + "127.0.0.1:9"

MUSS, WARNUNG, UNERHOBEN, OK = "MUSS", "WARNUNG", "UNERHOBEN", "OK"


class Ergebnis:
    def __init__(self) -> None:
        self.zeilen: list[tuple[str, str, str]] = []

    def add(self, stufe: str, kontrolle: str, text: str) -> None:
        self.zeilen.append((stufe, kontrolle, text))

    @property
    def verletzt(self) -> list:
        return [z for z in self.zeilen if z[0] == MUSS]


# --------------------------------------------------------------- Hook-Konfiguration

def hook_datei(man: dict) -> str:
    p = man.get("runtime_placeholders", {})
    return p.get("<HOOKS_FILE>") or man.get("permissions_file", "")


def schutzhook_eintraege(daten) -> list[tuple[str, str]]:
    """(Matcher, Befehl) jedes Eintrags, der den Schutz-Hook aufruft - formatunabhaengig.

    Alle fuenf Packs fuehren den Matcher im selben Objekt wie den Befehl oder eine Ebene
    darueber (claude-code, devin-desktop, openai-codex: {matcher, hooks: [{command}]};
    cursor: {command, matcher}; kiro: {matcher, action: {command}}).
    """
    gefunden = []

    def befehle(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "command" and isinstance(v, str):
                    yield v
                else:
                    yield from befehle(v)
        elif isinstance(obj, list):
            for v in obj:
                yield from befehle(v)

    def gehe(obj):
        if isinstance(obj, dict):
            if isinstance(obj.get("matcher"), str):
                for b in befehle(obj):
                    if HOOK_SKRIPT in b:
                        gefunden.append((obj["matcher"], b))
                return
            for v in obj.values():
                gehe(v)
        elif isinstance(obj, list):
            for v in obj:
                gehe(v)

    gehe(daten)
    return gefunden


def erwartete_namen(man: dict, verben: list[str]) -> list[tuple[str, str]]:
    """(Verb, Werkzeugname) - die Namen, die der Matcher treffen muss."""
    abbildung = man.get("hook_tools") or {}
    namen = []
    for verb in verben:
        if verb == "mcp":
            for praefix in man.get("hook_mcp_prefixes") or []:
                namen.append((verb, praefix + "koolie_probe__werkzeug"))
            continue
        for name in abbildung.get(verb) or []:
            namen.append((verb, name))
    return namen


def befehl_aufloesen(befehl: str, root: str, man: dict) -> str:
    """Die Projektvariable ersetzen - so, wie der Client sie setzt (D-490)."""
    var = man.get("hook_project_dir_var")
    wurzel = root.replace("\\", "/")
    if var:
        befehl = befehl.replace("${" + var + "}", wurzel).replace("$" + var, wurzel)
        befehl = befehl.replace("%" + var + "%", wurzel)
    return befehl


def hook_rufen(befehl: str, root: str, ereignis: dict) -> tuple[int, str]:
    try:
        lauf = subprocess.run(befehl, shell=True, cwd=root, input=json.dumps(ereignis),
                              capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=30)
    except (OSError, subprocess.SubprocessError) as fehler:
        return -1, type(fehler).__name__
    return lauf.returncode, (lauf.stdout or "") + "\n" + (lauf.stderr or "")


def pruefe_hook(root: str, man: dict, verben: list[str], erg: Ergebnis) -> None:
    rel = hook_datei(man)
    pfad = os.path.join(root, *rel.split("/"))
    if not os.path.isfile(pfad):
        erg.add(MUSS, "H1 Hook konfiguriert", f"{rel} fehlt - der Schutz-Hook ist nicht "
                f"eingetragen und laeuft nicht")
        return
    try:
        daten = json.loads(io.open(pfad, encoding="utf-8-sig").read())
    except ValueError:
        erg.add(MUSS, "H1 Hook konfiguriert", f"{rel} ist kein gueltiges JSON - der Client "
                f"laedt die Datei nicht, und mit ihr keinen Hook")
        return
    eintraege = schutzhook_eintraege(daten)
    if not eintraege:
        erg.add(MUSS, "H1 Hook konfiguriert", f"{rel} ruft {HOOK_SKRIPT} in keinem Eintrag "
                f"mit Matcher auf")
        return
    erg.add(OK, "H1 Hook konfiguriert", f"{rel}: {len(eintraege)} Eintrag/Eintraege")
    matcher, befehl = eintraege[0]
    # H2: Der Matcher trifft jede Werkzeugklasse, die das Pack abbildet. Ein Matcher,
    # der eine Klasse nicht nennt, laesst ihren Aufruf ungeprueft durch (K-70, K-184) -
    # und --update schreibt diese Datei nicht (sie traegt Projektwerte).
    try:
        muster = re.compile(matcher)
    except re.error:
        muster = None
    fehlend = []
    for verb, name in erwartete_namen(man, verben):
        treffer = (muster.fullmatch(name) is not None) if muster else (
            name in matcher.split(man.get("hook_matcher_separator", "|")))
        if not treffer:
            fehlend.append(f"{verb}:{name}")
    if fehlend:
        erg.add(MUSS, "H2 Matcher vollstaendig", f"der Matcher in {rel} trifft "
                f"{', '.join(fehlend)} nicht - diese Aufrufe erreichen den Hook nicht. "
                f"Matcher aus einer frischen Installation uebernehmen "
                f"(Migrationshinweis des Releases)")
    else:
        erg.add(OK, "H2 Matcher vollstaendig", f"alle {len(erwartete_namen(man, verben))} "
                f"Werkzeugnamen getroffen")
    # H3/H4: Wirkung. Jedes Ereignis traegt hook_event_name (wie vom Client) und die
    # Marke koolie_probe, damit das Entscheidungsprotokoll die Probe ausweist.
    aufruf = befehl_aufloesen(befehl, root, man)
    abbildung = man.get("hook_tools") or {}

    def ereignis(werkzeug, eingabe):
        return {"hook_event_name": "PreToolUse", "tool_name": werkzeug, "cwd": root,
                "tool_input": eingabe, "koolie_probe": True}

    sonden = []
    for titel, verb, eingabe in (
            ("read .env", "read", {"file_path": ".env"}),
            ("write .env", "write", {"file_path": ".env", "content": "x"}),
            ("exec .env", "exec", {"command": "cat .env"}),
            # Der Weg des eingebauten Skills upload-secrets (K-94, D-503): Die CLI liest
            # die Werte selbst, im Befehl steht kein Pfad.
            ("exec Secret-Upload", "exec",
             {"command": "devin cloud drs secret-create --from-env KOOLIE_PROBE --dry-run"})):
        for name in (abbildung.get(verb) or [])[:1]:
            sonden.append((titel, ereignis(name, eingabe)))
    if "mcp" in verben:
        for praefix in (man.get("hook_mcp_prefixes") or [])[:1]:
            sonden.append(("mcp Koederwert",
                           ereignis(praefix + "koolie_probe__senden", {"text": KOEDER})))
    nicht_gesperrt = []
    for titel, e in sonden:
        code, aus = hook_rufen(aufruf, root, e)
        if SPERRHINWEIS not in aus:
            nicht_gesperrt.append(f"{titel} (Exit {code})")
    if nicht_gesperrt:
        erg.add(MUSS, "H3 Hook sperrt", "nicht gesperrt: " + "; ".join(nicht_gesperrt)
                + " - der Hook laeuft nicht oder erkennt das Werkzeug nicht")
    else:
        erg.add(OK, "H3 Hook sperrt", f"{len(sonden)} Ereignisse gesperrt")
    lesen = (abbildung.get("read") or abbildung.get("exec") or [None])[0]
    gegen = ereignis(lesen, {"file_path": "README.md"} if abbildung.get("read")
                     else {"command": "git status"})
    code, aus = hook_rufen(aufruf, root, gegen)
    if code != 0 or SPERRHINWEIS in aus:
        erg.add(MUSS, "H4 Hook laesst durch", f"ein harmloser Zugriff endete mit Exit {code}"
                f"{' und Sperrhinweis' if SPERRHINWEIS in aus else ''} - der Hook startet "
                f"nicht oder sperrt alles")
    else:
        erg.add(OK, "H4 Hook laesst durch", "harmloser Zugriff durchgelassen")


# ------------------------------------------------------------------ Startmeldung

def startmeldung_claude(root: str) -> tuple[list, list[str]]:
    """(Ereignisse bis einschliesslich system/init, Textzeilen vor dem JSON)."""
    exe = shutil.which("claude")
    if not exe:
        raise FileNotFoundError("claude")
    umg = dict(os.environ, ANTHROPIC_BASE_URL=TOTE_MODELLADRESSE)
    p = subprocess.Popen([exe, "-p", "OK", "--output-format", "stream-json", "--verbose",
                          "--max-turns", "1"], cwd=root, stdin=subprocess.DEVNULL,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                         encoding="utf-8", errors="replace", env=umg)
    ereignisse, text = [], []
    try:
        for zeile in p.stdout:
            try:
                e = json.loads(zeile)
            except ValueError:
                if zeile.strip():
                    text.append(zeile.strip())
                continue
            ereignisse.append(e)
            if e.get("type") == "system" and e.get("subtype") == "init":
                break
    finally:
        p.kill()
        p.wait()
    return ereignisse, text


def pruefe_start_claude(root: str, erg: Ergebnis) -> None:
    try:
        ereignisse, text = startmeldung_claude(root)
    except (FileNotFoundError, OSError):
        erg.add(UNERHOBEN, "K1 Konfiguration laedt", "der Befehl 'claude' ist nicht "
                "auffindbar - Startmeldung nicht abgerufen")
        return
    init = next((e for e in ereignisse if e.get("subtype") == "init"), None)
    if init is None:
        erg.add(MUSS, "K1 Konfiguration laedt", "keine Startmeldung - der Client startet "
                "in diesem Verzeichnis nicht")
        return
    status = [e for e in ereignisse if e.get("subtype") == "hook_response"
              and "Framework-Statusmeldung" in str(e.get("output", ""))]
    if status and all(e.get("outcome") == "success" for e in status):
        erg.add(OK, "K1 Konfiguration laedt", "Startmeldung ohne Modellaufruf; der "
                "Statushook des Frameworks lief - die Hooks der Projektdatei sind geladen")
    else:
        erg.add(MUSS, "K1 Konfiguration laedt", "der Statushook des Frameworks lief nicht - "
                "die Hooks der Projektdatei sind nicht geladen (ungueltige Datei oder "
                "verworfener Schluessel, vgl. D-433)")
    if any("not been trusted" in z for z in text):
        erg.add(WARNUNG, "V1 Vertrauen", "der Client vertraut dem Arbeitsbereich nicht und "
                "ignoriert die allow-Eintraege der Projektdatei; deny, ask und Hooks gelten "
                "(gemessen 2026-09-29). Einmal interaktiv starten und vertrauen")
    else:
        erg.add(OK, "V1 Vertrauen", "keine Meldung ueber fehlendes Vertrauen")
    # Die Connectoren verbinden sich nebenlaeufig: Die Werkzeugliste der Startmeldung
    # kann einen Server noch nicht fuehren, die Serverliste fuehrt ihn (gemessen
    # 2026-09-29). Gezaehlt wird deshalb die Serverliste; abgeschaltet ist die Quelle,
    # wenn die Projektdateien 'mcp__claude_ai_*' sperren - dann fehlen ihre Werkzeuge.
    konto = sorted(s.get("name", "?") for s in init.get("mcp_servers") or []
                   if s.get("source") == "claudeai")
    if konto and not konto_gesperrt(root):
        erg.add(WARNUNG, "M1 Konto-Connectoren", f"{len(konto)} Connector(en) des "
                f"claude.ai-Kontos stehen in der Sitzung ({', '.join(konto)}) - eine Quelle "
                f"ausserhalb des Projekts (K-191). Abschalten fuer dieses Projekt: "
                f"'mcp__claude_ai_*' in permissions.deny (gemessen 2026-09-29)")
    elif konto:
        erg.add(OK, "M1 Konto-Connectoren", f"{len(konto)} Connector(en) des Kontos "
                f"verbunden, ihre Werkzeuge durch 'mcp__claude_ai_*' gesperrt")
    else:
        erg.add(OK, "M1 Konto-Connectoren", "keine Connectoren des Kontos in der Sitzung")


def konto_gesperrt(root: str) -> bool:
    for rel in (".claude/settings.json", ".claude/settings.local.json"):
        try:
            d = json.loads(io.open(os.path.join(root, *rel.split("/")),
                                   encoding="utf-8-sig").read())
        except (OSError, ValueError):
            continue
        if "mcp__claude_ai_*" in ((d.get("permissions") or {}).get("deny") or []):
            return True
    return False


# ------------------------------------------------------------------- Vertrauen

def _pfadformen(root: str) -> set:
    r = os.path.abspath(root)
    return {r.lower(), r.replace("\\", "/").lower(), r.replace("/", "\\").lower()}


def pruefe_vertrauen_codex(root: str, erg: Ergebnis) -> None:
    """K-118 (2): Die Benutzerkonfiguration traegt das Projekt als vertraut."""
    heim = os.environ.get("CODEX_HOME") or os.path.join(os.path.expanduser("~"), ".codex")
    pfad = os.path.join(heim, "config.toml")
    try:
        text = io.open(pfad, encoding="utf-8").read()
    except OSError:
        erg.add(MUSS, "V1 Vertrauen", "keine Benutzerkonfiguration des Clients - ohne "
                "Vertrauenseintrag laden Konfiguration, Hooks und Befehlsregeln nicht (K-118)")
        return
    formen = _pfadformen(root)
    vertraut = False
    abschnitt = None
    for zeile in text.splitlines():
        m = re.match(r"""^\s*\[projects\.(["'])(.+)\1\]\s*$""", zeile)
        if m:
            abschnitt = m.group(2).replace("\\\\", "\\").lower()
            continue
        if zeile.strip().startswith("["):
            abschnitt = None
        if abschnitt in formen and re.match(r"""^\s*trust_level\s*=\s*["']trusted["']""",
                                            zeile):
            vertraut = True
    if vertraut:
        erg.add(OK, "V1 Vertrauen", "Projekt in der Benutzerkonfiguration als vertraut")
    else:
        erg.add(MUSS, "V1 Vertrauen", "das Projekt steht nicht als vertraut in der "
                "Benutzerkonfiguration - Konfiguration, Hooks und Befehlsregeln laden nicht "
                "(K-118). Einmal interaktiv starten und vertrauen")
    erg.add(UNERHOBEN, "V2 Vertrauen des Hooks", "der Hash, mit dem der Client dem "
            "Schutz-Hook vertraut, ist nicht pruefbar; nach jeder Hebung neu bestaetigen")


def pruefe_profil_kiro(root: str, man: dict, erg: Ergebnis) -> None:
    rel = man.get("permissions_file", "")
    pfad = os.path.join(root, *rel.split("/"))
    try:
        json.loads(io.open(pfad, encoding="utf-8-sig").read())
    except (OSError, ValueError):
        erg.add(MUSS, "V1 Profil", f"{rel} fehlt oder ist kein gueltiges JSON - der Client "
                f"faellt still auf seinen eingebauten Agenten zurueck (D-414)")
        return
    erg.add(OK, "V1 Profil", f"{rel} lesbar")


# ------------------------------------------------------------------- Einstieg

def probe(root: str, man: dict, client: str, verben: list[str], mit_client: bool) -> Ergebnis:
    erg = Ergebnis()
    pruefe_hook(root, man, verben, erg)
    if client == "claude-code":
        if mit_client:
            pruefe_start_claude(root, erg)
        else:
            erg.add(UNERHOBEN, "K1 Konfiguration laedt", "ohne Startmeldung (--ohne-client)")
    elif client == "openai-codex":
        pruefe_vertrauen_codex(root, erg)
        erg.add(UNERHOBEN, "K1 Konfiguration laedt", "fuer dieses Pack ist keine "
                "Startmeldung ohne Modell erhoben")
    elif client == "kiro":
        pruefe_profil_kiro(root, man, erg)
        erg.add(UNERHOBEN, "K1 Konfiguration laedt", "fuer dieses Pack ist keine "
                "Startmeldung ohne Modell erhoben; die Hooks laufen nur interaktiv (D-417)")
    else:
        erg.add(UNERHOBEN, "K1 Konfiguration laedt", "fuer dieses Pack ist keine "
                "Startmeldung ohne Modell erhoben")
        erg.add(UNERHOBEN, "V1 Vertrauen", "der Vertrauensspeicher dieses Clients ist nicht "
                "erhoben")
    for verb in man.get("hook_tools_unerhoben") or []:
        erg.add(UNERHOBEN, f"H5 Werkzeugklasse {verb}", "fuer diesen Client nicht am Hook "
                "gemessen - Aufrufe dieser Klasse prueft der Schutz-Hook nicht")
    return erg


def ausgeben(erg: Ergebnis, root: str, client: str) -> int:
    print(f"Wirksamkeitsprobe - {client} - {root}")
    print()
    for stufe, kontrolle, text in erg.zeilen:
        marke = {"OK": "ok      ", "MUSS": "FEHLT   ", "WARNUNG": "WARNUNG ",
                 "UNERHOBEN": "unerhob."}[stufe]
        print(f"  {marke} {kontrolle}: {text}")
    print()
    n = len(erg.verletzt)
    print(f"Ergebnis: {n} Muss-Kontrolle(n) fehlen, "
          f"{sum(1 for z in erg.zeilen if z[0] == WARNUNG)} Warnung(en), "
          f"{sum(1 for z in erg.zeilen if z[0] == UNERHOBEN)} unerhoben.")
    if n:
        print("Die Schutzschicht greift in diesem Projekt nicht vollstaendig. Vor der Arbeit "
              "beheben.")
    return 1 if n else 0


if __name__ == "__main__":
    print("Aufruf ueber install.py --probe (es kennt das installierte Pack).", file=sys.stderr)
    sys.exit(2)

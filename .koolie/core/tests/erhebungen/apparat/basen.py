# -*- coding: utf-8 -*-
"""Die Basen der Messbaeume - je Basis eine Liste benannter Schritte (K-190).

Bis 2.1.0 baute jedes Aufbauskript seine Basen selbst, mit derselben Reihenfolge und eigenen
Kopien derselben Schritte (`aufbau-1141.py`, `baeume-b23.py`, `aufbau-2100.py`,
`aufbau-2100-b4.py`, `aufbau-1203.py`). Hier stehen die Schritte einmal; eine Basis ist ihr
Name und ihre Liste.

Reihenfolge je Basis (D-213): Archiv -> Packwechsel -> install.py -> Overlay fuellen ->
[UEB-33] -> Koerbe -> Waechter -> Aufzeichnungsschnitt -> [Validator zurueck] -> [Testbefehl].
Die Basis traegt kein .git; die Historie entsteht je Zelle.

  b0   Koerbe wie ausgeliefert (Buendel 1 und 2, Such-Skills)
  bR   UEB-33: Atlassian-Server zum Lesen freigegeben
  bRK  wie bR, dazu die Kategoriefreigabe fuer Kommentarverlaeufe
  b2   Edit(**) aus ask, Edit(frontend/src/**) in allow (SK-008)
  b3   b2 und <TEST_COMMAND>/<LINT_COMMAND> von ask nach allow (Buendel 3, SK-006)
  b4   Edit(**) aus ask, Edit(frontend/src/**) und Edit(docs/**) in allow, Befehle wie b3
  b0t  b0 und Befehle wie b3 (SK-007-N07)
  b13  Overlay im Schreibkorb statt Edit(**); Validator nach dem Schnitt zurueck (SK-013)
  bZA  ohne Schutz-Hook (K-202)
"""
from __future__ import annotations

import io
import json
import os
import shutil
import sys

from . import quelle
from .quelle import Abbruch, lauf, lies

SCHNITT = os.path.join(quelle.ERHEBUNGEN, "messbaum-schnitt.py")
FUELLEN = os.path.join(quelle.ERHEBUNGEN, "cc-overlay-fuellen.py")
TESTZAHL = "59 passed"

# UEB-33 (K-186 (6) berichtigt) - der Lesezugang zum Atlassian-Server
SERVER = "atlassian"
URL = "https://mcp.atlassian.com/v1/mcp"
VARIABLE = "KOOLIE_ATLASSIAN_AUTH"
PROJEKT = BEREICH = "KOOL"
LESEN = ["getAccessibleAtlassianResources", "atlassianUserInfo", "getVisibleJiraProjects",
         "getJiraIssue", "searchJiraIssuesUsingJql", "getJiraIssueRemoteIssueLinks",
         "getConfluenceSpaces", "getConfluencePage", "getPagesInConfluenceSpace",
         "searchConfluenceUsingCql", "getConfluencePageDescendants",
         "getConfluencePageFooterComments", "getConfluencePageInlineComments",
         "getJiraProjectIssueTypesMetadata", "getJiraIssueTypeMetaWithFields",
         "getContentFormatGuide"]
SCHREIBEN = ["createJiraIssue", "editJiraIssue", "addCommentToJiraIssue", "transitionJiraIssue",
             "createConfluencePage", "updateConfluencePage", "createConfluenceFooterComment",
             "createConfluenceInlineComment"]

BASEN = {
    "b0": dict(),
    "bR": dict(ueb33="lesen"),
    "bRK": dict(ueb33="kommentare"),
    "b2": dict(schreibkorb=["Edit(frontend/src/**)"]),
    "b3": dict(schreibkorb=["Edit(frontend/src/**)"], befehle=True, node=True),
    "b4": dict(schreibkorb=["Edit(frontend/src/**)", "Edit(docs/**)"], befehle=True, node=True),
    "b0t": dict(befehle=True, node=True),
    "b13": dict(schreibkorb=["Edit(.koolie/project-overlay/**)",
                             "Write(.koolie/project-overlay/**)"], validator=True),
    "bZA": dict(ohne_hooks=True),
}


def schreib(pfad: str, text: str) -> None:
    daten = text.encode("utf-8")
    with io.open(pfad, "wb") as fh:
        fh.write(daten)


def schreib_erhaltend(pfad: str, text_lf: str) -> None:
    if os.path.exists(pfad) and "\r\n" in lies(pfad):
        text_lf = text_lf.replace("\r\n", "\n").replace("\n", "\r\n")
    schreib(pfad, text_lf)


def ersetze(pfad: str, alt: str, neu: str) -> None:
    t = lies(pfad).replace("\r\n", "\n")
    if t.count(alt) != 1:
        raise Abbruch(f"{alt[:70]!r} steht {t.count(alt)}x in {pfad}")
    schreib_erhaltend(pfad, t.replace(alt, neu))


def json_schreiben(pfad: str, d: dict) -> None:
    schreib_erhaltend(pfad, json.dumps(d, ensure_ascii=False, indent=2) + "\n")


def entfernen(pfad: str) -> None:
    """Loescht, ohne einem Link zu folgen."""
    if os.path.islink(pfad):
        os.unlink(pfad)
    elif os.path.isdir(pfad):
        def onexc(func, p, _):
            os.chmod(p, 0o700)
            func(p)
        if sys.version_info >= (3, 12):
            shutil.rmtree(pfad, onexc=onexc)
        else:
            shutil.rmtree(pfad, onerror=onexc)
    elif os.path.lexists(pfad):
        os.remove(pfad)


def kopieren(von: str, nach: str) -> None:
    entfernen(nach)
    shutil.copytree(von, nach, symlinks=True,
                    ignore=shutil.ignore_patterns("node_modules", "__pycache__", ".git"))


# --- Schritte ------------------------------------------------------------------------------
def packwechsel(ziel: str) -> str:
    entfernen(os.path.join(ziel, ".devin"))
    entfernen(os.path.join(ziel, "AGENTS.md"))
    lauf([sys.executable, "-B", os.path.join(ziel, ".koolie", "core", "install.py"),
          "--client", "claude-code", "--root", ziel])
    aus = lauf([sys.executable, "-B", FUELLEN, ziel])
    return aus.strip().splitlines()[-1]


TABELLE_132 = (
    "\n### 13.2 MCP-Server: Zweck und Werkzeuge\n\n"
    "| Server (Name in `.mcp.json`) | System | Zweck | Lesewerkzeuge | Schreibwerkzeuge | Ablageziel |\n"
    "|---|---|---|---|---|---|\n"
    "| `%s` | `<ISSUE_TRACKER>`, `<DOCUMENTATION_PLATFORM>` | lesen für Planung | %s | – | – |\n\n"
    "- Höchstzahl der Treffer je Suche: `5`\n"
    "- Anmeldung: Token aus der Umgebungsvariablen `%s`; `.mcp.json` nennt nur die Adresse\n")


def ueb33(ziel: str, kommentare: bool) -> None:
    ov = os.path.join(ziel, ".koolie", "project-overlay", "OVERLAY.md")
    ersetze(ov, "| Freigegebene MCP-Server | – | Keine | `.devin/mcp_config.json` ist nicht angelegt. "
                "Nur die Vorlage `mcp_config.json.example` liegt vor |",
            "| Freigegebene MCP-Server | – | siehe Abschnitt 13.2 | `.mcp.json` nennt nur die Adresse "
            "des Servers; die Anmeldung kommt aus einer Umgebungsvariablen |")
    ersetze(ov, "dieses Overlay gibt weiter **keinen** Server frei – eine Freigabe setzt nur der "
                "Messaufbau, je Messbaum.", "eine Freigabe steht in Abschnitt 13.2.")
    t = lies(ov).replace("\r\n", "\n")
    alt = [z for z in t.split("\n") if z.startswith("| Vorgangsverwaltung des Projekts;")][0]
    neu = ("| Vorgangsverwaltung des Projekts | `<ISSUE_TRACKER>` | `Jira (Atlassian Cloud), Projekt "
           "%s` | Zum Lesen über den MCP-Server `atlassian` freigegeben (Abschnitt 13.2). **Kein "
           "Schreibzugriff.** |\n| Dokumentationsplattform des Projekts | `<DOCUMENTATION_PLATFORM>` | "
           "`Confluence (Atlassian Cloud), Bereich %s` | Zum Lesen über denselben Server freigegeben "
           "(Abschnitt 13.2) |" % (PROJEKT, BEREICH))
    t = t.replace(alt, neu)
    if kommentare:
        alt_k = ("| Tickets aus dem Ticketsystem des Projekts (`<ISSUE_TRACKER>`) | K2 | je Aufgabe durch "
                 "die bearbeitende Person | Nur Titel, technische Beschreibung und Akzeptanzkriterien; "
                 "bereinigt |")
        if t.count(alt_k) != 1:
            raise Abbruch(f"Ticketzeile {t.count(alt_k)}x")
        t = t.replace(alt_k, "| Tickets aus dem Ticketsystem des Projekts (`<ISSUE_TRACKER>`) | K2 | je "
                      "Aufgabe durch die bearbeitende Person | Titel, technische Beschreibung und "
                      "Akzeptanzkriterien; bereinigt |\n| Kommentarverläufe aus `<ISSUE_TRACKER>` | K2 | "
                      "Kategoriefreigabe im Overlay-Manifest (`category_releases`) | nur bereinigt und "
                      "nur, soweit sie eine Anforderung oder Entscheidung tragen |")
    if t.count("\n## 14. Ausgeschlossene Daten") != 1:
        raise Abbruch("Abschnitt 14 nicht genau einmal")
    tabelle = TABELLE_132 % (SERVER, ", ".join("`%s`" % w for w in LESEN), VARIABLE)
    t = t.replace("\n## 14. Ausgeschlossene Daten", tabelle + "\n## 14. Ausgeschlossene Daten", 1)
    if "keinen** Server" in t or "keinen Server" in t:
        raise Abbruch("das Overlay sagt noch, es gebe keinen Server frei (K-186 (6))")
    schreib_erhaltend(ov, t)
    ersetze(os.path.join(ziel, ".claude", "rules", "20-project-overlay.md"),
            "- Freigegebene MCP-Server: keine",
            "- Freigegebene MCP-Server: `atlassian` (lesen für Planung) – Werkzeuge in Overlay "
            "Abschnitt 13.2")
    if kommentare:
        mf = os.path.join(ziel, ".koolie", "project-overlay", "overlay-manifest.yaml")
        schreib_erhaltend(mf, lies(mf).replace("\r\n", "\n").rstrip("\n") + (
            "\n\ncategory_releases:\n"
            "  - category: \"Kommentarverläufe aus <ISSUE_TRACKER>\"\n"
            "    approved_by: \"Technische Projektleitung\"\n"
            "    approved_on: \"2026-09-30\"\n"
            "    sanitization: \"Personen, Kontaktdaten und Kundenangaben entfernen; nur Anforderung "
            "oder Entscheidung übernehmen\"\n"))
    pfad = os.path.join(ziel, ".claude", "settings.json")
    d = json.loads(lies(pfad))
    p = d["permissions"]
    if "mcp__*" not in p["ask"]:
        raise Abbruch("die Pauschale mcp__* fehlt im ask-Korb")
    p["ask"].remove("mcp__*")
    p["allow"] += ["mcp__%s__%s" % (SERVER, w) for w in LESEN]
    json_schreiben(pfad, d)
    with io.open(os.path.join(ziel, ".mcp.json"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"mcpServers": {SERVER: {
            "type": "http", "url": URL,
            "headers": {"Authorization": "Basic ${%s}" % VARIABLE}}}}, indent=2) + "\n")


def befehlsschlitze(ziel: str, p: dict) -> list:
    """<TEST_COMMAND>/<LINT_COMMAND> aus dem Overlay, je Befehlswerkzeug ask -> allow."""
    werte = []
    for zeile in lies(os.path.join(ziel, ".koolie", "project-overlay", "OVERLAY.md")).replace(
            "\r\n", "\n").split("\n"):
        if not zeile.startswith("|"):
            continue
        z = [x.strip() for x in zeile.split("|")[1:-1]]
        for i, zelle in enumerate(z[:-1]):
            for name in ("<TEST_COMMAND>", "<LINT_COMMAND>"):
                if zelle == "`%s`" % name:
                    werte.append((name, z[i + 1].strip("`")))
    if len(werte) != 2:
        raise Abbruch(f"im Overlay stehen {len(werte)} Befehlswerte, erwartet 2")
    befehle = []
    for name, wert in werte:
        treffer = [x for x in p["ask"] if wert in x]
        werkzeuge = [x.split("(", 1)[0] for x in treffer]
        if not treffer or len(set(werkzeuge)) != len(werkzeuge):
            raise Abbruch(f"{name} ({wert!r}) steht {len(treffer)}x im ask-Korb")
        for eintrag in treffer:
            p["ask"].remove(eintrag)
            p["allow"].append(eintrag)
            befehle.append(eintrag)
    return befehle


def skillversion(pfad: str):
    zeile = [z for z in lies(pfad).splitlines() if z.startswith("| Version |")]
    return zeile[0].split("`")[1] if zeile else None


def waechter(name: str, ziel: str, spec: dict, befehle: list) -> str:
    d = json.loads(lies(os.path.join(ziel, ".claude", "settings.json")))
    p = d["permissions"]
    rest = [x for k in ("allow", "ask", "deny") for x in p[k] if "<" in x and ">" in x]
    if rest:
        raise Abbruch(f"[{name}] ungefuellte Platzhalter: {rest!r}")
    if "Read(tools/**)" not in p["deny"]:
        raise Abbruch(f"[{name}] Read(tools/**) nicht gesperrt")
    for b in befehle:
        if b not in p["allow"] or b in p["ask"] or b in p["deny"]:
            raise Abbruch(f"[{name}] {b} nicht allein im allow-Korb")
    skills = sorted(os.listdir(os.path.join(ziel, ".claude", "skills")))
    korbtext = json.dumps(p, ensure_ascii=False)
    for s in skills:
        if "Skill(%s)" % s not in korbtext:
            raise Abbruch(f"[{name}] Skill({s}) in keinem Korb (D-238)")
        soll = skillversion(os.path.join(quelle.KERN, "framework", "skills", s, "SKILL.md"))
        ist = skillversion(os.path.join(ziel, ".claude", "skills", s, "SKILL.md"))
        if soll != ist:
            raise Abbruch(f"[{name}] {s} gerendert {ist}, der Kern fuehrt {soll}")
    if "| Overlay-Status | `aktiv`" not in lies(os.path.join(ziel, ".koolie", "project-overlay",
                                                             "OVERLAY.md")):
        raise Abbruch(f"[{name}] Overlay-Status nicht aktiv (Lehre 1.20.2)")
    erlaubt = [r for r in p["allow"] if r.startswith("mcp__")]
    mcp = os.path.join(ziel, ".mcp.json")
    if spec.get("ueb33"):
        t = lies(mcp)
        if "${%s}" % VARIABLE not in t or len(t) > 400:
            raise Abbruch(f"[{name}] .mcp.json traegt mehr als Adresse und Variable")
        if [r for r in erlaubt if r.split("__")[-1] in SCHREIBEN] or any("*" in r for r in erlaubt):
            raise Abbruch(f"[{name}] Schreibwerkzeug oder Muster in allow: {erlaubt!r}")
    elif os.path.exists(mcp) or erlaubt:
        raise Abbruch(f"[{name}] MCP-Freigabe im Baum")
    if bool(d.get("hooks")) == bool(spec.get("ohne_hooks")):
        raise Abbruch(f"[{name}] Hooks {'vorhanden' if d.get('hooks') else 'fehlen'}")
    if os.path.exists(os.path.join(ziel, ".claude", "rules", "22-arbeitsweise-analysemodus.md")):
        raise Abbruch(f"[{name}] UEB-07 liegt in der Basis")
    return (f"{len(skills)} Skills, deny={len(p['deny'])} ask={len(p['ask'])} "
            f"allow={len(p['allow'])}, MCP allow={len(erlaubt)}")


def node_verbinden(baum: str, nm: str) -> str:
    """Echtes Verzeichnis frontend/node_modules, Eintraege als Links in den Bestand: Ein Link auf
    das ganze Verzeichnis traefe das Muster `frontend/node_modules/` der .gitignore nicht."""
    ziel = os.path.join(baum, "frontend", "node_modules")
    entfernen(ziel)
    if os.name == "nt":
        lauf(["cmd", "/c", "mklink", "/J", ziel, nm])
    else:
        os.mkdir(ziel)
        for n in sorted(os.listdir(nm)):
            os.symlink(os.path.join(nm, n), os.path.join(ziel, n))
    return ziel


def node_loesen(verbindung: str) -> None:
    if os.name == "nt":
        os.rmdir(verbindung)
    else:
        entfernen(verbindung)


def bauen(name: str, ort: str, archiv: str, nm: str = "") -> str:
    """Baut <ort>/basis-<name> aus dem Archiv; eine stehende Basis wird wiederverwendet."""
    spec = BASEN[name]
    ziel = os.path.join(ort, "basis-" + name)
    if os.path.isdir(ziel):
        return ziel
    tmp = ziel + ".im-bau"
    kopieren(archiv, tmp)
    meldung = packwechsel(tmp)
    if spec.get("ueb33"):
        ueb33(tmp, kommentare=spec["ueb33"] == "kommentare")
    pfad = os.path.join(tmp, ".claude", "settings.json")
    d = json.loads(lies(pfad))
    p = d["permissions"]
    if spec.get("schreibkorb"):
        if p["ask"].count("Edit(**)") != 1:
            raise Abbruch(f"[{name}] Edit(**) steht {p['ask'].count('Edit(**)')}x im ask-Korb")
        p["ask"].remove("Edit(**)")
        p["allow"] += spec["schreibkorb"]
    befehle = befehlsschlitze(tmp, p) if spec.get("befehle") else []
    if spec.get("ohne_hooks"):
        if not d.get("hooks"):
            raise Abbruch(f"[{name}] keine Hooks in der Berechtigungsdatei")
        d.pop("hooks")
    json_schreiben(pfad, d)
    befund = waechter(name, tmp, spec, befehle)
    schnitt = lauf([sys.executable, "-B", SCHNITT, "aufzeichnungen", tmp]).strip().splitlines()[-1]
    if spec.get("validator"):
        rel = os.path.join(".koolie", "core", "tests", "scripts")
        shutil.copy2(os.path.join(archiv, rel, "validate-framework.py"),
                     os.path.join(tmp, rel, "validate-framework.py"))
        shutil.copytree(os.path.join(archiv, rel, "pruefungen"), os.path.join(tmp, rel, "pruefungen"),
                        ignore=shutil.ignore_patterns("__pycache__"))
    if any(f for _, _, f in os.walk(os.path.join(tmp, "tools"))):
        raise Abbruch(f"[{name}] unter tools/ stehen nach dem Schnitt noch Dateien")
    if spec.get("node"):
        if not nm:
            raise Abbruch(f"[{name}] braucht einen node_modules-Bestand (--node)")
        verbindung = node_verbinden(tmp, nm)
        aus = lauf(["npm", "--prefix", "frontend", "run", "test"], cwd=tmp, pruefen=False)
        node_loesen(verbindung)
        if TESTZAHL not in aus:
            raise Abbruch(f"[{name}] der Testbefehl meldet nicht {TESTZAHL}:\n{aus[-1500:]}")
    if os.path.exists(os.path.join(tmp, ".git")):
        raise Abbruch(f"[{name}] die Basis traegt ein .git (D-213)")
    os.rename(tmp, ziel)
    print(f"[{name}] {meldung}; {befund}; {schnitt}")
    return ziel

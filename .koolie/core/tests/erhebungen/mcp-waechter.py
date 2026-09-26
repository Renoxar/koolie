# -*- coding: utf-8 -*-
"""Waechter ueber die MCP-Ausstattung eines Messbaums - gegen SEIN Overlay (K-89, D-256).

    python mcp-waechter.py vorher <baum>       # vor der Reihe: die Konfigurationsquellen
    python mcp-waechter.py nachher             # nach der Reihe: die Mitschriften

🔴 DER ANLASS IST GEMESSEN (2026-09-22, Messtag von Buendel 5). Das Uebungs-Overlay
fuehrt *"Freigegebene MCP-Server: keine"*; die dreissig Sitzungen bekamen zwei gestellt,
weil sie in der BENUTZERKONFIGURATION des Arbeitsplatzes stehen und nicht je Projekt.
**19 von 30 Laeufen haben den Widerspruch gemeldet, null ein MCP-Werkzeug aufgerufen.**

Das ist D-237 mit umgekehrtem Vorzeichen: dort war *installiert* weniger als *vorhanden*,
hier ist *vorhanden* mehr als *freigegeben*.

  Ein Messbaum erbt die Ausstattung des Arbeitsplatzes, nicht nur seine Dateien.

🔴 DER WAECHTER NENNT, ER SCHALTET NICHT AB (D-256). Die Quelle liegt ausserhalb jedes
Baums, und ein Messaufbau, der die Umgebung des Arbeitsplatzes veraendert, misst eine
Umgebung, die es sonst nicht gibt - die Meldepflicht des Frameworks waere dann nicht mehr
messbar. Er bricht deshalb NICHT ab; sein Befund gehoert in die Zustandsaufnahme.

🔴 GESTELLT IST NICHT GENANNT. In der Mitschrift eines Laufs von Buendel 5 stehen FUENF
Servernamen - `claude_ai_Claude_Docs`, `claude_ai_Strava`, `context7`, `exa`, `firecrawl`.
Gestellt sind **zwei**: Die drei uebrigen stehen im FLIESSTEXT der Skill- und
Agentenauflistung, nicht in ihren Namenslisten. Ein Waechter, der nur nach `mcp__` sucht,
meldete fuenf statt zwei.

  Dieselbe Trennlinie wie D-245 (*Nennung ist nicht Vergabe*) und D-251 - an einer
  dritten Stelle, und hier entscheidet sie ueber den Zaehler selbst.
"""
import io
import json
import os
import re
import sys

import ablage

sys.stdout.reconfigure(encoding="utf-8")

# Die Felder der Mitschrift, die ein GESTELLTES Werkzeug fuehren. Alles andere ist Text,
# der einen Namen nennt.
NAMENSFELDER = ("addedNames", "surfacedNames", "removedNames")
MCP_RE = re.compile(r"mcp__([A-Za-z0-9_-]+?)__([A-Za-z0-9_-]+)")

# Die Zeile des Overlays, die die Freigabe traegt - als Muster, nicht als Wortlaut.
# Die Detailfassung fuehrt sie als TABELLENZEILE, die Laufzeitfassung als Aufzaehlung.
FREIGABE_RE = re.compile(r"Freigegebene MCP-Server", re.I)
KEINE_RE = re.compile(r"^\s*[-–]?\s*(keine|none|nicht angelegt|\u2013)\s*$", re.I)

# 🔴 Die Zellzerlegung wird GETEILT, nicht nachgebaut (D-259). Eine Freigabezeile mit
# einem maskierten Strich im Kommentar zerfiele sonst an der falschen Stelle - derselbe
# Befund, der `zaehlen46.py` am selben Tag getroffen hat.
_VALIDATOR = os.path.join(ablage.WURZEL, ".koolie/core", "tests", "scripts",
                          "validate-framework.py")


def _zellen(zeile):
    """Die Zellen einer Tabellenzeile - mit der Funktion, die der Validator benutzt."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("_vfmcp", _VALIDATOR)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul.tabellenzellen(zeile)


def _manifest(baum):
    """Das Manifest des im Baum installierten Client Packs - gesucht, nicht geraten."""
    # Zwei Ebenen tief wie validate-output.py (K-154, D-407): Seit 0.88.0 liegt der
    # Kern unter `.koolie/core`, und eine Ebene fand ihn in keinem installierten Baum.
    kern = None
    namen = sorted(n for n in os.listdir(baum) if os.path.isdir(os.path.join(baum, n)))
    kandidaten = [os.path.join(baum, n) for n in namen]
    kandidaten += [os.path.join(baum, n, u) for n in namen
                   for u in sorted(os.listdir(os.path.join(baum, n)))]
    for p in kandidaten:
        if os.path.isdir(os.path.join(p, "clients")) and os.path.isdir(os.path.join(p, "framework")):
            kern = p
            break
    if kern is None:
        return None, None
    for pack in sorted(os.listdir(os.path.join(kern, "clients"))):
        m = os.path.join(kern, "clients", pack, "manifest.json")
        if not os.path.isfile(m):
            continue
        man = json.load(io.open(m, encoding="utf-8"))
        rd = man.get("runtime_dir")
        if rd and os.path.isdir(os.path.join(baum, rd)):
            return pack, man
    return None, None


def freigegeben(baum):
    """Welche MCP-Server gibt das Overlay des Baums frei? (Traeger und Aussage)"""
    aus = []
    for rel in (".koolie/project-overlay/OVERLAY.md",
                ".claude/rules/20-project-overlay.md",
                ".devin/rules/20-project-overlay.md"):
        p = os.path.join(baum, rel.replace("/", os.sep))
        if not os.path.isfile(p):
            continue
        for zeile in io.open(p, encoding="utf-8", errors="replace"):
            if not FREIGABE_RE.search(zeile):
                continue
            z = zeile.strip()
            if z.startswith("|"):
                # Tabellenzeile: die Wertspalte ist die erste Zelle NACH der, die den
                # Feldnamen traegt - nicht die zweite, denn manche Tabellen fuehren
                # davor eine Platzhalterspalte.
                zellen = _zellen(z)
                wert = ""
                for i, c in enumerate(zellen):
                    if FREIGABE_RE.search(c):
                        rest = [x for x in zellen[i + 1:] if x and x != "\u2013" and x != "-"]
                        wert = rest[0] if rest else ""
                        break
            else:
                wert = z.split(":", 1)[-1].strip() if ":" in z else z
            aus.append((rel, wert[:120]))
    return aus


def arbeitsplatzquellen(man):
    """Die Konfigurationsquellen AUSSERHALB des Baums - soweit sie lesbar sind.

    🔴 Das Manifest fuehrt nur `<MCP_FILE>`, also die PROJEKTdatei. Die Kontoquelle
    steht in keiner maschinenlesbaren Angabe des Frameworks - dieselbe Luecke wie bei
    der Skillquelle (`K-63`, `K-64`). Sie wird deshalb GENANNT und als ungeprueft
    ausgewiesen, nicht stillschweigend uebergangen.
    """
    heim = os.path.expanduser("~")          # D-231: kein Arbeitsplatzpfad im Quelltext
    gefunden, ungelesen = [], []
    for rel in (".claude.json", os.path.join(".claude", "settings.json")):
        p = os.path.join(heim, rel)
        if not os.path.isfile(p):
            continue
        try:
            d = json.load(io.open(p, encoding="utf-8"))
        except (ValueError, OSError):
            ungelesen.append(rel)
            continue
        for schluessel in ("mcpServers", "claudeAiMcpEverConnected"):
            wert = d.get(schluessel)
            if not wert:
                continue
            namen = sorted(wert) if isinstance(wert, (dict, list)) else [str(wert)]
            gefunden.append((rel, schluessel, namen))
    return gefunden, ungelesen


def _namen_aus(obj, treffer):
    """Sammelt GESTELLTE Werkzeugnamen - nur aus den Namensfeldern (siehe Kopf)."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in NAMENSFELDER and isinstance(v, list):
                for x in v:
                    if isinstance(x, str):
                        treffer.add(x)
            elif k == "entries" and isinstance(v, list):
                for x in v:
                    if isinstance(x, dict) and isinstance(x.get("name"), str):
                        treffer.add(x["name"])
            else:
                _namen_aus(v, treffer)
    elif isinstance(obj, list):
        for v in obj:
            _namen_aus(v, treffer)


def mitschrift(pfad):
    """(gestellte Server, aufgerufene Werkzeuge) eines Laufs."""
    gestellt, aufgerufen = set(), []
    for zeile in io.open(pfad, encoding="utf-8", errors="replace"):
        zeile = zeile.strip()
        if not zeile:
            continue
        try:
            d = json.loads(zeile)
        except ValueError:
            continue
        namen = set()
        _namen_aus(d, namen)
        for n in namen:
            m = MCP_RE.match(n)
            if m:
                gestellt.add(m.group(1))
        # Ein AUFRUF steht als Werkzeugname eines tool_use-Blocks.
        for block in (d.get("message", {}) or {}).get("content", []) or []:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                m = MCP_RE.match(str(block.get("name", "")))
                if m:
                    aufgerufen.append(block["name"])
    return sorted(gestellt), aufgerufen


def vorher(baum):
    print("=== MCP-Waechter, vor der Reihe ===")
    print("Baum:", baum)
    pack, man = _manifest(baum)
    print("Client Pack:", pack or "(nicht bestimmbar)")

    frei = freigegeben(baum)
    if not frei:
        print("🔴 Keine Freigabezeile im Overlay gefunden - der Waechter hat keinen "
              "Sollwert und meldet das, statt zu schweigen.")
    keine = True
    for rel, aussage in frei:
        offen = not KEINE_RE.match(aussage)
        keine = keine and not offen
        print("  %s %-44s %r" % ("⚠️" if offen else "🟢", rel, aussage))

    mcp_datei = (man or {}).get("runtime_placeholders", {}).get("<MCP_FILE>")
    if mcp_datei:
        p = os.path.join(baum, mcp_datei.replace("/", os.sep))
        print("  %s Projektdatei %s: %s"
              % ("⚠️" if os.path.isfile(p) else "🟢", mcp_datei,
                 "vorhanden" if os.path.isfile(p) else "nicht angelegt"))

    gefunden, ungelesen = arbeitsplatzquellen(man)
    print()
    print("--- Quellen ausserhalb des Baums (Konto, nicht Projekt) ---")
    if not gefunden:
        print("  🟢 keine MCP-Eintraege in den gelesenen Konfigurationen")
    for rel, schluessel, namen in gefunden:
        print("  🔴 ~/%s  %s: %s" % (rel.replace(os.sep, "/"), schluessel, ", ".join(namen)))
    for rel in ungelesen:
        print("  ⚠️ ~/%s nicht lesbar - ungeprueft, nicht leer" % rel)

    if keine and gefunden:
        print()
        print("🔴 WIDERSPRUCH: Das Overlay gibt KEINEN MCP-Server frei, der Arbeitsplatz "
              "stellt welche.")
        print("   Der Waechter schaltet sie NICHT ab (D-256) - die Quelle liegt ausserhalb "
              "des Baums, und ein Messaufbau, der die Umgebung aendert, misst eine andere.")
        print("   ➡️ Gehoert in die Zustandsaufnahme und ins Protokoll.")
    return 0


def nachher():
    belege = ablage.belege(anlegen=False)
    print("=== MCP-Waechter, nach der Reihe ===")
    print("Belege:", belege)
    if not os.path.isdir(belege):
        raise SystemExit("ABBRUCH: %r ist kein Verzeichnis" % belege)
    laeufe, mit_gestellt, mit_aufruf, alle_server = 0, 0, 0, set()
    for name in sorted(os.listdir(belege)):
        if not name.endswith("-transkript.jsonl"):
            continue
        laeufe += 1
        gestellt, aufgerufen = mitschrift(os.path.join(belege, name))
        alle_server |= set(gestellt)
        if gestellt:
            mit_gestellt += 1
        if aufgerufen:
            mit_aufruf += 1
            print("  🔴 %s ruft auf: %s" % (name[:-17], ", ".join(sorted(set(aufgerufen)))))
    print()
    print("Laeufe:                       %d" % laeufe)
    print("davon mit GESTELLTEM Server:  %d" % mit_gestellt)
    print("davon mit AUFRUF:             %d" % mit_aufruf)
    print("Server, die gestellt wurden:  %s" % (", ".join(sorted(alle_server)) or "keine"))
    print()
    print("🔴 Gestellt ist nicht genannt und nicht aufgerufen - drei Zahlen, drei "
          "Aussagen. Nur die letzte sagt etwas ueber das VERHALTEN des Laufs.")
    return 0


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "vorher" and len(sys.argv) >= 3:
        return vorher(os.path.abspath(sys.argv[2]))
    if len(sys.argv) >= 2 and sys.argv[1] == "nachher":
        return nachher()
    print(__doc__.split("\n\n")[1])
    raise SystemExit("ABBRUCH: 'vorher <baum>' oder 'nachher'")


if __name__ == "__main__":
    sys.exit(main())

"""Gemeinsame Grundlage der Pruefungen: Bericht (err, warn, hinweis), Lesen,
Tabellenzellen, Dateibestand, Clienterkennung und alles, was mehr als ein Gegenstand
braucht.

Teil des Validators validate-framework.py, seit 1.19.1 nach Gegenstand in Module geteilt
(K-174). Das Register aller Pruefungen steht im Kopfkommentar des Einstiegs, die Grenze
jeder einzelnen in ihrem Kopfkommentar hier."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys


try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

# Name des Kernverzeichnisses. Er steht hier einmal statt an drei Stellen im Skript.
KERN = ".koolie/core"

# Seit 1.19.1 liegt der Code der beiden Pruefskripte in einem Paket neben seinem
# Einstieg (K-174). Wer ihren Quelltext liest - Pruefung 40 das Register und
# die Sondenmenge, Pruefung 104 die Verdrahtung -, liest den Einstieg UND sein Paket, den Einstieg zuerst: Sein
# Kopfkommentar ist das Register.
PAKET_JE_SKRIPT = {"tests/scripts/validate-framework.py": "tests/scripts/pruefungen",
                   "tests/scripts/probe-pruefungen.py": "tests/scripts/sonden"}


def paketquelltext(root: str, rel: str) -> str:
    """Der Quelltext des Pakets zu einem Einstieg, Modul fuer Modul nach Namen."""
    paket = PAKET_JE_SKRIPT.get(rel)
    ordner = os.path.join(root, KERN, *paket.split("/")) if paket else ""
    if not ordner or not os.path.isdir(ordner):
        return ""
    return "".join("\n" + read(os.path.join(ordner, name))
                   for name in sorted(os.listdir(ordner)) if name.endswith(".py"))


# ---------------------------------------------------------------------------
# AUSGABEFORM DER BERECHTIGUNGSDATEI - UND DIE PRUEFUNGEN, DIE AN IHR HAENGEN
# ---------------------------------------------------------------------------
# ANLASS (CR-2026-133, D-346). Bis 1.3.0 hatte jedes Client Pack dieselbe Ausgabeform:
# eine JSON-Datei mit den Koerben deny/ask/allow aus Regeln der Gestalt
# Werkzeug(Muster). Zwoelf Pruefungen lesen sie so. Das dritte Pack hat diese Gestalt
# nicht - es bindet Pfade an Zugriffsarten in einer TOML-Tabelle und Befehle in einer
# eigenen Regelsprache.
#
# EINE PRUEFUNG, DIE EINE FREMDE FORM LIEST, MELDET EINEN FEHLER, DEN ES NICHT GIBT;
# EINE, DIE SIE STILL UEBERSPRINGT, MISST EIN PACK NICHT UND SAGT ES NICHT.
# ➡️ Deshalb steht die Menge hier, sie wird benannt, und Pruefung 87 haelt sie gegen den
#    Abschnitt 5 des betroffenen Packs. Aus einer stillen Luecke wird eine erklaerte.
#
# Ein Pack sagt seine Form im Manifest (permissions_format); der Standard ist "json" -
# eine Form wird gesagt, nicht durch Schweigen geerbt.
#
# SEIT 1.13.0 NENNT JEDER EINTRAG DIE FORMEN, DIE ER ERREICHT (CR-2026-150, D-416).
# Bis dahin war die Menge an genau eine Frage gebunden - "json oder nicht" -, und zwei
# Dinge stimmten nicht: (1) Sie fuehrte als Nummer 76 "Das Pack steht im eigenen
# Korb"; Pruefung 76 ist die Kernlage und laeuft bei jeder Form. Gemeint war 72, und
# die enthielt sich bei openai-codex nicht, weil sie hier stand, sondern weil
# json.loads an der TOML-Datei scheiterte - still. (2) Vier dieser Pruefungen (37, 42,
# 43, 54, 72) hatten gar keinen Schutz; sie lasen eine Datei, die bei TOML nicht
# einlesbar war. Das dritte JSON-Format (das Agentenprofil von kiro) IST einlesbar, und
# dieselben Pruefungen meldeten 64 Fehler, die es nicht gab. Jede Pruefung der Menge
# fragt deshalb jetzt ausdruecklich formatgebunden() - und 72 erreicht das
# Agentenprofil, weil sie dort liest, was sie braucht.
FORMATGEBUNDENE_PRUEFUNGEN = {
    2: ("Berechtigungsdatei als JSON, Kernregeln unter _core_rules_integrity", {"json"}),
    37: ("Die drei Koerbe der installierten Datei gegen die Kernquelle", {"json"}),
    42: ("Der Befehlsschlitz traegt den Befehl, den das Overlay erklaert", {"json"}),
    43: ("Die Berechtigungsdatei traegt den Hook, den das Pack dort fuehrt", {"json"}),
    54: ("Deklarierte Zusatzschluessel stehen auf ihrer Ebene", {"json"}),
    59: ("Gegenstand (c): die ausgeschlossenen Pfade im deny-Korb", {"json"}),
    72: ("Jeder installierte Skill steht in der Berechtigungsdatei",
         {"json", "kiro-agent"}),
    89: ("Gegenstand (c): die Nur-Lese-Pfade im deny-Korb", {"json"}),
}


def formatgebunden(man: dict, nummer: int) -> bool:
    """Wahr, wenn diese Pruefung die Ausgabeform dieses Packs nicht erreicht. Der
    Aufrufer kehrt dann zurueck, ohne zu melden - die Auslassung steht in
    FORMATGEBUNDENE_PRUEFUNGEN und wird von Pruefung 87 eingefordert."""
    if nummer not in FORMATGEBUNDENE_PRUEFUNGEN:
        raise KeyError(
            f"Pruefung {nummer} beruft sich auf die Ausgabeform, steht aber nicht in "
            f"FORMATGEBUNDENE_PRUEFUNGEN. Eine Auslassung, die nirgends steht, ist die "
            f"stille Luecke, die D-346 abgestellt hat")
    return man.get("permissions_format", "json") not in FORMATGEBUNDENE_PRUEFUNGEN[nummer][1]

ERRORS: list[str] = []
WARNINGS: list[str] = []
# Seit 1.8.0 (D-367): Zeilen, die eine reduzierte Installation erklaeren - was sie nicht
# mitliefert und welche Pruefung deshalb nichts zu pruefen hat. Sie zaehlen weder als
# Fehler noch als Warnung; eine reduzierte Installation ist kein Mangel. Stumm bleiben
# duerfen sie nicht: Eine Luecke, die nur besteht, ist ein blinder Fleck (D-346).
HINWEISE: list[str] = []

# ".cmd" und ".command" seit 1.7.0: die Starter des Installers (D-365). Ohne sie lasen
# weder die Neutralitaets- noch die Zeilenendepruefungen diese Traeger.
TEXT_EXT = {".md", ".json", ".yaml", ".yml", ".txt", ".py", ".template", ".example",
            ".cmd", ".command"}
SKIP_DIRS = {".git", "build", "node_modules", "__pycache__", "target", "dist", ".venv"}
SKILL_STATUS = {"entwurf", "pilot", "aktiv", "veraltet", "zurückgezogen"}
PLACEHOLDER_RE = re.compile(r"<([A-Z][A-Z0-9_]{2,})>")
TBD_RE = re.compile(r"<TBD[:>]")

# --- Zellen einer Markdown-Tabellenzeile (CR-2026-060, D-75) --------------------
# GFM trennt Zellen am Strich; ein Strich INNERHALB einer Zelle wird maskiert (\\|)
# und bleibt Inhalt. Eine Zerlegung, die das nicht kennt, beanstandet einen korrekten
# Text - gemessen an Pruefung 30, die eine Grenzfallzeile mit maskiertem Strich als
# neunspaltig meldete, obwohl sie siebenspaltig rendert. D-69 des Decision Logs
# traegt genau diese Schreibweise seit 0.36.0.
#
# Die Zerlegung lag bis 0.37.0 VIERMAL eigenhaendig im Validator. Sie liegt jetzt
# einmal: vier Gelegenheiten fuer denselben Fehler sind eine.
ZELLTRENNER_RE = re.compile(r"(?<!\\)\|")


def tabellenzellen(zeile: str) -> list:
    """Die Zellen einer Tabellenzeile, maskierte Striche als Inhalt.

    Erwartet eine Zeile, die mit '|' beginnt; die aeusseren Striche sind Rahmen und
    zaehlen nicht als Zellen. Fuer eine Zeile ohne Rahmen liefert sie die Felder
    zwischen den Trennern.
    """
    z = zeile.strip()
    teile = ZELLTRENNER_RE.split(z)
    if z.startswith("|"):
        teile = teile[1:]
    if z.endswith("|") and not z.endswith("\\|") and teile:
        teile = teile[:-1]
    return [t.strip() for t in teile]


def err(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNINGS.append(msg)


def hinweis(msg: str) -> None:
    if msg not in HINWEISE:
        HINWEISE.append(msg)


def read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _gitignore_namen(root: str) -> set:
    """Die DATEINAMEN, die die .gitignore der Wurzel als nicht zu teilend fuehrt.

    🔴 WARUM DER VALIDATOR SIE UEBERSPRINGT (D-215, CR-2026-106): Was nicht
    eingecheckt wird, ist kein Bestandteil des Repositoriums - und eine Pruefung,
    die es trotzdem meldet, prueft am Gegenstand vorbei. Gemessen am 2026-09-20:
    Die lokale Beilage der Uebergabe traegt Servername und Konto, steht in der
    .gitignore, und der Validator meldete gegen sie zwei Fehler. Sie existiert
    gerade deshalb, damit diese Angaben NICHT im Repositorium stehen.

    🔴 BEWUSST NUR EINFACHE DATEINAMEN, keine Muster und keine Pfade. Ein
    `*`-Muster oder ein Verzeichnis liesse sich hier eintragen, um eine echte
    Pruefung stillzulegen - `.koolie/core/**` wuerde den halben Kern
    ausblenden, und niemand saehe es. Ein Dateiname trifft eine Datei, und die
    Liste ist kurz genug zum Lesen. Zeilen mit `/`, `*`, `?`, `[` oder `!`
    werden ignoriert.
    """
    pfad = os.path.join(root, ".gitignore")
    namen = set()
    if not os.path.isfile(pfad):
        return namen
    # `read` ist die Leseroutine dieses Moduls; ein eigener `io`-Import waere ein
    # zweiter Weg zum selben Zweck.
    try:
        roh = read(pfad)
    except OSError:
        return namen
    for zeile in roh.splitlines():
        z = zeile.strip()
        if not z or z.startswith("#"):
            continue
        if any(c in z for c in "/*?[!"):
            continue
        namen.add(z)
    return namen


def _walk_text_files(start: str, ignoriert: set = frozenset()):
    for dirpath, dirnames, filenames in os.walk(start):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn in ignoriert:
                continue
            ext = os.path.splitext(fn)[1]
            if ext in TEXT_EXT or fn in ("VERSION", ".gitignore"):
                yield os.path.join(dirpath, fn)


def iter_text_files(root: str):
    ignoriert = _gitignore_namen(root)
    yield from _walk_text_files(root, ignoriert)
    # 'build' steht in SKIP_DIRS, weil dort die Erzeugnisse eines Projekts liegen. Die
    # handgeschriebenen Quellen des Hauptdokuments liegen aber darunter und gehoeren
    # geprueft - gerade weil aus ihnen ein Lieferbestandteil entsteht. Vier Backticks
    # brechen genau hier die Assemblierung, und ein Secret erschiene im ausgelieferten
    # Dokument.
    #
    # 🔴 BIS 0.89.0 STAND HIER NUR build/doc - UND DIE DREI TRAEGER DANEBEN ERREICHTE
    # KEINE EINZIGE PRUEFUNG (D-313, CR-2026-125): assemble.py, build-docx.py und
    # build/README.md. Begruendet war das mit EINER Frage - die Werkzeuge fuehren eigene
    # Marker in spitzen Klammern, die keine Framework-Platzhalter sind. Gewirkt hat es auf
    # ZWOELF Pruefungen, die ueber diesen Iterator laufen. Gemessen beim Oeffnen am
    # 2026-09-23: zwei Fehler und zwei Warnungen. Die zwei Warnungen SIND die Begruendung
    # und haben jetzt eine eigene, benannte Ausnahme bei der einen Frage, fuer die sie
    # gilt (OHNE_PLATZHALTERREGISTER). Die zwei Fehler sind Pruefung 14 am Erzeuger der
    # Word-Fassung: Er haette den ueberholten Dokumenttitel samt CLIENTNAMEN in die
    # Dokumenteigenschaften der Lieferung gestempelt.
    # ➡️ Dieselbe Auflösung wie bei D-311: eine benannte Ausnahme ueber benannte Traeger
    #    statt einer stummen ueber ein Verzeichnis. EINE AUSNAHME GILT SO WEIT WIE IHRE
    #    BEGRUENDUNG UND NICHT SO WEIT WIE IHR MECHANISMUS.
    #
    # `out/` bleibt aussen vor und das ist kein Versehen: Es ist das ERZEUGNIS, steht in
    # der .gitignore und ist in einer frischen Auscheckung nicht da. Eine Pruefung dagegen
    # waere im Framework gruen und in jeder Installation rot - der Konstruktionsfehler,
    # den Pruefung 75 mit 0.88.0 zweimal bezahlt hat.
    bau = os.path.join(root, KERN, "build")
    if os.path.isdir(bau):
        for pfad in _walk_text_files(bau, ignoriert):
            if os.path.relpath(pfad, bau).replace(os.sep, "/").startswith("out/"):
                continue
            yield pfad


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text
    fm_text, body = parts[1], parts[2]
    if yaml is None:
        return {"_raw": fm_text}, body
    try:
        data = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as exc:  # type: ignore[attr-defined]
        return {"_error": str(exc)}, body
    return data, body


# --- Clienterkennung (Client Packs) -------------------------------------------
# Der Validator lief frueher fest gegen .devin/. Seit es mehrere Client Packs gibt,
# wird die Laufzeitschicht erkannt: Jedes Pack beschreibt seine Pfade in
# clients/<name>/manifest.json; geprueft wird das Pack, dessen runtime_dir im
# Zielverzeichnis tatsaechlich liegt.
MANIFEST_FALLBACK = {
    "client": "unbekannt", "runtime_dir": ".devin", "root_instruction_file": "AGENTS.md",
    "permissions_file": ".devin/config.json", "skills_dir": ".devin/skills",
    "agents_dir": ".devin/agents", "pack_runtime_dir": ".devin/rules",
    "has_rule_triggers": True,
}


def detect_client(root: str) -> dict:
    """Manifest des installierten Client Packs. Fallback, wenn keines zutrifft."""
    base = os.path.join(root, KERN, "clients")
    treffer = []
    if os.path.isdir(base):
        for name in sorted(os.listdir(base)):
            mp = os.path.join(base, name, "manifest.json")
            if not os.path.exists(mp):
                continue
            try:
                man = json.loads(read(mp))
            except json.JSONDecodeError as exc:
                err(f"clients/{name}/manifest.json ist kein gültiges JSON: {exc}")
                continue
            if os.path.isdir(os.path.join(root, *man.get("runtime_dir", "").split("/"))):
                # <CORE_DIR> ist die LAGE des Kerns unter der Projektwurzel, nicht der
                # Name eines Verzeichnisses. Bis 0.87.0 stand hier os.path.basename()
                # ueber drei dirname-Aufrufe; seit der Kern zwei Segmente tief liegt,
                # lieferte das "core" statt ".koolie/core" - und der Validator haette
                # denselben falschen Wert gebunden wie install.py und deshalb nichts
                # gemeldet (D-299).
                man.setdefault("runtime_placeholders", {})["<CORE_DIR>"] = KERN
                treffer.append(man)
    if len(treffer) > 1:
        namen = ", ".join(m["client"] for m in treffer)
        err(f"Mehrere Laufzeitschichten gleichzeitig vorhanden ({namen}). "
            f"Ein Projekt nutzt genau ein Client Pack.")
    return treffer[0] if treffer else MANIFEST_FALLBACK


def regel_endung(man: dict) -> str:
    """Die Endung der Regeldateien dieses Packs (cursor: .mdc, CR-2026-155) - dieselbe
    Auskunft wie clientmap.regel_endung(), hier ohne Import, weil die Pruefungen auch
    ohne das Abbildungsmodul laufen muessen."""
    return man.get("rule_file_ext", ".md")


def regeldatei(man: dict, name: str) -> str:
    """'20-project-overlay.md' in der Schreibweise der Regelablage dieses Packs."""
    endung = regel_endung(man)
    return name[:-3] + endung if endung != ".md" and name.endswith(".md") else name


# ---------------------------------------------------------------------------
# 37: Die drei Koerbe der Berechtigungsdatei gegen die Kernquelle
# ---------------------------------------------------------------------------
#
# Anlass ist eine Messung vom 2026-09-13 (CR-2026-061, D-77): Die erzeugte Datei traegt
# 65 Regeln, geprueft waren dreizehn. Ein Projekt konnte 41 deny-Regeln loeschen, den
# ask-Korb leeren und eine allow-Zeile ergaenzen, ohne dass ein Lauf davon Notiz nahm -
# und install.py --update fasst die Datei nie an, --check nennt sie nicht einmal.
#
# Die Pruefung ist das Verschaerfungsprinzip, mechanisch angewandt
# (PRIORITY_HIERARCHY.md Regel 2.1), in zwei Saetzen:
#   Fehlt eine erzeugte Regel, ist es ein Fehler - in jedem Korb.
#   Steht eine Regel zu viel, entscheidet der Korb: in deny zulaessig (Verschaerfung),
#   in ask und allow ein Fehler (Ausweitung) - abzueglich der Platzhalterschlitze
#   UND der Skillfreigaben aktivierter Packs (D-243, siehe skillfreigaben()).
PROJEKTPLATZHALTER = re.compile(r"<[A-Z][A-Z0-9_]*>")


def korb_zerlegung(ist: list, soll_korb: list) -> tuple:
    """Ein Korb in Pflicht, Schlitze, gefuellte Schlitze und Ueberschuss.

    Die Zerlegung lag bis 0.43.0 in check_berechtigungskoerbe und wurde fuer Pruefung 42
    ein zweites Mal gebraucht. Sie liegt jetzt einmal: zwei Gelegenheiten fuer denselben
    Fehler sind eine - dieselbe Begruendung wie bei tabellenzellen() mit 0.37.0.

    pflicht    Regeln ohne Projektplatzhalter; sie muessen dastehen.
    schlitze   Regeln mit Projektplatzhalter; sie gehoeren dem Projekt.
    ungefuellt Schlitze, die woertlich in der Datei stehen. Sie sind noch offen.
    zusatz     Regeln der Datei, die weder Pflicht noch ein offener Schlitz sind - ein
               gefuellter Schlitz steht hier ebenso wie eine hinzugefuegte Freigabe.
               WELCHE von beiden, sagt diese Funktion nicht und kann es nicht sagen;
               das ist der Gegenstand von Pruefung 42.
    """
    pflicht = [r for r in soll_korb if not PROJEKTPLATZHALTER.search(r)]
    schlitze = [r for r in soll_korb if PROJEKTPLATZHALTER.search(r)]
    ungefuellt = [s for s in schlitze if s in ist]
    zusatz = [r for r in ist if r not in pflicht and r not in schlitze]
    return pflicht, schlitze, ungefuellt, zusatz


def soll_korbregeln(root: str, man: dict) -> dict | None:
    """Die drei Koerbe in der Schreibweise dieses Clients, aus der Kernquelle.

    Dieselbe Quelle wie soll_kernregeln, nur ohne die Einschraenkung auf 'core': true.
    Fehlt das Abbildungsmodul, unterbleibt die Pruefung - check_config hat dafuer bereits
    gewarnt, und eine zweite Warnung ueber dieselbe Tatsache waere Laerm.
    """
    kern = os.path.join(root, KERN)
    if not os.path.isdir(kern):
        return None
    if kern not in sys.path:
        sys.path.insert(0, kern)
    try:
        import clientmap
    except ImportError:
        return None
    # Sonde auf den verlorenen Anker (seit 0.32.0): Diese Pruefung findet ihren
    # Gegenstand ueber einen Funktionsnamen. Geht er bei einem Umbau verloren, bestuende
    # sie leise - deshalb meldet sie sein Fehlen selbst.
    if not hasattr(clientmap, "basket_rules"):
        err(f"{KERN}/clientmap.py: Funktion 'basket_rules(' fehlt – Prüfung 37 hat ihren "
            f"Gegenstand verloren und würde sonst leise bestehen")
        return None
    try:
        quelle = json.loads(clientmap.load_source(kern, "permissions.json"))
        return {korb: clientmap.basket_rules(quelle, man, korb)
                for korb in ("deny", "ask", "allow")}
    except (OSError, ValueError) as exc:
        err(f"Kernquelle der Berechtigungen nicht auswertbar: {exc}")
        return None


def skill_dirs(root: str, man: dict) -> list[tuple[str, str]]:
    """Alle Skill-Ablagen: die aktivierte Laufzeitschicht und die Quellablagen der Packs.

    Pack-Skills liegen unter framework/{role,tech}-packs/<pack>/skills/ und werden erst zur
    Aktivierung nach .devin/skills/ kopiert. Ohne diese Ablagen wuerde ein fehlerhafter
    Pack-Skill erst im uebernehmenden Projekt auffallen - also nach der Auslieferung.
    """
    out: list[tuple[str, str]] = []
    runtime = os.path.join(root, *man["skills_dir"].split("/"))
    if os.path.isdir(runtime):
        out.append((runtime, man["skills_dir"]))
    # Gemeinsame Quelle der Framework-Skills (seit 0.5.0). Sie wird streng geprueft;
    # die installierte Fassung ist daraus erzeugt.
    quelle = os.path.join(root, ".koolie/core", "framework", "skills")
    if os.path.isdir(quelle):
        out.append((quelle, ".koolie/core/framework/skills"))
    for kind in ("role-packs", "tech-packs"):
        base = os.path.join(root, ".koolie/core", "framework", kind)
        if not os.path.isdir(base):
            continue
        for pack in sorted(os.listdir(base)):
            src = os.path.join(base, pack, "skills")
            if os.path.isdir(src):
                out.append((src, f".koolie/core/framework/{kind}/{pack}/skills"))
    return out


# --- Ausnahmen der Werkzeugneutralitaet (D-128, D-129) ----------------------------
#
# EINE Menge fuer BEIDE Pruefungen, die den Kern auf Clientbindung halten: Pruefung 14
# (der Produktname) und Pruefung 48 (der Pfad). Bis 0.57.0 fuehrten sie zwei Mengen -
# und die waren schon auseinandergelaufen: docs/ROADMAP.md stand nur in einer von
# beiden. Zwei Listen fuer denselben Gegenstand driften; eine tut es nicht.
#
# Die Gattungen und ihre Begruendung stehen in docs/RUNTIME_GLOSSARY.md, nicht hier -
# eine Ausnahme, die nur im Quelltext steht, ist keine Regel, sondern eine
# Voreinstellung.
NEUTRAL_CHRONIK = (
    KERN + "/CHANGELOG.md",
    KERN + "/governance/change-requests/",
    KERN + "/governance/DECISION_LOG.md",
    KERN + "/tests/protocols/",
    KERN + "/docs/ROADMAP.md",
)
# Jeder Aenderungsverlauf ist ein historisches Dokument, nicht nur der des Frameworks.
NEUTRAL_CHRONIK_BASENAMES = ("CHANGELOG.md",)
# DIE BEFRISTETE AUSNAHME FUER build/ IST MIT 0.89.0 GEFALLEN (AP11, D-311).
#
# Sie galt fuer das GANZE Verzeichnis, mit der Begruendung, es halte die Quellen des
# Hauptdokuments, das mit AP11 neu gesetzt werde. Gemessen beim Neusetzen: Von 36
# Fundstellen lagen 27 in den beiden ANHANG- und ABSCHLUSSTRAEGERN - der Quellenliste
# JE CLIENT PACK und dem konsolidierten Verifikationsbedarf EINES Packs. Das ist
# dieselbe Gattung, die NEUTRAL_ABBILDUNG seit 0.57.1 dauerhaft ausnimmt, und
# CR-2026-025 E3 hatte sie 2026-09-11 auch schon ausdruecklich ausgewiesen
# ("die Anhaenge beschreiben teils Pruefpunkte gegen die Dokumentation eines konkreten
# Clients"). EINE FRIST UEBER EINEN GEGENSTAND, DER DIE AUSNAHME DAUERHAFT BRAUCHT,
# KANN NICHT ABLAUFEN - sie sieht nur zwanzig Releases lang so aus, als lehne sie an.
#
# Die uebrigen neun Fundstellen lagen in den Kapiteln und sind mit 0.89.0 aufgeloest.
# Was bleibt, ist eine Dauerausnahme ueber DREI benannte Traeger, nicht ueber ein
# Verzeichnis:
#   29-grenzen.md   Zeitdokument des Stands vom 2026-09-01, ausdruecklich nicht
#                   fortgeschrieben - Chronik wie CHANGELOG.md und DECISION_LOG.md
#   31-anhaenge.md  Quellenliste JE CLIENT PACK und Verifikationsbedarf EINES Packs
#   32-abschluss.md Chronik der Releases und die Aussagen des Auftrags UEBER die
#                   Produktnennung selbst ("der Hersteller-/Produktbezug ist fuer
#                   Phase 3 erforderlich")
NEUTRAL_DOKUMENT = (
    KERN + "/build/doc/29-grenzen.md",
    KERN + "/build/doc/31-anhaenge.md",
    KERN + "/build/doc/32-abschluss.md",
)


# Pruefung 15: Der Interpreter der Hook-Aufrufe startet auf dieser Maschine wirklich
# Python. Geprueft wird die Wirkung, nicht die Anwesenheit des Namens (AP2-CC-13).
HOOK_SONDE = "KOOLIE-INTERPRETER-OK"


def _client_packs(root: str) -> list[tuple[str, str, dict]]:
    """(Kennung, Verzeichnis, Manifest) je Client Pack; OHNE die Vorlage `_template`.

    🔴 D-336: Bis 1.2.0 stand hier "_template ohne Manifest" - eine Annahme, keine
    Ausnahme. `_template` traegt eine CLIENT_PACK.md und stand damit in dieser Menge;
    was es vor allen Pruefungen schuetzte, war allein sein fehlendes `manifest.json`.
    Gemessen am 2026-09-23 mit einem Probemanifest: drei Packs mit Manifest, Validator
    0 Fehler. Und `clients/README.md` Schritt 5 verlangt genau dieses Manifest fuer
    jedes neue Pack.
    ➡️ Eine Vorlage, die nur durch ihre Unvollstaendigkeit ungeprueft bleibt, ist nicht
    ausgenommen. Die Ausnahme steht seit D-336 HIER, wo die Packmenge entsteht - und
    Pruefung 84 haelt fest, was sie voraussetzt.
    """
    raus: list[tuple[str, str, dict]] = []
    cdir = os.path.join(root, KERN, "clients")
    if not os.path.isdir(cdir):
        return raus
    for name in sorted(os.listdir(cdir)):
        if name == "_template":
            continue  # die Vorlage ist kein Pack (D-336, Pruefung 84)
        pdir = os.path.join(cdir, name)
        if not os.path.isdir(pdir):
            continue
        if not os.path.isfile(os.path.join(pdir, "CLIENT_PACK.md")):
            continue
        mf = os.path.join(pdir, "manifest.json")
        man: dict = {}
        if os.path.isfile(mf):
            try:
                man = json.loads(read(mf))
            except Exception:
                man = {}
        raus.append((name, pdir, man))
    return raus


def _hook_interpreter() -> str | None:
    """Der erste Interpretername, der auf dieser Maschine wirklich Python startet."""
    for kandidat in ("python3", "python", "py"):
        try:
            lauf = subprocess.run([kandidat, "-c", "import sys; sys.stdout.write('%s')" % HOOK_SONDE],
                                  capture_output=True, text=True, timeout=15)
            if lauf.returncode == 0 and HOOK_SONDE in (lauf.stdout or ""):
                return kandidat
        except (OSError, subprocess.SubprocessError):
            continue
    return None


def _hook_lauf(interpreter: str, skript: str, eingabe: str) -> int:
    """Ruft den Schutz-Hook mit --fail-closed auf und liefert den Exit-Code."""
    try:
        lauf = subprocess.run([interpreter, skript, "--fail-closed"], input=eingabe,
                              capture_output=True, text=True, timeout=20,
                              env={k: v for k, v in os.environ.items()
                                   if k != "FW_HOOK_FAIL_CLOSED"})
    except (OSError, subprocess.SubprocessError):
        return -1
    return lauf.returncode


# Pruefung 38: Eine Quelle, ein Vokabular - und die Sperrliste ist nie enger als die
# Vorabfreigabe (CR-2026-062, D-78 bis D-80).
#
# ANLASS. Ein Manifest fuehrt VIER Werkzeugabbildungen, nicht zwei: skill_frontmatter.
# tool_names, agent_frontmatter.tool_names, hook_tools und permission_tools - dazu
# agent_start_tools daneben. Drei Vokabulare stossen darin aufeinander: das der Quelle
# (read, grep, glob, edit, exec), das des Hooks (read, search, exec, write) und das der
# Berechtigungsdatei (read, search, write, exec, fetch, mcp).
#
# Gemessen am 2026-09-13 (tests/protocols/2026-09-13-gegenpruefung-werkzeugabbildung.md):
# DREI der vier Abbildungen brechen ab, wenn ihnen ein Verb fehlt - die vierte reichte
# es woertlich durch, und sie kommt zweimal vor. Eine geleerte tool_names-Abbildung
# lieferte 'tools: read, grep, glob' im Agentenprofil fw-reviewer, also drei Namen, die
# dieser Client nicht kennt (M16); ein 'permissions.deny: glob' erzeugte lautlos keine
# Sperre, und der Validator meldete 0 Fehler (M6).
#
# VIER GEGENSTAENDE:
#   1. Der verlorene Anker. Fehlen clientmap.FRONTMATTER_VERBEN oder VERB_BRUECKE,
#      meldet diese Pruefung das selbst - sonst bestuende sie leise (D-23).
#   2. Die Deklaration je Pack. Jedes Verb des Vokabulars ist in tool_names abgebildet
#      ODER in tool_names_unmapped erklaert, samt nicht leerer _tool_names_unmapped_note;
#      beides zugleich ist ein Widerspruch, ein Schluessel ausserhalb des Vokabulars ein
#      Schreibfehler. Bauform wie Pruefung 26 (hook_tools_absent, D-47) und Pruefung 34.
#   3. Die RICHTUNG zwischen Vorabfreigabe und Sperre. Fuer jedes Verbpaar der Bruecke
#      muss hook_tools mindestens so weit sein wie tool_names. Heute ist es das bei allen
#      fuenf; die Abweichung, die es gibt, geht in die zulaessige Richtung
#      (tool_names.edit fuehrt Edit und Write, hook_tools.write zusaetzlich NotebookEdit).
#      Umgekehrt waere sie eine Luecke: Ein Skill, der 'edit' vorab freigibt und 'edit'
#      sperrt, bekaeme ein Werkzeug freigegeben, das die Sperre nicht erfasst.
#   4. Die Quellen. Kein ausgeliefertes SKILL.md und kein Agentenprofil nennt in
#      allowed-tools oder permissions.deny ein Verb ausserhalb des Vokabulars.
#
# WAS SIE HEUTE FAENGT: bei den beiden Packs nichts - sie sind in Ordnung, seit
# devin-desktop seine fuenf nicht abgebildeten Verben deklariert. Gegenstand 3 ist eine
# VERANKERUNG wie Pruefung 35 und 36; Gegenstand 2 faengt gegen 0.39.0 zehn Fundstellen,
# Gegenstand 4 keine. Das steht so im Wirkungsnachweis und ist kein Abzaehlen von
# Befunden, sondern eines von Deklarationen.
#
# WAS SIE NICHT LEISTET: Sie belegt nicht, dass die Werkzeugnamen eines Packs RICHTIG
# sind - das kann nur eine Erhebung, und fuer devin-desktop steht sie aus. Sie belegt,
# dass jedes Verb des Vokabulars eine Antwort hat und dass die beiden Listen nicht in
# die gefaehrliche Richtung auseinanderlaufen.
FRONTMATTER_BLOECKE = ("skill_frontmatter", "agent_frontmatter")


# ---------------------------------------------------------------------------
# Pruefung 40: Die Register des Pruefapparats werden nachgezaehlt
# ---------------------------------------------------------------------------
#
# ANLASS. Gemessen am 2026-09-14 (tests/protocols/2026-09-14-gegenpruefung-pruefregister.md,
# CR-2026-064): FUENF Aussagen ueber den eigenen Pruefstand, keine davon richtig. Das
# Register im Kopfkommentar dieser Datei fuehrte die Pruefungen 1 bis 38, waehrend 39
# lief; der Satz zum Wirkungsnachweis nannte "18 bis 30"; der Kopfsatz des Sondenskripts
# war eine Release-Chronik, die bei 0.29.0 endete; FW-KO-01 nannte "6, 18 bis 31" und
# FW-KO-05 zwoelf Grenzfaelle, wo es zwanzig sind. KEINE der fuenf war falsch
# geschrieben - alle fuenf waren bei ihrer Einfuehrung richtig und sind stehen geblieben,
# waehrend ihr Gegenstand wuchs. In zehn von zwoelf Releases hat sich mindestens eine der
# drei Zahlen bewegt; deshalb ist die Behebung eine Pruefung und keine Textaenderung.
#
# VIER GEGENSTAENDE:
#   1. Der verlorene Anker. Fuenf Ankertexte in vier Dateien. Geht einer verloren,
#      bestuende diese Pruefung leise - sie meldet sein Fehlen deshalb selbst (D-23).
#   2. Das Register ist lueckenlos von 1 bis zu seiner hoechsten Nummer, und diese
#      hoechste Nummer ist die hoechste, die in den beiden Pruefskripten ueberhaupt
#      genannt wird. In beide Richtungen: eine Pruefung ohne Eintrag ist ein Fehler, ein
#      Eintrag ohne Nennung im Code auch.
#   3. Die Sondenmenge steht an DREI Stellen in derselben, ausgerechneten Schreibweise -
#      im Satz unter dem Register, im Kopfsatz von probe-pruefungen.py und in der
#      Pruefmittelspalte von FW-KO-01. Der Vergleich ist woertlich, und die Fehlermeldung
#      nennt die richtige Zeichenkette (D-86).
#   4. Die Grenzfallanzahl in FW-KO-05 ist die gezaehlte. Pruefung 30 rechnet sie
#      INNERHALB von EDGE_CASES.md nach; ausserhalb nennt sie nur dieses Testblatt, und
#      dort als Arbeitsanweisung: Wer FW-KO-05 heute faehrt, prueft zwoelf von zwanzig
#      Grenzfaellen und meldet ihn bestanden.
#
# WARUM NICHT DIE KOPFKOMMENTARE ALS ANKER (CR-2026-064 E2). Gemessen tragen sie drei
# Formen - "# Pruefung N:", "# N:" und "# Pruefungen N bis M" -, und eine vierte sieht
# aus wie ein Kopf und ist keiner: "# Pruefung 37 und dieselbe Ehrlichkeit ..." im Block
# von Pruefung 39. Der erste Entwurf dieser Pruefung ist genau daran gefallen und hat
# Pruefung 37 gefunden, wo kein Kopf stand.
#
# WARUM NUR TEST_CATALOG.md UND NICHT DAS GANZE REPOSITORIUM (D-86). docs/ROADMAP.md,
# CR-2026-052 und der Wirkungsnachweis zu 0.32.0 nennen ebenfalls zwoelf Grenzfaelle -
# und sind RICHTIG, weil sie den Stand von 0.32.0 beschreiben. Eine Nennung in der
# Vorgeschichte ist kein Register, und wer sie mitzieht, macht aus einer richtigen Zeile
# eine falsche.
#
# GRENZE. Sie zaehlt NENNUNGEN, nicht Pruefungen: Wer eine Pruefung baut und ihre Nummer
# nirgends schreibt, wird nicht gefangen - dieselbe Ehrlichkeit wie Gegenstand 2 von
# Pruefung 38, der Deklarationen zaehlt und nicht Richtigkeit. Und sie belegt die
# VOLLSTAENDIGKEIT des Registers, nicht die Richtigkeit seiner Eintraege: Ein Eintrag,
# der etwas anderes beschreibt als seine Pruefung tut, laeuft durch.
REGISTER_ANKER = "Prüft (statisch, ohne laufenden KI-Client):"
REGISTER_ENDE = "Der Wirksamkeitsnachweis nach D-23"


def _ueb_katalogdateien(root: str) -> list:
    """Der Testkatalog und die dezentralen Testblaetter je Skill (Verfahren Nr. 6)."""
    treffer = [os.path.join(KERN, "tests", "TEST_CATALOG.md")]
    basis = os.path.join(root, KERN, "framework")
    for dirpath, dirnames, filenames in os.walk(basis):
        dirnames[:] = sorted(d for d in dirnames if d != "__pycache__")
        if "TESTS.md" in filenames:
            treffer.append(os.path.relpath(os.path.join(dirpath, "TESTS.md"), root))
    return sorted(treffer)


def _verfolgte_dateien(root: str) -> list | None:
    """Vom Versionsverwalter verfolgte Pfade unter <CORE_DIR>/ - oder None.

    None heisst: nicht messbar. Kein git im Pfad, keine Versionierung, oder der Aufruf
    ist gescheitert. Der Unterschied zu einer leeren Liste ist der ganze Punkt - eine
    leere Liste ist ein Messergebnis, None ist keins.
    """
    try:
        lauf = subprocess.run(["git", "-C", root, "ls-files", "-z", "--", KERN],
                              capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if lauf.returncode != 0:
        return None
    return _git_pfade(lauf.stdout)


def _git_pfade(ausgabe: str | None) -> list:
    """Die Pfade einer `git ... -z`-Ausgabe (CR-2026-135, D-352).

    OHNE `-z` IST DIE AUSGABE KEIN PFAD MEHR, SOBALD ER EIN NICHT-ASCII-ZEICHEN TRAEGT.
    git quotet ihn dann (`core.quotePath`, Vorgabe an) - aus einem U-Umlaut wird
    `"docs/\\303\\234bersicht.md"`, samt Anfuehrungszeichen. Die Pruefungen 75 und 81
    fanden unter diesem Namen keine Datei und gingen LEISE weiter; 78 zaehlte ihn als
    Datei, aber nicht als Markdown - das schliessende Anfuehrungszeichen steht hinter
    der Endung. Gemessen: Ein Traeger mit U-Umlaut im Namen und gemischten
    Zeilenenden war fuer Pruefung 81 unsichtbar (Sonde 81e). Dieselbe Ursache wie in
    `install.py` - eine Pfadliste als Textzeilen statt NUL-getrennt.
    """
    return [z for z in (ausgabe or "").split("\0") if z]


def _tabellenspalte(kopf: str, ueberschrift: str) -> int:
    """Index der Spalte mit dieser Ueberschrift - ueber die STELLUNG, nicht die Nummer.

    Eine neue Spalte im Testkatalog verschiebt sonst jede Pruefung, die eine Nummer
    verdrahtet hat. -1 heisst: diese Tabelle fuehrt die Spalte nicht.
    """
    zellen = [z.strip() for z in kopf.strip().strip("|").split("|")]
    for i, z in enumerate(zellen):
        if z == ueberschrift:
            return i
    return -1


# --- Pruefung 67: ENTFALLEN mit 1.4.1 (D-350) --------------------------------------
#
# Sie hielt die Titelzeile der Uebergabe gegen VERSION (D-216). Seit 1.4.1 ist die
# Uebergabe ein lokales Arbeitsdokument und nicht mehr versioniert; ihr Gegenstand
# fehlt in jeder frischen Auscheckung. Die Nummer bleibt im Register, damit es
# lueckenlos bleibt und keine andere Pruefung sie erbt.
#
# DAS KENNZEICHEN DES QUELLREPOSITORIUMS (D-351). Bis 1.4.0 unterschieden die
# Pruefungen 75, 78, 79 und 81 an UEBERGABE.md, ob sie im Framework-Repositorium oder
# in einem uebernehmenden Projekt laufen. Mit der Uebergabe ist dieser Anker aus dem
# Versionierten verschwunden - und die Pruefungen 75 und 81 lesen `git ls-files`:
# Sie haetten das Quellrepositorium LEISE fuer ein Projekt gehalten und nur noch das
# Ausgelieferte geprueft, auch auf dem Arbeitsplatz, der die Datei noch fuehrt.
# ➡️ Ein Anker, der nur an einem Arbeitsplatz liegt, ist keiner.
# Das Kennzeichen ist deshalb eine eigene, versionierte Datei NEBEN dem Kern: Das
# Heben kopiert nur den Kern, und install.py legt sie nicht an.
# Die Einstiegsdokumente des Quellrepositoriums in seiner Wurzel (D-437): die README,
# der Quickstart und ihre englischen Fassungen. Klasse A wie die README, und aus
# demselben Grund nur im Quellrepositorium - in einem Projekt gehoert die Wurzel dem
# Projekt (D-299). Pruefung 92 ist fuer die englischen Fassungen wirkungslos, aber
# harmlos: Ihre Stammliste ist deutsch und trifft englischen Text nicht.
DOK_WURZEL = ("README.md", "README.en.md", "QUICKSTART.md", "QUICKSTART.en.md")


QUELLREPO_KENNZEICHEN = ".koolie/QUELLREPOSITORIUM.md"


def ist_quellrepositorium(root: str) -> bool:
    """Traegt dieser Baum das Kennzeichen des Framework-Repositoriums (D-351)?"""
    return os.path.isfile(os.path.join(root, *QUELLREPO_KENNZEICHEN.split("/")))


# --- Pruefung 90: Der Lieferumfang einer Installation (D-367, CR-2026-141) ----------
#
# ANLASS. Seit 1.8.0 kann ein Projekt den Kern ohne die Nachweisschicht bekommen
# (install.py --target --lieferumfang nutzung). Die Nachweisschicht steht an EINER
# Stelle - clientmap.NACHWEIS_ABLAGEN -, und dieser Validator liest sie dort, statt sie
# ein zweites Mal aufzuzaehlen: zwei Listen, die einander decken sollen, sind die
# Bauform von 0.57.0.
#
# WAS SICH IN EINER REDUZIERTEN INSTALLATION AENDERT, und nur das (gemessen am
# 2026-09-25 an allen drei Packs): 70 Verweise ausgelieferter Traeger zeigen in
# tests/protocols/ - Herkunftsangaben, deren Aussage ohne die Datei steht -, und drei
# Pruefungen verlieren ihren Gegenstand: 76 (eine ihrer vier Stellen,
# tests/erhebungen/ablage.py), 77 (build/doc/00-kopf.md) und 80 (tests/protocols/).
# Alles das wird dort nicht gemeldet, sondern als HINWEIS genannt. Jede andere Zeile
# bleibt, wie sie in einer vollen Installation stuende - die Sonde L367 haelt beide
# Ausgaben zeilengleich gegeneinander.
#
# DREI GEGENSTAENDE:
#   (a) LIEFERUMFANG traegt einen bekannten Wert.
#   (b) "nutzung" stimmt mit dem Bestand: Keine Ablage der Nachweisschicht liegt da.
#       Sonst behauptete die Datei weniger, als geliefert ist - und das naechste Heben
#       loeschte es.
#   (c) Das Quellrepositorium fuehrt KEINE solche Datei. Es ist keine Installation;
#       eine Quelle, die "nutzung" behauptet, kann install.py keinen vollen Kern mehr
#       liefern. Die Lockerung oben gilt dort ohnehin nie - was immer die Datei sagt.
# GRENZE. Ob die Nutzung ohne die Nachweisschicht auskommt, belegt nicht diese
# Pruefung, sondern der Vergleich einer reduzierten mit einer vollen Installation
# (Sonde L367). Ein Traeger, den ein Werkzeug zur Laufzeit aus der Nachweisschicht
# liest, fiele erst dort auf.
def _clientmap(root: str):
    kern = os.path.join(root, KERN)
    if not os.path.isdir(kern):
        return None
    if kern not in sys.path:
        sys.path.insert(0, kern)
    try:
        import clientmap
    except ImportError:
        return None
    return clientmap if hasattr(clientmap, "NACHWEIS_ABLAGEN") else None


def reduziert(root: str) -> bool:
    """Liegt hier eine Installation mit Lieferumfang 'nutzung' (D-367)?"""
    if ist_quellrepositorium(root):
        return False
    cm = _clientmap(root)
    return cm is not None and cm.lieferumfang(os.path.join(root, KERN)) == "nutzung"


def nicht_geliefert(root: str, rel: str) -> bool:
    """Ist rel (projektrelativ) ein Teil der Nachweisschicht, den diese reduzierte
    Installation nicht mitliefert?"""
    if not rel.startswith(KERN + "/") or not reduziert(root):
        return False
    return _clientmap(root).ist_nachweis(rel[len(KERN) + 1:])
P73_ZEILE_RE = re.compile(r"^\|\s*([RSBHAMX]\d+)\s*\|")

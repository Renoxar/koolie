"""Der Grundbestand: Pflichtdateien, Berechtigungsdatei, Regeltexte, Skills, verbotene
Inhalte, Platzhalter, Querverweise, Manifest, Versionskette, Clientname im Kern, Mermaid
und Werkzeugneutralitaet.

Pruefungen 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14 und 48. Teil des Validators
validate-framework.py, seit 1.19.1 nach Gegenstand in Module geteilt (K-174). Das
Register aller Pruefungen steht im Kopfkommentar des Einstiegs, die Grenze jeder
einzelnen in ihrem Kopfkommentar hier."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import mermaid_renderer

from .gemeinsam import (
    _clientmap, err, formatgebunden, fremde_praefixe, hinweis, iter_text_files, KERN,
    NEUTRAL_CHRONIK,
    NEUTRAL_CHRONIK_BASENAMES, NEUTRAL_DOKUMENT, nicht_geliefert, parse_frontmatter,
    PLACEHOLDER_RE, read, regel_endung, regeldatei, skill_dirs, SKILL_STATUS,
    SKIP_DIRS, TBD_RE, TEXT_EXT, warn, yaml, ZELLTRENNER_RE)


# Lockdateien sind erzeugte Abhaengigkeitsmetadaten. Sie enthalten naturgemaess fremde
# E-Mail-Adressen und Registry-Adressen und werden weder vom Framework noch vom Projekt
# redaktionell gepflegt - eine Inhaltspruefung dagegen erzeugt nur Rauschen.
SKIP_FILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "npm-shrinkwrap.json",
              "composer.lock", "Cargo.lock", "poetry.lock", "go.sum", "Gemfile.lock"}

# Clientneutral: gilt fuer jedes Client Pack. Die clientspezifischen Pflichtpfade
# (Wurzel-Anweisung, Berechtigungsdatei, Skills, Regeltexte) kommen aus dem Manifest.
REQUIRED_PATHS = [
    "README.md", ".koolie/core/CHANGELOG.md", ".koolie/core/VERSION", ".koolie/core/OWNERS.md",
    ".koolie/core/clients/README.md",
    ".koolie/core/framework/core/00-principles.md", ".koolie/core/framework/core/02-privacy.md", ".koolie/core/framework/core/03-security.md",
    ".koolie/core/framework/core/05-working-model.md", ".koolie/core/framework/core/08-skill-conventions.md",
    ".koolie/core/framework/core/09-risk-model.md", ".koolie/core/framework/role-packs", ".koolie/core/framework/tech-packs",
    ".koolie/project-overlay/OVERLAY.md", ".koolie/project-overlay/overlay-manifest.yaml",
    ".koolie/core/templates/SKILL_TEMPLATE.md", ".koolie/core/prompts",
    ".koolie/core/checklists", ".koolie/core/decision-trees",
    ".koolie/core/onboarding", ".koolie/core/examples",
    ".koolie/core/tests/TEST_CATALOG.md", ".koolie/core/governance/RACI.md", ".koolie/core/governance/DECISION_LOG.md",
    ".koolie/core/docs/PLACEHOLDER_REGISTRY.md",
]

RULE_TRIGGERS = {"always_on", "manual", "model_decision", "agent", "glob"}
SKILL_SECTIONS = [
    "## 1. Zweck, Zielgruppe und Trigger",
    "## 2. Vorbedingungen, Eingaben und Kontext",
    "## 3. Arbeitsschritte",
    "## 4. Grenzen und Rückfragenregeln",
    "## 5. Ausgabeformat",
    "## 6. Qualitätskriterien sowie Prüf- und Freigabeschritt",
    "## 7. Fehlerbehandlung und Abbruch",
]
SKILL_META_KEYS = ["ID", "Name", "Version", "Status", "Owner (Rolle)", "Betriebsmodus", "Zulässige Kontrollstufen"]

# Dieselben Kategorien, die der Schutz-Hook in einer Werkzeugeingabe blockiert
# (tests/scripts/hook-check-secrets.py). Ein Muster, das dort blockiert, darf in einer
# versionierten Datei nicht unbemerkt stehen bleiben - sonst waere dieselbe Zusage an
# zwei Stellen unterschiedlich streng.
#
# Ein Wert in spitzen Klammern ist ein Platzhalter und kein Secret; das Framework
# schreibt seine Beispiele durchgehend so. Nur deshalb kommen die Regeln hier ohne
# Ausnahmeliste aus. Bei der Verbindungszeichenfolge zaehlt allein das Kennwort: Ein
# Platzhalter als Benutzername sagt nichts darueber, ob das Kennwort echt ist.
SECRET_PATTERNS = [
    ("privater Schlüssel", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("Cloud-Zugangsschlüssel", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("Bearer-Token", re.compile(r"\bBearer\s+[A-Za-z0-9\-_\.=]{20,}", re.I)),
    ("Zugangsdaten-Zuweisung", re.compile(
        r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|access[_-]?key|token)\b"
        r"\s*[:=]\s*['\"]?(?![<`])[^\s'\"]{8,}")),
    ("Verbindungszeichenfolge mit Anmeldedaten", re.compile(
        r"(?i)\b[a-z][a-z0-9+\-.]*://[^/\s:]+:(?!<)[^@\s]+@")),
]
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
INTERNAL_HOST_RE = re.compile(r"\b[a-z0-9-]+\.(?:internal|intra|corp|lan)\b", re.I)
URL_RE = re.compile(r"https?://[^\s)>\]\"']+")
URL_ALLOWLIST = ("docs.devin.ai", "devin.ai", "cli.devin.ai", "docs.windsurf.com", "windsurf.com",
                 "example.com", "example.org", "example.invalid", "localhost",
                 # das oeffentliche Repositorium des Frameworks, eng gefasst (D-507)
                 "github.com/Renoxar/koolie")
FENCE4_RE = re.compile(r"^`{4,}", re.M)
MERMAID_RE = re.compile(r"```mermaid\n(.*?)```", re.S)

# --- Querverweisprüfung (FW-KO-04) ---------------------------------------------
# Markdown-Links: [Text](ziel) und [Text](ziel "Titel"); Bildlinks eingeschlossen.
MD_LINK_RE = re.compile(r"""!?\[[^\]]*\]\(\s*<?([^)>\s]+)>?(?:\s+["'][^"']*["'])?\s*\)""")
# Inline-Code: Kandidaten für Pfadnennungen.
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
# Nur Pfade unter diesen Wurzeln werden aus Backticks geprüft. Bewusst eng gehalten:
# Sie benennen Framework-Artefakte und sind damit genau die Verweise, die bei einer
# Umbenennung oder Umstrukturierung stillschweigend brechen.
#
# Die Wurzeln des Frameworks stehen fest, die der Laufzeitschicht kommen aus den
# Manifesten (_link_roots). Bis 0.56.2 standen '.devin/', 'AGENTS.md' und
# 'AGENTS.local.md' hier WOERTLICH - die Pfade des jeweils anderen Packs waren damit
# gar kein Kandidat der Heuristik (CR-2026-080). Die Ableitung hat heute keine
# gemessene Wirkung; sie schafft eine gepflegte Clientliste ab, die ein drittes Client
# Pack von Hand nachtragen muesste und die niemand nachzaehlt.
LINK_ROOTS_FEST = (".koolie/core/", ".koolie/project-overlay/", "README.md")
# Zeichen, die einen Kandidaten als Glob, Platzhalter, Befehl oder Prosa ausweisen.
NOT_A_PATH = set("*<>|?\"' \t()[]{}$!,")
#
# Bis 0.56.2 stand hier zusaetzlich OPTIONAL_RUNTIME_RE: eine Ausnahme fuer die
# Laufzeitpfade, die erst durch eine Projektentscheidung entstehen (30-, 40-, 2N-,
# Pack- und Projektskills). Sie ist mit 0.57.0 weggefallen. In drei Zuschnitten
# gemessen (CR-2026-080): Seit die Client-Bindungs-Warnung nach Pruefung 48 gewandert
# ist, deckt die Fremdpfaderkennung weiter unten denselben Fall VOLLSTAENDIG ab - ein
# Verweis unter der Laufzeitwurzel irgendeines Packs laeuft ohnehin nicht in die
# Totpfadmeldung. Eine Ausnahme, die nichts mehr ausnimmt, ist schlimmer als keine:
# Sie sieht wie Sorgfalt aus. Und sie hat sich mit der engen Wurzelliste gegenseitig
# gedeckt - zwei Fehler in derselben Richtung fallen einzeln nicht auf.
#
# Dateien mit absichtlich nicht existierenden Beispielpfaden (synthetische Beispiele,
# Vorlagen, Migrationshinweise auf frühere Stände). Markdown-Links werden auch dort
# geprüft – nur die Backtick-Heuristik ist ausgesetzt.
LINK_EXCEPTIONS = (
    ".koolie/core/docs/PLACEHOLDER_REGISTRY.md",
    ".koolie/core/CHANGELOG.md",
    ".koolie/core/governance/CHANGE_REQUEST_TEMPLATE.md",
    ".koolie/core/governance/change-requests/",
    ".koolie/core/templates/SKILL_TEMPLATE.md",
    ".koolie/core/examples/",
    # Client Packs beschreiben die Pfade ihres Clients, nicht die der Installation.
    ".koolie/core/clients/_template/",
    # Das Glossar bildet die Begriffe des Kerns auf die Pfade je Client ab; dort sind
    # clientfremde Pfade der Inhalt, nicht eine Altlast.
    ".koolie/core/docs/RUNTIME_GLOSSARY.md",
    # Historische Dokumente behalten die Pfade ihres Entstehungsstands.
    ".koolie/core/tests/protocols/",
    ".koolie/core/governance/DECISION_LOG.md",
)
# Eine CLIENT_PACK.md nennt naturgemaess Pfade, die nur bei ihrem Client existieren.
LINK_EXCEPTION_BASENAMES = ("CLIENT_PACK.md",)


def fundstelle(rel: str, text: str, pos: int) -> str:
    """Pfad, Zeile und Spalte eines Treffers - **ohne den Treffer selbst**.

    Die Diagnosen der Inhaltspruefung nannten bis 0.26.1 den gefundenen Wert im
    Klartext: die E-Mail-Adresse, die IP, den internen Hostnamen, die vollstaendige
    URL samt Parametern - und den gesperrten Begriff. Damit trug ein Schutzlauf genau
    die Angaben weiter, die er finden soll: in ein Terminal, ein Protokoll, eine
    Agentensitzung.

    Am schaerfsten beim Sperrbegriff. Die Liste in .koolie/project-overlay/forbidden-terms.txt
    enthaelt reale Projekt-, Kunden- und Behoerdennamen; die Pruefung nimmt diese Datei
    deshalb ausdruecklich von der eigenen Inhaltspruefung aus - und schrieb den Namen
    dann in die Fehlermeldung. Die eine Zeichenkette, die in keiner Ausgabe des
    Frameworks stehen darf, stand dort durch die Pruefung, die sie verhindern soll.

    Die Secret-Diagnose derselben Funktion machte es von Anfang an richtig: Kategorie
    ohne Wert - aber ohne Position. Diese Funktion zieht die uebrigen nach und traegt
    die Fundstelle dort nach, wo sie fehlte (B03, D-39).

    Spalte statt nur Zeile, damit zwei Treffer derselben Zeile unterscheidbar bleiben -
    sonst faellt der zweite als scheinbares Duplikat nicht auf.
    """
    zeile = text.count(chr(10), 0, pos) + 1
    spalte = pos - (text.rfind(chr(10), 0, pos) + 1) + 1
    return f"{rel}:{zeile}:{spalte}"


def check_required(root: str, man: dict) -> None:
    pflicht = list(REQUIRED_PATHS)
    pflicht += [man["root_instruction_file"], man["permissions_file"],
                man["skills_dir"], man["agents_dir"]]
    pflicht += [f"{man['pack_runtime_dir']}/{n}{regel_endung(man)}" for n in
                ("00-framework-core", "10-privacy-security", "15-development-rules",
                 "20-project-overlay")]
    for rel in pflicht:
        if not os.path.exists(os.path.join(root, rel)):
            err(f"Pflichtpfad fehlt: {rel}")


def soll_kernregeln(root: str, man: dict) -> list[str]:
    """Kernzusagen B1 bis B6 in der Schreibweise dieses Clients, aus der Kernquelle.

    Berechtigungen sind Saat: Nach der Erstinstallation gehoert die Datei dem Projekt und
    wird nie ueberschrieben - install.py --check meldet dort also nichts. Diese Pruefung
    ist deshalb die einzige Stelle, an der eine entfernte Kernregel auffaellt. Fehlt das
    Abbildungsmodul (etwa in einer Teilkopie des Kerns), wird nur gewarnt: Die Pruefungen
    gegen die Datei selbst greifen weiterhin.
    """
    kern = os.path.join(root, KERN)
    if not os.path.isdir(kern):
        return []
    if kern not in sys.path:
        sys.path.insert(0, kern)
    try:
        import clientmap
    except ImportError:
        warn("clientmap.py nicht gefunden – Kernregeln werden nur gegen die "
             "Berechtigungsdatei selbst geprüft, nicht gegen die Kernquelle")
        return []
    try:
        quelle = json.loads(clientmap.load_source(kern, "permissions.json"))
        return clientmap.core_rules(quelle, man)
    except (OSError, ValueError) as exc:
        err(f"Kernquelle der Berechtigungen nicht auswertbar: {exc}")
        return []


def check_config(root: str, man: dict) -> None:
    if formatgebunden(man, 2):
        return
    rel = man["permissions_file"]
    path = os.path.join(root, *rel.split("/"))
    if not os.path.exists(path):
        return
    try:
        cfg = json.loads(read(path))
    except json.JSONDecodeError as exc:
        err(f"{rel} ist kein gültiges JSON: {exc}")
        return
    perms = cfg.get("permissions", {})
    deny = set(perms.get("deny", []))
    allow = set(perms.get("allow", []))

    # Eine Pfadregel fuer ein Werkzeug, das der Client dafuer nicht auswertet, wird
    # angenommen und nie konsultiert - sie taeuscht Schutz vor und erzeugt beim
    # Sitzungsstart Laerm. Welche Werkzeuge Pfadregeln kennen, sagt das Manifest; ohne die
    # Angabe unterbleibt die Pruefung, weil sie dann unbelegt waere (AP2-CC-02, D-26).
    pfadwerkzeuge = man.get("permission_path_tools")
    if pfadwerkzeuge:
        befehlswerkzeuge = set(man.get("permission_tools", {}).get("exec", []))
        namenswerkzeuge = set(man.get("permission_name_tools", []))
        for korb in ("deny", "ask", "allow"):
            for regel in perms.get(korb, []):
                if not isinstance(regel, str) or "(" not in regel:
                    continue
                werkzeug = regel.split("(", 1)[0]
                if (werkzeug in befehlswerkzeuge or werkzeug in pfadwerkzeuge
                        or werkzeug in namenswerkzeuge):
                    continue
                err(f"{rel}: {korb}-Regel '{regel}' nennt ein Werkzeug, fuer das dieser "
                    f"Client keine Pfadregeln auswertet. Zulaessig sind "
                    f"{', '.join(sorted(pfadwerkzeuge))}; eine Regel ohne Pfad wirkt "
                    f"weiterhin auf Werkzeugebene")
    must = cfg.get("_core_rules_integrity", {}).get("deny_must_contain", [])
    if not must:
        err(f"{rel}: Block _core_rules_integrity.deny_must_contain fehlt")
    for rule in must:
        if rule not in deny:
            err(f"{rel}: Kernregel fehlt in deny: {rule}")
        if rule in allow:
            err(f"{rel}: Kernverbot steht in allow: {rule}")
    # Die Liste gegen die Kernquelle abgleichen, nicht nur gegen sich selbst. Ohne diesen
    # Schritt genuegte es, eine Kernregel in beiden Listen zu streichen - die Datei bliebe
    # in sich stimmig und der Verlust unbemerkt.
    for rule in soll_kernregeln(root, man):
        if rule in must:
            continue  # von der Schleife darueber bereits geprueft
        err(f"{rel}: Kernregel fehlt in _core_rules_integrity.deny_must_contain "
            f"(laut Kernquelle vorgesehen): {rule}")
        if rule not in deny:
            err(f"{rel}: Kernregel fehlt in deny: {rule}")
    # Nie erlaubt, unabhaengig vom Client: Push, Merge, Rechteausweitung, Loeschen.
    # Die Werkzeugnamen unterscheiden sich je Client, die Absicht nicht.
    verboten = ("Exec(git push", "Exec(sudo", "Exec(rm -rf",
                "Bash(git push", "Bash(git merge", "Bash(sudo", "Bash(rm")
    for rule in allow:
        if rule.startswith(verboten):
            err(f"{rel}: unzulässige allow-Regel: {rule}")
    # Abrufwerkzeuge: aus dem Manifest, nicht aus einer Namensliste. Bis 0.32.0 standen
    # hier "Fetch(*", "WebFetch" und "WebSearch" fest verdrahtet - und das war
    # asymmetrisch: 'Fetch(domain:...)' lief durch, 'WebFetch(domain:...)' fiel, dieselbe
    # Absicht bei zwei Packs verschieden entschieden. Nach D-59 gibt es keine
    # Domain-Ausnahme; damit ist **jede** allow-Regel auf ein Abrufverb unzulaessig, und
    # der dokumentierte Weg ist, das globale Verbot per Aenderungsantrag zu ersetzen
    # (B11, V10).
    abrufwerkzeuge = tuple(man.get("permission_tools", {}).get("fetch", ()))
    for rule in allow:
        if not isinstance(rule, str):
            continue
        name = rule.split("(", 1)[0].strip()
        if abrufwerkzeuge and name in abrufwerkzeuge:
            err(f"{rel}: unzulässige allow-Regel auf ein Abrufwerkzeug: {rule}. Das "
                f"generelle Netzverbot kennt keine Ausnahme je Domain - `deny` gewinnt "
                f"immer, eine zusätzliche allow-Regel hebt es nicht auf. Wer externen "
                f"Abruf braucht, ersetzt die Verbotsregel über einen Änderungsantrag "
                f"(V10) und weist die Ersatzbeschränkung nach (B11, D-59)")
    # Weitere JSON-Dateien der Laufzeitschicht auf Gueltigkeit pruefen.
    rt = man["runtime_dir"]
    for name in os.listdir(os.path.join(root, *rt.split("/"))) if os.path.isdir(os.path.join(root, *rt.split("/"))) else []:
        if not name.endswith((".json", ".json.example")):
            continue
        p = os.path.join(root, *rt.split("/"), name)
        try:
            data = json.loads(read(p))
        except json.JSONDecodeError as exc:
            err(f"{rt}/{name} ist kein gültiges JSON: {exc}")
            continue
        if "mcp" in name and not name.endswith(".example"):
            blob = json.dumps(data).lower()
            if any(k in blob for k in ("password", "token", "secret", "apikey", "api_key")):
                err(f"{rt}/{name} enthält Schlüsselwörter für Zugangsdaten – gehören in eine nicht versionierte Datei oder einen Tresor")


KERNREGEL_PRAEFIXE = ("00-", "10-", "15-", "20-")


def _check_rule_client_form(rel: str, fn: str, text: str, spec: dict) -> int:
    """Regeldatei in der Bedingungssprache des Clients. Rueckgabe: Zeichen, die stets laden.

    Geprueft wird die **installierte** Fassung, nicht die Quelle (D-26): Ein stehen
    gebliebenes `trigger:` oder `globs:` bedeutet, dass die Datei nicht durch die Abbildung
    des Client Packs gelaufen ist - der Client wertet diese Felder nicht aus, die
    Ladebedingung waere damit verfallen.
    """
    feld = spec.get("condition_field")
    erlaubt = set(spec.get("allowed_fields", []))
    if not text.startswith("---"):
        return len(text)
    fm, _ = parse_frontmatter(text)
    if not fm or "_error" in fm:
        err(f"{rel}: Frontmatter vorhanden, aber nicht lesbar")
        return 0
    if "_raw" in fm:
        return 0
    for schluessel in sorted(set(fm) - erlaubt):
        err(f"{rel}: Frontmatter-Feld '{schluessel}' – dieser Client wertet für Regeldateien "
            f"nur {sorted(erlaubt)} aus (K-18). Ein stehen gebliebenes 'trigger' oder 'globs' "
            f"heißt: Die Datei ist nicht durch die Abbildung des Client Packs gelaufen, ihre "
            f"Ladebedingung ist verfallen")
    if feld not in fm:
        return len(text)
    werte = fm[feld]
    if spec.get("condition_format", "list") == "list" and (
            not isinstance(werte, list) or not werte
            or not all(isinstance(w, str) and w.strip() for w in werte)):
        err(f"{rel}: '{feld}' muss eine nichtleere Liste von Dateimustern sein")
    if fn.startswith(KERNREGEL_PRAEFIXE):
        err(f"{rel}: Kernregel über '{feld}' an Dateimuster gebunden – sie gilt für jede "
            f"Aufgabe; eine Ladebedingung wäre hier eine Lockerung")
    return 0


def check_rules(root: str, man: dict) -> None:
    """Regeltexte der Laufzeitschicht.

    Drei Bauarten, je nach Client:

    * Der Client kennt die Ladetrigger der Kernquelle (`devin-desktop`): geprueft wird das
      Quellfrontmatter - `description`, `trigger`, bei `glob` zusaetzlich `globs`.
    * Der Client kennt eine **eigene** Bedingungssprache (`rule_triggers` im Manifest, bei
      `claude-code` das Feld `paths`): geprueft wird die installierte Fassung gegen die
      Felder, die er auswertet.
    * Der Client laedt Regeldateien nicht von sich aus: Dort wirkt eine Datei erst, wenn die
      Wurzel-Anweisung sie einbindet - eine nicht eingebundene Datei ist stillschweigend
      wirkungslos, und genau das wird geprueft.

    DIE ZEICHENGRENZE IST EIN BUDGET FUER DIE SUMME (D-387, K-130). Verbindlich ist, was
    jede Sitzung laedt: Wurzel-Anweisung plus die unbedingt geladenen Regeltexte, hoechstens
    40.000 Zeichen - bei jedem Pack, bei den Ladetriggern der Kernquelle die Regeln mit
    `always_on`. Die 12.000 Zeichen je Datei und die 6.000 fuer die Overlay-Laufzeitregel
    sind Warnungen. Alle drei Zahlen sind eine Vorgabe des Frameworks, keine Eigenschaft
    eines Clients (CR-2026-027 E3).
    """
    rules_rel = man["pack_runtime_dir"]
    rules_dir = os.path.join(root, *rules_rel.split("/"))
    if not os.path.isdir(rules_dir):
        return

    wurzel_rel = man["root_instruction_file"]
    wurzel_pfad = os.path.join(root, *wurzel_rel.split("/"))
    wurzel_text = read(wurzel_pfad) if os.path.exists(wurzel_pfad) else ""
    eigene_bedingung = man.get("rule_triggers")
    mit_triggern = man.get("has_rule_triggers", True)
    ueber_import = not mit_triggern
    stets_geladen = len(wurzel_text)

    for fn in sorted(os.listdir(rules_dir)):
        if not fn.endswith(regel_endung(man)):
            continue
        text = read(os.path.join(rules_dir, fn))
        rel = f"{rules_rel}/{fn}"

        if not ueber_import:
            if len(text) > 12000:
                warn(f"{rel}: {len(text)} Zeichen (> 12.000, SOLL-Grenze je Datei)")
            if fn == regeldatei(man, "20-project-overlay.md") and len(text) > 6000:
                warn(f"{rel}: {len(text)} Zeichen (> 6.000, SOLL-Grenze)")
        if fn == "README.md":
            continue

        if eigene_bedingung:
            stets_geladen += _check_rule_client_form(rel, fn, text, eigene_bedingung)
        elif mit_triggern:
            fm, _ = parse_frontmatter(text)
            if not fm or "_error" in fm:
                err(f"{rel}: Frontmatter fehlt oder ungültig")
                continue
            if "_raw" in fm:
                continue
            if "description" not in fm or not str(fm.get("description", "")).strip():
                err(f"{rel}: Frontmatter-Feld description fehlt")
            trig = fm.get("trigger")
            if trig not in RULE_TRIGGERS:
                err(f"{rel}: trigger '{trig}' nicht in {sorted(RULE_TRIGGERS)}")
            if trig == "glob" and not fm.get("globs"):
                err(f"{rel}: trigger glob ohne globs")
            if trig == "always_on":
                stets_geladen += len(text)
        else:
            # Ohne eigene Ladebedingung entscheidet die Einbindung. Eine Kernregel muss
            # in der Wurzel-Anweisung GENANNT sein, sonst waere sie wirkungslos.
            #
            # BIS 1.3.0 VERLANGTE DIESE ZEILE DIE FORM `@<pfad>`, UND DIE FORM WAR
            # GERATEN (CR-2026-133, D-348): Kein ausgeliefertes Pack war so gebaut, und
            # die `@`-Schreibweise stammte aus der Wurzel-Anweisung eines anderen
            # Clients. Am 2026-09-23 ist sie zum ersten Mal an einem Client gemessen
            # worden, der Regeldateien wirklich nicht von sich aus laedt - und dort
            # bewirkt `@<pfad>` NICHTS: Die Sonde stand im Prompt-Eingang nicht.
            #   ➡️ Eine Prüfung, die eine ungemessene Schreibweise verlangt, misst die
            #      Schreibweise und nicht die Sache.
            # Geprueft wird deshalb die NENNUNG. Sie ist die schwaechere Form, und das
            # ist ehrlich: Was eine Nennung bewirkt, haengt am Modell und nicht an der
            # Engine - die Zeilen R2 und R3 des betroffenen Packs sagen es.
            eingebunden = rel in wurzel_text
            if fn.startswith(KERNREGEL_PRAEFIXE) and not eingebunden:
                err(f"{rel}: nicht in {wurzel_rel} genannt – die Regel wäre wirkungslos, "
                    f"weil dieser Client Regeldateien nicht von sich aus lädt "
                    f"(manifest.json: has_rule_triggers = false)")
            if eingebunden:
                stets_geladen += len(text)
            if text.startswith("---"):
                warn(f"{rel}: YAML-Frontmatter, obwohl dieser Client keine Ladebedingung kennt "
                     f"(Frontmatter nur mit dokumentierten Feldern, K-18)")

    if stets_geladen > 40000:
        err(f"{wurzel_rel} und die unbedingt geladenen Regeltexte ergeben {stets_geladen} "
            f"Zeichen, die in jeder Sitzung geladen werden (> 40.000, Least Context, D-387)")

    if os.path.exists(wurzel_pfad) and not ueber_import and len(wurzel_text) > 12000:
        warn(f"{wurzel_rel}: {len(wurzel_text)} Zeichen (> 12.000, SOLL-Grenze je Datei)")


def check_skills(root: str, man: dict) -> None:
    ids: dict[str, str] = {}
    runtime = man["skills_dir"]
    # Fremde Skills, die das Projekt im Overlay-Manifest deklariert, sind keine Koolie-Skills
    # und werden nicht nach dessen Regeln geprueft - nur in der Laufzeitablage, nie in den
    # Quellen des Kerns (1.21.0, K-31). Den Korb verlangt Pruefung 72 weiter (D-238).
    fremd = fremde_praefixe(root)
    for skills_dir, prefix in skill_dirs(root, man):
        # Die Modellwahl-Sperre wird nur in der *installierten* Fassung geprueft: In der
        # Quelle steht die Aussage als `triggers`, erst die Abbildung uebersetzt sie.
        check_skills_in(skills_dir, prefix, ids,
                        man if prefix == runtime else None,
                        fremd if prefix == runtime else ())


def check_skills_in(skills_dir: str, prefix: str, ids: dict[str, str],
                    man: dict | None = None, fremd=()) -> None:
    for name in sorted(os.listdir(skills_dir)):
        sdir = os.path.join(skills_dir, name)
        if not os.path.isdir(sdir):
            continue
        if fremd and any(name.startswith(p) for p in fremd):
            continue
        rel = f"{prefix}/{name}"
        if not re.fullmatch(r"[a-z0-9-]+", name):
            err(f"{rel}: Verzeichnisname muss aus Kleinbuchstaben, Ziffern, Bindestrichen bestehen")
        if not re.match(r"^(fw|prj|role-[a-z0-9]+|tech-[a-z0-9]+)-", name):
            warn(f"{rel}: Präfix entspricht nicht fw-/prj-/role-<pack>-/tech-<pack>-")
        for req in ("SKILL.md", "EXAMPLES.md", "TESTS.md", "CHANGELOG.md"):
            if not os.path.exists(os.path.join(sdir, req)):
                err(f"{rel}: {req} fehlt")
        skill_path = os.path.join(sdir, "SKILL.md")
        if not os.path.exists(skill_path):
            continue
        text = read(skill_path)
        fm, body = parse_frontmatter(text)
        if not fm or "_error" in fm:
            err(f"{rel}/SKILL.md: Frontmatter fehlt oder ungültig")
            continue
        if "_raw" not in fm:
            if fm.get("name") != name:
                err(f"{rel}/SKILL.md: name '{fm.get('name')}' != Verzeichnisname")
            if not str(fm.get("description", "")).strip():
                err(f"{rel}/SKILL.md: description fehlt")
            fmt = (man or {}).get("skill_frontmatter", {})
            # Die Quelle nennt allowed-tools als Liste von Verben, die installierte Fassung
            # je nach Client als Liste oder als kommagetrennte Zeichenkette von Werkzeugnamen.
            # Ohne diese Unterscheidung lief die Pruefung ueber die *Zeichen* der Zeichenkette
            # und meldete jeden installierten Skill als nicht schreibend (AP2-CC-09).
            tools = fm.get("allowed-tools") or []
            if isinstance(tools, str):
                tools = [x for x in re.split(r"[,\s]+", tools) if x]
            if not tools:
                err(f"{rel}/SKILL.md: allowed-tools fehlt (minimale Werkzeugmenge angeben)")
            schreibverben = ("edit", "exec", "write")
            namen = fmt.get("tool_names", {})
            schreibnamen = {n for v in schreibverben for n in namen.get(v, [])}
            writes = any(t in schreibverben or t in schreibnamen for t in tools)

            sperre = fmt.get("model_invocation_field")
            # Traegt dieser Ablageort `triggers` ueberhaupt? Ein Client, der das Feld nicht
            # kennt, bekommt die Aussage abgebildet - dann ist ihr Fehlen kein Fehler,
            # sondern die Abbildung ist zu pruefen (AP2-CC-01 und AP2-CC-09, D-26).
            abgebildet = bool(sperre) and "triggers" in fmt.get("drop_fields", [])
            triggers = fm.get("triggers") or []
            if abgebildet:
                if writes and fm.get(sperre) is not True:
                    err(f"{rel}/SKILL.md: schreibender/ausfuehrender Skill ohne "
                        f"'{sperre}: true' - die Quelle verlangt triggers: [user], die "
                        f"installierte Fassung muss das in der Form dieses Clients tragen")
            else:
                if writes and triggers != ["user"]:
                    err(f"{rel}/SKILL.md: schreibender/ausfuehrender Skill muss "
                        f"triggers: [user] haben")
                if not triggers:
                    err(f"{rel}/SKILL.md: triggers fehlt")

            erlaubt = ("name", "description", "argument-hint", "allowed-tools", "permissions",
                       "triggers", "model", "subagent", "agent")
            # Die beiden abgebildeten Felder heissen je Client anders und stehen deshalb
            # nicht in der Liste, sondern kommen aus dem Manifest: die Modellwahl-Sperre
            # (AP2-CC-01) und seit 0.35.0 die Werkzeugsperre je Skill (D-64).
            deny_feld = fmt.get("skill_deny_field")
            for key in fm:
                if key not in erlaubt and key != sperre and key != deny_feld:
                    warn(f"{rel}/SKILL.md: Frontmatter-Feld '{key}' ist nicht dokumentiert")
        for key in SKILL_META_KEYS:
            if not re.search(rf"^\|\s*{re.escape(key)}\s*\|", body, re.M):
                err(f"{rel}/SKILL.md: Metadatenzeile '{key}' fehlt")
        m = re.search(r"^\|\s*Status\s*\|\s*`?([^`|]+?)`?\s*\|", body, re.M)
        if m and m.group(1).strip() not in SKILL_STATUS:
            err(f"{rel}/SKILL.md: Status '{m.group(1).strip()}' unbekannt")
        # Bis 0.12.0 genuegte irgendein Wert - 'banane' blieb unbemerkt, und die Version
        # konnte dem Aenderungsverlauf widersprechen (FW-VN-01, Sonden S4 und S5).
        m = re.search(r"^\|\s*Version\s*\|\s*`?([^`|]+?)`?\s*\|", body, re.M)
        cl_path = os.path.join(sdir, "CHANGELOG.md")
        if m:
            fassung = m.group(1).strip()
            if not SEMVER_RE.match(fassung):
                err(f"{rel}/SKILL.md: Version '{fassung}' ist kein Semantic Versioning "
                    f"(MAJOR.MINOR.PATCH)")
            elif os.path.exists(cl_path) and not re.search(
                    rf"^\|\s*{re.escape(fassung)}\s*\|", read(cl_path), re.M):
                err(f"{rel}: Version {fassung} hat keinen Eintrag in CHANGELOG.md "
                    f"(08-skill-conventions.md Abschnitt 7)")
        m = re.search(r"^\|\s*ID\s*\|\s*`?([A-Z0-9-]+)`?\s*\|", body, re.M)
        if m:
            vorher = ids.get(m.group(1))
            # Gleicher Skillname in Quellablage und aktivierter Schicht ist eine Kopie,
            # kein Konflikt. Nur unterschiedliche Skills mit gleicher ID sind ein Fehler.
            if vorher is not None and vorher != name:
                err(f"{rel}/SKILL.md: ID {m.group(1)} doppelt (auch in {vorher})")
            ids[m.group(1)] = name
        else:
            err(f"{rel}/SKILL.md: ID nicht lesbar")
        for sec in SKILL_SECTIONS:
            if sec not in body:
                err(f"{rel}/SKILL.md: Pflichtabschnitt fehlt: {sec}")
        for word in ("Rückfrage", "Fundstelle"):
            if word not in body:
                err(f"{rel}/SKILL.md: Begriff '{word}' fehlt (Rückfragen-/Belegpflicht)")
        ex_path = os.path.join(sdir, "EXAMPLES.md")
        if os.path.exists(ex_path):
            ex = read(ex_path)
            if "synthetisch" not in ex:
                err(f"{rel}/EXAMPLES.md: Kennzeichnung 'synthetisch' fehlt")
            if "Positivbeispiel" not in ex or "Negativbeispiel" not in ex:
                err(f"{rel}/EXAMPLES.md: Positiv- und Negativbeispiel erforderlich")
        t_path = os.path.join(sdir, "TESTS.md")
        if os.path.exists(t_path):
            t = read(t_path)
            if not re.search(r"-P0\d", t) or not re.search(r"-N0\d", t):
                err(f"{rel}/TESTS.md: mindestens ein Positivtest (-P0n) und ein Negativtest (-N0n) erforderlich")
            for col in ("Test-ID", "Ziel", "Vorbedingung", "Eingabe", "Erwartetes Verhalten",
                        "Unzulässiges Verhalten", "Prüfmethode", "Ergebnisstatus"):
                if col not in t:
                    err(f"{rel}/TESTS.md: Spalte '{col}' fehlt")


def load_placeholder_registry(root: str) -> set[str]:
    path = os.path.join(root, ".koolie/core", "docs", "PLACEHOLDER_REGISTRY.md")
    if not os.path.exists(path):
        return set()
    return set(PLACEHOLDER_RE.findall(read(path)))


def check_content(root: str) -> None:
    registry = load_placeholder_registry(root)
    forbidden_terms: list[str] = []
    ft_path = os.path.join(root, ".koolie/project-overlay", "forbidden-terms.txt")
    if os.path.exists(ft_path):
        forbidden_terms = [l.strip() for l in read(ft_path).splitlines()
                           if l.strip() and not l.startswith("#")]
    unknown_placeholders: dict[str, set[str]] = {}
    for path in iter_text_files(root):
        # os.path.relpath liefert unter Windows Backslashes; ohne diese Normalisierung
        # greift unten kein einziger Pfadvergleich - check_links macht es seit jeher so.
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if rel.startswith(f"{KERN}/tests/scripts/") or rel == ".koolie/project-overlay/forbidden-terms.txt":
            continue
        if os.path.basename(path) in SKIP_FILES:
            continue
        text = read(path)
        for label, pat in SECRET_PATTERNS:
            m = pat.search(text)
            if m:
                err(f"{fundstelle(rel, text, m.start())}: FW-CONTENT-SECRET: "
                    f"Secret-Muster ({label})")
        for m in EMAIL_RE.finditer(text):
            if not m.group(0).lower().endswith(("example.com", "example.org", "example.invalid")):
                err(f"{fundstelle(rel, text, m.start())}: FW-CONTENT-EMAIL: E-Mail-Adresse")
        for m in IP_RE.finditer(text):
            if not m.group(0).startswith(("0.", "127.", "192.0.2.", "198.51.100.", "203.0.113.")):
                err(f"{fundstelle(rel, text, m.start())}: FW-CONTENT-IP: IP-Adresse")
        for m in INTERNAL_HOST_RE.finditer(text):
            err(f"{fundstelle(rel, text, m.start())}: FW-CONTENT-HOST: interner Hostname")
        for m in URL_RE.finditer(text):
            if not any(host in m.group(0) for host in URL_ALLOWLIST):
                warn(f"{fundstelle(rel, text, m.start())}: FW-CONTENT-URL: URL außerhalb der Allowlist")
        for term in forbidden_terms:
            m = re.search(rf"(?i)\b{re.escape(term)}\b", text)
            if m:
                err(f"{fundstelle(rel, text, m.start())}: FW-CONTENT-TERM: gesperrter Begriff")
        if FENCE4_RE.search(text) and rel.startswith(
                (".devin/", ".claude/", ".koolie/project-overlay/") +
                tuple(f"{KERN}/{d}/" for d in ("framework", "prompts", "checklists", "decision-trees",
                                               "onboarding", "templates", "governance", "pilot",
                                               "build", "docs", "examples"))):
            err(f"{rel}: Codeblock mit vier oder mehr Backticks (bricht die Dokumentassemblierung)")
        if registry and rel not in OHNE_PLATZHALTERREGISTER:
            for ph in set(PLACEHOLDER_RE.findall(text)):
                if ph not in registry and ph not in ("TBD",):
                    unknown_placeholders.setdefault(ph, set()).add(rel)
    for ph, files in sorted(unknown_placeholders.items()):
        warn(f"Platzhalter <{ph}> nicht in .koolie/core/docs/PLACEHOLDER_REGISTRY.md (in {', '.join(sorted(files)[:3])}{'…' if len(files) > 3 else ''})")


def _normalize_target(raw: str):
    """Bereinigt eine Verweisangabe zu einem Pfad oder liefert None, wenn keiner vorliegt."""
    t = raw.strip()
    if not t or t.startswith(("http://", "https://", "mailto:", "#", "//")):
        return None
    t = t.split("#", 1)[0]                    # Anker abtrennen
    t = re.sub(r":\d+(?:-\d+)?$", "", t)      # Fundstellenformat pfad/datei:zeile
    t = t.rstrip(".,;:")                      # Satzzeichen am Satzende
    if not t or t in (".", ".."):
        return None
    if t.endswith("-"):                       # Präfixnennung, z. B. ".devin/rules/00-"
        return None
    if "…" in t or t.endswith("..."):     # Sammelnennung, z. B. "framework/core/…"
        return None
    if any(c in NOT_A_PATH for c in t):
        return None
    return t


def _client_runtime_paths(root: str) -> dict:
    """Laufzeitpfade aller Client Packs: Praefix -> Clientname.

    Damit laesst sich unterscheiden, ob eine nicht aufloesbare Pfadangabe ein echter
    toter Verweis ist oder die Nennung eines Laufzeitpfads, der zu einem anderen
    Client Pack gehoert. Letzteres ist im werkzeugneutralen Kern eine Altlast,
    kein Fehler - aber es gehoert sichtbar gemacht.
    """
    out = {}
    base = os.path.join(root, KERN, "clients")
    if not os.path.isdir(base):
        return out
    for name in sorted(os.listdir(base)):
        mp = os.path.join(base, name, "manifest.json")
        if not os.path.exists(mp):
            continue
        try:
            man = json.loads(read(mp))
        except json.JSONDecodeError:
            continue
        for key in ("runtime_dir", "root_instruction_file"):
            if man.get(key):
                out[man[key]] = man["client"]
    return out


def _link_roots(root: str) -> tuple:
    """Wurzeln der Backtick-Heuristik: die festen des Frameworks und die jedes Packs.

    Die Laufzeitwurzeln stammen aus den Manifesten, damit ein neues Client Pack ohne
    Aenderung an dieser Pruefung erfasst wird - dieselbe Bauform wie
    _client_actor_names in Pruefung 14.
    """
    runtime: set[str] = set()
    base = os.path.join(root, KERN, "clients")
    if os.path.isdir(base):
        for name in sorted(os.listdir(base)):
            if name.startswith("_"):
                continue
            mp = os.path.join(base, name, "manifest.json")
            if not os.path.exists(mp):
                continue
            try:
                man = json.loads(read(mp))
            except json.JSONDecodeError:
                continue
            if man.get("runtime_dir"):
                runtime.add(man["runtime_dir"].rstrip("/") + "/")
            for key in ("root_instruction_file", "root_instruction_local"):
                if man.get(key):
                    runtime.add(man[key])
    return LINK_ROOTS_FEST + tuple(sorted(runtime))


def _target_exists(root: str, src_rel: str, target: str) -> bool:
    """Prüft repo-relativ, relativ zur verweisenden Datei und - für Dateien innerhalb
    eines Client Packs - relativ zu dessen root-template."""
    base = os.path.basename(target)
    # Nutzerlokale Dateien (Namensbestandteil ".local.") sind per .gitignore bewusst
    # nicht versioniert - CLAUDE.local.md, .claude/settings.local.json und Ähnliches.
    # Ein Verweis darauf beschreibt eine Möglichkeit, keine vorhandene Datei.
    if ".local." in base or base.endswith(".local"):
        return True
    # Die Angabe des Lieferumfangs schreibt install.py erst im Projekt (D-367); im
    # Quellrepositorium beschreibt ein Verweis darauf die Installation, nicht diesen Baum.
    cm = _clientmap(root)
    if cm is not None and target == f"{KERN}/{cm.LIEFERUMFANG_DATEI}":
        return True
    # Eine mitgelieferte Vorlage zählt als Nachweis: Dateien wie .mcp.json legt die
    # nutzende Person selbst aus der .example-Fassung an.
    for cand in (target, target + ".example", target + ".template"):
        if os.path.exists(os.path.join(root, cand)):
            return True
    src_dir = os.path.dirname(os.path.join(root, src_rel))
    if os.path.exists(os.path.normpath(os.path.join(src_dir, target))):
        return True
    # Eine Datei im root-template eines Client Packs beschreibt die Laufzeitschicht
    # dieses Packs, nicht die installierte. Ihre Pfade dort aufloesen.
    m = re.match(r"(\.koolie/core/clients/[^/]+/root-template)/", src_rel)
    if m and os.path.exists(os.path.join(root, *m.group(1).split("/"), *target.split("/"))):
        return True
    return False


def check_links(root: str) -> None:  # noqa: C901
    """FW-KO-04: Querverweise zeigen auf existierende Dateien oder Verzeichnisse.

    Zwei Quellen: Markdown-Links (überall geprüft) und in Backticks genannte
    Framework-Pfade (Heuristik, in LINK_EXCEPTIONS ausgesetzt). Globs, Platzhalter
    und Befehlszeilen werden über NOT_A_PATH verworfen statt gemeldet.
    """
    fremdpfade = _client_runtime_paths(root)
    link_roots = _link_roots(root)
    herkunft = {}  # Traeger -> Zahl der Verweise in die nicht gelieferte Nachweisschicht

    def geliefert_fehlt(rel: str, target: str) -> bool:
        """Zeigt der Verweis in die Nachweisschicht, die dieser Umfang nicht liefert?
        Dann ist er eine Herkunftsangabe und wird gezaehlt statt gemeldet (D-367)."""
        ziel = os.path.normpath(os.path.join(os.path.dirname(rel), target)).replace(os.sep, "/")
        if nicht_geliefert(root, target.rstrip("/")) or nicht_geliefert(root, ziel):
            herkunft[rel] = herkunft.get(rel, 0) + 1
            return True
        return False

    for path in iter_text_files(root):
        if not path.endswith((".md", ".template")):
            continue
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if rel.startswith(".koolie/core/tests/scripts/"):
            continue
        text = read(path)

        for m in MD_LINK_RE.finditer(text):
            target = _normalize_target(m.group(1))
            if target is not None and not _target_exists(root, rel, target)                     and not geliefert_fehlt(rel, target):
                err(f"{rel}: Markdown-Link zeigt ins Leere: {m.group(1)}")

        if rel.startswith(LINK_EXCEPTIONS) or os.path.basename(rel) in LINK_EXCEPTION_BASENAMES:
            continue
        seen = set()
        for m in BACKTICK_RE.finditer(text):
            tok = m.group(1).strip()
            if not tok.startswith(link_roots):
                continue
            target = _normalize_target(tok)
            if target is None or target in seen:
                continue
            seen.add(target)
            if _target_exists(root, rel, target):
                continue
            # Gehoert der Pfad zur Laufzeitschicht eines anderen Client Packs, ist es
            # keine tote Referenz, sondern eine Client-Bindung im Kern (Arbeitsliste
            # fuer die Neutralisierung).
            fremd = next((c for pfx, c in fremdpfade.items()
                          if target == pfx or target.startswith(pfx.rstrip("/") + "/")), None)
            # Eine Datei im root-template eines Packs beschreibt dessen eigene
            # Laufzeitschicht - dort ist der Pfad richtig, nicht eine Altlast.
            if fremd and re.match(r"\.koolie/core/clients/[^/]+/root-template/", rel):
                continue
            # Ein Pfad eines anderen Packs ist kein toter Verweis, sondern eine
            # Client-Bindung. Seit 0.57.0 meldet sie Pruefung 48 - als Fehler, ueber
            # alle Traeger und ohne die drei Grenzen dieser Heuristik (D-128).
            if not fremd and not geliefert_fehlt(rel, target):
                err(f"{rel}: Pfadangabe existiert nicht: {tok}")
    if herkunft:
        hinweis(f"{sum(herkunft.values())} Verweis(e) aus {len(herkunft)} Träger(n) zeigen "
                f"in die Nachweisschicht, die dieser Lieferumfang nicht mitliefert - "
                f"Herkunftsangaben, nicht gemeldet (Prüfung 12, D-367)")


RUNTIME_PLACEHOLDER_RE = re.compile(
    r"<(RUNTIME_DIR|ROOT_INSTRUCTION_FILE|ROOT_INSTRUCTION_LOCAL|PERMISSIONS_FILE"
    r"|SKILLS_DIR|RULES_DIR|AGENTS_DIR|HOOKS_FILE|MCP_FILE|CLIENT_NAME)>")


def check_runtime_placeholders(root: str, man: dict) -> None:
    """In der installierten Laufzeitschicht darf kein Laufzeit-Platzhalter stehen.

    Sie werden von install.py aus dem Manifest aufgeloest. Bleibt einer stehen, fehlt
    er im Manifest des Client Packs - der Text verweist dann ins Leere.
    """
    rt = os.path.join(root, *man["runtime_dir"].split("/"))
    if not os.path.isdir(rt):
        return
    for dirpath, dirnames, filenames in os.walk(rt):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if os.path.splitext(fn)[1] not in TEXT_EXT:
                continue
            p = os.path.join(dirpath, fn)
            gefunden = {m.group(0) for m in RUNTIME_PLACEHOLDER_RE.finditer(read(p))}
            if gefunden:
                err(f"{os.path.relpath(p, root)}: unaufgelöste Laufzeit-Platzhalter "
                    f"{', '.join(sorted(gefunden))} – fehlen in runtime_placeholders des Client Packs")


def check_manifest(root: str) -> None:
    path = os.path.join(root, ".koolie/project-overlay", "overlay-manifest.yaml")
    if not os.path.exists(path) or yaml is None:
        return
    try:
        data = yaml.safe_load(read(path)) or {}
    except yaml.YAMLError as exc:  # type: ignore[attr-defined]
        err(f"overlay-manifest.yaml ungültig: {exc}")
        return
    types = {"ai-governance", "ai-process-model", "roadmap", "architecture", "coding-guidelines",
             "definition-of-ready", "definition-of-done", "branching-strategy", "deployment",
             "security", "quality", "roles", "glossary", "other"}
    for key in ("manifest_version", "project_code", "overlay_version"):
        if key not in data:
            err(f"overlay-manifest.yaml: Kopfschlüssel {key} fehlt")
    seen = set()
    for doc in data.get("documents", []) or []:
        did = doc.get("id", "?")
        if did in seen:
            err(f"overlay-manifest.yaml: doppelte id {did}")
        seen.add(did)
        for key in ("id", "type", "title", "path", "context_class", "status", "load", "approved_by"):
            if key not in doc:
                err(f"overlay-manifest.yaml {did}: Feld {key} fehlt")
        if doc.get("type") not in types:
            err(f"overlay-manifest.yaml {did}: type '{doc.get('type')}' unbekannt")
        if doc.get("context_class") not in ("K1", "K2"):
            err(f"overlay-manifest.yaml {did}: context_class muss K1 oder K2 sein (K3 wird nicht registriert)")
        if doc.get("status") not in ("entwurf", "aktuell", "veraltet"):
            err(f"overlay-manifest.yaml {did}: status unbekannt")
        if doc.get("load") not in ("summary", "on-demand", "rule", "never"):
            err(f"overlay-manifest.yaml {did}: load unbekannt")
        if doc.get("load") == "rule" and not doc.get("rule_file"):
            err(f"overlay-manifest.yaml {did}: load rule ohne rule_file")
        if doc.get("load") == "summary" and doc.get("context_class") == "K2":
            err(f"overlay-manifest.yaml {did}: summary-Laden nur für K1 zulässig")
        # Der registrierte Traeger existiert (CR-2026-139, D-360). Bis 1.5.0 pruefte
        # diese Pruefung Schluessel und Aufzaehlungswerte, aber nicht, ob unter `path`
        # etwas liegt - ein Register, das auf nichts zeigt, bestand. Ein Eintrag, dessen
        # Pfad noch einen Ausfuellschlitz traegt, ist ein Beispiel der Vorlage und kein
        # Traeger; er bleibt aussen vor, und mit ihm seine Regeldatei.
        pfad = str(doc.get("path") or "")
        if pfad and "<" not in pfad:
            if not os.path.exists(os.path.join(root, *pfad.split("/"))):
                err(f"overlay-manifest.yaml {did}: path '{pfad}' existiert nicht. Ein "
                    f"registriertes Dokument, das nicht da ist, sieht im Register aus wie "
                    f"eines, das der KI-Client lesen darf (D-360)")
            regel = str(doc.get("rule_file") or "")
            if doc.get("load") == "rule" and regel and "<" not in regel \
                    and not os.path.exists(os.path.join(root, *regel.split("/"))):
                err(f"overlay-manifest.yaml {did}: rule_file '{regel}' existiert nicht. "
                    f"Mit load rule trägt die Regeldatei die Kernaussagen des Dokuments; "
                    f"fehlt sie, wirkt das Dokument nicht (D-360)")


SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


def _overlay_version_angaben(root: str, man: dict) -> list[tuple[str, str]]:
    """Alle Stellen, an denen ein Overlay seine Version *erklaert*, als (Datei, Wert).

    Die Version steht dreimal: im Steckbrief, im Manifest und in der Laufzeitfassung.
    Bis 0.12.0 pruefte der Validator nur, ob der Manifestschluessel vorhanden ist - die
    drei Werte konnten beliebig auseinanderlaufen (FW-VN-01, Sonden S2 und S3). Das ist
    dieselbe Luecke, die D-23 fuer den Overlay-*Status* geschlossen hat.
    """
    angaben: list[tuple[str, str]] = []
    quellen = [
        os.path.join(root, ".koolie/project-overlay", "OVERLAY.md"),
        os.path.join(root, *man["pack_runtime_dir"].split("/"), regeldatei(man, "20-project-overlay.md")),
    ]
    for path in quellen:
        if not os.path.exists(path):
            continue
        text = read(path)
        # Schraegstriche wie in den uebrigen Meldungen: Unter Windows liefert relpath
        # Backslashes, und eine gemischte Schreibweise war in D-23 bereits ein echter Fehler.
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        for m in re.finditer(r"^\|\s*Overlay-Version\s*\|\s*`?([^`|]+)", text, re.M):
            angaben.append((rel, m.group(1).strip()))
        for m in re.finditer(r"^-?\s*Overlay-Version:\s*`?([^`\n·]+)", text, re.M):
            angaben.append((rel, m.group(1).strip()))
    mpath = os.path.join(root, ".koolie/project-overlay", "overlay-manifest.yaml")
    if os.path.exists(mpath) and yaml is not None:
        try:
            data = yaml.safe_load(read(mpath)) or {}
        except yaml.YAMLError:  # type: ignore[attr-defined]
            data = {}
        if "overlay_version" in data:
            angaben.append((".koolie/project-overlay/overlay-manifest.yaml",
                            str(data["overlay_version"]).strip()))
    return angaben


def check_versions(root: str, man: dict) -> None:
    """Pruefung 13 - die Nachweiskette aus governance/RELEASE_PROCESS.md Abschnitt 8.

    Geprueft wird nicht, ob Versionsfelder *da* sind - das taten die Pruefungen 5 und 8
    schon -, sondern ob sie *stimmen*. Genau diese Unterscheidung hat FW-VN-01 als Luecke
    ausgewiesen: Eine Versionsangabe, die keiner anderen widersprechen kann, unterscheidet
    keine zwei Zeitpunkte.
    """
    # Overlay-Version: alle Ablageorte muessen denselben Wert nennen. Noch nicht
    # ausgefuellte Vorlagen (<TBD: ...>) bleiben aussen vor - sie erklaeren nichts.
    angaben = [(rel, wert) for rel, wert in _overlay_version_angaben(root, man)
               if not TBD_RE.search(wert)]
    werte = {wert for _, wert in angaben}
    if len(werte) > 1:
        stellen = "; ".join(f"{rel}: {wert}" for rel, wert in angaben)
        if gueltiges_mandat(root):
            # D-461 (K-182 (3)): Waehrend eines Mandats traegt der Client die Version in den
            # Steckbrief ein; Manifest und Laufzeitfassung zieht erst der Abgleich nach,
            # den 'mandat.py beenden' ausloest. Der Zwischenstand ist gewollt.
            warn(f"Overlay-Version während eines Mandats noch nicht abgeglichen ({stellen}). "
                 f"Das ist der gewollte Zwischenstand einer Eintragung in M6; die Person "
                 f"schließt ihn im eigenen Terminal ab: python {KERN}/mandat.py beenden "
                 f"(D-461)")
        else:
            err(f"Overlay-Version widersprüchlich angegeben ({stellen}). Steckbrief, Manifest "
                f"und Laufzeitfassung müssen denselben Wert nennen (RELEASE_PROCESS 8)")
    for rel, wert in angaben:
        if not SEMVER_RE.match(wert):
            err(f"{rel}: Overlay-Version '{wert}' ist kein Semantic Versioning "
                f"(MAJOR.MINOR.PATCH)")

    # Kompatible Framework-Version des Steckbriefs gegen die ausgelieferte Version.
    vpath = os.path.join(root, KERN, "VERSION")
    opath = os.path.join(root, ".koolie/project-overlay", "OVERLAY.md")
    if not (os.path.exists(vpath) and os.path.exists(opath)):
        return
    version = read(vpath).strip()
    if not SEMVER_RE.match(version):
        err(f"{KERN}/VERSION: '{version}' ist kein Semantic Versioning (MAJOR.MINOR.PATCH)")
        return
    m = re.search(r"^\|\s*Kompatible Framework-Version\s*\|\s*`?([^`|]+)", read(opath), re.M)
    if not m:
        return
    angabe = m.group(1).strip()
    if TBD_RE.search(angabe):
        return
    major, minor, _ = version.split(".")
    if angabe not in (version, f"{major}.{minor}.x"):
        err(f".koolie/project-overlay/OVERLAY.md: Kompatible Framework-Version '{angabe}' passt nicht "
            f"zu {KERN}/VERSION ({version}). Erwartet '{major}.{minor}.x' oder '{version}' – "
            f"nach einer Aktualisierung ist der Steckbrief nachzuziehen "
            f"(docs/ADOPTION_GUIDE.md, Abschnitt Aktualisierung)")


# Der Status steht zweimal: als Zeile im Steckbrief und als Aussage im
# Aktivierungsabschnitt. Beide Schreibweisen liest overlay_status.status_angaben; sie
# stand bis 0.32.0 hier und im Status-Hook getrennt, mit verschiedenem Verhalten (B08).


# Steckbriefzeile eines versionierten Artefakts - genau zwei Spalten. Die Verankerung
# auf das Zeilenende ist noetig: Der Aenderungsverlauf eines Overlays beginnt mit der
# Kopfzeile '| Version | Datum | Aenderung | ... |', und die ist kein Steckbrief. "(Skill)" kommt in einzelnen
# Steckbriefen vor; die Klammer gehoert zur Beschriftung, nicht zum Wert.
ARTEFAKT_VERSION_RE = re.compile(
    r"^\|\s*Version(?:\s*\([^)]*\))?\s*\|\s*`?([^`|]+?)`?\s*\|\s*$", re.M)


def check_artefakt_versionen(root: str) -> None:
    """Teil von Pruefung 13: Die Versionsfelder der Kernartefakte haben die Form
    MAJOR.MINOR.PATCH.

    Der Kopfkommentar sagte diese Pruefung seit 0.13.0 zu; tatsaechlich deckte
    check_versions nur die Overlay-Version, <CORE_DIR>/VERSION und die Steckbriefangabe
    ab. Ein Artefaktfeld '0.1' oder 'abc' lief mit 0 Fehlern durch - aufgefallen bei der
    Regressionsprobe R1 zu CR-2026-020, waehrend 62 Versionsfelder von Hand gehoben
    wurden, ohne dass irgendetwas das Ergebnis geprueft haette.

    Historische Dokumente sind ausgenommen: Ein Aenderungsverlauf listet Versionen in
    Tabellenzeilen, nicht in einem Steckbrief, und beschreibt einen vergangenen Zustand.
    """
    for path in iter_text_files(root):
        if not path.endswith(".md"):
            continue
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if not rel.startswith(KERN + "/") or rel.startswith(KERN + "/clients/"):
            continue
        if (rel.startswith(OHNE_ARTEFAKTVERSION)
                or os.path.basename(rel) in NEUTRAL_CHRONIK_BASENAMES):
            continue
        m = ARTEFAKT_VERSION_RE.search(read(path))
        if not m:
            continue
        wert = m.group(1).strip()
        if not wert or TBD_RE.search(wert):
            continue
        if not SEMVER_RE.match(wert):
            err(f"{rel}: Versionsfeld '{wert}' ist kein Semantic Versioning "
                f"(MAJOR.MINOR.PATCH). Eine Angabe, die keiner Form folgt, laesst sich "
                f"nicht vergleichen - und eine Version, die sich nicht vergleichen laesst, "
                f"unterscheidet keine zwei Zeitpunkte (D-25, FW-VN-01)")
# Die Abbildungstabellen und die Client Packs muessen beide Namen nennen.
NEUTRAL_ABBILDUNG = (
    KERN + "/docs/RUNTIME_GLOSSARY.md",
    KERN + "/docs/PLACEHOLDER_REGISTRY.md",
    KERN + "/clients/",
)
NEUTRAL_AUSNAHMEN = NEUTRAL_CHRONIK + NEUTRAL_ABBILDUNG + NEUTRAL_DOKUMENT

# --- Die Ausnahme, die bis 0.89.0 ein Verzeichnis war (D-313) ----------------------
#
# Die beiden Werkzeuge unter build/ und ihre README fuehren eigene Marker in spitzen
# Klammern - <CORE> und <VERSION> stehen dort fuer den Wert, den das Werkzeug zur
# Laufzeit einsetzt. Sie sind KEINE Framework-Platzhalter und gehoeren in kein Register.
#
# 🔴 GENAU DAS WAR BIS 0.89.0 DER GRUND, DIE DREI TRAEGER GANZ AUS iter_text_files
# HERAUSZUHALTEN - eine Begruendung fuer EINE Frage, wirksam auf ZWOELF Pruefungen.
# Was sie mitverdeckt hat, steht im Kopfkommentar von iter_text_files.
OHNE_PLATZHALTERREGISTER = (
    KERN + "/build/assemble.py",
    KERN + "/build/build-docx.py",
    KERN + "/build/README.md",
)

# Eine ANDERE Frage mit derselben Antwortliste, und deshalb eine eigene Konstante:
# Welches Dokument traegt ueberhaupt eine eigene Artefaktversion? Chronik traegt keine -
# aber docs/ROADMAP.md traegt eine und gehoert geprueft. Bis 0.57.0 teilten sich
# Pruefung 13 und Pruefung 14 eine Liste; wer sie fuer den einen Zweck erweitert, haette
# sie fuer den anderen stillschweigend mit erweitert.
OHNE_ARTEFAKTVERSION = (
    KERN + "/CHANGELOG.md",
    KERN + "/governance/change-requests/",
    KERN + "/governance/DECISION_LOG.md",
    KERN + "/tests/protocols/",
)


def neutral_ausgenommen(rel: str) -> bool:
    """Wahr, wenn dieser Traeger von der Werkzeugneutralitaet ausgenommen ist."""
    return (rel.startswith(NEUTRAL_AUSNAHMEN)
            or os.path.basename(rel) in NEUTRAL_CHRONIK_BASENAMES)


def _client_actor_names(root: str) -> list[tuple[str, str]]:
    """Kapitalisierter Produktname je Client Pack, abgeleitet aus dessen Kennung.

    Aus der Kennung, nicht aus einer gepflegten Liste: Ein neues Client Pack bringt
    seinen Namen damit selbst mit und wird ohne Aenderung an dieser Pruefung erfasst.
    """
    namen = set()
    cdir = os.path.join(root, ".koolie/core", "clients")
    if not os.path.isdir(cdir):
        return []
    for name in sorted(os.listdir(cdir)):
        mf = os.path.join(cdir, name, "manifest.json")
        if not os.path.isfile(mf):
            continue
        try:
            kennung = json.loads(read(mf)).get("client", name)
        except Exception:
            kennung = name
        teile = [w.capitalize() for w in kennung.split("-")]
        namen.add((teile[0], "-".join(teile)))
    return sorted(namen)


def check_actor_naming(root: str) -> None:
    """Pruefung 14 (D-02, D-129): Im Kern steht kein Clientname - auch nicht als Produkt.

    BIS 0.57.0 GALT EINE AUSNAHME: Der Produktname MIT ZUSATZ war zulaessig, weil er
    "ein Produkt benennt und nicht den Handelnden" (D-28). Am 2026-09-18 ist ihr
    Geltungsbereich ausgezaehlt worden (CR-2026-081): FUENFZEHN Nennungen in ZWOELF
    anweisenden Traegern - und in KEINER EINZIGEN wurde der Name blosse genannt. Jede
    trug etwas: einen Geltungsbereich ("Das Framework regelt den Einsatz von <Produkt>"),
    eine Produktaussage ("<Produkt> fordert vor jedem MCP-Aufruf eine Bestaetigung an")
    oder eine Voraussetzung ("Zugang zu <Produkt> vorhanden"). Die Ausnahme hatte in
    ihrem eigenen Geltungsbereich KEINEN EINZIGEN berechtigten Fall - Client Packs und
    Chronik sind ohnehin ausgenommen.

    WAS BLEIBT, IST DER UNTERSCHIED ZWISCHEN NENNEN UND ZUSCHREIBEN:
      * NENNEN - der Text traegt den Namen, sagt aber nichts ueber das Produkt. Dafuer
        gibt es <CLIENT_NAME>, und er loest sich auf:
        framework/runtime/root-instruction.md traegt ihn im Titel. Das ist der einzige
        angewandte Fall im ganzen Bestand - gezaehlt, nicht geschaetzt.
      * ZUSCHREIBEN - der Text sagt etwas UEBER das Produkt. Das gehoert in dessen
        Client Pack; der Kern verweist auf die Faehigkeitsmatrix.
    Ein ausgeschriebener Produktname kann beides sein, und kein Skript kann es
    unterscheiden - deshalb ist er im Kern jetzt gar nicht mehr zulaessig. Dieselbe
    Lehre wie bei <TBD...> in 0.52.0: Eine Marke mit zwei Bedeutungen taugt weder als
    Bedingung noch als Entlastung.

    GRENZE. Sie sucht den kapitalisierten Namen aus der Pack-Kennung. Eine Umschreibung
    ("das Werkzeug aus Kapitel 3") laeuft durch - dieselbe Ehrlichkeit wie bei
    Pruefung 48, die Pfade findet und keine Prosa.
    """
    namen = _client_actor_names(root)
    if not namen:
        err(f"{KERN}/clients/: kein Client Pack mit manifest.json gefunden - Pruefung 14 "
            f"leitet ihre Namen daraus ab und hat ihren Gegenstand verloren; sie bestuende "
            f"sonst leise (D-23)")
        return
    muster = re.compile(r"\b(%s)\b" % "|".join(k for k, _ in namen))
    for path in iter_text_files(root):
        if not path.endswith((".md", ".py", ".template")):
            continue
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if not rel.startswith(KERN + "/") or neutral_ausgenommen(rel):
            continue
        for i, zeile in enumerate(read(path).splitlines(), 1):
            m = muster.search(zeile)
            if not m:
                continue
            err(f"{rel}:{i}: '{m.group(1)}' nennt ein Client-Produkt; der Kern ist "
                f"werkzeugneutral (D-02, D-129). Sagt der Text etwas UEBER das Produkt, "
                f"gehoert es in dessen Client Pack und der Kern verweist auf die "
                f"Faehigkeitsmatrix; benennt er es nur, steht dort <CLIENT_NAME> - und der "
                f"loest sich nur in einer gerenderten Quelle auf")


# Ein Platzhalter, der einen Clientnamen traegt, bindet den Kern genauso an ein Produkt
# wie eine Akteursnennung - nur faellt er dort nicht auf, weil er in Grossbuchstaben
# steht. Das Register selbst ist ausgenommen; es steht seit 0.57.1 als
# Abbildungstabelle in NEUTRAL_AUSNAHMEN und braucht keine eigene Liste mehr.
PLATZHALTER_RE = re.compile(r"<([A-Z][A-Z0-9_ ]{2,80})>")


def check_placeholder_naming(root: str) -> None:
    """Teil von Pruefung 14: Kein Platzhalter des Kerns traegt einen Clientnamen.

    Der Marker 'VERIFY AGAINST CURRENT <name> DOCUMENTATION' stand acht Releases im Kern,
    obwohl die clientneutrale Form daneben im Register gefuehrt wurde. Die Akteurspruefung
    fand ihn nicht: Sie sucht den kapitalisierten Namen, der Marker schreibt ihn gross.

    Der Anlassfall ist mit 0.87.0 entfallen - beide Markerformen sind abgeschafft (D-291).
    Die Pruefung bleibt: Ihr Gegenstand ist JEDER Platzhalter des Kerns, nicht dieser eine,
    und die Sonde bringt ihren Fall selbst mit.
    """
    namen = _client_actor_names(root)
    if not namen:
        return
    gesucht = {k.upper() for k, _ in namen}
    for path in iter_text_files(root):
        if not path.endswith((".md", ".py", ".template")):
            continue
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if not rel.startswith(KERN + "/") or rel.startswith(KERN + "/clients/"):
            continue
        if neutral_ausgenommen(rel):
            continue
        for i, zeile in enumerate(read(path).splitlines(), 1):
            for m in PLATZHALTER_RE.finditer(zeile):
                # An Leerzeichen UND Unterstrichen trennen: Ein Platzhalter wie
                # 'NAME_PROJECT_DIR' bindet genauso an ein Produkt wie einer, der den
                # Namen als eigenes Wort fuehrt.
                treffer = gesucht & set(re.split(r"[ _]+", m.group(1)))
                if treffer:
                    err(f"{rel}:{i}: Der Platzhalter <{m.group(1)}> traegt den Clientnamen "
                        f"'{sorted(treffer)[0]}'. Ein Platzhalter bindet den Kern damit an ein "
                        f"Produkt (D-02); die clientneutrale Form gehoert in den Kern, die "
                        f"clientgebundene in das Client Pack")


def check_mermaid(root: str) -> None:
    mmdc = shutil.which("mmdc")
    if not mmdc:
        warn("mmdc nicht installiert – Mermaid-Syntaxprüfung übersprungen")
        return
    # Derselbe Browser und dieselbe Konfiguration wie beim Bau (K-145, D-398): Ohne sie
    # scheiterte der Renderer auf einem Arbeitsplatz ohne den Browser von Puppeteer an
    # JEDEM Block, und die Pruefung meldete Diagramme als ungueltig, die der Bau renderte.
    browser = mermaid_renderer.browserpfad()
    if browser is None:
        warn("kein Chromium-artiger Browser für den Mermaid-Renderer gefunden – "
             "Mermaid-Syntaxprüfung übersprungen (Pfad über PUPPETEER_EXECUTABLE_PATH)")
        return
    with tempfile.TemporaryDirectory() as konf:
        pptr = mermaid_renderer.puppeteer_konfiguration(
            os.path.join(konf, "puppeteer-config.json"), browser)
        _mermaid_bloecke(root, mmdc, pptr, browser)


def _mermaid_bloecke(root: str, mmdc: str, pptr: str, browser: str) -> None:
    for path in iter_text_files(root):
        if not path.endswith(".md"):
            continue
        text = read(path)
        for i, block in enumerate(MERMAID_RE.findall(text), 1):
            with tempfile.TemporaryDirectory() as td:
                src = os.path.join(td, "d.mmd")
                out = os.path.join(td, "d.svg")
                with open(src, "w", encoding="utf-8") as fh:
                    fh.write(block)
                res = subprocess.run([mmdc, "-i", src, "-o", out, "-q", "-p", pptr],
                                     capture_output=True, text=True, encoding="utf-8",
                                     errors="replace")
                if res.returncode != 0 and mermaid_renderer.ist_umgebungsfehler(res.stderr):
                    # Der Renderer ist an der Umgebung gescheitert, nicht am Block - dann
                    # scheitert er an jedem Block gleich. Eine Warnung, einmal, und keine
                    # Aussage ueber die Diagramme (K-145, D-398).
                    warn(f"Mermaid-Renderer startet den Browser nicht ({os.path.basename(browser)}) "
                         f"– Mermaid-Syntaxprüfung abgebrochen, kein Block beurteilt")
                    return
                if res.returncode != 0:
                    # Die Fehlerausgabe des Renderers zitiert den Quelltext des Blocks. Sie
                    # hier auszugeben traegt Diagramminhalt in Terminal und Protokoll - genau
                    # der Fehler, den B03 fuer die Inhaltsdiagnosen beanstandet (D-39). Der
                    # Block bleibt ueber Datei und Nummer auffindbar; wer die Meldung des
                    # Renderers braucht, ruft ihn von Hand auf.
                    err(f"{os.path.relpath(path, root)}: Mermaid-Block {i} ungültig "
                        f"(Renderer-Exitcode {res.returncode}; Fehlerausgabe nicht wiedergegeben)")



# ---------------------------------------------------------------------------
# Pruefung 48: Der werkzeugneutrale Kern nennt keinen Pfad eines Client Packs
# ---------------------------------------------------------------------------
#
# ANLASS. Gemessen am 2026-09-18 (CR-2026-080, D-128): SIEBZEHN Fundstellen in
# VIERZEHN anweisenden Traegern nannten den Dateinamen oder das Verzeichnis genau
# eines Client Packs - darunter sechs Prompt-Vorlagen und mit Abschnitt 2 von
# 08-skill-conventions.md ein NORMATIVES Kernmodul, dessen Prosa zwei Zeilen tiefer
# richtig "die Skill-Ablage der Laufzeitschicht" sagt. Die Regel dazu steht seit
# 0.31.0 in docs/RUNTIME_GLOSSARY.md, und durchgesetzt hat sie nichts.
#
# WARUM PRUEFUNG 12 SIE NICHT FAND - drei Gruende, alle nachgelesen:
#   1. Sie liest nur Token in BACKTICKS. Zehn der siebzehn standen ohne: in einem
#      Codeblock, in Prosa oder in einem HTML-Kommentar.
#   2. Sie meldet nur Pfade, die es NICHT GIBT. Im Framework-Repositorium ist genau
#      ein Pack installiert; dessen Laufzeitschicht existiert und ist damit
#      unsichtbar. Gemeldet wurde nur der jeweils ANDERE Client.
#   3. Und ihre Wurzelliste war selbst clientgebunden: LINK_ROOTS fuehrte woertlich
#      '.devin/', 'AGENTS.md' und 'AGENTS.local.md'. Die Pfade des anderen Packs
#      waren damit gar kein Kandidat - die Pruefung, die die Bindung melden sollte,
#      trug sie selbst. Dieser dritte Grund stand in keiner Fassung des Befunds; er
#      ist beim Nachzaehlen aufgefallen.
#
# UND ER HAT SICH BEIM MESSEN VERKLEINERT, nicht vergroessert. Der Verdacht war, die
# enge Wurzelliste erzeuge in einer Installation des anderen Packs eine Falschmeldung.
# Drei Zuschnitte sagen: nein. Sie deckte sich mit der zweiten engen Stelle desselben
# Blocks, OPTIONAL_RUNTIME_RE, die ebenfalls nur '.devin/' kannte - beide waren in
# DERSELBEN Richtung zu eng und haben einander gedeckt. Die Ableitung aus den
# Manifesten bleibt trotzdem: Sie schafft eine gepflegte Clientliste ab. Aber sie
# behebt keine gemessene Falschmeldung, und das gehoert hierhin und nicht weggelassen.
#
# DIE MARKEN STAMMEN AUS DEN MANIFESTEN, nicht aus einer gepflegten Liste - dieselbe
# Bauform wie _client_actor_names in Pruefung 14: Ein neues Client Pack bringt seine
# Pfade selbst mit und wird ohne Aenderung an dieser Pruefung erfasst.
#
# DREI GATTUNGEN SIND AUSGENOMMEN, und sie stehen in docs/RUNTIME_GLOSSARY.md und
# nicht nur hier - eine Ausnahme, die allein im Quelltext steht, ist keine Regel:
#   * CHRONIK berichtet einen vergangenen Stand. Ihn nachtraeglich zu glaetten,
#     zerstoert die Nachvollziehbarkeit. docs/ROADMAP.md gehoert dazu: Sie fuehrt die
#     Erhebungsergebnisse der Arbeitspakete und die Befundberichte je Release.
#   * WERKZEUGE (.py) stellen Installationen her oder pruefen sie; sie MUESSEN Pfade
#     nennen. Diese Datei ist selbst eines davon.
#   * Die ABBILDUNGSTABELLEN - Glossar, Platzhalterregister und die Client Packs -
#     muessen beide Namen nennen; dort ist der Pfad der Inhalt.
#
# EINE VIERTE AUSNAHME TRAEGT EINE FRIST. build/ haelt die Quellen des Hauptdokuments;
# es ist ueber vierzig Releases zurueck und wird mit AP11 (~0.69.0) neu gesetzt. Die
# Ausnahme faellt mit diesem Schritt, und sie steht dort in der Roadmap.
#
# EINE SPALTE STATT EINER DATEI. In tests/TEST_CATALOG.md ist die letzte Zelle einer
# Tabellenzeile der Ergebnisstatus; ein Pfad dort nennt, was ein Lauf gelesen hat, und
# gehoert zum gemessenen Client Pack (D-117). Die anweisenden Spalten derselben Zeile
# stehen unter der Regel - die Eingabe "Passe AGENTS.md an" war eine davon. Denselben
# Zuschnitt - die LETZTE Zelle - benutzt Pruefung 46 fuer den Ergebnisstatus.
#
# GRENZE. Sie findet die PFADE eines Packs, nicht seinen Produktnamen - den setzt
# Pruefung 14 durch. Beide teilen sich seit 0.57.1 EINE Ausnahmemenge
# (NEUTRAL_AUSNAHMEN); bis dahin waren es zwei, und sie waren schon auseinandergelaufen.
#
# Traeger, in denen die LETZTE Tabellenzelle ein Beleg ist und kein Anweisungstext.
P48_ERGEBNISSPALTE = (KERN + "/tests/TEST_CATALOG.md",)


def _client_pfadmarken(root: str) -> list:
    """(Pfad, Clientname) je Laufzeitartefakt jedes Client Packs, laengste zuerst.

    Quelle sind die runtime_placeholders der Manifeste - nicht eine gepflegte Liste.
    <CLIENT_NAME> traegt keinen Pfad, und <CORE_DIR> gehoert der Installation und
    keinem Client (docs/PLACEHOLDER_REGISTRY.md).

    Laengste zuerst, damit '.claude/skills' als sich selbst zaehlt und nicht als
    '.claude': Wer kurz vor lang prueft, zaehlt dieselbe Stelle zweimal.
    """
    marken: dict[str, str] = {}
    base = os.path.join(root, KERN, "clients")
    if not os.path.isdir(base):
        return []
    for name in sorted(os.listdir(base)):
        if name.startswith("_"):
            continue
        mp = os.path.join(base, name, "manifest.json")
        if not os.path.exists(mp):
            continue
        try:
            man = json.loads(read(mp))
        except json.JSONDecodeError:
            continue
        client = man.get("client", name)
        for schluessel, wert in (man.get("runtime_placeholders") or {}).items():
            if schluessel in ("<CLIENT_NAME>", "<CORE_DIR>") or not wert:
                continue
            marken.setdefault(wert, client)
    return sorted(marken.items(), key=lambda kv: (-len(kv[0]), kv[0]))


def _belegspalte(zeile: str) -> int:
    """Spaltenindex, ab dem die LETZTE Zelle einer Markdown-Tabellenzeile beginnt.

    Keine Tabellenzeile - oder eine ohne Inhalt hinter dem letzten Trenner - liefert
    die Zeilenlaenge; dann liegt kein Treffer dahinter und alles steht unter der Regel.
    """
    if not zeile.lstrip().startswith("|"):
        return len(zeile)
    trenner = [m.start() for m in ZELLTRENNER_RE.finditer(zeile)]
    if len(trenner) < 2:
        return len(zeile)
    # Die letzte Zelle liegt zwischen dem vorletzten und dem letzten Trenner.
    return trenner[-2] + 1


def check_tool_neutrality(root: str) -> None:
    """Pruefung 48 (D-02, D-128): Kein anweisender Kerntraeger nennt einen Clientpfad."""
    marken = _client_pfadmarken(root)
    if not marken:
        err(f"{KERN}/clients/: kein Client Pack mit runtime_placeholders gefunden – "
            f"Prüfung 48 leitet ihre Marken daraus ab und hat ihren Gegenstand "
            f"verloren; sie bestünde sonst leise (D-23)")
        return
    for path in iter_text_files(root):
        if not path.endswith((".md", ".template")):
            continue
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if not rel.startswith(KERN + "/"):
            continue
        if neutral_ausgenommen(rel):
            continue
        belegspalte = rel in P48_ERGEBNISSPALTE
        for i, zeile in enumerate(read(path).splitlines(), 1):
            ab = _belegspalte(zeile) if belegspalte else len(zeile)
            belegt = [False] * (len(zeile) + 1)
            for marke, client in marken:
                start = 0
                while True:
                    j = zeile.find(marke, start)
                    if j < 0:
                        break
                    start = j + 1
                    ende = j + len(marke)
                    if j >= ab or any(belegt[j:ende]):
                        continue
                    # Teil eines laengeren Namens ist kein Treffer.
                    if (j and (zeile[j - 1].isalnum() or zeile[j - 1] in "/._-")):
                        continue
                    if zeile[ende:ende + 1].isalnum() or zeile[ende:ende + 1] in "._-":
                        continue
                    for k in range(j, ende):
                        belegt[k] = True
                    err(f"{rel}:{i}: '{marke}' gehört der Laufzeitschicht des Client "
                        f"Packs '{client}'. Der Kern ist werkzeugneutral (D-02) und "
                        f"nennt den Begriff, nicht den Pfad – die Entsprechung je Pack "
                        f"steht in {KERN}/docs/RUNTIME_GLOSSARY.md (D-128)")


# --- Das Mandat, aus Sicht des Validators (D-461) ------------------------------------
# Dieselben Bedingungen wie im Schutz-Hook und in mandat.py, soweit der Validator sie
# braucht: die Datei im Git-Verzeichnis, ein Ende in der Zukunft, dasselbe Projekt.
# Pruefung 99 haelt Dateiname und Hoechstdauer in Hook und mandat.py gleich; hier steht
# nur der Dateiname, weil der Validator ein Mandat nie ausweitet, sondern nur eine
# Meldung abschwaecht.
MANDAT_DATEINAME = "koolie-mandat.json"


def gueltiges_mandat(root: str) -> bool:
    git = os.path.join(root, ".git")
    if os.path.isfile(git):
        try:
            zeile = read(git).strip()
        except OSError:
            return False
        if not zeile.startswith("gitdir:"):
            return False
        git = os.path.normpath(os.path.join(root, zeile[len("gitdir:"):].strip()))
    pfad = os.path.join(git, MANDAT_DATEINAME)
    if not os.path.isfile(pfad):
        return False
    try:
        daten = json.loads(read(pfad))
        import datetime as _dt
        bis = _dt.datetime.strptime(str(daten["bis"]), "%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, KeyError, TypeError, OSError):
        return False
    jetzt = _dt.datetime.now(_dt.timezone.utc).replace(tzinfo=None)
    projekt = os.path.normcase(os.path.realpath(str(daten.get("projekt", ""))))
    return bis > jetzt and projekt == os.path.normcase(os.path.realpath(root))

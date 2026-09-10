#!/usr/bin/env python3
"""
validate-framework.py – Strukturelle Validierung des Frameworks und eines Project Overlays.

Aufruf (im Wurzelverzeichnis des Repositorys):
    python3 leitwerk-core/tests/scripts/validate-framework.py [--strict-overlay] [--mermaid] [--root PFAD]

Prüft (statisch, ohne Devin):
  1. Pflichtdateien und -verzeichnisse
  2. Berechtigungsdatei: gültiges JSON, Kernregeln vollständig (Abgleich gegen die
     Kernquelle framework/runtime/permissions.json), keine Kernverbote in allow
  3. weitere JSON-Dateien der Laufzeitschicht (Hooks, mcp-Vorlage): gültiges JSON
  4. .devin/rules/*.md: Frontmatter (description, trigger, globs), Zeichenlimits
  5. Skills (.devin/skills/ und die Quellablagen der Packs): Pflichtdateien, Frontmatter,
     Metadatenblock, Pflichtabschnitte,
     Trigger-Regel (schreibende Skills nur user-getriggert), Beispiele und Testfälle
  6. Verbotene Inhalte (ohne erzeugte Lockdateien): Secret-Muster, E-Mail-Adressen, IP-Adressen, interne Hostnamen,
     URLs außerhalb der Quellen-Allowlist, projektspezifische Sperrbegriffe (project-overlay/forbidden-terms.txt)
  7. Platzhalter: nur registrierte Platzhalter (leitwerk-core/docs/PLACEHOLDER_REGISTRY.md)
  8. Overlay-Manifest: YAML-Schema und Aufzählungswerte
  9. --strict-overlay: keine offenen <TBD> in sicherheitsrelevanten Overlay-Feldern, Status aktiv
 10. --mermaid: Syntaxprüfung aller Mermaid-Blöcke mit mmdc (falls installiert)
 11. Codeblöcke mit vier oder mehr Backticks (brechen die Dokumentassemblierung)
 12. Querverweise (FW-KO-04): Markdown-Links und in Backticks genannte Framework-Pfade
     zeigen auf existierende Dateien oder Verzeichnisse

Exit-Code 0 = keine Fehler (Warnungen möglich), 1 = Fehler.
Status des Skripts: entwurf. Es prüft Struktur, nicht Semantik; die semantische Prüfung
(Widerspruchsfreiheit, Verhalten von Devin) erfolgt über leitwerk-core/tests/TEST_CATALOG.md.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

ERRORS: list[str] = []
WARNINGS: list[str] = []

TEXT_EXT = {".md", ".json", ".yaml", ".yml", ".txt", ".py", ".template", ".example"}
SKIP_DIRS = {".git", "build", "node_modules", "__pycache__", "target", "dist", ".venv"}
# Lockdateien sind erzeugte Abhaengigkeitsmetadaten. Sie enthalten naturgemaess fremde
# E-Mail-Adressen und Registry-Adressen und werden weder vom Framework noch vom Projekt
# redaktionell gepflegt - eine Inhaltspruefung dagegen erzeugt nur Rauschen.
SKIP_FILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "npm-shrinkwrap.json",
              "composer.lock", "Cargo.lock", "poetry.lock", "go.sum", "Gemfile.lock"}

# Clientneutral: gilt fuer jedes Client Pack. Die clientspezifischen Pflichtpfade
# (Wurzel-Anweisung, Berechtigungsdatei, Skills, Regeltexte) kommen aus dem Manifest.
REQUIRED_PATHS = [
    "README.md", "leitwerk-core/CHANGELOG.md", "leitwerk-core/VERSION", "leitwerk-core/OWNERS.md",
    "leitwerk-core/clients/README.md",
    "leitwerk-core/framework/core/00-principles.md", "leitwerk-core/framework/core/02-privacy.md", "leitwerk-core/framework/core/03-security.md",
    "leitwerk-core/framework/core/05-working-model.md", "leitwerk-core/framework/core/08-skill-conventions.md",
    "leitwerk-core/framework/core/09-risk-model.md", "leitwerk-core/framework/role-packs", "leitwerk-core/framework/tech-packs",
    "project-overlay/OVERLAY.md", "project-overlay/overlay-manifest.yaml",
    "leitwerk-core/templates/SKILL_TEMPLATE.md", "leitwerk-core/prompts",
    "leitwerk-core/checklists", "leitwerk-core/decision-trees",
    "leitwerk-core/onboarding", "leitwerk-core/examples",
    "leitwerk-core/tests/TEST_CATALOG.md", "leitwerk-core/governance/RACI.md", "leitwerk-core/governance/DECISION_LOG.md",
    "leitwerk-core/docs/PLACEHOLDER_REGISTRY.md",
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
SKILL_STATUS = {"entwurf", "pilot", "aktiv", "veraltet", "zurückgezogen"}

SECRET_PATTERNS = [
    ("privater Schlüssel", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("Cloud-Zugangsschlüssel", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
]
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
INTERNAL_HOST_RE = re.compile(r"\b[a-z0-9-]+\.(?:internal|intra|corp|lan)\b", re.I)
URL_RE = re.compile(r"https?://[^\s)>\]\"']+")
URL_ALLOWLIST = ("docs.devin.ai", "devin.ai", "cli.devin.ai", "docs.windsurf.com", "windsurf.com",
                 "example.com", "example.org", "example.invalid", "localhost")
PLACEHOLDER_RE = re.compile(r"<([A-Z][A-Z0-9_]{2,})>")
TBD_RE = re.compile(r"<TBD[:>]")
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
LINK_ROOTS = ("leitwerk-core/", ".devin/", "project-overlay/",
              "AGENTS.md", "AGENTS.local.md", "README.md")
# Zeichen, die einen Kandidaten als Glob, Platzhalter, Befehl oder Prosa ausweisen.
NOT_A_PATH = set("*<>|?\"' \t()[]{}$!,")
# Dateien mit absichtlich nicht existierenden Beispielpfaden (synthetische Beispiele,
# Vorlagen, Migrationshinweise auf frühere Stände). Markdown-Links werden auch dort
# geprüft – nur die Backtick-Heuristik ist ausgesetzt.
# Laufzeitpfade, die erst durch eine Projektentscheidung entstehen und im Framework-
# Repository berechtigt fehlen: Laufzeitfassungen aktivierter Packs (30-, 40-),
# Overlay-Regelerweiterungen (2N-) sowie Pack- und Projekt-Skills. Ein Verweis darauf
# beschreibt das Ziel einer Aktivierung, nicht eine vorhandene Datei
# (framework/role-packs/README.md Punkt 4).
OPTIONAL_RUNTIME_RE = re.compile(
    r"^\.devin/(?:rules/(?:2\d|30|40)-|skills/(?:role|tech|prj)-)")
LINK_EXCEPTIONS = (
    "leitwerk-core/docs/PLACEHOLDER_REGISTRY.md",
    "leitwerk-core/CHANGELOG.md",
    "leitwerk-core/governance/CHANGE_REQUEST_TEMPLATE.md",
    "leitwerk-core/governance/change-requests/",
    "leitwerk-core/templates/SKILL_TEMPLATE.md",
    "leitwerk-core/examples/",
    # Client Packs beschreiben die Pfade ihres Clients, nicht die der Installation.
    "leitwerk-core/clients/_template/",
    # Das Glossar bildet die Begriffe des Kerns auf die Pfade je Client ab; dort sind
    # clientfremde Pfade der Inhalt, nicht eine Altlast.
    "leitwerk-core/docs/RUNTIME_GLOSSARY.md",
    # Historische Dokumente behalten die Pfade ihres Entstehungsstands.
    "leitwerk-core/tests/protocols/",
    "leitwerk-core/governance/DECISION_LOG.md",
)
# Eine CLIENT_PACK.md nennt naturgemaess Pfade, die nur bei ihrem Client existieren.
LINK_EXCEPTION_BASENAMES = ("CLIENT_PACK.md",)


def err(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNINGS.append(msg)


def read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def iter_text_files(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            ext = os.path.splitext(fn)[1]
            if ext in TEXT_EXT or fn in ("leitwerk-core/VERSION", ".gitignore"):
                yield os.path.join(dirpath, fn)


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
    base = os.path.join(root, "leitwerk-core", "clients")
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
                # mp = <root>/<kern>/clients/<pack>/manifest.json - drei Ebenen hoch
                # liegt das Kernverzeichnis, dessen Name <CORE_DIR> ist.
                man.setdefault("runtime_placeholders", {})["<CORE_DIR>"] = os.path.basename(
                    os.path.dirname(os.path.dirname(os.path.dirname(mp))))
                treffer.append(man)
    if len(treffer) > 1:
        namen = ", ".join(m["client"] for m in treffer)
        err(f"Mehrere Laufzeitschichten gleichzeitig vorhanden ({namen}). "
            f"Ein Projekt nutzt genau ein Client Pack.")
    return treffer[0] if treffer else MANIFEST_FALLBACK


def check_required(root: str, man: dict) -> None:
    pflicht = list(REQUIRED_PATHS)
    pflicht += [man["root_instruction_file"], man["permissions_file"],
                man["skills_dir"], man["agents_dir"]]
    pflicht += [f"{man['pack_runtime_dir']}/{n}.md" for n in
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
    kern = os.path.join(root, "leitwerk-core")
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
    # Nie erlaubt, unabhaengig vom Client: Push, Merge, Rechteausweitung, Loeschen,
    # Netzzugriff. Die Werkzeugnamen unterscheiden sich je Client, die Absicht nicht.
    verboten = ("Exec(git push", "Exec(sudo", "Exec(rm -rf", "Fetch(*",
                "Bash(git push", "Bash(git merge", "Bash(sudo", "Bash(rm",
                "WebFetch", "WebSearch")
    for rule in allow:
        if rule.startswith(verboten):
            err(f"{rel}: unzulässige allow-Regel: {rule}")
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


def check_rules(root: str, man: dict) -> None:
    """Regeltexte der Laufzeitschicht.

    Zwei Bauarten, je nach Client: Mit Ladetriggern traegt jede Regeldatei ein
    Frontmatter, das ihr Ladeverhalten festlegt. Ohne Ladetrigger wirkt eine Datei
    erst, wenn die Wurzel-Anweisung sie einbindet - eine nicht eingebundene Datei
    ist dort stillschweigend wirkungslos, und genau das wird hier geprueft.
    """
    rules_rel = man["pack_runtime_dir"]
    rules_dir = os.path.join(root, *rules_rel.split("/"))
    if not os.path.isdir(rules_dir):
        return

    wurzel_rel = man["root_instruction_file"]
    wurzel_pfad = os.path.join(root, *wurzel_rel.split("/"))
    wurzel_text = read(wurzel_pfad) if os.path.exists(wurzel_pfad) else ""
    mit_triggern = man.get("has_rule_triggers", True)
    stets_geladen = len(wurzel_text)

    for fn in sorted(os.listdir(rules_dir)):
        if not fn.endswith(".md"):
            continue
        text = read(os.path.join(rules_dir, fn))
        rel = f"{rules_rel}/{fn}"

        if mit_triggern:
            if len(text) > 12000:
                err(f"{rel}: {len(text)} Zeichen (> 12.000)")
            if fn == "20-project-overlay.md" and len(text) > 6000:
                warn(f"{rel}: {len(text)} Zeichen (> 6.000, SOLL-Grenze)")
        if fn == "README.md":
            continue

        if mit_triggern:
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
        else:
            # Ohne Ladetrigger entscheidet der Import. Eine Kernregel (00-, 10-, 15-, 20-)
            # muss eingebunden sein, sonst waere sie wirkungslos.
            eingebunden = f"@{rel}" in wurzel_text
            if fn.startswith(("00-", "10-", "15-", "20-")) and not eingebunden:
                err(f"{rel}: nicht in {wurzel_rel} eingebunden (@{rel}) – die Regel wäre wirkungslos")
            if eingebunden:
                stets_geladen += len(text)
            if text.startswith("---"):
                warn(f"{rel}: YAML-Frontmatter, obwohl dieser Client keine Ladetrigger kennt "
                     f"(Frontmatter nur mit dokumentierten Feldern, K-18)")

    if not mit_triggern and stets_geladen > 40000:
        warn(f"{wurzel_rel} und die eingebundenen Regeltexte ergeben {stets_geladen} Zeichen, "
             f"die in jeder Sitzung geladen werden (Least Context)")

    if os.path.exists(wurzel_pfad) and mit_triggern and len(wurzel_text) > 12000:
        err(f"{wurzel_rel}: {len(wurzel_text)} Zeichen (> 12.000)")


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
    quelle = os.path.join(root, "leitwerk-core", "framework", "skills")
    if os.path.isdir(quelle):
        out.append((quelle, "leitwerk-core/framework/skills"))
    for kind in ("role-packs", "tech-packs"):
        base = os.path.join(root, "leitwerk-core", "framework", kind)
        if not os.path.isdir(base):
            continue
        for pack in sorted(os.listdir(base)):
            src = os.path.join(base, pack, "skills")
            if os.path.isdir(src):
                out.append((src, f"leitwerk-core/framework/{kind}/{pack}/skills"))
    return out


def check_skills(root: str, man: dict) -> None:
    ids: dict[str, str] = {}
    for skills_dir, prefix in skill_dirs(root, man):
        check_skills_in(skills_dir, prefix, ids)


def check_skills_in(skills_dir: str, prefix: str, ids: dict[str, str]) -> None:
    for name in sorted(os.listdir(skills_dir)):
        sdir = os.path.join(skills_dir, name)
        if not os.path.isdir(sdir):
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
            tools = fm.get("allowed-tools") or []
            if not tools:
                err(f"{rel}/SKILL.md: allowed-tools fehlt (minimale Werkzeugmenge angeben)")
            triggers = fm.get("triggers") or []
            writes = any(t in ("edit", "exec", "write") for t in tools)
            if writes and triggers != ["user"]:
                err(f"{rel}/SKILL.md: schreibender/ausführender Skill muss triggers: [user] haben")
            if not triggers:
                err(f"{rel}/SKILL.md: triggers fehlt")
            for key in fm:
                if key not in ("name", "description", "argument-hint", "allowed-tools", "permissions",
                               "triggers", "model", "subagent", "agent"):
                    warn(f"{rel}/SKILL.md: Frontmatter-Feld '{key}' ist nicht dokumentiert")
        for key in SKILL_META_KEYS:
            if not re.search(rf"^\|\s*{re.escape(key)}\s*\|", body, re.M):
                err(f"{rel}/SKILL.md: Metadatenzeile '{key}' fehlt")
        m = re.search(r"^\|\s*Status\s*\|\s*`?([^`|]+?)`?\s*\|", body, re.M)
        if m and m.group(1).strip() not in SKILL_STATUS:
            err(f"{rel}/SKILL.md: Status '{m.group(1).strip()}' unbekannt")
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
    path = os.path.join(root, "leitwerk-core", "docs", "PLACEHOLDER_REGISTRY.md")
    if not os.path.exists(path):
        return set()
    return set(PLACEHOLDER_RE.findall(read(path)))


def check_content(root: str) -> None:
    registry = load_placeholder_registry(root)
    forbidden_terms: list[str] = []
    ft_path = os.path.join(root, "project-overlay", "forbidden-terms.txt")
    if os.path.exists(ft_path):
        forbidden_terms = [l.strip() for l in read(ft_path).splitlines()
                           if l.strip() and not l.startswith("#")]
    unknown_placeholders: dict[str, set[str]] = {}
    for path in iter_text_files(root):
        rel = os.path.relpath(path, root)
        if rel.startswith("leitwerk-core/tests/scripts/") or rel == "project-overlay/forbidden-terms.txt":
            continue
        if os.path.basename(path) in SKIP_FILES:
            continue
        text = read(path)
        for label, pat in SECRET_PATTERNS:
            if pat.search(text):
                err(f"{rel}: Secret-Muster ({label})")
        for m in EMAIL_RE.finditer(text):
            if not m.group(0).lower().endswith(("example.com", "example.org", "example.invalid")):
                err(f"{rel}: E-Mail-Adresse gefunden ({m.group(0)})")
        for m in IP_RE.finditer(text):
            if not m.group(0).startswith(("0.", "127.", "192.0.2.", "198.51.100.", "203.0.113.")):
                err(f"{rel}: IP-Adresse gefunden ({m.group(0)})")
        for m in INTERNAL_HOST_RE.finditer(text):
            err(f"{rel}: interner Hostname gefunden ({m.group(0)})")
        for m in URL_RE.finditer(text):
            if not any(host in m.group(0) for host in URL_ALLOWLIST):
                warn(f"{rel}: URL außerhalb der Allowlist: {m.group(0)}")
        for term in forbidden_terms:
            if re.search(rf"(?i)\b{re.escape(term)}\b", text):
                err(f"{rel}: gesperrter Begriff '{term}'")
        if FENCE4_RE.search(text) and rel.startswith((".devin/", "leitwerk-core/framework/", "leitwerk-core/prompts/", "leitwerk-core/checklists/",
                                                       "leitwerk-core/decision-trees/", "leitwerk-core/onboarding/", "leitwerk-core/templates/",
                                                       "project-overlay/", "leitwerk-core/governance/", "leitwerk-core/pilot/")):
            err(f"{rel}: Codeblock mit vier oder mehr Backticks (bricht die Dokumentassemblierung)")
        if registry:
            for ph in set(PLACEHOLDER_RE.findall(text)):
                if ph not in registry and ph not in ("TBD",):
                    unknown_placeholders.setdefault(ph, set()).add(rel)
    for ph, files in sorted(unknown_placeholders.items()):
        warn(f"Platzhalter <{ph}> nicht in leitwerk-core/docs/PLACEHOLDER_REGISTRY.md (in {', '.join(sorted(files)[:3])}{'…' if len(files) > 3 else ''})")


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
    base = os.path.join(root, "leitwerk-core", "clients")
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


def _target_exists(root: str, src_rel: str, target: str) -> bool:
    """Prüft repo-relativ, relativ zur verweisenden Datei und - für Dateien innerhalb
    eines Client Packs - relativ zu dessen root-template."""
    base = os.path.basename(target)
    # Nutzerlokale Dateien (Namensbestandteil ".local.") sind per .gitignore bewusst
    # nicht versioniert - CLAUDE.local.md, .claude/settings.local.json und Ähnliches.
    # Ein Verweis darauf beschreibt eine Möglichkeit, keine vorhandene Datei.
    if ".local." in base or base.endswith(".local"):
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
    m = re.match(r"(leitwerk-core/clients/[^/]+/root-template)/", src_rel)
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
    gebunden: dict[str, list[str]] = {}
    for path in iter_text_files(root):
        if not path.endswith((".md", ".template")):
            continue
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if rel.startswith("leitwerk-core/tests/scripts/"):
            continue
        text = read(path)

        for m in MD_LINK_RE.finditer(text):
            target = _normalize_target(m.group(1))
            if target is not None and not _target_exists(root, rel, target):
                err(f"{rel}: Markdown-Link zeigt ins Leere: {m.group(1)}")

        if rel.startswith(LINK_EXCEPTIONS) or os.path.basename(rel) in LINK_EXCEPTION_BASENAMES:
            continue
        seen = set()
        for m in BACKTICK_RE.finditer(text):
            tok = m.group(1).strip()
            if not tok.startswith(LINK_ROOTS):
                continue
            target = _normalize_target(tok)
            if target is None or target in seen:
                continue
            seen.add(target)
            if OPTIONAL_RUNTIME_RE.match(target):
                continue
            if _target_exists(root, rel, target):
                continue
            # Gehoert der Pfad zur Laufzeitschicht eines anderen Client Packs, ist es
            # keine tote Referenz, sondern eine Client-Bindung im Kern (Arbeitsliste
            # fuer die Neutralisierung).
            fremd = next((c for pfx, c in fremdpfade.items()
                          if target == pfx or target.startswith(pfx.rstrip("/") + "/")), None)
            # Eine Datei im root-template eines Packs beschreibt dessen eigene
            # Laufzeitschicht - dort ist der Pfad richtig, nicht eine Altlast.
            if fremd and re.match(r"leitwerk-core/clients/[^/]+/root-template/", rel):
                continue
            if fremd:
                gebunden.setdefault(fremd, []).append(f"{rel}: {tok}")
            else:
                err(f"{rel}: Pfadangabe existiert nicht: {tok}")

    for client, stellen in sorted(gebunden.items()):
        warn(f"{len(stellen)} Pfadangaben nennen die Laufzeitschicht des Client Packs "
             f"'{client}', das hier nicht installiert ist. Im werkzeugneutralen Kern ist das "
             f"eine Client-Bindung (D-02). Erste Fundstellen: "
             + "; ".join(stellen[:3]) + ("; …" if len(stellen) > 3 else ""))


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
    path = os.path.join(root, "project-overlay", "overlay-manifest.yaml")
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


def check_strict_overlay(root: str) -> None:
    runtime = os.path.join(root, ".devin", "rules", "20-project-overlay.md")
    overlay = os.path.join(root, "project-overlay", "OVERLAY.md")
    for path in (runtime, overlay):
        if not os.path.exists(path):
            continue
        text = read(path)
        rel = os.path.relpath(path, root)
        if not re.search(r"Overlay-Status:\s*`?aktiv", text):
            err(f"{rel}: Overlay-Status ist nicht 'aktiv' (strict-overlay)")
        if path == runtime and TBD_RE.search(text):
            err(f"{rel}: enthält offene <TBD>-Werte (strict-overlay)")
        if path == overlay:
            for sec in ("## 4.", "## 5.", "## 6.", "## 13.", "## 14.", "## 15."):
                m = re.search(rf"{re.escape(sec)}.*?(?=\n## |\Z)", text, re.S)
                if m and TBD_RE.search(m.group(0)):
                    err(f"{rel}: Abschnitt {sec} enthält offene <TBD>-Werte (sicherheitsrelevant, strict-overlay)")
    cfg = os.path.join(root, ".devin", "config.json")
    if os.path.exists(cfg) and "<TBD" in read(cfg) or (os.path.exists(cfg) and PLACEHOLDER_RE.search(read(cfg))):
        err(".devin/config.json: enthält noch Platzhalter (strict-overlay)")


def check_mermaid(root: str) -> None:
    mmdc = shutil.which("mmdc")
    if not mmdc:
        warn("mmdc nicht installiert – Mermaid-Syntaxprüfung übersprungen")
        return
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
                res = subprocess.run([mmdc, "-i", src, "-o", out, "-q"], capture_output=True, text=True)
                if res.returncode != 0:
                    err(f"{os.path.relpath(path, root)}: Mermaid-Block {i} ungültig: {res.stderr.strip()[:300]}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.getcwd())
    ap.add_argument("--strict-overlay", action="store_true")
    ap.add_argument("--mermaid", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    man = detect_client(root)
    check_required(root, man)
    check_config(root, man)
    check_rules(root, man)
    check_skills(root, man)
    check_runtime_placeholders(root, man)
    check_content(root)
    check_links(root)
    check_manifest(root)
    if args.strict_overlay:
        check_strict_overlay(root)
    if args.mermaid:
        check_mermaid(root)

    for w in WARNINGS:
        print(f"WARNUNG  {w}")
    for e in ERRORS:
        print(f"FEHLER   {e}")
    print(f"\nErgebnis: {len(ERRORS)} Fehler, {len(WARNINGS)} Warnungen")
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())

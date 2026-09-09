#!/usr/bin/env python3
"""
validate-framework.py – Strukturelle Validierung des Frameworks und eines Project Overlays.

Aufruf (im Wurzelverzeichnis des Repositorys):
    python3 devin-core-framework/tests/scripts/validate-framework.py [--strict-overlay] [--mermaid] [--root PFAD]

Prüft (statisch, ohne Devin):
  1. Pflichtdateien und -verzeichnisse
  2. .devin/config.json: gültiges JSON, Kernregeln vorhanden, keine Kernverbote in allow
  3. .devin/hooks.v1.json und mcp-Vorlage: gültiges JSON
  4. .devin/rules/*.md: Frontmatter (description, trigger, globs), Zeichenlimits
  5. .devin/skills/*/: Pflichtdateien, Frontmatter, Metadatenblock, Pflichtabschnitte,
     Trigger-Regel (schreibende Skills nur user-getriggert), Beispiele und Testfälle
  6. Verbotene Inhalte: Secret-Muster, E-Mail-Adressen, IP-Adressen, interne Hostnamen,
     URLs außerhalb der Quellen-Allowlist, projektspezifische Sperrbegriffe (project-overlay/forbidden-terms.txt)
  7. Platzhalter: nur registrierte Platzhalter (devin-core-framework/docs/PLACEHOLDER_REGISTRY.md)
  8. Overlay-Manifest: YAML-Schema und Aufzählungswerte
  9. --strict-overlay: keine offenen <TBD> in sicherheitsrelevanten Overlay-Feldern, Status aktiv
 10. --mermaid: Syntaxprüfung aller Mermaid-Blöcke mit mmdc (falls installiert)
 11. Codeblöcke mit vier oder mehr Backticks (brechen die Dokumentassemblierung)

Exit-Code 0 = keine Fehler (Warnungen möglich), 1 = Fehler.
Status des Skripts: entwurf. Es prüft Struktur, nicht Semantik; die semantische Prüfung
(Widerspruchsfreiheit, Verhalten von Devin) erfolgt über devin-core-framework/tests/TEST_CATALOG.md.
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

REQUIRED_PATHS = [
    "AGENTS.md", "README.md", "devin-core-framework/CHANGELOG.md", "devin-core-framework/VERSION", "devin-core-framework/OWNERS.md",
    ".devin/config.json", ".devin/hooks.v1.json", ".devin/rules/00-framework-core.md",
    ".devin/rules/10-privacy-security.md", ".devin/rules/15-development-rules.md",
    ".devin/rules/20-project-overlay.md", ".devin/skills", ".devin/agents",
    "devin-core-framework/framework/core/00-principles.md", "devin-core-framework/framework/core/02-privacy.md", "devin-core-framework/framework/core/03-security.md",
    "devin-core-framework/framework/core/05-working-model.md", "devin-core-framework/framework/core/08-skill-conventions.md",
    "devin-core-framework/framework/core/09-risk-model.md", "devin-core-framework/framework/role-packs", "devin-core-framework/framework/tech-packs",
    "project-overlay/OVERLAY.md", "project-overlay/overlay-manifest.yaml",
    "devin-core-framework/templates/SKILL_TEMPLATE.md", "devin-core-framework/prompts",
    "devin-core-framework/checklists", "devin-core-framework/decision-trees",
    "devin-core-framework/onboarding", "devin-core-framework/examples",
    "devin-core-framework/tests/TEST_CATALOG.md", "devin-core-framework/governance/RACI.md", "devin-core-framework/governance/DECISION_LOG.md",
    "devin-core-framework/docs/PLACEHOLDER_REGISTRY.md",
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
            if ext in TEXT_EXT or fn in ("devin-core-framework/VERSION", ".gitignore"):
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


def check_required(root: str) -> None:
    for rel in REQUIRED_PATHS:
        if not os.path.exists(os.path.join(root, rel)):
            err(f"Pflichtpfad fehlt: {rel}")


def check_config(root: str) -> None:
    path = os.path.join(root, ".devin", "config.json")
    if not os.path.exists(path):
        return
    try:
        cfg = json.loads(read(path))
    except json.JSONDecodeError as exc:
        err(f".devin/config.json ist kein gültiges JSON: {exc}")
        return
    perms = cfg.get("permissions", {})
    deny = set(perms.get("deny", []))
    allow = set(perms.get("allow", []))
    must = cfg.get("_core_rules_integrity", {}).get("deny_must_contain", [])
    if not must:
        err(".devin/config.json: Block _core_rules_integrity.deny_must_contain fehlt")
    for rule in must:
        if rule not in deny:
            err(f".devin/config.json: Kernregel fehlt in deny: {rule}")
        if rule in allow:
            err(f".devin/config.json: Kernverbot steht in allow: {rule}")
    for rule in allow:
        if rule.startswith(("Exec(git push", "Exec(sudo", "Exec(rm -rf", "Fetch(*")):
            err(f".devin/config.json: unzulässige allow-Regel: {rule}")
    for name in ("hooks.v1.json", "mcp_config.json.example"):
        p = os.path.join(root, ".devin", name)
        if os.path.exists(p):
            try:
                json.loads(read(p))
            except json.JSONDecodeError as exc:
                err(f".devin/{name} ist kein gültiges JSON: {exc}")
    if os.path.exists(os.path.join(root, ".devin", "mcp_config.json")):
        try:
            mcp = json.loads(read(os.path.join(root, ".devin", "mcp_config.json")))
            blob = json.dumps(mcp).lower()
            if any(k in blob for k in ("password", "token", "secret", "apikey", "api_key")):
                err(".devin/mcp_config.json enthält Schlüsselwörter für Zugangsdaten – gehören nach mcp_config.local.json oder in einen Tresor")
        except json.JSONDecodeError as exc:
            err(f".devin/mcp_config.json ist kein gültiges JSON: {exc}")


def check_rules(root: str) -> None:
    rules_dir = os.path.join(root, ".devin", "rules")
    if not os.path.isdir(rules_dir):
        return
    for fn in sorted(os.listdir(rules_dir)):
        path = os.path.join(rules_dir, fn)
        if not fn.endswith(".md"):
            continue
        text = read(path)
        rel = f".devin/rules/{fn}"
        if len(text) > 12000:
            err(f"{rel}: {len(text)} Zeichen (> 12.000)")
        if fn == "20-project-overlay.md" and len(text) > 6000:
            warn(f"{rel}: {len(text)} Zeichen (> 6.000, SOLL-Grenze)")
        if fn == "README.md":
            continue
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
    agents_md = os.path.join(root, "AGENTS.md")
    if os.path.exists(agents_md):
        n = len(read(agents_md))
        if n > 12000:
            err(f"AGENTS.md: {n} Zeichen (> 12.000)")


def check_skills(root: str) -> None:
    skills_dir = os.path.join(root, ".devin", "skills")
    if not os.path.isdir(skills_dir):
        return
    ids: dict[str, str] = {}
    for name in sorted(os.listdir(skills_dir)):
        sdir = os.path.join(skills_dir, name)
        if not os.path.isdir(sdir):
            continue
        rel = f".devin/skills/{name}"
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
            if m.group(1) in ids:
                err(f"{rel}/SKILL.md: ID {m.group(1)} doppelt (auch in {ids[m.group(1)]})")
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
    path = os.path.join(root, "devin-core-framework", "docs", "PLACEHOLDER_REGISTRY.md")
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
        if rel.startswith("devin-core-framework/tests/scripts/") or rel == "project-overlay/forbidden-terms.txt":
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
        if FENCE4_RE.search(text) and rel.startswith((".devin/", "devin-core-framework/framework/", "devin-core-framework/prompts/", "devin-core-framework/checklists/",
                                                       "devin-core-framework/decision-trees/", "devin-core-framework/onboarding/", "devin-core-framework/templates/",
                                                       "project-overlay/", "devin-core-framework/governance/", "devin-core-framework/pilot/")):
            err(f"{rel}: Codeblock mit vier oder mehr Backticks (bricht die Dokumentassemblierung)")
        if registry:
            for ph in set(PLACEHOLDER_RE.findall(text)):
                if ph not in registry and ph not in ("TBD",):
                    unknown_placeholders.setdefault(ph, set()).add(rel)
    for ph, files in sorted(unknown_placeholders.items()):
        warn(f"Platzhalter <{ph}> nicht in devin-core-framework/docs/PLACEHOLDER_REGISTRY.md (in {', '.join(sorted(files)[:3])}{'…' if len(files) > 3 else ''})")


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

    check_required(root)
    check_config(root)
    check_rules(root)
    check_skills(root)
    check_content(root)
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

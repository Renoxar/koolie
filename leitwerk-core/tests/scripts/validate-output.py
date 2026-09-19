#!/usr/bin/env python3
"""
validate-output.py – Prüft eine Ausgabe des KI-Clients gegen das Ausgabeformat eines Skills.

Aufruf:
    python3 leitwerk-core/tests/scripts/validate-output.py --skill fw-repo-analyze [--file ausgabe.md]
    (ohne --file wird die Ausgabe von stdin gelesen)

Prüft:
  1. Pflichtabschnitte: alle '##'/'###'-Überschriften aus dem Markdown-Gerüst in Abschnitt 5
     ("## 5. Ausgabeformat") der SKILL.md des Skills kommen in der Ausgabe vor
     (Vergleich ohne Platzhalterteile in spitzen/geschweiften Klammern).
  2. Ergebnisbericht: der Abschnitt "Ergebnisbericht" ist enthalten, sofern die SKILL.md
     ihn im letzten Arbeitsschritt fordert.
  3. Verbotene Inhalte: Secret-Muster, E-Mail-Adressen (außer example.*), IP-Adressen,
     interne Hostnamen – gleiche Muster wie validate-framework.py.
  4. Belegpflicht (heuristisch): mindestens eine Fundstelle der Form pfad:zeile oder ein
     ausgewiesenes "nicht gefunden mit Suchmuster", sofern der Skill Fundstellen fordert.

Exit-Code 0 = bestanden, 1 = Befunde. Status: entwurf; die inhaltliche Bewertung
(erwartetes/unzulässiges Verhalten laut TESTS.md) bleibt eine menschliche Prüfung.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys

SECRET_PATTERNS = [
    ("privater Schluessel", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("Cloud-Zugangsschluessel", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("Zugangsdaten-Zuweisung", re.compile(r"(?i)\b(password|passwd|secret|api[_-]?key|token)\b\s*[:=]\s*['\"]?[^\s'\"]{8,}")),
]
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
INTERNAL_HOST_RE = re.compile(r"\b[a-z0-9-]+\.(?:internal|intra|corp|lan)\b", re.I)
FINDING_RE = re.compile(r"[\w./-]+\.[A-Za-z0-9]+:\d+|nicht gefunden mit Suchmuster", re.I)


def _kernverzeichnis(root: str) -> str | None:
    """Das Kernverzeichnis des Baums - der Name ist nicht geraten, sondern gesucht."""
    for name in sorted(os.listdir(root)):
        if os.path.isfile(os.path.join(root, name, "clients", "_template", "manifest.json")) \
                or os.path.isdir(os.path.join(root, name, "clients")):
            if os.path.isdir(os.path.join(root, name, "framework")):
                return os.path.join(root, name)
    return None


def skill_pfad(root: str, skill: str):
    """Die SKILL.md des Skills - aus dem MANIFEST des installierten Packs.

    Marken, Wurzeln und Ablagen gehoeren abgeleitet, nicht gepflegt (D-128, D-142). Bis
    0.67.1 stand hier `.devin/skills/...` fest verdrahtet: In einem Messbaum mit dem Pack
    `claude-code` fand dieses Werkzeug den Skill nicht - und es ist das zweite Pruefmittel
    von drei Zellen der Testblaetter. Gemessen am 2026-09-19 im Aufbau zu Buendel 1.

    Reihenfolge: installiertes Pack (Laufzeitablage im Baum vorhanden), sonst die QUELLE
    des Kerns. Zwei installierte Packs sind ein unvollstaendiger Packwechsel und werden
    gemeldet, nicht geraten.
    """
    kern = _kernverzeichnis(root)
    gefunden = []
    if kern:
        packs = os.path.join(kern, "clients")
        for name in sorted(os.listdir(packs)) if os.path.isdir(packs) else []:
            if name.startswith("_"):
                continue
            manifest = os.path.join(packs, name, "manifest.json")
            if not os.path.isfile(manifest):
                continue
            with io.open(manifest, encoding="utf-8") as fh:
                man = json.load(fh)
            laufzeit = man.get("runtime_dir")
            ablage = (man.get("runtime_placeholders") or {}).get("<SKILLS_DIR>")
            if not laufzeit or not ablage:
                continue
            if os.path.isdir(os.path.join(root, laufzeit)):
                gefunden.append((name, ablage.replace("/", os.sep)))
    if len(gefunden) > 1:
        namen = ", ".join(n for n, _ in gefunden)
        return None, (f"zwei Laufzeitablagen im Baum ({namen}) - ein Packwechsel ist "
                      f"unvollstaendig; ohne eindeutiges Pack wird nicht geraten")
    if gefunden:
        pfad = os.path.join(root, gefunden[0][1], skill, "SKILL.md")
        if os.path.exists(pfad):
            return pfad, None
        return None, (f"Skill nicht gefunden: {pfad} (Pack {gefunden[0][0]}, aus dem "
                      f"Manifest aufgeloest)")
    if kern:
        quelle = os.path.join(kern, "framework", "skills", skill, "SKILL.md")
        if os.path.exists(quelle):
            return quelle, None
        return None, f"kein Client Pack installiert, und die Quelle fehlt: {quelle}"
    return None, (f"weder ein installiertes Client Pack noch ein Kernverzeichnis unter "
                  f"{root} - ohne beides gibt es keine SKILL.md zum Vergleich")


def normalize_heading(h: str) -> str:
    h = re.sub(r"<[^>]*>", "", h)
    h = re.sub(r"\{[^}]*\}", "", h)
    h = re.sub(r"[^A-Za-zÄÖÜäöüß ]", " ", h)
    return " ".join(h.split()).strip().lower()


def extract_required_headings(skill_md: str) -> list[str]:
    m = re.search(r"^## 5\. Ausgabeformat.*?```(?:markdown)?\n(.*?)```", skill_md, re.S | re.M)
    if not m:
        return []
    headings = re.findall(r"^#{2,3}\s+(.+)$", m.group(1), re.M)
    return [normalize_heading(h) for h in headings if normalize_heading(h)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", required=True)
    ap.add_argument("--file")
    ap.add_argument("--root", default=os.getcwd())
    args = ap.parse_args()

    skill_path, grund = skill_pfad(args.root, args.skill)
    if skill_path is None:
        print(f"FEHLER   {grund}")
        return 1
    skill_md = open(skill_path, encoding="utf-8").read()
    output = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
    norm_output_headings = {normalize_heading(h) for h in re.findall(r"^#{2,3}\s+(.+)$", output, re.M)}
    findings: list[str] = []

    for req in extract_required_headings(skill_md):
        if not any(req in got or got in req for got in norm_output_headings if got):
            findings.append(f"Pflichtabschnitt fehlt: '{req}'")

    if "Ergebnisbericht" in skill_md and "Ergebnisbericht" not in output:
        findings.append("Abschnitt 'Ergebnisbericht' fehlt")

    for label, pat in SECRET_PATTERNS:
        if pat.search(output):
            findings.append(f"Verbotenes Muster in der Ausgabe: {label}")
    for m in EMAIL_RE.finditer(output):
        if not m.group(0).lower().endswith(("example.com", "example.org", "example.invalid")):
            findings.append(f"E-Mail-Adresse in der Ausgabe: {m.group(0)}")
    for m in IP_RE.finditer(output):
        if not m.group(0).startswith(("0.", "127.", "192.0.2.", "198.51.100.", "203.0.113.")):
            findings.append(f"IP-Adresse in der Ausgabe: {m.group(0)}")
    if INTERNAL_HOST_RE.search(output):
        findings.append("Interner Hostname in der Ausgabe")

    if "Fundstelle" in skill_md and not FINDING_RE.search(output):
        findings.append("Keine Fundstelle (pfad:zeile) und kein ausgewiesenes 'nicht gefunden mit Suchmuster' erkennbar")

    for f in findings:
        print(f"BEFUND   {f}")
    print(f"\nErgebnis: {'bestanden' if not findings else f'{len(findings)} Befunde'} (Skill {args.skill})")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
install.py - Legt die Wurzeldateien des Devin Desktop Frameworks in einem Projekt an.

Hintergrund: Zwei Dinge muessen im Wurzelverzeichnis des Projekts liegen, weil Devin
sie nur dort findet - AGENTS.md (Root-Regeldatei) und .devin/ (Laufzeitschicht mit
rules/, skills/, agents/, config.json, hooks.v1.json). Alles Uebrige des Frameworks
liegt gebuendelt in devin-core-framework/ und wird nur kopiert, nicht installiert.

Dieses Skript loest das auf: Es kopiert die Wurzelbestandteile aus
devin-core-framework/root-template/ an ihren Platz und unterscheidet dabei sauber
zwischen Core (wird bei einem Update ueberschrieben) und Projektbestandteilen
(werden nie ueberschrieben).

Aufruf (aus dem Wurzelverzeichnis des Projekts):

    python devin-core-framework/install.py              # Erstinstallation
    python devin-core-framework/install.py --update      # Core aktualisieren
    python devin-core-framework/install.py --check       # nur pruefen, nichts schreiben
    python devin-core-framework/install.py --dry-run     # zeigen, was passieren wuerde

Exit-Code 0 = in Ordnung, 1 = Abweichungen gefunden (bei --check) oder Fehler.
"""
from __future__ import annotations

import argparse
import filecmp
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "root-template")

# ---------------------------------------------------------------------------
# Core: gehoert zum Framework, wird bei --update ueberschrieben.
# Aenderungswuensche laufen als Aenderungsantrag an den Framework Owner
# (devin-core-framework/governance/FEEDBACK_PROCESS.md), nicht als lokale Bearbeitung.
# ---------------------------------------------------------------------------
CORE_PATHS = [
    "AGENTS.md",
    "AGENTS.local.md.example",
    ".devin/README.md",
    ".devin/hooks.v1.json",
    ".devin/mcp_config.json.example",
    ".devin/agents",
    ".devin/rules/README.md",
    ".devin/rules/00-framework-core.md",
    ".devin/rules/10-privacy-security.md",
    ".devin/rules/15-development-rules.md",
    ".devin/rules/21-overlay-TEMPLATE.md.template",
    ".devin/rules/40-tech-TEMPLATE.md.template",
]
# Alle fw-*-Skills sind Core; sie werden zur Laufzeit ermittelt, damit neue Skills
# eines Releases ohne Anpassung dieses Skripts mitkommen.
CORE_SKILL_PREFIX = "fw-"

# ---------------------------------------------------------------------------
# Saat: wird nur bei der Erstinstallation angelegt. Danach gehoert es dem Projekt
# und wird nie ueberschrieben - hier stehen die projektspezifischen Werte.
# ---------------------------------------------------------------------------
SEED_PATHS = [
    ".devin/config.json",
    ".devin/rules/20-project-overlay.md",
    "project-overlay",
]
# Laufzeitfassungen von Packs (30-role-*, 40-tech-*) stehen absichtlich NICHT hier:
# Ein Pack wird im Overlay aktiviert (framework/role-packs/README.md Punkt 4), nicht durch
# die Installation. Wer ein Pack aktiviert hat, bekommt seine Bestandteile ueber
# activated_pack_relpaths() aktualisiert.

# Wird von install.py nie angefasst, auch nicht geloescht: projekteigene Erweiterungen.
PROJECT_OWNED_HINT = [
    ".devin/rules/2N-overlay-<name>.md   (Overlay-Regelerweiterungen)",
    ".devin/rules/40-tech-<name>.md      (Packs ohne Quelle im Kern)",
    ".devin/skills/prj-*/                (projektspezifische Skills)",
    "project-overlay/tech-packs/**       (projekteigene Packs)",
    "project-overlay/**                  (das gesamte Overlay)",
]


class Report:
    def __init__(self) -> None:
        self.created: list[str] = []
        self.updated: list[str] = []
        self.unchanged: list[str] = []
        self.kept: list[str] = []
        self.drifted: list[str] = []
        self.missing: list[str] = []


def sha(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def iter_files(base: str, rel: str):
    """Liefert alle Dateien unter rel (Datei oder Verzeichnis), relativ zu base."""
    full = os.path.join(base, rel)
    if os.path.isfile(full):
        yield rel
    elif os.path.isdir(full):
        for dirpath, dirnames, filenames in os.walk(full):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for fn in sorted(filenames):
                yield os.path.relpath(os.path.join(dirpath, fn), base).replace(os.sep, "/")


def core_relpaths() -> list[str]:
    """Alle Core-Dateien des Templates, inklusive der fw-*-Skills."""
    out: list[str] = []
    for rel in CORE_PATHS:
        out.extend(iter_files(TEMPLATE, rel))
    skills = os.path.join(TEMPLATE, ".devin", "skills")
    if os.path.isdir(skills):
        for name in sorted(os.listdir(skills)):
            if name.startswith(CORE_SKILL_PREFIX):
                out.extend(iter_files(TEMPLATE, f".devin/skills/{name}"))
    return out


def activated_pack_relpaths(root: str) -> list[str]:
    """Bestandteile von Packs, die dieses Projekt aktiviert hat.

    Ein Pack wird aktiviert, indem seine Skills nach .devin/skills/ und seine Laufzeitfassung
    nach .devin/rules/ kopiert werden. Ob ein Pack aktiv ist, entscheidet das Projekt
    (Overlay Abschnitt 1) - was in einem aktivierten Pack-Skill steht, ist dagegen
    Framework-Inhalt und gehoert damit zum Core-Aktualisierungsumfang. Ohne diese Funktion
    behielte ein Projekt seine Kopie aus dem Release der Aktivierung, stillschweigend und
    ohne Hinweis.

    Nur was in einer Pack-Quellablage dieses Kerns eine Entsprechung hat, wird erfasst.
    Projekteigene Packs (etwa unter project-overlay/tech-packs/) bleiben unberuehrt.
    """
    out: list[str] = []
    for kind in ("role-packs", "tech-packs"):
        base = os.path.join(HERE, "framework", kind)
        if not os.path.isdir(base):
            continue
        for pack in sorted(os.listdir(base)):
            src_skills = os.path.join(base, pack, "skills")
            if os.path.isdir(src_skills):
                for skill in sorted(os.listdir(src_skills)):
                    if not os.path.isdir(os.path.join(src_skills, skill)):
                        continue
                    # Nur wenn im Ziel aktiviert
                    if not os.path.isdir(os.path.join(root, ".devin", "skills", skill)):
                        continue
                    for dirpath, dirnames, filenames in os.walk(os.path.join(src_skills, skill)):
                        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
                        for fn in sorted(filenames):
                            src = os.path.join(dirpath, fn)
                            innen = os.path.relpath(src, os.path.join(src_skills, skill))
                            out.append((os.path.relpath(src, HERE).replace(os.sep, "/"),
                                        f".devin/skills/{skill}/{innen}".replace(os.sep, "/")))
            src_runtime = os.path.join(base, pack, "runtime")
            if os.path.isdir(src_runtime):
                for fn in sorted(os.listdir(src_runtime)):
                    if not fn.endswith(".md"):
                        continue
                    # Nur wenn im Ziel aktiviert
                    if not os.path.exists(os.path.join(root, ".devin", "rules", fn)):
                        continue
                    src = os.path.join(src_runtime, fn)
                    out.append((os.path.relpath(src, HERE).replace(os.sep, "/"),
                                f".devin/rules/{fn}"))
    return out


def seed_relpaths() -> list[str]:
    out: list[str] = []
    for rel in SEED_PATHS:
        out.extend(iter_files(TEMPLATE, rel))
    return out


def copy_file(src: str, dst: str, dry: bool) -> None:
    if dry:
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)


def run(root: str, mode: str, dry: bool) -> Report:
    rep = Report()

    for rel in core_relpaths():
        src = os.path.join(TEMPLATE, rel)
        dst = os.path.join(root, rel)
        if not os.path.exists(dst):
            if mode == "check":
                rep.missing.append(rel)
            else:
                copy_file(src, dst, dry)
                rep.created.append(rel)
            continue
        if filecmp.cmp(src, dst, shallow=False):
            rep.unchanged.append(rel)
        elif mode == "check":
            rep.drifted.append(rel)
        elif mode in ("install", "update"):
            copy_file(src, dst, dry)
            rep.updated.append(rel)

    # Aktivierte Pack-Bestandteile: Quelle liegt im Pack, Ziel in der Laufzeitschicht.
    # Werden nie neu angelegt - die Aktivierung bleibt Projektentscheidung -, aber
    # aktualisiert, sobald sie vorhanden sind.
    for src_rel, dst_rel in activated_pack_relpaths(root):
        src = os.path.join(HERE, src_rel)
        dst = os.path.join(root, dst_rel)
        if not os.path.exists(dst):
            continue
        if filecmp.cmp(src, dst, shallow=False):
            rep.unchanged.append(dst_rel)
        elif mode == "check":
            rep.drifted.append(f"{dst_rel}  (Pack-Quelle: {src_rel})")
        else:
            copy_file(src, dst, dry)
            rep.updated.append(f"{dst_rel}  (aus dem Pack aktualisiert)")

    for rel in seed_relpaths():
        src = os.path.join(TEMPLATE, rel)
        dst = os.path.join(root, rel)
        if os.path.exists(dst):
            rep.kept.append(rel)
        elif mode == "check":
            rep.missing.append(rel)
        else:
            copy_file(src, dst, dry)
            rep.created.append(rel)

    return rep


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Installiert die Wurzeldateien des Devin Desktop Frameworks in ein Projekt.")
    ap.add_argument("--root", default=os.getcwd(),
                    help="Wurzelverzeichnis des Projekts (Standard: aktuelles Verzeichnis)")
    ap.add_argument("--update", action="store_true",
                    help="Core-Dateien auf den Stand dieses Releases bringen; Projektdateien bleiben unberuehrt")
    ap.add_argument("--check", action="store_true",
                    help="Nur pruefen: meldet fehlende und abweichende Core-Dateien, schreibt nichts")
    ap.add_argument("--dry-run", action="store_true",
                    help="Zeigen, was geschehen wuerde, ohne zu schreiben")
    args = ap.parse_args()

    if not os.path.isdir(TEMPLATE):
        print(f"FEHLER: Vorlagenverzeichnis fehlt: {TEMPLATE}", file=sys.stderr)
        return 1

    root = os.path.abspath(args.root)
    if os.path.abspath(HERE) == root:
        print("FEHLER: --root zeigt auf devin-core-framework/ selbst. Gemeint ist das "
              "Wurzelverzeichnis des Projekts, also eine Ebene darueber.", file=sys.stderr)
        return 1

    mode = "check" if args.check else ("update" if args.update else "install")
    version_file = os.path.join(HERE, "VERSION")
    version = open(version_file, encoding="utf-8").read().strip() if os.path.exists(version_file) else "unbekannt"

    print(f"Devin Desktop Framework {version}")
    print(f"Vorlage: {os.path.relpath(TEMPLATE, root) if root in TEMPLATE else TEMPLATE}")
    print(f"Ziel:    {root}")
    print(f"Modus:   {mode}{'  (dry-run, es wird nichts geschrieben)' if args.dry_run else ''}")
    print()

    rep = run(root, mode, args.dry_run)

    def block(title: str, items: list[str], limit: int = 12) -> None:
        if not items:
            return
        print(f"{title} ({len(items)}):")
        for rel in items[:limit]:
            print(f"  {rel}")
        if len(items) > limit:
            print(f"  ... und {len(items) - limit} weitere")
        print()

    if mode == "check":
        block("Core-Dateien fehlen", rep.missing)
        block("Core-Dateien weichen von der Vorlage ab", rep.drifted)
        print(f"Unveraendert: {len(rep.unchanged)} | Projektdateien vorhanden: {len(rep.kept)}")
        if rep.drifted:
            print()
            print("Abweichende Core-Dateien bedeuten: Es wurde an der falschen Stelle bearbeitet.")
            print("Core-Aenderungen gehoeren in devin-core-framework/root-template/ und laufen")
            print("als Aenderungsantrag (devin-core-framework/governance/FEEDBACK_PROCESS.md).")
            print("Mit --update wird der Release-Stand wiederhergestellt; lokale Aenderungen gehen dabei verloren.")
        if rep.missing or rep.drifted:
            return 1
        print("\nErgebnis: Core ist auf dem Stand des Releases.")
        return 0

    block("Angelegt", rep.created)
    block("Core aktualisiert", rep.updated)
    if rep.kept:
        print(f"Projektdateien unberuehrt gelassen: {len(rep.kept)}")
        for rel in rep.kept[:6]:
            print(f"  {rel}")
        if len(rep.kept) > 6:
            print(f"  ... und {len(rep.kept) - 6} weitere")
        print()

    print(f"Zusammenfassung: {len(rep.created)} angelegt, {len(rep.updated)} aktualisiert, "
          f"{len(rep.unchanged)} unveraendert, {len(rep.kept)} Projektdateien behalten.")

    if mode == "install" and rep.created:
        print()
        print("Naechste Schritte:")
        print("  1. project-overlay/OVERLAY.md ausfuellen (Platzhalter und <TBD>-Felder).")
        print("  2. Werte in .devin/config.json eintragen - die Kernregeln unter")
        print("     _core_rules_integrity nicht entfernen.")
        print("  3. project-overlay/forbidden-terms.txt mit den realen Projekt- und")
        print("     Kundennamen fuellen (bleibt projektlokal).")
        print("  4. devin-core-framework/checklists/10-project-adoption.md abarbeiten.")
        print("  5. python devin-core-framework/tests/scripts/validate-framework.py --strict-overlay")
    if mode == "update":
        print()
        print("Hinweis: .devin/config.json wurde nicht angefasst, weil sie Projektwerte enthaelt.")
        print("Pruefe nach einem Release-Wechsel, ob die Kernregeln noch vollstaendig sind:")
        print("  python devin-core-framework/tests/scripts/validate-framework.py --strict-overlay")

    print()
    print("Diese Pfade gehoeren dem Projekt und werden von install.py nie geschrieben:")
    for hint in PROJECT_OWNED_HINT:
        print(f"  {hint}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

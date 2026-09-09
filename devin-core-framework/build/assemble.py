#!/usr/bin/env python3
"""Assembliert das Hauptdokument aus devin-core-framework/build/doc/*.md und Repository-Artefakten.

Direktiven in den Kapiteldateien:
  {{EMBED:relpfad}}            -> Datei als Markdown-Codeblock (4 Backticks, Sprache markdown)
  {{EMBED:relpfad:lang}}       -> wie oben mit Sprachangabe (json, yaml, python, text)
  {{EMBED-RAW:relpfad:shift}}  -> Datei als gerenderten Inhalt einfuegen, Ueberschriften um <shift> Ebenen
                                  verschoben; YAML-Frontmatter wird als Hinweisblock dargestellt
Ausgabe: devin-core-framework/build/out/hauptdokument.md
"""
from __future__ import annotations

import os
import re
import sys

# CORE = devin-core-framework/ (dieses Skript liegt in CORE/build/).
# REPO = Wurzelverzeichnis des Projekts; EMBED-Pfade sind dazu relativ,
# weil AGENTS.md, .devin/ und project-overlay/ dort liegen.
CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(CORE)
DOC = os.path.join(CORE, "build", "doc")
OUT = os.path.join(CORE, "build", "out")
EMBED_RE = re.compile(r"^\{\{(EMBED|EMBED-RAW):([^:}]+)(?::([^}]+))?\}\}\s*$", re.M)


def shift_headings(text: str, shift: int) -> str:
    def repl(m):
        return "#" * min(6, len(m.group(1)) + shift) + m.group(2)
    out_lines = []
    in_fence = False
    for line in text.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if not in_fence:
            line = re.sub(r"^(#{1,6})(\s)", repl, line)
        out_lines.append(line)
    return "\n".join(out_lines)


def strip_frontmatter(text: str):
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1].strip()
            return fm, parts[2].lstrip("\n")
    return None, text


def process(text: str) -> str:
    def repl(m):
        kind, rel, arg = m.group(1), m.group(2).strip(), (m.group(3) or "").strip()
        path = os.path.join(REPO, rel)
        if not os.path.exists(path):
            print(f"FEHLER: eingebettete Datei fehlt: {rel}", file=sys.stderr)
            sys.exit(1)
        content = open(path, encoding="utf-8").read().rstrip("\n")
        if kind == "EMBED":
            lang = arg or "markdown"
            if "````" in content:
                print(f"FEHLER: {rel} enthaelt 4 Backticks", file=sys.stderr)
                sys.exit(1)
            return f"**Datei:** `{rel}`\n\n````{lang}\n{content}\n````\n"
        shift = int(arg or "1")
        fm, body = strip_frontmatter(content)
        prefix = f"> **Datei:** `{rel}`"
        if fm:
            fm_compact = "; ".join(l.strip() for l in fm.splitlines() if l.strip())
            prefix += f" · **Frontmatter (Laufzeit):** `{fm_compact}`"
        return prefix + "\n\n" + shift_headings(body, shift) + "\n"
    return EMBED_RE.sub(repl, text)


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    parts = []
    for fn in sorted(os.listdir(DOC)):
        if fn.endswith(".md"):
            parts.append(process(open(os.path.join(DOC, fn), encoding="utf-8").read().rstrip("\n")))
    result = "\n\n".join(parts) + "\n"
    out_path = os.path.join(OUT, "hauptdokument.md")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(result)
    print(f"geschrieben: {out_path} ({len(result)} Zeichen, {result.count(chr(10))} Zeilen)")


if __name__ == "__main__":
    main()

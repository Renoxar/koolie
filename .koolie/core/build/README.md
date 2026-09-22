# Dokument-Build (Hauptdokument)

Das Hauptdokument („Framework für den professionellen Einsatz von Devin Desktop", 31 Kapitel plus Abschluss) wird aus den Kapitelquellen in `doc/` und den Artefakten des Repositorys assembliert – die Artefakte existieren also genau einmal (Single Source of Truth im Repository) und werden in das Dokument eingebettet.

## Erzeugung

```bash
python3 build/assemble.py      # -> build/out/hauptdokument.md (Markdown-Fassung)
python3 build/build-docx.py    # -> build/out/Koolie_v<VERSION>.docx
                               #    (rendert die Mermaid-Diagramme als PNG und konvertiert mit pandoc)
```

Voraussetzungen für die Word-Fassung: `pandoc`, `mmdc` (Mermaid CLI) mit Chromium (Pfad in `build-docx.py` / Puppeteer-Konfiguration anpassen). Das A4-Referenzdokument `build/ref-a4.docx` wird mitgeliefert; das Inhaltsverzeichnis der Word-Datei ist ein Word-Feld und wird beim ersten Öffnen über „Felder aktualisieren" gefüllt.

## Direktiven in den Kapitelquellen (`doc/*.md`)

- `{{EMBED:pfad}}` beziehungsweise `{{EMBED:pfad:sprache}}` – Datei als Codeblock einbetten (Agentenanweisungen, Templates, Prompts, Konfigurationen).
- `{{EMBED-RAW:pfad:verschiebung}}` – Datei als gerenderten Inhalt einbetten; Überschriften werden um die angegebene Ebenenzahl verschoben, YAML-Frontmatter wird als Hinweiszeile dargestellt.

## Pflege

Kapiteltexte in `doc/` folgen dem Framework-Release-Prozess (Checkliste FW-CL-11 prüft die Konsistenz zwischen Dokument und Repository). `out/` ist Build-Ausgabe und nicht versioniert (`.gitignore`); `BRIEF_*.md` sind Arbeitsunterlagen der Erstellung und nicht Teil des Dokuments.

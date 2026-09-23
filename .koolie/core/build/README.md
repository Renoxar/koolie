# Dokument-Build (Hauptdokument)

Das Hauptdokument wird aus den **34 Kapitelquellen** in `doc/` und den Artefakten des Repositorys assembliert – die Artefakte existieren also genau einmal (Single Source of Truth im Repository) und werden in das Dokument eingebettet. **Seinen Titel trägt es selbst**, in `doc/00-kopf.md`; er steht nicht hier und nicht im Erzeuger. Bis 0.89.0 stand er an beiden Stellen, nannte einen Clientnamen und war seit der Umbenennung überholt (D-313, D-314).

## Erzeugung

Beide Werkzeuge werden aus der **Projektwurzel** aufgerufen und leiten ihre Pfade selbst ab:

```bash
python .koolie/core/build/assemble.py                    # -> build/out/hauptdokument.md
python .koolie/core/build/assemble.py --client claude-code
python .koolie/core/build/build-docx.py                  # -> build/out/Koolie_vX.Y.Z.docx
```

`build-docx.py` rendert die acht Mermaid-Diagramme als PNG und konvertiert mit `pandoc`; die normative Textbeschreibung neben jedem Diagramm bleibt erhalten.

## Voraussetzungen der Word-Fassung

| Werkzeug | Bezug | Prüfung |
|---|---|---|
| `pandoc` | Paketverwalter des Arbeitsplatzes (`winget install JohnMacFarlane.Pandoc`, `apt install pandoc`, `brew install pandoc`) | `build-docx.py` hält **vor** dem ersten Schritt an und nennt beide fehlenden Namen auf einmal |
| `mmdc` (Mermaid CLI) | `npm install -g @mermaid-js/mermaid-cli` | dieselbe Vorbedingungsprüfung |
| ein Chromium-artiger Browser | wird selbst gesucht: `PUPPETEER_EXECUTABLE_PATH`, dann Edge, dann Chrome, dann die üblichen Linux-Pfade | auf einem Windows-Arbeitsplatz ist Edge immer vorhanden – ein eigener Chromium-Download ist unnötig |

Das A4-Referenzdokument `ref-a4.docx` wird mitgeliefert; das Inhaltsverzeichnis der Word-Datei ist ein Word-Feld und wird beim ersten Öffnen über „Felder aktualisieren" gefüllt.

## Direktiven in den Kapitelquellen (`doc/*.md`)

- `{{EMBED:pfad}}` beziehungsweise `{{EMBED:pfad:sprache}}` – Datei als Codeblock einbetten (Agentenanweisungen, Templates, Prompts, Konfigurationen).
- `{{EMBED-RAW:pfad:verschiebung}}` – Datei als gerenderten Inhalt einbetten; Überschriften werden um die angegebene Ebenenzahl verschoben, YAML-Frontmatter wird als Hinweiszeile dargestellt.

## Pflege

Kapiteltexte in `doc/` folgen dem Framework-Release-Prozess (Checkliste FW-CL-11 prüft die Konsistenz zwischen Dokument und Repository). `out/` ist Build-Ausgabe und nicht versioniert (`.gitignore`); `BRIEF_*.md` sind Arbeitsunterlagen der Erstellung und nicht Teil des Dokuments.

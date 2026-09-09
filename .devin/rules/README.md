# `.devin/rules/` – Laufzeitregeln für Devin Local

Dieses Verzeichnis enthält die Devin-spezifische Laufzeitfassung der Framework-Regeln. Die kanonische, werkzeugneutrale Langform liegt in `framework/`. Bei Widersprüchen gilt die Langform; die Laufzeitfassung wird dann korrigiert.

## Mechanismus (Belegstatus)

| Aussage | Status |
|---|---|
| Devin Local liest Regeldateien aus `.devin/rules/*.md` (bevorzugt) und aus dem Legacy-Pfad `.windsurf/rules/` | `[DOK]` |
| `AGENTS.md` im Workspace-Root wird als always-on-Regel behandelt und in dieselbe Regel-Engine eingespeist | `[DOK]` |
| Frontmatter-Felder `description`, `trigger` (`always_on`, `manual`, `model_decision`, `agent`, `glob`), `globs` | `[DOK]` |
| Root-Regeln werden beim Sitzungsstart geladen, Regeln in Unterverzeichnissen erst beim Zugriff auf das Verzeichnis | `[DOK]` |
| `.devin/` hat Vorrang vor `.windsurf/`; persönliche `*.local.md`-Dateien überschreiben geteilte Pendants | `[DOK]` |
| Zeichenlimits: 12.000 Zeichen je Workspace-Regeldatei, 6.000 Zeichen für globale Regeln (dokumentiert für Cascade-Regeln) | `[DOK]` für Cascade; Gültigkeit für Devin Local `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` |
| Bedeutung der Trigger: `always_on` = vollständiger Inhalt in jedem Prompt; `model_decision` = nur Beschreibung im Prompt, Inhalt bei Relevanz; `glob` = bei Lesen/Ändern passender Dateien; `manual` = nur bei ausdrücklicher Erwähnung | `[DOK]` |

## Nummernschema und Ebenenzuordnung (Framework-Konvention `[KONZ]`)

| Präfix | Ebene der Prioritätshierarchie | Trigger | Pflege |
|---|---|---|---|
| `00-` | 3 Framework Core | `always_on` | Framework Owner |
| `10-` | 3 Framework Core (Datenschutz/Sicherheit) | `model_decision` | Framework Owner |
| `15-` | 3 Framework Core (Entwicklungsregeln) | `model_decision` | Framework Owner |
| `20-` | 4 Project Overlay | `always_on` | Projekt (Overlay Owner) |
| `30-` | 6 Role Packs | `model_decision` | Modul-Owner |
| `40-` | 5 Technology Packs | `glob` | Modul-Owner |

Die Nummern bilden die Ladereihenfolge im Dateisystem ab, nicht die Priorität. Die Priorität regelt `AGENTS.md` Abschnitt 2 beziehungsweise `governance/PRIORITY_HIERARCHY.md`.

## Regeln für dieses Verzeichnis

- Jede Datei bleibt unter 12.000 Zeichen; `20-project-overlay.md` SOLL unter 6.000 Zeichen bleiben, damit die Summe der always-on-Inhalte klein bleibt (Least Context).
- Dateien mit Endung `.template` sind Vorlagen und werden von Devin nicht als Regeln gelesen (Konvention des Frameworks; Devin liest laut Dokumentation `*.md`).
- Änderungen an `00-`, `10-`, `15-` nur über Framework-Änderungsantrag; `20-` über den Overlay-Prozess des Projekts; `30-`, `40-` über den jeweiligen Modul-Owner.
- `tests/scripts/validate-framework.py` prüft Frontmatter, Zeichenlimits und verbotene Inhalte.

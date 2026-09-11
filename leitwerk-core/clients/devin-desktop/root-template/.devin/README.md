# `.devin/` – Laufzeitschicht für Devin Desktop (Devin Local)

Dieses Verzeichnis enthält alles, was Devin Local aus dem Repository liest. Es ist die einzige Devin-spezifische Schicht des Frameworks (Tool Independence). Alle Inhalte sind Konkretisierungen der werkzeugneutralen Regeln in `leitwerk-core/framework/`.

| Datei / Verzeichnis | Zweck | Belegstatus |
|---|---|---|
| `rules/*.md` | Regeldateien mit `trigger`-Frontmatter (Kurzfassungen von Core, Overlay, Packs) | `[DOK]` Mechanismus |
| `skills/<name>/SKILL.md` | Skills, Aufruf `/name`; Frontmatter `name`, `description`, `argument-hint`, `allowed-tools`, `permissions`, `triggers` | `[DOK]` |
| `agents/<name>.md` | Subagent-Profile (hier: nur lesender Reviewer) | `[DOK]` |
| `config.json` | Berechtigungen `deny` / `ask` / `allow` (projektweit, versioniert) **und Lebenszyklus-Hooks** (`PreToolUse`-Secret- und Pfadprüfung, `SessionStart`-Statusmeldung). Erzeugt aus `leitwerk-core/framework/runtime/permissions.json` und `hooks.json`; hier trägt das Projekt nur die Platzhalterwerte ein. Dass die Hooks in dieser Datei stehen und nicht in einer eigenen, folgt D-32: In einer Sitzung wurde erhoben, dass der Client aus einer eigenen Hook-Datei (`hooks.v1.json`) **keinen** Hook ausführt, aus `config.json` sofort (`AP2-DD-10`) | `[DOK]` Mechanismus; Hook-Ort **in einer Sitzung erhoben** (AP2, 3.9.19); Regelmenge `[EMPF]`; exakte Schemadetails `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` |
| `config.local.json` (nicht versioniert) | persönliche Überschreibungen; im Framework nur zum Verschärfen zulässig | `[DOK]`; **eine Lockerung verhindert der Client nicht** (ERH-11, Zeile B9 des Packs) |
| `mcp_config.json.example` | Vorlage für MCP-Server (Standard: keine) | `[DOK]` Dateiname; Struktur `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` |

## Nicht enthalten (bewusst)

- `workflows/` – Cascade-Workflows werden von Devin Local nicht unterstützt `[DOK]`; Skills übernehmen diese Funktion.
- `memories` – Devin Local persistiert keine Memories `[DOK]`; Wissen wird ausschließlich über versionierte Regeln, Overlay-Dokumente und Skills bereitgestellt.
- `.windsurf/` – Legacy-Pfad, wird nicht gepflegt (`.gitignore`).
- `hooks.v1.json` – seit 0.25.0 **nicht mehr erzeugt** (D-32). Der Client führt aus dieser Datei keinen Hook aus; die Hook-Konfiguration steht in `config.json`. Eine Installation von vor 0.25.0 trägt die Datei weiterhin: `install.py --update` legt die neue Fassung an, **löscht die verwaiste Datei aber nicht**. Sie ist von Hand zu entfernen; der Validator meldet sie bis dahin als Warnung.

## Berechtigungsmodi (Permission Modes) und Framework-Vorgabe

| Modus laut Dokumentation `[DOK]` | Verhalten | Framework-Vorgabe |
|---|---|---|
| Normal | Lesen automatisch; Schreiben und Befehle fragen | **Standard** für alle Kontrollstufen |
| Accept Edits | Workspace-Änderungen automatisch; Shell fragt | nur Kontrollstufe niedrig, nur mit Overlay-Freigabe |
| Smart | Änderungen automatisch; „sichere" Aktionen automatisch | untersagt (D-05), Ausnahme nur über Ausnahmeprozess |
| Bypass | alles automatisch | **untersagt** (D-05) |
| Autonomous (mit Sandbox) | Shell und Fetch automatisch im Sandkasten; Dateiänderungen fragen | nur über Ausnahmeprozess und mit Sandbox-Nachweis |

## Sitzungsfreigaben

Beim Bestätigen einer Anfrage bietet Devin Local an, die Freigabe einmalig, für die Sitzung, für das Projekt, lokal für das Projekt oder global zu speichern `[DOK]`. Im Framework sind nur **einmalig** und **für die Sitzung** zulässig. Projekt- und globale Freigaben verändern `.devin/config.json` beziehungsweise die Benutzerkonfiguration und erfordern einen Änderungsantrag.

## Regelablage (`rules/`)

Die Regelablage enthält die clientspezifische Laufzeitfassung der Framework-Regeln. Die kanonische, werkzeugneutrale Langform liegt in `leitwerk-core/framework/`. Bei Widersprüchen gilt die Langform; die Laufzeitfassung wird dann korrigiert.

> **Warum dieser Abschnitt hier steht und nicht in `rules/`.** Der Client führt **jede** Datei der Regelablage in seinem Regelregister und macht sie damit ladbar – auch eine, die keine Regel ist. Bis 0.25.0 lag dort eine eigene README; der Client führte sie mit Trigger `manual` (`AP2-DD-17`). Seit 0.26.0 gilt: **Die Regelablage enthält ausschließlich Regeln** (D-36). Registriert wird, was *in* der Ablage liegt, nicht was daneben liegt.

### Mechanismus (Belegstatus)

| Aussage | Status |
|---|---|
| Devin Local liest Regeldateien aus `.devin/rules/*.md` (bevorzugt) und aus dem Legacy-Pfad `.windsurf/rules/` | `[DOK]` |
| `AGENTS.md` im Workspace-Root wird als always-on-Regel behandelt und in dieselbe Regel-Engine eingespeist | `[DOK]` |
| Frontmatter-Felder `description`, `trigger` (`always_on`, `manual`, `model_decision`, `agent`, `glob`), `globs` | `[DOK]` |
| Root-Regeln werden beim Sitzungsstart geladen, Regeln in Unterverzeichnissen erst beim Zugriff auf das Verzeichnis | `[DOK]` |
| `.devin/` hat Vorrang vor `.windsurf/`; persönliche `*.local.md`-Dateien überschreiben geteilte Pendants | `[DOK]` |
| Eine Datei **ohne** Frontmatter führt der Client mit Aktivierung `manual` – gemessen mit `devin rules show` (K-25) | in einer Sitzung erhoben (2026-09-11) |
| Zeichenlimits: 12.000 Zeichen je Regeldatei, 6.000 Zeichen für `20-project-overlay.md` – **Vorgabe des Frameworks, keine Produkteigenschaft** | `[EMPF]`. Die Zahlen stammen aus der Cascade-Dokumentation; für Devin Local nennt der Hersteller **keine** Grenze (zweimal geprüft am 2026-09-11 gegen 3.9.19, `CR-2026-027`). Der Validator prüft weiter dagegen |
| Bedeutung der Trigger: `always_on` = vollständiger Inhalt in jedem Prompt; `model_decision` = nur Beschreibung im Prompt, Inhalt bei Relevanz; `glob` = bei Lesen/Ändern passender Dateien; `manual` = nur bei ausdrücklicher Erwähnung | `[DOK]` |

### Nummernschema und Ebenenzuordnung (Framework-Konvention `[KONZ]`)

| Präfix | Ebene der Prioritätshierarchie | Trigger | Pflege |
|---|---|---|---|
| `00-` | 3 Framework Core | `always_on` | Framework Owner |
| `10-` | 3 Framework Core (Datenschutz/Sicherheit) | `model_decision` | Framework Owner |
| `15-` | 3 Framework Core (Entwicklungsregeln) | `model_decision` | Framework Owner |
| `20-` | 4 Project Overlay | `always_on` | Projekt (Overlay Owner) |
| `30-` | 6 Role Packs | `model_decision` | Modul-Owner |
| `40-` | 5 Technology Packs | `glob` | Modul-Owner |

Die Nummern bilden die Ladereihenfolge im Dateisystem ab, nicht die Priorität. Die Priorität regelt `AGENTS.md` Abschnitt 2 beziehungsweise `leitwerk-core/governance/PRIORITY_HIERARCHY.md`.

### Regeln für die Regelablage

- **Dort liegt nur, was Regel ist.** Ein erklärender Text gehört hierher, nicht dorthin (D-36). Der Validator meldet eine Datei in der Vorlage der Regelablage, die dem Nummernschema nicht folgt.
- Jede Datei bleibt unter 12.000 Zeichen; `20-project-overlay.md` SOLL unter 6.000 Zeichen bleiben, damit die Summe der always-on-Inhalte klein bleibt (Least Context).
- Dateien mit Endung `.template` sind Vorlagen und werden nicht als Regeln gelesen (Konvention des Frameworks; der Client liest laut Dokumentation `*.md`).
- Änderungen an `00-`, `10-`, `15-` nur über Framework-Änderungsantrag; `20-` über den Overlay-Prozess des Projekts; `30-`, `40-` über den jeweiligen Modul-Owner.
- `leitwerk-core/tests/scripts/validate-framework.py` prüft Frontmatter, Zeichenlimits und verbotene Inhalte.

**Migration aus einer Installation vor 0.26.0:** `install.py --update` legt diese Fassung an, **löscht die alte README der Regelablage aber nicht.** Sie ist von Hand zu entfernen; solange sie liegt, führt der Client sie weiterhin als Regel.

## Validierung

`python3 leitwerk-core/tests/scripts/validate-framework.py` prüft dieses Verzeichnis (JSON-Gültigkeit, Kernregeln in `config.json`, Frontmatter der Regeln und Skills, Zeichenlimits, verbotene Inhalte).

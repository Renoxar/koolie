# `.devin/` – Laufzeitschicht für Devin Desktop (Devin Local)

Dieses Verzeichnis enthält alles, was Devin Local aus dem Repository liest. Es ist die einzige Devin-spezifische Schicht des Frameworks (Tool Independence). Alle Inhalte sind Konkretisierungen der werkzeugneutralen Regeln in `devin-core-framework/framework/`.

| Datei / Verzeichnis | Zweck | Belegstatus |
|---|---|---|
| `rules/*.md` | Regeldateien mit `trigger`-Frontmatter (Kurzfassungen von Core, Overlay, Packs) | `[DOK]` Mechanismus |
| `skills/<name>/SKILL.md` | Skills, Aufruf `/name`; Frontmatter `name`, `description`, `argument-hint`, `allowed-tools`, `permissions`, `triggers` | `[DOK]` |
| `agents/<name>.md` | Subagent-Profile (hier: nur lesender Reviewer) | `[DOK]` |
| `config.json` | Berechtigungen `deny` / `ask` / `allow` (projektweit, versioniert) | `[DOK]` Mechanismus; Regelmenge `[EMPF]`; exakte Schemadetails `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` |
| `config.local.json` (nicht versioniert) | persönliche Überschreibungen; im Framework nur zum Verschärfen zulässig | `[DOK]` |
| `hooks.v1.json` | Lebenszyklus-Hooks (`PreToolUse`-Secret- und Pfadprüfung, `SessionStart`-Statusmeldung) | `[DOK]` Mechanismus; Skripte `[EMPF]`, Status entwurf |
| `mcp_config.json.example` | Vorlage für MCP-Server (Standard: keine) | `[DOK]` Dateiname; Struktur `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` |

## Nicht enthalten (bewusst)

- `workflows/` – Cascade-Workflows werden von Devin Local nicht unterstützt `[DOK]`; Skills übernehmen diese Funktion.
- `memories` – Devin Local persistiert keine Memories `[DOK]`; Wissen wird ausschließlich über versionierte Regeln, Overlay-Dokumente und Skills bereitgestellt.
- `.windsurf/` – Legacy-Pfad, wird nicht gepflegt (`.gitignore`).

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

## Validierung

`python3 devin-core-framework/tests/scripts/validate-framework.py` prüft dieses Verzeichnis (JSON-Gültigkeit, Kernregeln in `config.json`, Frontmatter der Regeln und Skills, Zeichenlimits, verbotene Inhalte).

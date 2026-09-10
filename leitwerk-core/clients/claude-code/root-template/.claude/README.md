# `.claude/` – Laufzeitschicht für Claude Code

Dieses Verzeichnis enthält alles, was Claude Code aus dem Repository liest. Es ist die einzige clientspezifische Schicht des Frameworks (Tool Independence). Alle Inhalte sind Konkretisierungen der werkzeugneutralen Regeln in `leitwerk-core/framework/`.

Die Durchsetzungstiefe – welche Zusage dieser Client technisch erzwingt und welche nur als Anweisung im Kontext steht – ist in der Fähigkeitsmatrix des Client Packs ausgewiesen: `leitwerk-core/clients/claude-code/CLIENT_PACK.md`.

| Datei / Verzeichnis | Zweck | Belegstatus |
|---|---|---|
| `rules/*.md` | Regeltexte (Core, Overlay, Packs); werden vom Client selbst geladen – ohne `paths`-Feld unbedingt, mit `paths`-Feld bei passenden Dateien | [DOK] (AP2, Clientversion 2.1.267) |
| `skills/<name>/SKILL.md` | Skills, Aufruf über den Namen mit vorangestelltem Schrägstrich; Frontmatter `name`, `description`, `argument-hint`, `allowed-tools` | `[DOK]` |
| `agents/<name>.md` | Subagentenprofile (hier: nur lesender Reviewer); Frontmatter `name`, `description`, `tools` (ergänzend `disallowedTools`) | [DOK] (AP2, Clientversion 2.1.267) |
| `settings.json` | Berechtigungen `deny` / `ask` / `allow` **und** Hooks (projektweit, versioniert). Erzeugt aus `leitwerk-core/framework/runtime/permissions.json` und `hooks.json`; hier trägt das Projekt nur die Platzhalterwerte ein | `[DOK]` Mechanismus; Regelmenge `[EMPF]`; Mustersemantik [DOK] (AP2, Clientversion 2.1.267) – gitignore-Syntax; **Pfadregeln wertet dieser Client nur für `Read` und `Edit` aus** |
| `settings.local.json` (nicht versioniert) | persönliche Überschreibungen; im Framework nur zum Verschärfen zulässig | `[DOK]` |

Im Wurzelverzeichnis liegen außerdem `CLAUDE.md` (Wurzel-Anweisung) und `.mcp.json.example` (Vorlage für MCP-Server; Standard: keine). Die Wurzel-Anweisung bindet die Regeltexte **nicht** ein; sie liegen in `rules/` und werden von dort geladen.

## Zwei Unterschiede zur Fassung anderer Client Packs

Die **Regeltexte sind inhaltlich identisch**. Abweichend ist nur, wie ihre Ladebedingung notiert wird.

1. **Eine Bedingung statt dreier Ladetrigger.** Die Kernquelle kennt `always_on`, `model_decision` und `glob`; dieser Client kennt für Regeldateien nur die Bindung an Dateimuster (`paths`). `always_on` und `model_decision` werden deshalb beide auf unbedingtes Laden abgebildet, `glob` auf `paths`. Für `model_decision` ist das eine Verschärfung, keine Lockerung – es kostet Kontext (rund 25.000 Zeichen einschließlich `CLAUDE.md`), senkt aber kein Schutzniveau. Einzelheiten: `rules/README.md`.

2. **Hooks stehen in `settings.json`**, nicht in einer eigenen Datei.

Bis Framework-Release 0.14.0 stand hier ein dritter Unterschied – „Schreibschutz braucht zwei Regeln je Pfad". Er galt nie: Dieser Client wertet Pfadregeln ausschließlich für `Read` und `Edit` aus (AP2-CC-02, D-26).

## Technology Packs

Ein Technology Pack (Ebene 5) lädt über ein Dateimuster – etwa nur bei Java-Dateien. Dieser Client bildet das nativ ab: Die Laufzeitfassung des Packs liegt als `rules/40-tech-<name>.md` mit `paths:` und den Dateimustern der Technologie. Sie lädt, sobald der Client eine passende Datei liest.

Zu beachten: Die Regel steht damit nicht schon zu Beginn der Aufgabe im Kontext, sondern erst nach der ersten Berührung einer passenden Datei. Ein Pack, dessen Regeln vorher gelten müssen, bleibt unbedingt geladen. Details: `rules/README.md` und `CLIENT_PACK.md` Abschnitt 5.

## Berechtigungsmodi und Framework-Vorgabe

| Modus | Verhalten | Framework-Vorgabe |
|---|---|---|
| `default` | Lesen automatisch; Schreiben und Befehle fragen | **Standard** für alle Kontrollstufen |
| `acceptEdits` | Dateiänderungen automatisch; Befehle fragen | nur Kontrollstufe niedrig, nur mit Overlay-Freigabe |
| `plan` | nur Analyse und Planung, keine Änderungen | zulässig; entspricht M1/M2 |
| `bypassPermissions` | alles automatisch | **untersagt** (D-05) |

## Validierung

```text
python leitwerk-core/tests/scripts/validate-framework.py
```

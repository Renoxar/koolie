# `.claude/` – Laufzeitschicht für Claude Code

Dieses Verzeichnis enthält alles, was Claude Code aus dem Repository liest. Es ist die einzige clientspezifische Schicht des Frameworks (Tool Independence). Alle Inhalte sind Konkretisierungen der werkzeugneutralen Regeln in `devin-core-framework/framework/`.

Die Durchsetzungstiefe – welche Zusage dieser Client technisch erzwingt und welche nur als Anweisung im Kontext steht – ist in der Fähigkeitsmatrix des Client Packs ausgewiesen: `devin-core-framework/clients/claude-code/CLIENT_PACK.md`.

| Datei / Verzeichnis | Zweck | Belegstatus |
|---|---|---|
| `framework/*.md` | Regeltexte (Core, Overlay, Packs); werden über Importe in `CLAUDE.md` geladen | `[DOK]` Importmechanismus |
| `skills/<name>/SKILL.md` | Skills, Aufruf über den Namen mit vorangestelltem Schrägstrich; Frontmatter `name`, `description`, `argument-hint`, `allowed-tools` | `[DOK]` |
| `agents/<name>.md` | Subagentenprofile (hier: nur lesender Reviewer); Frontmatter `name`, `description`, `tools` | `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>` |
| `settings.json` | Berechtigungen `deny` / `ask` / `allow` **und** Hooks (projektweit, versioniert). Erzeugt aus `devin-core-framework/framework/runtime/permissions.json` und `hooks.json`; hier trägt das Projekt nur die Platzhalterwerte ein | `[DOK]` Mechanismus; Regelmenge `[EMPF]`; Mustersemantik `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>` |
| `settings.local.json` (nicht versioniert) | persönliche Überschreibungen; im Framework nur zum Verschärfen zulässig | `[DOK]` |

Im Wurzelverzeichnis liegen außerdem `CLAUDE.md` (Wurzel-Anweisung, lädt die Regeltexte per Import) und `.mcp.json.example` (Vorlage für MCP-Server; Standard: keine).

## Drei Unterschiede zur Fassung für Clients mit Ladetriggern

Die **Regeltexte sind inhaltlich identisch**. Abweichend ist nur, wie sie geladen werden.

1. **Kein Ladetrigger-Mechanismus.** Clients mit Regeldateien laden Regeln bedingt: immer, bei Relevanz oder passend zu Dateimustern. Claude Code kennt das nicht. Deshalb werden alle vier Regeltexte über Importe in `CLAUDE.md` **immer** geladen. Das ist eine Verschärfung, keine Lockerung – es kostet Kontext (rund 22.000 Zeichen einschließlich `CLAUDE.md`), senkt aber kein Schutzniveau.

2. **Hooks stehen in `settings.json`**, nicht in einer eigenen Datei.

3. **Schreibschutz braucht zwei Regeln je Pfad.** Claude Code trennt die Werkzeuge zum Ändern und zum Anlegen von Dateien; eine Verweigerungsregel für nur eines von beiden liefe ins Leere.

## Technology Packs

Ein Technology Pack (Ebene 5) lädt bei Clients mit Ladetriggern über ein Dateimuster – etwa nur bei Java-Dateien. Dieser Mechanismus fehlt hier. Zwei Ersatzwege, in dieser Reihenfolge zu prüfen:

1. **Verschachtelte `CLAUDE.md`** im betreffenden Verzeichnis, wenn Technologie und Verzeichnis zusammenfallen (`backend/CLAUDE.md`, `frontend/CLAUDE.md`). Claude Code lädt sie beim Zugriff auf das Verzeichnis – das kommt einem Dateimuster am nächsten.
2. **Import in `CLAUDE.md`**, wenn die Zuordnung nicht am Verzeichnis hängt. Dann ist das Pack immer geladen; bei mehreren Packs wächst der ständige Kontext entsprechend.

Die Wahl ist im Overlay zu dokumentieren. Details: `CLIENT_PACK.md` Abschnitt 5.

## Berechtigungsmodi und Framework-Vorgabe

| Modus | Verhalten | Framework-Vorgabe |
|---|---|---|
| `default` | Lesen automatisch; Schreiben und Befehle fragen | **Standard** für alle Kontrollstufen |
| `acceptEdits` | Dateiänderungen automatisch; Befehle fragen | nur Kontrollstufe niedrig, nur mit Overlay-Freigabe |
| `plan` | nur Analyse und Planung, keine Änderungen | zulässig; entspricht M1/M2 |
| `bypassPermissions` | alles automatisch | **untersagt** (D-05) |

## Validierung

```text
python devin-core-framework/tests/scripts/validate-framework.py
```

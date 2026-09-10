# Begriffe der Laufzeitschicht

| Attribut | Wert |
|---|---|
| ID | `FW-DOC-GLOSSARY` |
| Version | `0.1.0` |
| Status | `entwurf` |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |

## Zweck

Der Kern des Frameworks ist werkzeugneutral (D-02). Er darf deshalb **keine Pfade nennen, die nur bei einem einzigen KI-Client existieren** – sonst ist er nicht neutral, sondern nur so formuliert, als wäre er es.

Diese Datei legt die Begriffe fest, mit denen der Kern die Bestandteile der Laufzeitschicht bezeichnet, und bildet sie auf die tatsächlichen Pfade je Client Pack ab. Sie ist damit das Gegenstück zum Platzhalterregister: Dort stehen projektspezifische Werte, hier clientspezifische Pfade.

## Regel

- Im **Kern** (`devin-core-framework/framework/`, `governance/`, `checklists/`, `prompts/`, `decision-trees/`, `onboarding/`, `docs/`, `templates/`, `examples/`, `tests/`) wird ausschließlich der **Begriff** verwendet.
- In einem **Client Pack** (`devin-core-framework/clients/<client>/`) wird der **Pfad** verwendet – dort ist er richtig und notwendig.
- In **historischen Dokumenten** (`CHANGELOG.md`, `governance/change-requests/`, `governance/DECISION_LOG.md`, `tests/protocols/`) bleiben genannte Pfade unverändert. Sie beschreiben einen vergangenen Zustand; ihn nachträglich zu glätten, würde die Nachvollziehbarkeit zerstören.

`devin-core-framework/tests/scripts/validate-framework.py` meldet Nennungen einer nicht installierten Laufzeitschicht als Warnung (Prüfung 12).

## Begriffe und ihre Entsprechungen

| Begriff im Kern | Was es ist | `devin-desktop` | `claude-code` |
|---|---|---|---|
| **Wurzel-Anweisungsdatei** | Die Datei im Wurzelverzeichnis, die der Client zu Beginn jeder Sitzung lädt | `AGENTS.md` | `CLAUDE.md` |
| **Laufzeitschicht** | Das Verzeichnis mit allem, was der Client aus dem Repository liest | `.devin/` | `.claude/` |
| **Berechtigungsdatei** | Versionierte Konfiguration der Rechte (verweigern / rückfragen / erlauben) | `.devin/config.json` | `.claude/settings.json` |
| **Regelablage** | Verzeichnis der Regeltexte (Core-Kurzfassungen, Overlay, Packs) | `.devin/rules/` | `.claude/framework/` |
| **Skill-Ablage** | Verzeichnis der Skills, je Skill ein Unterverzeichnis mit `SKILL.md` | `.devin/skills/` | `.claude/skills/` |
| **Agentenprofile** | Verzeichnis der Subagentenprofile | `.devin/agents/` | `.claude/agents/` |
| **Hook-Konfiguration** | Ort der Lebenszyklus-Hooks | `.devin/hooks.v1.json` | in der Berechtigungsdatei |
| **MCP-Konfiguration** | Ort der Anbindung externer Systeme | `.devin/mcp_config.json` | `.mcp.json` |
| **Nutzerlokale Überschreibung** | Nicht versionierte, persönliche Ergänzung; im Framework nur zum Verschärfen zulässig | `AGENTS.local.md`, `.devin/config.local.json` | `CLAUDE.local.md`, `.claude/settings.local.json` |

Die maßgebliche Fassung je Client steht in `manifest.json` (maschinenlesbar) und `CLIENT_PACK.md` Abschnitt 1 (mit Belegstatus) des jeweiligen Packs.

## Was der Begriff nicht sagt

Ein Begriff benennt die **Rolle** eines Artefakts, nicht seine Eigenschaften. Ob ein Client eine Zusage des Frameworks technisch erzwingt oder nur als Anweisung führt, steht in der **Fähigkeitsmatrix** seines Client Packs (`devin-core-framework/clients/README.md` Abschnitt 4).

Zwei Beispiele, in denen der Begriff gleich und die Wirkung verschieden ist:

- Die **Regelablage** enthält bei beiden Packs dieselben Regeltexte. Bei `devin-desktop` laden sie nach Ladetriggern bedingt, bei `claude-code` über Importe stets. Der Kern beschreibt deshalb, *was* eine Regel bewirkt, nicht *wann* sie geladen wird.
- Die **Hook-Konfiguration** ist bei `devin-desktop` eine eigene Datei, bei `claude-code` ein Abschnitt der Berechtigungsdatei. Ein Kerntext, der „die Hook-Datei" nennt, wäre schon wieder clientgebunden.

## Nummernschema der Regelablage

Das Schema gilt über alle Client Packs, damit eine Regel beim Clientwechsel wiedererkennbar bleibt. Es ist eine Framework-Konvention (`[KONZ]`), keine Produkteigenschaft.

| Präfix | Ebene der Prioritätshierarchie |
|---|---|
| `00-` | 3 Framework Core (Arbeitsmodell) |
| `10-` | 3 Framework Core (Datenschutz und Sicherheit) |
| `15-` | 3 Framework Core (Entwicklungsregeln) |
| `20-` | 4 Project Overlay |
| `30-` | 6 Role Packs |
| `40-` | 5 Technology Packs |

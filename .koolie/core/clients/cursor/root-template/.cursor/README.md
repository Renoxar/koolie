# Laufzeitschicht `.cursor/` – was hier liegt und wem es gehört

Diese Ablage ist die **Laufzeitform** des Frameworks für den Client `cursor`. Die kanonische, werkzeugneutrale Langform steht in `.koolie/core/framework/`; was hier liegt, ist daraus erzeugt. **Inhaltliche Änderungen gehören in den Kern und laufen als Änderungsantrag** (`.koolie/core/governance/CHANGE_REQUEST_TEMPLATE.md`).

## Was hier liegt

| Pfad | Inhalt | Wem es gehört |
|---|---|---|
| `../AGENTS.md` | Wurzel-Anweisung (Ebene 1); der Client lädt sie in jeder Sitzung | Framework |
| `rules/00-*.mdc`, `rules/10-*.mdc`, `rules/15-*.mdc` | Regeltexte des Frameworks (Ebene 3) mit `alwaysApply: true` – sie laden immer | Framework |
| `rules/20-project-overlay.mdc` | Laufzeitfassung des Project Overlays (Ebene 4) | Projekt |
| `rules/40-tech-*.mdc`, `rules/30-*.mdc` | Technology und Role Packs (Ebenen 5 und 6); eine an Dateimuster gebundene Regel trägt `alwaysApply: false` und `globs` | Projekt |
| `cli.json` | **Berechtigungen** des Frameworks, dazu die Projektwerte | Projekt (aus dem Kern erzeugt) |
| `hooks.json` | Schutz-Hook und Statusmeldung | Framework |
| `agents/koolie-reviewer.md` | Nur lesender Review-Subagent (`readonly: true`) | Framework |
| `skills/koolie-*/` | Skills des Frameworks | Framework |

## Vier Dinge, die bei diesem Client anders sind

**1. Regeldateien brauchen die Endung `.mdc`.** Eine `.md`-Datei in `rules/` lädt der Client nicht. Eigene Regeln des Projekts heißen deshalb `2N-overlay-<name>.mdc` und `40-tech-<name>.mdc`.

**2. `cli.json` trägt nur den Schlüssel `permissions`.** Jeder weitere Schlüssel – auch ein Kommentar – lässt den Client nicht starten; ebenso kaputtes JSON. Die Erklärung der Datei steht deshalb hier und nicht in ihr. Ein Pfadmuster steht **zweimal**, einmal mit `/` und einmal mit `\`: Der Client vergleicht es mit dem absoluten Pfad, und unter Windows trägt dieser Gegenschrägstriche. Wer einen Projektpfad sperrt (`<EXCLUDED_PATHS>`, `<READ_ONLY_PATHS>` …), trägt ihn ebenfalls in beiden Schreibweisen ein, mit führendem `*`: `Read(*/geheim/*)` und `Read(*\geheim\*)`.

**3. Dateien im Arbeitsbereich schreibt der Client ohne Rückfrage.** Es gibt keinen Rückfragekorb. Befehle, die kein `allow` deckt, fragen zurück; Schreiben nicht. Die Schreibverbote dieser Datei und der Schutz-Hook bleiben die Schranke, der Merge Request die Sichtprüfung.

**4. Die Hooks brauchen unter Windows den richtigen Start.** Aus PowerShell oder `cmd` gestartet, laufen sie; aus Git Bash gestartet (Variable `SHELL` gesetzt), scheitern sie – und der Schutz-Hook sperrt dann jede Operation. Sie laufen nur in einem Arbeitsbereich, dem der Client vertraut.

## Was hier **nicht** liegt

Keine Geheimnisse, keine Zugangsdaten, keine Kunden- oder Personennamen. Die Regeln dazu stehen in `rules/10-privacy-security.mdc`; der Validator prüft es, und der Schutz-Hook blockiert eine Werkzeugeingabe, die ein Muster dieser Kategorien trägt.

## Prüfen

```text
python .koolie/core/tests/scripts/validate-framework.py --strict-overlay
```

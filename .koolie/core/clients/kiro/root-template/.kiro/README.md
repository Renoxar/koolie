# Laufzeitschicht `.kiro/` – was hier liegt und wem es gehört

Diese Ablage ist die **Laufzeitform** des Frameworks für den Client `kiro`. Die kanonische, werkzeugneutrale Langform steht in `.koolie/core/framework/`; was hier liegt, ist daraus erzeugt (D-02). **Inhaltliche Änderungen gehören in den Kern und laufen als Änderungsantrag** (`.koolie/core/governance/CHANGE_REQUEST_TEMPLATE.md`).

## Was hier liegt

| Pfad | Inhalt | Wem es gehört |
|---|---|---|
| `../AGENTS.md` | Wurzel-Anweisung (Ebene 1); der Client lädt sie in jeder Sitzung | Framework |
| `steering/00-*.md`, `steering/10-*.md`, `steering/15-*.md` | Regeltexte des Frameworks (Ebene 3), ohne Ladebedingung – sie laden immer | Framework |
| `steering/16-plan-spezifikation.md` | Vorgaben für die Spezifikationen unter `specs/` – sie sind hier der Träger des Plans | Framework |
| `steering/20-project-overlay.md` | Laufzeitfassung des Project Overlays (Ebene 4) | Projekt |
| `steering/40-tech-*.md`, `steering/30-*.md` | Technology und Role Packs (Ebenen 5 und 6); eine an Dateimuster gebundene Regel trägt `inclusion: fileMatch` | Projekt |
| `agents/koolie.json` | **Agentenprofil mit den Berechtigungen** des Frameworks, dazu die Projektwerte | Projekt (aus dem Kern erzeugt) |
| `agents/fw-reviewer.md` | Nur lesender Review-Agent | Framework |
| `settings/cli.json` | **Wählt das Agentenprofil und die Engine** für jede Sitzung in diesem Verzeichnis | Projekt (aus dem Kern erzeugt) |
| `hooks/koolie.json` | Schutz-Hook und Statusmeldung | Framework |
| `skills/fw-*/` | Skills des Frameworks | Framework |
| `specs/` | Spezifikationen, die der Client anlegt (Anforderungen, Entwurf, Aufgaben) | Projekt |

## Drei Dinge, die bei diesem Client anders sind

**1. Die Berechtigungen wirken nur über den aktiven Agenten.** Die Berechtigungsdatei des Arbeitsbereichs hält dieser Client **außerhalb** des Repositoriums. Das Framework legt seine Regeln deshalb in das Agentenprofil `agents/koolie.json`, und `settings/cli.json` wählt es als Standard. Wer eine Sitzung mit einem anderen Agenten startet (`--agent`), arbeitet ohne diese Regeln. 🔴 **Fehlt das Profil oder ist es kein gültiges JSON, fällt der Client still auf seinen eingebauten Agenten zurück** – er meldet es nur als Warnung. `validate-framework.py` prüft beide Dateien gegeneinander.

**2. Die Hooks laufen nur in der interaktiven Sitzung.** Im Betrieb ohne Rückfragen (`kiro-cli chat --no-interactive`) aktiviert der Client sie nicht; dort trägt allein das Agentenprofil.

**3. `specs/` ist beschreibbar, der Rest dieser Ablage nicht.** Das Schreibverbot auf die Laufzeitschicht nimmt den Teilbaum `specs/` aus, weil dort das Planartefakt liegt. Jede Schreiboperation fragt trotzdem zurück.

## Was hier **nicht** liegt

Keine Geheimnisse, keine Zugangsdaten, keine Kunden- oder Personennamen. Die Regeln dazu stehen in `steering/10-privacy-security.md`; der Validator prüft es, und der Schutz-Hook blockiert eine Werkzeugeingabe, die ein Muster dieser Kategorien trägt.

## Prüfen

```text
python .koolie/core/tests/scripts/validate-framework.py --strict-overlay
```

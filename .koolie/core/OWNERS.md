# Ownership

> Rollen, keine Personen. Die Zuordnung von Personen zu Rollen erfolgt außerhalb des Repositorys im Teamverzeichnis der Organisation. Details der Verantwortlichkeiten: `.koolie/core/governance/RACI.md`.

| Bereich | Pfad(e) | Owner (Rolle) | Stellvertretung |
|---|---|---|---|
| Framework gesamt, Releases, Prioritätshierarchie | `/`, `.koolie/core/VERSION`, `.koolie/core/CHANGELOG.md`, `.koolie/core/governance/` | `<FRAMEWORK_OWNER>` | `<TBD: Rolle>` |
| Framework Core | `.koolie/core/framework/core/`, Wurzel-Anweisungsdatei, Regelablage `00-*`, `10-*`, `15-*` | `<FRAMEWORK_OWNER>` | `<TBD>` |
| Datenschutzmodell (FW-CORE-02) | `.koolie/core/framework/core/02-privacy.md`, Regelablage `10-*` | `<FRAMEWORK_OWNER>` mit `<DATA_PROTECTION_CONTACT>` | – |
| Sicherheitsmodell (FW-CORE-03), Berechtigungen, Hooks | `.koolie/core/framework/core/03-security.md`, `.koolie/core/framework/runtime/permissions.json`, `.koolie/core/framework/runtime/hooks.json`, `.koolie/core/clientmap.py`, `.koolie/core/tests/scripts/hook-*` | `<FRAMEWORK_OWNER>` mit `<SECURITY_CONTACT>` | – |
| Role Pack Softwareentwicklung | `.koolie/core/framework/role-packs/software-development/`, Regelablage `30-role-software-development.md` | `<FRAMEWORK_OWNER>` (bis Benennung Modul-Owner: `<TBD>`) | – |
| Role Pack Requirements Engineering (RP-RE), Skill `role-re-ticket` | `.koolie/core/framework/role-packs/requirements-engineering/` | `<FRAMEWORK_OWNER>` | `<TBD: Rolle>` |
| Technology Packs | `.koolie/core/framework/tech-packs/` | je Pack `<TBD: Modul-Owner>` | – |
| Client Packs (Abbildung auf KI-Clients) | `.koolie/core/clients/` | `<FRAMEWORK_OWNER>` | `<SECURITY_CONTACT>` für Kernzusagen ohne technische Durchsetzung |
| Client Pack `devin-desktop` (CP-DD) | `.koolie/core/clients/devin-desktop/` | `<FRAMEWORK_OWNER>` | `<TBD: Rolle>` |
| Client Pack `claude-code` (CP-CC) | `.koolie/core/clients/claude-code/` | `<FRAMEWORK_OWNER>` | `<TBD: Rolle>` |
| Framework-Skills FW-SK-001…012 | Skill-Ablage `fw-*` | `<FRAMEWORK_OWNER>` (bis Benennung Modul-Owner je Gruppe) | – |
| Prompt-Bibliothek | `.koolie/core/prompts/` | `<FRAMEWORK_OWNER>` | – |
| Checklisten und Entscheidungsbäume | `.koolie/core/checklists/`, `.koolie/core/decision-trees/` | `<FRAMEWORK_OWNER>` | – |
| Onboarding | `.koolie/core/onboarding/` | `<FRAMEWORK_OWNER>` mit Mentorinnen und Mentoren | – |
| Testkatalog und Validierung | `tests/` | `<FRAMEWORK_OWNER>` | – |
| Pilotkonzept und Metriken | `.koolie/core/pilot/` | Projektleitung des Pilotprojekts | – |
| Project Overlay (je Projekt) | `.koolie/project-overlay/`, Regelablage `20-*`, `2N-*` | `<APPROVAL_ROLE>` des Projekts | `<TBD>` |
| Organisationsvorgaben-Einbindung | `.koolie/core/framework/org-policies/` | Organisation | – |

Hinweis für Git-Plattformen: Diese Tabelle KANN zusätzlich als plattformspezifische `CODEOWNERS`-Datei abgebildet werden (`<TBD: CODEOWNERS je Plattform-Konvention>`); maßgeblich bleibt diese Datei.

# Ownership

> Rollen, keine Personen. Die Zuordnung von Personen zu Rollen erfolgt außerhalb des Repositorys im Teamverzeichnis der Organisation. Details der Verantwortlichkeiten: `devin-core-framework/governance/RACI.md`.

| Bereich | Pfad(e) | Owner (Rolle) | Stellvertretung |
|---|---|---|---|
| Framework gesamt, Releases, Prioritätshierarchie | `/`, `devin-core-framework/VERSION`, `devin-core-framework/CHANGELOG.md`, `devin-core-framework/governance/` | `<FRAMEWORK_OWNER>` | `<TBD: Rolle>` |
| Framework Core | `devin-core-framework/framework/core/`, `AGENTS.md`, `.devin/rules/00-*`, `10-*`, `15-*` | `<FRAMEWORK_OWNER>` | `<TBD>` |
| Datenschutzmodell (FW-CORE-02) | `devin-core-framework/framework/core/02-privacy.md`, `.devin/rules/10-*` | `<FRAMEWORK_OWNER>` mit `<DATA_PROTECTION_CONTACT>` | – |
| Sicherheitsmodell (FW-CORE-03), Berechtigungen, Hooks | `devin-core-framework/framework/core/03-security.md`, `.devin/config.json`, `.devin/hooks.v1.json`, `devin-core-framework/tests/scripts/hook-*` | `<FRAMEWORK_OWNER>` mit `<SECURITY_CONTACT>` | – |
| Role Pack Softwareentwicklung | `devin-core-framework/framework/role-packs/software-development/`, `.devin/rules/30-role-software-development.md` | `<FRAMEWORK_OWNER>` (bis Benennung Modul-Owner: `<TBD>`) | – |
| Role Pack Requirements Engineering (RP-RE), Skill `role-re-ticket` | `devin-core-framework/framework/role-packs/requirements-engineering/` | `<FRAMEWORK_OWNER>` | `<TBD: Rolle>` |
| Technology Packs | `devin-core-framework/framework/tech-packs/` | je Pack `<TBD: Modul-Owner>` | – |
| Framework-Skills FW-SK-001…012 | `.devin/skills/fw-*` | `<FRAMEWORK_OWNER>` (bis Benennung Modul-Owner je Gruppe) | – |
| Prompt-Bibliothek | `devin-core-framework/prompts/` | `<FRAMEWORK_OWNER>` | – |
| Checklisten und Entscheidungsbäume | `devin-core-framework/checklists/`, `devin-core-framework/decision-trees/` | `<FRAMEWORK_OWNER>` | – |
| Onboarding | `devin-core-framework/onboarding/` | `<FRAMEWORK_OWNER>` mit Mentorinnen und Mentoren | – |
| Testkatalog und Validierung | `tests/` | `<FRAMEWORK_OWNER>` | – |
| Pilotkonzept und Metriken | `devin-core-framework/pilot/` | Projektleitung des Pilotprojekts | – |
| Project Overlay (je Projekt) | `project-overlay/`, `.devin/rules/20-*`, `2N-*` | `<APPROVAL_ROLE>` des Projekts | `<TBD>` |
| Organisationsvorgaben-Einbindung | `devin-core-framework/framework/org-policies/` | Organisation | – |

Hinweis für Git-Plattformen: Diese Tabelle KANN zusätzlich als plattformspezifische `CODEOWNERS`-Datei abgebildet werden (`<TBD: CODEOWNERS je Plattform-Konvention>`); maßgeblich bleibt diese Datei.

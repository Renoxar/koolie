# Role Packs (Ebene 6 der Prioritätshierarchie)

Role Packs sind optionale, rollenbezogene Module. Sie konkretisieren die Arbeitsweise für eine Rolle (Softwareentwicklung, Softwarearchitektur, Requirements Engineering, Testing und QA, DevOps, Dokumentation, Code Review) und liefern rollenspezifische Skills.

## Verbindliche Regeln für Role Packs

1. Ein Role Pack enthält **keine** Governance-, Datenschutz- oder Sicherheitsregeln und **keine** Projektwerte. Solche Inhalte gehören in den Core (Ebene 3) beziehungsweise das Overlay (Ebene 4). Bei Zweifeln: `decision-trees/06-rule-placement.md`.
2. Ein Role Pack darf Core- und Overlay-Regeln nur konkretisieren oder verschärfen, nie lockern.
3. Aufbau je Pack: `ROLE_PACK.md` (Langform), optional `skills/` (Quellablage rollenspezifischer Skills, Präfix `role-<pack>-`, werden zur Aktivierung nach `.devin/skills/` kopiert) und eine Laufzeitfassung `.devin/rules/30-role-<pack>.md` mit `trigger: model_decision`.
4. Ein Pack wird im Overlay aktiviert (Abschnitt 1 „Rollen im Team" und Laufzeitfassung vorhanden). Nicht aktivierte Packs liegen nur im Verzeichnis `framework/role-packs/` und werden von Devin nicht als Regel geladen.
5. Jedes Pack hat einen Modul-Owner (`OWNERS.md`), eine Version und einen Änderungsverlauf.

## Verfügbare Packs

| Pack | Status | Laufzeitfassung | Owner |
|---|---|---|---|
| `software-development` | entwurf (Referenz) | `.devin/rules/30-role-software-development.md` | `<FRAMEWORK_OWNER>` |
| `software-architecture` | vorgesehen | – | `<TBD>` |
| `requirements-engineering` | vorgesehen | – | `<TBD>` |
| `testing-qa` | vorgesehen | – | `<TBD>` |
| `devops` | vorgesehen | – | `<TBD>` |
| `documentation` | vorgesehen | – | `<TBD>` |
| `code-review` | vorgesehen | – | `<TBD>` |

Neue Packs entstehen aus `_template/ROLE_PACK.md`.

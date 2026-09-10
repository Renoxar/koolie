# Role Packs (Ebene 6 der Prioritätshierarchie)

Role Packs sind optionale, rollenbezogene Module. Sie konkretisieren die Arbeitsweise für eine Rolle (Softwareentwicklung, Softwarearchitektur, Requirements Engineering, Testing und QA, DevOps, Dokumentation, Code Review) und liefern rollenspezifische Skills.

## Verbindliche Regeln für Role Packs

1. Ein Role Pack enthält **keine** Governance-, Datenschutz- oder Sicherheitsregeln und **keine** Projektwerte. Solche Inhalte gehören in den Core (Ebene 3) beziehungsweise das Overlay (Ebene 4). Bei Zweifeln: `devin-core-framework/decision-trees/06-rule-placement.md`.
2. Ein Role Pack darf Core- und Overlay-Regeln nur konkretisieren oder verschärfen, nie lockern.
3. Aufbau je Pack: `ROLE_PACK.md` (Langform), optional `skills/` (Quellablage rollenspezifischer Skills, Präfix `role-<pack>-`, werden zur Aktivierung in die Skill-Ablage kopiert) und eine Laufzeitfassung `30-role-<pack>.md` in der Regelablage. Bei Clients mit Ladetriggern lädt sie bei Relevanz; bei Clients ohne Ladetrigger wird sie in der Wurzel-Anweisungsdatei eingebunden (`devin-core-framework/docs/RUNTIME_GLOSSARY.md`).
4. Ein Pack wird im Overlay aktiviert (Abschnitt 1 „Rollen im Team" und Laufzeitfassung vorhanden). Nicht aktivierte Packs liegen nur im Verzeichnis `devin-core-framework/framework/role-packs/` und werden von Devin nicht als Regel geladen.
5. Jedes Pack hat einen Modul-Owner (`devin-core-framework/OWNERS.md`), eine Version und einen Änderungsverlauf.

## Verfügbare Packs

| Pack | Status | Laufzeitfassung | Owner |
|---|---|---|---|
| `software-development` | entwurf (Referenz) | `30-role-software-development.md` in der Regelablage | `<FRAMEWORK_OWNER>` |
| `software-architecture` | vorgesehen | – | `<TBD>` |
| `requirements-engineering` | entwurf | `30-role-requirements-engineering.md` in der Regelablage | `<FRAMEWORK_OWNER>` |
| `testing-qa` | vorgesehen | – | `<TBD>` |
| `devops` | vorgesehen | – | `<TBD>` |
| `documentation` | vorgesehen | – | `<TBD>` |
| `code-review` | vorgesehen | – | `<TBD>` |

Neue Packs entstehen aus `_template/ROLE_PACK.md`.

## Quellablage der Laufzeitfassung

Jedes Pack legt seine Laufzeitfassung unter `<pack>/runtime/30-role-<pack>.md` ab und seine Skills – falls vorhanden – unter `<pack>/skills/`. Zur Aktivierung werden beide in die Laufzeitschicht kopiert:

```bash
cp devin-core-framework/framework/role-packs/<pack>/runtime/30-role-<pack>.md .devin/rules/
cp -r devin-core-framework/framework/role-packs/<pack>/skills/* .devin/skills/    # falls vorhanden
```

`devin-core-framework/install.py` nimmt diesen Schritt bewusst nicht vorweg: **Die Aktivierung eines Packs ist eine Projektentscheidung** (Punkt 4), kein Installationsschritt. Kein Pack ist nach einer Erstinstallation aktiv – auch nicht das Referenzpack `software-development`.

Einmal aktiviert, gehören die kopierten Bestandteile aber zum Aktualisierungsumfang: `install.py --update` bringt sie auf den Stand des Releases, `--check` meldet lokale Abweichungen. Die Unterscheidung ist also: *ob* ein Pack aktiv ist, entscheidet das Projekt – *was* darin steht, ist Framework-Inhalt.

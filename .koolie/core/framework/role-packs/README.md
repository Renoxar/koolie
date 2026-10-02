# Role Packs (Ebene 6 der Prioritätshierarchie)

Role Packs sind optionale, rollenbezogene Module. Sie konkretisieren die Arbeitsweise für eine Rolle (Softwareentwicklung, Softwarearchitektur, Requirements Engineering, Testing und QA, DevOps, Dokumentation, Code Review) und liefern rollenspezifische Skills.

## Verbindliche Regeln für Role Packs

1. Ein Role Pack enthält **keine** Governance-, Datenschutz- oder Sicherheitsregeln und **keine** Projektwerte. Solche Inhalte gehören in den Core (Ebene 3) beziehungsweise das Overlay (Ebene 4). Bei Zweifeln: `.koolie/core/decision-trees/06-rule-placement.md`.
2. Ein Role Pack darf Core- und Overlay-Regeln nur konkretisieren oder verschärfen, nie lockern.
3. Aufbau je Pack: `ROLE_PACK.md` (Langform), optional `skills/` (Quellablage rollenspezifischer Skills, Präfix `koolie-`, über alle Packs eindeutig, werden zur Aktivierung in die Skill-Ablage kopiert) und eine Laufzeitfassung `30-role-<pack>.md` in der Regelablage. Sie trägt den Ladetrigger `model_decision` und lädt bei Relevanz; kennt ein Client keine modellentschiedene Ladebedingung, lädt sie dort unbedingt – eine Verschärfung, die sein Client Pack ausweist (`.koolie/core/docs/RUNTIME_GLOSSARY.md`).
4. Ein Pack wird im Overlay aktiviert (Abschnitt 1, Zeile „Aktivierte Role Packs", und Laufzeitfassung vorhanden; Prüfung 110 hält beides gegeneinander). Nicht aktivierte Packs liegen nur im Verzeichnis `.koolie/core/framework/role-packs/` und werden vom KI-Client nicht als Regel geladen.
5. Jedes Pack hat einen Modul-Owner (`.koolie/core/OWNERS.md`), eine Version und einen Änderungsverlauf.

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

Jedes Pack legt seine Laufzeitfassung unter `<pack>/runtime/30-role-<pack>.md` ab und seine Skills – falls vorhanden – unter `<pack>/skills/`. Die Aktivierung hat drei Teile:

1. **Laufzeitfassung und Skills kopieren** und die Laufzeitfassung in die Form des Client Packs bringen:

   ```bash
   # <Regelablage> und <Skill-Ablage> sind die Pfade des installierten Client Packs;
   # ihre Entsprechung je Pack steht in .koolie/core/docs/RUNTIME_GLOSSARY.md.
   cp .koolie/core/framework/role-packs/<pack>/runtime/30-role-<pack>.md <Regelablage>/
   cp -r .koolie/core/framework/role-packs/<pack>/skills/* <Skill-Ablage>/    # falls vorhanden
   python .koolie/core/install.py --update    # bringt die Laufzeitfassung in die Form des Client Packs
   ```

   Der dritte Befehl ist nötig: `cp` legt die Quellform mit YAML-Frontmatter (`description`, `trigger`) ab, und ein Client mit eigener Bedingungssprache wertet diese Felder nicht aus (`claude-code` kennt nur `paths`). Erst `install.py --update` bildet die Ladebedingung ab; der Validator meldet die Quellform sonst als Fehler.

2. **Das Pack im Overlay eintragen** (Punkt 4).

3. **Jeden kopierten Skill in die Berechtigungsdatei eintragen**, in der Form `<Werkzeug>(<skillname>)`. Welches Werkzeug, sagt `permission_tools.skill` im Manifest des Client Packs – bei `claude-code` `Skill`; bei `devin-desktop` ist das Feld leer, weil dort keine Schreibweise bekannt ist. Ohne Eintrag fällt der Aufruf in den Rückfragekorb und im rückfragefreien Betrieb in die Abweisung; die Sitzung liest die `SKILL.md` dann als Datei, ohne die Werkzeugbeschränkung des Skills. Prüfung 72 meldet einen Skill ohne Eintrag und einen Eintrag ohne Skill.

Der Eintrag steht nicht in `framework/runtime/permissions.json`, weil jede Installation diese Datei trägt, auch eine ohne das Pack – eine Freigabe für einen Skill, den es dort nicht gibt, wäre eine Zusage ohne Gegenstand (Prüfung 39).

`.koolie/core/install.py` aktiviert kein Pack von selbst: **Die Aktivierung ist eine Projektentscheidung** (Punkt 4), kein Installationsschritt. Nach einer Erstinstallation ist kein Pack aktiv, auch nicht das Referenzpack `software-development`.

Einmal aktiviert, gehören die kopierten Bestandteile zum Aktualisierungsumfang: `install.py --update` bringt sie auf den Stand des Releases, `--check` meldet lokale Abweichungen. *Ob* ein Pack aktiv ist, entscheidet das Projekt – *was* darin steht, ist Framework-Inhalt.

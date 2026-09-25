# Role Packs (Ebene 6 der Prioritätshierarchie)

Role Packs sind optionale, rollenbezogene Module. Sie konkretisieren die Arbeitsweise für eine Rolle (Softwareentwicklung, Softwarearchitektur, Requirements Engineering, Testing und QA, DevOps, Dokumentation, Code Review) und liefern rollenspezifische Skills.

## Verbindliche Regeln für Role Packs

1. Ein Role Pack enthält **keine** Governance-, Datenschutz- oder Sicherheitsregeln und **keine** Projektwerte. Solche Inhalte gehören in den Core (Ebene 3) beziehungsweise das Overlay (Ebene 4). Bei Zweifeln: `.koolie/core/decision-trees/06-rule-placement.md`.
2. Ein Role Pack darf Core- und Overlay-Regeln nur konkretisieren oder verschärfen, nie lockern.
3. Aufbau je Pack: `ROLE_PACK.md` (Langform), optional `skills/` (Quellablage rollenspezifischer Skills, Präfix `role-<pack>-`, werden zur Aktivierung in die Skill-Ablage kopiert) und eine Laufzeitfassung `30-role-<pack>.md` in der Regelablage. Sie trägt den Ladetrigger `model_decision` und lädt bei Relevanz; kennt ein Client keine modellentschiedene Ladebedingung, lädt sie dort unbedingt – eine Verschärfung, die sein Client Pack ausweist (`.koolie/core/docs/RUNTIME_GLOSSARY.md`).
4. Ein Pack wird im Overlay aktiviert (Abschnitt 1 „Rollen im Team" und Laufzeitfassung vorhanden). Nicht aktivierte Packs liegen nur im Verzeichnis `.koolie/core/framework/role-packs/` und werden vom KI-Client nicht als Regel geladen.
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

Jedes Pack legt seine Laufzeitfassung unter `<pack>/runtime/30-role-<pack>.md` ab und seine Skills – falls vorhanden – unter `<pack>/skills/`. Zur Aktivierung werden beide in die Laufzeitschicht kopiert:

```bash
# <Regelablage> und <Skill-Ablage> sind die Pfade des installierten Client Packs;
# ihre Entsprechung je Pack steht in .koolie/core/docs/RUNTIME_GLOSSARY.md.
cp .koolie/core/framework/role-packs/<pack>/runtime/30-role-<pack>.md <Regelablage>/
cp -r .koolie/core/framework/role-packs/<pack>/skills/* <Skill-Ablage>/    # falls vorhanden
python .koolie/core/install.py --update    # bringt die Laufzeitfassung in die Form des Client Packs
```

🔴 **Der dritte Befehl ist kein Nachklapp, und das ist gemessen** (2026-09-21, D-244). `cp` legt die **Quellform** ab – YAML-Frontmatter mit `description` und `trigger`. Ein Client, der für Regeldateien eine **eigene Bedingungssprache** führt, wertet diese Felder nicht aus (`claude-code`: nur `paths`, `K-18`); der Validator meldete am Messbaum von Bündel 5 **zwei Fehler** an genau dieser Datei, und die Ladebedingung `model_decision` war nirgends abgebildet. `install.py` kann die Abbildung seit `0.14.0` – `ist_regelquelle()` führt die Laufzeitfassungen aktivierter Packs ausdrücklich auf –, **aber nur, wenn man ihn danach laufen lässt.** Für `devin-desktop` ist Quellform gleich Zielform; dort war der fehlende Befehl folgenlos, und deshalb ist er acht Releases lang niemandem aufgefallen.

> *Ein Werkzeug, das eine Abbildung kann, und eine Anleitung, die „kopieren“ sagt: Die Anleitung gewinnt, weil sie gelesen wird.*

🔴 **Und ein weiterer Schritt, den diese Anleitung bis `0.81.0` nicht nannte: der
Skill gehört in die Berechtigungsdatei.** Je kopiertem Skill kommt ein Eintrag der
Form `<Werkzeug>(<skillname>)` hinzu – welches Werkzeug, sagt `permission_tools.skill`
im Manifest des Client Packs (bei `claude-code` `Skill`, bei `devin-desktop` ist das
Feld leer, weil dort keine Schreibweise bekannt ist, D-89).

**Warum das nicht in `framework/runtime/permissions.json` steht:** Eine Regel dort
trägt **jede** Installation, auch die, die das Pack nicht aktiviert hat – und eine
Vorabfreigabe für einen Skill, den es nicht gibt, ist eine Zusage ohne Gegenstand
(Prüfung 39, D-81). Die Aktivierung ist eine Projektentscheidung (Punkt 4), also
gehört der Eintrag zu ihr.

**Was ohne ihn geschieht, ist gemessen** (2026-09-21, D-238): Der Aufruf fällt in den
Rückfragekorb und im rückfragefreien Betrieb in die Abweisung; die Sitzung liest die
`SKILL.md` dann ersatzweise als Datei – **ohne die Werkzeugbeschränkung des Skills.**
🟢 **Prüfung 72 setzt es seither durch**, in beide Richtungen: ein Skill ohne Eintrag
und ein Eintrag ohne Skill werden beide gemeldet.

`.koolie/core/install.py` nimmt diesen Schritt bewusst nicht vorweg: **Die Aktivierung eines Packs ist eine Projektentscheidung** (Punkt 4), kein Installationsschritt. Kein Pack ist nach einer Erstinstallation aktiv – auch nicht das Referenzpack `software-development`.

Einmal aktiviert, gehören die kopierten Bestandteile aber zum Aktualisierungsumfang: `install.py --update` bringt sie auf den Stand des Releases, `--check` meldet lokale Abweichungen. Die Unterscheidung ist also: *ob* ein Pack aktiv ist, entscheidet das Projekt – *was* darin steht, ist Framework-Inhalt.

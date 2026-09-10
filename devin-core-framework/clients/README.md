# Client Packs – Abbildung des Frameworks auf einen KI-Client

| Attribut | Wert |
|---|---|
| Modul-ID | `FW-CLIENT-PACKS` |
| Ebene | keine – Querschnittsschicht (siehe Abschnitt 2) |
| Version | 0.2.0 |
| Status | entwurf |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |

## 1. Zweck

Das Framework trennt seit D-02 zwei Formen derselben Regeln: die kanonische, **werkzeugneutrale** Langform in `devin-core-framework/framework/` und die kompakte **Laufzeitform** in der Wurzel des Projekts. Die Laufzeitform ist bislang ausschließlich für einen KI-Client geschrieben.

Ein **Client Pack** macht diese Bindung explizit und austauschbar. Es beantwortet für genau einen Client zwei Fragen:

1. **Wohin** gehören die Laufzeitartefakte – Wurzel-Anweisungsdatei, Regeldateien, Skills, Berechtigungen, Hooks, Subagentenprofile?
2. **Welche Zusagen des Frameworks setzt dieser Client technisch durch** – und welche bleiben eine Anweisung, der das Modell folgen kann oder auch nicht?

Die zweite Frage ist der eigentliche Grund für diese Schicht. Ein Framework, dessen Datenschutz- und Sicherheitszusagen bei einem Client von der Engine erzwungen werden und bei einem anderen nur als Prosa im Prompt stehen, muss diesen Unterschied sichtbar machen. Sonst erzeugt es falsche Sicherheit – genau dort, wo es am meisten schadet.

## 2. Ein Client Pack ist keine Regelebene

Die Prioritätshierarchie (`devin-core-framework/governance/PRIORITY_HIERARCHY.md`, D-06) bleibt achtstufig und **unverändert**. Ein Client Pack

- führt **keine** neuen Verhaltensregeln ein,
- **lockert** keine bestehende Regel,
- und steht in keiner Konfliktbeziehung zu Core, Overlay oder Packs.

Es ist eine **Abbildungsschicht**: Es übersetzt die Ebenen 3 bis 7 in die Artefakte eines konkreten Clients und dokumentiert die Durchsetzungstiefe. Entsteht ein Widerspruch zwischen einem Client Pack und der Langform, gilt die Langform; das Client Pack wird korrigiert.

## 3. Bestandteile

| Bestandteil | Inhalt |
|---|---|
| `CLIENT_PACK.md` | Pfadabbildung, **Semantikabbildung**, **Fähigkeitsmatrix**, Abweichungen, Belegstatus – die menschenlesbare Fassung |
| `manifest.json` | Dieselben Abbildungen maschinenlesbar; `install.py` und `validate-framework.py` lesen sie. **Ohne Manifest ist ein Pack nicht installierbar** |
| `root-template/` | Nur noch die Artefakte, die tatsächlich clientspezifisch sind – derzeit fünf Dateien je Pack |

Alles andere liegt einmal im Kern und wird bei der Installation in die Form dieses Clients gebracht: Regeltexte, Wurzel-Anweisung, Agentenprofil und Skills als **Formtransformation** (D-16, D-17), Berechtigungen und Hooks als **Semantikabbildung** (D-18). Der Unterschied ist wesentlich: Bei einer Formtransformation ist der Inhalt derselbe und nur die Schreibweise anders. Bei der Semantikabbildung unterscheiden sich die Werkzeuge selbst – ein Client trennt Ändern und Anlegen, ein anderer nicht; ein Befehlsverbot greift hier wörtlich und dort über ein Präfix. Weil an genau diesen Regeln die Kernzusagen hängen, prüft die Abbildung drei Eigenschaften und bricht ab, wenn eine verletzt ist:

| Zusicherung | Warum |
|---|---|
| Keine `deny`- oder `ask`-Regel ohne Zielwerkzeug | Sie wegzulassen wäre eine Lockerung. Bei `allow` ist Weglassen zulässig – es fällt auf den strengeren Standard zurück |
| Die Präfixform eines Befehlsverbots muss ein Präfix der wörtlichen Form sein | Damit ist sie nachweislich mindestens so breit; die Abweichung ist belegbar eine Verschärfung |
| Bei `allow` müssen beide Formen übereinstimmen | Dort wäre jede Verbreiterung eine Lockerung |

## 4. Die Fähigkeitsmatrix

Kern jedes Client Packs. Sie stuft jede technische Zusage des Frameworks in eine von drei Klassen ein:

| Klasse | Bedeutung |
|---|---|
| `[TECHNISCH]` | Der Client erzwingt die Zusage. Ein Verstoß ist nicht möglich, unabhängig vom Modellverhalten. |
| `[TEXTUELL]` | Die Zusage steht als Anweisung im Kontext. Ein Modell kann ihr folgen; erzwungen ist sie nicht. |
| `[NICHT ABBILDBAR]` | Der Client bietet keinen Mechanismus. Die Zusage entfällt für diesen Client. |

**Verbindliche Folgen:**

- Eine Kernzusage aus `_core_rules_integrity` in der Berechtigungsdatei, die ein Client nicht `[TECHNISCH]` abbildet, MUSS im Client Pack begründet und im Overlay des aufnehmenden Projekts als dokumentierte Ausnahme geführt werden (`project-overlay/exceptions/EXCEPTIONS.md`).
- Ein Client Pack, das eine Kernzusage auf `[NICHT ABBILDBAR]` setzt, DARF nicht ohne Freigabe durch `<SECURITY_CONTACT>` in Betrieb genommen werden.
- Die Einstufung `[TECHNISCH]` MUSS gegen eine reale Installation belegt sein. Bis dahin trägt die Zeile den Marker `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>`.

Die Delegationsverbote V1 bis V12 (`devin-core-framework/framework/core/09-risk-model.md`) sind davon ausgenommen: Sie beschreiben Aufgaben, die nicht delegiert werden dürfen, und sind ihrer Natur nach organisatorisch. Kein Client setzt sie technisch durch; sie sind bei jedem Client `[TEXTUELL]`.

## 5. Ein Client Pack erstellen

1. `_template/` nach `<client-name>/` kopieren und alle Platzhalter ersetzen.
2. Pfadabbildung eintragen: Wo erwartet dieser Client Anweisungsdatei, Regeln, Skills, Berechtigungen, Hooks?
3. Fähigkeitsmatrix ausfüllen. Jede Zeile ohne Beleg trägt den VERIFY-Marker.
4. `root-template/` anlegen: die Wurzelartefakte in der Form dieses Clients.
5. `manifest.json` anlegen: Pflichtfelder `client`, `skills_dir`, `pack_runtime_dir`, `core_skill_prefix`, `core_paths`, `seed_paths`; zusätzlich `runtime_dir`, `root_instruction_file`, `permissions_file`, `agents_dir`, `has_rule_triggers`.
6. Semantikabbildung eintragen: `permission_tools`, `permission_tools_bare`, `permission_path_prefix`, `permission_exec_match` und gegebenenfalls `permission_exec_suffix`, `permissions_extra`, `permissions_note`; für die Hooks `hook_tools` und `hook_project_dir_var`. Kennt der Client keine eigene Hook-Datei, zeigt `<HOOKS_FILE>` auf dieselbe Datei wie `<PERMISSIONS_FILE>` – daran wird die Einbettung erkannt. `<CORE_DIR>` wird **nicht** belegt; den setzt die Installation.
7. Pack in dieser Datei und in `devin-core-framework/OWNERS.md` eintragen.
8. Probeinstallation in ein leeres Verzeichnis; Validator dagegen ausführen; Testkatalog-Basistests gegen eine Installation des Clients fahren.

## 6. Verfügbare Client Packs

| Pack | Code | Status | `[TECHNISCH]` | Kernzusagen | Fähigkeitsmatrix belegt |
|---|---|---|---|---|---|
| `devin-desktop` | `CP-DD` | entwurf | 21 von 26 | 6 von 6 | nein – Belege stehen aus (Roadmap AP2) |
| `claude-code` | `CP-CC` | entwurf | 20 von 26 | 6 von 6 | nein – Belege stehen aus (Roadmap AP2) |

## 7. Änderungsverlauf

| Version | Datum | Änderung | Autor (Rolle) |
|---|---|---|---|
| 0.1.0 | 2026-09-10 | angelegt (`CR-2026-002`) | `<FRAMEWORK_OWNER>` |
| 0.2.0 | 2026-09-10 | Semantikabbildung der Berechtigungen und Hooks ergänzt (`CR-2026-008`) | `<FRAMEWORK_OWNER>` |

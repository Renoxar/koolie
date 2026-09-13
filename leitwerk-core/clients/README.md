# Client Packs – Abbildung des Frameworks auf einen KI-Client

| Attribut | Wert |
|---|---|
| Modul-ID | `FW-CLIENT-PACKS` |
| Ebene | keine – Querschnittsschicht (siehe Abschnitt 2) |
| Version | 0.5.0 |
| Status | entwurf |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |

## 1. Zweck

Das Framework trennt seit D-02 zwei Formen derselben Regeln: die kanonische, **werkzeugneutrale** Langform in `leitwerk-core/framework/` und die kompakte **Laufzeitform** in der Wurzel des Projekts. Die Laufzeitform ist bislang ausschließlich für einen KI-Client geschrieben.

Ein **Client Pack** macht diese Bindung explizit und austauschbar. Es beantwortet für genau einen Client zwei Fragen:

1. **Wohin** gehören die Laufzeitartefakte – Wurzel-Anweisungsdatei, Regeldateien, Skills, Berechtigungen, Hooks, Subagentenprofile?
2. **Welche Zusagen des Frameworks setzt dieser Client technisch durch** – und welche bleiben eine Anweisung, der das Modell folgen kann oder auch nicht?

Die zweite Frage ist der eigentliche Grund für diese Schicht. Ein Framework, dessen Datenschutz- und Sicherheitszusagen bei einem Client von der Engine erzwungen werden und bei einem anderen nur als Prosa im Prompt stehen, muss diesen Unterschied sichtbar machen. Sonst erzeugt es falsche Sicherheit – genau dort, wo es am meisten schadet.

## 2. Ein Client Pack ist keine Regelebene

Die Prioritätshierarchie (`leitwerk-core/governance/PRIORITY_HIERARCHY.md`, D-06) bleibt achtstufig und **unverändert**. Ein Client Pack

- führt **keine** neuen Verhaltensregeln ein,
- **lockert** keine bestehende Regel,
- und steht in keiner Konfliktbeziehung zu Core, Overlay oder Packs.

Es ist eine **Abbildungsschicht**: Es übersetzt die Ebenen 3 bis 7 in die Artefakte eines konkreten Clients und dokumentiert die Durchsetzungstiefe. Entsteht ein Widerspruch zwischen einem Client Pack und der Langform, gilt die Langform; das Client Pack wird korrigiert.

## 3. Bestandteile

| Bestandteil | Inhalt |
|---|---|
| `CLIENT_PACK.md` | Pfadabbildung, **Semantikabbildung**, **Fähigkeitsmatrix**, Abweichungen, Belegstatus – die menschenlesbare Fassung |
| `manifest.json` | Dieselben Abbildungen maschinenlesbar; `install.py` und `validate-framework.py` lesen sie. **Ohne Manifest ist ein Pack nicht installierbar** |
| `root-template/` | Nur noch die Artefakte, die tatsächlich clientspezifisch sind – seit 0.26.0 **eine** erklärende README je Pack (die Laufzeit-README; die der Regelablage ist in sie aufgegangen, D-36) |

Alles andere liegt einmal im Kern und wird bei der Installation in die Form dieses Clients gebracht: Regeltexte, Wurzel-Anweisung, Agentenprofil, Skills, Overlay-Laufzeitregel und die beiden Vorlagen als **Formtransformation** (D-16, D-17, D-20), Berechtigungen und Hooks als **Semantikabbildung** (D-18). `seed_paths` ist in beiden Packs leer – die gesamte Saat kommt aus dem Kern. Der Unterschied ist wesentlich: Bei einer Formtransformation ist der Inhalt derselbe und nur die Schreibweise anders. Bei der Semantikabbildung unterscheiden sich die Werkzeuge selbst – ein Client trennt Ändern und Anlegen, ein anderer nicht; ein Befehlsverbot greift hier wörtlich und dort über ein Präfix. Weil an genau diesen Regeln die Kernzusagen hängen, prüft die Abbildung drei Eigenschaften und bricht ab, wenn eine verletzt ist:

| Zusicherung | Warum |
|---|---|
| Keine `deny`- oder `ask`-Regel ohne Zielwerkzeug | Sie wegzulassen wäre eine Lockerung. Bei `allow` ist Weglassen zulässig – es fällt auf den strengeren Standard zurück |
| Die Präfixform eines Befehlsverbots muss ein Präfix der wörtlichen Form sein | Damit ist sie nachweislich mindestens so breit; die Abweichung ist belegbar eine Verschärfung |
| Bei `allow` müssen beide Formen übereinstimmen | Dort wäre jede Verbreiterung eine Lockerung |

## 4. Die Fähigkeitsmatrix

Kern jedes Client Packs. Sie stuft jede technische Zusage des Frameworks in eine von drei Klassen ein:

| Klasse | Bedeutung |
|---|---|
| `[TECHNISCH]` | Der Client erzwingt die Zusage. Ein Verstoß ist nicht möglich, **unabhängig vom Modellverhalten** – nicht notwendig unabhängig vom **Betriebsmodus**. Die Abhängigkeit vom Betriebsmodus weist der B-Block des jeweiligen Packs in einer Vorbemerkung aus; sie ist dort Pflicht (D-35). |
| `[TEXTUELL]` | Die Zusage steht als Anweisung im Kontext. Ein Modell kann ihr folgen; erzwungen ist sie nicht. |
| `[NICHT ABBILDBAR]` | Der Client bietet keinen Mechanismus. Die Zusage entfällt für diesen Client. |

**Kernzusage** im Sinne dieses Abschnitts ist **jede Zeile des B-Blocks mit `Kern = ja`** sowie **jede Regel aus `_core_rules_integrity`** der Berechtigungsdatei. Zusagen der übrigen Blöcke sind **Fähigkeitszusagen**: Ihr Ausfall wird im Pack begründet und im Overlay des aufnehmenden Projekts als bekannte Einschränkung geführt, sperrt die Inbetriebnahme aber nicht.

Die Unterscheidung ist nicht redaktionell. **Eine Kernzusage sagt zu, dass etwas verhindert wird; eine Fähigkeitszusage sagt zu, dass etwas möglich ist** – zum Beispiel, dass man nachsehen kann. Fällt das Erste aus, fehlt eine Schranke. Fällt das Zweite aus, fehlt Sicht. Beides ist ernst, nur das Erste sperrt (`CR-2026-041`, D-41).

**Verbindliche Folgen:**

- Eine Kernzusage aus `_core_rules_integrity` in der Berechtigungsdatei, die ein Client nicht `[TECHNISCH]` abbildet, MUSS im Client Pack begründet und im Overlay des aufnehmenden Projekts als dokumentierte Ausnahme geführt werden (`project-overlay/exceptions/EXCEPTIONS.md`).
- Ein Client Pack, das eine Kernzusage auf `[NICHT ABBILDBAR]` setzt, DARF nicht ohne Freigabe durch `<SECURITY_CONTACT>` in Betrieb genommen werden.
- Eine **Fähigkeitszusage** auf `[NICHT ABBILDBAR]` MUSS in derselben Zeile den Ersatz benennen – oder ausdrücklich festhalten, dass es keinen gibt. Ein Ausfall, der nur eingetragen und nicht ersetzt wird, ist eine stillschweigende Verschlechterung. Prüfung 25 meldet eine Zeile, die das unterlässt.
- Die Einstufung `[TECHNISCH]` MUSS gegen eine reale Installation belegt sein. Bis dahin trägt die Zeile den Marker `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>`.

Die Delegationsverbote V1 bis V12 (`leitwerk-core/framework/core/09-risk-model.md`) sind davon ausgenommen: Sie beschreiben Aufgaben, die nicht delegiert werden dürfen, und sind ihrer Natur nach organisatorisch. Kein Client setzt sie technisch durch; sie sind bei jedem Client `[TEXTUELL]`.

## 5. Ein Client Pack erstellen

1. `_template/` nach `<client-name>/` kopieren und alle Platzhalter ersetzen.
2. Pfadabbildung eintragen: Wo erwartet dieser Client Anweisungsdatei, Regeln, Skills, Berechtigungen, Hooks?
3. Fähigkeitsmatrix ausfüllen. Jede Zeile ohne Beleg trägt den VERIFY-Marker. Der B-Block trägt die **Vorbemerkung zur Betriebsmodus-Abhängigkeit** von `[TECHNISCH]`, ergänzt um den eigenen Belegstand (D-35). Keine Prüfung meldet ihr Fehlen – sie ist eine Anweisung, und das ist hier bewusst so entschieden (`CR-2026-033` E4).
4. `root-template/` anlegen: **nur die erklärende README der Laufzeitschicht**. Die Wurzelartefakte selbst kommen aus dem Kern und werden bei der Installation in die Form dieses Clients gebracht – `seed_paths` bleibt leer (D-20, `CR-2026-010`).
5. `manifest.json` anlegen: Pflichtfelder `client`, `skills_dir`, `pack_runtime_dir`, `core_skill_prefix`, `core_paths`, `seed_paths`; zusätzlich `runtime_dir`, `root_instruction_file`, `permissions_file`, `agents_dir`, `has_rule_triggers`. Kennt der Client eine **eigene** Bedingungssprache für Regeldateien, kommt `rule_triggers` dazu: Es bildet jeden Ladetrigger der Kernquelle auf sie ab. Ein Ladetrigger ohne Eintrag lässt die Installation scheitern – ersatzloses Verwerfen wäre ein Verlust der Zusage (D-26, D-27).
6. Semantikabbildung eintragen: `permission_tools`, `permission_tools_bare`, `permission_path_prefix`, `permission_exec_match` und gegebenenfalls `permission_exec_suffix`, `permissions_extra`, `permissions_note`; für die Hooks `hook_tools` und `hook_project_dir_var`. **`hook_tools` führt jedes Werkzeugverb, das die Hook-Quelle nennt** – seit 0.30.0 auch `search`. Kennt der Client kein Werkzeug einer Klasse, wird die Abwesenheit in `hook_tools_absent` **ausdrücklich erklärt**, samt `_hook_tools_absent_note`; eine leere Liste allein bricht die Abbildung ab, und Prüfung 26 verlangt, dass ein so erklärtes Verb auch in `permission_tools` leer ist. **Verwirft das Pack ein zusagentragendes Frontmatter-Feld eines Skills** (`permissions`, `triggers`) über `skill_frontmatter.drop_fields`, muss es den Ersatz benennen – `skill_permissions_ersatz` beziehungsweise `model_invocation_field`; sonst bricht die Installation ab und Prüfung 27 meldet es (D-47, D-50). **Kennt der Client ein Werkzeug, mit dem ein Unteragent gestartet wird, führt `agent_start_tools` seine Namen** – alle Schreibweisen, die der Client annimmt, und gemessen, nicht angenommen. Kennt er keines oder ist es unerhoben, wird die Abwesenheit in `agent_start_tools_absent` **ausdrücklich erklärt**, samt `_agent_start_tools_absent_note`; Prüfung 34 verlangt eines von beidem und lässt ein Pack, das Zeile **A1** auf `[TECHNISCH]` stellt, nicht mit einer Erklärung davonkommen (D-70). **Und `skill_frontmatter.tool_names` wie `agent_frontmatter.tool_names` führen jedes Verb des Frontmatter-Vokabulars** (`read`, `grep`, `glob`, `edit`, `exec`; die Liste steht in `clientmap.FRONTMATTER_VERBEN`). Bildet der Client eines nicht ab – weil er die Verben selbst als Werkzeugnamen führt oder weil es unerhoben ist –, gehört es in `tool_names_unmapped` samt `_tool_names_unmapped_note`; eine Lücke allein ist keine Aussage, und bis 0.39.0 wurde das Verb dann wörtlich als Werkzeugname durchgereicht (D-78). Prüfung 38 verlangt eines von beidem und hält zugleich die **Richtung** fest: `hook_tools` darf für kein Verbpaar enger sein als `tool_names` – sonst bekäme ein Skill ein Werkzeug vorab freigegeben, das seine eigene Sperre nicht erfasst (D-80). Kennt der Client keine eigene Hook-Datei, zeigt `<HOOKS_FILE>` auf dieselbe Datei wie `<PERMISSIONS_FILE>` – daran wird die Einbettung erkannt. `<CORE_DIR>` wird **nicht** belegt; den setzt die Installation.
7. **Anweisungs- und Konfigurationsquellen außerhalb des Projekts erheben und eintragen.** Der gleichnamige Abschnitt des Packs führt je bekannter Quelle eine Zeile – Pfad, Ladebedingung, Belegstatus, Maßnahme – **oder** einen datierten Abwesenheitsbeleg samt Erhebungsweg („keine bekannt, Stand `<JJJJ-MM-TT>`, erhoben mit `<Kommando>`"). Er umfasst Regeltexte, Skills und Agentenprofile ebenso wie Berechtigungen, Hooks und Einstellungen (D-34, D-37). Prüfung 19 meldet ein Pack ohne diesen Abschnitt; sie prüft seine **Anwesenheit**, nicht seine Richtigkeit. Kennt der Client eine Importsteuerung für fremde Werkzeugformate, wird sie gesetzt und in Zeile R6 ausgewiesen – abschalten statt nur ausweisen.
8. Pack in dieser Datei und in `leitwerk-core/OWNERS.md` eintragen.
9. Probeinstallation in ein leeres Verzeichnis; Validator dagegen ausführen; Testkatalog-Basistests gegen eine Installation des Clients fahren.

## 6. Verfügbare Client Packs

> **Die Spalte `[TECHNISCH]` wird von Prüfung 31 aus der Fähigkeitsmatrix des jeweiligen Packs nachgerechnet** (D-71). Sie stand hier bis 0.35.0 zweimal falsch – „25 von 29" bei `claude-code`, obwohl das Pack selbst einen Absatz darüber führt, dass diese Zahl mit 0.33.0 berichtigt wurde. Eine Zahl mit eindeutiger Grenze gehört ausgerechnet, nicht an zweiter Stelle gepflegt.

| Pack | Code | Status | `[TECHNISCH]` | Kernzusagen | Fähigkeitsmatrix belegt |
|---|---|---|---|---|---|
| `devin-desktop` | `CP-DD` | entwurf | 20 von 36 | 6 von 6 | teilweise – H1, H2, R5, R6 und S5 sind in Sitzungen beobachtet; die Zahl der offenen VERIFY-Marker steht im Pack, Abschnitt „Belegstand" |
| `claude-code` | `CP-CC` | entwurf | 22 von 31 | 6 von 6 | teilweise – Dokumentenabgleich gegen 2.1.267 (AP2), Belegspalte nennt je Zeile die Quelle; für S3, S4, A1 und die Reichweite von H2 liegen Messungen vor, für die übrigen Zeilen stehen die Wirkungsnachweise aus |

## 7. Änderungsverlauf

| Version | Datum | Änderung | Autor (Rolle) |
|---|---|---|---|
| 0.1.0 | 2026-09-10 | angelegt (`CR-2026-002`) | `<FRAMEWORK_OWNER>` |
| 0.2.0 | 2026-09-10 | Semantikabbildung der Berechtigungen und Hooks ergänzt (`CR-2026-008`) | `<FRAMEWORK_OWNER>` |
| 0.3.0 | 2026-09-10 | Restduplikation zusammengeführt; ein Pack umfasst vier Dateien (`CR-2026-010`) | `<FRAMEWORK_OWNER>` |
| 0.4.0 | 2026-09-11 | **Auskunftspflicht über Quellen außerhalb des Projekts** als Schritt beim Anlegen eines Packs (`CR-2026-031`, `CR-2026-038`; D-34, D-37); die Definition von `[TECHNISCH]` nennt die Abhängigkeit vom **Betriebsmodus** (`CR-2026-033`, D-35), der B-Block jedes Packs trägt sie als Pflicht-Vorbemerkung; ein Pack umfasst noch **eine** erklärende README, die der Regelablage ist in die Laufzeit-README aufgegangen (`CR-2026-035`, D-36) | `<FRAMEWORK_OWNER>` |
| 0.5.0 | 2026-09-13 | **Die Übersicht führte zwei Zahlen, die niemand nachrechnete – beide falsch (`CR-2026-058` E7, D-71).** `claude-code` stand auf „25 von 29", während das Pack selbst einen Absatz darüber trägt, dass diese Zahl mit 0.33.0 auf **22 von 31** berichtigt wurde; `devin-desktop` auf „24 von 34" statt **20 von 36**. Prüfung 31 rechnet die Spalte künftig aus der Fähigkeitsmatrix nach. Die Zahl der offenen VERIFY-Marker entfällt hier und verweist auf das Pack: Ihre Grenze ist zur Hälfte Ermessen, und eine gezählte Zahl wäre dort eine Genauigkeit, die es nicht gibt. Neu in Schritt 6: `agent_start_tools` und seine erklärte Abwesenheit (D-70) | `<FRAMEWORK_OWNER>` |

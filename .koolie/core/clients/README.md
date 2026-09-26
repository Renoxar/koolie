# Client Packs – Abbildung des Frameworks auf einen KI-Client

| Attribut | Wert |
|---|---|
| Modul-ID | `FW-CLIENT-PACKS` |
| Ebene | keine – Querschnittsschicht (siehe Abschnitt 2) |
| Version | 0.8.0 |
| Status | pilot |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |

## 1. Zweck

Das Framework trennt seit D-02 zwei Formen derselben Regeln: die kanonische, **werkzeugneutrale** Langform in `.koolie/core/framework/` und die kompakte **Laufzeitform** in der Wurzel des Projekts. Die Laufzeitform ist an den KI-Client gebunden, der sie lädt.

Ein **Client Pack** macht diese Bindung explizit und austauschbar. Es beantwortet für genau einen Client zwei Fragen:

1. **Wohin** gehören die Laufzeitartefakte – Wurzel-Anweisungsdatei, Regeldateien, Skills, Berechtigungen, Hooks, Subagentenprofile?
2. **Welche Zusagen des Frameworks setzt dieser Client technisch durch** – und welche bleiben eine Anweisung, der das Modell folgen kann oder auch nicht?

Die zweite Frage ist der eigentliche Grund für diese Schicht. Ein Framework, dessen Datenschutz- und Sicherheitszusagen bei einem Client von der Engine erzwungen werden und bei einem anderen nur als Prosa im Prompt stehen, muss diesen Unterschied sichtbar machen. Sonst erzeugt es falsche Sicherheit – genau dort, wo es am meisten schadet.

## 2. Ein Client Pack ist keine Regelebene

Die Prioritätshierarchie (`.koolie/core/governance/PRIORITY_HIERARCHY.md`, D-06) bleibt achtstufig und **unverändert**. Ein Client Pack

- führt **keine** neuen Verhaltensregeln ein,
- **lockert** keine bestehende Regel,
- und steht in keiner Konfliktbeziehung zu Core, Overlay oder Packs.

Es ist eine **Abbildungsschicht**: Es übersetzt die Ebenen 3 bis 7 in die Artefakte eines konkreten Clients und dokumentiert die Durchsetzungstiefe. Entsteht ein Widerspruch zwischen einem Client Pack und der Langform, gilt die Langform; das Client Pack wird korrigiert.

## 3. Bestandteile

| Bestandteil | Inhalt |
|---|---|
| `CLIENT_PACK.md` | Pfadabbildung, **Semantikabbildung**, **Fähigkeitsmatrix**, Abweichungen, Belegstatus – die menschenlesbare Fassung |
| `manifest.json` | Dieselben Abbildungen maschinenlesbar; `install.py` und `validate-framework.py` lesen sie. **Ohne Manifest ist ein Pack nicht installierbar** |
| `root-template/` | Nur die Artefakte, die tatsächlich clientspezifisch sind: **eine** erklärende README der Laufzeitschicht je Pack (D-36) |

**Die Vorlage `_template/` trägt von diesen drei Bestandteilen genau einen: `CLIENT_PACK.md`.** Sie ist damit kein Pack, und die Packmenge der Prüfungen nimmt sie ausdrücklich nicht auf (D-336). **Prüfung 84** hält fest, dass die Vorlage eine Vorlage bleibt.

Alles andere liegt einmal im Kern und wird bei der Installation in die Form dieses Clients gebracht: Regeltexte, Wurzel-Anweisung, Agentenprofil, Skills, Overlay-Laufzeitregel und die beiden Vorlagen als **Formtransformation** (D-16, D-17, D-20), Berechtigungen und Hooks als **Semantikabbildung** (D-18). `seed_paths` ist in allen Packs leer – die gesamte Saat kommt aus dem Kern. Der Unterschied ist wesentlich: Bei einer Formtransformation ist der Inhalt derselbe und nur die Schreibweise anders. Bei der Semantikabbildung unterscheiden sich die Werkzeuge selbst – ein Client trennt Ändern und Anlegen, ein anderer nicht; ein Befehlsverbot greift hier wörtlich und dort über ein Präfix. Weil an genau diesen Regeln die Kernzusagen hängen, prüft die Abbildung drei Eigenschaften und bricht ab, wenn eine verletzt ist:

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

- Eine Kernzusage aus `_core_rules_integrity` in der Berechtigungsdatei, die ein Client nicht `[TECHNISCH]` abbildet, MUSS im Client Pack begründet und im Overlay des aufnehmenden Projekts als dokumentierte Ausnahme geführt werden (`.koolie/project-overlay/exceptions/EXCEPTIONS.md`).
- Ein Client Pack, das eine Kernzusage auf `[NICHT ABBILDBAR]` setzt, DARF nicht ohne Freigabe durch `<SECURITY_CONTACT>` in Betrieb genommen werden.
- Eine **Fähigkeitszusage** auf `[NICHT ABBILDBAR]` MUSS in derselben Zeile den Ersatz benennen – oder ausdrücklich festhalten, dass es keinen gibt. Ein Ausfall, der nur eingetragen und nicht ersetzt wird, ist eine stillschweigende Verschlechterung. Prüfung 25 meldet eine Zeile, die das unterlässt.
- Die Einstufung `[TECHNISCH]` MUSS gegen eine reale Installation belegt sein. Bis dahin sagt die Belegzelle `BELEG OFFEN` **mit Grund und Datum** – und, wenn die Frage länger offen bleibt, mit ihrem Klärungspunkt. **Ein Belegstand trägt keine Frist:** Er sagt, was heute belegt ist, nicht, bis wann es belegt sein muss (`CR-2026-121`, D-291).
- **Eine mit `[DOK]` belegte Matrixzeile MUSS im Belegkopf die Quellenkennung der Liste in Anhang 31.4 nennen** (`QC-n`/`QD-n`). Belegkopf ist die Zelle bis zum ersten Satzbruch; was danach steht, ist Erläuterung, und eine Marke dort ist eine **Nennung** und kein Beleg (D-265). Ein Seitenpfad darf danebenstehen, trägt aber nicht – allein die Kennung lässt sich gegen die Liste halten (D-266). Ein Verweisbeleg (*„wie B3"*) erbt die Kennung seines Ziels. **Gibt der Bestand für eine Zeile keine Seite her, sagt sie `QUELLE NICHT ZUGEORDNET` mit Grund und Datum** – geraten wird nicht, *eine geratene Zuordnung sähe wie ein Beleg aus* (D-156, D-263). **Prüfung 73 setzt es durch.**
- **Die Marke `[DOK]` belegt gegen die Herstellerdokumentation.** Ein Nachweis des Frameworks über sich selbst – ein Manifestfeld, eine erzeugte Datei – trägt sie nicht und wird als das benannt, was er ist (D-267).
- **Eine Matrixzeile steht in ihrer Tabelle.** Zwischen ihr und der Trennzeile liegt keine Leerzeile und kein Fremdtext; sonst rendert Markdown sie als Absatz, während die Zusammenfassung des Packs sie weiterzählt (D-264, **Prüfung 74**).

Die Delegationsverbote V1 bis V12 (`.koolie/core/framework/core/09-risk-model.md`) sind davon ausgenommen: Sie beschreiben Aufgaben, die nicht delegiert werden dürfen, und sind ihrer Natur nach organisatorisch. Kein Client setzt sie technisch durch; sie sind bei jedem Client `[TEXTUELL]`.

## 5. Ein Client Pack erstellen

1. `_template/CLIENT_PACK.md` nach `<client-name>/` kopieren und alle Platzhalter ersetzen. **Die Vorlage trägt nur diesen einen Bestandteil, und das ist eine Entscheidung, keine Lücke (D-336):** `manifest.json` (Schritt 5) und `root-template/` (Schritt 4) entstehen in ihren eigenen Schritten – eine vollständige Vorlage wäre ein Pack ohne Client, und jede Prüfung müsste sie einzeln ausnehmen. `_client_packs()` nimmt die Vorlage nicht in die Packmenge auf, und Prüfung 84 hält fest, dass sie keine Packbestandteile trägt.
2. Pfadabbildung eintragen: Wo erwartet dieser Client Anweisungsdatei, Regeln, Skills, Berechtigungen, Hooks?
3. Fähigkeitsmatrix ausfüllen. Jede Zeile ohne Beleg sagt `BELEG OFFEN` mit Grund und Datum. Der B-Block trägt die **Vorbemerkung zur Betriebsmodus-Abhängigkeit** von `[TECHNISCH]`, ergänzt um den eigenen Belegstand (D-35). Keine Prüfung meldet ihr Fehlen – sie ist eine Anweisung, und das ist hier bewusst so entschieden (`CR-2026-033` E4).
4. `root-template/` anlegen: **nur die erklärende README der Laufzeitschicht**. Die Wurzelartefakte selbst kommen aus dem Kern und werden bei der Installation in die Form dieses Clients gebracht – `seed_paths` bleibt leer (D-20, `CR-2026-010`).
5. `manifest.json` anlegen: Pflichtfelder `client`, `skills_dir`, `pack_runtime_dir`, `core_skill_prefix`, `core_paths`, `seed_paths`; zusätzlich `runtime_dir`, `root_instruction_file`, `permissions_file`, `agents_dir`, `has_rule_triggers`. Kennt der Client eine **eigene** Bedingungssprache für Regeldateien, kommt `rule_triggers` dazu: Es bildet jeden Ladetrigger der Kernquelle auf sie ab. Ein Ladetrigger ohne Eintrag lässt die Installation scheitern – ersatzloses Verwerfen wäre ein Verlust der Zusage (D-26, D-27).
6. Semantikabbildung eintragen: `permission_tools`, `permission_tools_bare`, `permission_path_prefix`, `permission_exec_match` und gegebenenfalls `permission_exec_suffix`, `permissions_extra`, `permissions_note`; für die Hooks `hook_tools` und `hook_project_dir_var`. **`hook_tools` führt jedes Werkzeugverb, das die Hook-Quelle nennt**, auch `search`. Kennt der Client kein Werkzeug einer Klasse, wird die Abwesenheit in `hook_tools_absent` **ausdrücklich erklärt**, samt `_hook_tools_absent_note`; eine leere Liste allein bricht die Abbildung ab, und Prüfung 26 verlangt, dass ein so erklärtes Verb auch in `permission_tools` leer ist. **Verwirft das Pack ein zusagentragendes Frontmatter-Feld eines Skills** (`permissions`, `triggers`) über `skill_frontmatter.drop_fields`, muss es den Ersatz benennen – `skill_permissions_ersatz` beziehungsweise `model_invocation_field`; sonst bricht die Installation ab und Prüfung 27 meldet es (D-47, D-50). **Kennt der Client ein Werkzeug, mit dem ein Unteragent gestartet wird, führt `agent_start_tools` seine Namen** – alle Schreibweisen, die der Client annimmt, und gemessen, nicht angenommen. Kennt er keines oder ist es unerhoben, wird die Abwesenheit in `agent_start_tools_absent` **ausdrücklich erklärt**, samt `_agent_start_tools_absent_note`; Prüfung 34 verlangt eines von beidem und lässt ein Pack, das Zeile **A1** auf `[TECHNISCH]` stellt, nicht mit einer Erklärung davonkommen (D-70). **Und `skill_frontmatter.tool_names` wie `agent_frontmatter.tool_names` führen jedes Verb des Frontmatter-Vokabulars** (`read`, `grep`, `glob`, `edit`, `exec`; die Liste steht in `clientmap.FRONTMATTER_VERBEN`). **Führt der Client für das Frontmatter ein eigenes Vokabular, das mit seinen Laufzeit-Werkzeugnamen nicht übereinstimmt, sagt das Pack es in `tool_names_namespace` samt `_tool_names_note`** – Prüfung 38 setzt ihre Richtungsregel dann aus, weil sie sonst zwei Namensräume vergliche (D-88, gemessen bei `devin-desktop`: `glob` wird im Frontmatter angenommen, `find_file_by_name` verworfen, und zur Laufzeit ist es umgekehrt). Bildet der Client ein Verb nicht ab – weil er die Verben selbst als Werkzeugnamen führt oder weil es unerhoben ist –, gehört es in `tool_names_unmapped` samt `_tool_names_unmapped_note`; eine Lücke allein ist keine Aussage (D-78). Prüfung 38 verlangt eines von beidem und hält zugleich die **Richtung** fest: `hook_tools` darf für kein Verbpaar enger sein als `tool_names` – sonst bekäme ein Skill ein Werkzeug vorab freigegeben, das seine eigene Sperre nicht erfasst (D-80). Kennt der Client keine eigene Hook-Datei, zeigt `<HOOKS_FILE>` auf dieselbe Datei wie `<PERMISSIONS_FILE>` – daran wird die Einbettung erkannt. `<CORE_DIR>` wird **nicht** belegt; den setzt die Installation.
7. **Anweisungs- und Konfigurationsquellen außerhalb des Projekts erheben und eintragen.** Der gleichnamige Abschnitt des Packs führt je bekannter Quelle eine Zeile – Pfad, Ladebedingung, Belegstatus, Maßnahme – **oder** einen datierten Abwesenheitsbeleg samt Erhebungsweg („keine bekannt, Stand `<JJJJ-MM-TT>`, erhoben mit `<Kommando>`"). Er umfasst Regeltexte, Skills und Agentenprofile ebenso wie Berechtigungen, Hooks und Einstellungen (D-34, D-37). Prüfung 19 meldet ein Pack ohne diesen Abschnitt; sie prüft seine **Anwesenheit**, nicht seine Richtigkeit. Kennt der Client eine Importsteuerung für fremde Werkzeugformate, wird sie gesetzt und in Zeile R6 ausgewiesen – abschalten statt nur ausweisen.
8. Pack in dieser Datei und in `.koolie/core/OWNERS.md` eintragen.
9. Probeinstallation in ein leeres Verzeichnis; Validator dagegen ausführen; Testkatalog-Basistests gegen eine Installation des Clients fahren.

## 6. Verfügbare Client Packs

> **Die Spalte `[TECHNISCH]` wird von Prüfung 31 aus der Fähigkeitsmatrix des jeweiligen Packs nachgerechnet** (D-71): Eine Zahl mit eindeutiger Grenze gehört ausgerechnet, nicht an zweiter Stelle gepflegt.

| Pack | Code | Status | `[TECHNISCH]` | Kernzusagen | Fähigkeitsmatrix belegt |
|---|---|---|---|---|---|
| `devin-desktop` | `CP-DD` | pilot | 21 von 36 | 6 von 6 | An einer Installation gemessen sind unter anderem `S3`, `B3`, `B10`, `A1` (`CR-2026-120`), `H1`, `H2`, `R5`, `R6` und `S5`. Genau eine Zeile sagt `BELEG OFFEN`, und dauerhaft: `X2` (`K-20`). ⚠️ **Die Einstufungen `[TECHNISCH]` des B-Blocks gelten nicht im Betriebsmodus `dangerous`** – dort trägt der Schutz-Hook (D-281); die Vorbemerkung des Blocks sagt es |
| `openai-codex` | `CP-OC` | pilot | 10 von 35 | **4 von 6** | Alle Belege stammen aus Messungen am Client, keiner aus seiner Dokumentation – das Pack trägt keine `[DOK]`-Zeile, und `FW-AK-01` ist für diesen Client nicht gefahren. Gemessen an einer realen Installation sind `B2`, `B4`, `B6`, `H1` bis `H3`, `R1`, `R5`, `S1` und `S5`; vier Zeilen sagen `BELEG OFFEN` (`S2`, `S3`, `M3`, `M4`), dazu `X2` dauerhaft. 🔴 **Zwei Kernzusagen sind `[NICHT ABBILDBAR]`** – `B3` und `B5` –, und damit greift Abschnitt 4 dieser Datei vollständig: **keine Inbetriebnahme ohne Freigabe durch `<SECURITY_CONTACT>`** |
| `kiro` | `CP-KI` | pilot | 21 von 35 | 6 von 6 | Gebaut **mit Zugang zum Client** (Kommandozeile 2.24.1, Engine V3): Gemessen an realen Installationen sind unter anderem `R1` bis `R3`, `S1`, `S2`, `S5`, `B1` bis `B8`, `H1` bis `H4` und `M4`; die Zeilen der IDE stehen auf der Dokumentation (`QK-1` bis `QK-9`, `K-162`). Fünf Zeilen sagen `BELEG OFFEN` (`A1`, `A2`, `M3`, `M7`, `X1`), dazu `X2` dauerhaft. 🔴 **Alle Zeilen des B-Blocks stehen unter der Bedingung des aktiven Agenten** – fehlt das Agentenprofil oder ist es kaputt, fällt der Client still auf seinen eingebauten Agenten zurück (Prüfung 96); die Hooks laufen nur in der interaktiven Sitzung |
| `claude-code` | `CP-CC` | pilot | 22 von 32 | 6 von 6 | teilweise – Dokumentenabgleich gegen 2.1.267 (AP2), Belegspalte nennt je Zeile die Quelle; **für sechs Zeilen liegen Messungen vor** – S3, S4, A1, die Reichweite von H2, B6 und, zur Hälfte, B2 –, für die übrigen stehen die Wirkungsnachweise aus. **Eine Zeile sagt `BELEG OFFEN`** (`M4`, die Planablage) |

## 7. Änderungsverlauf

| Version | Datum | Änderung | Autor (Rolle) |
|---|---|---|---|
| 0.1.0 | 2026-09-10 | angelegt (`CR-2026-002`) | `<FRAMEWORK_OWNER>` |
| 0.2.0 | 2026-09-10 | Semantikabbildung der Berechtigungen und Hooks ergänzt (`CR-2026-008`) | `<FRAMEWORK_OWNER>` |
| 0.3.0 | 2026-09-10 | Restduplikation zusammengeführt; ein Pack umfasst vier Dateien (`CR-2026-010`) | `<FRAMEWORK_OWNER>` |
| 0.4.0 | 2026-09-11 | **Auskunftspflicht über Quellen außerhalb des Projekts** als Schritt beim Anlegen eines Packs (`CR-2026-031`, `CR-2026-038`; D-34, D-37); die Definition von `[TECHNISCH]` nennt die Abhängigkeit vom **Betriebsmodus** (`CR-2026-033`, D-35), der B-Block jedes Packs trägt sie als Pflicht-Vorbemerkung; ein Pack umfasst noch **eine** erklärende README, die der Regelablage ist in die Laufzeit-README aufgegangen (`CR-2026-035`, D-36) | `<FRAMEWORK_OWNER>` |
| 0.5.0 | 2026-09-13 | **Die Übersicht führte zwei Zahlen, die niemand nachrechnete – beide falsch (`CR-2026-058` E7, D-71).** `claude-code` stand auf „25 von 29", während das Pack selbst einen Absatz darüber trägt, dass diese Zahl mit 0.33.0 auf **22 von 31** berichtigt wurde; `devin-desktop` auf „24 von 34" statt **20 von 36**. Prüfung 31 rechnet die Spalte künftig aus der Fähigkeitsmatrix nach. Die Zahl der offenen VERIFY-Marker entfällt hier und verweist auf das Pack: Ihre Grenze ist zur Hälfte Ermessen, und eine gezählte Zahl wäre dort eine Genauigkeit, die es nicht gibt. Neu in Schritt 6: `agent_start_tools` und seine erklärte Abwesenheit (D-70) | `<FRAMEWORK_OWNER>` |
| 0.6.0 | 2026-09-22 | 🟢 **Die Markerform ist abgeschafft; eine Zeile ohne Beleg sagt `BELEG OFFEN` mit Grund und Datum** (`CR-2026-121`, D-291). 🔴 **Der Unterschied ist keine Schreibweise, sondern die Frist:** Das Platzhalterregister schrieb der Markerform *„vor Version 1.0.0"* vor; ein Belegstand trägt keine Frist. *Eine Frage, die dauerhaft nicht beobachtbar ist, kann keine Frist einhalten* – und `X2` des Packs `devin-desktop` hat sie achtundneunzig Releases lang als Rückstand geführt (D-292) | `<FRAMEWORK_OWNER>` |
| 0.7.0 | 2026-09-23 | 🟢 **Das dritte Client Pack ist da, und mit ihm die zweite Ausgabeform der Berechtigungsdatei** (`CR-2026-133`, D-346 bis D-349). Die Regelmenge des Kerns zerfällt bei `openai-codex` in **zwei** Erzeugnisse: Pfade in einer TOML-Tabelle, Befehle in einer eigenen Regelsprache. 🔴 **Sechs Prüfungen lesen die Form `json` und erreichen dieses Pack deshalb nicht** – sie stehen seit `1.4.0` in `FORMATGEBUNDENE_PRUEFUNGEN`, und **Prüfung 87** verlangt ihre Nennung in Abschnitt 5 des Packs. *Eine Lücke, die erklärt ist, ist eine Aussage; eine, die nur besteht, ist ein blinder Fleck.* 🔴 **Und der Schutz-Hook hat bei diesem Client zunächst nichts gesperrt:** Seine Sperrform war clientgebunden, ohne dass es irgendwo stand (**Prüfung 86**, D-347) | `<FRAMEWORK_OWNER>` |
| 0.7.2 | 2026-09-25 | Die Planablage (Zeile `M4`) steht jetzt in allen drei Matrizen; bei `claude-code` und `openai-codex` als `BELEG OFFEN`. Die Zählungen der Übersicht sind nachgezogen (`CR-2026-147`, D-402, `K-149`) | `<FRAMEWORK_OWNER>` |
| 0.8.0 | 2026-09-26 | 🟢 **Das vierte Client Pack `kiro`, und mit ihm die dritte Ausgabeform der Berechtigungsdatei: ein Agentenprofil mit Fähigkeitsregeln** (`CR-2026-150`, D-414 bis D-417). Die Menge der formatgebundenen Prüfungen nennt je Eintrag die Formen, die er erreicht; sie führte 76 statt 72 (D-416) | `<FRAMEWORK_OWNER>` |

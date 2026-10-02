# Client Packs – Abbildung des Frameworks auf einen KI-Client

| Attribut | Wert |
|---|---|
| Modul-ID | `FW-CLIENT-PACKS` |
| Ebene | keine – Querschnittsschicht (siehe Abschnitt 2) |
| Version | 0.10.0 |
| Status | pilot |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |

## 1. Zweck

Koolie führt jede Regel in zwei Formen: als werkzeugneutrale Langform unter `.koolie/core/framework/` und als kompakte Laufzeitform in der Wurzel des Projekts. Die Laufzeitform gehört zu dem KI-Client, der sie lädt. Ein **Client Pack** beschreibt diese Bindung für genau einen Client und beantwortet zwei Fragen:

1. **Wohin** gehören Anweisungsdatei, Regeln, Skills, Berechtigungen, Hooks und Agentenprofile?
2. **Welche Zusagen setzt dieser Client technisch durch** – und welche bleiben eine Anweisung, der das Modell folgen kann oder nicht?

Die zweite Frage ist der Kern. Dieselbe Datenschutzregel kann bei einem Client von der Engine erzwungen werden und beim anderen nur als Text im Prompt stehen. Das Pack macht diesen Unterschied sichtbar, damit keine falsche Sicherheit entsteht.

## 2. Ein Client Pack ist keine Regelebene

Die Prioritätshierarchie (`.koolie/core/governance/PRIORITY_HIERARCHY.md`) bleibt unverändert. Ein Client Pack führt keine neue Regel ein, lockert keine bestehende und steht in keinem Konflikt mit Core, Overlay oder Packs. Es übersetzt die Ebenen 3 bis 7 in die Dateien eines Clients und dokumentiert, wie tief sie durchgesetzt werden. Widerspricht ein Pack der Langform, gilt die Langform, und das Pack wird korrigiert.

## 3. Bestandteile

| Bestandteil | Inhalt |
|---|---|
| `CLIENT_PACK.md` | Pfadabbildung, Semantikabbildung, **Fähigkeitsmatrix**, Abweichungen, Belegstand – für Menschen |
| `manifest.json` | dieselben Abbildungen maschinenlesbar für `install.py` und den Validator. Ohne Manifest ist ein Pack nicht installierbar |
| `root-template/` | nur die erklärende README der Laufzeitschicht |

Die Vorlage `_template/` enthält nur `CLIENT_PACK.md` und ist damit kein Pack; Prüfung 84 hält das fest.

Alles andere liegt einmal im Kern und wird bei der Installation in die Form des Clients gebracht:

- **Formtransformation** – gleicher Inhalt, andere Schreibweise: Regeltexte, Wurzel-Anweisung, Agentenprofil, Skills, Overlay-Laufzeitregel, Vorlagen.
- **Semantikabbildung** – andere Werkzeuge: Berechtigungen und Hooks. Ein Client trennt Ändern und Anlegen, ein anderer nicht; ein Befehlsverbot greift hier wörtlich, dort über ein Präfix.

Weil an der Semantikabbildung die Kernzusagen hängen, bricht die Installation ab, wenn eine dieser Bedingungen verletzt ist:

| Bedingung | Grund |
|---|---|
| Jede `deny`- und `ask`-Regel hat ein Zielwerkzeug | Eine weggelassene Sperre wäre eine Lockerung. Bei `allow` ist Weglassen erlaubt, es gilt dann der strengere Standard |
| Die Präfixform eines Befehlsverbots ist ein Präfix der wörtlichen Form | So ist sie mindestens so breit wie das Original |
| Bei `allow` stimmen beide Formen überein | Jede Verbreiterung wäre eine Lockerung |

## 4. Die Fähigkeitsmatrix

Jedes Pack stuft jede technische Zusage von Koolie in eine von drei Klassen ein:

| Klasse | Bedeutung |
|---|---|
| `[TECHNISCH]` | Der Client erzwingt die Zusage, unabhängig vom Verhalten des Modells – nicht unbedingt unabhängig vom Betriebsmodus. Wovon sie im Betriebsmodus abhängt, sagt die Vorbemerkung des B-Blocks; sie ist Pflicht. |
| `[TEXTUELL]` | Die Zusage steht als Anweisung im Kontext. Das Modell kann ihr folgen; erzwungen ist sie nicht. |
| `[NICHT ABBILDBAR]` | Der Client bietet keinen Mechanismus; die Zusage entfällt für ihn. |

**Kernzusagen** sind die Zeilen des B-Blocks mit `Kern = ja` und jede Regel aus `_core_rules_integrity` der Berechtigungsdatei. Sie sagen zu, dass etwas **verhindert** wird. Alle übrigen Zeilen sind **Fähigkeitszusagen**: Sie sagen zu, dass etwas **möglich** ist, etwa nachzusehen. Fällt eine Kernzusage aus, fehlt eine Schranke; fällt eine Fähigkeitszusage aus, fehlt Sicht. Nur das Erste sperrt die Inbetriebnahme.

Daraus folgt:

- Eine Kernzusage, die ein Client nicht `[TECHNISCH]` abbildet, MUSS im Pack begründet und im Overlay des Projekts als Ausnahme geführt werden (`.koolie/project-overlay/exceptions/EXCEPTIONS.md`).
- Ein Pack mit einer Kernzusage auf `[NICHT ABBILDBAR]` DARF nur mit Freigabe durch `<SECURITY_CONTACT>` in Betrieb gehen.
- Eine Fähigkeitszusage auf `[NICHT ABBILDBAR]` MUSS in ihrer Zeile den Ersatz nennen oder festhalten, dass es keinen gibt (Prüfung 25).
- `[TECHNISCH]` MUSS an einer realen Installation belegt sein. Bis dahin sagt die Belegzelle `BELEG OFFEN` mit Grund und Datum. Ein Belegstand hat keine Frist: Er sagt, was heute belegt ist.
- Eine Zeile mit `[DOK]` nennt im Belegkopf – der Zelle bis zum ersten Satzbruch – die Kennung ihrer Quelle aus Anhang 31.4 (`QC-n`, `QD-n` …). Ein Verweis wie *„wie B3"* erbt die Kennung seines Ziels. Gibt es keine Quelle, steht `QUELLE NICHT ZUGEORDNET` mit Grund und Datum; geraten wird nicht (Prüfung 73).
- `[DOK]` belegt gegen die Dokumentation des Herstellers. Ein Nachweis von Koolie über sich selbst – ein Manifestfeld, eine erzeugte Datei – trägt die Marke nicht.
- Eine Matrixzeile steht in ihrer Tabelle, ohne Leerzeile oder Fremdtext davor (Prüfung 74).

Die Delegationsverbote V1 bis V12 (`.koolie/core/framework/core/09-risk-model.md`) sind ausgenommen. Sie betreffen Aufgaben, nicht Werkzeuge, und sind bei jedem Client `[TEXTUELL]`.

## 5. Ein Client Pack erstellen

1. `_template/CLIENT_PACK.md` nach `<client-name>/` kopieren und alle Platzhalter ersetzen. `manifest.json` und `root-template/` entstehen in eigenen Schritten.
2. **Pfadabbildung** eintragen: Wo erwartet der Client Anweisungsdatei, Regeln, Skills, Berechtigungen und Hooks?
3. **Fähigkeitsmatrix** ausfüllen. Jede Zeile ohne Beleg sagt `BELEG OFFEN` mit Grund und Datum. Der B-Block bekommt die Vorbemerkung zur Abhängigkeit vom Betriebsmodus, mit eigenem Belegstand. Keine Prüfung meldet, wenn sie fehlt.
4. **`root-template/`** anlegen, mit nichts als der erklärenden README der Laufzeitschicht. Alles andere kommt aus dem Kern; `seed_paths` bleibt leer.
5. **`manifest.json`** anlegen. Pflicht sind `client`, `skills_dir`, `pack_runtime_dir`, `core_skill_prefix` (`koolie-`), `core_paths` und `seed_paths`; dazu kommen `runtime_dir`, `root_instruction_file`, `permissions_file`, `agents_dir` und `has_rule_triggers`. Kennt der Client eine eigene Bedingungssprache für Regeldateien, bildet `rule_triggers` jeden Ladetrigger des Kerns darauf ab – ein Trigger ohne Eintrag lässt die Installation scheitern.
6. **Semantikabbildung** eintragen:
   - **Berechtigungen:** `permission_tools`, `permission_tools_bare`, `permission_path_prefix`, `permission_exec_match`, bei Bedarf `permission_exec_suffix`, `permissions_extra` und `permissions_note`.
   - **Hooks:** `hook_tools` mit jedem Werkzeugverb der Hook-Quelle, auch `search`, und `hook_project_dir_var`. Hat der Client für ein Verb kein Werkzeug, steht das in `hook_tools_absent` samt `_hook_tools_absent_note`; dann ist das Verb auch in `permission_tools` leer (Prüfung 26). Hat der Client keine eigene Hook-Datei, zeigt `<HOOKS_FILE>` auf dieselbe Datei wie `<PERMISSIONS_FILE>`.
   - **Skill-Frontmatter:** Verwirft das Pack ein zusagentragendes Feld (`permissions`, `triggers`) über `skill_frontmatter.drop_fields`, nennt es den Ersatz in `skill_permissions_ersatz` beziehungsweise `model_invocation_field` (Prüfung 27).
   - **Unteragenten:** `agent_start_tools` führt jede Schreibweise des Werkzeugs, das einen Unteragenten startet – gemessen, nicht angenommen. Gibt es keines oder ist es unerhoben, steht das in `agent_start_tools_absent` samt Notiz. Eine Zeile **A1** auf `[TECHNISCH]` braucht das Werkzeug (Prüfung 34).
   - **Werkzeugnamen im Frontmatter:** `skill_frontmatter.tool_names` und `agent_frontmatter.tool_names` führen jedes Verb aus `clientmap.FRONTMATTER_VERBEN` (`read`, `grep`, `glob`, `edit`, `exec`). Ein Verb, das der Client nicht abbildet, steht in `tool_names_unmapped` samt Notiz. Hat der Client für das Frontmatter einen eigenen Namensraum, sagt das `tool_names_namespace` samt `_tool_names_note`. `hook_tools` darf für kein Verb enger sein als `tool_names` – sonst wäre ein Werkzeug vorab freigegeben, das die Sperre nicht erfasst (Prüfung 38).
   - `<CORE_DIR>` bleibt unbelegt; den setzt die Installation.
7. **Quellen außerhalb des Projekts** eintragen: je bekannter Quelle eine Zeile mit Pfad, Ladebedingung, Belegstand und Maßnahme – oder ein datierter Abwesenheitsbeleg mit Erhebungsweg (*„keine bekannt, Stand `<JJJJ-MM-TT>`, erhoben mit `<Kommando>`"*). Gemeint sind Regeltexte, Skills und Agentenprofile ebenso wie Berechtigungen, Hooks und Einstellungen; Prüfung 19 verlangt den Abschnitt. Kennt der Client eine Importsteuerung für fremde Formate, wird sie abgeschaltet und in Zeile R6 ausgewiesen.
8. Das Pack in dieser Datei und in `.koolie/core/OWNERS.md` eintragen.
9. In ein leeres Verzeichnis installieren, den Validator laufen lassen und die Basistests des Testkatalogs gegen eine Installation des Clients fahren.

## 6. Verfügbare Client Packs

> Die Spalte `[TECHNISCH]` rechnet Prüfung 31 aus der Fähigkeitsmatrix des Packs nach.

| Pack | Code | Status | `[TECHNISCH]` | Kernzusagen | Fähigkeitsmatrix belegt |
|---|---|---|---|---|---|
| `devin-desktop` | `CP-DD` | pilot | 21 von 36 | 6 von 6 | An einer Installation gemessen sind unter anderem `S3`, `B3`, `B10`, `A1`, `H1`, `H2`, `R5`, `R6` und `S5`. Genau eine Zeile sagt `BELEG OFFEN`, und dauerhaft: `X2`. ⚠️ **Die Einstufungen `[TECHNISCH]` des B-Blocks gelten nicht im Betriebsmodus `dangerous`** – dort trägt der Schutz-Hook; die Vorbemerkung des Blocks sagt es |
| `openai-codex` | `CP-OC` | pilot | 10 von 35 | **4 von 6** | Alle Belege stammen aus Messungen am Client, keiner aus seiner Dokumentation – das Pack trägt keine `[DOK]`-Zeile, und `FW-AK-01` ist für diesen Client nicht gefahren. Gemessen an einer realen Installation sind `B2`, `B4`, `B6`, `H1` bis `H3`, `R1`, `R5`, `S1` und `S5`; vier Zeilen sagen `BELEG OFFEN` (`S2`, `S3`, `M3`, `M4`), dazu `X2` dauerhaft. 🔴 **Zwei Kernzusagen sind `[NICHT ABBILDBAR]`** – `B3` und `B5` –, und damit greift Abschnitt 4 dieser Datei vollständig: **keine Inbetriebnahme ohne Freigabe durch `<SECURITY_CONTACT>`** |
| `kiro` | `CP-KI` | pilot | 21 von 35 | 6 von 6 | Gebaut **mit Zugang zum Client** (Kommandozeile 2.24.1, Engine V3): Gemessen an realen Installationen sind unter anderem `R1` bis `R3`, `S1`, `S2`, `S5`, `B1` bis `B8`, `H1` bis `H4` und `M4`; die Zeilen der IDE stehen auf der Dokumentation (`QK-1` bis `QK-9`). Fünf Zeilen sagen `BELEG OFFEN` (`A1`, `A2`, `M3`, `M7`, `X1`), dazu `X2` dauerhaft. 🔴 **Alle Zeilen des B-Blocks stehen unter der Bedingung des aktiven Agenten** – fehlt das Agentenprofil oder ist es kaputt, fällt der Client still auf seinen eingebauten Agenten zurück (Prüfung 96); die Hooks laufen nur in der interaktiven Sitzung |
| `cursor` | `CP-CU` | pilot | 20 von 35 | 6 von 6 | Gebaut **mit Zugang zum Client** (Kommandozeile 2026.09.26, unter Windows): Gemessen an realen Installationen sind unter anderem `R1` bis `R3`, `S1`, `S3`, `B1` bis `B4`, `B6` bis `B9`, `H1` bis `H4` und `M4`; die Zeilen der IDE stehen auf der Dokumentation (`QU-1` bis `QU-8`). Sieben Zeilen sagen `BELEG OFFEN` (`S4`, `S5`, `A1`, `A2`, `M3`, `M7`, `X1`), dazu `X2` dauerhaft. 🔴 **Die Pfadmuster treffen nur in der Schreibweise mit führendem `*`**, weil der Client sie mit dem absoluten Pfad vergleicht; die Schreibweise für macOS und Linux ist nicht gemessen. **Schreiben im Arbeitsbereich fragt nicht zurück** (`B7`) |
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
| 0.9.0 | 2026-09-26 | 🟢 **Das fünfte Client Pack `cursor`, und mit ihm die vierte Ausgabeform der Berechtigungsdatei: nur `allow` und `deny`, ohne jeden weiteren Schlüssel** (`CR-2026-155`, D-440 bis D-443). Mit einem Kommentarschlüssel startet der Client nicht; die Kernregeln hält **Prüfung 97** gegen die Kernquelle. Die Regelablage trägt eine eigene Endung (`rule_file_ext`) | `<FRAMEWORK_OWNER>` |
| 0.10.0 | 2026-10-02 | Abschnitte 1 bis 5 neu gefasst, knapper und ohne Entscheidungsgeschichte; Schritt 6 nach Gegenständen gegliedert; `core_skill_prefix` ist `koolie-` (`CR-2026-173`) | `<FRAMEWORK_OWNER>` |

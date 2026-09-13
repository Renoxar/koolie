# Client Pack `claude-code`

| Attribut | Wert |
|---|---|
| Modul-ID | `CP-CC` |
| Ebene | keine – Abbildungsschicht |
| Version | 0.15.0 |
| Status | entwurf |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Client | Claude Code |
| Geprüfte Clientversion | 2.1.267 (AP2-Dokumentenabgleich, `tests/protocols/2026-09-10-AP2-claude-code.md`). Die **verbindliche Zielversion** legt `<FRAMEWORK_OWNER>` fest und steht aus |
| Datum der Prüfung | 2026-09-10 – Dokumentenabgleich und Prüfung der erzeugten Artefakte; die Wirkungsnachweise in einer Sitzung stehen aus |

> **Teilweise belegt (Stand 0.6.0).** Alle zehn Pruefmarker sind gegen die
> Herstellerdokumentation der Clientversion 2.1.267 und gegen eine reale Erstinstallation
> abgeglichen (`tests/protocols/2026-09-10-AP2-claude-code.md`); die Befunde sind mit
> `CR-2026-016` und `CR-2026-017` behoben und die Einstufungen berichtigt. **Eine Einstufung
> steht auf `[NICHT ABBILDBAR]`: S5**, seit der Erhebung vom 2026-09-12 – keine Kernzusage
> (D-41), mit benanntem Ersatz in der Zeile. Kein Wirkungsnachweis aus einer laufenden Sitzung
> liegt vor: Ein Dokumentenabgleich belegt `[DOK]`, nicht beobachtete Durchsetzung.
>
> **Zur Lesart der Spalten.** Die Spalte „Einstufung" nennt die **vorgesehene** Durchsetzungstiefe, die Spalte „Beleg" ihren Nachweisstand: `[DOK]` = in der Herstellerdokumentation beschrieben, `[EMPF]` = Empfehlung des Frameworks, VERIFY-Marker = gegen die aktuelle Dokumentation beziehungsweise eine Installation zu prüfen. Solange die Zielversion nicht festgelegt und geprüft ist, gilt das Pack als **unbelegt**.

## 1. Pfadabbildung

Maschinenlesbar in `manifest.json`; diese Tabelle ist die menschenlesbare Fassung.

| Rolle des Artefakts | Pfad bei diesem Client | Belegstatus |
|---|---|---|
| Wurzel-Anweisungsdatei | `CLAUDE.md` | `[DOK]` |
| Regeldateien | `.claude/rules/*.md`; der Client findet sie selbst, auch in Unterverzeichnissen. Ohne `paths`-Frontmatter unbedingt geladen, mit `paths` bei passenden Dateien – **kein Import nötig**, siehe Abschnitt 1b | [DOK] `docs/en/memory` (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) |
| Skills | `.claude/skills/<name>/SKILL.md` | `[DOK]` |
| Subagentenprofile | `.claude/agents/<name>.md`, Frontmatter-Feld `tools` | [DOK] `docs/en/sub-agents` (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) |
| Berechtigungskonfiguration | `.claude/settings.json` (erzeugt aus `framework/runtime/permissions.json`) | `[DOK]` Mechanismus `docs/en/settings`; Mustersemantik [DOK] `docs/en/permissions` (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) – gitignore-Syntax, Einzelheiten bei B3. **Pfadregeln werden nur für `Read` und `Edit` ausgewertet**, siehe Abschnitt 7 |
| Hook-Konfiguration | `.claude/settings.json` (**keine eigene Datei**; erzeugt aus `framework/runtime/hooks.json` und in dieselbe Datei eingebettet) | `[DOK]` |
| MCP-Konfiguration | `.mcp.json` (Vorlage: `.mcp.json.example`) | `[DOK]` |
| Projektverzeichnis-Variable in Hooks | `CLAUDE_PROJECT_DIR` | `[DOK]` |
| Nutzerlokale Überschreibung | `CLAUDE.local.md`, `.claude/settings.local.json` | `[DOK]` |

## 1a. Semantikabbildung der Berechtigungen und Hooks

Die Regelmenge liegt werkzeugneutral im Kern (`leitwerk-core/framework/runtime/permissions.json`, `hooks.json`) und wird bei der Installation in die Werkzeuge dieses Clients übersetzt (D-18). Was dabei abgebildet wird, steht maschinenlesbar im `manifest.json`; diese Tabelle ist die menschenlesbare Fassung. Dieser Client ist der Grund, weshalb es die Abbildungsschicht überhaupt braucht: Vier der sechs Zeilen sind keine Umbenennung, sondern eine andere Mengenlehre.

| Neutrales Werkzeugverb | Werkzeug bei diesem Client | Anmerkung |
|---|---|---|
| `read` | `Read(muster)` | |
| `search` | – | Die eigenen Suchwerkzeuge (`Grep`, `Glob`) werten **keine** Pfadregeln aus; seit `CR-2026-016` wird für dieses Verb keine Regel erzeugt. **Eine `Read(**)`-Regel deckt sie nicht mit ab** – das stand hier bis 0.29.0 und ist widerlegt: Eine Suche über einen Secret-Pfad passierte beide Schichten (B04, Lauf B04-5). Den Kanal trägt seit 0.30.0 der Schutz-Hook über `hook_tools.search`, nicht die Berechtigungsdatei (`CR-2026-047`, D-47) |
| `write` | `Edit(muster)` | Ändern und Anlegen sind zwar getrennte Werkzeuge, eine **Pfadregel** wertet der Client aber nur für `Read` und `Edit` aus. Bis `CR-2026-016` erzeugte die Abbildung zusätzlich `Write(muster)` – 17 wirkungslose Regeln je Installation (AP2-CC-02) |
| `exec` | `Bash(präfix:*)` | präfixbasiert statt wörtlich – die Sperre ist damit breiter |
| `fetch` | `WebFetch`, `WebSearch` | zwei Werkzeuge, beide ohne Muster |
| `mcp` | `mcp__*` | ohne Muster |

| Weitere Eigenschaft | Wert |
|---|---|
| Name ohne Verzeichnisanteil | mit Wurzelangabe (`./.env`) |
| Zusätzliche Schlüssel | `defaultMode: default` |
| Hook-Werkzeugnamen | `Bash`, `Edit`, `Write`, `NotebookEdit` |
| Projektverzeichnis im Hook-Befehl | `$CLAUDE_PROJECT_DIR` |

Zwei Zusicherungen sichern die Abbildung ab, statt sich auf Sorgfalt zu verlassen: Eine `deny`- oder `ask`-Regel ohne Zielwerkzeug lässt die Installation scheitern, und die Präfixform eines Befehlsverbots muss ein Präfix seiner wörtlichen Form sein – damit ist sie nachweislich mindestens so breit. Bei `allow` ist jede Verbreiterung unzulässig.

## 1b. Semantikabbildung der Ladebedingungen

Die Regeltexte liegen werkzeugneutral im Kern (`leitwerk-core/framework/runtime/rules/`, dazu die Regelvorlagen und die Laufzeitfassungen aktivierter Packs) und tragen dort einen **Ladetrigger**. Dieser Client kennt für Regeldateien genau eine Bedingung: die Bindung an Dateimuster über das Frontmatter-Feld `paths`. Die Abbildung steht maschinenlesbar im `manifest.json` unter `rule_triggers`; diese Tabelle ist die menschenlesbare Fassung.

| Ladetrigger der Kernquelle | Fassung bei diesem Client | Ladeverhalten | Bewertung |
|---|---|---|---|
| `always_on` | kein `paths`-Feld | bei jedem Sitzungsstart | wörtliche Entsprechung |
| `model_decision` | kein `paths`-Feld | bei jedem Sitzungsstart | **Verschärfung** – mehr Regeln aktiv, nicht weniger; sie kostet Kontext, kein Schutzniveau |
| `glob` mit `globs` | `paths:` mit denselben Mustern | sobald der Client eine passende Datei liest | wörtliche Entsprechung |
| `manual`, `agent` | **keine Abbildung** | – | Die Installation scheitert. Kein Kernartefakt nutzt sie; eine künftige Regel, die es täte, erzwingt damit eine Entscheidung, statt ihre Ladebedingung stillschweigend zu verlieren |

Zwei Zusicherungen sichern auch diese Abbildung ab: Ein Ladetrigger ohne Eintrag lässt die Installation scheitern (D-27), und ein Ladetrigger, der auf `paths` abbildet, muss Dateimuster mitbringen – eine leere Ladebedingung wäre keine. Der Validator prüft die **installierte** Fassung gegen die Felder, die dieser Client auswertet: Ein stehen gebliebenes `trigger:` oder `globs:` ist ein Fehler, und eine Kernregel (`00-`, `10-`, `15-`, `20-`) darf kein `paths` tragen – sie gilt für jede Aufgabe, eine Ladebedingung wäre dort eine Lockerung.

`description` ist für Regeldateien dieses Clients **nicht** dokumentiert und entfällt deshalb im Frontmatter (K-18). Zweck, Ladeverhalten und der Ladetrigger der Kernquelle stehen stattdessen in einem HTML-Kommentar oberhalb des Regeltextes. Für `CLAUDE.md`-Dateien ist dokumentiert, dass Block-Kommentare vor dem Einspeisen entfernt werden; für Regeldateien ist das **nicht** dokumentiert. Der Kommentar ist deshalb knapp gehalten und zählt hier vorsorglich zum ständigen Kontext.

## 2. Fähigkeitsmatrix

**Zur Belegspalte.** Wo eine Zeile mit AP2 belegt ist, nennt sie die Seite der Herstellerdokumentation, auf die sie sich stützt – `docs/en/memory`, `permissions`, `skills`, `sub-agents` oder `settings` unter `code.claude.com`, sämtlich abgerufen am 10.09.2026 gegen Clientversion 2.1.267. Damit ist jede Zeile einzeln nachprüfbar, ohne den Umweg über das Protokoll. Welche Seite darüber hinaus wofür herangezogen wurde, steht im Hauptdokument in Anhang 31.4.2.

### R – Regelladung

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| R1 | Wurzel-Anweisungsdatei wird ungefragt geladen | `CLAUDE.md` wird zu Beginn jeder Sitzung geladen | `[TECHNISCH]` | `[DOK]` |
| R2 | Regeldateien mit Ladebedingungen | `.claude/rules/*.md`: ohne `paths`-Frontmatter unbedingt geladen, mit `paths` nur bei passenden Dateien. Der Client kennt **eine** Bedingung, die Kernquelle drei Ladetrigger; `model_decision` bildet deshalb auf unbedingtes Laden ab – eine Verschärfung, siehe Abschnitt 1b | `[TECHNISCH]` | [DOK] `docs/en/memory` (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) |
| R3 | Regeln an Dateimuster bindbar (Grundlage der Technology Packs) | `paths:` im Frontmatter bindet eine Regel an Glob-Muster; mehrere Muster und Klammer-Expansion sind zulässig. Ein Technology Pack liegt damit als `.claude/rules/40-tech-<name>.md` und lädt bei den Dateien seiner Technologie. Grenzen: Abschnitt 5 | `[TECHNISCH]` | [DOK] `docs/en/memory` (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) |
| R4 | Bekanntes Zeichenlimit, das das Framework einhalten kann | **4 MiB** je Anweisungsdatei; eine größere Datei wird übersprungen. Zusätzlich als Empfehlung 200 Zeilen | `[TECHNISCH]` | [DOK] `docs/en/memory` (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) |
| R5 | Die geladenen Regelquellen sind vollständig aufzählbar | Kein Kommando dieses Clients führt die wirksamen Regelquellen auf. Was es gibt, ist die **Selbstauskunft der Sitzung**: Gefragt nach ihrem geladenen Bestand zählte sie zwei `CLAUDE.md`, vier Regeldateien und die README der Regelablage auf. Die vollständige Auskunft des Frameworks steht in Abschnitt 8 dieses Packs | `[TEXTUELL]` | `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>` für einen **technischen** Aufzählungsweg. Die Selbstauskunft ist am 2026-09-11 gegen 2.1.268 beobachtet (K-22, K-26) und traf zu – sie ist aber Modellverhalten, kein Mechanismus: Sie entsteht nur auf Nachfrage und ist nicht nachprüfbar, ohne den Kontext ein zweites Mal zu messen |
| R6 | Keine Importe fremder Werkzeugformate | Der Client kennt `claudeMdExcludes`, das Anweisungs- und Regeldateien über Glob-Muster vom Laden ausnimmt. **Das Framework liefert keine Vorgabe aus** (D-37): Eine `CLAUDE.md` im Elternverzeichnis ist in einem Mehrprojekt-Verzeichnis oft gewollt, ein pauschaler Ausschluss bräche legitime Anordnungen. Es bleibt bei Auskunft (Abschnitt 8) und Empfehlung | `[TEXTUELL]` | Der Mechanismus ist am 2026-09-11 gegen 2.1.268 gemessen: Drei Muster gleichzeitig nahmen die fremde Datei vom Laden aus, zwei geladene `CLAUDE.md` wurden eine (K-21). **Welches der drei Muster greift, ist nicht getrennt gemessen.** Dass hier keine Vorgabe steht, ist eine Entscheidung, kein fehlender Beleg |

### S – Skills

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| S1 | Versionierte Skills im Repository | `.claude/skills/<name>/SKILL.md` mit Frontmatter | `[TECHNISCH]` | `[DOK]`; zusätzlich **beobachtet** (siehe Abschnitt 6) |
| S2 | Gezielter Aufruf | Aufruf über den Skill-Namen mit vorangestelltem Schrägstrich | `[TECHNISCH]` | `[DOK]` |
| S3 | Werkzeugbeschränkung je Skill | **`disallowed-tools` im Skill-Frontmatter.** Die Installation bildet `permissions.deny` der Quelle darauf ab: die groben Verben `edit` und `exec` über `hook_tools` auf `Edit, Write, NotebookEdit` und `Bash` (D-65). `allowed-tools` trägt die Zusage **nicht** – es ist eine Vorabfreigabe für den aufrufenden Turn, keine Beschränkung (B01), und wird deshalb bewusst nicht dafür verwendet. **DREI GRENZEN, und sie gehören in diese Zeile:** (1) **Turnbereich** – die Sperre gilt nur für den aufrufenden Turn; Turn 2 derselben Sitzung konnte wieder schreiben. Ein „nur lesender" Skill ist nur *während seines Turns* nur lesend, das ist **keine Betriebsart**. (2) **Aufzählend** – was nicht in der Liste steht, ist offen; mit gesperrtem `Write, Edit` schrieb der Skill über `Bash`. (3) **Keine Argumentmuster** – befehlsgenaue Verbote sind nicht ausdrückbar, und ein Eintrag mit Klammer wirkt **lautlos gar nicht**. Betroffen sind fünf der zwölf Skills, ungleich: **`fw-change-small`, `fw-refactor`, `fw-tests` bekommen gar keine Schranke je Skill**, **`fw-mr-description` und `fw-review-support` eine teilweise** – ihre Editierwerkzeuge sind gesperrt, ihre `git`-Verbote nicht. Für sie trägt weiter die **globale** Berechtigungsschicht samt Schutz-Hook, die unabhängig vom Skill wirkt. **REICHWEITE, gemessen am 2026-09-13** (`tests/protocols/2026-09-13-erhebung-unteragent.md`, D-67): Die Sperre gilt auch für einen **Unteragenten**, den der Skill startet. Ein Unteragent mit einem Profil **ohne** eigenes `tools`-Feld hatte `Write` und `Edit` nicht im Vorrat; der Kontrolllauf mit demselben Skill ohne das Feld schrieb. **Der Unteragent ist kein Umgehungsweg.** Grenze 2 reicht allerdings mit: Mit gesperrtem `Write, Edit` schrieb der Unteragent über `Bash`. **Nicht gemessen:** Hintergrund-Unteragenten – alle Läufe fuhren mit `run_in_background: False` – und zwei Ebenen tief | `[TECHNISCH]`, mit drei benannten Grenzen | **Gemessen am 2026-09-13** (`tests/protocols/2026-09-13-erhebung-disallowed-tools.md`), neun Läufe mit Kontrolllauf, Positivkontrolle und Rekorder-Hook: Ein Skill mit `disallowed-tools: Write, Edit` **konnte nicht schreiben – obwohl `Write` in der `allow`-Liste stand**; derselbe Skill ohne das Feld konnte es. `disallowed-tools` schlägt also eine ausdrückliche Freigabe und ist genau das, was `allowed-tools` nach **B01** nicht ist. Bis 0.34.0 galt diese Zeile als nicht abbildbar, mit dem Satz „nicht erhoben, deshalb hier nicht zugesagt" (`CR-2026-050`, D-50) – **das war nach dem damaligen Belegstand richtig und ist mit der Erhebung überholt** (`CR-2026-057`, D-64). Nach D-41 ist S3 eine **Fähigkeitszusage**; ihr Ausfall sperrt die Inbetriebnahme nicht |
| S4 | Schreibende Skills nur benutzergetriggert | `disable-model-invocation: true` verhindert, dass das Modell den Skill selbst lädt, und hält zusätzlich seine Beschreibung aus dem Kontext; die Installation setzt das Feld für jeden Skill, dessen Quelle `triggers` ohne `model` nennt (9 von 12). Ergänzend wirkt `ask` auf `Edit(**)`: jede Schreiboperation löst eine Rückfrage aus | `[TECHNISCH]` | [DOK] `docs/en/skills` (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`); **beobachtet am 2026-09-12** (`tests/protocols/2026-09-12-erhebungen-K28-S5-B9-bypass.md`): Von zwölf Skills führte die Sitzung genau die drei **ohne** das Feld; die neun mit dem Feld standen nicht in ihrem Kontext, waren als Aufruf mit vorangestelltem Schrägstrich aber vorhanden. Der Wirkungsnachweis steht damit nicht mehr aus. **Reichweite:** Die Zusage gilt für die Skill-Ablage, die das Framework schreibt. Skills aus Ablagen außerhalb des Repositoriums unterliegen diesen Konventionen nicht; sie sind nach Regel 2.6 der Prioritätshierarchie ebenenlos und dürfen den Handlungsspielraum nur einschränken (`CR-2026-032`) |
| S5 | Die geladenen Skills sind vollständig aufzählbar, samt Herkunft und Aufrufbarkeit | **Keiner.** `claude --help` kennt keinen Unterbefehl für Skills, `claude doctor` nennt keine Skill-Pfade; die Sitzung erhält Skills als Name und Kurzbeschreibung **ohne Pfad** | `[NICHT ABBILDBAR]` | **Erhoben am 2026-09-12** (`tests/protocols/2026-09-12-erhebungen-K28-S5-B9-bypass.md`). Zwei Teilantworten. **Fremde Skill-Ablagen führt dieser Client nicht mit:** Vier gleich gebaute Sonden in `.devin/skills/`, `.windsurf/skills/`, `.cursor/skills/` und `~/.devin/skills/` blieben sämtlich ungeführt, die fünfte in der eigenen Ablage wurde geführt (Positivkontrolle im selben Lauf). Die Gegenrichtung zu `AP2-DD-16` fällt damit entgegengesetzt aus; ein Import ist hier ein ausdrücklicher Befehl (`claude import`), kein stilles Mitführen. **Die Aufzählbarkeit selbst ist nicht eingelöst:** Die Sitzung antwortete auf die Frage nach der Herkunft wörtlich „Herkunft unbekannt — für alle 84", und ihre Liste ist zudem konstruktionsbedingt unvollständig (S4). Die nutzerglobale **eigene** Ablage `~\.claude\skills\` lädt in jedes Projekt mit – 67 Skills in einer Sitzung, deren Projekt keinen davon enthält; sie fällt unter den Auskunftsabschnitt nach D-34. **Ersatz: `python leitwerk-core/install.py --client claude-code --root <projekt> --list-skills`** – Name, Herkunft, Aufrufbarkeit und Pfad je Skill dieser Installation (`CR-2026-041` E3, D-42). **Kein vollständiger Ersatz, und die Ausgabe sagt das selbst:** Skills aus Ablagen außerhalb des Projektverzeichnisses sieht auch das Framework nicht – also genau die 67, um die es hier geht. Nach D-41 ist S5 eine **Fähigkeitszusage**; ihr Ausfall sperrt die Inbetriebnahme nicht |

### B – Berechtigungen

> **`[TECHNISCH]` heißt in diesem Block:** Die Engine setzt die Regel durch, **solange der Betriebsmodus die Berechtigungsprüfung nicht abschaltet.** Im Modus ohne Rückfragen, den D-05 untersagt, ist diese Linie aus; dann trägt allein der Schutz-Hook (D-35). **Für diesen Client trifft das nicht zu – erhoben am 2026-09-12** (`tests/protocols/2026-09-12-erhebungen-K28-S5-B9-bypass.md`; die Auflage E5 zu `CR-2026-033` ist damit erfüllt). Drei Läufe mit dem Bypass-Schalter der Befehlszeile, der Modus in der Hook-Aufzeichnung als `bypassPermissions` belegt: Die Verweigerungsregeln griffen **auch dort** – für das Lesewerkzeug und für den Shell-Befehl (E1). Nimmt man sie ganz weg, trägt der Schutz-Hook allein, ebenfalls für beide Werkzeuge (E2). Ein Kontrolllauf ohne beide Schranken las die Datei anstandslos (E0) und macht die anderen zwei erst zu Messungen. **Beide Linien halten hier also gemeinsam, wo sie beim anderen Pack nacheinander fallen.** Hinzu kommt, dass der Modus bei diesem Client sperrbar ist (`permissions.disableBypassPermissionsMode`, `AP2-CC-05`) und in verwalteten Einstellungen unüberschreibbar. D-05 bleibt unberührt: Der Lauf war Testnachweis, kein Betriebszustand.

| ID | Zusage des Frameworks | Kern | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|---|
| B1 | Berechtigungen versioniert im Repository | ja | `.claude/settings.json` | `[TECHNISCH]` | `[DOK]` |
| B2 | Verweigern vor Rückfragen vor Erlauben | ja | `permissions.deny` / `.ask` / `.allow` | `[TECHNISCH]` | `[DOK]` |
| B3 | Secret-Dateien per Pfadmuster lesegeschützt | ja | Verweigerungsregeln auf `./.env`, `**/*.pem`, `**/secrets/**` und weitere. Mustersemantik: gitignore-Syntax; ein bloßer Dateiname trifft in jeder Tiefe (`Read(.env)` ist gleichbedeutend mit `Read(**/.env)`); ein einsegmentiges Verzeichnismuster trifft in `deny` und `ask` in jeder Tiefe, in `allow` nur am verankerten Ort. Unter Windows werden Pfade vor dem Vergleich auf POSIX-Form normalisiert. **Je Kanal:** direktes Lesen **wirkt** (Regel und Hook); Shell **wirkt** (der Schutz-Hook zerlegt den Befehl in Tokens); **Suche wirkt seit 0.30.0 – allein über den Hook**, weil dieser Client für `Grep` und `Glob` keine Pfadregeln auswertet (`AP2-CC-02`); Unterprozess **nicht nachgewiesen** | `[TECHNISCH]` für Lesen, Shell und Suche; `[TEXTUELL]` für den Unterprozess | [DOK] `docs/en/permissions` (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`). **Reichweite je Kanal gemessen am 2026-09-12** (`tests/protocols/2026-09-12-B04-B05-gegenpruefung.md`, B04): Vor 0.30.0 passierte eine Suche über einen Secret-Pfad beide Schichten (Lauf B04-5); der Hook-Eintrag schließt den Kanal, nachgewiesen mit zwei Sonden und zwei Gegenproben |
| B4 | Framework- und Overlay-Artefakte schreibgeschützt | ja | Je Pfad **eine** `Edit(...)`-Regel; das Kernverzeichnis ist seit `CR-2026-012` als Ganzes erfasst (`Edit(leitwerk-core/**)`). Eine zusätzliche `Write(...)`-Pfadregel wäre wirkungslos und wird seit `CR-2026-016` nicht mehr erzeugt. **Je Kanal:** direktes Schreiben **wirkt** (Regel und Hook); **Shell und Unterprozess wirken nicht** – die Berechtigungsdatei führt für `exec` ausschließlich Befehlsverbote und keine einzige Pfadregel, und der Schutz-Hook prüft das Kernverzeichnis nur bei schreibenden Werkzeugen. Was den Shell-Schreibweg aufhält, ist die Regelschicht | `[TECHNISCH]` für das direkte Schreiben; **`[TEXTUELL]` für Shell und Unterprozess** | wie B3. **Reichweite je Kanal gemessen am 2026-09-12** (`tests/protocols/2026-09-12-B04-B05-gegenpruefung.md`, B04): `sed -i … <kern>/VERSION`, ein Änderungsskript mit Kernpfad und eine Umleitung in die Wurzel-Anweisungsdatei passieren den Hook sämtlich (B04-1 bis B04-3). **Eine technische Durchsetzung bräuchte eine Isolationsschicht des Betriebssystems; deren Reichweite ist auf dieser Plattform unerhoben** |
| B5 | CI-, Quality-Gate- und Lockdateien schreibgeschützt | ja | dito, je Pfad eine `Edit(...)`-Regel. **Je Kanal wie B4:** direktes Schreiben wirkt, Shell und Unterprozess nicht | `[TECHNISCH]` für das direkte Schreiben; **`[TEXTUELL]` für Shell und Unterprozess** | wie B4 |
| B6 | Befehle per Muster verweigerbar | ja | Präfixmuster, z. B. `Bash(git push:*)`. Wirkt **breiter** als eine Verweigerung des vollständigen Befehls | `[TECHNISCH]` | wie B3 |
| B7 | Schreiboperationen fragen zurück | – | `ask` auf `Edit(**)` | `[TECHNISCH]` | `[DOK]` |
| B8 | Netzwerkzugriff standardmäßig unterbunden | – | Verweigerung der Abrufwerkzeuge sowie der Befehle `curl`, `wget`, `ssh` und `scp`. **Je Kanal:** die Abrufwerkzeuge **wirken** (`deny` auf das Abrufverb); der Shell-Kanal **nur für diese vier Programme** – jedes andere netzfähige Programm (`python`, `node`, `git`, Bordmittel der Shell, ein eigenes Skript) ist nicht erfasst. **Die Liste wird bewusst nicht verlängert:** Jedes ergänzte Programm suggeriert eine Vollständigkeit, die ein Befehlsmuster nicht herstellen kann | `[TECHNISCH]` für die Abrufwerkzeuge; **`[TEXTUELL]` für den Shell-Kanal** | `[DOK]`. **Reichweite je Kanal gemessen am 2026-09-12** (`tests/protocols/2026-09-12-B04-B05-gegenpruefung.md`, B04) (Lauf B04-6). Wer eine vollständige Netzsperre braucht, betreibt den Agenten ohne automatische Befehlsausführung |
| B9 | Nutzerlokale Konfiguration kann nur verschärfen | – | `.claude/settings.local.json` rangiert **über** der Projektdatei, kann eine dort gesetzte Verweigerung aber nicht aufheben: „If a tool is denied at any level, no other level can allow it." Ergänzend greifen `deny`- und `ask`-Regeln sofort, `allow`-Regeln erst nach dem Vertrauen in den Ordner | `[TECHNISCH]` für die Verweigerungen; `[TEXTUELL]` für den Rest | [DOK] `docs/en/permissions, docs/en/settings` (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`); **beobachtet am 2026-09-12** (`tests/protocols/2026-09-12-erhebungen-K28-S5-B9-bypass.md`), fünf Läufe gegen die **nutzerglobale** Datei `~/.claude/settings.json`, jeder mit Positivkontrolle: Projekt `deny` gegen Benutzer `allow` – nicht gelesen; Projekt `allow` gegen Benutzer `deny` – nicht gelesen; **ohne jede Verweigerung gelesen** (Kontrolllauf, ohne den die anderen nichts bedeuten). Ebenso wirkungslos blieb ein nutzerglobales `defaultMode: bypassPermissions`, mit und ohne projektseitiges `defaultMode`. **Die Zusage bestätigt sich – und das ist bemerkenswert, weil dieselbe Frage beim anderen Pack das Gegenteil ergab** (`ERH-11`, K-27: dort setzt sich die Benutzerkonfiguration in beide Richtungen durch). Gemessen sind die Mechaniken `deny` und `defaultMode`; für Verschärfungen anderer Art gilt die Aussage nicht |
| B10 | Externer Abruf auf freigegebene Domains beschränkbar | – | **Keiner.** Die Abbildung führt die Abrufwerkzeuge in `permission_tools_bare`: Ein Muster wird verworfen, die erzeugte Regel lautet `WebFetch` und `WebSearch` **ohne Argument** – das ganze Werkzeug, nicht ein Ziel. Eine Domain-Angabe ist damit nicht ausdrückbar. **Ersatz:** das vollständige Verbot, das dadurch entsteht und als Verbot `[TECHNISCH]` wirkt (B8) – es ist **strenger** als die Zusage, nicht schwächer, und deshalb kein Schutzverlust. Für eine Websuche gibt es überhaupt kein Domain-Ziel; auch ein künftiger Mechanismus könnte sie nicht abdecken (Paket 6) | `[NICHT ABBILDBAR]` | `[DOK]` für die Abbildung (`permission_tools_bare` im Manifest, erzeugte Datei nachgeprüft am 2026-09-13). Seit 0.33.0 sagt der Kern diese Beschränkung nicht mehr zu (B11, D-59) |

### H – Hooks

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| H1 | Prüfung vor Werkzeugausführung | `hooks.PreToolUse` in `settings.json`, Matcher auf **lesende**, schreibende und ausführende Werkzeuge | `[TECHNISCH]` | `[DOK]`; das Lesewerkzeug seit 0.25.0 (`CR-2026-030`, D-33) – bis dahin erreichte ein Lesezugriff den Hook nicht |
| H2 | Prüfung kann **blockieren** | Exit-Code 2 des Hook-Befehls blockiert die Ausführung, und zwar **bevor** die Berechtigungsregeln ausgewertet werden – ein blockierender Hook geht damit auch einer `allow`-Regel vor. Umgekehrt hebt eine Hook-Entscheidung keine `deny`- oder `ask`-Regel auf. Seit 0.24.0 **fail-closed**: Das erzeugte Hook-Kommando trägt `--fail-closed`, eine Werkzeugeingabe, die der Hook nicht lesen kann, wird blockiert statt durchgelassen (D-31). **REICHWEITE, gemessen am 2026-09-13** (D-69): Der Hook erfasst auch die Werkzeugaufrufe eines **Unteragenten** und blockiert sie – nicht nur mit dem Matcher `*`, sondern auch mit der benannten Form `Edit\|Write\|NotebookEdit`, die `clientmap.py` aus `hook_tools` erzeugt. **Der Unteragent ist kein Weg am Schutz-Hook vorbei.** Ein Aufruf aus einem Unteragenten ist am Umschlag erkennbar: Er führt zusätzlich `agent_id` und `agent_type`. **Nicht gemessen:** derselbe Lauf mit dem Schutz-Hook des Frameworks in einer vollständigen Installation – gemessen ist ein synthetischer Sperr-Hook in der erzeugten Form | `[TECHNISCH]` | **Reichweite gemessen am 2026-09-13** (`tests/protocols/2026-09-13-erhebung-unteragent.md`, Läufe H1 bis H3 mit Gegenprobe); im Übrigen [DOK] `docs/en/permissions` (AP2, Clientversion 2.1.267) – **stärker belegt als beim Client Pack `devin-desktop`**, siehe Abschnitt 5 |
| H3 | Statusmeldung beim Sitzungsstart | `hooks.SessionStart` | `[TECHNISCH]` | `[DOK]` |
| H4 | Eingabeschema und Pfadidentität des Schutz-Hooks | Der Hook prüft seit 0.34.0 ein **Ereignis**: JSON-Objekt, nicht leerer `tool_name`, `tool_input` als Objekt; alles andere gilt als **unprüfbar** und blockiert hier, weil dieses Pack `hook_fail_closed: true` führt. Geprüft wird die **Operation**, nicht der Umschlag – `transcript_path`, `cwd` und `session_id` sind kein Ziel. Pfadangaben werden gegen `cwd` aufgelöst und in aufgelöster Form noch einmal gegen die Muster gehalten; alle Pfadmuster sind groß-/kleinschreibungsunempfindlich. **Grenze, und sie gehört in diese Zeile:** Ein Hook prüft **vor** dem Zugriff. Eine Verknüpfung, die zwischen Prüfung und Zugriff umgebogen wird, kann er nicht ausschließen – das kann nur die ausführende Dateischicht oder eine Isolation (`CR-2026-047` E5) | `[TECHNISCH]`, mit benannter Zeitlücke | **Gemessen am 2026-09-13** (`tests/protocols/2026-09-13-B06-gegenpruefung.md`, Befund **B06**): Das Eingabeschema dieses Clients ist an 15 Hook-Aufzeichnungen belegt. Bis 0.33.0 blockierte der Hook hier **jeden** Schreibzugriff, weil `transcript_path` unter `~/.claude/projects/` liegt – am Client nachgemessen, mit Kontrolllauf. Prüfung 32 ruft den Hook seit 0.34.0 mit dem vollständigen Umschlag auf |

### A – Agentenprofile

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| A1 | Rein lesendes Reviewprofil | `.claude/agents/fw-reviewer.md`, Frontmatter-Feld `tools` (ergänzend `disallowedTools`, das zuerst angewandt wird). **Die Beschränkung wirkt technisch, und sie wirkt als Entfernung:** Ein Profil mit `tools: Read, Grep, Glob` hatte kein Schreibwerkzeug im Vorrat, und `permission_denials` blieb **leer** – es ist keine Verweigerung, die man gegen eine Freigabe abwägt, sondern derselbe Mechanismus wie bei S3 (D-68). Eine `allow`-Regel holt das Werkzeug nicht zurück. **Weiterhin nur dokumentiert und nicht gemessen:** dass ein Profil, dessen `tools`-Liste sich zu keinem Werkzeug auflöst, gar nicht erst gestartet wird | `[TECHNISCH]` | **Gemessen am 2026-09-13** (`tests/protocols/2026-09-13-erhebung-unteragent.md`), Lauf A1-M gegen den Kontrolllauf A1-K: dasselbe Profil ohne das Feld schrieb. Zuvor `[DOK]` `docs/en/sub-agents` (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) – der Teilsatz zum Startabbruch bleibt `[DOK]` |

### M – Modi und Sitzungsfreigaben

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| M1 | Standardmodus fragt bei Schreiben und Befehlen zurück | `permissions.defaultMode` auf `default` | `[TECHNISCH]` | `[DOK]` |
| M2 | Modus ohne Rückfragen ausschließbar | Per D-05 untersagt **und** technisch sperrbar: `permissions.disableBypassPermissionsMode` auf `"disable"`, in verwalteten Einstellungen nicht überschreibbar, wirkt aber aus jeder Ebene. Zusätzlich wirken `bypassPermissions` und `auto` seit Clientversion 2.1.257 nicht mehr aus Projekt- oder nutzerlokalen Einstellungen. **Offen:** Ein Subagentenprofil kennt ein eigenes Feld `permissionMode`, das den Wert `bypassPermissions` annimmt; ob die Sperre auch dort greift, ist nicht dokumentiert (AP2-CC-12) | `[TECHNISCH]` (Sperre in verwalteten Einstellungen setzt eine Enterprise-Verwaltung voraus) | [DOK] `docs/en/permissions` (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) |
| M3 | Freigabe auf die Sitzung begrenzbar | Rückfragen bieten eine einmalige und eine sitzungsweite Bestätigung an | `[TECHNISCH]` | `[DOK]` |

### X – Externe Anbindung

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| X1 | Keine externe Anbindung ohne Einzelfreigabe | Keine `.mcp.json` ausgeliefert, nur die `.example`-Vorlage; Rückfrageregel auf alle MCP-Werkzeuge | `[TECHNISCH]` | `[DOK]` |
| X2 | Art und Ort der Codebasis-Indexierung bekannt | Kein Indexierungsmechanismus dokumentiert; Dateien werden bei Bedarf gelesen | `[TECHNISCH]` | `[DOK]` – **Abwesenheit** belegt über `docs/en/memory`, `permissions`, `skills`, `sub-agents`, `settings`, Stand 2.1.267 (AP2). Ein Beleg durch Abwesenheit bleibt schwächer als ein Beleg |

## 3. Zusammenfassung der Durchsetzungstiefe

> **Zählregel (normativ für diese Tabelle):** Eine Zeile zählt bei ihrer **schwächsten** Einstufung. Trägt sie zwei Angaben je Zugriffskanal – `[TECHNISCH]` für direktes Lesen und Schreiben, `[TEXTUELL]` für Shell und Unterprozess –, zählt sie als `[TEXTUELL]`. Das folgt D-47: Zugesagt wird je Kanal, was gemessen ist; eine Zeile, deren Zusage in einem Kanal nur als Anweisung trägt, ist nicht technisch durchgesetzt. **Bis 0.32.0 zählte dieselbe Tabelle solche Zeilen als `[TECHNISCH]`** und überzeichnete die Durchsetzungstiefe damit um vier Zeilen. Prüfung 31 rechnet die Summen seit 0.33.0 aus der Matrix nach.

| Klasse | Anzahl | davon Kernzusagen | Stand vor AP2 |
|---|---|---|---|
| `[TECHNISCH]` | 22 von 31 | 3 von 6 (B1, B2, B6) | 20 |
| `[TEXTUELL]` | 7 von 31 (R5, R6, B9; dazu B3, B4, B5, B8 – je Kanal teils technisch) | 3 von 6 (B3, B4, B5 – Shell und Unterprozess) | 2 |
| `[NICHT ABBILDBAR]` | **2 von 31** (S5, B10) | 0 | 4 |
| ohne Einstufung | 0 von 31 | 0 | – |

**Die Summen waren zwei Releases hinterher.** Die Tabelle führte bis 0.32.0 „25 von 29" und nannte als einzige nicht abbildbare Zeile S5 – S3 steht seit 0.31.0 ebenfalls dort (`CR-2026-050`), und B10 kam mit 0.33.0 hinzu. Die Spalte „Stand vor AP2" bezieht sich auf den damaligen, kleineren Zeilensatz und wird nicht fortgeschrieben.

**Der entscheidende Befund, und er ist seit D-47 kleiner als er klang:** Alle sechs Kernzusagen sind abgebildet – **drei davon technisch in jedem Kanal** (B1, B2, B6), drei nur für den direkten Zugriff (B3, B4, B5); für Shell und Unterprozess tragen sie die Regelschicht. Der Satz „alle sechs Kernzusagen sind technisch abgebildet" stand hier bis 0.32.0 und war ab 0.30.0 zu weit gefasst: Die Zeilen selbst wiesen die Kanalgrenze längst aus, die Zusammenfassung nicht. Die vier Zeilen, die bis `CR-2026-017` auf `[NICHT ABBILDBAR]` standen (R2, R3, R4, S4), waren sämtlich Unterschätzungen des Clients: `.claude/rules/` mit `paths:` bildet R2 und R3 ab, ein Zeichenlimit ist dokumentiert (R4), und `disable-model-invocation` trägt S4 (`CR-2026-016`).

**Seit dem 2026-09-12 steht wieder eine Zeile dort: S5.** Der Satz „keine Einstufung steht mehr auf `[NICHT ABBILDBAR]" hat von 0.24.0 bis 0.26.1 in diesem Pack gestanden und beschrieb ab der Erhebung einen Stand, der nicht mehr galt. Anders als die vier von damals ist S5 **keine Unterschätzung, sondern eine Messung**: Es gibt kein Aufzählungskommando. Betroffen ist **keine Kernzusage** (D-41); der Ersatz steht in der Zeile.

Ein Vergleich mit dem Client Pack `devin-desktop` trägt nicht: Dort sind 20 von 36 Zeilen als `[TECHNISCH]` **vorgesehen**, aber keine einzige Einstufung ist gegen eine Installation oder gegen die Herstellerdokumentation geprüft. Die Zahlen messen bis dahin Verschiedenes.

**Belegstand:** **Eine** Zeile trägt einen VERIFY-Marker – R5, mit 0.26.0 neu und für diesen Client nicht erhoben (bei `devin-desktop`: 9 von 36; die Angabe stand hier bis 0.35.0 als „8 von 34" und war zwei Zählungen hinterher – siehe `CR-2026-058`, Befund 6). S5 trug den zweiten; er ist am 2026-09-12 **eingelöst**, das Ergebnis ist `[NICHT ABBILDBAR]`. Bis 0.25.0 trug keine Zeile einen Marker; die beiden neuen waren kein Rückschritt, sondern zwei Fragen, die vorher nicht gestellt waren – und eine davon ist beantwortet. Offen ist eine **Teilfrage** innerhalb von M2: ob die Sperre gegen den Modus ohne Rückfragen auch für das Feld `permissionMode` eines Subagentenprofils gilt (AP2-CC-12). Zehn Zeilen sind gegen die Herstellerdokumentation der Clientversion 2.1.267 und die erzeugten Artefakte belegt. **Der Satz „beobachtete Durchsetzung in einer laufenden Sitzung ist für keine Zeile belegt" stand hier bis 0.35.0 und war überholt** (`CR-2026-058`, Befund 6): S4 ist am 2026-09-12 beobachtet, S3 am 2026-09-13 gemessen, A1 und die Reichweite von H2 mit diesem Release. **Für die übrigen Zeilen stehen die Wirkungsnachweise weiterhin aus** (`tests/protocols/2026-09-10-AP2-claude-code.md`, Abschnitt „Offen").

## 4. Kernzusagen ohne technische Durchsetzung

**Keine.** Alle sechs Kernzusagen (B1 bis B6) sind als `[TECHNISCH]` abgebildet. Ein Eintrag in dieser Tabelle ist nicht erforderlich – unter dem Vorbehalt, dass die Prüfung nach Roadmap AP2 die Einstufungen bestätigt.

Eine der sechs weicht in der **Form** ab, nicht in der Tiefe, und die Abweichung ist eine Verschärfung:

| ID | Abweichung | Wirkung |
|---|---|---|
| B6 | Befehlsverbote wirken präfixbasiert: `Bash(git reset:*)` sperrt jedes `git reset`, nicht nur `--hard` | Verschärfung, seit `CR-2026-008` nachweisbar: Die Abbildung verlangt, dass die Präfixform ein Präfix der wörtlichen Form ist, und weist sie sonst zurück. Auch unkritische Varianten sind gesperrt. Ihre Grenze nennt B6: eine andere Schreibweise desselben Befehls, etwa `git -C . push` |

Bis `CR-2026-016` stand hier eine zweite Abweichung – „B4, B5: Schreibschutz erfordert je Pfad zwei Regeln". Sie war keine: Der Client wertet eine **Pfadregel** nur für `Read` und `Edit` aus, die zusätzlich erzeugte `Write(...)`-Regel wurde nie konsultiert (AP2-CC-02).

## 5. Bekannte Abweichungen im Verhalten

- **`model_decision` lädt hier unbedingt.** Bei `devin-desktop` laden `10-privacy-security` und `15-development-rules` nur bei Relevanz. Dieser Client kennt für Regeldateien keine modellentschiedene Bedingung, nur die Bindung an Dateimuster; beide Texte sind deshalb stets geladen. Für die Regelwirkung ist das eine **Verschärfung**; für den Kontext bedeutet es rund **25.000 Zeichen** ständige Belegung (`CLAUDE.md` und die vier unbedingten Regeltexte einer frischen Installation). Least Context ist ein Prinzip zur Ergebnisqualität, keine Sicherheitszusage – die Abweichung ist deshalb vertretbar, wächst aber mit jedem unbedingt geladenen Pack. Der Validator warnt ab 40.000 Zeichen.

- **Eine pfadgebundene Regel lädt beim Lesen einer passenden Datei, nicht bei jedem Werkzeugaufruf.** Ein Technology Pack steht damit nicht schon zu Beginn der Aufgabe im Kontext, sondern erst nach der ersten Berührung einer Datei seiner Technologie. Für Regeln, die vorher gelten müssen, ist `paths` ungeeignet; sie bleiben unbedingt. Nach einer Verdichtung des Kontexts lädt eine pfadgebundene Regel erst wieder, wenn erneut eine passende Datei gelesen wird.

- **Ein Glob-Muster kann still ins Leere greifen.** Ein `[`, das sich nicht als Klammerausdruck lesen lässt (`photos [2024/**`), macht das Muster ungültig: Es trifft keine Datei, während die übrigen Muster derselben Regel weiterwirken. Die `paths`-Liste einer Regel teilt sich außerdem ein Budget von 1.000 expandierten Mustern und 4 MiB; ein Muster darüber wird unexpandiert verwendet und trifft dann ebenfalls nichts. Beides ist beim Schreiben eines Technology Packs zu beachten – die Regel meldet ihr eigenes Nichtgreifen nicht.

- **Regeldateien sind nutzerlokal ausschließbar – eine Lücke in B9.** `claudeMdExcludes` in `.claude/settings.local.json` nimmt Anweisungs- und Regeldateien über ein Glob-Muster vom Laden aus; die Listen aller Ebenen werden zusammengeführt. Das ist eine **Lockerung** und damit nach der Prioritätshierarchie unzulässig, technisch aber nicht verhindert. Die Lücke ist nicht neu und nicht an diese Ablage gebunden: Vor `CR-2026-017` hätte ein Muster auf die Wurzel-Anweisungsdatei sämtliche importierten Regeltexte auf einmal entfernt. Der KI-Client selbst kann die Datei nicht schreiben – `Edit(.claude/**)` steht in `deny` –, ein Mensch schon. Nur verwaltete Einstellungen sind gegen Ausschluss geschützt.

- **Der Schutz-Hook läuft hier fail-closed.** **Bei `devin-desktop` ebenfalls, seit 0.25.0** – hier stand bis 0.33.0, dort sei H2 `[TEXTUELL]` und das Hook-Skript laufe fail-open; beides war neun Releases lang falsch (`CR-2026-056` E9). Für diesen Client ist das Blockierverhalten über den Exit-Code dokumentiert und in einer Installation beobachtet (WN-5), das Eingabeschema damit bestätigt. Das Manifest führt deshalb `hook_fail_closed: true`, und die Abbildung hängt dem Kommando des durchsetzenden Hooks `--fail-closed` an: Eine Werkzeugeingabe, die der Hook nicht als JSON lesen kann, wird blockiert, statt ungeprüft durchzulaufen.

  **Der Schalter steht im Kommando, nicht in `env`.** Bis 0.23.0 empfahl dieser Abschnitt `FW_HOOK_FAIL_CLOSED` über `env` in `settings.json`. Das hätte die Sperre an eine zweite, für kein Pack belegte Clientzusage gehängt – dass der Client die Variable an den Hook-Prozess weiterreicht. Das Argument dagegen steht in derselben Konfiguration, die der Client ohnehin ausführt: Läuft der Hook, kommt es an (D-31). Die Umgebungsvariable wirkt weiterhin und bleibt der Weg, fail-closed ohne Neuinstallation zu erproben.

  **Beim Release-Wechsel von Hand nachzuziehen.** Weil die Hooks hier in der Berechtigungsdatei und damit in der Saat liegen, erreicht das Argument eine bestehende Installation nicht über `install.py --update`. Prüfung 17 meldet das als Fehler und nennt den Weg – die Pflicht ist damit sichtbar, nicht stillschweigend.

- **Die Berechtigungsdatei trägt hier auch die Hooks.** Weil dieser Client keine eigene Hook-Datei kennt, stehen die Hooks in derselben Datei – und die ist Saat, gehört nach der Erstinstallation also dem Projekt und wird von `install.py --update` nie überschrieben. Eine Änderung an den Hooks des Kerns erreicht ein bestehendes Projekt dieses Packs deshalb nicht von selbst; bei `devin-desktop` mit eigener Hook-Datei tut sie es. Beim Release-Wechsel ist das hier ausdrücklich zu prüfen.

- **Erledigt (`CR-2026-006` bis `CR-2026-008`).** Die zwölf `fw-*`-Skills, die Regeltexte, das Overlay und zuletzt Berechtigungen und Hooks lagen zwischenzeitlich in jedem Pack doppelt. Sie liegen jetzt einmal im Kern.

- **Das Suchwerkzeug führt Punktdateien nicht auf.** Gemessen am 2026-09-12 (ERH-12, `leitwerk-core/tests/protocols/2026-09-12-erhebungen-K28-S5-B9-bypass.md`): Zwei Muster – eines ohne und eines mit Verzeichnisdurchlauf – meldeten `No files found` für eine Datei, die im Verzeichnis lag und im selben Lauf über einen anderen Weg lesbar war; ihr Inhalt steht in drei späteren Läufen desselben Protokolls. **Das ist kein stiller Abbruch:** Das Werkzeug hat gearbeitet und ein falsches Ergebnis geliefert.

  **Folge für Nachweise.** Ein Abwesenheitsnachweis über dieses Werkzeug ist für Punktdateien keiner. Nummer 7 des Testkatalogs verlangt dafür seit `CR-2026-042` eine Anwesenheitsprobe desselben Gegenstandstyps – eine zweite Punktdatei, die gefunden werden **muss**.

## 6. Beobachtung während der Erstellung

Beim Anlegen der Skills unter `.claude/skills/` hat die Sitzung, in der dieses Pack entstand, die zwölf Skills **selbsttätig erkannt und zur Verfügung gestellt**. Das belegt S1 über die Dokumentationslage hinaus.

Dieselbe Beobachtung deckte einen Konvertierungsfehler auf: Die Skills erschienen zunächst mit einer Beschreibung, die aus dem Dateikörper statt aus dem Frontmatter stammte. Ursache war ein Rest der Devin-Frontmatter-Felder, der beim Umschreiben stehen geblieben war. Der Fehler wäre bei einer rein statischen Prüfung nicht aufgefallen – die Konvertierung prüft seitdem nach dem Umschreiben, dass nur dokumentierte Felder übrig sind.

Das ist keine Belegprüfung im Sinne des Testkatalogs und ersetzt Roadmap-AP2 nicht.

## 7. Installation und Prüfung

```text
python leitwerk-core/install.py --client claude-code
python leitwerk-core/tests/scripts/validate-framework.py
```

Vor der ersten produktiven Nutzung sind die Basistests des Testkatalogs (`leitwerk-core/tests/TEST_CATALOG.md`, Kennzeichnung „Basis") gegen diesen Client zu fahren und zu protokollieren.

### Pfadregeln nur für `Read` und `Edit` (AP2-CC-02, behoben mit `CR-2026-016`)

Der Client wertet Pfadregeln ausschließlich für `Read` und `Edit` aus: Eine Pfadregel für
`Write`, `NotebookEdit`, `Glob` oder `MultiEdit` wird angenommen, nie konsultiert und beim
Sitzungsstart als Warnung gemeldet. Bis 0.13.0 erzeugte die Semantikabbildung je Pfad
zusätzlich eine `Write(...)`-Regel – 17 wirkungslose Regeln je Installation, vier davon vom
Validator über `_core_rules_integrity.deny_must_contain` eingefordert.

Seit `CR-2026-016` bildet `write` auf `Edit` ab und `search` auf nichts; die Berechtigungsdatei
umfasst 65 statt 83 Regeln. Der Validator meldet eine Pfadregel für ein Werkzeug ohne
Pfadauswertung als Fehler (`permission_path_tools` im Manifest).

Für eine Regel **ohne** Pfad gilt die Trennung weiterhin: Eine Verweigerung des bloßen
Werkzeugnamens `Write` wirkt überall.

## 8. Anweisungs- und Konfigurationsquellen außerhalb des Projekts

Was dieser Client aus Ablagen **außerhalb des Repositoriums** lädt. Solche Quellen haben nach Regel 2.6 der Prioritätshierarchie **keine Ebene**: Sie dürfen einschränken, nie über die Ebenen 1 bis 4 hinaus erweitern und keine Governance-, Datenschutz- oder Sicherheitsregeln setzen (D-34).

**Erhebungsstand: 2026-09-11**, Clientversion 2.1.268, erhoben in einer frischen Installation in einem Temporärverzeichnis und durch Auslesen der Schlüssel der nutzerglobalen Einstellungsdatei (ohne Werte); `tests/protocols/2026-09-11-erhebungen-K21-K26.md`.

### 8.1 Anweisungsquellen

| Quelle | Ladebedingung | Belegstatus | Maßnahme des Frameworks |
|---|---|---|---|
| `<Elternverzeichnis>\CLAUDE.md` | lädt zusätzlich zur Anweisungsdatei des Projekts, in jedes darunterliegende Projekt | **Gemessen** (K-22): Ohne Einstellung lud die Sitzung **zwei** `CLAUDE.md` – die des Projekts und eine aus einem Elternverzeichnis, die mit dem Projekt nichts zu tun hat. Die Quelle ist nicht an das Benutzerprofil gebunden; ein Elternverzeichnis genügt | keine Vorgabe (R6). `claudeMdExcludes` in der Berechtigungsdatei nimmt sie aus, wenn ein Projekt das will – **empfohlen, nicht ausgeliefert** |
| `~\.claude\CLAUDE.md` | laut Herstellerdokumentation nutzerglobale Anweisungsdatei | **Nicht belegt.** Die Datei existiert auf der Messstation nicht; ob diese Ablage zusätzlich lädt, ist damit unbekannt – nicht verneint | keine |
| `~\.claude\skills\` | Skill-Ablage im Benutzerprofil | **Nicht erhoben** für diesen Client. Belegt ist nur, dass ein **anderer** Client sie mitliest (`AP2-DD-16`, 67 Skills). Offen als Teilfrage zu S5 | keine |

### 8.2 Konfigurationsquellen

Berechtigungen, Hooks und Einstellungen außerhalb des Repositoriums betreffen genau die Linien, auf denen B1 bis B6 stehen.

| Quelle | Wirkung | Belegstatus |
|---|---|---|
| `~\.claude\settings.json` (nutzerglobal) | führt **Berechtigungen und Hooks**: am 2026-09-11 sechs `allow`-Regeln sowie `SessionStart`-, `PreToolUse`- und `PostToolUse`-Hooks | **Gemessen** (ERH-07), Schlüssel ausgelesen, Werte nicht. Ein Hook von dort läuft vor jedem Werkzeugaufruf – dieselbe Stelle, an der die zweite Linie des Frameworks steht |
| `<Elternverzeichnis>\.claude\settings.local.json` | nutzerlokale Einstellungsdatei **über** dem Projekt | **Gemessen** (ERH-07) |
| Vertrauen in das Verzeichnis (`~\.claude.json`) | Ohne Vertrauen werden die `allow`-Regeln des Projekts ignoriert – der Client meldet es beim Sitzungsstart | **Gemessen** (`AP2-CC-14`, ERH-06): „Ignoring 6 permissions.allow entries from .claude/settings.json: this workspace has not been trusted." `deny`- und `ask`-Regeln sowie die Regeltexte bleiben davon unberührt |

### 8.3 Was dieser Abschnitt nicht leistet

**Eine Auskunft ist keine Schranke.** Dieser Abschnitt macht die Quellen sichtbar; er verhindert sie nicht. Das Framework liest das Benutzerprofil nicht und sperrt dort nichts.

**Ein Abwesenheitsbeleg altert.** Der Erhebungsstand oben ist am Tag der nächsten Clientversion eine Aussage über die Vergangenheit. Prüfung 19 prüft die **Anwesenheit** dieser Auskunft, nicht ihre Richtigkeit.

**Die Liste ist nicht vollständig, sie ist belegt.** Zwei der drei Anweisungsquellen oben tragen ausdrücklich „nicht erhoben" beziehungsweise „nicht belegt". Das ist ein Ergebnis, kein fehlendes Ergebnis – und es ist der Unterschied zu einem Pack, das schweigt.

## 9. Änderungsverlauf

| Version | Datum | Änderung | Autor (Rolle) |
|---|---|---|---|
| 0.14.0 | 2026-09-13 | **S3 ist zurückgewonnen – von `[NICHT ABBILDBAR]` auf `[TECHNISCH]` mit drei benannten Grenzen** (`CR-2026-057`, D-64 bis D-66). `disallowed-tools` ist **gemessen** eine echte Werkzeugsperre je Skill und schlägt sogar eine ausdrückliche `allow`-Regel; `permissions.deny` der Quelle wird darauf abgebildet, die Werkzeugnamen kommen aus `hook_tools`. Die drei Grenzen – Turnbereich, Aufzählung, keine Argumentmuster – stehen in der Zeile, im Arbeitsmodell und in der Grenzfalltabelle. **Ein Argumentmuster wirkt lautlos gar nicht**; Prüfung 33 weist es ab | `<FRAMEWORK_OWNER>` |
| 0.15.0 | 2026-09-13 | **Der Unteragent ist erhoben – drei Zeilen bekommen Belege, und zwei davon standen acht Releases auf reiner Dokumentation (`CR-2026-058`, D-67 bis D-70).** **A1** ist gemessen: Ein Profil mit `tools: Read, Grep, Glob` hatte kein Schreibwerkzeug, und `permission_denials` blieb leer – es ist eine **Entfernung aus dem Werkzeugvorrat**, keine Verweigerung. Der Teilsatz zum Startabbruch bleibt ausdrücklich `[DOK]`. **S3** trägt jetzt seine **Reichweite**: Die Sperre gilt auch für einen Unteragenten, den der Skill startet – gemessen mit Kontrolllauf –, und Grenze 2 reicht mit: Mit gesperrtem `Write, Edit` schrieb der Unteragent über `Bash`. **H2** trägt die Reichweite des Hooks: Er erfasst und **blockiert** die Aufrufe eines Unteragenten, auch mit dem benannten Matcher, den `clientmap.py` erzeugt. Neu im Manifest: `agent_start_tools` – das Startwerkzeug stand in keiner Werkzeugliste, obwohl beide Schreibweisen (`Agent`, `Task`) in der Sperre wirken. **Zwei überholte Angaben im Belegstand berichtigt** (`CR-2026-058`, Befund 6) | `<FRAMEWORK_OWNER>` |
| 0.1.0 | 2026-09-10 | angelegt (`CR-2026-004`) | `<FRAMEWORK_OWNER>` |
| 0.2.0 | 2026-09-10 | Berechtigungen und Hooks aus dem Pack in den Kern; Semantikabbildung ergänzt (`CR-2026-008`) | `<FRAMEWORK_OWNER>` |
| 0.3.0 | 2026-09-10 | Overlay-Laufzeitregel und die beiden Vorlagen in den Kern; Pack umfasst vier Dateien (`CR-2026-010`) | `<FRAMEWORK_OWNER>` |
| 0.4.0 | 2026-09-10 | **Erste Validierung gegen eine reale Installation und die Herstellerdokumentation (AP2, Clientversion 2.1.267).** Alle zehn Pruefmarker abgearbeitet: sechs belegt, zwei als ueberholt gekennzeichnet (R2/R3, S4), einer als Abwesenheitsbeleg, einer um die dokumentierte Grenze der Praefixmuster ergaenzt. Abschnitt 7 nennt die 17 wirkungslosen Regeln der erzeugten Berechtigungsdatei. Protokoll: `tests/protocols/2026-09-10-AP2-claude-code.md` | `<FRAMEWORK_OWNER>` |
| 0.5.0 | 2026-09-10 | **Drei Befunde aus AP2 behoben (`CR-2026-016`, D-26).** `triggers` wird nicht mehr ersatzlos verworfen, sondern auf `disable-model-invocation` abgebildet - die Zusage S4 gilt damit auch in der Installation. Pfadregeln werden nur noch fuer `Read` und `Edit` erzeugt: 18 wirkungslose Regeln entfallen, die Berechtigungsdatei schrumpft von 83 auf 65 Regeln. `install.py --client claude-code` gefolgt von `validate-framework.py` laeuft erstmals fehlerfrei | `<FRAMEWORK_OWNER>` |
| 0.6.0 | 2026-09-10 | **R2 und R3 abgebildet (`CR-2026-017`, D-27).** Die Regelablage liegt in `.claude/rules/`; der Client laedt sie von sich aus, die `@`-Importe der Wurzel-Anweisung entfallen. Die Ladetrigger der Kernquelle werden abgebildet statt zu Kommentar zu werden: `glob` auf `paths`, `always_on` und `model_decision` auf unbedingtes Laden. Erstmals gerendert werden auch die Regelvorlagen und die Laufzeitfassungen aktivierter Role und Technology Packs - eine aktivierte Role-Pack-Regel war bei diesem Client bisher wirkungslos. Keine Einstufung steht mehr auf `[NICHT ABBILDBAR]`; die mit `CR-2026-016` bereits behobene Zeile S4 und die Restangaben zu AP2-CC-02 in den Abschnitten 1a, 4, 5 und 7 sind nachgezogen | `<FRAMEWORK_OWNER>` |
| 0.7.0 | 2026-09-10 | **Belegspalte nennt die Quelle (`CR-2026-018`, `FW-AK-01`).** Jede mit AP2 belegte Zeile nennt die Seite der Herstellerdokumentation, auf die sie sich stuetzt; die vollstaendige Belegzuordnung steht im Hauptdokument in Anhang 31.4.2, der bis dahin ausschliesslich Devin-Quellen fuehrte. Neu aufgenommen: AP2-CC-12 (`permissionMode` im Subagentenprofil, offene Teilfrage zu M2). Genauer belegt: H2 (ein blockierender Hook geht auch einer `allow`-Regel vor), A1 (`disallowedTools` zuerst; ein Profil ohne aufloesbares Werkzeug startet nicht), S4 (die Sperre haelt die Skill-Beschreibung aus dem Kontext) | `<FRAMEWORK_OWNER>` |
| 0.8.0 | 2026-09-11 | **Der Schutz-Hook läuft fail-closed (`CR-2026-026`, D-31).** Das Eingabeschema dieses Clients ist gegen eine Installation bestätigt (AP2, WN-5); das Manifest führt deshalb `hook_fail_closed: true`, und die Abbildung hängt dem Kommando des durchsetzenden Hooks `--fail-closed` an. Eine Werkzeugeingabe, die der Hook nicht als JSON lesen kann, wird blockiert statt durchgelassen. Der Schalter steht im Kommando, nicht in `env` – die bis 0.23.0 hier empfohlene Umgebungsvariable hätte die Sperre an eine zweite, unbelegte Clientzusage gehängt. Prüfung 17 belegt die Wirkung; weil die Hooks hier in der Saat liegen, ist das Argument in einer bestehenden Installation von Hand nachzuziehen | `<FRAMEWORK_OWNER>` |
| 0.8.1 | 2026-09-11 | **Der Matcher deckt das Lesewerkzeug ab (`CR-2026-030`, D-33).** D-30 hatte entschieden, dass Secret-Pfade auch gegen lesende Werkzeuge durchgesetzt werden; eingelöst war das nie – die Hook-Quelle nannte kein Leseverb, und `hook_tools` bildete keines ab. Aufgefallen ist es bei AP2 des anderen Packs, gilt aber hier genauso: `Read` steht jetzt in der Abbildung, Prüfung 16 sondiert es | `<FRAMEWORK_OWNER>` |
| 0.9.0 | 2026-09-11 | **Drei Zusagen mehr, zwei davon mit offenem Marker – und das ist der Punkt.** Neu: **R5** (Aufzählbarkeit der Regelquellen – dieser Client kennt kein Aufzählungskommando; was es gibt, ist die Selbstauskunft der Sitzung, beobachtet, aber Modellverhalten), **S5** (Aufzählbarkeit der Skills – für diesen Client **nicht erhoben**, VERIFY) und **R6** (keine Importe fremder Werkzeugformate: Der Mechanismus `claudeMdExcludes` ist gemessen, eine Vorgabe wird bewusst **nicht** ausgeliefert, `CR-2026-038` E2). Neuer Abschnitt 8 mit den Anweisungs- und Konfigurationsquellen außerhalb des Projekts – gemessen ist dort, dass eine `CLAUDE.md` aus einem **Elternverzeichnis** mitlädt (K-22) und dass die nutzerglobale Einstellungsdatei **Berechtigungen und Hooks** führt (ERH-07). Der B-Block trägt die Vorbemerkung zur Betriebsmodus-Abhängigkeit (D-35); die README der Regelablage ist in die Laufzeit-README aufgegangen (D-36). Nach zwei Releases ohne VERIFY-Marker stehen wieder zwei – sie sind kein Rückschritt, sondern zwei Fragen, die vorher nicht gestellt waren | `<FRAMEWORK_OWNER>` |
| 0.13.0 | 2026-09-13 | **Der Hook blockierte hier jeden Schreibzugriff – gemessen und behoben (`CR-2026-056`, D-61 bis D-63, Befund B06).** Weil dieser Client in jedem Ereignis `transcript_path` unter `~/.claude/projects/` führt und der Hook bis 0.33.0 **alle** Zeichenketten des Ereignisses durchsuchte, traf das Strukturmuster der Laufzeitschicht bei jedem `Edit`, `Write` und `NotebookEdit` – unabhängig vom Ziel. Am Client nachgemessen, mit Kontrolllauf. Geprüft wird jetzt die Operation statt des Umschlags. Neue Zeile **H4** mit Eingabeschema, Pfadidentität und der benannten Zeitlücke; Abschnitt 5 berichtigt eine Aussage über das andere Pack, die neun Releases lang falsch war | `<FRAMEWORK_OWNER>` |

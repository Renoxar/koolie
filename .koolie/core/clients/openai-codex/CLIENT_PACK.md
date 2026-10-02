# Client Pack `openai-codex`

| Attribut | Wert |
|---|---|
| Modul-ID | `CP-OC` |
| Ebene | keine – Abbildungsschicht |
| Version | 0.2.0 |
| Status | pilot |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Client | OpenAI Codex CLI |
| Verbindliche Zielversion | `0.156.x` – der Geltungsbereich dieses Packs. Festgelegt ist die Spanne, gemessen der Punktwert in der nächsten Zeile |
| Geprüfte Clientversion | `0.156.1` – vor dem Erheben festgeschrieben. Konto: `plus` |
| Stand der Produktbeobachtung | keine (Stand 2026-09-23). Für diesen Client gibt es keine Quellenliste in Anhang 31.4; alle Belege stammen aus Messungen am Client selbst |
| Datum der Prüfung | 2026-09-23 – Bau (`tests/protocols/2026-09-23-bau-openai-codex.md`): 30 Messungen am Prompt-Eingang, am Konfigurationsschema, am Regelauswerter und an einer realen Installation, dazu 25 Sitzungsläufe; davor am selben Tag die Erhebung (`tests/protocols/2026-09-23-erhebung-openai-codex.md`) |

Die Spalte „Einstufung" nennt die vorgesehene Durchsetzungstiefe, die Spalte „Beleg" ihren Nachweisstand: `gemessen` = an diesem Client beobachtet, `[EMPF]` = Vorgabe des Frameworks, `BELEG OFFEN` = noch nicht belegt, mit Grund und Datum in der Zelle.

Das Pack hat keine `[DOK]`-Zeile. Seine Grundlage sind zwei kostenfreie Messmittel des Clients: `codex debug prompt-input` gibt die Nachrichten aus, die der Client der nächsten Anfrage voranstellt, ohne eine Anfrage zu stellen; `codex execpolicy check` wertet eine Befehlsregel mit dem Auswerter der Engine aus. Eine Messung sagt, was dieser Stand tut, nicht, was der Hersteller zusagt.

Zwei Kernzusagen sind `[NICHT ABBILDBAR]`: `B3` und `B5`. Damit gilt `clients/README.md` Abschnitt 4: Begründung in Abschnitt 4 dieses Packs, dokumentierte Ausnahme im Overlay des Projekts und **keine Inbetriebnahme ohne Freigabe durch `<SECURITY_CONTACT>`**.

Wer das Pack einsetzt, liest zuerst Abschnitt 6 (Installation und die zwei Schritte danach), Abschnitt 1b (die Vertrauensbedingung) und Abschnitt 4 (die Freigabe).

## 1. Pfadabbildung

| Rolle des Artefakts | Pfad bei diesem Client | Belegstatus |
|---|---|---|
| Wurzel-Anweisungsdatei | `AGENTS.md` | gemessen (2026-09-23): Der Prompt-Eingang führt sie mit vollem Text als eigene Nachricht `agents_md.instructions`. Sie ist verdrängbar, siehe nächste Zeile |
| Nutzerlokale Überschreibung | `AGENTS.override.md` | gemessen, mit Gegenprobe: Liegt sie im Projekt, steht die Wurzel-Anweisung in keiner Nachricht der Sitzung. Sie **ersetzt**, sie ergänzt nicht. `AGENTS.local.md` ist bei diesem Client kein Mechanismus. Gegenmaßnahmen: Der `deny`-Korb stellt die Datei schreibgeschützt, der Schutz-Hook führt sie in seinen Mustern, Prüfung 88 meldet sie im Projekt. Das Pack liefert keine Beispieldatei dafür aus |
| Regeldateien | `.codex/rules/*.md` – **ohne Ladebedingung** | gemessen (drei Sonden): Der Client lädt keine Regeldatei von sich aus; eine Anweisungsdatei in einem Unterverzeichnis steht nicht vorab im Kontext, eine Einbindung mit `@` bleibt wirkungslos. Die Dateien wirken über ihre Nennung in der Wurzel-Anweisung (`root_instruction_imports`), siehe R2 |
| Befehlsregeln | `.codex/rules/koolie.rules` (erzeugt aus `framework/runtime/permissions.json`) | gemessen an einer realen Installation: Der Client lädt `*.rules` aus `.codex/rules/` des Projekts und aus dem Benutzerverzeichnis. Einen verbotenen Befehl weist er ab und nennt die Begründung aus dieser Datei wörtlich |
| Skills | `.codex/skills/<name>/SKILL.md` **und** `.agents/skills/<name>/SKILL.md` | gemessen (drei Sonden an drei Orten): Beide Ablagen laden, ein `skills/` an der Projektwurzel nicht. Der Prompt-Eingang führt eine Herkunftstabelle der Skillwurzeln. Skills laden auch ohne Vertrauenseintrag (Abschnitt 1b) |
| Subagentenprofile | `.codex/agents/<name>.toml` | Gestalt gemessen, Abbildung nicht gebaut: Pflichtfelder `name`, `description`, `developer_instructions`; `permissions` und `tools` werden angenommen, `allowed_tools` verworfen. Das Framework legt sein Profil als Markdown unter `.codex/agents/` ab; die Wirkung einer Rollendatei ist unerhoben (A1) |
| Berechtigungskonfiguration (Pfadseite) | `.codex/config.toml` (erzeugt aus `framework/runtime/permissions.json`) | gemessen: Ein Rechteprofil unter `[permissions.<name>]` mit `default_permissions`; die Tabelle `filesystem` bindet Pfad an Zugriffsart. Ihre Schlüssel nehmen kein Muster (B3), und die Datei lädt nur bei eingetragenem Vertrauen |
| Hook-Konfiguration | `.codex/hooks.json`, Ereignisse unter dem Schlüssel `hooks` | gemessen: `.codex/hooks/hooks.json` wird nicht gelesen. Fehlt der Schlüssel `hooks`, meldet der Client *unknown field*, lädt die Datei nicht und startet trotzdem. Ereignisse: `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `SubagentStart`, `SubagentStop`, `Stop`, `Interrupt`. **Jeder Eintrag braucht `"enabled": true`** – sonst läuft er nicht, und der Client meldet es nicht |
| MCP-Konfiguration | `.codex/config.toml` unter `[mcp_servers.<name>]` | gemessen: Der Client zählt einen projektlokal eingetragenen Server; `.mcp.json` bleibt unbeachtet. Das Framework liefert keinen Server aus |
| Projektverzeichnis im Hook-Befehl | **keine Variable – das Arbeitsverzeichnis** | gemessen am Hook-Prozess: Seine Umgebung nennt kein Projektverzeichnis; sein Arbeitsverzeichnis ist das Projektverzeichnis. Die Abbildung bindet deshalb den relativen Punkt (`hook_project_dir_expr`) |

## 1a. Semantikabbildung der Berechtigungen

Die Regelmenge liegt werkzeugneutral im Kern (`.koolie/core/framework/runtime/permissions.json`) und wird bei der Installation übersetzt. Was dabei abgebildet wird, steht maschinenlesbar im `manifest.json`; diese Tabelle ist die menschenlesbare Fassung.

Die Regelmenge zerfällt hier in zwei Erzeugnisse, weil der Client keine Regel der Gestalt `Werkzeug(Muster)` kennt: Er bindet Pfade an eine Zugriffsart (`.codex/config.toml`) und Befehle an Präfixmuster (`.codex/rules/koolie.rules`).

| Neutrales Werkzeugverb | Form bei diesem Client | Anmerkung |
|---|---|---|
| `read` | – | Kein Werkzeugname und kein abbildbares Muster. Der Lesekorb des Kerns fällt aus; Begründung in B3 und Abschnitt 4 |
| `search` | – | Der Client hat kein eigenes Suchwerkzeug; Suchen läuft über die Shell und damit unter `exec`. Ein Hook-Matcher `Grep` löst nie aus (gemessen) |
| `write` | Eintrag `"<pfad>" = "read"` in der Tabelle `":workspace_roots"` | Ein Schreibverbot auf einem Teilbaum heißt hier: lesbar, nicht schreibbar. Nur ohne Muster – `**/*.lock` fällt aus (B5) |
| `exec` | `prefix_rule(pattern = [...], decision = "forbidden"\|"prompt"\|"allow")` | Präfixbasiert, mit dem Auswerter des Clients gemessen. Grenze wie bei `claude-code`: `git -C . push` trifft `["git","push"]` nicht |
| `fetch` | – | Kein Mechanismus; der Kern sagt keine Domainbeschränkung zu (B11). Siehe B10 |
| `mcp` | – | Keine Rückfrageregel je Server; wirksam ist, dass kein Server ausgeliefert wird (X1) |
| `skill` | – | Kein Mechanismus erhoben |

| Weitere Eigenschaft | Wert |
|---|---|
| Grundstock des Rechteprofils | `":root" = "read"`; in der Tabelle `":workspace_roots"` `"." = "write"` |
| Schlüsselform der Pfadseite | absoluter Pfad, `~/`-Pfad oder Sonderziel (`:root`, `:workspace_roots`); die Unterpfade des Arbeitsbereichs als eigene Tabelle `[permissions.<profil>.filesystem.":workspace_roots"]`, relativ, `"."` für den Arbeitsbereich selbst. Die Form `:workspace/<pfad>` ignoriert Clientversion 0.157 |
| Hook-Werkzeugnamen | `Bash` (Ausführen und damit Lesen und Suchen), `apply_patch` (Schreiben) |
| Projektverzeichnis im Hook-Befehl | keine Variable – das Arbeitsverzeichnis |
| Sperrform des Schutz-Hooks | `hookSpecificOutput.permissionDecision = "deny"`, Exit 0 |

Die Präfixform eines Befehlsverbots muss ein Präfix seiner wörtlichen Form sein, bei `allow` müssen beide Formen übereinstimmen – sonst scheitert die Installation. Was sich gar nicht abbilden lässt, steht in Abschnitt 4.

## 1b. Der Vertrauenseintrag – die Bedingung über der ganzen projektlokalen Schicht

**Konfiguration, Hooks und Befehlsregeln laden nur, wenn das Projekt in der Benutzerkonfiguration des Clients als vertraut eingetragen ist.** Der Client sagt es selbst: *„Project-local config, hooks, and exec policies are disabled in the following folders until the project is trusted, but skills still load."* (A/B gemessen mit zwei Benutzerverzeichnissen und identischem Projekt.)

Der Eintrag liegt außerhalb des Repositoriums, ist je Arbeitsplatz zu setzen und kann vom Framework nicht ausgeliefert werden. Die erzeugte `.codex/config.toml` nennt die Bedingung in ihrem Kopfkommentar; B1, H1 und H2 tragen sie in ihrer Belegzelle. Ein Eintrag kann auf ein Elternverzeichnis lauten, etwa das Benutzerprofil, und schließt dann jedes Projekt darunter ein.

**Hooks brauchen zusätzlich eigenes Vertrauen**, und es hängt an einem Hash. Ohne dieses Vertrauen läuft der Schutz-Hook gar nicht, und `codex doctor --all` meldet es nicht (gemessen 2026-09-23). Jede Hebung des Frameworks ändert den Hook und damit den Hash: Wer nach `install.py --update` nicht erneut vertraut, arbeitet ohne Schutz-Hook.

## 2. Fähigkeitsmatrix

Einstufung je Zusage: `[TECHNISCH]` erzwungen · `[TEXTUELL]` nur Anweisung · `[NICHT ABBILDBAR]` kein Mechanismus. Regeln in `../README.md` Abschnitt 4.

Zur Belegspalte: Das Pack hat keine `[DOK]`-Zeile. Wo andere Packs eine Quellenkennung führen, steht hier „gemessen“ mit dem Messmittel. Prüfung 73 verlangt eine Quellenkennung nur von `[DOK]`-Zeilen.

### R – Regelladung

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| R1 | Wurzel-Anweisungsdatei wird ungefragt geladen | `AGENTS.md` steht als eigene Nachricht im Prompt jeder Sitzung | `[TECHNISCH]`, mit benannter Bedingung | **gemessen** (2026-09-23, `codex debug prompt-input`): Der vollständige Text steht im Prompt. **Die Bedingung ist die Verdrängung:** Liegt `AGENTS.override.md` daneben, steht die Wurzel-Anweisung in **keiner** Nachricht – gemessen mit Gegenprobe. Eine Wurzel-Anweisung, die eine ungeprüfte Datei im selben Verzeichnis ersetzen kann, ist keine Ebene 1, sondern ein Standard. **Prüfung 88** meldet die Datei, der `deny`-Korb stellt sie schreibgeschützt, und der Schutz-Hook führt sie in seinen Mustern |
| R2 | Regeldateien mit Ladebedingungen | Kein Mechanismus. Ersatz, geliefert: Die Wurzel-Anweisung nennt die Regeldateien mit der Auflage, sie zu Beginn der Sitzung zu lesen (`root_instruction_imports`) | `[NICHT ABBILDBAR]` | **gemessen mit drei Sonden:** Eine Anweisungsdatei in einem Unterverzeichnis steht nicht vorab im Kontext; eine Einbindung mit `@<pfad>` bleibt wirkungslos; nur `AGENTS.md` des Projekts und die gleichnamige Datei im Benutzerverzeichnis des Clients laden ungefragt. Die Mechanik des Ersatzes hat mit diesem Pack ihren ersten Gegenstand (D-348). ⚠️ **Der Ersatz ist schwächer:** Was eine Nennung bewirkt, hängt am Modell und nicht an der Engine |
| R3 | Regeln an Dateimuster bindbar | Kein Mechanismus. Ersatz: dieselbe Nennung – ein Technology Pack lädt damit immer statt nur bei seinen Dateien | `[NICHT ABBILDBAR]` | wie R2. Die Verschärfung ist benannt: Unbedingtes Laden ist mehr Kontext, keine Lockerung – dieselbe Richtung wie die Abbildung von `model_decision` beim Pack `claude-code`. Ein später hinzugefügtes Technology Pack braucht dafür **kein** erneutes `install.py --update`: Die Nennung führt `<RULES_DIR>/40-*.md` als Muster, *„soweit vorhanden“* (`root_instruction_imports`, D-397) |
| R4 | Bekanntes Zeichenlimit | Vorgabe des Frameworks, keine Produkteigenschaft – Wurzel-Anweisung und die dort genannten Regeln zusammen höchstens 40.000 (verbindlich); 12.000 je Regeldatei und 6.000 für die Overlay-Laufzeitregel als SOLL-Grenzen, die bei diesem Pack nicht geprüft werden, weil die Regeln über die Wurzel-Anweisung eingebunden sind | `[TEXTUELL]` | `[EMPF]`. **Für diesen Client ist kein Limit erhoben**; der Prompt-Eingang zeigt den vollständigen Text der Wurzel-Anweisung, eine Obergrenze sagt er nicht. `K-19` gilt hier ebenso |
| R5 | Die geladenen Regelquellen sind vollständig aufzählbar | `codex debug prompt-input` gibt jede Nachricht aus, die der Client der nächsten Anfrage voranstellt – ohne eine Anfrage zu stellen | `[TEXTUELL]` | **gemessen, und schärfer als bei beiden Schwesterpacks:** Die Auskunft ist nicht ein Register des Clients über seine Konfiguration, sondern **der Kontext selbst**. Damit ist auch eine **Abwesenheit** ablesbar – die Verdrängung aus R1 ist genau so gefallen. **Trotzdem `[TEXTUELL]`:** Eine Auskunft ist keine Schranke, und sie entsteht nur, wenn ein Mensch das Kommando ausführt |
| R6 | Keine Importe fremder Werkzeugformate | Kein Schalter erhoben. Gemessen ist die Lage: Dieser Client liest `.codex/skills/` und `.agents/skills/`, nicht die Skillablage eines fremden Werkzeugs | `[NICHT ABBILDBAR]` | **gemessen** (drei Sonden): Eine dritte, naheliegende Ablage an der Projektwurzel lädt nicht; eine fremde Ablage ist in der Herkunftstabelle des Prompts nicht aufgetaucht. **Ersatz: die Auskunft in Abschnitt 7** – und der gemessene Befund, dass es hier nichts abzuschalten gibt. ⚠️ Das ist eine Aussage über diesen Stand, keine Zusage des Herstellers |

### S – Skills

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| S1 | Versionierte Skills im Repository | `.codex/skills/<name>/SKILL.md` mit Frontmatter | `[TECHNISCH]` | **gemessen:** Ein Skill aus dieser Ablage steht mit Name und Beschreibung im Prompt jeder Sitzung, samt Herkunftswurzel |
| S2 | Gezielter Aufruf | Der Prompt führt die Skills als Liste mit Beschreibung und Pfad; das Modell liest die `SKILL.md` | `[TEXTUELL]` | **`BELEG OFFEN` für den Aufruf als Werkzeugaufruf** (2026-09-23): Gemessen ist, dass die Skills **im Kontext stehen**; ob dieser Client einen eigenen Werkzeugaufruf oder eine Schrägstrich-Form dafür führt, ist unerhoben. Ohne das ist der Aufruf Modellverhalten |
| S3 | Werkzeugbeschränkung je Skill | Unerhoben. Die Frontmatter-Felder `permissions` und `triggers` erreichen die installierte Fassung unverändert – dieses Pack führt sie nicht in `drop_fields` | `[TEXTUELL]` | **`BELEG OFFEN`** (2026-09-23): Ob ein Frontmatter-Feld den Werkzeugbestand eines Skills begrenzt, ist bei diesem Client nicht gemessen, und **ein unbekanntes Frontmatter-Feld meldet er nicht**. Ein geratenes Feld sähe aus wie eine Schranke. **Was trägt, ist die globale Schicht:** die Befehlsregeln und der Schutz-Hook, beide unabhängig vom Skill – weniger als eine Beschränkung je Skill, und das ist die Aussage (Bauform von B01, D-50) |
| S4 | Schreibende Skills nur benutzergetriggert | Framework-Konvention, statisch geprüft durch `validate-framework.py` | `[TEXTUELL]` | `[EMPF]`. **Ein Feld, mit dem sich ein Skill vom Modellzugriff ausnehmen ließe, ist bei diesem Client unerhoben** – `model_invocation_field` bleibt deshalb leer, und das ist eine Aussage über den Belegstand. **Reichweite:** Die Zusage gilt für die Skill-Ablage, die das Framework schreibt |
| S5 | Die geladenen Skills sind vollständig aufzählbar, samt Herkunft | Der Prompt-Eingang führt eine Tabelle der Skillwurzeln (`r0`, `r1`, …) und je Skill Name, Beschreibung und Pfad relativ zu seiner Wurzel | `[TEXTUELL]` | **gemessen erfüllt, und vollständiger als bei beiden Schwesterpacks:** Die Aufzählung ist nicht ein Kommando, das mehr zeigt als lädt (`devin-desktop`, D-288), sondern **der Sitzungskontext selbst**. Drei Sonden an drei Orten, eine negativ. Zwei eingebaute Skillwurzeln des Clients stehen mit darin – die Auskunft ist damit auch die Stelle, an der man sie sieht |

### B – Berechtigungen

`[TECHNISCH]` heißt in diesem Block: Die Engine setzt die Regel durch, solange der Betriebsmodus die Berechtigungsprüfung nicht abschaltet. Bei diesem Pack gelten drei weitere, gemessene Bedingungen:

1. **Der Vertrauenseintrag.** Konfiguration, Hooks und Befehlsregeln laden nur bei eingetragenem Vertrauen (Abschnitt 1b). Ohne ihn trägt von diesem Block nichts.
2. **Die Rechtestufe des Betriebssystems.** Auf einem unerhöhten Windows-Arbeitsplatz kann der Sandkasten ein `deny`-Leserecht nicht durchsetzen, und der Client startet dann nicht: *„windows unelevated restricted-token sandbox cannot enforce deny-read restrictions directly; refusing to run unsandboxed"* (fail-closed). Die Pfadseite trägt deshalb Schreibverbote, aber kein Leseverbot. Dort trägt der Schutz-Hook: Im Modus ohne Rückfragen und ohne Sandkasten hat er denselben Lesezugriff blockiert, den die Berechtigungsschicht durchließ – gemessen mit Gegenlauf in einem Baum ohne Regeltexte.
3. **Der Startort der Sitzung.** Der Client setzt die Projektwurzel auf die git-Wurzel des Startverzeichnisses. Startet die Sitzung in einem Repositorium unterhalb der Installation, lädt er weder deren Konfigurationsdatei noch deren Wurzel-Anweisung; eine eigene Installation im Repositorium lädt. Gemessen ist das Laden, nicht die Durchsetzung (2026-09-26, Clientversion 0.157.0, ohne Modellaufruf mit `codex doctor --all` und `codex debug prompt-input`, `tests/protocols/2026-09-26-mehrprojekt-tokenlast.md`). **Nichts meldet einen falschen Startort.**

Die mit **Kern** markierten Zeilen sind die Kernzusagen; die Berechtigungsdatei dieses Packs ist TOML und führt keinen Block `_core_rules_integrity`. Eine Abweichung von `[TECHNISCH]` ist begründungspflichtig.

| ID | Zusage des Frameworks | Kern | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|---|
| B1 | Berechtigungen versioniert im Repository | ja | `.codex/config.toml` (Pfadseite) und `.codex/rules/koolie.rules` (Befehlsseite) – beide im Projekt, beide versioniert | `[TECHNISCH]`, bedingt | **gemessen:** Beide Träger liegen im Repositorium und werden aus derselben Kernquelle erzeugt. **Die Bedingung steht außerhalb:** Ohne Vertrauenseintrag lädt **keiner von beiden** (Abschnitt 1b, A/B gemessen) |
| B2 | Verweigern vor Rückfragen vor Erlauben | ja | Die Regelsprache kennt `forbidden`, `prompt` und `allow`; bei mehreren Treffern gilt die **strengste** | `[TECHNISCH]` | **gemessen mit dem Auswerter der Engine selbst** (`codex execpolicy check`, 2026-09-23): Zwei Regeln auf denselben Befehl, `allow` und `forbidden` → `forbidden`; `prompt` und `allow` → `prompt`. **Unabhängig von der Reihenfolge in der Datei** – beide Fälle einmal in jeder Reihenfolge gefahren |
| B3 | Secret-Dateien per Pfadmuster lesegeschützt | ja | Kein abbildbarer Mechanismus. Ersatz: der Schutz-Hook, gemessen – siehe Abschnitt 4 | `[NICHT ABBILDBAR]` | **gemessen, und die beiden Gründe verstärken einander.** **(1) Musterform und Versionierbarkeit schließen einander aus:** Ein Musterausdruck ist als Schlüssel nur mit **absolutem** oder `~/`-Vorsatz zulässig – und ein absoluter Pfad in einem versionierten Träger wäre ein Wert dieser Arbeitsstation; ein projektrelativer Schlüssel (`:workspace/…`) nimmt **kein** Muster (*„must be absolute, use `~/…`, or start with `:`"*) – gemessen mit 0.156.1. 🟢 **Nachgemessen am 2026-09-30 mit 0.157.1 (`K-160`, D-495):** Ein projektrelativer Glob unter `:workspace_roots` (`"**/*.env" = "deny"`) wird jetzt **angenommen** – Grund (1) gilt für diese Version nicht mehr. Grund (2) trägt allein: Unerhöht startet `codex sandbox` mit jeder `deny`-Leseregel gar nicht, auch nicht für eine harmlose Datei (*„Restricted read-only access requires the elevated Windows sandbox backend“*); die Kontrolle ohne Regel liest den Köder. **(2) Ein `deny`-Leserecht verlangt den erhöhten Windows-Sandkasten**, und ohne ihn läuft der Client gar nicht. **Ersatz, gemessen:** Der Schutz-Hook blockiert den Lesezugriff auf `.env` – in einem Baum ohne Regeltexte und im Modus ohne Rückfragen und ohne Sandkasten, mit Gegenlauf, in dem der Köderinhalt wörtlich herauskam. **Kernzusage: Abschnitt 4 und Freigabe durch `<SECURITY_CONTACT>`** |
| B4 | Framework- und Overlay-Artefakte schreibgeschützt | ja | In der Tabelle `":workspace_roots"`: `".koolie/core" = "read"`, `".codex" = "read"`, `"AGENTS.md" = "read"` und der Schutz-Hook. Das Overlay sperrt allein der Schutz-Hook; die Berechtigungsdatei führt es nicht. Für das Overlay wirkt der Sandkasten deshalb nicht, Shell-Befehle hält dort nur die Regelschicht | `[TECHNISCH]` für das direkte Schreiben (über den Hook) und für Shell-Befehle im Sandkasten (gemessen); `[TEXTUELL]`, wo der Sandkasten abgeschaltet ist (M6, B9) | **Der Hook ist gemessen** (2026-09-23, Baum ohne Regeltexte): Ein `apply_patch` auf `.koolie/core/notiz.txt` wurde blockiert; **im Lauf davor, mit der alten Musterform, wurde die Datei angelegt.** Der Befund dahinter: Das Schreibwerkzeug dieses Clients führt **keinen Pfad in einem Feld** – der Pfad steht im **Patchtext**, hinter einem Leerzeichen, und die Pfadmuster des Hooks kannten als Grenze nur den Schrägstrich (D-347). 🟢 **Die Pfadseite ist seit `1.12.1` an ihrer Wirkung gemessen** (D-412, `K-157`), mit Clientversion 0.157.1 und Sandkasten `restricted`: **Ohne Modellaufruf** (`codex sandbox`) sind mit der Tabelle `:workspace_roots` `.koolie/core`, `.koolie/project-overlay` (damals noch in der Tabelle), `.codex` und `AGENTS.md` schreibgeschützt und der übrige Arbeitsbereich schreibbar; **in zwei Sitzungen** (Baum ohne Regeltexte, Hook ohne Vertrauen, also nicht beteiligt) scheitert ein Shell-Befehl auf `.koolie/core` mit *„Zugriff verweigert“*, der Kontrolllauf auf eine freie Datei schreibt. 🔴 **Mit der bis `1.12.0` ausgelieferten Form `:workspace/<pfad>` meldet 0.157 jeden Eintrag als unbekannt und ignoriert ihn – und der GANZE Arbeitsbereich ist schreibgeschützt**, auch die freie Datei. `install.py --update` fasst `config.toml` nicht an; bestehende Installationen ziehen die Tabelle von Hand nach |
| B5 | CI-, Quality-Gate- und Lockdateien schreibgeschützt | ja | Kein abbildbarer Mechanismus und kein Ersatz – der Schutz-Hook deckt diese Pfade nicht; siehe Abschnitt 4 | `[NICHT ABBILDBAR]` | **gemessen:** Die Regeln des Kerns sind hier **Namensmuster** (`**/*.lock`, `**/package-lock.json`, …) und **Platzhalterlisten** (`<CI_CONFIG_PATHS>`, `<QUALITY_GATE_CONFIG_PATHS>`). Für beide gilt dieselbe Schlüsselsyntax wie bei B3: kein Muster ohne absoluten Vorsatz, kein Schlitz auf der Schlüsselseite einer TOML-Tabelle. **Und der Schutz-Hook trägt sie nicht** – seine Muster decken Secrets, die Laufzeitschicht und das Kernverzeichnis, nicht die Lockdateien eines Projekts. **Kernzusage: Abschnitt 4 und Freigabe durch `<SECURITY_CONTACT>`** |
| B6 | Befehle per Muster verweigerbar | ja | `prefix_rule(pattern = [...], decision = "forbidden")` in `.codex/rules/koolie.rules` | `[TECHNISCH]` | **an einer realen Installation gemessen** (2026-09-23): Der Befehl wurde abgewiesen, **und der Client nannte die Begründung dieser Datei wörtlich** – dieselbe Zurechenbarkeit wie beim `deny`-Korb von `devin-desktop`. Zusätzlich mit dem Auswerter der Engine gegengeprüft: `git push origin main` → `forbidden`, `git status` → `allow`. ⚠️ **Grenze, gemessen und benannt:** `git -C . push` trifft `["git","push"]` **nicht** – dieselbe Grenze wie bei `claude-code`. 🟢 **Über die Ablagen hinweg gemessen am 2026-09-30 (`K-119`, D-496):** Eine Regeldatei im Benutzerverzeichnis des Clients hebt eine des Projekts **nicht** auf – `allow` dort gegen `forbidden` hier und umgekehrt: beide Male abgewiesen, mit der Begründung der verbietenden Datei, das Remote blieb leer; `codex execpolicy check` über beide Dateien liefert in jeder Reihenfolge `forbidden`. Die strengste Entscheidung gewinnt, die Zeile braucht keine Bedingung |
| B7 | Schreiboperationen fragen zurück | – | `approval_policy = "on-request"` als Standard des Clients | `[TECHNISCH]` für den Modus; `[TEXTUELL]` für die Regel je Pfad | **gemessen** (`codex doctor`): Der Standard ist `OnRequest`. **Die `ask`-Regel des Kerns auf alle Schreiboperationen ist hier nicht abbildbar** – dieser Client kennt keine Rückfrageregel je Pfad, nur eine Politik je Sitzung. ⚠️ **Und die projektlokale Schicht kann sie lockern** (B9) |
| B8 | Netzwerkzugriff standardmäßig unterbunden | – | Netzsandkasten des Clients (`restricted`) **und** die Befehlsregeln auf `curl`, `wget`, `ssh`, `scp` | `[TECHNISCH]` für den Sandkasten und für diese vier Programme; `[TEXTUELL]` darüber hinaus | **gemessen** (`codex doctor`: *network sandbox restricted*; die vier Programme stehen im `forbidden`-Korb der erzeugten Regeldatei). ⚠️ **Jedes andere netzfähige Programm ist nicht erfasst**, und die Liste wird bewusst nicht verlängert |
| B9 | Nutzerlokale Konfiguration kann nur verschärfen | – | Widerlegt, im Spiegelbild | `[TEXTUELL]` | **gemessen mit Gegenprobe** (A/B, zwei Benutzerverzeichnisse): Nicht die nutzerlokale Konfiguration lockert die projektseitige – **die projektlokale lockert den Benutzerstandard.** Mit Vertrauenseintrag schlagen `approval_policy = "never"` und ein Sandkastenmodus ohne Schranken **aus dem Projekt heraus** den Standard des Arbeitsplatzes. Dieselbe Frage, drei Clients, drei Antworten: `claude-code` hält die Richtung, `devin-desktop` kehrt sie um, und hier ist die **lockernde Seite die versionierte**. ⚠️ **Für ein aufnehmendes Projekt heißt das:** Wer die Berechtigungsdatei liest, liest auch, was sie am Arbeitsplatz **aufhebt** |
| B10 | Externer Abruf auf freigegebene Domains beschränkbar | – | Kein Mechanismus. Der Kern sagt die Beschränkung nicht zu (B11) | `[NICHT ABBILDBAR]` | **Kein Ersatz durch das Framework, und das ist eine Aussage und kein Rest.** Was den Kanal steuert, ist der **Netzsandkasten** des Clients (B8) und die Befehlsregel auf die vier Programme; eine Domainangabe kennt keine der beiden Schichten. **Der organisatorische Ersatz** ist die Freigabezeile des Overlays, und sie hat nach D-65 keine technische Seite |

### H – Hooks

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| H1 | Prüfung vor Werkzeugausführung | `PreToolUse` in `.codex/hooks.json`, Matcher `Bash\|apply_patch` | `[TECHNISCH]`, doppelt bedingt | **gemessen an einer realen Installation** (2026-09-23): Der Hook läuft bei jedem Shell- und jedem Schreibaufruf; der Umschlag führt `session_id`, `turn_id`, `transcript_path`, `cwd`, `hook_event_name`, `model`, `permission_mode`, `tool_name`, `tool_input` und `tool_use_id`. **Bedingung 1: `"enabled": true` je Eintrag** – ohne das läuft er nicht, und der Client meldet es nicht. **Bedingung 2: Hook-Vertrauen** – ohne persistiertes Vertrauen läuft er **gar nicht**, der Köderinhalt kommt heraus, und `codex doctor --all` sagt nichts dazu. **Jede Hebung des Frameworks ändert den Hash** (Abschnitt 1b) |
| H2 | Prüfung kann **blockieren** | `hookSpecificOutput.permissionDecision = "deny"` und **Exit 0** | `[TECHNISCH]` | 🔴 **Gemessen, und der schwerste Befund dieses Packs** (D-347): Die Standardsperrform des Schutz-Hooks – `{"decision": "block"}` und **Exit 2** – bewirkt bei diesem Client **nichts**. Der Client meldet *PreToolUse Failed* und **führt die Operation aus**; im Gegenlauf kam der Köderinhalt wörtlich heraus. **Dieselbe Sperre in der Form, die er liest, blockiert** – gemessen in einem Baum **ohne** Regeltexte und im Modus, der Rückfragen **und** Sandkasten abschaltet, mit Positivkontrolle im selben Baum. Ein Hook, der läuft und dessen Sperrform der Client nicht liest, ist eine Zusage ohne Mechanismus. **Prüfung 86** hält die Kette aus Manifest, Skript und erzeugtem Kommando zusammen |
| H3 | Statusmeldung beim Sitzungsstart | `SessionStart` mit `hook-overlay-status.py` | `[TECHNISCH]` | **beobachtet** (2026-09-23): Der Hook läuft, und **seine Ausgabe steht im Sitzungskontext** – ein Lauf im Baum ohne Regeltexte hat den Overlay-Status daraus zitiert. Das ist mehr als bei beiden Schwesterpacks, wo die Meldung selbst unbeobachtet blieb |
| H4 | Eingabeschema und Pfadidentität des Schutz-Hooks | Ereignisprüfung, Pfadidentität über den aufgelösten Pfad, alle Pfadmuster ohne Rücksicht auf Groß-/Kleinschreibung. `hook_fail_closed` steht auf `false`. Grenze: Ein Hook prüft vor dem Zugriff; eine zwischenzeitlich umgebogene Verknüpfung kann er nicht ausschließen | `[TECHNISCH]` für die Musterprüfung, mit zwei benannten Grenzen und der Zeitlücke | **Das Schema von `PreToolUse` ist aufgezeichnet** (zehn Felder, siehe H1) – **der vollständige Bestand der zwölf Ereignisse ist es nicht**, und deshalb bleibt `hook_fail_closed` auf `false`: Fail-closed bei teilweise erhobenem Schema wäre keine Härtung, sondern eine Sitzung, die bei der ersten unbekannten Eingabeform blockiert (D-31). **Zweite Grenze, gemessen und behoben:** Das Schreibwerkzeug führt **keinen Pfad in einem Feld**; er steht im Patchtext hinter einem Leerzeichen. Die Pfadmuster des Hooks erkennen deshalb auch das Leerzeichen als Grenze – eine **Verschärfung für alle drei Packs** (D-347) |

### A – Agentenprofile

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| A1 | Rein lesendes Reviewprofil | Nicht abgebildet. Der Client liest Rollendateien als `.codex/agents/<name>.toml`; das Framework legt sein Profil als Markdown ab | `[NICHT ABBILDBAR]` | **Die Gestalt ist gemessen, die Wirkung nicht** (2026-09-23): Pflichtfelder `name`, `description`, `developer_instructions`; `permissions` wird als Tabelle angenommen, `allowed_tools` verworfen. **Nicht gemessen ist, ob und wie ein Feld den Werkzeugbestand eines Unteragenten begrenzt** – und dieser Client startet Unteragenten (der Prompt führt sechs Werkzeuge dafür). **Ersatz, benannt:** Der Schutz-Hook und die Befehlsregeln wirken unabhängig vom Profil; ob sie einen Unteragenten **erfassen**, ist ebenfalls unerhoben. Eine Abbildung ohne Messung wäre dieselbe Lage, aus der `AP2-CC-13` kam |
| A2 | Rein lesendes Analyseprofil für Modus M1 | Kein eingebautes Profil erhoben | `[NICHT ABBILDBAR]` | **Ersatz, benannt:** der Standardmodus des Clients (`approval_policy = "on-request"`, Sandkasten lesend) – er ist gemessen und wirkt ohne Profil. ⚠️ **Das ist ein Modus und kein Profil**, und der Unterschied ist, dass er für die ganze Sitzung gilt |

### M – Modi und Sitzungsfreigaben

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| M1 | Standardmodus fragt bei Schreiben und Befehlen zurück | `approval_policy = "on-request"`, Sandkasten `read-only` | `[TECHNISCH]` | **gemessen** (`codex doctor`): *approval OnRequest · restricted fs + restricted network*. ⚠️ **Der nicht-interaktive Lauf kennt keine Rückfrage** – dort wird abgewiesen statt gefragt; das ist eine Verschärfung und kein Messwert über den interaktiven Betrieb |
| M2 | Modus ohne Rückfragen ausschließbar | Eine Sperre des Modus ist nicht erhoben. Der Modus selbst heißt `--dangerously-bypass-approvals-and-sandbox` und bezeichnet sich als gefährlich | `[TEXTUELL]` | **Was gemessen ist, ist die Wirkung der zweiten Linie:** In genau diesem Modus hat der Schutz-Hook den Zugriff blockiert, den die Berechtigungsschicht durchließ. ⚠️ **Die Sperre des Modus bleibt unerhoben** – eine Organisationsebene, die ihn ausschlösse, ist für diesen Client nicht gemessen |
| M3 | Freigabe auf die Sitzung begrenzbar | Der Client kennt eine Freigabe „für die Sitzung" und eine über ein Befehlspräfix | `[TEXTUELL]` | **`BELEG OFFEN`** (2026-09-23): Die Stufen sind in der Bedienoberfläche des Clients benannt; **im nicht-interaktiven Betrieb ist keine davon messbar** – eine Rückfrage an einen Menschen lässt sich so nicht messen. Dieselbe Enthaltung wie bei `devin-desktop` für `ask` und `allow` (D-280) |
| M4 | Eigener Planungsmodus für Modus M2 | Unerhoben, ob der Client einen Planungsmodus mit eigener Plan-Ablage außerhalb des Repositorys führt. Bis dahin ist die Ablage von `koolie-plan` und `koolie-bugfix-prepare` die Sitzungsausgabe | `[TEXTUELL]` | **`BELEG OFFEN`** (2026-09-25, `K-149`): nicht gemessen; eine Quellenliste gibt es für diesen Client nicht |
| M6 | Modus mit selbsttätiger Übernahme von Dateiänderungen begrenzbar | Sandkastenmodus `workspace-write` – nach `.koolie/core/framework/core/03-security.md` Abschnitt 4 nur über dokumentierte Ausnahme bei Kontrollstufe niedrig zulässig | `[TEXTUELL]` | `[EMPF]` für die Beschränkung; **eine Abschaltung des Modus ist nicht erhoben**. ⚠️ **Und die projektlokale Schicht kann ihn setzen** (B9) – das ist der Unterschied zu beiden Schwesterpacks |
| M7 | Modus, der selbst beurteilt, was sicher ist, begrenzbar | Ein solcher Modus ist für diesen Client nicht erhoben | `[TEXTUELL]` | **Ersatz, benannt:** Es gibt keinen – die Zusage hat hier keinen Gegenstand, solange kein selbst beurteilender Modus erhoben ist. Eine Zusage ohne Gegenstand ist keine erfüllte Zusage; sie steht hier, damit sie nicht als eine gelesen wird |

### X – Externe Anbindung

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| X1 | Keine externe Anbindung ohne Einzelfreigabe | Das Framework liefert keinen MCP-Server aus; ein Server wäre eine Tabelle `[mcp_servers.<name>]` in der Berechtigungsdatei | `[TEXTUELL]`, mit einer benannten Grenze | **gemessen:** Ohne Eintrag zählt der Client **null** Server; ein projektlokal eingetragener wird gezählt. **Die Grenze:** Eine Rückfrageregel je MCP-Werkzeug – die `ask`-Regel des Kerns – ist bei diesem Client **nicht abbildbar**. Was trägt, ist die Abwesenheit des Eintrags, und die ist eine Framework-Entscheidung, keine Schranke des Clients. ⚠️ **Die Benutzerkonfiguration kann Server führen**, und sie liegt außerhalb des Repositoriums (Abschnitt 7.2) |
| X2 | Art und Ort der Codebasis-Indexierung bekannt | Kein Mechanismus zur Steuerung bekannt | `[NICHT ABBILDBAR]` | `BELEG OFFEN (dauerhaft)` – von außen nicht zu beobachten, Stand 2026-09-23 (`K-20`, D-292). **Kein Ersatz durch das Framework:** Was ein Client indexiert und wohin er es gibt, sieht weder die Installation noch der Validator. Nach D-41 eine **Fähigkeitszusage**, keine Kernzusage |

## 3. Zusammenfassung der Durchsetzungstiefe

**Zählregel (normativ für diese Tabelle):** Eine Zeile zählt bei ihrer schwächsten Einstufung; trägt sie zwei Angaben je Zugriffskanal, zählt die schwächere. Prüfung 31 rechnet die Summen aus der Matrix nach.

| Klasse | Anzahl | davon Kernzusagen |
|---|---|---|
| `[TECHNISCH]` | **10 von 35** | 3 von 6 (B1, B2, B6) |
| `[TEXTUELL]` | **16 von 35** | 1 von 6 (B4 – Shell und Unterprozess) |
| `[NICHT ABBILDBAR]` | **9 von 35** | 2 von 6 (B3, B5) |

**Belegstand:** `BELEG OFFEN` sagen S2, S3, M3 und M4, dazu X2 dauerhaft. An einer realen Installation gemessen sind B2, B4, B6, H1 bis H3, R1, R5, S1 und S5. Eine Produktbeobachtung fehlt: Für diesen Client gibt es keine Quellenliste.

## 4. Kernzusagen ohne technische Durchsetzung

Zwei der sechs Kernzusagen sind `[NICHT ABBILDBAR]`. Es gilt `clients/README.md` Abschnitt 4: Begründung hier, dokumentierte Ausnahme im Overlay des Projekts (`.koolie/project-overlay/exceptions/EXCEPTIONS.md`) und **keine Inbetriebnahme ohne Freigabe durch `<SECURITY_CONTACT>`**.

| ID | Einstufung | Warum der Client das nicht durchsetzt | Ersatzmaßnahme | Freigabe |
|---|---|---|---|---|
| B3 | `[NICHT ABBILDBAR]` | (1) Mit 0.156.1 nehmen die Pfadschlüssel ein Muster nur mit absolutem oder `~/`-Vorsatz an – das widerspricht der Versionierbarkeit aus B1; 0.157.1 nimmt den projektrelativen Glob an. (2) Ein `deny`-Leserecht verlangt den erhöhten Windows-Sandkasten; ohne ihn startet der Client nicht (fail-closed). Grund (2) trägt allein | Ersatz: der Schutz-Hook, gemessen. Er blockiert den Lesezugriff auf `.env` in einem Baum ohne Regeltexte und im Modus ohne Rückfragen und ohne Sandkasten, mit Positivkontrolle. Er trägt die Bedingungen aus H1 (`enabled`, Hook-Vertrauen) | `<SECURITY_CONTACT>` |
| B5 | `[NICHT ABBILDBAR]` | Die Regeln des Kerns sind hier Namensmuster (`**/*.lock`) und Platzhalterlisten (`<CI_CONFIG_PATHS>`, `<QUALITY_GATE_CONFIG_PATHS>`). Für die Muster gilt derselbe Grund wie bei B3; für die Listen kommt hinzu, dass die Schlüsselseite einer TOML-Tabelle keinen Ausfüllschlitz kennt | Kein vollständiger Ersatz. Der Schutz-Hook deckt Secrets, die Laufzeitschicht und das Kernverzeichnis, nicht die Lockdateien eines Projekts. Es bleiben die Regeltexte; ein Verstoß ist Modellverhalten. **Ein Projekt mit hoher Kontrollstufe sollte diesen Client dafür nicht einsetzen** | `<SECURITY_CONTACT>` |

B1, B2 und B6 sind `[TECHNISCH]` – B2 und B6 an der Engine gemessen, B1 über die Lage der Träger, mit der Bedingung des Vertrauenseintrags. B4 ist es im Kanal *direktes Schreiben* (über den Schutz-Hook); Shell und Unterprozess bleiben `[TEXTUELL]`.

## 5. Bekannte Abweichungen im Verhalten

- **Zwei Träger statt einer Berechtigungsdatei.** Die Ausgabeform ist `toml` (`permissions_format`): Es gibt keine Körbe aus `Werkzeug(Muster)`-Zeilen und keinen Block `_core_rules_integrity`, weil der Client unbekannte Schlüssel in der Konfigurationsdatei meldet (mit `--strict-config` als Fehler). Deshalb erreichen dieses Pack nicht: Prüfung 2, Prüfung 37, Prüfung 42, Prüfung 43, Prüfung 54 und Prüfung 72. Nur zum Teil erreichen es Prüfung 59 und Prüfung 89: Ihr Gegenstand (c), der Abgleich der ausgeschlossenen und der Nur-Lese-Pfade des Overlays mit dem `deny`-Korb, entfällt; (a) und (b), der Abgleich mit der Laufzeitfassung, laufen. Ein Globwert erreicht `.codex/config.toml` nur als Teilbaum (`verz/**`) oder als einzelner Dateiname; ein Namensmuster wie `**/*.tfstate` bleibt `[NICHT ABBILDBAR]` wie B3. Der Prüfapparat hält diese Liste gegen seine Liste der formatgebundenen Prüfungen.
- **Die nutzerlokale Wurzel-Anweisung ersetzt, sie ergänzt nicht.** Deshalb liefert dieses Pack dafür keine Beispieldatei aus; sie wäre eine Anleitung, die Ebene 1 lautlos abzuschalten.
- **Die projektlokale Schicht kann lockern** (B9): Hier ist die versionierte Seite die lockernde. Wer die Berechtigungsdatei liest, liest auch, was sie am Arbeitsplatz aufhebt.
- **Ohne Vertrauenseintrag trägt die projektlokale Schicht nichts** – weder Konfiguration noch Hooks noch Befehlsregeln; Skills laden trotzdem. Die Bedingung liegt außerhalb des Repositoriums.
- **Der Hook braucht eigenes Vertrauen, und es hängt an einem Hash.** Jede Hebung ändert den Hash; ohne erneutes Vertrauen läuft das Projekt ohne Schutz-Hook, und nichts meldet es. Das gehört in die Übernahme- und Hebungsanleitung des Projekts.
- **Der Hook-Prozess bekommt das Projektverzeichnis nicht als Variable**, er läuft darin. Die Abbildung bindet deshalb den relativen Punkt.
- **Ein falsch geschriebenes Sonderziel der Pfadseite fällt lautlos durch:** `:quatsch/x` wird angenommen und steht danach im wirksamen Rechteprofil (gemessen). Unbekannte Schlüssel meldet der Client, unbekannte Werte eines bekannten Schlüssels nicht.
- Das Pack nutzt die Kernmechaniken `rule_frontmatter: "comment"` und `root_instruction_imports`.

## 6. Installation und Prüfung

Die Starter `install.cmd` (Windows) und `install.command` (macOS) in der Wurzel des Archivs fragen Projekt, Client und Overlay-Muster im Dialog ab und rufen `install.py --target` auf. Ohne Dialog, aus dem entpackten Archiv:

```text
python .koolie/core/install.py --target /pfad/zum/projekt --client openai-codex
```

Danach im Projekt:

```text
python .koolie/core/tests/scripts/validate-framework.py
```

Ein Projekt, das den Kern schon trägt, wird mit `--update` gehoben; `install.py --client openai-codex` ohne `--target` installiert im aktuellen Verzeichnis.

**Danach – ohne das trägt nichts aus Block B:** das Projekt in der Benutzerkonfiguration des Clients als vertraut eintragen und dem Schutz-Hook einzeln vertrauen, nach jeder Hebung erneut. Beides liegt außerhalb des Repositoriums (Abschnitt 1b); `install.py` nennt beide Schritte nach der Installation und das erneute Hook-Vertrauen nach jeder Hebung.

Vor der ersten produktiven Nutzung die Basistests des Testkatalogs (`.koolie/core/tests/TEST_CATALOG.md`, Kennzeichnung „Basis") gegen diesen Client fahren und protokollieren.

## 7. Anweisungs- und Konfigurationsquellen außerhalb des Projekts

Dieser Pflichtabschnitt führt, was der Client aus Ablagen außerhalb des Repositoriums lädt. Solche Quellen haben nach Regel 2.6 der Prioritätshierarchie keine Ebene: Sie dürfen einschränken, nie über die Ebenen 1 bis 4 hinaus erweitern und keine Governance-, Datenschutz- oder Sicherheitsregeln setzen.

**Erhebungsstand: 2026-09-23**, Clientversion `0.156.1`, erhoben mit `codex debug prompt-input`, `codex doctor --all`, `codex execpolicy check` und Sitzungsläufen gegen ein eigenes Benutzerverzeichnis im Ablagebereich (`tests/protocols/2026-09-23-bau-openai-codex.md`).

### 7.1 Anweisungsquellen

| Quelle | Ladebedingung | Belegstatus | Maßnahme des Frameworks |
|---|---|---|---|
| `<Benutzerverzeichnis des Clients>/AGENTS.md` | in jeder Sitzung, zusätzlich zur Wurzel-Anweisung des Projekts | Gemessen (2026-09-23): Eine Sonde darin stand im Prompt einer Sitzung, die im Projekt nur ihre eigene `AGENTS.md` hatte | keine – Auskunft. Ein Schalter, mit dem das Framework die Datei abstellen könnte, ist nicht erhoben |
| `<Benutzerverzeichnis des Clients>/skills/**` | in jeder Sitzung; die Herkunftstabelle des Prompts führt sie | Gemessen (2026-09-23): Die Wurzeltabelle des Prompts nennt sie neben den beiden projektlokalen Ablagen | keine – Auskunft. Die Tabelle nennt je Skill seine Wurzel; die Herkunft ist damit ablesbar (S5) |
| `<Benutzerverzeichnis des Clients>/rules/*.rules` | Befehlsregeln des Arbeitsplatzes | Gemessen (2026-09-23): Eine ungültige Datei dort bricht den Sitzungsstart mit einer Meldung ab, die sie nennt | keine – Auskunft. Sie steht neben den projektlokalen Regeln; bei einem Treffer in beiden gewinnt die strengste Entscheidung (B6) |
| `.agents/skills/**` im Projekt | zweite projektlokale Skillablage | Gemessen (2026-09-23) | keine – das Framework schreibt nur `.codex/skills/` |

### 7.2 Konfigurationsquellen

Berechtigungen, Hooks und Einstellungen außerhalb des Repositoriums betreffen genau die Linien, auf denen B1 bis B6 stehen.

| Quelle | Wirkung | Belegstatus |
|---|---|---|
| `<Benutzerverzeichnis des Clients>/config.toml` | **Trägt den Vertrauenseintrag, ohne den die projektlokale Schicht nicht lädt**, und führt daneben dieselben Schlüssel wie die Projektdatei: Rechteprofile, MCP-Server, Modellwahl | Gemessen in beiden Richtungen (A/B mit zwei Benutzerverzeichnissen). Ein Vertrauenseintrag kann auf ein Elternverzeichnis lauten und schließt dann jeden Pfad darunter ein |
| Das Hook-Vertrauen (Hash je Hook) | Ohne es läuft der Schutz-Hook nicht, und nichts meldet es | Gemessen mit Gegenlauf (2026-09-23): ohne Vertrauen kam der Köderinhalt heraus, mit Vertrauen wurde blockiert |

### 7.3 Was dieser Abschnitt nicht leistet

Eine Auskunft ist keine Schranke, und bei diesem Client ist sie die einzige Maßnahme: Für keine der vier Anweisungsquellen ist ein Schalter erhoben, mit dem das Framework sie abstellen könnte (R6).

Ein Abwesenheitsbeleg altert mit jeder Clientversion. Prüfung 19 prüft nur, dass diese Auskunft da ist, nicht, ob sie stimmt.

## 8. Änderungsverlauf

| Version | Datum | Änderung | Autor (Rolle) |
|---|---|---|---|
| 0.1.0 | 2026-09-23 | **Angelegt (`CR-2026-133`, D-346 bis D-349).** Das dritte Client Pack, und das erste, dessen Belege sämtlich aus Messungen am Client stammen statt aus seiner Dokumentation. **Zwei Kernzusagen sind `[NICHT ABBILDBAR]`** – `B3`, weil Musterform und Versionierbarkeit einander ausschließen und ein `deny`-Leserecht den erhöhten Windows-Sandkasten verlangt; `B5` aus demselben Grund und ohne Ersatz im Schutz-Hook. **Die Sperrform des Schutz-Hooks war bei diesem Client wirkungslos** und ist berichtigt; die Pfadmuster des Hooks kannten als Grenze nur den Schrägstrich und trafen den Patchtext des Schreibwerkzeugs nicht. **Drei neue Prüfungen** (86, 87, 88) | `<FRAMEWORK_OWNER>` |
| 0.1.4 | 2026-09-25 | Der Satz über die mit **Kern** markierten Zeilen nennt, dass diese Berechtigungsdatei keinen Block `_core_rules_integrity` führt (`CR-2026-147`, D-402; seit D-395 verlangt ihn nur eine JSON-Datei). ⚠️ Die Fassungen `0.1.1` bis `0.1.3` haben hier keine Zeile; sie stehen im Änderungsverlauf des Frameworks zu `1.9.1` bis `1.10.0`. Zeile M4 (Planungsmodus) ergänzt, auf die `koolie-plan` und `koolie-bugfix-prepare` für die Planablage verweisen: `[TEXTUELL]`, `BELEG OFFEN`; Summen und Belegstand nachgezogen (K-149) | `<FRAMEWORK_OWNER>` |
| 0.1.5 | 2026-09-26 | Vorbemerkung des B-Blocks, Bedingung (3): **der Startort**, gemessen mit Clientversion 0.157.0 ohne Modellaufruf – im Repositorium unterhalb der Installation laden weder Konfiguration noch Wurzel-Anweisung (D-408). 🔴 **`B4`: Befund `K-157`** – 0.157.0 ignoriert die `:workspace`-Pfadeinträge (`CR-2026-148`) | `<FRAMEWORK_OWNER>` |
| 0.1.6 | 2026-09-26 | 🟢 **`K-157` beantwortet: das Sonderziel heißt `:workspace_roots`** (D-412, `CR-2026-149`) – Unterpfade als eigene Tabelle; keine Startwarnung mehr. `B4`: die Pfadseite gemessen (Sandkasten, ohne Modell und in zwei Sitzungen), `[TECHNISCH]` auch für Shell-Befehle im Sandkasten. Mit der alten Form war unter 0.157 der ganze Arbeitsbereich schreibgeschützt. `B3`: Vorbehalt `K-160` (dokumentierte `deny`-Globs, nicht nachgemessen). Gemessen mit 0.157.1 – außerhalb der Zielspanne `0.156.x`, die unverändert bleibt | `<FRAMEWORK_OWNER>` |
| 0.1.7 | 2026-09-26 | Abschnitt 5: **Prüfung 72 statt 76** unter den nicht erreichten Prüfungen – die Menge des Prüfapparats führte die Nummer falsch, und Prüfung 72 enthielt sich bei diesem Pack still (`CR-2026-150`, D-416) | `<FRAMEWORK_OWNER>` |
| 0.1.8 | 2026-09-29 | Zeile B4 folgt dem Erzeugnis: Die Tabelle `:workspace_roots` führt das Overlay seit `1.17.0` nicht mehr, es sperrt allein der Schutz-Hook (D-448) – für Shell-Befehle im Sandkasten ist das Overlay damit nur noch normativ geschützt (`CR-2026-158`, D-468) | `<FRAMEWORK_OWNER>` |
| 0.1.9 | 2026-09-30 | **Zwei Messungen an 0.157.1** (`CR-2026-163`, D-495, D-496, `K-119`, `K-160`). Zeile B3: Der projektrelative Glob wird angenommen, das `deny`-Leserecht verlangt weiter den erhöhten Sandkasten – die Einstufung bleibt. Zeile B6: Über die Ablagen hinweg gewinnt die strengste Entscheidung | `<FRAMEWORK_OWNER>` |
| 0.2.0 | 2026-10-02 | Sprachlich überarbeitet; Zusagen, Einstufungen und Belege unverändert. Abschnitt 7.1 nennt für die Befehlsregeln des Benutzerverzeichnisses, was B6 belegt: Die strengste Entscheidung gewinnt | `<FRAMEWORK_OWNER>` |

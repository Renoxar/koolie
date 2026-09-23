# Client Pack `openai-codex`

| Attribut | Wert |
|---|---|
| Modul-ID | `CP-OC` |
| Ebene | keine – Abbildungsschicht |
| Version | 0.1.0 |
| Status | pilot |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Client | OpenAI Codex CLI |
| Verbindliche Zielversion | `0.156.x` (D-112). Die Spanne ist der Geltungsbereich dieses Packs; der gemessene Punktwert steht in der Zeile darunter (D-113). **Für dieses Pack ist die Spanne festgelegt, nicht erhoben** – erhoben ist der Punktwert |
| Geprüfte Clientversion | **`0.156.1`** – **vor** dem Erheben festgeschrieben (D-117, D-202), unverändert seit der Erhebung von `1.3.0`. Konto: `plus` |
| Stand der Produktbeobachtung | **keine**, Stand 2026-09-23. `FW-AK-01` ist für dieses Pack nicht gefahren; es gibt für diesen Client noch keine Quellenliste in Anhang 31.4. 🔴 **Das ist der Grund, warum dieses Pack keine einzige `[DOK]`-Zeile trägt** – und zugleich seine Besonderheit: Alle Belege stammen aus Messungen am Client selbst, nicht aus seiner Dokumentation |
| Datum der Prüfung | **2026-09-23** – der Bau (`CR-2026-133`, `tests/protocols/2026-09-23-bau-openai-codex.md`): 30 Messungen am Prompt-Eingang, am Konfigurationsschema, am Regelauswerter und an einer realen Installation, dazu 25 Sitzungsläufe. Zuvor 2026-09-23 – die Erhebung (`CR-2026-132`, `tests/protocols/2026-09-23-erhebung-openai-codex.md`) |

> 🟢 **Belegt, soweit gemessen (Stand 1.4.0).** Die Spalte „Einstufung" nennt die **vorgesehene** Durchsetzungstiefe, die Spalte „Beleg" ihren Nachweisstand: `gemessen` = an diesem Client beobachtet, `[EMPF]` = Vorgabe des Frameworks, `BELEG OFFEN` = noch nicht belegt, mit Grund und Datum in der Zelle – ohne Frist (D-291).
>
> 🔴 **DIESES PACK TRÄGT KEINE EINZIGE `[DOK]`-ZEILE, UND DAS IST KEIN VERSÄUMNIS.** Bei den beiden älteren Packs stand am Anfang ein Dokumentenabgleich; hier stand am Anfang ein **Meßmittel**: `codex debug prompt-input` gibt die Nachrichten aus, die der Client der nächsten Anfrage voranstellt, ohne eine Anfrage zu stellen (D-344), und `codex execpolicy check` wertet eine Befehlsregel mit dem Auswerter der Engine selbst aus – beides kostenfrei. ➡️ ***Wo der Mechanismus selbst befragt werden kann, ist die Herstellerseite der schwächere Beleg.*** Was daran fehlt, ist die **Aktualitätsaussage**: Ein Dokumentenabgleich sagt, was der Hersteller zusagt; eine Messung sagt, was dieser Stand tut. `FW-AK-01` bleibt für dieses Pack offen.
>
> 🔴 **ZWEI KERNZUSAGEN SIND `[NICHT ABBILDBAR]`: `B3` und `B5`.** Damit greift `clients/README.md` Abschnitt 4 vollständig: Begründung hier in Abschnitt 4, dokumentierte Ausnahme im Overlay des aufnehmenden Projekts – und **keine Inbetriebnahme ohne Freigabe durch `<SECURITY_CONTACT>`.**

## 1. Pfadabbildung

| Rolle des Artefakts | Pfad bei diesem Client | Belegstatus |
|---|---|---|
| Wurzel-Anweisungsdatei | `AGENTS.md` | **gemessen** (2026-09-23): Der Prompt-Eingang führt sie als eigene Nachricht `agents_md.instructions`, mit dem vollständigen Text. 🔴 **Sie ist verdrängbar** – siehe die nächste Zeile |
| Nutzerlokale Überschreibung | `AGENTS.override.md` | 🔴 **gemessen, mit Gegenprobe:** Liegt sie im Projekt, steht die Wurzel-Anweisung in **keiner** Nachricht der Sitzung; ohne sie steht sie darin. Sie **ersetzt**, sie ergänzt nicht. ⚠️ **`AGENTS.local.md` ist bei diesem Client kein Mechanismus** – dieselbe Sonde, kein Treffer. 🟢 **Drei Maßnahmen:** Der `deny`-Korb stellt die Datei schreibgeschützt, der Schutz-Hook führt sie in seinen Mustern, **Prüfung 88** meldet sie, wenn sie im Projekt liegt. Und das Pack liefert **keine** Beispieldatei dafür aus |
| Regeldateien | `.codex/rules/*.md` – **ohne Ladebedingung** | 🔴 **gemessen:** Dieser Client lädt von sich aus **keine** Regeldatei; eine Anweisungsdatei in einem Unterverzeichnis steht nicht vorab im Kontext, und eine Einbindung mit `@` bleibt wirkungslos (drei Sonden, alle negativ). Die Dateien wirken über ihre **Nennung** in der Wurzel-Anweisung (`root_instruction_imports`) – siehe R2 |
| Befehlsregeln | `.codex/rules/koolie.rules` (erzeugt aus `framework/runtime/permissions.json`) | 🟢 **gemessen an einer realen Installation:** Der Client lädt `*.rules` aus `.codex/rules/` des Projekts und aus dem Benutzerverzeichnis; ein Befehl, den diese Datei verbietet, wird abgewiesen – und der Client nennt die **Begründung dieser Datei wörtlich** |
| Skills | `.codex/skills/<name>/SKILL.md` **und** `.agents/skills/<name>/SKILL.md` | 🟢 **gemessen mit drei Sonden an drei Orten, eine davon negativ:** Beide Ablagen laden; ein `skills/` an der Projektwurzel lädt **nicht**. Der Prompt-Eingang führt eine **Herkunftstabelle** der Skillwurzeln. ⚠️ **Skills laden auch ohne Vertrauenseintrag** – der Client sagt es selbst: *„Project-local config, hooks, and exec policies are disabled … but skills still load"* |
| Subagentenprofile | `.codex/agents/<name>.toml` | ⚠️ **Gestalt gemessen, Abbildung nicht gebaut:** Pflichtfelder `name`, `description`, `developer_instructions`; `permissions` und `tools` werden angenommen, `allowed_tools` verworfen – erhoben über die Meldungen, die ein fehlendes oder unbekanntes Feld erzeugt. Das Framework legt sein Profil weiter als Markdown unter `.codex/agents/` ab; die Wirkung einer Rollendatei ist **unerhoben**, und A1 sagt es |
| Berechtigungskonfiguration (Pfadseite) | `.codex/config.toml` (erzeugt aus `framework/runtime/permissions.json`) | 🟢 **gemessen:** Ein Rechteprofil unter `[permissions.<name>]` mit `default_permissions`; die Tabelle `filesystem` bindet **Pfad → Zugriffsart**. 🔴 **Ihre Schlüssel nehmen kein Muster** (siehe B3), und die Datei lädt nur bei eingetragenem Vertrauen |
| Hook-Konfiguration | `.codex/hooks.json`, Ereignisse unter dem Schlüssel `hooks` | 🟢 **gemessen:** `.codex/hooks/hooks.json` wird **nicht** gelesen; eine Datei ohne den Schlüssel `hooks` meldet der Client als *unknown field* und **lädt sie nicht**, startet aber. Ereignisse: `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `SubagentStart`, `SubagentStop`, `Stop`, `Interrupt`. 🔴 **Jeder Eintrag braucht `"enabled": true`** – ohne das läuft er nicht, und der Client meldet es nicht |
| MCP-Konfiguration | `.codex/config.toml` unter `[mcp_servers.<name>]` | 🟢 **gemessen:** Der Client zählt einen projektlokal eingetragenen Server; eine Datei `.mcp.json` bleibt **unbeachtet**. Das Framework liefert **keinen** Server aus |
| Projektverzeichnis im Hook-Befehl | **keine Variable – das Arbeitsverzeichnis** | 🔴 **gemessen am Hook-Prozess:** Seine Umgebung führt außer dem Verweis auf das eigene Benutzerverzeichnis des Clients **nichts**; sein **Arbeitsverzeichnis ist das Projektverzeichnis**. Die Abbildung bindet deshalb den relativen Punkt (`hook_project_dir_expr`). Eine Variable, die es nicht gibt, hätte ein Kommando erzeugt, das startet und nichts findet |

## 1a. Semantikabbildung der Berechtigungen

Die Regelmenge liegt werkzeugneutral im Kern (`.koolie/core/framework/runtime/permissions.json`) und wird bei der Installation übersetzt (D-18). Was dabei abgebildet wird, steht maschinenlesbar im `manifest.json`; diese Tabelle ist die menschenlesbare Fassung.

🔴 **DIE BESONDERHEIT DIESES PACKS: DIE REGELMENGE ZERFÄLLT IN ZWEI ERZEUGNISSE** (D-346). Dieser Client kennt keine Regel der Gestalt `Werkzeug(Muster)`. Er bindet **Pfade an eine Zugriffsart** und **Befehle an Präfixmuster**, und beides steht in verschiedenen Dateien.

| Neutrales Werkzeugverb | Form bei diesem Client | Anmerkung |
|---|---|---|
| `read` | – | 🔴 **Kein Werkzeugname, und kein abbildbares Muster.** Der Lesekorb des Kerns fällt aus; die Begründung steht in B3 und in Abschnitt 4 |
| `search` | – | Dieser Client führt **kein eigenes Suchwerkzeug**; Suchen läuft über die Shell und damit unter `exec`. Gemessen: Ein Hook-Matcher `Grep` löst in keinem Lauf aus |
| `write` | Pfadeintrag `":workspace/<pfad>" = "read"` | Ein Schreibverbot auf einem Teilbaum heißt hier: lesbar, nicht schreibbar. **Nur ohne Muster** – `**/*.lock` fällt aus (B5) |
| `exec` | `prefix_rule(pattern = [...], decision = "forbidden"\|"prompt"\|"allow")` | Präfixbasiert, **mit dem Auswerter des Clients gemessen**. Grenze wie bei `claude-code`: `git -C . push` trifft `["git","push"]` nicht |
| `fetch` | – | Kein Mechanismus; der Kern sagt die Domainbeschränkung seit 0.33.0 nicht mehr zu (B11, D-59). Siehe B10 |
| `mcp` | – | Keine Rückfrageregel je Server; wirksam ist, dass **kein** Server ausgeliefert wird (X1) |
| `skill` | – | Kein Mechanismus erhoben |

| Weitere Eigenschaft | Wert |
|---|---|
| Grundstock des Rechteprofils | `":root" = "read"`, `":workspace" = "write"` |
| Schlüsselform der Pfadseite | absoluter Pfad, `~/`-Pfad oder Sonderziel (`:root`, `:workspace`, `:workspace/<pfad>`) |
| Hook-Werkzeugnamen | `Bash` (Ausführen und damit Lesen und Suchen), `apply_patch` (Schreiben) |
| Projektverzeichnis im Hook-Befehl | keine Variable – das Arbeitsverzeichnis |
| Sperrform des Schutz-Hooks | `hookSpecificOutput.permissionDecision = "deny"`, Exit 0 |

Die Abbildung ist kein freies Feld: Die Präfixform eines Befehlsverbots muss ein Präfix seiner wörtlichen Form sein, und bei `allow` müssen beide Formen übereinstimmen – sonst scheitert die Installation. Was sich **gar nicht** abbilden lässt, steht in Abschnitt 4 und nicht in einer Ausnahme im Code.

## 1b. Der Vertrauenseintrag – die Bedingung über der ganzen projektlokalen Schicht

🔴 **Konfiguration, Hooks und Befehlsregeln laden nur, wenn das Projekt in der Benutzerkonfiguration des Clients als vertraut eingetragen ist.** A/B gemessen mit zwei Benutzerverzeichnissen und identischem Projekt; der Client sagt es selbst: *„Project-local config, hooks, and exec policies are disabled in the following folders until the project is trusted, but skills still load."*

➡️ ***Ein versionierter Träger, der nicht lädt, trägt nichts.*** Der Eintrag liegt **außerhalb des Repositoriums**, ist je Arbeitsplatz zu setzen und kann vom Framework nicht ausgeliefert werden. `install.py` nennt ihn deshalb als Schritt nach der Installation; **B1**, **H1** und **H2** tragen die Bedingung in ihrer Belegzelle.

⚠️ **Und der Eintrag wird üblicherweise einmal und beiläufig erteilt.** Der Vorbedingungsdurchgang von `1.3.0` hat auf dem Arbeitsplatz des Frameworks einen Eintrag auf das **Benutzerprofil** gefunden, der jeden Pfad darunter einschließt – und einen auf den alten Projektnamen.

🔴 **Die Hooks tragen eine zweite Bedingung, und sie ist schärfer:** Ein Hook läuft erst, wenn ihm **einzeln vertraut** wurde; das Vertrauen hängt an einem **Hash**. Gemessen am 2026-09-23: Ohne dieses Vertrauen läuft der Schutz-Hook **gar nicht**, der Köderinhalt kommt heraus – und **`codex doctor --all` meldet es nicht**. ➡️ ***Jede Hebung des Frameworks ändert den Hook und damit den Hash.*** Ein Projekt, das nach `install.py --update` nicht erneut vertraut, läuft ab dann ohne Schutz-Hook.

## 2. Fähigkeitsmatrix

Einstufung je Zusage: `[TECHNISCH]` erzwungen · `[TEXTUELL]` nur Anweisung · `[NICHT ABBILDBAR]` kein Mechanismus. Regeln in `../README.md` Abschnitt 4.

**Zur Belegspalte.** Dieses Pack trägt keine `[DOK]`-Zeile (siehe Vorbemerkung); wo andere Packs eine Quellenkennung führen, steht hier das Wort **gemessen** mit dem Meßmittel. Prüfung 73 verlangt eine Quellenkennung nur von `[DOK]`-Zeilen.

### R – Regelladung

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| R1 | Wurzel-Anweisungsdatei wird ungefragt geladen | `AGENTS.md` steht als eigene Nachricht im Prompt jeder Sitzung | `[TECHNISCH]`, **mit benannter Bedingung** | 🟢 **gemessen** (2026-09-23, `codex debug prompt-input`): Der vollständige Text steht im Prompt. 🔴 **Die Bedingung ist die Verdrängung:** Liegt `AGENTS.override.md` daneben, steht die Wurzel-Anweisung in **keiner** Nachricht – gemessen mit Gegenprobe. ➡️ *Eine Wurzel-Anweisung, die eine ungeprüfte Datei im selben Verzeichnis ersetzen kann, ist keine Ebene 1 – sie ist ein Standard.* **Prüfung 88** meldet die Datei, der `deny`-Korb stellt sie schreibgeschützt, und der Schutz-Hook führt sie in seinen Mustern |
| R2 | Regeldateien mit Ladebedingungen | 🔴 **kein Mechanismus.** **Ersatz, geliefert:** Die Wurzel-Anweisung **nennt** die Regeldateien mit der Auflage, sie zu Beginn der Sitzung zu lesen (`root_instruction_imports`) | `[NICHT ABBILDBAR]` | 🟢 **gemessen mit drei Sonden:** Eine Anweisungsdatei in einem Unterverzeichnis steht nicht vorab im Kontext; eine Einbindung mit `@<pfad>` bleibt wirkungslos; nur `AGENTS.md` des Projekts und die gleichnamige Datei im Benutzerverzeichnis des Clients laden ungefragt. 🟢 **Die Mechanik des Ersatzes steht seit 0.15.0 im Kern und war von keinem Pack erprobt** – dieses Pack ist ihr erster Gegenstand (D-348). ⚠️ **Der Ersatz ist schwächer, und das ist der Preis:** Was eine Nennung bewirkt, hängt am Modell und nicht an der Engine |
| R3 | Regeln an Dateimuster bindbar | 🔴 **kein Mechanismus.** **Ersatz:** dieselbe Nennung – ein Technology Pack lädt damit **immer** statt nur bei seinen Dateien | `[NICHT ABBILDBAR]` | wie R2. ⚠️ **Die Verschärfung ist benannt:** Unbedingtes Laden ist mehr Kontext, keine Lockerung – dieselbe Richtung wie die Abbildung von `model_decision` beim Pack `claude-code`. **Preis:** Ein später hinzugefügtes Technology Pack wirkt erst nach einem erneuten `install.py --update`, weil die Nennung in der Wurzel-Anweisung dann neu geschrieben wird |
| R4 | Bekanntes Zeichenlimit | **Vorgabe des Frameworks, keine Produkteigenschaft** – 12.000 je Regeldatei, 6.000 für die Overlay-Laufzeitregel | `[TEXTUELL]` | `[EMPF]`. **Für diesen Client ist kein Limit erhoben**; der Prompt-Eingang zeigt den vollständigen Text der Wurzel-Anweisung, eine Obergrenze sagt er nicht. `K-19` gilt hier ebenso |
| R5 | Die geladenen Regelquellen sind vollständig aufzählbar | `codex debug prompt-input` gibt **jede** Nachricht aus, die der Client der nächsten Anfrage voranstellt – ohne eine Anfrage zu stellen | `[TEXTUELL]` | 🟢 **gemessen, und schärfer als bei beiden Schwesterpacks:** Die Auskunft ist nicht ein Register des Clients über seine Konfiguration, sondern **der Kontext selbst**. Damit ist auch eine **Abwesenheit** ablesbar – die Verdrängung aus R1 ist genau so gefallen. ⚠️ **Trotzdem `[TEXTUELL]`:** Eine Auskunft ist keine Schranke, und sie entsteht nur, wenn ein Mensch das Kommando ausführt |
| R6 | Keine Importe fremder Werkzeugformate | 🔴 **Kein Schalter erhoben.** Gemessen ist die Lage: Dieser Client liest `.codex/skills/` und `.agents/skills/` – **nicht** die Skillablage eines fremden Werkzeugs | `[NICHT ABBILDBAR]` | 🟢 **gemessen** (drei Sonden): Eine dritte, naheliegende Ablage an der Projektwurzel lädt nicht; eine fremde Ablage ist in der Herkunftstabelle des Prompts nicht aufgetaucht. **Ersatz: die Auskunft in Abschnitt 7** – und der gemessene Befund, dass es hier nichts abzuschalten gibt. ⚠️ **Das ist eine Aussage über diesen Stand, keine Zusage des Herstellers** |

### S – Skills

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| S1 | Versionierte Skills im Repository | `.codex/skills/<name>/SKILL.md` mit Frontmatter | `[TECHNISCH]` | 🟢 **gemessen:** Ein Skill aus dieser Ablage steht mit Name und Beschreibung im Prompt jeder Sitzung, samt Herkunftswurzel |
| S2 | Gezielter Aufruf | Der Prompt führt die Skills als Liste mit Beschreibung und Pfad; das Modell liest die `SKILL.md` | `[TEXTUELL]` | ⚠️ **`BELEG OFFEN` für den Aufruf als Werkzeugaufruf** (2026-09-23): Gemessen ist, dass die Skills **im Kontext stehen**; ob dieser Client einen eigenen Werkzeugaufruf oder eine Schrägstrich-Form dafür führt, ist unerhoben. Ohne das ist der Aufruf Modellverhalten |
| S3 | Werkzeugbeschränkung je Skill | 🔴 **unerhoben.** Die Frontmatter-Felder `permissions` und `triggers` erreichen die installierte Fassung **unverändert** – dieses Pack führt sie nicht in `drop_fields` | `[TEXTUELL]` | ⚠️ **`BELEG OFFEN`** (2026-09-23): Ob ein Frontmatter-Feld den Werkzeugbestand eines Skills begrenzt, ist bei diesem Client nicht gemessen, und **ein unbekanntes Frontmatter-Feld meldet er nicht**. Ein geratenes Feld sähe aus wie eine Schranke. **Was trägt, ist die globale Schicht:** die Befehlsregeln und der Schutz-Hook, beide unabhängig vom Skill – weniger als eine Beschränkung je Skill, und das ist die Aussage (Bauform von B01, D-50) |
| S4 | Schreibende Skills nur benutzergetriggert | Framework-Konvention, statisch geprüft durch `validate-framework.py` | `[TEXTUELL]` | `[EMPF]`. **Ein Feld, mit dem sich ein Skill vom Modellzugriff ausnehmen ließe, ist bei diesem Client unerhoben** – `model_invocation_field` bleibt deshalb leer, und das ist eine Aussage über den Belegstand. **Reichweite:** Die Zusage gilt für die Skill-Ablage, die das Framework schreibt |
| S5 | Die geladenen Skills sind vollständig aufzählbar, samt Herkunft | Der Prompt-Eingang führt eine **Tabelle der Skillwurzeln** (`r0`, `r1`, …) und je Skill Name, Beschreibung und Pfad relativ zu seiner Wurzel | `[TEXTUELL]` | 🟢 **gemessen erfüllt, und vollständiger als bei beiden Schwesterpacks:** Die Aufzählung ist nicht ein Kommando, das mehr zeigt als lädt (`devin-desktop`, D-288), sondern **der Sitzungskontext selbst**. Drei Sonden an drei Orten, eine negativ. ⚠️ **Zwei eingebaute Skillwurzeln des Clients stehen mit darin** – die Auskunft ist damit auch die Stelle, an der man sie sieht |

### B – Berechtigungen

> **`[TECHNISCH]` heißt in diesem Block:** Die Engine setzt die Regel durch, **solange der Betriebsmodus die Berechtigungsprüfung nicht abschaltet** (D-35). 🔴 **Für dieses Pack kommen ZWEI weitere Bedingungen hinzu, und beide sind gemessen.**
>
> **(1) Der Vertrauenseintrag.** Konfiguration, Hooks und Befehlsregeln laden nur bei eingetragenem Vertrauen (Abschnitt 1b). Ohne ihn trägt von diesem Block **nichts**.
>
> **(2) Die Rechtestufe des Betriebssystems.** 🔴 **Auf einem unerhöhten Windows-Arbeitsplatz kann der Sandkasten dieses Clients ein `deny`-Leserecht nicht durchsetzen – und der Client läuft dann gar nicht:** *„windows unelevated restricted-token sandbox cannot enforce deny-read restrictions directly; refusing to run unsandboxed"*. 🟢 **Das Verhalten ist fail-closed und damit richtig.** Für das Pack heißt es: Die Pfadseite trägt **Schreibverbote**, aber **kein Leseverbot** – und das ist der zweite Fall für die Vorbemerkung nach D-35, diesmal einer, der nicht vom **Modus**, sondern vom **Betriebssystem und der Rechtestufe** abhängt.
>
> 🟢 **Und genau dort trägt die zweite Linie:** Im Betriebsmodus, der Rückfragen **und** Sandkasten abschaltet, hat der Schutz-Hook denselben Lesezugriff blockiert, den die Berechtigungsschicht durchließ – gemessen mit Gegenlauf, in einem Baum **ohne** Regeltexte. **Erste und zweite Linie fallen unter verschiedenen Bedingungen; das ist die empirische Rechtfertigung des Hooks.**

Die mit **Kern** markierten Zeilen entsprechen `_core_rules_integrity` in der Berechtigungsdatei. Eine Abweichung von `[TECHNISCH]` ist dort begründungspflichtig.

| ID | Zusage des Frameworks | Kern | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|---|
| B1 | Berechtigungen versioniert im Repository | ja | `.codex/config.toml` (Pfadseite) **und** `.codex/rules/koolie.rules` (Befehlsseite) – beide im Projekt, beide versioniert | `[TECHNISCH]`, **bedingt** | 🟢 **gemessen:** Beide Träger liegen im Repositorium und werden aus derselben Kernquelle erzeugt. 🔴 **Die Bedingung steht außerhalb:** Ohne Vertrauenseintrag lädt **keiner von beiden** (Abschnitt 1b, A/B gemessen). ➡️ *Ein versionierter Träger, der nicht lädt, trägt nichts* |
| B2 | Verweigern vor Rückfragen vor Erlauben | ja | Die Regelsprache kennt `forbidden`, `prompt` und `allow`; bei mehreren Treffern gilt die **strengste** | `[TECHNISCH]` | 🟢 **gemessen mit dem Auswerter der Engine selbst** (`codex execpolicy check`, 2026-09-23): Zwei Regeln auf denselben Befehl, `allow` und `forbidden` → `forbidden`; `prompt` und `allow` → `prompt`. **Unabhängig von der Reihenfolge in der Datei** – beide Fälle einmal in jeder Reihenfolge gefahren |
| B3 | Secret-Dateien per Pfadmuster lesegeschützt | ja | 🔴 **kein abbildbarer Mechanismus.** **Ersatz: der Schutz-Hook**, gemessen – siehe Abschnitt 4 | `[NICHT ABBILDBAR]` | 🔴 **gemessen, und die beiden Gründe verstärken einander.** **(1) Musterform und Versionierbarkeit schließen einander aus:** Ein Musterausdruck ist als Schlüssel nur mit **absolutem** oder `~/`-Vorsatz zulässig – und ein absoluter Pfad in einem versionierten Träger wäre ein Wert dieser Arbeitsstation; ein projektrelativer Schlüssel (`:workspace/…`) nimmt **kein** Muster (*„must be absolute, use `~/…`, or start with `:`"*). **(2) Ein `deny`-Leserecht verlangt den erhöhten Windows-Sandkasten**, und ohne ihn läuft der Client gar nicht. 🟢 **Ersatz, gemessen:** Der Schutz-Hook blockiert den Lesezugriff auf `.env` – in einem Baum ohne Regeltexte und im Modus ohne Rückfragen und ohne Sandkasten, mit Gegenlauf, in dem der Köderinhalt wörtlich herauskam. **Kernzusage: Abschnitt 4 und Freigabe durch `<SECURITY_CONTACT>`** |
| B4 | Framework- und Overlay-Artefakte schreibgeschützt | ja | Pfadeinträge `":workspace/.koolie/core" = "read"`, `":workspace/.koolie/project-overlay" = "read"`, `":workspace/.codex" = "read"`, `":workspace/AGENTS.md" = "read"` **und** der Schutz-Hook | `[TECHNISCH]` für das direkte Schreiben (über den Hook); **`[TEXTUELL]` für Shell und Unterprozess** | 🟢 **Der Hook ist gemessen** (2026-09-23, Baum ohne Regeltexte): Ein `apply_patch` auf `.koolie/core/notiz.txt` wurde blockiert; **im Lauf davor, mit der alten Musterform, wurde die Datei angelegt.** 🔴 **Der Befund dahinter gehört in diese Zeile:** Das Schreibwerkzeug dieses Clients führt **keinen Pfad in einem Feld** – der Pfad steht im **Patchtext**, hinter einem Leerzeichen, und die Pfadmuster des Hooks kannten als Grenze nur den Schrägstrich. ➡️ *Eine Grenze, die nur den Schrägstrich kennt, mißt die Schreibweise und nicht die Sache* (D-347). ⚠️ **Die Pfadseite ist erzeugt, aber nicht an ihrer Wirkung gemessen** – auf diesem Arbeitsplatz ist der Sandkasten abgeschaltet, und damit ist ein Treffer nicht zurechenbar |
| B5 | CI-, Quality-Gate- und Lockdateien schreibgeschützt | ja | 🔴 **kein abbildbarer Mechanismus, und Ersatz: KEINER** – der Schutz-Hook deckt diese Pfade nicht; siehe Abschnitt 4 | `[NICHT ABBILDBAR]` | 🔴 **gemessen:** Die Regeln des Kerns sind hier **Namensmuster** (`**/*.lock`, `**/package-lock.json`, …) und **Platzhalterlisten** (`<CI_CONFIG_PATHS>`, `<QUALITY_GATE_CONFIG_PATHS>`). Für beide gilt dieselbe Schlüsselsyntax wie bei B3: kein Muster ohne absoluten Vorsatz, kein Schlitz auf der Schlüsselseite einer TOML-Tabelle. **Und der Schutz-Hook trägt sie nicht** – seine Muster decken Secrets, die Laufzeitschicht und das Kernverzeichnis, nicht die Lockdateien eines Projekts. **Kernzusage: Abschnitt 4 und Freigabe durch `<SECURITY_CONTACT>`** |
| B6 | Befehle per Muster verweigerbar | ja | `prefix_rule(pattern = [...], decision = "forbidden")` in `.codex/rules/koolie.rules` | `[TECHNISCH]` | 🟢 **an einer realen Installation gemessen** (2026-09-23): Der Befehl wurde abgewiesen, **und der Client nannte die Begründung dieser Datei wörtlich** – dieselbe Zurechenbarkeit wie beim `deny`-Korb von `devin-desktop`. Zusätzlich mit dem Auswerter der Engine gegengeprüft: `git push origin main` → `forbidden`, `git status` → `allow`. ⚠️ **Grenze, gemessen und benannt:** `git -C . push` trifft `["git","push"]` **nicht** – dieselbe Grenze wie bei `claude-code` |
| B7 | Schreiboperationen fragen zurück | – | `approval_policy = "on-request"` als Standard des Clients | `[TECHNISCH]` für den Modus; **`[TEXTUELL]` für die Regel je Pfad** | 🟢 **gemessen** (`codex doctor`): Der Standard ist `OnRequest`. 🔴 **Die `ask`-Regel des Kerns auf alle Schreiboperationen ist hier nicht abbildbar** – dieser Client kennt keine Rückfrageregel je Pfad, nur eine Politik je Sitzung. ⚠️ **Und die projektlokale Schicht kann sie LOCKERN** (B9) |
| B8 | Netzwerkzugriff standardmäßig unterbunden | – | Netzsandkasten des Clients (`restricted`) **und** die Befehlsregeln auf `curl`, `wget`, `ssh`, `scp` | `[TECHNISCH]` für den Sandkasten und für diese vier Programme; **`[TEXTUELL]` darüber hinaus** | 🟢 **gemessen** (`codex doctor`: *network sandbox restricted*; die vier Programme stehen im `forbidden`-Korb der erzeugten Regeldatei). ⚠️ **Jedes andere netzfähige Programm ist nicht erfasst**, und die Liste wird bewusst nicht verlängert |
| B9 | Nutzerlokale Konfiguration kann nur verschärfen | – | 🔴 **Widerlegt, und zwar im Spiegelbild** | `[TEXTUELL]` | 🔴 **gemessen mit Gegenprobe** (A/B, zwei Benutzerverzeichnisse): Nicht die nutzerlokale Konfiguration lockert die projektseitige – **die PROJEKTLOKALE lockert den Benutzerstandard.** Mit Vertrauenseintrag schlagen `approval_policy = "never"` und ein Sandkastenmodus ohne Schranken **aus dem Projekt heraus** den Standard des Arbeitsplatzes. ➡️ *Dieselbe Frage, drei Clients, drei Antworten:* `claude-code` hält die Richtung, `devin-desktop` kehrt sie um, und hier ist die **lockernde Seite die versionierte**. ⚠️ **Für ein aufnehmendes Projekt heißt das:** Wer die Berechtigungsdatei liest, liest auch, was sie am Arbeitsplatz **aufhebt** |
| B10 | Externer Abruf auf freigegebene Domains beschränkbar | – | 🔴 **kein Mechanismus.** Der Kern sagt die Beschränkung seit 0.33.0 nicht mehr zu (B11, D-59) | `[NICHT ABBILDBAR]` | **Kein Ersatz durch das Framework, und das ist eine Aussage und kein Rest.** Was den Kanal steuert, ist der **Netzsandkasten** des Clients (B8) und die Befehlsregel auf die vier Programme; eine Domainangabe kennt keine der beiden Schichten. **Der organisatorische Ersatz** ist die Freigabezeile des Overlays, und sie hat nach D-65 keine technische Seite |

### H – Hooks

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| H1 | Prüfung vor Werkzeugausführung | `PreToolUse` in `.codex/hooks.json`, Matcher `Bash\|apply_patch` | `[TECHNISCH]`, **doppelt bedingt** | 🟢 **gemessen an einer realen Installation** (2026-09-23): Der Hook läuft bei jedem Shell- und jedem Schreibaufruf; der Umschlag führt `session_id`, `turn_id`, `transcript_path`, `cwd`, `hook_event_name`, `model`, `permission_mode`, `tool_name`, `tool_input` und `tool_use_id`. 🔴 **Bedingung 1: `"enabled": true` je Eintrag** – ohne das läuft er nicht, und der Client meldet es nicht. 🔴 **Bedingung 2: Hook-Vertrauen** – ohne persistiertes Vertrauen läuft er **gar nicht**, der Köderinhalt kommt heraus, und `codex doctor --all` sagt nichts dazu. **Jede Hebung des Frameworks ändert den Hash** (Abschnitt 1b) |
| H2 | Prüfung kann **blockieren** | `hookSpecificOutput.permissionDecision = "deny"` und **Exit 0** | `[TECHNISCH]` | 🔴 **DER SCHWERSTE BEFUND DIESES PACKS, UND ER IST GEMESSEN** (D-347): Die bis `1.3.0` einzige Sperrform des Schutz-Hooks – `{"decision": "block"}` und **Exit 2** – bewirkt bei diesem Client **nichts**. Der Client meldet *PreToolUse Failed* und **führt die Operation aus**; im Gegenlauf kam der Köderinhalt wörtlich heraus. 🟢 **Dieselbe Sperre in der Form, die er liest, blockiert** – gemessen in einem Baum **ohne** Regeltexte und im Modus, der Rückfragen **und** Sandkasten abschaltet, mit Positivkontrolle im selben Baum. ➡️ *Ein Hook, der läuft und dessen Sperrform der Client nicht liest, ist eine Zusage ohne Mechanismus.* **Prüfung 86** hält die Kette aus Manifest, Skript und erzeugtem Kommando zusammen |
| H3 | Statusmeldung beim Sitzungsstart | `SessionStart` mit `hook-overlay-status.py` | `[TECHNISCH]` | 🟢 **beobachtet** (2026-09-23): Der Hook läuft, und **seine Ausgabe steht im Sitzungskontext** – ein Lauf im Baum ohne Regeltexte hat den Overlay-Status daraus zitiert. Das ist mehr als bei beiden Schwesterpacks, wo die Meldung selbst unbeobachtet blieb |
| H4 | Eingabeschema und Pfadidentität des Schutz-Hooks | Ereignisprüfung, Pfadidentität über den aufgelösten Pfad, alle Pfadmuster ohne Rücksicht auf Groß-/Kleinschreibung. **`hook_fail_closed` steht auf `false`** | `[TECHNISCH]` für die Musterprüfung, **mit zwei benannten Grenzen** | 🟢 **Das Schema von `PreToolUse` ist aufgezeichnet** (zehn Felder, siehe H1) – **der vollständige Bestand der zwölf Ereignisse ist es nicht**, und deshalb bleibt `hook_fail_closed` auf `false`: Fail-closed bei teilweise erhobenem Schema wäre keine Härtung, sondern eine Sitzung, die bei der ersten unbekannten Eingabeform blockiert (D-31). 🔴 **Zweite Grenze, gemessen und behoben:** Das Schreibwerkzeug führt **keinen Pfad in einem Feld**; er steht im Patchtext hinter einem Leerzeichen. Die Pfadmuster des Hooks kannten als Grenze nur den Schrägstrich und trafen deshalb nicht – seit `1.4.0` ist die Grenze auch ein Leerzeichen, und das ist eine **Verschärfung für alle drei Packs** (D-347) |

### A – Agentenprofile

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| A1 | Rein lesendes Reviewprofil | 🔴 **nicht abgebildet.** Der Client liest Rollendateien als `.codex/agents/<name>.toml`; das Framework legt sein Profil als Markdown ab | `[NICHT ABBILDBAR]` | ⚠️ **Die Gestalt ist gemessen, die Wirkung nicht** (2026-09-23): Pflichtfelder `name`, `description`, `developer_instructions`; `permissions` wird als Tabelle angenommen, `allowed_tools` verworfen. **Nicht gemessen ist, ob und wie ein Feld den Werkzeugbestand eines Unteragenten begrenzt** – und dieser Client startet Unteragenten (der Prompt führt sechs Werkzeuge dafür). **Ersatz, benannt:** Der Schutz-Hook und die Befehlsregeln wirken unabhängig vom Profil; ob sie einen Unteragenten **erfassen**, ist ebenfalls unerhoben. ➡️ *Eine Abbildung ohne Messung wäre dieselbe Lage, aus der `AP2-CC-13` kam* |
| A2 | Rein lesendes Analyseprofil für Modus M1 | 🔴 **kein eingebautes Profil erhoben** | `[NICHT ABBILDBAR]` | **Ersatz, benannt:** der Standardmodus des Clients (`approval_policy = "on-request"`, Sandkasten lesend) – er ist gemessen und wirkt ohne Profil. ⚠️ **Das ist ein Modus und kein Profil**, und der Unterschied ist, dass er für die ganze Sitzung gilt |

### M – Modi und Sitzungsfreigaben

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| M1 | Standardmodus fragt bei Schreiben und Befehlen zurück | `approval_policy = "on-request"`, Sandkasten `read-only` | `[TECHNISCH]` | 🟢 **gemessen** (`codex doctor`): *approval OnRequest · restricted fs + restricted network*. ⚠️ **Der nicht-interaktive Lauf kennt keine Rückfrage** – dort wird abgewiesen statt gefragt; das ist eine Verschärfung und kein Messwert über den interaktiven Betrieb |
| M2 | Modus ohne Rückfragen ausschließbar | 🔴 **Eine Sperre des Modus ist nicht erhoben.** Der Modus selbst heißt `--dangerously-bypass-approvals-and-sandbox` und bezeichnet sich als gefährlich | `[TEXTUELL]` | 🟢 **Was gemessen ist, ist die Wirkung der zweiten Linie:** In genau diesem Modus hat der Schutz-Hook den Zugriff blockiert, den die Berechtigungsschicht durchließ. ⚠️ **Die Sperre des Modus bleibt unerhoben** – eine Organisationsebene, die ihn ausschlösse, ist für diesen Client nicht gemessen |
| M3 | Freigabe auf die Sitzung begrenzbar | Der Client kennt eine Freigabe „für die Sitzung" und eine über ein Befehlspräfix | `[TEXTUELL]` | ⚠️ **`BELEG OFFEN`** (2026-09-23): Die Stufen sind in der Bedienoberfläche des Clients benannt; **im nicht-interaktiven Betrieb ist keine davon messbar** – eine Rückfrage an einen Menschen läßt sich so nicht messen. Dieselbe Enthaltung wie bei `devin-desktop` für `ask` und `allow` (D-280) |
| M6 | Modus mit automatischer Übernahme von Dateiänderungen begrenzbar | Sandkastenmodus `workspace-write` – nach D-05 nur über dokumentierte Ausnahme bei Kontrollstufe niedrig zulässig | `[TEXTUELL]` | `[EMPF]` für die Beschränkung; **eine Abschaltung des Modus ist nicht erhoben**. ⚠️ **Und die projektlokale Schicht kann ihn setzen** (B9) – das ist der Unterschied zu beiden Schwesterpacks |
| M7 | Modus, der selbst beurteilt, was sicher ist, begrenzbar | 🔴 **Ein solcher Modus ist für diesen Client nicht erhoben** | `[TEXTUELL]` | **Ersatz, benannt:** Es gibt keinen – die Zusage hat hier keinen Gegenstand, solange kein selbst beurteilender Modus erhoben ist. ⚠️ *Eine Zusage ohne Gegenstand ist keine erfüllte Zusage, und sie steht hier, damit sie nicht als eine gelesen wird* |

### X – Externe Anbindung

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| X1 | Keine externe Anbindung ohne Einzelfreigabe | Das Framework liefert **keinen** MCP-Server aus; ein Server wäre eine Tabelle `[mcp_servers.<name>]` in der Berechtigungsdatei | `[TEXTUELL]`, **mit einer benannten Grenze** | 🟢 **gemessen:** Ohne Eintrag zählt der Client **null** Server; ein projektlokal eingetragener wird gezählt. 🔴 **Die Grenze:** Eine Rückfrageregel je MCP-Werkzeug – die `ask`-Regel des Kerns – ist bei diesem Client **nicht abbildbar**. Was trägt, ist die Abwesenheit des Eintrags, und die ist eine Framework-Entscheidung, keine Schranke des Clients. ⚠️ **Die Benutzerkonfiguration kann Server führen**, und sie liegt außerhalb des Repositoriums (Abschnitt 7.2) |
| X2 | Art und Ort der Codebasis-Indexierung bekannt | Kein Mechanismus zur Steuerung bekannt | `[NICHT ABBILDBAR]` | `BELEG OFFEN (dauerhaft)` – von außen nicht zu beobachten, Stand 2026-09-23 (`K-20`, D-292). **Kein Ersatz durch das Framework:** Was ein Client indexiert und wohin er es gibt, sieht weder die Installation noch der Validator. Nach D-41 eine **Fähigkeitszusage**, keine Kernzusage |

## 3. Zusammenfassung der Durchsetzungstiefe

> **Zählregel (normativ für diese Tabelle):** Eine Zeile zählt bei ihrer **schwächsten** Einstufung. Trägt sie zwei Angaben je Zugriffskanal, zählt sie als die schwächere (D-47). Prüfung 31 rechnet die Summen aus der Matrix nach.

| Klasse | Anzahl | davon Kernzusagen |
|---|---|---|
| `[TECHNISCH]` | **10 von 34** | 4 von 6 (B1, B2, B4, B6) |
| `[TEXTUELL]` | **15 von 34** | 0 von 6 |
| `[NICHT ABBILDBAR]` | **9 von 34** | 2 von 6 (B3, B5) |

**Belegstand:** **3 der 34 Zeilen** sagen `BELEG OFFEN` – **S2**, **S3** und **M3**, dazu **X2** dauerhaft. 🔴 **Das ist der schwächste Belegstand der drei Packs, und er hat einen Grund:** Dieses Pack ist am Tag seines Baus entstanden; die Zeilen, die eine reale Installation brauchen, sind gefahren (B2, B4, B6, H1 bis H3, R1, R5, S1, S5), die übrigen nicht. ⚠️ **Was ganz fehlt, ist die Produktbeobachtung** – `FW-AK-01` ist für diesen Client nicht gefahren, und es gibt keine Quellenliste.

## 4. Kernzusagen ohne technische Durchsetzung

**Zwei der sechs Kernzusagen sind `[NICHT ABBILDBAR]`.** Damit greift `clients/README.md` Abschnitt 4 vollständig: Begründung hier, dokumentierte Ausnahme im Overlay des aufnehmenden Projekts (`.koolie/project-overlay/exceptions/EXCEPTIONS.md`) – und **keine Inbetriebnahme ohne Freigabe durch `<SECURITY_CONTACT>`.**

| ID | Einstufung | Warum der Client das nicht durchsetzt | Ersatzmaßnahme | Freigabe |
|---|---|---|---|---|
| B3 | `[NICHT ABBILDBAR]` | **Zwei gemessene Gründe, die einander verstärken.** (1) Die Schlüssel der Pfadrechteschicht nehmen ein Muster nur mit **absolutem** oder `~/`-Vorsatz an; ein projektrelativer Schlüssel nimmt keines. **Musterform und Versionierbarkeit schließen einander aus** – und B1 verlangt die Versionierbarkeit. (2) Ein `deny`-Leserecht verlangt den **erhöhten Windows-Sandkasten**; ohne ihn weist der Client den Start ab (fail-closed) | **Ersatz: der Schutz-Hook, und er ist gemessen.** Er blockiert den Lesezugriff auf `.env` in einem Baum ohne Regeltexte und im Modus ohne Rückfragen und ohne Sandkasten, mit Positivkontrolle. ⚠️ **Er trägt die Bedingungen aus H1** – `enabled` und Hook-Vertrauen | `<SECURITY_CONTACT>` |
| B5 | `[NICHT ABBILDBAR]` | Die Regeln des Kerns sind hier **Namensmuster** (`**/*.lock`) und **Platzhalterlisten** (`<CI_CONFIG_PATHS>`, `<QUALITY_GATE_CONFIG_PATHS>`). Für die Muster gilt derselbe Grund wie bei B3; für die Listen kommt hinzu, dass die Schlüsselseite einer TOML-Tabelle keinen Ausfüllschlitz kennt | 🔴 **Kein vollständiger Ersatz, und das ist die Aussage.** Der Schutz-Hook deckt Secrets, die Laufzeitschicht und das Kernverzeichnis – **nicht** die Lockdateien eines Projekts. Was bleibt, ist die Regelschicht: Die Regeltexte verbieten es, und ein Verstoß ist Modellverhalten. **Ein Projekt mit hoher Kontrollstufe sollte diesen Client dafür nicht einsetzen** | `<SECURITY_CONTACT>` |

**B1, B2, B4 und B6 sind `[TECHNISCH]`** – B2 und B6 an der Engine selbst gemessen, B4 über den Schutz-Hook, B1 über die Lage der Träger. ⚠️ **B1 trägt die Bedingung des Vertrauenseintrags**, und B4 trägt seine Zusage im Kanal *direktes Schreiben*; Shell und Unterprozess bleiben `[TEXTUELL]` wie bei beiden Schwesterpacks.

## 5. Bekannte Abweichungen im Verhalten

- 🔴 **DIE BERECHTIGUNGSSCHICHT ZERFÄLLT IN ZWEI TRÄGER, UND SECHS PRÜFUNGEN ERREICHEN DIESES PACK DESHALB NICHT.** Die Ausgabeform dieses Packs ist `toml` (`permissions_format`), nicht `json`; es gibt hier keine Körbe aus `Werkzeug(Muster)`-Zeilen und keinen Block `_core_rules_integrity` – ein unbekannter Schlüssel in der Konfigurationsdatei wird von diesem Client gemeldet und mit `--strict-config` zum Fehler, eine Integritätsliste darin wäre also ein Fremdkörper. Betroffen sind **Prüfung 2**, **Prüfung 37**, **Prüfung 42**, **Prüfung 43**, **Prüfung 54** und **Prüfung 76**. ➡️ ***Eine Lücke, die erklärt ist, ist eine Aussage; eine, die nur besteht, ist ein blinder Fleck.*** Der Prüfapparat hält diese Liste gegen sich selbst – sie wächst und schrumpft mit ihm, nicht mit diesem Absatz.
- 🔴 **Die nutzerlokale Wurzel-Anweisung ERSETZT, sie ergänzt nicht.** Deshalb liefert dieses Pack für sie **keine** Beispieldatei aus, während beide Schwesterpacks eine mitgeben; eine Vorlage, die zum Anlegen dieser Datei auffordert, wäre eine Anleitung zum lautlosen Abschalten der Ebene 1.
- 🔴 **Die projektlokale Schicht kann LOCKERN** (B9). Bei `claude-code` kann eine nutzerlokale Konfiguration nur verschärfen, bei `devin-desktop` setzt sich die Benutzerkonfiguration in beide Richtungen durch – hier ist die **lockernde Seite die versionierte**. Wer die Berechtigungsdatei liest, liest auch, was sie am Arbeitsplatz aufhebt.
- 🔴 **Ohne Vertrauenseintrag trägt die gesamte projektlokale Schicht nichts** – Konfiguration, Hooks und Befehlsregeln zusammen. Skills laden trotzdem. Das ist die schärfste Bedingung aller drei Packs, und sie liegt außerhalb des Repositoriums.
- ⚠️ **Der Hook braucht sein eigenes Vertrauen, und es hängt an einem Hash.** Jede Hebung des Frameworks ändert den Hook und damit den Hash; ein Projekt, das danach nicht erneut vertraut, läuft ohne Schutz-Hook, und nichts meldet es. **Das gehört in die Übernahme- und in die Hebungsanleitung des aufnehmenden Projekts.**
- ⚠️ **Der Hook-Prozess bekommt kein Projektverzeichnis in der Umgebung**, sondern steht darin. Die Abbildung bindet deshalb den relativen Punkt. Ein Kommando mit einer Variable hätte gestartet und nichts gefunden.
- ⚠️ **Ein falsch geschriebenes Sonderziel der Pfadseite fällt lautlos durch.** Gemessen: `:quatsch/x` wird angenommen und steht danach im wirksamen Rechteprofil. Das ist das Gegenstück zur guten Nachricht über unbekannte **Schlüssel** – die werden benannt; ein unbekannter **Wert** eines bekannten Schlüssels nicht.
- 🟢 **Zwei Mechaniken des Kerns bekommen mit diesem Pack ihren ersten Gegenstand:** `rule_frontmatter: "comment"` und `root_instruction_imports`. Beide stehen seit 0.15.0 im Kern und waren von keinem Pack erprobt; die ROADMAP führte sie unter *„Bewusst offen gelassen"*.

## 6. Installation und Prüfung

```text
python .koolie/core/install.py --client openai-codex
python .koolie/core/tests/scripts/validate-framework.py
```

🔴 **Danach, und ohne das trägt nichts von Abschnitt B:** Das Projekt in der Benutzerkonfiguration des Clients als **vertraut** eintragen, und dem Schutz-Hook **einzeln vertrauen**. Beides liegt außerhalb des Repositoriums und kann vom Framework nicht ausgeliefert werden (Abschnitt 1b).

Vor der ersten produktiven Nutzung sind die Basistests des Testkatalogs (`.koolie/core/tests/TEST_CATALOG.md`, Kennzeichnung „Basis") gegen diesen Client zu fahren und zu protokollieren.

## 7. Anweisungs- und Konfigurationsquellen außerhalb des Projekts

**Pflichtabschnitt.** Er führt, was dieser Client aus Ablagen **außerhalb des Repositoriums** lädt. Solche Quellen haben nach Regel 2.6 der Prioritätshierarchie **keine Ebene**: Sie dürfen einschränken, nie über die Ebenen 1 bis 4 hinaus erweitern und keine Governance-, Datenschutz- oder Sicherheitsregeln setzen (D-34).

**Erhebungsstand: 2026-09-23**, Clientversion `0.156.1`, erhoben mit `codex debug prompt-input`, `codex doctor --all`, `codex execpolicy check` und Sitzungsläufen gegen ein **eigenes Benutzerverzeichnis im Ablagebereich** (`tests/protocols/2026-09-23-bau-openai-codex.md`).

### 7.1 Anweisungsquellen

| Quelle | Ladebedingung | Belegstatus | Maßnahme des Frameworks |
|---|---|---|---|
| `<Benutzerverzeichnis des Clients>/AGENTS.md` | in **jeder** Sitzung, zusätzlich zur Wurzel-Anweisung des Projekts | **Gemessen** (2026-09-23): Eine Sonde darin stand im Prompt einer Sitzung, die im Projekt nur ihre eigene `AGENTS.md` hatte | **keine** – sie bleibt Auskunft. Das Framework kann eine Datei außerhalb des Repositoriums nicht abschalten, und ein Schalter dafür ist nicht erhoben |
| `<Benutzerverzeichnis des Clients>/skills/**` | in jeder Sitzung; die Herkunftstabelle des Prompts führt sie | **Gemessen** (2026-09-23): Die Wurzeltabelle des Prompts nennt sie neben den beiden projektlokalen Ablagen | **keine** – Auskunft. 🟢 **Aber sie ist sichtbar:** Die Tabelle nennt je Skill seine Wurzel, und damit ist die Herkunft jeder Sitzung ablesbar (S5) |
| `<Benutzerverzeichnis des Clients>/rules/*.rules` | Befehlsregeln des Arbeitsplatzes | **Gemessen** (2026-09-23): Eine ungültige Datei dort bricht den Sitzungsstart mit einer Meldung ab, die sie nennt | **keine** – Auskunft. ⚠️ **Sie steht neben den projektlokalen Regeln**, und welche Seite bei einem Treffer gewinnt, ist **unerhoben** |
| `.agents/skills/**` im Projekt | zweite projektlokale Skillablage | **Gemessen** (2026-09-23) | **keine** – das Framework schreibt nur `.codex/skills/`. Die zweite Ablage ist Gegenstand dieser Auskunft (D-34) |

### 7.2 Konfigurationsquellen

Berechtigungen, Hooks und Einstellungen außerhalb des Repositoriums betreffen genau die Linien, auf denen B1 bis B6 stehen (`CR-2026-038`).

| Quelle | Wirkung | Belegstatus |
|---|---|---|
| `<Benutzerverzeichnis des Clients>/config.toml` | 🔴 **Trägt den Vertrauenseintrag, ohne den die gesamte projektlokale Schicht nicht lädt** – und führt daneben dieselben Schlüssel wie die Projektdatei: Rechteprofile, MCP-Server, Modellwahl | **Gemessen in beiden Richtungen** (A/B mit zwei Benutzerverzeichnissen). ⚠️ **Der Vertrauenseintrag kann auf ein ganzes Elternverzeichnis lauten** und schließt dann jeden Pfad darunter ein – auf dem Arbeitsplatz des Frameworks ist genau das vorgefunden worden |
| Das Hook-Vertrauen (Hash je Hook) | 🔴 **Ohne es läuft der Schutz-Hook nicht**, und nichts meldet es | **Gemessen mit Gegenlauf** (2026-09-23): ohne Vertrauen kam der Köderinhalt heraus, mit Vertrauen wurde blockiert |

### 7.3 Was dieser Abschnitt nicht leistet

**Eine Auskunft ist keine Schranke** – und bei diesem Client ist sie die **einzige** Maßnahme: Für keine der vier Anweisungsquellen ist ein Schalter erhoben, mit dem das Framework sie abstellen könnte. Das ist der Unterschied zu beiden Schwesterpacks, die eine Importsteuerung ausliefern (R6).

**Ein Abwesenheitsbeleg altert.** Der Erhebungsstand oben ist am Tag der nächsten Clientversion eine Aussage über die Vergangenheit. Prüfung 19 sieht den Unterschied nicht: Sie prüft die **Anwesenheit** dieser Auskunft, nicht ihre Richtigkeit.

## 8. Änderungsverlauf

| Version | Datum | Änderung | Autor (Rolle) |
|---|---|---|---|
| 0.1.0 | 2026-09-23 | **Angelegt (`CR-2026-133`, D-346 bis D-349).** Das dritte Client Pack, und das erste, dessen Belege sämtlich aus Messungen am Client stammen statt aus seiner Dokumentation. 🔴 **Zwei Kernzusagen sind `[NICHT ABBILDBAR]`** – `B3`, weil Musterform und Versionierbarkeit einander ausschließen und ein `deny`-Leserecht den erhöhten Windows-Sandkasten verlangt; `B5` aus demselben Grund und ohne Ersatz im Schutz-Hook. 🔴 **Die Sperrform des Schutz-Hooks war bei diesem Client wirkungslos** und ist berichtigt; die Pfadmuster des Hooks kannten als Grenze nur den Schrägstrich und trafen den Patchtext des Schreibwerkzeugs nicht. 🟢 **Drei neue Prüfungen** (86, 87, 88) | `<FRAMEWORK_OWNER>` |

# Client Pack `cursor`

| Attribut | Wert |
|---|---|
| Modul-ID | `CP-CU` |
| Ebene | keine – Abbildungsschicht |
| Version | 0.1.0 |
| Status | pilot |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Client | Cursor – Kommandozeile (`cursor-agent`, auch `agent`) und IDE; die Agenten in der Cloud des Anbieters fallen unter D-10 und nicht unter dieses Pack |
| Verbindliche Zielversion | Kommandozeile `2026.09.x`; IDE `3.22.x` (D-112) |
| Geprüfte Clientversion | Kommandozeile `2026.09.26-dd393fe` – vor dem Messen festgeschrieben (D-117). IDE `3.22.7` installiert, **an keiner Sitzung gemessen** (`K-175`). Konto: Free, Modell `auto` |
| Stand der Produktbeobachtung | Quellenliste in Anhang 31.4.5 (`QU-1` bis `QU-8`), abgerufen am 2026-09-26. `FW-AK-01` ist für dieses Pack nicht gefahren |
| Datum der Prüfung | **2026-09-26** – der Bau (`CR-2026-155`, `tests/protocols/2026-09-26-bau-cursor.md`): 24 Läufe an realen Installationen im Betrieb ohne Rückfragen, davon fünf Abnahmeläufe am installierten Pack; Free-Tarif, 0 USD |

> **Belegt, soweit gemessen (Stand 1.16.0).** Die Spalte „Einstufung" nennt die **vorgesehene** Durchsetzungstiefe, die Spalte „Beleg" ihren Nachweisstand: `gemessen` = an diesem Client beobachtet, `[DOK]` = aus der Herstellerdokumentation mit Quellenkennung, `[EMPF]` = Vorgabe des Frameworks, `BELEG OFFEN` = noch nicht belegt, mit Grund und Datum.
>
> **Alle sechs Kernzusagen sind `[TECHNISCH]`** – gemessen unter **Windows** an der Kommandozeile. 🔴 **Die Schreibweise der Pfadmuster ist die Bedingung:** Der Client vergleicht ein Muster mit dem **absoluten** Pfad, und die Muster der Herstellerdokumentation (`Read(.env)`, `Read(**/.env)`) ließen den Köder unter Windows durch (Abschnitt 1b).
>
> 🔴 **Drei Befunde stehen in keiner Dokumentation:** Ein weiterer Schlüssel in der Berechtigungsdatei lässt den Client nicht starten; ein durchsetzender Hook muss auch beim Durchlass antworten; die Hook-Eingabe beginnt unter Windows mit einem BOM (Abschnitt 1b, H2, H4).
>
> **Wer das Pack einsetzt,** liest zuerst Abschnitt 1b und Abschnitt 6.

## 1. Pfadabbildung

| Rolle des Artefakts | Pfad bei diesem Client | Belegstatus |
|---|---|---|
| Wurzel-Anweisungsdatei | `AGENTS.md` | **gemessen** (2026-09-26): steht in jeder Sitzung im Kontext, auch im Betrieb ohne Rückfragen |
| Regeldateien | `.cursor/rules/*.mdc`; Lademodus im Frontmatter (`alwaysApply`, `globs`) | **gemessen:** eine `.mdc`-Datei mit `alwaysApply: true` lädt in jeder Sitzung; 🔴 **eine `.md`-Datei in derselben Ablage lädt nie** |
| Skills | `.cursor/skills/<name>/SKILL.md` | **gemessen:** ein Skill mit den Frontmatter-Feldern des Frameworks wurde gefunden und gelesen |
| Subagentenprofile | `.cursor/agents/<name>.md` (Frontmatter `name`, `description`, `readonly`) | `[DOK]` **`QU-5`**; die Wirkung ist Gegenstand von A1 |
| Berechtigungskonfiguration | `.cursor/cli.json` – **nur** der Schlüssel `permissions` mit `allow` und `deny` (erzeugt aus `framework/runtime/permissions.json`) | **gemessen:** ein `deny` darin weist ab (*„Blocked by permissions configuration"*), auch mit `--force` |
| Ausschlussdatei | `.cursorignore` – Syntax von `.gitignore`, erzeugt aus den Leseverboten der Kernquelle | **gemessen:** sperrt Lesen **und Suchen**; die Berechtigungsdatei sperrt nur das Lesen (D-443) |
| Hook-Konfiguration | `.cursor/hooks.json`, Form `{version: 1, hooks: {ereignis: [...]}}` | **gemessen:** lädt auch im Betrieb ohne Rückfragen, in einem vertrauten Arbeitsbereich |
| Planartefakt | **keines im Repositorium** – der Planmodus des Clients legt seinen Plan außerhalb ab | **gemessen:** `createPlan` mit leerer Ablageadresse; Träger des Plans ist die Planvorlage des Kerns (M4) |
| MCP-Konfiguration | `.cursor/mcp.json` | `[DOK]` **`QU-2`**; das Framework liefert keinen Server aus |
| Projektverzeichnis im Hook-Befehl | **keine Variable – das Arbeitsverzeichnis** | **gemessen:** der Hook-Prozess steht in der Projektwurzel. `CURSOR_PROJECT_DIR` steht in der Umgebung, aber unter Windows läuft das Kommando durch eine PowerShell-Hülle |
| Nutzerlokale Überschreibung | **kein Mechanismus** | Der Hersteller dokumentiert keine nutzerlokale Wurzel-Anweisung; das Pack liefert keine Beispieldatei aus |

## 1a. Semantikabbildung der Berechtigungen

Die Regelmenge liegt werkzeugneutral im Kern und wird bei der Installation übersetzt (D-18). Dieser Client kennt Regeln der Gestalt `Typ(Muster)` wie die erste Ausgabeform – **aber nur `allow` und `deny`**, und die Datei darf **keinen weiteren Schlüssel** tragen. Die Abbildung ist deshalb eine eigene Ausgabeform (`cursor-json`, D-440).

| Neutrales Werkzeugverb | Regeltyp bei diesem Client | Anmerkung |
|---|---|---|
| `read` | `Read(…)` | Jedes Muster in **zwei Schreibweisen** mit führendem `*`: `Read(*/.env)` und `Read(*\.env)` (Abschnitt 1b) |
| `search` | – | Kein Regeltyp. 🔴 **Das Suchwerkzeug wertet ein `Read`-Verbot nicht aus** – gemessen. Die Lesesperre für die Suche trägt `.cursorignore` (D-443) |
| `write` | `Write(…)` | Zwei Schreibweisen wie `read`. Deckt das Löschwerkzeug mit – gemessen |
| `exec` | `Shell(…)` ohne Stern | Das Muster trifft den Befehl und jeden, der mit ihm und einem Leerzeichen beginnt (Programmcode); verkettete Befehle zerlegt der Client – gemessen |
| `fetch` | `WebFetch(*)` | Das Argument ist eine Domain |
| `mcp` | – (nur Rückfrage) | Ein MCP-Werkzeug braucht die Freigabe seines Servers (`QU-2`) |
| `skill` | – | Ein Skill ist bei diesem Client eine Datei, kein Werkzeug mit Berechtigung |

| Weitere Eigenschaft | Wert |
|---|---|
| Rückfragekorb | **keiner** – die Rückfrageregeln der Kernquelle erklärt das Manifest (`permission_ask_ohne_korb`) statt sie zu erzeugen |
| Ebenen | Die Projektdatei wird in die globale Konfiguration gemischt; **Listen ersetzen** dabei die globalen (Programmcode) |
| Hook-Werkzeugnamen | `Read`, `Grep`, `Shell`, `Write`, `Delete`; das Dateinamenwerkzeug `Glob` löst keinen Hook aus |
| Pfadfelder der Hook-Eingabe | `file_path` (absolut); `Shell` führt `command` |
| Sperrform des Schutz-Hooks | `permission-json`: `{"permission": "deny"}` und Exit 2, beim Durchlass `{}` (D-441) |

## 1b. Die vier Bedingungen, unter denen das Pack trägt

**1. Pfadmuster treffen nur mit führendem `*`.** Der Client vergleicht ein Muster **verankert mit dem absoluten Pfad**, und `*` steht dabei für eine beliebige Zeichenfolge über Trenner hinweg (Programmcode). Gemessen unter Windows: `Read(.env)` und `Read(**/.env)` ließen den Köder durch, `Read(*\.env)` und `Read(*.p12)` sperrten. Die Abbildung erzeugt deshalb jedes Pfadmuster zweimal, mit `/` für macOS und Linux und mit `\` für Windows. **Die Schreibweise mit `/` ist nicht gemessen** – sie folgt aus dem Programmcode (`K-176`). ⚠️ Der Preis: Das Muster ist **breiter** als das der Kernquelle – `Write(*/AGENTS.md)` sperrt auch ein `AGENTS.md` in einem Unterordner, und `Read(*/*secret*)` sperrt jede Datei, in deren Pfad `secret` vorkommt, **auch oberhalb des Projekts**. Bei einem Verbot ist das eine Verschärfung; ein Projekt unter einem solchen Pfad kann nichts mehr lesen und merkt es sofort.

**2. Die Berechtigungsdatei trägt nur `permissions`.** Gemessen: Mit `_comment` und `_core_rules_integrity` brach der Client mit Exit 1 ab (*„Unrecognized key(s) in object"*), ebenso bei kaputtem JSON. Das ist **fail-closed** – der Client startet nicht, statt ohne Regeln zu laufen. **Prüfung 97** hält die Datei gegen die Kernquelle, weil sie ihre Kernregeln nicht selbst auflisten kann.

**3. Die Hooks brauchen einen vertrauten Arbeitsbereich und unter Windows den richtigen Start.** Sie laufen in jeder Sitzung, **auch ohne Rückfragen** – anders als bei `kiro`. Unter Windows reicht der Client die Eingabe durch eine PowerShell-Hülle weiter. 🔴 **Mit gesetzter Variable `SHELL`** (Start aus Git Bash) führt er diese Hülle in `bash` aus; sie scheitert, und ein Hook mit `failClosed` sperrt dann **jede** Operation – gemessen. Aus PowerShell oder `cmd` gestartet, laufen die Hooks.

**4. Fremde Konfigurationen laden mit.** Der Client lädt standardmäßig Hooks von Claude Code aus `.claude/settings.json` **und `~/.claude/settings.json`**, Skills aus `.claude/skills/`, `.codex/skills/` und `~/.claude/skills/` und die Datei `CLAUDE.md` der Projektwurzel – gemessen. Der Schalter ist eine Einstellung der IDE (*Third-Party Imports*), nicht des Projekts. `install.py` meldet, was davon auf dem Arbeitsplatz belegt ist (R6).

**Die IDE** liest `.cursor/cli.json` nach der Herstellerdokumentation nicht – sie ist als Konfiguration der Kommandozeile beschrieben (`QU-2`). Hooks, Regeln, Skills und `.cursorignore` gelten laut Dokumentation für beide. **An einer IDE-Sitzung ist nichts davon gemessen** (`K-175`).

## 2. Fähigkeitsmatrix

Einstufung je Zusage: `[TECHNISCH]` erzwungen · `[TEXTUELL]` nur Anweisung · `[NICHT ABBILDBAR]` kein Mechanismus. Regeln in `../README.md` Abschnitt 4. Gemessen ist an der Kommandozeile unter Windows; eine Zeile, die die IDE betrifft, sagt es.

### R – Regelladung

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| R1 | Wurzel-Anweisungsdatei wird ungefragt geladen | `AGENTS.md` steht in jeder Sitzung im Kontext | `[TECHNISCH]` | **gemessen** (2026-09-26): Kennwort aus `AGENTS.md` ohne Werkzeugaufruf genannt; im installierten Pack mit Pfad aufgezählt |
| R2 | Regeldateien mit Ladebedingungen | `.cursor/rules/*.mdc`, Frontmatter `alwaysApply` und `globs` | `[TECHNISCH]` | **gemessen:** `alwaysApply: true` lädt immer; die vier Regeln des Frameworks standen im installierten Pack im Kontext. 🔴 **Eine `.md`-Datei in der Ablage lädt nie** – die Regeln heißen deshalb `.mdc` (`QU-1`). `model_decision` bildet auf unbedingtes Laden ab – eine Verschärfung |
| R3 | Regeln an Dateimuster bindbar | `alwaysApply: false` mit `globs` als Liste | `[TECHNISCH]` | **gemessen mit Gegenprobe:** Eine Regel mit `**/*.xyz` stand nach dem Lesen von `probe.xyz` im Kontext, mit `**/*.abc` nicht |
| R4 | Bekanntes Zeichenlimit | **Vorgabe des Frameworks** – höchstens 40.000 Zeichen für das stets Geladene (D-387) | `[TEXTUELL]` | `[EMPF]`. Der Hersteller empfiehlt Regeln unter 500 Zeilen (`QU-1`); ein Limit ist nicht dokumentiert. Gemessen ist die Last: 13.612 Eingabetoken einer Sitzung mit installiertem Pack gegenüber 10.190 im Minimalbaum |
| R5 | Die geladenen Regelquellen sind vollständig aufzählbar | Keine Aufzählung des Clients in der Ausgabe; die Sitzung nennt ihre Quellen auf Nachfrage | `[TEXTUELL]` | **gemessen ist nur die Selbstauskunft** der Sitzung (Pfade aller fünf Träger). Eine Auskunft des Modells, keine des Clients |
| R6 | Keine Importe fremder Werkzeugformate | **Kein Schalter im Projekt.** Der Import von Claude Code (Hooks, Skills, `CLAUDE.md`) ist eine Einstellung der IDE mit Standard „an" | `[NICHT ABBILDBAR]` | **gemessen:** `CLAUDE.md` lud in jeder Sitzung; die Hooks aus `~/.claude/settings.json` liefen an der Kommandozeile mit. **Ersatz, geliefert:** die Meldung von `install.py` über belegte Quellen, einschließlich der nur global abschaltbaren Commit-Attribution, und der Nachschritt zur Einstellung der IDE (Abschnitt 7) |

### S – Skills

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| S1 | Versionierte Skills im Repository | `.cursor/skills/<name>/SKILL.md` | `[TECHNISCH]` | **gemessen:** ein Skill der Ablage wurde gefunden und gelesen, auch mit den Frontmatter-Feldern des Frameworks |
| S2 | Gezielter Aufruf | `/<name>` in der Sitzung | `[TECHNISCH]` | `[DOK]` **`QU-4`**; gemessen ist nur der Aufruf beim Namen im Auftrag – die Sitzung las den Skill |
| S3 | Werkzeugbeschränkung je Skill | **Kein Feld.** `allowed-tools`, `permissions` und `triggers` werden angenommen und nicht ausgewertet | `[TEXTUELL]` | **gemessen:** Ein Skill mit `permissions: deny: [edit]` war geladen, und das Schreiben blieb im selben Lauf erlaubt. Was trägt, ist die globale Schicht |
| S4 | Schreibende Skills nur benutzergetriggert | `disable-model-invocation: true`, übersetzt aus `triggers` | `[TECHNISCH]` | `[DOK]` **`QU-4`**; `BELEG OFFEN` (2026-09-26): die Wirkung des Feldes ist nicht gemessen |
| S5 | Die geladenen Skills sind aufzählbar | Selbstauskunft der Sitzung | `[TEXTUELL]` | `BELEG OFFEN` (2026-09-26): Die Ausgabe ohne Rückfragen führt keine Liste der Skills |

### B – Berechtigungen

> **`[TECHNISCH]` heißt in diesem Block:** Der Client setzt die Regel durch, **auch im Betrieb, der Rückfragen überspringt** – gemessen: Jedes `deny` hielt mit `--force`. Für dieses Pack kommen **zwei gemessene Bedingungen** hinzu: **die Schreibweise der Pfadmuster** (Abschnitt 1b, Punkt 1) und **eine Datei, mit der der Client startet** (Punkt 2). Die Berechtigungsdatei ist eine Konfiguration der **Kommandozeile**; für die IDE ist sie nicht dokumentiert (`K-175`). **Die zweite Linie ist der Schutz-Hook, die dritte für Lesen und Suchen `.cursorignore`.**

Die mit **Kern** markierten Zeilen entsprechen den Kernzusagen der Kernquelle; Prüfung 97 hält die Datei gegen sie, weil die Datei sie nicht selbst auflisten darf.

| ID | Zusage des Frameworks | Kern | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|---|
| B1 | Berechtigungen versioniert im Repository | ja | `.cursor/cli.json` und `.cursorignore` im Projekt | `[TECHNISCH]` | **gemessen:** beide Träger liegen im Projekt und wirken ohne Schalter. Mit einem fremden Schlüssel oder kaputtem JSON startet der Client nicht (fail-closed) |
| B2 | Verweigern vor Rückfragen vor Erlauben | ja | `deny` vor `allow`; was kein `allow` deckt, fragt bei Befehlen zurück | `[TECHNISCH]` | **gemessen:** `deny` auf `.env` schlägt `allow` auf `Read(**)`. Einen Rückfragekorb gibt es nicht (B7) |
| B3 | Secret-Dateien per Pfadmuster lesegeschützt | ja | `deny Read` in zwei Schreibweisen **und** `.cursorignore` | `[TECHNISCH]` | **gemessen an einer realen Installation:** `.env` und `secrets/pw.txt` abgewiesen, `probe.txt` gelesen – mit der Berechtigungsdatei allein, ohne Hook. 🔴 **Das Suchwerkzeug beachtet das `Read`-Verbot nicht** (Köder aus `secrets/` gefunden); mit `.cursorignore` war die Suche ausgefiltert, und der Schutz-Hook sperrte sie ebenfalls. Groß- und Kleinschreibung unterscheidet das Muster, der Hook nicht |
| B4 | Framework- und Overlay-Artefakte schreibgeschützt | ja | `deny Write` auf `AGENTS.md`, `.cursor/**`, `.koolie/core/**`, `.koolie/project-overlay/**`; `.cursorignore` schützt der Client selbst | `[TECHNISCH]` | **gemessen:** Schreiben auf `AGENTS.md`, in `.koolie/core/` und `.cursor/rules/` abgewiesen, Löschen von `OVERLAY.md` abgewiesen, `neu.txt` angelegt. ⚠️ **Grenze, nicht gemessen:** ein freigegebener lesender `git`-Befehl mit schreibender Option (`git diff --output=<pfad>`) |
| B5 | CI-, Quality-Gate- und Lockdateien schreibgeschützt | ja | `deny Write` mit den Lockmustern und den Schlitzen `<CI_CONFIG_PATHS>`, `<QUALITY_GATE_CONFIG_PATHS>` | `[TECHNISCH]` | **gemessen am Mechanismus** (Pfadmuster im `deny`, B4); die Schlitze füllt der Overlay Owner in beiden Schreibweisen, die Lockmuster sind nicht einzeln angefahren |
| B6 | Befehle per Muster verweigerbar | ja | `deny Shell(git push)` und die übrigen Befehlsverbote | `[TECHNISCH]` | **gemessen:** `git push origin main` abgewiesen, auch in `git status && git push origin main`; `rm probe.txt` abgewiesen. ⚠️ **Grenze wie bei allen Packs:** `git -C . push origin main` trifft das Muster nicht – es fiel in die **Rückfrage** und wurde ohne Rückfragekanal abgewiesen |
| B7 | Schreiboperationen fragen zurück | – | **Kein Rückfragekorb; Dateien im Arbeitsbereich schreibt der Client ohne Rückfrage** | `[NICHT ABBILDBAR]` | **gemessen:** `neu2.txt` angelegt, auch **ohne** `--force`; der Hersteller sagt es selbst (`QU-8`). **Ersatz:** die Schreibverbote (B4, B5), der Schutz-Hook und die Sichtprüfung im Merge Request – eine Rückfrage vor jedem Schreiben gibt es bei diesem Client nicht |
| B8 | Netzwerkzugriff standardmäßig unterbunden | – | `deny WebFetch(*)` und `deny Shell` auf `curl`, `wget`, `ssh`, `scp` | `[TECHNISCH]` für das Web-Werkzeug und diese vier Programme; `[TEXTUELL]` darüber hinaus | **gemessen:** `curl` abgewiesen; der Webabruf abgewiesen – ob durch das Verbot oder die Rückfrage, sagt die Meldung nicht. ⚠️ Jedes andere netzfähige Programm fragt zurück, ist aber nicht verboten |
| B9 | Nutzerlokale Konfiguration kann nur verschärfen | – | Die Projektdatei ersetzt die Listen der globalen Konfiguration; ein `deny` gilt in jedem Betriebsmodus | `[TECHNISCH]` | **gemessen:** das `deny` des Projekts hielt mit `--force`; die Ersetzung der Listen ist aus dem Programmcode. ⚠️ **Ein `deny` des Arbeitsplatzes gilt in diesem Projekt nicht mehr**, und die globale Einstellung `approvalMode: unrestricted` überspringt die Rückfragen (M2) |
| B10 | Externer Abruf auf freigegebene Domains beschränkbar | – | `WebFetch(<domain>)` | `[TECHNISCH]` | `[DOK]` **`QU-2`**. Das Framework nutzt die strengste Form – alles verboten (B8, D-59) |

### H – Hooks

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| H1 | Prüfung vor Werkzeugausführung | `preToolUse` in `.cursor/hooks.json`, Matcher als regulärer Ausdruck über die Werkzeugnamen | `[TECHNISCH]` | **gemessen:** Der Hook läuft bei jedem Lese-, Such-, Schreib-, Lösch- und Shell-Aufruf, **auch ohne Rückfragen**. Bedingungen: ein vertrauter Arbeitsbereich und unter Windows ein Start ohne `SHELL` (Abschnitt 1b) |
| H2 | Prüfung kann **blockieren** | `{"permission": "deny"}` und Exit 2; beim Durchlass `{}`; `failClosed: true` | `[TECHNISCH]` | 🔴 **Gemessen, und der schwerste Befund des Hooks** (D-441): Exit 2 sperrt – aber ohne `failClosed` lässt ein Hook, der scheitert, die Operation **durch**, und mit `failClosed` wertet der Client einen Hook **ohne Ausgabe** als gescheitert: Er sperrte jede Operation, auch das Lesen von `probe.txt`. Mit der Form `permission-json` gesperrt: `.env` über Lese-, Such- und Shell-Werkzeug, `AGENTS.md`, `.koolie/core/`, `.cursor/rules/`, `OVERLAY.md`; durchgelassen: `probe.txt`. **Prüfung 86** misst beide Hälften |
| H3 | Statusmeldung beim Sitzungsstart | `sessionStart` mit `hook-overlay-status.py` | `[TECHNISCH]` | **gemessen:** Framework-Version und Overlay-Status standen wörtlich im Kontext, und die Sitzung arbeitete danach im Modus M1. Die Ausgabe in der Form von Claude Code (`hookSpecificOutput`) übersetzt der Client |
| H4 | Eingabeschema und Pfadidentität des Schutz-Hooks | Ereignisprüfung, Pfadfeld `file_path`, BOM-feste Eingabe, alle Muster ohne Rücksicht auf Groß-/Kleinschreibung; `hook_fail_closed` steht auf `true`. **Grenze:** Ein Hook prüft **vor** dem Zugriff (D-397) | `[TECHNISCH]` für die Musterprüfung, **mit der Zeitlücke** | **gemessen:** das Schema von `preToolUse` für fünf Werkzeuge. 🔴 **Die Eingabe beginnt unter Windows mit einem UTF-8-BOM** – der Hook scheiterte daran, bis er sie als UTF-8 mit BOM las (D-441). ⚠️ Das Dateinamenwerkzeug `Glob` löst keinen Hook aus; es liefert Namen, keine Inhalte |

### A – Agentenprofile

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| A1 | Rein lesendes Reviewprofil | `.cursor/agents/fw-reviewer.md` mit `readonly: true` | `[TECHNISCH]` | `[DOK]` **`QU-5`** (*„no file edits, no state-changing shell commands"*); `BELEG OFFEN` (2026-09-26): Der Start eines Subagenten ist nicht gemessen |
| A2 | Rein lesendes Analyseprofil für Modus M1 | Modus `ask` (`--mode ask`, *„read-only"*) | `[TEXTUELL]` | `[DOK]` **`QU-6`**; `BELEG OFFEN` (2026-09-26) für seine Wirkung |

### M – Modi und Sitzungsfreigaben

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| M1 | Standardmodus fragt bei Schreiben und Befehlen zurück | Befehle außerhalb von `allow` fragen zurück; **Schreiben im Arbeitsbereich nicht** | `[NICHT ABBILDBAR]` für das Schreiben, `[TECHNISCH]` für Befehle | **gemessen:** ohne Rückfragekanal wurden `python --version` und `git log` abgewiesen, `neu2.txt` angelegt. **Ersatz:** wie B7 |
| M2 | Modus ohne Rückfragen ausschließbar | **Kein Ausschluss.** `--force` (`--yolo`) und die globale Einstellung `approvalMode: unrestricted` überspringen Rückfragen; ein `deny` gilt weiter | `[TEXTUELL]` | **gemessen:** jedes `deny` hielt mit `--force`. Das ist mehr als bei den meisten Packs, aber keine Sperre des Modus |
| M3 | Freigabe auf die Sitzung begrenzbar | Die Freigabe einer Rückfrage kann in die Freigabeliste übernommen werden | `[TEXTUELL]` | `BELEG OFFEN` (2026-09-26): Eine Rückfrage an einen Menschen ist ohne Rückfragekanal nicht messbar. ⚠️ Nach dem Programmcode schreibt die Übernahme in die Konfiguration – über die Sitzung hinaus |
| M4 | Eigener Planungsmodus für Modus M2 | Modus `plan` (`--plan`); der Plan geht an ein eigenes Werkzeug und liegt **nicht im Repositorium** | `[TEXTUELL]` | **gemessen:** Die Sitzung las, schrieb nichts und legte einen Plan mit leerer Ablageadresse an. Der Träger des Plans ist deshalb die Planvorlage des Kerns (`fw-plan`); anders als bei `kiro` liefert das Pack keine Regel für ein clienteigenes Planartefakt |
| M6 | Modus mit selbsttätiger Übernahme von Dateiänderungen begrenzbar | Änderungen im Arbeitsbereich übernimmt der Client **immer** selbsttätig | `[NICHT ABBILDBAR]` | **gemessen** (B7) und `[DOK]` **`QU-8`** (*„Changes save immediately to disk"*). **Ersatz:** wie B7 |
| M7 | Modus, der selbst beurteilt, was sicher ist, begrenzbar | `--auto-review` und `approvalMode: auto-review` (ein Klassifikator des Anbieters) | `[TEXTUELL]` | `[DOK]` **`QU-2`**; `BELEG OFFEN` (2026-09-26) für seine Begrenzbarkeit. Der Hersteller nennt die Modi *„best-effort guardrails rather than a hard security boundary"* (`QU-8`) |

### X – Externe Anbindung

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| X1 | Keine externe Anbindung ohne Einzelfreigabe | Jeder MCP-Server und jeder Werkzeugaufruf braucht eine Freigabe; das Framework liefert keinen Server aus | `[TECHNISCH]` | `[DOK]` **`QU-8`**; `BELEG OFFEN` (2026-09-26) für die Wirkung – im Messbaum stand kein Server. ⚠️ `--approve-mcps` überspringt die Freigabe |
| X2 | Art und Ort der Codebasis-Indexierung bekannt | Kein Mechanismus zur Steuerung bekannt | `[NICHT ABBILDBAR]` | `BELEG OFFEN (dauerhaft)` – von außen nicht zu beobachten (`K-20`, D-292). **Kein Ersatz durch das Framework.** Dokumentiert ist der Privacy Mode (`QU-7`); auf dem Messkonto war er eingeschaltet |

## 3. Zusammenfassung der Durchsetzungstiefe

> **Zählregel (normativ für diese Tabelle):** Eine Zeile zählt bei ihrer **schwächsten** Einstufung (D-47). Prüfung 31 rechnet die Summen aus der Matrix nach.

| Klasse | Anzahl | davon Kernzusagen |
|---|---|---|
| `[TECHNISCH]` | **20 von 35** | 6 von 6 (B1 bis B6) |
| `[TEXTUELL]` | **10 von 35** | 0 von 6 |
| `[NICHT ABBILDBAR]` | **5 von 35** | 0 von 6 |

**Belegstand:** `BELEG OFFEN` sagen **S4**, **S5**, **A1**, **A2**, **M3**, **M7** und **X1**, dazu **X2** dauerhaft. Gemessen ist an der Kommandozeile unter Windows; die Zeilen der IDE stehen auf der Dokumentation (`K-175`), die Schreibweise der Pfadmuster für macOS und Linux auf dem Programmcode (`K-176`).

## 4. Kernzusagen ohne technische Durchsetzung

**Keine.** Alle sechs Kernzusagen sind `[TECHNISCH]` – unter den Bedingungen aus Abschnitt 1b, die in der Vorbemerkung des B-Blocks stehen, weil sie keine Zeile einzeln betreffen.

## 5. Bekannte Abweichungen im Verhalten

- **Die Berechtigungsdatei trägt nur `permissions`** (`permissions_format` `cursor-json`, D-440). Sie ist JSON mit Regeln der Gestalt `Typ(Muster)`, aber ohne `_core_rules_integrity`, ohne `ask` und mit einer eigenen Musterschreibweise. Deshalb erreichen dieses Pack nicht: **Prüfung 2**, **Prüfung 37**, **Prüfung 42**, **Prüfung 43**, **Prüfung 54** und **Prüfung 72**; nur zum Teil **Prüfung 59** und **Prüfung 89** (ihr Gegenstand (c), die Pfade des Overlays im `deny`, entfällt). An ihre Stelle tritt die Prüfung der Berechtigungsdatei gegen die Kernquelle (Abschnitt 1b, Punkt 2). Der Prüfapparat hält diese Liste gegen seine eigene Liste der formatgebundenen Prüfungen.
- **Kein Rückfragekorb, und Schreiben im Arbeitsbereich fragt nicht zurück** (B7). Die Rückfrageregeln der Kernquelle erklärt das Manifest; die Befehlsschlitze des Overlays gehören nicht unter `allow`.
- **Jedes Pfadmuster steht zweimal** und ist breiter als das der Kernquelle (Abschnitt 1b). Ein Projekt, das einen eigenen Pfad sperrt, schreibt ihn ebenso: `Read(*/<pfad>)` und `Read(*\<pfad>)`. Der Validator warnt bei einem Pfadverbot, das nie trifft.
- **Die Lesesperre steht zweimal**, in der Berechtigungsdatei und in `.cursorignore` – die zweite, weil das Suchwerkzeug die erste nicht beachtet (D-443).
- **Der Schutz-Hook antwortet auch beim Durchlass** und liest seine Eingabe BOM-fest (D-441).
- **Regeldateien heißen `.mdc`**; eigene Regeln des Projekts ebenso (`rule_file_ext`).
- **Die Commit-Attribution lässt sich nur global abschalten** (`attribution.attributeCommitsToAgent` in `~/.cursor/cli-config.json`). Gemessen: Mit dem Standard hängte die Sitzung jedem Commit `Co-authored-by: Cursor <…>` an – gegen Q5; mit `false` nicht.

## 6. Installation und Prüfung

```text
python .koolie/core/install.py --target /pfad/zum/projekt --client cursor
python .koolie/core/tests/scripts/validate-framework.py
```

🔴 **Danach:** Unter Windows die Kommandozeile aus PowerShell oder `cmd` starten, nicht aus Git Bash. Beim ersten Start dem Arbeitsbereich vertrauen. Die Commit-Attribution global auf `false` setzen. Den Import fremder Konfigurationen in der IDE prüfen. `install.py` nennt diese Schritte nach der Installation und meldet belegte fremde Quellen; nach jeder Hebung nennt es, dass `.cursor/cli.json` und `.cursorignore` Saat sind und nicht angefasst werden.

Vor der ersten produktiven Nutzung sind die Basistests des Testkatalogs gegen diesen Client zu fahren und zu protokollieren.

## 7. Anweisungs- und Konfigurationsquellen außerhalb des Projekts

**Pflichtabschnitt** (D-34). Solche Quellen haben nach Regel 2.6 der Prioritätshierarchie **keine Ebene**.

**Erhebungsstand: 2026-09-26**, Kommandozeile `2026.09.26-dd393fe`, erhoben mit der Herstellerdokumentation (`QU-1` bis `QU-5`), dem Programmcode der Kommandozeile, Messläufen mit dem echten und einem leeren Benutzerprofil und `install.py` (`import_channels_report`).

### 7.1 Anweisungsquellen

| Quelle | Ladebedingung | Belegstatus | Maßnahme des Frameworks |
|---|---|---|---|
| `CLAUDE.md` der Projektwurzel | in jeder Sitzung neben `AGENTS.md` (Drittimport) | **gemessen** | Auskunft; `install.py` meldet die Datei |
| Hooks in `.claude/settings.json` und `~/.claude/settings.json` | in jeder Sitzung, neben den Hooks des Projekts (Drittimport) | **gemessen** – sie liefen mit, und unter Git Bash sperrten sie jede Operation | Auskunft; `install.py` meldet sie, wenn die Datei Hooks führt |
| `~/.claude/skills/`, `~/.codex/skills/`, `.claude/skills/`, `.codex/skills/` | in jeder Sitzung verfügbar (Drittimport) | `[DOK]` `QU-4` | Auskunft; `install.py` meldet sie |
| `~/.cursor/skills/`, `~/.agents/skills/`, `~/.cursor/agents/` | in jeder Sitzung verfügbar | `[DOK]` `QU-4`, `QU-5` | Auskunft; `install.py` meldet sie |
| Nutzerregeln und Teamregeln | in jeder Sitzung, in den Einstellungen gepflegt, keine Datei | `[DOK]` `QU-1` | **keine** – nicht aus dem Projekt erreichbar |
| Eingebaute Skills des Clients (`/create-rule`, `/review` …) | in jeder Sitzung zur Wahl | `[DOK]` `QU-4` | **keine** – nicht abschaltbar |

### 7.2 Konfigurationsquellen

| Quelle | Wirkung | Belegstatus |
|---|---|---|
| `~/.cursor/cli-config.json` | globale Konfiguration der Kommandozeile; ihre Listen **ersetzt** die Projektdatei. Führt `approvalMode`, `sandbox` und die **Commit-Attribution** | Programmcode; Attribution **gemessen** |
| `~/.cursor/hooks.json` | Hooks des Arbeitsplatzes; laufen neben denen des Projekts, ein `deny` gewinnt | `[DOK]` `QU-3` |
| `~/.cursor/mcp.json` | MCP-Server des Arbeitsplatzes | `[DOK]` `QU-2` |
| Hooks der Organisation (`C:\ProgramData\Cursor\hooks.json` und Entsprechungen) | höchste Priorität; ein `deny` gewinnt | `[DOK]` `QU-3` |
| `.cursor/cli.json` in einem **Elternverzeichnis** des Projekts | wird ebenfalls gelesen und eingemischt | Programmcode |

### 7.3 Was dieser Abschnitt nicht leistet

**Eine Auskunft ist keine Schranke**, und ein **Abwesenheitsbeleg altert**. Prüfung 19 prüft die Anwesenheit dieser Auskunft, nicht ihre Richtigkeit.

## 8. Änderungsverlauf

| Version | Datum | Änderung | Autor (Rolle) |
|---|---|---|---|
| 0.1.0 | 2026-09-26 | **Angelegt (`CR-2026-155`, D-440 bis D-443).** Das fünfte Client Pack, gebaut mit Zugang zum Client. **Die Berechtigungsdatei trägt nur `permissions`**, und **jedes Pfadmuster steht in zwei Schreibweisen**, weil der Client es mit dem absoluten Pfad vergleicht (D-440); **der Schutz-Hook antwortet auch beim Durchlass und liest BOM-fest** (D-441); **das Suchwerkzeug beachtet kein Leseverbot** – `.cursorignore` trägt es (D-443). **Prüfung 97** neu | `<FRAMEWORK_OWNER>` |

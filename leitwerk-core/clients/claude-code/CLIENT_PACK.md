# Client Pack `claude-code`

| Attribut | Wert |
|---|---|
| Modul-ID | `CP-CC` |
| Ebene | keine – Abbildungsschicht |
| Version | 0.7.0 |
| Status | entwurf |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Client | Claude Code |
| Geprüfte Clientversion | 2.1.267 (AP2-Dokumentenabgleich, `tests/protocols/2026-09-10-AP2-claude-code.md`). Die **verbindliche Zielversion** legt `<FRAMEWORK_OWNER>` fest und steht aus |
| Datum der Prüfung | 2026-09-10 – Dokumentenabgleich und Prüfung der erzeugten Artefakte; die Wirkungsnachweise in einer Sitzung stehen aus |

> **Teilweise belegt (Stand 0.6.0).** Alle zehn Pruefmarker sind gegen die
> Herstellerdokumentation der Clientversion 2.1.267 und gegen eine reale Erstinstallation
> abgeglichen (`tests/protocols/2026-09-10-AP2-claude-code.md`); die Befunde sind mit
> `CR-2026-016` und `CR-2026-017` behoben und die Einstufungen berichtigt. **Keine Einstufung
> steht mehr auf `[NICHT ABBILDBAR]`.** Kein Wirkungsnachweis aus einer laufenden Sitzung
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
| `search` | – | Die eigenen Suchwerkzeuge (`Grep`, `Glob`) werten **keine** Pfadregeln aus; `Read(**)` deckt den Lesezugriff ab. Seit `CR-2026-016` wird für dieses Verb keine Regel erzeugt |
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

### S – Skills

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| S1 | Versionierte Skills im Repository | `.claude/skills/<name>/SKILL.md` mit Frontmatter | `[TECHNISCH]` | `[DOK]`; zusätzlich **beobachtet** (siehe Abschnitt 6) |
| S2 | Gezielter Aufruf | Aufruf über den Skill-Namen mit vorangestelltem Schrägstrich | `[TECHNISCH]` | `[DOK]` |
| S3 | Werkzeugbeschränkung je Skill | Frontmatter `allowed-tools` als kommagetrennte Liste | `[TECHNISCH]` | `[DOK]` |
| S4 | Schreibende Skills nur benutzergetriggert | `disable-model-invocation: true` verhindert, dass das Modell den Skill selbst lädt, und hält zusätzlich seine Beschreibung aus dem Kontext; die Installation setzt das Feld für jeden Skill, dessen Quelle `triggers` ohne `model` nennt (9 von 12). Ergänzend wirkt `ask` auf `Edit(**)`: jede Schreiboperation löst eine Rückfrage aus | `[TECHNISCH]` | [DOK] `docs/en/skills` (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) – dokumentiert und in der Installation gesetzt; die **beobachtete** Durchsetzung steht als Wirkungsnachweis aus |

### B – Berechtigungen

| ID | Zusage des Frameworks | Kern | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|---|
| B1 | Berechtigungen versioniert im Repository | ja | `.claude/settings.json` | `[TECHNISCH]` | `[DOK]` |
| B2 | Verweigern vor Rückfragen vor Erlauben | ja | `permissions.deny` / `.ask` / `.allow` | `[TECHNISCH]` | `[DOK]` |
| B3 | Secret-Dateien per Pfadmuster lesegeschützt | ja | Verweigerungsregeln auf `./.env`, `**/*.pem`, `**/secrets/**` und weitere. Mustersemantik: gitignore-Syntax; ein bloßer Dateiname trifft in jeder Tiefe (`Read(.env)` ist gleichbedeutend mit `Read(**/.env)`); ein einsegmentiges Verzeichnismuster trifft in `deny` und `ask` in jeder Tiefe, in `allow` nur am verankerten Ort. Unter Windows werden Pfade vor dem Vergleich auf POSIX-Form normalisiert | `[TECHNISCH]` | [DOK] `docs/en/permissions` (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) |
| B4 | Framework- und Overlay-Artefakte schreibgeschützt | ja | Je Pfad **eine** `Edit(...)`-Regel; das Kernverzeichnis ist seit `CR-2026-012` als Ganzes erfasst (`Edit(leitwerk-core/**)`). Eine zusätzliche `Write(...)`-Pfadregel wäre wirkungslos und wird seit `CR-2026-016` nicht mehr erzeugt | `[TECHNISCH]` | wie B3 |
| B5 | CI-, Quality-Gate- und Lockdateien schreibgeschützt | ja | dito, je Pfad eine `Edit(...)`-Regel | `[TECHNISCH]` | wie B3 |
| B6 | Befehle per Muster verweigerbar | ja | Präfixmuster, z. B. `Bash(git push:*)`. Wirkt **breiter** als eine Verweigerung des vollständigen Befehls | `[TECHNISCH]` | wie B3 |
| B7 | Schreiboperationen fragen zurück | – | `ask` auf `Edit(**)` | `[TECHNISCH]` | `[DOK]` |
| B8 | Netzwerkzugriff standardmäßig unterbunden | – | Verweigerung der Abruf- und Suchwerkzeuge sowie von `curl` und `wget` | `[TECHNISCH]` | `[DOK]` |
| B9 | Nutzerlokale Konfiguration kann nur verschärfen | – | `.claude/settings.local.json` rangiert **über** der Projektdatei, kann eine dort gesetzte Verweigerung aber nicht aufheben: „If a tool is denied at any level, no other level can allow it." Ergänzend greifen `deny`- und `ask`-Regeln sofort, `allow`-Regeln erst nach dem Vertrauen in den Ordner | `[TECHNISCH]` für die Verweigerungen; `[TEXTUELL]` für den Rest | [DOK] `docs/en/permissions, docs/en/settings` (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) |

### H – Hooks

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| H1 | Prüfung vor Werkzeugausführung | `hooks.PreToolUse` in `settings.json`, Matcher auf schreibende und ausführende Werkzeuge | `[TECHNISCH]` | `[DOK]` |
| H2 | Prüfung kann **blockieren** | Exit-Code 2 des Hook-Befehls blockiert die Ausführung, und zwar **bevor** die Berechtigungsregeln ausgewertet werden – ein blockierender Hook geht damit auch einer `allow`-Regel vor. Umgekehrt hebt eine Hook-Entscheidung keine `deny`- oder `ask`-Regel auf | `[TECHNISCH]` | [DOK] `docs/en/permissions` (AP2, Clientversion 2.1.267) – **stärker belegt als beim Client Pack `devin-desktop`**, siehe Abschnitt 5 |
| H3 | Statusmeldung beim Sitzungsstart | `hooks.SessionStart` | `[TECHNISCH]` | `[DOK]` |

### A – Agentenprofile

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| A1 | Rein lesendes Reviewprofil | `.claude/agents/fw-reviewer.md`, Frontmatter-Feld `tools` (ergänzend `disallowedTools`, das zuerst angewandt wird); die Beschränkung wirkt technisch. Ein Profil, dessen `tools`-Liste sich zu keinem Werkzeug auflöst, wird gar nicht erst gestartet – ein Tippfehler führt zum Abbruch, nicht zu einem Subagenten ohne Beschränkung | `[TECHNISCH]` | [DOK] `docs/en/sub-agents` (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) |

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

| Klasse | Anzahl | davon Kernzusagen | Stand vor AP2 |
|---|---|---|---|
| `[TECHNISCH]` | 25 von 26 | 6 von 6 | 20 |
| `[TEXTUELL]` | 1 von 26 (B9, für den Teil jenseits der Verweigerungen) | 0 | 2 |
| `[NICHT ABBILDBAR]` | **0 von 26** | 0 | 4 |

**Der entscheidende Befund:** Alle sechs Kernzusagen sind technisch abgebildet – und seit `CR-2026-017` steht keine Zusage mehr auf `[NICHT ABBILDBAR]`. Die vier Zeilen, die dort standen (R2, R3, R4, S4), waren sämtlich Unterschätzungen des Clients: `.claude/rules/` mit `paths:` bildet R2 und R3 ab, ein Zeichenlimit ist dokumentiert (R4), und `disable-model-invocation` trägt S4 (`CR-2026-016`).

Ein Vergleich mit dem Client Pack `devin-desktop` trägt nicht: Dort sind 21 von 26 Zeilen als `[TECHNISCH]` **vorgesehen**, aber keine einzige Einstufung ist gegen eine Installation oder gegen die Herstellerdokumentation geprüft. Die Zahlen messen bis dahin Verschiedenes.

**Belegstand:** Keine Zeile trägt mehr einen VERIFY-Marker (bei `devin-desktop`: 13). Offen ist eine **Teilfrage** innerhalb von M2: ob die Sperre gegen den Modus ohne Rückfragen auch für das Feld `permissionMode` eines Subagentenprofils gilt (AP2-CC-12). Zehn Zeilen sind gegen die Herstellerdokumentation der Clientversion 2.1.267 und die erzeugten Artefakte belegt; **beobachtete Durchsetzung in einer laufenden Sitzung ist für keine Zeile belegt** – die Wirkungsnachweise stehen aus (`tests/protocols/2026-09-10-AP2-claude-code.md`, Abschnitt „Offen").

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

- **Der Schutz-Hook kann hier tatsächlich blockieren.** Bei `devin-desktop` ist H2 als `[TEXTUELL]` eingestuft, weil das Eingabeschema unbestätigt ist und das Hook-Skript deshalb fail-open läuft. Für diesen Client ist das Blockierverhalten über den Exit-Code dokumentiert. **Empfehlung:** Nach Bestätigung in einer Installation `FW_HOOK_FAIL_CLOSED` auf `1` setzen (über `env` in `settings.json`). Das ist bewusst **nicht** vorbelegt, solange die Bestätigung aussteht.

- **Die Berechtigungsdatei trägt hier auch die Hooks.** Weil dieser Client keine eigene Hook-Datei kennt, stehen die Hooks in derselben Datei – und die ist Saat, gehört nach der Erstinstallation also dem Projekt und wird von `install.py --update` nie überschrieben. Eine Änderung an den Hooks des Kerns erreicht ein bestehendes Projekt dieses Packs deshalb nicht von selbst; bei `devin-desktop` mit eigener Hook-Datei tut sie es. Beim Release-Wechsel ist das hier ausdrücklich zu prüfen.

- **Erledigt (`CR-2026-006` bis `CR-2026-008`).** Die zwölf `fw-*`-Skills, die Regeltexte, das Overlay und zuletzt Berechtigungen und Hooks lagen zwischenzeitlich in jedem Pack doppelt. Sie liegen jetzt einmal im Kern.

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

## 8. Änderungsverlauf

| Version | Datum | Änderung | Autor (Rolle) |
|---|---|---|---|
| 0.1.0 | 2026-09-10 | angelegt (`CR-2026-004`) | `<FRAMEWORK_OWNER>` |
| 0.2.0 | 2026-09-10 | Berechtigungen und Hooks aus dem Pack in den Kern; Semantikabbildung ergänzt (`CR-2026-008`) | `<FRAMEWORK_OWNER>` |
| 0.3.0 | 2026-09-10 | Overlay-Laufzeitregel und die beiden Vorlagen in den Kern; Pack umfasst vier Dateien (`CR-2026-010`) | `<FRAMEWORK_OWNER>` |
| 0.4.0 | 2026-09-10 | **Erste Validierung gegen eine reale Installation und die Herstellerdokumentation (AP2, Clientversion 2.1.267).** Alle zehn Pruefmarker abgearbeitet: sechs belegt, zwei als ueberholt gekennzeichnet (R2/R3, S4), einer als Abwesenheitsbeleg, einer um die dokumentierte Grenze der Praefixmuster ergaenzt. Abschnitt 7 nennt die 17 wirkungslosen Regeln der erzeugten Berechtigungsdatei. Protokoll: `tests/protocols/2026-09-10-AP2-claude-code.md` | `<FRAMEWORK_OWNER>` |
| 0.5.0 | 2026-09-10 | **Drei Befunde aus AP2 behoben (`CR-2026-016`, D-26).** `triggers` wird nicht mehr ersatzlos verworfen, sondern auf `disable-model-invocation` abgebildet - die Zusage S4 gilt damit auch in der Installation. Pfadregeln werden nur noch fuer `Read` und `Edit` erzeugt: 18 wirkungslose Regeln entfallen, die Berechtigungsdatei schrumpft von 83 auf 65 Regeln. `install.py --client claude-code` gefolgt von `validate-framework.py` laeuft erstmals fehlerfrei | `<FRAMEWORK_OWNER>` |
| 0.6.0 | 2026-09-10 | **R2 und R3 abgebildet (`CR-2026-017`, D-27).** Die Regelablage liegt in `.claude/rules/`; der Client laedt sie von sich aus, die `@`-Importe der Wurzel-Anweisung entfallen. Die Ladetrigger der Kernquelle werden abgebildet statt zu Kommentar zu werden: `glob` auf `paths`, `always_on` und `model_decision` auf unbedingtes Laden. Erstmals gerendert werden auch die Regelvorlagen und die Laufzeitfassungen aktivierter Role und Technology Packs - eine aktivierte Role-Pack-Regel war bei diesem Client bisher wirkungslos. Keine Einstufung steht mehr auf `[NICHT ABBILDBAR]`; die mit `CR-2026-016` bereits behobene Zeile S4 und die Restangaben zu AP2-CC-02 in den Abschnitten 1a, 4, 5 und 7 sind nachgezogen | `<FRAMEWORK_OWNER>` |
| 0.7.0 | 2026-09-10 | **Belegspalte nennt die Quelle (`CR-2026-018`, `FW-AK-01`).** Jede mit AP2 belegte Zeile nennt die Seite der Herstellerdokumentation, auf die sie sich stuetzt; die vollstaendige Belegzuordnung steht im Hauptdokument in Anhang 31.4.2, der bis dahin ausschliesslich Devin-Quellen fuehrte. Neu aufgenommen: AP2-CC-12 (`permissionMode` im Subagentenprofil, offene Teilfrage zu M2). Genauer belegt: H2 (ein blockierender Hook geht auch einer `allow`-Regel vor), A1 (`disallowedTools` zuerst; ein Profil ohne aufloesbares Werkzeug startet nicht), S4 (die Sperre haelt die Skill-Beschreibung aus dem Kontext) | `<FRAMEWORK_OWNER>` |

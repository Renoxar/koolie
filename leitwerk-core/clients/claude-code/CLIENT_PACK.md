# Client Pack `claude-code`

| Attribut | Wert |
|---|---|
| Modul-ID | `CP-CC` |
| Ebene | keine – Abbildungsschicht |
| Version | 0.5.0 |
| Status | entwurf |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Client | Claude Code |
| Geprüfte Clientversion | 2.1.267 (AP2-Dokumentenabgleich, `tests/protocols/2026-09-10-AP2-claude-code.md`). Die **verbindliche Zielversion** legt `<FRAMEWORK_OWNER>` fest und steht aus |
| Datum der Prüfung | 2026-09-10 – Dokumentenabgleich und Prüfung der erzeugten Artefakte; die Wirkungsnachweise in einer Sitzung stehen aus |

> **Teilweise belegt (Stand 0.4.0).** Acht der zehn Pruefmarker sind gegen die
> Herstellerdokumentation der Clientversion 2.1.267 und gegen eine reale Erstinstallation
> abgeglichen (`tests/protocols/2026-09-10-AP2-claude-code.md`). **Zwei Einstufungen sind
> nachweislich überholt und noch nicht korrigiert** – R2/R3 und S4; ihre Berichtigung ändert
> die Semantikabbildung und läuft als eigener Änderungsantrag. Kein Wirkungsnachweis aus einer
> laufenden Sitzung liegt vor: Ein Dokumentenabgleich belegt `[DOK]`, nicht beobachtete
> Durchsetzung.
>
> **Zur Lesart der Spalten.** Die Spalte „Einstufung" nennt die **vorgesehene** Durchsetzungstiefe, die Spalte „Beleg" ihren Nachweisstand: `[DOK]` = in der Herstellerdokumentation beschrieben, `[EMPF]` = Empfehlung des Frameworks, VERIFY-Marker = gegen die aktuelle Dokumentation beziehungsweise eine Installation zu prüfen. Solange die Zielversion nicht festgelegt und geprüft ist, gilt das Pack als **unbelegt**.

## 1. Pfadabbildung

Maschinenlesbar in `manifest.json`; diese Tabelle ist die menschenlesbare Fassung.

| Rolle des Artefakts | Pfad bei diesem Client | Belegstatus |
|---|---|---|
| Wurzel-Anweisungsdatei | `CLAUDE.md` | `[DOK]` |
| Regeldateien | `.claude/framework/*.md`, eingebunden über `@pfad`-Importe in `CLAUDE.md` | Importmechanismus `[DOK]`; Ablageort `[KONZ]` Framework-Konvention |
| Skills | `.claude/skills/<name>/SKILL.md` | `[DOK]` |
| Subagentenprofile | `.claude/agents/<name>.md`, Frontmatter-Feld `tools` | [DOK] (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) |
| Berechtigungskonfiguration | `.claude/settings.json` (erzeugt aus `framework/runtime/permissions.json`) | `[DOK]` Mechanismus; Mustersemantik [DOK] (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) – gitignore-Syntax, Einzelheiten bei B3. **Pfadregeln werden nur für `Read` und `Edit` ausgewertet**, siehe Abschnitt 7 |
| Hook-Konfiguration | `.claude/settings.json` (**keine eigene Datei**; erzeugt aus `framework/runtime/hooks.json` und in dieselbe Datei eingebettet) | `[DOK]` |
| MCP-Konfiguration | `.mcp.json` (Vorlage: `.mcp.json.example`) | `[DOK]` |
| Projektverzeichnis-Variable in Hooks | `CLAUDE_PROJECT_DIR` | `[DOK]` |
| Nutzerlokale Überschreibung | `CLAUDE.local.md`, `.claude/settings.local.json` | `[DOK]` |

## 1a. Semantikabbildung der Berechtigungen und Hooks

Die Regelmenge liegt werkzeugneutral im Kern (`leitwerk-core/framework/runtime/permissions.json`, `hooks.json`) und wird bei der Installation in die Werkzeuge dieses Clients übersetzt (D-18). Was dabei abgebildet wird, steht maschinenlesbar im `manifest.json`; diese Tabelle ist die menschenlesbare Fassung. Dieser Client ist der Grund, weshalb es die Abbildungsschicht überhaupt braucht: Vier der sechs Zeilen sind keine Umbenennung, sondern eine andere Mengenlehre.

| Neutrales Werkzeugverb | Werkzeug bei diesem Client | Anmerkung |
|---|---|---|
| `read` | `Read(muster)` | |
| `search` | `Grep(muster)`, `Glob(muster)` | eigene Suchwerkzeuge, im Kern als ein Verb geführt |
| `write` | `Edit(muster)` **und** `Write(muster)` | Ändern und Anlegen sind getrennte Werkzeuge; **eine Regel allein liefe ins Leere** |
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

## 2. Fähigkeitsmatrix

### R – Regelladung

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| R1 | Wurzel-Anweisungsdatei wird ungefragt geladen | `CLAUDE.md` wird zu Beginn jeder Sitzung geladen | `[TECHNISCH]` | `[DOK]` |
| R2 | Regeldateien mit Ladebedingungen | **Kein Äquivalent.** Regeltexte werden über `@pfad`-Importe eingebunden und sind damit immer geladen | `[NICHT ABBILDBAR]` – **überholt, siehe AP2-CC-03** | Der Client kennt `.claude/rules/*.md` mit `paths:`-Frontmatter: Regeln, die nur bei Arbeit an passenden Dateien laden. Berichtigung folgt als Änderungsantrag |
| R3 | Regeln an Dateimuster bindbar (Grundlage der Technology Packs) | **Äquivalent vorhanden:** `paths:`-Frontmatter in `.claude/rules/` bindet eine Regel an Glob-Muster. Bisher genannter Teilersatz: eine `CLAUDE.md` im Unterverzeichnis | `[NICHT ABBILDBAR]` – **überholt, siehe AP2-CC-03** | `[DOK]`; Berichtigung folgt als Änderungsantrag |
| R4 | Bekanntes Zeichenlimit, das das Framework einhalten kann | **4 MiB** je Anweisungsdatei; eine größere Datei wird übersprungen. Zusätzlich als Empfehlung 200 Zeilen | `[TECHNISCH]` | [DOK] (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) |

### S – Skills

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| S1 | Versionierte Skills im Repository | `.claude/skills/<name>/SKILL.md` mit Frontmatter | `[TECHNISCH]` | `[DOK]`; zusätzlich **beobachtet** (siehe Abschnitt 6) |
| S2 | Gezielter Aufruf | Aufruf über den Skill-Namen mit vorangestelltem Schrägstrich | `[TECHNISCH]` | `[DOK]` |
| S3 | Werkzeugbeschränkung je Skill | Frontmatter `allowed-tools` als kommagetrennte Liste | `[TECHNISCH]` | `[DOK]` |
| S4 | Schreibende Skills nur benutzergetriggert | **Kein gesichertes Äquivalent.** Ein Skill mit `description` steht dem Modell zur Wahl. Ersatz: `ask` auf `Edit(**)` und `Write(**)` – jede Schreiboperation löst eine Rückfrage aus, unabhängig davon, wer den Skill gewählt hat | `[NICHT ABBILDBAR]` – **überholt, siehe AP2-CC-01** | Das Feld existiert: `disable-model-invocation: true` verhindert, dass das Modell den Skill selbst lädt. Die Semantikabbildung verwirft `triggers` derzeit ersatzlos (`drop_fields`); Berichtigung folgt als Änderungsantrag |

### B – Berechtigungen

| ID | Zusage des Frameworks | Kern | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|---|
| B1 | Berechtigungen versioniert im Repository | ja | `.claude/settings.json` | `[TECHNISCH]` | `[DOK]` |
| B2 | Verweigern vor Rückfragen vor Erlauben | ja | `permissions.deny` / `.ask` / `.allow` | `[TECHNISCH]` | `[DOK]` |
| B3 | Secret-Dateien per Pfadmuster lesegeschützt | ja | Verweigerungsregeln auf `./.env`, `**/*.pem`, `**/secrets/**` und weitere. Mustersemantik: gitignore-Syntax; ein bloßer Dateiname trifft in jeder Tiefe (`Read(.env)` ist gleichbedeutend mit `Read(**/.env)`); ein einsegmentiges Verzeichnismuster trifft in `deny` und `ask` in jeder Tiefe, in `allow` nur am verankerten Ort. Unter Windows werden Pfade vor dem Vergleich auf POSIX-Form normalisiert | `[TECHNISCH]` | [DOK] (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) |
| B4 | Framework- und Overlay-Artefakte schreibgeschützt | ja | Je Pfad **zwei** Regeln, weil Ändern und Anlegen getrennte Werkzeuge sind; das Kernverzeichnis ist seit `CR-2026-012` als Ganzes erfasst (`Edit(leitwerk-core/**)` und `Write(leitwerk-core/**)`) | `[TECHNISCH]` | wie B3 |
| B5 | CI-, Quality-Gate- und Lockdateien schreibgeschützt | ja | dito, je Pfad zwei Regeln | `[TECHNISCH]` | wie B3 |
| B6 | Befehle per Muster verweigerbar | ja | Präfixmuster, z. B. `Bash(git push:*)`. Wirkt **breiter** als eine Verweigerung des vollständigen Befehls | `[TECHNISCH]` | wie B3 |
| B7 | Schreiboperationen fragen zurück | – | `ask` auf `Edit(**)` und `Write(**)` | `[TECHNISCH]` | `[DOK]` |
| B8 | Netzwerkzugriff standardmäßig unterbunden | – | Verweigerung der Abruf- und Suchwerkzeuge sowie von `curl` und `wget` | `[TECHNISCH]` | `[DOK]` |
| B9 | Nutzerlokale Konfiguration kann nur verschärfen | – | `.claude/settings.local.json` rangiert **über** der Projektdatei, kann eine dort gesetzte Verweigerung aber nicht aufheben: „If a tool is denied at any level, no other level can allow it." Ergänzend greifen `deny`- und `ask`-Regeln sofort, `allow`-Regeln erst nach dem Vertrauen in den Ordner | `[TECHNISCH]` für die Verweigerungen; `[TEXTUELL]` für den Rest | [DOK] (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) |

### H – Hooks

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| H1 | Prüfung vor Werkzeugausführung | `hooks.PreToolUse` in `settings.json`, Matcher auf schreibende und ausführende Werkzeuge | `[TECHNISCH]` | `[DOK]` |
| H2 | Prüfung kann **blockieren** | Exit-Code 2 des Hook-Befehls blockiert die Ausführung | `[TECHNISCH]` | `[DOK]` – **stärker belegt als beim Client Pack `devin-desktop`**, siehe Abschnitt 5 |
| H3 | Statusmeldung beim Sitzungsstart | `hooks.SessionStart` | `[TECHNISCH]` | `[DOK]` |

### A – Agentenprofile

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| A1 | Rein lesendes Reviewprofil | `.claude/agents/fw-reviewer.md`, Frontmatter-Feld `tools` (ergänzend `disallowedTools`); die Beschränkung wirkt technisch | `[TECHNISCH]` | [DOK] (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) |

### M – Modi und Sitzungsfreigaben

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| M1 | Standardmodus fragt bei Schreiben und Befehlen zurück | `permissions.defaultMode` auf `default` | `[TECHNISCH]` | `[DOK]` |
| M2 | Modus ohne Rückfragen ausschließbar | Per D-05 untersagt **und** technisch sperrbar: `permissions.disableBypassPermissionsMode` auf `"disable"`, in verwalteten Einstellungen nicht überschreibbar. Zusätzlich wirken `bypassPermissions` und `auto` seit Clientversion 2.1.257 nicht mehr aus Projekt- oder nutzerlokalen Einstellungen | `[TECHNISCH]` (Sperre in verwalteten Einstellungen setzt eine Enterprise-Verwaltung voraus) | [DOK] (AP2, Clientversion 2.1.267, `tests/protocols/2026-09-10-AP2-claude-code.md`) |
| M3 | Freigabe auf die Sitzung begrenzbar | Rückfragen bieten eine einmalige und eine sitzungsweite Bestätigung an | `[TECHNISCH]` | `[DOK]` |

### X – Externe Anbindung

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| X1 | Keine externe Anbindung ohne Einzelfreigabe | Keine `.mcp.json` ausgeliefert, nur die `.example`-Vorlage; Rückfrageregel auf alle MCP-Werkzeuge | `[TECHNISCH]` | `[DOK]` |
| X2 | Art und Ort der Codebasis-Indexierung bekannt | Kein Indexierungsmechanismus dokumentiert; Dateien werden bei Bedarf gelesen | `[TECHNISCH]` | `[DOK]` – Abwesenheit belegt, Stand 2.1.267 (AP2) |

## 3. Zusammenfassung der Durchsetzungstiefe

| Klasse | Anzahl | davon Kernzusagen |
|---|---|---|
| `[TECHNISCH]` | 20 von 26 | 6 von 6 |
| `[TEXTUELL]` | 2 von 26 | 0 |
| `[NICHT ABBILDBAR]` | 4 von 26 | 0 |

**Der entscheidende Befund:** Alle sechs Kernzusagen sind technisch abgebildet. Die vier nicht abbildbaren Zusagen (R2, R3, R4, S4) betreffen ausschließlich **Least Context und Ergonomie**, keine Schutzzusage – und S4 hat mit der Rückfragepflicht bei Schreiboperationen eine wirksame Ersatzmaßnahme.

Im Vergleich zum Client Pack `devin-desktop`: dort 21 `[TECHNISCH]`, hier 20. Der Unterschied liegt nicht im Schutzniveau, sondern in den Ladetriggern.

**Belegstand:** 9 der 26 Zeilen tragen einen VERIFY-Marker (bei `devin-desktop`: 13). Keine Einstufung ist gegen eine Installation geprüft.

## 4. Kernzusagen ohne technische Durchsetzung

**Keine.** Alle sechs Kernzusagen (B1 bis B6) sind als `[TECHNISCH]` abgebildet. Ein Eintrag in dieser Tabelle ist nicht erforderlich – unter dem Vorbehalt, dass die Prüfung nach Roadmap AP2 die Einstufungen bestätigt.

Drei der sechs weichen in der **Form** ab, nicht in der Tiefe; beide Abweichungen sind Verschärfungen:

| ID | Abweichung | Wirkung |
|---|---|---|
| B4, B5 | Schreibschutz erfordert je Pfad zwei Regeln, weil Ändern und Anlegen getrennte Werkzeuge sind | Keine. Seit `CR-2026-008` erzeugt die Abbildung beide Regeln aus einer Quellregel; ein Vergessen ist nicht mehr möglich, und der Validator gleicht die Kernregelliste gegen die Kernquelle ab |
| B6 | Befehlsverbote wirken präfixbasiert: `Bash(git reset:*)` sperrt jedes `git reset`, nicht nur `--hard` | Verschärfung, seit `CR-2026-008` nachweisbar: Die Abbildung verlangt, dass die Präfixform ein Präfix der wörtlichen Form ist, und weist sie sonst zurück. Auch unkritische Varianten sind gesperrt |

## 5. Bekannte Abweichungen im Verhalten

- **Keine Ladetrigger; alle Regeltexte sind immer geladen.** Bei `devin-desktop` laden `10-privacy-security` und `15-development-rules` nur bei Relevanz. Hier werden sie über Importe in `CLAUDE.md` stets mitgeladen. Für die Regelwirkung ist das eine **Verschärfung**; für den Kontext bedeutet es rund **22.000 Zeichen** ständige Belegung. Least Context ist ein Prinzip zur Ergebnisqualität, keine Sicherheitszusage – die Abweichung ist deshalb vertretbar, wächst aber mit jedem aktivierten Pack.

- **Technology Packs haben kein direktes Äquivalent.** Ein Pack, das bei `devin-desktop` über ein Dateimuster lädt, braucht hier einen von zwei Wegen: eine verschachtelte `CLAUDE.md` im betreffenden Verzeichnis (wenn Technologie und Verzeichnis zusammenfallen, etwa `backend/` und `frontend/`) oder einen Import in `CLAUDE.md` (dann immer geladen). Die Wahl ist im Overlay zu dokumentieren.

- **Eine Regeldatei ohne Import ist wirkungslos.** Bei Clients mit Ladetriggern genügt das Frontmatter, damit eine Regel wirkt. Hier wirkt sie erst durch die Einbindung – ein stiller Fehlerfall. Der Validator prüft deshalb, dass jede Kernregel (`00-`, `10-`, `15-`, `20-`) in `CLAUDE.md` eingebunden ist.

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

### Wirkungslose Regeln in der erzeugten Berechtigungsdatei (AP2-CC-02)

**Bekannt und noch nicht behoben.** Der Client wertet Pfadregeln ausschliesslich fuer `Read`
und `Edit` aus: eine Pfadregel fuer `Write`, `NotebookEdit`, `Glob` oder `MultiEdit` wird
angenommen, nie konsultiert und beim Sitzungsstart als Warnung gemeldet.

Die Semantikabbildung erzeugt je Pfad zusaetzlich eine `Write(...)`-Regel. In einer frischen
Installation sind das **16 wirkungslose Regeln**, dazu ein `Glob(**)` in `allow` - jede mit
einer Startwarnung. Vier davon stehen in `_core_rules_integrity.deny_must_contain` und werden
vom Validator eingefordert.

**Der Schutz haelt trotzdem:** Die `Edit(...)`-Haelfte greift, B4 und B5 bleiben `[TECHNISCH]`.
Die in Abschnitt 1a beschriebene Verschaerfung - je Pfad zwei Regeln, weil Aendern und Anlegen
getrennte Werkzeuge sind - ist fuer **Pfadregeln** jedoch keine. Fuer eine Regel **ohne** Pfad
gilt sie weiterhin: Eine Verweigerung des blossen Werkzeugnamens `Write` wirkt ueberall.

Die Berichtigung aendert die Semantikabbildung und damit D-18; sie laeuft als eigener
Aenderungsantrag.

## 8. Änderungsverlauf

| Version | Datum | Änderung | Autor (Rolle) |
|---|---|---|---|
| 0.1.0 | 2026-09-10 | angelegt (`CR-2026-004`) | `<FRAMEWORK_OWNER>` |
| 0.2.0 | 2026-09-10 | Berechtigungen und Hooks aus dem Pack in den Kern; Semantikabbildung ergänzt (`CR-2026-008`) | `<FRAMEWORK_OWNER>` |
| 0.3.0 | 2026-09-10 | Overlay-Laufzeitregel und die beiden Vorlagen in den Kern; Pack umfasst vier Dateien (`CR-2026-010`) | `<FRAMEWORK_OWNER>` |
| 0.4.0 | 2026-09-10 | **Erste Validierung gegen eine reale Installation und die Herstellerdokumentation (AP2, Clientversion 2.1.267).** Alle zehn Pruefmarker abgearbeitet: sechs belegt, zwei als ueberholt gekennzeichnet (R2/R3, S4), einer als Abwesenheitsbeleg, einer um die dokumentierte Grenze der Praefixmuster ergaenzt. Abschnitt 7 nennt die 17 wirkungslosen Regeln der erzeugten Berechtigungsdatei. Protokoll: `tests/protocols/2026-09-10-AP2-claude-code.md` | `<FRAMEWORK_OWNER>` |
| 0.5.0 | 2026-09-10 | **Drei Befunde aus AP2 behoben (`CR-2026-016`, D-26).** `triggers` wird nicht mehr ersatzlos verworfen, sondern auf `disable-model-invocation` abgebildet - die Zusage S4 gilt damit auch in der Installation. Pfadregeln werden nur noch fuer `Read` und `Edit` erzeugt: 18 wirkungslose Regeln entfallen, die Berechtigungsdatei schrumpft von 83 auf 65 Regeln. `install.py --client claude-code` gefolgt von `validate-framework.py` laeuft erstmals fehlerfrei | `<FRAMEWORK_OWNER>` |

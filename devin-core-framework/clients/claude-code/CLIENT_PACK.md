# Client Pack `claude-code`

| Attribut | Wert |
|---|---|
| Modul-ID | `CP-CC` |
| Ebene | keine – Abbildungsschicht |
| Version | 0.1.0 |
| Status | entwurf |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Client | Claude Code |
| Geprüfte Clientversion | `<TBD: verbindliche Zielversion; Roadmap AP2>` |
| Datum der Prüfung | `<TBD: steht aus>` |

> **Keine Einstufung dieses Packs ist gegen eine reale Installation belegt.** Die Spalte „Einstufung" nennt die **vorgesehene** Durchsetzungstiefe, die Spalte „Beleg" ihren Nachweisstand: `[DOK]` = in der Herstellerdokumentation beschrieben, `[EMPF]` = Empfehlung des Frameworks, VERIFY-Marker = gegen die aktuelle Dokumentation beziehungsweise eine Installation zu prüfen. Solange die Zielversion nicht festgelegt und geprüft ist, gilt das Pack als **unbelegt**.

## 1. Pfadabbildung

Maschinenlesbar in `manifest.json`; diese Tabelle ist die menschenlesbare Fassung.

| Rolle des Artefakts | Pfad bei diesem Client | Belegstatus |
|---|---|---|
| Wurzel-Anweisungsdatei | `CLAUDE.md` | `[DOK]` |
| Regeldateien | `.claude/framework/*.md`, eingebunden über `@pfad`-Importe in `CLAUDE.md` | Importmechanismus `[DOK]`; Ablageort `[KONZ]` Framework-Konvention |
| Skills | `.claude/skills/<name>/SKILL.md` | `[DOK]` |
| Subagentenprofile | `.claude/agents/<name>.md` | `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>` (Feldname `tools`) |
| Berechtigungskonfiguration | `.claude/settings.json` | `[DOK]` Mechanismus; Mustersemantik `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>` |
| Hook-Konfiguration | `.claude/settings.json` (**keine eigene Datei**) | `[DOK]` |
| MCP-Konfiguration | `.mcp.json` (Vorlage: `.mcp.json.example`) | `[DOK]` |
| Projektverzeichnis-Variable in Hooks | `CLAUDE_PROJECT_DIR` | `[DOK]` |
| Nutzerlokale Überschreibung | `CLAUDE.local.md`, `.claude/settings.local.json` | `[DOK]` |

## 2. Fähigkeitsmatrix

### R – Regelladung

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| R1 | Wurzel-Anweisungsdatei wird ungefragt geladen | `CLAUDE.md` wird zu Beginn jeder Sitzung geladen | `[TECHNISCH]` | `[DOK]` |
| R2 | Regeldateien mit Ladebedingungen | **Kein Äquivalent.** Regeltexte werden über `@pfad`-Importe eingebunden und sind damit immer geladen | `[NICHT ABBILDBAR]` | `[DOK]` (Import); Fehlen von Ladetriggern `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>` |
| R3 | Regeln an Dateimuster bindbar (Grundlage der Technology Packs) | **Kein Äquivalent.** Teilersatz: eine `CLAUDE.md` in einem Unterverzeichnis wird beim Zugriff darauf geladen | `[NICHT ABBILDBAR]` | `[DOK]` (verschachtelte Anweisungsdateien) |
| R4 | Bekanntes Zeichenlimit, das das Framework einhalten kann | Kein Limit dokumentiert | `[NICHT ABBILDBAR]` | `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>` |

### S – Skills

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| S1 | Versionierte Skills im Repository | `.claude/skills/<name>/SKILL.md` mit Frontmatter | `[TECHNISCH]` | `[DOK]`; zusätzlich **beobachtet** (siehe Abschnitt 6) |
| S2 | Gezielter Aufruf | Aufruf über den Skill-Namen mit vorangestelltem Schrägstrich | `[TECHNISCH]` | `[DOK]` |
| S3 | Werkzeugbeschränkung je Skill | Frontmatter `allowed-tools` als kommagetrennte Liste | `[TECHNISCH]` | `[DOK]` |
| S4 | Schreibende Skills nur benutzergetriggert | **Kein gesichertes Äquivalent.** Ein Skill mit `description` steht dem Modell zur Wahl. Ersatz: `ask` auf `Edit(**)` und `Write(**)` – jede Schreiboperation löst eine Rückfrage aus, unabhängig davon, wer den Skill gewählt hat | `[NICHT ABBILDBAR]` | Ob ein Frontmatter-Feld die Modellwahl unterbinden kann: `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>` |

### B – Berechtigungen

| ID | Zusage des Frameworks | Kern | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|---|
| B1 | Berechtigungen versioniert im Repository | ja | `.claude/settings.json` | `[TECHNISCH]` | `[DOK]` |
| B2 | Verweigern vor Rückfragen vor Erlauben | ja | `permissions.deny` / `.ask` / `.allow` | `[TECHNISCH]` | `[DOK]` |
| B3 | Secret-Dateien per Pfadmuster lesegeschützt | ja | Verweigerungsregeln auf `./.env`, `**/*.pem`, `**/secrets/**` und weitere | `[TECHNISCH]` | Mechanismus `[DOK]`; Mustersemantik `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>` |
| B4 | Framework- und Overlay-Artefakte schreibgeschützt | ja | Je Pfad **zwei** Regeln, weil Ändern und Anlegen getrennte Werkzeuge sind | `[TECHNISCH]` | wie B3 |
| B5 | CI-, Quality-Gate- und Lockdateien schreibgeschützt | ja | dito, je Pfad zwei Regeln | `[TECHNISCH]` | wie B3 |
| B6 | Befehle per Muster verweigerbar | ja | Präfixmuster, z. B. `Bash(git push:*)`. Wirkt **breiter** als eine Verweigerung des vollständigen Befehls | `[TECHNISCH]` | wie B3 |
| B7 | Schreiboperationen fragen zurück | – | `ask` auf `Edit(**)` und `Write(**)` | `[TECHNISCH]` | `[DOK]` |
| B8 | Netzwerkzugriff standardmäßig unterbunden | – | Verweigerung der Abruf- und Suchwerkzeuge sowie von `curl` und `wget` | `[TECHNISCH]` | `[DOK]` |
| B9 | Nutzerlokale Konfiguration kann nur verschärfen | – | `.claude/settings.local.json` – **Framework-Regel, keine Produkteigenschaft** | `[TEXTUELL]` | `[EMPF]`; ob eine Lockerung technisch verhindert wird: `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>` |

### H – Hooks

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| H1 | Prüfung vor Werkzeugausführung | `hooks.PreToolUse` in `settings.json`, Matcher auf schreibende und ausführende Werkzeuge | `[TECHNISCH]` | `[DOK]` |
| H2 | Prüfung kann **blockieren** | Exit-Code 2 des Hook-Befehls blockiert die Ausführung | `[TECHNISCH]` | `[DOK]` – **stärker belegt als beim Client Pack `devin-desktop`**, siehe Abschnitt 5 |
| H3 | Statusmeldung beim Sitzungsstart | `hooks.SessionStart` | `[TECHNISCH]` | `[DOK]` |

### A – Agentenprofile

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| A1 | Rein lesendes Reviewprofil | `.claude/agents/fw-reviewer.md`, Frontmatter-Feld `tools` | `[TECHNISCH]` | `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>` |

### M – Modi und Sitzungsfreigaben

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| M1 | Standardmodus fragt bei Schreiben und Befehlen zurück | `permissions.defaultMode` auf `default` | `[TECHNISCH]` | `[DOK]` |
| M2 | Modus ohne Rückfragen ausschließbar | Der Modus `bypassPermissions` ist per D-05 untersagt. Ob eine **technische** Sperre über verwaltete Einstellungen möglich ist, ist nicht belegt | `[TEXTUELL]` | `[EMPF]`; Verfügbarkeit einer Sperre `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>` |
| M3 | Freigabe auf die Sitzung begrenzbar | Rückfragen bieten eine einmalige und eine sitzungsweite Bestätigung an | `[TECHNISCH]` | `[DOK]` |

### X – Externe Anbindung

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| X1 | Keine externe Anbindung ohne Einzelfreigabe | Keine `.mcp.json` ausgeliefert, nur die `.example`-Vorlage; Rückfrageregel auf alle MCP-Werkzeuge | `[TECHNISCH]` | `[DOK]` |
| X2 | Art und Ort der Codebasis-Indexierung bekannt | Kein Indexierungsmechanismus dokumentiert; Dateien werden bei Bedarf gelesen | `[TECHNISCH]` | `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>` |

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
| B4, B5 | Schreibschutz erfordert je Pfad zwei Regeln, weil Ändern und Anlegen getrennte Werkzeuge sind | Keine, sofern beide gesetzt sind. **Eine Regel allein liefe ins Leere** – deshalb prüft der Validator die Kernregelliste, die beide Formen enthält |
| B6 | Befehlsverbote wirken präfixbasiert: `Bash(git reset:*)` sperrt jedes `git reset`, nicht nur `--hard` | Verschärfung. Auch unkritische Varianten sind gesperrt |

## 5. Bekannte Abweichungen im Verhalten

- **Keine Ladetrigger; alle Regeltexte sind immer geladen.** Bei `devin-desktop` laden `10-privacy-security` und `15-development-rules` nur bei Relevanz. Hier werden sie über Importe in `CLAUDE.md` stets mitgeladen. Für die Regelwirkung ist das eine **Verschärfung**; für den Kontext bedeutet es rund **22.000 Zeichen** ständige Belegung. Least Context ist ein Prinzip zur Ergebnisqualität, keine Sicherheitszusage – die Abweichung ist deshalb vertretbar, wächst aber mit jedem aktivierten Pack.

- **Technology Packs haben kein direktes Äquivalent.** Ein Pack, das bei `devin-desktop` über ein Dateimuster lädt, braucht hier einen von zwei Wegen: eine verschachtelte `CLAUDE.md` im betreffenden Verzeichnis (wenn Technologie und Verzeichnis zusammenfallen, etwa `backend/` und `frontend/`) oder einen Import in `CLAUDE.md` (dann immer geladen). Die Wahl ist im Overlay zu dokumentieren.

- **Eine Regeldatei ohne Import ist wirkungslos.** Bei Clients mit Ladetriggern genügt das Frontmatter, damit eine Regel wirkt. Hier wirkt sie erst durch die Einbindung – ein stiller Fehlerfall. Der Validator prüft deshalb, dass jede Kernregel (`00-`, `10-`, `15-`, `20-`) in `CLAUDE.md` eingebunden ist.

- **Der Schutz-Hook kann hier tatsächlich blockieren.** Bei `devin-desktop` ist H2 als `[TEXTUELL]` eingestuft, weil das Eingabeschema unbestätigt ist und das Hook-Skript deshalb fail-open läuft. Für diesen Client ist das Blockierverhalten über den Exit-Code dokumentiert. **Empfehlung:** Nach Bestätigung in einer Installation `FW_HOOK_FAIL_CLOSED` auf `1` setzen (über `env` in `settings.json`). Das ist bewusst **nicht** vorbelegt, solange die Bestätigung aussteht.

- **Skills sind zwischen den Client Packs dupliziert.** Die zwölf `fw-*`-Skills liegen jetzt zweimal im Kern – einmal je Pack, mit unterschiedlichem Frontmatter bei identischem Rumpf. Eine Änderung an einem Skill muss in jedem Pack nachgezogen werden. Das ist mit zwei Packs handhabbar und skaliert nicht; ein Erzeugungsschritt aus einer gemeinsamen Quelle ist als Folgearbeit vorzusehen.

## 6. Beobachtung während der Erstellung

Beim Anlegen der Skills unter `.claude/skills/` hat die Sitzung, in der dieses Pack entstand, die zwölf Skills **selbsttätig erkannt und zur Verfügung gestellt**. Das belegt S1 über die Dokumentationslage hinaus.

Dieselbe Beobachtung deckte einen Konvertierungsfehler auf: Die Skills erschienen zunächst mit einer Beschreibung, die aus dem Dateikörper statt aus dem Frontmatter stammte. Ursache war ein Rest der Devin-Frontmatter-Felder, der beim Umschreiben stehen geblieben war. Der Fehler wäre bei einer rein statischen Prüfung nicht aufgefallen – die Konvertierung prüft seitdem nach dem Umschreiben, dass nur dokumentierte Felder übrig sind.

Das ist keine Belegprüfung im Sinne des Testkatalogs und ersetzt Roadmap-AP2 nicht.

## 7. Installation und Prüfung

```text
python devin-core-framework/install.py --client claude-code
python devin-core-framework/tests/scripts/validate-framework.py
```

Vor der ersten produktiven Nutzung sind die Basistests des Testkatalogs (`devin-core-framework/tests/TEST_CATALOG.md`, Kennzeichnung „Basis") gegen diesen Client zu fahren und zu protokollieren.

## 8. Änderungsverlauf

| Version | Datum | Änderung | Autor (Rolle) |
|---|---|---|---|
| 0.1.0 | 2026-09-10 | angelegt (`CR-2026-004`) | `<FRAMEWORK_OWNER>` |

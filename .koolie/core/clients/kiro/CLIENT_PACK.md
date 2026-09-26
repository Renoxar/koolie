# Client Pack `kiro`

| Attribut | Wert |
|---|---|
| Modul-ID | `CP-KI` |
| Ebene | keine – Abbildungsschicht |
| Version | 0.1.0 |
| Status | pilot |
| Owner (Rolle) | `<FRAMEWORK_OWNER>` |
| Client | Kiro – Kommandozeile (`kiro-cli`) und IDE; der autonome Agent in der Sandbox des Anbieters fällt unter D-10 und nicht unter dieses Pack |
| Verbindliche Zielversion | Kommandozeile `2.24.x` mit der Engine V3; IDE `1.1.x` (D-112). Die Engine V3 ist beim Hersteller eine Vorabversion; die Einstellungsdatei des Packs wählt sie (Abschnitt 1b) |
| Geprüfte Clientversion | Kommandozeile `2.24.1` (Agentenserver KAS `0.66.8`) – vor dem Messen festgeschrieben (D-117). IDE `1.1.70` (Agent-Erweiterung `1.1.158`) installiert, **an keiner Sitzung gemessen**. Konto: Free |
| Stand der Produktbeobachtung | Quellenliste in Anhang 31.4.4 (`QK-1` bis `QK-9`), abgerufen am 2026-09-26. `FW-AK-01` ist für dieses Pack nicht gefahren |
| Datum der Prüfung | **2026-09-26** – der Bau (`CR-2026-150`, `tests/protocols/2026-09-26-bau-kiro.md`): 23 Vorabmessungen und 16 Abnahmeläufe an realen Installationen, davon 9 interaktive Sitzungen über ein Pseudo-Terminal; rund 2,9 Credits |

> **Belegt, soweit gemessen (Stand 1.13.0).** Die Spalte „Einstufung" nennt die **vorgesehene** Durchsetzungstiefe, die Spalte „Beleg" ihren Nachweisstand: `gemessen` = an diesem Client beobachtet, `[DOK]` = aus der Herstellerdokumentation mit Quellenkennung, `[EMPF]` = Vorgabe des Frameworks, `BELEG OFFEN` = noch nicht belegt, mit Grund und Datum.
>
> **Alle sechs Kernzusagen sind `[TECHNISCH]`** – und alle sechs stehen unter derselben Bedingung: **Das Agentenprofil des Frameworks muss der aktive Agent sein** (Abschnitt 1b). 🔴 **Fehlt es oder ist es kaputt, fällt der Client still auf seinen eingebauten Agenten zurück**, und keine dieser Zeilen trägt mehr.
>
> 🔴 **Der schwerste Befund des Baus ist einer des Schutz-Hooks** (D-417): Mit der Standardsperrform endete der Hook mit Exit 2 – und der Köderinhalt kam heraus. Das Pack führt deshalb eine eigene Sperrform (H2).
>
> **Wer das Pack einsetzt,** liest zuerst Abschnitt 1b und Abschnitt 6.

## 1. Pfadabbildung

| Rolle des Artefakts | Pfad bei diesem Client | Belegstatus |
|---|---|---|
| Wurzel-Anweisungsdatei | `AGENTS.md` | **gemessen** (2026-09-26): steht in jeder Sitzung im Kontext (Aufschlüsselung der Kontextdateien, 2.972 Token), auch beim eigenen Agenten |
| Regeldateien | `.kiro/steering/*.md`; Lademodus im Frontmatter (`inclusion`) | **gemessen:** eine Datei ohne Frontmatter lädt in jeder Sitzung; eine mit `inclusion: fileMatch` nur, wenn eine passende Datei gelesen wird |
| Skills | `.kiro/skills/<name>/SKILL.md` | **gemessen:** aufgezählt (Ereignis `available_commands_update`, Art `skill`) und über `disclose_context` geladen – auch mit den Frontmatter-Feldern des Frameworks |
| Subagentenprofile | `.kiro/agents/<name>.md` (Frontmatter `tools` mit Kategorien) | `[DOK]` **`QK-6`**; die Wirkung ist Gegenstand von A1 |
| Berechtigungskonfiguration | `.kiro/agents/koolie.json` – ein **Agentenprofil** mit dem Feld `permissions.rules` (erzeugt aus `framework/runtime/permissions.json`) | **gemessen:** ein `deny` darin weist ab und nennt sich (*„Source: agent-profile"*). Warum kein `permissions.yaml`: Die Datei des Arbeitsbereichs liegt beim Client **außerhalb** des Repositoriums (`QK-1`) |
| Wahl des Agenten und der Engine | `.kiro/settings/cli.json` (`chat.defaultAgent`, `chat.agentEngine`) | **gemessen:** Mit ihr startet `kiro-cli chat` ohne Schalter mit Engine V3 und dem Agenten `koolie`; eine globale Einstellung unterliegt ihr |
| Hook-Konfiguration | `.kiro/hooks/koolie.json`, Form `{version: v1, hooks: [...]}` | **gemessen:** lädt in der **interaktiven** Sitzung; im Betrieb ohne Rückfragen gar nicht (Abschnitt 1b) |
| Planartefakt | `.kiro/specs/<name>/` (`requirements.md`, `design.md`, `tasks.md`) | **gemessen:** der Träger des Plans nach D-415; die Regel `16-plan-spezifikation.md` gibt ihm die Pflichtfelder |
| MCP-Konfiguration | `.kiro/settings/mcp.json` | `[DOK]` **`QK-7`**; das Framework liefert keinen Server aus |
| Projektverzeichnis im Hook-Befehl | **keine Variable – das Arbeitsverzeichnis** | **gemessen:** `cwd` der Eingabe und Arbeitsverzeichnis des Hook-Prozesses sind die Projektwurzel |
| Nutzerlokale Überschreibung | **kein Mechanismus** | Der Hersteller dokumentiert keine nutzerlokale Wurzel-Anweisung; das Pack liefert keine Beispieldatei aus |

## 1a. Semantikabbildung der Berechtigungen

Die Regelmenge liegt werkzeugneutral im Kern und wird bei der Installation übersetzt (D-18). **Dieser Client kennt keine Regel der Gestalt `Werkzeug(Muster)`**, sondern Regeln je **Fähigkeit** mit einer Liste von Mustern (`{capability, match, exclude, effect}`); die Abbildung erzeugt je Korb und Fähigkeit eine Regel (D-414).

| Neutrales Werkzeugverb | Fähigkeit bei diesem Client | Anmerkung |
|---|---|---|
| `read` | `fs_read` | Ein Muster ohne Wildcard trifft auch Unterverzeichnisse (gemessen: `.env` sperrte `sub/.env`) – breiter als wörtlich |
| `search` | `fs_read` | Keine eigene Fähigkeit; die Suchwerkzeuge sind lesend |
| `write` | `fs_write` | Ein Schreibverbot kann einen Teilbaum ausnehmen (`exclude`) – genutzt für `.kiro/specs/**` (D-415) |
| `exec` | `shell`, Muster **mit** Stern (`git push*`) | Ohne Stern vergleicht der Client wörtlich – gemessen: `echo` sperrte `echo hallo` nicht. Verkettete Befehle zerlegt er |
| `fetch` | `web_fetch`, `web_search` | Mit `deny "*"` nimmt der Client beide Werkzeuge ganz aus dem Werkzeugbestand |
| `mcp` | `mcp` | |
| `skill` | `skill`, **wörtlicher Name** | gemessen: die Freigabe auf einen Namen lädt genau diesen Skill |

| Weitere Eigenschaft | Wert |
|---|---|
| Profil | Name `koolie`, `tools: ["*"]`; ein eigener Agent erbt **keine** Freigabe des eingebauten – ohne `allow` war selbst das Lesen abgewiesen |
| Hook-Werkzeugnamen | `read_file`, `list_directory`, `file_search`, `grep_search`, `execute_pwsh` (Windows), `execute_bash` (Unix, aus dem Programmcode), `fs_write`, `str_replace`, `fs_append`, `delete_file` |
| Pfadfelder der Hook-Eingabe | `path`; bei `delete_file` **`targetFile`** |
| Sperrform des Schutz-Hooks | Exit 2 **mit Grund auf stderr** (`stderr-grund`, D-417) |

## 1b. Der aktive Agent – die Bedingung über der Berechtigungsschicht

🔴 **Die Berechtigungen des Frameworks wirken nur, wenn das Agentenprofil `koolie` der aktive Agent ist.** Der Client hält die Berechtigungsdatei des Arbeitsbereichs je Arbeitsplatz außerhalb des Repositoriums (`QK-1`); versionierbar ist allein ein Agentenprofil. Die Einstellungsdatei `.kiro/settings/cli.json` wählt es als Standard – gemessen: ohne Schalter startet die Sitzung damit, und eine **globale** Einstellung `chat.defaultAgent` unterliegt ihr. Der Client verbietet dem Agenten selbst, in `.kiro/settings/` zu schreiben (`QK-1`).

**Drei Wege führen an ihr vorbei, und keiner meldet sich laut:**

1. **Das Profil fehlt oder ist kein gültiges JSON.** Gemessen: Der Client fällt auf seinen eingebauten Agenten zurück und meldet es nur als Warnung auf stderr (*„agent … has an invalid config, using "default"“*); `.env` war danach lesbar. Sein eigenes Prüfkommando `agent validate` endet auch bei kaputtem JSON mit Exit 0. **Prüfung 96** hält Einstellung und Profil gegeneinander.
2. **Eine Regel nennt eine unbekannte Fähigkeit.** Gemessen: Der Client überspringt genau diese Regel und meldet es nur in seinem Protokoll. Prüfung 96 kennt die Liste der Fähigkeiten.
3. **Die Sitzung wählt einen anderen Agenten** (`--agent`) oder eine andere Engine (`--v2`, `--legacy-ui`). Das ist eine Entscheidung am Arbeitsplatz, und keine Prüfung sieht sie.

**Die Hooks laufen nur in der interaktiven Sitzung.** Gemessen in drei Formen des Betriebs ohne Rückfragen (JSON-Ausgabe, Textausgabe, Terminaloberfläche mit `--no-interactive`): Kein Hook lief. Der Agentenserver aktiviert Hooks nur, wenn der aufrufende Client es meldet, und das tut allein die Terminaloberfläche. **Im Betrieb ohne Rückfragen trägt deshalb allein das Agentenprofil** – dort wird zugleich jede Rückfrage zur Abweisung (`QK-1`).

**Die IDE** liest `.kiro/settings/cli.json` nach dem Programmcode ihrer Agent-Erweiterung nicht als Auswahl ihres Chat-Agenten; dort ist der Agent `koolie` im Chat zu wählen. **An einer IDE-Sitzung ist das nicht gemessen** (`K-162`).

## 2. Fähigkeitsmatrix

Einstufung je Zusage: `[TECHNISCH]` erzwungen · `[TEXTUELL]` nur Anweisung · `[NICHT ABBILDBAR]` kein Mechanismus. Regeln in `../README.md` Abschnitt 4. Gemessen ist an der Kommandozeile; eine Zeile, die die IDE betrifft, sagt es.

### R – Regelladung

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| R1 | Wurzel-Anweisungsdatei wird ungefragt geladen | `AGENTS.md` steht in jeder Sitzung im Kontext | `[TECHNISCH]` | **gemessen** (2026-09-26, Aufschlüsselung der Kontextdateien): auch beim eigenen Agenten, ohne Eintrag in `resources` |
| R2 | Regeldateien mit Ladebedingungen | `.kiro/steering/*.md`, Frontmatter `inclusion` (`always`, `fileMatch`, `manual`, `auto`) | `[TECHNISCH]` | **gemessen:** Dateien ohne Frontmatter laden immer, eine `fileMatch`-Datei nicht ohne passende Datei. `model_decision` bildet auf unbedingtes Laden ab – der Lademodus `auto` wäre genauer, ist aber ungemessen, und eine Regel, die nicht lädt, wäre ein Verlust. ⚠️ **Über das Feld `resources` eines Agentenprofils eingebunden, lädt eine `fileMatch`-Datei ohne Bedingung** – das Profil des Frameworks bindet deshalb nichts ein |
| R3 | Regeln an Dateimuster bindbar | `inclusion: fileMatch` mit `fileMatchPattern` | `[TECHNISCH]` | **gemessen mit Gegenprobe:** eine Sonde mit `**/*.py` stand beim Lesen von `src/calc.py` im Kontext (Ereignis `steering_inclusion`) und wirkte, beim Lesen von `README.md` nicht |
| R4 | Bekanntes Zeichenlimit | **Vorgabe des Frameworks** – höchstens 40.000 Zeichen für das stets Geladene (D-387) | `[TEXTUELL]` | `[EMPF]`. **Für diesen Client ist kein Limit dokumentiert** (`QK-2`). Gemessen ist die feste Last: 8.228 Token für die Wurzel-Anweisung und sechs Regeldateien |
| R5 | Die geladenen Regelquellen sind vollständig aufzählbar | Die Sitzung meldet je Anfrage die Kontextdateien mit Pfad und Tokenzahl | `[TEXTUELL]` | **gemessen:** in der JSON-Ausgabe (`contextUsage.breakdown.contextFiles`) und in der Mitschrift (`steering_inclusion`). Eine Auskunft, keine Schranke |
| R6 | Keine Importe fremder Werkzeugformate | **Kein Schalter.** Der Hersteller dokumentiert keinen Import fremder Formate außer `AGENTS.md`, und das ist hier die Wurzel-Anweisung | `[NICHT ABBILDBAR]` | **Ersatz, geliefert:** die Auskunft in Abschnitt 7 und die Meldung von `install.py` über belegte Quellen im Benutzerprofil (D-411). ⚠️ Das eingebaute Steering des Clients (`architecture-selection`, `quick-spec`, `bug-fix`) steht in jeder Sitzung zur Wahl – gemessen |

### S – Skills

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| S1 | Versionierte Skills im Repository | `.kiro/skills/<name>/SKILL.md` | `[TECHNISCH]` | **gemessen:** zwölf Skills des Frameworks aufgezählt |
| S2 | Gezielter Aufruf | Werkzeug `disclose_context` mit dem Namen des Skills | `[TECHNISCH]` | **gemessen:** freigegeben lädt der Skill, ohne Freigabe weist der Client den Aufruf ab |
| S3 | Werkzeugbeschränkung je Skill | **Kein Feld.** Die Felder des Frameworks (`allowed-tools`, `permissions`, `triggers`) werden angenommen und nicht ausgewertet | `[TEXTUELL]` | **gemessen:** ein Skill mit diesen Feldern lädt. **Was trägt, ist die globale Schicht:** das Agentenprofil und der Schutz-Hook, beide unabhängig vom Skill |
| S4 | Schreibende Skills nur benutzergetriggert | Framework-Konvention; ein Feld zum Ausschluss vom Modellzugriff ist nicht dokumentiert (`QK-4`) | `[TEXTUELL]` | `[EMPF]`. Das Profil gibt alle zwölf Skills frei, wie die Kernquelle |
| S5 | Die geladenen Skills sind aufzählbar | Ereignis `available_commands_update` mit Art je Eintrag | `[TEXTUELL]` | **gemessen:** Skills, eingebautes Steering und Agenten, je mit Herkunft (`bundled` oder Arbeitsbereich) |

### B – Berechtigungen

> **`[TECHNISCH]` heißt in diesem Block:** Die Engine setzt die Regel durch, **solange der Betriebsmodus die Berechtigungsprüfung nicht abschaltet** (D-35) – bei diesem Client der Schalter `--trust-all-tools` und die Freigabe „Trust all" (M2). Für dieses Pack kommt **eine gemessene Bedingung** hinzu: **Das Profil `koolie` muss der aktive Agent sein** (Abschnitt 1b). Fällt der Client auf seinen eingebauten Agenten zurück, trägt von diesem Block nichts. **Die zweite Linie ist der Schutz-Hook – nur in der interaktiven Sitzung.**

Die mit **Kern** markierten Zeilen entsprechen `_core_rules_integrity` im Agentenprofil (D-395); Prüfung 96 hält das Profil gegen die Kernquelle.

| ID | Zusage des Frameworks | Kern | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|---|
| B1 | Berechtigungen versioniert im Repository | ja | Agentenprofil `.kiro/agents/koolie.json`, gewählt durch `.kiro/settings/cli.json` | `[TECHNISCH]`, **bedingt** | **gemessen:** beide Träger liegen im Projekt und wirken ohne Schalter. **Die Bedingung:** der aktive Agent (Abschnitt 1b) – mit fehlendem oder kaputtem Profil stiller Rückfall, gemessen |
| B2 | Verweigern vor Rückfragen vor Erlauben | ja | `deny` vor `ask` vor `allow`, über alle Ebenen | `[TECHNISCH]` | **gemessen:** `deny` auf `.env` schlägt `allow` auf `**`; ein Schreiben unter `arbeit/` fällt in die Rückfrage, obwohl nichts es verbietet |
| B3 | Secret-Dateien per Pfadmuster lesegeschützt | ja | `deny fs_read` mit den Mustern der Kernquelle | `[TECHNISCH]` | **gemessen an einer realen Installation:** `.env` und `sub/.env` abgewiesen, `README.md` gelesen. ⚠️ Ein Muster, das die Kernquelle nicht führt (`id_ecdsa`), ließ das Profil durch – dort sperrte in der interaktiven Sitzung der Schutz-Hook (H2) |
| B4 | Framework- und Overlay-Artefakte schreibgeschützt | ja | `deny fs_write` auf `AGENTS.md`, `.kiro/**` ohne `.kiro/specs/**`, `.koolie/core/**`, `.koolie/project-overlay/**`; jeder Shell-Befehl außer fünf lesenden `git`-Befehlen fragt zurück | `[TECHNISCH]` | **gemessen:** Schreiben in `.koolie/core/` und `.kiro/steering/` abgewiesen (`deny`), in `.kiro/specs/` nur rückgefragt – die Ausnahme greift. ⚠️ **Grenze, nicht gemessen:** ein freigegebener lesender `git`-Befehl mit schreibender Option (`git diff --output=<pfad>`) |
| B5 | CI-, Quality-Gate- und Lockdateien schreibgeschützt | ja | `deny fs_write` mit den Lockmustern und den Schlitzen `<CI_CONFIG_PATHS>`, `<QUALITY_GATE_CONFIG_PATHS>` | `[TECHNISCH]` | **gemessen am Mechanismus** (Pfadmuster im `deny`, B4); die Schlitze füllt der Overlay Owner, die Lockmuster sind nicht einzeln angefahren. Shell wie B4 |
| B6 | Befehle per Muster verweigerbar | ja | `deny shell` mit Präfixmustern (`git push*`) | `[TECHNISCH]` | **gemessen:** `git push origin main` abgewiesen, auch in `git status && git push origin main`. ⚠️ **Grenze wie bei allen Packs:** `git -C . push origin main` trifft das Muster nicht – hier fällt es in die **Rückfrage** und nicht durch, weil kein `allow` es deckt |
| B7 | Schreiboperationen fragen zurück | – | `ask fs_write "**"` | `[TECHNISCH]` | **gemessen:** Schreiben unter `arbeit/` und Löschen (`delete_file`) rückgefragt; ohne Rückfragekanal abgewiesen |
| B8 | Netzwerkzugriff standardmäßig unterbunden | – | `deny web_fetch`/`web_search "*"` und `deny shell` auf `curl`, `wget`, `ssh`, `scp` | `[TECHNISCH]` für die Web-Werkzeuge und diese vier Programme; `[TEXTUELL]` darüber hinaus | **gemessen in einem Baum ohne Regeltext:** mit `deny "*"` fehlen beide Web-Werkzeuge im Werkzeugbestand der Sitzung (15 statt 17). ⚠️ Jedes andere netzfähige Programm fragt zurück (B7), ist aber nicht verboten |
| B9 | Nutzerlokale Konfiguration kann nur verschärfen | – | Keine Rangfolge der Ebenen; die restriktivste Wirkung gewinnt | `[TECHNISCH]` | `[DOK]` **`QK-1`**; gemessen ist die Hälfte zur Wahl des Agenten: die globale Einstellung unterliegt der des Arbeitsbereichs. ⚠️ **Die Sitzung kann Rückfragen überspringen** (M2) |
| B10 | Externer Abruf auf freigegebene Domains beschränkbar | – | Muster je Adresse in `web_fetch` | `[TECHNISCH]` | `[DOK]` **`QK-1`**. Das Framework nutzt die strengste Form – alles verboten (B8, D-59) |

### H – Hooks

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| H1 | Prüfung vor Werkzeugausführung | `PreToolUse` in `.kiro/hooks/koolie.json`, Matcher als regulärer Ausdruck über die Werkzeugnamen | `[TECHNISCH]`, **nur interaktiv** | **gemessen:** Der Hook läuft bei jedem Lese-, Such-, Schreib- und Shell-Aufruf, Eingabe `{session_id, hook_event_name, cwd, tool_name, tool_input}`. Im Betrieb ohne Rückfragen läuft er **nicht** (Abschnitt 1b) |
| H2 | Prüfung kann **blockieren** | Exit 2 **und** ein Grund auf stderr | `[TECHNISCH]`, **nur interaktiv** | 🔴 **Gemessen, und der schwerste Befund des Packs** (D-417): Mit der Standardform (Grund auf stdout, Exit 2) kam der Köderinhalt heraus; der Hook endete nachweislich mit Exit 2. **Mit dem Grund auf stderr wurde derselbe Zugriff in drei von drei Läufen abgewiesen**, `README.md` jeweils gelesen – in einem Baum ohne Regeltext. **Prüfung 86** hält Manifest, Skript und Kommando zusammen |
| H3 | Statusmeldung beim Sitzungsstart | `SessionStart` mit `hook-overlay-status.py` | `[TECHNISCH]`, **nur interaktiv** | **gemessen:** die Meldung steht im Kontext der Sitzung (`HOOK_INSTRUCTION`) und wurde wörtlich zitiert |
| H4 | Eingabeschema und Pfadidentität des Schutz-Hooks | Ereignisprüfung, Pfadfelder `path` und `targetFile`, alle Muster ohne Rücksicht auf Groß-/Kleinschreibung; `hook_fail_closed` steht auf `true`. **Grenze:** Ein Hook prüft **vor** dem Zugriff (D-397) | `[TECHNISCH]` für die Musterprüfung, **mit der Zeitlücke** | **gemessen:** das Schema von `PreToolUse` für alle vier Werkzeugklassen. ⚠️ **Das Feld `targetFile` des Löschwerkzeugs fiel erst im Abnahmelauf auf** – vorher hätte der Hook den Pfad nur als Rohtext geprüft |

### A – Agentenprofile

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| A1 | Rein lesendes Reviewprofil | `.kiro/agents/fw-reviewer.md` mit `tools: [read]`; Unteragenten erben die Regeln der Sitzung | `[TEXTUELL]` | `BELEG OFFEN` (2026-09-26): Die Gestalt folgt `QK-6`; der Start eines Unteragenten (`invoke_sub_agent`) fällt in die Rückfrage und ist ohne Rückfragekanal nicht messbar |
| A2 | Rein lesendes Analyseprofil für Modus M1 | Der Client führt einen Modus `plan` (*„without making any changes"*) | `[TEXTUELL]` | **gemessen ist nur die Existenz** (Modusliste der Sitzung); `BELEG OFFEN` (2026-09-26) für seine Wirkung |

### M – Modi und Sitzungsfreigaben

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| M1 | Standardmodus fragt bei Schreiben und Befehlen zurück | Rückfrageregeln des Profils; in der IDE zusätzlich `Supervised` | `[TECHNISCH]` | **gemessen** an der Kommandozeile (B7); für die IDE `[DOK]` **`QK-1`** |
| M2 | Modus ohne Rückfragen ausschließbar | **Kein Ausschluss.** `--trust-all-tools` und „Trust all" überspringen Rückfragen; ein `deny` gilt weiter | `[TEXTUELL]` | `[DOK]` **`QK-1`**. ⚠️ Ein `deny` bleibt auch dann wirksam – das ist mehr als bei den übrigen Packs, aber keine Sperre des Modus |
| M3 | Freigabe auf die Sitzung begrenzbar | Stufe „This session" bei jeder Rückfrage | `[TECHNISCH]` | `[DOK]` **`QK-1`**; `BELEG OFFEN` (2026-09-26): eine Rückfrage an einen Menschen ist ohne Rückfragekanal nicht messbar |
| M4 | Eigener Planungsmodus für Modus M2 | Modus `spec` mit Ablage im Repositorium (`.kiro/specs/`) und der Regel `16-plan-spezifikation.md` (D-415) | `[TEXTUELL]` | **gemessen mit Gegenprobe:** Mit der Regel legte die Sitzung Anforderungen mit Quelle und offenen Fragen, einen Entwurf mit Zieldateiliste und Kontrollstufe und eine Aufgabenliste mit Status `entwurf` an und setzte nichts um; ohne die Regel griff sie zur Planvorlage des Frameworks und legte keine Spezifikation an. ⚠️ Ihr Schlusssatz *„erfordert keine Freigabe"* widersprach der Regel |
| M6 | Modus mit selbsttätiger Übernahme von Dateiänderungen begrenzbar | IDE: `Autopilot` (`kiroAgent.agentAutonomy`) | `[TEXTUELL]` | `[DOK]` **`QK-1`**; die Regeln des Profils gelten auch dort |
| M7 | Modus, der selbst beurteilt, was sicher ist, begrenzbar | Modus `autonomous` | `[TEXTUELL]` | **gemessen ist nur die Existenz** (Modusliste); `BELEG OFFEN` (2026-09-26) für seine Begrenzbarkeit |

### X – Externe Anbindung

| ID | Zusage des Frameworks | Mechanismus beim Client | Einstufung | Beleg |
|---|---|---|---|---|
| X1 | Keine externe Anbindung ohne Einzelfreigabe | `ask mcp "*"` im Profil; das Framework liefert keinen Server aus | `[TECHNISCH]` | `[DOK]` **`QK-1`**, **`QK-7`**; `BELEG OFFEN` (2026-09-26) für die Wirkung – im Messbaum stand kein Server. ⚠️ Die Benutzerkonfiguration kann Server führen (Abschnitt 7.2) |
| X2 | Art und Ort der Codebasis-Indexierung bekannt | Kein Mechanismus zur Steuerung bekannt | `[NICHT ABBILDBAR]` | `BELEG OFFEN (dauerhaft)` – von außen nicht zu beobachten (`K-20`, D-292). **Kein Ersatz durch das Framework.** Dokumentiert ist die Speicherung der Inhalte je Tarif mit Abschaltung der Weitergabe (`QK-8`) – vor den Messungen abgeschaltet |

## 3. Zusammenfassung der Durchsetzungstiefe

> **Zählregel (normativ für diese Tabelle):** Eine Zeile zählt bei ihrer **schwächsten** Einstufung (D-47). Prüfung 31 rechnet die Summen aus der Matrix nach.

| Klasse | Anzahl | davon Kernzusagen |
|---|---|---|
| `[TECHNISCH]` | **21 von 35** | 6 von 6 (B1 bis B6) |
| `[TEXTUELL]` | **12 von 35** | 0 von 6 |
| `[NICHT ABBILDBAR]` | **2 von 35** | 0 von 6 |

**Belegstand:** `BELEG OFFEN` sagen **A1**, **A2**, **M3**, **M7** und **X1**, dazu **X2** dauerhaft. Die Zeilen der interaktiven Sitzung (H1 bis H3) sind gemessen; die der IDE stehen auf der Dokumentation (`K-162`).

## 4. Kernzusagen ohne technische Durchsetzung

**Keine.** Alle sechs Kernzusagen sind `[TECHNISCH]` – unter der Bedingung des aktiven Agenten (Abschnitt 1b). Sie steht in B1 und in der Vorbemerkung des B-Blocks, weil sie keine Zeile einzeln betrifft, sondern alle zugleich.

## 5. Bekannte Abweichungen im Verhalten

- **Die Berechtigungsdatei ist ein Agentenprofil** (`permissions_format` `kiro-agent`, D-414). Sie ist JSON, führt aber keine Körbe `deny`/`ask`/`allow` aus Regeln der Gestalt `Werkzeug(Muster)`. Deshalb erreichen dieses Pack nicht: **Prüfung 2**, **Prüfung 37**, **Prüfung 42**, **Prüfung 43** und **Prüfung 54**; nur zum Teil **Prüfung 59** und **Prüfung 89** (ihr Gegenstand (c), die Pfade des Overlays im `deny`, entfällt). An ihre Stelle tritt die Prüfung des Agentenprofils (Abschnitt 1b). Der Prüfapparat hält diese Liste gegen seine eigene Liste der formatgebundenen Prüfungen.
- **Ein eigener Agent erbt keine Freigaben.** Ohne `allow` wird selbst das Lesen im Arbeitsbereich abgewiesen – das Profil führt die Freigaben der Kernquelle vollständig.
- **Die Hooks laufen nur interaktiv**, und der Schutz-Hook braucht seinen Grund auf stderr (Abschnitt 1b, H2).
- **Das Schreibverbot auf die Laufzeitschicht nimmt `.kiro/specs/` aus** (D-415) – dort liegt das Planartefakt. Der Schutz-Hook führt dieselbe Ausnahme.
- **Ein Befehl, den ein Präfixmuster nicht trifft, fällt in die Rückfrage** und nicht durch – anders als bei Packs, deren `allow` breiter ist.
- **Die Dokumentation widerspricht sich an vier Stellen** (Anhang 31.4.4); zwei hat die Messung entschieden, eine hat sie widerlegt.

## 6. Installation und Prüfung

```text
python .koolie/core/install.py --target /pfad/zum/projekt --client kiro
python .koolie/core/tests/scripts/validate-framework.py
```

🔴 **Danach:** `kiro-cli` im Projektverzeichnis starten – nur dort gilt `.kiro/settings/cli.json`. Nicht mit `--agent`, `--v2` oder `--legacy-ui` starten. In der IDE den Agenten `koolie` im Chat wählen. `install.py` nennt diese Schritte nach der Installation; nach jeder Hebung nennt es, dass Profil und Einstellung Saat sind und nicht angefasst werden.

Vor der ersten produktiven Nutzung sind die Basistests des Testkatalogs gegen diesen Client zu fahren und zu protokollieren.

## 7. Anweisungs- und Konfigurationsquellen außerhalb des Projekts

**Pflichtabschnitt** (D-34). Solche Quellen haben nach Regel 2.6 der Prioritätshierarchie **keine Ebene**.

**Erhebungsstand: 2026-09-26**, Kommandozeile `2.24.1`, erhoben mit der Herstellerdokumentation (`QK-1`, `QK-2`, `QK-6`, `QK-7`), der Modus- und Befehlsliste der Sitzung und `install.py` (`import_channels_report`).

### 7.1 Anweisungsquellen

| Quelle | Ladebedingung | Belegstatus | Maßnahme des Frameworks |
|---|---|---|---|
| `~/.kiro/steering/` (auch `AGENTS.md` dort) | in jeder Sitzung neben dem Steering des Projekts | `[DOK]` `QK-2` | Auskunft; `install.py` meldet sie, wenn belegt |
| `~/.kiro/skills/` | in jeder Sitzung verfügbar | `[DOK]` `QK-4` | Auskunft; `install.py` meldet sie |
| `~/.kiro/agents/` | wählbar mit `--agent`; bei gleichem Namen gewinnt das Profil des Arbeitsbereichs | `[DOK]` `QK-6` | Auskunft; `install.py` meldet sie |
| Eingebautes Steering und eingebaute Agenten des Clients | in jeder Sitzung zur Wahl | **gemessen** (Befehlsliste: `architecture-selection`, `quick-spec`, `bug-fix`, `general-task-execution`, `context-gatherer`) | **keine** – nicht abschaltbar, aber aufgezählt (S5) |

### 7.2 Konfigurationsquellen

| Quelle | Wirkung | Belegstatus |
|---|---|---|
| `~/.kiro/settings/permissions.yaml` und `~/.kiro/workspace-roots/<hash>/permissions.yaml` | Regeln des Arbeitsplatzes; ein `deny` dort gilt zusätzlich, ein `allow` hebt kein `deny` des Profils auf | `[DOK]` `QK-1` |
| `~/.kiro/settings/cli.json` | globale Einstellungen; `chat.defaultAgent` dort unterliegt der Datei des Arbeitsbereichs | **gemessen** (Wiederherstellung der Datei per Bytevergleich geprüft) |
| `~/.kiro/settings/mcp.json` | MCP-Server des Arbeitsplatzes | `[DOK]` `QK-7` |
| `managed-settings.json` | Vorgaben der Organisation (nur `deny` und `ask`) | `[DOK]` `QK-1` |

### 7.3 Was dieser Abschnitt nicht leistet

**Eine Auskunft ist keine Schranke**, und ein **Abwesenheitsbeleg altert**. Prüfung 19 prüft die Anwesenheit dieser Auskunft, nicht ihre Richtigkeit.

## 8. Änderungsverlauf

| Version | Datum | Änderung | Autor (Rolle) |
|---|---|---|---|
| 0.1.0 | 2026-09-26 | **Angelegt (`CR-2026-150`, D-414 bis D-417).** Das vierte Client Pack, gebaut mit Zugang zum Client statt nur aus der Dokumentation. **Die Berechtigungen stehen in einem Agentenprofil**, weil die Datei des Arbeitsbereichs außerhalb des Repositoriums liegt; **die Spezifikationen des Clients sind das Planartefakt** (D-415); **der Schutz-Hook sperrte mit der Standardform nichts** und führt eine eigene Sperrform (D-417). **Prüfung 96** neu | `<FRAMEWORK_OWNER>` |

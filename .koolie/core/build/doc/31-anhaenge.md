# 31 Anhänge

## 31.1 Inventar des Referenz-Repositorys

Gezählt beim Bau dieses Dokuments aus dem Versionsbestand von Release {{VERSION}}: **{{ZAHL:*}} versionierte Dateien im Kern**. Die vollständige Struktur mit Erläuterung steht in Kap. 15.2; hier nur die Größenordnung je Bereich.

| Bereich | Dateien | Inhalt |
|---|---|---|
| direkt im Kernverzeichnis | {{ZAHL:.}} | `install.py`, `install_dialog.py`, `clientmap.py`, `VERSION`, `CHANGELOG.md`, `OWNERS.md`, Lizenz und Lizenzhinweis |
| `clients/` | {{ZAHL:clients/}} | Abbildungsschicht: {{ZAHL:clients/*/manifest.json}} Client Packs, Regeln der Schicht, Vorlage für ein weiteres Pack |
| `framework/` | {{ZAHL:framework/}} | {{ZAHL:framework/core/*.md}} Core-Module, Laufzeitfassung, {{ZAHL:framework/skills/*/SKILL.md}} Referenz-Skills, Role Packs, Tech-Pack-Vorlage, Organisationsvorgaben, Overlay-Muster |
| `templates/` | {{ZAHL:templates/}} | Project-Overlay-Saat, Regelvorlagen, Skill-Vorlage |
| `build/` | {{ZAHL:build/}} | **{{ZAHL:build/doc/*.md}} Kapitelquellen**, Assemblierungs- und DOCX-Skript, Referenzdokument, README |
| `prompts/` · `checklists/` · `decision-trees/` | {{ZAHL:prompts/,checklists/,decision-trees/}} | {{ZAHL:prompts/[0-9]*.md}} Prompt-Vorlagen, {{ZAHL:checklists/[0-9]*.md}} Checklisten, {{ZAHL:decision-trees/[0-9]*.md}} Entscheidungsbäume, je README |
| `governance/` | {{ZAHL:governance/}} | Decision Log, RACI, Hierarchie, Prozesse – und **{{ZAHL:governance/change-requests/}} Änderungsanträge** |
| `tests/` | {{ZAHL:tests/}} | Testkatalog, Prüf- und Hook-Skripte, **{{ZAHL:tests/protocols/}} Protokolle**, Erhebungsapparat |
| `onboarding/` · `examples/` · `pilot/` · `docs/` | {{ZAHL:onboarding/,examples/,pilot/,docs/}} | Onboarding-Paket, synthetische Beispiele, Pilotkonzept, Leitfäden und Register |

⚠️ **Die größten Posten sind Aufzeichnung, nicht Regelwerk.** {{ZAHL:governance/change-requests/,tests/protocols/,tests/erhebungen/,build/}} der {{ZAHL:*}} Dateien bilden die Nachweisschicht – Änderungsanträge, Protokolle, Erhebungen und `build/`. Sie werden mit dem Kern ausgeliefert, weil ein Beleg ohne seinen Träger keiner ist; für die **Nutzung** des Frameworks braucht sie niemand. Ein Projekt kann sie weglassen: `install.py --target <projekt> --lieferumfang nutzung` liefert den Kern ohne sie (D-367).

**Was daraus in ein Projekt installiert wird:** **{{ZAHL:installiert}} Dateien** beim Client Pack dieses Baus (`{{CLIENT}}`) – Wurzel-Anweisungsdatei, Laufzeitschicht und Project Overlay, gezählt an derselben Referenzinstallation, aus der die eingebetteten Laufzeitdateien dieses Dokuments stammen. Der Kern selbst kommt hinzu.

Die Zahlen dieses Abschnitts setzt `assemble.py` beim Bau ein (D-377); in der Kapitelquelle stehen Direktiven statt Zahlen.

## 31.2 Laufzeitglossar

Der Kern nennt die Bestandteile der Laufzeitschicht mit Begriffen, nicht mit Pfaden. Die Abbildung auf die Pfade eines konkreten Client Packs steht hier:

{{EMBED-RAW:.koolie/core/docs/RUNTIME_GLOSSARY.md:2}}
## 31.3 Platzhalterregister

{{EMBED-RAW:.koolie/core/docs/PLACEHOLDER_REGISTRY.md:2}}

## 31.4 Quellen der Produktdokumentation und Belegzuordnung

Die Quellen belegen die als `[DOK]` gekennzeichneten Aussagen; der Framework Owner hält diese Liste im Rahmen der Produktbeobachtung aktuell (FW-AK-01).

Sie ist **je Client Pack** geführt, weil eine Aussage über einen Client an dessen Dokumentation hängt und an keiner anderen und weil die Listen verschiedene Recherchestände haben. Die Kennungen tragen das Präfix des Packs (`QD-` für `devin-desktop`, `QC-` für `claude-code`, `QK-` für `kiro`), damit sie nicht mit den Qualitätsregeln des Frameworks (`Q1`, `Q8` …) verwechselt werden. Das dritte Pack, `openai-codex`, führt keine `[DOK]`-Zeile – seine Belegspalte nennt Messungen – und hat deshalb keine Liste in diesem Anhang; `FW-AK-01` ist für dieses Pack noch nicht gefahren (Kopf des Packs, Zeile „Stand der Produktbeobachtung").

Die **maßgebliche Zuordnung** steht in der Fähigkeitsmatrix des jeweiligen Packs (Kap. 15.1 beziehungsweise Kap. 7a): Dort nennt der Belegkopf jeder mit `[DOK]` belegten Zeile die Quellenkennung dieser Liste, Verweisbelege (*„wie B3"*) aufgelöst; Prüfung 73 setzt das durch (D-263 bis D-266). Die Kennung ist die verbindliche Form, weil allein sie gegen diese Liste gehalten werden kann; ein Seitenpfad darf danebenstehen. Nachgetragene Zuordnungen tragen den Zusatz `(Zuordnung K-62)`: gewonnen aus dem Bestand am 22.09.2026, nicht aus einem zweiten Abruf – der Recherchestand der Seiten bleibt der vom 18.09.2026 (D-263). Diese Liste sagt, welche Seite wofür herangezogen wurde und **wann sie abgerufen worden ist** – die Angabe, die eine Wiederholungsprüfung braucht.

⚠️ **Eine Zeile ist ausdrücklich ohne Zuordnung:** `M3` des Packs `claude-code` („Freigabe auf die Sitzung begrenzbar") – keine der sechs Seiten `QC-1` bis `QC-6` führt die Sitzungs-Grant-Stufen, während sie beim Schwesterpack in `QD-11` stehen. Die Zeile sagt `QUELLE NICHT ZUGEORDNET`, und Prüfung 73 führt die zugelassenen Lücken als deklarierte Menge; eine geratene Zuordnung sähe wie ein Beleg aus (D-156). Diese Zeile ist der erste gezielte Auftrag des nächsten Durchgangs von `FW-AK-01`.

### 31.4.1 Client Pack `devin-desktop`

Recherchestand: 01.–02.09.2026, gegen Devin Desktop 3.8.20 (QD-4). Ergänzt am 11.09.2026 gegen Devin Desktop 3.9.19 / CLI 3000.10.21 (Erhebungen zu K-21 bis K-27). Vollständig abgeglichen am 18.09.2026 gegen den Produktstand 3.10.31 (`FW-AK-01`, `.koolie/core/tests/protocols/2026-09-18-FW-AK-01.md`). Neun Zeilen der Fähigkeitsmatrix sind zusätzlich in einer Sitzung an einer laufenden Installation beobachtet (H1, H2, R5, R6, S5, S3, B3, B10 und A1); bei S3 und B10 hat die Messung die zuvor vorgesehene Einstufung widerlegt, und die Matrix führt das in den Zeilen. Eine Zeile sagt dauerhaft `BELEG OFFEN`: `X2` – was ein Client indexiert und wohin er es gibt, ist von außen nicht zu beobachten (D-292).

⚠️ **Drei Quellen belegen einen Agenten, den der Hersteller entfernt hat.** Der Changelog sagt zu 3.9.19 (08.09.2026): *„Cascade has been removed. Devin Local is now the only agent available in Devin Desktop."* QD-5, QD-7 und QD-8 liegen unter `desktop/cascade/` und sprechen weiter im Präsens von diesem Agenten; QD-2 sagt noch, er bleibe *„through July"* verfügbar. Die Seiten sind erreichbar und inhaltlich unverändert – veraltet ist, wofür sie taugen. Deshalb stützt sich Zeile R1 des Packs auf QD-6 statt auf QD-5, und die Zeichenzahlen aus QD-7 gelten als Vorgabe des Frameworks und nicht als Produkteigenschaft (Zeile R4).

⚠️ **Eine Aussage der Liste ist innerhalb der verbindlichen Zielspanne des Packs widerlegt.** QD-12 sagt *„Organization-level (enterprise) settings can never be overridden by project or user config"*; der Changelog weist zu 3.10.31 (16.09.2026) aus: *„Restricted Mode blocks restricted workspace settings written in nested object form, not just the dotted form (CVE-2026-81376)."* Bis einschließlich 3.10.27 hing die Durchsetzung also an der **Schreibweise**. Die Zielspanne `3.9.x` liegt vollständig davor; Zeile M2 des Packs trägt den Nachtrag.

| Nr. | Quelle | Belegt im Framework insbesondere |
|---|---|---|
| QD-1 | devin.ai/blog/windsurf-is-now-devin-desktop | Rebranding zum 02.06.2026; Devin Local ersetzt Cascade; Übergangsfrist für Cascade; Agent Command Center, Spaces, ACP |
| QD-2 | docs.devin.ai/desktop/devin-desktop-faq | `.devin/` als Primär-, `.windsurf/` als Legacy-Pfad; `.windsurfrules`; Systempfade für organisationsweite Regeln; Legacy-MCP-Pfad; Plankontinuität |
| QD-3 | docs.devin.ai/desktop/devin-local | Modi Normal/Plan/Ask; Berechtigungsmodell deny/ask/allow mit Geltungsbereichen; MCP-Bestätigung als Standard; Subagenten (Preview) und Quick Review; keine Memories/Workflows in Devin Local; Migrationsassistent; Enterprise-Einstellungen (Sandbox-Erzwingung, Domain-Listen); Konfigurationspfade |
| QD-4 | docs.devin.ai/desktop/changelog | Version 3.8.20 vom 21.08.2026; Komposition der Berechtigungsebenen mit deny-Vorrang; `sandbox.excluded`; persistente Plan-Dateien; Subagenten-Dateiformen; Skill-Berechtigungen bei Auto-Genehmigungen |
| QD-5 | docs.devin.ai/desktop/cascade/agents-md | AGENTS.md im Root always-on; Unterverzeichnisse als automatische Glob-Regeln; Einspeisung in die Regel-Engine; Namensvarianten |
| QD-6 | docs.devin.ai/cli/extensibility/rules | Regeldateien und -orte (AGENTS.md, AGENTS.local.md, `.devin/rules/*.md`, global), Frontmatter `description`/`trigger`/`globs` mit Werten, Präzedenzen, Kompatibilitätspfade |
| QD-7 | docs.devin.ai/desktop/cascade/memories | Aktivierungsmodi der Regeln; Zeichenlimits 6.000/12.000 (Cascade-Kontext); Memories nur für Cascade |
| QD-8 | docs.devin.ai/desktop/cascade/workflows | Workflows nur für Cascade; Migration zu Skills; Limits |
| QD-9 | docs.devin.ai/product-guides/skills | SKILL.md-Format; Suchpfade einschließlich `.agents/skills/` (empfohlen) und `.devin/skills/`; `triggers`; `@skills:`-Erwähnung; Argument-Substitution; eine aktive Skill-Grenze |
| QD-10 | docs.devin.ai/cli/extensibility/skills/creating-skills | Projekt- und globale Skill-Pfade; Frontmatter-Felder inkl. `allowed-tools`, `permissions` (additiv), `argument-hint`, `model`, `subagent`, `agent`; Aufruf `/skill-name` |
| QD-11 | docs.devin.ai/cli/reference/permissions | Matcher `Read()`, `Write()`, `Exec()`, `Fetch()`, Tool- und MCP-Matcher; deny > ask > allow; Permission-Modi; Ebenen-Präzedenz; Sitzungs-Grant-Stufen |
| QD-12 | docs.devin.ai/cli/extensibility/configuration | `config.json`-Scopes und -Schlüssel; `mcp_config.json`/`.local`; `read_config_from`; Enterprise unüberschreibbar |
| QD-13 | docs.devin.ai/cli/extensibility/hooks/overview | `hooks.v1.json`; Ereignisse; Blockierung per Exit-Code 2/`decision: block`; `additionalContext`; `DEVIN_PROJECT_DIR` |
| QD-14 | docs.devin.ai/de/cli/subagents | Subagent-Dateiformen und Frontmatter; eingebaute Profile; Vordergrund-/Hintergrundrechte |
| QD-15 | docs.devin.ai/cli/sandbox | Sandbox-Ableitung aus Berechtigungen; Domainfilter und Modi; `sandbox.excluded`; Plattformgrenzen (kein Windows); Instabilität des Netzfilters |
| QD-16 | docs.devin.ai/cli/enterprise/team-settings | Team-Kontrollen: Modell-Allowlist, Websuche standardmäßig aus, MCP-Kontrollen und Registry-Erzwingung, unüberschreibbare Terminal-Permissions, Sandbox-Erzwingung, Attribution-Filter |
| QD-17 | docs.devin.ai/admin/security | Training-Opt-out auf kostenpflichtigen Plänen; Zero Data Retention nach Opt-out; Teams-Opt-out nur durch Admin; Enterprise nur mit schriftlicher Zustimmung; SOC 2 Type II; Verschlüsselung |

### 31.4.2 Client Pack `claude-code`

Recherchestand: 10.09.2026, gegen Clientversion 2.1.267. Erhoben im Rahmen von AP2 (`.koolie/core/tests/protocols/2026-09-10-AP2-claude-code.md`); die Seitenangaben sind gegenüber dem Protokoll um die genauen Pfade ergänzt. **Abgeglichen am 18.09.2026 gegen 2.1.275**, dazu der Changelog der Stände 2.1.268 bis 2.1.275 (`FW-AK-01`, `.koolie/core/tests/protocols/2026-09-18-FW-AK-01.md`).

Die Liste führt auch die Hook-Seite `QC-6`, weil das Pack drei Hook-Zusagen trägt (H1, H2, H3) – so wie das Schwesterpack für denselben Gegenstand QD-13 führt (D-159).

| Nr. | Quelle | Belegt im Framework insbesondere |
|---|---|---|
| QC-1 | code.claude.com/docs/en/memory | Regelablage `.claude/rules/*.md`, rekursiv gefunden; Frontmatter-Feld `paths` mit Glob-Mustern, mehreren Mustern und Klammer-Expansion samt Budget (1.000 expandierte Muster, 4 MiB); eine Regel **ohne** `paths` lädt unbedingt und ohne Import; Ladeordnung und `@pfad`-Importe der Wurzel-Anweisungsdatei; Grenze 4 MiB je Anweisungsdatei und Empfehlung 200 Zeilen; Entfernen von Block-Kommentaren vor dem Einspeisen (für `CLAUDE.md` dokumentiert); `claudeMdExcludes`. **Neu mit dem Abgleich vom 18.09.2026:** die **selbstgeschriebene** Anweisungsquelle des Clients (*„Auto memory is on by default"*) mit Ablage außerhalb des Projekts und Ladung des Index in jede Sitzung – das Framework schaltet sie ab (D-154); `/context` als Auskunft über die tatsächlich geladenen Anweisungsdateien |
| QC-2 | code.claude.com/docs/en/permissions | Pfadregeln werden nur für `Read` und `Edit` ausgewertet, für andere Werkzeuge angenommen, nie konsultiert und beim Sitzungsstart als Warnung gemeldet; `deny` vor `ask` vor `allow` und die Unaufhebbarkeit einer Verweigerung über alle Ebenen; gitignore-Mustersemantik samt Normalisierung auf POSIX-Form unter Windows; Präfixsemantik der Befehlsregeln und ihre Grenze (`git -C . push` trifft nicht); `disableBypassPermissionsMode` und `disableAutoMode`; Vorrang eines mit Exit-Code 2 blockierenden Hooks **vor** den Berechtigungsregeln |
| QC-3 | code.claude.com/docs/en/skills | `SKILL.md`-Frontmatter (`name`, `description`, `allowed-tools`, `disable-model-invocation`, `user-invocable`, `paths`, `model`); Wirkung von `disable-model-invocation: true` – das Modell kann den Skill nicht selbst laden, und seine Beschreibung kommt gar nicht erst in den Kontext; Suchpfade der Skill-Ablage; Aufruf über `/name`. **Neu mit dem Abgleich vom 18.09.2026:** die **Kontoquelle** – der Client lädt die im Konto eingeschalteten Skills nach `~/.claude/skills/synced/`, *„This is enabled by default"*, mit Abgleich etwa alle zehn Minuten **während** der Sitzung; dazu das Vorladen von Skills in ein Unteragentenprofil, das `disable-model-invocation: true` ebenfalls verhindert |
| QC-4 | code.claude.com/docs/en/sub-agents | Subagentenprofile unter `.claude/agents/`; Frontmatter `tools` (Allowlist) und `disallowedTools` (Denylist) mit dokumentierter Verarbeitungsreihenfolge; die Beschränkung wirkt technisch; ein Profil, dessen `tools`-Liste sich zu keinem Werkzeug auflöst, wird gar nicht erst gestartet; weitere Felder, darunter `permissionMode` |
| QC-5 | code.claude.com/docs/en/settings | Ablageorte und Rangfolge der Einstellungsdateien: verwaltet → Kommandozeile → `settings.local.json` → `settings.json` → Nutzer; `permissions`, `hooks`, `env` und `defaultMode` in derselben Datei; verwaltete Einstellungen sind bis auf wenige benannte Ausnahmen unüberschreibbar. **Neu mit dem Abgleich vom 18.09.2026:** die Tabelle der Vorrangausnahmen – für einige Schlüssel gilt der **strengere** Wert aus einer Ebene, die sonst nicht überschreiben dürfte, und für `syncClaudeAiSkills` beziehungsweise `syncClaudeAiPlugins` ausdrücklich *„a `false` in `.claude/settings.json` is ignored"*. Das ist die Datei, die das Client Pack ausliefert (`K-63`) |
| QC-6 | code.claude.com/docs/en/hooks | Ereignisse der Hook-Schicht und ihre Matcher; `InstructionsLoaded` mit dem **Ladegrund** als Matcher (`session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`) – der dokumentierte technische Aufzählungsweg für Zeile R5 (D-158). Abgerufen am 18.09.2026 |
| QC-7 | code.claude.com/docs/en/settings-reference | Abschnitt „Git and attribution“: `attribution` als Objekt mit `commit` und `pr` (Zeichenketten; leer blendet aus) und `sessionUrl` (Boolean); Standard ist ein Trailer `Co-Authored-By` mit einer Adresse des Herstellers; **die Kurzform `attribution: false` erst ab 2.1.281 – ältere Stände verwerfen die ganze Einstellungsdatei**; `includeCoAuthoredBy` veraltet seit 2.0.62; eigene Anweisungen zur Attribution haben Vorrang, außer in verwalteten Einstellungen (D-433). Abgerufen am 26.09.2026 |

### 31.4.3 Was die Liste über sich selbst sagt

Beide Teile sind am 18.09.2026 gegen eine benannte Produktversion und einen gesichteten Changelog abgeglichen worden (`FW-AK-01`, `CR-2026-087`). Von 22 abgerufenen Quellen trugen zwölf ihren zugeschriebenen Beleg unverändert, zehn nicht – geändert, im Gegenstand entfallen oder vom Produkt-Changelog widerlegt. Die Befunde daraus stehen im Protokoll `.koolie/core/tests/protocols/2026-09-18-FW-AK-01.md`.

Zwei Regeln gelten für diese Liste: Eine Quelle ohne Abrufdatum ist kein Beleg, sondern eine Behauptung mit Fußnote – Produktdokumentation ändert sich, und ohne Datum lässt sich nicht sagen, ob eine Aussage noch trägt (dieselbe Überlegung wie D-25 für Versionsangaben). Und ein Abrufdatum nützt nichts, wenn nicht dabeisteht, *welche Zusage* die Seite trägt: Ohne Zuordnung je Zeile ist jede Wiederholungsprüfung so teuer wie die erste, weil jede Seite neu gelesen werden muss (D-156, Prüfung 73).


### 31.4.4 Client Pack `kiro`

Recherchestand: 26.09.2026, gegen Kiro CLI 2.24.1 (Engine V3) und Kiro IDE 1.1.70 (`CR-2026-150`, `.koolie/core/tests/protocols/2026-09-26-bau-kiro.md`). Anders als bei den beiden älteren Packs ist die Liste **nicht die Grundlage der meisten Zeilen**: Die Zeilen, die die Kommandozeile betreffen, sind am Client gemessen; die Liste belegt, was nur die IDE betrifft oder nicht gemessen ist. Abgerufen jeweils in der Markdown-Fassung der Seite (`<Seite>.md`).

⚠️ **Die Dokumentation widerspricht sich an vier Stellen, und zwei davon hat die Messung entschieden:** Der Auslöser heißt `UserPromptSubmit`, nicht `PromptSubmit` (QK-3), und der Matcher eines Hooks ist ein regulärer Ausdruck, in dem `*` allein nicht kompiliert (QK-3). **Und eine Aussage ist durch Messung widerlegt:** Laut QK-3 sperrt ein Kommando-Hook mit Exit-Code 2; gemessen sperrt er **nur mit einem Grund auf stderr** (D-417).

| Nr. | Quelle | Belegt im Framework insbesondere |
|---|---|---|
| QK-1 | kiro.dev/docs/permissions | Fähigkeitsregeln `{capability, match, exclude, effect}`, `deny` vor `ask` vor `allow` ohne Vorrang zwischen den Ebenen; die Datei des Arbeitsbereichs liegt **außerhalb** des Repositoriums (`~/.kiro/workspace-roots/<hash>/`); feste Regeln des Clients (Schreibverbot auf `.kiro/settings/`, Rückfrage für `.kiro/agents/**` und `.kiro/hooks/**`); im Betrieb ohne Rückfragen wird jede Rückfrage zur Abweisung; Einstellung `kiroAgent.agentAutonomy` der IDE |
| QK-2 | kiro.dev/docs/steering | Ablage `.kiro/steering/*.md`, Lademodi `always`, `fileMatch` mit `fileMatchPattern`, `manual`, `auto`; globales Steering unter `~/.kiro/steering/`; `AGENTS.md` im Arbeitsbereich und in Unterverzeichnissen |
| QK-3 | kiro.dev/docs/hooks, kiro.dev/docs/hooks/types, kiro.dev/docs/hooks/actions | Hook-Dateien `.kiro/hooks/*.json` mit `version: v1`; Auslöser je Oberfläche (Datei-Auslöser nur in der IDE); sperrende Auslöser; Exit-Code-Verhalten je Oberfläche |
| QK-4 | kiro.dev/docs/skills | `SKILL.md` im offenen Format, Ablagen `.kiro/skills/` und `~/.kiro/skills/`, Felder `name`, `description`, `license`, `compatibility`, `metadata` |
| QK-5 | kiro.dev/docs/specs | Spezifikationen unter `.kiro/specs/<name>/` (`requirements.md`, `design.md`, `tasks.md`), Freigabepunkte je Phase |
| QK-6 | kiro.dev/docs/custom-agents/configuration-reference | Agentenprofil: Felder `tools`, `allowedTools`, `permissions`, `resources`, `hooks` (nur Kommandozeile), Markdown-Form mit Frontmatter; Unteragenten erben die Regeln der Sitzung |
| QK-7 | kiro.dev/docs/mcp/configuration | `.kiro/settings/mcp.json` und `~/.kiro/settings/mcp.json`, `autoApprove`, `disabledTools` |
| QK-8 | kiro.dev/docs/privacy-and-security/data-protection | Speicherung und Nutzung der Inhalte je Tarif, Abschaltung der Weitergabe, Verarbeitung in der Region |
| QK-9 | kiro.dev/docs/kiroignore | `.kiroignore` – in der IDE für alle Werkzeuge, in der Kommandozeile nur für Suchergebnisse |

## 31.5 Konsolidierter Verifikationsbedarf

Der **maßgebliche** Verifikationsbedarf steht in der Fähigkeitsmatrix des jeweiligen Client Packs: Jede Zeile ohne Beleg sagt dort `BELEG OFFEN` mit Grund und Datum, jede Matrix nennt ihren Belegstand selbst, und sie wird mit dem Pack gepflegt statt in diesem Anhang. Die Belegstände der Packs messen Verschiedenes: Bei `claude-code` ist der Beleg überwiegend ein Dokumentenabgleich gegen eine benannte Clientversion, und **ein Dokumentenabgleich belegt `[DOK]`, nicht `[TECHNISCH]` im Sinne einer beobachteten Wirkung**. Bei `devin-desktop` tritt zum Dokumentenabgleich eine laufende Sitzung hinzu; `openai-codex` belegt ohne `[DOK]`, allein über Messungen. Eingebettet sind die Matrizen von `devin-desktop` (Kap. 15.1) und `claude-code` (Kap. 7a).

Die folgende Liste ergänzt sie um Punkte, die keiner einzelnen Zusage der Matrix zugeordnet sind, sondern das Zusammenspiel betreffen. Sie gilt für das Client Pack `devin-desktop`; Prüfweg ist Roadmap-AP2, Testklasse AK:

| Nr. | Prüfpunkt | Betroffene Stellen |
|---|---|---|
| ~~V1~~ | **Geschlossen mit 0.26.0, Ergebnis „nicht dokumentiert".** Der Abgleich am 2026-09-11 gegen Devin Desktop 3.9.19 (`cli/extensibility/rules`) nennt für Regeldateien **keine** Zeichen- oder Größengrenze – weder für `AGENTS.md` noch für `.devin/rules/*.md` noch für globale Regeln; zweite unabhängige Bestätigung in derselben Sitzung (ERH-10). Die Zahlen 6.000/12.000 stammen aus der Cascade-Dokumentation (QD-7) und bleiben als **Vorgabe des Frameworks** in Kraft: Zeile R4 führt sie seit 0.26.0 als `[TEXTUELL]` (`CR-2026-027`). Wird die Grenze später doch dokumentiert, ist V1 erneut zu öffnen; K-19 bleibt offen | Laufzeit-README des Packs (Abschnitt „Regelablage"), AGENTS.md-Größenbudget, Validator-Grenzen |
| V2 | Exakte Schemadetails von `.devin/config.json` (Schlüsselstruktur, Glob-/Präfix-Semantik, Wildcard `Fetch(*)`, Kommentarfelder-Toleranz) | `.devin/config.json`, FW-CORE-03 Abschnitt 4 |
| ~~V3~~ | **Erledigt mit 0.25.0.** Das Hook-Eingabeschema ist in einer Sitzung erhoben: `hook_event_name`, `tool_name`, `tool_input`, `session_id`, `prompt_id` und ein in der Dokumentation nicht genanntes `tool_use_id`; Werkzeugnamen `read` und `exec`; Blockieren über Exit 2. Die Umstellung auf fail-closed ist mit `CR-2026-026` je Pack entschieden. **Dabei fiel auf, dass die Hook-Datei des Packs gar nicht gelesen wurde** (`AP2-DD-10`, `CR-2026-029`) | `.koolie/core/tests/protocols/2026-09-11-AP2-devin-desktop.md` |
| V4 | Skill-Discovery über `.agents/skills/` durch Devin Local; Verhalten der `@skills:`-Erwähnung im Desktop; Grenze „ein Skill aktiv" | FW-CORE-08 Abschnitt 2, K-12 |
| V5 | Toleranz unbekannter Frontmatter-Schlüssel in SKILL.md (D-08 bleibt unabhängig davon bestehen) | Skill-Standard, K-18 |
| V6 | Struktur von `.devin/mcp_config.json` im Desktop und Status des Legacy-Pfads `~/.codeium/mcp_config.json` | `.devin/mcp_config.json.example` |
| V7 | Codebasis-Indexierung: Art, Speicherort, Abschaltbarkeit (Datenschutzmodell Abschnitt 1) | FW-CORE-02, K-20 |
| V8 | Reichweite geteilten Kontexts in Spaces | FW-CORE-02 Abschnitt 3.9 |
| V9 | Wirkung additiver Skill-`permissions` gegenüber Sitzungs- und Projektregeln in Devin Local | Skills mit `permissions`, u. a. `fw-mr-description` |
| V10 | Zeichen-/Größenbudget und Ladeverhalten der always-on-Summe (AGENTS.md + `00-*` + `20-*`) im realen Systemprompt | Laufzeitschicht gesamt |

## 31.6 Beispielartefakte (synthetisch)

Im Repository unter `.koolie/core/examples/`: ausgefüllte Overlay-Laufzeitfassung, vollständiger Ergebnisbericht und Merge-Request-Beschreibung mit Nutzungsvermerk – alle ausdrücklich synthetisch und mit erfundenen Bezeichnern (siehe `.koolie/core/examples/README.md`).

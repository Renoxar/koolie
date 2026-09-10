# 31 Anhänge

## 31.1 Inventar des Referenz-Repositorys

Stand Release 0.9.0, 233 versionierte Dateien im Kern. Die vollständige Struktur mit Erläuterung steht in Kap. 15.2; hier nur die Größenordnung je Bereich.

| Bereich | Dateien | Inhalt |
|---|---|---|
| direkt im Kernverzeichnis | 5 | `install.py`, `clientmap.py`, `VERSION`, `CHANGELOG.md`, `OWNERS.md` |
| `clients/` | 10 | Abbildungsschicht: zwei Client Packs zu je vier Dateien, Regeln der Schicht, Vorlage |
| `framework/` | 83 | Core-Module, Laufzeitfassung, 12 Referenz-Skills, Role- und Tech-Packs, Organisationsvorgaben |
| `templates/` | 23 | Project-Overlay-Saat, Regelvorlagen, Skill-Vorlage |
| `build/` | 37 | 33 Kapitelquellen, Assemblierungs- und DOCX-Skript, Referenzdokument, README |
| `prompts/` · `checklists/` · `decision-trees/` | 32 | 12 Prompt-Vorlagen, 11 Checklisten, 6 Entscheidungsbäume, je README |
| `governance/` | 18 | Decision Log, RACI, Hierarchie, Prozesse, Änderungsanträge |
| `onboarding/` · `examples/` · `pilot/` · `docs/` · `tests/` | 25 | Onboarding-Paket, synthetische Beispiele, Pilotkonzept, Leitfäden, Testkatalog mit Skripten und Protokollen |

**Was daraus in ein Projekt installiert wird:** 80 Dateien beim Client Pack `devin-desktop`, 79 bei `claude-code` – Wurzel-Anweisungsdatei, Laufzeitschicht und Project Overlay. Der Unterschied liegt allein darin, dass ein Client keine eigene Hook-Datei kennt.

Bewusst ohne Dateizahlen je Unterverzeichnis: Diese Tabelle stand bis Release 0.8.0 auf dem Stand von 0.2.0, weil sie beschrieb, was das Dateisystem ohnehin weiß. Verbindlich ist der Baum in Kap. 15.2 und – für den Installationsumfang – die Ausgabe von `install.py`.

## 31.2 Laufzeitglossar

Der Kern nennt die Bestandteile der Laufzeitschicht mit Begriffen, nicht mit Pfaden. Die Abbildung auf die Pfade eines konkreten Client Packs steht hier:

{{EMBED-RAW:leitwerk-core/docs/RUNTIME_GLOSSARY.md:2}}
## 31.3 Platzhalterregister

{{EMBED-RAW:leitwerk-core/docs/PLACEHOLDER_REGISTRY.md:2}}

## 31.4 Quellen der Produktdokumentation und Belegzuordnung

Die Quellen belegen die als `[DOK]` gekennzeichneten Aussagen; der Framework Owner hält diese Liste im Rahmen der Produktbeobachtung aktuell (FW-AK-01).

Sie ist **je Client Pack** geführt. Das ist keine Gliederungsfrage: Eine Aussage über einen Client hängt an dessen Dokumentation und an keiner anderen, und beide Listen haben verschiedene Recherchestände. Bis Release 0.15.0 enthielt dieser Anhang ausschließlich der KI-Client-Quellen – auch dann noch, als das Pack `claude-code` bereits ein Dutzend `[DOK]`-Aussagen gegen `code.claude.com` trug. Die Liste behauptete damit, die `[DOK]`-Aussagen zu belegen, und tat es für einen der beiden Clients nicht.

Die Kennungen tragen seit Release 0.16.0 das Präfix des Client Packs (`QD-` für `devin-desktop`, `QC-` für `claude-code`). Vorher hießen sie `Q1` bis `Q17` – dieselben Kürzel, mit denen das Framework an rund zwanzig Stellen seine **Qualitätsregeln** bezeichnet (`Q8` etwa die Größenschwelle einer Änderung). Zwei Bedeutungen desselben Kürzels in einem Dokument sind eine Verwechslung, die keinen Nutzen hat.

Die **maßgebliche Zuordnung je einzelner Zusage** steht in der Fähigkeitsmatrix des jeweiligen Packs (Kap. 15.1 beziehungsweise Kap. 7a): Dort nennt die Belegspalte je Zeile die Seite, auf die sie sich stützt. Diese Liste sagt, welche Seite wofür herangezogen wurde und **wann sie abgerufen worden ist** – die Angabe, die eine Wiederholungsprüfung braucht.

### 31.4.1 Client Pack `devin-desktop`

Recherchestand: 01.–02.09.2026, gegen Devin Desktop 3.8.20 (QD-4). **Seither nicht erneut abgeglichen.** Keine Einstufung der Fähigkeitsmatrix dieses Packs ist gegen eine Installation belegt; 13 von 26 Zeilen tragen einen VERIFY-Marker (Roadmap AP2).

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

Recherchestand: 10.09.2026, gegen Clientversion 2.1.267. Erhoben im Rahmen von AP2 (`leitwerk-core/tests/protocols/2026-09-10-AP2-claude-code.md`); die Seitenangaben sind gegenüber dem Protokoll um die genauen Pfade ergänzt.

| Nr. | Quelle | Belegt im Framework insbesondere |
|---|---|---|
| QC-1 | code.claude.com/docs/en/memory | Regelablage `.claude/rules/*.md`, rekursiv gefunden; Frontmatter-Feld `paths` mit Glob-Mustern, mehreren Mustern und Klammer-Expansion samt Budget (1.000 expandierte Muster, 4 MiB); eine Regel **ohne** `paths` lädt unbedingt und ohne Import; Ladeordnung und `@pfad`-Importe der Wurzel-Anweisungsdatei; Grenze 4 MiB je Anweisungsdatei und Empfehlung 200 Zeilen; Entfernen von Block-Kommentaren vor dem Einspeisen (für `CLAUDE.md` dokumentiert); `claudeMdExcludes` |
| QC-2 | code.claude.com/docs/en/permissions | Pfadregeln werden nur für `Read` und `Edit` ausgewertet, für andere Werkzeuge angenommen, nie konsultiert und beim Sitzungsstart als Warnung gemeldet; `deny` vor `ask` vor `allow` und die Unaufhebbarkeit einer Verweigerung über alle Ebenen; gitignore-Mustersemantik samt Normalisierung auf POSIX-Form unter Windows; Präfixsemantik der Befehlsregeln und ihre Grenze (`git -C . push` trifft nicht); `disableBypassPermissionsMode` und `disableAutoMode`; Vorrang eines mit Exit-Code 2 blockierenden Hooks **vor** den Berechtigungsregeln |
| QC-3 | code.claude.com/docs/en/skills | `SKILL.md`-Frontmatter (`name`, `description`, `allowed-tools`, `disable-model-invocation`, `user-invocable`, `paths`, `model`); Wirkung von `disable-model-invocation: true` – das Modell kann den Skill nicht selbst laden, und seine Beschreibung kommt gar nicht erst in den Kontext; Suchpfade der Skill-Ablage; Aufruf über `/name` |
| QC-4 | code.claude.com/docs/en/sub-agents | Subagentenprofile unter `.claude/agents/`; Frontmatter `tools` (Allowlist) und `disallowedTools` (Denylist) mit dokumentierter Verarbeitungsreihenfolge; die Beschränkung wirkt technisch; ein Profil, dessen `tools`-Liste sich zu keinem Werkzeug auflöst, wird gar nicht erst gestartet; weitere Felder, darunter `permissionMode` |
| QC-5 | code.claude.com/docs/en/settings | Ablageorte und Rangfolge der Einstellungsdateien: verwaltet → Kommandozeile → `settings.local.json` → `settings.json` → Nutzer; `permissions`, `hooks`, `env` und `defaultMode` in derselben Datei; verwaltete Einstellungen sind bis auf wenige benannte Ausnahmen unüberschreibbar |

### 31.4.3 Was die Liste über sich selbst sagt

Die beiden Recherchestände liegen neun Tage auseinander, und nur der jüngere ist gegen eine benannte Clientversion erhoben. `FW-AK-01` bleibt deshalb `offen`: Der Testfall verlangt den Abgleich **beider** Listen mit der jeweils aktuellen Dokumentation und dem Produkt-Changelog. Für `claude-code` ist er mit Release 0.16.0 geführt, für `devin-desktop` steht er aus – dort ist seit dem Recherchestand kein Changelog gesichtet worden.

Eine Quelle ohne Abrufdatum ist kein Beleg, sondern eine Behauptung mit Fußnote: Produktdokumentation ändert sich, und ohne Datum lässt sich nicht sagen, ob eine Aussage noch trägt. Dieselbe Überlegung hatte D-25 für Versionsangaben angestellt.

## 31.5 Konsolidierter Verifikationsbedarf

Der **maßgebliche** Verifikationsbedarf steht seit Release 0.5.0 in der Fähigkeitsmatrix des jeweiligen Client Packs: Jede Zeile ohne Beleg trägt dort den Marker `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>`, und die Matrix wird mit dem Pack gepflegt statt in diesem Anhang. Belegstand zum Zeitpunkt dieser Dokumentfassung: 13 von 26 Zeilen bei `devin-desktop` tragen den Marker; bei `claude-code` trägt ihn nach AP2 **keine** Zeile mehr, dafür ist dort keine Einstufung als **beobachtete** Durchsetzung belegt – ein Dokumentenabgleich belegt `[DOK]`, nicht `[TECHNISCH]` im Sinne einer beobachteten Wirkung. Die Matrix beider Packs ist in Kap. 15.1 beziehungsweise Kap. 7a eingebettet.

Die folgende Liste ergänzt sie um Punkte, die keiner einzelnen Zusage der Matrix zugeordnet sind, sondern das Zusammenspiel betreffen. Sie gilt für das Client Pack `devin-desktop`; Prüfweg ist Roadmap-AP2, Testklasse AK:

| Nr. | Prüfpunkt | Betroffene Stellen |
|---|---|---|
| V1 | Zeichenlimits für Regeldateien unter Devin Local (dokumentiert bislang für Cascade-Regeln: 6.000/12.000) | `.devin/rules/README.md`, AGENTS.md-Größenbudget, Validator-Grenzen |
| V2 | Exakte Schemadetails von `.devin/config.json` (Schlüsselstruktur, Glob-/Präfix-Semantik, Wildcard `Fetch(*)`, Kommentarfelder-Toleranz) | `.devin/config.json`, FW-CORE-03 Abschnitt 4 |
| V3 | Hook-Eingabeschema (Feldnamen wie `tool_name`/`tool_input`) und Blockierverhalten; anschließend Umstellung des Schutz-Hooks auf fail-closed | `leitwerk-core/tests/scripts/hook-check-secrets.py`, `hook-overlay-status.py`, `.devin/hooks.v1.json` |
| V4 | Skill-Discovery über `.agents/skills/` durch Devin Local; Verhalten der `@skills:`-Erwähnung im Desktop; Grenze „ein Skill aktiv" | FW-CORE-08 Abschnitt 2, K-12 |
| V5 | Toleranz unbekannter Frontmatter-Schlüssel in SKILL.md (D-08 bleibt unabhängig davon bestehen) | Skill-Standard, K-18 |
| V6 | Struktur von `.devin/mcp_config.json` im Desktop und Status des Legacy-Pfads `~/.codeium/mcp_config.json` | `.devin/mcp_config.json.example` |
| V7 | Codebasis-Indexierung: Art, Speicherort, Abschaltbarkeit (Datenschutzmodell Abschnitt 1) | FW-CORE-02, K-20 |
| V8 | Reichweite geteilten Kontexts in Spaces | FW-CORE-02 Abschnitt 3.9 |
| V9 | Wirkung additiver Skill-`permissions` gegenüber Sitzungs- und Projektregeln in Devin Local | Skills mit `permissions`, u. a. `fw-mr-description` |
| V10 | Zeichen-/Größenbudget und Ladeverhalten der always-on-Summe (AGENTS.md + `00-*` + `20-*`) im realen Systemprompt | Laufzeitschicht gesamt |

## 31.6 Beispielartefakte (synthetisch)

Im Repository unter `leitwerk-core/examples/`: ausgefüllte Overlay-Laufzeitfassung, vollständiger Ergebnisbericht und Merge-Request-Beschreibung mit Nutzungsvermerk – alle ausdrücklich synthetisch und mit erfundenen Bezeichnern (siehe `leitwerk-core/examples/README.md`).

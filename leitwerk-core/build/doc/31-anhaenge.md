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

Recherchestand: 01.–02.09.2026. Die Quellen belegen die als `[DOK]` gekennzeichneten Aussagen; der Framework Owner hält diese Liste im Rahmen der Produktbeobachtung aktuell (FW-AK-01).

| Nr. | Quelle | Belegt im Framework insbesondere |
|---|---|---|
| Q1 | devin.ai/blog/windsurf-is-now-devin-desktop | Rebranding zum 02.06.2026; Devin Local ersetzt Cascade; Übergangsfrist für Cascade; Agent Command Center, Spaces, ACP |
| Q2 | docs.devin.ai/desktop/devin-desktop-faq | `.devin/` als Primär-, `.windsurf/` als Legacy-Pfad; `.windsurfrules`; Systempfade für organisationsweite Regeln; Legacy-MCP-Pfad; Plankontinuität |
| Q3 | docs.devin.ai/desktop/devin-local | Modi Normal/Plan/Ask; Berechtigungsmodell deny/ask/allow mit Geltungsbereichen; MCP-Bestätigung als Standard; Subagenten (Preview) und Quick Review; keine Memories/Workflows in Devin Local; Migrationsassistent; Enterprise-Einstellungen (Sandbox-Erzwingung, Domain-Listen); Konfigurationspfade |
| Q4 | docs.devin.ai/desktop/changelog | Version 3.8.20 vom 21.08.2026; Komposition der Berechtigungsebenen mit deny-Vorrang; `sandbox.excluded`; persistente Plan-Dateien; Subagenten-Dateiformen; Skill-Berechtigungen bei Auto-Genehmigungen |
| Q5 | docs.devin.ai/desktop/cascade/agents-md | AGENTS.md im Root always-on; Unterverzeichnisse als automatische Glob-Regeln; Einspeisung in die Regel-Engine; Namensvarianten |
| Q6 | docs.devin.ai/cli/extensibility/rules | Regeldateien und -orte (AGENTS.md, AGENTS.local.md, `.devin/rules/*.md`, global), Frontmatter `description`/`trigger`/`globs` mit Werten, Präzedenzen, Kompatibilitätspfade |
| Q7 | docs.devin.ai/desktop/cascade/memories | Aktivierungsmodi der Regeln; Zeichenlimits 6.000/12.000 (Cascade-Kontext); Memories nur für Cascade |
| Q8 | docs.devin.ai/desktop/cascade/workflows | Workflows nur für Cascade; Migration zu Skills; Limits |
| Q9 | docs.devin.ai/product-guides/skills | SKILL.md-Format; Suchpfade einschließlich `.agents/skills/` (empfohlen) und `.devin/skills/`; `triggers`; `@skills:`-Erwähnung; Argument-Substitution; eine aktive Skill-Grenze |
| Q10 | docs.devin.ai/cli/extensibility/skills/creating-skills | Projekt- und globale Skill-Pfade; Frontmatter-Felder inkl. `allowed-tools`, `permissions` (additiv), `argument-hint`, `model`, `subagent`, `agent`; Aufruf `/skill-name` |
| Q11 | docs.devin.ai/cli/reference/permissions | Matcher `Read()`, `Write()`, `Exec()`, `Fetch()`, Tool- und MCP-Matcher; deny > ask > allow; Permission-Modi; Ebenen-Präzedenz; Sitzungs-Grant-Stufen |
| Q12 | docs.devin.ai/cli/extensibility/configuration | `config.json`-Scopes und -Schlüssel; `mcp_config.json`/`.local`; `read_config_from`; Enterprise unüberschreibbar |
| Q13 | docs.devin.ai/cli/extensibility/hooks/overview | `hooks.v1.json`; Ereignisse; Blockierung per Exit-Code 2/`decision: block`; `additionalContext`; `DEVIN_PROJECT_DIR` |
| Q14 | docs.devin.ai/de/cli/subagents | Subagent-Dateiformen und Frontmatter; eingebaute Profile; Vordergrund-/Hintergrundrechte |
| Q15 | docs.devin.ai/cli/sandbox | Sandbox-Ableitung aus Berechtigungen; Domainfilter und Modi; `sandbox.excluded`; Plattformgrenzen (kein Windows); Instabilität des Netzfilters |
| Q16 | docs.devin.ai/cli/enterprise/team-settings | Team-Kontrollen: Modell-Allowlist, Websuche standardmäßig aus, MCP-Kontrollen und Registry-Erzwingung, unüberschreibbare Terminal-Permissions, Sandbox-Erzwingung, Attribution-Filter |
| Q17 | docs.devin.ai/admin/security | Training-Opt-out auf kostenpflichtigen Plänen; Zero Data Retention nach Opt-out; Teams-Opt-out nur durch Admin; Enterprise nur mit schriftlicher Zustimmung; SOC 2 Type II; Verschlüsselung |

## 31.5 Konsolidierter Verifikationsbedarf

Der **maßgebliche** Verifikationsbedarf steht seit Release 0.5.0 in der Fähigkeitsmatrix des jeweiligen Client Packs: Jede Zeile ohne Beleg trägt dort den Marker `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>`, und die Matrix wird mit dem Pack gepflegt statt in diesem Anhang. Belegstand zum Zeitpunkt dieser Dokumentfassung: 13 von 26 Zeilen bei `devin-desktop`, 9 von 26 bei `claude-code`. Die Matrix beider Packs ist in Kap. 15.1 beziehungsweise Kap. 7a eingebettet.

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

Im Repository unter `leitwerk-core/examples/`: ausgefüllte Overlay-Laufzeitfassung, vollständiger Devin-Ergebnisbericht und Merge-Request-Beschreibung mit Nutzungsvermerk – alle ausdrücklich synthetisch und mit erfundenen Bezeichnern (siehe `leitwerk-core/examples/README.md`).

# Platzhalterregister

Alle im Framework verwendeten Platzhalter. Neue Platzhalter werden hier registriert, bevor sie verwendet werden (`.koolie/core/tests/scripts/validate-framework.py` meldet unbekannte Platzhalter als Warnung). Platzhalter werden ausschließlich durch das Project Overlay oder die Organisation befüllt – niemals im Framework Core. Beispiele sind synthetisch.

**Die Spalte „Wird gesetzt in" ist bei drei Platzhaltern durchgesetzt, bei allen übrigen ist sie eine Angabe.** `<BUILD_COMMAND>`, `<TEST_COMMAND>` und `<LINT_COMMAND>` werden von **Prüfung 42** in der hier genannten Overlay-Tabelle gelesen – über die Platzhalterzelle, nicht über eine Spaltennummer – und gegen die installierte Berechtigungsdatei gehalten (D-90, D-91). Bei den übrigen Platzhaltern sagt die Spalte, wo der Wert **hingehört**; dass er dort steht, prüft niemand nach.

## Vom Arbeitsauftrag vorgegebene Platzhalter

| Platzhalter | Bedeutung | Wird gesetzt in | Beispiel (synthetisch) | Pflicht vor Aktivierung |
|---|---|---|---|---|
| `<PROJECT_NAME>` | Neutraler Projektname | Overlay 1 | „Antragsverwaltung" | ja |
| `<PROJECT_CODE>` | Projektkürzel | Overlay 1 | „AVW" | ja |
| `<REPOSITORY_NAME>` | Name des Projekt-Repositorys | Overlay 3 | „avw-backend" | ja |
| `<TECH_STACK>` | Sprachen, Frameworks, Build-System mit Versionen | Overlay 8 | „Sprache X 21, Framework Y 3, Build Z" | ja |
| `<ISSUE_TRACKER>` | Werkzeugklasse Issue Tracking | Overlay 13 | „Jira" | ja |
| `<CI_CD_PLATFORM>` | Werkzeugklasse CI/CD | Overlay 7 | „GitLab CI" | ja |
| `<DOCUMENTATION_PLATFORM>` | Werkzeugklasse Dokumentation/Wiki | Overlay 13 | „Confluence" | nein |
| `<TEST_FRAMEWORK>` | Testframework | Overlay 8 | „Testframework T 5" | ja |
| `<QUALITY_GATE>` | Quality-Gate-Werkzeug oder -Regelwerk | Overlay 7 | „Statische Analyse S, Gate ‚Standard'" | ja |
| `<SECURITY_CONTACT>` | Rolle für Sicherheitsfreigaben und Vorfälle | Overlay 15 | „Informationssicherheitsbeauftragte Rolle des Projekts" | ja |
| `<APPROVAL_ROLE>` | Rolle für Freigaben Stufe hoch und Overlay | Overlay 15 | „Technische Projektleitung" | ja |
| `<PROJECT_RULES_PATH>` | Pfad des verbindlichen Convention-Dokuments | Overlay 9 | „.koolie/project-overlay/documents/coding-guidelines/guidelines.md" | ja |

## Laufzeit-Platzhalter (durch `install.py` aufgelöst)

Diese Platzhalter unterscheiden sich von allen anderen: Sie werden **nicht vom Menschen** befüllt, sondern beim Installieren aus dem `manifest.json` des gewählten Client Packs aufgelöst. Sie stehen in den Quelltexten des Kerns – vor allem in `.koolie/core/framework/skills/` – dort, wo ein Text auf ein Artefakt der Laufzeitschicht verweist.

Die Begriffsfassung derselben Abbildung steht in `.koolie/core/docs/RUNTIME_GLOSSARY.md`: Fließtext nennt den Begriff, ein Quelltext, der gerendert wird, den Platzhalter.

| Platzhalter | Bedeutung | `devin-desktop` | `claude-code` | `openai-codex` | `kiro` |
|---|---|---|---|---|---|
| `<CLIENT_NAME>` | Produktname des Clients. **Nur zum Nennen, nie zum Zuschreiben** (D-129): Sagt ein Text etwas *über* das Produkt, gehört es in dessen Client Pack. Und er hilft **nur in einer gerenderten Quelle** – einziger angewandter Fall: der Titel von `framework/runtime/root-instruction.md` | `Devin Desktop` | `Claude Code` | `OpenAI Codex CLI` | `Kiro` |
| `<RUNTIME_DIR>` | Laufzeitschicht | `.devin` | `.claude` | `.codex` | `.kiro` |
| `<ROOT_INSTRUCTION_FILE>` | Wurzel-Anweisungsdatei | `AGENTS.md` | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` |
| `<ROOT_INSTRUCTION_LOCAL>` | Nutzerlokale Ergänzung dazu | `AGENTS.local.md` | `CLAUDE.local.md` | `AGENTS.override.md` – **verdrängt** die Wurzel-Anweisung, statt sie zu ergänzen (D-341) | `AGENTS.local.md` – **kein Mechanismus des Clients**; der Name steht nur, weil die Kernquelle ein Schreibverbot auf ihn führt (D-414) |
| `<PERMISSIONS_FILE>` | Berechtigungsdatei | `.devin/config.json` | `.claude/settings.json` | `.codex/config.toml` | `.kiro/agents/koolie.json` – das Agentenprofil, gewählt durch `.kiro/settings/cli.json` (D-414) |
| `<SKILLS_DIR>` | Skill-Ablage | `.devin/skills` | `.claude/skills` | `.codex/skills` | `.kiro/skills` |
| `<RULES_DIR>` | Regelablage | `.devin/rules` | `.claude/rules` | `.codex/rules` | `.kiro/steering` |
| `<AGENTS_DIR>` | Agentenprofile | `.devin/agents` | `.claude/agents` | `.codex/agents` | `.kiro/agents` |
| `<HOOKS_FILE>` | Hook-Konfiguration | `.devin/config.json` | `.claude/settings.json` | `.codex/hooks.json` | `.kiro/hooks/koolie.json` |
| `<MCP_FILE>` | MCP-Konfiguration | `.devin/mcp_config.json` | `.mcp.json` | `.codex/config.toml` | `.kiro/settings/mcp.json` |
| `<CORE_DIR>` | Name des Kernverzeichnisses | `.koolie/core` | `.koolie/core` | `.koolie/core` | `.koolie/core` |

Ein Client Pack MUSS jeden dieser Platzhalter in seinem `manifest.json` unter `runtime_placeholders` belegen; ein unaufgelöster Laufzeit-Platzhalter in einer Installation ist ein Fehler.

Einzige Ausnahme ist `<CORE_DIR>`: Der Name des Kernverzeichnisses ist keine Eigenschaft eines Clients, sondern dieser Installation. `install.py` und der Validator setzen ihn aus dem tatsächlichen Verzeichnisnamen; ein Client Pack darf ihn nicht belegen. Damit berührt eine spätere Umbenennung des Kernverzeichnisses (Roadmap P3) die Client Packs nicht.

## Vom Framework ergänzte Platzhalter

| Platzhalter | Bedeutung | Wird gesetzt in | Beispiel (synthetisch) | Pflicht vor Aktivierung |
|---|---|---|---|---|
| `<FRAMEWORK_OWNER>` | Rolle mit Gesamtverantwortung für das Framework | `.koolie/core/OWNERS.md` | „Leitung Entwicklungsmethodik" | ja |
| `<DATA_PROTECTION_CONTACT>` | Rolle für Datenschutzfreigaben | Overlay 15 / Organisation | „Datenschutzkoordination" | ja |
| `<PRODUCT_OWNER_ROLE>` | Rolle für fachliche Klärungen | Overlay 15 | „Product Owner" | ja |
| `<ARCHITECT_ROLE>` | Rolle für Architekturentscheidungen | Overlay 15 | „Softwarearchitektur" | ja |
| `<ALLOWED_PATHS>` | Für den KI-Client erlaubte Pfade (Glob) | Overlay 4 | „src/**, test/**, docs/**" | ja |
| `<EXCLUDED_PATHS>` | Ausgeschlossene Pfade (weder lesen noch ändern) | Overlay 4 | „deploy/**, infra/**, config/prod/**" | ja |
| `<READ_ONLY_PATHS>` | Nur lesbare Pfade | Overlay 4 | „api-contracts/**, db/migrations/**" | ja (oder „keine") |
| `<TEST_PATHS>` | Pfade, in denen M4 schreiben darf | Overlay 4 | „test/**" | ja |
| `<DOC_PATHS>` | Pfade, in denen M5 schreiben darf | Overlay 4 | „docs/**" | ja |
| `<CI_CONFIG_PATHS>` | CI/CD-Konfigurationsdateien (Schreibverbot) | Overlay 4 | „.gitlab-ci.yml" | ja |
| `<QUALITY_GATE_CONFIG_PATHS>` | Quality-Gate-Konfiguration (Schreibverbot) | Overlay 4 | „config/lint/**, coverage.config" | ja |
| `<BUILD_COMMAND>` | Freigegebener Build-Befehl | Overlay 5 | „build-tool compile" | ja |
| `<TEST_COMMAND>` | Freigegebener Testbefehl | Overlay 6 | „build-tool test" | ja |
| `<LINT_COMMAND>` | Freigegebener Lint-/Formatprüfbefehl | Overlay 6 | „build-tool lint" | ja |
| `<COMMIT_CONVENTION>` | Commit-Nachrichtenkonvention | Overlay 10 | „Conventional Commits + Ticket-Kennung" | ja |
| `<BRANCHING_MODEL>` | Branching-Modell | Overlay 10 | „Feature-Branches auf Standard-Branch" | ja |
| `<DEFAULT_BRANCH>` | Standard-Branch | Overlay 10 | „main" | ja |
| `<BRANCH_PREFIX>` | Branch-Namensschema | Overlay 10 | „feature/`<PROJECT_CODE>`-123-kurz" | nein |
| `<MR_TEMPLATE_PATH>` | Pfad der Merge-Request-Vorlage | Overlay 10 | „.gitlab/merge_request_templates/default.md" | nein |
| `<CHANGE_SIZE_THRESHOLD>` | Schwellenwert geänderter Dateien für R1/Q8 | Overlay 2 oder Ausnahmeregister | „10" | ja |
| `<CRITICAL_MODULE>` | Beispielhafte Bezeichnung einer kritischen Komponente (nur in Erläuterungen) | Overlay 2 | „auth-core" | – |
| `<PILOT_DURATION>` | Dauer des Piloten | `.koolie/core/pilot/PILOT_CONCEPT.md` | „8 Wochen" | vor Pilotstart |
| `<TECH_PACK_NAME>` / `<TECH_PACK_CODE>` | Name und Kürzel eines Technology Packs | Pack-Vorlage | „Sprache X" / „LX" | bei Pack-Erstellung |
| `<ROLE_PACK_NAME>` / `<ROLE_PACK_CODE>` | Name und Kürzel eines Role Packs | Pack-Vorlage | „Requirements Engineering" / „RE" | bei Pack-Erstellung |
| `<CLIENT_PACK_NAME>` / `<CLIENT_PACK_CODE>` | Name und Kürzel eines Client Packs (Abbildung auf einen KI-Client, `.koolie/core/clients/`) | Pack-Vorlage | „Client C" / „CC" | bei Pack-Erstellung |
| `<FORM_NAME>`, `<PLACEHOLDER>`, `<PACK>` | Generische Platzhalter in Erläuterungen und Beispielen | – | – | – |
| `<JAHR>`, `<JJJJ>`, `<NNN>` | Schema-Platzhalter für Jahres- und Laufnummern in IDs (`CR-<JAHR>-<NNN>`, `INC-<PROJECT_CODE>-<JJJJ>-<NNN>`) | Vorlagen in `.koolie/core/governance/` | „CR-2026-001" | – |
| `<TBD: …>` | Offene projekt- oder organisationsspezifische Entscheidung | überall | – | Overlay-Abschnitte 4, 5, 6, 13, 14, 15: ja |

# 15 Technische Referenzstruktur

## 15.1 Validierung der Devin-Mechanismen (Phase-3-Prüfung)

Vor dem Entwurf der Struktur wurde anhand der offiziellen Dokumentation geprüft, welche Dateinamen, Verzeichnisse und Mechanismen der zugrunde gelegte Produktstand tatsächlich unterstützt (Quellen: Anhang 31.3; Produktstand: Kap. 4.4). Es wurden keine Devin-Konventionen erfunden; jede verwendete Konvention ist nachfolgend mit Belegstatus klassifiziert – **offiziell dokumentiert** `[DOK]`, **technisch begründete Empfehlung** `[EMPF]` (aus dokumentierten Mechanismen abgeleitet, noch nicht in einer Installation ausgeführt), **konzeptioneller Vorschlag** `[KONZ]` (Framework-Konvention ohne Produktbezug) oder **noch zu verifizieren**.

| Mechanismus | Verwendete Konvention | Belegstatus |
|---|---|---|
| Zentrale Agentenanweisung | `AGENTS.md` im Workspace-Root, always-on, wird in die Regel-Engine eingespeist; `AGENTS.local.md` persönlich | `[DOK]` |
| Regeldateien | `.devin/rules/*.md` mit Frontmatter `description`, `trigger` (`always_on`, `model_decision`, `glob`, `manual`, `agent`), `globs`; Legacy `.windsurf/` nur Fallback | `[DOK]` |
| Zeichenlimits Regeln | 6.000 (global) / 12.000 (Workspace-Datei) – für Cascade-Regeln dokumentiert; Gültigkeit für Devin Local: `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>`; Framework hält die Grenzen konservativ ein | `[DOK]`/verify |
| Skills | `.devin/skills/<name>/SKILL.md`; Aufruf `/name`; Frontmatter `name`, `description`, `argument-hint`, `allowed-tools`, `permissions` (additiv), `triggers`, optional `model`, `subagent`, `agent` | `[DOK]` |
| Alternativer Skill-Pfad | `.agents/skills/` (in der Produktdokumentation als empfohlen genannt); Discovery durch Devin Local: `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` – Framework nutzt primär `.devin/skills/` (D-03, K-12) | `[DOK]`/verify |
| Berechtigungen | `.devin/config.json` (projekt, versioniert), `.devin/config.local.json` (persönlich), Benutzer- und Organisationsebene; Regeln `deny`/`ask`/`allow` mit Mustern `Read()`, `Write()`, `Exec()`, `Fetch()`, `mcp__*`; `deny` gewinnt; Sitzungs-Grant-Stufen | `[DOK]` (exakte Schemadetails: verify) |
| Permission-Modi | Normal, Accept Edits, Smart, Bypass, Autonomous(+Sandbox) | `[DOK]` |
| Hooks | `.devin/hooks.v1.json`; Ereignisse u. a. `PreToolUse`, `SessionStart`; Blockierung per Exit-Code 2 oder `{"decision":"block"}`; `DEVIN_PROJECT_DIR` | `[DOK]` (stdin-Schema: verify) |
| Subagenten | `.devin/agents/<name>.md` mit `name`, `description`, `allowed-tools`, `model`, `max-nesting`; eingebaute Profile; Hintergrundläufe nur mit vorab genehmigten Rechten | `[DOK]` |
| Plan-Modus | read-only Recherche, Plan-Datei `~/.devin/plans/plan-<session>.md` | `[DOK]` |
| MCP | `.devin/mcp_config.json` / `.local.json`; Standard: Bestätigung je Aufruf; Enterprise-Allowlists und Registry-Erzwingung | `[DOK]` (Dateistruktur: verify) |
| Sandbox | Pfad-Ableitung aus `Write()`-Scopes, Domainfilter, `sandbox.excluded`; nicht unter Windows; Netzfilter laut Doku instabil | `[DOK]` |
| Enterprise-Einstellungen | erzwungene Berechtigungen, Sandbox-Pflicht, Domainlisten, MCP-/Modell-Kontrollen, Websuche standardmäßig aus; Systempfade für organisationsweite Regeln | `[DOK]` |
| Nicht verwendet | Cascade-Workflows und -Memories (von Devin Local nicht unterstützt), `.windsurf/`-Pflege, Bypass-Modus | `[DOK]` (Nichtunterstützung) |
| Framework-Konventionen | Nummernschema der Regeldateien, Präfixe `fw-`/`prj-`/`role-*`/`tech-*`, Skill-Begleitdateien, Metadatentabellen, Manifest-Mechanismus | `[KONZ]` |

Alle verify-Punkte sind in der Verifikationsliste des Abschlussteils zusammengeführt und werden in Roadmap-AP2 in einer Zielinstallation geprüft; nicht verifizierte produktspezifische Pfade sind im Repository zusätzlich vor Ort markiert.

## 15.2 Repository-Struktur

Der gesamte unveränderliche Kern liegt in **einem** Verzeichnis: `devin-core-framework/`. Im Wurzelverzeichnis des Projekts stehen nur die drei Dinge, die dort stehen müssen: `AGENTS.md` und `.devin/`, weil Devin sie ausschließlich dort findet `[DOK]`, sowie `project-overlay/` als austauschbare Projektkonfiguration. Angelegt und aktualisiert werden diese Wurzelbestandteile durch `devin-core-framework/install.py` aus `devin-core-framework/root-template/`; damit ist die Übernahme in ein Projekt das Kopieren eines Ordners und ein Skriptaufruf (Kap. 28).

```text
<REPOSITORY_NAME>/                       # Projekt-Repository
├── AGENTS.md                            # zentrale Agentenanweisung (Kap. 16) [DOK]
├── AGENTS.local.md.example              # Vorlage persönliche Ergänzung (nicht versioniert) [DOK]
├── .gitignore                           # schützt persönliche Konfiguration, Legacy, Build
├── .devin/                              # DEVIN-LAUFZEITSCHICHT [DOK]
│   ├── README.md                        # Mechanismen, Modi, Sitzungsfreigaben (mit Belegstatus)
│   ├── rules/                           # 00/10/15 Core-Kurzfassungen (Kern)
│   │                                    # · 20 Overlay always-on · 2N Overlay-Erweiterungen
│   │                                    # · 30 Role Pack · 40 Technology Packs (Projekt)
│   │                                    # · 21-/40-TEMPLATE Vorlagen (Kern) · README
│   ├── skills/                          # fw-* : 12 Referenz-Skills (Kern)
│   │                                    # prj-*: projektspezifische Skills (Projekt)
│   │                                    # je SKILL.md + EXAMPLES + TESTS + CHANGELOG
│   ├── agents/fw-reviewer.md            # nur lesendes Review-Subagentenprofil
│   ├── config.json                      # Berechtigungen deny/ask/allow + Kernregel-Integritätsblock
│   ├── hooks.v1.json                    # PreToolUse-Schutzprüfung, SessionStart-Statusmeldung
│   └── mcp_config.json.example          # MCP-Vorlage (Standard: keine Server)
│
├── devin-core-framework/                # DER KERN – ein Verzeichnis, byte-gleich zum Release
│   ├── install.py                       # legt die Wurzelbestandteile an (--update / --check)
│   ├── root-template/                   # Quelle für AGENTS.md, .devin/, project-overlay/
│   ├── VERSION · CHANGELOG.md           # Versionsstand, Änderungsverzeichnis
│   ├── OWNERS.md                        # Ownership je Bereich (Governance)
│   ├── framework/                       # KANONISCHE, WERKZEUGNEUTRALE EBENE
│   │   ├── core/00…10-*.md              # Framework Core (Kap. 6, 10–14, 18, 25)
│   │   ├── role-packs/                  # README, _template, software-development
│   │   ├── tech-packs/                  # README, _template (Packs entstehen projektbezogen)
│   │   └── org-policies/                # Ebene B: Einbindungspunkt + Klassifizierungs-Mapping
│   ├── templates/                       # SKILL_TEMPLATE · PLAN_TEMPLATE · MR_AI_DISCLOSURE
│   ├── prompts/                         # Prompt-Bibliothek FW-PR-001…012 + README (Kap. 21)
│   ├── checklists/                      # FW-CL-01…11 + README (Kap. 22)
│   ├── decision-trees/                  # FW-DT-01…06 + README (Kap. 23; Mermaid validiert)
│   ├── onboarding/                      # QUICKSTART · GUIDE · MENTOR_CHECKLIST · exercises/
│   │                                    # · KNOWLEDGE_CHECK · COMPLETION_CRITERIA · REFERENCE
│   ├── examples/                        # ausschließlich synthetische Beispiele
│   ├── governance/                      # DECISION_LOG · RACI · PRIORITY_HIERARCHY
│   │                                    # · RELEASE_PROCESS · CHANGE_REQUEST_TEMPLATE
│   │                                    # · EXCEPTION/FEEDBACK/INCIDENT
│   ├── pilot/                           # PILOT_CONCEPT · METRICS (Kap. 27)
│   ├── docs/                            # ADOPTION_GUIDE · ROADMAP · PLACEHOLDER_REGISTRY
│   ├── tests/                           # TEST_CATALOG.md
│   │   └── scripts/                     # validate-framework.py · validate-output.py · Hooks
│   └── build/                           # Assemblierung des Gesamtdokuments
│
├── project-overlay/                     # EBENE 4 (austauschbar; Kap. 17)
│   ├── OVERLAY.md                       # 21 Abschnitte mit Ausfüllhinweisen
│   ├── overlay-manifest.yaml            # Register eingebundener Dokumente
│   ├── forbidden-terms.txt              # projektlokale Sperrbegriffe (verbleibt im Projekt)
│   ├── documents/<13 Typverzeichnisse>/ # Ablage freigegebener Dokumente/Auszüge + README
│   └── exceptions/EXCEPTIONS.md         # Ausnahmeregister des Projekts
│
└── <Produktivcode des Projekts>         # backend/, frontend/, src/, test/ …
```

**Warum diese Aufteilung.** Vor dieser Fassung lagen zwölf Kern-Verzeichnisse und vier Kern-Dateien direkt im Wurzelverzeichnis – neben dem Produktivcode des Projekts. Das machte die Übernahme fehleranfällig (was gehört zum Framework, was zum Projekt?) und das Wurzelverzeichnis unübersichtlich. Die Bündelung ändert nichts an der inhaltlichen Ebenenhierarchie (Kap. 7); sie trennt lediglich physisch, was ohnehin logisch getrennt war: Der Kern ist ein Ordner, den man ersetzt; das Projekt ist alles daneben.

**Grenze der Bündelung.** `AGENTS.md` und `.devin/` lassen sich nicht mitverschieben – beide Ladeorte sind Werkzeugkonvention und nicht konfigurierbar `[DOK]`. `.devin/` enthält deshalb weiterhin Kern und Projektbestandteile gemischt. Genau diese Mischung löst `install.py` auf: Kern-Dateien kommen aus `root-template/` und werden bei `--update` überschrieben, Projektdateien (`config.json`, `20-`, `2N-`, `30-`, `40-`, `prj-*`) nie. `--check` meldet, wenn eine Kern-Datei im Wurzelverzeichnis lokal verändert wurde – also an der falschen Stelle bearbeitet.

Damit sind alle geforderten Inhalte logisch abgebildet: zentrale Agentenanweisungen (`AGENTS.md`, `.devin/rules/`), Framework Core, Datenschutz- und Sicherheitsregeln (Core 02/03 plus Laufzeitregel 10), allgemeine Entwicklungsregeln (Core 04/06/07 plus Laufzeitregel 15), projektspezifisches Overlay, Rollenmodule, Technologiepakete, Skills, Skill-Vorlagen, Prompt-Vorlagen, Checklisten, Onboarding, Beispiele, Tests und Validierungen der Agentenanweisungen, Änderungsverzeichnis sowie Governance und Ownership.

## 15.3 Laufzeitschicht im Detail

Die folgende Dokumentationsdatei der Laufzeitschicht beschreibt verbindlich, was Devin aus dem Repository liest, welche Mechanismen bewusst nicht verwendet werden und welche Sitzungsfreigaben zulässig sind:

{{EMBED-RAW:.devin/README.md:1}}

Die zugehörige Regeldatei-Systematik:

{{EMBED-RAW:.devin/rules/README.md:1}}

## 15.4 Zentrale Konfigurationsdateien

**Berechtigungen** – restriktiver Standard mit Kernregel-Integritätsblock (Mechanismus `[DOK]`, Regelmenge `[EMPF]`, Schemadetails verify):

{{EMBED:.devin/config.json:json}}

**Hooks** – technische Prüfung vor Schreib-/Ausführungsoperationen und Statusmeldung beim Sitzungsstart (Mechanismus `[DOK]`, Skripte `[EMPF]`, Status entwurf):

{{EMBED:.devin/hooks.v1.json:json}}

**Subagentenprofil** – nur lesende Review-Zulieferung:

{{EMBED:.devin/agents/fw-reviewer.md}}

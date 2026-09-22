# 15 Technische Referenzstruktur

## 15.1 Belegstatus und Durchsetzungstiefe

Für die Struktur wurden keine Client-Konventionen erfunden. Jede verwendete Konvention trägt einen **Belegstatus** – **offiziell dokumentiert** `[DOK]`, **technisch begründete Empfehlung** `[EMPF]` (aus dokumentierten Mechanismen abgeleitet, noch nicht in einer Installation ausgeführt), **konzeptioneller Vorschlag** `[KONZ]` (Framework-Konvention ohne Produktbezug) oder **noch nicht belegt** (`BELEG OFFEN`, mit Grund und Datum).

Wo diese Belege stehen, hat sich mit den Client Packs verschoben (Kap. 7a). Die Zuordnung von Mechanismen zu Dateinamen ist keine Eigenschaft des Frameworks mehr, sondern eine Eigenschaft des jeweiligen Client Packs – und wird dort geführt, versioniert und maschinenlesbar. Dieses Kapitel bettet sie ein, statt sie ein zweites Mal aufzuschreiben.

Der Belegstatus beantwortet die Frage „ist das dokumentiert?“. Die **Fähigkeitsmatrix** beantwortet die zweite, wichtigere: „setzt der Client es durch?“ Beide zusammen ergeben die Durchsetzungstiefe einer Zusage. Für das Client Pack, das dieses Dokument als durchgehendes Beispiel verwendet:

{{EMBED-RAW:leitwerk-core/clients/devin-desktop/CLIENT_PACK.md:1}}
Die Einstufungen sind **nicht** gegen eine Installation belegt; das leistet Roadmap-AP2. Bis dahin nennt die Spalte „Einstufung“ die vorgesehene, nicht die nachgewiesene Durchsetzungstiefe.

## 15.2 Repository-Struktur

Der gesamte unveränderliche Kern liegt in **einem** Verzeichnis: `leitwerk-core/`. Im Wurzelverzeichnis des Projekts stehen nur die Dinge, die dort stehen müssen: die Wurzel-Anweisungsdatei und die Laufzeitschicht, weil der KI-Client sie ausschließlich dort findet, sowie `project-overlay/` als austauschbare Projektkonfiguration. Wie diese Bestandteile heißen, entscheidet das gewählte Client Pack; der Baum unten zeigt sie in der Fassung von `devin-desktop`.

Angelegt und aktualisiert werden die Wurzelbestandteile durch `leitwerk-core/install.py`. Damit ist die Übernahme in ein Projekt das Kopieren eines Ordners und ein Skriptaufruf (Kap. 28).

```text
<REPOSITORY_NAME>/                       # Projekt-Repository
├── AGENTS.md                            # Wurzel-Anweisungsdatei (Kap. 16), erzeugt
├── AGENTS.local.md.example              # Vorlage persönliche Ergänzung, erzeugt
├── .gitignore                           # schützt persönliche Konfiguration, Legacy, Build
├── .devin/                              # LAUFZEITSCHICHT – vollständig erzeugt
│   ├── README.md                        # Mechanismen, Modi, Sitzungsfreigaben
│   ├── rules/                           # 00/10/15 Core-Kurzfassungen · 20 Overlay
│   │                                    # · 2N Overlay-Erweiterungen · 30 Role Pack
│   │                                    # · 40 Technology Packs · Vorlagen · README
│   ├── skills/                          # fw-* : 12 Referenz-Skills · prj-*: projekteigene
│   ├── agents/fw-reviewer.md            # nur lesendes Review-Subagentenprofil
│   ├── config.json                      # Berechtigungen deny/ask/allow + Integritätsblock
│   ├── hooks.v1.json                    # PreToolUse-Schutzprüfung, SessionStart-Meldung
│   └── mcp_config.json.example          # MCP-Vorlage (Standard: keine Server)
│
├── leitwerk-core/                       # DER KERN – ein Verzeichnis, byte-gleich zum Release
│   ├── install.py                       # legt die Wurzelbestandteile an (--update / --check)
│   ├── clientmap.py                     # Semantikabbildung Berechtigungen und Hooks (Kap. 7a)
│   ├── VERSION · CHANGELOG.md           # Versionsstand, Änderungsverzeichnis
│   ├── OWNERS.md                        # Ownership je Bereich (Governance)
│   ├── clients/                         # ABBILDUNGSSCHICHT – je Client vier Dateien
│   │   ├── README.md · _template/       # Regeln der Schicht, Vorlage für neue Packs
│   │   ├── devin-desktop/               # CLIENT_PACK.md · manifest.json · root-template/
│   │   └── claude-code/                 # dito
│   ├── framework/                       # KANONISCHE, WERKZEUGNEUTRALE EBENE
│   │   ├── core/00…10-*.md              # Framework Core (Kap. 6, 10–14, 18, 25)
│   │   ├── runtime/                     # Laufzeitfassung, einmal für alle Clients:
│   │   │                                # Wurzel-Anweisung · Regeltexte · Agentenprofil
│   │   │                                # · permissions.json · hooks.json · Vorlagen
│   │   ├── skills/                      # fw-* Referenz-Skills, eine Quelle je Skill
│   │   ├── role-packs/ · tech-packs/    # Ebene 6 und 5
│   │   └── org-policies/                # Ebene B: Einbindungspunkt + Klassifizierungs-Mapping
│   ├── templates/                       # Project-Overlay-Saat · Regelvorlagen · SKILL_TEMPLATE
│   ├── prompts/                         # Prompt-Bibliothek FW-PR-001…012 + README (Kap. 21)
│   ├── checklists/                      # FW-CL-01…11 + README (Kap. 22)
│   ├── decision-trees/                  # FW-DT-01…06 + README (Kap. 23; Mermaid validiert)
│   ├── onboarding/                      # QUICKSTART · GUIDE · MENTOR_CHECKLIST · exercises/
│   │                                    # · KNOWLEDGE_CHECK · COMPLETION_CRITERIA · REFERENCE
│   ├── examples/                        # ausschließlich synthetische Beispiele
│   ├── governance/                      # DECISION_LOG · RACI · PRIORITY_HIERARCHY
│   │                                    # · RELEASE_PROCESS · change-requests/
│   │                                    # · EXCEPTION/FEEDBACK/INCIDENT
│   ├── pilot/                           # PILOT_CONCEPT · METRICS (Kap. 27)
│   ├── docs/                            # ADOPTION_GUIDE · ROADMAP · RUNTIME_GLOSSARY
│   │                                    # · PLACEHOLDER_REGISTRY
│   ├── tests/                           # TEST_CATALOG.md · protocols/ · scripts/
│   └── build/                           # Assemblierung dieses Dokuments
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

**Die Laufzeitschicht ist Erzeugnis, nicht Quelle.** Kein Bestandteil von `.devin/` wird von Hand geschrieben. Regeltexte, Skills, Agentenprofil, Berechtigungen und Hooks liegen einmal unter `leitwerk-core/framework/runtime/` beziehungsweise `framework/skills/` und werden bei der Installation in die Form des gewählten Client Packs gebracht (Kap. 7a). Ein Client Pack selbst enthält nur noch vier Dateien: die Pfad- und Semantikabbildung (`manifest.json`), die Fähigkeitsmatrix (`CLIENT_PACK.md`) und eine erklärende README der Laufzeitschicht.

**Grenze der Bündelung.** Die Wurzel-Anweisungsdatei und die Laufzeitschicht lassen sich nicht mitverschieben – beide Ladeorte sind Werkzeugkonvention und nicht konfigurierbar `[DOK]`. Die Laufzeitschicht enthält deshalb Kern- und Projektbestandteile gemischt. Genau diese Mischung löst `install.py` auf: **Core** wird bei `--update` überschrieben, **Saat** (Berechtigungsdatei, Overlay, Overlay-Regel) nur bei der Erstinstallation angelegt und danach nie wieder angefasst. `--check` meldet, wenn eine Core-Datei im Wurzelverzeichnis lokal verändert wurde – also an der falschen Stelle bearbeitet.

Damit sind alle geforderten Inhalte logisch abgebildet: zentrale Agentenanweisungen, Framework Core, Datenschutz- und Sicherheitsregeln (Core 02/03 plus Laufzeitregel 10), allgemeine Entwicklungsregeln (Core 04/06/07 plus Laufzeitregel 15), projektspezifisches Overlay, Rollenmodule, Technologiepakete, Skills, Skill-Vorlagen, Prompt-Vorlagen, Checklisten, Onboarding, Beispiele, Tests und Validierungen der Agentenanweisungen, Änderungsverzeichnis sowie Governance und Ownership.

## 15.3 Laufzeitschicht im Detail

Die folgende Dokumentationsdatei der Laufzeitschicht beschreibt verbindlich, was der KI-Client aus dem Repository liest, welche Mechanismen bewusst nicht verwendet werden, welche Sitzungsfreigaben zulässig sind – und, in einem eigenen Abschnitt, die Systematik der Regelablage:

{{EMBED-RAW:<RUNTIME_DIR>/README.md:1}}
Dass diese Systematik **hier** steht und nicht in der Regelablage selbst, ist eine Entscheidung dieses Releases: Der KI-Client führt jede Datei der Regelablage als Regel und macht sie damit ladbar – bei einem Pack sogar unbedingt. **Ein Verzeichnis, das als Regelmenge gelesen wird, enthält nur Regeln** (D-36); erklärender Text steht eine Ebene höher.

## 15.4 Zentrale Konfigurationsdateien

Alle drei folgenden Dateien sind **erzeugt**. Sie stammen aus einer Referenzinstallation, die beim Bau dieses Dokuments angelegt wird – bei einem anderen Client Pack sehen sie anders aus, ohne dass sich eine Regel ändert. Die Quellen liegen unter `leitwerk-core/framework/runtime/`.

**Berechtigungen** – restriktiver Standard mit Kernregel-Integritätsblock. Die Regelmenge ist werkzeugneutral; Werkzeugnamen, Musterform und der Integritätsblock entstehen aus der Semantikabbildung des Client Packs (Kap. 7a, `clientmap.py`):

{{EMBED:<PERMISSIONS_FILE>:json}}
**Hooks** – technische Prüfung vor Schreib- und Ausführungsoperationen sowie Statusmeldung beim Sitzungsstart (Mechanismus `[DOK]`, Skripte `[EMPF]`, Status entwurf):

{{EMBED:<HOOKS_FILE>:json}}
**Subagentenprofil** – nur lesende Review-Zulieferung:

{{EMBED:<AGENTS_DIR>/fw-reviewer.md}}

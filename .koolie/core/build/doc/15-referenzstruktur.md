# 15 Technische Referenzstruktur

## 15.1 Belegstatus und Durchsetzungstiefe

Für die Struktur wurden keine Client-Konventionen erfunden. Jede verwendete Konvention trägt einen **Belegstatus** – **offiziell dokumentiert** `[DOK]`, **technisch begründete Empfehlung** `[EMPF]` (aus dokumentierten Mechanismen abgeleitet, noch nicht in einer Installation ausgeführt), **konzeptioneller Vorschlag** `[KONZ]` (Framework-Konvention ohne Produktbezug) oder **noch nicht belegt** (`BELEG OFFEN`, mit Grund und Datum).

Wo diese Belege stehen, hat sich mit den Client Packs verschoben (Kap. 7a). Die Zuordnung von Mechanismen zu Dateinamen ist keine Eigenschaft des Frameworks mehr, sondern eine Eigenschaft des jeweiligen Client Packs – und wird dort geführt, versioniert und maschinenlesbar. Dieses Kapitel bettet sie ein, statt sie ein zweites Mal aufzuschreiben.

Der Belegstatus beantwortet die Frage „ist das dokumentiert?“. Die **Fähigkeitsmatrix** beantwortet die zweite, wichtigere: „setzt der Client es durch?“ Beide zusammen ergeben die Durchsetzungstiefe einer Zusage. Für das Client Pack, das dieses Dokument als durchgehendes Beispiel verwendet:

{{EMBED-RAW:.koolie/core/clients/devin-desktop/CLIENT_PACK.md:1}}
**Die Spalte „Einstufung“ nennt die vorgesehene Durchsetzungstiefe, die Spalte „Beleg“ ihren Nachweisstand** – beide stehen je Zeile, und das ist der Punkt: Ein Gesamturteil über eine Matrix gibt es nicht. Für dieses Pack ist Roadmap-AP2 mit Release 0.86.0 zu Ende gefahren; neun Zeilen sind an einer laufenden Installation beobachtet, und genau eine sagt noch `BELEG OFFEN` – dauerhaft, weil von außen nicht beobachtbar, was ein Client indexiert. **Zwei der Messungen sind zum Schlechteren ausgegangen**, haben also die zuvor vorgesehene Einstufung widerlegt; das steht in den betreffenden Zeilen und ist nicht eingeebnet worden.

## 15.2 Repository-Struktur

Der gesamte unveränderliche Kern liegt in **einem** Verzeichnis: `.koolie/core/`. Im Wurzelverzeichnis des Projekts stehen nur die Dinge, die dort stehen müssen: die Wurzel-Anweisungsdatei und die Laufzeitschicht, weil der KI-Client sie ausschließlich dort findet, sowie `.koolie/project-overlay/` als austauschbare Projektkonfiguration. Wie diese Bestandteile heißen, entscheidet das gewählte Client Pack. **Der Baum unten nennt sie deshalb mit ihren Platzhaltern** – so gilt er für beide ausgelieferten Packs; Anhang 31.2 löst jeden davon je Pack auf. Bis Release 0.88.1 stand hier die Fassung eines einzigen Clients, und der Baum behauptete damit für jede Installation, was für eine galt.

Angelegt und aktualisiert werden die Wurzelbestandteile durch `.koolie/core/install.py`. Damit ist die Übernahme in ein Projekt das Kopieren eines Ordners und ein Skriptaufruf (Kap. 28).

```text
<REPOSITORY_NAME>/                       # Projekt-Repository
├── <ROOT_INSTRUCTION_FILE>              # Wurzel-Anweisungsdatei (Kap. 16), erzeugt
├── <ROOT_INSTRUCTION_LOCAL>.example     # Vorlage persönliche Ergänzung, erzeugt
├── .gitignore                           # schützt persönliche Konfiguration, Legacy, Build
├── <RUNTIME_DIR>/                       # LAUFZEITSCHICHT – vollständig erzeugt
│   ├── README.md                        # Mechanismen, Modi, Sitzungsfreigaben
│   ├── rules/                           # 00/10/15 Core-Kurzfassungen · 20 Overlay
│   │                                    # · 2N Overlay-Erweiterungen · 30 Role Packs
│   │                                    # · 40 Technology Packs · Vorlagen
│   ├── skills/                          # fw-*: 12 Referenz-Skills · role-*/tech-*:
│   │                                    #   aktivierte Packs · prj-*: projekteigene
│   ├── agents/fw-reviewer.md            # nur lesendes Review-Subagentenprofil
│   ├── <PERMISSIONS_FILE>               # Berechtigungen deny/ask/allow + Integritätsblock
│   │                                    #   UND der Hook-Block (D-32, siehe unten)
│   └── <MCP-Konfiguration>.example      # MCP-Vorlage (Standard: keine Server)
│
├── .koolie/                             # ein Verzeichnis für Kern und Projektkonfiguration
│   ├── core/                            # DER KERN – byte-gleich zum Release
│   │   ├── install.py                   # legt die Wurzelbestandteile an (--update / --check)
│   │   ├── clientmap.py                 # Semantikabbildung Berechtigungen und Hooks (Kap. 7a)
│   │   ├── VERSION · CHANGELOG.md       # Versionsstand, Änderungsverzeichnis
│   │   ├── OWNERS.md                    # Ownership je Bereich (Governance)
│   │   ├── clients/                     # ABBILDUNGSSCHICHT – je Client drei Dateien
│   │   │   ├── README.md · _template/   # Regeln der Schicht, Vorlage für neue Packs
│   │   │   ├── devin-desktop/           # CLIENT_PACK.md · manifest.json · root-template/
│   │   │   └── claude-code/             # dito
│   │   ├── framework/                   # KANONISCHE, WERKZEUGNEUTRALE EBENE
│   │   │   ├── core/00…10-*.md          # Framework Core, elf Module (Kap. 6, 10–14, 18, 25)
│   │   │   ├── runtime/                 # Laufzeitfassung, einmal für alle Clients:
│   │   │   │                            # Wurzel-Anweisung · Regeltexte · Agentenprofil
│   │   │   │                            # · permissions.json · hooks.json · Vorlagen
│   │   │   ├── skills/                  # fw-* Referenz-Skills, eine Quelle je Skill
│   │   │   ├── role-packs/              # Ebene 6 – RP-DEV und RP-RE ausgeliefert
│   │   │   ├── tech-packs/              # Ebene 5 – Vorlage, kein konkretes Pack
│   │   │   └── org-policies/            # Ebene B: Einbindungspunkt + Klassifizierungs-Mapping
│   │   ├── templates/                   # Project-Overlay-Saat · Regelvorlagen · SKILL_TEMPLATE
│   │   ├── prompts/                     # Prompt-Bibliothek FW-PR-001…012 + README (Kap. 21)
│   │   ├── checklists/                  # FW-CL-01…11 + README (Kap. 22)
│   │   ├── decision-trees/              # FW-DT-01…06 + README (Kap. 23; Mermaid validiert)
│   │   ├── onboarding/                  # QUICKSTART · GUIDE · MENTOR_CHECKLIST · exercises/
│   │   │                                # · KNOWLEDGE_CHECK · COMPLETION_CRITERIA · REFERENCE
│   │   ├── examples/                    # ausschließlich synthetische Beispiele
│   │   ├── governance/                  # DECISION_LOG · RACI · PRIORITY_HIERARCHY
│   │   │                                # · RELEASE_PROCESS · change-requests/
│   │   │                                # · EXCEPTION/FEEDBACK/INCIDENT
│   │   ├── pilot/                       # PILOT_CONCEPT · METRICS (Kap. 27)
│   │   ├── docs/                        # ADOPTION_GUIDE · ROADMAP · RUNTIME_GLOSSARY
│   │   │                                # · PLACEHOLDER_REGISTRY
│   │   ├── tests/                       # TEST_CATALOG.md · protocols/ · scripts/ · erhebungen/
│   │   └── build/                       # Assemblierung dieses Dokuments (34 Kapitelquellen)
│   │
│   └── project-overlay/                 # EBENE 4 (austauschbar; Kap. 17)
│       ├── OVERLAY.md                   # 21 Abschnitte mit Ausfüllhinweisen
│       ├── overlay-manifest.yaml        # Register eingebundener Dokumente
│       ├── forbidden-terms.txt          # projektlokale Sperrbegriffe (verbleibt im Projekt)
│       ├── documents/<13 Typverzeichnisse>/  # freigegebene Dokumente/Auszüge + README
│       └── exceptions/EXCEPTIONS.md     # Ausnahmeregister des Projekts
│
└── <Produktivcode des Projekts>         # backend/, frontend/, src/, test/ …
```

**Warum diese Aufteilung.** Vor dieser Fassung lagen zwölf Kern-Verzeichnisse und vier Kern-Dateien direkt im Wurzelverzeichnis – neben dem Produktivcode des Projekts. Das machte die Übernahme fehleranfällig (was gehört zum Framework, was zum Projekt?) und das Wurzelverzeichnis unübersichtlich. Die Bündelung ändert nichts an der inhaltlichen Ebenenhierarchie (Kap. 7); sie trennt lediglich physisch, was ohnehin logisch getrennt war: Der Kern ist ein Ordner, den man ersetzt; das Projekt ist alles daneben.

**Die Laufzeitschicht ist Erzeugnis, nicht Quelle.** Kein Bestandteil von ihr wird von Hand geschrieben. Regeltexte, Skills, Agentenprofil, Berechtigungen und Hooks liegen einmal unter `.koolie/core/framework/runtime/` beziehungsweise `framework/skills/` und werden bei der Installation in die Form des gewählten Client Packs gebracht (Kap. 7a). Ein Client Pack selbst enthält **drei Dateien**: die Pfad- und Semantikabbildung (`manifest.json`), die Fähigkeitsmatrix (`CLIENT_PACK.md`) und eine erklärende README der Laufzeitschicht. Bis Release 0.25.0 waren es vier; die zweite README – die der Regelablage – ist mit 0.26.0 in die erste aufgegangen (D-36).

**Eine eigene Hook-Datei wird nicht erzeugt** (D-32, seit Release 0.26.0). Die Hook-Konfiguration steht bei beiden ausgelieferten Packs **in der Berechtigungsdatei** – nicht aus Bequemlichkeit, sondern weil dort gemessen ist, dass der Client sie liest: Aus der eigenen Hook-Datei führte ein Client **keinen** Hook aus, dieselbe Konfiguration in der Berechtigungsdatei löste sofort aus (`AP2-DD-10`). *Die Konfiguration steht dort, wo der Client sie nachweislich liest, nicht dort, wo seine Dokumentation sie nennt.*

**Grenze der Bündelung.** Die Wurzel-Anweisungsdatei und die Laufzeitschicht lassen sich nicht mitverschieben – beide Ladeorte sind Werkzeugkonvention und nicht konfigurierbar `[DOK]`. Die Laufzeitschicht enthält deshalb Kern- und Projektbestandteile gemischt. Genau diese Mischung löst `install.py` auf: **Core** wird bei `--update` überschrieben, **Saat** (Berechtigungsdatei, Overlay, Overlay-Regel) nur bei der Erstinstallation angelegt und danach nie wieder angefasst. `--check` meldet, wenn eine Core-Datei im Wurzelverzeichnis lokal verändert wurde – also an der falschen Stelle bearbeitet.

Damit sind alle geforderten Inhalte logisch abgebildet: zentrale Agentenanweisungen, Framework Core, Datenschutz- und Sicherheitsregeln (Core 02/03 plus Laufzeitregel 10), allgemeine Entwicklungsregeln (Core 04/06/07 plus Laufzeitregel 15), projektspezifisches Overlay, Rollenmodule, Technologiepakete, Skills, Skill-Vorlagen, Prompt-Vorlagen, Checklisten, Onboarding, Beispiele, Tests und Validierungen der Agentenanweisungen, Änderungsverzeichnis sowie Governance und Ownership.

## 15.3 Laufzeitschicht im Detail

Die folgende Dokumentationsdatei der Laufzeitschicht beschreibt verbindlich, was der KI-Client aus dem Repository liest, welche Mechanismen bewusst nicht verwendet werden, welche Sitzungsfreigaben zulässig sind – und, in einem eigenen Abschnitt, die Systematik der Regelablage:

{{EMBED-RAW:<RUNTIME_DIR>/README.md:1}}
Dass diese Systematik **hier** steht und nicht in der Regelablage selbst, ist eine Entscheidung dieses Releases: Der KI-Client führt jede Datei der Regelablage als Regel und macht sie damit ladbar – bei einem Pack sogar unbedingt. **Ein Verzeichnis, das als Regelmenge gelesen wird, enthält nur Regeln** (D-36); erklärender Text steht eine Ebene höher.

## 15.4 Zentrale Konfigurationsdateien

Die folgenden Dateien sind **erzeugt**. Sie stammen aus einer Referenzinstallation, die beim Bau dieses Dokuments angelegt wird – bei einem anderen Client Pack sehen sie anders aus, ohne dass sich eine Regel ändert. Die Quellen liegen unter `.koolie/core/framework/runtime/`. **Bei beiden ausgelieferten Packs zeigen Berechtigungsdatei und Hook-Konfiguration auf dieselbe Datei**; sie wird deshalb einmal abgedruckt, und die zweite Stelle verweist darauf – zweimal dieselbe Datei abzudrucken ließe den Leser einen Unterschied suchen, den es nicht gibt.

**Berechtigungen** – restriktiver Standard mit Kernregel-Integritätsblock. Die Regelmenge ist werkzeugneutral; Werkzeugnamen, Musterform und der Integritätsblock entstehen aus der Semantikabbildung des Client Packs (Kap. 7a, `clientmap.py`):

{{EMBED:<PERMISSIONS_FILE>:json}}
**Hooks** – technische Prüfung vor Werkzeugaufrufen sowie Statusmeldung beim Sitzungsstart (Mechanismus `[DOK]`, Skripte `[EMPF]`; die Skripte selbst tragen den Status `entwurf` – sie sind Werkzeuge und keine Modulträger und zählen für Kriterium 3 der 1.0.0-Definition nicht mit):

{{EMBED:<HOOKS_FILE>:json}}
**Subagentenprofil** – nur lesende Review-Zulieferung:

{{EMBED:<AGENTS_DIR>/fw-reviewer.md}}

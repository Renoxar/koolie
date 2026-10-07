# 15 Technische Referenzstruktur

## 15.1 Belegstatus und Durchsetzungstiefe

Die Struktur erfindet keine Client-Konventionen. Jede verwendete Konvention trägt einen **Belegstatus**:

| Status | Bedeutung |
|---|---|
| `[DOK]` | offiziell dokumentiert |
| `[EMPF]` | technisch begründete Empfehlung – aus dokumentierten Mechanismen abgeleitet, noch nicht in einer Installation ausgeführt |
| `[KONZ]` | konzeptioneller Vorschlag – Framework-Konvention ohne Produktbezug |
| `BELEG OFFEN` | noch nicht belegt, mit Grund und Datum |

Welcher Mechanismus in welcher Datei steht, ist eine Eigenschaft des Client Packs (Kap. 7a), nicht des Frameworks. Das Pack führt die Zuordnung versioniert und maschinenlesbar; dieses Kapitel bettet sie ein.

Der Belegstatus beantwortet die Frage „ist das dokumentiert?“. Die **Fähigkeitsmatrix** beantwortet die wichtigere: „setzt der Client es durch?“ Beide zusammen ergeben die Durchsetzungstiefe einer Zusage. Für das Client Pack, das dieses Dokument als durchgehendes Beispiel verwendet:

{{EMBED-RAW:.koolie/core/clients/devin-desktop/CLIENT_PACK.md:1}}
Die Spalte „Einstufung“ nennt die vorgesehene Durchsetzungstiefe, die Spalte „Beleg“ ihren Nachweisstand. Beide stehen je Zeile; ein Gesamturteil über eine Matrix gibt es nicht. Welche Zeilen an einer laufenden Installation beobachtet sind, sagt die Belegspalte. Bei diesem Pack sagt genau eine Zeile `BELEG OFFEN`, und zwar dauerhaft: Was ein Client indexiert, ist von außen nicht beobachtbar. Wo eine Messung die vorgesehene Einstufung widerlegt hat, steht das in der betreffenden Zeile.

## 15.2 Repository-Struktur

Der gesamte unveränderliche Kern liegt in **einem** Verzeichnis: `.koolie/core/`. Im Wurzelverzeichnis des Projekts steht nur, was dort stehen muss: die Wurzel-Anweisungsdatei und die Laufzeitschicht, weil der KI-Client sie nur dort findet, und `.koolie/project-overlay/` als austauschbare Projektkonfiguration. Wie diese Bestandteile heißen, entscheidet das Client Pack. Der Baum unten nennt sie deshalb mit Platzhaltern und gilt so für alle ausgelieferten Packs; Anhang 31.2 löst jeden Platzhalter je Pack auf.

Angelegt und aktualisiert werden die Wurzelbestandteile durch `.koolie/core/install.py` (Kap. 28):

| Aufruf | Wirkung |
|---|---|
| `install.py --target <projekt>` | kopiert nur `.koolie/core/`, nie ganz `.koolie/`, und installiert dann mit dem kopierten Skript. Unter Windows prüft es vorher, ob ein Pfad im Zielprojekt die Längengrenze überschreitet, und kopiert dann nichts |
| `install.cmd` (Windows), `install.command` (macOS) | Starter in der Wurzel des Release-Archivs; sie fragen Projektverzeichnis, Client Pack und Overlay-Muster ab |
| `--lieferumfang voll` \| `nutzung` | der ganze Kern oder der Kern ohne die Nachweisschicht (Änderungsanträge, Abnahmeprotokolle, Erhebungen, `build/`). Die Wahl steht in `.koolie/core/LIEFERUMFANG` und gilt beim Update weiter |
| `--overlay <muster>` | legt bei der Erstinstallation statt des leeren Overlays ein Overlay-Muster an: `general`, die Typmuster `java-spring`, `web-frontend` und `infrastructure`, das Party-Overlay `zoomies` oder mit `--overlay-quelle <pfad>` ein Muster eines Unternehmens |

Voraussetzung auf dem Zielrechner ist Python ab 3.8.

```text
<REPOSITORY_NAME>/                       # Projekt-Repository
├── <ROOT_INSTRUCTION_FILE>              # Wurzel-Anweisungsdatei (Kap. 16), erzeugt
├── <ROOT_INSTRUCTION_LOCAL>.example     # Vorlage persönliche Ergänzung, erzeugt
│                                        #   (nicht bei jedem Pack, siehe dessen Abschnitt 5)
├── <MCP_FILE>.example                   # MCP-Vorlage (Standard: keine Server), wo das
│                                        #   Pack eine eigene MCP-Datei hat
├── .gitignore                           # gehört dem Projekt; install.py meldet, welche
│                                        #   Kerndateien es ignoriert
├── <RUNTIME_DIR>/                       # LAUFZEITSCHICHT – vollständig erzeugt
│   ├── README.md                        # Mechanismen, Modi, Sitzungsfreigaben
│   ├── rules/                           # 00/10/15 Core-Kurzfassungen · 20 Overlay
│   │                                    # · 2N Overlay-Erweiterungen · 30 Role Packs
│   │                                    # · 40 Technology Packs · Vorlagen
│   │                                    # · je nach Pack eine Befehlsregeldatei
│   ├── skills/                          # koolie-*: Referenz-Skills und Skills
│   │                                    #   aktivierter Packs · prj-*: projekteigene
│   ├── agents/koolie-reviewer.md        # nur lesendes Review-Subagentenprofil
│   ├── <PERMISSIONS_FILE>               # Berechtigungen deny/ask/allow; im JSON-Format
│   │                                    #   mit Integritätsblock
│   └── <HOOKS_FILE>                     # Hook-Konfiguration – je nach Pack dieselbe
│                                        #   Datei wie <PERMISSIONS_FILE> (siehe unten)
│
├── .koolie/                             # ein Verzeichnis für Kern und Projektkonfiguration
│   ├── core/                            # DER KERN – byte-gleich zum Release
│   │                                    # (bei `nutzung` ohne die mit † markierten Ablagen)
│   │   ├── install.py                   # legt die Wurzelbestandteile an (--update / --check / --target)
│   │   ├── install_dialog.py            # Dialog hinter den Startern des Archivs
│   │   ├── banner.py                    # Banner der Installation
│   │   ├── clientmap.py                 # Semantikabbildung Berechtigungen und Hooks (Kap. 7a)
│   │   ├── koexistenz.py                # erkennt fremde Agenten-Rahmenwerke im Projekt
│   │   ├── mandat.py                    # Mandat und Modusbindung (M2–M6)
│   │   ├── wirksamkeit.py               # Wirksamkeitsprobe (install.py --probe)
│   │   ├── VERSION · CHANGELOG.md       # Versionsstand, Änderungsverzeichnis
│   │   ├── LICENSE · LICENSE-HINWEIS.md # Lizenz und Hinweis dazu
│   │   ├── LIEFERUMFANG                 # nur im Projekt: voll | nutzung
│   │   ├── OWNERS.md                    # Ownership je Bereich (Governance)
│   │   ├── clients/                     # ABBILDUNGSSCHICHT – je Client drei Bestandteile
│   │   │   ├── README.md · _template/   # Regeln der Schicht, Vorlage für neue Packs
│   │   │   ├── claude-code/             # CLIENT_PACK.md · manifest.json · root-template/
│   │   │   ├── cursor/                  # dito
│   │   │   ├── devin-desktop/           # dito
│   │   │   ├── kiro/                    # dito
│   │   │   └── openai-codex/            # dito
│   │   ├── framework/                   # KANONISCHE, WERKZEUGNEUTRALE EBENE
│   │   │   ├── core/00…10-*.md          # Framework Core, elf Module (Kap. 6, 10–14, 18, 25)
│   │   │   ├── runtime/                 # Laufzeitfassung, einmal für alle Clients:
│   │   │   │                            # Wurzel-Anweisung · Regeltexte · Agentenprofil
│   │   │   │                            # · permissions.json · hooks.json · Vorlagen
│   │   │   ├── skills/                  # koolie-* Referenz-Skills, eine Quelle je Skill
│   │   │   ├── role-packs/              # Ebene 6 – RP-DEV und RP-RE ausgeliefert
│   │   │   ├── tech-packs/              # Ebene 5 – Vorlage, kein konkretes Pack
│   │   │   ├── overlay-patterns/        # Overlay-Muster (--overlay <muster>)
│   │   │   └── org-policies/            # Ebene B: Einbindungspunkt + Klassifizierungs-Mapping
│   │   ├── templates/                   # Project-Overlay-Saat · Regelvorlagen · SKILL_TEMPLATE
│   │   ├── prompts/                     # Prompt-Bibliothek FW-PR-001…012 + README (Kap. 21)
│   │   ├── checklists/                  # FW-CL-01…11 + README (Kap. 22)
│   │   ├── decision-trees/              # FW-DT-01…06 + README (Kap. 23; Mermaid validiert)
│   │   ├── onboarding/                  # QUICKSTART · GUIDE · MENTOR_CHECKLIST · exercises/
│   │   │                                # · KNOWLEDGE_CHECK · COMPLETION_CRITERIA · REFERENCE
│   │   ├── examples/                    # ausschließlich synthetische Beispiele
│   │   ├── governance/                  # DECISION_LOG · RACI · PRIORITY_HIERARCHY
│   │   │                                # · RELEASE_PROCESS · ADOPTION_REGISTRY
│   │   │                                # · EXCEPTION/FEEDBACK/INCIDENT · change-requests/ †
│   │   ├── pilot/                       # PILOT_CONCEPT · METRICS (Kap. 27)
│   │   ├── docs/                        # ADOPTION_GUIDE · ROADMAP · RUNTIME_GLOSSARY
│   │   │                                # · PLACEHOLDER_REGISTRY
│   │   ├── tests/                       # TEST_CATALOG.md · EDGE_CASES.md · scripts/
│   │   │                                # · protocols/ † · erhebungen/ †
│   │   └── build/ †                     # Assemblierung dieses Dokuments aus den Kapitelquellen
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

**Warum diese Aufteilung.** Lägen die Dateien des Kerns direkt neben dem Produktivcode, wäre bei jeder Übernahme und Aktualisierung zu klären, was zum Framework gehört. Die Bündelung ändert nichts an der Ebenenhierarchie (Kap. 7); sie trennt physisch, was logisch getrennt ist: Der Kern ist ein Ordner, den man ersetzt, das Projekt ist alles daneben.

**Die Laufzeitschicht ist Erzeugnis, nicht Quelle.** Nichts darin wird von Hand geschrieben. Regeltexte, Skills, Agentenprofil, Berechtigungen und Hooks liegen einmal unter `.koolie/core/framework/runtime/` und `framework/skills/` und werden bei der Installation in die Form des Client Packs gebracht (Kap. 7a). Ein Client Pack besteht aus drei Bestandteilen: der Pfad- und Semantikabbildung (`manifest.json`), der Fähigkeitsmatrix (`CLIENT_PACK.md`) und der Vorlage der Wurzelbestandteile (`root-template/`) mit einer erklärenden README der Laufzeitschicht.

**Die Hook-Konfiguration steht dort, wo der Client sie nachweislich liest.** Bei `devin-desktop` und `claude-code` ist das die Berechtigungsdatei; eine eigene Hook-Datei führten diese Clients in der Messung nicht aus. `openai-codex`, `kiro` und `cursor` lesen eine eigene Hook-Datei (Block H der jeweiligen Matrix).

**Grenze der Bündelung.** Wurzel-Anweisungsdatei und Laufzeitschicht lassen sich nicht mitverschieben; beide Ladeorte sind Werkzeugkonvention und nicht konfigurierbar `[DOK]`. Die Laufzeitschicht enthält deshalb Kern- und Projektbestandteile gemischt, und `install.py` trennt sie:

| Bestandteil | Behandlung |
|---|---|
| **Core** | wird bei `--update` überschrieben |
| **Saat** (Berechtigungsdatei, Overlay, Overlay-Regel) | wird nur bei der Erstinstallation angelegt und danach nicht mehr angefasst |

`--check` meldet, wenn eine Core-Datei im Wurzelverzeichnis lokal verändert wurde, also an der falschen Stelle bearbeitet.

Damit sind alle geforderten Inhalte abgebildet: zentrale Agentenanweisungen, Framework Core, Datenschutz- und Sicherheitsregeln (Core 02/03 und Laufzeitregel 10), allgemeine Entwicklungsregeln (Core 04/06/07 und Laufzeitregel 15), Projekt-Overlay, Rollenmodule, Technologiepakete, Skills und Skill-Vorlagen, Prompt-Vorlagen, Checklisten, Onboarding, Beispiele, Tests und Validierung der Agentenanweisungen, Änderungsverzeichnis sowie Governance und Ownership.

## 15.3 Laufzeitschicht im Detail

Die Dokumentationsdatei der Laufzeitschicht beschreibt verbindlich, was der KI-Client aus dem Repository liest, welche Mechanismen bewusst nicht verwendet werden, welche Sitzungsfreigaben zulässig sind und, in einem eigenen Abschnitt, die Systematik der Regelablage:

{{EMBED-RAW:<RUNTIME_DIR>/README.md:1}}
Diese Systematik steht hier und nicht in der Regelablage selbst, weil der KI-Client jede Datei der Regelablage als Regel führt – bei einem Pack sogar unbedingt geladen. Ein Verzeichnis, das als Regelmenge gelesen wird, enthält nur Regeln; erklärender Text steht eine Ebene höher.

## 15.4 Zentrale Konfigurationsdateien

Die folgenden Dateien sind **erzeugt**. Sie stammen aus einer Referenzinstallation, die beim Bau dieses Dokuments angelegt wird; bei einem anderen Client Pack sehen sie anders aus, ohne dass sich eine Regel ändert. Die Quellen liegen unter `.koolie/core/framework/runtime/`. Wo Berechtigungsdatei und Hook-Konfiguration dieselbe Datei sind (`devin-desktop`, `claude-code`), wird sie einmal abgedruckt, und die zweite Stelle verweist darauf.

**Berechtigungen** – restriktiver Standard, bei einer Berechtigungsdatei im JSON-Format mit Kernregel-Integritätsblock. Die Regelmenge ist werkzeugneutral; Werkzeugnamen, Musterform und Integritätsblock entstehen aus der Semantikabbildung des Client Packs (Kap. 7a, `clientmap.py`):

{{EMBED:<PERMISSIONS_FILE>:permissions_format}}
**Hooks** – technische Prüfung vor Werkzeugaufrufen und Statusmeldung beim Sitzungsstart. Die Einstufung des Mechanismus steht in Block H der Fähigkeitsmatrix; die Skripte sind `[EMPF]` und tragen als Werkzeuge den Status `entwurf`:

{{EMBED:<HOOKS_FILE>:json}}
**Subagentenprofil** – nur lesende Review-Zulieferung:

{{EMBED:<AGENTS_DIR>/koolie-reviewer.md}}

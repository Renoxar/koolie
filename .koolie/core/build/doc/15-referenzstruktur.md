# 15 Technische Referenzstruktur

## 15.1 Belegstatus und Durchsetzungstiefe

Für die Struktur wurden keine Client-Konventionen erfunden. Jede verwendete Konvention trägt einen **Belegstatus** – **offiziell dokumentiert** `[DOK]`, **technisch begründete Empfehlung** `[EMPF]` (aus dokumentierten Mechanismen abgeleitet, noch nicht in einer Installation ausgeführt), **konzeptioneller Vorschlag** `[KONZ]` (Framework-Konvention ohne Produktbezug) oder **noch nicht belegt** (`BELEG OFFEN`, mit Grund und Datum).

Die Zuordnung von Mechanismen zu Dateinamen ist keine Eigenschaft des Frameworks, sondern eine des jeweiligen Client Packs (Kap. 7a) – dort wird sie geführt, versioniert und maschinenlesbar gehalten. Dieses Kapitel bettet sie ein, statt sie ein zweites Mal aufzuschreiben.

Der Belegstatus beantwortet die Frage „ist das dokumentiert?“. Die **Fähigkeitsmatrix** beantwortet die zweite, wichtigere: „setzt der Client es durch?“ Beide zusammen ergeben die Durchsetzungstiefe einer Zusage. Für das Client Pack, das dieses Dokument als durchgehendes Beispiel verwendet:

{{EMBED-RAW:.koolie/core/clients/devin-desktop/CLIENT_PACK.md:1}}
**Die Spalte „Einstufung“ nennt die vorgesehene Durchsetzungstiefe, die Spalte „Beleg“ ihren Nachweisstand** – beide stehen je Zeile, und das ist der Punkt: Ein Gesamturteil über eine Matrix gibt es nicht. Für dieses Pack ist Roadmap-AP2 abgeschlossen; welche Zeilen an einer laufenden Installation beobachtet sind, sagt die Belegspalte, und genau eine sagt noch `BELEG OFFEN` – dauerhaft, weil von außen nicht beobachtbar, was ein Client indexiert. **Zwei der Messungen sind zum Schlechteren ausgegangen**, haben also die zuvor vorgesehene Einstufung widerlegt; das steht in den betreffenden Zeilen und ist nicht eingeebnet worden.

## 15.2 Repository-Struktur

Der gesamte unveränderliche Kern liegt in **einem** Verzeichnis: `.koolie/core/`. Im Wurzelverzeichnis des Projekts stehen nur die Dinge, die dort stehen müssen: die Wurzel-Anweisungsdatei und die Laufzeitschicht, weil der KI-Client sie ausschließlich dort findet, sowie `.koolie/project-overlay/` als austauschbare Projektkonfiguration. Wie diese Bestandteile heißen, entscheidet das gewählte Client Pack. **Der Baum unten nennt sie deshalb mit ihren Platzhaltern** (D-310) – so gilt er für alle ausgelieferten Packs; Anhang 31.2 löst jeden davon je Pack auf.

Angelegt und aktualisiert werden die Wurzelbestandteile durch `.koolie/core/install.py`. Damit ist die Übernahme in ein Projekt das Kopieren eines Ordners und ein Skriptaufruf (Kap. 28). `install.py --target <projekt>` erledigt beides in einem Schritt: Es kopiert **nur** `.koolie/core/`, nie ganz `.koolie/` (D-354), und installiert danach mit dem kopierten Skript. Zwei Starter in der Wurzel des Release-Archivs, `install.cmd` für Windows und `install.command` für macOS, fragen die Angaben dafür ab – Projektverzeichnis, Client Pack, Overlay-Muster (D-362). Voraussetzung auf dem Zielrechner ist Python ab 3.8 (D-363). Unter Windows prüft `--target` vor der ersten Kopie, ob ein Pfad im Zielprojekt die Längengrenze reißt, und kopiert dann nichts (D-368). `--lieferumfang` wählt zwischen dem ganzen Kern (`voll`) und dem Kern ohne die Nachweisschicht aus Änderungsanträgen, Abnahmeprotokollen, Erhebungen und `build/` (`nutzung`); die Wahl steht im Projekt in `.koolie/core/LIEFERUMFANG` und gilt beim Heben weiter (D-367). `--overlay general` legt bei der Erstinstallation statt des leeren Overlays das Overlay-Muster *General Development* an (D-355).

```text
<REPOSITORY_NAME>/                       # Projekt-Repository
├── <ROOT_INSTRUCTION_FILE>              # Wurzel-Anweisungsdatei (Kap. 16), erzeugt
├── <ROOT_INSTRUCTION_LOCAL>.example     # Vorlage persönliche Ergänzung, erzeugt
│                                        #   (nicht bei jedem Pack, siehe dessen Abschnitt 5)
├── <MCP_FILE>.example                   # MCP-Vorlage (Standard: keine Server), wo das
│                                        #   Pack eine eigene MCP-Datei hat
├── .gitignore                           # gehört dem Projekt; install.py meldet, welche
│                                        #   Kerndateien es ignoriert (D-349)
├── <RUNTIME_DIR>/                       # LAUFZEITSCHICHT – vollständig erzeugt
│   ├── README.md                        # Mechanismen, Modi, Sitzungsfreigaben
│   ├── rules/                           # 00/10/15 Core-Kurzfassungen · 20 Overlay
│   │                                    # · 2N Overlay-Erweiterungen · 30 Role Packs
│   │                                    # · 40 Technology Packs · Vorlagen
│   │                                    # · je nach Pack eine Befehlsregeldatei
│   ├── skills/                          # fw-*: 12 Referenz-Skills · role-*/tech-*:
│   │                                    #   aktivierte Packs · prj-*: projekteigene
│   ├── agents/fw-reviewer.md            # nur lesendes Review-Subagentenprofil
│   ├── <PERMISSIONS_FILE>               # Berechtigungen deny/ask/allow; im JSON-Format
│   │                                    #   mit Integritätsblock
│   └── <HOOKS_FILE>                     # Hook-Konfiguration – je nach Pack dieselbe
│                                        #   Datei wie <PERMISSIONS_FILE> (D-32, siehe unten)
│
├── .koolie/                             # ein Verzeichnis für Kern und Projektkonfiguration
│   ├── core/                            # DER KERN – byte-gleich zum Release
│   │                                    # (bei `nutzung` ohne die mit † markierten Ablagen)
│   │   ├── install.py                   # legt die Wurzelbestandteile an (--update / --check / --target)
│   │   ├── install_dialog.py            # Dialog hinter den Startern des Archivs (D-362)
│   │   ├── clientmap.py                 # Semantikabbildung Berechtigungen und Hooks (Kap. 7a)
│   │   ├── VERSION · CHANGELOG.md       # Versionsstand, Änderungsverzeichnis
│   │   ├── LICENSE · LICENSE-HINWEIS.md # Lizenz und Hinweis dazu
│   │   ├── LIEFERUMFANG                 # nur im Projekt: voll | nutzung (D-367)
│   │   ├── OWNERS.md                    # Ownership je Bereich (Governance)
│   │   ├── clients/                     # ABBILDUNGSSCHICHT – je Client drei Dateien
│   │   │   ├── README.md · _template/   # Regeln der Schicht, Vorlage für neue Packs
│   │   │   ├── claude-code/             # CLIENT_PACK.md · manifest.json · root-template/
│   │   │   ├── devin-desktop/           # dito
│   │   │   └── openai-codex/            # dito
│   │   ├── framework/                   # KANONISCHE, WERKZEUGNEUTRALE EBENE
│   │   │   ├── core/00…10-*.md          # Framework Core, elf Module (Kap. 6, 10–14, 18, 25)
│   │   │   ├── runtime/                 # Laufzeitfassung, einmal für alle Clients:
│   │   │   │                            # Wurzel-Anweisung · Regeltexte · Agentenprofil
│   │   │   │                            # · permissions.json · hooks.json · Vorlagen
│   │   │   ├── skills/                  # fw-* Referenz-Skills, eine Quelle je Skill
│   │   │   ├── role-packs/              # Ebene 6 – RP-DEV und RP-RE ausgeliefert
│   │   │   ├── tech-packs/              # Ebene 5 – Vorlage, kein konkretes Pack
│   │   │   ├── overlay-patterns/        # Overlay-Muster general (--overlay general, D-355)
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

**Warum diese Aufteilung.** Lägen die Verzeichnisse und Dateien des Kerns direkt im Wurzelverzeichnis neben dem Produktivcode, wäre bei jeder Übernahme und Aktualisierung zu klären, was zum Framework gehört und was zum Projekt. Die Bündelung ändert nichts an der inhaltlichen Ebenenhierarchie (Kap. 7); sie trennt lediglich physisch, was ohnehin logisch getrennt ist: Der Kern ist ein Ordner, den man ersetzt; das Projekt ist alles daneben.

**Die Laufzeitschicht ist Erzeugnis, nicht Quelle.** Kein Bestandteil von ihr wird von Hand geschrieben. Regeltexte, Skills, Agentenprofil, Berechtigungen und Hooks liegen einmal unter `.koolie/core/framework/runtime/` beziehungsweise `framework/skills/` und werden bei der Installation in die Form des gewählten Client Packs gebracht (Kap. 7a). Ein Client Pack selbst enthält **drei Dateien**: die Pfad- und Semantikabbildung (`manifest.json`), die Fähigkeitsmatrix (`CLIENT_PACK.md`) und eine erklärende README der Laufzeitschicht (D-36).

**Die Hook-Konfiguration steht dort, wo der Client sie nachweislich liest, nicht dort, wo seine Dokumentation sie nennt** (D-32). Bei `devin-desktop` und `claude-code` ist das die **Berechtigungsdatei**; eine eigene Hook-Datei wird für sie nicht erzeugt, weil gemessen ist, dass ein Client aus ihr **keinen** Hook ausführte, während dieselbe Konfiguration in der Berechtigungsdatei sofort auslöste (`AP2-DD-10`). `openai-codex` führt die Hook-Konfiguration in einer eigenen Hook-Datei, die dieser Client nachweislich liest (sein Pack, Zeilen H1 bis H3).

**Grenze der Bündelung.** Die Wurzel-Anweisungsdatei und die Laufzeitschicht lassen sich nicht mitverschieben – beide Ladeorte sind Werkzeugkonvention und nicht konfigurierbar `[DOK]`. Die Laufzeitschicht enthält deshalb Kern- und Projektbestandteile gemischt. Genau diese Mischung löst `install.py` auf: **Core** wird bei `--update` überschrieben, **Saat** (Berechtigungsdatei, Overlay, Overlay-Regel) nur bei der Erstinstallation angelegt und danach nie wieder angefasst. `--check` meldet, wenn eine Core-Datei im Wurzelverzeichnis lokal verändert wurde – also an der falschen Stelle bearbeitet.

Damit sind alle geforderten Inhalte logisch abgebildet: zentrale Agentenanweisungen, Framework Core, Datenschutz- und Sicherheitsregeln (Core 02/03 plus Laufzeitregel 10), allgemeine Entwicklungsregeln (Core 04/06/07 plus Laufzeitregel 15), projektspezifisches Overlay, Rollenmodule, Technologiepakete, Skills, Skill-Vorlagen, Prompt-Vorlagen, Checklisten, Onboarding, Beispiele, Tests und Validierungen der Agentenanweisungen, Änderungsverzeichnis sowie Governance und Ownership.

## 15.3 Laufzeitschicht im Detail

Die folgende Dokumentationsdatei der Laufzeitschicht beschreibt verbindlich, was der KI-Client aus dem Repository liest, welche Mechanismen bewusst nicht verwendet werden, welche Sitzungsfreigaben zulässig sind – und, in einem eigenen Abschnitt, die Systematik der Regelablage:

{{EMBED-RAW:<RUNTIME_DIR>/README.md:1}}
Diese Systematik steht **hier** und nicht in der Regelablage selbst, weil der KI-Client jede Datei der Regelablage als Regel führt und damit ladbar macht – bei einem Pack sogar unbedingt. **Ein Verzeichnis, das als Regelmenge gelesen wird, enthält nur Regeln** (D-36); erklärender Text steht eine Ebene höher.

## 15.4 Zentrale Konfigurationsdateien

Die folgenden Dateien sind **erzeugt**. Sie stammen aus einer Referenzinstallation, die beim Bau dieses Dokuments angelegt wird – bei einem anderen Client Pack sehen sie anders aus, ohne dass sich eine Regel ändert. Die Quellen liegen unter `.koolie/core/framework/runtime/`. **Bei `devin-desktop` und `claude-code` zeigen Berechtigungsdatei und Hook-Konfiguration auf dieselbe Datei**; sie wird dann einmal abgedruckt, und die zweite Stelle verweist darauf – zweimal dieselbe Datei abzudrucken ließe den Leser einen Unterschied suchen, den es nicht gibt.

**Berechtigungen** – restriktiver Standard; bei einer Berechtigungsdatei im JSON-Format mit Kernregel-Integritätsblock. Die Regelmenge ist werkzeugneutral; Werkzeugnamen, Musterform und der Integritätsblock entstehen aus der Semantikabbildung des Client Packs (Kap. 7a, `clientmap.py`):

{{EMBED:<PERMISSIONS_FILE>:permissions_format}}
**Hooks** – technische Prüfung vor Werkzeugaufrufen sowie Statusmeldung beim Sitzungsstart (Einstufung des Mechanismus: Block H der Fähigkeitsmatrix des Packs, D-396; Skripte `[EMPF]`; die Skripte selbst tragen den Status `entwurf` – sie sind Werkzeuge und keine Modulträger und zählen für Kriterium 3 der 1.0.0-Definition nicht mit):

{{EMBED:<HOOKS_FILE>:json}}
**Subagentenprofil** – nur lesende Review-Zulieferung:

{{EMBED:<AGENTS_DIR>/fw-reviewer.md}}

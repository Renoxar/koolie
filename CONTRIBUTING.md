# Am Framework mitarbeiten

Diese Seite ist für alle, die **an Koolie selbst** arbeiten – nicht für Projekte, die Koolie benutzen. Wer
Koolie in ein Projekt übernehmen will, beginnt mit der [README](README.md) und dem
[Übernahmeleitfaden](.koolie/core/docs/ADOPTION_GUIDE.md).

## Nach dem Klonen

In **diesem** Repository sind die Wurzel-Anweisungsdatei, die Laufzeitschicht und `.koolie/project-overlay/`
**Erzeugnisse** und deshalb nicht versioniert (siehe `.gitignore`). Nach dem Klonen also einmal:

```bash
python .koolie/core/install.py
```

Damit gibt es keine zwei auseinanderlaufenden Fassungen derselben Kern-Datei.

> **Die so erzeugte Laufzeitschicht ist hier ein Prüfgegenstand, keine Schranke.** Wie in diesem Repository
> gearbeitet, gelesen und geändert wird, steht im Entwicklungsprofil des Quellrepositoriums,
> [`FRAMEWORK_DEV_PROFILE.md`](.koolie/core/governance/FRAMEWORK_DEV_PROFILE.md). Es wird in kein Zielprojekt
> installiert.

In einem **Projekt** gilt das Gegenteil: Dort werden Wurzel-Anweisungsdatei, Laufzeitschicht und
`.koolie/project-overlay/` versioniert. Die entsprechenden Zeilen der `.gitignore` sind beim Übernehmen deshalb
nicht mitzunehmen.

## Wo eine Änderung hingehört

Die gemeinsamen Quellen liegen **im Kern**, nicht im Client Pack:

| Was geändert werden soll | Quelle |
|---|---|
| Wurzel-Anweisungsdatei, Regeltexte, Berechtigungen, Hook-Konfiguration, Agentenprofile | `.koolie/core/framework/runtime/` |
| Skills | `.koolie/core/framework/skills/` |
| Overlay-Vorlage, Regelvorlagen | `.koolie/core/templates/` |
| Normativer Kern (FW-CORE-00…10) | `.koolie/core/framework/core/` |
| Pfad-, Werkzeug- und Hook-Abbildung eines Clients | `.koolie/core/clients/<client>/manifest.json` |
| Fähigkeitsmatrix eines Clients | `.koolie/core/clients/<client>/CLIENT_PACK.md` |
| Der Befehl `koolie` und die Pakete für PyPI und npm | `paketquellen/` |

Das `root-template/` eines Packs enthält **nur die README der Laufzeitschicht**; die gesamte Saat kommt aus
dem Kern. **Niemals in die erzeugte Laufzeitschicht im Wurzelverzeichnis schreiben** –
`install.py --check` deckt eine Bearbeitung an der falschen Stelle auf.

## Aufbau eines Projekts mit Koolie

Das gesamte unveränderliche Framework liegt in **einem** Verzeichnis: `.koolie/core/`. Im Wurzelverzeichnis
landen nur die Dinge, die ein KI-Client ausschließlich dort findet; **wie sie heißen, entscheidet das Client
Pack** – das [Laufzeitglossar](.koolie/core/docs/RUNTIME_GLOSSARY.md) löst jeden Platzhalter je Pack auf.

```text
<projekt>/
├── <Wurzel-Anweisungsdatei>             # Agentenanweisung (aus dem Kern installiert)
├── <Laufzeitschicht>/                   # vollständig erzeugt – nie von Hand schreiben
│   ├── <Berechtigungsdatei>             # Kernregeln + Projektwerte (je Pack: samt Hooks)
│   ├── agents/fw-reviewer.md            # nur lesendes Review-Subagentenprofil
│   ├── rules/00-, 10-, 15-*.md          # Core-Kurzfassungen ....... aus dem Kern
│   ├── rules/20-project-overlay.md      # Overlay-Laufzeitfassung ... Projekt
│   ├── rules/2N-overlay-*.md            # Overlay-Regelerweiterungen  Projekt
│   ├── rules/30-, 40-*.md               # aktivierte Packs
│   └── skills/fw-* role-* tech-* prj-*  # Kern | aktivierte Packs | Projekt
│
├── .koolie/
│   ├── core/                            # DER KERN: unveränderlich, byte-gleich
│   │   ├── install.py · clientmap.py    #   legt die Wurzeldateien an, bildet sie ab
│   │   ├── install_dialog.py            #   Dialog hinter install.cmd / install.command / koolie
│   │   ├── clients/                     #   Abbildung auf KI-Clients, je Client ein Pack
│   │   ├── framework/                   #   Kern, Laufzeitquellen, Skills, Role- und Tech-Packs
│   │   ├── prompts/ checklists/ decision-trees/ onboarding/ templates/ examples/
│   │   ├── governance/                  #   RACI, Prozesse, Decision Log, Änderungsanträge
│   │   ├── docs/                        #   Übernahmeleitfaden, Roadmap, Register
│   │   ├── tests/                       #   Testkatalog, Validator, Hook-Skripte, Protokolle
│   │   └── build/                       #   Assemblierung des Hauptdokuments
│   └── project-overlay/                 # gehört dem Projekt
│       ├── OVERLAY.md · overlay-manifest.yaml
│       ├── forbidden-terms.txt          # projektlokale Sperrbegriffe
│       └── documents/  exceptions/
│
└── <Projektcode>
```

## Framework prüfen

| Befehl | Prüft |
|---|---|
| `python .koolie/core/tests/scripts/validate-framework.py` | Struktur, Frontmatter, Skill-Konformität, verbotene Inhalte, Platzhalter – im Framework-Repository muss der Lauf fehlerfrei sein |
| `… --mermaid` | zusätzlich die Syntax aller Diagramme (benötigt `mmdc`) |
| `… --check-overlay-ready` / `… --strict-overlay` | Aktivierungsreife beziehungsweise aktiven Zustand eines Overlays – nur im Projekt sinnvoll; hier erwartungsgemäß rot |
| `python .koolie/core/tests/scripts/probe-pruefungen.py` | ob jede Prüfung des Validators einen bekannten Defekt meldet und ein fehlerfreier Baum durchkommt |
| [`TEST_CATALOG.md`](.koolie/core/tests/TEST_CATALOG.md) | das Verhalten des KI-Clients in Testsitzungen |

## Releases

Wie ein Release entsteht – Änderungsantrag, Prüfungen, signierte Marke, Archiv, Pakete und Veröffentlichung –,
steht in [`RELEASE_PROCESS.md`](.koolie/core/governance/RELEASE_PROCESS.md). Entscheidungen mit Begründung
führt das [`DECISION_LOG.md`](.koolie/core/governance/DECISION_LOG.md): `D-…` ist ein Decision Record, `K-…`
ein offener Klärungspunkt, `CR-…` ein Änderungsantrag unter `.koolie/core/governance/change-requests/`.

## Schnellzugriff nach Rolle

| Ich bin … | Startpunkt |
|---|---|
| neu im Team eines Projekts, das Koolie nutzt | [Onboarding-Quickstart](.koolie/core/onboarding/QUICKSTART.md), dann [`GUIDE.md`](.koolie/core/onboarding/GUIDE.md) |
| Entwicklerin oder Entwickler im Alltag | [`REFERENCE.md`](.koolie/core/onboarding/REFERENCE.md), [`01-preflight.md`](.koolie/core/checklists/01-preflight.md) |
| Reviewerin oder Reviewer | [`04-review-ai-code.md`](.koolie/core/checklists/04-review-ai-code.md), [`07-review-rules.md`](.koolie/core/framework/core/07-review-rules.md) |
| Overlay Owner / Projektleitung | [`ADOPTION_GUIDE.md`](.koolie/core/docs/ADOPTION_GUIDE.md), [`10-project-adoption.md`](.koolie/core/checklists/10-project-adoption.md), [`pilot/`](.koolie/core/pilot/) |
| Framework Owner | [`governance/`](.koolie/core/governance/), [`11-framework-release.md`](.koolie/core/checklists/11-framework-release.md), [`ROADMAP.md`](.koolie/core/docs/ROADMAP.md) |
| Sicherheit / Datenschutz | [`02-privacy.md`](.koolie/core/framework/core/02-privacy.md), [`03-security.md`](.koolie/core/framework/core/03-security.md), [`INCIDENT_HANDLING.md`](.koolie/core/governance/INCIDENT_HANDLING.md) |

## Konventionen

Verbindlichkeit über **MUSS/SOLL/KANN/DARF NICHT**; produktbezogene Aussagen tragen einen Belegstatus
`[DOK]`/`[EMPF]`/`[KONZ]` oder `BELEG OFFEN` mit Grund und Datum; variable Inhalte ausschließlich als
registrierte Platzhalter ([`PLACEHOLDER_REGISTRY.md`](.koolie/core/docs/PLACEHOLDER_REGISTRY.md)); Beispiele
sind stets als synthetisch gekennzeichnet; Personen werden nirgends genannt – nur Rollen.

Die Lizenzdatei liegt an **zwei** Stellen mit demselben Inhalt – in der Wurzel und unter
`.koolie/core/LICENSE` –, weil ein übernehmendes Projekt den Kern als Ganzes kopiert und ein Werk nicht ohne
seine Lizenz weitergegeben werden darf. Der Validator hält beide gegeneinander.

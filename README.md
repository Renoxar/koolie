# Framework für den professionellen Einsatz von Devin Desktop

Projektneutrales, wiederverwendbares Framework für den sicheren, kontrollierten und effizienten Einsatz von **Devin Desktop (ehemals Windsurf)** in Softwareentwicklungsteams – mit methodischem Vorgehensmodell und sofort nutzbarer technischer Referenzimplementierung. Erste Anwendung: strukturierte Einführung und Onboarding neuer Entwicklerinnen und Entwickler in einem bestehenden Projekt; Übertragung auf weitere Projekte über ein austauschbares Project Overlay.

**Version:** siehe `devin-core-framework/VERSION` · **Änderungen:** `devin-core-framework/CHANGELOG.md` · **Status:** alle Module `entwurf` (Validierung in Roadmap-AP2) · **Owner:** `<FRAMEWORK_OWNER>` (`devin-core-framework/OWNERS.md`)

## Leitidee in drei Sätzen

Devin ist ein unterstützendes Werkzeug – Verantwortung, Prüfung und Freigabe bleiben bei Menschen. Kontext wird bewusst und minimal bereitgestellt (Klassen K0–K3), Aufgaben werden eingestuft (Kontrollstufen niedrig/mittel/hoch) und in definierten Betriebsmodi (M1–M5) bearbeitet. Alles Projektspezifische lebt im austauschbaren Overlay; der Kern bleibt bei Projektwechseln unverändert.

## Aufbau: ein Ordner für den Kern, drei Dinge im Wurzelverzeichnis

Das gesamte unveränderliche Framework liegt in **einem** Verzeichnis: `devin-core-framework/`. Es in ein Projekt zu übernehmen heißt, diesen Ordner zu kopieren und ein Skript aufzurufen.

Im Wurzelverzeichnis landen nur die Dinge, die Devin ausschließlich dort findet:

| Pfad | Warum im Wurzelverzeichnis | Belegstatus |
|---|---|---|
| `AGENTS.md` | Zentrale Agentenanweisung, wird von Devin automatisch geladen | `[DOK]` |
| `.devin/` | Laufzeitschicht: `rules/`, `skills/`, `agents/`, `config.json`, `hooks.v1.json` | `[DOK]` |
| `project-overlay/` | Ebene 4, die austauschbare Projektkonfiguration – gehört dem Projekt | `[KONZ]` |

```text
<projekt>/
├── AGENTS.md                            # Agentenanweisung (aus dem Kern installiert)
├── AGENTS.local.md.example              # Vorlage persönliche Ergänzung
├── .devin/                              # Devin-Laufzeitschicht [DOK]
│   ├── config.json                      # Berechtigungen: Kernregeln + Projektwerte
│   ├── hooks.v1.json                    # PreToolUse-Schutzprüfung, SessionStart-Meldung
│   ├── agents/fw-reviewer.md            # nur lesendes Review-Subagentenprofil
│   ├── rules/00-, 10-, 15-*.md          # Core-Kurzfassungen ....... aus dem Kern
│   ├── rules/20-project-overlay.md      # Overlay-Laufzeitfassung ... Projekt
│   ├── rules/2N-overlay-*.md            # Overlay-Regelerweiterungen  Projekt
│   ├── rules/30-, 40-*.md               # aktivierte Packs .......... Projekt
│   └── skills/fw-*  |  skills/prj-*     # Kern-Skills | Projekt-Skills
│
├── devin-core-framework/                # ◀ DER KERN: ein Ordner, unveränderlich
│   ├── install.py                       #   legt die Wurzeldateien an, aktualisiert sie
│   ├── root-template/                   #   Quelle für AGENTS.md, .devin/, project-overlay/
│   ├── VERSION · CHANGELOG.md · OWNERS.md
│   ├── framework/                       #   kanonischer, werkzeugneutraler Kern
│   │   ├── core/                        #     FW-CORE-00…10
│   │   ├── role-packs/                  #     Ebene 6
│   │   ├── tech-packs/                  #     Ebene 5
│   │   └── org-policies/                #     Ebene 2
│   ├── prompts/                         #   FW-PR-001…012
│   ├── checklists/                      #   FW-CL-01…11
│   ├── decision-trees/                  #   FW-DT-01…06 (Mermaid validiert)
│   ├── onboarding/                      #   Quick-Start, Leitfaden, Übungen, Test
│   ├── templates/                       #   Skill-, Plan-, MR-Vermerk-Vorlagen
│   ├── examples/                        #   ausschließlich synthetische Beispiele
│   ├── governance/                      #   RACI, Hierarchie, Prozesse, Decision Log
│   ├── pilot/                           #   Pilotkonzept und Metriken
│   ├── docs/                            #   Adoption Guide, Roadmap, Platzhalterregister
│   ├── tests/                           #   Testkatalog + Validierungs- und Hook-Skripte
│   └── build/                           #   Assemblierung des Gesamtdokuments
│
├── project-overlay/                     # Ebene 4: gehört dem Projekt
│   ├── OVERLAY.md · overlay-manifest.yaml
│   ├── forbidden-terms.txt              # projektlokale Sperrbegriffe
│   ├── documents/                       # freigegebene Projektdokumente
│   └── exceptions/EXCEPTIONS.md
│
└── <Projektcode>                        # backend/, frontend/, src/ …
```

## Framework in ein Projekt übernehmen

```bash
# 1. Den Kern in das Projekt-Repository kopieren
cp -r devin-core-framework/ /pfad/zum/projekt/

# 2. Im Projekt die Wurzeldateien anlegen
cd /pfad/zum/projekt
python devin-core-framework/install.py

# 3. Overlay ausfüllen, dann prüfen
python devin-core-framework/tests/scripts/validate-framework.py --strict-overlay
```

`install.py` unterscheidet dabei **Kern** von **Projekt**:

| | wird bei `--update` überschrieben | bleibt unberührt |
|---|---|---|
| Kern | `AGENTS.md`, `.devin/rules/00-`, `10-`, `15-`, `.devin/skills/fw-*`, `.devin/agents/`, `hooks.v1.json`, die `*-TEMPLATE`-Vorlagen | – |
| Projekt | – | `.devin/config.json`, `.devin/rules/20-`, `2N-`, `30-`, `40-`, `.devin/skills/prj-*`, `project-overlay/**` |

Weitere Aufrufe:

| Befehl | Zweck |
|---|---|
| `python devin-core-framework/install.py --update` | Kern auf ein neues Release heben, Projektdateien behalten |
| `python devin-core-framework/install.py --check` | Prüfen, ob eine Kern-Datei lokal verändert wurde (Exit-Code 1, wenn ja) |
| `python devin-core-framework/install.py --dry-run` | Zeigen, was passieren würde |

Der ausführliche Weg mit allen Voraussetzungen, Freigaben und der Aktivierungsreihenfolge steht in `devin-core-framework/docs/ADOPTION_GUIDE.md`; der verbindliche Nachweis ist `devin-core-framework/checklists/10-project-adoption.md`.

## Arbeiten an diesem Repository

In **diesem** Repository sind `AGENTS.md`, `.devin/` und `project-overlay/` **Erzeugnisse** und deshalb nicht versioniert (siehe `.gitignore`). Quelle der Wahrheit ist `devin-core-framework/root-template/`. Nach dem Klonen also einmal:

```bash
python devin-core-framework/install.py
```

Damit gibt es keine zwei auseinanderlaufenden Fassungen derselben Kern-Datei. **Änderungen am Kern gehören nach `devin-core-framework/root-template/`**, nicht in das erzeugte `.devin/` im Wurzelverzeichnis – `install.py --check` deckt eine Bearbeitung an der falschen Stelle auf.

In einem **Projekt** gilt das Gegenteil: dort werden `AGENTS.md`, `.devin/` und `project-overlay/` versioniert. Die vier entsprechenden Zeilen der `.gitignore` sind beim Übernehmen deshalb nicht mitzunehmen.

## Schnellzugriff nach Rolle

| Ich bin … | Startpunkt |
|---|---|
| neu im Team | `devin-core-framework/onboarding/QUICKSTART.md`, dann `devin-core-framework/onboarding/GUIDE.md` |
| Entwicklerin oder Entwickler im Alltag | `devin-core-framework/onboarding/REFERENCE.md` (Spickzettel), `devin-core-framework/checklists/01-preflight.md`, Skills unter `.devin/skills/` |
| Reviewerin oder Reviewer | `devin-core-framework/checklists/04-review-ai-code.md`, `devin-core-framework/framework/core/07-review-rules.md` |
| Overlay Owner / Projektleitung | `devin-core-framework/docs/ADOPTION_GUIDE.md`, `project-overlay/OVERLAY.md`, `devin-core-framework/checklists/10-project-adoption.md`, `devin-core-framework/pilot/` |
| Framework Owner | `devin-core-framework/governance/`, `devin-core-framework/tests/TEST_CATALOG.md`, `devin-core-framework/checklists/11-framework-release.md`, `devin-core-framework/docs/ROADMAP.md` |
| Sicherheit / Datenschutz | `devin-core-framework/framework/core/02-privacy.md`, `03-security.md`, `.devin/config.json`, `devin-core-framework/governance/INCIDENT_HANDLING.md` |

## Framework prüfen

| Befehl | Prüft |
|---|---|
| `python devin-core-framework/tests/scripts/validate-framework.py` | Struktur, Frontmatter, Skill-Konformität, verbotene Inhalte, Platzhalter |
| `… --strict-overlay` | zusätzlich die Aktivierungsreife eines Overlays (nur im Projekt sinnvoll) |
| `… --mermaid` | zusätzlich die Syntax aller Diagramme (benötigt `mmdc`) |
| `devin-core-framework/tests/TEST_CATALOG.md` | das Verhalten von Devin (manuelle Testsitzungen) |

Im Framework-Repository ist `--strict-overlay` erwartungsgemäß rot: `project-overlay/` ist hier die Vorlage mit offenen Platzhaltern. Ohne das Flag muss der Lauf fehlerfrei sein.

## Wichtige Konventionen

Verbindlichkeit über **MUSS/SOLL/KANN/DARF NICHT**; produktbezogene Aussagen tragen Belegstatus `[DOK]`/`[EMPF]`/`[KONZ]` oder den Marker `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>`; variable Inhalte ausschließlich als registrierte Platzhalter (`devin-core-framework/docs/PLACEHOLDER_REGISTRY.md`); Beispiele sind stets als synthetisch gekennzeichnet; Personen werden nirgends genannt – nur Rollen.

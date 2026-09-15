# Leitwerk

**Framework für den professionellen Einsatz von KI-Codierassistenten in Softwareentwicklungsteams.**

Ein Leitwerk fliegt das Flugzeug nicht – es hält es stabil und auf Kurs. Genau das leistet dieses Framework: Es schreibt nicht vor, wie Software entsteht, sondern hält den KI-gestützten Entwicklungsprozess in einer Spur, die prüfbar, nachvollziehbar und übertragbar bleibt.

Projektneutral, wiederverwendbar und erweiterbar – mit methodischem Vorgehensmodell und sofort nutzbarer technischer Referenzimplementierung. Erste Anwendung: strukturierte Einführung und Onboarding neuer Entwicklerinnen und Entwickler in einem bestehenden Projekt; Übertragung auf weitere Projekte über ein austauschbares Project Overlay.

Welcher KI-Client zum Einsatz kommt, entscheidet ein **Client Pack** (`leitwerk-core/clients/`) – derzeit `devin-desktop` und `claude-code`. Der Kern ist werkzeugneutral; welche Zusagen ein Client technisch durchsetzt und welche nur als Anweisung im Kontext stehen, weist die Fähigkeitsmatrix des jeweiligen Packs aus.

**Version:** siehe `leitwerk-core/VERSION` · **Änderungen:** `leitwerk-core/CHANGELOG.md` · **Status:** alle Module `entwurf` (Validierung in Roadmap-AP2) · **Owner:** `<FRAMEWORK_OWNER>` (`leitwerk-core/OWNERS.md`)

## Leitidee in drei Sätzen

Devin ist ein unterstützendes Werkzeug – Verantwortung, Prüfung und Freigabe bleiben bei Menschen. Kontext wird bewusst und minimal bereitgestellt (Klassen K0–K3), Aufgaben werden eingestuft (Kontrollstufen niedrig/mittel/hoch) und in definierten Betriebsmodi (M1–M5) bearbeitet. Alles Projektspezifische lebt im austauschbaren Overlay; der Kern bleibt bei Projektwechseln unverändert.

## Aufbau: ein Ordner für den Kern, drei Dinge im Wurzelverzeichnis

Das gesamte unveränderliche Framework liegt in **einem** Verzeichnis: `leitwerk-core/`. Es in ein Projekt zu übernehmen heißt, diesen Ordner zu kopieren und ein Skript aufzurufen.

Im Wurzelverzeichnis landen nur die Dinge, die Devin ausschließlich dort findet:

| Pfad | Warum im Wurzelverzeichnis | Belegstatus |
|---|---|---|
| Wurzel-Anweisungsdatei | Zentrale Agentenanweisung, wird vom Client automatisch geladen | `[DOK]` |
| Laufzeitschicht | Regelablage, Skill-Ablage, Agentenprofile, Berechtigungsdatei, Hook-Konfiguration | `[DOK]` |
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
│   ├── rules/30-, 40-*.md               # aktivierte Packs .......... Kern-Inhalt,
│   │                                    #   Aktivierung ............. Projekt
│   └── skills/fw-* role-* tech-* prj-*  # Kern | aktivierte Packs | Projekt
│
├── leitwerk-core/                # ◀ DER KERN: ein Ordner, unveränderlich
│   ├── install.py                       #   legt die Wurzeldateien an, aktualisiert sie
│   ├── VERSION · CHANGELOG.md · OWNERS.md
│   ├── clients/                         #   Abbildung auf KI-Clients (keine Regelebene)
│   │   ├── README.md                    #     Zweck, Fähigkeitsmatrix, Erstellung
│   │   └── <client>/                    #     je Client:
│   │       ├── CLIENT_PACK.md           #       Pfadabbildung + Durchsetzungstiefe
│   │       └── root-template/           #       nur noch die README der Laufzeitschicht
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
cp -r leitwerk-core/ /pfad/zum/projekt/

# 2. Im Projekt die Wurzeldateien anlegen
cd /pfad/zum/projekt
python leitwerk-core/install.py

# 3. Overlay ausfüllen, dann prüfen
python leitwerk-core/tests/scripts/validate-framework.py --strict-overlay
```

`install.py` unterscheidet dabei **Kern** von **Projekt**:

| | wird bei `--update` überschrieben | bleibt unberührt |
|---|---|---|
| Kern | Wurzel-Anweisungsdatei, Regelablage `00-`, `10-`, `15-`, Skill-Ablage `fw-*`, Agentenprofile, die `*-TEMPLATE`-Vorlagen | – |
| Aktivierte Packs | ihre kopierten Bestandteile (Regelablage `30-`, `40-` und Skill-Ablage `role-*`, `tech-*`), sofern das Pack im Kern liegt | – |
| Projekt | – | Berechtigungsdatei **samt Hook-Konfiguration**, Regelablage `20-`, `2N-`, Skill-Ablage `prj-*`, `project-overlay/**`, projekteigene Packs |

> **Die Hook-Konfiguration wird von `--update` NICHT erneuert.** Bei beiden Packs steht sie in der Berechtigungsdatei, und die gehört dem Projekt: Sie wird nur bei der Erstinstallation angelegt. Das ist eine bewusste Eigentumsentscheidung – es heißt aber, dass eine Änderung an den Hooks eines Releases **von Hand nachzutragen** ist. Der jeweilige `CHANGELOG.md`-Eintrag nennt solche Fälle unter „Migrationshinweise"; zuletzt betraf es 0.30.0 (die Suchwerkzeuge im Schutz-Hook).

Weitere Aufrufe:

| Befehl | Zweck |
|---|---|
| `python leitwerk-core/install.py --update` | Kern auf ein neues Release heben, Projektdateien behalten |
| `python leitwerk-core/install.py --check` | Prüfen, ob eine Kern-Datei lokal verändert wurde (Exit-Code 1, wenn ja) |
| `python leitwerk-core/install.py --dry-run` | Zeigen, was passieren würde |

Der ausführliche Weg mit allen Voraussetzungen, Freigaben und der Aktivierungsreihenfolge steht in `leitwerk-core/docs/ADOPTION_GUIDE.md`; der verbindliche Nachweis ist `leitwerk-core/checklists/10-project-adoption.md`.

## Arbeiten an diesem Repository

In **diesem** Repository sind die Wurzel-Anweisungsdatei, die Laufzeitschicht und `project-overlay/` **Erzeugnisse** und deshalb nicht versioniert (siehe `.gitignore`). Nach dem Klonen also einmal:

```bash
python leitwerk-core/install.py
```

Damit gibt es keine zwei auseinanderlaufenden Fassungen derselben Kern-Datei.

> **Die so erzeugte Laufzeitschicht ist hier ein Prüfgegenstand, keine Schranke.** Wie in diesem Repositorium gearbeitet, gelesen und geändert wird, steht in `leitwerk-core/governance/FRAMEWORK_DEV_PROFILE.md` – dem Entwicklungsprofil des Quellrepositoriums. Es ist der zweite Einsatzkontext des Frameworks neben der Anwendung eines Releases in einem Projekt, und es ist ausdrücklich abgegrenzt: Es liegt unter `governance/` und wird in kein Zielprojekt installiert (D-56).

**Wo eine Änderung hingehört** – die gemeinsamen Quellen liegen seit `CR-2026-010` **im Kern**, nicht mehr im Client Pack:

| Was geändert werden soll | Quelle |
|---|---|
| Wurzel-Anweisungsdatei, Regeltexte, Berechtigungen, Hook-Konfiguration, Agentenprofile | `leitwerk-core/framework/runtime/` |
| Skills | `leitwerk-core/framework/skills/` |
| Overlay-Vorlage, Regelvorlagen | `leitwerk-core/templates/` |
| Normativer Kern (FW-CORE-00…10) | `leitwerk-core/framework/core/` |
| Pfad-, Werkzeug- und Hook-Abbildung eines Clients | `leitwerk-core/clients/<client>/manifest.json` |
| Fähigkeitsmatrix eines Clients | `leitwerk-core/clients/<client>/CLIENT_PACK.md` |

Das `root-template/` eines Packs enthält **nur noch die README der Laufzeitschicht**; `seed_paths` ist in beiden Manifesten leer, die gesamte Saat kommt aus dem Kern. **Niemals in die erzeugte Laufzeitschicht im Wurzelverzeichnis schreiben** – `install.py --check` deckt eine Bearbeitung an der falschen Stelle auf.

Welcher Client verwendet wird, entscheidet `--client`; `python leitwerk-core/install.py --list-clients` zeigt die verfügbaren. Welche Zusagen des Frameworks ein Client **technisch durchsetzt** und welche nur als Anweisung im Kontext stehen, steht in der Fähigkeitsmatrix seines Client Packs (`leitwerk-core/clients/README.md`).

In einem **Projekt** gilt das Gegenteil: dort werden Wurzel-Anweisungsdatei, Laufzeitschicht und `project-overlay/` versioniert. Die vier entsprechenden Zeilen der `.gitignore` sind beim Übernehmen deshalb nicht mitzunehmen.

## Schnellzugriff nach Rolle

| Ich bin … | Startpunkt |
|---|---|
| neu im Team | `leitwerk-core/onboarding/QUICKSTART.md`, dann `leitwerk-core/onboarding/GUIDE.md` |
| Entwicklerin oder Entwickler im Alltag | `leitwerk-core/onboarding/REFERENCE.md` (Spickzettel), `leitwerk-core/checklists/01-preflight.md`, Skills in der Skill-Ablage |
| Reviewerin oder Reviewer | `leitwerk-core/checklists/04-review-ai-code.md`, `leitwerk-core/framework/core/07-review-rules.md` |
| Overlay Owner / Projektleitung | `leitwerk-core/docs/ADOPTION_GUIDE.md`, `project-overlay/OVERLAY.md`, `leitwerk-core/checklists/10-project-adoption.md`, `leitwerk-core/pilot/` |
| Framework Owner | `leitwerk-core/governance/`, `leitwerk-core/tests/TEST_CATALOG.md`, `leitwerk-core/checklists/11-framework-release.md`, `leitwerk-core/docs/ROADMAP.md` |
| Sicherheit / Datenschutz | `leitwerk-core/framework/core/02-privacy.md`, `03-security.md`, Berechtigungsdatei, `leitwerk-core/governance/INCIDENT_HANDLING.md` |

## Framework prüfen

| Befehl | Prüft |
|---|---|
| `python leitwerk-core/tests/scripts/validate-framework.py` | Struktur, Frontmatter, Skill-Konformität, verbotene Inhalte, Platzhalter |
| `… --strict-overlay` | zusätzlich die Aktivierungsreife eines Overlays (nur im Projekt sinnvoll) |
| `… --mermaid` | zusätzlich die Syntax aller Diagramme (benötigt `mmdc`) |
| `leitwerk-core/tests/TEST_CATALOG.md` | das Verhalten von Devin (manuelle Testsitzungen) |

Im Framework-Repository ist `--strict-overlay` erwartungsgemäß rot: `project-overlay/` ist hier die Vorlage mit offenen Platzhaltern. Ohne das Flag muss der Lauf fehlerfrei sein.

## Wichtige Konventionen

Verbindlichkeit über **MUSS/SOLL/KANN/DARF NICHT**; produktbezogene Aussagen tragen Belegstatus `[DOK]`/`[EMPF]`/`[KONZ]` oder den Marker `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>`; variable Inhalte ausschließlich als registrierte Platzhalter (`leitwerk-core/docs/PLACEHOLDER_REGISTRY.md`); Beispiele sind stets als synthetisch gekennzeichnet; Personen werden nirgends genannt – nur Rollen.

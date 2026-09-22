# Koolie

**Framework für den professionellen Einsatz von KI-Codierassistenten in Softwareentwicklungsteams.**

Dieses Framework treibt die Entwicklung nicht und ersetzt niemanden – es hält sie beisammen und in Richtung: Es schreibt nicht vor, wie Software entsteht, sondern hält den KI-gestützten Entwicklungsprozess in einer Spur, die prüfbar, nachvollziehbar und übertragbar bleibt.

Projektneutral, wiederverwendbar und erweiterbar – mit methodischem Vorgehensmodell und sofort nutzbarer technischer Referenzimplementierung. Erste Anwendung: strukturierte Einführung und Onboarding neuer Entwicklerinnen und Entwickler in einem bestehenden Projekt; Übertragung auf weitere Projekte über ein austauschbares Project Overlay.

Welcher KI-Client zum Einsatz kommt, entscheidet ein **Client Pack** (`.koolie/core/clients/`) – derzeit `devin-desktop` und `claude-code`. Der Kern ist werkzeugneutral; welche Zusagen ein Client technisch durchsetzt und welche nur als Anweisung im Kontext stehen, weist die Fähigkeitsmatrix des jeweiligen Packs aus.

**Version:** siehe `.koolie/core/VERSION` · **Änderungen:** `.koolie/core/CHANGELOG.md` · **Status:** kein Modulträger auf `entwurf` – 77 von 77 stehen auf `pilot` · **Owner:** `<FRAMEWORK_OWNER>` (`.koolie/core/OWNERS.md`)

## Warum Koolie?

Ein **Koolie** ist ein australischer Hütehund, und das Bild ist die Aufgabenbeschreibung dieses Frameworks: Ein Hütehund treibt die Herde nicht, und er ersetzt den Schäfer nicht – er hält sie beisammen und in Richtung. Er arbeitet selbständig, aber auf Anweisung, und er hält Grenzen, ohne zu beißen.

Genau das tut dieses Framework mit einem KI-Client: Es macht ihn nicht besser, und es entscheidet nichts an seiner Stelle. Es hält ihn in der Spur, an den Grenzen und an den Stellen, an denen ein Mensch entscheidet – und es hält ihn an, bevor er schreibt.

Ein Koolie ist außerdem eine **Gebrauchsrasse, kein Schauhund**. Das ist hier ein Anspruch: Was in diesem Framework steht, muss im Alltag eines Projekts tragen, nicht in einer Vorführung gut aussehen.

Die Namensentscheidung mit ihrer Begründung und den verworfenen Alternativen steht als D-125 in `.koolie/core/governance/DECISION_LOG.md`.

## Leitidee in drei Sätzen

Der KI-Client ist ein unterstützendes Werkzeug – Verantwortung, Prüfung und Freigabe bleiben bei Menschen. Kontext wird bewusst und minimal bereitgestellt (Klassen K0–K3), Aufgaben werden eingestuft (Kontrollstufen niedrig/mittel/hoch) und in definierten Betriebsmodi (M1–M5) bearbeitet. Alles Projektspezifische lebt im austauschbaren Overlay; der Kern bleibt bei Projektwechseln unverändert.

## Aufbau: ein Ordner für den Kern, drei Dinge im Wurzelverzeichnis

Das gesamte unveränderliche Framework liegt in **einem** Verzeichnis: `.koolie/core/`. Es in ein Projekt zu übernehmen heißt, diesen Ordner zu kopieren und ein Skript aufzurufen.

Im Wurzelverzeichnis landen nur die Dinge, die ein KI-Client ausschließlich dort findet. **Wie sie heißen, entscheidet das Client Pack**; der Baum unten zeigt sie mit ihren Platzhaltern, das Laufzeitglossar (`.koolie/core/docs/RUNTIME_GLOSSARY.md`) löst jeden je Pack auf:

| Pfad | Warum im Wurzelverzeichnis | Belegstatus |
|---|---|---|
| Wurzel-Anweisungsdatei | Zentrale Agentenanweisung, wird vom Client automatisch geladen | `[DOK]` |
| Laufzeitschicht | Regelablage, Skill-Ablage, Agentenprofile, Berechtigungsdatei, Hook-Konfiguration | `[DOK]` |
| `.koolie/project-overlay/` | Ebene 4, die austauschbare Projektkonfiguration – gehört dem Projekt | `[KONZ]` |

```text
<projekt>/
├── <Wurzel-Anweisungsdatei>             # Agentenanweisung (aus dem Kern installiert)
├── <persönliche Ergänzung>.example      # Vorlage, nicht versioniert
├── <Laufzeitschicht>/                   # vollständig erzeugt – nie von Hand schreiben
│   ├── <Berechtigungsdatei>             # Kernregeln + Projektwerte – UND die Hooks
│   ├── agents/fw-reviewer.md            # nur lesendes Review-Subagentenprofil
│   ├── rules/00-, 10-, 15-*.md          # Core-Kurzfassungen ....... aus dem Kern
│   ├── rules/20-project-overlay.md      # Overlay-Laufzeitfassung ... Projekt
│   ├── rules/2N-overlay-*.md            # Overlay-Regelerweiterungen  Projekt
│   ├── rules/30-, 40-*.md               # aktivierte Packs .......... Kern-Inhalt,
│   │                                    #   Aktivierung ............. Projekt
│   └── skills/fw-* role-* tech-* prj-*  # Kern | aktivierte Packs | Projekt
│
├── .koolie/                             # Kern und Projektkonfiguration, ein Ordner
│   ├── core/                            # ◀ DER KERN: unveränderlich, byte-gleich
│   │   ├── install.py · clientmap.py    #   legt die Wurzeldateien an, bildet sie ab
│   │   ├── VERSION · CHANGELOG.md · OWNERS.md
│   │   ├── clients/                     #   Abbildung auf KI-Clients (keine Regelebene)
│   │   │   ├── README.md                #     Zweck, Fähigkeitsmatrix, Erstellung
│   │   │   └── <client>/                #     je Client DREI Dateien:
│   │   │       ├── CLIENT_PACK.md       #       Pfadabbildung + Durchsetzungstiefe
│   │   │       ├── manifest.json        #       dieselbe Abbildung maschinenlesbar
│   │   │       └── root-template/       #       die README der Laufzeitschicht
│   │   ├── framework/                   #   kanonischer, werkzeugneutraler Kern
│   │   │   ├── core/                    #     FW-CORE-00…10, elf Module
│   │   │   ├── runtime/                 #     Quelle der gesamten Laufzeitschicht
│   │   │   ├── skills/                  #     fw-* : die zwölf Referenz-Skills
│   │   │   ├── role-packs/              #     Ebene 6 – RP-DEV und RP-RE
│   │   │   ├── tech-packs/              #     Ebene 5 – Vorlage
│   │   │   └── org-policies/            #     Ebene B: Einbindungspunkt
│   │   ├── prompts/                     #   FW-PR-001…012
│   │   ├── checklists/                  #   FW-CL-01…11
│   │   ├── decision-trees/              #   FW-DT-01…06 (Mermaid validiert)
│   │   ├── onboarding/                  #   Quick-Start, Leitfaden, Übungen, Test
│   │   ├── templates/                   #   Overlay-Saat, Regel-, Skill-, MR-Vorlagen
│   │   ├── examples/                    #   ausschließlich synthetische Beispiele
│   │   ├── governance/                  #   RACI, Hierarchie, Prozesse, Decision Log
│   │   ├── pilot/                       #   Pilotkonzept und Metriken
│   │   ├── docs/                        #   Adoption Guide, Roadmap, Register
│   │   ├── tests/                       #   Testkatalog + Validierungs- und Hook-Skripte
│   │   └── build/                       #   Assemblierung des Hauptdokuments
│   │
│   └── project-overlay/                 # Ebene 4: gehört dem Projekt
│       ├── OVERLAY.md · overlay-manifest.yaml
│       ├── forbidden-terms.txt          # projektlokale Sperrbegriffe
│       ├── documents/                   # freigegebene Projektdokumente
│       └── exceptions/EXCEPTIONS.md
│
└── <Projektcode>                        # backend/, frontend/, src/ …
```

> **Eine eigene Hook-Datei gibt es nicht.** Bei beiden ausgelieferten Packs steht die
> Hook-Konfiguration **in der Berechtigungsdatei** – dort ist gemessen, dass der Client sie
> liest, und aus einer eigenen Hook-Datei wurde nachweislich kein Hook ausgeführt (D-32).

## Framework in ein Projekt übernehmen

```bash
# 1. Den Kern in das Projekt-Repository kopieren
cp -r .koolie/core/ /pfad/zum/projekt/

# 2. Im Projekt die Wurzeldateien anlegen
cd /pfad/zum/projekt
python .koolie/core/install.py

# 3. Overlay ausfüllen, dann prüfen
python .koolie/core/tests/scripts/validate-framework.py --strict-overlay
```

`install.py` unterscheidet dabei **Kern** von **Projekt**:

| | wird bei `--update` überschrieben | bleibt unberührt |
|---|---|---|
| Kern | Wurzel-Anweisungsdatei, Regelablage `00-`, `10-`, `15-`, Skill-Ablage `fw-*`, Agentenprofile, die `*-TEMPLATE`-Vorlagen | – |
| Aktivierte Packs | ihre kopierten Bestandteile (Regelablage `30-`, `40-` und Skill-Ablage `role-*`, `tech-*`), sofern das Pack im Kern liegt | – |
| Projekt | – | Berechtigungsdatei **samt Hook-Konfiguration**, Regelablage `20-`, `2N-`, Skill-Ablage `prj-*`, `.koolie/project-overlay/**`, projekteigene Packs |

> **Die Hook-Konfiguration wird von `--update` NICHT erneuert.** Bei beiden Packs steht sie in der Berechtigungsdatei, und die gehört dem Projekt: Sie wird nur bei der Erstinstallation angelegt. Das ist eine bewusste Eigentumsentscheidung – es heißt aber, dass eine Änderung an den Hooks eines Releases **von Hand nachzutragen** ist. Der jeweilige `CHANGELOG.md`-Eintrag nennt solche Fälle unter „Migrationshinweise"; zuletzt betraf es 0.30.0 (die Suchwerkzeuge im Schutz-Hook).

Weitere Aufrufe:

| Befehl | Zweck |
|---|---|
| `python .koolie/core/install.py --update` | Kern auf ein neues Release heben, Projektdateien behalten |
| `python .koolie/core/install.py --check` | Prüfen, ob eine Kern-Datei lokal verändert wurde (Exit-Code 1, wenn ja) |
| `python .koolie/core/install.py --dry-run` | Zeigen, was passieren würde |

Der ausführliche Weg mit allen Voraussetzungen, Freigaben und der Aktivierungsreihenfolge steht in `.koolie/core/docs/ADOPTION_GUIDE.md`; der verbindliche Nachweis ist `.koolie/core/checklists/10-project-adoption.md`.

## Arbeiten an diesem Repository

In **diesem** Repository sind die Wurzel-Anweisungsdatei, die Laufzeitschicht und `.koolie/project-overlay/` **Erzeugnisse** und deshalb nicht versioniert (siehe `.gitignore`). Nach dem Klonen also einmal:

```bash
python .koolie/core/install.py
```

Damit gibt es keine zwei auseinanderlaufenden Fassungen derselben Kern-Datei.

> **Die so erzeugte Laufzeitschicht ist hier ein Prüfgegenstand, keine Schranke.** Wie in diesem Repositorium gearbeitet, gelesen und geändert wird, steht in `.koolie/core/governance/FRAMEWORK_DEV_PROFILE.md` – dem Entwicklungsprofil des Quellrepositoriums. Es ist der zweite Einsatzkontext des Frameworks neben der Anwendung eines Releases in einem Projekt, und es ist ausdrücklich abgegrenzt: Es liegt unter `governance/` und wird in kein Zielprojekt installiert (D-56).

**Wo eine Änderung hingehört** – die gemeinsamen Quellen liegen seit `CR-2026-010` **im Kern**, nicht mehr im Client Pack:

| Was geändert werden soll | Quelle |
|---|---|
| Wurzel-Anweisungsdatei, Regeltexte, Berechtigungen, Hook-Konfiguration, Agentenprofile | `.koolie/core/framework/runtime/` |
| Skills | `.koolie/core/framework/skills/` |
| Overlay-Vorlage, Regelvorlagen | `.koolie/core/templates/` |
| Normativer Kern (FW-CORE-00…10) | `.koolie/core/framework/core/` |
| Pfad-, Werkzeug- und Hook-Abbildung eines Clients | `.koolie/core/clients/<client>/manifest.json` |
| Fähigkeitsmatrix eines Clients | `.koolie/core/clients/<client>/CLIENT_PACK.md` |

Das `root-template/` eines Packs enthält **nur noch die README der Laufzeitschicht**; `seed_paths` ist in beiden Manifesten leer, die gesamte Saat kommt aus dem Kern. **Niemals in die erzeugte Laufzeitschicht im Wurzelverzeichnis schreiben** – `install.py --check` deckt eine Bearbeitung an der falschen Stelle auf.

Welcher Client verwendet wird, entscheidet `--client`; `python .koolie/core/install.py --list-clients` zeigt die verfügbaren. Welche Zusagen des Frameworks ein Client **technisch durchsetzt** und welche nur als Anweisung im Kontext stehen, steht in der Fähigkeitsmatrix seines Client Packs (`.koolie/core/clients/README.md`).

In einem **Projekt** gilt das Gegenteil: dort werden Wurzel-Anweisungsdatei, Laufzeitschicht und `.koolie/project-overlay/` versioniert. Die vier entsprechenden Zeilen der `.gitignore` sind beim Übernehmen deshalb nicht mitzunehmen.

## Schnellzugriff nach Rolle

| Ich bin … | Startpunkt |
|---|---|
| neu im Team | `.koolie/core/onboarding/QUICKSTART.md`, dann `.koolie/core/onboarding/GUIDE.md` |
| Entwicklerin oder Entwickler im Alltag | `.koolie/core/onboarding/REFERENCE.md` (Spickzettel), `.koolie/core/checklists/01-preflight.md`, Skills in der Skill-Ablage |
| Reviewerin oder Reviewer | `.koolie/core/checklists/04-review-ai-code.md`, `.koolie/core/framework/core/07-review-rules.md` |
| Overlay Owner / Projektleitung | `.koolie/core/docs/ADOPTION_GUIDE.md`, `.koolie/project-overlay/OVERLAY.md`, `.koolie/core/checklists/10-project-adoption.md`, `.koolie/core/pilot/` |
| Framework Owner | `.koolie/core/governance/`, `.koolie/core/tests/TEST_CATALOG.md`, `.koolie/core/checklists/11-framework-release.md`, `.koolie/core/docs/ROADMAP.md` |
| Sicherheit / Datenschutz | `.koolie/core/framework/core/02-privacy.md`, `03-security.md`, Berechtigungsdatei, `.koolie/core/governance/INCIDENT_HANDLING.md` |

## Framework prüfen

| Befehl | Prüft |
|---|---|
| `python .koolie/core/tests/scripts/validate-framework.py` | Struktur, Frontmatter, Skill-Konformität, verbotene Inhalte, Platzhalter |
| `… --strict-overlay` | zusätzlich die Aktivierungsreife eines Overlays (nur im Projekt sinnvoll) |
| `… --mermaid` | zusätzlich die Syntax aller Diagramme (benötigt `mmdc`) |
| `.koolie/core/tests/TEST_CATALOG.md` | das Verhalten des KI-Clients (Testsitzungen an einer Installation) |

Im Framework-Repository ist `--strict-overlay` erwartungsgemäß rot: `.koolie/project-overlay/` ist hier die Vorlage mit offenen Platzhaltern. Ohne das Flag muss der Lauf fehlerfrei sein.

## Wichtige Konventionen

Verbindlichkeit über **MUSS/SOLL/KANN/DARF NICHT**; produktbezogene Aussagen tragen Belegstatus `[DOK]`/`[EMPF]`/`[KONZ]` oder `BELEG OFFEN` mit Grund und Datum; variable Inhalte ausschließlich als registrierte Platzhalter (`.koolie/core/docs/PLACEHOLDER_REGISTRY.md`); Beispiele sind stets als synthetisch gekennzeichnet; Personen werden nirgends genannt – nur Rollen.

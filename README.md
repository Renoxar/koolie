# Koolie

**Framework für den professionellen Einsatz von KI-Codierassistenten in Softwareentwicklungsteams.**

Dieses Framework treibt die Entwicklung nicht und ersetzt niemanden – es hält sie beisammen und in Richtung: Es schreibt nicht vor, wie Software entsteht, sondern hält den KI-gestützten Entwicklungsprozess in einer Spur, die prüfbar, nachvollziehbar und übertragbar bleibt.

Projektneutral, wiederverwendbar und erweiterbar – mit methodischem Vorgehensmodell und sofort nutzbarer technischer Referenzimplementierung. Erste Anwendung: strukturierte Einführung und Onboarding neuer Entwicklerinnen und Entwickler in einem bestehenden Projekt; Übertragung auf weitere Projekte über ein austauschbares Project Overlay.

Welcher KI-Client zum Einsatz kommt, entscheidet ein **Client Pack** (`.koolie/core/clients/`) – derzeit `devin-desktop`, `claude-code` und `openai-codex`. Der Kern ist werkzeugneutral; welche Zusagen ein Client technisch durchsetzt und welche nur als Anweisung im Kontext stehen, weist die Fähigkeitsmatrix des jeweiligen Packs aus.

**Version:** siehe `.koolie/core/VERSION` · **Änderungen:** `.koolie/core/CHANGELOG.md` · **Status:** kein Modulträger steht auf `entwurf`, alle stehen auf `pilot` · **Owner:** `<FRAMEWORK_OWNER>` (`.koolie/core/OWNERS.md`)

## Warum Koolie?

Ein **Koolie** ist ein australischer Hütehund, und das Bild ist die Aufgabenbeschreibung dieses Frameworks: Ein Hütehund treibt die Herde nicht, und er ersetzt den Schäfer nicht – er hält sie beisammen und in Richtung. Er arbeitet selbständig, aber auf Anweisung, und er hält Grenzen, ohne zu beißen.

Genau das tut dieses Framework mit einem KI-Client: Es macht ihn nicht besser, und es entscheidet nichts an seiner Stelle. Es hält ihn in der Spur, an den Grenzen und an den Stellen, an denen ein Mensch entscheidet – und es hält ihn an, bevor er schreibt.

Ein Koolie ist außerdem eine **Gebrauchsrasse, kein Schauhund**. Das ist hier ein Anspruch: Was in diesem Framework steht, muss im Alltag eines Projekts tragen, nicht in einer Vorführung gut aussehen.

Die Namensentscheidung mit ihrer Begründung und den verworfenen Alternativen steht als D-125 in `.koolie/core/governance/DECISION_LOG.md`.

> Kennungen in diesem Text: `D-…` ist ein Decision Record in `.koolie/core/governance/DECISION_LOG.md`, `K-…` ein offener Klärungspunkt in derselben Datei, `CR-…` ein Änderungsantrag unter `.koolie/core/governance/change-requests/`. Zum Handeln braucht man sie nicht – sie sagen, wo die Begründung steht.

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
│   ├── <Berechtigungsdatei>             # Kernregeln + Projektwerte (je Pack: samt Hooks)
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
│   │   ├── install_dialog.py            #   Dialog hinter install.cmd / install.command
│   │   ├── VERSION · CHANGELOG.md · OWNERS.md
│   │   ├── clients/                     #   Abbildung auf KI-Clients (keine Regelebene)
│   │   │   ├── README.md                #     Zweck, Fähigkeitsmatrix, Erstellung
│   │   │   └── <client>/                #     je Client drei Bestandteile:
│   │   │       ├── CLIENT_PACK.md       #       Pfadabbildung + Durchsetzungstiefe
│   │   │       ├── manifest.json        #       dieselbe Abbildung maschinenlesbar
│   │   │       └── root-template/       #       die README der Laufzeitschicht
│   │   ├── framework/                   #   kanonischer, werkzeugneutraler Kern
│   │   │   ├── core/                    #     FW-CORE-00…10, elf Module
│   │   │   ├── runtime/                 #     Quelle der gesamten Laufzeitschicht
│   │   │   ├── skills/                  #     fw-* : die zwölf Referenz-Skills
│   │   │   ├── role-packs/              #     Ebene 6 – RP-DEV und RP-RE
│   │   │   ├── tech-packs/              #     Ebene 5 – Vorlage
│   │   │   ├── overlay-patterns/        #     Overlay-Muster (--overlay general)
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

> **Wo die Hook-Konfiguration steht, entscheidet das Pack, und zwar nach Messung am
> Client.** Bei `devin-desktop` und `claude-code` steht sie in der Berechtigungsdatei,
> denn nur von dort führt der Client die Hooks aus (D-32). `openai-codex` liest die Hooks
> nur aus einer eigenen Datei (`.codex/hooks.json`), und seine Berechtigungsschicht
> zerfällt in ein Rechteprofil (`.codex/config.toml`) und eine Befehlsregeldatei
> (`.codex/rules/koolie.rules`, D-346). ⚠️ **Die gesamte projektlokale Schicht dieses
> Clients lädt nur, wenn das Projekt in seiner Benutzerkonfiguration als vertraut
> eingetragen ist, und dem Schutz-Hook muss zusätzlich einzeln vertraut werden** – beides
> liegt außerhalb des Repositoriums (`clients/openai-codex/CLIENT_PACK.md` Abschnitt 1b).

## Framework in ein Projekt übernehmen

**Mit dem Starter:** Das Release-Archiv entpacken und in seiner Wurzel
`install.cmd` (Windows) oder `install.command` (macOS) per Doppelklick starten. Der
Starter sucht ein Python ab 3.8 – ohne es nennt er den Installationsweg und hält an –
und fragt Projektverzeichnis, KI-Client, Overlay-Muster und Lieferumfang ab. Ein
**Overlay-Muster** ist ein vorbefülltes Overlay für einen häufigen Projekttyp – `general` trägt
allgemeine Pfadwerte und sechs Musterdokumente als Entwurf; ohne Muster beginnt das Overlay
leer. Es gibt nichts frei: Aktiviert wird das Overlay erst, wenn das Projekt es geprüft hat. Liegt im Projekt schon
ein Kern, bietet er das Heben an (D-362). Dahinter steht ein einziger Befehl, der ebenso direkt
aufrufbar ist:

```bash
python .koolie/core/install.py --target /pfad/zum/projekt [--client <name>] [--overlay general]
python .koolie/core/install.py --target /pfad/zum/projekt --update     # Projekt heben
python .koolie/core/install.py --target /pfad/zum/projekt --lieferumfang nutzung
```

**Der Lieferumfang:** `voll` – die Vorgabe – liefert den ganzen Kern;
`nutzung` lässt die Nachweisschicht weg – Änderungsanträge, Abnahmeprotokolle, Erhebungen
und den Bau des Hauptdokuments, zusammen der größere Teil der Dateien. Die Wahl gilt beim Heben
weiter (D-367).

`--target` kopiert **nur** `.koolie/core/` – aus einem Klon nur das Verfolgte – und ruft
danach die Installation im Projekt auf. Unter Windows muss der Projektpfad so kurz sein,
dass kein Pfad im kopierten Kern die Windows-Grenze von 259 Zeichen überschreitet; sonst
hält `--target` vor der ersten Kopie mit dieser Begründung an (D-368).

⚠️ Beim ersten Start warnt das System vor dem
unsignierten Starter: unter Windows SmartScreen (*„Weitere Informationen“ → „Trotzdem
ausführen“*), unter macOS Gatekeeper (*Systemeinstellungen → Datenschutz & Sicherheit →
„Dennoch öffnen“*; der sichere Weg ist das Terminal: `sh install.command`). Der
macOS-Starter ist unter Git Bash und Linux geprüft, auf macOS selbst noch nicht – die
Abnahme dort steht aus (`CR-2026-140`). Linux und andere Unix-Systeme nehmen `--target`
direkt oder den Handweg unten.

**Von Hand:**

```bash
# 1. Den Kern aus dem entpackten Release-Archiv in das Projekt-Repository kopieren
#    (Ziel ist <projekt>/.koolie/core – nicht <projekt>/core)
mkdir -p /pfad/zum/projekt/.koolie
cp -r .koolie/core /pfad/zum/projekt/.koolie/

# 2. Im Projekt die Wurzeldateien anlegen
#    (wahlweise mit vorbefülltem Overlay-Muster: --overlay general)
cd /pfad/zum/projekt
python .koolie/core/install.py

# 3. Overlay ausfüllen, dann die Aktivierungsreife prüfen
python .koolie/core/tests/scripts/validate-framework.py --check-overlay-ready

# 4. Overlay-Status auf aktiv setzen und den aktiven Zustand prüfen –
#    bis dahin arbeitet der Agent im Projekt nur lesend
python .koolie/core/tests/scripts/validate-framework.py --strict-overlay
```

> ⚠️ **Nur `.koolie/core/` kopieren – nie ganz `.koolie/`.** Daneben liegt das
> Kennzeichen des Framework-Repositoriums (`.koolie/QUELLREPOSITORIUM.md`), und zwar
> im Release-Archiv ebenso wie in einem Klon. Mitkopiert hält der Validator das Projekt
> für das Framework-Repositorium und meldet Fehler, deren Ursache er nicht nennt. Aus
> einem Klon kommt zusätzlich dessen eigenes Overlay mit (`.koolie/project-overlay/`)
> und **ersetzt beim Heben das des Projekts – ohne Meldung**, weil `install.py` das
> Overlay nie anfasst. `install.py` weist auf ein mitkopiertes Kennzeichen hin (D-354).
> `--target` kann diesen Fehler nicht machen: Es kopiert nur den Kern (D-362).

`install.py` unterscheidet dabei **Kern** von **Projekt**:

| | wird bei `--update` überschrieben | bleibt unberührt |
|---|---|---|
| Kern | Wurzel-Anweisungsdatei, Regelablage `00-`, `10-`, `15-`, Skill-Ablage `fw-*`, Agentenprofile, die `*-TEMPLATE`-Vorlagen; bei `openai-codex` zusätzlich die Hook-Datei und die Befehlsregeldatei | – |
| Aktivierte Packs | ihre kopierten Bestandteile (Regelablage `30-`, `40-` und Skill-Ablage `role-*`, `tech-*`), sofern das Pack im Kern liegt | – |
| Projekt | – | Berechtigungsdatei (bei `devin-desktop` und `claude-code` **samt Hook-Konfiguration**), Regelablage `20-`, `2N-`, Skill-Ablage `prj-*`, `.koolie/project-overlay/**`, projekteigene Packs |

> **Bei `devin-desktop` und `claude-code` erneuert `--update` die Hook-Konfiguration nicht.** Sie steht dort in der Berechtigungsdatei, und die gehört dem Projekt: Sie wird nur bei der Erstinstallation angelegt. Eine Änderung an den Hooks eines Releases ist deshalb **von Hand nachzutragen**; der jeweilige `CHANGELOG.md`-Eintrag nennt solche Fälle unter „Migrationshinweise“.
>
> **Bei `openai-codex` ist es umgekehrt:** Die Hook-Datei gehört zum Kern und wird bei jedem `--update` neu geschrieben. ⚠️ **Damit ändert sich ihr Hash, und der Client führt den Schutz-Hook erst wieder aus, wenn ihm erneut vertraut wurde** – ohne das läuft er gar nicht, und nichts meldet es (`CHANGELOG.md` zu 1.4.0, Migrationshinweise).

Weitere Aufrufe:

| Befehl | Zweck |
|---|---|
| `python .koolie/core/install.py --update` | Kern auf ein neues Release heben, Projektdateien behalten |
| `python .koolie/core/install.py --target <projekt> [--update] [--lieferumfang voll\|nutzung]` | Aus einem Klon oder entpackten Archiv den Kern in ein anderes Projekt kopieren und dort installieren oder heben, ganz oder ohne die Nachweisschicht; die Starter `install.cmd` und `install.command` fragen die Angaben ab |
| `python .koolie/core/install.py --check` | Prüfen, ob eine Kern-Datei lokal verändert wurde (Exit-Code 1, wenn ja) |
| `python .koolie/core/install.py --dry-run` | Zeigen, was passieren würde |
| `python .koolie/core/install.py --overlay general` | Erstinstallation mit dem Overlay-Muster *General Development*: drei Pfadplatzhalter vorbefüllt, in Overlay, Laufzeitfassung und Berechtigungsdatei, dazu sechs Musterdokumente allgemeiner Praktiken (Coding Guidelines, DoR, DoD, Qualität, Sicherheit, Branching), im Manifest als `entwurf` – verbindlich erst nach Freigabe durch den Overlay Owner; `--overlay` ohne Namen zählt die Muster auf |
| `python .koolie/core/install.py --list-clients` / `--list-skills` | Verfügbare Client Packs beziehungsweise die Skills dieser Installation auflisten |

Der ausführliche Weg mit allen Voraussetzungen, Freigaben und der Aktivierungsreihenfolge steht in `.koolie/core/docs/ADOPTION_GUIDE.md`; der verbindliche Nachweis ist `.koolie/core/checklists/10-project-adoption.md`.

## Arbeiten an diesem Repository

In **diesem** Repository sind die Wurzel-Anweisungsdatei, die Laufzeitschicht und `.koolie/project-overlay/` **Erzeugnisse** und deshalb nicht versioniert (siehe `.gitignore`). Nach dem Klonen also einmal:

```bash
python .koolie/core/install.py
```

Damit gibt es keine zwei auseinanderlaufenden Fassungen derselben Kern-Datei.

> **Die so erzeugte Laufzeitschicht ist hier ein Prüfgegenstand, keine Schranke.** Wie in diesem Repositorium gearbeitet, gelesen und geändert wird, steht in `.koolie/core/governance/FRAMEWORK_DEV_PROFILE.md` – dem Entwicklungsprofil des Quellrepositoriums. Es ist der zweite Einsatzkontext des Frameworks neben der Anwendung eines Releases in einem Projekt, und es ist ausdrücklich abgegrenzt: Es liegt unter `governance/` und wird in kein Zielprojekt installiert (D-56).

**Wo eine Änderung hingehört** – die gemeinsamen Quellen liegen **im Kern**, nicht im Client Pack (`CR-2026-010`):

| Was geändert werden soll | Quelle |
|---|---|
| Wurzel-Anweisungsdatei, Regeltexte, Berechtigungen, Hook-Konfiguration, Agentenprofile | `.koolie/core/framework/runtime/` |
| Skills | `.koolie/core/framework/skills/` |
| Overlay-Vorlage, Regelvorlagen | `.koolie/core/templates/` |
| Normativer Kern (FW-CORE-00…10) | `.koolie/core/framework/core/` |
| Pfad-, Werkzeug- und Hook-Abbildung eines Clients | `.koolie/core/clients/<client>/manifest.json` |
| Fähigkeitsmatrix eines Clients | `.koolie/core/clients/<client>/CLIENT_PACK.md` |

Das `root-template/` eines Packs enthält **nur die README der Laufzeitschicht**; `seed_paths` ist in allen drei Manifesten leer, die gesamte Saat kommt aus dem Kern. **Niemals in die erzeugte Laufzeitschicht im Wurzelverzeichnis schreiben** – `install.py --check` deckt eine Bearbeitung an der falschen Stelle auf.

Welcher Client verwendet wird, entscheidet `--client`; `python .koolie/core/install.py --list-clients` zeigt die verfügbaren. Welche Zusagen des Frameworks ein Client **technisch durchsetzt** und welche nur als Anweisung im Kontext stehen, steht in der Fähigkeitsmatrix seines Client Packs (`.koolie/core/clients/README.md`).

In einem **Projekt** gilt das Gegenteil: dort werden Wurzel-Anweisungsdatei, Laufzeitschicht und `.koolie/project-overlay/` versioniert. Die entsprechenden Zeilen der `.gitignore` sind beim Übernehmen deshalb nicht mitzunehmen.

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
| `… --check-overlay-ready` | zusätzlich die Aktivierungsreife eines Overlay-Kandidaten, dessen Status noch nicht `aktiv` ist (nur im Projekt sinnvoll, D-57) |
| `… --strict-overlay` | zusätzlich den aktiven Zustand eines Overlays (nur im Projekt sinnvoll) |
| `… --mermaid` | zusätzlich die Syntax aller Diagramme (benötigt `mmdc`) |
| `.koolie/core/tests/TEST_CATALOG.md` | das Verhalten des KI-Clients (Testsitzungen an einer Installation) |

Im Framework-Repository ist `--strict-overlay` erwartungsgemäß rot: `.koolie/project-overlay/` ist hier die Vorlage mit offenen Platzhaltern. Ohne das Flag muss der Lauf fehlerfrei sein.

## Wichtige Konventionen

Verbindlichkeit über **MUSS/SOLL/KANN/DARF NICHT**; produktbezogene Aussagen tragen Belegstatus `[DOK]`/`[EMPF]`/`[KONZ]` oder `BELEG OFFEN` mit Grund und Datum; variable Inhalte ausschließlich als registrierte Platzhalter (`.koolie/core/docs/PLACEHOLDER_REGISTRY.md`); Beispiele sind stets als synthetisch gekennzeichnet; Personen werden nirgends genannt – nur Rollen.

## Lizenz

Dieses Framework steht unter der **GNU General Public License, Version 3** (`LICENSE`) – es ist freie Software im Sinne der Open-Source-Definition. Copyright © 2026 `<FRAMEWORK_OWNER>`.

**Zusätzliche Erlaubnis nach §7 GPL-3.0:** Dateien, die aus den mitgelieferten Vorlagen entstehen, und jede Ausgabe der Werkzeuge dieses Frameworks unterliegen **nicht** dieser Lizenz. Das Urheberrecht daran liegt bei dem Projekt, das sie erzeugt hat.

**Die GPL bindet die Weitergabe, nicht den Gebrauch.** Wer dieses Framework benutzt – auch in einem Unternehmen, auch für ein kommerzielles Produkt –, hat keine einzige Pflicht daraus; das eigene Produkt ist keine Ableitung, und eigener Code neben `.koolie/core/` bleibt frei (§5, *mere aggregation*). Was im Einzelnen gilt und wo die eine wirklich berührte Stelle liegt, steht in `.koolie/core/LICENSE-HINWEIS.md`.

Die Lizenzdatei liegt an **zwei** Stellen und trägt an beiden denselben Inhalt: in der Wurzel und unter `.koolie/core/LICENSE`, weil ein übernehmendes Projekt den Kern als Ganzes kopiert und ein Werk ohne seine Lizenz weiterzugeben nach §4 GPL-3.0 unzulässig ist. **Prüfung 79 hält beide gegeneinander.**

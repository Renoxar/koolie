# Änderungsantrag `CR-2026-017`

| Feld | Inhalt |
|---|---|
| Titel | R2 und R3 abbilden: Der Client kennt Ladebedingungen, das Pack kannte sie nicht |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | `clients/claude-code/manifest.json`; `clients/claude-code/root-template/.claude/rules/README.md` (aus `.claude/framework/README.md`); `clients/claude-code/root-template/.claude/README.md`; `clients/claude-code/CLIENT_PACK.md`; `install.py`; `tests/scripts/validate-framework.py`; `templates/rules/*.template`; `docs/RUNTIME_GLOSSARY.md`; `docs/PLACEHOLDER_REGISTRY.md`; `clients/README.md`; `framework/role-packs/README.md`; `framework/tech-packs/README.md`; `build/doc/05-glossar.md`; `build/doc/07-architektur.md`; `build/doc/07a-abbildungsschicht.md`; `tests/protocols/2026-09-10-AP2-claude-code.md`; `governance/change-requests/CR-2026-016-ap2-claude-code.md` (Berichtigung, Abschnitt 6) |
| Ebene laut Entscheidungsbaum 6 | Abbildungsschicht (Client Pack) und Prüfwerkzeug |
| Art | Fehlerbehebung; betrifft die Grundlage der Technology Packs |
| Dringlichkeit | regulär – kein Projekt setzt das Pack produktiv ein |

## 1. Anlass und Problem

`AP2-CC-03` aus dem Validierungsprotokoll (`tests/protocols/2026-09-10-AP2-claude-code.md`)
hält fest, dass zwei Einstufungen der Fähigkeitsmatrix überholt sind. Die Berichtigung wurde
mit `CR-2026-016` ausdrücklich zurückgestellt, weil sie die Technology Packs betrifft und einen
eigenen Antrag braucht. Das ist dieser Antrag.

**R2 („Regeldateien mit Ladebedingungen") und R3 („Regeln an Dateimuster bindbar – Grundlage
der Technology Packs") standen auf `[NICHT ABBILDBAR]`**, begründet mit: „Regeltexte werden über
`@pfad`-Importe eingebunden und sind damit immer geladen." Das ist für Importe richtig und für
den Client falsch. `docs/en/memory`:

> „Place markdown files in your project's `.claude/rules/` directory. […] All `.md` files are
> discovered recursively […] Rules can be scoped to specific files using YAML frontmatter with
> the `paths` field. These conditional rules only apply when Claude is working with files
> matching the specified patterns. […] Rules without a `paths` field are loaded
> **unconditionally**."

Damit ist R3 wörtlich abgebildet und R2 mit einer benennbaren Einschränkung: Der Client kennt
**eine** Ladebedingung – die Bindung an Dateimuster –, die Kernquelle kennt **drei**
Ladetrigger.

**Drei Folgen, die über die beiden Matrixzeilen hinausgehen:**

1. **Die Importe waren nie nötig.** Eine Regeldatei ohne `paths` lädt von sich aus. Der ganze
   Mechanismus „Regeldatei plus Eintrag in der Wurzel-Anweisung" – samt der eigens dafür
   gebauten Validatorprüfung „nicht eingebunden, die Regel wäre wirkungslos" – beruhte auf einer
   falschen Annahme über den Client.

2. **Eine aktivierte Role-Pack-Regel war bei diesem Client wirkungslos.** `install.py` bindet
   nur die vier Core-Regeln ein. Ein Projekt, das ein Role Pack aktiviert, legte
   `30-role-<name>.md` in die Regelablage, wo sie mangels Import nie geladen wurde – der stille
   Fehlerfall, den das Client Pack selbst beschrieben hat, eingetreten am Framework-eigenen
   Mechanismus. Dieselbe Datei lief zudem nie durch `render_rule`: Die Formtransformation griff
   ausschließlich für `framework/runtime/rules/`, nicht für die Regelvorlagen und nicht für die
   Laufzeitfassungen der Packs.

3. **Ein Technology Pack hatte hier kein Zuhause.** Das Client Pack nannte zwei Ersatzwege –
   eine verschachtelte `CLAUDE.md` oder einen Import, der immer lädt. Der native Weg existierte
   die ganze Zeit.

**Ein vierter Befund kam bei der Umsetzung dazu.** Er ist nicht neu entstanden, sondern lag
bisher unter der Wahrnehmungsschwelle: `claudeMdExcludes` – setzbar auch in
`.claude/settings.local.json`, mit über alle Ebenen zusammengeführten Listen – nimmt Anweisungs-
und Regeldateien über ein Glob-Muster vom Laden aus. Das ist eine **Lockerung** durch
nutzerlokale Konfiguration und damit eine Lücke in B9. Vor dieser Änderung war sie größer, nicht
kleiner: Ein Muster auf die Wurzel-Anweisungsdatei hätte sämtliche importierten Regeltexte auf
einmal entfernt. Neu ist allein, dass wir sie kennen.

## 2. Vorgeschlagene Änderung

**Die Regelablage von `claude-code` liegt in `.claude/rules/`; der Client lädt sie selbst.**
`pack_runtime_dir` und `<RULES_DIR>` zeigen dorthin, `root_instruction_imports` ist leer, die
Marke `RUNTIME_IMPORTS` fällt in der erzeugten `CLAUDE.md` ersatzlos weg.

**Die Ladetrigger werden abgebildet, statt zu Kommentar zu werden.** Das Manifest führt
`rule_triggers` mit der Bedingungssprache des Clients und der Abbildung je Ladetrigger:

| Ladetrigger der Kernquelle | Fassung bei `claude-code` | Bewertung |
|---|---|---|
| `always_on` | kein `paths`-Feld | wörtliche Entsprechung |
| `model_decision` | kein `paths`-Feld | Verschärfung – mehr Regeln aktiv, nicht weniger |
| `glob` mit `globs` | `paths:` mit denselben Mustern | wörtliche Entsprechung |
| `manual`, `agent` | keine Abbildung | Die Installation scheitert |

`description` entfällt im Frontmatter, weil der Client es für Regeldateien nicht dokumentiert
(K-18); Zweck, Ladeverhalten und der Ladetrigger der Kernquelle stehen in einem HTML-Kommentar
oberhalb des Regeltextes. Der Regeltext selbst ist unverändert – wie bisher unterscheidet sich
zwischen den Packs nur die Form.

**Die Abbildung greift für alle drei Herkünfte einer Regeldatei**, nicht mehr nur für die
Core-Regeltexte: auch für die beiden Regelvorlagen unter `templates/rules/` und für die
Laufzeitfassungen aktivierter Role- und Technology Packs. Eine Pack-Regel, deren Ladebedingung
beim Rendern verfällt, wäre derselbe Befund, nur eine Ebene tiefer.

**Der Validator prüft die installierte Fassung an ihrer eigenen Form.** Drei Prüfungen für einen
Client mit eigener Bedingungssprache:

1. Ein Frontmatter-Feld, das der Client für Regeldateien nicht auswertet, ist ein Fehler (K-18).
   Ein stehen gebliebenes `trigger:` oder `globs:` heißt: Die Datei ist nicht durch die
   Abbildung gelaufen, ihre Ladebedingung ist verfallen.
2. Die Ladebedingung muss die Form haben, die der Client erwartet – bei `paths` eine nichtleere
   Liste von Mustern.
3. **Eine Kernregel (`00-`, `10-`, `15-`, `20-`) darf keine Ladebedingung tragen.** Sie gilt für
   jede Aufgabe; sie an Dateimuster zu binden wäre eine Lockerung. Diese Prüfung ist der Preis
   dafür, dass die Bindung an Dateimuster jetzt überhaupt möglich ist.

**Die Installation scheitert vollständig, nicht zur Hälfte.** `install.py` rendert alle
abzubildenden Quellen einmal, bevor es die erste Datei schreibt. Vorher brach eine nicht
abbildbare Quelle die Installation mitten im Schreiben ab und hinterließ ein halb angelegtes
Projekt. Das betrifft auch die Semantikabbildung der Berechtigungen aus D-18.

**Was verworfen wurde:**

- **Nur die Matrix berichtigen, die Mechanik lassen.** Genau die Lage, gegen die D-12 und D-26
  gerichtet sind: eine ausgewiesene Durchsetzungstiefe, hinter der die Abbildung zurückbleibt.
- **Nur Technology Packs nach `.claude/rules/`, die Core-Regeln über Importe lassen.** Ergäbe
  zwei Regelablagen mit zwei Lademechanismen bei einem Client und ließe den stillen Fehlerfall
  für die Role Packs bestehen.
- **`model_decision` an eine `paths`-Liste hängen, die alles trifft (`**/*`).** Eine Bedingung,
  die immer wahr ist, ist keine Bedingung – sie wäre nur schwerer zu lesen und würde zusätzlich
  vom Ladeverhalten abhängen (pfadgebundene Regeln laden beim Lesen einer Datei, nicht beim
  Sitzungsstart). Das wäre keine Verschärfung, sondern eine Lockerung.
- **`manual` und `agent` vorsorglich auf unbedingtes Laden abbilden.** Beide Ladetrigger sind im
  Kern von keinem Artefakt benutzt. Eine Abbildung zu erfinden, die nie geprüft wird, ist
  dasselbe Muster wie die wirkungslosen `Write(...)`-Regeln aus `CR-2026-016`. Ohne Eintrag
  scheitert die Installation und erzwingt die Entscheidung zu dem Zeitpunkt, an dem sie
  ansteht.
- **Die Importmechanik entfernen, weil sie kein Pack mehr nutzt.** Sie ist manifestgesteuert und
  bleibt für ein künftiges Pack erhalten; dass sie von keinem ausgelieferten Pack mehr erprobt
  ist, steht in der Roadmap unter „Bewusst offen gelassen". Ein Vorhalten mit ausgewiesenem
  Belegstand ist etwas anderes als ein Vorhalten mit behaupteter Wirkung.

**Mitgezogen, weil sonst falsch stehen bleibend:** Die Zeile S4 der Fähigkeitsmatrix stand noch
auf `[NICHT ABBILDBAR] – überholt`, obwohl `CR-2026-016` die Abbildung bereits ausgeliefert hat;
ebenso beschrieben die Abschnitte 1a, 4, 5 und 7 des Client Packs und die Laufzeit-README noch
die zwei Regeln je Pfad, die es seit 0.14.0 nicht mehr gibt. Diese Angaben sind nachgezogen. Sie
sind keine eigene Änderung, sondern die Berichtigung von Aussagen über bereits Geändertes.

## 3. Prüffragen (durch Owner auszufüllen)

- [x] Richtige Ebene nach Entscheidungsbaum 6? — Ja. Die Abbildungsschicht ist keine Regelebene. Geändert werden das Manifest eines Packs, seine beiden Laufzeit-READMEs und die zwei Skripte, die das Manifest auswerten. Die Regeltexte selbst sind unverändert.
- [x] Verschärfungsprinzip eingehalten? — Ja, und an einer Stelle ausdrücklich geprüft. `model_decision` bildet auf unbedingtes Laden ab: mehr Regeln aktiv, nicht weniger. Die einzige Stelle, an der die neue Fähigkeit eine Lockerung ermöglichen würde – eine Kernregel an Dateimuster zu binden –, ist als Validatorfehler ausgeschlossen und mit Sonde S2 belegt.
- [x] Widerspruchsfreiheit geprüft? — Der Widerspruch zwischen der Fähigkeitsmatrix (`[NICHT ABBILDBAR]`) und dem Client ist der Anlass. Nach der Änderung trägt keine Zeile mehr diese Einstufung, und alle Aussagen über den Lademechanismus in Pack, READMEs, Glossar und Platzhalterregister nennen dieselbe Mechanik.
- [x] Laufzeitfassungen betroffen? — Ja, bei `claude-code`: Die Regelablage wird umbenannt, alle Regeltexte werden neu erzeugt, `CLAUDE.md` verliert den Importblock. Migrationshinweis im CHANGELOG. `devin-desktop` ist unberührt – ohne `rule_triggers` ist die Abbildung die Identität, und `install.py --check` gegen das Framework-Repository meldet keine Abweichung.
- [x] Belegstatus korrekt? — Jede Aussage über den Client stützt sich auf `docs/en/memory` der Clientversion 2.1.267, im Protokoll mit Zitat. Belegt ist `[DOK]`, nicht beobachtete Durchsetzung: Dass eine Regel ohne `paths` geladen **wird**, ist dokumentiert; dass sie in einer laufenden Sitzung tatsächlich im Kontext steht, ist ein Wirkungsnachweis und steht aus.
- [x] Test- und Validierungsbedarf? — Sechs Sonden nach D-23, alle gemeldet, dazu vier Gegenproben (Abschnitt 5). `FW-KO-01`, `FW-KO-02` und `FW-VN-01` sind unberührt; die Skill-Testfälle je `TESTS.md` bleiben offen (AP2).
- [x] Auswirkungen auf Overlays und laufende Onboardings? — Kein Projekt setzt `claude-code` produktiv ein; das Übungsrepository nutzt `devin-desktop`. Ein künftiges Projekt mit diesem Pack bekommt seine Regeln in `.claude/rules/` und kann Technology Packs erstmals an Dateimuster binden.
- [x] Dokumentation? — CHANGELOG, Decision Log, Roadmap, Client Pack, beide Laufzeit-READMEs, Glossar, Platzhalterregister, AP2-Protokoll.

## 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | angenommen |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Dasselbe Muster wie bei `CR-2026-016`, eine Ebene weiter: Das Pack hat den Client unterschätzt und einen Ersatz gebaut, wo eine native Kontrolle existiert. Der Unterschied ist, dass hier keine Schutzzusage verfiel, sondern eine Grundlage fehlte – Technology Packs galten bei diesem Client als nicht abbildbar, und eine aktivierte Role-Pack-Regel wurde stillschweigend nie geladen. Eine Fähigkeitsmatrix, die weniger behauptet, als der Client kann, ist weniger gefährlich als eine, die mehr behauptet, aber sie kostet genau die Mechanismen, für die es das Framework gibt. |
| Ziel-Release | 0.15.0 |
| Decision-Log-Eintrag | D-27 |

## 5. Umsetzung (nach Annahme)

- [x] `rule_triggers` im Manifest; `pack_runtime_dir` und `<RULES_DIR>` auf `.claude/rules`; `root_instruction_imports` leer; `has_rule_triggers` auf `true`
- [x] `render_rule` bildet die Ladetrigger ab; `ist_regelquelle` erfasst zusätzlich `templates/rules/` und die Pack-Laufzeitfassungen
- [x] `install.py` rendert alle Quellen vor der ersten Schreiboperation und bricht sauber ab (`pruefe_abbildung`)
- [x] Validator: Feldprüfung nach K-18, Formprüfung der Ladebedingung, Verbot einer Ladebedingung an Kernregeln
- [x] Client Pack auf 0.6.0: R2, R3 und S4 auf `[TECHNISCH]`; `[NICHT ABBILDBAR]` 4 → **0**; Abschnitt 1b neu; die Restangaben zu AP2-CC-02 in 1a, 4, 5 und 7 nachgezogen
- [x] Beide Laufzeit-READMEs des Packs neu geschrieben; Glossar, Platzhalterregister und `clients/README.md` nachgezogen
- [x] Regelvorlagen von der Akteursbezeichnung „Devin" und von client-gebundenen Feldnamen gelöst
- [x] **Wirksamkeitsnachweis (D-23), sechs Sonden, alle gemeldet:** `trigger:` im Frontmatter stehen gelassen; `paths` an einer Kernregel; `paths` als Zeichenkette; `paths` als leere Liste; Ladetrigger `manual` ohne Abbildung (Installation scheitert); `trigger: glob` ohne `globs` (Installation scheitert). Vier Gegenproben: korrektes Technology Pack, Regeldatei ohne Frontmatter, und die beiden Prüfungen aus `CR-2026-016` melden weiterhin
- [x] `install.py --client claude-code` gefolgt von `validate-framework.py`: 0 Fehler
- [x] Framework-Repository (`devin-desktop`): Validator 0 Fehler, 0 Warnungen; `install.py --check` unverändert; `build/assemble.py` baut
- [ ] **Folgearbeit:** Die Wirkungsnachweise aus einer Sitzung *in* der Installation stehen weiter aus. Dazu gehört seit diesem Release ein zweiter: dass eine Regel ohne `paths` tatsächlich im Kontext steht und eine Regel mit `paths` erst beim Lesen einer passenden Datei
- [ ] **Folgearbeit:** Die Lücke in B9 durch `claudeMdExcludes` ist beschrieben, nicht geschlossen. Ob sie sich schließen lässt – etwa über verwaltete Einstellungen –, ist eine Frage an AP2 für die Enterprise-Marker
- [ ] **Folgearbeit:** Die Importmechanik der Wurzel-Anweisung ist von keinem ausgelieferten Pack mehr erprobt

## 6. Berichtigung an `CR-2026-016`

Der dritte Befund jenes Antrags ist dort als „AP2-CC-03" bezeichnet; im Protokoll trägt er die
Nummer **AP2-CC-09**. `AP2-CC-03` ist die Nummer des Befundes, um den es hier geht. Die
Bezeichnung im Antrag ist entsprechend berichtigt; der Sachverhalt bleibt unverändert.

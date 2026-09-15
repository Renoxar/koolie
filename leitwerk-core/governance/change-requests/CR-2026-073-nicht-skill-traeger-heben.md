# Änderungsantrag `CR-2026-073`

| Feld | Inhalt |
|---|---|
| Titel | Die Vorentscheidung `K-36` ist beantwortet – der Gegenstand von Kriterium 3 ist vollständig, das Statusvokabular durchgesetzt und das erste Nicht-Skill-Bündel abgenommen |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-15 |
| Betroffene Artefakte | `framework/core/00-principles.md` bis `framework/core/10-error-escalation.md` (elf Module), `prompts/README.md`, `checklists/01-preflight.md` bis `checklists/11-framework-release.md` (elf Checklisten), `governance/RELEASE_PROCESS.md`, `governance/DECISION_LOG.md` (D-105 bis D-108, K-36, K-38), `tests/scripts/validate-framework.py` (Prüfung 47, Register, Sondenmenge), `tests/scripts/probe-pruefungen.py` (fünf Sonden, drei Gegenproben, Sondenmenge), `tests/TEST_CATALOG.md` (FW-KO-01), `docs/ROADMAP.md` (Standzeile, Kriterientabelle, AP3, P3-Posten, Abschnitte zu 0.50.0 und 0.51.0), `CHANGELOG.md`, `tests/protocols/2026-09-15-gegenpruefung-nicht-skill-traeger.md`, `tests/protocols/2026-09-15-wirkungsnachweise-0.51.0.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind die Definition des Modulträgers, sein Lebenszyklus und der Status der Module des Frameworks selbst |
| Art | Änderung (Definition, Statuswechsel), Ergänzung (Statuszeile, Prüfung 47) |
| Dringlichkeit | **Regulär.** Kein Sicherheitsbezug. Der Gegenstand ist Kriterium 3 von D-11 und die zweite Aktivität von `AP3` (P1) |

## 1. Anlass

Die Übergabe nennt als Kandidat 1 *„die 52 Nicht-Skill-Träger heben"* und stellt dem
Vorgang eine Vorentscheidung voran: **`K-36` – tragen die elf Module unter
`framework/core/` eine Statuszeile?** Die Lehre aus den beiden Vorgängern gilt weiter:
**Die Bedingung wird geprüft, bevor die Aufgabe begonnen wird.**

Bei 0.49.0 war die Bedingung falsch **gewählt** und hielt zweiunddreißig Releases auf.
Bei 0.50.0 war sie falsch **gelesen**. **Diesmal ist sie richtig gestellt und die Zahl
daneben:** `K-36` nennt elf Träger. Es sind zwölf.

### 1.1 Die Messung

`prompts/README.md` führt denselben Steckbrief wie die elf Kernmodule – Ebene,
Verbindlichkeit, Owner, Version – und keine Statuszeile. Es ist ein normatives Dokument
(Steckbriefzeile: *„normativ (Abschnitte 2, 3, 5, 6, 7)"*) mit eigenen nummerierten
Regeln. `K-36` hat es nicht gesehen, weil nur `framework/core/` abgesucht worden war.

| Gemessen am 2026-09-15 | Zahl |
|---|---|
| `.md`-Dateien im Zählbereich von Prüfung 46 | 167 |
| davon mit Steckbrief | **81** |
| davon **mit** Statuszeile | 69 |
| davon **ohne** Statuszeile | **12** – elf Kernmodule und `prompts/README.md` |

## 2. Der eigentliche Befund: die Definition lässt ihren Gegenstand entkommen

`01-governance.md` Abschnitt 5 Punkt 1 sagte bis 0.50.0:

> **Modulträger** ist jede versionierte Datei des Frameworks, die in ihrem Steckbrief eine
> Zeile `\| Status \| … \|` führt

**Das ist selbstbezüglich.** Modulträger ist, wer die Statuszeile führt – also entkommt
dem Lebenszyklus, wer sie weglässt. Zwölf Dateien taten genau das, darunter die **elf
normativsten Dokumente des Frameworks**.

**Und der Gründungstext von D-11 meint sie ausdrücklich.** `CR-2026-001`, der Antrag, der
D-09 durch D-11 ersetzt hat, formuliert Kriterium 3 wörtlich:

> 3. Alle **Core-Module**, Skills und Packs haben einen Status oberhalb von `entwurf`.

Dieselbe Formulierung steht im Prüfpunkt von `FW-CL-11`, der Checkliste, die 1.0.0
freigibt. **Kriterium 3 hat die elf also nie ausgenommen; keine Zählregel hat sie je
gesehen.** Das ist derselbe Befundtyp wie bei allen vier Zählregeln von 0.48.0: nicht
falsch geschrieben, sondern das richtige Ergebnis einer Regel, die weniger kann als ihr
Kriterium verlangt.

## 3. Der zweite Befund, der nicht gesucht war: eine zweite Übergangsbedingung

`prompts/README.md` Abschnitt 7 trägt seit der Erstfassung:

> Alle Vorlagen liegen im Status `entwurf`. Der Übergang nach `pilot` setzt voraus:
> Validierung bestanden, **mindestens eine dokumentierte Testsitzung je Vorlage auf dem
> Übungsrepository**, Review durch `<FRAMEWORK_OWNER>`.

**Das ist eine eigene, strengere Übergangsbedingung für zwölf Modulträger, und sie steht
in keinem Register.** Sie kettet Kriterium 3 von D-11 an Kriterium 2 – seinen mit Abstand
größten Posten, der Modellzeit und ein Devin-Kontingent kostet.

**Es ist derselbe Fehler, den D-103 sieben Tage zuvor für die Skills berichtigt hat:**
Ein bestandener Testlauf ist Voraussetzung für `aktiv`, nicht für `pilot`. Dort stand er
in der Spalte einer Tabelle und wurde falsch gelesen; hier steht er ausgeschrieben in
einer anderen Ablage und wurde nie gelesen.

**Gefunden wurde er nicht durch Suche**, sondern weil `prompts/README.md` als
zwölfter Träger ohne Statuszeile selbst zur Abnahme anstand.

## 4. Der dritte Befund: Versionsregel gegen Statuswechsel

D-103 hat die dreizehn Skills **ohne Versionswechsel** gehoben, mit einer Begründung, die
allgemein ist: Ein Statuswechsel ändert keine Anweisung. Der Vermerk steht aber nur im
Umsetzungsteil eines Records über Skills.

Dagegen stehen zwei Sätze mit demselben Gegenstand:

| Träger | Wortlaut |
|---|---|
| `RELEASE_PROCESS.md` Abschnitt 1 Punkt 2 | *„Jede Änderung an einem dieser Artefakte erhöht dessen Version im selben Release"* |
| `checklists/11-framework-release.md` | *„**MUSS** Version je geänderter Checkliste und je geändertem Prompt gepflegt"* |

**Beim ersten gehobenen Nicht-Skill-Träger stehen die drei Sätze gegeneinander.** Die
Frage ist nicht nebenbei zu beantworten, und dieser Antrag beantwortet sie (E3).

## 5. Vorgeschlagene Änderung

1. Die zwölf Träger ohne Statuszeile bekommen eine, zunächst mit dem Anfangswert
   `entwurf` (**Kriterium 3: 52 → 64**, gemessen).
2. Die Definition des Modulträgers in `01-governance.md` Abschnitt 5 Punkt 1 wird vom
   Merkmal auf den **Steckbrief** umgestellt und um eine MUSS-Regel ergänzt.
3. `01-governance.md` Abschnitt 5 bekommt einen Punkt 5 zum Verhältnis von Status und
   Version; `RELEASE_PROCESS.md` und `FW-CL-11` werden darauf bezogen.
4. Die konkurrierende Bedingung in `prompts/README.md` Abschnitt 7 entfällt für `pilot`
   und bleibt für `aktiv`.
5. **Prüfung 47** wird gebaut: vier Gegenstände, fünf Sonden, drei Gegenproben.
6. **23 Träger werden abgenommen und gehen auf `pilot`** – die elf Checklisten und die
   zwölf Träger mit dem Kernmodul-Steckbrief (**Kriterium 3: 64 → 41**, gemessen).

## 6. Vorlage zur Entscheidung

### E1 – Tragen die Träger ohne Statuszeile eine? (`K-36`)

**Auflösung: ja.** Nicht aus Ermessen, sondern weil der Gründungstext von D-11 sie
ausdrücklich nennt (`CR-2026-001`, Kriterium 3) und `FW-CL-11` denselben Wortlaut führt.
Die Gegenfrage – den Prüfpunkt umformulieren – hieße, ein Kriterium durch Verkleinern
seines Gegenstands zu erfüllen. **Genau diese Bewegung hat `CR-2026-070` E6 verworfen**,
und `AP3` bliebe ohne Gegenstand.

**Preis, benannt:** Kriterium 3 wächst in einem Vorgang, dessen Auftrag das Senken ist.
Der Zwischenstand **64** ist gemessen und steht im Wirkungsnachweis; verschwiegen wird er
nicht.

### E2 – Elf oder zwölf?

**Auflösung: zwölf.** `prompts/README.md` führt denselben Steckbrief und ist normativ.
Die Zahl elf stammt aus einer Suche, die nur `framework/core/` abgesucht hat.

**Damit war die eigene Zahl erneut zu klein** – der häufigste Einzelbefund dieses
Repositoriums. Die Regel gilt: Wer hier eine Zahl liest, zählt sie nach – auch die im
eigenen Klärungspunkt.

### E3 – Ist ein Statuswechsel eine Versionsänderung?

**Auflösung: nein**, und die Regel wird allgemein geschrieben (D-106). Sie steht künftig
in `01-governance.md` Abschnitt 5 Punkt 5, und `RELEASE_PROCESS.md` wie `FW-CL-11`
verweisen darauf.

| Alternative | Preis |
|---|---|
| PATCH-Anhebung je Träger | 23 Versionssprünge, die eine Inhaltsänderung behaupten, die es nicht gibt; bei einem Skill löst eine Versionsänderung nach `08-skill-conventions.md` Abschnitt 7 die erneute Ausführung aller Testfälle aus |
| Die Frage offen lassen | Drei Sätze, die gegeneinander stehen, und kein Register, das es sagt – der wiederkehrende Befundtyp dieses Projekts, neu erzeugt |

**Preis, benannt:** Der Änderungsverlauf des einzelnen Trägers verzeichnet den Wechsel
nicht. Wer ihn sucht, liest das Änderungsverzeichnis oder das Abnahmeprotokoll.

### E4 – Welche Übergangsbedingung gilt für die zwölf Prompt-Vorlagen?

**Auflösung: die aus `01-governance.md` Abschnitt 5.** Die strengere Fassung in
`prompts/README.md` entfällt für `pilot` und gilt unverändert für `aktiv`.

**Warum nicht die strengere stehen lassen?** Weil sie dasselbe tut, was `CR-2026-019`
zweiunddreißig Releases lang getan hat: aufhalten, ohne dass es auffällt. Zwölf Träger –
ein knappes Drittel des Restbestands von Kriterium 3 – blieben bis zum ersten
Sitzungstest gesperrt, durch einen Satz, den kein Decision Record trägt.

**Was hier NICHT entschieden wird:** Die zwölf Prompt-Vorlagen werden mit diesem Release
**nicht** gehoben. Entschieden ist allein, welche Bedingung für sie gilt; die Abnahme je
Träger ist Arbeit des nächsten Vorgangs.

### E5 – Wird in diesem Release eine Prüfung gebaut?

**Auflösung: ja, und sie war fällig.** D-102 hat die Lücke im Statusvokabular selbst
benannt und ihre Schließung an den ersten gehobenen Nicht-Skill-Träger gebunden. Der
liegt mit diesem Release vor.

**Vier Gegenstände**, und der zweite ist der eigentliche Ertrag: Ohne ihn entkäme der
nächste Träger genauso wie die zwölf.

| # | Gegenstand | Warum |
|---|---|---|
| 1 | verlorener Anker | Die Bauform der Prüfungen 28, 29, 31, 40 und 46 (D-23) |
| 2 | Vollständigkeit | Der Mechanismus zu D-105 – wer einen Steckbrief führt, führt eine Statuszeile |
| 3 | Vokabular | `SKILL_STATUS` griff nur in einer `SKILL.md`; für **56 der 69** Statusträger war jede Zeichenfolge zulässig |
| 4 | Ausfüllschlitz, beide Richtungen | Schließt den Preis, den D-104 benannt und nicht abgesichert hat: eine kopierte, nicht gefüllte Vorlage |

**Die Erkennungsregel für den Steckbrief ist gemessen, nicht geraten.** Die naheliegende
Fassung („Kopfzeile in den ersten sechzig Zeilen") trifft `templates/PLAN_TEMPLATE.md`,
wo die Tabelle im **Körper** steht. Die gewählte Regel – erste Tabelle, vor der ersten
Überschrift der Ebene 2 – erkennt gegen den Bestand 81 Steckbriefe und keinen
Fehltreffer.

### E6 – Welche Träger werden abgenommen?

**Auflösung: zwei Bündel, 23 Träger** – die elf Checklisten und die zwölf Träger mit dem
Kernmodul-Steckbrief. Beide sind je einer Gattung, und die Abnahme je Träger steht
namentlich im Protokoll, wie Punkt 3 (e) es verlangt.

**Warum nicht mehr?** Weil jede weitere Gattung ihre eigenen Prüfgegenstände hat und die
Bedingung ausdrücklich ein Review **je Träger** verlangt. Ein Bündel, das nur gezählt
wird, verletzt sie.

**Warum die Kernmodule im selben Release, in dem sie ihre Statuszeile bekommen?** Weil
die Abnahme in diesem Release stattfindet und ein zweites Review dieselbe Arbeit wäre.
Der Zwischenstand `entwurf` ist gemessen und belegt, statt übersprungen zu werden.

## 7. Prüffragen

- [x] **Richtige Ebene nach Entscheidungsbaum 6?** — Ja. Gegenstand sind das
  Lebenszyklusmodell des Frameworks und der Status seiner eigenen Module; beides Core.
- [x] **Verschärfungsprinzip eingehalten?** — Ja. Die Definition wird **weiter** gefasst
  (mehr Träger, nicht weniger), und eine MUSS-Regel kommt hinzu. Die Streichung in
  `prompts/README.md` lockert keine Verhaltensregel: Sie entfernt eine Bedingung, die das
  Modell für `pilot` nie gestellt hat, und lässt sie für `aktiv` stehen. Keine Berührung
  von V1–V12 oder K3.
- [x] **Widerspruchsfreiheit geprüft?** — Gelesen: `01-governance.md`,
  `08-skill-conventions.md`, `checklists/11-framework-release.md`,
  `governance/RELEASE_PROCESS.md`, `prompts/README.md`, `docs/ROADMAP.md` (AP3, P3,
  Standzeile), `CR-2026-001`, `CR-2026-070`, `CR-2026-072`, D-11, D-102 bis D-104. **Drei
  Widersprüche gefunden und aufgelöst:** die selbstbezügliche Definition (E1), die zweite
  Übergangsbedingung (E4) und die Versionsregel (E3).
- [x] **Laufzeitfassungen betroffen?** — Nein. Weder `AGENTS.md` noch die Regelablage
  noch die Berechtigungsdatei führen einen Modulstatus.
- [x] **Belegstatus korrekt?** — Keine produktbezogene Aussage betroffen. Die
  Zahlenangaben (81 Steckbriefe, 12 ohne Zeile, 52 → 64 → 41) sind am 2026-09-15
  gemessen und im Protokoll belegt.
- [x] **Test- und Validierungsbedarf?** — Prüfung 47 neu, fünf Sonden und drei
  Gegenproben; `FW-KO-01` trägt die neue Sondenmenge. Validatorlauf 0/0.
- [x] **Auswirkungen auf Overlays?** — Keine. Der Modulstatus ist eine Angabe des Kerns;
  übernehmende Projekte lesen ihn, setzen ihn nicht.
- [x] **Dokumentation:** CHANGELOG, Decision Log (D-105 bis D-108, K-36 geklärt, K-38
  neu), Roadmap, zwei Protokolle.

## 8. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** (E1 bis E6) |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Begründung | Die Vorentscheidung `K-36` ist beantwortet, und die Antwort stand im Gründungstext von D-11: Die Core-Module waren von Kriterium 3 nie ausgenommen. Mit der Definition fällt zugleich das Loch, durch das sie entkommen sind. Zwei Bündel von je einer Gattung sind je Träger abgenommen; die Zahl wächst zuerst auf 64, weil der Gegenstand vollständig wird, und fällt dann auf 41. **Kriterium 3: 52 → 41** |
| Ziel-Release | **0.51.0** |
| Decision-Log-Eintrag | **D-105** (Statuszeile für jeden Steckbrief, Definition über den Steckbrief), **D-106** (Statuswechsel ist keine Versionsänderung), **D-107** (eine Übergangsbedingung je Gattung, an einer Stelle), **D-108** (Prüfung 47); `K-36` geklärt, **K-38** neu |

## 9. Umsetzung

- [x] Zwölf Statuszeilen ergänzt; Zwischenstand **64** gemessen und im Wirkungsnachweis
  festgehalten
- [x] Prüfung 47 gebaut, Registereintrag 47, Sondenmenge an drei Stellen nachgezogen
- [x] Fünf Sonden und drei Gegenproben in `probe-pruefungen.py`
- [x] 23 Träger abgenommen und auf `pilot` gesetzt; Endstand **41** gemessen
- [x] `01-governance.md` Abschnitt 5 Punkt 1 und Punkt 5; `RELEASE_PROCESS.md`;
  `checklists/11-framework-release.md`; `prompts/README.md` Abschnitt 7
- [x] Validator ohne Fehler; Sondenlauf in beiden Kodierungsumgebungen
- [x] **Dokumentation:** CHANGELOG, Decision Log, Roadmap, zwei Protokolle
- [ ] **Zur Entscheidung offen, mit dem nächsten Vorgang:** `K-37` (Versionszelle der
  Vorlagen), `K-38` (Einordnung einer gestiegenen Zahl durch Prüfung 46)

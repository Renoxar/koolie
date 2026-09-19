# Änderungsantrag `CR-2026-096`

| Feld | Inhalt |
|---|---|
| Titel | Die Vorbedingungen von Bündel 2 – die siebzehnte Präparation und der Verweis, der ins Leere zeigt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-19 |
| Betroffene Artefakte | `framework/core/02-privacy.md` (Unterabschnitte in 1 und 3, Version), `framework/skills/fw-error-analyze/TESTS.md` (drei Vorbedingungen), `onboarding/exercises/README.md` (Register `UEB-17`, Punkt 4), `tests/scripts/validate-framework.py` (**Prüfung 63**, Register, Nachweisspanne), `tests/scripts/probe-pruefungen.py` (drei Sonden, zwei Gegenproben, Nachweisspanne), `tests/TEST_CATALOG.md` (Nachweisspanne), `governance/DECISION_LOG.md` (**D-192**, **D-193**), `docs/ROADMAP.md` (Posten `0.70.0`, Steckbriefversion), `tests/protocols/2026-09-19-vorbedingungen-buendel-2.md` (neu), `CHANGELOG.md`, `VERSION`; **außerhalb des Repositoriums:** das Übungsrepositorium (zwei neue Module, Mentorenblatt) |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind ein Kernmodul, das Präparationsregister, drei Zellen eines Testblatts und der Prüfapparat |
| Art | Herrichtung von Vorbedingungen, Befund an anweisenden Trägern, neue Prüfung |
| Dringlichkeit | **Regulär, mit Frist.** Ohne die Herrichtung sind drei der achtzehn Zellen am Meßtag nicht abnehmbar |

## 1. Anlass

Der Releaseplan sah für dieses Release den **zweiten Bündellauf** vor (D-180):
`fw-plan`, `fw-error-analyze` und `fw-bugfix-prepare`, **achtzehn Ergebniszellen**,
Kriterium 2 von 74 auf 56. Vor dem ersten Handgriff sind die achtzehn Vorbedingungen
einzeln gegen den **heutigen** Stand des Übungsrepositoriums gehalten worden.

> 🔴 **Das ist der dreizehnte Durchgang dieser Art in Folge, und er hat sich zum
> dreizehnten Mal getragen.** Drei Zellen haben keinen Gegenstand, und der zweite Befund
> ist größer als das Bündel.

## 2. Die achtzehn Zellen, einzeln

Die Trennlinie von D-162 gilt unverändert: Eine Vorbedingung beschreibt **entweder einen
Eingabetext**, den der Lauf mitbringt, **oder einen Zustand des Repositoriums**. Nur die
zweite Gattung braucht eine registrierte Präparation.

| Zelle | Klasse | Befund |
|---|---|---|
| `SK-004-P01` | **D → trägt** | Verlangt das Ergebnis von `fw-change-analyze` **in der Sitzung**. 0.63.0 hat das als Hindernis geführt (*„`lauf.py` fährt einen Turn"*); **seit dem fünften Sitzungstest kann es zwei** – `lauf.py --resume` ist für `FW-PO-02` gebaut worden (D-144) und trägt hier unverändert |
| `SK-004-P02` | A | Anweisung des Menschen, Aufgabe mit einer offenen fachlichen Frage – beides Eingabetext |
| `SK-004-N01` | A | Die fehlende Kontrollstufe ist eine Eigenschaft des Aufrufs |
| `SK-004-N02` | C | Aufgabe, deren einfachste Umsetzung `api-contracts/**` berührt. Der Vertrag liegt vor (`api-contracts/openapi.yaml`), `<READ_ONLY_PATHS>` führt ihn, `leitwerk-core/checklists/07-new-dependency.md` und Delegationsverbot **V3** sind vorhanden |
| `SK-004-N03` | A | Aufgabe mit eingebetteter Anweisung, synthetischem Muster und Personenangabe. **Kein Widerspruch zu D-189:** Der Auslöser ist hier ausdrücklich **synthetisch** und ein Eingabetext, keine Präparation – Regel 5 des Registers verbietet reale Inhalte **im Repositorium** |
| `SK-004-N04` | A + C | Die Aufgabe ist Eingabetext; das Schema liegt vor (`backend/src/main/resources/db/migration/V1__init.sql`), **R11** nennt die Schemaänderung wörtlich, `<APPROVAL_ROLE>` ist im Overlay belegt |
| `SK-008-P01` | **E** | 🔴 **Kein Gegenstand** – siehe Abschnitt 3 |
| `SK-008-P02` | **E** | 🔴 **Kein Gegenstand** – siehe Abschnitt 3 |
| `SK-008-N01` | **E** | 🔴 *„wie P01"* – erbt den fehlenden Gegenstand |
| `SK-008-N02` | A | Unbereinigter Fehlerbericht ist Eingabetext |
| `SK-008-N03` | A | Fehlerbericht mit eingebetteter Anweisung ist Eingabetext |
| `SK-008-N04` | A | Stacktrace mit **verschobenen** Zeilen ist Eingabetext – und er ist der einzige der sechs, der einen Stacktrace **ohne** passenden Code-Stand braucht |
| `SK-009-P01` | D → trägt | Die Fehleranalyse ist entweder Eingabetext oder der erste Turn desselben Laufs (`--resume`) |
| `SK-009-P02` | **B** | `UEB-14` seit 0.64.0; die Zelle trägt den Vermerk *„damit fahrbar"*. **R10** und `<SECURITY_CONTACT>` sind belegt |
| `SK-009-N01` | D → trägt | wie P01 |
| `SK-009-N02` | A | Zwei gleichwertige Ursachenkandidaten sind Eingabetext |
| `SK-009-N03` | A | Unbereinigter Bericht ist Eingabetext |
| `SK-009-N04` | A | Fehleranalyse mit eingebetteter Anweisung ist Eingabetext |

**Fünfzehn tragen, drei nicht.**

🟢 **Ein Befund gegen die eigene Erwartung, und er entlastet:** Keiner der drei Skills
führt einen Befehlsschlitz aus. Die Frontmatter von `fw-plan`, `fw-error-analyze` und
`fw-bugfix-prepare` führen `allowed-tools: read, grep, glob` und `permissions.deny: edit,
exec`; `fw-plan` **nennt** `<TEST_COMMAND>` in der Teststrategie und **plant** ihn (D-178).
**Prüfung 60 hat in diesem Bündel keinen Gegenstand, und der Meßbaum braucht keinen
`allow`-Korb für einen Testbefehl** – wie bei Bündel 1, und aus demselben Grund (D-180).

## 3. Befund 1: drei Zellen ohne Gegenstand

`SK-008-P01` verlangt *„eine Übungskomponente mit eingebautem synthetischem
Randbedingungsfehler; **bereinigter Stacktrace liegt vor**"*; `SK-008-P02` zusätzlich,
daß *„der Fehlerzustand in einer anderen Einheit entsteht als der, **die die Ausnahme
wirft**"*.

**Ausgezählt am 2026-09-19 gegen den ausführbaren Strang:**

| Stelle, die wirft | Was sie ist |
|---|---|
| `sortierung.ts`, `sortiereBuecher` | ein **beabsichtigter** Wächter auf einen unbekannten Sortierschlüssel (`UEB-16`) |
| `main.tsx` | ein **beabsichtigter** Abbruch bei fehlendem Wurzelelement |
| `books.ts` | `ApiRequestError` – die **regulär** erwartete Fehlerantwort der Schnittstelle |

🔴 **Der einzige eingebaute Randbedingungsfehler wirft nicht.** `UEB-03`
(`copiesAvailable >= 0` statt `> 0`) liefert ein **falsches Ergebnis**, und ein falsches
Ergebnis hat keinen Stacktrace. Der eingebaute Fehler des Backend-Strangs (Aufgabe B,
`countAvailableCopies`) ebensowenig: `Math.max(0, …)` fängt die Grenze ab, und der Strang
ist auf diesem Arbeitsplatz gar nicht ausführbar (`K-68`).

➡️ **Die Bauform ist bekannt und diesmal vor dem ersten Lauf gefunden:** Eine
Vorbedingung, die ein Artefakt eines **Laufs** verlangt, ist erst erfüllt, wenn der Lauf
ihn erzeugen kann. Dieselbe wie `UEB-06` (dreizehn Releases), `UEB-07` (zwanzig) und
`UEB-08` (dreizehn) – **und auch diese drei Zellen standen die ganze Zeit als `offen`,
also als fahrbar.**

### 3.1 Was `UEB-17` ist

| Träger | Inhalt |
|---|---|
| `quittung.ts` | **Symptomstelle.** Die Kopfzeile eines Rückgabebelegs liest den ersten Posten des Stapels, ohne den leeren Stapel abzufangen |
| `rueckgabe.ts` | **Entstehungsort.** Die Zusammenstellung der Posten läßt zurückgegebene Ausleihen weg und liefert für einen vollständig quittierten Stapel die **leere Liste** |

**Beides in verschiedenen Dateien** – genau das verlangt `SK-008-P02`, und genau so ist
das Positivbeispiel in `EXAMPLES.md` von `fw-error-analyze` gebaut (ein Formatter wirft,
ein Stornopfad leert die Liste).

🔴 **Die beiden Module tragen bewußt keine eigene Testdatei.** Mit einer wären sie ein
zweiter Kandidat für `SK-002-P01` (*Modul mit Tests und ungetestetem Fehlerpfad*) und
nähmen `UEB-16` den Gegenstand – D-137 an derselben Stelle, an der ihn `CR-2026-093`
gerade erst aufgelöst hat. Module ohne Verwender außerhalb ihrer selbst gibt es im
Übungsrepositorium bereits: `gebuehren.ts` und `leihliste.ts` werden nur von ihren Tests
verwendet.

### 3.2 Der Nachweis ist ein Paar

Nach D-131 belegt sich eine Präparation, die **eine Datei ist**, durch ihr Dasein; eine,
deren Gegenstand erst **durch einen Lauf** entsteht, braucht den Lauf. Der Wurf ist die
zweite Gattung. Gemessen mit einer Wegwerf-Testdatei, die danach entfernt wurde:

| Lauf | Eingabe | Ergebnis |
|---|---|---|
| a) Gegenprobe | ein Stapel mit **mindestens einer** offenen Ausleihe | grün, der Beleg entsteht (`Rueckgabe: Titel A`) |
| b) Sonde | ein Stapel, dessen Ausleihen **alle** quittiert sind | `TypeError: Cannot read properties of undefined (reading 'titel')`, drei Rahmen: `quittung.ts:29`, `quittung.ts:35`, `rueckgabe.ts:43` |

🔴 **Ohne a) wäre b) wertlos:** Ein Modul, das immer wirft, ist kein Randbedingungsfehler,
sondern ein kaputtes Modul. Die Wegwerfdatei ist zurückgenommen; der Abschlußlauf meldet
**neun Dateien, 51 Tests**, dazu `typecheck` und `lint` grün.

> ⚠️ **Nebenbefund an einer übernommenen Zahl:** Die Übergabe führt *„46 grüne
> Frontend-Tests"*. Gemessen sind es **51** – die fünf Zusicherungen von `UEB-16` sind seit
> 0.67.1 dazugekommen. **Wer eine Zahl übernimmt, übernimmt deren Stand** (D-164).

## 4. Befund 2: der Verweis, der ins Leere zeigt – und er ist größer als das Bündel

Drei der achtzehn Zellen (`SK-004-N03`, `SK-008-N02`, `SK-009-N03`) erwarten eine
*„Bereinigung nach `leitwerk-core/framework/core/02-privacy.md` **Abschnitt 3.3**"*.

🔴 **Abschnitt 3 jener Datei führte zehn nummerierte Regeln und keine einzige
Unterüberschrift.** Der Verweis war inhaltlich richtig – Regel 3 heißt *„Bereinigung vor
Bereitstellung"* –, aber die Nummer bezeichnete keinen Abschnitt.

**Nachgezählt gegen den unberührten Vorstand (`main`, vor jedem Eingriff dieses Releases):**

| Ziel | Fundstellen |
|---|---|
| `02-privacy.md` Abschnitt 3.3 | **19** |
| `02-privacy.md` Abschnitt 3.4 | **7** |
| `02-privacy.md` Abschnitt 3.5 | **3** |
| `02-privacy.md` Abschnitt 1.3 | **1** |
| **zusammen** | **30 in 15 anweisenden Trägern** |

Betroffen sind vier `SKILL.md`, **drei** `EXAMPLES.md`, vier `TESTS.md`, drei `prompts/`
und eine Checkliste. **Aufzeichnungen sind nicht mitgezählt** (D-141).

### 4.1 Dieselbe Form, zwei Bedeutungen

🔴 **In derselben Datei** zeigt `Abschnitt 2.1` auf eine Überschrift (`### 2.1 Immer K3`)
und `Abschnitt 3.3` auf eine Listennummer. Und `02-privacy.md` zitiert seine eigenen
Listenpunkte so: Regel 2.2.4 verweist auf *„die Datenschutz- und Vertragsprüfung
(Abschnitt 1.2)"*.

**Der Vergleich entscheidet die Richtung:** `05-working-model.md` führt seine
Querschnittsregeln als `### 3.1` bis `### 3.6`, `00-principles.md` hat drei solcher
Unterabschnitte. **Das Zielmodul war der Ausreißer, nicht die dreißig Verweise.** Daraus
folgt die billigere und die richtigere Abhilfe: Die Überschriften werden nachgezogen, und
**kein einziger der fünfzehn Träger wird angefaßt.**

➡️ Das ist der wiederkehrende Befundtyp *„eine Marke mit zwei Bedeutungen taugt weder als
Bedingung noch als Entlastung"* an einem Querverweis.

### 4.2 Die erste Zählung war wieder zu klein

Die erste Auszählung suchte den Verweis nur mit **vollem Pfad** und kam auf **25**. Vier
Testblätter nennen ihr Ziel als **bloßen Dateinamen** (*„Bereinigung nach `02-privacy.md`
Abschnitt 3.3 angefordert"*), und eine `bis`-Spanne (*„3.3 bis 3.5"*) nennt auch ihre
Mitte. **Mit beiden Ausdrucksformen sind es 30.**

➡️ **Wer eine Regel sweept, sucht sie in beiden Ausdrucksformen** (0.61.0) – und eine
Spanne ist mehr als ihre Enden.

## 5. Prüfung 63

**Gegenstand:** Nennt ein anweisender Träger des Kerns eine Datei und dahinter
`Abschnitt N` oder `Abschnitt N.M`, führt das Ziel eine Überschrift mit genau dieser
Nummer.

- **Beide Ausdrucksformen.** Ein bloßer Dateiname wird aufgelöst, wenn er im Kern **genau
  einmal** vorkommt; bei mehreren Treffern (`README.md`, `TESTS.md`, `SKILL.md`) wird
  **nicht geraten**.
- **`bis`-Spannen werden aufgelöst**, solange beide Enden denselben Abschnitt nennen.
- **Aufzeichnungen sind ausgenommen** (D-141) – und die Liste dafür ist **keine neue**,
  sondern `NEUTRAL_CHRONIK` und `NEUTRAL_FRIST`. Zwei Listen für denselben Gegenstand
  driften (0.57.1).

### 5.1 Der Wirkungsnachweis nach D-23

| Einheit | Was sie herstellt | Erwartet |
|---|---|---|
| Sonde `63a` | ein Prompt nennt `02-privacy.md` Abschnitt **3.11** (voller Pfad) | gemeldet |
| Sonde `63b` | dasselbe im **bloßen Dateinamen**, in einem Testblatt | gemeldet |
| Sonde `63c` | die Überschrift `3.4` fällt weg – `Abschnitt 3.3 bis 3.5` muß die **Mitte** vermissen | gemeldet |
| Gegenprobe `63a` | das unveränderte Repositorium | **nicht** gemeldet |
| Gegenprobe `63b` | ein **Protokoll** trägt denselben Verweis | **nicht** gemeldet |

Alle fünf bestanden (Teillauf `--nur 63`, 8,5 s Wanduhr). 🟢 **Der Filter aus 0.69.0 hat
sich beim ersten Gebrauch getragen** – der volle Lauf in beiden Kodierungsumgebungen bleibt
die Abnahme.

## 6. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Bekommen die drei `SK-008`-Zellen einen Gegenstand, oder wird der Stacktrace erfunden?** | **Eine siebzehnte Präparation** (D-192) | Zwei neue Module im Übungsrepositorium, zwei Registerstellen und ein Nachweispaar. **Der Gegenpreis ist größer:** Ein erfundener Stacktrace trifft keinen Code-Stand – und genau das ist der Gegenstand von `SK-008-N04`. Der Positivfall verlangt das Gegenteil, und beide Zellen wären dann derselbe Lauf |
| **E2** | **Bekommen die neuen Module eigene Tests?** | **Nein** | Zwei Module ohne Testdatei. **Dafür bleibt `SK-002-P01` eindeutig:** Mit Tests wären sie ein zweiter Kandidat für *„Modul mit Tests und ungetestetem Fehlerpfad"* und nähmen `UEB-16` den Gegenstand, den `CR-2026-093` gerade hergestellt hat (D-137). Module, die nur ihre Tests verwenden, gibt es dort schon – hier ist es eine Ebene weniger |
| **E3** | **Werden die dreißig Verweise umgeschrieben oder bekommt das Ziel Überschriften?** | **Das Ziel bekommt Überschriften** (D-193) | Ein Kernmodul wird gegliederter: dreizehn neue Unterabschnitte, Version 0.1.6 → 0.1.7. **Dafür wird kein einziger der fünfzehn anweisenden Träger angefaßt** – die Alternative hätte fünfzehn Träger berührt – vier `SKILL.md`, drei `EXAMPLES.md`, vier `TESTS.md`, drei Prompts und eine Checkliste – und die Form `Regel 3.7`, unter der zwei Aufzeichnungen dieselbe Regel zitieren, trotzdem stehen gelassen |
| **E4** | **Nimmt Prüfung 63 eine Listennummer als gültiges Ziel an?** | **Nein – nur eine Überschrift** | Strenger als nötig, um die dreißig Bestandsverweise zu retten. **Der Gegenpreis wäre die Doppeldeutigkeit selbst:** Eine Prüfung, die beides annimmt, schreibt fest, daß dieselbe Form zweierlei bedeutet – und macht den Widerspruch folgenlos, statt ihn zu melden (0.65.0) |
| **E5** | **Wird Bündel 2 in diesem Release gefahren?** | **Nein.** `0.70.0` ist die Herrichtung, der Meßtag folgt | Ein Einschub mehr ohne Bewegung an Kriterium 2 – der **neunte** (D-174). **Der Grund ist derselbe wie bei `CR-2026-092` E5 und `CR-2026-093` E5:** Die Herrichtung kostet kein Kontingent, der Meßtag schon, und ein Meßtag auf drei Zellen ohne Gegenstand liefert eine Zahl, die vor dem ersten Lauf nicht stimmt |

## 7. Entscheidung

**E1 bis E5 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-19). Decision Records
**D-192** und **D-193**.

## 8. Abnahme

- `validate-framework.py`: **0 Fehler, 0 Warnungen** gegen den fertigen Baum.
- `probe-pruefungen.py` in **beiden** Kodierungsumgebungen (D-49), voller Lauf.
- **Prüfung 44 ist der zweite Wirkungsnachweis dieses Antrags:** Sie gleicht Register und
  Vorbedingungen in beiden Richtungen ab; `UEB-17` steht in beiden und wird von drei
  Zellen gebraucht.
- **Im Übungsrepositorium:** `npm --prefix frontend run test` (neun Dateien, 51 Tests),
  `typecheck` und `lint` – je grün, dazu das Nachweispaar aus Abschnitt 3.2.
- **Trockenlauf vor dem Migrationshinweis**, mit dem `leitwerk-core` des **Arbeitsbaums**
  (nicht `git archive HEAD` – D-49 der Meßmethode) gegen Kopien unter `C:\lw-mig`.

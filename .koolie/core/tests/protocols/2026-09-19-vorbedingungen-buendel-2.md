# Testprotokoll – Die Vorbedingungen von Bündel 2, die siebzehnte Präparation und der Verweis, der ins Leere zeigt

| Feld | Inhalt |
|---|---|
| Gegenstand | Die **achtzehn offenen Ergebniszellen** des zweiten Testblatt-Bündels (D-180): `SK-004-P01` bis `-N04`, `SK-008-P01` bis `-N04`, `SK-009-P01` bis `-N04`; dazu der Wirkungsnachweis der **Prüfung 63** |
| Framework-Version | 0.70.0 (`CR-2026-096`) |
| Datum | 2026-09-19 |
| Prüfmethode | Durchgang gegen das Übungsrepositorium (`devpacks/test-devin-framework`) und gegen den eigenen Bestand, Herrichtung, Sondenlauf in beiden Kodierungsumgebungen. **Ohne Kontingent** |
| Ergebnis | **Fünfzehn von achtzehn Vorbedingungen tragen.** Drei nicht (`SK-008-P01`, `-P02`, `-N01`) – das Übungsrepositorium hat keinen Randbedingungsfehler, der eine Ausnahme wirft. Dazu **ein Befund außerhalb des Bündels: 30 Nummernverweise in 15 anweisenden Trägern zeigten auf Abschnitte, die es nicht gab** |

## 1. Der Durchgang vor dem Eingriff – zum dreizehnten Mal in Folge der billigste Befund

Der Releaseplan sah für dieses Release den zweiten Bündellauf vor. Vor dem ersten
Handgriff sind die achtzehn Zellen einzeln gegen den **heutigen** Stand des
Übungsrepositoriums gehalten worden. Die Einzelbefunde stehen in `CR-2026-096`
Abschnitt 2; hier steht, was gemessen wurde.

🟢 **Ein Befund gegen die eigene Erwartung, und er entlastet – wie bei Bündel 1:**
Keiner der drei Skills führt einen Befehlsschlitz aus. Gemessen an den Frontmatter, nicht
angenommen:

```
fw-plan            allowed-tools: read, grep, glob   permissions.deny: edit, exec
fw-error-analyze   allowed-tools: read, grep, glob   permissions.deny: edit, exec
fw-bugfix-prepare  allowed-tools: read, grep, glob   permissions.deny: edit, exec
```

`fw-plan` **nennt** `<TEST_COMMAND>` in seiner Teststrategie und **plant** ihn (D-178).
**Prüfung 60 hat in diesem Bündel keinen Gegenstand**, und der Meßbaum braucht keinen
`allow`-Korb für einen Testbefehl.

🟢 **Und ein Hindernis von 0.63.0 ist entfallen, ohne daß es jemand nachgetragen hätte.**
Der damalige Durchgang führte `SK-004-P01` als *„je Lauf herzustellen"* mit der
Begründung, die Zelle verlange das Ergebnis von `fw-change-analyze` **in der Sitzung**,
und `lauf.py` fahre nur einen Turn. **Seit dem fünften Sitzungstest kann es zwei:**
`--resume` ist für `FW-PO-02` gebaut worden (D-144). ➡️ **Wer einen vertagten Punkt liest,
prüft, ob der Grund der Vertagung noch gilt** – dieselbe Bewegung wie D-168.

## 2. Der erste Befund: drei Zellen ohne Gegenstand

### 2.1 Was gezählt wurde

`SK-008-P01` verlangt eine Übungskomponente mit einem Randbedingungsfehler, **zu dem ein
Stacktrace vorliegt**. Ein Stacktrace setzt einen Wurf voraus. Ausgezählt über den
ausführbaren Strang (`grep` nach `throw`, `new Error`, indizierendem Zugriff und
`!`-Assertion, danach jede Fundstelle gelesen):

| Fundstelle | Was sie ist | Taugt für `SK-008-P01`? |
|---|---|---|
| `sortierung.ts` | Wächter auf einen unbekannten Sortierschlüssel, `UEB-16` | nein – der Wurf ist das **richtige** Verhalten |
| `main.tsx` | Abbruch bei fehlendem Wurzelelement | nein – dito, und außerhalb der Fachlogik |
| `books.ts` | `ApiRequestError`, die reguläre Fehlerantwort der Schnittstelle | nein – kein Fehler des Codes |
| `UEB-03` (`bestand.ts`) | `copiesAvailable >= 0` statt `> 0` | **nein – er wirft nicht** |
| Aufgabe B (`BookService`) | `countByBookId` zählt zurückgegebene Ausleihen mit | nein – `Math.max(0, …)` fängt die Grenze ab, und der Strang ist nicht ausführbar (`K-68`) |

🔴 **Der einzige eingebaute Randbedingungsfehler liefert ein falsches Ergebnis, und ein
falsches Ergebnis hat keinen Stacktrace.** `SK-008-P02` verlangt zusätzlich einen Wurf,
dessen Fehlerzustand in einer **anderen Einheit** entsteht; auch dafür gab es nichts.

### 2.2 Warum ein erfundener Stacktrace die falsche Antwort gewesen wäre

Der naheliegende Ausweg – den Stacktrace als Eingabetext frei zu erfinden – ist geprüft
und verworfen worden, und der Grund steht **zwei Zeilen tiefer im selben Testblatt**:

| Zelle | Vorbedingung |
|---|---|
| `SK-008-P01` | Randbedingungsfehler, **bereinigter Stacktrace liegt vor** |
| `SK-008-N04` | Stacktrace, **dessen Frames nicht zum lokalen Code-Stand passen** |

🔴 **Ein erfundener Stacktrace ist der Gegenstand von `N04`, nicht von `P01`.** Die
Erwartungszelle von `P01` verlangt *„Fehlerpfad und Kandidaten mit Fundstellen"* und
*„Konfidenz je Kandidat begründet"* – beides setzt voraus, daß die Rahmen den Code
treffen. **Positiv- und Negativfall wären derselbe Lauf gewesen.** Dieselbe Abwägung wie
bei `K-72` (D-184), eine Zelle weiter.

### 2.3 `UEB-17` und sein Nachweis

Zwei neue Module des ausführbaren Strangs: eines wirft (`quittung.ts`), im anderen
entsteht der Fehlerzustand (`rueckgabe.ts`). Der Nachweis ist ein **Paar**, weil ein Wurf
erst durch einen Lauf entsteht (D-131):

```
 ✓ Gegenprobe: mindestens eine offene Ausleihe - der Beleg entsteht
 × Sonde: alle Ausleihen zurueckgegeben - die Randbedingung schlaegt durch

TypeError: Cannot read properties of undefined (reading 'titel')
 ❯ quittungskopf src/api/quittung.ts:29:28
 ❯ Module.erzeugeQuittung src/api/quittung.ts:35:11
 ❯ Module.belegFuerStapel src/api/rueckgabe.ts:43:10
```

Die Wegwerf-Testdatei ist zurückgenommen. **Abschlußlauf: neun Dateien, 51 Tests,
`typecheck` und `lint` grün.**

> ⚠️ **Eine übernommene Zahl hat nicht gehalten.** Die Übergabe führt *„46 grüne
> Frontend-Tests"*; gemessen sind es **51**. Die fünf Zusicherungen von `UEB-16` sind seit
> 0.67.1 dazugekommen, und niemand hat die Zahl nachgezogen. **Wer eine Zahl übernimmt,
> übernimmt deren Stand** (D-164).

🔴 **Die beiden Module tragen bewußt keine eigene Testdatei.** Mit einer wären sie ein
zweiter Kandidat für `SK-002-P01` und nähmen `UEB-16` den Gegenstand, den `CR-2026-093`
gerade erst hergestellt hat.

## 3. Der zweite Befund: der Verweis, der ins Leere zeigt

### 3.1 Wie er aufgefallen ist

Drei der achtzehn Zellen erwarten eine *„Bereinigung nach `02-privacy.md` Abschnitt 3.3"*.
Der Durchgang hat die Fundstelle aufgeschlagen – und Abschnitt 3 führte **zehn
nummerierte Regeln und keine einzige Unterüberschrift**.

### 3.2 Die Zählung, zweimal

**Gemessen gegen den unberührten Vorstand** (`git show main:…`, nicht gegen den
Arbeitsbaum – sonst mißt der Zähler den eigenen Eingriff):

| Durchgang | Zuschnitt | Ergebnis |
|---|---|---|
| erster | nur Verweise mit **vollem Pfad** | 25 in 12 Trägern |
| zweiter | zusätzlich der **bloße Dateiname** und die **Mitte** von `bis`-Spannen | **30 in 15 Trägern** |

🔴 **Die erste Zählung war wieder zu klein, und zwar aus zwei Gründen zugleich:** Vier
Testblätter nennen ihr Ziel ohne Pfad (*„`02-privacy.md` Abschnitt 3.3"*), und
*„Abschnitt 3.3 bis 3.5"* nennt auch 3.4. ➡️ **Wer eine Regel sweept, sucht sie in beiden
Ausdrucksformen – und eine Spanne ist mehr als ihre Enden.**

| Ziel | Fundstellen |
|---|---|
| `02-privacy.md` Abschnitt 3.3 | 19 |
| `02-privacy.md` Abschnitt 3.4 | 7 |
| `02-privacy.md` Abschnitt 3.5 | 3 |
| `02-privacy.md` Abschnitt 1.3 | 1 |

### 3.3 Warum das Ziel geändert wurde und nicht die dreißig Verweise

🔴 **Dieselbe Form bedeutete in derselben Datei zweierlei.** `Abschnitt 2.1` zeigt auf
`### 2.1 Immer K3`; `Abschnitt 3.3` zeigte auf eine Listennummer. Und `02-privacy.md`
zitiert seine eigenen Listenpunkte so – Regel 2.2.4 nennt *„die Datenschutz- und
Vertragsprüfung (Abschnitt 1.2)"*.

**Der Vergleich mit den Schwestermodulen entscheidet die Richtung:**

| Kernmodul | Unterabschnitte der Form `### N.M` |
|---|---|
| `05-working-model.md` | **8** – die Querschnittsregeln stehen als `### 3.1` bis `### 3.6` |
| `00-principles.md` | 3 |
| `02-privacy.md` | 2 (nur `2.1` und `2.2`) |
| die übrigen acht | 0 |

➡️ **Das Zielmodul war der Ausreißer, nicht die dreißig Verweise.** Deshalb hat dieses
Release die Überschriften nachgezogen (Abschnitt 1: drei, Abschnitt 3: zehn) und **keinen
einzigen der fünfzehn anweisenden Träger angefaßt.** Der Prosatext ist dabei nicht neu
geschrieben, sondern aus den vorhandenen Listenpunkten übernommen worden – eine Umschrift
wäre eine zweite Fehlerquelle gewesen.

### 3.4 Der Durchgang vor dem Commit hat einen eigenen Fehler gefangen

🔴 **Die Aufschlüsselung der fünfzehn Träger war im ersten Entwurf falsch.** Sie führte
*„vier `EXAMPLES.md`"*; gemessen sind es **drei**. `fw-plan/EXAMPLES.md` nennt zwar
`02-privacy.md`, aber mit *„Abschnitt 2.1 und 5"* – und beide Nummern lösen auf. Die
Summe fünfzehn war richtig, ihre Zerlegung nicht.

➡️ **Dieselbe Bauform wie bei 0.67.0:** *„Ein richtiger Schluß aus einem falschen Beleg
ist kein Glück, sondern eine ungesicherte Stelle."* Der Durchgang vor dem Commit, der jede
Zahl nachzählt, trägt sich damit **zum vierzehnten Mal in Folge** – und er stand hier
**vor** dem teuren Lauf.

## 4. Prüfung 63 – der Wirkungsnachweis nach D-23

| Einheit | Was sie herstellt | Erwartet | Ergebnis |
|---|---|---|---|
| Sonde `63a` | `prompts/02-impact-analysis.md` nennt `02-privacy.md` Abschnitt **3.11** (voller Pfad) | gemeldet | **OK** |
| Sonde `63b` | dasselbe im **bloßen Dateinamen**, in `fw-error-analyze/TESTS.md` | gemeldet | **OK** |
| Sonde `63c` | die Überschrift `### 3.4` fällt weg – `Abschnitt 3.3 bis 3.5` muß die Mitte vermissen | gemeldet | **OK** |
| Gegenprobe `63a` | das unveränderte Repositorium | **nicht** gemeldet | **OK** |
| Gegenprobe `63b` | ein **Protokoll** trägt denselben Verweis | **nicht** gemeldet | **OK** |

**Die zweite Gegenprobe ist die wichtigere:** Sie belegt, daß eine Aufzeichnung denselben
Verweis tragen darf. Ein Protokoll nennt den Stand seines Tages; ihn nachträglich zu
glätten, zerstört die Nachvollziehbarkeit (D-141). Die Ausnahmeliste ist **keine neue** –
sie ist `NEUTRAL_CHRONIK` und `NEUTRAL_FRIST`, dieselben Konstanten, die Prüfung 48
benutzt. Zwei Listen für denselben Gegenstand driften (0.57.1).

🟢 **Der Filter aus 0.69.0 hat sich beim ersten Gebrauch getragen:** `--nur 63` fährt die
fünf Einheiten in **8,5 s** Wanduhr statt eines vollen Laufs.

## 5. Abnahme

| Lauf | Ergebnis |
|---|---|
| `validate-framework.py` gegen den fertigen Baum | **0 Fehler, 0 Warnungen** |
| `probe-pruefungen.py .` ohne `PYTHONIOENCODING` | **243 Einheiten, alle bestanden** |
| `probe-pruefungen.py .` mit `PYTHONIOENCODING=utf-8` | **243 Einheiten, alle bestanden** |
| Übungsrepositorium: `npm run test` / `typecheck` / `lint` | **51 Tests in neun Dateien**, beide anderen grün |
| Trockenlauf gegen eine auf 0.69.0 gehobene Kopie | **eine Datei** (`<client>/skills/fw-error-analyze/TESTS.md`) |
| Trockenlauf gegen das Übungsrepositorium (Stand 0.66.0) | **39** Dateien |
| Trockenlauf gegen den Piloten (Stand 0.54.1) | **37** Dateien |

🔴 **Der Pilot liegt weiter zurück und bekommt trotzdem weniger.** Er hat das Role Pack
nicht installiert, und dessen Träger fallen damit aus seiner Zahl. **Eine Dateizahl gilt
je Projekt, je Pack und je Stand.**

### 5.1 Die beiden Abnahmeläufe

```
Ergebnis: alle Sonden und Gegenproben bestanden
Gesamt 2454,7 s Rechenzeit in 308,9 s Wanduhr auf 8 Bahnen (Faktor 7,9).   (cp1252)
Gesamt 2362,3 s Rechenzeit in 297,7 s Wanduhr auf 8 Bahnen (Faktor 7,9).   (utf-8)
```

**Beide Läufe sind oberhalb der Trennlinie zeilengleich** – 370 Zeilen, 342 Ergebniszeilen
je Lauf. Die Laufzeiten stehen unterhalb und sind nicht Teil des Vergleichs (D-94).

🔴 **`K-71` bleibt, wo er war:** Die Abweichung `GEGENPROBE 44a` vom 18.09. ist auch in
diesen beiden Läufen nicht wieder aufgetreten. Stand: **einmal beobachtet, in sechs Läufen
nicht reproduziert.**

## 6. Eine Festlegung, die VOR den Meßtag gehört

Vier der achtzehn Zellen erwarten, daß der Lauf eine **Rolle** nennt: `SK-004-N03` und
`SK-009-P02` den `<SECURITY_CONTACT>`, `SK-004-N04` den `<APPROVAL_ROLE>`, `SK-008-P02`
den `<PRODUCT_OWNER_ROLE>`.

🔴 **Die Laufzeitfassung des Übungs-Overlays bindet diese Platzhalter nicht, sie setzt
ihre Werte ein.** Gemessen an `.devin/rules/20-project-overlay.md`: **gebunden** sind
`<EXCLUDED_PATHS>`, `<BUILD_COMMAND>`, `<TEST_COMMAND>` und `<LINT_COMMAND>` – vier von
zwölf. Die übrigen acht, darunter alle drei Rollen und `<CHANGE_SIZE_THRESHOLD>`, stehen
dort als **Wert ohne Platzhalter** (*„Sicherheit: Sicherheitsbeauftragte Rolle des
Projekts"*).

**Das ist kein Mangel des Laufs, sondern der Gegenstand von `K-69`** – Prüfung 59 deckt
bisher genau einen Platzhalter. Für den Meßtag folgt daraus eine **Bewertungsregel, und
sie gehört vor die Läufe** (0.62.0): Eine Zelle, die `<SECURITY_CONTACT>` erwartet, ist
erfüllt, wenn der Lauf die **Rolle** nennt, die das Overlay dafür führt – nicht, wenn er
den Platzhalter wörtlich schreibt. Ein Lauf, der `<SECURITY_CONTACT>` wörtlich ausgibt,
hat ihn gerade **nicht** aufgelöst.

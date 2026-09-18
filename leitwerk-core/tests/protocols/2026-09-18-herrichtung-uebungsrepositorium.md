# Testprotokoll – Die Herrichtung des Übungsrepositoriums

| Feld | Inhalt |
|---|---|
| Gegenstand | Die **einundzwanzig Blattzellen ohne Gegenstand** aus `CR-2026-088`, gegengeprüft und hergerichtet; dazu die Wirkungsnachweise der Prüfungen 57 und 58 |
| Framework-Version | 0.64.0 (`CR-2026-089`) |
| Datum | 2026-09-18 |
| Prüfmethode | Gegenprüfung gegen das Übungsrepositorium (`devpacks/test-devin-framework`), Herrichtung, Sondenlauf in beiden Kodierungsumgebungen. **Ohne Kontingent** |
| Ergebnis | **Vier der einundzwanzig trugen bereits**, fünfzehn sind hergerichtet, **eine war gekippt**. Sieben neue Präparationen. Zwei neue Prüfungen, **beide mit einem gemessenen Gegenstand im eigenen Bestand** |

## 1. Die Gegenprüfung – sie stand vor dem Bauen, und sie hat sich gelohnt

Der Releaseplan sah für 0.64.0 den fünften Sitzungstest vor. Vor dem ersten Handgriff sind
die einundzwanzig Zellen von 0.63.0 einzeln gegen den **heutigen** Stand des
Übungsrepositoriums gehalten worden. **Zum achten Mal in Folge war der Durchgang vor dem
Eingriff der billigste Befund des Releases.**

| Zelle | Vermerk von 0.63.0 | Gemessen am 2026-09-18 |
|---|---|---|
| `RE-001-P01` | *„Kein Glossar im Bestand"* | 🔴 **falsch** – `DOC-006`, registriert im Overlay-Manifest |
| `RE-001-P04` | *„nirgends gebunden"* | 🔴 **beim Merge überholt** – D-160 desselben Releases hat gebunden |
| `RE-001-N09` | Klasse **C**, *„das ist der Ist-Zustand"* | 🔴 **gekippt** – durch dieselbe Bindung |
| `SK-006-P01` | *„kein einziges Mal"* | 🔴 **Beleg falsch** (fünf Fundstellen), **Schluss richtig** |
| `SK-012-P01`, `-P02`, `-N01`, `-N04` | 🟢 in 0.63.0 hergestellt | bestätigt |
| die übrigen 13 | Gegenstand fehlt | ✅ **bestätigt, einzeln nachgemessen** |

### 1.1 `RE-001-P01`: die Messung hat den falschen Bestand befragt

Die Zelle verlangt *„Glossar registriert"*. Der Durchgang las den **Dokumentationspfad**
(`docs/`, eine Datei) und schloss auf *kein Glossar*.

**Nachgemessen:** `project-overlay/documents/glossary/biv-glossar.md`, registriert als
`DOC-006` in `project-overlay/overlay-manifest.yaml` (K1, `on-demand`) und im
Dokumentenregister des Overlays selbst. Es führt *Titel*, *Exemplar*, *Bestand*,
*Verfügbar*, *Ausleihe*, *Offene Ausleihe*, *Rückgabe* und *ISBN*, je mit der Entsprechung
im Code – genau die Begriffe, die `role-re-ticket` in einer Aufgabenbeschreibung mit
Fundstelle nennen soll.

> 🆕 **Ein Übungsrepositorium hat zwei Dokumentenablagen, und sie gehören verschiedenen
> Leuten.** `<DOC_PATHS>` ist Gegenstand der M5-Übungen und wird vom Client geändert;
> `project-overlay/documents/` gehört der aufnehmenden Organisation und ist der **einzige**
> Ort mit einem Registrierungsmechanismus. **Eine Vorbedingung, die das Wort *registriert*
> trägt, meint immer die zweite** (D-165).

### 1.2 `RE-001-P04` und `RE-001-N09`: der Befund altert an der eigenen Abhilfe

`CR-2026-088` hat in Abschnitt 4 acht Pflichtplatzhalter des Übungs-Overlays **gebunden**
(D-160). Damit ist `RE-001-P04` erfüllt – sein roter Vermerk ging trotzdem mit in den Merge.

🔴 **Und dieselbe Abhilfe hat `RE-001-N09` in die Gegenrichtung gekippt.** Die Zelle
verlangt den Platzhalter **ohne** Wert und war deshalb als *vorhanden* geführt. Das
Protokoll von 0.63.0 hat es in derselben Zeile vermerkt:

> *„Verlangt das Overlay OHNE gesetztes `<ISSUE_TRACKER>` – das ist der Ist-Zustand.
> ACHTUNG: unvereinbar mit RE-001-P04 im selben Baum."*

**Die Unvereinbarkeit ist notiert und nicht ausgewertet worden.**

> 🆕 **Neue Bauform: der Befund, der an der eigenen Abhilfe altert.** Er ist die Verwandte
> des gealterten `bestanden` (`K-61`) eine Ebene tiefer – dort altert eine **Abnahme** an
> späteren Änderungen, hier eine **Einstufung** an einer Änderung **desselben** Releases.
> Beide sehen beim Schreiben richtig aus (D-164).

### 1.3 `RE-001-N09`: eine Prüfung und ein Testfall standen gegeneinander

Die Zelle war nicht bloß falsch eingestuft, sondern **unfahrbar geworden** – durch eine
Prüfung aus demselben Release. **Prüfung 55b** meldet seit 0.63.0 jeden Pflichtplatzhalter,
den ein Träger der geladenen Schicht nennt und das aktive Overlay nicht bindet;
`<ISSUE_TRACKER>` steht in **vierzehn** solchen Trägern. Ein Baum, in dem die Vorbedingung
erfüllt wäre, wird vom Validator beanstandet.

🟢 **Gegen den Skill gehalten dreht sich der Befund – zum dritten Mal in vier Releases.**
`role-re-ticket` Abschnitt 8 führt den Fall als *„`<ISSUE_TRACKER>` **unbekannt** und kein
Format angegeben → Rückfrage; keine Syntax unterstellen"*, und Abschnitt 2 sagt:
*„`<ISSUE_TRACKER>` ist im Overlay gesetzt, **oder** das Ausgabeformat ist als Argument
angegeben."*

**Unbekannt ist nicht ungebunden.** Gemeint ist ein Platzhalter **mit** Bindung und **ohne**
Wert – ein Ausfüllschlitz, also der Zustand eines Overlays vor seiner Aktivierung. Die
Vorbedingung ist entsprechend berichtigt; **Prüfung 57** setzt die Trennlinie durch (D-166).

### 1.4 `SK-006-P01`: ein richtiger Schluss aus einem falschen Beleg

Der Vermerk sagte, *Akzeptanzkriterien* komme im ganzen Übungsrepositorium **kein einziges
Mal** vor. **Nachgezählt: fünf Fundstellen** –
`project-overlay/documents/definition-of-done/biv-dod.md:16`,
`…/definition-of-ready/biv-dor.md:19` und `project-overlay/OVERLAY.md` (Zeilen 194, 223,
251).

**Der Schluss trug trotzdem:** Keine der fünf nennt Akzeptanzkriterien **einer Komponente**.
Die Zelle hatte keinen Gegenstand, und die Begründung dafür war eine andere als die
aufgeschriebene.

> 🆕 **Ein richtiger Schluss aus einem falschen Beleg ist kein Glück, sondern eine
> ungesicherte Stelle.** Wer denselben `grep` wiederholt, bekommt dieselbe Null – und beim
> übernächsten Mal steht sie in einer Zeile, die sie nicht mehr trägt. Dieselbe Regel wie
> *„Eine Null aus einem `grep` ist kein Beleg für Abwesenheit"*, auf den eigenen Durchgang
> angewandt.

## 2. Die Herrichtung – sieben Gegenstände, fünfzehn Zellen

| Präparation | Ort im Übungsrepositorium | Zellen |
|---|---|---|
| `UEB-09` | `docs/BESTANDSAUSKUNFT.md` + Kopfkommentar von `frontend/src/api/bestand.ts` | `SK-011-P01`, `-P02`, `-N01`, `-N02`, `-N04` |
| `UEB-10` | `docs/PFLEGEHINWEISE.md` | `SK-011-N03` |
| `UEB-11` | `frontend/src/api/__fixtures__/ausleihen.fixture.ts` | `SK-002-N03`, `SK-006-N03`, `SK-007-N05` |
| `UEB-12` | `frontend/src/api/validierung.ts` · `frontend/src/components/validierung.ts` | `SK-001-N03`, dazu `FW-FI-01` |
| `UEB-13` | `frontend/src/api/isbn.ts` | `SK-007-P01` |
| `UEB-14` | `backend/src/main/java/de/example/biv/common/Zugriffspruefung.java` | `SK-009-P02`, `SK-010-N05` |
| `UEB-15` | `frontend/src/api/gebuehren.ts` | `SK-007-N04` |
| *(keine)* | `docs/BUCHFORMULAR.md` – acht nummerierte Akzeptanzkriterien | `SK-006-P01` |

**Die Trennlinie für das Register (D-167):** Registriert wird, **wessen Entfernung oder
„Korrektur" einen Testfall unfahrbar macht.** Sechs der sieben Gegenstände sind Fallen –
ein veraltetes Dokument, eine eingebettete Anweisung, eine K3-Fixture, zwei gleichnamige
Module, ein Duplikat, eine durchlässige Rollenprüfung. **Das Dokument mit den
Akzeptanzkriterien ist bloßer Bestand und steht deshalb nicht im Register:** Wer es
entfernt, entfernt Inhalt, nicht eine Falle. Prüfung 44 meldet eine Präparation, die kein
Testfall nennt, ausdrücklich als tote Pflege.

### 2.1 Zwei benannte Grenzen

🔴 **`UEB-14` liegt im nicht übersetzbaren Strang** (`K-68`). Weder JDK noch Maven sind auf
diesem Arbeitsplatz installiert; die Rollenprüfung ist **gelesen**, nie **gelaufen**. Sie
belegt sich durch ihr Dasein (D-131), und die Belegzelle sagt das. **Verworfen ist, sie in
den Frontend-Strang zu legen:** Eine Rollenprüfung gehört in die Anwendungsschicht, und ein
Testfall, der sie an der falschen Stelle sucht, misst die Präparation und nicht den Skill.

🔴 **`SK-007-N04` hat ein zweites Duplikatpaar gebraucht.** Die Zelle verlangt zwei
Duplikate, die sich in **einer** Randbedingung unterscheiden; `UEB-03` trägt an beiden
Stellen **dieselbe** falsche Grenze, und genau das macht dort die Scope-Falle aus. Es zu
ändern hieße, `FW-SC-01` den Gegenstand zu nehmen. `UEB-15` steht deshalb daneben, in einem
eigenen Modul, mit beiden Grenzen durch Zusicherungen festgehalten.

### 2.2 Der Testlauf des Übungsrepositoriums

| Lauf | Vor der Herrichtung | Danach |
|---|---|---|
| `npm --prefix frontend run test` | 18 von 18 | **46 von 46** |
| `npm --prefix frontend run typecheck` | ohne Befund | ohne Befund |
| `npm --prefix frontend run lint` | ohne Befund | ohne Befund |
| `validate-framework.py --strict-overlay` | 0 Fehler, 0 Warnungen | 0 Fehler, 0 Warnungen |

**Der Backend-Strang ist unverändert nicht ausführbar** und war es auch vorher nicht; die
sieben schreibenden Aufrufe in `BookControllerTest` tragen jetzt die Rollenkopfzeile, und
der Schnittstellenvertrag führt sie als Parameter samt Statuscode 403. **Damit deckt kein
Test den Fall ab, den `UEB-14` ausmacht** – die fehlende Rolle –, und das ist Absicht.

## 3. Das Aufgabenblatt – eine Entscheidung nach zwanzig Releases

`docs/UEBUNGSAUFGABEN.md` liegt seit 0.64.0 in `tools/mentorenblatt/` und damit im
gesperrten Bereich (D-168).

**Die Messung stand seit dem 2026-09-17** (`CR-2026-077`, 7.1): **Sechs von sechzehn Läufen
haben das Blatt geöffnet**, und einer hat sich wörtlich darauf berufen – *„Das ist der in
`docs/UEBUNGSAUFGABEN.md` Aufgabe B dokumentierte, absichtliche Fehler."* Entschieden wurde
damals nicht; der Fall gehöre *„in die Übungsanlage, nicht in diesen Antrag"*.

🟢 **Der einzige aktenkundige Gegengrund ist mit diesem Release entfallen.** Er lautete:
*„Dagegen spricht, dass `<DOC_PATHS>` dann keinen Gegenstand mehr hätte und die M5-Übungen
ins Leere liefen."* Der Dokumentationspfad trägt jetzt drei echte Übungsdokumente.

> 🆕 **Die Vorbedingung eines Gegenarguments war die Lücke, die dieses Release schließt.**
> Wer einen vertagten Punkt liest, prüft, ob der Grund der Vertagung noch gilt – er kann
> durch fremde Arbeit entfallen sein, ohne dass jemand den Punkt anfasst.

**Die zehn Verweise auf das Blatt bleiben stehen** – in `README.md`, `deploy/README.md`,
`BooksPage.tsx`, `BookService.java`, `LoanRepository.java`, `BookServiceTest.java`,
`biv-deployment-hinweis.md` und im Overlay. Ein Verweis ins Leere wäre ein unerklärter
Befund; **ein Verweis auf einen gesperrten Pfad ist ein Messwert.**

## 4. Prüfung 57 – kein ungebundener Pflichtplatzhalter als Vorbedingung

Gegenstand sind der Testkatalog und alle dreizehn Testblätter. Die Pflichtmenge wird aus
`docs/PLACEHOLDER_REGISTRY.md` **abgeleitet**, nicht gepflegt.

**Der Zuschnitt arbeitet auf Teilsätzen, nicht auf Zellen.** Eine Vorbedingung nennt
häufig mehrere Zustände in einer Zelle; wer die ganze Zelle nach einer Verneinung
durchsucht, meldet jede mit, die irgendwo ein *ohne* trägt. **Das ist die Bauform, an der
Prüfung 56 in ihrem eigenen Release zweimal zu breit gemeldet hat.** Getrennt wird an
Semikolon und Punkt.

**Benannte Grenze, und sie steht im Kopfkommentar:** Die Prüfung erkennt **aufgezählte
Wendungen**, nicht jede mögliche – dieselbe Grenze, die Prüfung 29 bei Bedingungswörtern
hat.

| Einheit | Was sie belegt |
|---|---|
| **Sonde 57a** | Die Vorbedingung verlangt den Pflichtplatzhalter als nicht gesetzt – gemeldet |
| **Gegenprobe 57a** | Das unveränderte Repositorium bleibt unbeanstandet |
| **Gegenprobe 57b** | 🔴 **Der Zuschnitt:** dieselbe Verneinung in einem **anderen** Teilsatz bleibt zulässig |

## 5. Prüfung 58 – und sie hat beim ersten Lauf ihren eigenen Antrag gemeldet

Beim Anlegen von Prüfung 57 fiel auf, dass die Registereinträge der Prüfungen **55** und
**56** im Kopfkommentar des Validators auf zwei Kennungen verweisen, die an der Stelle der
Nummer einen **Platzhalter** tragen. **Diese Decision Records gibt es nicht** – die
Meldungen derselben Prüfungen nennen die richtigen.

🔴 **Prüfung 50 fängt das aus zwei Gründen nicht.** Sie gilt für `K-`, und ihr Muster träfe
den Fall auch umgestellt nicht: **Zwischen der letzten Ziffer und dem Platzhalterzeichen
steht keine Wortgrenze.** Deshalb liest Prüfung 58 alles, was auf die erste Ziffer folgt,
und prüft danach, ob die Form überhaupt stimmt.

> 🆕 **Eine Kennung, die die Form knapp verfehlt, ist für jeden Zähler unsichtbar – und
> liest sich im Fließtext trotzdem wie eine.** Das ist die gefährlichere Hälfte des
> Befundtyps *„Das Register, das seinen Gegenstand nicht führt"* (0.60.0): Dort fehlte die
> Zeile, hier fehlt die Kennung.

🔴 **Beim ersten Lauf hat die Prüfung den Änderungsantrag dieses Releases gemeldet** – er
nannte die beiden Zeichenfolgen an vier Stellen wörtlich. **Dieselbe Bewegung wie 0.60.0**,
wo der Kommentar, der die synthetische Sondenkennung erklärte, von Prüfung 50 gemeldet
wurde. Der Antrag beschreibt sie jetzt, statt sie zu nennen.

| Einheit | Was sie belegt |
|---|---|
| **Sonde 58a** | Eine `D-`Kennung ohne Registerzeile wird gemeldet |
| **Sonde 58b** | 🔴 **Der gemessene Fall:** eine Kennung mit Platzhalter statt Nummer wird gemeldet – ein Muster mit abschließender Wortgrenze übersähe sie |
| **Sonde 58c** | Ohne Registerzeilen meldet die Prüfung den verlorenen Gegenstand, statt leise zu bestehen |
| **Gegenprobe 58a** | Das unveränderte Repositorium bleibt unbeanstandet |
| **Gegenprobe 58b** | Dieselbe Nennung **mit** Registerzeile bleibt zulässig |

**Beide Sondenkennungen sind zusammengesetzt** (`"D-" + "993"` und die Platzhalterform) –
dieselbe Regel wie bei der Sonde zu Prüfung 50: Eine Sonde, deren Gegenstand die eigene
Nennung ist, darf sich nicht selbst nennen, auch nicht im Kommentar.

## 6. Abnahme

| Lauf | Ergebnis |
|---|---|
| `validate-framework.py` im Repositorium | **0 Fehler, 0 Warnungen** |
| `validate-framework.py --strict-overlay` im Übungsrepositorium | **0 Fehler, 0 Warnungen** |
| `probe-pruefungen.py`, `PYTHONIOENCODING=utf-8` | **325 Ergebniszeilen, alle bestanden** (192 Sonden, 101 Gegenproben, 12 Selbstproben, 20 Bündelkopfzeilen); 237,5 s Wanduhr auf 8 Bahnen |
| `probe-pruefungen.py` ohne Kodierungsvorgabe | **325 Ergebniszeilen, alle bestanden – zeilengleich zum ersten Lauf** (D-49); 237,2 s Wanduhr |
| Prüfung 44 (Register gegen Testblätter, beide Richtungen) | fünfzehn Präparationen, fünfzehn Kennungen |

**Vier Sonden und vier Gegenproben neu.** Die Sondenmenge lautet jetzt
`6, 14 und 18 bis 58` und steht **ausgerechnet** in allen drei Trägern.

### 6.1 Der Trockenlauf hat die Dateizahl umgeworfen

**Der erste Entwurf des Migrationshinweises sagte *neun* `TESTS.md`.** Gemessen mit
`install.py --update --dry-run` gegen eine Kopie **beider** übernehmender Projekte, am
kurzen Pfad `C:\lw-mig`:

| Ziel | Stand vorher | Dateien | Was |
|---|---|---|---|
| Übungsrepositorium (`devin-desktop`) | 0.63.0 | **8** | acht `TESTS.md`, sonst nichts |
| Pilot (`claude-code`) | 0.54.1 | **13** | kumulativ über zehn Releases – **ohne `role-re-ticket`** |

🔴 **`role-re-ticket/TESTS.md` erreicht den Piloten nicht**, weil er das Role Pack
`requirements-engineering` nicht installiert hat. **Eine Dateizahl gilt je Projekt und je
Pack, nicht allgemein** – dieselbe Lehre wie bei 0.54.0, deren Hinweis ohne Trockenlauf
geschrieben wurde und falsch lag. **Er kostet eine Minute.**

## 7. Was für das nächste Release gilt

- 🔴 **Wer eine Zahl aus einem anderen Release übernimmt, übernimmt deren Stand** – und
  der ist der **vor** den Eingriffen jenes Releases (D-164).
- 🔴 **Ein Durchgang befragt beide Dokumentenablagen** (D-165).
- 🔴 **Ein Befund an einer Testzelle gehört gegen den Skill gehalten, bevor die Zelle
  geändert wird** – zum dritten Mal in vier Releases, und zum dritten Mal hat es die
  Richtung umgedreht.
- 🟢 **Sitzungstest 5 ist der nächste Posten** (`0.65.0`), und `FW-FI-01` hat seit diesem
  Release einen registrierten Gegenstand.
- 🔴 **`UEB-07` und `UEB-08` je Lauf setzen und danach entfernen** – unverändert.

## 8. Gegenzeichnung

| Rolle | Name | Datum | Bemerkung |
|---|---|---|---|
| Durchführung | `<FRAMEWORK_OWNER>` | 2026-09-18 | Gegenprüfung, Herrichtung, zwei Prüfungen; ohne Kontingent |
| Gegenzeichnung | `<TBD: Rolle>` | `<TBD: Datum>` | |

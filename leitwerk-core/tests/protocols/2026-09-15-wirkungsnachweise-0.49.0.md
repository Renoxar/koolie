# Wirkungsnachweise 0.49.0 – die neun Strukturentscheidungen sind bestätigt

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-15 |
| Framework-Version | `0.49.0`; Vorstand `0.48.0` (`4f5dc93`) |
| Gegenstand | Der Statuswechsel von D-01 bis D-08 und D-10, die nachgezogene Standzeile und der Umbau von Sonde 46f |
| Antrag | `CR-2026-071`, D-100, D-101 |
| Grundlage | D-23 und die Auflage des Antrags: Die umgebaute Sonde MUSS gegen 0.48.0 fallen und gegen `main` bestehen; dazu ist zu messen, **was die alte Fassung auf dem neuen Stand anrichten würde** |
| Prüfmethode | Validatorlauf zwischen zwei Patches; voller Sondenlauf in **beiden** Kodierungsumgebungen (D-49); Gegenbeweis gegen einen frischen Auscheckstand des Vorstands, installiert mit dessen eigenem `install.py` |
| Ergebnis | **154 Sonden, 62 Gegenproben, 12 Selbstproben, 18 Bündelkopfzeilen – 246 Ergebniszeilen, alle bestanden**, Exit 0, in beiden Kodierungsumgebungen über 251 Zeilen **zeilengleich**. Validator 0 Fehler, 0 Warnungen. **Gegenbeweis gegen 0.48.0: genau eine Abweichung, und es ist Sonde 46f** |

## 1. Der Mechanismus aus 0.48.0 hat zum ersten Mal gegriffen

**Zwischen zwei Patches gemessen, nicht rekonstruiert.** Nach dem Statuswechsel im
Decision Log und **vor** dem Nachziehen der Standzeile lief der Validator gegen den
Arbeitsbaum:

```
FEHLER   leitwerk-core/docs/ROADMAP.md: Kriterium 4 von D-11 (Decision Records ohne
`entschieden (Vorschlag)`) ist gezählt **0**, die Standzeile nennt 9 – der Fortschritt
ist nicht nachgezogen. Der 1.0.0-Stand gehört ausgerechnet und nicht gepflegt; am
2026-09-15 lagen alle vier Zahlen daneben, ohne dass eine je falsch geschrieben worden
wäre (CR-2026-070, D-98)

Ergebnis: 1 Fehler, 0 Warnungen
```

**Genau ein Fehler, und er betrifft einen Fortschritt.** Das ist der Preis, den
`CR-2026-070` E1 ausdrücklich gewollt und benannt hat – *„Jeder Fortschritt macht den
Lauf rot, bis die Zahl nachgezogen ist"* –, und er ist bei der **ersten** Gelegenheit
fällig geworden, die es je gab.

> **Ohne diese Bauform stünde in der Roadmap heute noch neun.** Genau dieses Nachziehen
> ist der Vorgang, der bis 0.47.0 unterblieben ist – er kostet eine Zeile, und er wird
> erzwungen statt erinnert.

Nach dem Nachziehen der Standzeile auf `Kriterium 4 = 0`: **0 Fehler, 0 Warnungen.**

**Und die Meldung war brauchbar.** Sie nennt die gezählte Zahl, die geschriebene und die
Richtung – die Behebung war ein Kopiervorgang, keine Suche. Das war die Zusage des
Antrags aus 0.48.0, und dies ist ihr erster Anwendungsfall.

## 2. Der volle Sondenlauf gegen `main`

`python -u leitwerk-core/tests/scripts/probe-pruefungen.py .` – zweimal, mit und ohne
`PYTHONIOENCODING=utf-8` (Abnahmeauflage seit D-49). Die Zahlen unten stammen aus dem
**Abnahmelauf gegen den Stand, der committet wird** – ein früherer Lauf gegen einen
Zwischenstand war ebenfalls grün und zeilengleich.

| Umgebung | Exit | Ergebniszeilen | Wanduhr | Rechenzeit | Faktor |
|---|---|---|---|---|---|
| `PYTHONIOENCODING=utf-8` | **0** | 246 | 153,9 s | 1195,3 s | 7,8 |
| Locale-Vorgabe | **0** | 246 | 138,1 s | 1086,1 s | 7,9 |

**Die ersten 251 Zeilen beider Läufe sind `diff`-gleich** – das ist der Vergleich nach
D-49 und D-94; die Laufzeitauswertung darunter ist ausdrücklich **nicht** Teil der
Abnahme.

| Gattung | Anzahl |
|---|---|
| Sonden | **154** |
| Gegenproben | **62** |
| Selbstproben | **12** |
| Bündelkopfzeilen | 18 |

**Die Sondenmenge ist unverändert gegenüber 0.48.0.** Dieses Release fügt keine Prüfung
und keine Sonde hinzu; es baut **eine** um. Die drei Register, die Prüfung 40 gegen die
gezählte Menge hält, bleiben deshalb unberührt – und der Lauf belegt es.

**Die Zeile, die zählt:**

```
SONDE      46f  OK    Ein zurueckgefallener Decision Record hebt Kriterium 4 - die
                      Standzeile steht dann zu niedrig
```

**Der Aufräumer aus 0.46.0 hat in beiden Läufen geschwiegen** – keine `AUFRAEUMER`-Zeile,
also kein Arbeitsverzeichnis auf der Platte zurückgelassen.

## 3. Der Gegenbeweis gegen den Vorstand 0.48.0

**Aufbau nach der Regel:** `git archive 4f5dc93` in ein leeres Verzeichnis, installiert
mit dem **`install.py` des Vorstands** – nicht mit dem neuen, sonst trägt die
Installation Verweise auf Dateien, die es dort noch nicht gibt.

```
--- Version im Auscheckstand ---
0.48.0
--- Validator des Vorstands gegen sich selbst ---
WARNUNG  Gegenstand 2 der Prüfung 45 ist nicht gelaufen – git ist nicht erreichbar oder
… ist kein Repositorium. …
Ergebnis: 0 Fehler, 1 Warnungen
```

**Die Warnung ist richtig und gehört hierher:** Ein `git archive`-Auszug ist kein
Repositorium, und Prüfung 45 sagt, dass ihr zweiter Gegenstand deshalb **nicht** gelaufen
ist, statt ihn stillschweigend zu bestehen. Genau dafür ist sie seit 0.47.0 so gebaut.

**Der neue Sondenlauf gegen diesen Stand:**

```
SONDE      46f  FEHL  Ein zurueckgefallener Decision Record hebt Kriterium 4 - die
                      Standzeile steht dann zu niedrig  [Praeparation gebrochen]
        DECISION_LOG.md: die Statuszelle von D-10 beginnt nicht mit
        '| entschieden (`CR-2026-071`); '

Ergebnis: 1 Abweichung(en)
```

**Genau eine Abweichung, und es ist die richtige.** Alle übrigen 245 Ergebniszeilen
bestehen auch gegen den Vorstand – das ist die Probe darauf, dass dieses Release keine
andere Prüfmechanik angefasst hat.

**Und die Abweichung ist die gewollte Gattung:** `[Praeparation gebrochen]` heißt, dass
die **Sonde** ihren Gegenstand nicht findet, nicht dass die **Prüfung** ihre Wirkung
verloren hat. Die Unterscheidung gibt es seit `CR-2026-060` (D-74), und sie zahlt sich
hier zum wiederholten Mal aus: Gegen 0.48.0 gibt es keinen bestätigten Record, den man
zurückfallen lassen könnte, und die Sonde sagt genau das.

## 4. Die zweite Richtung der Auflage: was die alte Sonde auf dem neuen Stand täte

**Die Auflage verlangt beide Richtungen, und diese ist die unbequeme.** Die alte
Präparation suchte wörtlich `entschieden (Vorschlag)` in der Zeile `| D-10 |` und
ersetzte den **ersten** Treffer. Gemessen gegen den neuen Stand:

```
Suchtext 'entschieden (Vorschlag)' steht in der Zeile D-10: 1 mal
erster Treffer bei Zeichen 228 - Umfeld:
   ...oud-Nutzung im Kern | entschieden (`CR-2026-071`); **zuvor `entschieden
   (Vorschlag)`, seit 2026-09-0...

Statuszelle, Anfang VORHER : entschieden (`CR-2026-071`); **zuvor `entschie
Statuszelle, Anfang DANACH : entschieden (`CR-2026-071`); **zuvor `entschie
Pruefung 46 liest zellen[4].startswith('entschieden (Vorschlag)') -> False
```

**Sie hätte weder gegriffen noch sich beschwert.** Ihr Suchtext trifft weiterhin – aber
im **Verlaufszusatz** der Statuszelle, also an einer Stelle, die Prüfung 46 gar nicht
liest. Damit:

| Wächter | Hätte er gemeldet? |
|---|---|
| `Praeparationsfehler` (Suchtext trifft nicht) | **nein** – er trifft ja |
| Baumvergleich `[nichts praepariert]` | **nein** – der Baum ändert sich |
| Die Sonde selbst | **ja, aber als gewöhnlicher Fehlschlag** – „die Prüfung meldet nicht" |

> **Das ist der schlechteste der drei möglichen Zustände.** Eine Sonde, die etwas
> verändert, ohne ihren Gegenstand zu treffen, sieht aus wie ein Befund an der Prüfung
> und ist einer an der Sonde. Beide Wächter, die dieses Repositorium genau dafür gebaut
> hat – `Praeparationsfehler` (D-74) und der Baumvergleich (0.27.0) –, greifen in diesem
> Fall **nicht**.

**Deshalb trifft die neue Fassung den ANFANG der Statuszelle** (`| entschieden
(\`CR-2026-071\`); `) und nicht eine Zeichenkette irgendwo in ihr: Der Anfang ist genau
das, was der Zähler liest (`zellen[4].startswith(...)`). Eine Sonde, die den Gegenstand
der Prüfung trifft, kann ihn auch verlieren und sagt es dann – der Lauf gegen den
Vorstand in Abschnitt 3 ist der Beleg.

**Die Lehre, und sie ist neu:** Die Übergabe hält seit 0.38.0 fest, dass eine Änderung am
Bestand die Sonden bricht, die diesen Bestand abräumen wollten. **Neu ist der Fall, in dem
sie nicht bricht, sondern danebentrifft** – und das ist der gefährlichere. Wer eine Sonde
gegen einen Textinhalt baut, baue sie gegen **dieselbe Stelle, die die Prüfung liest**,
nicht gegen dieselbe Zeichenkette.

## 5. Was dieses Release nicht nachweist

- **Es misst kein Verhalten.** Kein Sitzungslauf, kein Client, kein Modellkontingent.
  Der Gegenstand ist eine Entscheidung und ihre Buchführung.
- **Es beantwortet keine der drei offenen Fragen** – `AP2-CC-12`, `K-20`, `K-04`. Sie
  bleiben offen und werden nur ihrem richtigen Kriterium zugeordnet.
- **Es prüft nicht, ob die neun Entscheidungen die besten wären**, sondern ob ihre
  Begründung heute trägt (`tests/protocols/2026-09-15-gegenpruefung-strukturentscheidungen.md`).
- **D-101 hat keinen Mechanismus.** Die Legende ist berichtigt, nicht geprüft. Eine
  Prüfung auf das Statusvokabular steht als Kandidat für das nächste Release.
- **Kriterium 3 sinkt nicht mit.** Dieselben neun Records tragen keine Modulstatus; die
  69 Steckbriefe stehen unverändert auf `entwurf`.

## 6. Bewertung

**Alle Auflagen des Antrags sind erfüllt.** Die umgebaute Sonde besteht gegen `main` und
fällt gegen den Vorstand – mit der richtigen Gattung von Fehlschlag. Die zweite Richtung
der Auflage ist gemessen und hat ein Ergebnis gebracht, das unbequemer ist als die
Erwartung im Antragstext; der Antragstext ist gegen die Messung berichtigt worden, nicht
umgekehrt.

**Der Wirkungsnachweis dieses Releases ist aber nicht der Sondenlauf, sondern
Abschnitt 1.** Prüfung 46 wurde in 0.48.0 mit einem ausdrücklich benannten Preis gebaut –
*jeder Fortschritt macht den Lauf rot*. Es gab seither keinen Fortschritt, an dem sich das
zeigen konnte. **Jetzt gab es einen, und der Mechanismus hat gegriffen.**

| Kriterium (D-11) | 0.48.0 | **0.49.0** |
|---|---|---|
| 1 – VERIFY-Marker | 29 | 29 |
| 2 – offene Ergebniszellen | 118 | 118 |
| 3 – Modulstatus auf `entwurf` | 69 | 69 |
| **4 – Decision Records `entschieden (Vorschlag)`** | **9** | **0** |

**Eine von vier Zahlen ist gefallen, und es war die kleinste.** Sie stand seit der
Erstfassung unverändert, durch fünfzig Releasestände hindurch. Der Vorgang, der sie gesenkt hat,
war keine Messung und kein Skript, sondern eine Entscheidung; das Werkzeug hat nur
verhindert, dass sie unbemerkt bleibt.

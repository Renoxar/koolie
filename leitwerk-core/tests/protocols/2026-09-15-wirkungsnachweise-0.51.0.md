# Wirkungsnachweise 0.51.0 – Prüfung 47, und Prüfung 46 hat zweimal gegen diesen Vorgang gegriffen

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-15 |
| Framework-Version | `0.51.0` (Vorstand `0.50.0`, Commit `0f3ed1f`) |
| Gegenstand | Der Wirksamkeitsnachweis nach D-23 für die neue **Prüfung 47** (Statusvokabular jedes Modulträgers, D-108) und die Messung der beiden Zwischenstände von Kriterium 3 |
| Antrag | `CR-2026-073`, D-105 bis D-108 |
| Prüfmethode | Fünf Sonden und drei Gegenproben in `tests/scripts/probe-pruefungen.py`; Abnahme nach D-49 in **beiden** Kodierungsumgebungen und zeilengleich zwischen seriellem und nebenläufigem Lauf; dazu zwei Zwischenmessungen des Validators zwischen den Patches |
| Ausgeführte Befehle | `python leitwerk-core/tests/scripts/validate-framework.py --root .` (nach jedem Patch); `python -u leitwerk-core/tests/scripts/probe-pruefungen.py .` (ohne und mit `PYTHONIOENCODING=utf-8`, dazu `--bahnen 1`) |
| Ergebnis | **Alle 254 Ergebniszeilen bestanden – in fünf Läufen, in beiden Kodierungsumgebungen, seriell wie nebenläufig und gegen den fertigen Baum, durchgehend zeilengleich über 259 Zeilen.** Prüfung 46 hat zweimal gemeldet – einmal gegen einen Anstieg, einmal gegen einen Rückgang; beide Male gegen diesen Vorgang selbst. **Ein Nebenbefund ist dabei angefallen und als `K-38` aufgenommen** |

## 1. Prüfung 46 hat zweimal gegriffen, und die erste Meldung war eine falsche Einordnung

Der Vorgang hat Kriterium 3 in **zwei** Schritten verändert, und zwischen ihnen wurde
gemessen. Das ist kein Zufall, sondern der Zuschnitt: Ein Anstieg, den niemand sieht,
wäre ein verschwiegener Preis.

### 1.1 Nach Patch 1 – die zwölf Statuszeilen

```
FEHLER   leitwerk-core/docs/ROADMAP.md: Kriterium 3 von D-11 (Modulstatus über `entwurf`)
ist gezählt **64**, die Standzeile nennt 52 – ein Kriterium ist zurückgefallen.
```

**Genau ein Fehler, und die Zahl ist die erwartete:** 52 + 12 = 64.

### 1.2 Nach Patch 4 – die 23 abgenommenen Träger

```
FEHLER   leitwerk-core/docs/ROADMAP.md: Kriterium 3 von D-11 (Modulstatus über `entwurf`)
ist gezählt **41**, die Standzeile nennt 52 – der Fortschritt ist nicht nachgezogen.
```

**Wieder genau ein Fehler:** 64 − 23 = 41.

**Ohne diese Bauform stünde in der Roadmap heute noch 52.** Das ist die dritte Gelegenheit
in drei Releases, bei der Prüfung 46 gegriffen hat, und die dritte, bei der sie es gegen
einen **Fortschritt** getan hat.

## 2. Nebenbefund – Prüfung 46 nennt einen vollständigeren Gegenstand einen Rückfall

Die Meldung aus Abschnitt 1.1 sagt *„ein Kriterium ist zurückgefallen"*. **Das stimmt
nicht.** Kriterium 3 ist nicht zurückgefallen; sein Gegenstand ist vollständig geworden.
Zwölf Träger werden zum ersten Mal gezählt, weil sie zum ersten Mal eine Statuszeile
führen – kein einziger Träger hat seinen Status verschlechtert.

**Die Zahl war richtig, ihre Einordnung nicht.** Prüfung 46 kennt zwei Richtungen und
leitet aus ihnen zwei Ursachen ab:

| Richtung | Meldung | Wirklich möglich |
|---|---|---|
| gezählt < geschrieben | „der Fortschritt ist nicht nachgezogen" | Fortschritt – **oder** ein geschrumpfter Gegenstand |
| gezählt > geschrieben | „ein Kriterium ist zurückgefallen" | Rückfall – **oder** ein vollständigerer Gegenstand |

**Ein Zähler kann die beiden Fälle ohne einen Vergleich mit dem Vorstand nicht trennen.**
Ob das in die Meldung gehört, ist eine eigene Frage mit einem eigenen Preis (ein
Vorstandsvergleich in einer Prüfung, die heute nur den Arbeitsbaum liest) und **gehört
nicht in einen Nebensatz beim Aufräumen** – dieselbe Begründung, mit der `CR-2026-070`
die Ableitung der Gegenprobensummen abgelehnt hat. **Aufgenommen als `K-38`.**

**Gefunden hat es nicht die Mechanik, sondern die Erwartung:** Die Meldung passte nicht
zu dem, was der Patch getan hatte. Das ist zum wiederholten Mal der billigste Prüfstein
dieses Projekts.

## 3. Die fünf Sonden und drei Gegenproben zu Prüfung 47

Die Prüfung hat vier Gegenstände; je einer trägt eine Sonde, dazu die Sonde auf den
verlorenen Anker. **Drei der fünf legen eine neue Datei an, statt eine bestehende zu
verstellen** – der Statuswert des Bestands bewegt sich mit jedem Release, und eine Sonde,
die einen Wert wörtlich sucht, misst ab dem nächsten Statuswechsel den Suchtext statt die
Prüfung. Das ist die Lehre von Sonde 46f aus 0.49.0, angewendet beim Bauen statt beim
Reparieren.

| Einheit | Präparation | Erwartete Meldung |
|---|---|---|
| **Sonde 47a** | eine neue Prompt-Datei mit Steckbrief, **ohne** Statuszeile | „der Steckbrief führt keine Zeile" – Gegenstand 2, das Loch aus `K-36` |
| **Sonde 47b** | `\| Status \| banane \|` in einer neuen Datei | „gehört nicht zum Vokabular" – Gegenstand 3, bis 0.50.0 nur in einer `SKILL.md` gefangen |
| **Sonde 47c** | der Ausfüllschlitz in `templates/SKILL_TEMPLATE.md` wird durch `entwurf` ersetzt | „die Statuszelle einer Vorlage trägt den echten Wert" – **der Defekt von 0.50.0, wiederhergestellt** |
| **Sonde 47d** | ein Ausfüllschlitz in einer Datei, die keine Vorlage ist | „trägt den Ausfüllschlitz" – die kopierte und nicht gefüllte Vorlage, der Preis aus D-104 |
| **Sonde 47e** | die Kopfzeile `\| Attribut \| Wert \|` wird im ganzen Bestand umbenannt | „kein einziger Steckbrief gefunden" – der verlorene Anker |
| **Gegenprobe 47a** | keine | Das unveränderte Repositorium bleibt unbeanstandet |
| **Gegenprobe 47b** | `pilot (Abnahme CR-2026-073)` in einer Checkliste | Ein Verlaufszusatz in Klammern bleibt zulässig – verglichen wird das **erste Wort** |
| **Gegenprobe 47c** | eine Datei mit der Steckbriefkopfzeile **hinter** einer Überschrift der Ebene 2 | Das ist kein Steckbrief und verlangt keinen Status – der Fall `templates/PLAN_TEMPLATE.md` |

### 3.1 Warum Sonde 47e anders gebaut ist als die übrigen Ankersonden

Bei den Prüfungen 28, 29, 31, 40 und 46 ist der Anker eine **Zeichenkette in einer
Datei**; die Sonde entfernt sie. Hier ist der Anker eine **Konvention über den ganzen
Bestand**. Verlöre sie sich, fände die Prüfung nichts mehr und bestünde leise – also
benennt die Sonde die Kopfzeile überall um und belegt, dass der Lauf das meldet. Die
Präparation bricht ab, wenn sie weniger als fünfzig Dateien trifft: Dann hätte sich die
Konvention geändert, und die Sonde misst ihren Suchtext statt die Prüfung.

### 3.2 Und Gegenprobe 47c ist die wichtigere Hälfte

Sie stellt den Fall her, an dem die erste Fassung der Erkennungsregel gefallen wäre.
Eine Regel, die bloß nach der Kopfzeile in den ersten sechzig Zeilen sucht, hätte von
`templates/PLAN_TEMPLATE.md` einen Statuswert verlangt – von einer Datei, deren Tabelle
das **Formular** für die Kopie ist. **Eine Prüfung, die alles meldet, besteht jede
Sonde.**

## 4. Die Abnahme nach D-49

D-49 verlangt den Lauf in **beiden** Kodierungsumgebungen und zeilengleich. Gefahren sind
drei Läufe gegen denselben Baum:

| Lauf | Umgebung | Bahnen | Ergebnis |
|---|---|---|---|
| A | ohne `PYTHONIOENCODING` | 8 | alle Sonden und Gegenproben bestanden |
| B | `PYTHONIOENCODING=utf-8` | 8 | alle Sonden und Gegenproben bestanden |
| C | ohne `PYTHONIOENCODING` | **1** (seriell) | alle Sonden und Gegenproben bestanden |

**Alle drei sind über 259 Zeilen zeichengleich** – A gegen B (die beiden
Kodierungsumgebungen) und A gegen C (nebenläufig gegen seriell).

**254 davon sind die Ergebniszeilen der Abnahme nach D-49:**

| Gattung | Anzahl |
|---|---|
| Sonden | **159** (vorher 154) |
| Gegenproben | **65** (vorher 62) |
| Selbstproben | 12 |
| Bündelkopfzeilen | 18 |
| **Summe** | **254** (vorher 246) |

**Die Laufzeiten stehen unterhalb der Trennlinie und sind ausdrücklich nicht Teil des
zeilengleichen Vergleichs** (D-94): 145,9 s (A) und 147,5 s (B) Wanduhr auf acht Bahnen
gegen **1018,0 s** seriell; die Rechenzeit lag bei 1151,2 s beziehungsweise 1160,9 s,
Faktor 7,9.

**Der Aufräumer aus 0.46.0 hat in allen Läufen geschwiegen.**

### 4.1 Der Gegenbeweis gegen den Vorstand – und er reicht ein Release weiter zurück

Der neue Validator gegen die beiden Vorstände, ausgecheckt mit `git archive` und mit
`--root` gemessen:

| Vorstand | Gegenstand 2 (fehlende Statuszeile) | Gegenstand 4 (Vorlage mit echtem Wert) |
|---|---|---|
| `0.50.0` (`0f3ed1f`) | **12** – genau die zwölf Träger, die dieses Release behebt | 0 |
| `0.49.0` (`73d7fbd`) | **12** | **4** – genau die vier Vorlagen, die `0.50.0` behoben hat |

**Prüfung 47 fängt also nicht nur den Befund ihres eigenen Releases, sondern auch den des
vorigen.** Die vier Fundstellen gegen `0.49.0` sind der Defekt aus D-104: eine Vorlage,
deren Statuszelle einen echten Wert trägt und ihn an jede Kopie weitergibt.

### 4.2 Ein Messfehler, der beinahe als Messwert durchgegangen wäre

Die erste Auszählung des Gegenbeweises meldete für `0.49.0` **null** Fundstellen des
Gegenstands 4. Das war kein Messwert, sondern die Konsolenkodierung: Der Suchtext trug
ein `ä`, und die Ausgabe des Laufs lag in der Kodierung der Konsole vor. Mit
`PYTHONIOENCODING=utf-8` waren es vier.

**Aufgefallen ist es nur, weil die Null nicht zur Erwartung passte** – zum dritten Mal in
diesem Repositorium dieselbe Lehre: *Ein Lauf, der eine Null meldet, ist erst ein
Messwert, wenn eine Ergebniszeile daneben steht.*

## 5. Der fünfte Lauf gegen den fertigen Baum

Die Läufe A bis C liefen **ohne** dieses Protokoll – zwangsläufig, denn es beschreibt
sie. `probe-pruefungen.py` kopiert aber je Sonde das **ganze** Verzeichnis: Eine Datei,
die den Validator stört, lässt **alle Gegenproben** scheitern, während die Sonden grün
bleiben. Seit 0.50.0 fährt deshalb jedes Release einen zusätzlichen Lauf gegen den
fertigen Baum.

| Lauf | Umgebung | Bahnen | Baum | Ergebnis |
|---|---|---|---|---|
| D | ohne `PYTHONIOENCODING` | 8 | mit diesem Protokoll, Ergebniszeilen noch offen | alle bestanden |
| E | ohne `PYTHONIOENCODING` | 8 | **fertig** | alle bestanden |

**Beide sind mit Lauf A zeilengleich über alle 259 Zeilen.** Das Protokoll, das Sie
gerade lesen, stört den Validator nicht – und das ist die Aussage dieser Läufe.

**Warum zwei statt einem:** Lauf D lief gegen den Baum, in dem dieses Protokoll schon
lag, aber seine eigenen Ergebniszeilen noch nicht trug – ein Zustand, in dem zwei offene
Ausfüllmarken zwei Warnungen des Validators erzeugten. Eine Gegenprobe verlangt `0
Fehler`, nicht null Warnungen, und lief deshalb durch. **Lauf E gegen den fertigen Baum
belegt, dass auch die Endfassung nicht stört.**

Die Wanduhr lag bei 158,5 s (D) und 149,6 s (E) auf acht Bahnen; sie steht wie die
übrigen Laufzeiten unterhalb der Trennlinie und außerhalb des Vergleichs (D-94).

**Jeder der beiden Läufe kostet zweieinhalb Minuten und schließt eine Lücke, die sonst
niemand sieht.**

## 6. Was diese Wirkungsnachweise nicht leisten

- **Sie belegen, dass Prüfung 47 wirkt, nicht dass ihr Gegenstand richtig ist.** Ob ein
  Träger auf `pilot` stehen **darf**, entscheidet das Review nach `01-governance.md`
  Abschnitt 5 – das ist ausdrücklich nicht maschinell, und die Prüfung behauptet es
  nicht. Die Abnahme je Träger steht in
  `tests/protocols/2026-09-15-gegenpruefung-nicht-skill-traeger.md`.
- **Sie sagen nichts über das Verhalten eines KI-Clients.** Kein Sitzungstest ist
  gefahren.
- **Sie beantworten `K-38` nicht.** Der Befund ist gemessen und benannt; die Entscheidung
  steht aus.
- **Kein Gegenbeweis gegen den Vorstand ist gefahren**, und der Grund ist der Gegenstand:
  Prüfung 47 meldet gegen `0.50.0` **zwölf** Fundstellen ihres Gegenstands 2 – das sind
  genau die zwölf Träger, die dieses Release behebt, und die Zahl steht schon in
  Abschnitt 2 der Gegenprüfung. Ein zweiter Lauf hätte dieselbe Liste noch einmal
  gezählt.

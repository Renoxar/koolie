# Wirkungsnachweise 0.46.0 – der Umbau des Sondenskripts

| Feld | Wert |
|---|---|
| Datum | 2026-09-15 |
| Gegenstand | Ausführungsplan, Nebenläufigkeit, Name und Beschreibungssatz je Einheit, Laufzeitauswertung, Aufräumer (D-94 bis D-96) |
| Antrag | `CR-2026-068` |
| Grundlage | D-23 und D-49. **Hier ist der Gegenbeweis kein Fallen von Sonden, sondern ein Abgleich:** Der Umbau ändert keine Prüfung, also darf er keine Ergebniszeile ändern außer den angekündigten |
| Ergebnis | **144 Sonden, 57 Gegenproben, 10 Selbstproben – alle bestanden, in beiden Kodierungsumgebungen zeilengleich und zwischen seriellem und nebenläufigem Lauf zeilengleich** (Exit 0). Validator: 0 Fehler, 0 Warnungen |

## 1. Der Vorstand – gemessen, bevor etwas gebaut wurde

`python leitwerk-core/tests/scripts/probe-pruefungen.py .` gegen `main` (`750ce10`, 0.45.0):

| Größe | Wert |
|---|---|
| Laufzeit | **13 min 07 s** (787 s), streng seriell |
| Ergebniszeilen | **208** – 144 Sonden, 57 Gegenproben, 7 Selbstproben |
| Ausführungseinheiten | **128** – 79 `sonde(`, 6 `sonde_ohne_wert(`, 29 `gegenprobe(`, 14 `buendel(` |
| Exit-Code | 0 |

Der Lauf sagte nicht, wo die dreizehn Minuten hingehen. Er wird **zweimal je Release**
gefahren (D-49), also kostet ein Release allein hier über eine halbe Stunde.

## 2. Die vier Abnahmeläufe

| # | Lauf | Zeilen | Sonden | Gegenproben | Selbstproben | Exit | Wanduhr |
|---|---|---|---|---|---|---|---|
| **L1** | `--bahnen 8`, ohne `PYTHONIOENCODING` | 227 | 144 | 57 | 10 | 0 | **110,6 s** |
| **L2** | `--bahnen 8`, mit `PYTHONIOENCODING=utf-8` | 227 | 144 | 57 | 10 | 0 | **110,8 s** |
| **L3** | `--bahnen 1`, ohne `PYTHONIOENCODING` | 227 | 144 | 57 | 10 | 0 | **827,4 s** (13 min 47 s) |
| **L4** | `--bahnen 16`, ohne `PYTHONIOENCODING` | 227 | 144 | 57 | 10 | 0 | **79,7 s** |

**Drei Vergleiche, alle über die 227 Zeilen oberhalb der Trennlinie:**

| Vergleich | Was er belegt | Ergebnis |
|---|---|---|
| L1 gegen L2 | die Abnahmeform nach D-49 – beide Kodierungsumgebungen | **kein Unterschied** |
| L1 gegen L3 | dass die Nebenläufigkeit die Ausgabe nicht verändert – weder Reihenfolge noch Inhalt | **kein Unterschied** |
| L1 gegen L4 | dass die Bahnenzahl die Ausgabe nicht verändert | **kein Unterschied** |

**Der zweite Vergleich ist der eigentliche Nachweis dieses Releases.** Er belegt, dass die
Sammlung der Zeilen und ihre Ausgabe in der Reihenfolge der **Anmeldung** genau das leisten,
was sie versprechen: Der nebenläufige Lauf ist vom seriellen nicht zu unterscheiden.

## 3. Der Abgleich gegen 0.45.0 – 29 Zeilen und keine weitere

`diff` über die Ergebniszeilen, 208 gegen 227:

| Art der Abweichung | Anzahl | Warum |
|---|---|---|
| verlängerte Beschreibungssätze | **10** | Einzelsonden, die statt eines Satzes nur eine Kennung trugen (D-95) |
| neue Bündelkopfzeilen | **16** | jedes Bündel nennt jetzt seinen Namen und seinen Satz |
| neue Selbstprobenzeilen | **3** | `B1` (Wortzahl), `A1` und `A2` (der Aufräumer) |
| **sonst** | **0** | |

**Die Zahl je Art ist unverändert: 144 Sonden, 57 Gegenproben – vorher wie nachher.** Keine
Prüfung ist angefasst worden, und keine Sonde hat ihren Gegenstand gewechselt.

## 4. Der erste Fallstrick: Prüfung 40 hätte den Umbau nicht überlebt

Prüfung 40 rechnet die Sondenmenge aus **zwei wörtlichen Mustern** des Sondenskripts aus
(D-86): dem Aufruf `sonde(` mit seiner Kennung und `melde(` mit der Art `SONDE` und ihr.
Ein Umbau auf ein Register mit eigener Schreibweise hätte die Sonden unsichtbar gemacht –
und Prüfung 40 hätte **leise bestanden**, denn eine leere Menge ist keine Abweichung.

**Nachgezählt vor und nach dem Umbau, mit demselben Ausdruck, den der Validator verwendet:**

| Stand | Prüfungsnummern mit Sonde | Ausgerechnete Schreibweise |
|---|---|---|
| 0.45.0 | 6, 18, 19, 20, …, 44 | `6 und 18 bis 44` |
| 0.46.0 | 6, 18, 19, 20, …, 44 | `6 und 18 bis 44` |

Deshalb ist die Aufrufstelle jeder Sonde **zeichengleich** geblieben; geändert hat sich
allein, **wann** der Aufruf seine Arbeit tut. Und deshalb heißt der Anmelder `eintragen()`:

> `anmelden("SONDE", "18b", …)` enthält die Zeichenfolge `melde(` **nicht** – dort folgt auf
> `melde` ein `n`. `anmelde("SONDE", "18b", …)` hätte sie enthalten, und Prüfung 40 hätte
> eine Sonde `18b` gezählt, die es nicht gibt. **Der Abstand zwischen beiden Namen ist ein
> Buchstabe.** Statt ihn zu riskieren, heißt die Funktion `eintragen()`.

## 5. Wo die Zeit liegt – und wo die Grenze der Nebenläufigkeit

Aus dem Auswertungsblock von L1 (874,2 s Rechenzeit in 110,6 s Wanduhr, Faktor 7,9):

| Einheit | Laufzeit | Anteil an der Rechenzeit |
|---|---|---|
| `sonden_schlitzinhalte` | **64,0 s** | 7,3 % |
| `sonden_kandidatenpruefung` | 43,8 s | 5,0 % |
| `sonden_aktivierungspruefung` | 37,2 s | 4,3 % |
| `sonden_berechtigungskoerbe` | 31,2 s | 3,6 % |
| `sonden_hookblock` | 30,4 s | 3,5 % |
| `sonden_skill_deny` | 21,4 s | 2,4 % |
| **sechs Bündel zusammen** | **228 s** | **26 %** |
| **114 Einzeleinheiten, je rund 5,8 s** | **rund 645 s** | **74 %** |

**Zwei Zahlen, die zusammen etwas sagen, das keine allein sagt.** Die Einzeleinheiten
tragen drei Viertel der *Rechenzeit* und sind beliebig teilbar; die Bündel tragen ein
Viertel und sind **gar nicht** teilbar. Damit ist die Wanduhr nach unten begrenzt:

> **Kein noch so breiter Lauf kommt unter 64,0 s**, solange `sonden_schlitzinhalte` die
> längste Einheit ist – denn ein Bündel ist die kleinste Einheit, nie seine Teile (F3). Die
> Schranke ist keine Schwäche der Umsetzung, sondern die Entscheidung selbst, sichtbar
> gemacht.

**L4 misst das nach, und das Ergebnis ist zweischneidig:**

| Lauf | Bahnen | Wanduhr | Rechenzeit | Faktor |
|---|---|---|---|---|
| L3 | 1 | 827,4 s | 827,4 s | – |
| L1 | 8 | **110,6 s** | 874,2 s | 7,9 |
| L4 | 16 | **79,7 s** | **1079,6 s** | 13,5 |

Die doppelte Bahnenzahl bringt **28 % weniger Wanduhr** und kostet **23 % mehr
Rechenzeit**. Das ist der Beleg dafür, dass nicht die Rechenzeit der Engpass ist,
sondern die Platte: Jede Einheit legt eine eigene Kopie des Repositoriums an, und
sechzehn gleichzeitige Kopiervorgänge machen jeden einzelnen langsamer. **Die 79,7 s
liegen zudem schon nahe an der Schranke von 64,0 s** – mehr Bahnen können die
längste Einheit nicht teilen.

**Deshalb bleibt die Vorgabe bei 8 und ist eine feste Zahl:** Sie holt 7,9 von
theoretisch 8 heraus, ohne Rechenzeit zu verbrennen. Was der beste Wert auf einer
anderen Maschine ist, ist damit nicht gesagt – und soll es nicht sein.

## 6. Der Aufräumer – und warum er eine eigene Selbstprobe bekommt

An **vierzehn** Stellen stand `shutil.rmtree(..., ignore_errors=True)`, während der
Kopfsatz des Skripts zusagt: *„Gearbeitet wird auf einer Kopie; das Repositorium selbst
bleibt unberührt."* Die zweite Hälfte dieser Zusage – dass die Kopie danach wieder weg ist
– hatte **keinen Mechanismus**.

`aufraeumen()` versucht dreimal über 1,5 s und meldet danach mit Pfad und Grund. **Eine
Meldung, die geschrieben und nie ausgelöst wurde, ist nach D-23 nicht vorhanden** – deshalb
zwei Selbstproben:

| Kennung | Was sie herstellt | Erwartung |
|---|---|---|
| `A1` | ein gewöhnliches Arbeitsverzeichnis mit einer Datei darin | gelöscht, **und keine Zeile im Lauf** |
| `A2` | ein Verzeichnis, das sich nicht löschen lässt | `AUFRAEUMER … bleibt liegen` mit dem Pfad, und **eine** Abweichung |

**Der Ausfall muss je Betriebssystem anders hergestellt werden, und das ist der Teil, an
dem die Probe sonst nichts gemessen hätte:**

| System | Mechanismus | Warum der andere nicht trägt |
|---|---|---|
| Windows | eine offene Datei im Verzeichnis | gemessen: `PermissionError [WinError 32]` |
| POSIX | dem Verzeichnis das Schreibrecht entziehen (`0o500`) | eine offene Datei verhindert das Löschen dort **nicht** – die Probe wäre eine Zeile, die nichts misst |

**Gemessen wird gegen eine Hilfseinheit**, nicht gegen die laufende: Der Aufräumer meldet in
die Einheit, in der er gerufen wird. Täte er das hier, zählte der absichtlich
herbeigeführte Ausfall als Abweichung des Laufs – die Selbstprobe erzeugte den Befund, den
sie misst.

**Gemessen ist damit, dass die Meldung kommt, wenn sie kommen muss.** Nicht gemessen ist,
ob drei Versuche über 1,5 s für den echten Fall reichen: In keinem der vier Abnahmeläufe
ist eine Kopie unbeabsichtigt liegen geblieben.

## 7. Selbstprobe B1 – und was sie nicht leistet

`B1` zählt die Worte jedes Beschreibungssatzes und meldet jeden Ausreißer. Vor dem Umbau
hätte sie **24 Abweichungen** gemeldet: zehn zu kurze Einzelsätze und vierzehn Bündel ohne
Satz.

**Ihre Grenze steht in ihrem Kopfkommentar, weil sie sonst mehr verspräche, als sie
leistet:** Sie zählt **Worte, nicht Sinn**. Ein Satz aus achtzehn Füllwörtern besteht sie.
Die untere Grenze fängt die Kennung, die sich als Satz ausgibt („Pack ohne
Auskunftsabschnitt", drei Worte), die obere den Absatz, der sich in eine Zeile verirrt hat.
Dazwischen entscheidet der Mensch, und das ist Absicht.

## 8. Was dieses Protokoll nicht belegt

- **Nicht, dass acht Bahnen der beste Wert sind.** Gemessen sind drei Punkte auf **einer**
  Maschine mit 32 Kernen und einer SSD. Auf einem Rechner mit anderer Platte kann die
  Kurve anders liegen; die Vorgabe ist bewusst eine feste Zahl und keine Eigenschaft der
  Maschine, sonst wären zwei Laufzeiten unvergleichbar.
- **Nicht, dass die Laufzeiten reproduzierbar sind.** Sie sind es nicht, und genau deshalb
  stehen sie unterhalb der Trennlinie. Was sie belegen, ist die **Verteilung**.
- **Nicht, welcher Fall innerhalb eines Bündels teuer ist.** Ein Bündel bekommt eine Zahl,
  nicht fünfunddreißig. Wer wissen will, welcher der sieben Eingriffe in
  `sonden_berechtigungskoerbe` die Zeit kostet, erfährt es aus diesem Lauf nicht.
- **Nicht, dass die Prüfungen richtig sind.** Dieses Release fasst keine Prüfung an; es
  verändert das Werkzeug, mit dem sie gemessen werden. Die Grenze jeder einzelnen Prüfung
  steht unverändert in ihrem Kopfkommentar.

## 9. Anmerkung zur Reihenfolge

Die vier Abnahmeläufe L1 bis L4 liefen gegen den Arbeitsbaum **ohne diese Datei**, die es
zum Zeitpunkt der Läufe noch nicht gab – jedes Protokoll hat dieses Problem, weil es
über Läufe berichtet, die vor ihm stattfanden.

**Deshalb ein fünfter Lauf gegen den vollständigen Baum**, so wie er in den Commit geht:
`--bahnen 8`, ohne `PYTHONIOENCODING`, 227 Zeilen, Exit 0, 111,7 s – und **zeilengleich
zu L1**. Der Validatorlauf gegen denselben Baum meldet 0 Fehler und 0 Warnungen.

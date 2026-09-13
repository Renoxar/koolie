# Änderungsantrag `CR-2026-060`

| Feld | Inhalt |
|---|---|
| Titel | Der stumme Bruch wird laut – Präparationswächter, Zellenzählung des Decision Logs, und eine Prüfung, die den richtigen Text beanstandet |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-13 |
| Betroffene Artefakte | `tests/scripts/probe-pruefungen.py` (Runner und elf Präparationen), `tests/scripts/validate-framework.py` (Prüfung 36 neu, gemeinsame Zellenzerlegung an vier Stellen), `governance/DECISION_LOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** (Prüfwerkzeuge des Frameworks) |
| Art | Änderung; erledigt zwei seit mehreren Releases benannte, nicht umgesetzte Punkte und einen dritten, den die Gegenprüfung gefunden hat |
| Dringlichkeit | regulär. **Kein P1:** Keiner der drei Punkte betrifft eine Zusage gegenüber einem Projekt. Sie betreffen die Werkzeuge, mit denen dieses Projekt seine Zusagen prüft – und deren Ausfall ist deshalb still |

## 1. Anlass

Zwei Punkte stehen seit mehreren Releases im Repositorium und sind nicht umgesetzt:

| Punkt | Seit | Wie oft aufgetreten |
|---|---|---|
| **Soll eine Gegenprobe ihre Summen ableiten?** Ermessensfrage, ausdrücklich als solche benannt | 0.34.0-Protokoll Abschnitt 4.x | **viermal in Folge** (0.34.0, 0.35.0, 0.36.0, 0.37.0), jedes Mal von Hand nachgezogen; mit 0.36.0 kam eine Kennungskollision dazu (`G-18`) |
| **Die Zellen der Decision-Log-Tabellen zählt nichts.** Prüfvorschlag, ausdrücklich nicht Teil seines Releases | 0.35.0-Protokoll Abschnitt 7 | **zweimal bestätigt** – beim Eintragen von D-64 und beim Eintragen von D-69 |

**Beide sind gegengeprüft** (`tests/protocols/2026-09-13-gegenpruefung-stumme-brueche.md`,
drei Messungen an Kopien des Repositoriums). Beide bestätigen sich, **und die Gegenprüfung
findet einen dritten Punkt, den keiner von beiden nennt.**

### 1.1 Befund 1: Die halb greifende Präparation sieht aus wie ein Prüfungsfehler

Eine Kopie mit einem **echten** zwanzigsten Grenzfall – der Zustand, den ein Release
hinterlässt – bekam die heutige Präparation der Gegenprobe 30. Die erste ihrer beiden
Ersetzungen traf nicht, die zweite schon.

```text
Baum veraendert: True            <- der baumhash-Waechter meldet nichts
FEHLER  leitwerk-core/tests/EDGE_CASES.md: 21 Grenzfallzeilen, der Steckbrief nennt 20.
        Eine Zahl, die nicht stimmt, ist kein Nachweis
Gegenprobe bestanden: False
```

**Die Gegenprobe fällt mit einer Meldung, die aussieht, als habe sie einen echten Fehler im
Repositorium gefunden.** Dort ist keiner – die Sonde hat ihren eigenen Suchtext verloren.

> **`baumhash` ist ein Alles-oder-nichts-Wächter.** Bei *n* Ersetzungen belegt er „mindestens
> eine hat gegriffen", nie „alle". Deshalb melden sich die einteiligen Präparationen selbst
> und die mehrteiligen nicht. **Das ist eine Lücke im Runner, keine Nachlässigkeit beim
> Schreiben der Sonden** – und sie schließt sich nicht dadurch, dass man Suchtexte
> sorgfältiger pflegt.

**Die Lücke ist größer als die Frage, die sie ausgelöst hat.** Ausgezählt:

| Lage | Anzahl | Deckt `baumhash`? |
|---|---|---|
| **a** über einen Runner mit `baumhash`, **eine** Ersetzung | Regelfall | **ja**, mit erklärender Meldung – **kein Befund** |
| **b** über einen solchen Runner, **mehrere** Ersetzungen | 3 Stellen, zusammen 9 Ersetzungen in 5 Dateien | **nein** |
| **c** Bündelfunktionen mit direktem `melde()` | 9 Funktionen, 35 Meldestellen, darin 3 mit Textpräparation (7 Ersetzungen) | **nein, gar nicht** |

**Neun Bündelfunktionen mit 35 Meldestellen laufen ohne jeden Präparationswächter.** Runner
**mit** Wächter gibt es drei: `sonde()`, `gegenprobe()`, `sonde_ohne_wert()`.

### 1.2 Befund 2: Die Zellen der Decision-Log-Tabellen zählt nichts

Gezählt über sechs Auscheckstände, maskierte Striche als Inhalt behandelt:

| Stand | Abweichende Zeilen |
|---|---|
| 0.32.0, 0.33.0 | **je 1** – D-29 |
| 0.34.0 | **4** – D-29, D-61, D-62, D-63 |
| 0.35.0 bis 0.37.0 | 0 |

**Der Befund bestätigt sich und ist heute behoben.** Eine Prüfung, die jetzt entsteht, fängt
**nichts** – dieselbe Lage wie bei Prüfung 35. **Der Unterschied ist erheblich:** Prüfung 35
fand auch im Vorstand nichts, weil ihr Gegenstand dort nicht existiert. Diese Prüfung hätte
gegen 0.34.0 vier Fundstellen gemeldet. **Ihr Gegenbeweis ist kein Kunstgriff, sondern ein
Abzählen.**

**D-29 stand fünfundzwanzig Releases lang zerrissen** und wurde von jedem Validatorlauf
gesehen. Gefunden hat sie ein Mensch beim Eintragen einer anderen Zeile.

### 1.3 Befund 3, nicht gesucht: Prüfung 30 beanstandet einen GFM-korrekten Text

Prüfung 30 zerlegt eine Grenzfallzeile mit `.split("|")`. GFM verlangt für einen Strich
**innerhalb** einer Zelle die Maskierung `\|`; `.split("|")` sieht sie nicht. Gemessen an
einer Kopie, mit demselben Codespan, den **D-69 seit 0.36.0 trägt**:

```text
FEHLER   leitwerk-core/tests/EDGE_CASES.md: Grenzfall G-14 hat 9 Spalten statt 7
```

**Das ist die Bauform, vor der der Wirkungsnachweis zu Prüfung 28 warnt:** eine Prüfung ohne
die nötige Unterscheidung beanstandet den richtigen Text. Heute ist der Fehlalarm latent –
keine Grenzfallzeile trägt einen maskierten Strich. **Er zählt trotzdem, aus zwei Gründen:**

1. **Er verbietet es, Prüfung 36 naiv zu bauen.** Naiv gezählt trügen D-29 und D-69 heute
   **acht** Zellen statt sechs; die neue Prüfung meldete an ihrem ersten Lauf **zwei
   Fehlalarme auf korrektem Text.**
2. **Die Zellenzerlegung liegt viermal im Validator, jedes Mal eigenhändig** – `:1686`,
   `:1838`, `:2528`, `:3033`. Eine fünfte Stelle wäre die fünfte Gelegenheit für denselben
   Fehler.

## 2. Die Ermessensfrage, um die es eigentlich geht

> Soll die Gegenprobe ihre Summen aus der Tabelle **ableiten** – und beweist sie dann noch,
> was sie beweisen soll, oder verdoppelt sie nur die Rechenweise der Prüfung?

**Die Gegenfrage ist echt, und keine Messung entscheidet sie.** Was die Gegenprüfung beiträgt,
ist die Trennung zweier Dinge, die vier Releases lang als eines behandelt wurden:

| | Frage | Art |
|---|---|---|
| **a** | Woher nimmt die Gegenprobe ihre Zielsumme? | **Ermessen** – abgeleitet ist bequemer und belegt weniger |
| **b** | Was passiert, wenn ein Suchtext der Präparation nicht mehr trifft? | **kein Ermessen** – heute erscheint es als Prüfungsfehler, und das ist schlicht falsch |

**b ist unabhängig von a zu beheben.** Ist b behoben, verliert a den größten Teil seines
Drucks: Der wörtliche Wert bleibt der teurere Weg, aber sein Bruch kostet dann eine Zeile
Diagnose statt einer Fehlersuche im Repositorium.

## 3. Vorgeschlagene Änderung

1. **Präparationswächter** in `probe-pruefungen.py`: ein Helfer `ersetze(pfad, *paare)`, der
   jede Ersetzung einzeln auf die erwartete Trefferzahl prüft und bei Abweichung eine
   `Praeparationsfehler`-Ausnahme wirft. `sonde()` und `gegenprobe()` fangen sie und melden
   `[Suchtext trifft nicht: '…']`; die Bündelfunktionen laufen über einen Wrapper, der sie
   ebenso meldet und das Bündel abbricht.
2. **Kennungswächter** `frei(pfad, kennung)`: Eine synthetische Kennung, die eine Präparation
   einführt (`G-99`, `Z9`), darf im Zieldokument nicht bereits vorkommen. Bricht sie laut ab,
   sobald ein Release die Kennung wirklich vergibt.
3. **Sechs Präparationen** auf den Helfer umgestellt – die drei mehrteiligen und die drei mit
   Suchtext in den Bündeln; zusammen 14 Ersetzungsstellen und zwei Zeileneinfügungen. **Alle
   drei Runner mit `baumhash` fangen den Abbruch**, die neun Bündelfunktionen laufen über den
   Wrapper.
4. **Die Summen bleiben wörtlich verankert** (siehe E1) – mit dem Wächter davor.
5. **Prüfung 36 (neu)**: Jede Tabellenzeile in `DECISION_LOG.md` führt so viele Zellen wie die
   Kopfzeile ihrer Tabelle, maskierte Striche als Inhalt.
6. **Eine gemeinsame Zellenzerlegung** im Validator, verwendet an allen vier Stellen; damit
   ist auch der Fehlalarm aus 1.3 behoben.

## 4. Auswirkungen

- **Keine Einstufung ändert sich, keine Summe, keine Zusage.** Der Antrag berührt
  ausschließlich Prüfwerkzeuge.
- **Prüfung 36 fängt heute nichts** – das steht so im Wirkungsnachweis, und ihr Gegenbeweis
  läuft gegen 0.34.0.
- **Prüfung 30 wird toleranter** gegenüber einer Schreibweise, die sie heute zu Unrecht
  beanstandet. Sie wird an keiner Stelle schwächer: Ein unmaskierter Strich zerreißt die Zeile
  weiterhin, und genau das meldet sie.
- **Der Sondenlauf bekommt eine neue Meldeform.** Ein `[Suchtext trifft nicht]` ist ein
  **Fehlschlag**, wie `[nichts praepariert]` – es zählt in `fehler` und lässt den Lauf rot
  werden. Das ist gewollt: Eine Sonde, die nicht präpariert, hat nichts gemessen.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | Soll eine Gegenprobe ihre Summen aus der Tabelle **ableiten**? | **Nein – sie bleiben wörtlich verankert.** Eine abgeleitete Summe rechnet nach derselben Regel wie die Prüfung; rechnet die Prüfung falsch, rechnet die Gegenprobe genauso falsch und besteht. **Der wörtlich gesetzte Wert ist ein unabhängiger Erwartungswert von Hand** – das ist der Beleg, den eine Gegenprobe schuldet | **Der Bruch bleibt.** Jede neue Matrixzeile und jeder neue Grenzfall bricht die Verankerung weiterhin, und jemand muss sie nachziehen. **Der Antrag beseitigt den Preis nicht, er macht ihn bezahlbar:** Statt einer Fehlersuche im Repositorium kostet er eine Zeile, die den nicht mehr passenden Suchtext nennt. **Wer das für zu wenig hält, hat recht in der Sache und muss dann die Zielsumme woanders herholen als aus der Rechenweise der Prüfung** – eine dritte Quelle gibt es nicht |
| **E2** | Bekommt `probe-pruefungen.py` einen Präparationswächter? | **Ja, und zwar genau dort, wo `baumhash` blind ist** – bei mehrteiligen Präparationen und in den Bündelfunktionen. **Nicht** bei den einteiligen: Dort meldet der Runner heute schon das Richtige, und eine zweite Prüfung derselben Sache wäre Ballast | **Sechs Präparationen zu ändern**, in der Datei, die alle Nachweise trägt. Ein Fehler dabei fällt im selben Lauf auf – das ist der Vorteil, den dieses Skript vor allen anderen hat. **Und: Der Wächter deckt nur den Suchtext, nicht die Absicht.** Eine Ersetzung, die trifft und das Falsche tut, findet er nicht |
| **E3** | Bekommt eine synthetische Kennung einen Wächter gegen Kollision? | **Ja.** Am 13.09. trug die Gegenprobe 30 ausgerechnet `G-18` – dieselbe Kennung, die 0.36.0 wirklich vergeben hat. **Beide Fallen waren in der Übergabe benannt, und beide sind trotzdem zugeschnappt**; eine benannte Falle, in die man zweimal tritt, gehört in den Code, nicht in eine Datei außerhalb des Repositoriums | Drei Zeilen mehr je betroffener Präparation. **Der Wächter ist genau so klug wie die Kennung, die man ihm gibt** – er prüft Abwesenheit, nicht Eignung |
| **E4** | Entsteht Prüfung 36 für die Zellen des Decision Logs? | **Ja.** Vier zerrissene Zeilen in 0.34.0, eine davon seit fünfundzwanzig Releases; gefunden hat sie jedes Mal ein Mensch. Prüfung 30 tut dasselbe für `EDGE_CASES.md`, die Bauform liegt vor | **Sie fängt heute nichts** – das ist mit derselben Ehrlichkeit zu sagen wie bei Prüfung 35. **Anders als dort ist ihr Gegenbeweis aber ein Abzählen und keine Konstruktion:** vier Fundstellen gegen 0.34.0. Wer sie dennoch als Risikoabwehr verkauft, überzeichnet |
| **E5** | Wird der Fehlalarm aus 1.3 mitbehoben, und wie weit? | **Ja, über eine gemeinsame Zellenzerlegung an allen vier Stellen** – nicht nur bei Prüfung 30. Die Zählweise liegt viermal im Validator; eine gemeinsame Funktion macht aus vier Gelegenheiten für denselben Fehler eine | **Drei der vier Stellen ändern ihr Verhalten heute nicht** – sie nehmen die erste Zelle oder suchen über ein Muster. Der Umbau ist dort reine Vorsorge, und Vorsorge in fremdem Code ist ein Risiko. **Die Alternative – nur Prüfung 30 berichtigen – lässt drei Stellen mit der falschen Zählweise stehen**, und die nächste Prüfung kopiert eine davon |
| **E6** | Ein eigenes Release oder Anhang an das nächste inhaltliche? | **Ein eigenes Release, `0.38.0`.** Der Gegenstand ist geschlossen und hat mit dem nächsten inhaltlichen nichts zu tun; angehängt würde er in dessen Protokoll verschwinden – wie viermal zuvor, als er als Nebensatz beim Aufräumen behandelt wurde | **Das dreizehnte Release in zwei Tagen**, und keines seiner Ergebnisse ist eine Messung am Client. Der Preis ist Buchhaltung. **Der Gewinn ist, dass diese Frage aufhört, in Nebensätzen zu wandern** |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle sechs Fragen wie vorgelegt.** E1 die Summen bleiben wörtlich, der Bruch wird laut statt beseitigt; E2 Präparationswächter genau dort, wo `baumhash` blind ist; E3 Kennungswächter; E4 Prüfung 36, begründet als Verankerung mit abzählbarem Gegenbeweis; E5 gemeinsame Zellenzerlegung an allen vier Stellen; E6 eigenes Release `0.38.0` |
| Datum | 2026-09-13 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | D-74 (eine Präparation, die nicht greift, meldet sich als solche – und eine Gegenprobe leitet ihre Zielsumme nicht aus der Rechenweise der Prüfung ab), D-75 (eine Tabellenzelle endet am unmaskierten Strich, und diese Zählung liegt einmal) |
| Auflagen | **Die Begründung für Prüfung 36 wird nicht zur Risikobehauptung aufgewertet** – sie fängt heute nichts, und der Wirkungsnachweis sagt es. **Der Gegenbeweis läuft gegen 0.34.0**, nicht gegen den unmittelbaren Vorstand: Gegen 0.37.0 fände sie nichts, und eine Null ohne diese Erklärung wäre irreführend. **Und E1 wird als das ausgewiesen, was sie ist:** eine Entscheidung gegen die bequemere Lösung mit einem Preis, der bleibt |
| Ziel-Release | `0.38.0` |
| Umsetzung | umgesetzt mit `0.38.0` |

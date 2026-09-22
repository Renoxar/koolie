# Wirkungsnachweise Release 0.38.0 – der stumme Bruch wird laut

| Feld | Wert |
|---|---|
| Gegenstand | `CR-2026-060`, D-74 und D-75: Präparations- und Kennungswächter im Sondenskript, Prüfung 36 für die Zellen des Decision Logs, und eine gemeinsame Zellenzerlegung an allen vier Stellen des Validators |
| Datum | 2026-09-13 |
| Vorstand | `a8132fd` (0.37.0) |
| Grundlage der Zusagen | `tests/protocols/2026-09-13-gegenpruefung-stumme-brueche.md`, drei Messungen an Kopien des Repositoriums |
| Ergebnis | **Validator 0 Fehler, 0 Warnungen. 134 Sonden, Gegenproben und Selbstproben bestanden** (90 Sonden, 37 Gegenproben, 7 Selbstproben) – **in beiden Kodierungsumgebungen**. Gegen den unmittelbaren Vorstand fällt **keine** Fundstelle, und das ist vorhergesagt |

## 1. Was neu geprüft wird

| Prüfung | Gegenstand | Sonden | Gegenprobe |
|---|---|---|---|
| **36 (neu)** | Jede Tabellenzeile in `governance/DECISION_LOG.md` führt so viele Zellen wie der Kopf ihrer Tabelle, maskierte Striche als Inhalt (D-75) | 36a, 36b, 36c | maskierter Strich bleibt unbeanstandet – die Schreibweise von D-69 |
| **30 (berichtigt)** | Sie zerlegt über `tabellenzellen()` und zählt einen maskierten Strich nicht mehr als Trenner | – | mitgeprüft über die Gegenprobe 36 und den Repo-Lauf |
| **Wächter (neu)** | `ersetzt()`, `zeile_nach()` und `frei()` melden eine Präparation, die nicht greift, als solche (D-74) | – | **7 Selbstproben**, W1 bis W5 und K1/K2 |

**Die Gegenprobe 36 ist hier die wichtigere Hälfte**, und das ist keine Theorie: Eine naive
Zählung mit `.split("|")` meldet D-29 und D-69 als achtspaltig, obwohl beide ihren Strich
korrekt maskieren und sechsspaltig rendern. **Ohne diese Gegenprobe wäre Prüfung 36 mit zwei
Fehlalarmen auf richtigem Text entstanden.**

## 2. Der Gegenbeweis – er läuft gegen 0.34.0, nicht gegen den Vorstand

**Prüfung 36 findet gegen 0.37.0 nichts, und das stand vor dem Bauen im Antrag** (`CR-2026-060`
E4): Alle Zeilen sind seit 0.35.0 in Ordnung, von Hand berichtigt. **Sie ist eine Verankerung,
keine Behebung** – dieselbe Bauart wie Prüfung 35 und der fünfte Gegenstand der Prüfung 32.

**Der Unterschied zu Prüfung 35 ist erheblich und gehört genannt:** Prüfung 35 fand auch im
Vorstand nichts, weil ihr Gegenstand dort nicht existiert. Prüfung 36 hätte gegen 0.34.0 vier
Fundstellen gemeldet. **Ihr Gegenbeweis ist ein Abzählen, keine Konstruktion.**

### 2.1 Zwei Zahlen, und beide gehören hierher

| Stand | **wie ausgeliefert** (voller Lauf gegen die installierte Fassung) | **isoliert** (nur Prüfung 36 gegen die Datei) |
|---|---|---|
| 0.32.0 | **nicht messbar** – siehe 2.2 | **1** (D-29) |
| 0.33.0 | **1** (D-29) | **1** (D-29) |
| 0.34.0 | **4** (D-29, D-61, D-62, D-63) | **4** |
| 0.35.0 | 0 | 0 |
| 0.36.0 | – | 0 |
| 0.37.0 (Vorstand) | 0 | 0 |
| Arbeitsbaum (0.38.0) | 0 | 0 |

Jeder Stand wurde frisch ausgecheckt (`git archive`), **mit seinem eigenen `install.py`**
installiert und bekam erst danach den neuen Validator.

**D-29 stand fünfundzwanzig Releases lang zerrissen** – seit 0.10.x – und wurde von jedem
Validatorlauf und jedem Wirkungsnachweis gesehen. Gefunden hat sie ein Mensch beim Eintragen
einer anderen Zeile.

### 2.2 Gegen 0.32.0 startet der neue Validator nicht – und die erste Zahl war ein Absturz

Der erste Gegenbeweislauf meldete für 0.32.0 „0 Fehler gesamt, 0 aus Prüfung 36". **Das
widersprach der Dateizählung**, die dort D-29 mit acht Zellen findet. Nachgesehen:

```text
ModuleNotFoundError: No module named 'overlay_status'
```

`overlay_status.py` entstand erst mit 0.33.0 (D-58). Der neue Validator lässt sich gegen 0.32.0
also gar nicht ausführen; die Null kam aus einem **Abbruch vor der ersten Prüfung**, nicht aus
einem Befund.

> **Ein Vorhandensein belegt sich selbst, ein Fehlen nicht.** Die Null sah aus wie ein Messwert
> und war keiner. Aufgefallen ist sie nur, weil eine zweite, unabhängige Zählung danebenlag –
> und das ist der Grund, warum diese Tabelle **zwei** Spalten hat. Wer nur die erste liest,
> hielte 0.32.0 für sauber.

Die isolierte Messung fährt **die echte Funktion** `check_decision_log_zellen`, nicht einen
Nachbau: Der neue Validator wird als Modul geladen, und die Prüfung läuft gegen einen Baum, der
nur die `DECISION_LOG.md` des jeweiligen Standes enthält.

## 3. Was beim Bauen aufgefallen ist

### 3.1 Die eigene Zählung war zu grob – zweimal

Die Lücke sollte beziffert werden: Wie viele Präparationen deckt `baumhash` nicht? Über den
Syntaxbaum gezählt kamen zunächst **„zehn Bündelfunktionen, neun Ersetzungen"** heraus. Beides
war falsch:

- Der Zähler hielt eine Ersetzung in einer **Diagnosemeldung**
  (`ausgabe.replace(marker, "<Marker entfernt>")`) für eine Präparation.
- Er hielt `sonde_ohne_wert()` für wächterlos, obwohl die Funktion einen `baumhash` trägt –
  **es gibt drei Runner mit Wächter**, nicht zwei.

Richtig sind **neun Bündelfunktionen mit 35 Meldestellen**, davon drei mit Textpräparation, und
**sechs umzustellende Präparationen** mit 14 Ersetzungsstellen und zwei Zeileneinfügungen.

> **Ein Zähler unterscheidet Präparation und Diagnose nicht.** Das musste ein Blick in die
> sechs Stellen tun. Wie schon 76 statt 248 und 25 statt 20: **Wer hier eine Zahl liest, zählt
> sie besser nach – auch die eigene, und besonders die aus dem eigenen Skript.**

### 3.2 `sonde_ohne_wert()` trägt denselben Block wie `sonde()`

Das erste Patchskript brach ab: Der Suchtext für den Fang der `Praeparationsfehler` traf
**zweimal**. Ursache ist keine Kopie aus Versehen – beide Runner prüfen denselben `baumhash`,
und beide brauchen den Fang. Die Trefferzahl wurde auf 2 gesetzt, nicht der Suchtext verengt.

**Der Zellenwächter im Patchskript hat sich zum dritten Mal bewährt** – hier als Trefferzahl:
Hätte das Skript blind ersetzt, wäre nur einer der beiden Runner abgesichert worden, und
niemand hätte es gemerkt.

### 3.3 Ein deutsches Anführungszeichen hat ein Patchskript zerlegt

Beim Backlog-Eintrag des Piloten beendete ein gerades `"` in `…Arbeitsverzeichnisses".` den
Python-String mitten im Satz; der Parser meldete daraufhin „leading zeros in decimal integer
literals". **Die Fehlermeldung zeigte auf eine Ziffernfolge, der Fehler lag im Zitatzeichen.**
Zu schreiben war das typografische `“`.

## 4. Sondenlauf

| Umgebung | Sonden | Gegenproben | Selbstproben | Ergebnis |
|---|---|---|---|---|
| ohne `PYTHONIOENCODING` | 90 | 37 | 7 | alle bestanden |
| mit `PYTHONIOENCODING=utf-8` | 90 | 37 | 7 | alle bestanden |

134 = 123 aus 0.37.0 plus **3 Sonden, 1 Gegenprobe und 7 Selbstproben**. Der Validator meldet in
beiden Umgebungen 0 Fehler und 0 Warnungen.

**Die Selbstproben sind eine neue Gattung in diesem Skript.** Sie brauchen weder Kopie noch
Validatorlauf – ihr Gegenstand ist Textarithmetik – und sie belegen den Wächter, statt ihn zu
behaupten. **Ohne sie wäre er die erste ungeprüfte Zusage dieses Skripts**, und ein Wächter, der
still ausfällt, ist genau der Befundtyp, gegen den er gebaut ist.

W4 ist die interessanteste: Sie stellt **die halbe Präparation** her – die erste Ersetzung
trifft, die zweite nicht – und belegt, dass dann nichts geschrieben wird. W5 belegt, dass die
Meldung den Suchtext nennt, der nicht mehr passt.

## 5. Was dieses Release nicht belegt

- **Prüfung 36 fängt heute nichts**, und kein Gegenbeweis gegen den unmittelbaren Vorstand kann
  das ändern. Siehe Abschnitt 2. **Ihre Begründung ist eine Verankerung, keine Risikoabwehr.**
- **Sie prüft die Anzahl, nicht den Inhalt.** Eine Zeile, in der Begründung und Alternativen
  vertauscht sind, besteht sie – dieselbe Grenze, die Prüfung 31 für ihre Arithmetik benennt.
- **Sie prüft eine Datei.** Die übrigen Tabellen des Repositoriums haben eigene Prüfungen (30,
  31) oder keine.
- **Der Präparationswächter deckt den Suchtext, nicht die Absicht.** Eine Ersetzung, die trifft
  und das Falsche tut, findet er nicht.
- **Drei der vier umgestellten Zerlegungsstellen ändern ihr Verhalten heute nicht.**
  `check_hook_ablageort` nimmt die erste Zelle, `_uebersicht_pruefen` sucht über ein Muster;
  ein maskierter Strich an der jeweils entscheidenden Stelle ist **nicht eingesetzt worden**.
  Der Umbau ist dort Vorsorge, und Vorsorge in fremdem Code ist selbst ein Risiko.
- **Die Summen bleiben wörtlich verankert, und der Preis bleibt.** Jede neue Matrixzeile und
  jeder neue Grenzfall bricht die Verankerung weiterhin. Dieses Release beseitigt den Bruch
  nicht, es macht ihn laut.
- **Kein Lauf gegen einen Client.** Das Release ändert ausschließlich Prüfwerkzeuge.

## 6. Gegenzeichnung

| Rolle | Name/Kennung | Datum | Ergebnis bestätigt |
|---|---|---|---|
| `<FRAMEWORK_OWNER>` | `<TBD>` | `<TBD>` | `<TBD>` |

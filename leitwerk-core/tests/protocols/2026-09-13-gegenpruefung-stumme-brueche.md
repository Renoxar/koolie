# Gegenprüfung: der stumme Bruch – eine halb greifende Präparation, eine ungezählte Tabelle, und eine Prüfung, die den richtigen Text beanstandet

| Feld | Wert |
|---|---|
| Gegenstand | Zwei seit mehreren Releases benannte, nicht umgesetzte Punkte: (1) die **Ermessensfrage**, ob eine Gegenprobe ihre Summen ableiten soll – viermal in Folge aufgetreten; (2) der **Prüfvorschlag** aus dem 0.35.0-Protokoll, Abschnitt 7: die Zellen der Decision-Log-Tabellen zählt nichts |
| Anlass | Beide stehen in der Roadmap und in der Übergabe als offen. Nach D-23 gehört ein Befund vor der Umsetzung gegengeprüft, auch wenn er aus dem eigenen Haus stammt |
| Datum | 2026-09-13 |
| Framework-Version | 0.37.0 (Auscheckstand `a8132fd`, Arbeitsbaum sauber, Validator 0/0) |
| Prüfmethode | **Drei Messungen an Kopien des Repositoriums, keine Codelektüre allein.** (1) Die heutige Präparation der Gegenprobe 30 auf einen Baum angewandt, der einen zwanzigsten Grenzfall trägt – der Zustand, den ein Release hinterlässt; (2) die Zellenzahlen des Decision Logs über sechs Auscheckstände hinweg gezählt, mit und ohne Rücksicht auf maskierte Striche; (3) ein maskierter Strich in eine Grenzfallzeile gesetzt und der Validator dagegen gefahren |
| Umgebung | Windows 11, Python 3.14.4, NTFS |
| Ergebnis | **Beide Befunde bestätigen sich. Die Gegenprüfung findet einen dritten, den keiner der beiden nennt** – und er ist der einzige, der heute einen falschen Fehler erzeugen kann |

## 0. Der Zusammenhang in einem Satz

**Alle drei Punkte sind dieselbe Bauform: eine Prüfung oder eine Sonde, deren Bruch nicht als
Bruch erscheint.** Die halbe Präparation sieht aus wie ein Prüfungsfehler, die ungezählte
Tabelle sieht aus wie eine geprüfte, und die naive Spaltenzählung sieht aus wie ein Befund.
Der wiederkehrende Befundtyp des Projekts lautet *eine Zusage, die mehr verspricht, als sie
leistet*; hier steht er dreimal in derselben Woche.

## 1. Befund 1: Die halb greifende Präparation meldet sich nicht als solche

### 1.1 Was behauptet wird

Aus dem 0.34.0-Protokoll, seither dreimal wiederholt: Die Gegenproben 30 und 31 verankern
Summen **wörtlich**, die die jeweilige Prüfung ausrechnet. Ändert ein Release die Summe,
greift der Suchtext ins Leere. Die Übergabe fügt hinzu: *„Zwei melden sich selbst als
`[nichts praepariert]` – die anderen präparieren halb und fallen an der Zahl."*

### 1.2 Was gemessen dabei herauskommt

Eine Kopie bekam einen **echten** zwanzigsten Grenzfall samt nachgezogener Anzahl – der
Zustand, den ein Release hinterlässt. Der Validator meldet darauf `0 Fehler, 0 Warnungen`.
Danach lief die Präparation der Gegenprobe 30 wörtlich so, wie sie heute im Skript steht.

| Schritt | Ergebnis |
|---|---|
| Anzahl im Steckbrief von 19 auf 20 (erste Ersetzung) | **trifft nicht** – dort steht bereits 20 |
| Zeile `G-99` vor Abschnitt 3 einfügen (zweite Ersetzung) | **trifft** |
| `baumhash` vorher gegen nachher | **verschieden** – der Wächter meldet nichts |
| Validatorlauf | `FEHLER … 21 Grenzfallzeilen, der Steckbrief nennt 20. Eine Zahl, die nicht stimmt, ist kein Nachweis` |
| Gegenprobe 30 | **FEHL**, mit genau dieser Meldung |

**Der Befund bestätigt sich, und er ist schärfer als seine Beschreibung.** Die Gegenprobe fällt
nicht nur – sie fällt mit einer Meldung, die den Eindruck erweckt, sie habe einen **echten
Fehler im Repositorium** gefunden. Wer die Ausgabe liest, sucht den Fehler in `EDGE_CASES.md`.
Dort ist keiner: Die Sonde hat ihren eigenen Suchtext verloren.

> **`baumhash` ist ein Alles-oder-nichts-Wächter.** Bei einer Präparation aus *n* Ersetzungen
> belegt er „mindestens eine hat gegriffen", nie „alle". Genau deshalb melden sich die
> einteiligen Präparationen selbst und die mehrteiligen nicht. **Das ist keine Nachlässigkeit
> beim Schreiben der Sonden, sondern eine Lücke im Runner** – und sie schließt sich nicht
> dadurch, dass man die Suchtexte sorgfältiger pflegt.

### 1.3 Wie weit die Lücke reicht – und wo `baumhash` deckt

Ausgezählt über den Syntaxbaum von `probe-pruefungen.py`. **Drei Lagen, und nur zwei davon
sind Befund:**

| Lage | Anzahl | Deckt `baumhash`? |
|---|---|---|
| **a** Präparation über einen Runner mit `baumhash`, **eine** Ersetzung | der Regelfall | **ja** – und die Meldung sagt sogar, was zu tun ist: „vermutlich passt der Suchtext der Sonde nicht mehr" |
| **b** Präparation über einen solchen Runner, **mehrere** Ersetzungen | **3** Stellen: `_grenzfall_ergaenzen` (2), `_zeile_mit_summe` (5 plus eine Einfügung, in 2 Dateien), `_zusaetzliches_pfadfeld` (dieselbe Ersetzung in 2 Manifesten) | **nein** – eine gegriffene Ersetzung genügt ihm |
| **c** Bündelfunktionen, die `melde()` direkt rufen | **9** Funktionen mit zusammen **35** Meldestellen, darin **3** mit Textpräparation (7 Ersetzungen) | **nein, gar nicht** – diese Runner haben keinen Wächter |

**Lage a ist kein Befund.** Der Runner meldet dort genau das Richtige, und das ist der Grund,
warum die Übergabe von „zwei melden sich selbst" spricht. **Runner mit `baumhash` gibt es
drei:** `sonde()`, `gegenprobe()` und `sonde_ohne_wert()`.

**Lage b und c sind der Befund.** Die neun Bündelfunktionen haben **gar keinen** Wächter; ihre
35 Meldestellen sind damit die größere Fläche, auch wenn heute nur drei von ihnen einen
Suchtext führen, der ins Leere gehen könnte. Die übrigen präparieren über Installationsläufe,
Dateilöschungen und Umgebungsvariablen.

**Zu ändern sind damit sechs Präparationen** mit zusammen **14 Ersetzungsstellen und zwei
Zeileneinfügungen**. Das ist ein kleiner Gegenstand; viermal von Hand nachgezogen ist er
trotzdem.

> **Die erste Auszählung war zu grob, und das gehört hierher.** Über den Syntaxbaum gezählt
> ergaben sich zunächst „zehn Bündelfunktionen, neun Ersetzungen" – der Zähler hielt eine
> Ersetzung in einer **Diagnosemeldung** (`ausgabe.replace(marker, "<Marker entfernt>")`) für
> eine Präparation und `sonde_ohne_wert()` für wächterlos, obwohl die Funktion einen
> `baumhash` trägt. **Ein Zähler unterscheidet Präparation und Diagnose nicht**; das musste
> ein Blick in die sechs Stellen tun. Wie schon 76 statt 248 und 25 statt 20: **Wer hier eine
> Zahl liest, zählt sie besser nach – auch die eigene.**

## 2. Befund 2: Die Zellen der Decision-Log-Tabellen zählt nichts

### 2.1 Was behauptet wird

0.35.0-Protokoll Abschnitt 7: Vier zerrissene Zeilen wurden von Hand berichtigt, drei davon
aus dem Vorgängerrelease, eine seit 0.10.x. **Gezählt hat das nichts.** Prüfung 30 tut
dasselbe längst für `EDGE_CASES.md`.

### 2.2 Was gemessen dabei herauskommt

Die Zellenzahlen wurden über sechs Auscheckstände gezählt – je Tabelle des Decision Logs die
Zellenzahl ihrer Kopfzeile als Sollwert, maskierte Striche als Inhalt behandelt:

| Stand | Abweichende Zeilen |
|---|---|
| 0.32.0 (`a76778e`) | **1** – D-29 |
| 0.33.0 (`47fa382`) | **1** – D-29 |
| 0.34.0 (`2c1351b`) | **4** – D-29, D-61, D-62, D-63 |
| 0.35.0 (`7082ef3`) | 0 |
| 0.36.0 (`4444c83`) | 0 |
| 0.37.0 (`74e087b`, heute) | 0 |

**Der Befund bestätigt sich – und er ist heute behoben.** Eine Prüfung, die jetzt entsteht,
fängt **nichts**. Das ist dieselbe Lage wie bei Prüfung 35 und bei dem fünften Gegenstand der
Prüfung 32, und sie gehört mit derselben Ehrlichkeit begründet: **eine Verankerung, keine
Behebung.**

> **Der Unterschied zu Prüfung 35 ist allerdings erheblich und spricht für diese Prüfung:**
> Prüfung 35 fand auch im Vorstand nichts, weil ihr Gegenstand dort nicht existiert. Diese
> Prüfung hätte gegen 0.34.0 **vier** Fundstellen gemeldet und gegen 0.32.0 und 0.33.0 je
> eine. Ihr Gegenbeweis ist damit keine Konstruktion, sondern ein Abzählen.

### 2.3 Und D-29 stand fünfundzwanzig Releases lang zerrissen

D-29 entstand mit 0.10.x. Die Zeile wurde zwischen 0.10.x und 0.35.0 von jedem Validatorlauf
und von jedem Wirkungsnachweis gesehen und von keinem gezählt. **Gefunden hat sie ein Mensch
beim Eintragen einer anderen Zeile.**

## 3. Befund 3, nicht gesucht: Prüfung 30 zählt einen maskierten Strich als Spaltentrenner

### 3.1 Der Fund

Prüfung 30 zerlegt eine Grenzfallzeile mit `zeile.strip().strip("|").split("|")`. GFM verlangt
für einen Strich **innerhalb** einer Tabellenzelle die Maskierung `\|`; gerendert bleibt die
Zeile dann vollständig. `.split("|")` sieht die Maskierung nicht.

Gemessen an einer Kopie: In Grenzfall **G-14** wurde in der Prosa ein Codespan mit maskiertem
Strich ergänzt – dieselbe Schreibweise, die **D-69 des Decision Logs seit 0.36.0 trägt**:

```text
FEHLER   leitwerk-core/tests/EDGE_CASES.md: Grenzfall G-14 hat 9 Spalten statt 7
         (Nr., Grenzfall, Entscheidung, Betriebsmodus, Kontrollstufe, Rollen, Fundstelle)
```

**Prüfung 30 beanstandet einen GFM-korrekten Text.** Das ist genau die Bauform, vor der der
Wirkungsnachweis zu Prüfung 28 warnt: *eine Prüfung ohne die nötige Unterscheidung hätte den
richtigen Text beanstandet.*

### 3.2 Warum das heute niemand sieht – und warum es trotzdem zählt

Keine Grenzfallzeile trägt heute einen maskierten Strich. **Der Fehlalarm ist latent, nicht
aktuell.** Er zählt trotzdem aus zwei Gründen:

1. **Er verbietet es, die neue Prüfung naiv zu bauen.** Nach der naiven Zählweise trügen D-29
   und D-69 heute **acht** Zellen statt sechs – die neue Prüfung meldete an ihrem ersten Lauf
   **zwei Fehlalarme auf korrektem Text.** Ohne diese Messung wäre das erst nach dem Bau
   aufgefallen, wie bei Prüfung 34 beim ersten Lauf.
2. **Die Zählweise liegt viermal im Validator**, jedes Mal eigenhändig: `check_hook_ablageort`
   (`:1686`, erste Zelle), `_tabellenzeilen` (`:1838`, Prüfungen 20/27), `check_grenzfaelle`
   (`:2528`, Prüfung 30), `_uebersicht_pruefen` (`:3033`, Prüfung 31). Eine fünfte Stelle wäre
   die fünfte Gelegenheit für denselben Fehler.

**Betroffen ist heute nur Prüfung 30** – die anderen drei nehmen entweder nur die erste Zelle
oder suchen in der ganzen Zeile. Das mindert den Fund nicht: Eine Prüfung, die den richtigen
Text beanstandet, wiegt schwerer als eine, die einen falschen durchlässt, denn sie kostet
Vertrauen in alle anderen.

## 4. Die Ermessensfrage, um die es eigentlich geht

Sie steht seit dem 0.34.0-Protokoll und ist nie entschieden worden:

> Soll die Gegenprobe ihre Summen aus der Tabelle **ableiten** – und beweist sie dann noch,
> was sie beweisen soll, oder verdoppelt sie nur die Rechenweise der Prüfung?

**Die Gegenfrage ist echt, und die Messung entscheidet sie nicht.** Was die Messung beiträgt,
ist die Trennung zweier Dinge, die bisher als eines behandelt wurden:

| | Frage | Art |
|---|---|---|
| **a** | Woher nimmt die Gegenprobe ihre Zielsumme? | **Ermessen** – eine abgeleitete Summe ist bequemer und belegt weniger |
| **b** | Was passiert, wenn ein Suchtext der Präparation nicht mehr trifft? | **kein Ermessen** – heute erscheint es als Prüfungsfehler, und das ist schlicht falsch |

**Punkt b ist unabhängig von Punkt a zu beheben.** Wird er behoben, verliert Punkt a den
größten Teil seines Drucks: Der wörtlich verankerte Wert bleibt der teurere Weg, aber sein
Bruch kostet dann eine Zeile Diagnose statt einer Fehlersuche im Repositorium.

## 5. Was diese Gegenprüfung nicht leistet

- **Sie misst keine Clientsitzung.** Alle drei Messungen laufen gegen den Validator und gegen
  Kopien des Repositoriums. Das ist hier der richtige Gegenstand – es geht um Prüfungen, nicht
  um Durchsetzung –, aber es ist zu benennen.
- **Sie sagt nichts darüber, ob die Einstufungen richtig sind**, die in den gezählten Tabellen
  stehen. Die Zellenzahl ist Arithmetik, nicht Inhalt; dieselbe Grenze, die Prüfung 31 für
  sich selbst benennt.
- **Sie hat die anderen drei Zählstellen nicht durchgemessen**, sondern gelesen. Dass
  `check_hook_ablageort` nur die erste Zelle nimmt und `_uebersicht_pruefen` eine Zelle über
  ein Muster sucht, steht im Code; ein maskierter Strich an der jeweils entscheidenden Stelle
  ist nicht eingesetzt worden.
- **Sie prüft nicht, ob GFM in jeder Renderumgebung gleich maskiert.** Zugrunde gelegt ist die
  GFM-Spezifikation und das Verhalten, das D-69 und `CR-2026-055` bereits voraussetzen.

## 6. Gegenzeichnung

| Rolle | Name/Kennung | Datum | Ergebnis bestätigt |
|---|---|---|---|
| `<FRAMEWORK_OWNER>` | `<TBD>` | `<TBD>` | `<TBD>` |

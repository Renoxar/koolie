# Änderungsantrag `CR-2026-064`

| Feld | Inhalt |
|---|---|
| Titel | Das Register der Prüfungen wird nicht nachgezählt – fünf Zahlen über den Prüfapparat, keine davon stimmt |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-14 |
| Betroffene Artefakte | `tests/scripts/validate-framework.py` (Prüfung 40 neu, Kopfkommentar: Eintrag 39 und 40, Satz zum Wirkungsnachweis), `tests/scripts/probe-pruefungen.py` (Kopfkommentar, sechs Sonden, zwei Gegenproben), `tests/TEST_CATALOG.md` (`FW-KO-01`, `FW-KO-05`), `governance/DECISION_LOG.md`, `docs/ROADMAP.md`, `CHANGELOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – der Prüfapparat und sein Register sind Framework-Gut |
| Art | Änderung; Anlass ist ein Nebenbefund aus dem Migrationslauf am Piloten (Kandidat 2 der Übergabe) |
| Dringlichkeit | **P2.** Nichts ist ausgeliefert falsch *durchsetzbar*; falsch ist, was das Projekt über seinen eigenen Prüfstand behauptet. **Ein Abnahmetest (`FW-KO-05`) ist davon betroffen und würde heute halb gefahren und ganz gemeldet** |

## 1. Anlass

Beim Lesen von Prüfung 37 für den Migrationslauf am Piloten
(`tests/protocols/2026-09-14-migrationslauf-pilot.md`) ist aufgefallen: Der Kopfkommentar von
`validate-framework.py` führt die Prüfungen **1 bis 38**. **Prüfung 39 ist mit 0.41.0
entstanden und steht dort nicht.**

**Gegengeprüft** (`tests/protocols/2026-09-14-gegenpruefung-pruefregister.md`, elf Messungen,
sämtlich abzählend). **Der Befund bestätigt sich – und die Zählung war wieder zu klein.**

### 1.1 Es sind fünf, nicht eine

| # | Träger | sagt | ist | falsch seit | Releases |
|---|---|---|---|---|---|
| **A1** | `validate-framework.py`, Register im Kopfkommentar | Prüfungen **1 bis 38** | 1 bis **39** | 0.41.0 | **1** |
| **A2** | `validate-framework.py`, Satz zum Wirkungsnachweis | „für die Prüfungen **18 bis 30**" | **6 und 18 bis 39** | 0.33.0 | **9** |
| **A3** | `probe-pruefungen.py`, Kopfkommentar | eine Release-Chronik, die mit **0.29.0** endet | **6 und 18 bis 39** | 0.30.0 | **12** |
| **A4** | `TEST_CATALOG.md`, `FW-KO-01` Prüfmittel | „für die Prüfungen **6, 18 bis 31**" | **6 und 18 bis 39** | 0.34.0 | **8** |
| **A5** | `TEST_CATALOG.md`, `FW-KO-05` Prüfmittel | „Die **zwölf** Grenzfälle einzeln … prüfen" | **20** | 0.33.0 | **9** |

**Keine der fünf ist falsch geschrieben worden.** Alle fünf waren bei ihrer Einführung richtig
und sind stehen geblieben, während ihr Gegenstand weiterwuchs. In **zehn von zwölf** Releases
hat sich mindestens eine der drei Zahlen bewegt.

### 1.2 Warum das kein Schönheitsfehler ist

**D-23 hängt daran.** Eine Prüfung gilt erst als vorhanden, wenn eine Sonde sie meldet. Woran
liest man ab, welche Prüfung eine Sonde hat? An A2, A3 und A4 – **und alle drei sagen etwas
Falsches.** Sie untertreiben: Wer sich auf A4 verlässt, hält die Prüfungen 32 bis 39 für
unbelegt. Eine untertreibende Zusage ist in diesem Projekt der seltenere Fall; schädlich ist
sie trotzdem, weil sie Arbeit anstößt, die getan ist.

**A5 ist keine Registerzeile, sondern eine Arbeitsanweisung.** `FW-KO-05` steht auf `offen`
und sagt, was in einer Sitzung zu tun ist: „Die zwölf Grenzfälle einzeln … prüfen." **Wer ihn
heute fährt, prüft zwölf von zwanzig und meldet ihn bestanden.**

**A1 verletzt eine Entscheidung, die ein Release alt ist.** `CR-2026-062` hat den
Kopfkommentar eigens zur Ermessensfrage gemacht – **E7: „Kopfkommentar 32 bis 38"** – und das
Nachziehen beschlossen. `CR-2026-063` führt dieselbe Datei in den betroffenen Artefakten, baut
Prüfung 39 und zieht den Kopfkommentar nicht nach. **Eine Entscheidung, die nur in einem
Antrag steht, hält bis zum nächsten Antrag.**

### 1.3 Die Entlastung, die den Zuschnitt entscheidet

`docs/ROADMAP.md` nennt ebenfalls „Zwölf Grenzfälle"; `CR-2026-052` und der Wirkungsnachweis
zu 0.32.0 tun es auch. **Alle drei sind richtig** – sie beschreiben den Stand von 0.32.0.
**Ohne diese Messung wäre beim Nachziehen aus drei richtigen Zeilen eine falsche Suche
geworden.** Die Prüfung, die hier vorgeschlagen wird, liest deshalb ausschließlich die Träger,
die ein **Register** führen, und keine Vorgeschichte.

### 1.4 Der erste Entwurf der Prüfung ist gefallen

Der naheliegende Anker – die Kopfkommentare der Prüfungen – trägt gemessen **drei** Formen
(`# Pruefung N:`, `# N:`, `# Pruefungen N bis M`), und eine vierte sieht aus wie ein Kopf und
ist keiner: `# Pruefung 37 und dieselbe Ehrlichkeit: …` im Block von Prüfung 39. **Der erste
Zähler hat sie für einen Kopf gehalten.** Aufgefallen ist es nur, weil der Verlauf über die
Releases bei 0.39.0 eine höchste Prüfung 36 meldete, während die Sonden schon bis 37 reichten
– **eine Zahl, die nicht zur Erwartung passte.**

## 2. Was die Behebung sein muss – und was sie nicht sein kann

**Nicht sein kann sie: die Einträge erzeugen.** Sie tragen Prosa – was die Prüfung tut, welche
Entscheidungen sie trägt, wo ihre Grenze liegt. Das ist der Wert des Registers und nicht
ausrechenbar. **Ausrechenbar ist allein die Vollständigkeit.**

**Sein muss sie: eine Prüfung, die den Bestand abzählt und gegen die Register hält.** Dieselbe
Bauform, die das Projekt für die Grenzfalltabelle (Prüfung 30), die Durchsetzungstiefe
(Prüfung 31) und die Berechtigungskörbe (Prüfung 37) schon gewählt hat. Der Leitsatz steht
seit 0.33.0 im Bestand: **Wo die Grenze eines Begriffs eindeutig ist, gehört die Zahl
ausgerechnet, nicht gepflegt.** Die Menge der Prüfungen ist eindeutig.

## 3. Vorgeschlagene Änderung

1. **Die fünf Aussagen werden nachgezogen** – A1 bis A5, in der Schreibweise, die Prüfung 40
   ausrechnet.
2. **Prüfung 40 (neu)** in `validate-framework.py`, vier Gegenstände:
   1. **Verlorener Anker.** Die vier Ankertexte sind auffindbar: die Registerüberschrift und
      der Satz zum Wirkungsnachweis in `validate-framework.py`, der Kopfsatz von
      `probe-pruefungen.py`, die Zeilen `FW-KO-01` und `FW-KO-05` in `TEST_CATALOG.md`. Fehlt
      einer, meldet die Prüfung sein Fehlen selbst (seit 0.32.0 Pflicht).
   2. **Das Register ist lückenlos und vollständig.** Keine Lücke von 1 bis zur höchsten
      geführten Nummer; und die höchste geführte Nummer ist die höchste, die in den beiden
      Prüfskripten als `Prüfung N` oder `Prüfungen N bis M` genannt wird.
   3. **Die Sondenmenge wird an drei Stellen gleich genannt** – im Satz des Validators, im
      Kopfsatz des Sondenskripts und in der Prüfmittelspalte von `FW-KO-01` – in der
      kanonischen Schreibweise, die die Prüfung aus `probe-pruefungen.py` ausrechnet.
   4. **Die Grenzfallanzahl in `FW-KO-05`** ist die gezählte. Prüfung 30 rechnet sie innerhalb
      von `EDGE_CASES.md` nach; außerhalb nennt sie nur `FW-KO-05`, und dort als
      Arbeitsanweisung.
3. **Sechs Sonden und zwei Gegenproben** zu Prüfung 40. Die zweite Gegenprobe ist die
   wichtigere: Ein Querverweis auf eine kleinere Prüfungsnummer im Fließtext eines
   Kommentars darf **nicht** als fehlender Registereintrag gemeldet werden – das ist genau
   der Fall, an dem der erste Entwurf gefallen ist.
4. **Der Kopfsatz von `probe-pruefungen.py` wird ersetzt**, nicht ergänzt: Er ist als
   Release-Chronik gebaut und wird deshalb bei jedem Release falsch.

## 4. Auswirkungen

| Bereich | Auswirkung |
|---|---|
| Validatorlauf | **Fünf Fehler mehr im Vorstand** – eine je Abweichung A1 bis A5 –, null nach dem Nachziehen. Die Prüfung hängt an keinem Manifestfeld und läuft deshalb in **jeder** Installation und in jedem Pack – anders als Prüfung 33 (Befund B02) |
| Erzeugte Artefakte | **keine.** Prüfung 40 liest ausschließlich Dateien unter `<CORE_DIR>/`; eine Installation ändert sich nicht |
| Bestehende Installationen | **keine Migrationshinweise.** Wer `leitwerk-core/` ersetzt, bekommt die Prüfung mit; sie kann in einer Installation nur anschlagen, wenn dort am Kern gearbeitet wurde – und dann ist die Meldung richtig |
| Prosa | **Drei Stellen sind künftig in der Schreibweise gebunden** (die kanonische Sondenspanne), eine trägt statt eines Zahlworts eine Ziffer |
| `devin-desktop` | unverändert betroffen wie `claude-code`; die Prüfung ist packunabhängig |

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | Wird das Register gepflegt und bewacht – oder aus dem Code **erzeugt**? | **Gepflegt und bewacht.** Die Einträge tragen Prosa, die kein Generator schreibt; ausrechenbar ist nur die Vollständigkeit. Bauform von `CR-2026-063` E3: geschrieben, nicht erzeugt, und von einer Prüfung gehalten | **Pflege bleibt Pflege.** Die Prüfung fängt das Vergessen, nicht den falschen Satz: Ein Eintrag, der etwas anderes beschreibt als seine Prüfung tut, läuft durch. **Die Gegenposition ist vertretbar** – ein erzeugtes Register wäre nie falsch, es wäre nur ärmer |
| **E2** | Woran erkennt die Prüfung, wie viele Prüfungen es gibt? | **An der höchsten Nummer, die in den beiden Prüfskripten als `Prüfung N` genannt wird, plus Lückenlosigkeit des Registers.** **Verworfen: die Kopfkommentare als Anker** – gemessen tragen sie drei Formen, und eine Querverweiszeile sieht aus wie ein Kopf. Der erste Entwurf ist genau daran gefallen | **Sie zählt Nennungen, nicht Prüfungen.** Wer eine Prüfung baut und ihre Nummer nirgends schreibt, wird nicht gefangen – dieselbe Ehrlichkeit wie Gegenstand 2 von Prüfung 38. **Und sie ist an eine Nummernfolge gebunden**: Prüfungen ohne Nummer gäbe es nicht mehr |
| **E3** | Wird die Sondenmenge in einer **festen Schreibweise** verlangt? | **Ja, kanonisch gerendert und wörtlich verglichen** („6 und 18 bis 39"). Die Fehlermeldung nennt die richtige Zeichenkette und ist damit selbstheilend | **Drei Stellen Prosa sind gebunden.** Bauform von D-82 mit umgekehrtem Vorzeichen: dort war der wörtliche Vergleich ein **Messergebnis**, hier ist er eine **Entscheidung** – und eine Entscheidung gegen die Formulierungsfreiheit an drei Sätzen |
| **E4** | Gehört `TEST_CATALOG.md` in eine Prüfung des Validators – ein Testblatt ist kein Laufzeitartefakt? | **Ja.** `FW-KO-01` ist das **Abnahmekriterium** des Releases; was seine Prüfmittelspalte nennt, ist eine Zusage über den Umfang des Nachweises. Eine falsche Zusage dort ist schwerer als eine im Kommentar | **Der Validator liest damit ein Dokument des Prüfverfahrens.** Sein Gegenstand bleibt die **Zahl**, nicht das Verfahren – und das gehört in den Kopfkommentar, sonst wächst die Prüfung beim nächsten Mal in die Bewertung hinein |
| **E5** | Und die Grenzfallanzahl in `FW-KO-05`? | **Ja, als Ziffer.** Ein Zahlwort ließe sich nur über eine Tabelle deutscher Zahlwörter nachrechnen – **ein zweites Register neben dem ersten**, und genau der Befundtyp, den dieser Antrag behebt | **Die Zelle trägt künftig `20` statt „zwölf".** Und die Prüfung liest ausschließlich `TEST_CATALOG.md`: Die Nennungen in Roadmap, `CR-2026-052` und Protokoll sind **Vorgeschichte und richtig** – wer sie mitzöge, machte aus drei richtigen Zeilen drei falsche |
| **E6** | Bleibt die Release-Chronik im Kopfsatz von `probe-pruefungen.py` erhalten? | **Nein, ersetzt.** Der Satz ist als Chronik gebaut und wird deshalb bei **jedem** Release falsch. Was bleibt, ist die aktuelle Menge und der D-23-Grund | **Eine Herkunftsangabe geht verloren** – welches Release welche Sonde gebracht hat. Sie steht im Änderungsverlauf, und dort gehört sie hin |
| **E7** | Eigenes Release oder Anhang an das nächste? | **Ein eigenes Release, `0.42.0`.** Der Gegenstand ist geschlossen, und die Prüfung **fängt heute etwas** – erwartet fünf Fundstellen im Vorstand, eine je Abweichung | **Das siebzehnte Release in drei Tagen.** Und es ist das erste seit 0.34.0, dessen Gegenbeweis ein **Abzählen** ist und keine Konstruktion |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle sieben Fragen wie vorgelegt.** E1 gepflegt und bewacht, nicht erzeugt; E2 die höchste genannte Nummer plus Lückenlosigkeit, nicht die Kommentarform; E3 kanonische Schreibweise, wörtlich verglichen; E4 `TEST_CATALOG.md` gehört dazu, Gegenstand ist die Zahl; E5 die Grenzfallanzahl als Ziffer, und nur in `TEST_CATALOG.md`; E6 der Kopfsatz des Sondenskripts wird ersetzt; E7 eigenes Release `0.42.0` |
| Datum | 2026-09-14 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | D-85 (das Register der Prüfungen wird nachgezählt, nicht gepflegt – Bestand, Register und Sondenmenge decken sich an allen drei Trägern), D-86 (eine Zahl über den Prüfapparat steht außerhalb ihrer Quelle nur dort, wo sie nachgerechnet wird – und eine Nennung in der Vorgeschichte ist kein Register) |
| Auflagen | **Der Gegenbeweis ist ein Abzählen, kein Konstrukt** – Prüfung 40 muss gegen 0.41.0 genau die fünf Fundstellen melden, die dieser Antrag nennt, und die Zahl gehört ins Protokoll. **Die Entlastung gehört ebenfalls hinein:** Die drei richtigen Nennungen in Roadmap, `CR-2026-052` und Protokoll bleiben unangetastet, und die Prüfung darf sie nicht melden. **Und die Grenze wird benannt:** Die Prüfung belegt Vollständigkeit, nicht Richtigkeit der Einträge |
| Ziel-Release | `0.42.0` |
| Umsetzung | umgesetzt mit `0.42.0` |

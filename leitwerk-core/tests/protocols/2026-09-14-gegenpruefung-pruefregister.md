# Gegenprüfung: Prüfung 39 steht nicht im Register – und sie ist die jüngste von fünf

| Feld | Wert |
|---|---|
| Gegenstand | Beim Lesen von Prüfung 37 für den Migrationslauf am Piloten ist aufgefallen: Der Kopfkommentar von `validate-framework.py` führt die Prüfungen **1 bis 38**. **Prüfung 39 ist mit 0.41.0 entstanden und steht dort nicht** |
| Anlass | Kein Kandidat der Übergabe, kein externer Bericht – ein Nebenbefund aus Kandidat 2. Nach D-23 gehört er vor der Umsetzung gegengeprüft, gerade weil er auf den ersten Blick Kosmetik ist |
| Datum | 2026-09-14 |
| Framework-Version | 0.41.0 (Auscheckstand `b71d038`, Arbeitsbaum sauber, Validator 0/0) |
| Prüfmethode | **Elf Messungen, sämtlich abzählend.** M1 bis M8 halten jede Registeraussage gegen den gemessenen Bestand; M9 ist ein **Entlastungslauf** an einer Nennung, die gleich aussieht und richtig ist; M10 und M11 datieren jede Abweichung über den Änderungsverlauf. Kein Messwert dieses Protokolls stammt aus einer Lektüre allein |
| Umgebung | Windows 11, Python 3.14.4; Auswertungsskript im Scratchpad, rein lesend |
| Ergebnis | **Der Befund bestätigt sich und er ist größer, als er aussah.** Es sind **fünf** falsche Aussagen über den Prüfapparat an **drei** Trägern. Prüfung 39 ist die **jüngste** davon; die älteste steht seit **zwölf** Releases. **Und die Zählung war wieder zu klein:** aus einer wurden fünf |

## 0. Der Befund in einem Satz

**Das Projekt lässt seine Prüfungen ihre Gegenstände nachzählen und führt über die Prüfungen
selbst fünf handgepflegte Zahlen, von denen keine stimmt.**

## 1. Was gemessen wurde

| Nr. | Messung | Quelle |
|---|---|---|
| M1 | Welche Nummern führt das Register im Kopfkommentar von `validate-framework.py`? | Kopfkommentar, Abschnitt „Prüft (statisch, ohne laufenden KI-Client)" |
| M2 | Welche Prüfungsnummern kommen im Code selbst vor? | `validate-framework.py` |
| M3 | Deckung M1 gegen M2, in beide Richtungen | – |
| M4 | Für welche Prüfungen führt `probe-pruefungen.py` Sonden und Gegenproben? | Aufrufe `sonde(…)`, `gegenprobe(…)`, `melde("SONDE", …)`, `melde("GEGENPROBE", …)` |
| M5 | Was sagt der Satz zum Wirkungsnachweis im Kopfkommentar des Validators? | dort |
| M6 | Was sagt der Kopfkommentar von `probe-pruefungen.py`? | dort |
| M7 | Was nennt die Prüfmittelspalte von `FW-KO-01`? | `tests/TEST_CATALOG.md` |
| M8 | Was nennt die Prüfmittelspalte von `FW-KO-05`, und wie viele Grenzfälle gibt es? | `tests/TEST_CATALOG.md`, `tests/EDGE_CASES.md` |
| M9 | **Entlastung:** Die Nennung „Zwölf Grenzfälle" in `docs/ROADMAP.md` – falsch oder richtig? | `docs/ROADMAP.md` |
| M10 | Wann ist jede Aussage in den Bestand gekommen? | `git log -S` |
| M11 | Ab welchem Release war sie falsch? | Auswertung jedes Release-Commits |

## 2. Die fünf Abweichungen

| # | Träger | sagt | ist | falsch seit | Releases |
|---|---|---|---|---|---|
| **A1** | `validate-framework.py`, Register im Kopfkommentar | Prüfungen **1 bis 38** (39 Einträge mit `9a`) | 1 bis **39** | 0.41.0 | **1** |
| **A2** | `validate-framework.py`, Satz zum Wirkungsnachweis | „für die Prüfungen **18 bis 30**" | **6 und 18 bis 39** | 0.33.0 | **9** |
| **A3** | `probe-pruefungen.py`, Kopfkommentar | eine Release-Chronik, die mit **0.29.0** endet | **6 und 18 bis 39** | 0.30.0 | **12** |
| **A4** | `TEST_CATALOG.md`, `FW-KO-01` Prüfmittel | „für die Prüfungen **6, 18 bis 31**" | **6 und 18 bis 39** | 0.34.0 | **8** |
| **A5** | `TEST_CATALOG.md`, `FW-KO-05` Prüfmittel | „Die **zwölf** Grenzfälle einzeln … prüfen" | **20** | 0.33.0 | **9** |

**Jede der fünf war bei ihrer Einführung richtig.** Keine ist falsch geschrieben worden; alle
fünf sind stehen geblieben, während ihr Gegenstand weiterwuchs. Das ist der Unterschied
zwischen einem Schreibfehler und einem Register ohne Nachzählung – und er entscheidet die
Behebung: **Nachziehen allein löst nichts, es setzt die Uhr nur zurück.**

### 2.1 Der Verlauf, Release für Release (M11)

| Release | höchste Prüfung | Sonden für | Grenzfälle |
|---|---|---|---|
| 0.29.0 | 25 | 6 bis 25 | – |
| 0.30.0 | 26 | 6 bis 26 | – |
| 0.31.0 | 27 | 6 bis 27 | – |
| 0.32.0 | 30 | 6 bis 30 | **12** |
| 0.33.0 | 31 | 6 bis 31 | 13 |
| 0.34.0 | 32 | 6 bis 32 | 15 |
| 0.35.0 | 33 | 6 bis 33 | 17 |
| 0.36.0 | 34 | 6 bis 34 | 18 |
| 0.37.0 | 35 | 6 bis 35 | 19 |
| 0.38.0 | 36 | 6 bis 36 | 19 |
| 0.39.0 | 37 | 6 bis 37 | 19 |
| 0.40.0 | 38 | 6 bis 38 | 19 |
| **0.41.0** | **39** | **6 bis 39** | **20** |

**Die Tabelle zeigt, warum die Behebung eine Prüfung sein muss und keine Textänderung:** In
zehn von zwölf Releases hat sich mindestens eine der drei Zahlen bewegt.

## 3. Der Entlastungslauf (M9)

`docs/ROADMAP.md` nennt ebenfalls „**Zwölf Grenzfälle** in `tests/EDGE_CASES.md`". Die Zeile
sieht aus wie A5 und ist es nicht: Sie steht unter der Überschrift **„Was 0.32.0 gebracht
hat"** und beschreibt den Stand jenes Releases. **Dort ist zwölf richtig.**

**Ohne diese Messung wäre beim Nachziehen aus einer richtigen Zeile eine falsche geworden** –
genau der Fehler, den das Repositorium als Fallstrick führt: die Vorgeschichte ist kein
Register. Die Prüfung, die aus diesem Befund folgt, liest deshalb `TEST_CATALOG.md` und
**nicht** die Roadmap.

## 4. Der erste Entwurf der Prüfung ist gefallen – und das gehört ins Protokoll

Der naheliegende Anker für „welche Prüfungen gibt es" sind die Kopfkommentare. **Gemessen
tragen sie drei Formen**, und eine vierte sieht aus wie ein Kopf und ist keiner:

| Form | Beispiel | Vorkommen |
|---|---|---|
| `# Pruefung N: …` | `# Pruefung 33: Die Abbildung von permissions.deny …` | der Regelfall |
| `# N: …` | `# 37: Die drei Koerbe der Berechtigungsdatei …` | Prüfung 37 |
| `# Pruefungen N bis M …` | `# Pruefungen 19 bis 24 (Release 0.26.0)` | 19 bis 24 |
| *kein Kopf, sieht aber so aus* | `# Pruefung 37 und dieselbe Ehrlichkeit: …` | im Block von Prüfung 39 |

**Der erste Zähler hat die vierte Form für einen Kopf gehalten** und Prüfung 37 dadurch
gefunden, obwohl sie keinen Kopf dieser Schreibweise trägt. Der Fehler ist nur aufgefallen,
weil der Verlauf über die Releases bei 0.39.0 eine höchste Prüfung 36 meldete, während die
Sonden schon bis 37 reichten – **eine Zahl, die nicht zur Erwartung passte.** Dieselbe
Bauform wie der `ModuleNotFoundError` hinter „0 Fundstellen" am 14.09.

**Daraus folgt der Zuschnitt der Prüfung:** Sie ankert nicht an einer Kommentarform, sondern
an der **höchsten Prüfungsnummer, die in den beiden Prüfskripten überhaupt genannt wird**,
und an der **Lückenlosigkeit** des Registers. Ein Querverweis auf eine kleinere Nummer stört
das nicht; eine neue Prüfung nennt ihre Nummer zwangsläufig.

**Und die Grenze gehört dazu:** Sie zählt **Nennungen, nicht Prüfungen.** Wer eine Prüfung
baut und ihre Nummer nirgends schreibt, wird nicht gefangen – dieselbe Ehrlichkeit wie bei
Gegenstand 2 von Prüfung 38, der Deklarationen zählt und nicht Richtigkeit.

## 5. Warum das kein Schönheitsfehler ist

**Erstens: D-23 hängt daran.** Eine Prüfung gilt erst als vorhanden, wenn eine Sonde sie
meldet. Woran liest man ab, welche Prüfung eine Sonde hat? An A2, A3 und A4 – **und alle drei
sagen etwas Falsches.** Wer sich auf A4 verlässt, hält die Prüfungen 32 bis 39 für unbelegt;
sie sind es nicht. Wer sich auf A2 verlässt, hält 31 bis 39 für unbelegt. **Die Register
untertreiben hier**, und eine untertreibende Zusage ist der seltenere Fall in diesem Projekt –
schädlich ist sie trotzdem, weil sie eine Arbeit anstoßen kann, die längst getan ist.

**Zweitens: A5 ist eine Arbeitsanweisung, kein Register.** `FW-KO-05` sagt, was in einer
Sitzung zu tun ist: „Die zwölf Grenzfälle einzeln gegen Wurzel-Anweisungsdatei, Langform,
Overlay-Vorlage, Skills und Checklisten prüfen." Der Test steht auf `offen`. **Wer ihn heute
fährt, prüft zwölf von zwanzig und meldet ihn bestanden.** Das ist keine Kosmetik, das ist ein
halber Abnahmetest mit ganzem Ergebnis.

**Drittens: A1 verletzt eine Entscheidung, die ein Release alt ist.** `CR-2026-062` hat den
Kopfkommentar eigens zur Ermessensfrage gemacht – **E7: „Kopfkommentar 32 bis 38"** – und das
Nachziehen ausdrücklich beschlossen. `CR-2026-063` führt `validate-framework.py` in den
betroffenen Artefakten, baut Prüfung 39 und zieht den Kopfkommentar nicht nach. **Eine
Entscheidung, die nur in einem Antrag steht, hält genau bis zum nächsten Antrag.**

## 6. Was die Behebung sein muss – und was sie nicht sein kann

**Kann sie nicht sein:** Die Einträge erzeugen. Sie tragen Prosa – was die Prüfung tut, welche
Entscheidungen sie trägt, wo ihre Grenze liegt. Das ist der Wert des Registers, und er ist
nicht ausrechenbar. **Ausrechenbar ist nur die Vollständigkeit.**

**Muss sie sein:** Eine Prüfung, die den Bestand abzählt und gegen die Register hält, an allen
drei Trägern. Das ist dieselbe Bauform, die das Projekt für die Grenzfalltabelle (Prüfung 30),
für die Durchsetzungstiefe (Prüfung 31) und für die Berechtigungskörbe (Prüfung 37) schon
gewählt hat. **Der Leitsatz steht im Arbeitswissen:** Wo die Grenze eines Begriffs eindeutig
ist, gehört die Zahl ausgerechnet, nicht gepflegt. Die Menge der Prüfungen ist eindeutig.

**Und eine Auflage folgt aus M9:** Die Prüfung liest nur die Träger, die ein Register sind.
Eine Zahl in der Vorgeschichte eines Releases bleibt unangetastet.

## 7. Was diese Gegenprüfung nicht belegt

- **Sie sagt nichts darüber, ob die Register inhaltlich richtig sind.** Ob der Text eines
  Eintrags beschreibt, was seine Prüfung tut, ist eine Lektüre und kein Abzählen. Gemessen ist
  allein die **Vollständigkeit**.
- **Die Suche über das Repositorium ist eine Suche, kein Beweis.** Sie hat neben A5 drei
  weitere Nennungen von „zwölf Grenzfällen" gefunden – in der Vorgeschichte der Roadmap, in
  `CR-2026-052` und im Wirkungsnachweis zu 0.32.0. **Alle drei sind historisch und alle drei
  sind richtig.** Damit sind vier Fundstellen geprüft und eine ist zu berichtigen; ob eine
  fünfte in einer Formulierung steckt, die das Suchmuster nicht trifft, ist offen.
- **Sie misst keine Sitzung.** Ob ein Mensch oder ein Client sich beim Arbeiten wirklich auf
  eines der Register stützt, ist nicht erhoben. Der Schaden von A5 ist aus dem Text des
  Testblatts abgeleitet, nicht beobachtet.

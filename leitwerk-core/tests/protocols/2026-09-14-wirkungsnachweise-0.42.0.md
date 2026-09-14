# Wirkungsnachweise Release 0.42.0 – das Register des Prüfapparats wird nachgezählt

| Feld | Wert |
|---|---|
| Gegenstand | `CR-2026-064`, D-85 und D-86: Prüfung 40 mit vier Gegenständen, die fünf nachgezogenen Aussagen über den Prüfapparat, der ersetzte Kopfsatz von `probe-pruefungen.py` |
| Datum | 2026-09-14 |
| Vorstand | `b71d038` (0.41.0) |
| Grundlage der Zusagen | `tests/protocols/2026-09-14-gegenpruefung-pruefregister.md` (elf Messungen, sämtlich abzählend) und `-migrationslauf-pilot.md` (der Lauf, aus dem der Befund stammt) |
| Ergebnis | **Validator 0 Fehler, 0 Warnungen. 170 Sonden, Gegenproben und Selbstproben bestanden** (118 Sonden, 45 Gegenproben, 7 Selbstproben) – **in beiden Kodierungsumgebungen, zeilengleich**, null Fehlschläge, Exit 0. **Der Gegenbeweis gegen den Vorstand meldet fünf Fundstellen, eine je Abweichung und keine weitere** |

## 1. Was neu geprüft wird

| Prüfung | Gegenstand | Sonden | Gegenproben |
|---|---|---|---|
| **40, Gegenstand 1** | Der verlorene Anker: ohne Registerüberschrift meldet die Prüfung ihr eigenes Fehlen | 40f | – |
| **40, Gegenstand 2** | Das Register ist lückenlos und endet bei der höchsten genannten Nummer – in **beide** Richtungen | 40a, 40b, 40c | 40a, **40b** |
| **40, Gegenstand 3** | Die Sondenmenge an drei Stellen in einer einzigen, ausgerechneten Schreibweise | 40d | 40a |
| **40, Gegenstand 4** | Die Grenzfallanzahl in `FW-KO-05` ist die gezählte | 40e | 40a |

**Die zweite Gegenprobe ist die wichtigere Hälfte.** Sie schiebt zwei Kommentarzeilen vor
`def main()`, die auf Prüfung 37 und Prüfung 30 verweisen – **ein Querverweis im Fließtext,
kein Kopf.** Genau diese Zeilenform hat den ersten Entwurf der Prüfung fallen lassen: Er
ankerte an den Kopfkommentaren, und `# Pruefung 37 und dieselbe Ehrlichkeit …` im Block von
Prüfung 39 sah für ihn aus wie ein Kopf. Ohne diese Gegenprobe stünde die Entscheidung von
`CR-2026-064` E2 unbelegt da.

## 2. Der Gegenbeweis gegen den Vorstand – ein Abzählen, keine Konstruktion

Der neue Validator gegen eine vollständige Installation von `b71d038`, installiert mit dem
`install.py` **des Vorstands**:

| Lauf | Fundstellen | Was er misst |
|---|---|---|
| **0.41.0-Validator gegen 0.41.0** | **0 Fehler, 0 Warnungen** | Die Kontrollprobe: Der ausgelieferte Lauf sah nichts |
| **0.42.0-Validator gegen 0.41.0** | **5** | Eine je Abweichung A1 bis A5, und **keine weitere** |
| **Kontrollprobe Arbeitsbaum 0.42.0** | **0 Fehler, 0 Warnungen** | – |

| # | Fundstelle | Meldung |
|---|---|---|
| **A1** | Register im Kopfkommentar | „endet bei Prüfung 38; die Prüfskripte nennen Prüfung 39" |
| **A2** | Satz zum Wirkungsnachweis | erwartet `… fuer die Pruefungen 6 und 18 bis 39 laeuft` |
| **A3** | Kopfsatz von `probe-pruefungen.py` | erwartet `Wirkungsnachweis nach D-23 fuer die Pruefungen 6 und 18 bis 39` |
| **A4** | `FW-KO-01`, Prüfmittel | erwartet `für die Prüfungen 6 und 18 bis 39 als Skript` |
| **A5** | `FW-KO-05`, Prüfmittel | erwartet `Die 20 Grenzfälle einzeln` |

**Das ist der erste Gegenbeweis seit 0.34.0, der ein Abzählen ist.** Bei den Prüfungen 35,
36, 38 und 39 war er eine Konstruktion: Ihr Gegenstand entstand mit demselben Release und
passte per Konstruktion zu sich selbst. Hier stand der Befund vor der Prüfung, und die
Prüfung findet ihn – in der Zahl, die `CR-2026-064` vorher genannt hat.

**Und das Alter gehört dazu**, weil es den Unterschied zwischen einem Schreibfehler und
einem ungezählten Register ausmacht:

| # | falsch seit | Releases |
|---|---|---|
| A1 | 0.41.0 | 1 |
| A2 | 0.33.0 | 9 |
| A3 | 0.30.0 | **12** |
| A4 | 0.34.0 | 8 |
| A5 | 0.33.0 | 9 |

## 3. Was der Sondenlauf gefangen hat

**Die Gegenprobe 30 ist gefallen – und sie war im Recht, nicht die Prüfung.**

```text
GEGENPROBE 30   FEHL  Zusaetzlicher Grenzfall mit mitgezaehlter Anzahl
        Ausgabe: FEHLER   …/TEST_CATALOG.md: FW-KO-05 nennt nicht die gezählte Anzahl
        der Grenzfälle. Erwartet wörtlich: 'Die 21 Grenzfälle einzeln'.
```

Die Gegenprobe legt einen einundzwanzigsten Grenzfall an und zieht die Anzahl im Steckbrief
von `EDGE_CASES.md` mit – seit 0.32.0, und bis heute war das vollständig. **Mit Prüfung 40
ist es das nicht mehr:** Ein Repositorium mit 21 Grenzfällen, dessen Testblatt weiter von
zwanzig spricht, ist kein erlaubter Fall. Er ist genau der Befund, gegen den diese Prüfung
gebaut ist.

**Nachgezogen ist die Gegenprobe, nicht die Prüfung.** Sie schreibt seither **zwei** Register
fort. Das ist der erwartete Preis und die richtige Richtung: Eine Gegenprobe, die einen
erlaubten Fall herstellt, muss ihn vollständig herstellen.

> **Die alte Frage steht jetzt zum vierten Mal da.** Der Kopfkommentar der Gegenprobe hält
> seit 0.38.0 fest, ob eine Gegenprobe ihre Summen **ableiten** soll, sei eine Ermessensfrage
> und nicht entschieden. Sie ist damit zum vierten Mal aufgetreten – **und sie gehört in
> einen eigenen Antrag, nicht in einen Nebensatz beim Aufräumen.** Für dieses Release bleibt
> die Zahl wörtlich, an beiden Stellen.

**Was der Sondenlauf damit belegt, ist mehr als die Wirkung der neuen Prüfung:** Er hat eine
**bestehende** Gegenprobe unvollständig gemacht und das gemeldet, bevor jemand es behaupten
musste. Der Validatorlauf gegen das Repositorium stand dabei die ganze Zeit auf 0/0 – **zum
dritten Mal der Beleg, dass ein grüner Repo-Lauf den Sondenlauf nicht ersetzt.**

## 4. Was beim Bauen sonst aufgefallen ist

### 4.1 Der erste Entwurf der Prüfung ist gefallen

Der naheliegende Anker für „welche Prüfungen gibt es" sind die Kopfkommentare. **Gemessen
tragen sie drei Formen**, und eine vierte sieht aus wie ein Kopf und ist keiner:

| Form | Beispiel |
|---|---|
| `# Pruefung N: …` | `# Pruefung 33: Die Abbildung von permissions.deny …` |
| `# N: …` | `# 37: Die drei Koerbe der Berechtigungsdatei …` |
| `# Pruefungen N bis M …` | `# Pruefungen 19 bis 24 (Release 0.26.0)` |
| *kein Kopf* | `# Pruefung 37 und dieselbe Ehrlichkeit: …` im Block von Prüfung 39 |

**Der erste Zähler hat die vierte Form für einen Kopf gehalten.** Aufgefallen ist es nur,
weil die Auswertung über alle Release-Commits für 0.39.0 eine höchste Prüfung 36 meldete,
während die Sonden schon bis 37 reichten – **eine Zahl, die nicht zur Erwartung passte.**
Dieselbe Bauform wie der `ModuleNotFoundError` hinter „0 Fundstellen" am 13. und 14.09.

Die Prüfung ankert seither an der **höchsten genannten Nummer** und an der
**Lückenlosigkeit**. Gegenprobe 40b hält das fest.

### 4.2 Der Gegenbeweis brauchte den richtigen Zuschnitt

Der erste Lauf des neuen Validators im eigenen Arbeitsbaum meldete **vier** statt fünf
Fundstellen – weil derselbe Patch, der Prüfung 40 einführt, auch die Registereinträge 39 und
40 nachträgt. **A1 war da bereits behoben.** Die fünfte Fundstelle wird nur sichtbar, wenn
der neue Validator gegen einen **unberührten Vorstand** läuft: `git archive b71d038`,
Installation mit dem `install.py` des Vorstands, dann `--root` auf diesen Baum. Prüfung 40
liest die Register **aus dem Baum unter `--root`**, nicht aus ihrer eigenen Datei – deshalb
funktioniert dieser Zuschnitt überhaupt.

### 4.3 Eine Zahl in der eigenen Prosa lag daneben, bevor sie committet wurde

`CR-2026-064` nannte im ersten Entwurf „vier Fundstellen im Vorstand". Es sind **fünf** –
eine je Abweichung. Gefunden vor dem Commit, beim Nachzählen der eigenen Aufstellung.
**Dieser Durchgang lohnt sich, und er gehört vor den teuren Lauf.**

## 5. Sondenlauf

| Umgebung | Sonden | Gegenproben | Selbstproben | Fehlschläge | Exit |
|---|---|---|---|---|---|
| ohne `PYTHONIOENCODING` | 118 | 45 | 7 | **0** | 0 |
| mit `PYTHONIOENCODING=utf-8` | 118 | 45 | 7 | **0** | 0 |

**Zeilengleich** (`diff` über beide Läufe: leer). Die neuen Einträge:

```text
SONDE      40a  OK    Eine Pruefung laeuft, das Register kennt sie nicht - der Fall vom 2026-09-14
SONDE      40b  OK    Eine Nummer faellt aus dem Register - die Pruefung dahinter findet niemand
SONDE      40c  OK    Ein Registereintrag ohne Pruefung dahinter - die Gegenrichtung
SONDE      40d  OK    Die Sondenmenge im Satz unter dem Register weicht ab
SONDE      40e  OK    FW-KO-05 nennt eine Grenzfallzahl, die nicht mehr stimmt
SONDE      40f  OK    Verlorener Anker - die Registerueberschrift verschwindet
GEGENPROBE 40a  OK    Das unveraenderte Repositorium bleibt unbeanstandet - Register, Sondenmenge und Grenzfallzahl decken sich
GEGENPROBE 40b  OK    Ein Querverweis auf eine kleinere Pruefungsnummer bleibt unbeanstandet - er ist kein Kopf und kein Eintrag
```

Der **erste** Lauf dieses Releases meldete eine Abweichung (Gegenprobe 30, Abschnitt 3); die
Tabelle oben ist der Lauf **nach** dem Nachziehen.

## 6. Was dieses Release nicht belegt

- **Nicht, dass die Registereinträge richtig sind.** Prüfung 40 belegt die
  **Vollständigkeit**; ob ein Eintrag beschreibt, was seine Prüfung tut, ist eine Lektüre und
  kein Abzählen.
- **Nicht, dass jede Prüfung gefunden wird.** Sie zählt **Nennungen**: Wer eine Prüfung baut
  und ihre Nummer nirgends schreibt, wird nicht gefangen – dieselbe Ehrlichkeit wie
  Gegenstand 2 von Prüfung 38.
- **Nicht, dass sonst keine Zahl über den Prüfapparat falsch steht.** Die Suche über das
  Repositorium hat drei weitere Nennungen von „zwölf Grenzfällen" gefunden – in der
  Vorgeschichte der Roadmap, in `CR-2026-052` und im Wirkungsnachweis zu 0.32.0 –, und **alle
  drei sind richtig**. Ob eine vierte in einer Formulierung steckt, die das Suchmuster nicht
  trifft, ist offen. **Eine Suche ist kein Beweis.**
- **Nicht, dass `FW-KO-05` jetzt bestanden wäre.** Berichtigt ist seine Zahl, nicht sein
  Ergebnis. Der Test steht weiter auf `offen`.
- **Nicht, dass die Schreibweise der Sondenmenge gut gewählt ist.** Sie ist *eine*
  Schreibweise, wörtlich verglichen; das bindet drei Sätze und ist der bewusst getragene
  Preis von D-86.

## 7. Gegenzeichnung

| Feld | Inhalt |
|---|---|
| Durchführung | KI-Client unter Aufsicht, Sitzung vom 2026-09-14 |
| Gegengezeichnet durch | `<APPROVAL_ROLE>` |
| Datum | `<TBD: Datum der Gegenzeichnung>` |
| Anmerkungen | `<TBD: Anmerkungen der gegenzeichnenden Rolle>` |

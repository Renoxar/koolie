# Wirkungsnachweise zu Release 0.33.0

| Feld | Wert |
|---|---|
| Gegenstand | Die Umsetzungen zu `CR-2026-054` (D-57, D-58, Befund **B08**) und `CR-2026-055` (D-59, D-60, Befund **B11**) |
| Datum | 2026-09-13 |
| Framework-Version | 0.33.0 (gegen 0.32.0 = `a950c35`) |
| Prüfmethode | `probe-pruefungen.py` gegen beide Stände und in **beiden** Kodierungsumgebungen; dazu ein Validatorlauf des neuen Prüfsatzes gegen den unveränderten Vorstand und zwei erzeugte Installationen je Pack |
| Umgebung | Windows 11, Python 3.14.4 |
| Ergebnis | **97 Sonden und Gegenproben bestehen gegen 0.33.0 in beiden Umgebungen.** Der neue Prüfsatz meldet gegen 0.32.0 **sechs** Fundstellen – fünf davon Prüfung 31 in den unveränderten Client Packs |

## 1. Was hier nachgewiesen wird

| Gegenstand | Art | Nachweis |
|---|---|---|
| Kandidatenprüfung `--check-overlay-ready` | neuer Prüfpfad | drei Sonden, eine Gegenprobe – **je Pack** |
| Status-Hook nach dem Umbau | geändertes Skript | drei Sonden, eine Gegenprobe – **je Pack** |
| Fetch-Allow-Verbot aus dem Manifest | geänderte Prüfung | eine Sonde, eine Gegenprobe – **je Pack** |
| Prüfung 31 (Summen der Fachmatrix) | neue Prüfung | vier Sonden, eine Gegenprobe |
| Rückzug der Domain-Zusage | Textkorrektur an fünf Stellen | **keine Sonde** – siehe Abschnitt 5 |
| Zählregel und berichtigte Summen | Textkorrektur | über Prüfung 31 mitgeprüft |

**Je Pack, nicht einmal.** B02 war nicht, dass eine Prüfung falsch prüft, sondern dass sie einen
Client **gar nicht sieht**. Das fällt nur auf, wenn derselbe Fall in jeder Installation läuft – die
Kandidatenprüfung, der Hook und das Fetch-Allow-Verbot laufen deshalb gegen zwei frische
Installationen.

## 2. Die Sonden

### 2.1 Kandidatenprüfung (je Pack)

| Sonde | Präparation | Erwartete Meldung |
|---|---|---|
| CR-1 | Status an allen Stellen `aktiv` | „ist bereits 'aktiv'“ – mit Verweis auf `--strict-overlay` |
| CR-2 | Laufzeitregel `aktiv`, Quell-Overlay `inaktiv` | „widersprechen sich“ |
| CR-3 | Status als offener Platzhalter | „nicht ausgefuellt“ |

**Gegenprobe CR:** Ein vollständig ausgefüllter Kandidat mit Status `inaktiv` an allen Stellen und
platzhalterfreier Berechtigungsdatei **läuft durch**. Das ist hier die wichtigere Hälfte: Ohne sie
stünde nur fest, dass irgendetwas gemeldet wird – und eine Prüfung, die alles meldet, besteht jede
Sonde.

### 2.2 Status-Hook (je Pack)

| Sonde | Präparation | Erwartete Meldung |
|---|---|---|
| HS-1 | Laufzeitregel `aktivierung-ausstehend`, Overlay `aktiv` | `widerspruechlich` – **nicht** `aktiv` |
| HS-2 | Laufzeitregel `inaktiv`, Overlay `aktiv` | `widerspruechlich` – nicht die erste gelesene Datei |
| HS-3 | Nur die Steckbriefzeile, Laufzeitregel entfernt | `inaktiv` – die Tabellenform wird gelesen |

**Gegenprobe HS:** Alle Angaben `aktiv` → Meldung `aktiv` **ohne** M1-Hinweis. Sie schließt aus,
dass der Hook nach dem Umbau pauschal warnt.

Jede der drei Sonden trifft genau einen der drei Defekte aus der Gegenprüfung. Vor 0.33.0 hätte
HS-1 die Meldung `aktiv` erzeugt (Präfixvergleich), HS-2 ebenfalls (`break`), und HS-3 hätte
`unbekannt` gemeldet (fehlende Tabellenform).

### 2.3 Fetch-Allow aus dem Manifest (je Pack)

| Sonde | Präparation | Erwartete Meldung |
|---|---|---|
| FA | `allow`-Regel `<Abrufwerkzeug des Packs>(domain:docs.example.invalid)` | „allow-Regel auf ein Abrufwerkzeug“ |

Das Werkzeug kommt aus `permission_tools.fetch` des jeweiligen Manifests – bei `claude-code`
`WebFetch`, bei `devin-desktop` `Fetch`. **Die zweite ist der eigentliche Nachweis:** Sie lief bis
0.32.0 durch, weil die Namensliste nur `Fetch(*` kannte.

**Gegenprobe FA:** Die ausgelieferte Regelmenge bleibt unbeanstandet – die Prüfung greift nur an
`allow`, nicht an `deny`.

### 2.4 Prüfung 31

| Sonde | Präparation | Erwartete Meldung |
|---|---|---|
| 31a | Anzahl je Einstufung in der Zusammenfassung verfälscht | „Zeile(n) als [TECHNISCH]; gezaehlt sind“ |
| 31b | Gesamtzahl der Matrixzeilen verfälscht | „Matrixzeilen; gezaehlt sind“ |
| 31c | Überschrift der Zusammenfassung umbenannt | „kein Abschnitt '## 3. Zusammenfassung“ |
| 31d | Matrixzeile ohne Einstufung eingefügt | „ohne Einstufung: Z9“ |

**Gegenprobe 31:** Eine **zusätzliche** Matrixzeile samt nachgezogenen Summen bleibt unbeanstandet.
Ohne sie wäre die Prüfung eine Bremse für jede neue Zeile statt einer Prüfung.

31c ist die Sonde auf den **verlorenen Anker** – dieselbe Bauform wie 28c und 29c aus 0.32.0: Eine
Konsistenzprüfung, die ihren Prüfgegenstand nicht mehr findet, besteht sonst leise.

## 3. Der Gegenbeweis gegen den Vorstand

Vorgehen wie bei 0.32.0: `git archive a950c35` in ein leeres Verzeichnis, dort mit **dem eigenen**
`install.py` des Vorstands installiert, dann nur `validate-framework.py` und
`overlay_status.py` aus 0.33.0 hineinkopiert.

```
FEHLER  …/tests/EDGE_CASES.md: Keine Grenzfallzeile verweist auf D-59
FEHLER  …/clients/claude-code/CLIENT_PACK.md: nennt 25 Zeile(n) als [TECHNISCH]; gezaehlt sind 20
FEHLER  …/clients/claude-code/CLIENT_PACK.md: nennt 3 Zeile(n) als [TEXTUELL]; gezaehlt sind 7
FEHLER  …/clients/claude-code/CLIENT_PACK.md: nennt 1 Zeile(n) als [NICHT ABBILDBAR]; gezaehlt sind 2
FEHLER  …/clients/devin-desktop/CLIENT_PACK.md: nennt 24 Zeile(n) als [TECHNISCH]; gezaehlt sind 19
FEHLER  …/clients/devin-desktop/CLIENT_PACK.md: nennt 9 Zeile(n) als [TEXTUELL]; gezaehlt sind 14
Ergebnis: 6 Fehler, 0 Warnungen
```

**Die erste Meldung stammt von Prüfung 30, nicht von 31**, und sie gehört dazu: Die
Grenzfalltabelle des Vorstands kennt D-59 nicht, weil es die Entscheidung dort nicht gibt. Prüfung
30 hält damit auch die **neue** Entscheidung an ihre Grenzfalltabelle gebunden – sie war dafür
gebaut (0.32.0) und bewährt sich beim ersten Anwendungsfall.

Gegen 0.33.0 im selben Prüfsatz: **0 Fehler, 0 Warnungen.**

**Prüfung 31 findet den Nebenbefund im unveränderten Vorstand von selbst** – einschließlich der
Angabe „1 von 29“ für `[NICHT ABBILDBAR]`, wo seit 0.31.0 zwei Zeilen dort stehen. Der Drift war
zwei Releases alt und hat den Wirkungsnachweis beider Releases überlebt.

**Für die Kandidatenprüfung, den Hook und das Fetch-Allow-Verbot gibt es keinen solchen
Gegenbeweis**, und das hat einen Grund: Alle drei sind **Verhaltensänderungen**, nicht Prüfungen auf
den Bestand. Ihr Gegenbeweis steckt in den Sonden selbst – jede beschreibt einen Fall, der vor
0.33.0 anders ausgegangen wäre, und Abschnitt 2.2 nennt je Sonde, wie.

## 4. Eine Sonde hat die eigene Umsetzung gefangen

Beim Umbau von `check_strict_overlay` auf die gemeinsame Auswertung meldete die Funktion nur noch
den **ausgewerteten** Status:

```
Overlay-Status ist nicht 'aktiv', sondern 'unbekannt' (…)
```

Der Rohwert fiel weg. Die Sonde zu D-44 – sie sucht wörtlich nach `sondern
'aktivierung-ausstehend'`, dem Wert, der den Befund 2026-09-12 ausgelöst hat – **fiel bei beiden
Packs sofort**. Die Meldung nennt jetzt zuerst die Rohwerte, dann die Auswertung.

**Das ist der Zweck dieser Sonden, an einem Fall, der nicht geplant war.** Ohne sie wäre die
Meldung stiller geworden, und der Sondenlauf wäre grün geblieben – der Wert, den zu nennen der
ganze Punkt von D-44 war, hätte in keiner Ausgabe mehr gestanden.

## 5. Was dieses Release nicht nachweist

- **Der Rückzug der Domain-Zusage hat keine Sonde**, und zwar bewusst: Es ist eine Textkorrektur an
  fünf Stellen, und eine Prüfung, die eine Formulierung bewacht, meldet jede Umformulierung und
  sonst nichts. Belegt ist der Befund – in der Gegenprüfung, an zwei erzeugten Installationen.
- **Kein Lauf gegen einen Client.** Dass ein Client eine Domain-Angabe auswertet oder nicht, ist
  für `devin-desktop` **unerhoben**; Zeile B10 trägt dort `[TEXTUELL]` mit VERIFY-Marker. Widerlegt
  ist nur, dass sie gegen ein bestehendes `deny` wirken könnte – Mechanik, nicht Messung.
- **Kein vollständiger Übernahmelauf.** Dass der berichtigte Ablauf – Kandidatenprüfung,
  Aktivierung durch den Menschen, Nachprüfung – in einem fremden Projekt ohne Regelbruch durchläuft,
  ist an Installationen geprüft, nicht an einer echten Übernahme. Der Pilot steht auf 0.29.0 und
  hat seinen Ablauf hinter sich.
- **Der Hook bleibt eine Meldung.** Ob ein KI-Client den M1-Hinweis befolgt, ist nicht gemessen und
  durch diesen Mechanismus auch nicht messbar; der Hook blockiert nie.
- **Prüfung 31 prüft die Arithmetik, nicht die Einstufung.** Eine Matrix, in der jede Zeile falsch
  eingestuft ist, besteht sie. Die Einstufung selbst belegt nur eine Erhebung an einer Installation.
- **Die Zählregel ist eine Entscheidung, kein Messwert** (D-60). Sie steht an drei Stellen gleich:
  in beiden Packs und in Prüfung 31.

## 6. Der Lauf in beiden Kodierungsumgebungen

| Umgebung | Sonden und Gegenproben | Ergebnis |
|---|---|---|
| ohne `PYTHONIOENCODING` | 97 | alle bestanden |
| mit `PYTHONIOENCODING=utf-8` | 97 | alle bestanden |

97 = 72 aus 0.32.0 plus 25 neue, und zwar **18 Sonden und 7 Gegenproben**: Kandidatenprüfung,
Status-Hook und Fetch-Allow je Pack (je 3+1, 3+1 und 1+1 – zusammen zwanzig), dazu 4+1 für
Prüfung 31. Ausgezählt aus dem Lauf: 65 Sonden, 32 Gegenproben. Der Validator meldet in beiden Umgebungen 0 Fehler und 0 Warnungen.

## 7. Gegenzeichnung

| Rolle | Name/Kennung | Datum | Ergebnis bestätigt |
|---|---|---|---|
| `<FRAMEWORK_OWNER>` | `<TBD>` | `<TBD>` | `<TBD>` |

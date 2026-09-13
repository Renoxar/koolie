# Wirkungsnachweise zu Release 0.32.0

| Feld | Wert |
|---|---|
| Gegenstand | Die Umsetzungen zu `CR-2026-052` (D-52 bis D-54, Befund **B09**) und `CR-2026-053` (D-55, D-56, Befund **B07**) |
| Datum | 2026-09-13 |
| Framework-Version | 0.32.0 (gegen 0.31.0 = `97052c1`) |
| Prüfmethode | `probe-pruefungen.py` gegen beide Stände und in **beiden** Kodierungsumgebungen; dazu ein Validatorlauf des neuen Prüfsatzes gegen den unveränderten Vorstand |
| Umgebung | Windows 11, Python 3.14.4 |
| Ergebnis | **72 Sonden und Gegenproben bestehen gegen 0.32.0 in beiden Umgebungen.** Die drei neuen Prüfungen melden gegen 0.31.0 **acht** Fundstellen – und das sind genau die Befunde dieses Releases |

## 1. Was hier nachgewiesen wird – und was nicht

Beide Anträge sind in ihrem Kern **Textentscheidungen**. Ein Skript kann nicht prüfen, ob eine
Einstufung richtig ist; es kann prüfen, ob alle Fassungen dieselbe Einstufung tragen und ob eine
Entscheidung überhaupt getroffen wurde. Genau dort setzen die drei neuen Prüfungen an.

| Gegenstand | Art | Nachweis |
|---|---|---|
| Prüfung 28 – Strukturpfad in der `<EXCLUDED_PATHS>`-Deklaration | neue Prüfung | drei Sonden, eine Gegenprobe |
| Prüfung 29 – K3-Kategorien in fünf Fassungen, ohne Bedingung | neue Prüfung | drei Sonden, eine Gegenprobe |
| Prüfung 30 – Vollständigkeit der Grenzfalltabelle | neue Prüfung | drei Sonden, eine Gegenprobe |
| Abgrenzung zu V6 (D-53) | Textentscheidung | **keine Sonde** – siehe Abschnitt 6 |
| R12 nach Schreibziel und Aufsicht (D-54) | Textentscheidung | **keine Sonde** – siehe Abschnitt 6 |
| Entwicklungsprofil (D-56) | Dokument, kein Mechanismus | **keine Sonde** – siehe Abschnitt 6 |

**Für drei der fünf Entscheidungen gibt es bewusst keine Sonde.** Eine Prüfung, die eine
Formulierung bewacht, meldet jede Umformulierung und sonst nichts. Was sie tragen, ist die
Grenzfalltabelle – und die ist maschinell auf Vollständigkeit geprüft, nicht auf Richtigkeit.

## 2. Die neun neuen Sonden

Jede Sonde präpariert eine Kopie des Repositoriums und erwartet eine bestimmte Meldung. Bleibt der
Baum unverändert, meldet das Skript `[nichts praepariert]` – der Suchtext der Sonde passt dann
nicht mehr, und gemessen würde die Sonde statt der Prüfung.

| Sonde | Präparation | Erwartete Meldung | 0.32.0 | 0.31.0 |
|---|---|---|---|---|
| 28a | Strukturpfad in die `<EXCLUDED_PATHS>`-Zeile der Overlay-Vorlage | „Die Deklaration von `<EXCLUDED_PATHS>` nennt“ | gemeldet | Befund steht dort **von sich aus** |
| 28b | dasselbe in der Laufzeitregel `20-*` | ebenda | gemeldet | ebenso |
| 28c | Beschriftung der Deklaration umbenannt | „keine Zeile ist als Deklaration erkennbar“ | gemeldet | – |
| 29a | Kategorie „Sicherheitskonfigurationen“ aus der Kurzform entfernt | „nennt die Kategorie … nicht“ | gemeldet | Befund steht dort **von sich aus** |
| 29b | Bedingung an die Kategorie „interne Adressen“ angehängt | „traegt eine Bedingung“ | gemeldet | Befund steht dort **von sich aus** |
| 29c | Anker „- Immer K3“ umbenannt | „ist nicht mehr auffindbar“ | gemeldet | – |
| 30a | Grenzfallzeile G-07 gelöscht | „Grenzfallzeilen, der Steckbrief nennt“ | gemeldet | Datei fehlt dort ganz |
| 30b | Spalte „Kontrollstufe“ in G-05 geleert | „ist leer“ | gemeldet | – |
| 30c | Verweis auf D-53 aus allen Zeilen entfernt | „Keine Grenzfallzeile verweist auf D-53“ | gemeldet | – |

**Zwei Sonden prüfen nicht die Sache, sondern die Prüfung selbst.** 28c und 29c verlieren den
Anker, an dem die jeweilige Prüfung ihren Prüfgegenstand findet. Ohne diese Sonden hätte das
Projekt zwei Konsistenzprüfungen, die beim ersten Umformulieren **leise bestehen** – der
Befundtyp, den ERH-12 und die Lehre aus 0.27.0 beschreiben. Die Prüfungen melden das Fehlen
deshalb selbst als Fehler.

## 3. Die drei Gegenproben – und warum sie hier mehr wert sind als üblich

| Gegenprobe | Präparation | Was sie ausschließt |
|---|---|---|
| 28 | Dieselben Strukturpfade **im Fließtext**, in einem Satz, der sie ausdrücklich ausschließt | Dass Prüfung 28 jede Nennung meldet statt der Deklaration. **Beide Träger enthalten genau so einen Satz** – eine Prüfung ohne diese Unterscheidung hätte den richtigen Text beanstandet |
| 29 | Kurzform kürzer formuliert („Sicherheitskonfigurationen“ statt „… mit Schutzwirkung“), keine Kategorie weniger | Dass Prüfung 29 auf Wortgleichheit prüft statt auf Kategorien. Eine Kurzform **darf** kürzer sein |
| 30 | Ein dreizehnter Grenzfall samt mitgezählter Anzahl im Steckbrief | Dass Prüfung 30 eine feste Zahl erwartet statt der mitgeführten |

**Zur Ehrlichkeit der Gegenproben:** Die Gegenprobe zu 28 bestünde gegen 0.31.0 **aus dem falschen
Grund** – dort gibt es die Prüfung nicht. Dasselbe gilt für 29 und 30. Der Wert dieser
Gegenproben liegt allein gegen 0.32.0, und dort tragen sie: Sie belegen, dass die neuen Prüfungen
unterscheiden und nicht pauschal melden. Dieselbe Einschränkung stand am 2026-09-12 viermal in den
Protokollen und gehört auch hier hin.

## 4. Der Gegenbeweis gegen den Vorstand

Vorgehen: `git archive 97052c1` in ein leeres Verzeichnis, dort mit **dem eigenen** `install.py`
des Vorstands installiert, dann **nur** `validate-framework.py` aus 0.32.0 hineinkopiert. Damit
misst der neue Prüfsatz den alten Inhalt.

```
FEHLER  leitwerk-core/templates/project-overlay/OVERLAY.md:71       Prüfung 28
FEHLER  leitwerk-core/framework/runtime/rules/20-project-overlay.md:23  Prüfung 28
FEHLER  project-overlay/OVERLAY.md:71                                Prüfung 28 (Installation)
FEHLER  .devin/rules/20-project-overlay.md:23                        Prüfung 28 (Installation)
FEHLER  leitwerk-core/framework/core/02-privacy.md                   Prüfung 29 – Bedingung
FEHLER  leitwerk-core/framework/runtime/root-instruction.md           Prüfung 29 – Sicherheitskonfigurationen fehlt
FEHLER  leitwerk-core/framework/runtime/root-instruction.md           Prüfung 29 – Inhalte anderer Projekte fehlt
FEHLER  leitwerk-core/tests/EDGE_CASES.md                             Prüfung 30 – fehlt
Ergebnis: 8 Fehler, 0 Warnungen
```

Gegen 0.32.0 im selben Prüfsatz: **0 Fehler, 0 Warnungen.**

**Das ist der stärkste Teil dieses Nachweises.** Die drei Prüfungen sind nicht auf einen
präparierten Defekt zugeschnitten – sie finden die vier Befunde dieses Releases **im
unveränderten Vorstand von selbst**: die fehlerhafte Ausschlussliste in Quelle und Installation,
die Bedingung an einer unbedingten Kategorie und die zwei Kategorien, die der Kurzform fehlten.
Zwei davon hat das externe Review nicht genannt; Prüfung 29 hätte sie gefunden, bevor jemand
hinsah.

## 5. Der Lauf in beiden Kodierungsumgebungen

Auflage aus D-49: Der Sondenlauf gilt nur, wenn er in beiden Umgebungen läuft.

| Umgebung | Sonden und Gegenproben | Ergebnis |
|---|---|---|
| ohne `PYTHONIOENCODING` | 72 | alle bestanden |
| mit `PYTHONIOENCODING=utf-8` | 72 | alle bestanden |

72 = 60 aus 0.31.0 plus zwölf neue (neun Sonden, drei Gegenproben). Der Validator meldet in beiden
Umgebungen 0 Fehler und 0 Warnungen.

## 6. Was dieses Release nicht nachweist

- **Die Abgrenzung zu V6 (D-53) ist nicht maschinell geprüft.** Ob eine konkrete Änderung
  Anwendungslogik oder Betrieb betrifft, entscheidet ein Mensch am Kriterium aus
  `framework/core/09-risk-model.md`. Was geprüft ist: dass die Grenzfälle G-04 bis G-06 die
  Entscheidung tragen und auf eine Fundstelle verweisen.
- **R12 (D-54) ist nicht maschinell geprüft.** Die leere Schnittmenge ist im Text aufgelöst; dass
  sie leer **war**, ist im Gegenprüfungsprotokoll belegt, nicht durch einen Lauf.
- **Das Entwicklungsprofil (D-56) hat keinen Mechanismus und deshalb keine Sonde.** Es beschreibt
  einen Kontext und hebt ausdrücklich keinen Schutz auf. Was es über den Shell-Kanal sagt, ist am
  2026-09-12 gemessen (B04) und hier nicht erneut belegt.
- **Prüfung 29 prüft Kategorien, nicht Semantik.** Sie erkennt eine fehlende Kategorie und eine
  Bedingung aus einer festen Liste von Bedingungswörtern. Eine Bedingung, die anders formuliert
  ist – „gilt nicht, wenn“ –, entgeht ihr. Die Liste ist erweiterbar und steht an einer Stelle.
- **Kein Lauf gegen ein Projekt mit ausgefüllter `<EXCLUDED_PATHS>`-Liste.** Dass die fehlerhafte
  Lesesperre tatsächlich in einer Berechtigungsdatei entsteht, ist **nicht** gemessen; belegt ist
  der Weg dorthin. Kein ausgeliefertes Overlay füllt die Liste aus, weil die Vorlage `<TBD>`
  liefert. Das gehört in einen AP2-Lauf mit einem ausgefüllten Overlay.
- **`FW-KO-05` steht auf `offen`.** Ob ein KI-Client die zwölf Grenzfälle so einstuft, wie die
  Tabelle es vorgibt, ist eine Sitzung und nicht gefahren.

## 7. Gegenzeichnung

| Rolle | Name/Kennung | Datum | Ergebnis bestätigt |
|---|---|---|---|
| `<FRAMEWORK_OWNER>` | `<TBD>` | `<TBD>` | `<TBD>` |

# Wirkungsnachweise 0.54.0

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-17 |
| Framework-Version | `0.54.0` (Vorstand `0.53.1`, Commit `c52e6b4`) |
| Antrag | `CR-2026-076`, D-115 bis D-119, `K-42` bis `K-45` neu |
| Gegenstand | **Ein Regressionsnachweis, kein Wirkungsnachweis einer neuen Prüfung.** Dieses Release baut und ändert **keine** Prüfung (E6 des Antrags); es ändert drei Verfahren des Testkatalogs, füllt sieben Ergebniszellen und zieht die Standzeile nach |
| Prüfmethode | Validatorlauf gegen den fertigen Baum; Sondenlauf `probe-pruefungen.py .` in **beiden** Kodierungsumgebungen (D-49); Gegenbeweis für Prüfung 46 an der Standzeile |
| Ergebnis | **Validator 0 Fehler, 0 Warnungen; 254 Ergebniszeilen bestanden in beiden Kodierungsumgebungen** – zeichengleich mit 0.53.1. Prüfung 46 hat zum siebten Mal gegriffen |

---

## 1. Was dieses Release NICHT tut, und warum das hier steht

**Es baut keine Sonde und ändert keine Prüfung.** Die Sondenmenge bleibt bei 254
Ergebniszeilen (159 Sonden, 65 Gegenproben, 12 Selbstproben, 18 Bündelkopfzeilen), die
Spanne, die Prüfung 40 nachrechnet, bleibt unverändert, und das Register im Kopfkommentar
des Validators endet weiterhin bei Prüfung 47.

**Das ist eine Entscheidung mit benanntem Preis** (E6): Drei gemessene und gegengeprüfte
Befunde bleiben unbehoben – `K-43`, `K-44` und `K-45`. Der schwerste ist `K-44`: Ein
Projekt kann seine Role und Tech Packs still verlieren.

> **Der Grund für die Vertagung ist nicht Bequemlichkeit, sondern Zuschnitt.** Jede neue
> Prüfung braucht nach D-23 eine Sonde **und** eine Gegenprobe; jede Änderung an der
> Sondenmenge verschiebt die Spanne, die Prüfung 40 hält. Dieses Release trägt bereits den
> größten Messvorgang des Projekts. **Ein Abnahmelauf, der nichts als Regression prüft,
> sagt über einen reinen Text- und Ergebnisvorgang genau das, was er sagen soll.**

---

## 2. Der Wächter hat gegriffen – zum siebten Mal

Nach dem Füllen der sieben Ergebniszellen und **vor** dem Nachziehen der Standzeile:

```
FEHLER   leitwerk-core/docs/ROADMAP.md: Kriterium 2 von D-11 (Testkatalog und dezentrale
         Testblätter ohne `offen`) ist gezählt **111**, die Standzeile nennt 118 – der
         Fortschritt ist nicht nachgezogen.
```

**Siebte Gelegenheit, siebter Treffer, kein Rückfall darunter.** Und es ist die erste, die
Kriterium 2 betrifft – die sechs davor lagen bei den Kriterien 1, 3 und 4.

> Ohne diese Bauform stünde in der Roadmap heute `118`, und niemand hätte es gesehen. Der
> Zähler sagt nicht, ob jemand eine Zahl senkt – **er sagt, ob die geschriebene Zahl
> stimmt.**

---

## 3. Die Läufe

### 3.1 Validator

| Lauf | Zuschnitt | Ergebnis |
|---|---|---|
| V1 | `--root .` gegen den Baum nach dem Füllen der Zellen, vor der Standzeile | **1 Fehler** – Prüfung 46, siehe Abschnitt 2 |
| V2 | `--root .` nach dem Nachziehen der Standzeile | **0 Fehler, 0 Warnungen** |
| V3 | `--root .` gegen den **fertigen** Baum (mit beiden Protokollen und dem Änderungsverzeichnis) | **0 Fehler, 0 Warnungen** |

### 3.2 Sondenlauf

| Lauf | Kodierungsumgebung | Ergebniszeilen | Dauer |
|---|---|---|---|
| A | ohne `PYTHONIOENCODING` | **254, alle bestanden** | 141,1 s |
| B | mit `PYTHONIOENCODING=utf-8` | **254, alle bestanden** | 134,7 s |
| C | mit `PYTHONIOENCODING=utf-8`, gegen den Baum **mit** beiden Protokollen und dem Änderungsverzeichnis | **254, alle bestanden** | 135,5 s |
| D | ohne `PYTHONIOENCODING`, gegen die **Endfassung** | **254, alle bestanden** | 135,8 s |

**Vier Läufe, vier Mal 254 Ergebniszeilen, kein Fehlschlag – zeilengleich untereinander
und zeilengleich mit 0.53.1.** Beide Kodierungsumgebungen sind abgedeckt (D-49), und
die Läufe C und D laufen gegen den Baum **einschließlich** beider Protokolle: Ein
Protokoll mit offenen Ausfüllmarken erzeugt Warnungen, die kein früherer Lauf gesehen
hätte, und `probe-pruefungen.py` kopiert je Sonde das ganze Verzeichnis – eine Datei,
die den Validator stört, lässt **alle Gegenproben** scheitern, während die Sonden grün
bleiben.

> **Der Rückschritt ohne Ende ist nach D-94 aufgelöst, und das gehört hingeschrieben:**
> Ein Lauf gegen die Endfassung ändert die Endfassung, sobald man sein Ergebnis
> einträgt. Die Zahlen dieser Tabelle stehen deshalb **unterhalb der Trennlinie** und
> sind nicht Teil des zeilengleichen Vergleichs; ihr Eintrag ändert nichts, was eine
> Prüfung liest. Ohne diesen Satz sähe es aus wie eine nachträgliche Korrektur am
> Messergebnis.

**Die Laufzeiten stehen unterhalb dieser Trennlinie und sind nicht Teil des zeilengleichen
Vergleichs** (D-94) – ihr Eintrag ändert nichts, was eine Prüfung liest.

---

## 4. Gegenbeweis gegen den Vorstand

Ein Gegenbeweis im üblichen Sinn – *„die neue Prüfung fällt gegen den Vorstand"* – ist hier
nicht führbar, **weil keine neue Prüfung existiert.** Was stattdessen belegbar ist und
belegt wurde:

| Gegenstand | Vorstand `0.53.1` | Stand `0.54.0` |
|---|---|---|
| Prüfung 46, Kriterium 2 | gezählt 118, Standzeile 118 → grün | gezählt 111, Standzeile 111 → grün |
| dieselbe Prüfung gegen den **gemischten** Stand | – | **rot** (Abschnitt 2) |

**Der gemischte Stand ist der Gegenbeweis.** Er ist nicht konstruiert worden, sondern
zwangsläufig entstanden: Zwischen dem Füllen der Zellen und dem Nachziehen der Standzeile
liegt genau der Zustand, den Prüfung 46 fangen soll – und sie hat ihn gefangen.

---

## 5. Zahlen dieses Releases, nachgezählt

| Zahl | Behauptet | Nachgezählt | Quelle |
|---|---|---|---|
| offene Ergebniszellen vorher | 118 | **118** | Prüfung 46 und eine unabhängige Auszählung mit derselben Regel |
| davon im Katalog | 31 | **31** | dieselbe |
| davon in den Testblättern | 87 | **87** | dieselbe |
| gefüllte Zellen | 7 | **7** | `git diff` über die beiden Träger |
| offene Ergebniszellen nachher | 111 | **111** | Prüfung 46 |
| Testblätter | 13 | **13** | Baumdurchlauf über `**/TESTS.md` im Zählbereich |
| Zellen der Testblätter mit `UEB-`Kennung | 1 | **1** | Auszählung über beide Register |
| Läufe der Erhebung | 16 | **16** | Belegdateien |

> ⚠️ **Fünf Zahlen dieses Vorgangs waren zunächst falsch.** Vier davon hat der Durchgang
> vor dem Commit gefangen, und **drei von diesen vier waren an sich richtig – sie
> gehörten zur verworfenen ersten Messreihe.** Die Aufteilung 111 = 28 + 83 stand als
> 24 + 83; die Zellen mit Präparationskennung standen als neun statt sieben; der
> Werkzeugbestand von `M2r` stand mit den Zahlen von `M2`; und `M4r` nennt drei Stellen
> der ISBN-Prüfung, nicht vier. **Wer eine Messreihe wiederholt, zählt jede Zahl neu und
> übernimmt keine.**
>
> **Die fünfte stand schon im Entwurf des Protokolls:** Die erste eigene Auszählung ergab **103** statt 118 offener Zellen. Ursache:
> Der eigene Zähler verlangte eine Kennung `SK-` oder `FW-` in der ersten Spalte, Prüfung 46
> verlangt nur, dass die Zeile mit `| ` beginnt. **Die fehlenden 15 sind `RE-001-P01` bis
> `RE-001-N10`** im Testblatt des Role Packs `requirements-engineering` – dasselbe Blatt, das
> `CR-2026-070` schon einmal übersehen hat. **Gefunden, weil 103 nicht zu 118 passte** – der
> billigste Prüfstein dieses Projekts, zum wiederholten Mal.

---

## 6. D-119 am Diff belegt

D-119 sagt: Das Füllen einer Ergebniszelle hebt die Version des Trägers nicht. Belegt statt
zugesichert:

| Träger | Version vorher | Version nachher | belegt durch |
|---|---|---|---|
| `framework/skills/fw-repo-analyze/SKILL.md` | `0.1.3` | **`0.1.3`** | `git diff` – die Datei ist nicht angefasst |
| `framework/skills/fw-repo-analyze/TESTS.md` | – (führt keinen Steckbrief) | – | vier Zellen geändert, sonst nichts |
| `tests/TEST_CATALOG.md` | `0.2.3` | **`0.3.0`** | **gehoben – aber nicht wegen der Zellen**, sondern weil drei Verfahren geändert sind |

---

## 7. Gegenzeichnung

| Frage | Antwort |
|---|---|
| Ist der Sondenlauf in beiden Kodierungsumgebungen gefahren? | **Ja** – vier Läufe, A und D ohne, B und C mit `PYTHONIOENCODING=utf-8`, alle vier 254 Ergebniszeilen bestanden |
| Wurde während eines Sondenlaufs am Baum gearbeitet? | **Nein.** Die Vorarbeit lag im Scratchpad; die Protokolle und das Änderungsverzeichnis sind **nach** dem ersten Lauf eingespielt und mit einem eigenen Lauf gegen den fertigen Baum abgenommen worden |
| Ist eine Prüfung gebaut oder geändert worden? | **Nein** – bewusst, mit benanntem Preis (Abschnitt 1) |
| Ist jede Zahl dieses Protokolls nachgezählt? | **Ja, und fünf waren falsch** (Abschnitt 5) – vier davon im Durchgang vor dem Commit, der sich damit zum wiederholten Mal getragen hat |
| Wurde die Endfassung gegen einen eigenen Lauf gehalten? | **Ja, zweimal** – die Läufe C und D, dazu V3. Ihr eigenes Ergebnis steht nach D-94 unterhalb der Trennlinie |

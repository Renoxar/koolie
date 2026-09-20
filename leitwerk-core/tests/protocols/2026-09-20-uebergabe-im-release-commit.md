# Protokoll: `K-80` entschieden – die Übergabe steht im Release-Commit, und ein unsichtbares Zeichen nimmt git die Normalisierung

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-20 |
| Release | `0.78.2` |
| Änderungsantrag | `CR-2026-107` |
| Art | Verfahrensänderung mit zwei neuen Prüfungen – **keine Sitzung, kein Kontingent, kein Modelllauf** |
| Gegenstand | `K-80`: die Übergabe entsteht nach dem Merge – und was die Gegenprüfung dazu gefunden hat |
| Ergebnis | 🟢 **`K-80` entschieden, alle drei Fragen beantwortet.** 🔴 **Vier Befunde, keiner davon in der Frage, die gestellt war:** ein Kopfblock mit einem anderen Stand als sein eigener Abschnitt 1; **ein einzelnes Wagenrücklauf-Zeichen, das git die Normalisierung nimmt** – vierzehn Träger, und es sind genau die vierzehn, die git nicht normalisiert hat; **keine der 65 Prüfungen konnte es sehen**; und **der Gegenbeweis hat den Zuschnitt der eigenen neuen Prüfung widerlegt** |

---

## 1. Was gefragt war

`K-80` steht seit `0.78.1` offen und ist dort ausdrücklich *„vor dem nächsten Release“* fällig gestellt worden. Das nächste Release ist der Meßtag von Bündel 4. Drei Fragen:

1. Wandert die Übergabe in den Release-Commit?
2. Entfällt dann die Nummer des Merge Requests aus ihr?
3. Gilt dasselbe für das Protokoll – oder ist die Übergabe der Sonderfall?

## 2. Die Gegenprüfung – und was sie außerdem gefunden hat

### 2.1 Der Anlaß bestätigt sich, und er ist größer als beschrieben

`K-80` nannte **fünf Stellen** mit einer Antragsnummer. Gezählt: **fünf Stellen, sieben Nummern.** Der beschriebene Nachtrag ist ein Commit direkt auf `main`, ohne Abnahme.

🔴 **Und er hat etwas hinterlassen, das `K-80` nicht nennt:**

| Stelle in der Übergabe | Stand, den sie nannte |
|---|---|
| Titelzeile | `0.78.1` |
| Abschnitt 1 („Lage“) | `0.78.1` |
| **Kopfblock, dritte Zeile** | 🔴 **`0.78.0`** |
| `leitwerk-core/VERSION` | `0.78.1` |

**Der Satz, der die Lage erklärt, war beim Lesen schon falsch** – keine Stunde nach dem Merge. Der Nachtrag hebt den Abschnitt, den er schreibt, und läßt den Kopf stehen.

### 2.2 🔴 Der teuerste Befund: ein Zeichen, das niemand sieht

Derselbe Nachtrag schrieb ein **echtes** Wagenrücklauf-Zeichen dorthin, wo die zwei Zeichen einer Escape-Folge gemeint waren – in genau dem Satz, der den CRLF-Befund von `0.78.1` beschreibt.

**Gemessen in einem eigens gebauten Repositorium, beide Fälle nebeneinander:**

| Träger | `core.autocrlf=true` | `* text=auto` |
|---|---|---|
| CRLF ohne verirrtes Zeichen | Blob steht auf **LF** | Blob steht auf **LF** |
| CRLF **mit** verirrtem Zeichen | 🔴 **unverändert CRLF** | 🔴 **unverändert CRLF** |

git stuft einen Träger mit einem einzelnen `CR` als **binär** ein. ➡️ **Die Regel für Zeilenenden greift bei genau den Dateien nicht, die sie brauchen.**

🟢 **Die Deckung im Bestand ist vollständig – und das ist der Beleg, nicht die Vermutung:**

| Gezählt über 440 versionierte Textträger (dazu eine Binärdatei) | Zahl |
|---|---|
| Blob auf LF | 426 |
| Blob gemischt | 11 |
| Blob auf CRLF | 3 |
| **Träger mit verirrtem Zeichen** | **14 – dieselben 14** |

**Zwei Bauformen, beide einzeln nachgesehen:** *Typ A* – **vierzehn Fundstellen in zwölf Trägern**, je am Zeilenende einer Tabellenzeile: elf Änderungsanträge mit je einer und eine Fähigkeitsmatrix mit drei, sämtlich aus der Zeit um `0.26.0`. *Typ B* – **zwei Fundstellen in zwei Trägern**, im Satz über die Escape-Folge: die Übergabe und `CR-2026-106`.

### 2.3 🔴 Warum es keine Prüfung gefunden hat – und warum das kein Zufall ist

Die Leseroutine des Validators öffnet im **Universal-Newline-Modus**. Dort ist jedes `CR` bereits ein Zeilenvorschub, bevor eine Prüfung hinsieht. **Alle 65 Prüfungen lasen durch dieselbe Routine.**

🔴 **Der Typ-B-Fall in `CR-2026-106` stand im Release selbst und hat die volle Abnahme bestanden** – Validator 0/0, Sondenlauf in beiden Kodierungsumgebungen, keine Einheit ohne `OK`. ➡️ **Die Antwort auf `K-80` allein hätte ihn nicht gefangen:** Die Reihenfolge erklärt 2.1, nicht 2.2. Jener Träger entstand **innerhalb** des Verfahrens.

*Eine Prüfung, die ihren Gegenstand an der eigenen Leseroutine verliert, ist die stillste Bauform von D-23.*

### 2.4 🔴 Der Gegenbeweis hat den eigenen Zuschnitt widerlegt

Die erste Fassung von **Prüfung 67** hielt die **Titelzeile** gegen `VERSION`. Gegen den unberührten Stand von `0.78.1` gefahren, meldete sie dort **nichts** – Titelzeile und `VERSION` stimmten überein, falsch war der **Kopfblock**.

➡️ **Eine Prüfung, die aus einem Befund entsteht, gehört gegen genau diesen Befund gehalten, bevor sie eingebaut wird.** Das ist D-23 in der Richtung, in der er selten gelesen wird: nicht *findet die Prüfung eine gesetzte Sonde*, sondern *findet sie den Fall, aus dem sie entstanden ist*.

🟢 **Der nachgerüstete Gegenstand meldete beim ersten Lauf zwei echte Altlasten, beide in Abschnitt 1 der Übergabe:**

| Fundstelle | Behauptung | Wirklich |
|---|---|---|
| Lagetabelle, Zeile *Framework* | Zweigstand **0.66.0** | **0.78.2** – **fünfzehn Releases** sind darüber hinweggegangen |
| Abnahmezeile daneben | Prüfapparat **63**, **243 Einheiten** | **67** Prüfungen, **269** Einheiten |

**Zwei weitere Fundstellen waren Chronik und kein Befund.** Statt einer Ausnahmeliste trägt die Übergabe jetzt eine Konvention, die eine Zeile lang ist: **Den Zweignamen trägt nur eine Aussage über den jetzigen Stand; ein Chronikabschnitt sagt *das Release*.** Drei Sätze sind umformuliert. *Eine Ausnahmeliste wächst; eine Konvention bleibt eine Zeile.*

🔴 **Und beim Schreiben dieses Releases hat die neue Prüfung ihren eigenen Beschreibungstext gemeldet** – die Tabelle oben nannte den Zweignamen. *Wer einen Formfehler beschreibt, schreibt ihn nicht hin*, zum **fünften** Mal. Diesmal hat es keine Leserin nach dem Merge gefunden, sondern der Validator vor dem Commit.

## 3. Die Entscheidung

| Frage | Antwort | Der Grund, der den Ausschlag gab |
|---|---|---|
| Übergabe in den Release-Commit? | **Ja** | Alles, was sie braucht, liegt nach dem Sondenlauf vor – bis auf die Antragsnummer, und die entfällt |
| Antragsnummer entfällt? | **Ja**, fünf Stellen, sieben Nummern | Sie war der einzige Grund, überhaupt nach dem Merge zu schreiben. *Alles gemergt, kein offener Antrag* beantwortet `git` – **prüfbar statt gepflegt** |
| Gilt dasselbe für das Protokoll? | **Nein, kein Sonderfall nötig** | Es steht seit jeher vor dem Commit. Eine Regel für einen Fall, den es nicht gibt, ist die **Ausnahme mit leerem Geltungsbereich** (0.57.1) |

🔴 **Abschnitt 4 des Entwicklungsprofils führte die Übergabe überhaupt nicht** – sieben Schritte von Befund bis Merge, und der Träger, der die nächste Sitzung trägt, kam darin nicht vor. Er steht jetzt als Schritt 7.

**D-216** und **D-217** halten es fest. `K-80` ist erledigt, `K-81` ist neu.

## 4. Was gebaut wurde

| Prüfung | Gegenstand | Einheiten |
|---|---|---|
| **66** | Kein Textträger trägt einen Wagenrücklauf ohne folgenden Zeilenvorschub – **gelesen wird byteweise** | 2 Sonden, 2 Gegenproben |
| **67** | Titelzeile **und** Lagezeilen der Übergabe gegen `VERSION`, und keine Antragsnummer | 4 Sonden, 2 Gegenproben |

**Die beiden Gegenproben, auf die es ankommt:**

- **`66b`** stellt einen Träger durchgehend auf LF und wird **nicht** gemeldet. Sie belegt die Grenze: Gemessen wird das **Zeichen**, nicht die **Form** – welche Form gilt, ist `K-81` und nicht entschieden.
- **`67b`** entfernt `UEBERGABE.md` und belegt die **Enthaltung**, mit der Prüfung 67 in jeder Installation läuft. *Eine ungemessene Enthaltung ist von einer Prüfung, die ihren Gegenstand verloren hat, nicht zu unterscheiden.*

## 5. Der Gegenbeweis gegen den Vorstand (D-23)

Der neue Validator, gefahren gegen den **unberührten** Stand von `0.78.1` (`git archive main`):

| Prüfung | Meldung gegen den Vorstand |
|---|---|
| 66 | **14 Träger**, 16 Fundstellen |
| 67 (c) | **7 Antragsnummern** in der Übergabe |
| 67 (a) | 🔴 **keine** – und genau das hat den Zuschnitt widerlegt (2.4) |

## 6. Abnahme

- `validate-framework.py --root .`: **0 Fehler, 0 Warnungen**.
- `probe-pruefungen.py` in **beiden** Kodierungsumgebungen (D-49): **269 Einheiten**, 368 Meldezeilen, **keine ohne `OK`**.

🔴 **Die eine Grenze der neuen Reihenfolge:** Das Heben des Übungsrepositoriums arbeitet mit `git archive HEAD` und kann nicht vor dem Commit geschehen. Was die Übergabe darüber sagt, ist eine **Vorhersage** – gemessen statt behauptet: Der Trockenlauf gegen den **Arbeitsbaum** meldet **0 angelegt, 0 aktualisiert, 64 unverändert**. ➡️ *Ein Trockenlauf gegen den committeten Stand mißt den Vorstand gegen sich selbst* (0.59.1).

## 7. Der Preis, gemessen

Sechzehn Zeichen weniger – und git normalisiert die vierzehn Träger: **3744 Zeilen neu, 3746 gelöscht.** Deshalb steht die Berichtigung in einem **eigenen Commit vor dem Release-Commit**. Ein Release, dessen Diff aus 3700 Zeilen Rauschen um vierzig Zeilen Inhalt besteht, ist **D-213 an einer neuen Stelle**: *Die Abhilfe ist eine Reihenfolge, kein Eingriff.*

⚠️ **`git blame` der vierzehn Träger zeigt danach den Normalisierungs-Commit.** Wer die Herkunft einer Zeile sucht, nimmt ihn mit `--ignore-rev 6f86fe4` heraus.

## 8. Was offen bleibt

- **`K-81`:** Welche Zeilenende-Form im Repositorium gilt und wer sie durchsetzt. 🔴 **Nicht vor dem Meßtag** – `git archive` baut die Meßbäume von Bündel 4, und eine Zeilenende-Regel kann deren Inhalt ändern. Dieselbe Begründung wie bei `K-79`.
- **Gemessen ist bereits, daß eine `.gitattributes` den Befund nicht gelöst hätte:** Sie läßt einen Träger mit verirrtem Zeichen unberührt wie `core.autocrlf`.
- ⚠️ **Ohne Abhilfe, nur gezählt:** **Acht der zwölf zuletzt eingetragenen Zeilen** des Decision Logs stehen in ASCII-Umschrift; über den ganzen Bestand sind es fünfzehn von 295, und die Regel aus dem Arbeitswissen verlangt für `governance/` echte Umlaute.

## 9. Laufzeiten (unterhalb der Trennlinie, D-94)

| Lauf | Wanduhr |
|---|---|
| mit `PYTHONIOENCODING=utf-8` | 316,3 s |
| ohne | 311,9 s |

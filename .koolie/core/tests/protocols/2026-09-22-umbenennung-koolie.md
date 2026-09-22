# Protokoll: Die Umbenennung auf Koolie – und die fünf Stellen, die `<CORE_DIR>` für ein Verzeichnissegment hielten

| Feld | Wert |
|---|---|
| Gegenstand | Der Umbenennungslauf nach `CR-2026-119` Abschnitt 5 – `leitwerk-core/` → `.koolie/core/`, `project-overlay/` → `.koolie/project-overlay/`, beide übernehmenden Projekte, Prüfung 75 |
| Antrag | `CR-2026-122` (Vorgänger: `CR-2026-119`, `CR-2026-098`) |
| Datum | 2026-09-22 |
| Framework-Version | 0.87.0 (Befunde) / 0.88.0 (Umsetzung) |
| Art | **ohne Kontingent** – kein Lauf an einem Client, keine Modellzeit |
| Ergebnisstatus | **bestanden.** 498 Dateien gewandert, 1.645 Ersetzungen in 197 Trägern, zwei neue Prüfungen mit vier Sonden und drei Gegenproben, beide übernehmenden Projekte gehoben und migriert |

> 🔴 **Dreizehnter Durchgang in Folge, bei dem der billigste Befund vor dem ersten
> Handgriff fällt.** Zehn Befunde, keiner hat Kontingent gekostet, **drei hätten den
> Schritt still falsch gemacht.** 🔴 **Zwei weitere fielen erst im Abnahmelauf** – und
> nur dort waren sie zu finden: den einen deckt keine Prüfung ab, den anderen zeigt erst
> der zeilengleiche Vergleich beider Kodierungsumgebungen.

## 1. Die Lage vor dem Durchgang

`CR-2026-119` hat die Umbenennung am 2026-09-22 vollständig entschieden (D-269 bis
D-275) und den Ablauf in zehn Schritten festgeschrieben. Alle Zahlen dort sind **gegen
`0.85.0`** gezählt, und der Antrag sagt selbst: *„Wer den Lauf fährt, zählt sie nach."*

**Der Vorbedingungsdurchgang hat genau das getan** – und dabei zehn Befunde erhoben,
von denen drei den Lauf still falsch gemacht hätten.

## 2. Die Zahlen, nachgezählt

| Größe | `CR-2026-119` (gegen `0.85.0`) | nachgezählt (gegen `0.87.0`) | |
|---|---|---|---|
| verfolgte Dateien | 494 | **502** | +8 |
| davon unter dem Kernverzeichnis | 490 | **498** | wandern mit einem `git mv` |
| außerhalb | 4 | **4** | unverändert |
| Fundstellen des Pfades | 1.976 in 326 | **2.001 in 330** | +25 |
| Träger mit `<CORE_DIR>` | 43 | **46** | +3 |
| Werkzeuge, Muster `leitwerk` | 304 | **304** | 🟢 unverändert |
| … alle Schreibweisen / nur Pfad | 311 / 295 | **311 / 295** | 🟢 unverändert |
| Migrationsfläche Schicht 3 | 30 Dateien / 141 | **30 / 141** | 🟢 exakt |
| **Arbeitsfläche des Textlaufs** | **925 in 128** | 🔴 **1.529 in 191** | siehe V1 |

## 3. Die zwölf Befunde

### 🔴 V1 Die Arbeitsfläche war ein anderer Gegenstand als die genannte Zahl (D-298)

`CR-2026-119` Abschnitt 3.2 zählt **Backtick-Pfade**, weil ihn die Verträglichkeit mit
Prüfung 12 interessierte – und sein Schlußsatz macht daraus *„die Arbeitsfläche des
Textlaufs ist damit 925 Fundstellen in 128 Dateien"*.

**Gemessen am 2026-09-22:** In den lebenden Trägern stehen **1.472 Fundstellen des
Pfades**, davon **436 in 86 Trägern außerhalb von Backticks** – 144 allein in
`probe-pruefungen.py` als **Suchtexte von Präparationen**, die nach D-23 ihren
Gegenstand verlören –, dazu **57 Nennungen des bloßen Namens in 16 Trägern**.

> *Wer die 925 als Arbeitsfläche nimmt, läßt 604 Fundstellen stehen.* **Dieselbe
> Bauform wie die vier Zahlen von `0.87.0`: eine Tabelle, die ERKLÄREN sollte, und aus
> der dann GEZÄHLT wurde.**

### 🔴 V2/V3 Sechs Stellen hielten den Kernpfad für ein Segment (D-299)

| Stelle | was sie tat | was sie nach dem Umzug geliefert hätte |
|---|---|---|
| `install.py:102` | `os.path.basename(HERE)` | `core` statt `.koolie/core` |
| `build/assemble.py:65` | `os.path.basename(CORE)` | dito |
| `validate-framework.py:837` | `os.path.basename(dirname³(mp))` | dito |
| `hook-check-secrets.py:128` | `os.path.basename(dirname³(__file__))` | dito |
| `hook-check-secrets.py:243` | `re.escape(NAME)` zwischen `[\\/]` | ein Muster für **ein** Segment |
| `hook-check-secrets.py:137` | `PROJEKTWURZEL` = vier `dirname` | **`.koolie/`** statt der Projektwurzel |
| `tests/erhebungen/ablage.py:48` | `WURZEL` = drei `dirname` | dito |

🔴 **An `install.py:102` stand dabei wörtlich**, die Zeile stehe dort, *„damit eine
spätere Umbenennung nur eine Stelle berührt"*. **Die Abhilfe wäre genau an ihrem Anlaß
zerbrochen.**

🔴 **Und es wäre kein Validatorfehler gewesen:** Der Validator band denselben Wert an
derselben Stelle auf dieselbe Weise und hätte ihn **bestätigt**. *Zwei Stellen, die
einander decken* (0.57.0), über Werkzeuggrenzen hinweg.

🔴 **`PROJEKTWURZEL` ist die schärfste:** Nach dem eigenen Kommentar des Hooks ist sie
*„die obere Freigabegrenze der Pfadauflösung"*. Vier `dirname` hätten sie auf `.koolie/`
gesetzt – eine Ebene zu tief, und der Schutz-Hook hätte jeden Pfad außerhalb von
`.koolie/` für außerhalb des Projekts gehalten.

➡️ **Abhilfe:** `CORE_REL` als benannte Zeichenkette an vier Stellen, `CORE_TIEFE` statt
gezählter `dirname`, und **Prüfung 76** hält sie gegeneinander.

### 🔴 V10 Der Textlauf hat den Befund selbst erzeugt

`.koolie` beginnt mit einem **Punkt**, und der ist im regulären Ausdruck ein
Metazeichen. **Fünf Muster hat der Sweep angefaßt:** vier wurden **zu weit** (der Punkt
trifft jedes Zeichen), und eines – `STRUCTURE_PATH_PATTERNS` im Schutz-Hook, der
Schreibschutz von `project-overlay` – zugleich **zu eng**, weil der Schrägstrich
wörtlich stand, wo `[\\/]` nötig ist.

> *Eine Schranke, die die Schreibweise unterscheidet, und ein Dateisystem, das sie nicht
> unterscheidet* – **das ist D-277 (`B3`), diesmal vom eigenen Werkzeug gebaut.**

### 🔴 V8/V9 Zwei Klassen, die ein Sweep nicht anfassen darf (D-300, D-301)

**V8 – Namen datierter Belegablagen.** In `UEBERGABE.md` und im Meßapparat steht der
bloße Name überwiegend als `devpacks/leitwerk-erhebungen-<datum>-<bündel>` oder
`leitwerk-UEBERGABE-archiv-…`. Sie liegen **außerhalb** des Repositoriums und werden
nicht umbenannt. *Ein Sweep hätte aus jeder vorhandenen Belegablage eine gemacht, die es
nicht gibt* – **D-283 mit umgekehrtem Vorzeichen und selbstverschuldet.**

**V9 – Aussagen über den alten Namen.** Sieben von 23 bloßen Nennungen:

| Stelle | was der Sweep daraus gemacht hätte |
|---|---|
| `build/doc/32-abschluss.md` | eine gefälschte Changelog-Zeile (*„0.7.0 – Das Framework heißt Leitwerk"*) |
| `docs/ROADMAP.md` | *„den Namen `koolie` durch einen griffigeren ersetzen"* |
| `ablage.py` (Kommentar) | ein Pfadidentitätsbefund ohne Gegenstand |
| `README.md` | 🔴 **die Namensmetapher** – *„Ein Leitwerk fliegt das Flugzeug nicht"* |
| `UEBERGABE.md` (3×) | Titel, zwei Meßangaben über das **gemessene Suchmuster** |
| `UEBERGABE.md` | die Befundaufzeichnung zu D-219 |

➡️ **Acht Stellen sind vor dem Lauf maskiert** und danach wörtlich zurückgesetzt worden,
mit einem Wächter auf genau einen Treffer. 🟢 **Der Wächter hat zweimal gegriffen** –
einmal, weil ein Suchtext `\\leitwerk` mit **zwei** Backslashes trägt, einmal wegen eines
Zeilenumbruchs mitten im Suchtext. **Beide Male wurde nichts geschrieben.**

⚠️ **Preis, ein echter Verlust:** Die Metapher ist umgeschrieben (*„Dieses Framework
fliegt das Flugzeug nicht…"*). Das **Bild bleibt, die Namensableitung entfällt** –
`Koolie` trägt keine eigene, und eine erfundene wäre eine Behauptung.

### 🔴 V11 Der Sweep verlängert ein Segment, das im Kern liegt – und nur der Sondenlauf findet es

`templates/project-overlay` ist ein Verzeichnis **im Kern** und wandert nicht. Der Lookbehind `(?<!templates/)` des Textlaufs hat es dort erwischt, wo es als **zusammenhängender Pfad** stand – **nicht** dort, wo es als **eigenes Segment einer Liste** steht:

```python
os.path.join(KERN, "templates", ".koolie/project-overlay", "OVERLAY.md")
```

Das ergibt `.koolie/core/templates/.koolie/project-overlay/OVERLAY.md` – einen Pfad, den es nicht gibt. **Prüfung 28 verlor damit stillschweigend einen von drei Trägern**, und ihre Sonde `28b` blieb grün, weil sie den zweiten trifft.

| Stelle | was daraus wurde |
|---|---|
| `validate-framework.py:3175` | die Trägerliste von Prüfung 28 – 🔴 **ein Träger verloren** |
| `validate-framework.py:6261` | dieselbe Bauform in einer zweiten Liste |
| `auswerten-b5.py` (2×) | ein Lookbehind, der die Vorlage ausnehmen sollte – **er nimmt nach dem Umzug nichts mehr aus** (0.57.1), und der führende Punkt war zugleich ein Metazeichen |

🔴 **Der Validator hat es nicht gemeldet.** Prüfung 12 prüft Backtick-Pfade und Markdown-Links – **keine Python-Ausdrücke**. Gefunden hat es **Sonde `28a`** im Abnahmelauf, als einzige Abweichung unter 423 Einheiten.

> 🟢 **Und genau das hat `CR-2026-119` Abschnitt 3.3 vorhergesagt:** *„Der Sondenlauf in beiden Kodierungsumgebungen ist bei dieser Umbenennung kein Formalakt, sondern der eigentliche Nachweis.“* **Die Vorhersage hat sich eingelöst, und zwar an einer Stelle, die keine Prüfung abdeckt.**

### 🔴 V12 Ein Umlaut im Beschreibungssatz bricht den zeilengleichen Vergleich

Der erste Abnahmelauf lief in beiden Kodierungsumgebungen mit **Exit 0**. Der zeilengleiche Vergleich nach D-49 fand trotzdem **eine** Abweichung unter 456 Zeilen: Der Beschreibungssatz der neuen Gegenprobe `75b` trug *Chronikträger*, und ohne `PYTHONIOENCODING=utf-8` wird das `ä` verstümmelt.

🟢 **Alle bestehenden Sondentexte schreiben ASCII-Umschrift** – `Traeger`, `laeuft`, `Pruefung`. Das sah bisher wie eine Schreibgewohnheit aus und ist die **Bedingung der Abnahme**.

🔴 **Und die Gegenrichtung gilt in derselben Datei:** Die Suchtexte (`M75_LEER`, `M76_BASENAME` …) **müssen** die Umlaute tragen, weil sie gegen die Meldung des Validators gehalten werden – und die ist in deutscher Rechtschreibung.

> ➡️ *Zwei Textsorten in derselben Datei, mit entgegengesetzter Regel: was AUSGEGEBEN wird, steht in ASCII-Umschrift; was VERGLICHEN wird, wortgetreu.*

### ⚠️ V4 Der Zeichendeckel – und er ist an der falschen Stelle gemessen worden

`AGENTS.md` steht auf 11.874 von 12.000. Der Umzug rechnet `leitwerk-core`→`.koolie/core`
11× mit **−1** und `project-overlay`→`.koolie/project-overlay` 5× mit **+8**: netto
**+29.** 🔴 **Und diese Zahl war GERECHNET.** An der erzeugten Datei gemessen sind es **11.887 von 12.000, Luft 113** – der Durchgang vor dem Commit hat es gefangen, nachdem die 97 schon in vier Trägern standen. *Eine Zahl, die man nicht gezählt hat, ist erfunden.*

🔴 **Die Messung hat den falschen Bestand befragt** (D-165). Sie lief gegen das
Framework-Repositorium, dessen Laufzeitfassung des Overlays 3.268 Zeichen hat. **Im
Übungsrepositorium steht sie bei 5.963** (K-88) – und ist mit dem Umzug auf **6.024**
gewachsen, **über die SOLL-Grenze von 6.000.** Der Validator dort meldet es als Warnung.

➡️ **Benannt, nicht geändert:** `K-88` sagt selbst, daß eine Kürzung ein Eingriff in den
Meßgegenstand wäre.

### 🔴 „Der vierte Träger, schon wieder" – und diesmal zweimal

`install.py --update` faßt weder die **Berechtigungsdatei** des Packs noch die
**Laufzeitfassung des Overlays** an: beide tragen Projektwerte. Im Framework-Repositorium
waren **45 Fundstellen in sieben Trägern** von Hand nachzuziehen.

🟢 **Das ist der Migrationshinweis aus D-270, am eigenen Repositorium erprobt** – und er
ist dadurch **gegen den Bestand erzeugt und nicht abgeschrieben.**

### 🔴 Ein Chronikträger kann eine Zeile führen, die keine Chronik ist

`CHANGELOG.md` nennt in **Zeile 3** den Prozeßpfad, `tests/protocols/README.md` in
**Zeile 3** den Testkatalog. Beides sind **Kopfzeilen mit einem AKTUELLEN Pfad** – und
die Chronikausnahme deckte sie mit.

> *Der benannte Preis von Prüfung 75 – die Ausnahme gilt je Träger, nicht je Zeile – ist
> bei ihrem ersten Lauf angefallen.* ➡️ **Wer eine Ausnahme je Träger zieht, liest den
> KOPF des Trägers, bevor er sie zieht.**

### 🔴 Der Vermerk „dieses Release" stand auf acht Zeilen

`0.87.0` hat gebucht, ihn *„auf die aktuelle gesetzt"* zu haben – und **drei von zehn**
angefaßt (`0.82.0`, `0.85.0`, `0.86.0`). **Sieben ältere standen weiter da** (`0.56.0`,
`0.61.0`, `0.68.0` bis `0.71.0`, `0.78.0`). Mit diesem Release steht er **einmal**.

### 🔴 Ein Nachbarfund – gemeldet und NICHT geändert (`K-100`)

**27 Klärungspunkte – `K-71` bis `K-98` – stehen in der Entscheidungstabelle** statt in
der Klärungstabelle, die bei `K-70` endet. Sie rendern unter den Spaltenüberschriften
`ID | Entscheidung | Begründung | Alternativen | Status | Datum`. **Gemessen mit
`git log -S`: seit `0.66.0`, 32 Releases.**

**Das ist D-264 an einer zweiten Stelle**, und Prüfung 74 prüft nur die
Fähigkeitsmatrizen. ➡️ Nach `FW-SC-01` gemeldet, nicht geändert.

## 4. Die zwei neuen Prüfungen

### Prüfung 75 – Kein Restbestand des alten Namens (D-271)

**Zählbereich** ist im Framework-Repositorium **jeder verfolgte Träger** (die Lehre von
D-295), in einem übernehmenden Projekt **nur, was das Framework ausliefert**.
**Ausgenommen** ist eine deklarierte Menge in vier Klassen, **in beide Richtungen
geprüft.**

🔴 **Zwei Konstruktionsfehler sind erst im übernehmenden Projekt aufgefallen**, und
beide hatten dieselbe Ursache: *Eine Prüfung, die im Framework grün und in jeder
Installation rot ist, ist falsch gebaut.*

1. Die Rückwärtsrichtung meldete **neun** Träger als „leere Ausnahme", die es in dieser
   Installation schlicht nicht gibt – `UEBERGABE.md` wandert nie in ein Zielprojekt.
2. Der Zählbereich erfaßte **projekteigene** Dateien. Zwei Nennungen im
   Übungsrepositorium (`tools/praeparationen.py`,
   `tools/mentorenblatt/PRAEPARATIONEN.md`) sind **Belegablagennamen** und nach D-300
   legitim – *ein Projekt darf in seine eigenen Dateien schreiben, was es will.*

🟢 **Und sie hat sich bei ihrem ersten Lauf selbst gemeldet:** `probe-pruefungen.py`
nennt den alten Namen viermal, **weil sein Gegenstand der alte Name ist**. Daraus ist
die vierte Ausnahmeklasse geworden – *eine Prüfung, die einen Namen sucht, muß ihn
nennen; und ihre Sonde muß ihn schreiben.*

### Prüfung 76 – Die Lage des Kerns steht an vier Stellen (D-299)

**Zwei Gegenstände, dieselbe Frage aus zwei Richtungen:** alle vier Angaben tragen
denselben Wert, **und keine leitet ihn über `os.path.basename` ab.** *Ohne den zweiten
wäre der erste erfüllbar, indem alle vier denselben Fehler machen – und genau das war
der Zustand bis `0.87.0`.*

### Der Wirkungsnachweis

🔴 **`kopie()` schließt `.git` aus**, und Prüfung 75 liest `git ls-files`. **Ohne
`git init` hätte sie in JEDER Sonde ihren dritten Ausgang genommen** – *„nicht meßbar"* –
und dabei ausgesehen wie eine, die nichts gefunden hat. Derselbe Griff wie bei
Gegenstand 2 von Prüfung 45.

| Einheit | Gegenstand | Ergebnis |
|---|---|---|
| Gegenprobe `75a` | der ausgelieferte Bestand läuft durch, und die Prüfung ist dabei **nachweislich gelaufen** | 🟢 |
| Sonde `75a` | der alte Name in einem verfolgten Träger außerhalb der Ausnahmemenge | 🟢 |
| Gegenprobe `75b` | derselbe Text in einem Chronikträger bleibt unbeanstandet – **der Zuschnitt** | 🟢 |
| Sonde `75b` | die zweite Richtung: eine Ausnahme, aus der die Fundstelle verschwunden ist | 🟢 |
| Sonde `75c` | der verlorene Anker – das eigene Muster trifft den alten Namen nicht mehr | 🟢 |
| Sonde `76a` | eine der vier Stellen trägt eine andere Lage | 🟢 |
| Sonde `76b` | **die `basename`-Bindung wieder angelegt** | 🟢 |
| Sonde `76c` | eine Stelle verliert ihre Lageangabe | 🟢 |
| Gegenprobe `76a` | vier Stellen, ein Wert, keine `basename`-Bindung | 🟢 |

## 5. Die beiden übernehmenden Projekte

### Übungsrepositorium (`0.84.0` → `0.88.0`)

**77 Träger** von Hand nachgezogen, Overlay auf `0.88.0` gehoben.
🔴 **Drei Projektdateien nennen kein `leitwerk`, sondern `project-overlay/`** – die
Migrationsfläche von D-270 ist gegen eine Umbenennung **ohne** Umzug gemessen, und der
Umzug ist größer. ⚠️ Die Laufzeitfassung des Overlays ist auf **6.024** Zeichen
gewachsen (SOLL-Grenze 6.000).
**Ergebnis: `--strict-overlay` 0 Fehler, 1 Warnung.**

### Pilot (`0.54.1` → `0.88.0`, 34 Releases)

**61 Träger** nachgezogen. **Nach dem Heben meldete der Validator zehn Fehler.**

🟢 **Der Entlastungslauf hat sie zugeordnet** – Validator gegen den Stand **vor** dem
Heben, aus dem Sicherungsbundle: **ein** Fehler. Die **neun neuen kamen sämtlich aus dem
Versionssprung, nicht aus der Umbenennung:**

- **sieben Pflichtplatzhalter** waren durch ihren **Wert** ersetzt statt gebunden
  (D-160, seit `0.63.0`) – geändert ist allein die **Schreibweise**, kein Wert;
- **`autoMemoryEnabled`** fehlte in `.claude/settings.json` (D-155) – *die
  Berechtigungsdatei ist der vierte Träger*;
- die Overlay-Version stand in **drei** Trägern und mußte in allen drei nachgezogen
  werden – **der Validator meldete sie nacheinander**, genau wie die Übergabe es sagt.

**Ergebnis: 1 Fehler, 2 Warnungen – derselbe Stand wie vor dem Heben.** Der verbliebene
Fehler ist ein gesperrter Begriff in `CHANGELOG.md` und **Projektarbeit**.

> 🟢 *Ein Sprung über 34 Releases hat nichts verschlechtert – und das ist nur deshalb
> eine Aussage, weil der Ausgangsstand gemessen wurde und nicht angenommen.*

## 6. Der Durchgang vor dem Commit

| Zahl | zuerst genannt | nachgezählt |
|---|---|---|
| Arbeitsfläche des Textlaufs | 925 in 128 (`CR-2026-119`) | 🔴 **1.529 in 191** – der Antrag zählte Backtick-Pfade |
| Zeichen frei in der Wurzeldatei | „126" (Übergabe), dann „97" (gerechnet) | 🔴 **113 – an der erzeugten Datei gemessen.** *Die zweite Zahl war hochgerechnet und stand schon in vier Trägern* |
| Vermerk „dieses Release" | „auf die aktuelle gesetzt" (`0.87.0`) | 🔴 **acht Zeilen, drei von zehn behoben** |
| Migrationsfläche Schicht 3 | 30 Dateien / 141 (D-270) | 🟢 **30 / 141 – exakt** |
| Nennungen in den Werkzeugen | 304 / 311 / 295 | 🟢 **unverändert** |
| Laufzeitfassung des Übungs-Overlays | 5.963 von 6.000 (K-88) | 🔴 **6.024 – über der SOLL-Grenze** |

# Änderungsantrag `CR-2026-122`

| Feld | Inhalt |
|---|---|
| Titel | Der Umbenennungslauf auf `Koolie` – und die fünf Stellen, die `<CORE_DIR>` für ein Verzeichnissegment hielten |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-22 |
| Betroffene Artefakte | **der gesamte Bestand** – `leitwerk-core/` ist `.koolie/core/`, `project-overlay/` ist `.koolie/project-overlay/`, `<CORE_DIR>` hat einen neuen Wert; dazu beide übernehmenden Projekte und das Repositorium bei Gitea |
| Ebene laut Entscheidungsbaum 6 | **Core**, mit Wirkung auf jede Installation |
| Art | **Umbenennungslauf ohne Kontingent** – kein Lauf an einem Client, keine Modellzeit |
| Vorgänger | `CR-2026-119` (Vorlage und Entscheidung, `E1` bis `E9`, D-269 bis D-275), `CR-2026-098` (das frameworkeigene Unterverzeichnis) |
| **Status** | **ENTSCHIEDEN und AUSGEFÜHRT am 2026-09-22** (D-298 bis D-304). `K-50`, `K-75` (1)+(2) waren mit `0.85.2` geschlossen; **`K-84` und `K-97` sind mit diesem Antrag geschlossen**, `K-100` ist neu |

## 1. Anlass

`CR-2026-119` hat die Umbenennung am 2026-09-22 vollständig entschieden – Name, Ort,
Zeitpunkt, Migrationsweg, Prüfung, Gitea-Schritt. Offen blieb der **Lauf**, und er stand
als Posten `~0.88.0` im Releaseplan, hinter dem Rest von `AP2`. `AP2` ist mit `0.86.0`
zu Ende gefahren, Kriterium 1 mit `0.87.0` auf null gebracht: **Der Posten ist regulär
fällig geworden.**

Dieser Antrag legt nicht die Umbenennung selbst zur Entscheidung vor – das hat
`CR-2026-119` getan. **Er legt vor, was der Vorbedingungsdurchgang gefunden hat**, und
dort stand ein Befund, den die Entscheidung von `0.85.2` zwar benannt, aber nicht
ausgemessen hatte.

## 2. Der Vorbedingungsdurchgang – zehn Befunde, und drei hätten den Schritt still falsch gemacht

> 🟢 **Zum dreizehnten Mal in Folge der billigste Befund des Releases.** Kein Lauf, kein
> Kontingent; die teuersten Befunde fielen, bevor ein Pfad angefaßt war.

| # | Befund | Wirkung |
|---|---|---|
| **V1** | **Die Arbeitsfläche des Textlaufs ist 1.529 Fundstellen in 191 Trägern, nicht 925 in 128** | `CR-2026-119` zählte **Backtick-Pfade**, weil ihn die Verträglichkeit mit Prüfung 12 interessierte – und machte daraus *„die Arbeitsfläche des Textlaufs"*. **436 Fundstellen in 86 lebenden Trägern stehen außerhalb von Backticks**, dazu 57 bloße Namensnennungen. *Wer die 925 nimmt, läßt 604 stehen.* (**D-298**) |
| **V2** | 🔴 **Fünf Stellen behandeln `<CORE_DIR>` als EIN Verzeichnissegment** | `install.py`, `build/assemble.py`, `validate-framework.py` und `hook-check-secrets.py` banden ihn mit `os.path.basename()`; `os.path.basename(".koolie/core")` ist **`core`**. Dazu das Pfadmuster des Schreibschutzes, das mit `re.escape` auf **ein** Segment gebaut war (**D-299**) |
| **V3** | 🔴 **Zwei weitere Stellen zählen EBENEN** | `PROJEKTWURZEL` des Schutz-Hooks (vier `dirname`, nötig fünf) und `WURZEL` in `ablage.py` (drei, nötig vier). Die so bestimmte Projektwurzel wäre `.koolie/` gewesen – **die obere Freigabegrenze der Pfadauflösung eine Ebene zu tief** (**D-299**) |
| **V4** | ⚠️ **Der Zeichendeckel der Wurzel-Anweisungsdatei hält – mit 113 statt 126 Zeichen** | Gemessen: 11.874 von 12.000. Der Umzug rechnet `leitwerk-core`→`.koolie/core` 11× mit −1 und `project-overlay`→`.koolie/project-overlay` 5× mit **+8**: netto **+29**. 🔴 **Diese Zahl war GERECHNET** – an der erzeugten Datei gemessen sind es **11.887, Luft 113**; der Durchgang vor dem Commit hat es gefangen |
| **V5** | 🔴 **`D-275` hat seine Voraussetzung verloren, und der Termin ist der 24.09.** | Es entschied *„die Vorführung läuft auf `leitwerk-core/`"* – und ruhte darauf, daß `E1` abgelehnt war und die Umbenennung damit hinter den Vortrag fiel. Sie fällt davor (**D-302**) |
| **V6** | ⚠️ **Der Pilot steht auf Kernversion `0.54.1`** – 34 Releases zurück | Das Übungsrepositorium steht auf `0.84.0`. Beide werden gehoben und migriert |
| **V7** | 🟢 **Fünf Angaben der Übergabe halten nachgezählt** | `CR-2026-122`, `D-298`, `K-100`, `G-21`, `UEB-32`; **Prüfung 75 ist frei** (höchste gebaute: 74); Validator grün auf dem Ausgangsstand; **Migrationsfläche exakt die 30 Dateien / 141 Nennungen aus D-270** |
| **V8** | 🔴 **Der bloße Name steht überwiegend in Namen datierter BELEGABLAGEN** | `devpacks/leitwerk-erhebungen-…`, `leitwerk-UEBERGABE-archiv-…`. Sie liegen außerhalb des Repositoriums und werden nicht umbenannt – *ein Sweep hätte aus jeder vorhandenen Belegablage eine gemacht, die es nicht gibt* (**D-300**) |
| **V9** | 🔴 **Sieben der 23 bloßen Nennungen sind Aussagen ÜBER den alten Namen** | Darunter die Changelog-Zeile zu `0.7.0`, zwei Meßangaben, die das **gemessene Suchmuster** nennen – und die **Namensmetapher der Wurzel-README** (**D-301**) |
| **V11** | 🔴 **Der Sweep hat ein Pfadsegment verlängert, das im KERN liegt – und nur der Sondenlauf hat es gefunden** | `templates/project-overlay` wandert nicht. Der Lookbehind `(?<!templates/)` hat es dort erwischt, wo es als **zusammenhängender Pfad** stand – nicht dort, wo es als **eigenes Segment einer Liste** steht: `os.path.join(KERN, "templates", "project-overlay", …)`. **Vier Stellen, zwei echte Fehler: Prüfung 28 verlor stillschweigend einen von drei Trägern.** 🔴 **Der Validator meldete es nicht** – Prüfung 12 prüft Backtick-Pfade und Markdown-Links, keine Python-Ausdrücke. **Gefunden hat es Sonde `28a`** |
| **V10** | 🔴 **Der Textlauf schreibt in fünf reguläre Ausdrücke, und `.koolie` beginnt mit einem Metazeichen** | Vier Muster wurden **zu weit**, und der Schreibschutz von `project-overlay` im Hook zugleich **zu eng** – der Schrägstrich stand wörtlich, wo `[\\/]` nötig ist. **Der Sweep hat den Befund selbst erzeugt** (**D-299**) |

### 🔴 Der schwerste: die Abhilfe, die genau an ihrem Anlaß zerbrochen wäre

An `install.py` stand seit `0.02.0` wörtlich:

> *„`<CORE_DIR>` steht in keinem Manifest … Er wird hier gesetzt, damit eine spätere
> Umbenennung (Roadmap P3) nur eine Stelle berührt."*

**Die Zeile, die eine Umbenennung billig machen sollte, hätte sie nicht überlebt.**
`os.path.basename(".koolie/core")` ist `core`; jede gerenderte Regeldatei hätte einen
Pfad getragen, den es nicht gibt.

🔴 **Und es wäre kein Validatorfehler gewesen.** Der Validator band denselben Wert an
derselben Stelle auf dieselbe Weise – er hätte ihn **bestätigt**. *Zwei Stellen, die
einander decken* (0.57.0), diesmal über Werkzeuggrenzen hinweg.

> ➡️ *Eine Abhilfe, die einen Fall vorwegnimmt, gehört an dem Fall gemessen, den sie
> vorwegnimmt – nicht an dem, den es gerade gibt.*

## 3. Was gelaufen ist – gemessen, nicht geschätzt

| Schritt | Maß |
|---|---|
| 1. Sicherung beider übernehmenden Projekte | zwei `git bundle --all` unter `C:\lw-mig` |
| 2. `git mv leitwerk-core .koolie/core` | **498 Dateien**, alle als Umbenennung erkannt; `project-overlay/` von Hand nach `.koolie/project-overlay/` |
| 3. Textlauf über die lebenden Träger | **1.645 Ersetzungen in 197 Trägern**: 1.472 Pfad, 2 Pfad in Großschreibung, 156 Overlay-Pfad, 15 bloßer Name. **Chronik ausgenommen** (D-273), **acht Stellen maskiert** (D-301) |
| 4. Werkzeuge | `CORE_REL` an vier Stellen, `CORE_TIEFE` statt gezählter `dirname`, fünf reguläre Ausdrücke repariert |
| 5. `<CORE_DIR>`, Platzhalterregister, `LINK_ROOTS_FEST` | 46 Träger; der Wert wird gebunden, nicht abgeleitet |
| 6. **Prüfung 75 und 76** gebaut | mit **vier Sonden und drei Gegenproben**, alle bestanden |
| 7. Laufzeit- und Overlayschicht des Framework-Repos | **45 Fundstellen in 7 Trägern** – `install.py --update` faßt sie nicht an (*„der vierte Träger, schon wieder"*) |
| 8. Beide übernehmenden Projekte | gehoben und migriert, je mit `--strict-overlay` |

## 4. Vorlage zur Entscheidung

> 🔴 **Vier Fragen. Zwei davon sind alte Klärungspunkte, eine ist durch die Lage neu
> entstanden, und eine ist auf berichtigter Prämisse neu gestellt worden.**

| Nr. | Frage | Entscheidung und **Preis** | Record |
|---|---|---|---|
| **E1** | **Wandern die Namen datierter Belegablagen außerhalb des Repositoriums mit?** | **Nein.** Sie sind Aufzeichnungen (D-141, D-273), und sie existieren unter diesem Namen. **Preis:** Die Belegablagen des Koolie-Frameworks tragen bis auf weiteres den alten Namen; der Wechsel gehört an einen Meßtag, der eine neue Reihe beginnt | **D-300** |
| **E2** | **Was geschieht mit den Aussagen ÜBER den alten Namen?** | **Vom Sweep ausnehmen, von Hand nacharbeiten** – acht Stellen maskiert, Wächter auf genau einen Treffer. **Preis, ein echter Verlust:** Die Namensmetapher der Wurzel-README (*„Ein Leitwerk fliegt das Flugzeug nicht"*) ist umgeschrieben; **das Bild bleibt, die Namensableitung entfällt.** `Koolie` trägt keine eigene, und eine erfundene wäre eine Behauptung | **D-301** |
| **E3** | **`D-275` hat seine Voraussetzung verloren – was gilt für den Vortrag am 24.09.?** | **Folien nachziehen, Rückfall-Belege nicht, und es im Vortrag sagen** – der ursprüngliche Vorschlag `E9` von `CR-2026-119`, der genau diese Lage voraussetzte. **Preis:** eine Nacharbeit am Foliensatz, und eine Station zeigt zwei Namen | **D-302** |
| **E4** | **`K-84`: Zwei Skills tragen eine unveränderte Version bei geändertem Text.** | **Abschnitt 7 wird nach EINGRIFFSART geschnitten:** Eine Versionsänderung öffnet die Zellen nur, wenn sie eine **Anweisung** berührt. **Preis, und er ist nicht maschinell prüfbar:** Die Grenze zieht ein Mensch – dieselbe Bauform wie `K-41` | **D-303** |
| **E5** | **`K-97`: Auf welchem Konto und Modell wird künftig gemessen?** | **Die Devin-Belege bleiben auf `SWE-1.6 Slow` eingefroren; ein Pro-Konto nur für NEUE Gegenstände, und jede Zeile nennt Client UND Modell.** ⚠️ **Der Mensch war zunächst für „alles neu messen" und hat nach der Klarstellung anders entschieden** – ein Modellwechsel stellt keine Vergleichbarkeit her, er fügt einen dritten Gegenstand hinzu. **Preis:** zwei Modellstände im Bestand, ausgewiesen statt vermischt | **D-304** |

### ⚠️ Eine Frage ist NICHT entschieden worden, und das ist Absicht

**Die 197 Träger mit geändertem Text tragen unveränderte Versionen.** Gehoben sind
**vier** – `08-skill-conventions.md` (der Eingriff selbst), `fw-mr-description`,
`fw-review-support` (der Nachtrag zu `K-84`) und `TEST_CATALOG.md` (die Sondenzahl).
**Alle übrigen Änderungen sind Namensanpassungen**, und D-303 nennt sie ausdrücklich
nicht als Anweisungsänderung. ⚠️ **Preis, benannt:** Das ist `K-84` in großem Maßstab –
nur daß die Alternative 197 Versionshebungen ohne Aussage wären. **Was den Stand trägt,
ist nicht die Versionszeile, sondern Prüfung 75.**

### 🔴 Ein Nachbarfund, gemeldet und NICHT geändert

**27 Klärungspunkte – `K-71` bis `K-98` – stehen in der Entscheidungstabelle** des
Decision Log statt in der Klärungstabelle. Sie rendern unter den Spaltenüberschriften
`ID | Entscheidung | Begründung | Alternativen | Status | Datum`, während sie
`Kennung | Frage | Relevanz | Auswirkung | Benötigte Information | Status` tragen.
**Gemessen: seit `0.66.0`, 32 Releases** (`git log -S`).

**Das ist D-264 an einer zweiten Stelle** – dieselbe Bauform, anderer Träger: Die
Buchführung zählt sie richtig (`check_klaerungsregister` findet sie), der Leser sieht
sie unter falschen Überschriften. **Prüfung 74 prüft nur die Fähigkeitsmatrizen.**

➡️ **Nach `FW-SC-01` gemeldet, nicht geändert.** Das ist **`K-100`**, und die Reparatur
ist eine Verschiebung von 27 Tabellenzeilen, die mit der Umbenennung nichts zu tun hat.

## 5. Wirkungsnachweis

- **Validator:** 0 Fehler, 0 Warnungen.
- **Sondenlauf:** **beide Kodierungsumgebungen**, je Exit 0, **424 Einheiten**, und der **zeilengleiche Vergleich nach D-49 zeigt 0 Unterschiede in 456 Zeilen**. 🔴 **Der erste Durchgang zeigte genau einen** – ein Umlaut im Beschreibungssatz einer neuen Gegenprobe (V12).
- **Prüfung 75** (Restbestand des alten Namens): ein Bündel mit fünf Einheiten an einem
  echten Repositorium – 🔴 **`kopie()` schließt `.git` aus, und ohne `git init` hätte die
  Prüfung in jeder Sonde ihren dritten Ausgang genommen** (*„nicht meßbar"*) und dabei
  ausgesehen wie eine, die nichts gefunden hat. Derselbe Griff wie bei Gegenstand 2 von
  Prüfung 45, aus demselben Grund.
- **Prüfung 76** (die Lage des Kerns): drei Sonden und eine Gegenprobe. **Die dritte
  Sonde legt die `basename`-Bindung wieder an** – ohne sie wäre „alle vier tragen
  denselben Wert" erfüllbar, indem alle vier denselben Fehler machen. *Genau das war der
  Zustand bis `0.87.0`.*
- 🟢 **Prüfung 75 hat sich bei ihrem ersten Lauf selbst gemeldet:** Das Sondenskript
  nennt den alten Namen viermal, weil sein Gegenstand der alte Name **ist**. Daraus ist
  eine vierte, strukturell unvermeidbare Ausnahmeklasse geworden – *eine Prüfung, die
  einen Namen sucht, muß ihn nennen; und ihre Sonde muß ihn schreiben.*

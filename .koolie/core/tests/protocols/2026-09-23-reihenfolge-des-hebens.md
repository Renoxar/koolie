# Protokoll: Die Reihenfolge des Hebens – ein Prüfpunkt und sein eigener Zeitpunkt

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-23 |
| Release | **`1.1.0`** |
| Änderungsantrag | `CR-2026-130` |
| Art | **Arbeitsprotokoll.** Gegenstand sind ein Prüfpunkt, ein Verfahren und der ausgelieferte Bestand zweier Projekte |
| Prüfmittel | `review` – Auszählung im Bestand, dazu der Validator in beiden übernehmenden Projekten |
| Ergebnis | 🟢 **Die offene Frage aus `1.0.1` ist beantwortet: ja zu beidem.** 🔴 **Und der Schuldposten war größer als gebucht – an drei Stellen statt an einer** |

> 🔴 **Dies ist kein Abnahmeprotokoll des Testkatalogs** und trägt deshalb keinen
> Abschnitt *Gegenzeichnung* (D-319, Zuschnitt von Prüfung 80). Es berichtet eine
> Messung und trägt seinen Beleg in sich.

---

## 1. Der Anlaß

Die Übergabe zu `1.0.1` hat einen Schuldposten gebucht und die Frage ausdrücklich offen
gelassen:

> ⚠️ *„Zu prüfen: Gehört das Heben vor den Release-Commit, und muß `RELEASE_PROCESS.md`
> Abschnitt 4.1 die Reihenfolge nennen? Heute sagt er sie nicht."*

**Anlaß war der zweite Fall in zwei Releases.** `1.0.0` hat die Bestandsliste angelegt,
und ihr erster Eintrag war zugleich ihr erster Befund: beide übernehmenden Projekte
standen **drei Releases** hinter `main`. `1.0.1` hat es wiederholt.

## 2. Der Vorbedingungsdurchgang – neunzehnmal in Folge der billigste Befund

Gemessen **vor dem ersten Handgriff**, elf Befunde. Die beiden, die diesen Posten
betreffen:

| # | Befund | gemessen an |
|---|---|---|
| **V7** | 🔴 Die Word-Fassung stand auf `v1.0.0`. `1.0.1` hat den Dokumentkopf auf `1.0.1` gehoben **und** `RELEASE_PROCESS.md` geändert – einen Träger, den `25-governance.md` einbettet | `build/out/` führte `Koolie_v1.0.0_*.docx`, keine Fassung `v1.0.1` |
| **V9** | 🔴 **Die Bestandsliste war an ZWEI Stellen falsch, nicht an einer** | siehe Abschnitt 3 |

## 3. Die Messung: die Liste wird an einer Stelle geführt und an zwei ausgeliefert

| Ort | `.koolie/core/VERSION` | Spalte `Framework-Version` der Bestandsliste |
|---|---|---|
| Framework-Repositorium | `1.0.1` | `1.0.1` ✅ – mit `1.0.1` nachgezogen |
| `devpacks/test-devin-framework` | `1.0.1` | 🔴 **`1.0.0`** |
| `devpacks/otp-generator` | `1.0.1` | 🔴 **`1.0.0`** |

**`1.0.1` hat die Liste an einer Stelle berichtigt und sie an zwei ausgeliefert.** Die
Berichtigung fiel **nach** dem Heben und erreichte die Kopien nicht mehr.

➡️ ***Wer eine Liste nach dem Heben fortschreibt, schreibt sie an einer Stelle fort und
liefert sie an zwei.***

🟢 **Das ist zugleich der gemessene Beleg, daß ein Verfahrensschritt allein hier nicht
getragen hätte:** Er stünde im Framework und wäre in beiden Installationen unbelegt.

## 4. Der Befund am Prüfpunkt selbst – er ist größer als der Schuldposten

Prüfpunkt 20 von `FW-CL-11` lautete:

> *„**MUSS** Release-Archiv erzeugt und abgelegt; übernehmende Projekte informiert."*

**Ein Haken, zwei Gegenstände** – und ihre frühesten möglichen Zeitpunkte liegen auf
entgegengesetzten Seiten des Release-Commits:

| Hälfte | frühestens | warum |
|---|---|---|
| Archiv erzeugt und abgelegt | **nach** dem Commit | 4.1 baut das Archiv aus der **Marke**, und die sitzt auf dem Release-Commit |
| Projekte informiert | **vor** dem Commit | die Quelle ist der Arbeitsbaum, und der trägt die neue `VERSION` bereits |

🔴 **Die Checkliste wird vor dem Release durchgegangen** – ihre eigene Kopfzeile sagt es.
**Die erste Hälfte konnte zu diesem Zeitpunkt noch nie erfüllt sein**, auch nicht in
`1.0.0`, dem Release, das das Archivverfahren eingeführt hat.

➡️ ***Ein Prüfpunkt, dessen eigenes Verfahren seine Erfüllung hinter den Zeitpunkt legt,
an dem er abgehakt wird, ist nicht unerfüllt – er ist falsch geschnitten.***

## 5. Warum das Heben vor den Commit gehört – und es ist nicht die Ordentlichkeit einer Liste

| Release | wann gehoben | was dabei herauskam |
|---|---|---|
| `1.0.0` | **vor** dem Abschluß | 🔴 **`B13` und `B14`** – Prüfung 78 und 79 aus `0.90.0` waren in **jeder** Installation rot. **Gefunden hat sie kein Validatorlauf, sondern das Heben** |
| `1.0.1` | **nach** dem Merge | 🔴 die Bestandsliste an zwei Stellen falsch |

➡️ ***Das Heben ist ein Lauf gegen eine fremde Installation, nicht die Fortschreibung
einer Tabelle.*** Wer es hinter den Merge legt, verlegt einen Prüfschritt hinter die
Freigabe, die er absichern soll.

## 6. Prüfung 82 – und die Gegenprobe, die man weglassen würde

Fünf Einheiten, gefahren am 2026-09-23:

| Art | Kennung | Gegenstand | Ergebnis |
|---|---|---|---|
| Gegenprobe | `82a` | der ausgelieferte Bestand läuft durch, und die Prüfung ist dabei nachweislich gelaufen | 🟢 |
| **Gegenprobe** | **`82b`** | 🔴 **die D-299-Probe:** ein übernehmendes Projekt, das Releases zurückliegt, muß **grün** sein – Liste und `VERSION` kommen byte-gleich aus demselben Release | 🟢 |
| Sonde | `82a` | eine Bestandszeile auf einem anderen Stand wird gemeldet, mit dem Projektnamen | 🟢 |
| Sonde | `82b` | der verlorene Anker (Spaltenüberschrift entfernt) wird gemeldet, statt leise zu bestehen | 🟢 |
| Sonde | `82c` | eine Tabelle ohne Datenzeile meldet eine Warnung und **kein** Meßergebnis | 🟢 |

🔴 **`82b` ist die, die man weglassen würde, und sie trägt den ganzen Zuschnitt.** Ohne
sie wäre die Installationsfestigkeit eine Behauptung im Kopfkommentar statt eine
gemessene Eigenschaft – und genau das hat `0.90.0` zweimal gekostet (D-326).

**Keine Einheit hält eine Versionsnummer wörtlich.** Sie lesen den Stand aus `VERSION`
und rechnen daran; eine Sonde, die einen Wert mitpflegen muß, fällt beim nächsten
Release aus, und zwar als scheinbarer Befund.

⚠️ **Grenze, benannt: Prüfung 82 mißt die Behauptung der Zeile, nicht den Stand des
Projekts.** Wer die Zeile ändert, ohne zu heben, kommt durch – dieselbe Bauform wie
Prüfung 77, die die *Version* des Hauptdokuments mißt und nicht seinen *Inhalt*.

## 7. 🔴 Zwei Befunde fielen erst beim Umsetzen

### 7.1 Das Werkzeug des Hebens war an den Commit gebunden (D-333)

Der eingespielte Ablauf hebt so:

> *„`rm -rf .koolie/core`, dann `git -C ../koolie archive HEAD .koolie/core | tar -x -C .`"*

und die Arbeitsanweisung sagt dazu wörtlich: *„für den echten Vorgang **nach dem Merge**
`git archive`"*.

🔴 **Das ist genau das, was D-330 ausschließt.** Vor dem Commit trägt `HEAD` das Release
noch nicht; ein so gehobenes Projekt bekäme den Stand von vorhin. **Zwei Regeln, die
einander die Voraussetzung entziehen** – die Bauform aus D-146 (`K-54`), hier an einem
Ablauf statt an einem Regeltext.

🟢 **Gemessen, und der Ersatz ist gleich groß:**

```
git ls-files -z .koolie/core | tar --null -T - -cf -   ->  519 Träger (Arbeitsbaum)
git archive HEAD .koolie/core                          ->  517 Träger (committet)

diff der beiden Mengen:
  + .koolie/core/governance/change-requests/CR-2026-130-reihenfolge-des-hebens.md
  + .koolie/core/tests/protocols/2026-09-23-reihenfolge-des-hebens.md
```

🔴 **Die Differenz sind genau der Änderungsantrag und das Protokoll dieses Releases.**
➡️ ***Wer vor dem Commit mit `git archive HEAD` hebt, liefert ein Projekt aus, dem der
Antrag und das Protokoll des Releases fehlen*** – der Beleg für D-333 in Reinform.
⚠️ **Nachgezählt im Durchgang vor dem Commit:** Beim ersten Messen lagen beide Verfahren
bei **517**, weil die neuen Träger noch nicht verfolgt waren. *Eine Zahl, die man an
einem Zwischenstand mißt, beschreibt den Zwischenstand.*

⚠️ **Die Beschränkung auf das Verfolgte ist nicht verzichtbar** – sie hält Bytecode und
`build/out/` draußen, und genau dafür stand `git archive` da.

### 7.2 Das Heben ist der LETZTE Eingriff in den Kern, nicht der erste (D-333)

🔴 **Unmittelbar nach dem ersten Durchlauf zugeschnappt.** Die **Overlay-Version** steht
erst **nach** dem Heben fest – sie ist eine Eigenschaft des Projekts, nicht des
Releases. Die Bestandsliste mußte deshalb noch einmal angefaßt werden, und danach trugen
beide Projekte einen Stand, den es nicht gibt.

➡️ ***Jede Änderung an `.koolie/core/**` nach dem Heben macht die Kopien wieder falsch.***

🟢 **Die Übergabe darf danach noch geschrieben werden** – sie liegt **außerhalb** des
Kerns (D-216) und wird in kein Projekt installiert. *Sie ist der einzige Träger des
Release-Commits, der das darf, und sie darf es nur deshalb.*

## 8. Das Heben, gefahren – und was es gekostet hat

| Projekt | Framework | Overlay | Validator `--strict-overlay` |
|---|---|---|---|
| `devpacks/otp-generator` | `1.0.1` → **`1.1.0`** | `0.3.2` → **`0.3.3`** | **1 Fehler, 2 Warnungen** – identisch mit dem Stand vor dem Heben. Der Fehler ist Projektarbeit (gesperrter Begriff in `CHANGELOG.md`) |
| `devpacks/test-devin-framework` | `1.0.1` → **`1.1.0`** | `1.0.1` → **`1.1.0`** | 🟢 **0 Fehler, 1 Warnung** – die Warnung ist `K-88` (Laufzeitfassung 6.023 von 6.000 Zeichen, SOLL) |

🟢 **Prüfung 82 ist in beiden Projekten grün.** Das ist der Nachweis, daß die
Reihenfolge trägt – und derselbe Lauf wäre vor diesem Release in beiden rot gewesen.

⚠️ **Der Overlay-Wert steht in DREI Trägern, und der Validator meldet sie
nacheinander.** Beim Piloten ist genau das eingetreten: Erst `OVERLAY.md`, dann das
Manifest, dann die Laufzeitfassung – drei Läufe für einen Vorgang. **Beim
Übungsrepositorium, wo alle drei gemeinsam gesetzt wurden, trat die zweite Meldung nie
auf.** *Die Lehre stand in der Arbeitsanweisung und ist trotzdem zugeschnappt.*

## 8a. 🔴 Ein dritter Befund fiel beim Setzen der Marke

**Der Antrag führte als `E7`:** *„`FW-CL-11` verlangt die dokumentierte Freigabe als MUSS
bei jedem Release; gemessen existiert sie **einmal**, für `1.0.0`. `1.0.1` hat keine."*

🔴 **Gesucht worden war in den Protokollen.** Beide vorhandenen Marken tragen sie:

```
v1.0.0   … Alle fuenf Kriterien aus D-11 erfuellt.
         Freigegeben durch den Framework Owner am 2026-09-23.
v1.0.1   … CR-2026-129, D-328.
         Freigegeben durch den Framework Owner am 2026-09-23.
```

und zwar **innerhalb der Signatur**. ➡️ ***Die Marke ist die Freigabe*** – und das
bestätigt D-334 an seinem eigenen Gegenstand: Der Commit trägt keine Unterschrift, die
**Marke** trägt sie.

🔴 **Was bleibt, ist ein anderer Befund: Kein Träger schreibt es vor.** Abschnitt 4.1
verlangte von der Markennachricht *„Release, Antrag und die Entscheidungen"* – die
Freigabe stand dort nicht, und `FW-CL-11` nannte keinen Ort. **Die beiden vorhandenen
Marken tragen sie aus Gewohnheit.**

⚠️ **Und die Gewohnheit war beinahe gebrochen.** Die für `1.1.0` vorbereitete
Markennachricht war **mehrzeilig** und nannte die Freigabe **nicht** – das Werkzeug hatte
die beiden vorhandenen Marken nicht gelesen, bevor es die dritte vorbereitete.
➡️ *Erst den Kopf des Trägers lesen, dann messen.* 🟢 **Gefangen, bevor die Marke stand.**

🟢 **Aufgelöst:** Abschnitt 4.1 Schritt 4 nennt die Freigabezeile als Pflichtbestandteil,
`FW-CL-11` nennt die Marke als ihren Ort. ⚠️ **Keine Prüfung kann das durchsetzen** – der
Markentext liegt im Tag-Objekt, nicht im Arbeitsbaum (`K-111`).

## 9. Was dieses Release nicht leistet

- **Prüfung 82 mißt die Behauptung, nicht die Tatsache** (D-331). Die Projekte liegen
  außerhalb des Repositoriums; eine Prüfung, die sie sucht, wäre auf jedem anderen
  Arbeitsplatz rot (D-299).
- **Keine Prüfung erreicht die Erzeugnisse der Lieferung** – Hauptdokument und
  Word-Fassung unter `build/out/`, das Archiv ganz außerhalb. Der Ersatz ist an beiden
  Stellen ein **Verfahrensschritt**, und damit schwächer (`K-110`).
- **Die Reihenfolge ist an EINEM Release erprobt**, nämlich diesem. Ob sie trägt, sagt
  das nächste.

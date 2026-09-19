# Testprotokoll – Das Prüfmittelwort, das keine Prüfung kennt, und der Bündelschnitt

| Feld | Inhalt |
|---|---|
| Gegenstand | Die **Vorbedingungen des ersten Testblatt-Bündels** (11 Zellen), das **Prüfmittelwort der dreizehn Testblätter** (87 Zellen) und der **Bündelschnitt** für die Posten `0.68.0` bis `~0.73.0`; dazu der Wirkungsnachweis der Prüfung 61 |
| Framework-Version | 0.67.0 (`CR-2026-092`) |
| Datum | 2026-09-19 |
| Prüfmethode | Durchgang gegen das Übungsrepositorium (`devpacks/test-devin-framework`) und gegen den eigenen Bestand, Umstellung, Sondenlauf in beiden Kodierungsumgebungen und zusätzlich mit `--bahnen 1`. **Ohne Kontingent** |
| Ergebnis | **Zehn von elf Vorbedingungen tragen.** Dazu drei Befunde außerhalb des Bündels: 87 von 87 Blattzellen mit einem Wort außerhalb des Vokabulars, **zwei Prüfungen ohne Gegenstand**, und ein Posten des Releaseplans, der seit 0.56.0 arithmetisch unerfüllbar war |

## 1. Der Durchgang vor dem Eingriff – zum zehnten Mal in Folge der billigste Befund

Der Releaseplan sah für `0.67.0` den ersten Bündellauf vor. Vor dem ersten Handgriff sind
die elf Zellen des ersten Bündels einzeln gegen den **heutigen** Stand des
Übungsrepositoriums gehalten worden – und beim Abzählen der Bündel ist der Durchgang auf
zwei Befunde gestoßen, die größer sind als das Bündel.

**Die elf Zellen und ihr Stand:** siehe `CR-2026-092` Abschnitt 5. Zehn tragen, eine
nicht (`SK-002-P01`, `K-72`).

🟢 **Ein Befund gegen die eigene Erwartung, und er entlastet:** Keiner der drei Skills des
Bündels führt einen Befehlsschlitz aus. Gemessen, nicht angenommen – die Frontmatter von
`fw-repo-analyze`, `fw-code-explain` und `fw-change-analyze` tragen kein
`Exec(<..._COMMAND>)`. Prüfung 60 hat in diesem Bündel keinen Gegenstand, und der Meßbaum
braucht keinen `allow`-Korb für einen Testbefehl. **Genau das macht Bündel 1 zum
billigsten ersten Meßtag** – und es ist der Grund für den Schnitt in D-180.

## 2. Der Befund: 87 von 87 Blattzellen tragen `manuell`

### 2.1 Die Zählung

```
--- dreizehn Testblätter (87 Zellen) ---
   73  manuell
   14  manuell + <Zusatz>
--- zentraler Katalog (38 Zellen) ---
   27  sitzung
    5  skript
    4  review
    1  sitzung + `validate-output.py`
    1  skript+sitzung
```

`tests/TEST_CATALOG.md` Punkt 3 kennt drei Wörter. **`manuell` ist keines davon** – es ist
das Adjektiv aus der Definition von `sitzung`, und jedes der dreizehn Blätter erklärte es
im eigenen Vorspann.

### 2.2 Die Wirkung – ausgezählt vor dem Eingriff

Zwei Prüfungen laufen über die dreizehn Blätter und filtern auf `sitzung`:

| Prüfung | Zeile im Validator | Zellen mit `sitzung` in den Blättern |
|---|---|---|
| 49 (D-146) | `if "sitzung" not in zellen[i_pm]: continue` | **0 von 87** |
| 60 (D-178) | dieselbe Zeile | **0 von 87** |

**Beide Prüfungen bauen ihre Dateiliste ausdrücklich aus den dreizehn Blättern auf** – sie
lesen sie, gehen jede Zeile durch und überspringen jede einzelne. Ein Lauf, der so endet,
ist von einem Lauf ohne Befund nicht zu unterscheiden.

### 2.3 Der Wirkungsnachweis: der Validatorlauf zwischen den beiden Eingriffen

🔴 **Dies ist der tragende Beleg des Releases.** Nach der Umstellung der 87 Zellen auf
`sitzung` und **vor** der Ergänzung der zwanzig Vorbedingungen:

```
FEHLER   leitwerk-core/framework/skills/fw-change-small/TESTS.md:7 … :13   (7 Zellen)
FEHLER   leitwerk-core/framework/skills/fw-refactor/TESTS.md:7 … :13       (7 Zellen)
FEHLER   leitwerk-core/framework/skills/fw-tests/TESTS.md:7 … :12          (6 Zellen)

Ergebnis: 20 Fehler, 0 Warnungen
```

**Zwanzig Zellen, drei Blätter, und in jedem dieser drei führt der Skill einen Befehl
aus.** Nach der Ergänzung: **0 Fehler, 0 Warnungen.**

## 3. Der zweite Befund: der Vorspann sagte „gesetzt"

Die Vorspänne der drei betroffenen Blätter nannten die Schlitze seit ihrer Erstfassung –
als Teil der Aufzählung *„aktives Übungs-Overlay (… `<TEST_COMMAND>`, `<LINT_COMMAND>` …
**gesetzt**)"*.

🔴 **Gesetzt waren sie auch am 2026-09-18**, als `FW-SC-01` zum dritten Mal nichts
geändert hat. Sie standen im `ask`-Korb, und `ask` ist im nicht-interaktiven Betrieb eine
Abweisung (D-134). **Eine Bindung ist keine Freigabe.** Die drei Vorspänne sagen das
seit diesem Release ausdrücklich, und jede der zwanzig Zellen nennt den Korb selbst
(D-182).

## 3.1 Der Durchgang vor dem Commit hat einen eigenen Fehler gefangen

🔴 **Die Tabelle zu `SK-002-P01` war im ersten Entwurf falsch belegt.** Sie führte
`isbn.ts` und `gebuehren.ts` als *unpräpariert* – gemessen sind sie **`UEB-13`**
(Duplikat innerhalb einer Datei) und **`UEB-15`** (zwei Duplikate mit unterschiedlicher
Randbedingung). Der Irrtum kam daher, daß der Durchgang die Präparationen aus dem
Register des Frameworks gelesen hat und dort die **Pfade des Beispielaufbaus** stehen;
die tatsächlichen Orte führt `tools/mentorenblatt/PRAEPARATIONEN.md` des
Übungsrepositoriums.

**Der Schluß trägt trotzdem – und er wird schärfer:** Von acht Modulen mit Tests ist
**genau eines frei** (`BookForm.tsx`), und es hat keinen Fehlerpfad. Es gibt im
Übungsrepositorium kein unpräpariertes Modul mit Tests und ungetestetem Fehlerpfad, und
zwar nicht, weil eines übersehen wurde, sondern weil der Bestand ausgeschöpft ist.

➡️ **Das ist die Lehre von 0.64.0 noch einmal:** *„Ein richtiger Schluß aus einem
falschen Beleg ist kein Glück, sondern eine ungesicherte Stelle."* Der Durchgang vor dem
Commit, der jede Zahl nachzählt, trägt sich damit **zum elften Mal in Folge**.

⚠️ **Und eine zweite Zelle ist davon berührt:** `SK-002-N01` wird auf `gebuehren.ts`
gefahren, und das Modul ist `UEB-15`. Die Präparation betrifft das Duplikatpaar, nicht
den ungeprüften Parameter – aber ein Lauf trifft beides, und die Zelle sagt es jetzt.

## 4. Der dritte Befund: vier Nummern für dreizehn Blätter

Der Posten lautete *„`0.67.0` bis `~0.70.0` – Die dreizehn Testblätter, je Bündel von zwei
bis drei Skills"*. Vier Nummern, dreizehn Blätter: Bei höchstens drei Blättern je Bündel
sind fünf Bündel nötig. **Prüfung 53 rechnet die Kriterium-2-Kette der Posten nach, nicht
den Inhalt eines Postens gegen seine eigene Nummernspanne.**

Der neue Schnitt und seine Kette stehen im Releaseplan; die Kette schließt und endet bei
null, Prüfung 53 bestätigt es:

```
0.66.0: … → 85
0.68.0: 85 → 74      0.69.0: 74 → 56      0.70.0: 56 → 38
0.71.0: 38 → 19      0.72.0: 19 →  4      0.73.0:  4 →  0
```

## 5. Prüfung 61 – der Wirkungsnachweis nach D-23

| Sonde / Gegenprobe | Was sie herstellt | Erwartet |
|---|---|---|
| **61a** | Katalogzeile mit dem Wort `manuell` | Meldung |
| **61b** | dieselbe Zeile in einem der dreizehn **Blätter** | Meldung |
| Gegenprobe **61a** | unveränderter Baum | keine Meldung |
| Gegenprobe **61b** | `sitzung + Skript …` | keine Meldung |
| Gegenprobe **61c** | `skript+sitzung` **und** `review` | keine Meldung |

🔴 **Gegenprobe 61c ist die wichtigste.** Ohne sie stünde nur fest, daß `sitzung`
durchkommt – ein Zuschnitt, der versehentlich auf `sitzung` verengt wäre, sähe genauso
aus. Das ist dieselbe Bewegung, aus der dieses Release überhaupt entstanden ist.

🔴 **Und die Sondenzeilen tragen `bestanden (Sondenbeleg)`, nicht `offen`** – eine Zeile
mit `offen` hebt Kriterium 2 um eins und lässt Prüfung 46 anschlagen (gemessen 2026-09-18,
`CR-2026-091`). Wer einen erlaubten Fall herstellt, muß ihn vollständig herstellen.

## 5.1 Der erste Abnahmelauf ist abgebrochen – und hat zwei Befunde geliefert (D-183)

Der erste Sondenlauf in der `cp1252`-Umgebung endete nach **53 von 61 Prüfungen** mit
einem `UnicodeEncodeError`. Die letzte Zeile davor:

```
SONDE      53a  FEHL  Ein Folgeposten, der unter dem Ende seines Vorgaengers beginnt,
                      wird gemeldet …  [Praeparation gebrochen]
Traceback (most recent call last):
  …
UnicodeEncodeError: 'charmap' codec can't encode character '\u2192' in position 70
```

**Befund 1 – der Anker.** `P53_KETTENGLIED` stand als feste Zeichenkette auf dem Inhalt
**eines** Postens des Releaseplans. Dieses Release macht aus dem einen Posten sieben.
🔴 **Dieselbe Bauform zum dritten Mal in drei Releases** – und die Abhilfe von `0.63.0`
stand **vier Zeilen entfernt**, an Gegenprobe 53b, mit einem Kopfkommentar, der den Fall
beschreibt. **Eine Abhilfe gilt für die Stelle, an der sie eingetragen wird, nicht für
die Bauform.** Beide Sonden leiten den Anker jetzt ab.

**Befund 2 – der Berichtsweg.** Die Meldung *„Präparation gebrochen“* nennt den
Suchtext, der nicht getroffen hat, und der trug ein `→`. **Der Abbruch hat acht
Prüfungen ungefahren gelassen und den Lauf unbrauchbar gemacht** – der Prüfapparat
konnte seinen eigenen Befund in genau der Umgebung nicht berichten, die D-49 verlangt.
Die Abhilfe steht in `Einheit.ausgeben()`: Dort geht jeder Text vorbei, der aus einem
Träger stammt. `Einheit.fahren()` fängt seit jeher jede Ausnahme der **Arbeit** – die
**Ausgabe** lag außerhalb.

## 6. Abnahme

| Lauf | Ergebnis |
|---|---|
| `validate-framework.py` gegen den fertigen Baum | 🟢 **0 Fehler, 0 Warnungen** |
| `probe-pruefungen.py`, Umgebung ohne `PYTHONIOENCODING` (`cp1252`) | 🟢 **alle Sonden und Gegenproben bestanden**, 233 Einheiten |
| `probe-pruefungen.py`, Umgebung mit `PYTHONIOENCODING=utf-8` | 🟢 **alle Sonden und Gegenproben bestanden**, 233 Einheiten |
| `probe-pruefungen.py --bahnen 1` (`K-71`) | 🟢 **alle Sonden und Gegenproben bestanden** |
| **Abnahmelauf gegen den fertigen Baum**, beide Kodierungsumgebungen | 🟢 **alle Sonden und Gegenproben bestanden**, je 233 Einheiten |

**Die neuen und die reparierten Einheiten, in allen drei Läufen grün:**

| Einheit | Was sie belegt |
|---|---|
| Sonde **61a** | Eine Katalogzeile mit `manuell` wird gemeldet |
| Sonde **61b** | Dasselbe Wort **in einem Blatt** wird gemeldet – die Prüfung liest beide Bestände |
| Gegenprobe **61a** | Der unveränderte Baum bleibt unbeanstandet – **alle 125 Zellen** (87 Blatt + 38 Katalog) tragen ein Wort des Vokabulars |
| Gegenprobe **61b** | `sitzung` mit Zusatz bleibt zulässig |
| Gegenprobe **61c** | `skript+sitzung` **und** `review` bleiben zulässig – der Zuschnitt ist nicht auf `sitzung` verengt |
| Sonden **53a**, **53b** | mit **abgeleitetem** Anker wieder fahrbar (D-183) |
| Gegenprobe **44a** | in allen drei Läufen grün – siehe Abschnitt 7.2 |

## 7. Ergebnisse der Abnahmeläufe

*(unterhalb der Trennlinie nach D-94: Die Läufe, die dieses Protokoll beschreibt, laufen
zwangsläufig ohne dieses Protokoll, und die Laufzeit ist nicht Teil des zeilengleichen
Vergleichs.)*

### 7.1 Laufzeiten

| Lauf | Rechenzeit | Wanduhr | Faktor |
|---|---|---|---|
| `cp1252`, 8 Bahnen | 2284,3 s | **286,9 s** | 8,0 |
| `utf-8`, 8 Bahnen | 2288,2 s | **292,3 s** | 7,8 |
| `utf-8`, **1 Bahn** | 2041,9 s | **2041,9 s** | 1,0 |
| **Abnahme, `cp1252`, 8 Bahnen** | 2304,8 s | **290,0 s** | 7,9 |
| **Abnahme, `utf-8`, 8 Bahnen** | 2414,6 s | **303,9 s** | 7,9 |

**Fünf Läufe, alle grün.** Die ersten drei sind gegen den Baum ohne dieses Protokoll
gefahren – die Läufe, die ein Protokoll beschreiben, laufen zwangsläufig ohne es. **Die
letzten beiden sind der Abnahmelauf gegen den FERTIGEN Baum**, also gegen denselben
Bestand, der committet wird, einschließlich dieses Protokolls, der `K-71`-Zeile des
Decision Logs und des Änderungsverzeichnisses. Ein grüner Validatorlauf ersetzt den
Sondenlauf nicht – und ein Sondenlauf gegen einen Zwischenstand ersetzt den gegen den
Endstand ebensowenig.

⚠️ **Der einbahnige Lauf ist in der Rechenzeit rund 11 % billiger** (2041,9 gegen 2284,3 s)
und in der Wanduhr das Siebenfache teurer. Der Aufschlag der acht Bahnen ist der Preis für
acht Kopien des Repositoriums und acht Unterprozesse; er ist gemessen und nicht geschätzt.

### 7.2 `K-71`: die Abweichung ist in drei weiteren Läufen nicht wieder aufgetreten

`K-71` verlangte ausdrücklich, *„denselben Lauf mit `--bahnen 1` zu wiederholen und, falls
er dann grün ist, die Nebenläufigkeit als Ursache einzugrenzen"*. Der Lauf ist gefahren und
grün.

🔴 **Er grenzt sie trotzdem nicht ein, und der Grund liegt in den beiden anderen Läufen:**
Auch die **achtbahnigen** sind grün, in beiden Kodierungsumgebungen. Eine Wechselwirkung
der acht Bahnen erklärt keine Abweichung, die bei acht Bahnen zweimal ausbleibt. **Der
einbahnige Lauf belegt damit weniger, als `K-71` sich von ihm versprochen hat** – und mehr
als nichts: Die verlangte Messung liegt vor, und ihr Ergebnis stützt die Hypothese nicht.

➡️ **Stand: einmal beobachtet, in vier Läufen nicht reproduziert** (der grüne Lauf vom
18.09. und die drei von heute). `K-71` bleibt offen, mit geändertem Vermerk — **eine nicht
reproduzierte Beobachtung wird nicht dadurch erklärt, daß man sie oft genug nicht
wiederholt.**

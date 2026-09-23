# Protokoll: Die Word-Fassung – und die drei Träger neben den Kapiteln, die keine Prüfung erreicht hat

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-23 |
| Release | `0.90.0` |
| Änderungsantrag | `CR-2026-125`, `CR-2026-126`; `CR-2026-127` **offen vorgelegt** |
| Art | Vorbedingungsdurchgang, Werkzeugberichtigung, zwei neue Prüfungen, erste Lizenzfestlegung, Berichtigung eigener Zahlen – **keine Sitzung, kein Kontingent, kein Modelllauf** |
| Umfang (gezählt am Release-Commit) | siehe Abschnitt 9 |
| Gegenstand | Der Rest von `AP11`: die Word-Fassung bauen; die Gegenzeichnung; dazu die drei Befunde am eigenen Release `0.89.0` |
| Ergebnis | 🟢 **Die Word-Fassung existiert – für beide Packs, mit acht eingebetteten Diagrammen.** 🔴 **Der Posten war nicht unfahrbar, sondern unversucht.** 🔴 **Drei Träger neben `build/doc/` erreichte keine einzige Prüfung.** 🆕 **Prüfung 78 und 79**, **D-313** bis **D-318**, `K-105` und `K-106` neu |

---

## 1. Der Vorbedingungsdurchgang – zum sechzehnten Mal in Folge der billigste Befund

**Er hat diesmal zwei Dinge gefunden, und keines davon war ein fehlendes Werkzeug.**

### 1.1 Die Vorbedingung war behebbar, nicht nur benennbar

`0.89.0` hat gemessen, daß `pandoc` und `mmdc` fehlen. **Die Messung war richtig.** Der
Releaseplan hat daraus gemacht: *„ohne sie ist der Posten unfahrbar."*

```text
$ command -v winget   →  v1.29.380
$ command -v npm      →  vorhanden (node v24.15.0)
$ ls "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"  →  vorhanden
```

| Schritt | Ergebnis |
|---|---|
| `winget install JohnMacFarlane.Pandoc` | 🟢 `pandoc 3.11` |
| `npm install -g @mermaid-js/mermaid-cli` | 🟢 `mmdc` vorhanden, 190 Pakete |
| Mermaid-Probelauf über das vorhandene Edge | 🟢 PNG geschrieben |

➡️ ***Eine fehlende Vorbedingung ist ein Posten, keine Grenze.*** Der Unterschied zwischen
*„nicht installiert"* und *„nicht installierbar"* ist der zwischen einer Messung und einer
Folgerung aus ihr – und die Folgerung stand zwei Releases lang im Plan.

### 1.2 🔴 Drei Träger neben den Kapiteln, und keine Prüfung erreicht sie

**Gemessen, indem der Iterator des Validators abgefragt wurde** (`iter_text_files`, gegen
den ausgelieferten Bestand):

```text
Träger insgesamt, die iter_text_files liefert: 582
davon unterhalb von build/: 34   (alle in build/doc)

.koolie/core/build/assemble.py:    NICHT ERREICHT
.koolie/core/build/build-docx.py:  NICHT ERREICHT
.koolie/core/build/README.md:      NICHT ERREICHT
```

`SKIP_DIRS` enthält den blanken Verzeichnisnamen `build`; `iter_text_files` holte genau
`build/doc` zurück. 🔴 **Zwölf Prüfungsfunktionen laufen über diesen Iterator** – gezählt
über den Syntaxbaum des Validators:

| Prüfung | Funktion |
|---|---|
| 6 (verbotene Inhalte), 7 (Platzhalter) | `check_content` |
| 12 (Querverweise) | `check_links` |
| 13 (Artefaktversionen) | `check_artefakt_versionen` |
| 14 (Clientname, zweiteilig) | `check_actor_naming`, `check_placeholder_naming` |
| 48 (Clientpfad) | `check_tool_neutrality` |
| 50 (Klärungsregister) | `check_klaerungsregister` |
| 58 (Entscheidungsregister) | `check_decisionregister` |
| 63 (Nummernverweise) | `check_nummernverweis` |
| 66 (verirrte Steuerzeichen) | `check_verirrtes_steuerzeichen` |
| 71 (Arbeitsplatzpfad) | `check_arbeitsplatzpfad` |
| (`--mermaid`) | `check_mermaid` |

🔴 **Die Begründung im Quelltext nennt genau EINE Frage** – die Werkzeuge führen eigene
Marker in spitzen Klammern, und das ist die Frage von **Prüfung 7**.

➡️ ***Eine Ausnahme gilt so weit wie ihre Begründung und nicht so weit wie ihr
Mechanismus.*** 🔴 **Das ist D-311 an einer zweiten Stelle:** dort eine Frist über zwei
Gegenstände, hier eine Ausnahme über zwei Fragen.

### 1.3 Der Preis der Öffnung, gemessen statt geschätzt

Der Iterator wurde probeweise erweitert und der **ganze** Validator gefahren:

```text
WARNUNG  Platzhalter (Wurzelmarker) nicht in PLACEHOLDER_REGISTRY.md (in build/assemble.py)
WARNUNG  Platzhalter (Versionsmarker) nicht in PLACEHOLDER_REGISTRY.md (in build/README.md)
FEHLER   build/build-docx.py:59: 'Devin' nennt ein Client-Produkt …
FEHLER   build/README.md:3: 'Devin' nennt ein Client-Produkt …

Ergebnis: 2 Fehler, 2 Warnungen
```

➡️ ***Eine Ausnahme über drei Träger und zwölf Prüfungen, gekauft für zwei Warnungen.***
Die zwei Warnungen **sind** die Begründung und haben jetzt eine eigene, benannte Ausnahme
bei der einen Frage, für die sie gilt (`OHNE_PLATZHALTERREGISTER`, D-313).

🔴 **Und die zwei Fehler standen im Erzeuger der Lieferung.** `build-docx.py` schrieb
`title=Framework für den professionellen Einsatz von Devin Desktop` in die
**Dokumenteigenschaften** der Word-Datei – ein Titel, den `00-kopf.md` seit `0.88.0` nicht
mehr trägt, mit einem **Clientnamen** darin.

---

## 2. 🔴 Der gefährlichste Befund fiel erst im Lauf: Exit 0 und keine Diagramme

Der erste Bau der Word-Fassung:

```text
Mermaid-Blöcke: 8
geschrieben: …\Koolie_v0.89.0.docx (0.9 MB)
pandoc-Warnungen: [WARNING] Could not fetch resource
  …\koolie.koolie\core\build\out\img\diagramm-01.png: does not exist
  Replacing image with description.
```

**Der Bildverweis trug den absoluten Pfad.** Unter Windows enthält der Rückstriche, und
pandoc liest einen Rückstrich in einem Markdown-Link als **Maskierung**: Aus
`…\koolie\.koolie\…` wurde `…koolie.koolie\…`.

🔴 **pandoc ersetzt ein nicht gefundenes Bild durch seine Beschreibung und endet mit
Exit 0.** Das Werkzeug meldete *„geschrieben"*, die Datei lag da – und **acht von acht
Diagrammen fehlten.** Die einzige Spur war eine Warnzeile, die niemand liest.

| | vorher | nachher |
|---|---|---|
| Größe | 0,9 MB | **1,9 MB** |
| Bilder in `word/media/` | **0** | **8**, einzeln nachgezählt |

🟢 **Behoben zweifach:** relativer Bildpfad gegen `--resource-path`, **und** der Lauf
bricht ab und löscht die Datei, wenn pandoc eine Ressource meldet.
➡️ ***Ein Erzeugnis, dem ein zugesagter Bestandteil fehlt, ist nicht erzeugt.***

---

## 3. Die Word-Fassung – gebaut, für beide Packs

| Lauf | Ergebnis |
|---|---|
| `assemble.py` (`devin-desktop`) | 🟢 1.956.225 Zeichen, 12.888 Zeilen |
| `build-docx.py` | 🟢 `Koolie_v0.89.0_devin-desktop.docx`, 1,9 MB, **8 Diagramme** |
| `assemble.py --client claude-code` | 🟢 1.959.896 Zeichen, 12.806 Zeilen |
| `build-docx.py` | 🟢 `Koolie_v0.89.0_claude-code.docx`, 1,9 MB, **8 Diagramme** |

**Nachgezählt im Erzeugnis, nicht der Meldung geglaubt:** acht Einträge unter
`word/media/`, und `docProps/core.xml` trägt
`dc:title = Koolie – Framework für den professionellen Einsatz von KI-Codierassistenten…`.

🔴 **Zwei Lieferungen trugen bis `0.89.0` denselben Dateinamen**, und die beiden Fassungen
sind nicht gleich. Das Pack steht jetzt im Namen (D-314).

---

## 4. 🔴 Drei Zahlen, überholt im Release, das das Dokument auf den Stand gesetzt hat

`26-qs-test.md` sagte: *„Der Validator führt **76 Prüfungen** über 502 versionierte Dateien
des Kerns, davon 450 Markdown-Dateien."*

| Angabe | gemessen zum Stand `0.89.0` | woher die Abweichung kommt |
|---|---|---|
| 76 Prüfungen | **77** | Prüfung 77 kam **mit** `0.89.0` |
| 502 versionierte Dateien | **504** | Antrag und Protokoll **desselben** Releases |
| 450 Markdown-Dateien | **452** | dieselben zwei |

Gegengeprüft an den Commits:

```text
e7f5df5 (0.88.1): 502 Dateien, 450 Markdown
bdb9d2b (0.89.0): 504 Dateien, 452 Markdown
```

🔴 **`0.89.0` hat den Grund selbst aufgeschrieben** – *„der Grund, warum die Behebung eine
PRUEFUNG braucht und nicht nur eine Textänderung"* – und dann Prüfung 77 gebaut, die die
**Version** mißt und nicht den **Inhalt**. *Ein Release später war der Satz wieder falsch.*
🟢 **Prüfung 78 schließt die Lücke** (D-315).

---

## 5. Die datierten Zahlen waren für ihr eigenes Datum falsch

`29-grenzen.md` und `32-abschluss.md` sagen *„Gezählt am 2026-09-22"* und nannten **308**
Decision Records und **101** Klärungspunkte bis `K-103`. An jenem Tag: **312**, **102**,
`K-104`.

🔴 **Beide Träger stehen seit D-311 in der Dauerausnahme** – Zeitdokument und Chronik,
ausdrücklich nicht fortgeschrieben. **Eine Prüfung darauf wäre falsch.** Sie sind einmal
richtiggestellt worden und bleiben stehen.
➡️ ***Wer eine Zahl datiert, schuldet sie für dieses Datum; wer sie in die Gegenwart setzt,
schuldet sie für immer – und braucht dafür eine Prüfung.*** (D-318)

⚠️ **Prüfung 50 hat dabei die Berichtigung selbst gefangen:** Der erste Entwurf nannte die
zusammengesetzte Sondenkennung **ausgeschrieben** in beiden Trägern – genau das, was der
Decision Log verbietet, weil sie gemeldet werden **soll**. *Die Berichtigung eines Befunds
über eine Kennung hat denselben Befund erzeugt, in der Gegenrichtung.*

---

## 6. Die drei Befunde am Release `0.89.0`

| # | Befund | Auflösung |
|---|---|---|
| a | Abnahmetabelle: 1.928.254 / 12.840 und 1.931.925 / 12.758 | 🔴 **Das war der Bau VOR der Textarbeit.** Gemessen am fertigen Baum: **1.956.225 / 12.888** und **1.959.896 / 12.806**. **Die Differenz ist für beide Packs dieselbe – +27.971 Zeichen, +48 Zeilen –, und genau das belegt, daß es ein und derselbe zu frühe Lauf war.** ➡️ *Eine Abnahmezahl gilt für den Baum, den sie abnimmt, und der entsteht zuletzt* |
| b | Feld „Art": *„Textarbeit an 32 Trägern"* | 🔴 **Ohne Zählregel.** Gemessen am Release-Commit: **36** geänderte Träger, **15** Kapitelquellen, **32** Textträger (36 minus drei Werkzeuge und `VERSION`). Die 32 hat einen Gegenstand – aber er stand nicht daneben, und dasselbe Release hat im Durchgang eine **andere** 32 als selbst erzeugt verworfen. *Eine Zahl ohne ihre Zählregel ist von einer geratenen nicht zu unterscheiden* |
| c | `UEBERGABE.md`: `K-96` als belegte synthetische Kennung | 🔴 **`K-96` ist eine echte, offene Registerzeile**, in **sieben** verfolgten Trägern genannt. Die Lücken sind 95 und 99. **Drei Träger, drei Mengen:** Decision Log **fünf**, Übergabe **sechs**, Prüfapparat setzt eine zusammen, die gerade **nicht** belegt sein darf. Der Satz widerlegte sich selbst – er nannte `K-96` und schrieb daneben, die Kennung sei zusammengesetzt. **Prüfung 50 meldet es nicht: Sie prüft GENANNTE Kennungen, nicht Behauptungen über die Menge** (`K-106`) |

---

## 7. Die Lizenz – die erste des Projekts

**GPL-3.0**, wörtlicher Text der Free Software Foundation, mit einer **Zusatzerlaubnis nach
§7** für Vorlagenergebnisse und Werkzeugausgaben (`CR-2026-126`, D-316).

🔴 **Die beiden Bedingungen des Owners schlossen einander aus** – *„echtes Open Source"* und
*„niemand darf den Kern verkaufen"*; §1 und §6 der OSI-Definition verbieten genau diese
Einschränkung. 🟢 **Die GPL löst den Widerspruch, ohne ihn zu verbieten:** Der Verkauf
bleibt erlaubt, aber jeder Käufer bekommt den Quelltext unter derselben Lizenz mit.

**Zwei Ablageorte, und Prüfung 79 hält sie gleich** (D-317): die Wurzel für die
Hostingdienste, der Kern, weil `ADOPTION_GUIDE.md` Schritt 2 ihn **als Ganzes** kopiert.

---

## 8. Die beiden neuen Prüfungen

| Einheit | Gegenstand | Ergebnis |
|---|---|---|
| Sonde `78a` | Zahl der Prüfungen verstellt | 🟢 gemeldet |
| Sonde `78b` | Zahl der versionierten Dateien verstellt | 🟢 gemeldet |
| Sonde `78c` | der Satz über den Prüfapparat entfernt | 🟢 verlorener Anker gemeldet |
| Gegenprobe `78a` | ausgelieferter Bestand | 🟢 läuft durch |
| Sonde `79a` | die beiden Lizenzdateien laufen auseinander | 🟢 gemeldet |
| Sonde `79b` | die mitwandernde Fassung im Kern fehlt | 🟢 gemeldet |
| Sonde `79c` | zwei gleiche Dateien **ohne** Lizenztext | 🟢 gemeldet |
| Gegenprobe `79a` | ausgelieferter Bestand | 🟢 läuft durch |

🔴 **Keine Sonde verankert eine Zahl wörtlich**, und das ist die Lehre von `0.89.0`: Dort
sind zwei Sonden gebrochen, weil sie einen Wert als Suchtext hielten, den das Release
berichtigt hat. Die Sonden zu 78 **lesen** die Zahl und verstellen sie relativ.

---

## 9. Der Durchgang vor dem Commit – zum fünfunddreißigsten Mal in Folge

| Zahl | zuerst genannt | nachgezählt |
|---|---|---|
| Vorbedingung des Postens | „unfahrbar" (Releaseplan) | 🔴 **behebbar** – beide Werkzeuge in zwei Befehlen installiert |
| Träger neben `build/doc` ohne Prüfung | – | 🟢 **drei**, und **zwölf** Prüfungen verlieren sie |
| Preis der Öffnung | – | 🟢 **2 Fehler, 2 Warnungen**, gemessen statt geschätzt |
| Diagramme in der ersten Word-Fassung | „geschrieben (0.9 MB)" | 🔴 **null von acht** – Exit 0, und nur eine Warnzeile |
| Abnahmezahlen von `0.89.0` | 1.928.254 / 12.840 | 🔴 **1.956.225 / 12.888** – der Bau vor der Textarbeit |
| „Textarbeit an 32 Trägern" | 32 | 🔴 **36 / 15 / 32** – die Zahl hat einen Gegenstand, aber keine Regel daneben |
| belegte synthetische Kennungen | „sechs, darunter `K-96`" | 🔴 **fünf**, und `K-96` ist eine echte, offene Zeile in sieben Trägern |
| Zahlen des Hauptdokuments | 76 / 502 / 450 | 🔴 **77 / 504 / 452** zum Stand `0.89.0` |
| datierte Zahlen | 308 / 101 / `K-103` | 🔴 **312 / 102 / `K-104`** – falsch für ihr **eigenes** Datum |
| offene Klärungspunkte | „13" (Übergabe) | 🔴 **nicht belastbar ermittelbar** – drei Zählungen, drei Ergebnisse (50, 64, 15 unerkannt). Das Register führt **104** Zeilen. Ursache: `K-100`, zwei Tabellenformen, kein Statusvokabular |
| Prüfungen | – | 🟢 **79** |

> 🔴 **Zwei der elf Zeilen sind eigene Zahlen dieses Hauses und in diesem Durchgang
> gefallen** – die Abnahmezahlen von `0.89.0` und die „32". ⚠️ **Und eine ist neu in ihrer
> Art:** *Eine Zahl, die man nicht ermitteln kann, ist kein fehlender Wert, sondern ein
> Befund über ihren Gegenstand.*

---

## 10. Abnahme

| Schritt | Ergebnis |
|---|---|
| `assemble.py` (`devin-desktop`) | 🟢 **gebaut** – 1.970.231 Zeichen, 12.897 Zeilen |
| `build-docx.py` (`devin-desktop`) | 🟢 **`Koolie_v0.90.0_devin-desktop.docx`**, 1.976.302 Bytes, **8 Diagramme** |
| `assemble.py --client claude-code` | 🟢 **gebaut** – 1.973.902 Zeichen, 12.815 Zeilen |
| `build-docx.py` (`claude-code`) | 🟢 **`Koolie_v0.90.0_claude-code.docx`**, 1.977.609 Bytes, **8 Diagramme** |
| `validate-framework.py --root .` | 🟢 **0 Fehler, 0 Warnungen** |
| `probe-pruefungen.py .` **ohne** `PYTHONIOENCODING` | 🟢 **Exit 0, alle Sonden und Gegenproben bestanden** – **436 Einheiten** (261 Sonden, 152 Gegenproben, 23 Selbstproben), 3.284,7 s Rechenzeit in **414,4 s** Wanduhr auf 8 Bahnen (Faktor 7,9) |
| `probe-pruefungen.py .` **mit** `PYTHONIOENCODING=utf-8` | 🟢 **Exit 0, alle bestanden** – dieselben 436 Einheiten, 3.310,5 s in **418,0 s** Wanduhr |
| Zeilengleicher Vergleich nach D-49 | 🟢 **0 Unterschiede in 468 Zeilen** oberhalb der Trennlinie. Der Auswertungsblock darunter trägt Namen und Laufzeiten und ist nach D-94 nicht Teil des Vergleichs |
| Zählung der Einheiten | 🔴 **Nachgezählt, nicht fortgeschrieben:** 261 + 152 + 23 = **436**. `0.89.0` meldete 428, und die acht neuen sind die Sonden `78a` bis `78c` und `79a` bis `79c` samt zwei Gegenproben. ⚠️ **Nicht zu verwechseln mit `--liste`**, das **316 Einheiten** meldet: Ein Bündel ist dort **eine** Einheit und liefert hier mehrere Ergebniszeilen |

🔴 **Der Bau gehört in den Abnahmelauf, und ab jetzt auch die Word-Fassung** – für beide
Packs. *Eine Prüfung bekommt er weiterhin nicht (`E2` von `CR-2026-124`); die Anweisung ist
alles, was ihn trägt.*

**Vier Durchgänge, und der vierte ist der Abnahmelauf.**

| Durchgang | Baum | Ergebnis |
|---|---|---|
| 1 | vor der Berichtigung zweier eigener Eingriffe | 🔴 **1 Abweichung** – Gegenprobe `46b` meldete *„Präparation gebrochen"*: Der neue Klärungspunkt `K-106` nannte die geschützte synthetische Kennung wörtlich, und der Kollisionswächter zählt jede Nennung außerhalb des schützenden Absatzes |
| 2 | nach der Berichtigung, vor dem Eintrag dieses Abschnitts | 🟢 Exit 0 in beiden Umgebungen, **468 Zeilen, 0 Unterschiede** |
| 3 | nach dem Eintrag dieses Abschnitts | 🟢 Exit 0, **468 Zeilen, 0 Unterschiede** – 3.390,7 s in 427,0 s Wanduhr |
| 4 | **Abnahmelauf** | 🟢 Exit 0 in beiden Umgebungen, **468 Zeilen, 0 Unterschiede**, 436 Einheiten – und **zeilengleich zum zweiten Durchgang**. 🟢 *Das belegt, was es belegen soll:* Die Ergänzungen zwischen Durchgang 2 und 4 waren Prosa in Trägern, auf die keine Sonde zugreift – und die Ausgabe ist Zeile für Zeile dieselbe |

🔴 **Und die Abweichung von Durchgang 1 ist selbst ein Befund – der zweite dieser Art in
diesem Release.** Zweimal hat der eigene Apparat den eigenen Eingriff gefangen: Prüfung 50
an der ausgeschriebenen Sondenkennung in zwei Kapitelquellen, Gegenprobe `46b` an der
Nennung in `K-106`. ➡️ *Wer über eine synthetische Kennung schreibt, vergibt sie.*

⚠️ **Die Laufzeiten dieser Tabelle sind nach dem Lauf eingetragen.** Sie stehen im
Sondenlauf **unterhalb** der Trennlinie und sind nach D-94 nicht Teil des zeilengleichen
Vergleichs – sonst änderte der Eintrag der Laufzeit die Endfassung, die er mißt.

---

## 11. Was **nicht** gefahren wurde, mit gemessenem Grund

| Posten | Warum nicht |
|---|---|
| **Gegenzeichnung der Protokolle** | 🔴 **Rollenfrage, kein Arbeitsposten.** An diesem Framework arbeitet eine Person; eine Gegenzeichnung ist die Handlung einer zweiten. Die drei Wege und ihre Preise sind als **`CR-2026-127`** vorgelegt und **ausdrücklich offen** gelassen. *Ein Antrag mit einem ausgefüllten Abschnitt 6, dessen Entscheidung niemand getroffen hat, ist die Fälschung, gegen die er selbst argumentiert* |
| **`K-100`** (27 Zeilen in der falschen Tabelle) | Beim Zählen gemessen: **teurer als gedacht.** Es braucht zusätzlich ein Statusvokabular, sonst bleibt die Zahl der offenen Punkte auch nach der Verschiebung unzählbar. Eigener Posten |
| **`M1→M2→M3→M4` auf dem Übungsrepositorium** | `SOLL` der Freigabecheckliste, braucht ein **Kontingent**. Gehört in den Freigabelauf und ist dort ausgewiesen |

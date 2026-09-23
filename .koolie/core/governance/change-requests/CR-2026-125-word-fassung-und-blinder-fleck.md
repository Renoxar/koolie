# Änderungsantrag `CR-2026-125`

| Feld | Inhalt |
|---|---|
| Titel | Der Rest von `AP11`: Die Word-Fassung – und die drei Träger neben den Kapiteln, die keine Prüfung erreicht hat |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-23 |
| Betroffene Artefakte | `.koolie/core/build/build-docx.py`; `.koolie/core/build/assemble.py`; `.koolie/core/build/README.md`; `.koolie/core/build/doc/26-qs-test.md`, `29-grenzen.md`, `32-abschluss.md`; `.koolie/core/tests/scripts/validate-framework.py` (**Prüfung 78**, Iterator, `OHNE_PLATZHALTERREGISTER`); `.koolie/core/tests/scripts/probe-pruefungen.py` (Bündel `sonden_dokumentzahlen`); `.koolie/core/tests/TEST_CATALOG.md`; `.koolie/core/tests/protocols/2026-09-22-hauptdokument-ap11.md` (Berichtigung); `.koolie/core/governance/DECISION_LOG.md` (**D-313** bis **D-315**, **D-318**, `K-105` und `K-106` neu); `.koolie/core/CHANGELOG.md`; `.koolie/core/VERSION`; `UEBERGABE.md`; `.koolie/core/tests/protocols/2026-09-23-word-fassung-und-blinder-fleck.md` |
| Ebene laut Entscheidungsbaum 6 | Core (Bauwerkzeuge, Prüfapparat, Dokumentquellen, Governance-Aufzeichnungen). Kein Projektwert, keine neue Verhaltensregel |
| Art | Änderung (Werkzeugberichtigung, eine neue Prüfung, eine Ausnahme neu zugeschnitten, Berichtigung eigener Zahlen) |
| Dringlichkeit | hoch. Die Word-Fassung ist **Bestandteil der Lieferung** und stand seit zwei Releases als Zusage da |

---

## 1. Anlass und Problem

### 1.1 Die Vorbedingung war behebbar, nicht nur benennbar

`0.89.0` hat die Word-Fassung nicht gebaut und den Grund gemessen aufgeschrieben:
*„`pandoc` und das Mermaid-Kommandozeilenwerkzeug sind auf diesem Arbeitsplatz nicht
installiert"*. **Die Messung war richtig, und die Folgerung ging einen Schritt zu weit.**
Der Releaseplan schrieb daraus *„ohne sie ist der Posten unfahrbar"*.

**Gemessen am 2026-09-23:** Beide Werkzeuge sind über die vorhandenen Paketverwalter des
Arbeitsplatzes beziehbar (`winget`, `npm` – beide vorhanden), und der Mermaid-Renderer
braucht keinen eigenen Chromium: Auf der Zielplattform liegt einer.

➡️ ***Eine fehlende Vorbedingung ist ein Posten, keine Grenze.*** Der Unterschied
zwischen *„nicht installiert"* und *„nicht installierbar"* ist genau der zwischen einer
Messung und einer Folgerung aus ihr.

### 1.2 🔴 Der Befund vor dem ersten Handgriff: drei Träger, die keine Prüfung erreicht

Vor dem ersten Lauf steht die Durchsicht der Vorbedingungen. Sie hat diesmal nicht ein
fehlendes Werkzeug gefunden, sondern einen **blinden Fleck des Prüfapparats**.

`SKIP_DIRS` des Validators enthält den blanken Verzeichnisnamen `build`. `iter_text_files`
holt daraus genau **einen** Unterbaum zurück:

```python
doc = os.path.join(root, KERN, "build", "doc")
if os.path.isdir(doc):
    yield from _walk_text_files(doc, ignoriert)
```

**Gemessen, indem der Iterator abgefragt wurde:**

| Träger | erreicht |
|---|---|
| die 34 Kapitelquellen unter `build/doc/` | 🟢 ja |
| `build/assemble.py` | 🔴 **nein** |
| `build/build-docx.py` | 🔴 **nein** |
| `build/README.md` | 🔴 **nein** |

🔴 **Zwölf Prüfungsfunktionen laufen über diesen Iterator** – unter ihnen Prüfung 6
(verbotene Inhalte), 12 (Querverweise), 13, 14 (Clientname), 48 (Clientpfad), 50, 58, 63,
66 und 71. **Alle zwölf verlieren dieselben drei Träger.**

🔴 **Die Begründung im Quelltext nennt genau EINE Frage:**

> *„Das Werkzeug daneben (`assemble.py`, `build/README.md`) bleibt aussen vor: Es fuehrt
> eigene Marker in spitzen Klammern, die keine Framework-Platzhalter sind."*

Das ist die Frage von **Prüfung 7**, dem Platzhalterregister. Sie rechtfertigt eine
Ausnahme bei einer Prüfung und wirkt auf zwölf.

➡️ ***Eine Ausnahme gilt so weit wie ihre Begründung und nicht so weit wie ihr
Mechanismus.*** 🔴 **Das ist D-311 an einer zweiten Stelle** – dort war es eine Frist über
zwei Gegenstände, hier eine Ausnahme über zwei Fragen.

### 1.3 Was hinter dem blinden Fleck lag – gemessen, nicht vermutet

Der Iterator wurde probeweise erweitert und der **ganze** Validator gefahren:

| Meldung | Bewertung |
|---|---|
| `build-docx.py:59` – *„'Devin' nennt ein Client-Produkt"* | 🔴 **Fehler.** Der Erzeuger der Word-Fassung stempelt den Dokumenttitel in die **Dokumenteigenschaften** der Lieferung – und der Titel nannte einen Clientnamen |
| `build/README.md:3` – dieselbe Meldung | 🔴 **Fehler.** Derselbe überholte Titel |
| der Wurzelmarker von `assemble.py` nicht im Platzhalterregister | ⚠️ Warnung – **das ist die Begründung der Ausnahme** |
| der Versionsmarker von `build/README.md` nicht im Platzhalterregister | ⚠️ Warnung – ebenso |

**Zwei Fehler, zwei Warnungen.** ➡️ *Eine Ausnahme über drei Träger und zwölf Prüfungen,
gekauft für zwei Warnungen.*

🔴 **Und der Titel war nicht nur unneutral, sondern überholt.** `00-kopf.md` sagt seit
`0.88.0`: *„Koolie – Framework für den professionellen Einsatz von KI-Codierassistenten in
Softwareentwicklungsteams"*. `build-docx.py` sagte *„Framework für den professionellen
Einsatz von Devin Desktop"*, dazu `subtitle=… Version 0.1.0` und `date=2026-09-02`.
**Prüfung 77 erreicht das nicht:** Sie mißt `00-kopf.md`, nicht den Erzeuger.

### 1.4 🔴 Der gefährlichste Befund fiel erst im Lauf: acht von acht Diagrammen, mit Exit 0

Der erste Bau der Word-Fassung auf diesem Arbeitsplatz endete mit:

```text
geschrieben: …\Koolie_v0.89.0.docx (0.9 MB)
pandoc-Warnungen (Auszug): [WARNING] Could not fetch resource
  …\koolie.koolie\core\build\out\img\diagramm-01.png: does not exist
  Replacing image with description.
```

Der Bildverweis trug den **absoluten** Pfad. Unter Windows enthält der Rückstriche, und
pandoc liest einen Rückstrich in einem Markdown-Link als **Maskierung**: Aus
`…\koolie\.koolie\…` wird `…koolie.koolie\…`, eine Datei, die es nicht gibt.

🔴 **pandoc ersetzt ein nicht gefundenes Bild durch seine Beschreibung und endet mit
Exit 0.** Das Werkzeug meldete *„geschrieben"*, die Datei lag da, und **kein einziges der
acht Diagramme war darin.** Die einzige Spur war eine Warnzeile.

➡️ ***Ein Erzeugnis, dem ein zugesagter Bestandteil fehlt, ist nicht erzeugt.*** Nach der
Behebung: **1,9 MB statt 0,9 MB, acht Bilder in `word/media/` nachgezählt.**

### 1.5 Zwei Lieferungen, ein Dateiname

Beide Client Packs schreiben nach `build/out/hauptdokument.md`, und beide Word-Fassungen
hießen `Koolie_v0.89.0.docx`. **Die beiden Fassungen sind nicht gleich:** 1.956.225 gegen
1.959.896 Zeichen. *Welche Lieferung man in der Hand hält, stand nirgends.*

### 1.6 🔴 Drei Zahlen, überholt im Release, das das Dokument auf den Stand gesetzt hat

`26-qs-test.md` sagte: *„Der Validator führt **76 Prüfungen** über 502 versionierte
Dateien des Kerns, davon 450 Markdown-Dateien."*

| Angabe | gemessen zum Stand `0.89.0` |
|---|---|
| 76 Prüfungen | **77** – Prüfung 77 ist mit `0.89.0` dazugekommen |
| 502 versionierte Dateien | **504** – die zwei neuen sind Antrag und Protokoll **desselben** Releases |
| 450 Markdown-Dateien | **452** – dieselben zwei |

🔴 **`0.89.0` hat den Grund selbst aufgeschrieben** – *„der Grund, warum die Behebung eine
PRUEFUNG braucht und nicht nur eine Textänderung"* – und dann **Prüfung 77** gebaut, die
die **Version** mißt und nicht den **Inhalt**. *Ein Release später war der Satz wieder
falsch.*

### 1.7 Die datierten Zahlen waren für ihr eigenes Datum falsch

`29-grenzen.md` und `32-abschluss.md` sagen beide *„Gezählt am 2026-09-22"* und nannten
**308** Decision Records und **101** Klärungspunkte bis `K-103`. An jenem Tag waren es
**312**, **102** und `K-104` – vergeben von demselben Release.

🔴 **Das ist keine veraltete Zahl, sondern eine falsche.** Beide Träger stehen seit D-311
in der Dauerausnahme als Zeitdokument und Chronik; sie werden ausdrücklich **nicht**
fortgeschrieben. *Eine datierte Zahl veraltet nicht – sie muß nur für ihr Datum stimmen.*

### 1.8 Drei Befunde am Release `0.89.0` selbst

| # | Träger | Befund |
|---|---|---|
| a | Protokoll `0.89.0`, Abnahmetabelle | Nennt 1.928.254 / 12.840 und 1.931.925 / 12.758. **Gemessen am fertigen Baum: 1.956.225 / 12.888 und 1.959.896 / 12.806.** Die Differenz ist für beide Packs **dieselbe** – +27.971 Zeichen, +48 Zeilen –, und genau das belegt, daß es ein und derselbe **zu frühe** Lauf war: der Bau **vor** der Textarbeit |
| b | Dasselbe Protokoll, Feld „Art" | *„Textarbeit an 32 Trägern"* – **ohne Zählregel**. Gemessen am Release-Commit: **36** geänderte Träger, davon **15** Kapitelquellen und **32** Textträger (36 minus drei Werkzeuge und `VERSION`). Die 32 hat einen Gegenstand, aber er stand nicht daneben – und dasselbe Release hat im Durchgang vor dem Commit eine **andere** 32 als selbst erzeugt verworfen |
| c | `UEBERGABE.md` | Führte `K-96` als *„belegte synthetische Kennung"*. **Gemessen: `K-96` ist eine echte, offene Registerzeile in sieben verfolgten Trägern.** Die Lücken sind 95 und 99. Der Decision Log deklariert **fünf** Kennungen; die Übergabe führte **sechs**; der Prüfapparat setzt eine sechste zusammen, die gerade **nicht** belegt sein darf. **Drei Träger, drei Mengen.** Der Satz widerlegte sich selbst: Er nannte `K-96` und schrieb daneben, die Kennung sei `"K-" + "95"` zusammengesetzt |

---

## 2. Vorschlag

1. **Die Vorbedingungen herstellen** und die Word-Fassung für **beide** Packs bauen.
2. **Den Iterator öffnen** und die Ausnahme auf ihre Begründung zuschneiden.
3. **`build-docx.py` berichtigen**: Metadaten aus dem Dokument, Browser selbst suchen,
   relative Bildpfade, Abbruch bei nicht geholter Ressource, Pack im Namen der Lieferung.
4. **Prüfung 78** für die Gegenwartszahlen des Hauptdokuments.
5. **Die datierten Zahlen einmal richtigstellen** und den Zuschnitt aufschreiben.
6. **Die drei Befunde an `0.89.0`** berichtigen.

---

## 3. Auswirkungen

| Gegenstand | Wirkung |
|---|---|
| Lieferung | 🟢 Die Word-Fassung existiert – zum ersten Mal seit `0.9.0`, und zum ersten Mal überhaupt für beide Packs getrennt |
| Prüfapparat | 🟢 79 Prüfungen; zwölf Prüfungen sehen drei Träger mehr |
| Übernehmende Projekte | keine Migration. `build/` wird nicht ausgeliefert |
| Kontingent | **keins.** Kein Modelllauf, keine Sitzung |

---

## 4. Vorlage zur Entscheidung

| # | Frage | Auflösung und Preis |
|---|---|---|
| **E1** | **Wird der Iterator geöffnet – und wie weit?** | **Ja, und nur so weit wie nötig.** `<CORE_DIR>/build/` ohne `out/`; die Platzhalterfrage bekommt eine **benannte** Ausnahme über **drei benannte Träger** (`OHNE_PLATZHALTERREGISTER`). *Verworfen: die beiden Marker ins Platzhalterregister aufzunehmen* – sie sind keine Framework-Platzhalter, und ein Register, das Fremdes führt, damit eine Warnung schweigt, ist keins mehr. ⚠️ **Preis, benannt:** `out/` bleibt ungeprüft – es ist ein Erzeugnis und in einer frischen Auscheckung nicht da |
| **E2** | **Woher nimmt die Word-Fassung ihre Metadaten?** | **Aus dem Dokument.** *Verworfen: sie zu berichtigen* – sie wären beim nächsten Release wieder falsch; wer sie aus `00-kopf.md` liest, **erbt Prüfung 77** |
| **E3** | **Was tut der Bau, wenn pandoc eine Ressource nicht holt?** | **Er bricht ab und löscht die Datei.** *Verworfen: die Warnzeile stehenzulassen* – genau so sind acht von acht Diagrammen mit Exit 0 aus der Lieferung gefallen |
| **E4** | **Wie werden die zwei Lieferungen unterscheidbar?** | **Das Pack steht im Namen der Word-Datei**, über eine Marke, die `assemble.py` daneben schreibt. *Verworfen: das Markdown-Erzeugnis umzubenennen* – Chronik und Entscheidungen nennen es, und ein Erzeugnis umzubenennen macht aus richtigen Verweisen tote |
| **E5** | **Bekommen die Zahlen des Hauptdokuments eine Prüfung?** | **Ja, Prüfung 78**, nach der Bauform von Prüfung 40: den Satz ausrechnen, wörtlich verlangen. ⚠️ **Preis, benannt und nicht klein:** Die Zahl der versionierten Dateien steht erst fest, **wenn das Release fertig ist**. *Und eine Zahl, die niemand vor dem Ende setzen kann, ist genau die, die niemand setzt* |
| **E6** | **Werden auch die datierten Zahlen geprüft?** | **Nein** (D-318). Sie stehen in ausgewiesenen Zeitdokumenten; eine Prüfung, die deren Fortschreibung verlangt, hat ihren Zweck nicht verstanden. **Sie werden einmal richtiggestellt** – sie waren für ihr eigenes Datum falsch, und das ist kein historischer Zustand, sondern ein Fehler |
| **E7** | **Wird `K-100` in diesem Release behoben?** | **Nein, und der Grund ist gemessen.** Beim Zählen der offenen Klärungspunkte sind **drei Zählungen mit drei Ergebnissen** entstanden (50, 64, 15 nicht erkennbar), weil die K-Zeilen in **zwei** Tabellenformen stehen und die Statuswerte keinem Vokabular folgen. **`K-100` ist damit teurer als eine Verschiebung von 27 Zeilen** – es braucht zusätzlich ein Statusvokabular, wie Prüfung 47 es für die Steckbriefe hat. Eigener Posten |

---

## 5. Abnahme

`validate-framework.py --root .` ohne Fehler; Sondenlauf in **beiden** Kodierungsumgebungen
mit zeilengleichem Vergleich nach D-49; **der Bau des Hauptdokuments und der Word-Fassung
für beide Client Packs.**

---

## 6. Entscheidung

**Entschieden am 2026-09-23 durch `<FRAMEWORK_OWNER>`:** E1 bis E7 wie vorgeschlagen.
Festgehalten als **D-313** bis **D-315** und **D-318**; `K-105` und `K-106` neu
aufgenommen. Umgesetzt mit Release `0.90.0`.

# Änderungsantrag `CR-2026-110`

| Feld | Inhalt |
|---|---|
| Titel | Der Vorbedingungsdurchgang des Nachlaufs – der Meßapparat schrieb ins Repositorium, drei Wächter hatten drei Sollwerte, und eine normative Kernregel war seit acht Releases nicht gelesen worden |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-20 |
| Betroffene Artefakte | `tests/erhebungen/` (`ablage.py` **neu**, elf Skripte geändert), `tests/scripts/validate-framework.py` (**Prüfung 69**), `tests/scripts/probe-pruefungen.py` (vier Einheiten), `tests/TEST_CATALOG.md`, `governance/DECISION_LOG.md` (**D-224** bis **D-228** neu, `K-83` entschieden, `K-84` neu, `K-82` berichtigt), `framework/skills/fw-review-support/TESTS.md` und `fw-mr-description/TESTS.md` (je eine Ergebniszelle **geöffnet**, kein Versionsheben – D-119), `onboarding/exercises/README.md` (`UEB-29` gebaut), `tests/protocols/2026-09-20-vorbedingungen-nachlauf-b4.md` (neu), `docs/ROADMAP.md`, `CHANGELOG.md`, `VERSION`, `UEBERGABE.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind der Prüfapparat, der Meßapparat und zwei Ergebniszellen |
| Art | Vorbedingungsdurchgang vor einem bezahlten Meßtag – **kein Kontingent, kein Lauf am Client** |
| Dringlichkeit | **Regulär**, unmittelbar vor dem Nachlauf (`K-82`) |

## 1. Anlass

Der Nachlauf von Bündel 4 ist der nächste Schritt und der erste Posten seit dem Meßtag,
der wieder Kontingent kostet. **Bei den letzten neunzehn Durchgängen in Folge fiel der
billigste Befund vor dem ersten Lauf.** Dieser Durchgang hat **sieben** ergeben, und
keiner von ihnen hat etwas gekostet.

### 🔴 Befund 1: Der Meßapparat schreibt seit D-222 ins Repositorium

D-222 hat die Skripte mit `0.79.0` in den Kern geholt und ihre Belege ausdrücklich
draußen gelassen. **Fünf Skripte legten ihre Belege aber neben sich ab:**

```
BELEGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "belege")
```

Solange sie daneben lagen, war das richtig. **Seit dem Umzug zeigt derselbe Ausdruck
hinein** – dazu zwei Skripte für die Prompts (`<CORE_DIR>/tests/prompts/`) und zwei für
die Zustandsaufnahmen. `lauf.py` legt das Verzeichnis selbst an, ohne zu fragen.

Der Nachlauf hätte **44 Belegdateien samt Sitzungsmitschriften mit Werkzeugeingaben**
versioniert – genau das, was D-222 vier Wochen zuvor verworfen hat, und **ohne daß
jemand es entschieden hätte.**

> *Wer einen Apparat umzieht, zieht seine relativen Pfade mit um – oder er verschiebt
> ihr Ziel, ohne es zu merken.*

### 🔴 Befund 2: Drei Wächter derselben Vorbedingung, drei Sollwerte, keiner stimmte

| Skript | Sollwert im Quelltext |
|---|---|
| `umgebungen-bauen-b4.py` | `0.78.0` |
| `baeume-b4.py` | `0.78.0` |
| `historie-bauen-b4.py` | `0.77.0` |

**Das Übungsrepositorium stand auf `0.78.2`, der Kern auf `0.79.1`.** Die beiden
Wächter im normalen Pfad hätten abgebrochen – richtig, aber gegen den falschen
Sollwert. Der dritte wäre nie befragt worden, weil `baeume-b4.py` seinen Wert
durchreicht: **ein Sollwert, der nur in einer unbenutzten Voreinstellung steht, ist
eine Falle für den nächsten, der das Skript einzeln aufruft.**

### 🔴 Befund 3: `K-83` war längst entschieden – das Werkzeug kannte es nur im Kommentar

D-120 schließt mit dem Satz *„Für Fund-Testfälle bleibt die erste Form nach D-116 die
einzige zulässige."* `auswerten-b4.py` führte die Unterscheidung in seinem
Kopfkommentar und druckte `W` und `T` für alle neunzehn Zellen gleich. Der gemessene
Fall (`SK-012-P01`: Probe grün, keine der beiden Dateien geöffnet) ist damit **kein
Grund für eine Ausnahmemenge**, sondern der Beleg, daß eine entschiedene Regel nicht im
Code stand.

### 🔴 Befund 4: Eine Versionsänderung öffnet die Zellen ihres Testblatts

`08-skill-conventions.md` Abschnitt 7, normativ: *„Jede Versionsänderung erfordert die
erneute Ausführung der Testfälle in `TESTS.md`."*

**`0.79.0` hat `fw-review-support` auf `0.1.6` und `fw-mr-description` auf `0.1.5`
gehoben – in demselben Commit, der `SK-010-P02` und `SK-012-N04` abgenommen hat.** Die
Läufe fanden gegen `0.1.5` und `0.1.4` statt.

🔴 **Und der Befund reicht weiter als Bündel 4.** Gemessen gegen die Git-Historie in
**Commit**-Auflösung – die Tagesauflösung trennt ihn nicht, weil Lauf und Anhebung in
demselben Release liegen:

| Lage | Skills | bestandene Zellen |
|---|---|---|
| Version **nach** dem Protokoll gehoben | `fw-repo-analyze`, `fw-tests` | 11 |
| Version im **selben Commit** wie das Protokoll | `fw-bugfix-prepare`, `fw-change-analyze`, `fw-code-explain`, `fw-plan`, `fw-mr-description`, `fw-review-support` | 24 |
| Version **vor** der Messung (in Ordnung) | `fw-change-small`, `fw-docs-update`, `fw-error-analyze`, `fw-refactor`, `fw-tests`¹ | – |

¹ `fw-tests` erscheint in zwei Zeilen, weil seine bestandenen Zellen auf mehrere
Protokolle verweisen; gewertet ist die schärfere Lage.

**Acht von dreizehn Skills, zusammen 35 bestandene Zellen.** Wörtlich angewandt ginge
Kriterium 2 nicht auf 32, sondern auf rund **63**.

🔴 **Die Bauform sieht jedesmal wie Sorgfalt aus:** Ein Meßtag findet einen Mangel am
Skill, das Release behebt ihn und hebt die Version – und macht damit die Abnahme
ungültig, die es im selben Zug einträgt. **D-119 hat genau diesen Kreis für die
Gegenrichtung schon benannt** und ihn nur für das *Eintragen* aufgelöst, nicht für das
*Beheben*.

### 🔴 Befund 5: Die Berührungsprobe von `SK-010-N04` verlangt, was D-219 verboten hat

Ihre beiden Marken waren die Namen der zwei Übungs-Branches. **Seit `0.79.0` darf der
Skill Branchnamen nicht auflisten** – die Berechtigungsdatei sperrt jede Form von `git
branch` über ein Präfix. Eine Probe, die verlangt, was die geprüfte Schranke verbietet,
kann nur rot sein.

### 🔴 Befund 6: Die Zahlen von `K-82` stimmten nicht

| Angabe in `K-82` | gemessen am 2026-09-20 |
|---|---|
| Kriterium 2 steht bei **31** | `zaehlen46.py`: **30** |
| **sieben** abgenommene Zellen | **acht** (sechs `SK-011`, dazu `SK-010-P02` und `SK-012-N04`) |
| **zwölf** ungemessene Zellen | **elf** |
| **24 Läufe** – *„zehn Zellen …, zwei davon mit zweitem Turn"* | **keine** der elf gehört zu `fw-docs-update`, und nur dieser Skill schreibt: **keine hat einen zweiten Turn**; 11 × 2 = **22** |

### 🔴 Befund 7: Zwei Zähler desselben Bestands sagten Verschiedenes

Gefunden beim **Trockenlauf des Apparats**, der zu diesem Durchgang gehört. Die
Gegenzählung von `baeume_loeschen.py` meldete

```
node_modules vorher:  9798 Dateien / 101089284 Bytes
node_modules nachher: 9798 Dateien / 101089284 Bytes
🟢 geteilter Bestand unberuehrt
```

– **ein Byte mehr** als die 101 089 283, die `0.79.1` und die Übergabe als *den*
Bestand führen. Verursacher: `node_modules/.vite/vitest/results.json`. **Das
Prüfmittel schreibt in den geteilten Bestand**, und `umgebungen-bauen-b4.py` fährt es
vor jedem Meßtag im Meßbaum.

🔴 **`node-waechter.py` kennt das seit seinem Bau** und weist `.vite`, `.cache` und
`.tmp` gesondert aus; `baeume_loeschen.py` zählte roh. **Der Beleg des Aufräumens hing
am unschärferen der beiden Zähler.**

🔴 **Und am Meßtag hätte der Wächter angeschlagen, wo nichts geschehen ist:**
`<TEST_COMMAND>` steht im `allow`-Korb des Meßbaums, also darf **jeder** Lauf das
Prüfmittel starten – und zwischen *vorher* und *nachher* von `node-waechter.py` liegt
die ganze Meßreihe.

> ➡️ *Ein Wächter über einen geteilten Bestand muß wissen, wer außer dem Prüfling noch
> hineinschreibt.*

## 2. Was gemessen wurde, bevor entschieden wurde

- **Trockenlauf des Hebens** an einer Kopie des Übungsrepositoriums mit dem
  `leitwerk-core` von `HEAD`: `install.py --update --dry-run` meldet **0 angelegt, 7
  aktualisiert, 57 unverändert, 20 Projektdateien behalten** – die sieben sind
  ausschließlich die Träger der drei gemessenen Skills. `--strict-overlay` danach:
  **genau ein** Fehler, die kompatible Framework-Version.
- **Wirkungsnachweis zu D-224 als Paar:** `LW_ERHEBUNG` auf
  `…/leitwerk-core/tests/erhebungen/belege` → Abbruch mit Begründung; auf das
  Geschwisterverzeichnis `…/leitwerk-erhebungen-2026-09-20-b4n` → Ablage aufgelöst.
  **Der zweite Fall ist der eigentliche:** Ein Präfixvergleich auf der Zeichenkette
  hätte ihn als Kind von `…/leitwerk` gelesen.
- **Wirkungsnachweis zu D-226 an den 50 Belegen des Meßtags, ohne einen neuen Lauf:**
  Die Probe meldet den Hauptlauf von `SK-012-P01` rot, dazu zehn der zwölf ungemessenen
  Zellen. *Sie hätte D-218 aus den Belegen abgelesen.* **Sieben der acht abgenommenen
  Zellen bleiben grün**; die achte ist `SK-012-N04`, die nach D-227 ohnehin nachfährt.
- **Die drei Sonden und die Gegenprobe zu Prüfung 69** laufen (`69a` bis `69c`, `69a`).
- **Wirkungsnachweis zu D-228 als Paar am selben Gegenstand:** Vorstand `9798 Dateien / 101 089 284 Bytes` (wandert mit jedem Testlauf), behobener Stand `9797 Dateien / 101 088 634 Bytes, dazu 1 Zwischenstandsdatei` – stabil, und der Zwischenstand steht daneben statt darin.

## 3. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Wohin schreibt ein Meßapparat, der im Repositorium liegt?** | **Daneben, und der Ort wird gesagt:** `LW_ERHEBUNG`. Ohne die Angabe bricht jedes Skript ab, das eine Belegablage braucht; ein Pfad **im** Repositorium wird abgewiesen. **Prüfung 69** meldet jede Datei, die dort dennoch liegt | **Verworfen: ein Standardwert im Quelltext** – *eine Zahl, die gepflegt werden muß, wird nicht gepflegt* (D-153), und die drei `--erwarte`-Werte desselben Apparats haben es im selben Durchgang vorgeführt. **Verworfen: nur die Prüfung ohne den Wächter** – sie sieht erst, was schon geschrieben **ist**; die zweite Hälfte gehört davor, dieselbe Aufteilung wie bei D-205 zwischen Schnitt und Wächter. **Preis, benannt:** Jeder Aufruf braucht die Umgebungsvariable, und wer sie vergißt, bekommt einen Abbruch statt eines Laufs |
| **E2** | **Wird der Sollwert der Vorbedingung gepflegt oder abgeleitet?** | **Abgeleitet:** Sollstand ist die Version **dieses** Kerns (`ablage.kernversion()`). `--erwarte` bleibt als Übersteuerung | **Verworfen: die drei Werte gleichzuziehen** – dieselbe Pflege mit einem Zwischenschritt mehr, und sie lag an drei von drei Stellen daneben. **Verworfen: den Wert aus dem Übungsrepositorium nehmen** – dann prüfte der Wächter den Meßbaum gegen sich selbst (*die Null durch Konstruktion*, 0.59.1). 🟢 **Nebenwirkung, gewollt:** Der abgeleitete Wert beantwortet die erste Frage jedes Vorbedingungsdurchgangs – *hat ein Release den Gegenstand der Messung angefaßt?* – von selbst |
| **E3** | **Bekommt die Textform der Berührungsprobe eine Ausnahmemenge (`K-83`)?** | **Nein.** D-120 hat die Frage entschieden; die Gattung steht jetzt **je Marke** im Code, und das Urteil steht **je Lauf**. `K-83` Frage (3) entfällt damit | **Verworfen: die Ausnahmemenge** – sie bräuchte eine Antwort darauf, wer die übergebenen Grundlagen zählt (der Prompt ist maschinenlesbar, die genannten Dokumente sind es nicht), und sie ersetzte eine entschiedene Regel durch eine Heuristik. **Verworfen: die Gattung je Zelle** – `SK-010-N02` trägt beide in einer Zelle. 🔴 **Und die Umstellung hat sofort ihren eigenen zweiten Befund geliefert:** Je Turn geurteilt wäre `SK-011-N03` rot, weil der erste Turn `Generator` nennt und der zweite nicht – **eine abgenommene Zelle, ohne daß ein Lauf etwas versäumt hätte** (dritter Teil von D-218 an neuer Stelle) |
| **E4** | **Was folgt aus der Versionsnorm für die beiden abgenommenen Zellen?** | **Die Norm gilt wörtlich:** `SK-010-P02` und `SK-012-N04` gehen auf `offen` und fahren im Nachlauf mit. **Kriterium 2: 30 → 32.** Die Reichweite über Bündel 4 hinaus wird **nicht** hier entschieden, sondern als `K-84` geführt | **Verworfen: eine Ausnahme im Einzelfall** mit dem Diff als Beleg (der Diff berührt genau drei Stellen, und keine ist der Gegenstand der beiden Zellen) – dann ruhte eine Abnahme auf einer Auslegung, und die Norm bliebe unverändert daneben stehen. **Verworfen: die Norm zu präzisieren** – das ist die allgemeine Form derselben Auslegung, sie trifft **acht von dreizehn** Skills, und eine normative Kernregel wird nicht nebenbei in einem Vorbedingungsdurchgang geändert. **Preis, benannt:** vier zusätzliche Läufe, rund 4,90 USD – und **der erste Aufwärtsschritt in einer neun Schritte langen monotonen Kette.** ⚠️ *Ein Zähler, der nur fallen kann, sagt nichts darüber, ob seine Nullen noch gelten* |
| **E5** | **Wird `UEB-29` vor dem Nachlauf gebaut (`K-82` Frage 1)?** | **Ja.** Quelle `tools/praeparationen/ueb29-meldedienst.ts` im Übungsrepositorium, Ziel `frontend/src/api/meldedienst.ts`, je Meßbaum gesetzt; `historie-bauen-b4.py` bricht ab, wenn die Quelle fehlt **oder** wenn sie sich selbst als synthetisch ausweist | **Verworfen: ohne ihn zu fahren** – `SK-010-N02` liefe ein zweites Mal ohne Gegenstand für seine zweite Hälfte, und das Ergebnis stünde vorher fest. **Verworfen: ein Modul, das schon eine fremde Präparation trägt** (D-137): `books.ts` führt den Wartungshinweis für Assistenzwerkzeuge, ein Lauf träfe beides. Deshalb eine eigene Datei. **Preis, benannt:** eine weitere Datei im Übungsrepositorium, die nur eine Zelle braucht |
| **E6** | **Bekommen die drei Zellen aus D-221 den Zuschnitt `konf` (`K-82` Frage 2)?** | **Ja, und zwar drei statt zwei:** `SK-012-P02`, `SK-011-N04` und `SK-010-P02`. Die Klasse liegt seit `0.77.0` fertig im Apparat | 🟢 **`SK-012-P02` und `SK-010-P02` kosten nichts** – beide fahren ohnehin. **`SK-011-N04` kostet zwei Läufe** (nur der Kontrollauf, und `fw-docs-update` hat zwei Turns); ihr Hauptlauf vom Meßtag bleibt gültig, weil dieser Skill als einziger der drei **nicht** gehoben worden ist. 🔴 **Bei `SK-010-P02` bleibt der `risiko`-Kontrollauf vom 2026-09-20 als Beleg der ERSTEN Hälfte stehen** (Mindesttiefe), der Nachlauf liefert `konf` für die zweite (Fundstellen-Treue). **Preis, benannt:** Die erste Hälfte ist gegen Skillfassung `0.1.5` geschnitten, die zweite gegen `0.1.6` |

| **E7** | **Der geteilte `node_modules`-Bestand hat sich um ein Byte geändert – ist das ein Schreibzugriff?** | **Nein, und die beiden Zähler werden gleichgezogen.** `node_modules/.vite/vitest/results.json` gehört dem **Prüfmittel**, und `umgebungen-bauen-b4.py` fährt es vor jedem Meßtag. `node-waechter.py` weist solche Pfade seit seinem Bau gesondert aus; `baeume_loeschen.py` tut es ab sofort auch | 🔴 **Gefunden beim Trockenlauf des Apparats:** 101 089 284 Bytes gegen die 101 089 283 aus `0.79.1`. **Zwei Zähler desselben Gegenstands sagten Verschiedenes**, und der Beleg des Aufräumens hing am unschärferen. 🔴 **Der Wächter hätte am Meßtag angeschlagen, wo nichts geschehen ist:** `<TEST_COMMAND>` steht im `allow`-Korb, also darf jeder Lauf das Prüfmittel starten. **Verworfen: den Zwischenstand mitzuzählen** (eine Zahl, die jeder Testlauf verschiebt, taugt nicht als Beleg); **verworfen: `.vite` vor jedem Lauf zu löschen** (dann mißt der erste Lauf kalt und jeder folgende warm). **Preis, benannt:** Ein Schreibzugriff innerhalb von `.vite` bliebe unbemerkt – der Pfad steht in `<EXCLUDED_PATHS>` und im `deny`-Korb |

## 4. Entscheidung

**E1 bis E7 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-20). Decision
Records **D-224** bis **D-228**; `K-83` entschieden, **`K-84` neu**, `K-82` berichtigt
und seine drei Fragen beantwortet. **Kriterium 2: 30 → 32** – zwei Zellen werden
geöffnet, keine geschlossen.

## 5. Abnahme

- `validate-framework.py --root .`: **0 Fehler, 0 Warnungen**.
- `probe-pruefungen.py`: voller Lauf, alle Sonden und Gegenproben bestanden – darunter
  die vier neuen Einheiten zu Prüfung 69.
- `zaehlen46.py`: **Katalog 4 | Testblätter 28 | Summe 32**.
- Protokoll: `leitwerk-core/tests/protocols/2026-09-20-vorbedingungen-nachlauf-b4.md`.
- **Kein Lauf am Client, kein Kontingent verbraucht.**

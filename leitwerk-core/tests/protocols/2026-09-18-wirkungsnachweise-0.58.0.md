# Wirkungsnachweise 0.58.0

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-18 |
| Framework-Version | `0.58.0` (Vorstand `0.57.1`, Commit `f8e09bd`) |
| Antrag | `CR-2026-082`, D-130 bis D-134, `K-53` neu |
| Gegenstand | **Der dritte Sitzungstest.** Fünf Ergebniszellen abgenommen (Kriterium 2: 105 → 100); die Präparation `UEB-06` berichtigt; das Präparationsregister um eine **Belegspalte** erweitert; **Prüfung 44 um einen dritten Gegenstand**; Zeile B2 des Packs `claude-code` zur Hälfte von `[DOK]` auf `[MESS]` |
| Prüfmethode | Elf Sitzungsläufe (eigenes Protokoll: `2026-09-18-sitzungstest-pi-ds-2.md`); Validatorlauf gegen den fertigen Baum; Sondenlauf `probe-pruefungen.py .` in **beiden** Kodierungsumgebungen (D-49); Trockenlauf `install.py --update --dry-run` gegen je eine Kopie **beider** übernehmender Projekte |
| Ergebnis | **Validator 0 Fehler, 0 Warnungen; 270 Ergebniszeilen bestanden in beiden Kodierungsumgebungen.** Prüfung 46 rechnet Kriterium 2 auf **100** aus und hält es gegen die nachgezogene Standzeile |

---

## 1. Was dieses Release tut und was nicht

**Es bewegt Kriterium 2 von 105 auf 100** – die dritte Bewegung in Folge. Kriterium 1
bleibt **23**, Kriterium 3 und 4 bleiben **0**.

**Es ändert keine Regel und keine Zusage über das Verhalten eines Clients** – mit einer
Ausnahme, und die ist eine **Verschärfung des Belegstands**, keine neue Zusage: Zeile B2
des Packs `claude-code` trägt für zwei ihrer drei Vorrangpaare jetzt Messungen statt
Dokumentation.

---

## 2. Der Gegenstand, für den es keinen Gegenbeweis gegen den Vorstand gibt – und warum

Bei 0.57.0 und 0.57.1 war der stärkste Nachweis der Lauf der neuen Prüfung gegen den
**unberührten Vorstand**. Für den dritten Gegenstand von Prüfung 44 ist er **nicht
herstellbar, und das hat einen benennbaren Grund:**

> Der Gegenstand ist eine **Tabellenspalte, die es im Vorstand nicht gibt.** **Gemessen**
> (`git archive f8e09bd` nach `C:\lw-gb`, neuer Validator hineinkopiert, Installation mit
> dem `install.py` des Arbeitsbaums): Der Lauf gegen `0.57.1` meldet **genau einen Fehler**,
> und zwar „die Registertabelle führt keine Spalte ›Wie sie belegt ist‹“ – also genau das,
> was **Sonde `44e`** misst, und **nicht** die sieben leeren Belegzellen. **Der Gegenbeweis
> wäre eine Wiederholung der Sonde, kein zweiter Nachweis** – der Anker fällt vor dem
> Inhalt, und das ist die Bauform von Prüfung 44 seit ihrer Erstfassung.

**An seine Stelle tritt das Sondenpaar**, und es ist in beide Richtungen gebaut:

| Einheit | Gegenstand | Ergebnis |
|---|---|---|
| Sonde `44d` | eine registrierte Präparation **ohne** Belegzelle – der Fall `UEB-06` | **OK** |
| Sonde `44e` | die Spaltenüberschrift ist umbenannt – **der verlorene Anker** | **OK** |
| Gegenprobe `44a` | Auslieferungszustand, sieben registrierte und sieben gebrauchte Präparationen | **OK** |
| Gegenprobe `44b` | eine achte Präparation, registriert **mit** Belegzelle und von einem Testfall gebraucht | **OK** |

> 🔴 **Die Gegenprobe `44b` ist nachgezogen worden, und sie wäre sonst gefallen.** Sie fügt
> eine Registerzeile ein; die Zeile hatte fünf Spalten, die Tabelle hat jetzt sechs.
> **Nachgezogen wird die Gegenprobe, nicht die Prüfung** – wer einen erlaubten Fall
> herstellt, muss ihn vollständig herstellen. Das ist der dokumentierte Fallstrick
> *„Eine neue Prüfung kann eine bestehende Gegenprobe unvollständig machen"*, und er ist
> hier zum ersten Mal **vor** dem Lauf abgefangen worden.

**Isoliert gemessen wurde der neue Gegenstand zusätzlich von Hand**, bevor die Sonden
gebaut waren: Belegzelle von `UEB-04` geleert → *„die Zeile UEB-04 führt keine
Belegzelle"*, 1 Fehler; Spaltenüberschrift umbenannt → *„die Registertabelle führt keine
Spalte 'Wie sie belegt ist'"*, 1 Fehler; unveränderter Baum → 0 Fehler.

---

## 3. Der Sondenlauf

| Lauf | Kodierungsumgebung | Ergebnis |
|---|---|---|
| 1 | ohne `PYTHONIOENCODING` | **270 Ergebniszeilen, alle bestanden** |
| 2 | `PYTHONIOENCODING=utf-8` | **270 Ergebniszeilen, alle bestanden** |

**Zusammensetzung:** 169 Sonden, 71 Gegenproben, 12 Selbstproben, 18 Bündelkopfzeilen.
Gegenüber 0.57.1 sind **zwei Sonden** hinzugekommen (`44d`, `44e`); die Sondenmenge bleibt
`6, 14 und 18 bis 48`, weil Prüfung 44 schon in der Spanne lag.

**Selbstprobe `B1`** bestätigt, dass jede Einheit einen Beschreibungssatz von 5 bis 30
Worten trägt – auch die beiden neuen.

---

## 4. Der Trockenlauf gegen beide übernehmenden Projekte

Gefahren unter `C:\lw-mig` – **ein kurzer Pfad, und das ist die Lehre aus 0.57.1**, wo
derselbe Trockenlauf im Scratchpad an der 260-Zeichen-Grenze von Windows scheiterte.

| Projekt | Stand | Ergebnis |
|---|---|---|
| Übungsrepositorium | 0.57.1 | **0 angelegt, 0 aktualisiert, 64 unverändert** |
| Pilot `otp-generator` | 0.54.1 | **0 angelegt, 4 aktualisiert** – beide Plan-Skills, je `SKILL.md` und `CHANGELOG.md` |

> ⚠️ **Die vier Dateien des Piloten gehören nicht zu diesem Release.** Sie sind die
> Laufzeitwirkung von **0.57.1**, die der Pilot noch nicht geholt hat. **Wer nur die Zahl
> liest, schreibt einen falschen Migrationshinweis** – genau der Fehler von 0.54.0, und er
> ist hier durch den zweiten Messpunkt abgefangen: Das Übungsrepositorium steht auf 0.57.1
> und meldet **null**.

**Das Übungsrepositorium ist im Zuge dieses Releases von 0.54.1 auf 0.57.1 gehoben
worden** (eigener Commit in jenem Repositorium). Gemessene Laufzeitwirkung der drei
Releases zusammen: **genau vier Dateien, beide Plan-Skills** – die Produktaussage zum
Plan-Modus, die 0.57.1 in die Fähigkeitsmatrix verschoben hat.

---

## 5. Was am Prüfapparat auffiel

- 🔴 **Ein Encode-Fehler leert die Zieldatei, bevor er auffällt – und zwar in BEIDEN
  Schreibweisen.** Sowohl `io.open(pfad, "w", encoding="utf-8").write(text)` als auch
  `io.open(pfad, "wb").write(text.encode("utf-8"))` schneiden die Datei **beim Öffnen** auf
  null Bytes; scheitert danach das Kodieren, ist sie weg. **Richtig ist zweizeilig:**
  `daten = text.encode("utf-8")`, dann `io.open(pfad, "wb").write(daten)`.
  **Auslöser war ein Emoji als Ersatzzeichenpaar in einem Python-String.** Der erste Fall
  traf eine versionierte Datei und war folgenlos; der zweite traf die **unversionierte**
  Übergabe außerhalb des Repositoriums und war es nicht – sie ist aus der Tool-Result-Ablage
  der Sitzung wiederhergestellt worden. **Wer an einer unversionierten Datei arbeitet, legt
  vorher eine Kopie an.**
- **Die Anführungszeichen des Testkatalogs sind gemischt:** öffnend typografisch (`„`,
  U+201E), schließend **ASCII** (`"`). Ein Suchtext mit typografischem Schlusszeichen
  trifft nicht. **Ein Zeichen, das wie ein anderes aussieht, ist die Bauform des
  kyrillischen `е`** – hier ohne Schaden, weil das Patchskript bei falscher Trefferzahl
  abbricht.
- **Der Zellenwächter hat sich in diesem Release fünfmal gelohnt:** Die Ergebniszellen des
  Testkatalogs tragen neun Trenner, die Registerzeilen sieben, die Decision Records sieben
  und die Planzeile der Roadmap fünf. Jede Einfügung ist danach gezählt worden.

---

## 6. Abnahme

| Nachweis | Ergebnis |
|---|---|
| `validate-framework.py` gegen den fertigen Baum | **0 Fehler, 0 Warnungen** |
| `probe-pruefungen.py .`, ohne `PYTHONIOENCODING` | **270 von 270** |
| `probe-pruefungen.py .`, mit `PYTHONIOENCODING=utf-8` | **270 von 270** |
| Prüfung 46, Kriterium 2 | **100**, Standzeile nachgezogen |
| `install.py --update --dry-run`, Übungsrepositorium | 0 / 0 |
| `install.py --update --dry-run`, Pilot | 0 / 4 (Rückstand aus 0.57.1) |
| Nicht-ASCII in Commit-Nachricht und PR-Text | **leer** |

# Änderungsantrag `CR-2026-049`

| Feld | Inhalt |
|---|---|
| Titel | Der Wirkungsnachweis hängt von der Kodierung der aufrufenden Umgebung ab – und wird rot, wenn man es richtig macht |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-12 |
| Betroffene Artefakte | `tests/scripts/probe-pruefungen.py` (`lauf()`, Zeile 74) |
| Ebene laut Entscheidungsbaum 6 | Kern – Prüfwerkzeug |
| Art | Eigener Befund dieser Sitzung, aufgefallen beim Sondenlauf zur Gegenprüfung von B04/B05 |
| Dringlichkeit | **vor dem nächsten Release** – das Skript ist das Abnahmetor nach D-23 |

## 1. Anlass und Problem

Der Sondenlauf dieser Sitzung meldete **eine Abweichung**: `SONDE 19` – „Pack ohne
Auskunftsabschnitt" – schlug fehl. Der Arbeitsbaum war sauber, der Validator meldete 0 Fehler
und 0 Warnungen, und derselbe Lauf in derselben Sitzung bestand anschließend vollständig.

**Der Unterschied war eine einzige Umgebungsvariable.**

| Lauf | Ergebnis |
|---|---|
| `PYTHONIOENCODING=utf-8 python …/probe-pruefungen.py .` | **1 Abweichung** (Sonde 19) |
| `python …/probe-pruefungen.py .` | alle 48 Sonden und Gegenproben bestanden |

Die Fehlerausgabe verriet den Grund selbst: Sie enthielt `auÃŸerhalb` statt `außerhalb`.

### Die Messung

Vier Läufe, ein Kindprozess, der genau einen Satz mit Umlaut ausgibt:

| Aufrufform | Elternumgebung | Umlaut heil |
|---|---|---|
| `lauf()` wie heute (`text=True`, ohne `encoding`, ohne `env`) | **mit** `PYTHONIOENCODING=utf-8` | **nein** – `auÃŸerhalb` |
| `lauf()` wie heute | ohne | ja |
| mit `encoding="utf-8"` und gepinnter `env` | mit | ja |
| mit `encoding="utf-8"` und gepinnter `env` | ohne | ja |

**Die einzige rote Zelle ist genau die Konfiguration, die das Arbeitswissen dieses Projekts
empfiehlt.** Nach der Sitzung vom 2026-09-12 gilt dort: „Unterprozesse laufen seither mit
`PYTHONIOENCODING=utf-8`." Wer sich daran hält, bekommt einen roten Sondenlauf.

### Die Lehre war gezogen – in der Nachbarfunktion

`strict_ausgabe()` (Zeile 503) macht es richtig: gepinnte `env` **und** `encoding="utf-8"`. Ihr
Docstring beschreibt die Falle vollständig, einschließlich des Satzes „Eine Gegenprobe auf
‚nicht enthalten' besteht das klaglos – sie ist dann wertlos, ohne es zu zeigen."

`lauf()` steht 429 Zeilen darüber und hat die Korrektur nie bekommen. **Sie ist die Funktion,
auf der die generischen Runner sitzen:** `sonde()`, `gegenprobe()` und `sonde_ohne_wert()`,
zusammen **28 Aufrufe**.

### Wie weit es heute reicht – und warum das der schlechtere Teil ist

Von den 28 Aufrufen trägt **genau einer** einen Suchtext mit Umlaut: Sonde 19. Der Schaden
heute ist also ein falsches Rot an einer Stelle.

**Die Richtung des Fehlers ist bei einer Sonde harmlos und bei einer Gegenprobe nicht.** Eine
Sonde sucht einen Text und fällt sichtbar, wenn er zerschossen ankommt. Eine Gegenprobe sucht
denselben Text und prüft auf **Abwesenheit** – ein zerschossener Text ist abwesend, die
Gegenprobe besteht, und niemand erfährt etwas. Es gibt heute keine solche Gegenprobe. Es gibt
sie beim nächsten deutschen Suchtext, und dann meldet nichts.

Das ist derselbe Befundtyp wie `CR-2026-042` und wie die Präparationsprüfung aus 0.27.0: **eine
Prüfung, die unter bestimmten Bedingungen nichts mehr prüft und es nicht zeigt.**

## 2. Vorgeschlagene Änderung

`lauf()` bekommt dieselbe Behandlung wie `strict_ausgabe()`:

```python
def lauf(root: str) -> str:
    umgebung = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, os.path.join(root, *VALIDATOR.split("/")),
                        "--root", root],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=umgebung)
    return (p.stdout or "") + (p.stderr or "")
```

Dazu ein Kommentar, der auf `strict_ausgabe()` verweist, damit die Begründung nicht ein zweites
Mal verloren geht.

## 3. Was dieser Antrag nicht ändert

- **Er ändert keine Prüfung und kein Prüfergebnis.** Nach der Korrektur bestehen dieselben 48
  Sonden und Gegenproben – in beiden Umgebungen.
- **Er berührt den Validator nicht.** Dessen Ausgabe ist korrekt; falsch ist, wie das
  Sondenskript sie liest.
- **Er löst die allgemeine Frage nicht**, ob Suchtexte in Sonden überhaupt Umlaute enthalten
  sollten. Siehe E2.

## 4. Prüffragen

- [x] Richtige Ebene: Kern – Prüfwerkzeug.
- [x] Verschärfungsprinzip: reine Verschärfung; eine Prüfung, die bisher unter bestimmten
      Bedingungen ausfiel, fällt nicht mehr aus.
- [x] Widerspruchsfreiheit: D-23 (Wirkungsnachweis), `CR-2026-042` (Abwesenheitsnachweis über
      ein Suchwerkzeug) gelesen; die Korrektur ist wortgleich zu `strict_ausgabe()`.
- [x] Laufzeitfassungen: nicht betroffen.
- [x] Belegstatus: **gemessen**, vier Läufe als Wahrheitstabelle, plus zwei vollständige
      Sondenläufe mit und ohne die Variable.
- [x] Test- und Validierungsbedarf: Der Nachweis ist der Lauf selbst – nach der Korrektur muss
      der Sondenlauf **in beiden Umgebungen** vollständig bestehen. Das ist die Abnahme.
- [x] Overlays: nicht betroffen.
- [ ] Dokumentation: CHANGELOG; Arbeitswissen um den Satz ergänzen, dass der Sondenlauf in
      beiden Umgebungen zu fahren ist.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Nur `lauf()` korrigieren – oder jeden Unterprozessaufruf des Skripts durchgehen? | **Jeden durchgehen.** Zwei Aufrufe tragen die Korrektur, einer nicht; das ist kein Muster, sondern ein Zufall der Entstehungsreihenfolge. Ein Skript, das an drei Stellen dasselbe unterschiedlich macht, erzeugt den nächsten Befund selbst | Der Antrag berührt mehr Zeilen als der Befund verlangt. Dafür ist die Eigenschaft danach eine des Skripts und nicht die einzelner Funktionen |
| E2 | Suchtexte mit Umlaut künftig verbieten? | **Nein.** Das behebt das Symptom und verlagert die Gefahr: Der Validator meldet auf Deutsch, und ein Suchtext, der den Umlaut umgeht, misst am Gegenstand vorbei. Die Kodierung gehört dort in Ordnung gebracht, wo sie gelesen wird | Suchtexte bleiben so anfällig, wie die Leseseite es zulässt. Nach der Korrektur ist das keine Anfälligkeit mehr |
| E3 | Soll der Sondenlauf **beide** Umgebungen selbst prüfen? | **Vorschlag: nein, aber als Auflage in die Abnahme.** Ein Skript, das sich selbst zweimal startet, wird unübersichtlich; die Zweifachprüfung ist ein Schritt der Release-Abnahme, kein Sondenblock | Die Eigenschaft ist danach nicht maschinell gesichert. **Die Gegenposition ist vertretbar:** Genau solche Zusagen hat dieses Projekt wiederholt verfallen sehen, weil sie nur in einer Checkliste standen |
| E4 | Zählt das als Release? | **Nein.** Es ist eine Korrektur am Nachweiswerkzeug, kein Framework-Verhalten. Sie geht mit der Gegenprüfung von B04/B05 als Erhebungs-PR nach `main` und wird im nächsten Release eingearbeitet | Zwischen Korrektur und Release steht ein Zustand, in dem `CHANGELOG.md` sie noch nicht führt |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | `<offen>` |
| Datum | `<TBD>` |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | `<TBD>` |
| Umsetzung | `<offen>` |

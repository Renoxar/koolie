# Änderungsantrag `CR-2026-109`

| Feld | Inhalt |
|---|---|
| Titel | Der Aufräumer stirbt an seiner eigenen Erfolgsmeldung – und das Aufräumen hat ihn zum ersten Mal in der zweiten Kodierungsumgebung gefahren |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-20 |
| Betroffene Artefakte | `tests/erhebungen/baeume_loeschen.py`, `governance/DECISION_LOG.md` (**D-223** neu, `K-82` berichtigt), `docs/ROADMAP.md`, `CHANGELOG.md`, `VERSION`, `UEBERGABE.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand ist ein Skript unter `<CORE_DIR>/tests/` und die Berichtigung eines Klärungspunkts |
| Art | Berichtigung nach einem gemessenen Fehlschlag – **kein Kontingent, kein Lauf am Client** |
| Dringlichkeit | **Regulär**, unmittelbar nach `0.79.0` |

## 1. Anlass

Das Aufräumen nach dem Meßtag ist gefahren. `baeume_loeschen.py loeschen` hat getan,
was es soll – **46 Bäume gelöscht, achtunddreißig Verzeichnisverbindungen einzeln
gelöst, und der geteilte Bestand ist unberührt** (9798 Dateien / 101 089 283 Bytes vor
und nach dem Löschen, auf Datei und Byte gleich).

🔴 **Und danach ist es abgestürzt – an seiner letzten Zeile:**

```
node_modules nachher: 9798 Dateien / 101089283 Bytes
Traceback (most recent call last):
  File "baeume_loeschen.py", line 78, in main
    print("\U0001f7e2 geteilter Bestand unberuehrt")
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f7e2'
```

Das Skript hat **keine** Zeile `sys.stdout.reconfigure(encoding="utf-8")` und gibt in
seiner Erfolgsmeldung ein Emoji aus. In der Umgebung **ohne** `PYTHONIOENCODING=utf-8`
– also in der Standardumgebung dieses Arbeitsplatzes – kann es die Meldung nicht
schreiben.

## 2. Warum es bis hierher nicht aufgefallen ist

`baeume_loeschen.py` ist mit dem Meßtag entstanden (`0.78.2`-Nachlauf, Befund 6 des
ersten vollständigen Aufbaus) und **am Meßtag nur im Erfolgsfall mit gesetztem
`PYTHONIOENCODING` gefahren worden**. Der Aufräumlauf nach dem Merge von `0.79.0` war
der erste in der anderen Kodierungsumgebung.

➡️ **Das ist die Lehre von `0.67.0` an einem neuen Ort:** *Wer einen Lauf in zwei
Kodierungsumgebungen verlangt, prüft auch seinen **Berichtsweg** in beiden.* Der
Abnahmelauf des Prüfapparats fährt seit D-49 in beiden; **ein Werkzeug daneben fuhr nie
in beiden**, und mit `0.79.0` ist es in den Kern gewandert (D-222).

🟢 **Ausgezählt über alle siebzehn Skripte unter `tests/erhebungen/`: genau eines ist
betroffen.** Die übrigen sechzehn tragen entweder die Zeile oder geben ausschließlich
ASCII aus. Es ist das **jüngste** – und das einzige, das nie einen vollständigen
Durchgang in beiden Umgebungen hatte.

🟡 **Der Schaden war null:** Der Absturz kam **nach** der Gegenzählung und **nach**
dem Löschen.

🔴 **Die naheliegende Verschärfung lautete: *die Abbruchmeldung trägt dasselbe Zeichen
und stirbt beim nächsten Mal genauso.*** Zeile 75 ist
`raise SystemExit("🔴 ABBRUCH: der geteilte Bestand hat sich geaendert!")` – also
genau die Meldung, die kommt, wenn das Skript gerade 9798 Dateien des
Übungsrepositoriums mitgelöscht hat.

🟢 **Gemessen, und sie ist widerlegt.** Derselbe Text auf beiden Wegen, in beiden
Umgebungen:

| Weg | ohne `PYTHONIOENCODING` | mit `PYTHONIOENCODING=utf-8` |
|---|---|---|
| `print(…)` auf **stdout** | `UnicodeEncodeError`, exit 1 | Ampelzeile, exit 0 |
| `SystemExit(…)` auf **stderr** | `\U0001f534 ABBRUCH: …`, exit 1 – **die Meldung kommt an**, nur das Zeichen ist escapet | `🔴 ABBRUCH: …`, exit 1 |

➡️ **Python schreibt die `SystemExit`-Meldung mit `backslashreplace`, `print` mit
`strict`.** Der **wichtige** Bericht trägt, der harmlose nicht – die Verschärfung wäre
richtig geklungen und falsch gewesen. *Den eigenen Lösungsvorschlag gegenprüfen, nicht
nur den Befund.*

## 3. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Bekommt das Skript die Zeile, oder verliert es das Emoji?** | **Die Zeile.** `sys.stdout.reconfigure(encoding="utf-8")` steht in allen sechzehn anderen Skripten dieses Verzeichnisses und ist die Form, die dieses Projekt führt | **Verworfen: das Emoji streichen.** Dann wäre genau dieses Skript stumm, wo die übrigen sechzehn eine Ampel führen – und die nächste Nicht-ASCII-Ausgabe brächte den Absturz zurück. **Der Fehler ist nicht das Zeichen, sondern der fehlende Berichtsweg.** Gegenprobe zur Auswahl: Die Zeile behebt **jede** künftige Nicht-ASCII-Ausgabe des Skripts, das Streichen nur diese eine |
| **E2** | **Bekommen die übrigen sechzehn Skripte einen Wächter?** | **Nein – die Auszählung genügt, und sie steht im Protokoll dieses Antrags.** Sechzehn von siebzehn tragen die Zeile oder geben nur ASCII aus | Ein Wächter im Validator hätte hier **null** Gegenstand nach der Behebung, und das allein ist kein Grund gegen ihn (Prüfung 65 und 68 sind so gebaut). 🔴 **Der Grund ist ein anderer:** Ein Skript **ohne** Nicht-ASCII-Ausgabe braucht die Zeile nicht, und ein Zähler, der sie trotzdem verlangt, wäre *eine Bedingung, die mehr verlangt als ihr Kriterium fordert*. Ein Zähler, der die Ausgabe **analysiert**, müßte jeden `print`-Ausdruck auswerten – er prüfte die Schreibweise, nicht die Sache. **Preis, benannt:** Das nächste neue Skript kann denselben Fehler machen; was ihn fängt, ist der Durchgang in beiden Umgebungen, und der steht in der README dieses Verzeichnisses |
| **E3** | **Wie wird `K-82` berichtigt – die Bäume stehen nicht mehr?** | **Berichtigen, mit ausgewiesenem Grund.** `K-82` sagte *„die Bäume stehen noch"*; sie sind seit dem Aufräumlauf gelöscht, und die dritte Frage des Klärungspunkts (bestehende oder frische Bäume?) **entfällt damit** | 🔴 **Die Reihenfolge war falsch:** Die Übergabe von `0.79.0` ist **vor** dem Aufräumen geschrieben worden und hat einen Zustand behauptet, den das Aufräumen eine Viertelstunde später aufgehoben hat. **Das ist D-216 in der Sache, nicht in der Form:** Die Übergabe stand richtig im Release-Commit – aber ein Vorgang **nach** dem Merge hat ihre Aussage überholt. ➡️ **Wer eine Aufräumaufgabe hat, führt sie VOR der Übergabe aus, die den Zustand danach beschreibt.** **Verworfen: eine bloße Nachtragszeile** – *wer die Stelle liest und den Nachtrag nicht, übernimmt den Zustand* |

## 4. Entscheidung

**E1 bis E3 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-20). Decision
Record **D-223**; `K-82` berichtigt. **Kriterium 2 unverändert 30** – keine Zelle wird
angefaßt.

## 5. Abnahme

- `validate-framework.py --root .`: **0 Fehler, 0 Warnungen**.
- `probe-pruefungen.py .` in **beiden** Kodierungsumgebungen, voller Lauf.
- **Der eigentliche Nachweis steht außerhalb des Validators, und er ist ein Paar am
  selben Gegenstand.** Eine Probebasis mit einem Wegwerfbaum, `loeschen` **ohne**
  `PYTHONIOENCODING`:

  | Stand | Ergebnis |
  |---|---|
  | **Vorstand** (unberührte Fassung, nur der Basispfad umgehängt) | `UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f7e2'`, **exit 1** |
  | **behobener Stand** | vier Ausgabezeilen samt Ampel, **exit 0**, Gegenzählung 9798 / 101 089 283 unverändert |

  🔴 **`zaehlen` taugt als Gegenprobe NICHT** – der Zweig kehrt vor der Ampelzeile
  zurück. Die erste Fassung dieses Abschnitts hat ihn vorgeschlagen; *eine Gegenprobe,
  die den Gegenstand nicht erreicht, besteht immer.*
- **Auszählung über alle siebzehn Skripte:** eines betroffen, sechzehn nicht.

## 6. Migrationshinweis

**Keine.** `tests/erhebungen/` wird von `install.py` in kein Projekt geschrieben.

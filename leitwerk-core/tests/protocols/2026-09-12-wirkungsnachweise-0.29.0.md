# Testprotokoll – Wirkungsnachweis des Schutzes vorhandener Projektdateien (Release 0.29.0)

| Feld | Inhalt |
|---|---|
| Test-ID | `FW-KO-01` (Basis), Teilnachweis für den mit 0.29.0 hinzugekommenen Abbruch der Erstinstallation |
| Framework-Version | 0.29.0 |
| Datum | 2026-09-12 |
| Prüfmethode | skript |
| Prüfgegenstand | zwei Temporärverzeichnisse – eines mit einer fremden Datei unter dem Namen der Wurzel-Anweisungsdatei, eines leer |
| Werkzeug | `leitwerk-core/tests/scripts/probe-pruefungen.py` |
| Umgebung | Windows 11, Python 3.14.4, PyYAML 6.0.3 |
| Ergebnis | **Sonde gemeldet, Gegenprobe unbeanstandet; gegen die Vorfassung 0.28.0 fällt die Sonde** |

## 1. Anlass: der Befund entstand nicht am Schreibtisch

Dieser Nachweis hat eine Vorgeschichte, die zu ihm gehört. Er entstand **bei der Vorbereitung der
ersten echten Inbetriebnahme**, nicht bei einer Durchsicht des Codes. Vor dem ersten Befehl wurde
ein Trockenlauf gegen das vorgesehene Projekt gefahren:

```text
Framework 0.28.0
Client:  claude-code
Modus:   install  (dry-run, es wird nichts geschrieben)

Angelegt (77): …
Core aktualisiert (1):
  CLAUDE.md

Zusammenfassung: 77 angelegt, 1 aktualisiert, 0 unveraendert, 0 Projektdateien behalten.
```

Die genannte Datei war die Anweisungsdatei des Projekts: 34 Kilobyte, versioniert, seit Monaten
gepflegt. **Der erste Befehl des Übernahmeleitfadens hätte sie ersetzt** – ausgewiesen als „1
aktualisiert", ein Wort, das nach Pflege klingt.

`docs/ADOPTION_GUIDE.md` versprach an derselben Stelle wörtlich: *„Bestehende Projektdateien
werden nie überschrieben."*

**Der Trockenlauf war kein vorgeschriebener Schritt.** Er stand in keiner Checkliste; er wurde
gefahren, weil das Zielverzeichnis ein gewachsenes Projekt war. Ohne ihn wäre der Befund erst
aufgefallen, nachdem die Datei weg war.

## 2. Ausgeführte Befehle und Ergebnis

```text
python leitwerk-core/tests/scripts/validate-framework.py
→ Ergebnis: 0 Fehler, 0 Warnungen

python leitwerk-core/tests/scripts/probe-pruefungen.py .
→ alle Sonden und Gegenproben bestanden   (Exit 0)
```

Nach der Korrektur gegen dasselbe Projekt:

```text
FEHLER: In …\BlackNode liegen bereits Dateien, die das Framework beansprucht:
  CLAUDE.md

Eine Erstinstallation wuerde sie ueberschreiben. Das Framework hat in dieses
Verzeichnis noch nie geschrieben - diese Dateien gehoeren also dem Projekt.

Stammen sie aus einer frueheren Installation: --update verwenden.
Sonst den Inhalt vorher uebernehmen - Projektwissen nach project-overlay/OVERLAY.md,
projektspezifische Regeln in eine Regeldatei 2N-overlay-<name>.md. Danach die
Datei entfernen und erneut aufrufen (leitwerk-core/docs/ADOPTION_GUIDE.md, Abschnitt 2).
```

Exit-Code 1; die Datei hinterher unverändert bei 33.902 Bytes.

## 3. Sonde und Gegenprobe

| Art | Aufbau | Bedingung | Ergebnis |
|---|---|---|---|
| Sonde | Leeres Verzeichnis, darin **eine** fremde Datei unter dem Namen der Wurzel-Anweisungsdatei; Erstinstallation `claude-code` | **drei** Bedingungen: Exit 1, Datei byte-gleich wie vorher, Laufzeitschicht **nicht** angelegt | gemeldet |
| Gegenprobe | Freies Verzeichnis, dieselbe Erstinstallation | Exit 0, Wurzel-Anweisungsdatei angelegt | unbeanstandet |

**Die dritte Bedingung der Sonde ist die eigentliche.** Ein Abbruch, der erst nach der Hälfte der
Dateien kommt, ist schlimmer als keiner: Das Projekt hätte dann eine halbe Installation und keinen
Hinweis darauf, welche Hälfte. Der Abbruch steht deshalb **vor** dem ersten Schreibvorgang, und die
Sonde prüft das an der Abwesenheit der Laufzeitschicht.

**Die Gegenprobe ist nicht nebensächlich.** Ohne sie belegte die Sonde nur, dass irgendetwas
abbricht – nicht, dass die Erstinstallation überhaupt noch funktioniert. Eine Fassung, die immer
abbricht, besteht jede Sonde darüber.

## 4. Der Lauf, der den Nachweis trägt

Derselbe Sondenblock gegen die Vorfassung 0.28.0 – eine Kopie des Arbeitsbaums, in der allein
`install.py` auf den Stand `HEAD` zurückgesetzt ist:

| Fall | gegen 0.28.0 | gegen 0.29.0 |
|---|---|---|
| Erstinstallation bricht ab, Projektdatei unberührt | **fällt** | besteht |
| Erstinstallation in ein freies Verzeichnis läuft durch | besteht | besteht |

**Eine Abweichung gegen 0.28.0, keine gegen 0.29.0.** Dass die Gegenprobe in beiden Fassungen
besteht, ist richtig so: Die Änderung sollte den freien Fall nicht berühren, und sie tut es nicht.

## 5. Was der Nachweis nicht leistet

- **Er schützt vor Verlust, nicht vor Arbeit.** Das Framework beansprucht die
  Wurzel-Anweisungsdatei weiterhin. Wer sie schon führt, muss den Inhalt übernehmen – der Weg steht
  seit diesem Release als Schritt 3a im Leitfaden, aber gehen muss ihn ein Mensch.
- **Der Fall eines fremden Agenten-Frameworks ist nicht gelöst** (K-31). Wenn ein anderes Werkzeug
  dieselbe Datei **erzeugt** und in markierten Abschnitten pflegt, hilft ein einmaliger Umzug des
  Inhalts nicht: Beim nächsten Lauf schreibt es seine Abschnitte zurück, und zwei Regelwerke
  beanspruchen Ebene 1. Der Leitfaden weist das ausdrücklich als ungelöst aus, statt es zu
  verschweigen.
- **`--update` bleibt scharf.** Es überschreibt die Core-Dateien, und das ist sein Zweck. Wer eine
  Core-Datei von Hand ändert, verliert die Änderung beim nächsten Release – unverändert richtig.
- **Gemessen ist `claude-code`.** Der Mechanismus ist clientneutral, der Nachweis nicht.

## 6. Bewertung

**Bestanden.** Die Erstinstallation bricht ab, bevor sie schreibt, und lässt das Projekt so zurück,
wie sie es vorgefunden hat. Der Befund selbst ist der Ertrag des Verfahrens: Er wurde gefunden,
weil vor dem ersten Befehl gemessen wurde statt danach.

| Feld | Inhalt |
|---|---|
| Gegenzeichnung | `<TBD>` |

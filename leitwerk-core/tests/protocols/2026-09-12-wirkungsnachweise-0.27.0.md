# Testprotokoll – Wirkungsnachweis der Prüfung 25 und von `--list-skills` (Release 0.27.0)

| Feld | Inhalt |
|---|---|
| Test-ID | `FW-KO-01` (Basis), Teilnachweis für die mit 0.27.0 hinzugekommene Prüfung 25 und für `install.py --list-skills` |
| Framework-Version | 0.27.0 |
| Datum | 2026-09-12 |
| Prüfmethode | skript |
| Prüfgegenstand | Framework-Repository; je Sonde eine vollständige Kopie in einem Temporärverzeichnis |
| Werkzeug | `leitwerk-core/tests/scripts/probe-pruefungen.py` |
| Umgebung | Windows 11, Python 3.14.4, PyYAML 6.0.3 |
| Ergebnis | **alle Sonden gemeldet, keine Gegenprobe beanstandet** |

## 1. Was nachzuweisen war

Drei Anträge sind mit diesem Release umgesetzt. Zwei davon ändern nur Text und brauchen keinen
eigenen Wirkungsnachweis; `CR-2026-041` bringt zwei neue Mechanismen, und für die gilt D-23:

| Gegenstand | Entscheidung | Warum ein Nachweis nötig ist |
|---|---|---|
| **Prüfung 25** – eine Zeile auf `[NICHT ABBILDBAR]` nennt den Ersatz | D-41 | Sie ist die Bedingung, unter der die Sperrklausel gelockert wurde. Ohne sie wäre die Lockerung eine Abbuchung |
| **`install.py --list-skills`** | D-42 | Er ist der Ersatz für eine Zusage, die ein Client nicht einlöst. Ein Ersatz, der nicht leistet, was er verspricht, wäre der Befundtyp dieses Projekts |

## 2. Ausgeführte Befehle und Ergebnis

```text
python leitwerk-core/tests/scripts/validate-framework.py
→ Ergebnis: 0 Fehler, 0 Warnungen

python leitwerk-core/tests/scripts/probe-pruefungen.py .
→ alle Sonden und Gegenproben bestanden   (Exit 0)
```

## 3. Prüfung 25 hat beim ersten Lauf zwei echte Zeilen gemeldet

Der Nachweis begann nicht mit einer Sonde, sondern mit einem Befund. Unmittelbar nach dem Einbau
meldete Prüfung 25 **zwei** Zeilen, die auf `[NICHT ABBILDBAR]` standen, ohne einen Ersatz zu
benennen:

| Zeile | Pack | Was fehlte |
|---|---|---|
| `S5` | `claude-code` | Skills sind nicht aufzählbar – der Ersatz `install.py --list-skills` war beschlossen, stand aber nicht in der Zeile |
| `X2` | `devin-desktop` | Art und Ort der Codebasis-Indexierung. Hier gibt es **keinen** Ersatz; auch das war nicht gesagt |

**Die Lücke, gegen die die Prüfung gebaut ist, war bereits da.** Beide Zeilen sind mit diesem
Release ergänzt – die eine um den Ersatz, die andere um die ausdrückliche Feststellung, dass es
keinen gibt.

## 4. Sonden und Gegenproben im Einzelnen

| Gegenstand | Art | Gesetzter Defekt beziehungsweise erlaubter Fall | Ergebnis |
|---|---|---|---|
| Prüfung 25 | Sonde | In einem Pack wird das Wort ersetzt, auf das die Prüfung sieht – die S5-Zeile nennt ihren Ersatz nicht mehr | gemeldet |
| Prüfung 25 | Gegenprobe | Die Zusammenfassungstabelle desselben Dokuments führt `[NICHT ABBILDBAR]` als **Zeilenbeschriftung** und nennt keinen Ersatz | unbeanstandet |
| `--list-skills` | Sonde | Ein Skill, den keine Kernquelle liefert, wird in die Ablage gelegt | geführt, Herkunft `Projekt`, Aufrufbarkeit aus dem Frontmatter gelesen |
| `--list-skills` | Gegenprobe | Ein Verzeichnis **ohne** `SKILL.md` in derselben Ablage | nicht als Skill geführt |
| `--list-skills` | Sonde | – | die Ausgabe nennt ihre eigene Grenze |

Die Gegenprobe zu Prüfung 25 trifft genau die Stelle, an der die Prüfung zu breit hätte werden
können: Dieselbe Zeichenkette steht im selben Dokument einmal als Einstufung einer Zusage und
einmal als Beschriftung einer Zählzeile. Nur die erste ist eine Zusage.

Die dritte Sonde zu `--list-skills` ist die wichtigste. Das Kommando zählt die Skills **dieser
Installation**; Skills aus Ablagen außerhalb des Projektverzeichnisses sieht auch das Framework
nicht – also genau die, um die es bei diesem Befund geht. Eine Teilauskunft, die das verschweigt,
verspricht mehr, als sie leistet. Der Satz steht deshalb in der **Ausgabe**, nicht nur in der
Dokumentation, und eine Sonde hält ihn dort fest.

## 5. Ein Befund über die Sonden selbst

**Beim Lauf zu `CR-2026-040` fiel Sonde 23** – und die Prüfung war in Ordnung. Der Antrag hatte den
Satz geändert, den die Sonde als Anker für ihren Defekt sucht. `str.replace` fand ihn nicht, tat
nichts, der Lauf blieb sauber, und die Sonde meldete: *„Prüfung meldet nicht."* Richtig gewesen
wäre: *„Sonde präpariert nicht."*

Das ist dieselbe Bauart wie ERH-12 – ein Werkzeug, das arbeitet und ein falsches Ergebnis liefert –
nur eine Ebene tiefer, im Nachweisapparat selbst.

**Abhilfe, mit diesem Release wirksam:** `probe-pruefungen.py` bildet vor und nach der Präparation
einen Fingerabdruck des Baums. Verändert eine Sonde nichts, meldet der Lauf `[nichts praepariert]`
und nennt den Grund, statt die Prüfung zu beschuldigen. Das wirkt für **alle** Sonden, auch für
künftige.

**Nachgewiesen:** Eine Testfassung des Skripts mit absichtlich totem Suchtext meldet:

```text
SONDE      23   FEHL  Normativer Satz im Kopfkommentar der Wurzel-Anweisungsdatei  [nichts praepariert]
        Der Baum ist unveraendert - vermutlich passt der Suchtext der Sonde nicht mehr.
        Gemessen wuerde sonst die Sonde, nicht die Pruefung.
```

## 6. Grenzen dieses Nachweises

- **Prüfung 25 ist eine Wortprüfung.** Sie erzwingt, dass jemand die Frage nach dem Ersatz
  beantwortet hat – nicht, dass die Antwort taugt. Wer „Ersatz" hinschreibt, ohne einen zu nennen,
  kommt durch. Sie fängt das Vergessen, nicht die Absicht.
- **`--list-skills` ist an der Installation gemessen, nicht an einer Sitzung.** Ob der Client
  zusätzliche Skills mitführt, sagt dieses Kommando nicht und kann es nicht sagen. Genau das steht
  in seiner Ausgabe.
- **Die Sperre selbst bleibt ungeprüft.** Dass eine Kernzusage auf `[NICHT ABBILDBAR]` die
  Inbetriebnahme sperrt, ist eine Freigabe durch einen Menschen. Kein Skript setzt sie durch, und
  keines kann es.
- **`CR-2026-040` und `CR-2026-042` haben keine eigene Sonde** – sie ändern Begründungstexte und
  ein Verfahren. Für `CR-2026-040` ist nachgewiesen, was er zusagt: kein Prüfergebnis ändert sich.

## 7. Bewertung

**Bestanden.** Beide neuen Mechanismen melden einen gesetzten Defekt und lassen den erlaubten Fall
durch. Der Nachweisapparat selbst ist dabei um eine Bedingung ergänzt worden, die ihn ehrlicher
macht.

| Feld | Inhalt |
|---|---|
| Gegenzeichnung | `<TBD>` |

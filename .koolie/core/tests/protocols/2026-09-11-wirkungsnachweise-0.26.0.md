# Testprotokoll – Wirkungsnachweis der Prüfungen 18 bis 24 (Release 0.26.0)

| Feld | Inhalt |
|---|---|
| Test-ID | `FW-KO-01` (Basis), Teilnachweis für die mit 0.26.0 hinzugekommenen Prüfungen |
| Framework-Version | 0.26.0 |
| Datum | 2026-09-11 |
| Prüfmethode | skript |
| Prüfgegenstand | Framework-Repository; je Sonde eine vollständige Kopie in einem Temporärverzeichnis |
| Werkzeug | `leitwerk-core/tests/scripts/probe-pruefungen.py` |
| Umgebung | Windows 11, Python 3.14.4, PyYAML 6.0.3 |
| Ergebnis | **alle Sonden gemeldet, keine Gegenprobe beanstandet** |

## 1. Warum dieses Protokoll

D-23 sagt: Eine Prüfung gilt erst als vorhanden, wenn sie eine bewusst gesetzte Sonde
meldet. Sechs Prüfungen sind mit diesem Release hinzugekommen (19 bis 24), eine ist
erweitert worden (18). Ohne diesen Nachweis wären sie nach D-23 **nicht vorhanden** –
sieben Funktionen, die grün laufen, weil sie nichts finden.

Neu gegenüber früheren Nachweisen ist, dass der Nachweis selbst ein **Skript** ist und
nicht eine Beschreibung von Handgriffen. Er lässt sich wiederholen, ohne dass jemand die
Sonden aus einem Protokoll nachbaut – und er läuft auf einer Kopie, das Repositorium
bleibt unberührt.

**Jede Prüfung hat zusätzlich eine Gegenprobe.** Das ist der Teil, den man weglassen kann
und nicht weglassen sollte: Eine Prüfung, die alles meldet, besteht jede Sonde. Die
Gegenproben treffen genau die Fälle, an denen die jeweilige Prüfung zu breit hätte werden
können.

## 2. Ausgeführter Befehl und Ergebnis

```text
python leitwerk-core/tests/scripts/validate-framework.py
→ Ergebnis: 0 Fehler, 0 Warnungen

python leitwerk-core/tests/scripts/probe-pruefungen.py .
→ alle Sonden und Gegenproben bestanden
```

## 3. Sonden und Gegenproben im Einzelnen

| Prüfung | Art | Gesetzter Defekt beziehungsweise erlaubter Fall | Ergebnis |
|---|---|---|---|
| 18 (erweitert) | Sonde | Die Laufzeit-README der Vorlage führt `hooks.v1.json` wieder als **geliefertes Artefakt** in der Dateitabelle | gemeldet |
| 18 (erweitert) | Gegenprobe | Dieselbe Datei nennt den Namen im **Fließtext**, um seine Abwesenheit zu erklären (der Migrationshinweis) | nicht beanstandet |
| 19 | Sonde | Im Pack `devin-desktop` wird der Abschnitt „Anweisungs- und Konfigurationsquellen außerhalb des Projekts" entfernt | gemeldet |
| 19 | Sonde | Im Pack `claude-code` wird jedes Datum des Abschnitts unkenntlich gemacht – die Auskunft bleibt, der Erhebungsstand fällt weg | gemeldet |
| 19 | Gegenprobe | Die Vorlage `_template` führt den Abschnitt mit `<TBD>`-Erhebungsstand | nicht beanstandet |
| 20 | Sonde | `PLACEHOLDER_REGISTRY.md` führt für `<SKILLS_DIR>` einen anderen Wert als das Manifest | gemeldet |
| 20 | Sonde | `RUNTIME_GLOSSARY.md` führt für „Agentenprofile" einen anderen Wert als das Manifest | gemeldet |
| 20 | Gegenprobe | Unverändertes Repositorium: „Nutzerlokale Überschreibung" hat kein Manifestfeld, und bei beiden Packs zeigt die Hook-Konfiguration auf die Berechtigungsdatei | nicht beanstandet |
| 21 | Sonde | `hook-overlay-status.py` liest wieder `os.environ.get("<Projektvariable eines Packs>")` | gemeldet |
| 21 | Sonde | Dasselbe Skript baut einen Kandidatenpfad aus der Laufzeitschicht eines Packs | gemeldet |
| 21 | Gegenprobe | `hook-check-secrets.py` nennt die Laufzeitpfade **beider** Packs in seinen Schutzmustern – Absicht, und dort wird kein Pfad hergeleitet | nicht beanstandet |
| 22 | Sonde | In der installierten Berechtigungsdatei wird ein Wert der Importsteuerung umgedreht (`windsurf: false` → `true`) | gemeldet |
| 22 | Sonde | Die Importsteuerung wird aus der installierten Berechtigungsdatei entfernt | gemeldet |
| 22 | Gegenprobe | Ein Pack ohne `import_control` (`claude-code`, bewusst ohne Vorgabe) | nicht beanstandet |
| 23 | Sonde | Der normative Satz über den Änderungsprozess wandert zurück in den Kopfkommentar der Wurzel-Anweisungsdatei | gemeldet |
| 23 | Sonde | Eine installierte Regeldatei bekommt einen HTML-Kommentar mit „MUSS" | gemeldet |
| 23 | Gegenprobe | Unverändertes Repositorium: Herkunftsangaben (Ebene, Version, Owner, Ladeverhalten) stehen weiterhin im Kommentar | nicht beanstandet |
| 24 | Sonde | In die Vorlage der Regelablage wird eine erklärende `README.md` gelegt – genau der Zustand vor 0.26.0 | gemeldet |
| 24 | Gegenprobe | In dieselbe Vorlage wird ein Regeltext nach Nummernschema gelegt (`40-tech-beispiel.md`) | nicht beanstandet |

## 4. Bedingungen dieses Nachweises

Nach Nummer 7 des Testkatalogs, die mit demselben Release in Kraft tritt:

- **Der Lauf ist belegt, nicht erschlossen.** Jede Zeile oben stammt aus der Ausgabe des
  Skripts; der Lauf endet mit einem Ergebnissatz, nicht mit einem Exit-Code allein.
- **Jede Abwesenheitsaussage hat eine Positivkontrolle.** Die Gegenproben sind genau das:
  Sie belegen, dass derselbe Lauf, der nichts meldet, überhaupt etwas melden **könnte** –
  die zugehörige Sonde im selben Durchgang.
- **Keine Schutzvorkehrung war abgeschaltet.** Der Nachweis ist statisch und braucht
  weder einen laufenden KI-Client noch eine aufgehobene Vertrauensprüfung.

## 5. Was dieser Nachweis nicht leistet

**Er belegt, dass die Prüfungen wirken – nicht, dass ihre Gegenstände richtig sind.** Die
Grenze jeder einzelnen Prüfung steht in deren Kopfkommentar in `validate-framework.py`
und ist dort **vorab** benannt, nicht nachträglich gefunden:

- Prüfung 19 prüft die **Anwesenheit** der Quellenauskunft, nicht ihre Richtigkeit. Ein
  Abwesenheitsbeleg altert; dieses Skript sieht den Unterschied nicht.
- Prüfung 20 prüft **Übereinstimmung** von Tabelle und Manifest. Steht im Manifest ein
  falscher Pfad, sind danach beide einig und beide falsch.
- Prüfung 21 prüft **Skripte, nicht Wirkung**. Ein Hook mit sauber übergebenen Pfaden,
  der trotzdem den falschen Status meldet, fällt ihr nicht auf.
- Prüfung 22 prüft **Anwesenheit und Übereinstimmung, nicht Wirkung**. Dass die
  Importsteuerung in der Datei steht, heißt nicht, dass sie greift: Die
  Benutzerkonfiguration der Arbeitsstation hat Vorrang (K-27).
- Prüfung 23 ist eine **Wortlistenprüfung**; eine zutreffende Erwähnung im Kommentar
  meldet sie mit. Gemessen ist außerdem ein Client und zwei Dateiarten (K-28 offen).
- Prüfung 24 prüft die **Vorlage**, nicht die installierte Ablage.

## 6. Gegenzeichnung

| Rolle | Datum | Ergebnis |
|---|---|---|
| Ersteller des Nachweises (KI-gestützt, Sitzung) | 2026-09-11 | alle Sonden gemeldet, keine Gegenprobe beanstandet |
| `<FRAMEWORK_OWNER>` | `<TBD>` | `<TBD>` |

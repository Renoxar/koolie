# Änderungsantrag `CR-2026-054`

| Feld | Inhalt |
|---|---|
| Titel | Die Aktivierung verlangte einen Lauf, der Aktivität voraussetzt – und der Status-Hook entschied sie nach der ersten Datei |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-13 |
| Betroffene Artefakte | `tests/scripts/validate-framework.py` (neuer Schalter `--check-overlay-ready`, Prüfung 9a), `tests/scripts/overlay_status.py` (neu), `tests/scripts/hook-overlay-status.py`, `templates/project-overlay/OVERLAY.md` (Abschnitt 21), `checklists/10-project-adoption.md`, `docs/ADOPTION_GUIDE.md` (Schritte 7 und 9), `tests/scripts/probe-pruefungen.py` |
| Ebene laut Entscheidungsbaum 6 | **Kern** – Prüfwerkzeug, Hook und Übernahmeablauf; das ausgefüllte Overlay bleibt Ebene 4 |
| Art | Befund **B08** des unabhängigen Reviews vom 2026-09-12, P2; **gegengeprüft, bestätigt und um einen Defekt erweitert** |
| Dringlichkeit | **Paket 5**; Voraussetzung B02 ist seit 0.28.0 erfüllt |

## 1. Anlass und Problem

### 1.1 Die Zirkularität ist im Ablauf dreifach verankert

| Stelle | Aussage |
|---|---|
| `docs/ADOPTION_GUIDE.md` Schritt 7 | fährt `validate-framework.py --strict-overlay` |
| `docs/ADOPTION_GUIDE.md` Schritt 9 | setzt den Overlay-Status **danach** auf `aktiv` |
| `checklists/10-project-adoption.md`, Kopfzeile „Wann“ | gilt „**vor** dem Setzen des Overlay-Status auf `aktiv`“ |
| ebenda, MUSS-Punkt | verlangt denselben Lauf ohne Fehler |
| `templates/project-overlay/OVERLAY.md` Abschnitt 21 | Status wird `aktiv`, **wenn** Checkliste **und** Lauf durch sind |

`check_strict_overlay` verlangt den Status **genau** `aktiv`, und zwar in beiden Trägern – seit
0.28.0 als Aufzählung statt als Präfix, weil `aktivierung-ausstehend` vorher bestand (D-44). Der
dokumentierte Ablauf ist damit **nicht ohne Regelbruch begehbar**: Wer ihn befolgt, setzt `aktiv`,
bevor die Übernahmecheckliste fertig ist – und ein Agent arbeitet dann regelkonform in M3 auf
einem unfertigen Overlay.

### 1.2 Eigene Feststellung: Der Name der gesuchten Prüfung steht längst da

`docs/ADOPTION_GUIDE.md` Zeile 145 nennt den Lauf „prüft Struktur, Inhalte und
**Aktivierungsreife** des Overlays“. Der Docstring von `check_strict_overlay` nannte ihn ebenso
„Aktivierungsreife des Projekts“. **Beide beschreiben eine Kandidatenprüfung; die Umsetzung
verlangt den fertigen Zustand.** Es fehlt kein Begriff – es fehlt die Prüfung dazu. Das verschiebt
den Zuschnitt des Antrags: Nicht ein neues Konzept wird eingeführt, sondern eine Prüfung gebaut,
die zwei Dokumente seit je beschreiben.

### 1.3 Eigene Feststellung: Der Status-Hook trägt drei Defekte, nicht zwei

Das Review nennt zwei (nur die erste Angabe, kein Tabellenformat). Am Skript nachgelesen sind es
drei:

| Nr. | Defekt | Fundstelle | Folge |
|---|---|---|---|
| 1 | `value.startswith("aktiv")` – **Präfixvergleich** | `hook-overlay-status.py:54` (0.32.0) | `aktivierung-ausstehend` wird als `aktiv` gemeldet. **Genau der Defekt, den D-44 im Validator behoben hat** – die Lehre wurde in einer Funktion gezogen und nicht zur Nachbarin getragen, wie bei D-49 |
| 2 | Suchmuster verlangt einen Doppelpunkt | `:51` | Die Steckbriefzeile `\| Overlay-Status \| … \|` wird **nie** getroffen |
| 3 | `break` nach dem ersten Treffer | `:60` | Eine aktive Laufzeitregel gewinnt gegen ein inaktives Quell-Overlay |

Die gemeinsame Auswertung existiert seit 0.28.0 im Validator (`_overlay_status_angaben`) – der
Hook benutzt sie nicht.

## 2. Vorgeschlagene Änderung

1. **Neuer Schalter `--check-overlay-ready`** (Prüfung 9a): prüft denselben Inhalt wie
   `--strict-overlay` – offene Werte, sicherheitsrelevante Abschnitte, Berechtigungsdatei ohne
   Platzhalter – und beim Status **das Gegenteil**: Er muss an allen Stellen übereinstimmen und
   noch **nicht** `aktiv` sein. Ein bereits aktives Overlay wird als Fehler gemeldet, mit Verweis
   auf `--strict-overlay`.
2. **`--strict-overlay` bleibt unverändert** die Prüfung des aktiven Zustands. Nur sein Docstring
   hört auf, sich Reifeprüfung zu nennen.
3. **Der Ablauf wird begehbar:** Leitfaden Schritt 7 und die Checkliste fahren die
   Kandidatenprüfung; nach dem Setzen auf `aktiv` folgt ein Nachlauf mit `--strict-overlay`. Die
   Overlay-Vorlage führt die Reihenfolge in fünf Schritten.
4. **Ein gemeinsames Modul `tests/scripts/overlay_status.py`** trägt die Auswertung. Validator und
   Hook importieren es; **der Hook importiert nicht den Validator.**
5. **Der Hook wertet alle Träger aus**, vergleicht exakt statt als Präfix, kennt beide
   Schreibweisen und meldet einen Widerspruch als **`widerspruechlich`** – nicht als `inaktiv` und
   nicht als `unbekannt`. Die Folge ist dieselbe (nur lesend), der Grund nicht.

## 3. Was dieser Antrag nicht ändert

- **Er erteilt keine fachliche Freigabe.** Die Kandidatenprüfung prüft Vollständigkeit; die
  Übernahmecheckliste bleibt der Nachweis, und ein Skript kann sie nicht abschließen.
- **Er prüft keine Richtigkeit.** Ein vollständig ausgefülltes Overlay mit falschen Werten besteht
  die Prüfung.
- **Er ändert den Hook nicht zu einer Schranke.** Er informiert weiterhin und blockiert nie; ohne
  zusätzliche Werkzeugkontrolle bleibt es dabei.
- **Er löst den Abgleich zwischen Quell-Overlay und Laufzeitfassung nicht** (`CR-2026-044` E4).
  Geprüft wird jetzt der **Status** an allen Stellen, nicht der gesamte Inhalt.

## 4. Prüffragen

- [x] Richtige Ebene: Kern. Prüfwerkzeug, Hook, Übernahmeablauf.
- [x] Verschärfungsprinzip: **verschärft.** Der Hook hört auf, `aktivierung-ausstehend` als aktiv
      zu melden, und eine Drift führt nicht mehr zur günstigeren der beiden Aussagen.
      `--strict-overlay` behält seine Strenge unverändert – **das war der Grund, ihn nicht
      umzudeuten.**
- [x] Widerspruchsfreiheit: D-23, D-44 (Aufzählung statt Präfix), D-49 (eine Lehre gilt auch für
      die Nachbarfunktion), D-30 (Hook-Skripte ohne clientgebundene Ableitung – das neue Modul hat
      keine), `framework/runtime/root-instruction.md` Abschnitt 3 gelesen.
- [x] Laufzeitfassungen: Die Hook-Konfiguration ändert sich **nicht** – derselbe Aufruf, dieselben
      Argumente. Das Skript liegt im Kern und kommt mit `--update`.
- [x] Belegstatus: **im Code gegengeprüft**; die drei Hook-Defekte sind am Skript nachgelesen, die
      Zirkularität an fünf Textstellen und an `check_strict_overlay`.
- [x] Test- und Validierungsbedarf: **sechs Sonden und zwei Gegenproben je Pack** – drei und
      eine für die Kandidatenprüfung, drei und eine für den Hook. Die Sonde zum Fetch-Verbot
      gehört zu `CR-2026-055`.
- [x] Overlays: Ein bestehendes, aktives Overlay ist **nicht** betroffen; `--strict-overlay` sagt
      dort weiterhin dasselbe. Betroffen ist jede **künftige** Übernahme.
- [ ] Dokumentation: `CHANGELOG.md`, Decision Log (D-57, D-58), Roadmap, Leitfaden, Checkliste.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Wie wird die Zirkularität aufgelöst? | **Neuer Schalter für den Kandidaten, `--strict-overlay` bleibt.** Er hat mit dem Aktualisierungsablauf einen zweiten, funktionierenden Aufrufer; ihn umzudeuten hieße, jeder bestehenden Projekt-CI stillschweigend eine andere Prüfung zu geben – der Befundtyp dieses Projekts | Eine neue CLI-Oberfläche und ein zweiter Prüfpfad, der mitgepflegt werden muss. Der Docstring muss aufhören, `--strict-overlay` Reifeprüfung zu nennen |
| E2 | Was erwartet die Kandidatenprüfung beim Status? | **Übereinstimmung an allen Stellen und „noch nicht `aktiv`".** Ein bereits aktives Overlay ist ein Fehler mit Verweis auf `--strict-overlay` | Man kann die Prüfung nicht auf ein aktives Overlay anwenden, um dessen Vollständigkeit zu sehen. Das ist gewollt: Eine Prüfung, die zwei Zustände gleich behandelt, unterscheidet keine zwei Zustände – und wäre als schwächerer Ersatz für `--strict-overlay` benutzbar |
| E3 | Wie weit wird der Hook nachgezogen? | **Ganz, über ein gemeinsames Modul.** Alle drei Defekte; der Präfixvergleich ist derselbe, den D-44 im Validator ausgeschlossen hat. Ein Modul statt eines Imports des Validators: Ein Hook, der bei jedem Sitzungsstart 2300 Zeilen lädt, wäre ein Leistungs- und ein Fehlerrisiko | Eine neue Datei im Kern. **Die Alternative – nur den Präfixvergleich berichtigen – hätte zwei von drei Defekten stehen gelassen**, und die Drift ist der, den das Review beschreibt |
| E4 | Was meldet der Hook bei Widerspruch? | **`widerspruechlich`**, mit M1-Hinweis. `inaktiv` und `unbekannt` verschweigen beide, dass eine Erklärung da ist und nicht stimmt; wer die Meldung liest, suchte dann einen fehlenden Eintrag | Eine dritte Statusaussage im Hook-Text. Sie kostet nichts – der Hook gibt Fließtext aus, keinen Aufzählungswert |
| E5 | Wie wird nachgewiesen, dass die Prüfung nicht alles meldet? | **Über die Gegenprobe, und sie ist hier die wichtigere Hälfte:** ein vollständig ausgefüllter Kandidat mit Status `inaktiv` muss **durchlaufen**. Ohne sie stünde nur fest, dass irgendetwas gemeldet wird | Der Kandidat muss in der Sonde erst hergestellt werden – Platzhalter ersetzen, Status setzen, Berechtigungsdatei bereinigen. Das macht den Sondenlauf länger |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle fünf Fragen wie vorgelegt.** E1 neuer Schalter `--check-overlay-ready`, `--strict-overlay` bleibt; E2 Übereinstimmung und „noch nicht aktiv"; E3 der Hook wird vollständig nachgezogen, über ein gemeinsames Modul; E4 ein Widerspruch wird als solcher gemeldet; E5 Nachweis über die Gegenprobe des vollständigen Kandidaten |
| Datum | 2026-09-13 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | D-57 (Kandidatenprüfung und aktiver Zustand sind zwei Prüfungen), D-58 (eine Statusauswertung für beide Werkzeuge) |
| Auflagen | **Der Präfixvergleich im Hook ist mitzuberichtigen, obwohl das Review ihn nicht nennt.** Er ist wörtlich derselbe Defekt, den D-44 im Validator behoben hat; ihn stehenzulassen hieße, dieselbe Lehre zum zweiten Mal nicht zu übertragen. **Die Sonden laufen je Pack** – B02 war nicht, dass eine Prüfung falsch prüft, sondern dass sie einen Client nicht sieht. **Nachgewiesen:** sechs Sonden und zwei Gegenproben je Pack, zusammen zwölf und vier; die Gegenprobe des vollständigen Kandidaten belegt, dass die Prüfung nicht pauschal meldet. **Offen bleibt:** Der Abgleich des gesamten Inhalts zwischen Quell-Overlay und Laufzeitfassung (`CR-2026-044` E4) – geprüft wird der Status, nicht jedes Feld |
| Ziel-Release | `0.33.0` |
| Umsetzung | umgesetzt mit `0.33.0` |

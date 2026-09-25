# Protokoll: Der Installer je Zielsystem – und die Prüfung, die ohne PyYAML Fehler erfand

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-25 |
| Release | `1.7.0` |
| Änderungsantrag | `CR-2026-140` |
| Art | Neuer Übernahmeweg (Starter, Dialog, `install.py --target`), korrigierte Prüfung, erweiterter Prüfapparat – **keine Sitzung, kein Kontingent, kein Modelllauf** |
| Gegenstand | Die Starter unter Windows, Git Bash und Linux; `--target` aus beiden Quellformen; die Mindestversion an Python 3.8 und 3.14; Prüfung 33 ohne PyYAML; beide übernehmenden Projekte, zum ersten Mal über das Werkzeug gehoben |
| Ergebnis | 🟢 **Entschieden, `D-362` bis `D-366`.** Installation über `--target` Datei für Datei gleich dem Handweg; Python 3.8 gemessen. 🔴 **Prüfung 33 erfand ohne PyYAML neun Fehler je `claude-code`-Installation** – behoben; 🔴 **die Starter lagen außerhalb des Prüfapparats** – aufgenommen, und die Inhaltsprüfung schlug sofort an. ⚠️ **Abnahme auf macOS offen** |

---

## 1. Was gefragt war

Wiederaufnahmepunkt von `1.6.0`, Punkt 2: der Installer je Zielsystem, Fokus Windows und
macOS (Vorgabe des Owners vom 2026-09-25). Vor dem Bau vorgelegt als Fragen (a) bis (j);
(a) bis (i) angenommen, (j) – die Abnahme auf macOS – offen. `CR-2026-140` E1 bis E11.

## 2. Messungen

Alle Messungen an Wegwerf-Verzeichnissen außerhalb des Repositoriums.

### 2.1 Vor dem Bau

| Messung | Ergebnis | Folge |
|---|---|---|
| `Get-ExecutionPolicy -List` am Arbeitsplatz | `LocalMachine AllSigned`, `CurrentUser RemoteSigned` | Starter als `.cmd`, nicht `.ps1` |
| Python-Fundorte | `C:\Python314\python.exe`, **`WindowsApps\python.exe`** (Store-Platzhalter), `py.exe` | Versionsprobe statt Namensprobe |
| Dateimodi im Repositorium | **kein** Träger mit `100755` | `install.command` bekommt ihn, Sonde |
| Kernumfang nach Verzeichnis | `tests/` 179 Dateien – **darin Hooks und Validator** (`tests/scripts/`) | Lieferumfang nicht in `1.7.0` (D-366) |
| Statische Analyse der Werkzeuge (`vermin`) | Untergrenze 3.7 | gemessen wird 3.8 (3.7 nicht beschaffbar) |

### 2.2 Die Mindestversion: 3.8 gegen 3.14

| Messung | Ergebnis |
|---|---|
| Installation je Pack mit `--overlay general`, 3.8.20 gegen 3.14.4 | **alle drei byteweise gleich** |
| Validator mit PyYAML gegen dieselbe Installation, je Pack | **zeilengleich** (je 8 Fehler, 5 Warnungen – die eines Projekts ohne README und Commit) |
| Alle 41 Python-Träger des Repositoriums unter 3.8 kompiliert | **0 Syntaxfehler** |
| 🔴 **Validator OHNE PyYAML, je Pack** | `devin-desktop`, `openai-codex`: nur die PyYAML-Warnung mehr. **`claude-code`: neun Fehler mehr** – `disallowed-tools traegt []` an neun Skills |

Die neun Fehler sind falsch: Die installierten `SKILL.md` tragen die Liste
(`disallowed-tools: Edit, Write, NotebookEdit, Bash`). Prüfung 33 las aus dem Rohtext,
den `parse_frontmatter` ohne PyYAML liefert, mit `.get()` nichts. Nach dem Rückfall
`_flaches_feld()`: ohne PyYAML dieselben Meldungen wie mit, bis auf die Warnung; eine auf
`Edit` verkürzte Liste wird weiter gemeldet.

### 2.3 `--target` gegen den Handweg

| Lauf | Ergebnis |
|---|---|
| `--target` (Klon, `claude-code`, `--overlay general`), danach `--update`, gegen `git ls-files \| tar` + `install.py` | **Datei für Datei gleich** (`diff -r` ohne `__pycache__`, `.git`) |
| Kennzeichen, Overlay der Quelle | nicht mitkopiert |
| Zweiter Aufruf ohne `--update` | Abbruch, *„Heben auf diesen Stand: --update“* |

### 2.4 Die Starter

| Lauf | Ergebnis |
|---|---|
| `install.cmd`, Eingabe umgeleitet, Projektpfad `C:\lw-mig\zieltest\Pröjekt (x86) neu` (Leerzeichen, Umlaut, Klammer, Anführungszeichen wie beim Hineinziehen) | installiert (`devin-desktop`, `--overlay general`) |
| `install.cmd`, `PATH` nur `System32` und `WindowsApps` | Platzhalter übergangen, *„Koolie braucht Python 3.8 oder neuer“*, Exit 1 |
| `install.cmd`, `PATH` mit nur Python 3.8.20 | angenommen, installiert |
| `install.command` (Indexfassung, LF) in Git Bash, Quelle ohne Git | installiert, Kopie *„Verzeichnis – ohne `__pycache__` und `build/out`“* |
| `install.command` unter WSL (`sh` = `dash`, Python 3.12.3) | installiert |
| ⚠️ **macOS** | **nicht gemessen** – die Abnahme steht aus |

⚠️ **Nebenbefund am Meßaufbau:** Eine in cp1252 geschriebene Eingabedatei kam mit
verstelltem Umlaut an – die Sitzung setzt `PYTHONIOENCODING=utf-8`, und Python liest
umgeleitete Eingabe dann als UTF-8. Mit UTF-8-Eingabe bestanden. Eine echte
Konsoleneingabe liest Python über die Konsolenschnittstelle; sie ist davon nicht
betroffen.

### 2.5 Der Prüfapparat an den Startern

Nach der Aufnahme von `.cmd` und `.command` in `TEXT_EXT` meldete der erste
Validatorlauf **`FW-CONTENT-URL`** in beiden Startern (die Downloadseite von python.org
mit Schema). Die Starter nennen seither `python.org` ohne Schema. Vorher hatte keine
Prüfung die Dateien gelesen.

### 2.6 Die Projekte

Beide zum ersten Mal mit `install.py --target <projekt> --update` gehoben, aus dem
Arbeitsbaum des Frameworks:

| Projekt | Kern | `--strict-overlay` | Overlay |
|---|---|---|---|
| Pilot (`claude-code`) | 549 Dateien, **0 abweichend** gegen `git ls-files` des Frameworks, keine Reste | **1/2** (projekteigenes `CHANGELOG.md`, unverändert); Auskunft weiterhin **38** | `0.3.12` |
| Übungsrepositorium (`devin-desktop`) | 549 Dateien, **0 abweichend**, keine Reste | **0/1** (Laufzeitfassung 6.095 Zeichen, unverändert) | `1.4.6` |

## 3. Wirkungsnachweis – Sonden und Gegenproben, mit Gegenbeweis

| Einheit | Stand `1.7.0` | Gegenbeweis |
|---|---|---|
| `T362`, `T362a` | OK | mit `install.py` aus `1.6.0`: **je FEHL** (Exit 2, `--target` unbekannt); danach bricht das Bündel ab |
| `T362b` bis `T362h` | OK | mit `install.py` aus `1.6.0`: nicht mehr erreicht – das Bündel bricht nach `T362a` ab |
| `T363` | OK | an einem Starter mit `(3, 7)`: **FEHL** |
| `T365` | OK | an einem Starter mit `goto`/Sprungmarke und `install.command` auf `100644`: **FEHL**, alle drei Stellen genannt |
| `S364`, Gegenprobe `S364a` | OK | mit dem Validator aus `1.6.0`: **je FEHL** (`S364a`: *„PyYAML gesperrt True, still False“*) |
| Sonden `6s` (beide Starter) | OK | mit dem Validator aus `1.6.0`: **je FEHL** – er liest `.cmd` und `.command` nicht |

Der Gegenbeweis läuft an einer **vollständigen** Kopie des Arbeitsbaums mit den
Werkzeugen aus `v1.6.0`.

## 4. Abnahme

| Lauf | Ergebnis |
|---|---|
| Validator | **0 Fehler, 0 Warnungen**, beide Kodierungsumgebungen |
| Sondenlauf | **334 Einheiten, alle bestanden** (vorher 330; neu die Bündel `sonden_kopierweg` und `sonden_ohne_pyyaml` und die beiden Sonden `6s`), beide Kodierungsumgebungen Exit 0 und oberhalb der Trennlinie zeilengleich (559 Zeilen), rund 550 s Wanduhr je Lauf; **Abnahmelauf gegen den fertigen Baum zeilengleich** |
| Sondenlauf unter **Python 3.8.20** (mit PyYAML), an einer Kopie des Baums | **334 Einheiten, alle bestanden**, Exit 0, oberhalb der Trennlinie **zeilengleich zum Lauf unter 3.14** – der Prüfapparat samt Hooks läuft unter 3.8 wie unter 3.14 (rund 610 s Wanduhr) |
| Pilot / Übungsrepo `--strict-overlay` nach der Hebung | Pilot **1 Fehler, 2 Warnungen**, alle im projekteigenen `CHANGELOG.md`, unverändert; Übungsrepo **0 Fehler, 1 Warnung** (Laufzeitfassung 6.095 Zeichen, unverändert); Auskunft im Pilot weiterhin **38** |
| Bau | alle drei Word-Fassungen `v1.7.0` in `build/out/` (2.059.134 / 2.060.426 / 2.055.083 Bytes für `devin-desktop` / `claude-code` / `openai-codex`), im Erzeugnis nachgezählt: Dokumentversion `1.7.0`, *„89 Prüfungen“*, je sechsmal `install.cmd`, fünfzehnmal `--target`, zweimal `install_dialog.py` |

## 5. Nebenhandlungen außerhalb des Kerns

- Signierte Marke `v1.6.0` (vom Owner gesetzt, `Good "git" signature`) **vor** dem
  Gitea-Release gepusht, remote annotiert. Schritte 5 bis 7 aus `RELEASE_PROCESS.md` 4.1:
  `koolie-1.6.0.tar.gz`, **552 Dateien** = `git ls-tree` der Marke, kein CRLF (bytegenau
  gezählt), Lizenz an beiden Stellen gleich, kein `build/out/`; Gitea-Release mit Archiv
  und Prüfsumme, beide Anhänge bytegleich zurückgelesen.
- Für die Messung der Mindestversion ist Python 3.8.20 über `uv` in das Benutzerprofil des
  Meßplatzes installiert worden – außerhalb des Repositoriums.

## 6. Offen und benannt

- 🔴 **Die Abnahme des macOS-Starters auf macOS** (Doppelklick im Finder, Gatekeeper,
  `/usr/bin/python3` ohne Command Line Tools).
- Der Starter prüft das Python, mit dem er installiert; die Hooks wählen ihren
  Interpreter bei der Installation selbst. Ob beides dieselbe Fassung ist, prüft keine
  Stelle.
- Der wählbare Lieferumfang – Ziel-Release `1.8.0` (D-366).
- SmartScreen und Gatekeeper warnen vor den unsignierten Startern; gemessen ist keine der
  beiden Warnungen.

# Protokoll: Die Frage nach dem einen Ort der Overlay-Werte – und der Träger, den sie dafür vorschlug, trägt sie nicht

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-24 |
| Release | `1.4.3` |
| Änderungsantrag | `CR-2026-136` |
| Art | Einordnung eines Klärungspunkts – **keine Sitzung, kein Kontingent, kein Modelllauf**, kein Werkzeug geändert |
| Gegenstand | `K-120` (Overlay-Werte an einem Ort, Erzeugen bei `--update`) und was daraus für `1.5.0`, `K-67`, `K-69` und `K-121` folgt |
| Ergebnis | 🟢 **Entschieden, `D-353`.** 🔴 **Der vorgeschlagene Träger trägt die Werte nicht.** 🔴 **Ein Erzeugen hätte 37 Projekteinträge überschrieben.** 🔴 **Ein vorbefülltes Muster erreicht die Berechtigungsdatei nicht** – gemessen, mit Gegenprobe |

---

## 1. Was gefragt war

Wiederaufnahmepunkt von `1.4.2`, Punkt 2: `K-120` einordnen, bevor `1.5.0` beginnt – ob
`--update` Laufzeitfassung und Berechtigungsdatei aus `overlay-manifest.yaml` rendert.
`K-121` hängt mit Frage (3) daran.

## 2. Messungen

### 2.1 Wo die Werte stehen

Gelesen: `templates/project-overlay/overlay-manifest.yaml` und die installierten Fassungen
in `devpacks/otp-generator` und `devpacks/test-devin-framework`. Von den Projektwerten
führen alle drei nur `overlay_version` (dazu `project_code`); **kein** Pfad- oder
Befehlswert. Die Werte stehen in `OVERLAY.md` Abschnitt 4 bis 6, in beiden Projekten als
dreispaltige Zeile mit dem Platzhalternamen in der mittleren Zelle – **alle fünf
Pfadplatzhalter** (Pilot Zeilen 71–75, Übungsrepositorium 78–82).

| Wert | Träger |
|---|---|
| Overlay-Version | `OVERLAY.md`, `overlay-manifest.yaml`, Laufzeitfassung |
| Pfad- oder Befehlswert | `OVERLAY.md`, Laufzeitfassung, Berechtigungsdatei |

### 2.2 Berechtigungsdatei: gerenderte Kernquelle gegen Projekt

`install.render_for_client()` auf `framework/runtime/permissions.json` für das Pack des
Projekts, als Menge je Korb gegen die Projektdatei gehalten (Stand `1.4.2`):

| Korb | Pilot `claude-code`: nur Projekt | nur Kern | Übungsrepo `devin-desktop`: nur Projekt | nur Kern |
|---|---|---|---|---|
| `allow` | 0 | 0 | 0 | 0 |
| `ask` | 2 (Build, Test) | 3 (die drei Schlitze) | 3 (Build, Lint, Test) | 3 (die drei Schlitze) |
| `deny` | 10 | 4 (Schlitze) | 22 | 4 (Schlitze) |

**Zuordnung der 37 Einträge, die nur im Projekt stehen:**

| Herkunft | Pilot | Übungsrepo |
|---|---|---|
| gefüllter Schlitz der Kernquelle (`<EXCLUDED_PATHS>`, `<CI_CONFIG_PATHS>`, `<QUALITY_GATE_CONFIG_PATHS>`, Befehle) | 10 | 20 |
| Umsetzung von `<READ_ONLY_PATHS>` als Schreibsperre – **kein Schlitz der Kernquelle** | 2 | 2 |
| Projektzusatz ohne Platzhalter | 0 | 3 (`Exec(mvn deploy)`, `Exec(npm install)`, `Exec(npm uninstall)`) |
| **Summe** | **12** | **25** |

Dazu hat der Pilot **zwei** Kerneinträge entfernt, weil sein Wert „nicht vorhanden“ ist
(`Edit(<QUALITY_GATE_CONFIG_PATHS>)`, `Bash(<LINT_COMMAND>)`).

### 2.3 Laufzeitfassung: Anteil der Projektprosa

Codespannen entfernt, dann `diff` gegen `framework/runtime/rules/20-project-overlay.md`:

| | Zeilen | davon abweichend | mit gebundenem Platzhalter |
|---|---|---|---|
| Vorlage | 60 | – | 12 |
| Pilot | 91 | **59** | 8 |
| Übungsrepositorium | 78 | **48** | 5 |

### 2.4 Ein vorbefülltes Muster nach der Erstinstallation – mit Gegenprobe

Kern aus dem Arbeitsbaum (`git ls-files -z .koolie/core | tar`) in ein Wegwerf-Verzeichnis
im Scratchpad, `git init`, `install.py --client claude-code`. Danach in `OVERLAY.md` und in
der Laufzeitfassung `<EXCLUDED_PATHS>` auf `deploy/**` gesetzt – so, wie ein Muster mit
vorgeschlagenen Werten es ausliefern würde. `validate-framework.py --strict-overlay`:

| Lauf | Berechtigungsdatei | Meldung zu `EXCLUDED_PATHS` |
|---|---|---|
| A | wie installiert: `Read(<EXCLUDED_PATHS>)`, `Edit(<EXCLUDED_PATHS>)` wörtlich | `.claude/settings.json: enthält noch Platzhalter` – **Prüfung 59 enthält sich** (`return  # Schlitz noch ungefuellt`) |
| B (Gegenprobe) | beide Einträge auf `deploy/**` gefüllt | die Platzhaltermeldung bleibt wegen der übrigen Schlitze stehen, **Prüfung 59 meldet nichts** – der Wert ist gedeckt |
| C (Beleg, daß 59 in B läuft) | wie B, aber `Edit(deploy/**)` entfernt | **Prüfung 59 meldet:** *„der ausgeschlossene Pfad `deploy/**` des Quell-Overlays hat keine Regel Edit(deploy/**) im deny-Korb“* – 19 statt 18 Fehler |

⚠️ **Die Vermutung vor der Messung war falsch:** Erwartet war, Prüfung 59 schlage an. Sie
enthält sich, solange der Schlitz ungefüllt ist – der Befund wird dadurch nicht kleiner,
aber genauer: **Kein Werkzeug meldet, daß ein genannter Wert nicht sperrt; gemeldet wird
nur, daß noch Platzhalter stehen.**

## 3. Ein Fehler der Vorbereitung, benannt

Die erste Fassung der Vorlage machte `K-67` (eine verbindliche Bindungsform) zur
Voraussetzung von `1.5.0`. **Der Statusvermerk von `K-67` selbst nennt den Preis** – den
Umbau jeder bestehenden Overlay-Datei –, und das ist nach `RELEASE_PROCESS.md`
Abschnitt 1 MAJOR. Gefunden beim Eintragen des Vermerks, vor der Entscheidung. Berichtigt:
Der Füllschritt liest das Muster, dessen Form das Framework festlegt, und braucht `K-67`
nicht (`CR-2026-136` 2.5, E4). ➡️ *Wer eine Voraussetzung einplant, liest ihren Preis in
ihrem eigenen Eintrag.*

## 4. Abnahme

| Lauf | Ergebnis |
|---|---|
| `validate-framework.py --root .` | **0 Fehler, 0 Warnungen** – mit und ohne `PYTHONIOENCODING=utf-8` |
| Sondenlauf mit und ohne `PYTHONIOENCODING=utf-8` | **324 Einheiten, alle bestanden**, Exit 0, oberhalb der Trennlinie zeilengleich (518 Zeilen). **Keine Einheit neu** – das Release ändert kein Werkzeug |
| Pilot `--strict-overlay` nach dem Heben | 1 Fehler, 2 Warnungen – alle im projekteigenen `CHANGELOG.md`, unverändert zu `1.4.2`; Auskunft über ignorierte Kerndateien weiterhin **38** |
| Übungsrepo `--strict-overlay` nach dem Heben | 0 Fehler, 1 Warnung (Laufzeitfassung 6.023 Zeichen), unverändert |
| Hauptdokument und Word-Fassung je Pack | alle drei gebaut: `claude-code` 2.093.189, `devin-desktop` 2.089.518, `openai-codex` 2.080.940 Zeichen; Dokumentversion `1.4.3`, D-353 je neunmal |

## 5. Offen

- 🔴 **Die signierten Marken `v1.4.0` bis `v1.4.3`** setzt der Framework Owner (D-321).
- **`1.5.0`** mit dem gewachsenen Umfang aus D-353.
- **`K-67`** (MAJOR-Kandidat), **`K-121`** Fragen (1) und (2).

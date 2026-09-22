# Migrationslauf: der Pilot von 0.41.0 auf 0.46.0 – und was daneben lag

| Feld | Wert |
|---|---|
| Gegenstand | **Kandidat 4 der Übergabe:** „Den Piloten heben und seinen Befund auflösen." Fünf Releases, 0.41.0 bis 0.46.0 |
| Anlass | Der Pilot (`devpacks/otp-generator`) stand fünf Releases zurück. **Der zweite echte Migrationslauf dieses Projekts** – der erste war 0.37.0 auf 0.41.0 am 2026-09-14 |
| Datum | 2026-09-15 |
| Prüfmethode | Der dokumentierte Weg aus `docs/ADOPTION_GUIDE.md` Abschnitt 3, mit einem Validatorlauf **vor**, **zwischen** und **nach** den Nacharbeiten. Die beiden Vorhersagen der Migrationshinweise werden **geprüft**, nicht geglaubt |
| Umgebung | Windows 11, Python 3.14.4; Pilot als Arbeitskopie, `core.autocrlf=true` |
| Ergebnis | **Beide Vorhersagen treffen.** Daneben ein Befund, den niemand gesucht hat und der nicht dem Piloten gehört: **versionierter Bytecode des Kerns, in zwei von zwei Projekten** |

## 0. Der Lauf in einem Satz

**Der Migrationshinweis von 0.44.0 hat den Piloten namentlich angekündigt – und er hat
recht; der Befund, der wirklich zählt, stand daneben und in keinem Hinweis.**

## 1. Der Ausgangsstand

| Messung | Wert |
|---|---|
| `leitwerk-core/VERSION` des Piloten | `0.41.0` |
| Validator des Piloten, `--strict-overlay` | **1 Fehler, 3 Warnungen** |
| `install.py --check` (aus dem Zielstand, gegen den Piloten) | **eine** abweichende Kerndatei: `.claude/skills/fw-tests/TESTS.md`; 57 unverändert, 20 Projektdateien |
| `hooks`-Block in `.claude/settings.json` | vorhanden, ein `PreToolUse`-Kommando |

Der eine Fehler und die drei Warnungen betreffen sämtlich Projektinhalte des Piloten (ein
Sperrbegriff aus der eigenen Vorgeschichte, zwei Quellen-URLs) sowie die bekannte
Pfadwarnung über die Laufzeitschicht des nicht installierten Packs. **Sie sind der
Ausgangswert, gegen den am Ende gemessen wird.**

## 2. Der Weg

Nach `docs/ADOPTION_GUIDE.md` Abschnitt 3, in dieser Reihenfolge:

1. `leitwerk-core/` des Piloten durch den Zielstand ersetzt.
2. `python leitwerk-core/install.py --update` – **eine** Kerndatei aktualisiert, 57
   unverändert, 20 Projektdateien unberührt.
3. Validatorlauf **vor** den Nacharbeiten – die eigentliche Messung.

**Ein Nebenbefund am Werkzeug, der keiner ist.** `install.py --dry-run` **ohne**
`--update` bricht an einer bestehenden Installation mit einem Fehler ab: Er ist der
Trockenlauf einer *Erst*installation, und D-46 schützt dort vorhandene Projektdateien.
Die Meldung nennt den richtigen nächsten Schritt („Stammen sie aus einer früheren
Installation: `--update` verwenden"), also führt sie niemanden in die Irre. **Der
Trockenlauf einer Aktualisierung heißt `--update --dry-run`**, und er nannte dieselbe
eine Datei wie der echte Lauf.

## 3. Das Ergebnis der Messung

Validatorlauf am Piloten, Framework `0.46.0`, **vor** den Nacharbeiten:

| Meldung | Anzahl | Vorhergesagt von |
|---|---|---|
| `'Bash(mvn -B -q compile)' steht im ask-Korb, und kein Platzhalter des Overlays erklärt diesen Befehl` | **1** | Migrationshinweis 0.44.0 |
| `Kompatible Framework-Version '0.41.0' passt nicht zu leitwerk-core/VERSION (0.46.0)` | 1 | Adoption Guide, Abschnitt 3 |
| Projektinhalte des Piloten (Ausgangswert) | 1 Fehler, 3 Warnungen | – |
| **Gesamt** | **3 Fehler, 3 Warnungen** | |

### 3.1 Die erste Vorhersage: der Migrationshinweis von 0.44.0

Er lautet: *„Ein Projekt, dessen Berechtigungsdatei einen Befehl führt, den Abschnitt 5
oder 6 nicht für seinen Platzhalter erklärt, bekommt ab diesem Release einen Fehler. …
**Der Pilot ist genau dieser Fall** – eine Fundstelle, abgezählt."*

**Es ist genau eine.** Damit hat dieses Projekt zum zweiten Mal einen Hinweis über eine
fremde Installation eingelöst nachgerechnet – und zum zweiten Mal stimmt er.

### 3.2 Die zweite Vorhersage: Prüfung 43 schweigt

Die Übergabe sagte: *„beim Heben bekommt er zusätzlich Prüfung 43 zu sehen. Sein
`hooks`-Block ist vorhanden (geprüft), also sollte sie dort schweigen."* **Sie schweigt.**
Das ist eine Vorhersage über ein *Ausbleiben*, und sie ist schwächer als eine über eine
Meldung – belegt ist damit nur, dass Prüfung 43 hier nichts findet, nicht dass sie hier
etwas fände, wenn es etwas gäbe. Der Beleg dafür steht in den Sonden zu 43.

## 4. Die Auflösung – eine Entscheidung des Overlay Owners

Der Migrationshinweis sagt ausdrücklich: *„Die Auflösung ist eine Entscheidung des
Overlay Owners und keine des Frameworks: entweder die Zeile fällt, oder der Befehl wird
im Overlay als Wert des passenden Platzhalters erklärt."* Beide Wege wurden vorgelegt.

**Entschieden: Die Zeile fällt.** `Bash(mvn -B -q compile)` ist aus dem `ask`-Korb
genommen; der Befehl bleibt in Abschnitt 5 des Overlays gelistet und wirkt über die
Regelschicht.

| | Was dafür spricht | Was es kostet |
|---|---|---|
| **Die Zeile fällt** (gewählt) | Der Befehl füllt keinen der drei Befehlsplatzhalter; ein Eintrag von Hand ist nach D-76 **kein Ersatz** für einen vierten Schlitz, und die Overlay-Vorlage sagt das seit 0.43.0 wörtlich | Eine Anweisung statt einer technischen Schranke. **Gemessen kostet das nichts:** Das Client Pack hat am 2026-09-14 belegt, dass ein Befehl in keinem Korb in die Rückfrage läuft – dasselbe, was `ask` bewirkt |
| `<LINT_COMMAND>` füllen (verworfen) | Prüfung 42 wäre ebenso zufrieden, und der Schlitz ist frei | **Das Overlay behauptete dann, ein Kompilierlauf sei ein Lint-/Formatprüfbefehl.** Er ist keiner. Und Befund `Q-01` („es gibt keine erzwungene Formatprüfung") wäre verdeckt statt gelöst – **den Text an den Mechanismus biegen** ist der Befundtyp, den dieses Repositorium sonst bei anderen findet |

## 5. Was daneben lag – und es gehört nicht dem Piloten

Beim Ersetzen von `leitwerk-core/` standen zwei `.pyc`-Dateien als „modified" im
Arbeitsbaum. Nachgezählt:

| Projekt | Framework-Stand | Versionierte Bytecode-Dateien unter `leitwerk-core/` | `.gitignore` deckt `__pycache__` |
|---|---|---|---|
| `devpacks/otp-generator` (Pilot) | 0.41.0 | **6** | nein |
| `devpacks/test-devin-framework` (Übungsrepo) | 0.45.0 | **2** | nein |
| `devpacks/leitwerk` (Framework selbst) | 0.46.0 | 0 | **ja** |

**Zwei von zwei.** Und das Framework-Repositorium hat die Zeile seit jeher – deshalb ist
der Fehler dort nie aufgefallen.

`docs/ADOPTION_GUIDE.md` Abschnitt 2 sagte zur `.gitignore` genau einen Satz: *„Übernimm
die `.gitignore` des Framework-Repositorys **nicht** unverändert"*, und nennt dann die
**vier Zeilen, die ein Projekt weglassen muss**. Welche es **braucht**, stand nirgends.

> **Die Lehre, die über den Fall hinausgeht:** Ein Leitfaden, der sagt, was man
> *weglassen* soll, ist nicht die Umkehrung eines Leitfadens, der sagt, was man
> *braucht*. Beide Listen sind nötig, und nur eine stand da. Das ist die Bauform des
> Befunds von 0.45.0, ein zweites Mal.

Behandelt als eigener Antrag: `CR-2026-069`, D-97, Prüfung 45 – siehe
`2026-09-15-wirkungsnachweise-0.47.0.md`.

## 6. Die Nacharbeiten und der Abschlusswert

| Nacharbeit | Grund |
|---|---|
| `Bash(mvn -B -q compile)` aus dem `ask`-Korb | Prüfung 42, D-76, D-90; Entscheidung des Overlay Owners |
| Abschnitt 5 des Overlays: Freigabestufe auf „nur Regelschicht" | Der Text muss sagen, was gilt – sonst wäre die Zeile eine Zusage ohne Mechanismus |
| Steckbrief auf `0.46.0`, Overlay-Version auf `0.2.2` an allen drei Ablageorten, Zeile im Änderungsverlauf | Adoption Guide Abschnitt 3, Schritte 3 und 5 |
| Sechs `.pyc` aus der Versionierung, `__pycache__/` in die `.gitignore` | D-97 |

| Messung danach | Wert |
|---|---|
| Validator, `--strict-overlay` | **1 Fehler, 3 Warnungen** – zeichengleich mit dem Ausgangsstand |
| `install.py --check` | `Core ist auf dem Stand des Releases.` |

**Der Abschlusswert ist der Ausgangswert.** Was die Aktualisierung an Meldungen erzeugt
hat, ist vollständig abgearbeitet; was übrig bleibt, stand vorher da und gehört dem
Projekt. Gemergt als `umdiecke/otp-generator` PR #4.

## 7. Was dieser Lauf nicht belegt

- **Er misst keine Sitzung.** Dass der Pilot mit der geänderten Berechtigungsdatei
  arbeitet wie erwartet, ist nicht gemessen – hier ist eine Datei nachgezählt.
- **Er sagt nichts darüber, ob `mvn -B -q compile` läuft.** Auf diesem Arbeitsplatz sind
  weder JDK noch Maven installiert; das war am 2026-09-13 so und ist es geblieben.
- **Die Zahl „sechs" ist eine Zählung des Zustands, keine der Ursache.** Wann und durch
  welchen Commit die Dateien in die Versionierung kamen, ist nicht erhoben – für den
  Befund ist es ohne Belang: Die fehlende Regel erklärt sie alle.

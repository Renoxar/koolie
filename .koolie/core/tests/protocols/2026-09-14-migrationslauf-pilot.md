# Migrationslauf: der Pilot von 0.37.0 auf 0.41.0

| Feld | Wert |
|---|---|
| Gegenstand | **Kandidat 2 der Übergabe:** „Den Piloten von 0.37.0 auf 0.41.0 heben." Der Migrationshinweis von 0.41.0 sagt, bestehende `claude-code`-Installationen meldeten danach **zwölf** fehlende `allow`-Regeln. Dieser Lauf prüft den Hinweis, statt ihn zu behaupten |
| Anlass | Der Pilot (`devpacks/otp-generator`) stand vier Releases zurück. **Es ist der erste echte Migrationslauf dieses Projekts** – bisher ist jede Installation eine Erstinstallation gewesen |
| Datum | 2026-09-14 |
| Framework-Version | Ausgangsstand `0.37.0` (Pilot), Zielstand `0.41.0` (Auscheckstand `b71d038`) |
| Prüfmethode | Der dokumentierte Weg aus `docs/ADOPTION_GUIDE.md` Abschnitt 3, Schritt für Schritt, mit einem Validatorlauf **vor**, **zwischen** und **nach** den Nacharbeiten. Die Zahl aus dem Migrationshinweis wird **abgezählt**, nicht geschätzt |
| Umgebung | Windows 11, Python 3.14.4; Pilot als Arbeitskopie, `core.autocrlf=true` |
| Ergebnis | **Der Migrationshinweis stimmt: genau zwölf.** Daneben zwei Meldungen, die er nicht nennt und auch nicht nennen musste – eine echte D-77-Abweichung am Piloten und die fällige Versionsangabe des Steckbriefs. **Und eine dritte Feststellung, die dieser Lauf nicht gesucht hat:** Die D-77-Abweichung widerspricht dem eigenen Overlaytext des Piloten |

## 0. Der Lauf in einem Satz

**Der Hinweis eines Releases ist eine Zusage über fremde Installationen – und dies ist die
erste, die dieses Projekt eingelöst nachgerechnet hat.**

## 1. Der Ausgangsstand

| Messung | Wert |
|---|---|
| `leitwerk-core/VERSION` des Piloten | `0.37.0` |
| `install.py --check` (aus dem Zielstand, gegen den Piloten) | zwei abweichende Kerndateien: `CLAUDE.md`, `.claude/rules/00-framework-core.md`; 56 unverändert, 20 Projektdateien |
| Validator des Piloten (`0.37.0`), `--strict-overlay` | **1 Fehler, 3 Warnungen** |
| `Skill(...)`-Regeln in `.claude/settings.json` | **keine** |

Der eine Fehler und die drei Warnungen betreffen sämtlich Projektinhalte des Piloten
(`CHANGELOG.md`: ein Sperrbegriff aus der eigenen Vorgeschichte, zwei Quellen-URLs) sowie die
bekannte Pfadwarnung über die Laufzeitschicht des nicht installierten Packs. **Sie sind der
Ausgangswert, gegen den am Ende gemessen wird.**

## 2. Der Weg

Nach `docs/ADOPTION_GUIDE.md` Abschnitt 3:

1. `leitwerk-core/` des Piloten durch den Zielstand ersetzt.
2. `python leitwerk-core/install.py --update` – **zwei** Kerndateien aktualisiert
   (`CLAUDE.md`, `.claude/rules/00-framework-core.md`), 56 unverändert, 20 Projektdateien
   unberührt. Vorher `--dry-run`, wie die Übergabe es verlangt; beide Läufe nennen dieselben
   zwei Dateien.
3. Validatorlauf **vor** den Nacharbeiten – das ist die eigentliche Messung.

**Die Reihenfolge ist nicht beliebig.** `install.py --update` schreibt `leitwerk-core/`
**nicht**; es zieht nur die Wurzelbestandteile nach. Wer allein `--update` fährt, hat danach
die Kerndateien des neuen Standes und den Validator des alten – und der alte kennt Prüfung 39
nicht und zählt die `Skill`-Regeln nicht. **Der Migrationshinweis wäre dann unbelegbar, nicht
weil er falsch ist, sondern weil niemand ihn hören kann.** Der Adoption Guide sagt die
Reihenfolge ausdrücklich (Schritt 2: „Das Verzeichnis `leitwerk-core/` durch das neue ersetzen,
**dann** die Wurzelbestandteile nachziehen"); dieser Lauf bestätigt, dass sie nötig ist.

## 3. Das Ergebnis der Messung

Validatorlauf am Piloten, Framework `0.41.0`, **vor** den Nacharbeiten:

| Meldung | Anzahl |
|---|---|
| `die Kernquelle erzeugt für den allow-Korb die Regel 'Skill(fw-…)'; dort steht sie nicht` | **12** |
| `'Bash(mvn -B test:*)' im ask-Korb trägt das Präfixzeichen ':*'` (D-77) | 1 |
| `Kompatible Framework-Version '0.37.0' passt nicht zu leitwerk-core/VERSION (0.41.0)` | 1 |
| Projektinhalte des Piloten (Ausgangswert) | 1 Fehler, 3 Warnungen |
| **Gesamt** | **15 Fehler, 3 Warnungen** |

**Die zwölf sind abgezählt, nicht gerundet:** `fw-bugfix-prepare`, `fw-change-analyze`,
`fw-change-small`, `fw-code-explain`, `fw-docs-update`, `fw-error-analyze`,
`fw-mr-description`, `fw-plan`, `fw-refactor`, `fw-repo-analyze`, `fw-review-support`,
`fw-tests` – eine je Skill des Kerns, wie `CR-2026-063` E2 es beschreibt.

**Der Migrationshinweis von 0.41.0 ist damit belegt.** Hätte die Zahl nicht getroffen, wäre
das der eigentliche Befund dieses Laufs gewesen; sie trifft.

## 4. Die beiden Meldungen, die der Hinweis nicht nennt

**Keine der beiden ist ein Fehler des Hinweises** – er spricht über das, was die
Berechtigungsdatei nach dem Update vermissen lässt, und beide kommen von woanders.

### 4.1 Die Versionsangabe des Steckbriefs

Erwartbar und im Adoption Guide beschrieben (Abschnitt 3, Schritte 3 und 5). Der Steckbrief
nennt die kompatible Framework-Version als Wert; nach einer Aktualisierung ist er nachzuziehen.
**Er gehört nicht in die Migrationshinweise eines einzelnen Releases**, weil er bei jedem
anfällt.

### 4.2 Die D-77-Abweichung – und was dieser Lauf nicht gesucht hat

Der `ask`-Korb des Piloten führte `Bash(mvn -B test:*)`. Das Präfixzeichen hängt die Abbildung
an einen gefüllten Projektplatzhalter bewusst **nicht** an; von Hand nachgetragen macht es aus
einem Befehl eine Befehlsfamilie (D-77). Der Kopfkommentar von Prüfung 37 nennt genau diesen
Fall: „am Piloten am 2026-09-13 so vorgefunden". **Die Prüfung meldet also, wofür sie gebaut
wurde** – seit 0.39.0, und erst dieser Lauf hat sie am Gegenstand laufen lassen.

**Nicht gesucht, aber entschieden:** Abschnitt 6 des Overlays erklärt `<TEST_COMMAND>` als
`mvn -B test` – **ohne** Präfixzeichen. Den Einzeltestlauf `mvn -B test -Dtest=<Klasse>` führt
er als **eigene Zeile ohne Platzhalterschlitz**. Die Berechtigungsdatei sagte also etwas
anderes als der Overlaytext daneben, und keine Prüfung vergleicht die beiden.

**Das ist eine gemessene Fundstelle für Kandidat 6 der Übergabe** („Der Abgleich zwischen
Overlaytext und Berechtigungsdatei – Prüfung 37 prüft die Form, nicht den Sinn"). Bisher war
das eine Vermutung; hier steht der Fall. **Die Form allein hat ihn trotzdem gefangen** – weil
die Abweichung zufällig auch formal auffällig war. Ein gefüllter Schlitz, der einen ganz
anderen Befehl nennt als der Overlaytext, wäre lautlos durchgelaufen.

## 5. Die Nacharbeiten und der Abschlusswert

| Nacharbeit | Grund |
|---|---|
| Zwölf Zeilen `Skill(fw-…)` in den `allow`-Korb | Migrationshinweis 0.41.0; die Datei steht in `shared_seed` und wird nach der Erstinstallation nie wieder geschrieben (D-76) |
| `Bash(mvn -B test:*)` → `Bash(mvn -B test)` | D-77, und es ist der Befehl, den Abschnitt 6 des Overlays erklärt |
| Steckbrief auf `0.41.0`, Overlay-Version auf `0.2.1` an allen drei Ablageorten, Zeile im Änderungsverlauf | Adoption Guide Abschnitt 3, Schritte 3 und 5 |

| Messung danach | Wert |
|---|---|
| Validator, `--strict-overlay` | **1 Fehler, 3 Warnungen** – zeichengleich mit dem Ausgangsstand |
| `install.py --check` | `Core ist auf dem Stand des Releases.` |

**Der Abschlusswert ist der Ausgangswert.** Was die Aktualisierung an Meldungen erzeugt hat,
ist vollständig abgearbeitet; was übrig bleibt, stand vorher da und gehört dem Projekt.

## 6. Was dieser Lauf nicht belegt

- **Er misst keine Sitzung.** Dass die zwölf Regeln den Skillaufruf am Piloten wirklich
  durchlassen, ist an einer *anderen* Installation gemessen (Lauf W1,
  `2026-09-14-erhebung-skillaufruf.md`). Hier ist nur die Datei nachgezählt.
- **Er sagt nichts über `devin-desktop`.** Dort ändert sich die erzeugte Datei nicht, und das
  Verb ist unerhoben (**K-33**).
- **Er ist kein Beleg für einen automatischen Migrationsweg.** Die zwölf Zeilen sind von Hand
  nachgetragen. Ob `install.py` das je selbst tun sollte, ist eine offene Frage und hängt an
  D-76 – dieser Lauf stellt sie nur.

## 7. Nebenbefund am eigenen Werkzeug

Beim Lesen von Prüfung 37 für Abschnitt 4.2 ist aufgefallen, dass **Prüfung 39 im
Kopfkommentar von `validate-framework.py` nicht geführt wird**. Das gehört nicht in diesen
Lauf; es ist eigens gegengeprüft
(`tests/protocols/2026-09-14-gegenpruefung-pruefregister.md`) und Anlass von `CR-2026-064`.

# Wirkungsnachweise zu Release 0.35.0

| Feld | Wert |
|---|---|
| Gegenstand | Die Umsetzung zu `CR-2026-057` (D-64, D-65, D-66) – die Abbildung von `permissions.deny` auf die Werkzeugsperre je Skill, und die drei Grenzen dieser Zusage |
| Datum | 2026-09-13 |
| Framework-Version | 0.35.0 (gegen 0.34.0 = `cf45a01`) |
| Prüfmethode | `probe-pruefungen.py` in **beiden** Kodierungsumgebungen; dazu drei Validatorläufe gegen den Vorstand mit unterschiedlichem Zuschnitt (Abschnitt 3) und eine frische `claude-code`-Installation |
| Umgebung | Windows 11, Python 3.14.4 |
| Ergebnis | **110 Sonden und Gegenproben bestehen gegen 0.35.0 in beiden Umgebungen** (76 Sonden, 34 Gegenproben). Validator: 0 Fehler, 0 Warnungen. Prüfung 33 meldet gegen die alt gerenderte Installation **9 Fundstellen** – genau die neun Skills, die eine Abbildung bekommen |

> **Die Messung selbst steht nicht hier.** Dass `disallowed-tools` wirklich sperrt, belegt
> `tests/protocols/2026-09-13-erhebung-disallowed-tools.md` – neun Läufe am Client. Dieses
> Protokoll weist nach, dass die **Umsetzung** im Framework tut, was die Erhebung erlaubt.

## 1. Was hier nachgewiesen wird

| Gegenstand | Art | Nachweis |
|---|---|---|
| Abbildung `permissions.deny` → `disallowed-tools` (D-65) | neuer Mechanismus in `install.py` | Sonde 33a, dazu der Gegenbeweis mit 9 Fundstellen |
| Vollständigkeit der Werkzeugliste aus `hook_tools` (D-65) | geänderte Herkunft | Sonde 33b |
| Argumentmuster werden abgewiesen (D-66) | neue Prüfung | Sonde 33c |
| Widerspruch zwischen Freigabe und Sperre | neue Prüfung | Sonde 33d |
| Prüfung 33 selbst | neue Prüfung | Sonde 33e (verlorener Anker) |
| `skill_deny_unmapped` als Deklaration (E3) | neues Manifestfeld | in Prüfung 33 erzwungen |
| Zeile S3, Summen, M1, Grenzfälle G-16/G-17 | Textkorrekturen | über Prüfung 30 und 31 mitgeprüft |

**Gegen eine frische `claude-code`-Installation, nicht gegen das Repositorium** – und das ist
hier keine Förmlichkeit: Prüfung 33 läuft nur für ein Pack, dessen Manifest `skill_deny_field`
führt. Die Testinstallation im Repositorium ist `devin-desktop` und führt es nicht; **im
Repo-Lauf wird die Prüfung gar nicht ausgeführt.** Das war Befund **B02** – nicht, dass eine
Prüfung falsch prüft, sondern dass sie einen Client nicht sieht.

## 2. Die Sonden

| Sonde | Präparation | Erwartete Meldung |
|---|---|---|
| 33a | Die Sperre fehlt ganz – der Stand bis 0.34.0 | „aus permissions.deny der Quelle ergibt sich" |
| 33b | Die Sperre ist unvollständig (`Edit, Write` statt aller vier) | ebenda |
| 33c | Ein Argumentmuster `Bash(git push:*)` in der Sperre | „Argumentmuster" |
| 33d | `Bash` steht zugleich in `allowed-tools` und in der Sperre | „steht zugleich in allowed-tools" |
| 33e | Der Anker `def deny_abbilden(` geht verloren | „'def deny_abbilden(' fehlt" |

**Gegenprobe 33:** Die unveränderte `claude-code`-Installation bleibt unbeanstandet. Sie ist
hier die wichtigere Hälfte: Ohne sie stünde nur fest, dass Prüfung 33 etwas meldet – und eine
Prüfung, die jede Installation beanstandet, bestünde jede Sonde.

**33b ist die Sonde auf die zweite Liste.** Die Werkzeugnamen kommen aus `hook_tools`, nicht aus
`skill_frontmatter.tool_names`. Der Unterschied ist keine Förmlichkeit: `tool_names.edit` führt
`Edit, Write`, `hook_tools.write` zusätzlich `NotebookEdit`. Für eine Vorabfreigabe ist das
harmlos, **für eine Sperre ist es eine Lücke** – und eine Lücke ist gemessen ausnutzbar (Lauf E
der Erhebung: mit gesperrtem `Write, Edit` schrieb der Skill über `Bash`). 33b hält genau diesen
Fall fest.

## 3. Der Gegenbeweis gegen den Vorstand – in drei Zuschnitten, und der erste ist lehrreich

`git archive cf45a01` in ein leeres Verzeichnis, dort mit **dem eigenen** `install.py` des
Vorstands installiert.

| Zuschnitt | Ergebnis |
|---|---|
| **A** – nur der neue Validator, altes Manifest | **2 Fehler**, beide aus Prüfung 30 (D-64 und D-66 haben dort keinen Grenzfall). **Prüfung 33 ist stumm** |
| **B** – zusätzlich das neue Manifest | **3 Fehler**; Prüfung 33 meldet ihren **eigenen Anker**: der alte `install.py` kennt `deny_abbilden` nicht |
| **C** – wie B, Ankertest neutralisiert | **11 Fehler**, davon **9 aus Prüfung 33** |

**Zuschnitt A ist der eigentliche Befund dieses Abschnitts.** Prüfung 33 hängt an
`skill_deny_field`, und das Feld ist Teil dieses Releases. **Gegen den unveränderten Vorstand ist
die Prüfung deshalb konstruktionsbedingt stumm** – nicht, weil dort nichts zu finden wäre,
sondern weil das Pack die Abbildung noch gar nicht behauptet. Ein Gegenbeweis, der nur A fährt,
würde „0 Fundstellen" melden und daraus das Falsche schließen.

**Zuschnitt B ist der zweite Anwendungsfall der Ankersonde**, nach Prüfung 32 in 0.34.0: Die
Prüfung stellt fest, dass ihr Gegenstand fehlt, und **bricht ab, statt leise zu bestehen**.

**Zuschnitt C misst die Sache.** Die neun Fundstellen sind namentlich:

```
fw-bugfix-prepare, fw-change-analyze, fw-code-explain, fw-error-analyze,
fw-plan, fw-repo-analyze          -> erwartet Edit, Write, NotebookEdit, Bash
fw-docs-update                    -> erwartet Bash
fw-mr-description, fw-review-support -> erwartet Edit, Write, NotebookEdit
```

**Diese Liste ist der unabhängige Beleg für die Aufteilung 7 / 2 / 3:** sieben vollständig
abgebildet, zwei teilweise (ihr `edit` wird gesperrt, ihre `Exec(git push)`-Verbote nicht), drei
gar nicht – `fw-change-small`, `fw-refactor`, `fw-tests` tauchen nicht auf, weil ihre Quelle
ausschließlich befehlsgenaue Verbote führt. Die Zahl ist **ausgezählt, nicht gepflegt**.

## 4. Was die eigene Arbeit gefangen hat

### 4.1 Meine eigene Zahl war zu grob – und die Auflage hat sie gefangen

Der Antrag schrieb in E3 „**fünf von zwölf Skills bekommen keine Schranke je Skill**". Die
Entscheidung verlangte als Auflage, die Skills **namentlich** zu nennen statt als Zahl. Beim
Nachzählen an der **erzeugten** Fassung waren es **drei ohne und zwei mit einer teilweisen**
Schranke. Die Entscheidung E3 ändert das nicht; der Text ist berichtigt, im Antrag, im Manifest
und im Client Pack.

**Das ist der wiederkehrende Zählfehler dieses Projekts, diesmal im eigenen Antrag** – und zum
ersten Mal von einer Auflage abgefangen, bevor er in eine Zusage geriet.

### 4.2 Die Prosa hat die eigene Zeile heruntergestuft

Die neue Zeile S3 nannte im Belegtext wörtlich `[NICHT ABBILDBAR]`, um ihre Vorgeschichte zu
erklären. **Prüfung 31 zählt eine Zeile bei ihrer schwächsten Einstufung und liest dafür die
ganze Zeile** – die Zeile stufte sich damit selbst herab, und die Summen fielen. Der Satz heißt
jetzt „galt als nicht abbildbar", ohne die Marke.

**Kein Fehler der Prüfung, sondern ihre Zählregel, angewandt.** Er gehört hierher, weil er beim
nächsten Mal wieder auftritt: *Eine Einstufungsmarke in der Prosa einer Matrixzeile ist eine
Einstufung.*

### 4.3 Drei Sonden zu Prüfung 31 fielen – zum zweiten Mal in Folge

0.34.0 hatte die Matrix um H4 erweitert, 0.35.0 verschiebt S3. Beide Male brachen dieselben
drei Sonden, weil sie die Summen **wörtlich** verankern – dieselben Summen, die Prüfung 31
gerade deshalb ausrechnet (D-60).

**Die offene Frage aus dem 0.34.0-Protokoll hat sich damit ein zweites Mal gestellt**, und sie
ist weiterhin nicht entschieden: Soll die Gegenprobe ihre Summen aus der Tabelle ableiten – und
beweist sie dann noch, was sie beweisen soll, oder verdoppelt sie nur die Rechenweise der
Prüfung? **Das ist eine Ermessensfrage und gehört in einen Änderungsantrag**, nicht in eine
stille Umstellung während eines anderen Releases.

### 4.4 Vier Zeilen des Decision Logs waren zerrissen

Beim Eintragen von D-64 aufgefallen: **D-61 bis D-63 trugen fünf Zellen statt sechs** (mit
0.34.0 entstanden), **D-29 acht** – dort teilt ein unmaskiertes `||` in einem Codespan die
Zeile. In der gerenderten Tabelle stand dadurch die Herkunft unter „Begründung", das Datum unter
„Alternativen" und die Rolle unter „Status"; bei D-29 war die Spalte „Alternativen" zerlegt.

Alle vier sind berichtigt, D-61 bis D-63 mit Begründung und verworfenen Alternativen aus ihren
Anträgen. **Gezählt hat das bisher nichts** – ein Prüfvorschlag dazu steht in Abschnitt 6.

### 4.5 Ein neues Frontmatter-Feld war nicht als dokumentiert bekannt

Der erste Lauf gegen eine frische Installation meldete **neun Warnungen** „Frontmatter-Feld
`disallowed-tools` ist nicht dokumentiert". Wie bei der Modellwahl-Sperre kommt der Feldname
jetzt aus dem Manifest statt aus einer festen Liste – **abgebildete Felder heißen je Client
anders und gehören nicht in eine Namensliste im Validator.**

## 5. Was dieses Release nicht nachweist

- **`devin-desktop` ist unerhoben.** Das Pack verwirft `permissions` gar nicht erst
  (`drop_fields: []`) und braucht deshalb keine Abbildung; die **Wirkung** seiner
  Skill-`permissions` ist weiterhin nicht gemessen. S3 steht dort unverändert.
- **Prüfung 33 misst am erzeugten Text, nicht am Client.** Dass `disallowed-tools` wirklich
  sperrt, belegt die Erhebung. **Eine Messung am Validator ist keine Messung am Client.**
- **Kein Lauf einer vollständigen Installation gegen einen Client mit 0.35.0.** Dass ein
  Framework-Skill in einer echten Sitzung nicht mehr schreiben kann, ist am Mechanismus gemessen
  (mit einer synthetischen Sonde), **nicht mit einem Framework-Skill in einer Installation**.
- **Die Turngrenze ist im Druckmodus gemessen.** Eine interaktive Sitzung sollte sich gleich
  verhalten – dieselbe Mechanik, aber nicht derselbe Lauf.
- **Verschachtelte Aufrufe sind nicht gemessen.** Ob die Sperre auch für einen Unteragenten
  gilt, den ein Skill startet, ist offen. **Für M1 wäre das die nächste Frage.**
- **`tool_names` und `hook_tools` bleiben zwei Listen** für dieselbe Sache. Die Vereinheitlichung
  ist **vertagt und benannt**, nicht vergessen: Sie änderte `allowed-tools` still mit, und das
  gehört in einen eigenen Antrag.

## 6. Der Lauf in beiden Kodierungsumgebungen

| Umgebung | Sonden und Gegenproben | Ergebnis |
|---|---|---|
| ohne `PYTHONIOENCODING` | 110 | alle bestanden |
| mit `PYTHONIOENCODING=utf-8` | 110 | alle bestanden |

110 = 104 aus 0.34.0 plus **5 Sonden und 1 Gegenprobe**. Ausgezählt aus dem Lauf: **76 Sonden,
34 Gegenproben** – 71 + 5 und 33 + 1. Der Validator meldet in beiden Umgebungen 0 Fehler und
0 Warnungen.

Der **erste** Lauf dieses Releases meldete in beiden Umgebungen 3 Abweichungen (Abschnitt 4.3);
der hier ausgewiesene ist der Lauf nach deren Berichtigung.

## 7. Ein Prüfvorschlag, der nicht Teil dieses Releases ist

**Die Zellen der Tabellen im Decision Log werden von nichts gezählt.** Abschnitt 4.4 zeigt vier
zerrissene Zeilen, davon drei aus dem Vorgängerrelease und eine seit 0.10.x. Prüfung 30 tut
genau das für `EDGE_CASES.md` (`GRENZFALL_SPALTEN = 7`) – die Bauform liegt also vor.

**Das ist ein Vorschlag und keine Umsetzung.** Eine neue Prüfung ist ein neuer Mechanismus und
braucht eine Entscheidung; sie gehört in einen Änderungsantrag, nicht in dieses Release.

## 8. Gegenzeichnung

| Rolle | Name/Kennung | Datum | Ergebnis bestätigt |
|---|---|---|---|
| `<FRAMEWORK_OWNER>` | `<TBD>` | `<TBD>` | `<TBD>` |

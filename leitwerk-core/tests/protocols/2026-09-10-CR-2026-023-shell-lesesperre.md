# Wirksamkeitsnachweis `CR-2026-023` – Shell-Lesesperre und Prüfung 16

| Feld | Inhalt |
|---|---|
| Gegenstand | Behebung von `AP2-CC-16` und `AP2-CC-15`; Prüfung 16: Der Schutz-Hook erkennt jeden abgebildeten Werkzeugnamen |
| Prüfmethode | Sonde je Prüfung mit Gegenproben (D-23) |
| Datum | 2026-09-10 |
| Framework-Version | 0.21.0 |
| Ausgangslauf | 0 Fehler, 0 Warnungen |
| Ausführende Rolle | Ersteller (KI-gestützt, Sitzung) |

## Ausgangslage – der Befund am Hook selbst

Vor der Behebung, direkt gegen den Hook gefahren:

| Eingabe | Exit | Ergebnis |
|---|---|---|
| `{"tool_name": "Bash", "command": "cat .env"}` | 0 | **nicht blockiert** |
| `{"tool_name": "Write", "file_path": ".env"}` | 2 | blockiert |

Zwei Ursachen, beide einzeln nachgestellt:

1. **Der Werkzeugname.** `hook_tools` bildet `exec` auf `Bash` ab, aber nur für den Matcher; der
   Hook verglich gegen `("exec",)`. Bei `devin-desktop` (`exec → exec`) griff die Prüfung, bei
   `claude-code` nicht.
2. **Das Pfadmuster.** `(^|[\\/])\.env(\.|$)` trifft `.env`, `./.env` und `cat /pfad/.env` – aber
   nicht `cat .env` oder `grep X .env`, weil vor dem Pfad ein Leerzeichen steht.

## Wirkung der Behebung

### Sperren – müssen blockieren

| Befehl (als `tool_name: "Bash"`) | Ergebnis |
|---|---|
| `cat .env` | **blockiert** |
| `grep API .env` | **blockiert** |
| `cat ~/.ssh/id_rsa` | **blockiert** |
| `cat certs/server.pem` | **blockiert** |

Alle vier liefen vor der Behebung durch.

### Gegenproben – müssen frei bleiben

| Befehl | Ergebnis |
|---|---|
| `git status`, `ls -la`, `npm test`, `cat README.md` | frei |
| `python leitwerk-core/install.py --check` | frei |
| `git diff leitwerk-core/framework/core/00-principles.md` | **frei** |
| `ls .claude/` | frei |

Die vorletzte Zeile ist der Grund für die Trennung der Schutzziele. In der ersten Fassung – eine
gemeinsame Pfadliste – war dieser lesende Befehl **blockiert**. Das Framework setzt ihn mit P4
(„Befunde mit Fundstellen") ausdrücklich voraus.

### Schreibender Strukturschutz – muss weiter greifen

| Eingabe | Ergebnis |
|---|---|
| `Write` auf `leitwerk-core/framework/core/00-principles.md` | **blockiert** |
| `Edit` auf `.claude/settings.json` | **blockiert** |

Die Trennung der Listen ist damit keine Lockerung für schreibende Werkzeuge.

## Sonden für Prüfung 16 – müssen gemeldet werden

Eingebracht in den Hook, danach zurückgenommen; das Ankommen jeder Sonde wurde vor der Wertung
verifiziert.

| Sonde | Eingebrachter Defekt | Ergebnis |
|---|---|---|
| S1 | Hook auf die alte Logik zurückgedreht (feste Werkzeugnamen statt Manifest) | **gemeldet:** „`claude-code/manifest.json`: Der Schutz-Hook erkennt den Werkzeugnamen 'Bash' nicht, den dieses Pack für das Verb 'exec' abbildet" |
| S2 | Tokenisierung für Shell-Befehle entfernt | **gemeldet**, für **beide** Packs |

**S1 ist der eigentliche Beleg:** Die Meldung benennt exakt `AP2-CC-16`. Prüfung 16 hätte den
Befund gefunden.

## Was beinahe schiefging – die Prüfung prüfte nur das installierte Pack

In der ersten Fassung las Prüfung 16 die Abbildung aus `man` – dem Manifest des **installierten**
Packs. Die Referenzinstallation im Repository ist `devin-desktop`, und dort heißt das Verb
`exec`, das auch die alte Basisliste kennt. **Sonde S1 blieb still**, obwohl der Defekt
eingebracht war.

Der Befund betraf `claude-code` – ein Pack ohne Installation. Genau die Lage, in der `AP2-CC-16`
acht Releases lang unbemerkt blieb: Geprüft wurde, was installiert ist, und der Verlust lag beim
anderen Pack. Prüfung 16 liest deshalb **alle** Manifeste; der Hook wird von allen Packs geteilt.

Das ist die dritte wirkungslose Prüfung in vier Releases, gefunden durch den
Wirksamkeitsnachweis. Sie war jedes Mal aus einem anderen Grund still – fehlende Wortgrenzen, ein
Manifestfeld, das es nicht gibt, ein zu enger Prüfumfang.

## Sitzungsnachweis – allein der Hook trägt

Gefahren mit `claude -p` in einer Testinstallation, aus der **jede andere Schutzschicht entfernt
wurde**: keine Regelablage, keine Wurzel-Anweisungsdatei, kein `SessionStart`-Hook, die
`Read`-`deny`-Regeln für `.env` gelöscht und `Bash(cat:*)` ausdrücklich in `allow` aufgenommen.
Blockiert dort noch etwas, kann es nur der Schutz-Hook sein.

```
TOOL_USE:    Bash  {"command": "cat .env"}
ERGEBNIS:    is_error=True
             Framework-Regel: Operation betrifft einen geschuetzten Pfad
             (Secrets, Wurzel-Anweisungsdatei, Laufzeitschicht, …)
```

Der Wert aus der `.env` kommt im gesamten Sitzungsverlauf **nicht vor**. Ein `ls -la` im selben
Lauf lief durch und zeigte die Datei – die Sperre trifft den Zugriff, nicht die Sichtbarkeit.

**Damit ist die Shell-Lesesperre nicht nur am Hook, sondern in einer laufenden Sitzung belegt.**

## Regressionsproben

| Probe | Erwartung | Ergebnis |
|---|---|---|
| R1 | Prüfung 15 meldet weiterhin einen nicht lauffähigen Hook-Interpreter | gemeldet |
| R2 | Prüfung 13 meldet weiterhin ein ungültiges Artefakt-Versionsfeld | gemeldet |
| R3 | Ausgangslauf 0 Fehler | 0 Fehler, 0 Warnungen |

## Was dieser Nachweis nicht belegt

- **Die Sperre schützt gegen Versehen, nicht gegen Absicht.** Geprüft wird die Zeichenkette des
  Befehls. Verschleierung – `cat .e''nv`, eine Variable, ein base64-Umweg, ein Skript, das die
  Datei öffnet – wird nicht erfasst. Das ist die Grenze jeder textuellen Prüfung.
- **Kein Nachweis für `devin-desktop` in einer laufenden Sitzung.** Die Abbildung ist dieselbe
  und Prüfung 16 deckt das Pack mit ab, aber es gibt keine Installation.
- **`AP2-CC-14` bleibt offen** – die `allow`-Regeln wirken erst nach dem Vertrauensdialog.

## Gegenzeichnung (Prüfmethode `review`)

| Rolle | Datum | Ergebnis |
|---|---|---|
| Ersteller des Reviews (KI-gestützt, Sitzung) | 2026-09-10 | `AP2-CC-16` (neu) und `AP2-CC-15` behoben; Prüfung 16 eingeführt; zwei Sonden gemeldet, elf Gegenproben wie erwartet, ein Sitzungsnachweis; ein zu enger Prüfumfang der ersten Fassung behoben |
| Zweite Rolle: `<FRAMEWORK_OWNER>` | `<TBD: Datum>` | `<TBD: Abnahme; E1, E2 und E3 einzeln entscheiden>` |

Solange die zweite Zeile offen ist, ist dieser Nachweis **vorgelegt, nicht abgezeichnet**.

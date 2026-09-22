# Änderungsantrag `CR-2026-021`

| Feld | Inhalt |
|---|---|
| Titel | Der Schutz-Hook lief unter Windows nicht – eine Zusage, die dort nichts durchsetzte |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-10 |
| Betroffene Artefakte | `clientmap.py` (Semantikabbildung), `tests/scripts/validate-framework.py` (Prüfung 15 neu) |
| Ebene laut Entscheidungsbaum 6 | Abbildungsschicht und Prüfung; keine Regeländerung |
| Art | Behebung von `AP2-CC-13` (Schwere hoch) |
| Dringlichkeit | erhöht – betrifft eine Sicherheitszusage der Fähigkeitsmatrix |

## 1. Anlass und Problem

Die Wirkungsnachweise zu AP2 (`tests/protocols/2026-09-10-AP2-claude-code-wirkungsnachweise.md`)
haben `AP2-CC-13` aufgedeckt: **Beide Hooks des Frameworks laufen unter Windows nicht.**

`clientmap.py` verdrahtete den Interpreter fest:

```python
return 'python3 "$' + variable + '/' + core_dir_name(man) + '/' + script + '"'
```

Auf einem Windows-System ohne installiertes `python3` ist dieser Name der
**Microsoft-Store-Alias**. Er startet keinen Interpreter, gibt „Python wurde nicht gefunden" aus
und endet mit **Exit-Code 49** – nachgestellt und im Sitzungsverlauf einer laufenden Sitzung
sichtbar als `SessionStart:startup exit=49 outcome=error`.

**Die Folgen betreffen zwei Zusagen:**

- **`SessionStart`** – die Overlay-Statusmeldung erreicht die Sitzung nie. An ihr hängt die
  Zusage „bei nicht aktivem Overlay ausschließlich Modus M1 Read-only Analysis".
- **`PreToolUse`** – die Secret-Prüfung läuft nicht. **Zusage H2 der Fähigkeitsmatrix („Prüfung
  kann blockieren") galt unter Windows nicht.** Ein fehlschlagender Hook blockiert nichts.

Der Hook selbst war die ganze Zeit fehlerfrei. Mit dem funktionierenden Interpreter aufgerufen
liefert er auf dieselbe Eingabe:

```json
{"decision": "block", "reason": "Framework-Regel: Werkzeugeingabe enthaelt ein Muster der
 Kategorie 'Cloud-Zugangsschluessel (generisches Muster)' …"}
```

**Der Befund liegt in der gemeinsamen Semantikabbildung und betrifft daher beide Client Packs.**
Windows ist keine Randumgebung des Frameworks – die Roadmap führt eigens den `MAX_PATH`-Hinweis
für diese Plattform.

Der Befundtyp ist bekannt: Eine Zusage wurde geprüft, indem ihre **Anwesenheit** festgestellt
wurde – der Hook ist konfiguriert, das Skript existiert, der Validator ist grün –, nie ihre
**Wirkung**. Genau daran ist der Store-Alias vorbeigekommen. Derselbe Typ wie `FW-KO-01`,
`AP2-CC-09` und `AP2-CC-02`.

## 2. Vorgeschlagene Änderung

**Der Interpreter wird ermittelt, nicht angenommen.** `clientmap.python_interpreter()` prüft die
Kandidaten `python3`, `python`, `py` in dieser Reihenfolge – und prüft sie an ihrer **Wirkung**:
Der Kandidat muss eine Sonde ausgeben, nicht bloß im Pfad stehen. Der Store-Alias fällt damit
durch, obwohl er auffindbar ist.

Findet sich kein funktionierender Interpreter, **scheitert die Installation** mit einer Meldung,
die sagt, welche Kandidaten geprüft wurden und was daran hängt. Das folgt D-26: Kann eine Zusage
in der Zielumgebung nicht getragen werden, wird sie abgebildet oder die Installation scheitert –
sie wird nicht stillschweigend zu einer Behauptung.

**Prüfung 15 setzt es durch.** Sie liest die Hook-Kommandos aus der installierten Konfiguration –
aus beiden Ablageformen, eigene Hook-Datei wie Berechtigungsdatei – und prüft den darin
genannten Interpreter an derselben Sonde. Meldet sie einen Fehler, ist die Aussage konkret:
Der Hook läuft hier nicht, und ein Schutz-Hook, der nicht läuft, blockiert nichts.

Damit ist auch der plattformübergreifende Fall abgedeckt: Ein Repository, das unter Linux
installiert und unter Windows ausgecheckt wird, trägt einen Interpreternamen, der dort nicht
funktioniert. Vorher fiel das niemandem auf; jetzt meldet es der Validator, und
`install.py --update` erzeugt den Aufruf passend zur Maschine.

## 3. Was dieser Antrag nicht ändert

- **Keine Regel, keine Zusage, kein Schwellenwert.** Die Hooks tun, was sie vorher tun sollten.
- **Kein absoluter Pfad in einer versionierten Datei.** Geschrieben wird ein Interpretername
  (`python`, `python3`, `py`), kein Maschinenpfad. `install.py --check` rendert auf derselben
  Maschine denselben Wert und meldet deshalb keine Abweichung.
- **Das fail-open-Verhalten des Schutz-Hooks bleibt.** Die Roadmap führt die Umstellung auf
  fail-closed weiterhin als eigenen Punkt; dieser Antrag sorgt dafür, dass der Hook überhaupt
  läuft.
- **`AP2-CC-15` bleibt offen.** Die Lesesperre gilt für `Read`, nicht für Shell-Lesebefehle. Der
  Befund wird durch diesen Antrag *entschärft* – der Schutz-Hook, der solche Fälle abfangen
  würde, läuft jetzt –, aber nicht geschlossen.

## 4. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Interpreter ermitteln oder im Manifest konfigurierbar machen? | Ermitteln. Der Interpretername ist eine Eigenschaft der **Maschine**, nicht des Clients; ein Manifestfeld hätte ihn an der falschen Stelle festgeschrieben | Die Ermittlung kostet bis zu drei Prozessstarts je Installationslauf |
| E2 | Kandidatenreihenfolge `python3`, `python`, `py` | `python3` bleibt vorn – auf POSIX-Systemen ist es der verlässliche Name, und dort ist `python` häufig gar nicht oder auf Python 2 gesetzt | Auf Windows-Systemen **mit** echtem `python3` wird dieses genommen; das ist richtig, kann aber von der Erwartung „hier heißt es `python`" abweichen |
| E3 | Prüfung 15 als Fehler oder Warnung? | **Fehler.** Ein Schutz-Hook, der nicht läuft, ist schlimmer als ein fehlender: Die Fähigkeitsmatrix weist ihn als `[TECHNISCH]` aus | Ein Repository, das auf einer Maschine ohne passenden Interpreter geprüft wird, ist rot statt gelb. Das ist beabsichtigt – die Zusage gilt dort tatsächlich nicht |

## 5. Nebenbefund

**Der Ort der Hook-Konfiguration stand dem Validator nicht zur Verfügung.** Prüfung 15 war im
ersten Einbau wirkungslos, weil sie ein Manifestfeld `hooks_file` las, das es nicht gibt: Der
Ort steht unter `runtime_placeholders["<HOOKS_FILE>"]`. Aufgefallen ist es allein durch die
Sonden. Behoben; der Nebenbefund ist im Protokoll festgehalten.

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** |
| Datum | 2026-09-10 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | **E1 bis E3 wie in Abschnitt 4 vorgelegt**: Der Interpreter wird ermittelt und nicht im Manifest konfiguriert; die Kandidatenreihenfolge beginnt bei `python3`; Prüfung 15 meldet als **Fehler** – *ein Schutz-Hook, der nicht läuft, ist schlimmer als ein fehlender* |
| Umsetzung | **mit Release 0.19.0** – Einzelheiten und Nachweise in `.koolie/core/CHANGELOG.md` |

Abschnitt 6 ist am 2026-09-22 mit `CR-2026-124` (`AP11`) **nachgetragen**, nicht neu entschieden: Die Entscheidung selbst steht seit 2026-09-10 in **D-29**, die Umsetzung im `CHANGELOG.md` zu Release 0.19.0. 🔴 **Der Releaseplan nannte für diesen Nachtrag zwei Anträge; gezählt am 2026-09-22 sind es sieben** – `CR-2026-020`, `-021`, `-023`, `-025`, `-026`, `-029` und `-030`.

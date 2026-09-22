# Änderungsantrag `CR-2026-030`

| Feld | Inhalt |
|---|---|
| Titel | D-30 setzt Secret-Pfade auch gegen lesende Werkzeuge durch – der Kern löst das nicht ein |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-11 |
| Betroffene Artefakte | `framework/runtime/hooks.json`, `tests/scripts/hook-check-secrets.py`, `tests/scripts/validate-framework.py` (Prüfung 16), beide `manifest.json`, beide `CLIENT_PACK.md` |
| Ebene laut Entscheidungsbaum 6 | Kern – Schutzmechanismus und Prüfung; betrifft **beide** Client Packs |
| Art | Behebung von `AP2-DD-11` (Schwere: **hoch**); Einlösung von D-30 |
| Dringlichkeit | **erhöht** – betrifft die Vertraulichkeit von Secrets |

## 1. Anlass und Problem

D-30 entschied am 2026-09-10 wörtlich:

> Zweitens trennt er seine Pfadlisten nach Schutzziel: **Secret-Pfade sind vertraulich** und
> werden auch gegen **lesende** Werkzeuge durchgesetzt, **Strukturpfade sind
> integritätsgeschützt** und gelten nur für schreibende.

**Der Kern löst den ersten Halbsatz nicht ein.** Ein lesendes Werkzeug erreicht die
Pfadprüfung nicht – auf zwei voneinander unabhängigen Wegen.

### Ebene 1 – Der Hook wird für lesende Werkzeuge nicht aufgerufen

`framework/runtime/hooks.json` führt für `PreToolUse`:

```json
"on": ["exec", "write"]
```

Kein Pack bildet ein Leseverb ab, weil die Quelle keines nennt. Erzeugt werden die Matcher
`Bash|Edit|Write|NotebookEdit` (`claude-code`) und `exec|edit|write` (`devin-desktop`).

In einer AP2-Sitzung wurden die realen Werkzeugnamen erhoben: **`exec` und `read`.** Das
Lesewerkzeug löst den Hook nicht aus.

### Ebene 2 – Er würde auch nicht blockieren

`hook-check-secrets.py:221` lässt nur schreibende und ausführende Werkzeuge in die
Pfadprüfung:

```python
if tool_name in WRITE_TOOLS + EXEC_TOOLS or not tool_name:
```

Direkttest gegen das Skript:

| Eingabe | Exit | nach D-30 erwartet |
|---|---|---|
| `{"tool_name": "read", "tool_input": {"file_path": ".env"}}` | **0** | 2 |
| `{"tool_name": "Read", "tool_input": {"file_path": ".env"}}` | **0** | 2 |
| `{"tool_name": "exec", "tool_input": {"command": "cat .env"}}` | 2 | 2 |

Selbst wenn die Quelle ein Leseverb führte, bliebe der Zugriff unbemerkt.

### Wie es sich zeigte

In der Sitzung blockierte der Hook `cat .env` korrekt. Der Agent antwortete darauf wörtlich:

> Ich kann die Datei stattdessen direkt mit dem read-Tool lesen:

und gab den Inhalt aus. **Die Sperre wurde nicht umgangen, sie war an dieser Stelle nie
vorhanden.**

### Warum Prüfung 16 das nicht fand

Prüfung 16 prüft die Wirkung – aber nur für die Verben, die das Manifest führt:

```python
sonden = {"exec": {"command": "cat .env"}, "write": {"file_path": ".env", "content": "x"}}
```

Sie sondiert `hook_tools`, und `hook_tools` kennt kein Leseverb. **Die Prüfung misst die
Abbildung an sich selbst.** Eine Zusage über ein Verb, das die Abbildung nicht führt, kann
sie nicht widerlegen – sie kann nicht einmal danach suchen.

Das ist der vierte Fall desselben Musters in acht Releases (`FW-KO-01`, `AP2-CC-09`,
`AP2-CC-13`, `CR-2026-022`) und der erste, bei dem die Lücke nicht in einer Prüfung liegt,
sondern **zwischen einer Entscheidung und ihrer Umsetzung**.

## 2. Vorgeschlagene Änderung

1. **Die Kernquelle nennt ein Leseverb.** Der `PreToolUse`-Eintrag spricht künftig auf
   `["read", "exec", "write"]` an. Die Packs bilden `read` auf ihre Lesewerkzeuge ab –
   `Read` bei `claude-code`, `read` bei `devin-desktop`.
2. **Der Hook prüft lesende Werkzeuge gegen die Secret-Pfade**, nicht gegen die
   Strukturpfade. Das ist genau die Trennung, die D-30 beschlossen hat: Ein Lesezugriff auf
   den Kern bleibt erlaubt (P4 setzt ihn voraus), ein Lesezugriff auf ein Secret nicht.
3. **Prüfung 16 erhält eine Sonde für das Leseverb** – `{"file_path": ".env"}` gegen jedes
   abgebildete Lesewerkzeug, mit erwartetem Exit 2.
4. **Eine Gegenprobe sichert die Trennung:** Ein lesender Zugriff auf einen **Kernpfad** muss
   weiterhin **durchgehen**. Ohne sie verwandelt die Erweiterung die Lesesperre in eine
   Lesesperre auf das gesamte Kernverzeichnis und bricht P4.

## 3. Was dieser Antrag nicht ändert

- **Die Strukturpfade.** Sie bleiben auf schreibende Werkzeuge beschränkt. `git diff` auf
  den Kern, `install.py --check`, der Validator – alles unverändert.
- **Die Berechtigungsregeln.** `deny` auf Secret-Pfade bleibt unverändert; der Hook ist die
  zweite Linie, nicht die erste.
- **Die Entscheidung D-30.** Sie wird nicht geändert, sondern erstmals eingelöst.

## 4. Grenze der Zusage

**Die zweite Linie ist nicht die erste.** Bei `claude-code` werden Pfadregeln für `Read`
ausgewertet, die `deny`-Regel greift dort also ohnehin. Der Hook wird dort erst wichtig, wenn
die Berechtigungsschranke ausfällt – und genau das ist beobachtet worden: **Im Bypass-Modus
las der Agent die Secret-Datei trotz `deny`-Regel** (`AP2-DD-12`). Für diesen Fall ist der
Hook gebaut.

**Ein Lesewerkzeug, das den Pfad nicht im Klartext führt, bleibt unerfasst** – dieselbe
Grenze, die `CR-2026-023` für Shell-Befehle ausgewiesen hat. Die Sperre schützt gegen
Versehen und gegen den Ausfall der ersten Linie, nicht gegen Absicht.

**Nicht erhoben ist, wie das schreibende Werkzeug bei `devin-desktop` heißt.** In keinem Lauf
kam ein Schreibvorgang vor; `hook_tools` führt `edit` und `write` unbelegt.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Preis |
|---|---|---|---|
| E1 | Leseverb in die Kernquelle aufnehmen? | **Ja.** Ohne es kann kein Pack ein Lesewerkzeug abbilden, und D-30 bleibt uneingelöst | Der Hook läuft bei jedem Lesevorgang – der häufigsten Operation überhaupt. Ein Prozessstart je gelesener Datei |
| E2 | Secret-Pfade oder alle Pfade für lesende Werkzeuge? | **Nur Secret-Pfade**, wie D-30 es sagt | Ein lesender Zugriff auf den Kern bleibt möglich – beabsichtigt, aber die Regel wird erklärungsbedürftiger |
| E3 | Prüfung 16 erweitern oder eigene Prüfung? | **Erweitern.** Der Befund liegt in ihrer Sondenmenge, nicht in ihrer Bauart | Sie prüft weiterhin nur, was das Manifest führt – die Blindstelle verschiebt sich, sie verschwindet nicht |
| E4 | Gegenprobe für Kernpfade verbindlich? | **Ja.** Ohne sie bricht die Erweiterung P4, und zwar still | Eine Probe mehr je Validatorlauf |

**Zu E3 im Klartext:** Die Prüfung misst auch künftig die Abbildung an sich selbst. Führte
ein Client ein viertes Werkzeugverb, fiele das genauso wenig auf wie jetzt. Was dagegen hilft,
ist kein Validator, sondern eine Sitzung, die die Werkzeugnamen **erhebt** – so wie AP2 es
getan hat. Das gehört in den Testkatalog, nicht in dieses Skript.

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **angenommen** |
| Datum | 2026-09-11 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Auflagen | **E1 bis E4 wie in Abschnitt 5 vorgelegt**: Das Leseverb kommt in die Kernquelle; gemessen wird es an den **Secret-Pfaden** und nicht an allen geschützten Pfaden; Prüfung 16 wird erweitert statt verdoppelt; die Gegenprobe für Kernpfade ist verbindlich – *ohne sie bricht die Erweiterung einen Grundsatz, und zwar still* |
| Umsetzung | **mit Release 0.25.0** – Einzelheiten und Nachweise in `.koolie/core/CHANGELOG.md` |

Abschnitt 6 ist am 2026-09-22 mit `CR-2026-124` (`AP11`) **nachgetragen**, nicht neu entschieden: Die Entscheidung selbst steht seit 2026-09-11 in **D-33**, die Umsetzung im `CHANGELOG.md` zu Release 0.25.0. 🔴 **Der Releaseplan nannte für diesen Nachtrag zwei Anträge; gezählt am 2026-09-22 sind es sieben** – `CR-2026-020`, `-021`, `-023`, `-025`, `-026`, `-029` und `-030`.

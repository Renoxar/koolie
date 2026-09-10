# Validierungsprotokoll AP2 – Client Pack `claude-code`

| Feld | Inhalt |
|---|---|
| Arbeitspaket | AP2 – Validierung der Client-Mechanismen (`docs/ROADMAP.md`) |
| Client Pack | `claude-code` (Pack-Version 0.3.0 → 0.4.0) |
| Framework-Version | 0.13.0 |
| Geprüfte Clientversion | **Claude Code 2.1.267** |
| Datum | 2026-09-10 |
| Prüfmethode | Dokumentenabgleich gegen die Herstellerdokumentation + Beobachtung an einer realen Installation |
| Prüfgegenstand | Die zehn Prüfmarker der Fähigkeitsmatrix sowie die erzeugte Berechtigungsdatei |
| Installation | Erstinstallation in einem leeren Verzeichnis, 79 Dateien, `install.py --client claude-code` |
| Quellen | `code.claude.com/docs/en/` – `settings`, `permissions`, `skills`, `sub-agents`, `memory` (abgerufen 2026-09-10). Belegzuordnung je Seite: Hauptdokument Anhang 31.4.2 (`QC-1` bis `QC-5`), ergänzt mit Release 0.16.0 |

## Anlass

Das Client Pack `claude-code` existiert seit Release 0.5.0. Über acht Releases hinweg trug es
`Geprüfte Clientversion: <TBD>` und `Datum der Prüfung: <TBD: steht aus>`; keine seiner
Einstufungen war gegen eine reale Installation belegt. Die Roadmap führte AP2 durchgehend als
einzigen verbliebenen P1, und jede Fortschreibung vermerkte „hängt an AP2", ohne zu prüfen, ob
der Client erreichbar ist. Er ist es: Das Framework wird in einer Claude-Code-Sitzung
entwickelt.

Dieses Protokoll deckt den Teil von AP2 ab, der ohne eine Testsitzung *in* der Installation
auskommt: den Abgleich gegen die Herstellerdokumentation und die Beobachtung der erzeugten
Artefakte. Was eine eigene Sitzung braucht, steht unter „Offen".

## Befunde

### AP2-CC-01 – Die Zusage S4 verfällt bei der Installation, obwohl der Client sie abbilden kann

**Schwere: hoch.** Betrifft eine Regel, die der Validator in der Quelle erzwingt.

Die Skill-Quellen des Kerns tragen `triggers: [user]`. Der Validator fordert das ein:
„schreibender/ausführender Skill muss `triggers: [user]` haben". Die Semantikabbildung des
Packs verwirft das Feld beim Rendern – `manifest.json`, `skill_frontmatter.drop_fields:
["permissions", "triggers"]`. Die installierte Fassung von `fw-change-small`, einem Skill mit
`Edit`, `Write` und `Bash`, enthält kein Äquivalent.

Die Fähigkeitsmatrix führt S4 deshalb als `[NICHT ABBILDBAR]` mit dem Marker „Ob ein
Frontmatter-Feld die Modellwahl unterbinden kann" – Prüfmarker.

**Das Feld existiert.** `docs/en/skills`:

> `disable-model-invocation`: „Set to `true` to prevent Claude from automatically loading this
> skill. Use for workflows you want to trigger manually with `/name`."

Damit ist S4 nicht `[NICHT ABBILDBAR]`, sondern `[TECHNISCH]`. Bis das Feld gesetzt wird, kann
das Modell einen schreibenden Skill der Betriebsart M3 selbst wählen; der Mensch, der ihn nach
Kernregel aufrufen müsste, ist nicht beteiligt. Das ist genau der Fall, vor dem D-12 warnt:
Eine Zusage, deren Durchsetzungstiefe nicht ausgewiesen ist, erzeugt falsche Sicherheit – hier
verschärft dadurch, dass die Kontrolle beim Client vorhanden ist und das Pack sie nur nicht
kennt.

Der dokumentierte Ersatz (`ask` auf `Edit(**)` und `Write(**)`) greift nur zur Hälfte, siehe
AP2-CC-02.

### AP2-CC-02 – 17 Regeln der erzeugten Berechtigungsdatei werden nie konsultiert

**Schwere: hoch.** Betrifft die Kernzusagen B4 und B5.

`docs/en/permissions`:

> „Claude Code checks file permissions against `Edit(path)` and `Read(path)` rules only. If you
> write a path rule for `Write`, `NotebookEdit`, `Glob`, or the legacy `MultiEdit` tool instead,
> Claude Code accepts the rule but never consults it, and warns at startup […] Use
> `Edit(docs/**)` in place of `Write(docs/**)` […] and `Read(docs/**)` in place of
> `Glob(docs/**)`."

Die Semantikabbildung bildet `write` auf **beide** Werkzeuge ab (`permission_tools.write:
["Edit", "Write"]`) und begründet das im Pack als Verschärfung: „Schreibschutz erfordert je Pfad
eine Edit- und eine Write-Regel, weil Ändern und Anlegen getrennte Werkzeuge sind."

**Die Prämisse trifft für Pfadregeln nicht zu.** In der frischen Installation:

| Liste | Regeln gesamt | davon `Edit(pfad)` | davon `Write(pfad)` – nie konsultiert |
|---|---|---|---|
| `deny` | 69 | 15 | **15** |
| `ask` | 6 | 1 | **1** |
| `allow` | 8 | 0 | 0, aber ein `Glob(**)` – ebenfalls nie konsultiert |

**17 Regeln ohne Wirkung, jede davon mit einer Startwarnung.** Der Schutz selbst hält, weil die
`Edit(...)`-Hälfte greift; die beschriebene Verschärfung ist aber keine.

Verschärfend: **Vier** der wirkungslosen Regeln stehen in
`_core_rules_integrity.deny_must_contain` – `Write(./CLAUDE.md)`, `Write(.claude/**)`,
`Write(leitwerk-core/**)` und `Write(project-overlay/**)`. Der Validator **erzwingt** damit die
Anwesenheit von Regeln, die der Client ignoriert: Ein Projekt, das sie folgenlos entfernte,
bekäme vier Fehler gemeldet.

Nicht betroffen ist eine Regel ohne Pfad: „Claude Code doesn't warn about a tool-name rule with
no path, such as a deny rule for `Write`; it matches that rule at the tool level everywhere."

### AP2-CC-03 – R2 und R3 sind abbildbar; die Grundlage der Technology Packs existiert

**Schwere: mittel.** Zwei Einstufungen `[NICHT ABBILDBAR]` sind überholt. **Behoben mit `CR-2026-017` (Release 0.15.0) – siehe Nachtrag 2.**

Die Matrix führt R2 („Regeldateien mit Ladebedingungen") und R3 („Regeln an Dateimuster bindbar
– Grundlage der Technology Packs") als **kein Äquivalent**, weil `@pfad`-Importe immer geladen
werden. Das ist für Importe richtig und für den Client falsch. `docs/en/memory` beschreibt
`.claude/rules/`:

> „Rules can be scoped to specific files using YAML frontmatter with the `paths` field. These
> conditional rules only apply when Claude is working with files matching the specified
> patterns. […] Rules without a `paths` field are loaded unconditionally."

Das ist eine wörtliche Entsprechung beider Zusagen: Ladebedingung und Bindung an Dateimuster,
mit Glob-Syntax und Mehrfachmustern. Ein Technology Pack (Ebene 6) ließe sich bei diesem Client
damit nativ abbilden statt als „nicht abbildbar" zu entfallen.

### AP2-CC-04 – R4: Ein Zeichenlimit ist dokumentiert

**Schwere: mittel.** Die Matrix sagt „Kein Limit dokumentiert", eingestuft `[NICHT ABBILDBAR]`.

`docs/en/memory`: „Claude Code loads a CLAUDE.md file of up to **4 MiB** in full and skips a
larger file." Zusätzlich als Empfehlung: „target under 200 lines per CLAUDE.md file. Longer
files consume more context and reduce adherence."

Es gibt also eine harte Grenze, die das Framework einhalten kann, und eine weiche, an der es
sich ausrichten sollte. Die Laufzeitschicht liegt weit darunter (`00-framework-core.md`: 3.946
Zeichen). Die Einstufung ist auf `[TECHNISCH]` zu heben, das Limit im Pack zu nennen.

### AP2-CC-05 – M2: Eine technische Sperre gegen den Modus ohne Rückfragen existiert

**Schwere: mittel.** Die Matrix sagt: „Ob eine **technische** Sperre über verwaltete
Einstellungen möglich ist, ist nicht belegt", eingestuft `[TEXTUELL]`.

Zwei belegte Mechanismen:

> „To prevent `bypassPermissions` or `auto` mode from being used, set
> `permissions.disableBypassPermissionsMode` or `permissions.disableAutoMode` to `"disable"` in
> any settings file. These are most useful in managed settings where they can't be overridden."

> „`permissions.defaultMode` values `auto` and `bypassPermissions` don't take effect from project
> or local settings; set them in user or managed settings instead […] Before v2.1.257,
> `bypassPermissions` took effect from any file."

D-05 untersagt den Bypass-Modus als Regel. Der Client kann ihn zusätzlich technisch sperren –
in verwalteten Einstellungen unüberschreibbar. Die Einstufung ist auf `[TECHNISCH]` zu heben,
mit dem Vorbehalt, dass verwaltete Einstellungen eine Enterprise-Voraussetzung sind.

### AP2-CC-06 – A1: Feldname bestätigt, Kommentar der Kernvorlage falsch

**Schwere: gering.**

Der Marker fragt nach dem Frontmatter-Feld des Subagentenprofils. `docs/en/subagents` führt
`tools` als Feldnamen; die 22 Agentendefinitionen auf der Prüfmaschine verwenden ausnahmslos
`tools:`. Die erzeugte Datei `.claude/agents/fw-reviewer.md` ist damit **korrekt**.

Falsch ist ihr eigener Kommentar: „Mechanismus: `.claude/agents/<name>.md` mit Frontmatter
`name`, `description`, **`allowed-tools`** `[DOK]`". Er steht in der Kernvorlage
`framework/runtime/agents/fw-reviewer.md` und wird in jedes Pack installiert. `allowed-tools`
ist der Feldname bei **Skills**, nicht bei Subagenten – zwei Mechanismen mit ähnlichem Zweck und
verschiedenen Feldnamen, im Kommentar vertauscht.

Zusätzlich belegt: Die Beschränkung wirkt technisch, und es gibt ein ergänzendes
`disallowedTools`.

### AP2-CC-07 – B9: Eine `deny`-Regel ist nicht lockerbar

**Schwere: gering.** Die Matrix führt B9 als `[TEXTUELL]` mit `[EMPF]` und dem Marker „ob eine
Lockerung technisch verhindert wird".

> „If a tool is denied at any level, no other level can allow it. For example, a managed settings
> deny can't be overridden by `--allowedTools`, and `--disallowedTools` can add restrictions
> beyond what managed settings define."

Die nutzerlokale Datei rangiert zwar **über** der Projektdatei (Reihenfolge: verwaltet →
Kommandozeile → `settings.local.json` → `settings.json` → Nutzer), kann eine dort gesetzte
Verweigerung aber nicht aufheben. Die Zusage „nutzerlokale Konfiguration kann nur verschärfen"
gilt für ihren wichtigsten Teil technisch. Ergänzend: „`deny` and `ask` rules apply right away",
während `allow`-Regeln erst nach dem Vertrauen in den Ordner greifen – eine Verschärfung
zugunsten des Frameworks.

### AP2-CC-08 – B6: Präfixsemantik bestätigt, mit dokumentierter Grenze

**Schwere: Hinweis.**

Die Matrix beschreibt Befehlsverbote als präfixbasiert und damit breiter. Bestätigt: `Bash(ls
*)` trifft auch `ls`, `:*` ist die gleichwertige Schreibweise, `Bash(git * main)` trifft jedes
Unterkommando.

Dokumentiert ist auch die Grenze, die das Pack bisher nicht nennt:

> „A push written another way, such as `git -C . push`, isn't matched."

Ein Befehlsverbot ist damit kein vollständiger Schutz, sondern eine Hürde. Das gehört in die
Fähigkeitsmatrix, weil B6 eine Kernzusage ist.

## Nicht abschließend geklärt

**X2 – Art und Ort der Codebasis-Indexierung.** Die Matrix sagt „Kein Indexierungsmechanismus
dokumentiert; Dateien werden bei Bedarf gelesen". In den fünf abgerufenen Seiten findet sich
kein Indexierungsmechanismus, und die Beschreibung des Ladeverhaltens stützt die Aussage. Ein
Beleg durch Abwesenheit bleibt aber schwächer als ein Beleg: Der Marker wird auf `[DOK]
(Abwesenheit belegt, Stand 2.1.267)` gesetzt statt entfernt.

**AP2-CC-12 – `permissionMode` im Subagentenprofil.** Die Zeile M2 stützt sich darauf, dass
`permissions.disableBypassPermissionsMode` den Modus ohne Rückfragen sperrt. `docs/en/sub-agents`
führt für ein Subagentenprofil ein **eigenes** Frontmatter-Feld `permissionMode`, das unter
anderen Werten auch `bypassPermissions` annimmt. Ob die Sperre auch dort greift, sagt keine der
fünf abgerufenen Seiten. Solange das offen ist, gilt M2 für die Hauptsitzung als belegt und für
den Weg über ein Subagentenprofil als ungeklärt. Das Framework liefert genau ein Profil aus
(`fw-reviewer`), und es setzt das Feld nicht; ein Projekt könnte es setzen. **Nachgetragen mit
Release 0.16.0** beim Abgleich der Quellenliste (`FW-AK-01`, `CR-2026-018`).

## Sitzungsnachweise – Stand nach den Wirkungsnachweisen (2026-09-10)

Die folgenden Nachweise verlangen eine Sitzung, die **in** der Installation startet, weil
Berechtigungen und Regeln beim Sitzungsstart gelesen werden. Sie sind mit
`tests/protocols/2026-09-10-AP2-claude-code-wirkungsnachweise.md` teilweise geführt.

| Nachweis | Erwartung | Stand |
|---|---|---|
| `FW-DS-02` – Read-Sperre wirkt | Eine `.env`-Testdatei ist nicht lesbar; Hinweis statt Inhalt | **belegt** (WN-5), technisch isoliert gegen die Anweisungsebene |
| R2 / R3 an der Wirkung | Eine Regel ohne `paths` steht im Kontext; eine Regel mit `paths` erst nach dem Lesen einer passenden Datei | **belegt** (WN-2, WN-3) |
| Startwarnungen aus AP2-CC-02 | keine Meldung über wirkungslose Regeln | **belegt** (WN-1) |
| H2 – Hook blockiert | Werkzeugausführung unterbleibt | **belegt** (`CR-2026-021`, SN-3) – technisch, in einer Umgebung ohne jede Anweisungsebene. Bis 0.19.0 widerlegt, weil der Hook nicht lief |
| B4 an der Wirkung | `Edit(leitwerk-core/**)` blockiert | offen |
| B7 / S4-Ersatz | Jede Schreiboperation löst eine Rückfrage aus | offen |
| AP2-CC-12 – `permissionMode` im Subagentenprofil | Ein Profil mit `permissionMode: bypassPermissions` startet bei gesetztem `disableBypassPermissionsMode` nicht oder ohne den Modus | offen |
| `FW-ZA-06` – Schreibverbot auf den Kern in realer Installation | blockiert | offen |

Drei Befunde kamen bei den Nachweisen dazu:

- **AP2-CC-13** – beide Hooks laufen unter Windows nicht, Schwere hoch. **Behoben mit
  `CR-2026-021` (Release 0.19.0, D-29):** Der Interpreter wird an seiner Wirkung geprüft statt
  angenommen, Prüfung 15 setzt es als Fehler durch. Damit ist auch **H2 belegt** statt widerlegt.
- **AP2-CC-14** – die `allow`-Regeln wirken erst nach dem Vertrauensdialog. **Offen**; der Weg
  zur Behebung liegt außerhalb des Repositorys. Eine Verschärfung, kein Bruch von B9.
- **AP2-CC-15** – die Lesesperre gilt für `Read`, nicht für Shell-Lesebefehle. **Offen, aber
  entschärft:** Was die `deny`-Liste beim Lesen über die Shell nicht abdeckt, finge der
  Schutz-Hook ab – und der läuft seit 0.19.0.


## Bewertung

Zehn Marker geprüft, **acht Befunde** aus dem Abgleich, davon zwei schwer; ein neunter (AP2-CC-09) kam bei der Behebung dazu, siehe Nachtrag. Zwei Einstufungen `[NICHT ABBILDBAR]`
(R2, R3) und zwei weitere (R4, S4) sind überholt; der Client kann mehr, als das Pack ihm
zutraut. Eine Einstufung `[TEXTUELL]` (M2) und eine (B9) sind auf `[TECHNISCH]` zu heben.

Das Muster ist bemerkenswert: **Kein einziger Befund lautet, das Pack habe eine Fähigkeit
behauptet, die der Client nicht hat.** Sechs von acht lauten umgekehrt – das Pack hat
unterschätzt, was der Client leistet, und einen Ersatz gebaut, wo eine native Kontrolle
existiert. Der gefährlichste Befund (AP2-CC-01) ist genau von dieser Art: Eine Kernregel, die
der Validator in der Quelle erzwingt, wird beim Rendern verworfen, obwohl der Zielclient ein
Feld dafür hat.

Der zweitgefährlichste (AP2-CC-02) ist die Ausnahme, die die Regel bestätigt: Dort hat das Pack
eine Verschärfung beschrieben, die keine ist – 17 Regeln ohne Wirkung, sechs davon vom
Validator erzwungen.

**Ergebnis: AP2 für `claude-code` ist begonnen und nicht abgeschlossen.** Die Marker sind
belegt oder korrigiert; die Wirkungsnachweise stehen aus. AP2-CC-01, AP2-CC-02 und der bei der
Behebung gefundene AP2-CC-09 sind mit `CR-2026-016` (Release 0.14.0) behoben – siehe Nachtrag.

## Nachtrag: Behebung mit Release 0.14.0 (`CR-2026-016`, D-26)

AP2-CC-01 und AP2-CC-02 sind behoben. Bei der Behebung kam ein dritter schwerer Befund dazu.

### AP2-CC-09 – Die in Abschnitt 7 vorgeschriebene Prüfung ist nie gelaufen

**Schwere: hoch.** Gefunden beim Versuch, die Behebung zu prüfen.

`CLIENT_PACK.md` Abschnitt 7 nennt zwei Befehle: `install.py --client claude-code`, dann
`validate-framework.py`. Nacheinander ausgeführt – gegen den unveränderten Stand 0.13.0 – meldet
der Validator **zwölf Fehler „triggers fehlt"**. Er verlangt das Feld unbedingt, während die
Abbildung es für diesen Client verwirft. Die beiden Befehle widersprachen einander seit 0.5.0.

Dieselbe Prüfung trug einen zweiten Defekt: `allowed-tools` steht in der installierten Fassung
als **kommagetrennte Zeichenkette**. Die Prüfung `any(t in ("edit","exec","write") for t in
tools)` lief damit über die *Zeichen* dieser Zeichenkette und meldete jeden installierten Skill
als nicht schreibend.

**Damit ist erklärt, warum AP2-CC-01 acht Releases unbemerkt blieb:** Die Prüfung, die es hätte
finden müssen, war gegen diese Installation nie gelaufen – und hätte es auch nicht gefunden.

### Was 0.14.0 ändert

| Befund | Behebung | Wirkung |
|---|---|---|
| AP2-CC-01 | `model_invocation_field` im Manifest; `triggers` ohne `model` wird zu `disable-model-invocation: true` | 9 von 12 Skills tragen die Sperre; die drei ohne sind die rein lesenden mit `model`-Trigger |
| AP2-CC-02 | `permission_tools.write` → `["Edit"]`, `search` → `[]`; neues `permission_path_tools` | Berechtigungsdatei 83 → 65 Regeln, `deny_must_contain` 17 → 13 |
| AP2-CC-09 | Validator liest beide Formen von `allowed-tools`, führt Werkzeugnamen über `tool_names` zurück und prüft bei abgebildetem `triggers` das Zielfeld | Beide Befehle laufen nacheinander mit **0 Fehlern** – erstmals seit 0.5.0 |

Zusätzlich eine neue Prüfung: Eine Pfadregel für ein Werkzeug, für das der Client keine
Pfadregeln auswertet, ist ein Fehler. Ohne die Manifestangabe `permission_path_tools` unterbleibt
sie – bei `devin-desktop` ist sie unbelegt und wird deshalb nicht behauptet.

### Wirksamkeitsnachweis (D-23)

Vier Sonden in einer frischen `claude-code`-Installation. Ausgangs- und Schlusslauf je 0 Fehler.

| Sonde | Eingebrachter Defekt | Ergebnis |
|---|---|---|
| S1 | `disable-model-invocation` aus `fw-change-small` entfernt | **gemeldet:** „schreibender/ausführender Skill ohne 'disable-model-invocation: true'" |
| S2 | dasselbe Feld auf `false` gesetzt | **gemeldet:** dieselbe Meldung |
| S3 | `Write(leitwerk-core/**)` von Hand in `deny` eingefügt | **gemeldet:** „nennt ein Werkzeug, für das dieser Client keine Pfadregeln auswertet" |
| S4 | `NotebookEdit(project-overlay/**)` eingefügt | **gemeldet:** dieselbe Meldung |

### Was der Nachtrag nicht belegt

**Dass die Sperre gesetzt wird, ist nicht dasselbe wie, dass sie greift.** Der Beleg dafür steht
weiter unter „Offen" und braucht eine Sitzung in der Installation. Bis dahin ist S4 belegt als
`[DOK]` – dokumentiert und korrekt gesetzt –, nicht als beobachtete Durchsetzung.

Ebenfalls offen bleibt eine Unsicherheit aus AP2-CC-02: Ob `Grep(pfad)` tatsächlich nicht
ausgewertet wird, stützt sich auf die Formulierung „checks file permissions against `Edit(path)`
and `Read(path)` rules **only**"; in der Warnliste des Herstellers ist `Grep` nicht genannt. Die
Regel wurde entfernt, weil `Read(**)` den Lesezugriff ohnehin abdeckt. Die Startwarnungen einer
realen Sitzung entscheiden es endgültig.

## Bekannte Grenzen

- Geprüft wurde gegen die Dokumentation und die erzeugten Artefakte, nicht gegen das Verhalten
  einer laufenden Sitzung. Ein Dokumentenabgleich belegt `[DOK]`, nicht `[TECHNISCH]` im Sinne
  einer beobachteten Durchsetzung.
- Die geprüfte Clientversion ist die auf der Prüfmaschine laufende (2.1.267). Die **verbindliche
  Zielversion** ist eine Festlegung des `<FRAMEWORK_OWNER>` und steht weiterhin aus; bis dahin
  gilt das Pack als gegen eine Version geprüft, nicht als für eine Version freigegeben.
- Das Client Pack `devin-desktop` ist unberührt. Seine zwölf Marker brauchen eine Installation
  von Devin Desktop; nichts an diesem Protokoll überträgt sich darauf.
- Fünf Dokumentationsseiten wurden ausgewertet. Marker, die Sandbox-Verhalten je Betriebssystem
  oder Enterprise-Einstellungen betreffen, sind darin nur gestreift.


## Nachtrag 2: Behebung von AP2-CC-03 mit Release 0.15.0 (`CR-2026-017`, D-27)

AP2-CC-03 ist behoben. Bei der Umsetzung kamen ein weiterer Befund und eine bisher unbenannte
Grenze dazu.

### Was der Befund tatsächlich umfasste

Der Protokollpunkt oben nennt zwei Matrixzeilen. Die Prüfung der Mechanik hat gezeigt, dass an
derselben Fehlannahme drei weitere Dinge hingen:

1. **Die Importe waren nie nötig.** `docs/en/memory`: „Rules without a `paths` field are loaded
   unconditionally." Der gesamte Mechanismus – Regeldatei plus Eintrag in der Wurzel-Anweisung,
   samt der eigens dafür gebauten Validatorprüfung „nicht eingebunden, die Regel wäre
   wirkungslos" – beruhte darauf, dass der Client Regeldateien nicht von sich aus lädt. Er tut
   es.

2. **AP2-CC-10 (neu) – eine aktivierte Role-Pack-Regel wurde nie geladen.** `install.py` bindet
   nur die vier Core-Regeln ein. Ein Projekt, das ein Role Pack aktiviert, legte
   `30-role-<name>.md` in die Regelablage, wo sie mangels Import wirkungslos blieb. Das ist genau
   der stille Fehlerfall, den das Client Pack in Abschnitt 5 selbst beschrieben hatte –
   eingetreten am framework-eigenen Mechanismus. Dieselbe Datei lief zudem nie durch
   `render_rule`: Die Formtransformation griff ausschließlich für `framework/runtime/rules/`,
   nicht für die Regelvorlagen unter `templates/rules/` und nicht für die Laufzeitfassungen der
   Packs. **Schwere: hoch** – eine Regelebene des Frameworks (Ebene 6) war bei diesem Client
   ohne Wirkung, ohne dass irgendetwas es gemeldet hätte.

3. **Ein Technology Pack hatte hier kein Zuhause.** Die beiden im Pack genannten Ersatzwege –
   verschachtelte `CLAUDE.md` oder Import – waren beide Notlösungen für ein Problem, das der
   Client nicht hat.

### AP2-CC-11 (neu) – `claudeMdExcludes` ist eine Lücke in B9

**Schwere: mittel.** Betrifft eine Kernzusage der Fähigkeitsmatrix.

`docs/en/memory`:

> „The `claudeMdExcludes` setting lets you skip specific files by path or glob pattern. […]
> Patterns are matched against absolute file paths using glob syntax. You can configure
> `claudeMdExcludes` at any settings layer: user, project, local, or managed policy. Arrays
> merge across layers."

Das Beispiel des Herstellers schließt ausdrücklich ein Regelverzeichnis aus. Eine nutzerlokale
`.claude/settings.local.json` kann damit Regeldateien vom Laden ausnehmen – eine **Lockerung**,
während B9 zusagt, dass nutzerlokale Konfiguration nur verschärfen kann. Für Berechtigungen
gilt B9 unverändert („If a tool is denied at any level, no other level can allow it"); für
Regeltexte gilt sie nicht.

Die Lücke ist **nicht neu und nicht Folge dieser Änderung**: Vor 0.15.0 hätte ein Muster auf die
Wurzel-Anweisungsdatei sämtliche importierten Regeltexte auf einmal entfernt. Neu ist allein,
dass sie benannt ist. Der KI-Client selbst kann die Datei nicht schreiben – `Edit(.claude/**)`
steht in `deny` –, ein Mensch schon. Nur eine über verwaltete Einstellungen ausgelieferte
`CLAUDE.md` ist gegen Ausschluss geschützt; ob sich daraus eine Gegenmaßnahme bauen lässt, ist
eine Frage an die noch offenen Enterprise-Marker.

### Was 0.15.0 ändert

| Befund | Behebung | Wirkung |
|---|---|---|
| AP2-CC-03 | Regelablage in `.claude/rules/`; `rule_triggers` im Manifest bildet jeden Ladetrigger der Kernquelle ab | R2 und R3 auf `[TECHNISCH]`; `[NICHT ABBILDBAR]` 4 → 0. Ein Technology Pack liegt als `40-tech-<name>.md` mit `paths:` |
| AP2-CC-10 | `ist_regelquelle` erfasst zusätzlich `templates/rules/` und die Pack-Laufzeitfassungen; eine Regeldatei wirkt ohne Import | Eine aktivierte Role-Pack-Regel lädt und ist in der Form des Clients gerendert |
| AP2-CC-11 | keine – die Lücke ist ausgewiesen, nicht geschlossen | Client Pack Abschnitt 5 und die Laufzeit-README benennen sie |

Die Abbildung der drei Ladetrigger:

| Ladetrigger der Kernquelle | Fassung bei `claude-code` | Bewertung |
|---|---|---|
| `always_on` | kein `paths`-Feld | wörtliche Entsprechung |
| `model_decision` | kein `paths`-Feld | Verschärfung – mehr Regeln aktiv, nicht weniger |
| `glob` mit `globs` | `paths:` mit denselben Mustern | wörtliche Entsprechung |
| `manual`, `agent` | keine Abbildung | Die Installation scheitert (D-27) |

Drei neue Prüfungen des Validators für einen Client mit eigener Bedingungssprache: ein
Frontmatter-Feld, das der Client nicht auswertet, ist ein Fehler (K-18); die Ladebedingung muss
die Form haben, die der Client erwartet; und **eine Kernregel darf keine Ladebedingung tragen** –
sie gilt für jede Aufgabe, sie an Dateimuster zu binden wäre eine Lockerung.

Zusätzlich: `install.py` rendert alle Quellen, bevor es die erste Datei schreibt. Vorher brach
eine nicht abbildbare Quelle die Installation mitten im Schreiben ab und hinterließ ein halb
angelegtes Projekt.

### Wirksamkeitsnachweis (D-23)

Sechs Sonden in einer frischen `claude-code`-Installation (79 Dateien, `install.py --client
claude-code`, danach `README.md` angelegt). Ausgangslauf: 0 Fehler. Jede Sonde wurde einzeln in
eine unveränderte Kopie eingebracht.

| Sonde | Eingebrachter Defekt | Ergebnis |
|---|---|---|
| S1 | Quellfrontmatter in `.claude/rules/15-development-rules.md` stehen gelassen (`trigger: model_decision`) | **gemeldet:** „Frontmatter-Feld 'trigger' – dieser Client wertet für Regeldateien nur ['paths'] aus (K-18). Ein stehen gebliebenes 'trigger' oder 'globs' heißt: Die Datei ist nicht durch die Abbildung des Client Packs gelaufen, ihre Ladebedingung ist verfallen" |
| S2 | `paths: ["src/**"]` an der Kernregel `10-privacy-security.md` | **gemeldet:** „Kernregel über 'paths' an Dateimuster gebunden – sie gilt für jede Aufgabe; eine Ladebedingung wäre hier eine Lockerung" |
| S3 | `40-tech-java.md` mit `paths: "**/*.java"` als Zeichenkette | **gemeldet:** „'paths' muss eine nichtleere Liste von Dateimustern sein" |
| S4 | dasselbe mit `paths: []` | **gemeldet:** dieselbe Meldung |
| S5 | Ladetrigger `manual` in der Kernquelle `15-development-rules.md` | **Installation scheitert:** „Ladetrigger 'manual' hat keinen Eintrag in rule_triggers.map - die Regel liesse sich nur durch Weglassen der Ladebedingung abbilden, und das waere ein Verlust der Zusage (D-27). Bekannt: always_on, glob, model_decision"; Exit-Code 1, **kein Verzeichnis angelegt** |
| S6 | `trigger: glob` ohne `globs` in derselben Quelle | **Installation scheitert:** „Ladetrigger 'glob' bildet auf 'paths' ab, die Quelle nennt aber keine Dateimuster - die Ladebedingung waere leer" |

Vier Gegenproben:

| Gegenprobe | Erwartung | Ergebnis |
|---|---|---|
| G1 | Ein korrektes Technology Pack (`paths` als Liste, zwei Muster, eines mit Klammer-Expansion) bleibt fehlerfrei | 0 Fehler |
| G2 | Eine Regeldatei ganz ohne Frontmatter bleibt fehlerfrei | 0 Fehler |
| G3 | Die Prüfung aus `CR-2026-016` meldet weiterhin: `disable-model-invocation` aus `fw-change-small` entfernt | gemeldet |
| G4 | Die zweite Prüfung aus `CR-2026-016` meldet weiterhin: `Write(leitwerk-core/**)` in `deny` eingefügt | gemeldet |

G3 und G4 sind Regressionsproben: Keine der neuen Prüfungen hat eine bestehende verdrängt.

### Was der Nachtrag nicht belegt

**Dass eine Regel geladen wird, ist dokumentiert, nicht beobachtet.** Der Beleg dafür, dass eine
Regel ohne `paths` tatsächlich im Kontext steht – und eine Regel mit `paths` erst nach dem Lesen
einer passenden Datei –, braucht eine Sitzung *in* der Installation und steht unter „Offen".

Ebenfalls nicht belegt: dass ein `paths`-Muster in der Praxis so trifft, wie die Dokumentation es
beschreibt. Die dokumentierten Grenzen – ein ungültiger Klammerausdruck trifft nichts, das
Expansionsbudget von 1.000 Mustern – sind übernommen, nicht nachgestellt.

## Gegenzeichnung (Prüfmethode `review`)

Rollen statt Personen (`framework/runtime/rules/20-project-overlay.md`). AP2 ist ein
Arbeitspaket, kein Testfall des Katalogs; die Prüfmethode dieses Protokolls ist gleichwohl
`review`, und D-23 verlangt dafür eine **zweite Rolle**. Ein grüner Lauf und ein
Wirksamkeitsnachweis ersetzen sie nicht.

**Zur Entscheidung vorgelegt** – drei Auflösungen mit Ermessensspielraum, jede einzeln:

| Nr. | Frage | Vorgeschlagene Auflösung | Preis |
|---|---|---|---|
| E1 | Regelablage ganz nach `.claude/rules/` oder nur die Technology Packs? | Ganz. Zwei Regelablagen mit zwei Lademechanismen bei einem Client wären schwerer zu erklären als der einmalige Umzug, und nur der vollständige Weg beseitigt AP2-CC-10 | Ein bestehendes Projekt zieht von Hand nach (CHANGELOG, Migrationshinweise). Es gibt keines |
| E2 | Die Zeile S4 im selben Release mit berichtigen, obwohl sie zu `CR-2026-016` gehört? | Ja. Ihre Abbildung ist seit 0.14.0 ausgeliefert; die Matrix stand falsch. Dasselbe gilt für die Restangaben zu AP2-CC-02 in vier Abschnitten des Packs | Der Antrag berichtigt Aussagen über eine fremde Änderung. Ohne die Berichtigung stünde die Matrix bis zum nächsten Anlass falsch |
| E3 | Die Importmechanik entfernen, weil sie kein Pack mehr nutzt? | Nein, erhalten – manifestgesteuert, für ein künftiges Pack. Aber als von keinem Pack erprobt ausweisen | Unerprobter Code im Kern. Die Gegenposition ist `CR-2026-016`: „Eine wirkungslose Regel vorzuhalten ist das Gegenteil einer ausgewiesenen Durchsetzungstiefe" |

| Rolle | Datum | Ergebnis |
|---|---|---|
| Ersteller des Reviews (KI-gestützt, Sitzung) | 2026-09-10 | AP2-CC-03 behoben; zwei weitere Befunde (AP2-CC-10, AP2-CC-11) aufgenommen; sechs Sonden gemeldet, vier Gegenproben wie erwartet |
| Zweite Rolle: `<FRAMEWORK_OWNER>` | `<TBD: Datum>` | `<TBD: Abnahme; E1, E2 und E3 einzeln entscheiden>` |

Solange die zweite Zeile offen ist, ist dieser Nachtrag **vorgelegt, nicht abgezeichnet**.

# Änderungsantrag `CR-2026-065`

| Feld | Inhalt |
|---|---|
| Titel | Zwei Enthaltungen von `devin-desktop` sind erhoben – und eine war keine Enthaltung, sondern eine falsche Behauptung |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-14 |
| Betroffene Artefakte | `clients/devin-desktop/manifest.json` (`hook_tools`, `hook_tools_absent`, `permissions_note`, `permission_tools`-Noten, beide `tool_names`-Blöcke), `clients/devin-desktop/CLIENT_PACK.md` (Verbtabelle, Zeilen S2, S3, B3, Änderungsverlauf), `install.py` (die Abbildung wirkt auch in der Listenform), `tests/scripts/validate-framework.py` (Prüfung 41 neu, Prüfung 38 namensraumbewusst, Register), `tests/scripts/probe-pruefungen.py`, `governance/DECISION_LOG.md`, `docs/ROADMAP.md`, `CHANGELOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – ein Client Pack und die Durchsetzungsschicht sind Framework-Gut |
| Art | Änderung; Anlass sind **Kandidat 1 und 6** der Übergabe, in einer Sitzung erhoben |
| Dringlichkeit | **P1.** Eine Werkzeugklasse ist per Deklaration aus der fail-closed-Schicht genommen, und die Deklaration ist **gemessen falsch**. Dass die zweite Schicht heute trägt, ist Entlastung, nicht Entwarnung |

## 1. Anlass

Beide Fragen standen als **Enthaltung** im Manifest, und der Änderungsverlauf des Packs sagt
seit 0.10.0: *„Beides kann nicht stimmen; welche Seite falsch ist, entscheidet eine
Erhebung."* Sie liegt vor: `tests/protocols/2026-09-14-erhebung-devin-werkzeuge.md`, **elf
Läufe am Client**, davon zwei Kontrollläufe, ein Entlastungslauf, ein verworfener Lauf und
einer mit berichtigtem Messartefakt.

### 1.1 Befund 1: „Dieser Client führt kein eigenes Suchwerkzeug" ist falsch

Die Mitschrift führt unter `agent.tool_definitions` den Werkzeugbestand selbst – **25
Werkzeuge**, darunter `grep` („a powerful search tool built on ripgrep") und
`find_file_by_name` („fast file name/path pattern matching … using glob patterns"). **Ein
Werkzeug `glob` gibt es nicht.**

**Die Folge ist gemessen.** Aus `hook_tools_absent: ["search"]` erzeugt `install.py` den
Matcher `read|exec|edit|write`; beim Pack `claude-code` lautet dieselbe Stelle
`Read|Grep|Glob|Bash|Edit|Write|NotebookEdit`. In einer Umgebung mit **nur** dem Hook:

| Lauf | Werkzeug | Ergebnis |
|---|---|---|
| **H1** *(Positivkontrolle)* | `read` auf `.env` | **blockiert** |
| **H2** | `grep` auf `.env` | **durchgelassen**, Secret wörtlich |

**Das Hook-Skript ist nicht das Problem** – von Hand gefüttert blockiert es beide Aufrufe. Es
wird nicht gefragt.

### 1.2 Die Entlastung – und warum sie den Befund nicht aufhebt

**Wie ausgeliefert ist das Secret geschützt.** Die Berechtigungsklasse `Read(...)` dieses
Clients umfasst das Suchwerkzeug mit: Lauf **P4** (nur `permissions`) und Lauf **W1** (wie
ausgeliefert) weisen denselben `grep`-Aufruf ab.

**Trotzdem ist es ein Befund.** Die Berechtigungsdatei gehört dem Projekt und ist
bearbeitbar – genau deshalb gibt es Prüfung 37, seit ein Projekt 41 `deny`-Regeln löschen
konnte, ohne dass ein Lauf davon Notiz nahm (D-77). Der Hook ist die Schicht, die das
überleben soll (D-31). **Hier trägt nur die editierbare Schicht; die zweite ist per
Deklaration abgeschaltet.**

### 1.3 Befund 2: Der Skillaufruf ist ein Werkzeugaufruf (K-33)

`permission_tools.skill: []` war als **unerhoben** deklariert. Gemessen: Der Client führt ein
Werkzeug `skill`; die Mitschrift zeigt
`{"function_name": "skill", "arguments": {"command": "invoke", "skill": "fw-code-explain"}}`.

**Und ein zweiter Weg, den niemand gesucht hat:** Die Slash-Form wird **clientseitig**
expandiert – im `user`-Schritt der Mitschrift steht der Inhalt der `SKILL.md`, nicht der
Befehl. **Eine Schranke auf dem Werkzeug erreicht diesen Weg gar nicht.**

**Die Schranke selbst greift nicht**, in zwei Schreibweisen: `Skill(fw-code-explain)` (P2)
und `skill(fw-code-explain)` (P3) laufen durch, während `Read(**/.env)` in **derselben Datei
und denselben Läufen** abweist (P1b, **Kontrolllauf**).

**Im Ergebnis bleibt die leere Liste richtig; ihre Begründung wird falsch.**

### 1.4 Befund 3 – nicht gesucht: `glob` benennt bei diesem Client nichts

Jede ausgelieferte Skilldatei trägt `allowed-tools: read, grep, glob`. `read` und `grep` sind
Werkzeugnamen dieses Clients, **`glob` ist keiner** – das glob-förmige Werkzeug heißt
`find_file_by_name`, und die Skills benutzen es, ohne dass ihre Liste es nennt.

### 1.5 Befund 4 – der systemische: Prüfung 26 prüft Folgerichtigkeit, nicht Wahrheit

D-47 wurde gebaut, damit **ein Pack eine Werkzeugklasse nicht dadurch aus der Durchsetzung
nehmen kann, dass es sie weglässt** – eine Abwesenheit muss erklärt werden. Prüfung 26
erzwingt seither, dass die Erklärung **vorhanden** und **mit `permission_tools` widerspruchsfrei**
ist. **Beides war hier erfüllt, und die Erklärung war trotzdem falsch.**

Der Unterschied, den niemand verlangt hat: `agent_start_tools_absent` sagt **„UNERHOBEN,
nicht abwesend"** – eine Enthaltung. `_hook_tools_absent_note` sagte **„Dieser Client führt
kein eigenes Suchwerkzeug"** – eine **Behauptung ohne Datum und ohne Protokoll.** Die eine
Bauform ist ehrlich, die andere sieht genauso aus und ist es nicht.

### 1.6 Befund 5 – bei der Umsetzung entstanden: es sind **zwei** Namensräume

**Der erste Entwurf dieser Änderung war falsch, und die Messung hat ihn widerlegt.** Er
trug `glob → find_file_by_name` in beide `tool_names`-Blöcke ein – der Name ist
schließlich gemessen. Danach meldete der Client für dieselbe Skilldatei nur noch
`Allowed tools: read, grep`: **Er hatte den Eintrag lautlos verworfen.**

Eine Sondendatei mit zwölf angebotenen Namen zeigt, warum:

| angeboten | Ergebnis |
|---|---|
| `read`, `grep`, `glob`, `edit`, `exec`, `web_search` | **angenommen** |
| `Read`, `Grep` | angenommen, auf Kleinschreibung normalisiert |
| `find_file_by_name`, `write`, `skill`, ein erfundener Name | **verworfen** |

**Dieser Client führt für das Frontmatter ein eigenes, normalisiertes und geschlossenes
Vokabular** – es ist nicht die Liste seiner Laufzeitwerkzeuge. `glob` ist dort
**richtig**, obwohl es zur Laufzeit kein Werkzeug dieses Namens gibt; `find_file_by_name`
ist dort **falsch**, obwohl es das Werkzeug ist, das läuft.

**Beim Pack `claude-code` fallen beide Namensräume zusammen** (`Read`, `Grep`, `Glob`
sind Frontmatter-Vokabular **und** Werkzeugnamen). Deshalb ist der Unterschied bis 0.42.0
niemandem aufgefallen – und deshalb vergleicht **Prüfung 38, Gegenstand 3** seit D-80
zwei Listen, die nicht in jedem Pack denselben Namensraum führen.

**Ohne die Gegenprobe am Client wäre die Vorabfreigabe von drei Namen auf zwei
geschrumpft**, und der Validator hätte 0 Fehler gemeldet.

## 2. Vorgeschlagene Änderung

1. **`hook_tools.search: ["grep", "find_file_by_name"]`**; `hook_tools_absent` und seine Note
   entfallen. Der erzeugte Matcher deckt die Suchklasse.
2. **`permissions_note` berichtigt** und mit dem gemessenen Grund versehen: Die Suchklasse
   fällt bei diesem Client unter `Read(...)` – belegt durch P4 und W1 –, deshalb entfällt
   eine eigene `Search`-Regel, **nicht weil es keine Suche gäbe.**
3. **Beide `tool_names`-Blöcke abgebildet – als Identität**, gemessen am
   Frontmatter-Vokabular des Clients; `tool_names_unmapped` entfällt,
   `tool_names_namespace` kommt hinzu. **`install.py` wendet die Abbildung jetzt
   auch in der Listenform an** – bis 0.42.0 tat das nur der csv-Zweig, während der
   Agenten-Renderer daneben immer umschrieb: dieselbe Abbildung mit zwei
   Ergebnissen.
4. **`_permission_tools_skill_note`** von „unerhoben" auf gemessen: Das Werkzeug heißt
   `skill`, die Liste bleibt leer, weil keine wirksame Schreibweise bekannt ist. **K-33
   geschlossen, K-34 neu.**
5. **Client Pack**: Verbtabelle, Zeile **B3** (die Zusage, die die falsche Behauptung
   wiederholt), Zeile **S2** (der Aufruf ist ein Werkzeugaufruf, und die Slash-Form ist ein
   zweiter Weg), Zeile **S3**, Änderungsverlauf.
6. **Prüfung 41 (neu)**: Eine Abwesenheitserklärung ist **entweder** als Enthaltung markiert
   **oder** mit Datum und Protokollpfad belegt. Eine bloße Behauptung ist keines von beidem.
7. **Sechs Sonden und zwei Gegenproben** zu Prüfung 41.

## 3. Auswirkungen

| Bereich | Auswirkung |
|---|---|
| Erzeugte Hook-Konfiguration `devin-desktop` | Matcher **`read\|grep\|find_file_by_name\|exec\|edit\|write`** statt `read\|exec\|edit\|write`. **Der Schutz-Hook läuft künftig auch bei Suchaufrufen** – mehr Hook-Aufrufe je Sitzung, je 10 s Zeitfenster |
| Erzeugte Skill- und Profildateien `devin-desktop` | **unverändert** `allowed-tools: read, grep, glob` – gemessen ist das die richtige Liste (Befund 5). Geändert hat sich, dass die Abbildung jetzt **erhoben** ist statt unerhoben, und dass `install.py` sie in der Listenform überhaupt anwendet |
| Erzeugte Berechtigungsdatei | **unverändert** |
| Pack `claude-code` | **unverändert** |
| Bestehende Installationen | **Migrationshinweis:** Nach dem Update ist `install.py --update` nötig, damit Hook-Konfiguration und Skilldateien den neuen Stand tragen. Ohne das bleibt die Lücke bestehen |
| Sicherheit | **Eine Werkzeugklasse kommt in die fail-closed-Schicht zurück.** Kein Schutz wird gelockert |

## 4. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | Wird die Suchklasse in `hook_tools` aufgenommen – obwohl die Berechtigungsschicht sie heute schon deckt? | **Ja.** Die beiden Schichten sollen einander tragen, und die Berechtigungsdatei ist die **editierbare**. Prüfung 37 existiert, weil ein Projekt 41 `deny`-Regeln löschen konnte; der Hook ist die Schicht, die das überleben soll (D-31) | **Jeder Suchaufruf kostet künftig einen Hook-Lauf** mit 10 s Zeitfenster – bei einer Sitzung mit vielen `grep`-Aufrufen ist das spürbar. **Die Gegenposition ist vertretbar:** Wer die Berechtigungsschicht für ausreichend hält, spart die Last. Gemessen ist nur, dass beide Wege heute abweisen |
| **E2** | Wird `glob` auf `find_file_by_name` abgebildet? | **Nein – der Vorschlag war falsch und ist an der Messung gescheitert (Befund 5).** Das Frontmatter dieses Clients führt ein **eigenes** Vokabular; `glob` ist dort richtig, `find_file_by_name` wird verworfen. Die Abbildung ist deshalb die **Identität** – und das ist ein Messergebnis, kein Nichtstun. Der Namensraum wird deklariert (`tool_names_namespace`) | **Prüfung 38, Gegenstand 3 fällt für dieses Pack weg**: Sie vergleicht `tool_names` gegen `hook_tools`, und die leben hier in zwei Namensräumen. **Die Frage von D-80 bleibt für `devin-desktop` offen** – sie ist anders gestellt, nicht beantwortet, und das steht jetzt im Code und im Pack. Der Preis ist ein deklarierter blinder Fleck statt einer falschen Zusage |
| **E3** | Bleibt `permission_tools.skill` leer? | **Ja, mit gemessener Begründung.** Zwei Schreibweisen sind geprüft und beide wirkungslos; eine Regel, die nichts tut, wäre die Bauform von D-66 und D-82 – sie sähe richtig aus | **Eine Lücke bleibt eine Lücke**, und der Skillaufruf ist bei diesem Client über die Berechtigungsdatei nicht kontrollierbar. **Das ist zu sagen, nicht zu verschweigen:** neuer Klärungspunkt **K-34**. Und der Slash-Weg ist ohnehin kein Werkzeugaufruf |
| **E4** | Wird `K-33` geschlossen? | **Ja.** Die Frage lautete „ist der Skillaufruf dort rückfragepflichtig" und ist beantwortet: Er ist ein Werkzeugaufruf, und er ist über diese Datei nicht adressierbar | **Die Nachfolgefrage ist enger und offen** (K-34). Ein geschlossener Klärungspunkt, aus dem ein neuer folgt, sieht nach Stillstand aus und ist Fortschritt: Aus „unbekannt" wurde „bekannt und nicht erreichbar" |
| **E5** | Bekommt die Abwesenheitserklärung eine Prüfung – oder genügt die Lehre im Protokoll? | **Eine Prüfung.** Genau diese Bauform hat eine Werkzeugklasse aus der Durchsetzung genommen, und Prüfung 26 hat sie durchgelassen, weil sie **Folgerichtigkeit** prüft und nicht **Wahrheit**. Was prüfbar ist: ob die Erklärung sich als **Enthaltung** ausweist oder einen **datierten Beleg** nennt | **Sie prüft eine Form, nicht eine Tatsache.** Wer ein Datum und einen Protokollpfad in die Note schreibt, besteht sie – auch wenn das Protokoll etwas anderes sagt. **Sie fängt nach dieser Änderung nichts mehr** und ist eine Verankerung; ihr Gegenbeweis gegen 0.42.0 ist dafür ein **Abzählen** |
| **E6** | Wird der Werkzeugbestand gegen ein zweites Modell gehalten? | **Nein – er ist auf diesem Konto nicht messbar.** Der Versuch endet mit `Error: Upgrade to Pro to access this model`. Elf Läufe auf `SWE-1.6 Slow` zeigen denselben Bestand | **Die Aussage gilt für ein Modell.** Bietet der Client einem anderen Modell einen anderen Bestand an, wäre `hook_tools` erneut zu prüfen. **Das gehört als Grenze in das Pack**, nicht in eine Fußnote |
| **E7** | Eigenes Release oder Anhang? | **Ein eigenes Release, `0.43.0`.** Der Gegenstand ist geschlossen, und er trägt einen Migrationshinweis | **Das achtzehnte Release in drei Tagen.** Und das erste, das einen **Client** misst statt eines Mechanismus – elf Läufe, vier Umgebungen |

## 5. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle sieben Fragen wie vorgelegt.** E1 die Suchklasse kommt in den Hook; **E2 im Vollzug überstimmt** – die Abbildung ist die Identität, weil das Frontmatter dieses Clients ein eigenes Vokabular führt (Befund 5); der Namensraum wird deklariert und Prüfung 38 wird namensraumbewusst; E3 `permission_tools.skill` bleibt leer mit gemessener Begründung; E4 K-33 geschlossen, K-34 neu; E5 Prüfung 41 als Form-, nicht Tatsachenprüfung, Grenze benannt; E6 ein Modell, Grenze im Pack; E7 eigenes Release `0.43.0` |
| Datum | 2026-09-14 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | D-87 (der Werkzeugbestand von `devin-desktop` ist erhoben; die Suchklasse gehört in `hook_tools`), D-88 (eine Abwesenheitserklärung ist Enthaltung **oder** datierter Beleg – nie eine bloße Behauptung), D-89 (der Skillaufruf ist bei `devin-desktop` ein Werkzeugaufruf und über die Berechtigungsdatei nicht adressierbar) |
| Auflagen | **Der Wirkungsnachweis führt einen Lauf am Client**: derselbe `grep`-Aufruf auf `.env` in der Hook-Umgebung, der vor der Änderung durchlief, muss danach blockiert werden. **Ohne diesen Lauf ist die Behebung eine Behauptung.** Und die Grenze wird benannt: ein Modell, ein Konto, elf Läufe |
| Ziel-Release | `0.43.0` |
| Umsetzung | umgesetzt mit `0.43.0` |

# Änderungsantrag `CR-2026-058`

| Feld | Inhalt |
|---|---|
| Titel | Der Unteragent ist erhoben – die Skill-Sperre reicht hinein, A1 steht nicht mehr auf reinem `[DOK]`, und das Startwerkzeug kennt kein Manifest |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-13 |
| Betroffene Artefakte | `clients/claude-code/CLIENT_PACK.md` (Zeilen **S3**, **A1**, **H2**), `clients/claude-code/manifest.json` und `clients/devin-desktop/manifest.json` (neues Feld), `clients/_template/CLIENT_PACK.md` und `clients/README.md` (Vorlage), `framework/core/05-working-model.md` (M1 und die Regel zu Hintergrund-Subagenten), `tests/scripts/validate-framework.py` (Prüfung 32 erweitert, Prüfung 34 neu), `tests/scripts/probe-pruefungen.py`, `tests/EDGE_CASES.md`, `clients/README.md` (Befund 6) |
| Ebene laut Entscheidungsbaum 6 | **Client Pack** (Matrix, Manifest) und **Core** (die Aussage zum Arbeitsmodell) |
| Art | Offener Punkt aus `CR-2026-057` und Eintrag in **Paket 6**; **erhoben am 2026-09-13**, zwölf Läufe, davon sechs Kontroll- und Entlastungsläufe |
| Dringlichkeit | **Paket 6.** Kein P1: Alle drei Befunde fallen **zugunsten** der Durchsetzung aus. Der Antrag holt Belege nach und schließt eine Deklarationslücke; er behebt keine Fehlfunktion |

## 1. Anlass und Befundlage

Die Erhebung liegt vor: `tests/protocols/2026-09-13-erhebung-unteragent.md`. Aufbau wie bei
`CR-2026-057` – ohne Regeltexte, ohne Bypass, mit `allow`-Liste und Rekorder-Hook.

Drei Fragen an denselben Gegenstand, jede seit Längerem benannt:

| Frage | Seit wann offen |
|---|---|
| Gilt `disallowed-tools` eines Skills auch für einen Unteragenten, den der Skill startet? | **Dreimal benannt** – im Protokoll zu `CR-2026-057` („für M1 wäre genau das die nächste Frage"), in `docs/ROADMAP.md` und in der Übergabe |
| Beschränkt das Profilfeld `tools` technisch? | Zeile **A1** sagt es seit **0.7.0** auf `[TECHNISCH]` zu – **auf reinem `[DOK]`-Beleg** |
| Erfasst der Schutz-Hook die Werkzeugaufrufe eines Unteragenten, und blockiert er sie? | Nie gestellt |

### 1.1 Der harte Marker – warum diese Erhebung überhaupt zuordnen kann

Ein Werkzeugaufruf **aus einem Unteragenten** trägt im Umschlag zwei Felder, die der Aufruf
des Hauptagenten nicht trägt: **`agent_id` und `agent_type`** (Profilname). Jede Zuordnung
„dieser Aufruf kam aus dem Unteragenten" stützt sich darauf und nicht auf den Bericht des
Agenten – dieselbe Rolle, die `permission_denials` bei `CR-2026-057` gespielt hat.

### 1.2 Befund 1: Die Skill-Sperre reicht in den Unteragenten

| Lauf | Aufbau | Ergebnis |
|---|---|---|
| **V-M** | Skill mit `disallowed-tools: Write, Edit` startet das Profil `lw-unter-offen` – **ohne eigenes `tools`-Feld** | `Write` und `Edit` fehlten im Vorrat des Unteragenten; `ToolSearch select:Write` ergab wörtlich „No matching deferred tools found" |
| **V-K** | **Kontrolllauf:** derselbe Skill **ohne** das Feld | Unteragent rief `Write` auf, Datei entstand |

**Der Unteragent ist kein Umgehungsweg.** Die Entfernung gilt für den ganzen Turn, und der
Unteragent läuft innerhalb dieses Turns. Die Turngrenze aus D-64 bleibt unberührt.

**Grenze 2 aus D-64 reicht allerdings mit:** Mit gesperrtem `Write, Edit` schrieb der
Unteragent über `Bash` (Lauf **V-E**, Kontrolle **V-EK**). Wer `exec` nicht sperrt, hat den
Unteragenten nicht schmaler gemacht als den Hauptagenten.

### 1.3 Befund 2: Das Profilfeld beschränkt – durch Entfernung, nicht durch Verweigerung

| Lauf | Aufbau | Ergebnis |
|---|---|---|
| **A1-M** | Profil mit `tools: Read, Grep, Glob` | kein Schreibwerkzeug im Vorrat; **`permission_denials` leer** |
| **A1-K** | **Kontrolllauf:** dasselbe ohne `tools` | `Write` gelang |

Derselbe Mechanismus wie `disallowed-tools`: **Entfernung aus dem Vorrat, keine
Berechtigungsregel.** Eine `allow`-Regel holt das Werkzeug nicht zurück.

**Was A1 zusätzlich behauptet, ist weiterhin nur dokumentiert:** dass ein Profil, dessen
`tools`-Liste sich zu keinem Werkzeug auflöst, gar nicht erst startet. Nicht gemessen.

### 1.4 Befund 3: Der Schutz-Hook erfasst und blockiert den Unteragenten

Der Rekorder allein belegt nur, dass der Hook **aufgerufen** wird – nicht, dass er
**entscheidet**. Dieselbe Unterscheidung, an der die Roadmap für 0.30.0 einen Nachweis
vermisst. Deshalb ein Hook mit Exit 2:

| Lauf | Aufbau | Ergebnis |
|---|---|---|
| **H1** | Sperr-Hook, Matcher `*` | **blockiert**, Datei nicht entstanden |
| **H2** | **Gegenprobe im selben Aufbau**, anderes Ziel | Hook sieht denselben Aufruf, lässt durch, Datei entstand |
| **H3** | derselbe Hook, Matcher `Edit\|Write\|NotebookEdit` – **die Form, die `clientmap.py` erzeugt** | **blockiert** |

Ohne H3 wäre nur das Sternchen gemessen, und das erzeugt das Framework nirgends.

**Die B06-Berichtigung trägt hier zum ersten Mal etwas.** `agent_id` und `agent_type` sind zwei
Umschlagfelder, die kein aufgezeichnetes Schema kannte. Ein Hook, der wie bis 0.33.0 „alle
Zeichenketten des Ereignisses" durchsucht, hätte sie mitgeprüft. Seit 0.34.0 wird
ausschließlich `tool_input` geprüft (D-62) – **eine additive Erweiterung des Clients erreicht
die Entscheidung nicht mehr.**

### 1.5 Befund 4: Das Startwerkzeug kennt kein Manifest

Gemessen ist, dass es **sperrbar** ist: `disallowed-tools: Agent` weist den Start ab (Lauf
**V-S**), und `disallowed-tools: Task` ebenso (Lauf **V-S2**) – kein stiller Ausfall wie bei
den Argumentmustern aus D-66.

**Aber die Kanäle nennen es verschieden**, in derselben Sitzung, für denselben Aufruf:

| Kanal | Name |
|---|---|
| Frontmatter `disallowed-tools` | akzeptiert **beide** |
| Umschlag des Hooks (`tool_name`) | `Agent` |
| `permission_denials` | **`Task`** |

Und in **keiner** Werkzeugliste des Manifests steht es: nicht in `hook_tools`, nicht in
`permission_tools`, nicht in `agent_frontmatter.tool_names`. **Ein Kanal ohne Deklaration** –
und genau das hat sich dieses Projekt mit D-47 (`hook_tools_absent`) abgewöhnt.

### 1.6 Befund 5: Prüfung 32 behauptet eine Vollständigkeit, die es nicht mehr gibt

Der Kopfkommentar sagt, sie rufe den Hook „mit dem vollständigen Umschlag **beider**
aufgezeichneter Schemata" auf. Es sind jetzt **drei** aufgezeichnete Formen: die zwei aus den
AP2-Mitschriften und der Unteragenten-Umschlag mit zwei zusätzlichen Feldern.

**Das ist keine Risikobehauptung.** Weder `agent_id` noch `agent_type` trägt heute einen Pfad.
Der Grund ist ein anderer: Eine Prüfung, die ihre Grundlage benennt, darf sie nicht überholt
tragen – sonst ist sie die nächste Aussage, die ihren Gegenstand überlebt hat.

### 1.7 Befund 6: Sieben überholte Angaben in Übersichten, die nichts nachrechnet

**Beim Nachzählen für Zeile A1 aufgefallen, nicht gesucht.** Prüfung 31 rechnet die
Zusammenfassung **im Pack** nach – seit 0.33.0, und dort stimmt sie. Daneben stehen dieselben
Zahlen ein zweites Mal, und **dort rechnet sie niemand**:

| Stelle | Steht da | Gezählt |
|---|---|---|
| `clients/README.md`, `devin-desktop` | `[TECHNISCH]` **24 von 34** | **20 von 36** |
| `clients/README.md`, `devin-desktop` | „**8** Zeilen tragen einen VERIFY-Marker" | **9** |
| `clients/README.md`, `claude-code` | `[TECHNISCH]` **25 von 29** | **22 von 31** |
| `clients/README.md`, `claude-code` | „die Wirkungsnachweise aus einer Sitzung stehen aus" | überholt – S4 beobachtet am 12.09., S3 gemessen am 13.09. |
| `claude-code/CLIENT_PACK.md`, Belegstand | „(bei `devin-desktop`: **8 von 34**)" | **9 von 36** |
| `claude-code/CLIENT_PACK.md`, Belegstand | „beobachtete Durchsetzung … ist für **keine** Zeile belegt" | überholt, dieselben zwei Zeilen |
| `devin-desktop/CLIENT_PACK.md`, Belegstand | „**8 der 36** Zeilen tragen einen offenen VERIFY-Marker – S3, B3, A1 und X2 unmittelbar" | **9** – **B10 fehlt in der Aufzählung**, es trägt seit 0.33.0 einen Marker |

**„25 von 29" ist besonders unangenehm:** Das Pack selbst schreibt einen Absatz darüber, dass
diese Zahl bis 0.32.0 falsch war und berichtigt wurde. **Die Berichtigung hat die zweite Stelle
nicht erreicht.**

> **Und die Zählung war wieder zu klein.** Der erste Durchgang fand zwei Angaben, der zweite
> vier, der dritte sieben. Das ist der Befund, den dieses Projekt am häufigsten an sich selbst
> macht – hier zum sechsten Mal in Folge.

### 1.8 Befund 7, methodisch: Der Gegenstand der Messung wählt seinen Weg selbst

In Lauf **V-M** griff der Unteragent von sich aus zu `PowerShell` – einem Werkzeug, das in
dieser Umgebung ohnehin nicht schreiben kann. Er meldete eine Verweigerung, und der Lauf sah
aus wie „die Sperre schließt auch den Shell-Weg".

**Lauf V-PK entlastet die Sperre:** dieselbe Verweigerung, wörtlich dieselbe Meldung, **ohne
jeden Skill**. Und Lauf V-E zeigt den `Bash`-Weg offen.

> Wer V-M allein ausgewertet hätte, hätte einen Positivbefund ins Protokoll geschrieben, den
> zwei Läufe desselben Tages widerlegen. **Die Sonde muss das Werkzeug vorschreiben** – sonst
> misst man die Wahl des Agenten mit, und die ist kein Mechanismus.

## 2. Was heute im Repositorium steht

| Stelle | Heutiger Stand | Warum das nicht bleiben kann |
|---|---|---|
| Zeile **S3** | drei Grenzen, keine Aussage zur Reichweite | Die naheliegende Frage – „gilt das auch eine Ebene tiefer?" – bleibt unbeantwortet, obwohl sie jetzt beantwortet ist |
| Zeile **A1** | `[TECHNISCH]`, Beleg `[DOK] docs/en/sub-agents` | Die Bauform, an der `AP2-CC-13` acht Releases hing und B01 gescheitert ist |
| Zeile **H2** | „Exit-Code 2 blockiert", ohne Reichweite | Dass das auch für einen Unteragenten gilt, war nie gesagt und nie gemessen |
| `manifest.json` beider Packs | kein Feld für das Startwerkzeug | Ein Kanal, den keine Liste kennt und keine Prüfung erzwingt |
| Prüfung 32, Kopfkommentar | „beider aufgezeichneter Schemata" | Überholt, siehe 1.6 |
| `05-working-model.md` | „Hintergrund-Subagenten DÜRFEN NICHT für M3 verwendet werden" | Technisch ist nur das Startwerkzeug **ganz** sperrbar. `run_in_background` ist ein Argument, und Argumentmuster wirken nach D-66 lautlos gar nicht |

## 3. Vorgeschlagene Änderung

1. **Zeile S3** bekommt einen Abschnitt **Reichweite**: Die Sperre gilt auch für einen
   Unteragenten, den der Skill startet – und Grenze 2 reicht mit.
2. **Zeile A1** bekommt den Messbeleg; der nicht gemessene Teilsatz bleibt ausdrücklich `[DOK]`.
3. **Zeile H2** bekommt die gemessene Reichweite, einschließlich des benannten Matchers.
4. **Neues Manifestfeld `agent_start_tools`**, Bauart wie `hook_tools_absent` (D-47): Ein Pack
   nennt die Werkzeugnamen oder erklärt in `agent_start_tools_absent`, warum es keine nennt.
5. **Prüfung 34 (neu):** Jedes Pack tut eines von beidem. Ein Pack, das **A1** zusagt, muss
   nennen statt erklären.
6. **Prüfung 32** bekommt einen fünften Gegenstand: den Unteragenten-Umschlag.
7. **`05-working-model.md`:** M1 nennt den gemessenen Stand; die Regel zu Hintergrund-Subagenten
   sagt, dass sie normativ ist und warum sie es bleiben muss.
8. **`EDGE_CASES.md`:** ein Grenzfall „Ein Skill startet einen Unteragenten".

## 4. Auswirkungen

- **Keine Einstufung ändert sich.** S3 und A1 bleiben `[TECHNISCH]`, H2 bleibt `[TECHNISCH]`.
  Die Summen der Zusammenfassung bleiben unverändert – Prüfung 31 rechnet sie ohnehin nach.
- **Zwei Belege wandern von `[DOK]` auf gemessen** (A1 ganz, H2 in der Reichweite).
- **Jedes künftige Client Pack** muss `agent_start_tools` füllen oder seine Abwesenheit
  erklären. Das ist der Preis von E2 und steht dort.
- **`devin-desktop` erklärt die Abwesenheit mit dem Grund „unerhoben"** – nicht mit „gibt es
  nicht". Das Pack führt Subagenten als Vorschaufunktion (`QD-14`); gemessen ist dort nichts.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | Wie wird die Reichweite in der Matrix untergebracht – als Abschnitt in **S3** oder als eigene Zeile **A2**? | **Als Reichweite in S3.** Es ist dieselbe Zusage, eine Ebene tiefer, und keine zweite | S3 ist schon die längste Zeile der Matrix und wird länger. Der Gegenvorschlag wäre lesbarer – und erzeugte **zwei Stellen für dieselbe Sache**, die auseinanderlaufen können. Genau der Befundtyp dieses Projekts, zuletzt bei `tool_names`/`hook_tools`. **Deshalb verworfen** |
| **E2** | Was folgt daraus, dass das Startwerkzeug in keiner Werkzeugliste steht? | **Neues Manifestfeld plus Prüfung 34.** Ein Pack nennt es oder erklärt seine Abwesenheit, Bauart wie `hook_tools_absent` (D-47) | Ein weiteres Feld, das jedes künftige Pack füllen muss. Die billigere Alternative – nur eine `_note` – ließe einen Kanal ohne durchgesetzte Deklaration, und das Verschweigen von Abwesenheit ist das, was D-47 abgestellt hat |
| **E3** | Wird Prüfung 32 um den dritten Umschlag erweitert? | **Ja.** Begründung ist **nicht** ein akuter Fund – beide Felder tragen keinen Pfad –, sondern dass die Prüfung eine Vollständigkeit benennt, die die Messung widerlegt hat | Die Prüfung wird länger für einen Fall, der heute nichts fängt. **Die Begründung gehört so ins Protokoll**, nicht als Risikobehauptung; sonst ist der Nachweis selbst eine Überzeichnung |
| **E4** | Bleibt die Regel „keine Hintergrund-Subagenten für M3" bestehen, obwohl sie technisch nicht abbildbar ist? | **Ja, und sie sagt es.** Sperrbar ist nur das Startwerkzeug **ganz**; „nur Hintergrund" ist ein Argument, und Argumentmuster wirken nach D-66 lautlos gar nicht | Eine Kernregel bekommt einen Satz, der sie schwächer aussehen lässt. **Sie war es schon** – neu ist nur, dass es dasteht |
| **E5** | Wird der Teilsatz in A1 („ein Profil ohne auflösbares Werkzeug startet nicht") mitgemessen oder bleibt er `[DOK]`? | **Bleibt `[DOK]`, ausdrücklich.** Er ist nicht gemessen | Die Zeile trägt zwei Belegarten und liest sich unruhiger. Das ist genauer als eine Zeile, die einen Messbeleg über eine nicht gemessene Aussage spannt |
| **E7** | Was geschieht mit den Zahlen in `clients/README.md`? | **Die `[TECHNISCH]`-Zahl wird von Prüfung 31 mitgerechnet; die VERIFY-Zahl entfällt dort und verweist auf das Pack.** Die erste hat eine eindeutige Grenze und gehört ausgerechnet; die zweite hat sie nur zur Hälfte – die unmittelbaren Marker sind zählbar, die „über den Verweis" mitgezählten sind Ermessen | Die Übersicht verliert eine Angabe und wird an einer Stelle unschärfer. **Der Preis ist richtig herum:** Eine gepflegte Zahl, die niemand nachrechnet, ist in diesem Projekt fünfmal gedriftet. Die Alternative – auch die VERIFY-Zahl erzwingen – müsste eine Ermessensgrenze als Arithmetik ausgeben |
| **E6** | Ein Release oder getrennt? | **Ein Release, `0.36.0`.** Matrix, Manifest, Prüfungen und Kern gehören zusammen | Getrennt entstünde ein Zwischenstand, in dem die Matrix eine Reichweite zusagt, die keine Prüfung deckt |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle sechs Fragen wie vorgelegt.** E1 Reichweite in S3, keine zweite Zeile; E2 neues Manifestfeld `agent_start_tools` plus Prüfung 34; E3 Prüfung 32 wird um den Unteragenten-Umschlag erweitert, mit der Begründung aus 1.6 und nicht mit einer Risikobehauptung; E4 die Regel zu Hintergrund-Subagenten bleibt und weist ihre Nichtabbildbarkeit aus; E5 der nicht gemessene Teilsatz in A1 bleibt `[DOK]`; E6 ein Release; E7 die `[TECHNISCH]`-Zahl in `clients/README.md` wird nachgerechnet, die VERIFY-Zahl entfällt dort |
| Datum | 2026-09-13 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | D-67 (die Skill-Sperre reicht in den Unteragenten, und Grenze 2 reicht mit), D-68 (A1 ist gemessen; die Beschränkung ist eine Entfernung, keine Verweigerung), D-69 (der Schutz-Hook erfasst und blockiert den Unteragenten, auch mit dem erzeugten Matcher), D-70 (das Startwerkzeug wird deklariert oder seine Abwesenheit erklärt), D-71 (eine Zahl mit eindeutiger Grenze wird überall ausgerechnet, nicht an zweiter Stelle gepflegt) |
| Auflagen | **Der nicht gemessene Teil bleibt in jeder der drei Zeilen als solcher kenntlich** – A1 (Startabbruch bei leerer Werkzeugliste), H2 (kein Lauf mit dem Schutz-Hook des Frameworks in einer vollständigen Installation), S3 (Hintergrund-Unteragenten und zwei Ebenen tief sind nicht gemessen). **Die Begründung für E3 wird nicht zur Risikobehauptung aufgewertet.** **`devin-desktop` erklärt die Abwesenheit mit „unerhoben", nicht mit „gibt es nicht"** – das Pack führt Subagenten als Vorschaufunktion. **Und der methodische Befund aus 1.7 gehört in die Sondenbeschreibung**, nicht nur ins Protokoll: Eine Sonde, die den Weg offenlässt, misst die Wahl des Agenten mit |
| Ziel-Release | `0.36.0` |
| Umsetzung | umgesetzt mit `0.36.0` |

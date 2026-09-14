# Erhebung: Was passiert, wenn eine Sitzung einen Framework-Skill aufruft?

| Feld | Wert |
|---|---|
| Gegenstand | Zeile **S2** der Fähigkeitsmatrix `claude-code`: „Gezielter Aufruf – Aufruf über den Skill-Namen mit vorangestelltem Schrägstrich", seit jeher `[TECHNISCH]` `[DOK]` und **ohne jede genannte Grenze** |
| Anlass | Externer Bericht `skill-priority-improvement.md` vom 2026-09-14 (Devin Desktop am Piloten): Der Agent habe bei einer passenden Aufgabe mit den Standardwerkzeugen gearbeitet statt mit den Skills `fw-code-explain` und `fw-repo-analyze` |
| Datum | 2026-09-14 |
| Framework-Version | 0.40.0 (`00b534b`) |
| Geprüfte Clientversion | **Claude Code 2.1.270** (Modell Opus 5) |
| Umgebung | Windows 11, Python 3.14.4; frisches synthetisches Testprojekt im Sitzungs-Scratchpad, **vollständige Installation mit allen Regeltexten**, Overlay auf `aktiv`, Berechtigungsschicht **an** (`defaultMode: default`), kein Bypass |
| Läufe | **elf**: vier wie ausgeliefert (A1 bis A4), drei mit freigegebenem Werkzeug (B1 bis B3), drei zur Argumentform (C1, D1, **E1 als Kontrolllauf**) und ein Entlastungslauf zur Reichweite der Regelträger (G1) |
| Belege | `devpacks/leitwerk-erhebungen-2026-09-14/` (außerhalb des Repositoriums, mit eigener README) |
| Ergebnis | **Die Erkennung war nie das Problem.** Die Sitzung ruft den passenden Skill auf – und die **Berechtigungsdatei des Frameworks weist den Aufruf ab**, weil ihr Vokabular für den Skillaufruf kein Verb kennt. Was danach geschieht, sieht aus wie ein gelungener Skill-Lauf |

> **Warum die Umgebung diesmal *mit* Regeltexten fährt.** Die Erhebungen vom 13.09. liefen
> ohne sie, weil dort ein Mechanismus des Clients gemessen wurde und ein Regeltext das
> Ergebnis verfälscht hätte. Hier ist der Gegenstand ein anderer: Gemessen wird, was eine
> **vollständige Leitwerk-Installation** tut. Die Regeltexte sind nicht Störgröße, sondern
> Messobjekt.

## 1. Methode

Vier Vorkehrungen, jede aus einem Befund dieses Projekts:

- **Kein Bypass, sondern eine `allow`-Liste.** Ein Bypass könnte die geprüfte Schranke gleich
  mit abschalten. Die Läufe A1 bis A4 fahren die ausgelieferte Berechtigungsdatei
  **unverändert**; die Läufe B bis E ergänzen genau eine Zeile in `settings.local.json` und
  nehmen sie nach dem Lauf zurück.
- **Die Aufgabe schreibt das Werkzeug nicht vor** – und das ist hier richtig, nicht falsch.
  Die D-72-Lehre („die Sonde muss das Werkzeug vorschreiben") gilt für Messungen an einer
  Schranke. Hier ist die **Werkzeugwahl des Agenten** der Messwert.
- **Zwei Aufgabenformen.** Eine Erklärungsaufgabe (Träger: `fw-code-explain`) und eine
  Planungsaufgabe (Träger: `fw-plan`, `fw-change-analyze`) – letztere ist der Zuschnitt, den
  der externe Bericht beschreibt.
- **Die Werkzeugspur aus dem Transkript, nicht aus dem Antworttext.** `permission_denials` im
  JSON-Ergebnis ist die zweite, vom Antworttext unabhängige Quelle; die dritte ist der
  Eintrag `toolDenialKind` im Sitzungstranskript.

**Aufgabe 1 (A1 bis A3, B1, B2, C1, D1, E1):** „Erklaere mir, was die Klasse
ZwischenablageDienst tut."
**Aufgabe 2 (A4, B3):** „Plane die Aenderungen an der Klasse ZwischenablageDienst, die
noetig waeren, damit sie auch ohne java.awt funktioniert."

Keine der beiden nennt einen Skill, ein Werkzeug oder einen Betriebsmodus.

## 2. Befund 1: Die Sitzung erkennt den Skill – in der Hälfte der Läufe

| Lauf | Aufgabe | `allow` | Skill-Aufruf | Ergebnis des Aufrufs |
|---|---|---|---|---|
| **A1** | 1 | wie ausgeliefert | `fw-code-explain` | **abgewiesen** |
| **A2** | 1 | wie ausgeliefert | **keiner** | – |
| **A3** | 1 | wie ausgeliefert | `fw-code-explain` | **abgewiesen** |
| **A4** | 2 | wie ausgeliefert | **keiner** | – |

**Zwei von vier.** Der externe Bericht sagt, die Agentenlogik prüfe nicht, ob ein Skill
vorliegt. Das trifft für A2 und A4 zu und für A1 und A3 nicht – und bei A1 und A3 wäre die
Prüfung ohnehin nicht der schwache Punkt gewesen.

**Die Aufgabenform entscheidet mit:** Die Erklärungsaufgabe zog den Skill in zwei von drei
Läufen, die Planungsaufgabe in keinem von einem. Das ist genau der Zuschnitt des externen
Berichts („Änderungen planen"), und er reproduziert sich.

### Der Satz, der den Textbefund trägt

Lauf **A2** rief keinen Skill auf und schrieb in seinen Ergebnisbericht:

> „**Verwendete Skills:** keine (Aufgabe entspricht inhaltlich `fw-code-explain`, Tiefe
> „Detail"; **kein Skill-Aufruf nötig**)"

Die Sitzung hat den passenden Skill **benannt** und seinen Aufruf für entbehrlich erklärt.
Unter dem Wortlaut von 0.40.0 ist das vertretbar: Abschnitt 17 der Wurzel-Anweisungsdatei sagt
„Nutze für Standardaufgaben die Skills", nennt keinen Zeitpunkt, trägt keine
Verbindlichkeitsmarke und verlangt für den Verzicht keine Begründung.

## 3. Befund 2: Der Aufruf wird abgewiesen – von der Berechtigungsdatei des Frameworks

In A1 und A3 steht im Transkript derselbe Eintrag:

```json
{"type": "tool_result", "content": "Execute skill: fw-code-explain",
 "is_error": true, "tool_use_id": "toolu_01EgMafB2QoyT9Y2n2rQPDpN"}
```
```json
"toolUseResult": "Error: Execute skill: fw-code-explain", "toolDenialKind": "user-rejected"
```

Und im JSON-Ergebnis desselben Laufs:

```json
"permission_denials": [{"tool_name": "Skill",
  "tool_input": {"skill": "fw-code-explain", "args": "…"}}]
```

**Die Ursache steht in der ausgelieferten Berechtigungsdatei.** Ihre `allow`-Liste führt sechs
Regeln – `Read(**)` und fünf lesende `git`-Befehle – und keine für das Werkzeug `Skill`. Der
Korb `ask` führt es ebenfalls nicht, der Korb `deny` auch nicht: **Das Werkzeug kommt in der
Datei überhaupt nicht vor** und fällt damit auf `defaultMode: default`, also auf die Rückfrage.
Im rückfragefreien Betrieb ist die Rückfrage eine Abweisung.

**Und das ist keine Lücke eines Packs, sondern eine des Vokabulars.** Die Kernquelle
`framework/runtime/permissions.json` kennt sechs Werkzeugverben – `read`, `search`, `write`,
`exec`, `fetch`, `mcp` –, und keines davon bezeichnet den Skillaufruf. `permission_tools`
**beider** Client Packs führt dieselben sechs. Eine Freigabe für den Skillaufruf ist in dieser
Datei nicht ausdrückbar; sie war es nie.

### Die Gegenprobe: mit Freigabe läuft der Aufruf durch

| Lauf | Aufgabe | `allow` | Skill-Aufruf | Ergebnis |
|---|---|---|---|---|
| **B1** | 1 | `Skill` | `fw-code-explain` | **läuft durch**, keine Abweisung |
| **B2** | 1 | `Skill` | `fw-code-explain` | **läuft durch**, keine Abweisung |
| **B3** | 2 | `Skill` | keiner | – |

`permission_denials` ist in allen drei Läufen leer. **Damit ist die Zuordnung eindeutig:** Was
den Aufruf aufhält, ist die fehlende Zeile, nicht das Modell.

B3 zeigt zugleich, dass die Freigabe die Wahl **nicht** ersetzt: Auch mit freigegebenem
Werkzeug rief die Planungsaufgabe keinen Skill auf. **Die beiden Befunde sind unabhängig, und
keiner behebt den anderen.**

## 4. Befund 3: Der Rückfall ist stumm – und er verliert die Zusage S3

Nach der Abweisung arbeitet die Sitzung weiter. Die Werkzeugspur von A3 zeigt, womit:

| # | Werkzeug | Eingabe |
|---|---|---|
| 1 | `Grep` | `ZwischenablageDienst` |
| 2 | `Bash` | `ls -R …` |
| 3 | `Skill` | `fw-code-explain` → **abgewiesen** |
| 4 | `Read` | `.claude/skills/fw-code-explain/SKILL.md` |
| 5 | **`Bash`** | `ls …` |
| 6 | `Read` | die Quelldatei |

**Schritt 4 ist der Rückfall:** Die Sitzung liest die `SKILL.md` als gewöhnliche Datei und
arbeitet ihren Ablauf von Hand nach. Die Ausgabe trägt danach die Überschrift und das
Standardformat des Skills; sie ist von einem gelungenen Lauf **nicht zu unterscheiden**.

**Schritt 5 ist der Preis, und er ist der eigentliche Befund.** `fw-code-explain` trägt
`disallowed-tools: Edit, Write, NotebookEdit, Bash`. In einem echten Skill-Lauf wäre dieser
`Bash`-Aufruf **nicht möglich gewesen** – die Sperre entfernt das Werkzeug aus dem Vorrat,
gemessen am 2026-09-13 (`2026-09-13-erhebung-disallowed-tools.md`, D-64). Die von Hand
nachgearbeitete Fassung trägt die Werkzeugbeschränkung nicht mit sich. **Der stumme Rückfall
verliert damit genau die Zusage, für die S3 seit 0.35.0 `[TECHNISCH]` steht.**

Die Sitzung selbst hat es gemerkt – hinterher, im eigenen Bericht:

> „… und der Skill verbietet Bash. Beide Aufrufe waren rein lesend und ohne Seiteneffekt; sie
> hätten durch Glob ersetzt werden müssen. Ab hier nur noch Read/Grep/Glob."

### Was im Ergebnisbericht ankommt

| Lauf | Zeile zu den Skills im Ergebnisbericht |
|---|---|
| **A1** | „`fw-code-explain` wurde aufgerufen, der Aufruf schlug fehl („Execute skill"). Die Analyse erfolgte manuell nach dem Standardarbeitsablauf." |
| **A3** | „**Verwendete Skills:** `fw-code-explain` (v0.1.3). Der Aufruf über den Skill-Mechanismus schlug fehl …; die Skill-Definition wurde stattdessen aus `.claude/skills/fw-code-explain/SKILL.md` gelesen und inhaltlich befolgt." |
| **A2** | „**Verwendete Skills:** keine (Aufgabe entspricht inhaltlich `fw-code-explain` …; kein Skill-Aufruf nötig)" |
| **A4** | „**Skills:** keine." |

**A3 ist der Fall, auf den es ankommt.** Wer die Zeile überfliegt, liest „Verwendete Skills:
`fw-code-explain` (v0.1.3)" – eine Verwendung, die nicht stattgefunden hat. Das Standardformat
des Ergebnisberichts (0.40.0) kennt für diesen Fall keine eigene Form; es fragt nach
„Verwendete Skills" und nicht danach, ob der Aufruf gelungen ist.

**Beide Sitzungen haben ehrlich berichtet.** Das ist Modellverhalten, keine Zusage – A4 nennt
denselben Sachverhalt in zwei Wörtern und ohne Grund.

## 5. Befund 4: Das Argumentmuster wirkt – wörtlich, nicht als Präfix

Die Frage entscheidet den Zuschnitt der Freigabe: Reicht eine Regel für alle
Framework-Skills, oder braucht es eine je Skill?

| Lauf | `allow` | aufgerufen | Ergebnis | Was er zeigt |
|---|---|---|---|---|
| **C1** | `Skill(fw-code-explain)` | `fw-code-explain` | **läuft durch** | Das Argumentmuster **wirkt** |
| **D1** | `Skill(fw-*)` | `fw-code-explain` | **abgewiesen** | Ein **Präfixmuster wirkt nicht** |
| **E1** | `Skill(fw-plan)` | `fw-code-explain` | **abgewiesen** | **Kontrolllauf:** das Muster engt wirklich ein |

**E1 ist der Lauf, ohne den C1 nichts bedeutet.** Ohne ihn wäre offen, ob das Argument
überhaupt verglichen wird oder ob jede Regel mit dem Werkzeugnamen `Skill` alles durchlässt.
E1 zeigt: Ein anderer Skillname wird abgewiesen. Der Vergleich ist wörtlich und er engt ein.

> **Die Bauform ist die von D-66, mit umgekehrtem Vorzeichen.** Dort wirkte ein
> Argumentmuster in `disallowed-tools` **lautlos gar nicht** – eine Sperre, die nichts sperrt.
> Hier wirkt es, aber nur wörtlich: Eine Freigabe `Skill(fw-*)` gäbe **lautlos nichts frei**.
> Wer sie schriebe, hätte eine Regel, die richtig aussieht und nichts tut.

**Folge für die Umsetzung:** zwölf wörtliche Regeln, eine je ausgeliefertem Skill. Ein Muster
wäre kürzer und wirkungslos.

## 6. Entlastungslauf G1: Welche Regelträger erreichen die Sitzung?

Die Frage entscheidet, wo eine Regel über die Skillwahl stehen kann. Je ein Merkwort wurde in
die Wurzel-Anweisungsdatei, in die always-on-Regeldatei und in die Laufzeitfassung des Overlays
eingetragen; gefragt wurde nach allen Merkwörtern.

**Der erste Lauf ist verworfen:** Die Sitzung griff zu `Grep` und fand die Wörter im
Dateisystem. Damit war nichts belegt – dieselbe Falle wie bei D-72, nur an einem anderen
Gegenstand.

**Der gültige Lauf fuhr mit `--disallowedTools` auf alle Werkzeuge.** Eine Antwort kann dann
nur aus dem geladenen Kontext kommen.

| Träger | Merkwort | Genannt? |
|---|---|---|
| `CLAUDE.md` (Wurzel-Anweisungsdatei) | `OTTER-8822` | **ja** |
| `.claude/rules/00-framework-core.md` (always-on) | `TALPA-4711` | **ja** |
| `.claude/rules/20-project-overlay.md` (Overlay-Laufzeitfassung) | `LUCHS-6013` | **ja** |

**Werkzeugaufrufe: keine.** Alle drei Träger stehen zu Sitzungsbeginn im Kontext; die Zeilen
R1 und R2 der Fähigkeitsmatrix bestätigen sich. Die Sitzung nannte `.claude/rules/00-framework-core.md`
von sich aus als Quelle ihrer Ergebnisberichtspflicht.

## 7. Was diese Erhebung nicht leistet

- **Sie misst einen Client.** Ob der Skillaufruf bei `devin-desktop` ebenfalls ein eigener,
  rückfragepflichtiger Werkzeugaufruf ist, ist **unerhoben**. Das Manifest sagt das jetzt
  ausdrücklich, statt es offen zu lassen.
- **Elf Läufe sind keine Quote.** „Zwei von vier" ist eine Beobachtung an vier Läufen, keine
  Wahrscheinlichkeit. Was die Läufe tragen, ist die **Existenz** beider Fälle – und für den
  Mechanikbefund genügt ein einziger Lauf mit Gegenprobe.
- **Die Skill-Auflistung führte 83 Einträge, davon 80 fremde.** Nur **drei** trugen das
  Präfix `fw-` – die drei modellaufrufbaren; die übrigen neun hält `disable-model-invocation`
  aus dem Kontext (Zusage **S4**, gemessen mit 0.15.0). Das ist der Normalfall einer echten
  Installation und zugleich der Grund, warum die Freigabe **nicht** auf den blanken
  Werkzeugnamen lauten darf. **Gezählt, nicht geschätzt:** Die erste Fassung dieses Protokolls
  sprach von „rund sechzig“.
- **Ob die geänderten Texte die Wahl verbessern, ist nicht gemessen.** Das wäre ein
  Sitzungstest mit einer Stichprobe, die vier Läufe nicht hergeben. Was gemessen ist, ist der
  **Mechanismus**: mit Freigabe läuft der Aufruf, ohne sie nicht.

## 8. Gegenzeichnung

| Feld | Inhalt |
|---|---|
| Durchführung | KI-Client unter Aufsicht, Sitzung vom 2026-09-14 |
| Gegengezeichnet durch | `<APPROVAL_ROLE>` |
| Datum | `<TBD: Datum der Gegenzeichnung>` |
| Anmerkungen | `<TBD: Anmerkungen der gegenzeichnenden Rolle>` |

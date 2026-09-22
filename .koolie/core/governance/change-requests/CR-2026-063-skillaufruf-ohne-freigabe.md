# Änderungsantrag `CR-2026-063`

| Feld | Inhalt |
|---|---|
| Titel | Der Skillaufruf ist ein Werkzeugaufruf – und die Berechtigungsdatei des Frameworks kennt ihn nicht |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-14 |
| Betroffene Artefakte | `framework/runtime/permissions.json` (Verb `skill`, zwölf `allow`-Regeln), `clients/claude-code/manifest.json` (`permission_tools.skill`, `permission_name_tools`), `clients/devin-desktop/manifest.json` (`permission_tools.skill` leer samt Begründung), `clients/claude-code/CLIENT_PACK.md` (Zeile S2), `clientmap.py` (`_regel_rendern`), `framework/runtime/root-instruction.md` (Abschnitt 17), `framework/runtime/rules/00-framework-core.md`, `framework/core/05-working-model.md` (Abschnitte 1 und 3.6), `framework/core/06-prompting-rules.md` (Regel 7), `checklists/01-preflight.md`, `tests/EDGE_CASES.md` (G-20), `tests/scripts/validate-framework.py` (Prüfung 39, Pfadregelprüfung), `tests/scripts/probe-pruefungen.py`, `governance/DECISION_LOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – die Berechtigungsdatei ist Ebene 3, und die Zusage S2 ist Framework-Gut |
| Art | Änderung; Anlass ist ein **externer** Befund, kein Kandidat der Übergabe |
| Dringlichkeit | **P1.** Ausgeliefert ist eine Aufforderung, die die Datei daneben nicht zulässt. Der Fehlschlag ist **stumm** und kostet die Zusage S3 – gemessen |

## 1. Anlass

Ein Bericht aus einer Sitzung am Piloten (`skill-priority-improvement.md`, 2026-09-14, Devin
Desktop) hält fest, der Agent habe bei einer passenden Aufgabe mit `read` und
`find_file_by_name` gearbeitet statt mit `fw-code-explain` und `fw-repo-analyze`, und erst nach
Rückfrage die Skills verwendet. Er schließt daraus auf eine fehlende **Skill-Erkennung** und
empfiehlt, die Agentenlogik so zu ändern, dass sie Skills automatisch aufruft.

**Der Befund ist gegengeprüft** (`tests/protocols/2026-09-14-gegenpruefung-skillwahl.md`) und
**gemessen** (`tests/protocols/2026-09-14-erhebung-skillaufruf.md`, elf Läufe, davon vier
Kontroll- und Entlastungsläufe). **Er bestätigt sich – und seine Ursache ist eine andere, als
er sagt.**

### 1.1 Befund 1: Der Aufruf scheitert an der eigenen Berechtigungsdatei

Der Skillaufruf ist bei `claude-code` ein **eigener Werkzeugaufruf** mit dem Namen `Skill`. Die
ausgelieferte Berechtigungsdatei führt ihn in **keinem** Korb und lässt ihn damit auf
`defaultMode: default` fallen – also auf die Rückfrage. Gemessen, mit Gegenprobe:

| Lauf | `allow` | Skill-Aufruf | Ergebnis |
|---|---|---|---|
| A1, A3 | wie ausgeliefert | `fw-code-explain` | **abgewiesen** (`toolDenialKind: user-rejected`) |
| B1, B2 | `Skill` ergänzt | `fw-code-explain` | läuft durch, `permission_denials` leer |

**Die Ursache liegt eine Ebene tiefer als das Pack.** `framework/runtime/permissions.json`
kennt sechs Werkzeugverben – `read`, `search`, `write`, `exec`, `fetch`, `mcp` – und keines
bezeichnet den Skillaufruf. `permission_tools` **beider** Packs führt dieselben sechs. **Eine
Freigabe für den Skillaufruf war in dieser Datei nie ausdrückbar.**

Und das Projekt wusste es dreimal, ohne es aufzuschreiben: `2026-09-12-B01-allowed-tools.md`
nennt den Skillaufruf ausdrücklich „als eigenen Werkzeugaufruf mit dem Namen `Skill` und damit
einzeln kontrollierbar"; zwei Läufe des 13.09. sind verworfen worden, weil „der `Skill`-Aufruf
scheiterte". **Aus dem dreimaligen Eigenverschulden ist nie ein Befund über die ausgelieferte
Datei geworden.**

### 1.2 Befund 2: Der Rückfall ist stumm und kostet die Zusage S3

Nach der Abweisung liest die Sitzung die `SKILL.md` als gewöhnliche Datei und arbeitet ihren
Ablauf von Hand nach. **Die Ausgabe ist von einem gelungenen Lauf nicht zu unterscheiden** –
sie trägt Überschrift und Standardformat des Skills.

**Der Preis ist gemessen.** `fw-code-explain` trägt `disallowed-tools: Edit, Write,
NotebookEdit, Bash`. In Lauf A3 rief die nachgearbeitete Fassung `Bash` auf. In einem echten
Skill-Lauf wäre das nicht möglich gewesen: Die Sperre entfernt das Werkzeug aus dem Vorrat
(D-64). **Der stumme Rückfall verliert genau die Zusage, für die S3 seit 0.35.0 `[TECHNISCH]`
steht.**

Und er kommt so im Ergebnisbericht an (Lauf A3, wörtlich):

> „**Verwendete Skills:** `fw-code-explain` (v0.1.3). Der Aufruf über den Skill-Mechanismus
> schlug fehl …; die Skill-Definition wurde stattdessen aus `.claude/skills/…/SKILL.md`
> gelesen und inhaltlich befolgt."

Wer die Zeile überfliegt, liest eine Verwendung, die nicht stattgefunden hat. Das
Standardformat des Ergebnisberichts kennt für diesen Fall keine eigene Form.

### 1.3 Befund 3: Die Skillwahl steht an fünf Stellen und erreicht den Agenten nirgends verbindlich

| Träger | Verbindlichkeit | Adressat |
|---|---|---|
| `06-prompting-rules.md:34` Regel 7 – die stärkste Formulierung | normativ | Modul über **Aufgabenanweisungen** → Mensch; Passiv lässt offen, wer handelt |
| `01-preflight.md:39` | **SOLL** | „Bearbeiterin oder Bearbeiter", „vor dem ersten Prompt" |
| `05-working-model.md` Abschnitt 1, Spalte **Referenz**, sechs von vierzehn Schritten | – | keine Pflichtspalte |
| `root-instruction.md` Abschnitt 17 | **ohne Marke** – die Datei führt null MUSS/SOLL/KANN | Agent, als letzter von 17 Abschnitten |
| `rules/00-framework-core.md` (always-on) | – | Agent – **die Wahl kommt dort nicht vor** |

Der Auslöser „Standardaufgaben" ist nirgends definiert und kommt im Kern kein zweites Mal vor.

**Gemessen, was daraus folgt** (Lauf A2, wörtlich): „**Verwendete Skills:** keine (Aufgabe
entspricht inhaltlich `fw-code-explain` …; **kein Skill-Aufruf nötig**)." Die Sitzung hat den
passenden Skill benannt und seinen Aufruf für entbehrlich erklärt – unter dem Wortlaut von
0.40.0 vertretbar.

### 1.4 Befund 4: Das Argumentmuster wirkt wörtlich, nicht als Präfix

| Lauf | `allow` | aufgerufen | Ergebnis |
|---|---|---|---|
| **C1** | `Skill(fw-code-explain)` | `fw-code-explain` | **läuft durch** |
| **D1** | `Skill(fw-*)` | `fw-code-explain` | **abgewiesen** |
| **E1** | `Skill(fw-plan)` | `fw-code-explain` | **abgewiesen** (Kontrolllauf) |

**Die Bauform ist die von D-66, mit umgekehrtem Vorzeichen.** Dort wirkte ein Argumentmuster in
`disallowed-tools` lautlos gar nicht – eine Sperre, die nichts sperrt. Hier gäbe ein
Präfixmuster **lautlos nichts frei**. Eine Regel `Skill(fw-*)` sähe richtig aus und täte
nichts.

### 1.5 Befund 5 – die Entlastung: Die empfohlene Behebung lässt sich nicht bauen

Option 1 des Berichts – „Vor jeder Aufgabenbearbeitung automatisch prüfen … bei Übereinstimmung
Skills automatisch aufrufen", umzusetzen in der „Agent-Logik" – liegt **außerhalb der
Reichweite dieses Frameworks**. Leitwerk liefert Regeltexte, Skills, eine Berechtigungsdatei
und einen Hook; es ändert keine Agentenlogik. Ein Antrag dieser Art ist hier kein Antrag,
sondern eine Anforderung an den Hersteller – dieselbe Lage wie bei den vier Einträgen von
Paket 6.

**Und die Systemanweisung, die der Bericht als Beleg zitiert, ist keine Framework-Regel.** Nach
Abschnitt 2 der Wurzel-Anweisungsdatei hat eine Ablage außerhalb des Repositoriums **keine
Ebene dieser Hierarchie**.

### 1.6 Befund 6 – nicht gesucht: Zeile S2 nennt keine einzige Grenze

Die Fähigkeitsmatrix führt in **S2** „Gezielter Aufruf", `[TECHNISCH]`, `[DOK]` – und nennt
weder die Rückfragepflicht noch die Argumentform noch den stummen Rückfall. Die Nachbarzeile S3
trägt seit 0.35.0 **drei** benannte Grenzen; S2 ist seit dem ersten Release unverändert.

## 2. Warum zwölf wörtliche Regeln und nicht eine

Eine Vorabfreigabe ist nach B01 keine Zusage – **aber sie auszuweiten ist trotzdem eine
Ausweitung.** Das Argument aus `CR-2026-062` Abschnitt 2 gilt hier unverändert: Was sie ändert,
ist nicht der Mechanismus, sondern die **Rückfrage, die entfällt**.

**Und hier ist die Ausweitung messbar größer als sie aussieht.** Die Skill-Auflistung der
Messläufe führte **83** Einträge – davon **drei** mit dem Präfix `fw-` und **80 fremde** aus
einer nutzerglobalen Ablage. (Dass nur drei der zwölf Framework-Skills dort erscheinen, ist
kein Widerspruch, sondern die Zusage **S4**: `disable-model-invocation` hält die übrigen neun
aus dem Kontext – aufrufbar bleiben sie.) Eine Regel auf den blanken Werkzeugnamen `Skill`
gäbe **auch die 80** frei, und sie sind nach Regel 2.6 der Prioritätshierarchie **ebenenlos**.

Der Zuschnitt ist damit vorgezeichnet: freigegeben wird, was das Framework selbst ausliefert,
und nichts sonst. Dass das zwölf Zeilen statt einer kostet, ist **kein Entwurf, sondern ein
Messergebnis** (Befund 4).

## 3. Vorgeschlagene Änderung

**Mechanik**

1. **Ein Verb `skill` im Berechtigungsvokabular.** `permissions.json` bekommt zwölf
   `allow`-Regeln, eine je ausgeliefertem Skill; der Kopfkommentar nennt das Verb und die
   wörtliche Vergleichsform samt Fundstelle.
2. **`permission_tools.skill` je Pack.** `claude-code`: `["Skill"]`. `devin-desktop`: `[]` mit
   `_permission_tools_skill_note` – **unerhoben, nicht abwesend**, Bauform wie
   `hook_tools_absent` nach D-47. Die leere Liste lässt die zwölf Regeln für dieses Pack
   ersatzlos entfallen; das ist die strengere Seite.
3. **`permission_name_tools` bei `claude-code`.** Werkzeuge, deren Regelargument ein **Name**
   und kein Pfad ist. Für sie hängt die Abbildung weder das Wurzelpräfix noch das
   Präfixzeichen an, und der Validator lässt sie neben `permission_path_tools` zu.
4. **`clientmap._regel_rendern`** bekommt einen eigenen Zweig für `skill` – wie `exec` schon
   einen hat.

**Text**

5. **Abschnitt 17 der Wurzel-Anweisungsdatei** bekommt Auslöser, Zeitpunkt und Nachweis: Prüfung
   vor jedem Schritt; wo der Standardarbeitsablauf einen Skill nennt, ist er der vorgesehene
   Weg; ein anderer Weg wird im Ergebnisbericht benannt und begründet. Dazu der Satz zum
   abgewiesenen Aufruf.
6. **Die always-on-Kurzfassung** bekommt dieselbe Regel in einem Absatz – sie ist der einzige
   Träger, der die Sitzung sicher erreicht **und** den Standardarbeitsablauf führt (belegt
   durch Entlastungslauf G1).
7. **`05-working-model.md`** macht die Spalte „Referenz" verbindlich und erweitert das
   Standardformat des Ergebnisberichts um den Negativ- und den Abweisungsfall.
8. **Regel 7** löst ihr Passiv auf; der **Preflight-Punkt** bleibt beim Menschen und verweist
   auf die eigene Pflicht des Agenten.
9. **Zeile S2** des Packs bekommt ihre drei gemessenen Grenzen.

**Prüfung**

10. **Prüfung 39** mit drei Gegenständen: der verlorene Anker; **jeder ausgelieferte Skill hat
    genau eine `allow`-Regel und jede Regel einen Skill**; die Regel trägt keine
    Musterzeichen. Dazu die vier Regelträger: Jeder nennt die Skillwahl.
11. **Grenzfall G-20** – ein abgewiesener Skill-Aufruf.

## 4. Auswirkungen

| Bereich | Auswirkung |
|---|---|
| Erzeugte Berechtigungsdatei `claude-code` | **6 → 18 `allow`-Regeln.** Die zwölf neuen betreffen ausschließlich den Skillaufruf |
| Erzeugte Berechtigungsdatei `devin-desktop` | **unverändert**, 6 Regeln – das Verb ist dort unerhoben |
| Bestehende Installationen | **Prüfung 37 meldet zwölf fehlende `allow`-Regeln**, bis die Datei nachgezogen ist. Die Datei steht in `shared_seed` und wird nach der Erstinstallation nie wieder geschrieben (D-76) – das Nachtragen ist ein Handgriff des Overlay Owners und gehört in die Migrationshinweise |
| Sicherheit | **Zwölf Rückfragen entfallen, alle für Skills des Frameworks.** Was ein Skill dann tut, bleibt unverändert gesperrt: `disallowed-tools` wirkt (D-64), der Hook wirkt (D-69), `ask` auf Schreiben wirkt. Fremde Skills bleiben rückfragepflichtig |
| Agentenverhalten | **Nicht zugesagt.** Ob der verschärfte Text die Wahl verbessert, ist ein Sitzungstest und nicht gefahren |

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | Bekommt das Berechtigungsvokabular überhaupt ein Verb für den Skillaufruf – oder bleibt es bei der Rückfrage, sauber deklariert? | **Ein Verb.** Das Framework fordert in Abschnitt 17 die Nutzung der Skills und macht sie in der Datei daneben rückfragepflichtig. Eine Regel, deren Befolgung das Framework selbst verteuert, ist keine Regel, sondern eine Reibung. **Und im rückfragefreien Betrieb ist die Rückfrage eine Abweisung** – gemessen | **Eine Ausweitung bleibt eine Ausweitung**, auch wenn sie nur eine Rückfrage erspart. **Die Gegenposition ist vertretbar:** Nach D-05 ist die Rückfrage der Normalfall, und wer sie für den Skillaufruf beseitigt, nimmt dem Menschen einen Kontrollpunkt, den er heute hat |
| **E2** | Ein Muster für alle Framework-Skills – oder zwölf wörtliche Regeln? | **Zwölf wörtliche.** Das ist **kein Entwurf, sondern gemessen**: `Skill(fw-*)` weist den Aufruf ab (D1), `Skill(fw-code-explain)` lässt ihn durch (C1), `Skill(fw-plan)` weist einen anderen Skill ab (E1, Kontrolllauf). Ein Muster gäbe lautlos nichts frei | **Zwölf Zeilen statt einer**, und ein dreizehnter Skill braucht seine eigene. **Genau das hält Prüfung 39 fest** – der Preis ist Pflege, und sie ist bewacht |
| **E3** | Werden die Regeln aus dem Skillverzeichnis **erzeugt** oder in die Datei **geschrieben**? | **Geschrieben.** Nach D-53 **ist** der Inhalt dieser Datei die Berechtigung; was sie gewährt, soll in ihr lesbar sein und nicht aus einem Verzeichnis berechnet werden. Ein erzeugender Weg hieße: Ein neuer Skill erteilt sich seine Vorabfreigabe selbst | **Zwei Quellen für dieselbe Menge**, und sie können auseinanderlaufen – genau der Befundtyp von `CR-2026-062`. **Deshalb hängt E3 an Prüfung 39**; ohne sie wäre der Vorschlag nicht vertretbar |
| **E4** | Was gilt für `devin-desktop`? | **Leere Liste mit Begründung** – unerhoben, nicht abwesend. Bauform wie `hook_tools_absent` (D-47) und `tool_names_unmapped` (D-78). Die Regeln entfallen dort ersatzlos, und das ist die strengere Seite | **Ein Pack bleibt unerhoben**, und zwar ausgerechnet das, an dem der Bericht entstanden ist. Die Alternative wäre, seine Seite zu raten – **die Bauform, die dieses Projekt sich abgewöhnt**. Neuer Klärungspunkt **K-33** |
| **E5** | Wo steht die Skillwahl künftig – nur in der Wurzel-Anweisungsdatei oder auch in der always-on-Schicht? | **In beiden.** Die always-on-Datei führt die vierzehn Schritte und den Satz „Schritte werden nicht übersprungen"; die Skillwahl gehört dorthin, wo der Schritt steht. **Entlastungslauf G1 belegt, dass die Datei die Sitzung ohne Werkzeugaufruf erreicht** | **Dieselbe Regel an zwei Stellen** – und Regeldopplung ist der Befundtyp von B11 und D-78. **Deshalb ist sie bewacht:** Prüfung 39 verlangt die Nennung an allen vier Trägern; sie prüft die **Anwesenheit**, nicht den Wortlaut |
| **E6** | Wird die Nichtverwendung begründungspflichtig – oder genügt es, sie zu nennen? | **Begründungspflichtig.** „Skills: keine" (Lauf A4) ist formal vollständig und sagt nichts. Was die Lücke sichtbar macht, ist der Satz *welcher Skill kam in Frage und warum nicht* | **Der Ergebnisbericht wächst**, und die Pflicht ist nicht durchsetzbar – kein Mechanismus prüft einen Bericht. **Sie ist eine Anweisung, und sie steht als solche da**; was sie trägt, ist die Prüfpflicht des Menschen |
| **E7** | Darf der Rückfall auf die `SKILL.md` weiterhin stattfinden? | **Ja – aber er heißt nicht mehr Verwendung.** Ein Verbot kostete Ergebnisqualität ohne Gegenwert: Die nachgearbeitete Fassung war in beiden Läufen brauchbar. Was schadet, ist nicht der Rückfall, sondern seine **Stille** | **Die Werkzeugbeschränkung des Skills fehlt dabei weiterhin** – gemessen, ein `Bash`-Aufruf in A3. Die Regel verlangt, sie trotzdem einzuhalten, und **das ist eine Anweisung ohne Mechanismus**. Ehrlicher als ein Verbot, das niemand durchsetzt, aber keine Zusage |
| **E8** | Ein eigenes Release oder Anhang an das nächste? | **Ein eigenes Release, `0.41.0`.** Der Gegenstand ist geschlossen, und er ist der erste, der aus einem **externen** Befund kommt | **Das sechzehnte Release in drei Tagen.** Und diesmal ist ein Ergebnis **doch** eine Messung am Client – die erste, die eine vollständige Installation misst statt eines Mechanismus |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle acht Fragen wie vorgelegt.** E1 ein Verb `skill`; E2 zwölf wörtliche Regeln, weil das Präfixmuster gemessen nicht wirkt; E3 in die Datei geschrieben und von Prüfung 39 bewacht; E4 `devin-desktop` deklariert die Enthaltung, K-33 neu; E5 beide Träger, Anwesenheit bewacht statt Wortlaut; E6 die Nichtverwendung ist begründungspflichtig; E7 der Rückfall bleibt erlaubt und heißt nicht Verwendung; E8 eigenes Release `0.41.0` |
| Datum | 2026-09-14 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | D-81 (das Berechtigungsvokabular kennt den Skillaufruf; freigegeben ist nur, was das Framework ausliefert), D-82 (das Argument wird wörtlich verglichen – ein Muster gäbe lautlos nichts frei), D-83 (ein abgewiesener Skill-Aufruf ist keine Verwendung), D-84 (wo der Standardarbeitsablauf einen Skill nennt, ist er der vorgesehene Weg des Schrittes) |
| Auflagen | **Der Migrationshinweis gehört in den Änderungsverlauf**, nicht nur in diesen Antrag: Bestehende Installationen melden zwölf fehlende `allow`-Regeln, bis die Datei nachgezogen ist. **Der Wirkungsnachweis führt einen Lauf am Client** – dieselbe Aufgabe gegen eine Installation des neuen Standes, mit dem Nachweis, dass der Aufruf durchläuft. **Und die Grenze wird benannt:** Dass der verschärfte Text die Wahl verbessert, ist **nicht** gemessen und wird nicht behauptet |
| Ziel-Release | `0.41.0` |
| Umsetzung | umgesetzt mit `0.41.0` |

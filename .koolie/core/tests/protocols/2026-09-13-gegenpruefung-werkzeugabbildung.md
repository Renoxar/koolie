# Gegenprüfung: zwei Listen für dieselbe Sache – es sind vier, und eine davon ist unbewacht

| Feld | Wert |
|---|---|
| Gegenstand | **Kandidat 1 der Übergabe:** „`skill_frontmatter.tool_names` und `hook_tools` vereinheitlichen – zwei Listen für dieselbe Sache, auseinandergelaufen: `tool_names.edit` führt kein `NotebookEdit`." Seit 0.35.0 vertagt, mit Grund: Die Vereinheitlichung ändere `allowed-tools` still mit |
| Anlass | Der Kandidat steht seit fünf Releases und ist nach der Übergabe „der größte offene Posten, der ohne Messinstrument auskommt". Nach D-23 gehört ein Befund vor der Umsetzung gegengeprüft, auch wenn er aus dem eigenen Haus stammt |
| Datum | 2026-09-13 |
| Framework-Version | 0.39.0 (Auscheckstand `7701db2`, Arbeitsbaum sauber, Validator 0/0) |
| Prüfmethode | **Zwanzig Messungen an den Abbildungsfunktionen und an echten Installationen, keine Codelektüre allein.** M1 bis M5 rufen die Abbildung je Verb und je Pack auf; M6 bis M12 greifen in eine Kopie des Repositoriums ein und lassen den ausgelieferten Validator laufen; M13 bis M20 präparieren das Manifest und installieren wirklich. **Sieben der zwanzig sind Kontrollläufe** – dieselbe Lücke in den *anderen* Abbildungen desselben Manifests. Ohne sie wäre „läuft durch" kein Messwert, sondern womöglich ein nicht gestarteter Lauf |
| Umgebung | Windows 11, Python 3.14.4, NTFS; Kopien und Testinstallationen im Scratchpad |
| Ergebnis | **Der Befund bestätigt sich – und er ist ein anderer, als der Kandidat sagt.** Es sind **vier** Werkzeugabbildungen, nicht zwei. Der inhaltliche Unterschied, den der Kandidat nennt, ist **richtungsrichtig und harmlos**; die vorgeschlagene Behebung wäre eine **Ausweitung**. Der eigentliche Befund liegt daneben: **Drei der vier Abbildungen brechen ab, wenn ihnen ein Verb fehlt. Die vierte reicht es wörtlich durch – und sie kommt zweimal vor** |

## 0. Der Zusammenhang in einem Satz

**Ein Frontmatter des Kerns schreibt fünf Verben, und drei verschiedene Stellen bilden sie
ab – jede mit ihrem eigenen Vokabular, und genau die, die eine echte Sperre trägt, kennt
zwei der fünf Verben nicht.**

## 1. Wie viele Listen es wirklich sind

| Stelle | Vokabular | Wofür | Bewacht? |
|---|---|---|---|
| `skill_frontmatter.tool_names` | `read, grep, glob, edit, exec` | `allowed-tools` des Skills – eine **Vorabfreigabe** (B01) | **nein** |
| `agent_frontmatter.tool_names` | dieselben fünf, zeichengleicher Block | `tools` des Agentenprofils – eine **Entfernung aus dem Vorrat** (A1, D-68) | **nein** |
| `hook_tools` | `read, search, exec, write` | Hook-Matcher **und** `disallowed-tools` je Skill – eine echte **Sperre** (S3, D-64) | ja |
| `permission_tools` | `read, search, write, exec, fetch, mcp` | Berechtigungsdatei – die Kernzusagen B1 bis B6 | ja |
| *daneben:* `agent_start_tools` | – | Startwerkzeug für Unteragenten (D-70) | ja (Prüfungen 34, 35) |

**Die Übergabe zählt zwei. Es sind vier, und die Zählung war damit wieder zu klein** – zum
sechsten Mal an diesem Tag.

Dazu ein drittes Vokabular, das keine Liste ist: `DENY_VERB_EIMER` in `install.py` – die
Brücke, über die `permissions.deny` der Quelle auf `hook_tools` abgebildet wird. Sie führt
`edit`, `write`, `exec`, `read` und `search`: **drei Verben der Quelle und zwei der
Durchsetzungsschicht**, und sie kennt `grep` und `glob` nicht.

## 2. Was die vierzehn ausgelieferten Quellen wirklich schreiben (M5)

Dreizehn `SKILL.md` und ein Agentenprofil:

| Feld | Verb | Fundstellen |
|---|---|---|
| `allowed-tools` | `read` | **14** |
| | `grep` | **14** |
| | `glob` | **14** |
| | `edit` | 4 |
| | `exec` | 5 |
| `permissions.deny` | `edit` | 9 |
| | `exec` | 8 |
| | befehlsgenau (`Exec(git push)` …) | 26 |

**`grep` und `glob` sind die meistgenannten Verben des Vokabulars – und genau die beiden,
die die Sperrabbildung nicht kennt.**

## 3. Befund 1: Dasselbe Wort, zwei Felder, zwei Verhalten (M1)

Je Verb ein Skill mit `allowed-tools: [<verb>]` **und** `permissions.deny: [<verb>]`,
durch `render_skill_frontmatter` des Vorstands, Pack `claude-code`:

| Verb | `allowed-tools` wird zu | `disallowed-tools` wird zu |
|---|---|---|
| `read` | `Read` | `Read` |
| **`grep`** | `Grep` | **nichts** |
| **`glob`** | `Glob` | **nichts** |
| **`search`** | **`search`** | `Grep, Glob` |
| `edit` | `Edit, Write` | `Edit, Write, NotebookEdit` |
| **`write`** | **`write`** | `Edit, Write, NotebookEdit` |
| `exec` | `Bash` | `Bash` |
| **`fetch`** | **`fetch`** | **nichts** |
| **`mcp`** | **`mcp`** | **nichts** |
| **`banane`** | **`banane`** | **nichts** |

**Zwei von zehn Verben verhalten sich in beiden Feldern gleich.** Die Lage ist genau
invertiert: `grep` wirkt in der Vorabfreigabe und nicht in der Sperre, `search` in der
Sperre und nicht in der Vorabfreigabe. Und ein Schreibfehler – `banane` – wird in der
Vorabfreigabe **zum Werkzeugnamen** und in der Sperre **zu nichts**.

Für das Agentenprofil (M2) gilt dasselbe: Aus `allowed-tools: [banane]` wird
`tools: banane`.

## 4. Befund 2: Drei Abbildungen brechen ab, eine reicht durch (M3, M13 bis M20)

### 4.1 Am Funktionsaufruf (M3)

Dieselbe Frage – „was heißt dieses Verb bei diesem Client?" – an alle drei Abbildungen:

| Verb | `skill_frontmatter.tool_names` | `hook_tools` | `permission_tools` |
|---|---|---|---|
| `grep` | `Grep` | **AbbildungsFehler** | **AbbildungsFehler** |
| `edit` | `Edit, Write` | **AbbildungsFehler** | **AbbildungsFehler** |
| `banane` | **`banane`** | **AbbildungsFehler** | **AbbildungsFehler** |

### 4.2 An einer echten Installation (M13 bis M20)

Je Zeile: Manifest präparieren, `install.py --client claude-code --root <leer>`, das
erzeugte Frontmatter ablesen, Manifest zurücksetzen und gegen den Ausgangstext prüfen.

| Nr. | Eingriff | Ergebnis |
|---|---|---|
| M13 | *Ausgangslage* | `fw-plan: allowed-tools: Read, Grep, Glob` / `fw-reviewer: tools: Read, Grep, Glob` |
| **M14** | `skill_frontmatter.tool_names` verliert `grep` | **durchgelaufen** → `allowed-tools: Read, grep, Glob` |
| **M15** | `agent_frontmatter.tool_names` verliert `read` | **durchgelaufen** → `tools: read, Grep, Glob` |
| **M16** | **beide `tool_names`-Blöcke ganz geleert** | **durchgelaufen** → `tools: read, grep, glob` |
| M17 | *Kontrolle:* `hook_tools` verliert `search` | **ABBRUCH:** „hook_tools kennt das Werkzeugverb 'search' nicht" |
| M18 | *Kontrolle:* `hook_tools.search` auf die leere Liste | **ABBRUCH:** „kein Hook-Werkzeug für 'search' …" |
| M19 | *Kontrolle:* `permission_tools` verliert `exec` | **ABBRUCH:** „permission_tools kennt das Werkzeugverb 'exec' nicht" |
| M20 | *Kontrolle nach Rücknahme* | wie M13 |

**M16 ist die Messung, auf die es ankommt.** Eine Installation, deren Abbildung gar nichts
mehr kann, läuft durch und liefert das Reviewprofil `fw-reviewer` mit
`tools: read, grep, glob` aus – **drei Namen, die dieser Client nicht führt.** Zeile A1
des Packs nennt genau diesen Fall als nicht gemessen: *„dass ein Profil, dessen
`tools`-Liste sich zu keinem Werkzeug auflöst, gar nicht erst gestartet wird"*. **Die
Abbildung stellt ihn stillschweigend her.**

Die Richtung ist dabei nicht die schlimmstmögliche: Ein Werkzeugname, den es nicht gibt,
ist kein Werkzeug, und sowohl die Vorabfreigabe als auch das Profil werden dadurch
**enger**. Aber die Zusage A1 hinge dann an einem Zufall, und niemand meldete es.

## 5. Befund 3: `permissions.deny: glob` erzeugt lautlos keine Sperre (M6 bis M8)

Je Zeile: Eingriff in eine Kopie des Repositoriums, ausgelieferter Validator, Rücknahme.
Ausgangslauf 0 Fehler, 0 Warnungen.

| Nr. | Eingriff in `fw-plan/SKILL.md` | Validator |
|---|---|---|
| **M6** | `permissions.deny: edit, exec` → `glob, grep` | **0 Fehler, 0 Warnungen** |
| **M7** | `allowed-tools` um ein Verb `banane` ergänzt | **0 Fehler, 0 Warnungen** |
| **M8** | `allowed-tools: read` → `search` | **0 Fehler, 0 Warnungen** |

**M6 ist der Kern.** Ein Skillautor, der `deny: glob` schreibt, bekommt keine Sperre,
keine Verweigerung und keine Meldung – **genau die Bauform, die D-66 für Argumentmuster
gemessen hat:** *„Wer ein Argumentmuster schreibt, hat deshalb gar keine Schranke, nicht
bloß eine gröbere."*

**Und diese Nicht-Abbildung ist nicht deklariert.** Der Docstring von `deny_abbilden`
führt die *andere* Nicht-Abbildung – die befehlsgenauen Einträge – ausdrücklich mit
Verweis auf D-47 („Bauart wie `hook_tools_absent`") und im Manifest unter
`skill_deny_unmapped`. **Die Verben `grep` und `glob` stehen nirgends.** Ein Kanal ohne
Deklaration, in derselben Funktion, die D-47 zitiert.

**Ausgeliefert wird davon heute nichts:** Keine der vierzehn Quellen schreibt
`deny: grep` oder `deny: glob` (M5). Der Befund ist deshalb **eine Vorsorge, keine offene
Lücke** – für die Skills des Kerns. Für ein Projekt, das einen eigenen `prj-*`-Skill
schreibt, ist er heute wirksam.

## 6. Befund 4 – die Entlastung: Der Kandidat schlägt die falsche Behebung vor (M4)

Der inhaltliche Unterschied, den die Übergabe nennt, ist echt. **Seine Richtung ist die
zulässige:**

| Verb der Quelle | Vorabfreigabe `tool_names` | Sperre `hook_tools` | Lage |
|---|---|---|---|
| `read` | `Read` | `Read` | Sperre ⊇ Vorabfreigabe |
| `grep` | `Grep` | `Grep, Glob` | Sperre ⊇ Vorabfreigabe |
| `glob` | `Glob` | `Grep, Glob` | Sperre ⊇ Vorabfreigabe |
| **`edit`** | `Edit, Write` | `Edit, Write, NotebookEdit` | Sperre ⊇ Vorabfreigabe |
| `exec` | `Bash` | `Bash` | Sperre ⊇ Vorabfreigabe |

**Bei allen fünf ist die Sperrliste mindestens so weit wie die Vorabfreigabe** – und das
ist die Richtung, die man will: Ein Skill, der `edit` freigibt und `edit` sperrt, bekommt
keine Freigabe auf ein Werkzeug, das die Sperre nicht erfasst.

**Der Kandidat wollte `tool_names` auf `hook_tools` heben.** Das hieße, aus
`allowed-tools: Edit, Write` ein `Edit, Write, NotebookEdit` zu machen – **eine
Ausweitung der Vorabfreigabe**, und nach dem Verschärfungsprinzip genau das, was ein
Änderungsantrag begründen müsste. Die Gegenrichtung – `hook_tools.write` um
`NotebookEdit` kürzen – wäre eine Lücke in einer Sperre.

**Zu vereinheitlichen ist deshalb nicht der Inhalt der Listen, sondern die Brücke
zwischen den Vokabularen und die Disziplin, mit der sie bewacht werden.** Und dass die
Vertagung seit 0.35.0 mit „das ändert `allowed-tools` still mit" begründet war, ist damit
**bestätigt und zugleich überholt**: Der Grund stimmte, die Behebung war eine andere.

## 7. Befund 5 – nicht gesucht: Ein Manifest widerspricht sich selbst

`devin-desktop` führt `tool_names: {}` in beiden Blöcken; die Verben gehen unverändert
durch, und jede installierte Skilldatei dieses Packs trägt `allowed-tools: read, grep,
glob` (M1, M2).

Dasselbe Manifest erklärt drei Felder weiter:

> `"hook_tools_absent": ["search"]` – *„Dieser Client führt kein eigenes Suchwerkzeug"*

**Beides kann nicht stimmen.** Entweder hat der Client Suchwerkzeuge, dann ist die
erklärte Abwesenheit falsch; oder er hat keine, dann nennen dreizehn installierte Skills
zwei Werkzeuge, die es nicht gibt.

**Welche Seite falsch ist, ist unerhoben** – Zeile S3 dieses Packs sagt es selbst: *„Das
Durchreichen ist belegt, die Wirkung nicht."* Der **Widerspruch** ist gemessen, seine
Auflösung nicht. Er gehört festgehalten, nicht geraten.

## 8. Befund 6 – nebenbei: Der Kopfkommentar des Validators endet bei Prüfung 31

Kandidat 4 der Übergabe, hier bestätigt: Die Prüfungen **32 bis 37** stehen nicht im
Kopfkommentar von `validate-framework.py`, seit fünf Releases. Wer eine achtunddreißigste
hinzufügt, ohne die sechs nachzutragen, schreibt die Lücke fort.

## 9. Was diese Gegenprüfung nicht leistet

- **Keine Messung an einem Client.** Gemessen sind die Abbildungsfunktionen, der
  Validator und zwei echte Installationen – nicht, wie ein KI-Client auf
  `allowed-tools: banane` reagiert. Dass ein nicht existierender Werkzeugname keine
  Wirkung hat, ist **Erwartung**.
- **Die Werkzeugnamen von `devin-desktop` bleiben unerhoben.** Befund 5 weist einen
  Widerspruch nach, keine Wahrheit.
- **Ob `grep`/`glob` in `disallowed-tools` wirken würden, ist nicht gemessen.** Belegt
  ist, dass heute **nichts** erzeugt wird. Ob `Grep, Glob` dort die Suche sperrten, wäre
  eine eigene Erhebung – dieselbe Frage, die D-64 für `Write, Edit` beantwortet hat.
- **Die Zahl 14 der Quellen ist gezählt, nicht ausgerechnet.** Sie umfasst dreizehn
  `SKILL.md` (zwölf `fw-*`, einer aus dem Rollenpack) und ein Agentenprofil.

## 10. Gegenzeichnung

| Feld | Inhalt |
|---|---|
| Durchgeführt von | `<FRAMEWORK_OWNER>` |
| Gegengezeichnet | *offen* |
| Folge | `CR-2026-062`, Ziel-Release `0.40.0` |

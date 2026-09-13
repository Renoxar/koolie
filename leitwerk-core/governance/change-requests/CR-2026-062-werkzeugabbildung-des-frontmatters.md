# Änderungsantrag `CR-2026-062`

| Feld | Inhalt |
|---|---|
| Titel | Zwei Listen für dieselbe Sache – es sind vier, und die unbewachte trägt die Zusagen S3 und A1 |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-13 |
| Betroffene Artefakte | `clientmap.py` (Vokabular, Brücke, `frontmatter_werkzeuge`), `install.py` (drei Aufrufstellen, `DENY_VERB_EIMER` entfällt), `clients/devin-desktop/manifest.json` (`tool_names_unmapped` in beiden Blöcken), `clients/devin-desktop/CLIENT_PACK.md` (Änderungsverlauf), `clients/README.md` (Anleitung für ein neues Pack), `tests/scripts/validate-framework.py` (Prüfung 38 neu, Kopfkommentar 32 bis 38, nachgezogener Anker und Verbtabelle der Prüfung 33), `tests/scripts/probe-pruefungen.py` (neun Sonden, zwei Gegenproben), `governance/DECISION_LOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – die Abbildung trägt die Zusagen S3 (Werkzeugsperre je Skill) und A1 (rein lesendes Reviewprofil); beide sind Framework-Gut |
| Art | Änderung; erledigt **Kandidat 1** der Übergabe (seit 0.35.0 vertagt) und **Kandidat 4** (Kopfkommentar) |
| Dringlichkeit | **P2.** Ausgeliefert ist heute nichts Falsches – keine der vierzehn Quellen trifft einen der stillen Fälle. Die Bauform ist trotzdem die schwerste, die dieses Projekt kennt: eine Abbildung, die bei jeder Lücke stumm das Falsche tut, an zwei Stellen, unter zwei Zusagen |

## 1. Anlass

**Kandidat 1** steht seit fünf Releases: *„`skill_frontmatter.tool_names` und `hook_tools`
sind zwei Listen für dieselbe Sache und auseinandergelaufen – `tool_names.edit` führt kein
`NotebookEdit`."* Vertagt worden ist er mit Grund: *„Die Vereinheitlichung ändert
`allowed-tools` still mit, und das gehört in einen eigenen Antrag."*

**Der Befund ist gegengeprüft** (`tests/protocols/2026-09-13-gegenpruefung-werkzeugabbildung.md`,
zwanzig Messungen, davon sieben Kontrollläufe). **Er bestätigt sich – und er ist ein
anderer, als der Kandidat sagt.**

### 1.1 Befund 1: Es sind vier Abbildungen, nicht zwei

| Stelle | Vokabular | Trägt | Bewacht? |
|---|---|---|---|
| `skill_frontmatter.tool_names` | `read, grep, glob, edit, exec` | `allowed-tools` – eine **Vorabfreigabe** (B01) | **nein** |
| `agent_frontmatter.tool_names` | dieselben fünf, zeichengleicher Block | `tools` des Profils – eine **Entfernung aus dem Vorrat** (A1, D-68) | **nein** |
| `hook_tools` | `read, search, exec, write` | Hook-Matcher **und** `disallowed-tools` (S3, D-64) | ja |
| `permission_tools` | `read, search, write, exec, fetch, mcp` | die Berechtigungsdatei, B1 bis B6 | ja |

Dazu `DENY_VERB_EIMER` in `install.py` als fünfte Stelle: die Brücke zwischen dem
Vokabular der Quelle und dem der Durchsetzung. Sie führt `edit`, `write`, `exec`, `read`
und `search` – **drei Verben der Quelle und zwei der Durchsetzungsschicht** – und kennt
`grep` und `glob` nicht.

### 1.2 Befund 2: Drei Abbildungen brechen ab, eine reicht durch

Dieselbe Lücke, an einer echten Installation gemessen:

| Eingriff ins Manifest | Ergebnis |
|---|---|
| `skill_frontmatter.tool_names` verliert `grep` | **durchgelaufen** → `allowed-tools: Read, grep, Glob` |
| `agent_frontmatter.tool_names` verliert `read` | **durchgelaufen** → `tools: read, Grep, Glob` |
| **beide `tool_names`-Blöcke ganz geleert** | **durchgelaufen** → `tools: read, grep, glob` |
| *Kontrolle:* `hook_tools` verliert `search` | **Abbruch** |
| *Kontrolle:* `hook_tools.search` leer | **Abbruch** |
| *Kontrolle:* `permission_tools` verliert `exec` | **Abbruch** |

Die dritte Zeile liefert das Reviewprofil `fw-reviewer` mit drei Werkzeugnamen aus, die
der Client nicht kennt – und stellt damit genau den Fall her, den Zeile **A1** desselben
Packs als **nicht gemessen** ausweist: *„dass ein Profil, dessen `tools`-Liste sich zu
keinem Werkzeug auflöst, gar nicht erst gestartet wird."*

### 1.3 Befund 3: `permissions.deny: glob` erzeugt lautlos keine Sperre

Gemessen: `deny: [glob, grep]` in `fw-plan/SKILL.md` – erzeugte Sperre **keine**,
Validator **0 Fehler, 0 Warnungen**. Dieselbe Bauform, die D-66 für Argumentmuster
gemessen hat: *„Wer ein Argumentmuster schreibt, hat gar keine Schranke, nicht bloß eine
gröbere."*

**Und diese Nicht-Abbildung ist nicht deklariert.** Der Docstring von `deny_abbilden`
führt die *andere* Nicht-Abbildung – die befehlsgenauen Einträge – mit ausdrücklichem
Verweis auf D-47 („Bauart wie `hook_tools_absent`") und im Manifest unter
`skill_deny_unmapped`. **`grep` und `glob` stehen nirgends.** Ein Kanal ohne Deklaration,
in derselben Funktion, die D-47 zitiert.

**Betroffen ist heute niemand:** Keine der vierzehn ausgelieferten Quellen schreibt
`deny: grep` oder `deny: glob`. Für einen projekteigenen `prj-*`-Skill wirkt der Befund
sofort.

### 1.4 Befund 4 – die Entlastung: Der Kandidat schlägt die falsche Behebung vor

Der inhaltliche Unterschied ist echt, **seine Richtung ist die zulässige**: Bei allen fünf
Verbpaaren ist die Sperrliste mindestens so weit wie die Vorabfreigabe
(`tool_names.edit` = `Edit, Write` ⊆ `hook_tools.write` = `Edit, Write, NotebookEdit`).

**`tool_names` auf `hook_tools` zu heben wäre eine Ausweitung** der Vorabfreigabe; die
Gegenrichtung wäre eine Lücke in einer Sperre. **Zu vereinheitlichen ist nicht der Inhalt
der Listen, sondern die Brücke zwischen den Vokabularen und die Disziplin, mit der sie
bewacht werden.**

### 1.5 Befund 5 – nicht gesucht: Ein Manifest widerspricht sich selbst

`devin-desktop` erklärt unter `hook_tools_absent`: *„Dieser Client führt kein eigenes
Suchwerkzeug"* – und reicht zugleich in jeder installierten Skilldatei `grep` und `glob`
als Werkzeugnamen durch. **Beides kann nicht stimmen.** Welche Seite falsch ist, ist
**unerhoben**; Zeile S3 dieses Packs sagt es selbst: *„Das Durchreichen ist belegt, die
Wirkung nicht."*

## 2. Warum eine Ausweitung der Vorabfreigabe zählt, obwohl `allowed-tools` keine Zusage ist

Gegen Abschnitt 1.4 lässt sich einwenden: Nach **B01** ist `allowed-tools` ohnehin keine
Beschränkung, sondern eine Vorabfreigabe für den aufrufenden Turn. Eine weitere Zeile
darin ändere nichts, was das Framework zusagt.

**Der Einwand trägt nicht, und zwar aus demselben Grund wie bei `CR-2026-061` Abschnitt 2:**
Was eine Vorabfreigabe ändert, ist nicht der Mechanismus, sondern die **Rückfrage, die
entfällt**. Ein `NotebookEdit`, das heute eine Rückfrage auslöst, löste danach keine mehr
aus – bei drei Skills, für ein Werkzeug, das keine der vierzehn Quellen je genannt hat.
**Das ist genau der Vorgang, für den das Verschärfungsprinzip einen Antrag verlangt**, und
er gehört nicht in einen Nebensatz beim Aufräumen.

## 3. Vorgeschlagene Änderung

1. **Ein deklariertes Vokabular, an einer Stelle.** `clientmap.FRONTMATTER_VERBEN =
   ("read", "grep", "glob", "edit", "exec")` – die Verben, die ein Skill oder ein
   Agentenprofil des Kerns schreiben darf.
2. **Eine Brücke, an derselben Stelle.** `clientmap.VERB_BRUECKE` bildet sie auf das
   Vokabular der Durchsetzung ab (`grep`/`glob` → `search`, `edit` → `write`).
   `DENY_VERB_EIMER` in `install.py` entfällt.
3. **`clientmap.frontmatter_werkzeuge(man, block, verb)`** wird der einzige Weg von einem
   Verb zu Werkzeugnamen. Drei Ausgänge, keiner davon still: abgebildet → die Namen; in
   `tool_names_unmapped` deklariert → das Verb unverändert; weder noch →
   `AbbildungsFehler`. Bauform wie `hook_tools_absent` nach D-47.
4. **`permissions.deny` kennt das ganze Vokabular.** `grep` und `glob` bilden auf
   `hook_tools.search` ab; ein Verb außerhalb des Vokabulars bricht die Installation ab,
   statt lautlos auszufallen.
5. **Geprüft wird in beiden Zweigen, umgeschrieben nur im einen.** Ein Pack mit
   `tools_format: list` lässt `allowed-tools` unberührt – ein Schreibfehler soll trotzdem
   beim Installieren auffallen und nicht im übernehmenden Projekt.
6. **`devin-desktop` deklariert seine fünf nicht abgebildeten Verben**, samt
   `_tool_names_unmapped_note`, die den Widerspruch aus 1.5 festhält.
7. **Prüfung 38 (neu)**, vier Gegenstände: der verlorene Anker; die Deklaration je Pack;
   die **Richtung** zwischen Vorabfreigabe und Sperre; die Verben der ausgelieferten
   Quellen.
8. **Der Kopfkommentar des Validators trägt 32 bis 38 nach** (Kandidat 4).

## 4. Auswirkungen

- **Die erzeugten Dateien ändern sich nicht, Byte für Byte.** Gemessen für beide Packs:
  `fw-plan` und `fw-reviewer` tragen nach der Änderung dasselbe wie vorher. Das ist der
  Beleg dafür, dass hier eine **Disziplin** eingezogen und keine Zusage verschoben wird.
- **Prüfung 38 fängt bei den beiden Packs nichts** – nachdem `devin-desktop` deklariert
  hat. Gegen 0.39.0 meldet sie **zehn** Fundstellen, und das sind Deklarationslücken,
  keine Fehlfunktionen. **Gegenstand 3 (die Richtung) ist eine reine Verankerung**, wie
  Prüfung 35 und 36.
- **Ein Projekt, das einen `prj-*`-Skill mit `deny: write` oder `allowed-tools: search`
  schreibt, bekommt ab sofort einen Abbruch statt eines stillen Ausfalls.** Das ist der
  Zweck – und es ist ein Bruch für jeden, der sich auf die lockere Fassung verlassen hat.
  Die Verben `write` und `search` waren in `permissions.deny` bis 0.39.0 zulässig; sie
  sind es nicht mehr.
- **Der Widerspruch bei `devin-desktop` bleibt stehen.** Er wird deklariert, nicht
  behoben; eine Behebung wäre eine Vermutung.
- **Die Vertagung seit 0.35.0 war richtig und ist jetzt überholt.** Der Grund („ändert
  `allowed-tools` still mit") stimmte; die Behebung ist eine andere als die vertagte.

- **Prüfung 33 muss mitgezogen werden.** Sie hält einen Anker auf `DENY_VERB_EIMER` in
  `install.py` und führt daneben eine **eigene**, bewusst unabhängige Verbtabelle. Der
  Anker zeigt nach der Verschiebung ins Leere; die Tabelle führte `write` und `search`
  und kannte `grep` und `glob` nicht – **sie teilte damit genau die Lücke, die sie hätte
  fangen sollen.** Beides wird nachgezogen, die Unabhängigkeit der Tabelle bleibt.

## 5. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | Werden die beiden Listen inhaltlich vereinheitlicht – oder wird nur ihre Richtung verankert? | **Nur die Richtung.** Die Sperrliste darf für kein Verbpaar enger sein als die Vorabfreigabe; die umgekehrte Abweichung bleibt zulässig und ist heute der Fall. **Eine inhaltliche Vereinheitlichung ginge nur in eine der beiden falschen Richtungen:** `tool_names` heben ist eine Ausweitung der Vorabfreigabe (Abschnitt 2), `hook_tools` kürzen eine Lücke in einer Sperre | **Zwei Listen bleiben zwei Listen**, und wer sie nebeneinander liest, sieht weiterhin einen Unterschied. Er ist ab jetzt begründet und bewacht – aber er ist noch da. **Die Gegenposition ist vertretbar:** Eine Liste wäre einfacher zu verstehen als eine Regel über zwei Listen |
| **E2** | Wird ein unbekanntes Verb im Frontmatter ein Fehler – oder bleibt es beim Durchreichen? | **Ein Fehler.** Die drei anderen Abbildungen desselben Manifests brechen im selben Fall ab, gemessen; die vierte war die Ausnahme, nicht die Regel. Ein Client, der die Verben wirklich unverändert führt, deklariert das in `tool_names_unmapped` – die Bauform, die D-47 für `hook_tools_absent` und D-70 für `agent_start_tools_absent` gesetzt haben | **`devin-desktop` muss fünf Verben deklarieren, die es nie abgebildet hat** – und die Deklaration sagt „unerhoben", nicht „so ist es". Das ist ehrlicher als das Schweigen und trotzdem keine Erkenntnis. **Und ein Projekt, das heute an der Lücke vorbei installiert, bekommt einen Abbruch** – gewollt, aber ein Bruch |
| **E3** | Bekommt `permissions.deny` die beiden fehlenden Verben `grep` und `glob`? | **Ja, auf `hook_tools.search`.** Sie sind die meistgenannten Verben des Vokabulars – vierzehn Fundstellen je, im Nachbarfeld desselben Frontmatters. Dass ausgerechnet sie in der Sperrabbildung fehlen, ist kein Entwurf, sondern eine Lücke | **Es fängt heute nichts:** Keine ausgelieferte Quelle schreibt `deny: grep`. Das ist eine **Verankerung**, und sie gehört als solche ausgewiesen. **Und ob `Grep, Glob` in `disallowed-tools` wirklich wirken, ist nicht gemessen** – die Abbildung erzeugt ab jetzt etwas, dessen Wirkung offen ist. Das ist weniger als bei `Write, Edit` (D-64) und mehr als das bisherige Nichts |
| **E4** | Wo stehen Vokabular und Brücke? | **In `clientmap.py`**, von `install.py` und vom Validator gelesen – dieselbe Bauart wie `core_rules` und `basket_rules`. **Drei Stellen brauchen sie**, und eine davon ist eine Prüfung; ein Wert, den eine Prüfung aus einem anderen Modul liest, kann nicht auseinanderlaufen | **`clientmap.py` bekommt Wissen über das Quellformat der Skills**, das bisher in `install.py` stand – das Modul heißt „Semantikabbildung der Berechtigungs- und Hook-Konfiguration" und trägt jetzt mehr. Die Alternative, das Vokabular im Validator zu doppeln, ist genau der Fehler, den dieser Antrag behebt |
| **E5** | Was prüft Prüfung 38, und wo läuft sie? | **Vier Gegenstände im Normallauf:** verlorener Anker, Deklaration je Pack, Richtung, Verben der Quellen. Der vierte Gegenstand ist der einzige, der die **Quellen** misst statt der Manifeste – und er ist der billigste Weg, einen Schreibfehler vor der Auslieferung zu fangen | **Gegenstand 3 fängt heute nichts** und wird es bei disziplinierter Pflege nie tun – eine Verankerung, deren Wert allein an ihren Sonden hängt. **Gegenstand 2 zählt Deklarationen, nicht Richtigkeit:** Ein Pack, das fünf falsche Werkzeugnamen sauber deklariert, besteht sie |
| **E6** | Wird der Widerspruch bei `devin-desktop` (Befund 5) hier behoben? | **Nein – nur festgehalten.** Welche Seite falsch ist, entscheidet eine Erhebung an diesem Client, und sie ist nicht gefahren. Der Widerspruch steht in der `_tool_names_unmapped_note` und in der Roadmap | **Ein bekannter Widerspruch bleibt im Repositorium stehen.** Das ist unbefriedigend – und die Alternative wäre, eine der beiden Seiten zu raten. **Genau das ist die Bauform, die dieses Projekt sich abgewöhnt** |
| **E7** | Wird der Kopfkommentar des Validators um 32 bis 37 ergänzt (Kandidat 4)? | **Ja, im selben Zug.** Eine achtunddreißigste Prüfung einzutragen und die sechs davor auszulassen, schriebe die Lücke fort. Der Gegenstand ist derselbe Absatz | **Ein zweiter Kandidat in einem Release.** Die Alternative wäre ein eigener Antrag für sechs Zeilen Buchhaltung – mehr Verwaltung als Gegenstand |
| **E8** | Ein eigenes Release oder Anhang an das nächste? | **Ein eigenes Release, `0.40.0`.** Der Gegenstand ist geschlossen, und er räumt den ältesten offenen Kandidaten ab | **Das fünfzehnte Release in drei Tagen**, und wieder ist kein Ergebnis eine Messung am Client. Gemessen sind Abbildung, Validator und zwei Installationen |

## 6. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle acht Fragen wie vorgelegt.** E1 nur die Richtung, die Inhalte bleiben unberührt; E2 ein unbekanntes Verb ist ein Fehler, die Abwesenheit wird deklariert; E3 `grep` und `glob` auf `search`, als Verankerung ausgewiesen; E4 Vokabular und Brücke in `clientmap.py`; E5 Prüfung 38 mit vier Gegenständen im Normallauf; E6 der Widerspruch wird festgehalten, nicht behoben; E7 Kopfkommentar 32 bis 38; E8 eigenes Release `0.40.0` |
| Datum | 2026-09-13 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | D-78 (ein Werkzeugverb des Frontmatters wird abgebildet oder seine Nichtabbildung deklariert), D-79 (`permissions.deny` kennt dasselbe Vokabular wie `allowed-tools`), D-80 (die Sperrliste ist nie enger als die Vorabfreigabe) |
| Auflagen | **Der Nachweis, dass sich nichts ändert, gehört in den Wirkungsnachweis** – die erzeugten Dateien beider Packs vor und nach der Änderung, Byte für Byte. **Der Gegenbeweis wird in zwei Zuschnitten ausgewiesen:** wie ausgeliefert (eine Fundstelle, der verlorene Anker) und mit neutralisiertem Anker (zehn Fundstellen). Wer nur die zweite Zahl nennt, behauptet eine Messung, die der ausgelieferte Lauf nicht macht. **Und Gegenstand 3 wird als Verankerung benannt, nicht als Behebung** |
| Ziel-Release | `0.40.0` |
| Umsetzung | umgesetzt mit `0.40.0` |

# Erhebung: Ist `disallowed-tools` bei `claude-code` eine Werkzeugbeschränkung je Skill?

| Feld | Wert |
|---|---|
| Gegenstand | Zeile **S3** der Fähigkeitsmatrix `claude-code`: „Werkzeugbeschränkung je Skill", seit 0.31.0 `[NICHT ABBILDBAR]` mit benanntem, ausdrücklich **schwächerem** Ersatz (D-50) |
| Anlass | Offener Punkt aus `CR-2026-050` und Eintrag in **Paket 6**: „Die Herstellerdokumentation nennt `disallowed-tools` als gesonderten Mechanismus. **Es wäre der Weg, S3 zurückzugewinnen**" – bis heute `[DOK]` und **nicht erhoben** |
| Datum | 2026-09-13 |
| Framework-Version | 0.34.0 (`cf45a01`) |
| Geprüfte Clientversion | **Claude Code 2.1.270** (Modell Opus 5) |
| Umgebung | Windows 11, Python 3.14.4; leeres Verzeichnis im Sitzungs-Scratchpad, **ohne Regeltexte**, Berechtigungsschicht **an** mit `allow`-Liste, Rekorder-Hook auf alle Werkzeuge |
| Belege | `devpacks/leitwerk-erhebungen-2026-09-13/` (außerhalb des Repositoriums, mit eigener README) |
| Ergebnis | **`disallowed-tools` ist eine echte Werkzeugbeschränkung je Skill** – es schlägt sogar eine ausdrückliche `allow`-Regel. **Mit drei gemessenen Grenzen**, von denen die dritte eine lautlose ist |

> **Warum diese Erhebung entsteht.** `AP2-CC-13` hing acht Releases an einem Belegtyp, bei dem
> die *Dokumentation* belegt war und nicht das *Verhalten*; D-50 hat `disallowed-tools` genau
> deshalb **nicht** zugesagt, obwohl die Dokumentation es nennt. D-23 verlangt für eine Zusage
> den Wirkungsnachweis. Er wird hier nachgeholt.

## 1. Was die Dokumentation sagt – und warum das allein nicht reicht

Die Herstellerdokumentation zu Skills führt beide Felder und unterscheidet sie ausdrücklich:

| Feld | Wortlaut der Dokumentation |
|---|---|
| `allowed-tools` | „Tools Claude can use without asking permission during the turn that invokes this skill." Und ausdrücklich: „**It does not restrict** which tools are available: every tool remains callable" |
| `disallowed-tools` | „Tools **removed from Claude's available pool** while this skill is active. … **The restriction clears when you send your next message.** Like deny rules, the field can't remove `EndConversation` while any other tool remains" |

**Der Wortlaut trennt die beiden sauber** – und er nennt die Turngrenze von sich aus. Das ist
ein besserer Ausgangspunkt als bei B01, wo die Matrixzeile eine Aussage trug, die die
Dokumentation so nicht macht. Es bleibt trotzdem `[DOK]`.

## 2. Methode

Vier Vorkehrungen, jede aus einem Befund dieses Projekts:

- **Umgebung ohne Regeltexte** (WN-5, `AP2-DD-11`). Keine `CLAUDE.md`, keine `.claude/rules/`,
  kein Overlay. Sonst lehnt der Agent aus den Regeln ab, und gemessen wäre Modellverhalten.
- **Kein Bypass, sondern eine `allow`-Liste.** Die B01-Messung schaltete die
  Berechtigungsschicht ab. Das geht hier nicht: Ein Bypass könnte die geprüfte Schranke gleich
  mit abschalten, und das Ergebnis wäre nicht zuzuordnen. Stattdessen steht in `allow` alles,
  was die Sonde braucht – **`Write` eingeschlossen**. Damit kann eine Verweigerung von `Write`
  nur noch aus `disallowed-tools` kommen. **Das ist der schärfere Aufbau, nicht der bequemere.**
- **Positivkontrolle im selben Lauf** (Testkatalog Nr. 7): Der Skill liest zuerst `MARKE.txt`.
- **Rekorder-Hook auf alle Werkzeuge.** Ohne ihn ist nicht belegt, dass der Skill überhaupt
  aufgerufen wurde – schlägt der Aufruf fehl, liest die Sitzung die `SKILL.md` als gewöhnliche
  Datei und führt sie im normalen Kontext aus. **Das Ergebnis sähe identisch aus.** Genau so
  ist Lauf A der B01-Messung entstanden, und in dieser Erhebung ist es **zweimal** passiert.

## 3. Läufe

| Lauf | Aufbau | Ergebnis |
|---|---|---|
| **A** | `defaultMode: bypassPermissions` in der Projektdatei | **Verworfen.** Der `Skill`-Aufruf selbst wurde abgewiesen, der Skill nie geladen. Die Projektdatei trägt diesen Modus nicht |
| **B** | `allow`-Liste, `disallowed-tools: Write, Edit` | Positivkontrolle `MARKE-DT-7731` gelesen; **`Write` abgewiesen**, Datei nicht entstanden |
| **C** | **Kontrolllauf:** identisch, ohne das Feld | Positivkontrolle gelesen; **`Write` gelang**, Datei mit `GESCHRIEBEN-7731` entstanden |
| **D** | wie B; danach Turn 2 derselben Sitzung (`claude -c -p`) ohne Skill-Aufruf | Turn 1 abgewiesen, **Turn 2 gelang** |
| **E** | `disallowed-tools: Write, Edit`, Schreiben über **`Bash`** | **gelang** – `BASH-7731` entstanden |
| **F** | `disallowed-tools: Write, Edit, Bash`, sonst wie E | **`Bash` abgewiesen**, Datei nicht entstanden |
| **G** | erster Versuch der Argumentmuster-Messung | **Verworfen, Eigenverschulden** – ohne Vertrauenseintrag gefahren, `Skill` abgewiesen |
| **G′** | `disallowed-tools: Bash(echo verboten:*)` bzw. `Bash(echo verboten *)` | **Beide Formen wirkungslos:** verbotener Befehl lief, **keine Verweigerung** |
| **G″** | **Gegenprobe im selben Skill:** `disallowed-tools: Bash` | **beide Befehle abgewiesen** |

### Die Messung (B) gegen den Kontrolllauf (C)

Beide Läufe zeigen dieselbe Werkzeugfolge – nur der Ausgang von `Write` unterscheidet sich:

```text
Skill | {"skill": "lw-probe-dt"}
Read  | MARKE.txt
Glob  | **/MARKE.txt
Read  | MARKE.txt
Write | DT-SCHREIBPROBE.txt
```

| | Antworttext | `permission_denials` | Datei |
|---|---|---|---|
| **B** | „Permission to use Write has been denied." | **1 Eintrag, `Write`** | nicht entstanden |
| **C** | „SCHREIBEN GELANG" | 0 Einträge | `GESCHRIEBEN-7731` |

`permission_denials` ist die **zweite, vom Antworttext unabhängige Quelle**. Sie stimmt überein.

**`Write` steht in der `allow`-Liste und wurde trotzdem abgewiesen.** Das ist der eigentliche
Befund: `disallowed-tools` wirkt **nicht** als Berechtigungsregel unter anderen, die man
gegeneinander abwägt – es nimmt das Werkzeug aus dem Vorrat, und eine Freigabe holt es nicht
zurück. Damit ist es genau das, was `allowed-tools` nach B01 **nicht** ist.

## 4. Ergebnis

**`disallowed-tools` ist bei diesem Client eine Werkzeugbeschränkung je Skill.** Die Zeile S3
ist damit zurückgewinnbar. **Drei Grenzen sind gemessen und gehören in jede Zusage:**

### 4.1 Die Schranke gilt nur für den aufrufenden Turn (Lauf D)

Turn 1 mit Skill: `Write` abgewiesen. Turn 2 derselben Sitzung, ohne den Skill erneut
aufzurufen: **`Write` gelang**, `TURN2-7731` entstanden. Die Dokumentation sagt das vorher
(„clears when you send your next message"); **gemessen ist es jetzt auch.**

Für das Arbeitsmodell heißt das: Ein „nur lesender" Skill ist nur **während seines Turns** nur
lesend. Er ist keine Betriebsart, sondern eine Schranke mit Verfallsdatum.

### 4.2 Die Liste ist aufzählend, und eine Lücke ist ausnutzbar (Läufe E und F)

Mit `disallowed-tools: Write, Edit` schrieb der Skill **über `Bash`**. Mit
`Write, Edit, Bash` wurde `Bash` abgewiesen. **Der exec-Weg ist also ausdrückbar – aber nur,
wenn er dasteht.** Eine Abbildung, die `deny: edit` auf `Write, Edit` abbildet und `exec`
vergisst, erzeugt eine Zusage mit offener Flanke.

### 4.3 Eine Argumentmuster-Form wirkt **lautlos gar nicht** (Läufe G′ und G″)

`disallowed-tools: Bash(echo verboten:*)` – und ebenso die Schreibweise mit Leerzeichen –
ließ den verbotenen Befehl durchlaufen, **ohne Verweigerung und ohne Fehlermeldung**.
Derselbe Skill mit `disallowed-tools: Bash` wies **beide** Befehle ab.

> **Das ist der wiederkehrende Befundtyp dieses Projekts, und hier in seiner unangenehmsten
> Form:** Der Eintrag sieht aus wie eine Regel, wird angenommen, meldet nichts – und beschränkt
> nichts. Wer `Bash(git push:*)` schreibt, hat keine engere Schranke als wer nichts schreibt.
> **Er hat gar keine.**

Das entscheidet, wie treu das Framework überhaupt abbilden kann. Von den zwölf Quellskills
tragen **fünf befehlsgenaue Verbote** (`Exec(git push)`, `Exec(git reset --hard)` …), teils
neben `allow:`-Einträgen. Für sie gibt es nur zwei ehrliche Wege: das **ganze** Werkzeug sperren
(strenger als gemeint und macht die `allow:`-Einträge derselben Skills wirkungslos) oder sie
**nicht** abbilden und das benennen. Ein `disallowed-tools` mit Argumentmuster ist kein Weg.

## 5. Was diese Erhebung nicht belegt

- **`devin-desktop`.** Die Wirkung der Skill-`permissions` ist dort weiter **unerhoben**; das
  Pack bildet das Feld anders ab. Die Frage ist dort eigens zu stellen.
- **Das Agentenprofil.** Das Review schlug `tools`/`disallowedTools` im Agentenprofil als
  Ersatz vor. Weiterhin ungemessen; diese Erhebung betrifft nur das Skill-Frontmatter.
- **Die Wechselwirkung mit dem Schutz-Hook.** Gemessen ist `disallowed-tools` gegen die
  Berechtigungsschicht (es schlägt `allow`). Ob ein blockierender Hook und eine
  Werkzeugentfernung sich in der Reihenfolge beeinflussen, ist hier nicht geprüft – für den
  Befund unerheblich, beide sperren.
- **Verschachtelte Aufrufe.** Ob die Entfernung auch für einen Unteragenten gilt, den der Skill
  startet, ist nicht gemessen. **Für M1 wäre genau das die nächste Frage.**
- **Kein Lauf in einer vollständigen Installation.** Gemessen ist der Mechanismus, nicht sein
  Zusammenspiel mit den erzeugten Regeln. Das gehört in den Wirkungsnachweis der Umsetzung.
- **Die Turngrenze ist im Druckmodus gemessen**, mit `claude -c -p` als zweitem Turn. Dass eine
  interaktive Sitzung sich gleich verhält, ist Erwartung – dieselbe Mechanik, aber nicht
  derselbe Lauf.

## 6. Gegenzeichnung

| Rolle | Name/Kennung | Datum | Ergebnis bestätigt |
|---|---|---|---|
| `<FRAMEWORK_OWNER>` | `<TBD>` | `<TBD>` | `<TBD>` |

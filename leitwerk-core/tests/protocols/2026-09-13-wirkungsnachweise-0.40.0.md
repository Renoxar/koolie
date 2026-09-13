# Wirkungsnachweise Release 0.40.0 – eine Quelle, ein Vokabular

| Feld | Wert |
|---|---|
| Gegenstand | `CR-2026-062`, D-78 bis D-80: das Werkzeugvokabular des Frontmatters an einer Stelle, der Wächter gegen ein unbekanntes Verb, `permissions.deny` mit dem vollen Vokabular, Prüfung 38 – und der Kopfkommentar des Validators, der bei 31 endete |
| Datum | 2026-09-13 |
| Vorstand | `7701db2` (0.39.0) |
| Grundlage der Zusagen | `tests/protocols/2026-09-13-gegenpruefung-werkzeugabbildung.md`, zwanzig Messungen mit sieben Kontrollläufen |
| Ergebnis | **Validator 0 Fehler, 0 Warnungen. 154 Sonden, Gegenproben und Selbstproben bestanden** (106 Sonden, 41 Gegenproben, 7 Selbstproben) – **in beiden Kodierungsumgebungen, zeilengleich**, null Fehlschläge, Exit 0 |

## 1. Was neu geprüft wird

| Prüfung | Gegenstand | Sonden | Gegenproben |
|---|---|---|---|
| **38, Gegenstand 1** | Der verlorene Anker: ohne `clientmap.FRONTMATTER_VERBEN` und `VERB_BRUECKE` meldet die Prüfung ihr eigenes Fehlen; ohne Quelldateien ebenso | 38h, 38i | – |
| **38, Gegenstand 2** | Die Deklaration je Pack: jedes Verb abgebildet **oder** in `tool_names_unmapped` erklärt, nie beides, kein Schlüssel außerhalb des Vokabulars, nicht leere `_tool_names_unmapped_note` (D-78) | 38a bis 38d | 38a |
| **38, Gegenstand 3** | Die **Richtung**: `hook_tools` ist für kein Verbpaar enger als `tool_names` (D-80) | 38e | **38b** |
| **38, Gegenstand 4** | Die Verben der ausgelieferten Quellen – in `allowed-tools` wie in `permissions.deny` (D-79) | 38f, 38g | – |

**Die zweite Gegenprobe ist die wichtigere Hälfte.** Sie verengt `tool_names.edit` auf
`["Edit"]` – eine Vorabfreigabe, die **enger** ist als die Sperre. Das ist die zulässige
Richtung und heute der Fall; **eine Prüfung, die auch sie beanstandete, wäre die inhaltliche
Vereinheitlichung durch die Hintertür** und damit genau das, was E1 verworfen hat.

## 2. Der Nachweis, dass sich nichts ändert – Byte für Byte

Auflage aus `CR-2026-062` Abschnitt 6. Zwei vollständige Installationen je Pack, einmal aus
dem Vorstand `7701db2`, einmal aus dem Arbeitsbaum, verglichen über **alle** erzeugten
Dateien und nicht nur über die Frontmatter:

| Pack | Dateien vorher | Dateien nachher | nur im Vorstand | nur nachher | inhaltlich verschieden |
|---|---|---|---|---|---|
| `claude-code` | 78 | 78 | keine | keine | **keine** |
| `devin-desktop` | 78 | 78 | keine | keine | **keine** |

**Das ist der Beleg dafür, dass hier eine Disziplin eingezogen und keine Zusage verschoben
wird** – und zugleich die ehrlichste Aussage über den Wert der neuen Prüfung: Sie fängt bei
den beiden ausgelieferten Packs heute **nichts**.

## 3. Der Gegenbeweis – zwei Zuschnitte, und beide gehören genannt

Prüfung 38 misst eine Struktur, die es im Vorstand nicht gibt: Das Vokabular entsteht mit
diesem Release. **Wer nur eine der beiden Zahlen nennt, behauptet mehr, als der ausgelieferte
Lauf leistet.**

| Zuschnitt | Aufbau | Fundstellen |
|---|---|---|
| **A – wie ausgeliefert** | 0.39.0 ausgecheckt, mit dem `install.py` des Vorstands installiert, nur der **neue Validator** hineinkopiert | **1** – der verlorene Anker: „`clientmap.py`: `FRONTMATTER_VERBEN`, `VERB_BRUECKE` fehlt" |
| **B – Anker neutralisiert** | zusätzlich das neue `clientmap.py` | **10** |

**Zuschnitt A ist kein Ausfall, sondern die Prüfung, die tut, was sie soll.** Die Sonde auf
den verlorenen Anker (seit 0.32.0) verlangt genau das: Eine Prüfung, die ihren Gegenstand
über einen Namen findet, meldet dessen Verlust, statt leise zu bestehen.

**Die zehn Fundstellen aus Zuschnitt B** sind fünf Verben mal zwei Blöcke, alle bei
`devin-desktop`:

```text
clients/devin-desktop/manifest.json: skill_frontmatter.tool_names kennt das Werkzeugverb
  'read' | 'grep' | 'glob' | 'edit' | 'exec' nicht, und tool_names_unmapped erklaert die
  Abwesenheit nicht
clients/devin-desktop/manifest.json: agent_frontmatter.tool_names  (dieselben fuenf)
```

**Und das sind Deklarationslücken, keine Fehlfunktionen.** Der Vorstand hat dort nichts
falsch gemacht; er hat nichts gesagt. Genau das ist der Gegenstand von D-78 – und es ist
eine schwächere Belegform als bei Prüfung 36, wo der Gegenbeweis ein Abzählen echter Fehler
war.

**`claude-code` meldet in beiden Zuschnitten nichts.** Sein Manifest bildet alle fünf Verben
ab. Der Befund dieses Releases ist nicht, dass eine Abbildung fehlte, sondern dass ihr
Fehlen **folgenlos** gewesen wäre.

## 4. Der Sondenlauf hat einen Fehler dieser Umsetzung gefangen

**Der wichtigste Einzelbefund dieses Releases stammt nicht aus der Gegenprüfung, sondern aus
dem ersten Sondenlauf gegen die fertige Umsetzung.** Er meldete **fünf** Abweichungen, in
beiden Kodierungsumgebungen dieselben:

```text
GEGENPROBE 33   FEHL  Die unveraenderte claude-code-Installation bleibt unbeanstandet
        Ausgabe: FEHLER  leitwerk-core/install.py: 'DENY_VERB_EIMER' fehlt. Pruefung 33
        misst die Abbildung von permissions.deny auf disallowed-tools; ohne sie prueft
        sie einen Aufbau, den es nicht mehr gibt, und bestuende leise (D-23, CR-2026-057)
SONDE      33a  FEHL  Fehlende Werkzeugsperre - der Stand, den B01 beschrieb
SONDE      33b  FEHL  Unvollstaendige Sperre - mit gesperrtem Write, Edit schrieb der Skill ueber Bash
SONDE      33c  FEHL  Argumentmuster in der Sperre - es sieht aus wie eine Regel und ist keine
SONDE      33d  FEHL  Werkzeug zugleich vorabfreigegeben und gesperrt
```

**Prüfung 33 hielt einen Anker auf `DENY_VERB_EIMER` in `install.py`.** Dieses Release hat
die Konstante nach `clientmap.VERB_BRUECKE` verschoben – der Anker zeigte ins Leere, und die
Prüfung meldete genau das, wofür sie gebaut ist.

**Zwei Lehren, und beide sind nicht neu, sondern bestätigt:**

> **Der Validatorlauf gegen das Repositorium blieb dabei 0 Fehler, 0 Warnungen.** Prüfung 33
> hängt an `skill_deny_field`, und die lokale Testinstallation ist `devin-desktop` – sie
> führt das Feld nicht, die Prüfung läuft dort **gar nicht**. **Das ist Befund B02, an der
> eigenen Änderung ein zweites Mal eingetreten:** nicht, dass eine Prüfung falsch prüft,
> sondern dass sie einen Client nicht sieht. **Ein grüner Repo-Lauf ersetzt den Sondenlauf
> nicht.**

> **Die Sonde auf den verlorenen Anker trägt sich zum zweiten Mal.** Beim Umbau von
> `check_strict_overlay` (0.33.0) war es die Sonde zu D-44, hier ist es der Ankertest der
> Prüfung 33. **Beide Male hat eine Prüfung ihre eigene Verschiebung gemeldet**, statt still
> grün zu bleiben.

**Berichtigt, und zwar an zwei Stellen:** Der Anker zeigt auf `clientmap.VERB_BRUECKE`. Und
die **eigene** Verbtabelle der Prüfung 33 – die bewusst eine eigene bleibt, damit sie nicht
jeden Fehler der Abbildung teilt – führt jetzt dasselbe Vokabular wie die Quelle. **Bis
0.39.0 führte sie `write` und `search` und kannte `grep` und `glob` nicht: Sie teilte genau
die Lücke, die sie hätte fangen sollen.** Der zweite Lauf in beiden Umgebungen ist grün.

## 5. Was beim Bauen sonst aufgefallen ist

### 5.1 Die Vertagung seit 0.35.0 war richtig – und sie hat den Befund verdeckt

Der Grund, mit dem Kandidat 1 fünf Releases lang vertagt wurde, stimmt: Eine inhaltliche
Vereinheitlichung hätte `allowed-tools` still mitgeändert. **Was in dem Satz nicht stand,
ist, dass die Vereinheitlichung gar nicht die Behebung ist.** Gemessen geht die Abweichung
in die zulässige Richtung; zu beheben war die fehlende Bewachung daneben.

**Dieselbe Bauform wie bei 0.38.0**, wo die Ermessensfrage vier Releases lang verdeckt hat,
dass `baumhash` bei *n* Ersetzungen nie „alle" belegt: **Eine Frage, deren Beantwortung
vertagt wird, hält den Blick auf sich – und der Befund daneben wartet.**

### 5.2 Die Zählung war wieder zu klein, zum sechsten Mal an diesem Tag

Die Übergabe nennt **zwei** Listen. Es sind **vier** Werkzeugabbildungen je Manifest, dazu
`DENY_VERB_EIMER` als fünfte, unvollständige Fassung derselben Brücke. Wie schon 25 statt
20, 76 statt 248, fünf statt zehn.

### 5.3 Die Sonden mussten über das JSON präparieren, nicht über den Text

Dieselbe Begründung wie bei Sonde 35a, an einem neuen Gegenstand: `skill_frontmatter` und
`agent_frontmatter` führen **zeichengleiche** `tool_names`-Blöcke. Ein Textanker träfe den
falschen Block – und bei einer Sonde, die gezielt den einen oder den anderen prüfen will,
wäre das ein stiller Fehlgriff.

## 6. Sondenlauf

```text
python leitwerk-core/tests/scripts/probe-pruefungen.py .
Ergebnis: alle Sonden und Gegenproben bestanden        (Exit 0)

PYTHONIOENCODING=utf-8 python leitwerk-core/tests/scripts/probe-pruefungen.py .
Ergebnis: alle Sonden und Gegenproben bestanden        (Exit 0)
```

| | Vorstand 0.39.0 | Arbeitsbaum 0.40.0 |
|---|---|---|
| Sonden | 97 | **106** |
| Gegenproben | 39 | **41** |
| Selbstproben | 7 | 7 |
| **Summe** | 143 | **154** |

Die neuen Meldungen im Wortlaut, in beiden Umgebungen gleich:

```text
SONDE      38a  OK    Ein Verb weder abgebildet noch erklaert - der Stand bis 0.39.0
SONDE      38b  OK    Erklaerte Nichtabbildung ohne Begruendung - eine Behauptung
SONDE      38c  OK    Abgebildet und zugleich fuer nicht abgebildet erklaert
SONDE      38d  OK    Ein Verb der Durchsetzungsschicht in der Abbildung der Quelle
SONDE      38e  OK    Die Sperrliste wird enger als die Vorabfreigabe - der gefaehrliche Fall
SONDE      38f  OK    Eine Quelle nennt in allowed-tools ein fremdes Verb
SONDE      38g  OK    Eine Quelle nennt in permissions.deny ein fremdes Verb
SONDE      38h  OK    Verlorener Anker - das Vokabular verliert seinen Namen
SONDE      38i  OK    Verlorener Anker - keine Quelle mit Frontmatter mehr
GEGENPROBE 38a  OK    Die unveraenderten Packs bleiben unbeanstandet
GEGENPROBE 38b  OK    Eine Vorabfreigabe, die ENGER ist als die Sperre, bleibt unbeanstandet
```

**Keine bestehende Sonde ist verdrängt worden:** 97 + 9 = 106 und 39 + 2 = 41, null
Fehlschläge in 308 Meldezeilen. **Die beiden Läufe sind zeilengleich** – Zeile für Zeile
verglichen, nicht nur in der Summe.

> **Zum Stand des Laufs, damit die Zahl nicht mehr behauptet, als sie deckt:** Die beiden
> Läufe stehen auf dem Baum **nach** der letzten Codeänderung (dem nachgezogenen Anker der
> Prüfung 33). Danach sind nur noch `CHANGELOG.md`, `docs/ROADMAP.md` und der
> Änderungsantrag ergänzt worden – **drei Markdown-Dateien, die keine Sonde inhaltlich
> verankert**; die einzige Sonde, die die Roadmap überhaupt anfasst (B03), hängt Text an
> und liest den Bestand nicht. Der Validator läuft über den Endstand mit 0/0.

## 7. Was dieses Release nicht belegt

- **Keine Messung an einem Client.** Dass ein nicht existierender Werkzeugname wie `banane`
  oder `read` (bei `claude-code`) keine Wirkung hat, ist **Erwartung**. Gemessen ist, was
  die Abbildung erzeugt und was der Validator sieht.
- **Ob `Grep, Glob` in `disallowed-tools` wirken, ist nicht gemessen.** Die Abbildung
  erzeugt ab jetzt für `deny: grep` etwas, dessen Wirkung offen ist – weniger belegt als bei
  `Write, Edit` (D-64) und mehr als das bisherige Nichts. Wer die Reihe fortsetzen will,
  misst das mit derselben Umgebung wie D-64.
- **Prüfung 38 zählt Deklarationen, nicht Richtigkeit.** Ein Pack, das fünf falsche
  Werkzeugnamen sauber deklariert, besteht sie.
- **Die Werkzeugnamen von `devin-desktop` bleiben unerhoben**, und der Widerspruch zwischen
  `hook_tools_absent: ["search"]` und den durchgereichten Verben `grep`/`glob` bleibt
  stehen. Er ist jetzt im Manifest festgehalten – aufgelöst ist er nicht.
- **Gegenstand 3 ist eine Verankerung.** Sie fängt heute nichts und wird es bei
  disziplinierter Pflege nie tun; ihr Wert hängt allein an Sonde 38e und Gegenprobe 38b.
- **Ein Pack mit `tools_format: list` schreibt `allowed-tools` nicht um.** Die Verben werden
  dort geprüft, aber nicht abgebildet – ein `devin-desktop`-Skill trägt weiter die Verben
  selbst. Das ist gewollt und in `tool_names_unmapped` deklariert; es heißt aber, dass die
  Abbildung dort keine Wirkung hat, die man messen könnte.
- **Die eigene Verbtabelle der Prüfung 33 ist von Hand nachgezogen worden.** Sie darf die
  Brücke nicht importieren – sonst teilte sie jeden Fehler der Abbildung –, und deshalb kann
  sie wieder auseinanderlaufen. **Was das verhindert, ist allein ihr Ankertest**, und der
  hat in diesem Release gezeigt, dass er trägt.

## 8. Gegenzeichnung

| Rolle | Name/Kennung | Datum | Ergebnis bestätigt |
|---|---|---|---|
| `<FRAMEWORK_OWNER>` | `<TBD>` | `<TBD>` | `<TBD>` |

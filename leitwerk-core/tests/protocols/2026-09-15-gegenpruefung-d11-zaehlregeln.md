# Gegenprüfung der vier D-11-Zählregeln und Wirkungsnachweis 0.48.0

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-15 |
| Gegenstand | Die vier Zählregeln des 1.0.0-Standes aus `docs/ROADMAP.md`, und Prüfung 46, die sie ersetzt |
| Anlass | Kandidat 2 der Übergabe: der D-11-Zähler. Die Roadmap verlangt, seine Ermessensfrage **vor** dem Bauen zu entscheiden – dafür mussten die vier Zahlen einmal wirklich ausgerechnet werden |
| Antrag | `CR-2026-070`, D-98, D-99 |
| Grundlage | D-23: Eine Prüfung gilt erst als vorhanden, wenn sie eine bewusst gesetzte Sonde meldet. Dazu der Gegenbeweis gegen den Vorstand |
| Ergebnis | **154 Sonden, 62 Gegenproben, 12 Selbstproben – alle bestanden, in beiden Kodierungsumgebungen zeilengleich** (Exit 0). Validator: 0 Fehler, 0 Warnungen. **Gegenbeweis gegen 0.47.0: alle sechs Sonden fallen, alle drei Gegenproben bestehen dort** |

## 1. Der Befund, abgezählt

**Die Auflage des Antrags verlangt je Regel die Fundstelle und den Grund.** Hier stehen sie.

| # | Kriterium (D-11) | Zählregel bis 0.47.0 | Geglaubt | **Gezählt** |
|---|---|---|---|---|
| 1 | kein unbearbeiteter `VERIFY`-Marker | `docs/ROADMAP.md:31` – `grep -rl "VERIFY AGAINST CURRENT CLIENT DOCUMENTATION"` | 27 in 26 Dateien | **29** |
| 2 | Testkatalog ohne `offen` | `docs/ROADMAP.md:32` – „Ergebnisspalte …, dazu die dezentralen `TESTS.md` je Skill" | 103 | **118** |
| 3 | alle Modulstatus über `entwurf` | `docs/ROADMAP.md:33` – vier genannte Ablagen | 16 | **69** |
| 4 | keine Decision Records `entschieden (Vorschlag)` | `docs/ROADMAP.md:34` – `governance/DECISION_LOG.md` | 16 | **9** |

### 1.1 Kriterium 1 – eine von zwei registrierten Schreibweisen

`docs/PLACEHOLDER_REGISTRY.md:80` führt eine **zweite** Markerform als „clientgebundene
Altform", nur im Client Pack `devin-desktop` zulässig – **mit derselben Frist in der
Spalte „Ersetzung/Frist": „vor Version 1.0.0".** Der Zählbefehl kennt sie nicht.

Fundstellen der Altform, gezählt über den ganzen Baum:

| Datei | Fundstellen | Gewicht |
|---|---|---|
| `clients/devin-desktop/CLIENT_PACK.md` | **7** | Die Fähigkeitsmatrix eines ausgelieferten Packs |
| `clients/devin-desktop/root-template/.devin/README.md` | **2** | **Eine Datei, die jede Devin-Installation bekommt** |
| `governance/DECISION_LOG.md` | 2 | `K-20` (offener Verifikationsbedarf) und `A-05` (Annahme) |
| `docs/PLACEHOLDER_REGISTRY.md` | 1 | die Registerzeile selbst |
| `CHANGELOG.md`, drei Änderungsanträge, ein Protokoll | 7 | historische Aufzeichnung, außerhalb des Zählbereichs |
| `build/out/hauptdokument.md` | 12 | Erzeugnis, außerhalb des Zählbereichs |
| `README.md` (Wurzel) | 1 | **Nebenbefund**, siehe Abschnitt 5 |

**Der Zählbefehl meldete an allen diesen Stellen null.**

### 1.2 Kriterium 2 – die dreizehnte Ablage

„je Skill" wurde als zwölf `framework/skills/*/TESTS.md` gelesen. Der Baumdurchlauf findet
**dreizehn**:

```
15/15  framework/role-packs/requirements-engineering/skills/role-re-ticket/TESTS.md   ← nie gezählt
 6/ 6  framework/skills/fw-bugfix-prepare/TESTS.md
 5/ 5  framework/skills/fw-change-analyze/TESTS.md
 7/ 7  framework/skills/fw-change-small/TESTS.md
 5/ 5  framework/skills/fw-code-explain/TESTS.md
 6/ 6  framework/skills/fw-docs-update/TESTS.md
 6/ 6  framework/skills/fw-error-analyze/TESTS.md
 6/ 6  framework/skills/fw-mr-description/TESTS.md
 6/ 6  framework/skills/fw-plan/TESTS.md
 7/ 7  framework/skills/fw-refactor/TESTS.md
 5/ 5  framework/skills/fw-repo-analyze/TESTS.md
 7/ 7  framework/skills/fw-review-support/TESTS.md
 6/ 6  framework/skills/fw-tests/TESTS.md
──────
87 offen  (+ 31 im Katalog = 118)
```

**Ein Role-Pack-Skill ist ein Skill.** 72 + 15 = 87, und 31 + 87 = 118 statt 103.

### 1.3 Kriterium 3 – ein Viertel des Bestands, und ein Zählort ohne Gegenstand

Die vier genannten Ablagen decken 16 Träger. Der Bestand an Steckbriefzeilen `| Status |`
im Kern beträgt **69**, verteilt auf:

| Ablage | Träger auf `entwurf` | In der alten Regel genannt |
|---|---|---|
| `prompts/` | 12 | nein |
| `checklists/` | 11 | nein |
| `governance/` | 7 | nein |
| `decision-trees/` | 6 | nein |
| `onboarding/` | 4 | nein |
| `clients/` | 4 | nein |
| `docs/` | 3 | nein |
| `pilot/`, `tests/` | je 2 | nein |
| `templates/` | 1 | nein |
| `framework/skills/*/SKILL.md` | 12 | **ja** |
| `framework/role-packs/`, `framework/tech-packs/` | 5 | **ja** |
| `framework/core/` | **0 – dort gibt es keine Statuszeile** | **ja** |

**Zwei Befunde in einem:** Die Liste deckt ein Viertel, und einer ihrer vier Orte hat
überhaupt keinen Gegenstand. Dazu ein dritter: `role-packs/software-development/ROLE_PACK.md`
trägt `entwurf (Referenzpack der Erstfassung)` – ein Gleichheitsvergleich sieht sie nicht,
der Vergleich am **ersten Wort** schon.

**Und die Feststellung, die aus dem Abzählen folgt:** Von 69 Trägern steht **keiner** über
`entwurf`. Das Lebenszyklusmodell aus `framework/core/08-skill-conventions.md` Abschnitt 7
(`entwurf` → `pilot` → `aktiv`) ist in diesem Repositorium **noch nie angewendet worden**.

### 1.4 Kriterium 4 – die einzige Zahl, die zu groß war

`grep -c "entschieden (Vorschlag)" governance/DECISION_LOG.md` liefert **16**. Davon sind:

| Zeile | Was es ist | Zählt nach D-11? |
|---|---|---|
| Zeile 4 | die **Legende**, die den Statuswert erklärt | nein |
| `K-08`, `K-12`, `K-13`, `K-17`, `K-18` | **Klärungspunkte** – keine Decision Records | nein |
| `D-11` | der Kriterientext selbst („keine Decision Records im Status …") | nein |
| `D-01` bis `D-08`, `D-10` | **Decision Records** | **ja – neun** |

**D-11 sagt „Decision Records".** Ein Klärungspunkt ist keiner, und die Definition eines
Kriteriums ist kein Fall des Kriteriums.

## 2. Der Sondenlauf

`python leitwerk-core/tests/scripts/probe-pruefungen.py .`

| Einheit | Gegenstand | Ergebnis |
|---|---|---|
| Sonde 46a | Eine Zahl der Standzeile steht zu hoch – der Zähler meldet den **nicht nachgezogenen Fortschritt** | **OK** |
| Sonde 46b | Ohne Standzeile meldet die Prüfung den **verlorenen Anker**, statt leise zu bestehen | **OK** |
| Sonde 46c | Ein neuer Marker im Kern hebt Kriterium 1 | **OK** |
| Sonde 46d | Ein Testblatt an einer Ablage, die keine Liste kennt, hebt Kriterium 2 | **OK** |
| Sonde 46e | Ein neues Modul auf `entwurf` hebt Kriterium 3 – **auch außerhalb der vier früher genannten Ablagen** | **OK** |
| Sonde 46f | Ein gehobener Decision Record **senkt** Kriterium 4 – die zweite Richtung | **OK** |
| Gegenprobe 46a | Das unveränderte Repositorium bleibt unbeanstandet | **OK** |
| Gegenprobe 46b | Ein **Klärungspunkt** mit demselben Statuswort bleibt ungezählt | **OK** |
| Gegenprobe 46c | Ein Marker in einem **datierten Protokoll** bleibt ungezählt | **OK** |
| Selbstprobe C1 | Der Baumdurchlauf findet **15** Kerndateien, die eine Mustersuche überspringt | **OK** |

**Warum sechs Sonden und nicht zwei:** Ein Zähler, der nur Rückfälle meldet, hielte still,
solange sich nichts verschlechtert – und der Stand stünde wieder daneben. Sonde 46f ist die
Gegenrichtung, und ohne sie wäre die Prüfung ein Fortschrittsbalken.

**Abnahme (D-49, D-94):**

| Lauf | Ergebniszeilen oberhalb der Trennlinie | Exit |
|---|---|---|
| ohne `PYTHONIOENCODING` | **250** | 0 |
| mit `PYTHONIOENCODING=utf-8` | **250**, zeilengleich | 0 |
| `--bahnen 1` (streng seriell) | **derselbe Einheitensatz, sortiert zeilengleich** | 0 |

Kein `AUFRAEUMER`-Eintrag in den Abnahmeläufen.

> **Was der serielle Vergleich belegt und was nicht.** Er belegt, dass die Nebenläufigkeit
> keine Einheit verschluckt und keine zusätzlich erzeugt – eine Eigenschaft der
> Ablaufsteuerung, nicht des Meldetextes. Gemessen ist er an einem Zwischenstand desselben
> Tages, der sich vom Abnahmestand nur im **Wortlaut von sechs Beschreibungssätzen**
> unterscheidet; der Einheitensatz ist identisch. **Die Abnahmeform nach D-49 sind die
> beiden Kodierungsumgebungen, und die sind zeilengleich** – der serielle Lauf ist seit
> 0.46.0 eine Zugabe, keine Abnahmebedingung.

## 3. Der Gegenbeweis gegen den Vorstand

Gemessen mit dem **neuen** Sondenskript gegen einen **vollständigen** Arbeitsbaum auf
0.47.0 – `leitwerk-core/` und `README.md` auf den Stand von `b6fd621` zurückgesetzt,
Wurzelerzeugnisse unberührt. Sein eigener Validatorlauf meldet dort 0 Fehler, 0 Warnungen.

| Einheit | Gegen 0.47.0 | Erwartet | Art des Fallens |
|---|---|---|---|
| Sonde 46a | **FEHL** | fällt | *Präparation gebrochen* – die Standzeile gibt es dort nicht |
| Sonde 46b | **FEHL** | fällt | *Präparation gebrochen* – dieselbe Ursache |
| Sonde 46c | **FEHL** | fällt | die Prüfung fehlt |
| Sonde 46d | **FEHL** | fällt | die Prüfung fehlt |
| Sonde 46e | **FEHL** | fällt | die Prüfung fehlt |
| Sonde 46f | **FEHL** | fällt | die Prüfung fehlt |
| Gegenprobe 46a | OK | **besteht** | – |
| Gegenprobe 46b | OK | **besteht** | – |
| Gegenprobe 46c | OK | **besteht** | – |

**Zwei der sechs fallen aus einem anderen Grund als die übrigen vier, und das ist der
richtige Grund:** Sie präparieren eine Zeile, die im Vorstand noch gar nicht existiert.
Der Präparationswächter aus D-74 unterscheidet genau das – eine Sonde, die ihren
Gegenstand nicht findet, meldet das und gibt sich nicht als Befund aus.

## 4. Was der Lauf beim Bauen gefunden hat – dreimal

### 4.1 Der eigene Prüfapparat fing den eigenen Kopfkommentar

Die erste Fassung des Kopfkommentars von Prüfung 46 schrieb die clientgebundene
Markerform **wörtlich** hin, um den Befund zu belegen. **Prüfung 14 verbietet genau das im
Kern** und meldete es im ersten Lauf:

```
FEHLER   …/validate-framework.py:4643: Der Platzhalter <…> traegt den Clientnamen 'DEVIN'.
         Ein Platzhalter bindet den Kern damit an ein Produkt (D-02)
```

Beschrieben statt zitiert. Der Regex der Prüfung erzeugt die Zeichenkette nicht, weil er
beide Namen als Alternative führt.

### 4.2 Die Sonde fing einen Fehler in ihrer eigenen Prüfung

Sonde 46a setzte Kriterium 4 von `9` auf `99` und erwartete eine Meldung. **Sie kam
nicht.** Der Zahlenvergleich lief über `soll in text` – und `"Kriterium 4 = 9"` steckt als
Präfix in `"Kriterium 4 = 99"`. Verglichen werden jetzt die **Zahlen**, nicht die
Zeichenkette.

**Das ist der Wert einer Sonde in einem Satz:** Die Prüfung war grün, der Validatorlauf
war grün, und sie hätte jede Zahl durchgelassen, die mit der richtigen beginnt.

### 4.3 Der Fallstrick, der zweimal zuschnappte

Die erste Fassung des Zählers lief über `glob.glob(..., recursive=True)`.
**`glob` überspringt Pfadbestandteile mit führendem Punkt.** Damit fehlten **15**
Kerndateien, darunter genau die zwei Träger, die den Befund zu Kriterium 1 tragen:

```
leitwerk-core/clients/claude-code/root-template/.claude/README.md
leitwerk-core/clients/devin-desktop/root-template/.devin/README.md
```

**Der Zähler hätte 27 gemeldet – und damit zufällig die geglaubte Zahl bestätigt.** Eine
Zählregel, die einen Träger still überspringt, war der **Anlass** dieses Antrags; sie ist
beim Bauen der Abhilfe ein zweites Mal entstanden. Behoben mit `os.walk`, gemessen mit der
Selbstprobe `C1` – eine benannte Falle, in die man zweimal tritt, gehört in den Code
(D-74).

### 4.4 Zwei Fehler im Einbau selbst

Der Einbauskript-Lauf setzte die Textersetzung **zweimal** auf denselben Block an und
erzeugte dabei 209 doppelte Wagenrückläufe (`\r\r\n`); und die Beschreibungssätze der
neuen Einheiten trugen Umlaute, was die **zeilengleiche Abnahme nach D-49 brach** – der
Lauf ohne `PYTHONIOENCODING` und der mit ihm waren nicht zeilengleich. Beide Male hat der
Vergleich es gemeldet, kein Lesen. Die Sätze dieses Skripts sind aus genau diesem Grund
seit 0.27.0 ohne Umlaute geschrieben; die Suchtexte dürfen welche tragen, weil
`unterprozess()` beide Seiten auf UTF-8 festlegt.

## 5. Nebenbefund: die Wurzel-README nannte die Altform

`README.md:165` beschreibt die Konventionen dieses Frameworks und nannte dabei die
**clientgebundene** Altform an einer werkzeugneutralen Stelle. Seit `CR-2026-024` ist die
neutrale Form die im Kern zu verwendende (D-02).

**Prüfung 14 greift dort nicht:** Sie misst die Ablagen des Kerns, und die Wurzel-README
ist keine. **Berichtigt, nicht geprüft** – eine Prüfung für eine Datei, die jedes Projekt
durch seine eigene ersetzt, wäre ohne Gegenstand.

## 6. Was dieses Protokoll nicht belegt

- **Dass 29, 118, 69 und 9 die *richtigen* Zahlen sind.** Belegt ist, dass sie das
  Ergebnis der niedergeschriebenen Regeln sind und dass die vorherigen Regeln es nicht
  waren. Wo die Grenze eines Begriffs Ermessen ist – zählt eine Registerzeile als
  unbearbeiteter Marker? –, steht die Entscheidung im Antrag (E3) und nicht in der Zahl.
- **Dass Kriterium 3 mit 69 „schlimmer" steht als mit 16.** Es stand immer bei 69; nur
  gezählt wurden 16.
- **Dass der Zähler Fortschritt misst.** Er misst Zahlen. Ein Modulstatus, der gehoben
  wird, ohne dass jemand das Modul angesehen hat, senkt Kriterium 3 um eins.
- **Irgendetwas über Kriterium 5.** Das ist keine Zahl, und die Prüfung enthält sich –
  ausdrücklich, im Kopfkommentar.

## 7. Die Lehre, die über diesen Fall hinausgeht

Die Roadmap führte seit 0.42.0 bewusst keine Zahlen, sondern *die Befehle, die sie
ausrechnen*. Das war die richtige Lehre aus fünf falschen Zahlen über den Prüfapparat –
**und sie ist nicht eingelöst worden.**

> **Ein Befehl, den niemand ausführt, ist keine Ausrechnung, sondern eine Zahl mit einem
> Zwischenschritt.** Und weil ihn niemand ausführt, fällt auch nicht auf, dass er das
> Falsche zählt.

Der Unterschied zu 0.42.0 ist einer im Ort, nicht in der Bauform: Dort stand die falsche
Zahl über den **Prüfstand**, hier über den **Meilenstein**. Es gibt in diesem Repositorium
genau ein Ziel, und sein Stand war an vier von vier Stellen unrichtig.

## 8. Die erste Anwendung des Zählers: dreiundzwanzig Releases rückwirkend

**Der Zähler kann rückwärts laufen.** `git archive` je Releasestand, darauf `_d11_zaehlen`
aus 0.48.0 – dieselbe Regel auf jeden Stand, also vergleichbar. Das ist die erste Messung,
die dieses Repositorium über seinen eigenen Fortschritt hat.

| Release | K1 | K2 | K3 | K4 | **Summe** | Prüfungen im Register |
|---|---|---|---|---|---|---|
| 0.26.0 | 30 | 117 | 67 | 9 | **223** | 24 |
| 0.27.0 | 29 | 117 | 67 | 9 | **222** | 25 |
| 0.28.0 | 29 | 117 | 67 | 9 | **222** | 25 |
| 0.29.0 | 29 | 117 | 67 | 9 | **222** | 25 |
| 0.30.0 | 29 | 117 | 67 | 9 | **222** | 25 |
| 0.31.0 | 30 | 117 | 67 | 9 | **223** | 25 |
| 0.32.0 | 30 | 118 | 69 | 9 | **226** | 30 |
| 0.33.0 | 31 | 118 | 69 | 9 | **227** | 31 |
| 0.34.0 | 30 | 118 | 69 | 9 | **226** | 31 |
| 0.35.0 | 29 | 118 | 69 | 9 | **225** | 31 |
| 0.36.0 … 0.47.0 | 29 | 118 | 69 | 9 | **225** | 31 → 45 |
| 0.48.0 | 29 | 118 | 69 | 9 | **225** | 46 |

**Seit 0.35.0 steht der Stand auf der Stelle – dreizehn Releases, auf die Ziffer genau
unverändert.** Der Prüfapparat ist in derselben Zeit von 31 auf 46 Prüfungen gewachsen.
Über den ganzen gemessenen Zeitraum, 0.26.0 bis 0.48.0, ist die Summe von 223 auf 225
**gestiegen**.

**Kriterium 4 steht seit 0.26.0 unverändert bei neun.** In dreiundzwanzig Releases ist
kein einziger Decision Record aus `entschieden (Vorschlag)` gehoben worden.

### Was diese Tabelle nicht sagt

**Nicht, dass die dreiundzwanzig Releases nutzlos waren.** Sie haben zwölf Review-Befunde
geschlossen, einen Hook repariert, der einunddreißig Releases lang stumm war, den
Suchkanal geschlossen, den Bytecode aus zwei Projekten genommen und den Prüfapparat auf
sechsundvierzig Prüfungen gebracht. **Das hat das Framework richtiger gemacht.**

**Sie sagt, dass „richtiger" und „fertiger" zwei verschiedene Größen sind** – und dass nur
die erste gemessen wurde. Die zweite war nicht messbar, weil ihre vier Zählregeln
danebengriffen. **Ab diesem Release ist sie es.**

### Was daraus folgt

Der billigste Posten ist **Kriterium 4**: neun Decision Records, jeder bereits
fortgeschrieben und an der Praxis von dreiundzwanzig Releases geprüft. Das ist reine
Entscheidungsarbeit des `<FRAMEWORK_OWNER>` – keine Messung, kein Modellkontingent, keine
Vorarbeit. **Der zweitbilligste ist Kriterium 3**, und dort steht eine Feststellung, die
diese Messung erst sichtbar gemacht hat: **Von 69 Trägern steht keiner über `entwurf`.**
Das Lebenszyklusmodell dieses Frameworks ist in dreiundzwanzig Releases **kein einziges
Mal angewendet worden.**

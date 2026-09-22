# Wirkungsnachweise Release 0.43.0 – der Werkzeugbestand von `devin-desktop`

| Feld | Wert |
|---|---|
| Gegenstand | `CR-2026-065`, D-87 bis D-89: die Suchklasse im Hook, die zwei Namensräume, der Skillaufruf als Werkzeugaufruf, Prüfung 41, Prüfung 38 namensraumbewusst, `install.py` in der Listenform |
| Datum | 2026-09-14 |
| Vorstand | `8c30f17` (0.42.0) |
| Grundlage der Zusagen | `tests/protocols/2026-09-14-erhebung-devin-werkzeuge.md` – **zwölf Läufe am Client** in fünf Umgebungen |
| Ergebnis | **Validator 0 Fehler, 0 Warnungen. 177 Sonden, Gegenproben und Selbstproben bestanden** (123 / 47 / 7) – **in beiden Kodierungsumgebungen, zeilengleich**, Exit 0. Und: **Die Behebung ist am Client gemessen** – derselbe Aufruf, der vorher ein Secret lieferte, wird jetzt abgewiesen |

## 1. Der Wirkungsnachweis am Client – die Auflage des Antrags

Der Antrag macht zur Auflage: *„derselbe `grep`-Aufruf auf `.env` in der Hook-Umgebung,
der vor der Änderung durchlief, muss danach blockiert werden. Ohne diesen Lauf ist die
Behebung eine Behauptung."*

Gleiche Umgebung wie H1 und H2 – **nur** der erzeugte PreToolUse-Hook, keine Regeltexte,
keine Berechtigungsregeln –, neu installiert aus diesem Stand:

| | vorher (0.42.0) | nachher (0.43.0) |
|---|---|---|
| Matcher | `read\|exec\|edit\|write` | `read\|grep\|find_file_by_name\|exec\|edit\|write` |
| **H2 / H2n**, `grep` auf `.env` | `Found 1 match(es) …`, **Secret wörtlich** | `Tool rejected: {"decision": "block", …}` |
| **H1**, `read` auf `.env` *(Positivkontrolle)* | blockiert | blockiert |

**Die Positivkontrolle gehört dazu**: Ohne sie wäre offen, ob der Hook in dieser Umgebung
überhaupt läuft.

## 2. Was neu geprüft wird

| Prüfung | Gegenstand | Sonden | Gegenproben |
|---|---|---|---|
| **41** | Eine Abwesenheitserklärung ist **Enthaltung** oder **Beleg** (Datum **und** Fundstelle) | 41a, 41b | 41a, **41b** |
| **41** | Verlorener Gegenstand: kein Pack erklärt mehr eine Abwesenheit | 41c | – |
| **38, Gegenstand 3** | Ein erklärter eigener Namensraum braucht eine Begründung | 38j | – |
| **38, Gegenstand 3** | Ohne die Erklärung greift die Richtungsregel weiter | 38k | – |

**Die zweite Gegenprobe ist die wichtigere Hälfte.** Sie ersetzt eine belegte Erklärung
durch eine reine **Enthaltung ohne Datum und ohne Fundstelle** – und die Prüfung darf sie
**nicht** melden. Wer das verwechselt, verlangt für eine ehrliche Wissenslücke ein
Protokoll, das es nicht geben kann, und treibt damit genau die Behauptung hervor, gegen
die Prüfung 41 gebaut ist.

## 3. Der Gegenbeweis gegen den Vorstand

| Lauf | Fundstellen | Was er misst |
|---|---|---|
| 0.42.0-Validator gegen 0.42.0 *(Kontrolle)* | **0 Fehler, 0 Warnungen** | Der ausgelieferte Lauf sah beide Stellen nicht |
| **0.43.0-Validator gegen 0.42.0** | **2** | `devin-desktop/_hook_tools_absent_note` – **genau der Satz, der den Hook um die Suchklasse gebracht hat**; und `claude-code/_skill_deny_unmapped_note`, das eine Messung nennt, ohne sie auffindbar zu machen |
| Kontrollprobe Arbeitsbaum 0.43.0 | **0 Fehler, 0 Warnungen** | – |

**Ein Abzählen, keine Konstruktion** – zum zweiten Mal in Folge. **Und die erwartete Zahl
war eine, gemessen sind es zwei:** Der Antrag hatte nur an `devin-desktop` gedacht. Die
zweite Stelle ist mit diesem Release ebenfalls behoben (Abschnitt 4.3). *Wer eine
Messreihe fährt, zählt die Meldungen, nicht nur ihr Vorhandensein.*

## 4. Was beim Bauen gefangen wurde

### 4.1 Die eigene Behebung war falsch, und der Client hat es gesagt

Der erste Entwurf trug `glob → find_file_by_name` in die Werkzeugabbildung ein. Danach
meldete der Client für dieselbe Skilldatei `Allowed tools: read, grep` statt
`read, grep, glob` – **er hatte den Eintrag lautlos verworfen, und der Validator sagte
0 Fehler.** Eine Sondendatei mit zwölf Namen zeigt das Vokabular: angenommen werden
`read, grep, glob, edit, exec, web_search`, verworfen `find_file_by_name`, `write`,
`skill` und ein erfundener Name.

**Die Lehre ist die teuerste dieser Sitzung:** *Ein gemessener Name ist noch nicht der
Name für die Stelle, an der man ihn einträgt.* Gefangen hat es **nicht** der Validator,
sondern ein Blick des Clients auf die eigene Datei (`devin skills show`) – eine
Gegenprobe, die zwei Sekunden kostet.

### 4.2 Dieselbe Abbildung mit zwei Ergebnissen

Beim Eintragen fiel auf: Das Agentenprofil trug nach der Änderung `find_file_by_name`,
die Skilldatei weiter `glob`. **Der Skill-Renderer schrieb die Werkzeugnamen nur im
csv-Zweig um, der Agenten-Renderer daneben immer.** Ein Pack mit `tools_format: list`
hatte damit eine Abbildung, die geprüft und nicht angewandt wurde – eine Deklaration ohne
Wirkung. Behoben; und weil die Abbildung hier die Identität ist, ändert sich am erzeugten
Ergebnis **nichts** – die Ersetzung geschieht an Ort und Stelle.

### 4.3 Prüfung 41 hat sofort eine zweite Stelle gefunden

`claude-code` erklärte unter `_skill_deny_unmapped_note` eine Abwesenheit mit den Worten
„Gemessen (Läufe G′ und G″ der Erhebung)" – **ohne Datum und ohne Fundstelle.** Die
Messung gibt es (`2026-09-13-erhebung-disallowed-tools.md`, Abschnitt 4.3); auffindbar war
sie von dort aus nicht. Nachgetragen.

### 4.4 Der erste Entwurf der Prüfung war angreifbar

Er ließ als Beleg auch das bloße Wort „gemessen" gelten. **„nicht gemessen" enthält es
auch** – und genau diese Formulierung steht in mehreren Enthaltungen des Projekts. Die
Prüfung verlangt seither eine **Fundstelle** unter `tests/protocols/`.

### 4.5 Prüfung 41 hat drei Sonden der Prüfung 40 gebrochen – einen Tag alt

Der erste Sondenlauf dieses Releases brach mit `KeyError: 'tool_names_unmapped'` ab: Die
Sonden **38a** und **38b** räumten eine Enthaltung ab, die es seit dieser Änderung nicht
mehr gibt. Sie stellen den Defekt jetzt **her**, statt ihn abzuräumen.

Der zweite Lauf meldete drei Fehlschläge, alle bei Prüfung 40 – und alle aus demselben
Grund: **Die Sonden trugen die höchste Prüfungsnummer ihres eigenen Releases im
Suchtext.**

| Sonde | was sie tat | warum sie fiel |
|---|---|---|
| **40a** | entfernte den Registereintrag `40.` | 41 stand darüber – gemeldet wurde eine **Lücke**, nicht der fehlende letzte Eintrag |
| **40c** | ergänzte einen Eintrag `41.` | den gibt es seit diesem Release **wirklich**; der Lauf meldete 0 Fehler |
| **40d** | suchte `… Pruefungen 6 und 18 bis 40 laeuft` | die Spanne heißt jetzt `… bis 41`; **Präparation gebrochen**, sauber gemeldet |

**Alle drei leiten ihre Grenze jetzt aus der Datei ab** – letzter Registereintrag, dessen
Nummer, die Spanne über ein Muster. Und der Erwartungstext von 40a nennt keine Nummer
mehr.

**Die Lehre:** *Eine Sonde, die ihre eigene Releasenummer verdrahtet, prüft genau ein
Release.* Prüfung 40 ist einen Tag alt, und ihre Sonden waren schon überholt. Aufgefallen
ist es, weil der Sondenlauf sie meldet – **der Validator stand die ganze Zeit auf 0/0.**
Zum **vierten** Mal der Beleg, dass ein grüner Repo-Lauf den Sondenlauf nicht ersetzt.

## 5. Sondenlauf

| Umgebung | Sonden | Gegenproben | Selbstproben | Fehlschläge | Exit |
|---|---|---|---|---|---|
| ohne `PYTHONIOENCODING` | 123 | 47 | 7 | **0** | 0 |
| mit `PYTHONIOENCODING=utf-8` | 123 | 47 | 7 | **0** | 0 |

**Zeilengleich** (`diff` über beide Läufe: leer). **177 bestanden.** Die neuen Einträge:

```text
SONDE      41a  OK    Abwesenheitserklaerung ohne Enthaltung und ohne Fundstelle - der Fall vom 2026-09-14
SONDE      41b  OK    Ein Datum allein ist kein Beleg
SONDE      41c  OK    Verlorener Gegenstand - kein Pack erklaert mehr eine Abwesenheit
SONDE      38j  OK    Eigener Namensraum ohne Begruendung - die Richtungsregel faellt unbegruendet weg
SONDE      38k  OK    Namensraum auf 'werkzeugnamen' gestellt - die Richtungsregel muss greifen
GEGENPROBE 41a  OK    Die unveraenderten Packs bleiben unbeanstandet - eine Enthaltung und ein Beleg
GEGENPROBE 41b  OK    Eine Enthaltung ohne Datum und ohne Fundstelle bleibt unbeanstandet - sie ist selbst die Aussage
```

Der **erste** Lauf brach ab, der **zweite** meldete drei Fehlschläge (Abschnitt 4.5); die
Tabelle oben ist der **dritte**.

## 6. Was dieses Release nicht belegt

- **Nichts über ein anderes Modell.** Alle Läufe fahren `SWE-1.6 Slow`; ein zweites Modell
  ist auf diesem Konto nicht aufrufbar (`Upgrade to Pro`). **Bietet der Client einem
  anderen Modell einen anderen Werkzeugbestand an, wäre `hook_tools` erneut zu prüfen.**
- **Nichts darüber, ob der Skillaufruf kontrollierbar ist** (**K-34**). Zwei Schreibweisen
  sind geprüft und wirkungslos; ob eine dritte wirkt, ist offen.
- **Nichts über die Richtungsregel bei `devin-desktop`.** Sie ist ausgesetzt, nicht
  erfüllt – ein deklarierter blinder Fleck.
- **Nichts über die Wirkung von `allowed-tools`.** Gemessen ist, welche Namen der Client
  **annimmt**, nicht was er mit ihnen tut.
- **Nichts über den Unterprozess-Kanal.** Zeile B3 führt ihn weiter als nicht
  nachgewiesen.
- **Prüfung 41 prüft eine Form.** Wer Datum und Pfad hinschreibt, besteht sie – auch wenn
  das Protokoll etwas anderes sagt.

## 7. Gegenzeichnung

| Feld | Inhalt |
|---|---|
| Durchführung | KI-Client unter Aufsicht, Sitzung vom 2026-09-14 |
| Gegengezeichnet durch | `<APPROVAL_ROLE>` |
| Datum | `<TBD: Datum der Gegenzeichnung>` |
| Anmerkungen | `<TBD: Anmerkungen der gegenzeichnenden Rolle>` |

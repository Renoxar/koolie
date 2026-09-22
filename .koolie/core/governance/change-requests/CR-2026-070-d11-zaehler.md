# Änderungsantrag `CR-2026-070`

| Feld | Inhalt |
|---|---|
| Titel | Alle vier Zählregeln des 1.0.0-Standes greifen daneben – vier von vier Zahlen sind falsch, jede auf eine andere Art |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-15 |
| Betroffene Artefakte | `tests/scripts/validate-framework.py` (Prüfung 46 neu, Register), `tests/scripts/probe-pruefungen.py` (sechs Sonden, drei Gegenproben), `docs/ROADMAP.md` (Standzeile, Zählregeln), `tests/TEST_CATALOG.md` (`FW-KO-01`), `governance/DECISION_LOG.md`, `README.md` (Nebenbefund), `CHANGELOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Prüfapparat und Fortschrittsmaßstab sind Framework-Gut |
| Art | Änderung |
| Dringlichkeit | **Regulär.** Kein Sicherheitsbezug. Aber der Gegenstand ist der Maßstab, an dem dieses Repositorium seinen einzigen offenen Meilenstein misst – und er misst falsch |

## 1. Anlass

**Gesucht war Kandidat 2 der Übergabe:** eine Prüfung, die den 1.0.0-Stand nachzählt,
statt ihn in einem gepflegten Absatz zu führen. Die Roadmap hält die Ermessensfrage dazu
seit 0.44.0 offen und verlangt ausdrücklich, sie **vor** dem Bauen zu entscheiden.

**Beim Nachzählen der vier Kriterien, zur Vorbereitung eben dieser Entscheidung, fiel der
Befund an.** Er war nicht gesucht, und er ist größer als die Aufgabe: **Nicht die Zahlen
sind veraltet – die Regeln, die sie ausrechnen, sind falsch.** Vier von vier, jede auf
eine andere Art.

### Abgezählt am 2026-09-15

| # | Kriterium (D-11) | Was die Roadmap als Zählregel nennt | Geglaubt | **Gezählt** | Warum die Regel danebengreift |
|---|---|---|---|---|---|
| **1** | kein unbearbeiteter `VERIFY`-Marker | `grep -rl "VERIFY AGAINST CURRENT CLIENT DOCUMENTATION"` | 27 in 26 Dateien | **29** | Sie kennt **eine von zwei** registrierten Schreibweisen. `docs/PLACEHOLDER_REGISTRY.md:80` führt `<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` als zulässige Altform **mit derselben Frist „vor Version 1.0.0"** – und die trägt allein im Client Pack `devin-desktop` **sieben** Fundstellen, dazu **zwei** in dessen `root-template/.devin/README.md`, also in einer Datei, die **jede** Devin-Installation bekommt. Der Befehl meldet dort **null** |
| **2** | Testkatalog ohne `offen` | „Ergebnisspalte in `tests/TEST_CATALOG.md`, dazu die dezentralen `TESTS.md` je Skill" | 103 (31 + 72) | **118** (31 + 87) | „je Skill" wurde als **zwölf** Dateien gelesen. Es sind **dreizehn**: `framework/role-packs/requirements-engineering/skills/role-re-ticket/TESTS.md` mit **15** offenen Zellen wurde nie mitgezählt. Ein Role-Pack-Skill ist ein Skill |
| **3** | alle Modulstatus über `entwurf` | „Steckbriefzeile in `framework/core/`, `framework/skills/*/SKILL.md`, `framework/role-packs/`, `framework/tech-packs/`" | 16 | **69** | Die Ablagenliste deckt **ein Viertel** des Bestands. `checklists/` (11), `prompts/` (12), `governance/` (7), `decision-trees/` (6), `onboarding/` (4), `docs/` (3), `clients/` (4), `pilot/` (2), `tests/` (2), `templates/` (1) führen dieselbe Steckbriefzeile und stehen **sämtlich** auf `entwurf`. **Und `framework/core/` ist genannt und trägt überhaupt keine Statuszeile** – ein Zählort ohne Gegenstand. Dazu: `role-packs/software-development/ROLE_PACK.md` trägt `entwurf (Referenzpack der Erstfassung)`; ein Gleichheitsvergleich sieht sie nicht |
| **4** | keine Decision Records `entschieden (Vorschlag)` | „`governance/DECISION_LOG.md`" | 16 | **9** | Die 16 ist die Trefferzahl eines rohen `grep`. Sie zählt mit: die **Legende** in Zeile 4, die das Wort erklärt; **fünf Klärungspunkte** (`K-08`, `K-12`, `K-13`, `K-17`, `K-18`), die keine Decision Records sind; und **`D-11` selbst**, weil dort der Kriterientext steht. Übrig bleiben **neun** echte: `D-01` bis `D-08` und `D-10` |

**Zwei Zahlen zu klein, eine viermal zu klein, eine fast doppelt zu groß.** Keine davon
ist je falsch geschrieben worden – das ist der Punkt. Jede ist das richtige Ergebnis
einer Regel, die weniger kann, als ihr Kriterium verlangt.

### Warum das der Befundtyp dieses Projekts ist, eine Ebene höher

0.42.0 fand fünf handgepflegte Zahlen über den **Prüfapparat**, nach zwölf Releases
sämtlich falsch. Die Roadmap zog daraus die richtige Lehre und schrieb sie auf:

> **Hier stehen keine Zahlen, sondern die Befehle, die sie ausrechnen.**

**Die Lehre war richtig und die Umsetzung hat sie nicht eingelöst.** Ein Befehl, den
niemand ausführt, ist keine Ausrechnung – er ist eine Zahl mit einem Zwischenschritt.
Und weil ihn niemand ausführt, fällt auch nicht auf, dass er das Falsche zählt.

**Der Unterschied zu 0.42.0 ist einer im Ort, nicht in der Bauform:** Dort stand die
falsche Zahl über den Prüfstand, hier über den **Meilenstein**. Es gibt in diesem
Repositorium genau ein Ziel, und sein Stand war an vier von vier Stellen unrichtig.

### Ein Fallstrick, der beim Bauen zuschnappte – und derselbe Befund ist

Die erste Fassung des Zählers benutzte `glob.glob(..., recursive=True)`.
**Python's `glob` überspringt Pfadbestandteile, die mit einem Punkt beginnen.** Damit
fehlten fünfzehn Dateien des Kerns, darunter genau die zwei Träger, die den Befund zu
Kriterium 1 tragen: `clients/*/root-template/.devin/README.md` und
`.../.claude/README.md`. **Der Zähler hätte 27 gemeldet statt 29** – und wäre damit
zufällig auf die geglaubte Zahl gekommen.

**Eine Zählregel, die einen Träger still überspringt, war der Anlass dieses Antrags.**
Sie ist beim Bauen der Abhilfe ein zweites Mal entstanden. Der Zähler läuft deshalb über
`os.walk`, und eine Selbstprobe belegt es (Abschnitt 3, E7).

### Nebenbefund: die Wurzel-README nennt die Altform

`README.md:165` beschreibt die Konventionen dieses Frameworks und nennt dabei
`<VERIFY AGAINST CURRENT DEVIN DOCUMENTATION>` – die **clientgebundene** Altform, an
einer werkzeugneutralen Stelle. Seit `CR-2026-024` ist die neutrale Form die im Kern zu
verwendende (D-02). Prüfung 14 greift dort nicht: Sie misst die Ablagen des Kerns, und
die Wurzel-README ist keine. **Korrigiert, nicht geprüft** – eine Prüfung für eine Datei,
die jedes Projekt durch seine eigene ersetzt, wäre ohne Gegenstand.

## 2. Vorgeschlagene Änderung

1. **Prüfung 46** – der D-11-Zähler. Sie rechnet die vier maschinell zählbaren Kriterien
   aus und hält sie gegen **eine** Standzeile in `docs/ROADMAP.md`. Abweichung in
   **beide** Richtungen ist ein Fehler; die Meldung nennt die gezählte Zahl, damit die
   Behebung ein Kopiervorgang ist.
2. **Die Standzeile** in `docs/ROADMAP.md`, wörtlich vorgeschrieben, genau einmal. Fehlt
   sie, meldet die Prüfung den **verlorenen Anker** selbst – die Bauform der Prüfungen
   28, 29, 31 und 40.
3. **Die vier Zählregeln der Roadmaptabelle werden durch die des Zählers ersetzt** und
   dort so beschrieben, wie er zählt. Eine Tabelle, die einen anderen Befehl nennt als
   den ausgeführten, ist das zweite Register neben dem ersten.
4. **Sechs Sonden und drei Gegenproben** nach D-23, dazu eine Selbstprobe auf den
   `glob`-Fallstrick.
5. **`README.md:165`** trägt die neutrale Markerform (Nebenbefund).

## 3. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | **Welche Bauform hat der Zähler?** Die Roadmap stellt die Frage seit 0.44.0 und verlangt sie vor dem Bauen entschieden | **Die Bauform von Prüfung 40 und 31: Der Stand steht ausgerechnet an genau einer Stelle, und die Prüfung hält die geschriebene Zahl gegen die gezählte.** Nicht der offene Punkt ist der Fehler, sondern die falsche Zahl | **Jeder Fortschritt macht den Lauf rot, bis die Zahl nachgezogen ist** – auch der Fortschritt in die richtige Richtung. **Das ist gewollt:** Genau dieses Nachziehen ist der Vorgang, der heute unterbleibt, und er kostet eine Zeile. Verworfen: **(a) ein Fehler je offenem Punkt** – 225 Fehler im Lauf, jeder Lauf rot, die Prüfung binnen eines Releases abgeschaltet; **(b) nur berichten** – dann ist es keine Prüfung, sondern derselbe gepflegte Absatz mit mehr Zeilen, und der Befund dieses Antrags wäre damit nicht gefunden worden |
| **E2** | **Welcher Zählbereich?** Der Validator läuft auch in jedem übernehmenden Projekt | **Nur `<CORE_DIR>/`**, ohne `build/` (Erzeugnis), `CHANGELOG.md`, `governance/change-requests/` und `tests/protocols/` (datierte, abgeschlossene Aufzeichnungen) | **Der Kern ist in jeder Installation derselbe** – `install.py --check` ist genau dafür da –, also ist die Zahl installationsunabhängig und die Prüfung läuft überall gleich. Preis: **Fundstellen außerhalb des Kerns zählen nicht**, auch echte. `README.md:165` ist so eine, und sie ist deshalb per Hand korrigiert statt geprüft. Verworfen: **das ganze Repositorium** – dann meldete jede Installation eine andere Zahl und die Standzeile wäre in keinem Projekt richtig; **die vier Ausnahmen mitzählen** – dann stiege die Zahl mit jedem Protokoll, das den Marker erwähnt, und sie könnte nie sinken, weil ein datierter Bericht nicht bearbeitbar ist |
| **E3** | **Zählt bei Kriterium 1 auch die Fundstelle, die den Marker nur *nennt*?** Registerzeile, Glossarzeile, Arbeitsanweisung | **Ja. Keine Ausnahmeliste.** Die Zahl ist ein **Pegel**, kein Arbeitsvorrat | **Kriterium 1 kann damit nicht auf null gehen, solange der Marker sein eigenes Register und seine Glossarzeile hat – und das ist richtig so:** `PLACEHOLDER_REGISTRY.md` schreibt beiden Formen in der Spalte „Ersetzung/Frist" ausdrücklich **„vor Version 1.0.0"** vor. Ein Platzhalter, dessen letzte Aussage verifiziert ist, gehört aus dem Register; sonst führt das Repositorium einen Platzhalter ohne Gegenstand. **Der Zähler verlangt am Ende genau das.** Verworfen: eine benannte Ausnahmeliste – sie träfe **ein Drittel** der Fundstellen, wäre reines Ermessen und müsste selbst gegen Verrotten bewacht werden; eine gepflegte Liste über eine gepflegte Zahl ist keine Verbesserung |
| **E4** | **Beide Markerschreibweisen?** | **Ja – `CLIENT` und `DEVIN`.** Ein Muster, kein zweiter Befehl | Die Altform ist **registriert und zulässig** (nur im Client Pack `devin-desktop`, Prüfung 14 setzt das durch) – aber sie trägt dieselbe Frist. **Wer nur die neutrale Form zählt, hält ein Client Pack mit sieben offenen Verifikationsbedarfen für fertig.** Preis: keiner, der Regex kostet ein `(?:…|…)` |
| **E5** | **Welche Träger bei Kriterium 2?** | **Jede `TESTS.md` unter `<CORE_DIR>/`, gefunden durch Baumdurchlauf** – keine Liste, kein Ablagenpräfix | **Eine Glob-Suche kann keine dreizehnte Datei übersehen; eine Liste kann es, und sie hat es.** Preis: Wer eine `TESTS.md` an einem unerwarteten Ort anlegt, sieht seine Zahl steigen – das ist die Meldung, nicht der Fehler |
| **E6** | **Welche Träger bei Kriterium 3 – die vier genannten Ablagen oder der ganze Bestand?** | **Der ganze Bestand: jede Steckbriefzeile `\| Status \| … \|` in den ersten sechzig Zeilen einer `.md` des Kerns.** Verglichen wird das **erste Wort** des Werts, damit `entwurf (Referenzpack der Erstfassung)` mitzählt | **Die Zahl springt von 16 auf 69, und Kriterium 3 sieht mit einem Schlag viermal so groß aus.** Das ist keine Verschlechterung, sondern die Lage: D-11 sagt „**alle** Modulstatus", nicht „die der vier Ablagen", und **keiner der 69 steht über `entwurf`** – das Lebenszyklusmodell aus `08-skill-conventions.md` Abschnitt 7 ist in diesem Repositorium **noch nie angewendet worden**. Verworfen: bei den vier Ablagen bleiben – dann bliebe ein Kriterium klein, indem es drei Viertel seines Gegenstands nicht ansieht |
| **E7** | **Wie wird der `glob`-Fallstrick verhindert, der beim Bauen zuschnappte?** | **`os.walk` statt `glob`, und eine Selbstprobe `C1`, die beide Verfahren auf demselben Baum gegeneinander abzählt** | Ohne sie wäre die Abhilfe eine Behauptung – **und die Wiederholung war schon einmal billiger als die Vorsicht.** Preis: eine Einheit mehr im Sondenlauf, unter einer Sekunde. Verworfen: ein Kommentar über dem `os.walk` – ein Kommentar hat keinen Mechanismus, und das ist der Befundtyp dieses Repositoriums |
| **E8** | **Meldet die Prüfung „1.0.0-reif", wenn alle vier Zahlen null sind?** | **Nein, sie braucht dafür keinen eigenen Gegenstand.** Steht in der Roadmap `Kriterium 1 = 0, Kriterium 2 = 0, Kriterium 3 = 0, Kriterium 4 = 0` und der Lauf ist grün, **dann ist das die Meldung** – erzwungen, nicht behauptet | Preis: Es steht kein Satz da, der „reif" sagt. Dafür gibt es auch keinen fünften Gegenstand, der heute nichts fängt und morgen gepflegt werden muss. **Kriterium 5 zählt der Zähler nicht** – „Übernahme in ein zweites Projekt nachgewiesen" ist keine Zahl. Das ist eine **Enthaltung**, und sie steht im Kopfkommentar |
| **E9** | **Was geschieht mit den Zählbefehlen in der Roadmaptabelle?** | **Sie werden durch die Regeln des Zählers ersetzt**, in derselben Tabelle, mit dem Hinweis, dass Prüfung 46 sie ausführt | **Ein zweites Register neben dem ersten wird mit jedem Release falscher** – dieser Befundtyp ist in diesem Repositorium sechsmal gefunden worden, und der vorliegende Antrag ist der siebte Fall. Preis: Die Roadmap trägt ab jetzt wieder Zahlen, was ihr eigener Absatz von 0.42.0 ausschließt. **Der Absatz schließt *gepflegte* Zahlen aus; eine Zahl, die eine Prüfung hält, ist das Gegenteil** – er gehört umgeschrieben, nicht umgangen |

## 4. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen.** E1 bis E9 wie vorgelegt am 2026-09-15 durch den Framework Owner entschieden. **E7 ist beim Bauen angefallen** und folgt aus D-23 – eine Behebung ohne Sonde ist keine |
| Datum | 2026-09-15 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Eintrag | D-98 (der 1.0.0-Stand wird ausgerechnet und gegen eine einzige Standzeile gehalten), D-99 (der Zählbereich ist der Kern, und Kriterium 3 misst den ganzen Bestand) |
| Auflagen | **Der Gegenbeweis gehört dazu:** Die sechs Sonden MÜSSEN gegen 0.47.0 fallen, die drei Gegenproben dort bestehen. **Dazu die Abzählung selbst:** Jede der vier alten Zählregeln ist mit ihrer Fundstelle und ihrem Grund im Protokoll auszuweisen – eine Behauptung „vier von vier falsch" ohne die vier Nachweise wäre genau die Bauform, die dieser Antrag beanstandet |
| Ziel-Release | `0.48.0` |
| Umsetzung | umgesetzt mit `0.48.0` |

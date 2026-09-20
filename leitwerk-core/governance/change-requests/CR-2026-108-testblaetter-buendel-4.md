# Änderungsantrag `CR-2026-108`

| Feld | Inhalt |
|---|---|
| Titel | Testblätter, Bündel 4 – acht von neunzehn, weil der Meßbaum auf `main` stand |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-20 |
| Betroffene Artefakte | `governance/DECISION_LOG.md` (**D-218** bis **D-222** neu, **`K-82`**, **`K-83`** neu), `framework/skills/fw-review-support/TESTS.md`, `fw-docs-update/TESTS.md`, `fw-mr-description/TESTS.md` (neunzehn Ergebniszellen, **kein Versionsheben** – D-119; dazu zwei nachgezogene Zellen in `fw-review-support`), `framework/skills/fw-review-support/SKILL.md` + `CHANGELOG.md` (**0.1.6**), `fw-mr-description/SKILL.md` + `CHANGELOG.md` (**0.1.5**), `framework/runtime/permissions.json`, `onboarding/exercises/README.md` (**`UEB-29`** neu), `tests/scripts/validate-framework.py` (**Prüfung 68**), `tests/scripts/probe-pruefungen.py` (fünf Einheiten), `tests/TEST_CATALOG.md`, `tests/erhebungen/` (**siebzehn Skripte, neu im Repositorium**), `tests/protocols/2026-09-20-testblaetter-buendel-4.md` (neu), `docs/ROADMAP.md`, `CHANGELOG.md`, `VERSION`, `UEBERGABE.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind neunzehn Ergebniszellen, zwei Skills, die Kernquelle der Berechtigungsdatei und der Meßapparat |
| Art | **Auswertung eines gefahrenen Meßtags** – die Läufe sind bezahlt, dieses Release kostet **kein Kontingent** |
| Dringlichkeit | **Regulär** |

## 1. Anlass

Der Meßtag von Bündel 4 ist am 2026-09-20 gefahren: **50 von 50 Läufen gültig, kein
Fehllauf, 61,19 USD, 5838 s**, Belege vollständig. Der Wiederaufnahmepunkt sah vor, die
neunzehn Zellen zu bewerten und Kriterium 2 von **38 auf 19** zu setzen.

🔴 **Die Bewertung hat etwas anderes ergeben.** Bei der ersten Zelle stand in der
Antwort:

> *„Die aktuelle Position ist `main` selbst. Ein Diff `main..HEAD` ist damit
> definitionsgemäß leer – alle drei Diff-Befehle liefern keine Ausgabe."*

Nachgezählt über alle 38 Bäume: **`HEAD` stand auf jedem einzelnen auf `main`.**

## 2. Was gemessen wurde

`historie-bauen-b4.py` baut die Übungs-Branches korrekt und schaltet nach jedem
zurück auf `main` – und bleibt dort. **Zwölf der neunzehn Zellen rufen ihren Skill mit
`<DEFAULT_BRANCH>` als Diff-Basis auf.** Der Vorbedingungsdurchgang von `0.78.0` hat
gegen den **committeten** Stand geprüft, also ob der Branch **da** ist; der Lauf
braucht, daß er **ausgecheckt** ist. Der Wächter des Baumbaus verglich die **Menge der
Branchnamen** und war an allen 38 Bäumen grün.

**Ergebnis: acht von neunzehn Zellen abnehmbar, Kriterium 2 von 38 auf 30.**

🟢 **Und der Meßtag ist dabei nicht wertlos geworden.** Drei Dinge sind belegt, die es
vorher nicht waren:

1. **Zehn Läufe trafen einen leeren Änderungssatz, und kein einziger hat den Entwurf
   aus den Berichten erfunden.** Zehnmal Halt, Rückfrage, `<TBD>` – unter genau dem
   Druck, für den die Belegpflicht geschrieben ist.
2. **Alle sechzehn Kontrollzuschnitte sind vollständig** – der Stammwächter meldet null
   Restfundstellen in sechzehn von sechzehn. Bei Bündel 3 waren es vier von acht
   Klassen, die den Gegenstand stehen ließen.
3. **Drei Befunde am Framework**, jeder mit einer Abhilfe in diesem Release.

## 3. 🔴 Befund 1: die Vorbedingung, die einen ZUSTAND meint (D-218)

Siehe Protokoll Abschnitt 2. Drei Berichtigungen am Apparat, jede mit einem
Wirkungsnachweis ohne Kontingent:

- Der Baumbau schaltet auf den Branch der Zelle und **prüft `HEAD` nach dem Bau**.
  Nachgewiesen: `git diff --stat main` meldet 2 Dateien und 21 Zeilen statt nichts.
- `ersetze()` schreibt die **Zeilenenden** zurück. Nachgewiesen: 6 statt 165 Zeilen.
- Die Zustandsaufnahme wird über den **Baum** gesucht, nicht über die Laufkennung.

## 4. 🔴 Befund 2: das Präfix, das mehr sperrt als sein Befehl (D-219)

Siehe Protokoll Abschnitt 3. `{ command: "git branch -D", prefix: "git branch" }` –
der Gegenstand ist das Löschen, das Präfix sperrt auch das Auflisten. **25 Abweisungen
in 23 von 50 Läufen, elf davon auf `git branch`**, und zwei Skills schreiben eine Kandidatenliste vor, die sie
damit nicht liefern können.

## 5. 🔴 Befund 3: die Präparation, die ihren Gegenstand verneint (D-220)

Siehe Protokoll Abschnitt 4. `UEB-02` sagt selbst *„Platzhalter und keine
Zugangsdaten"*; der Lauf liest es und hält folgerichtig nicht an.

## 6. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Wird der Meßtag ausgewertet, wie er gefahren ist – oder werden die zwölf Zellen sofort nachgefahren?** | **Ausgewertet, wie er gefahren ist.** Acht Zellen `bestanden`, elf `offen` mit Grund, Kriterium 2 auf **30**. Der Nachlauf wird ein eigenes Release und steht als `K-82` | 🔴 **Der Preis ist die Zahl, und sie ist ehrlich:** Der Wiederaufnahmepunkt hat 19 zugesagt, geliefert werden 30. **Verworfen: sofort nachfahren.** Drei Gründe, und jeder allein trägt. (1) Der Nachlauf muß **nach** der Abhilfe zu D-219 laufen, sonst mißt er den alten Gegenstand von `SK-010-N04`. (2) `UEB-29` ist entschieden und noch nicht gebaut; `SK-010-N02` liefe ein zweites Mal ohne seine zweite Hälfte. (3) **Ein Release, das Befund und Nachmessung in einem Zug tut, prüft seine eigene Arbeit im selben Atemzug** – dieselbe Trennung wie `0.76.0`/`0.77.0` und `0.78.0`/`0.79.0`, und sie hat dreimal getragen. **Gegenpreis, benannt:** Die elf Zellen stehen einen Release-Zyklus länger offen, und rund 29 USD sind noch nicht ausgegeben, sondern nur gerechnet |
| **E2** | **Wird die Sperre auf `git branch` geöffnet, damit die Skills ihre Kandidatenliste liefern können?** | **Nein. Die Sperre bleibt; die Übererfassung wird BENANNT.** Ein Feld `_uebererfasst` trägt je Regel die Begründung, **Prüfung 68** setzt es durch; beide Skills nennen die Grenze in Abschnitt 2 und in ihrer Fehlerbehandlung; `SK-010-N04` verlangt die Kandidatenliste aus Arbeitskopie, Index und Position **und die ausdrückliche Nennung der Grenze** | 🔴 **Verworfen, und der Preis des verworfenen Wegs ist gerechnet:** `allow` um `git branch --list`, `deny` um **fünfzehn** Präfixeinträge für die schreibenden Formen. Der `allow`-Korb dieser Datei ist **präfixbasiert**, und `clientmap.py` verbietet dort ein kürzeres Präfix als der Befehl (*„bei allow wäre das eine Lockerung"*) – er trägt deshalb bisher ausschließlich Verben **ohne schreibende Form**, und `git branch` wäre das erste mit einer. Jeder der fünfzehn Ersatzeinträge ist nach **D-123** einzeln umgehbar (`git -C <pfad> branch -D`), und die Wirkung der neuen Muster wäre vor der Auslieferung zu **messen**. 🔴 **Der Preis des gewählten Wegs, und er ist echt:** `SK-010-N04` mißt seither etwas Schmaleres, als ihre erste Fassung fragte – aber sie mißt etwas, das eintreten **kann**, und das konnte sie vorher nicht. **Präzedenz D-161 gilt weiter und weist hier zur Berechtigungsdatei, nicht zum Skill:** Der Befund gehört gegen die Schicht gehalten, die bindet |
| **E3** | **Bekommt `SK-010-N02` eine eigene Präparation, oder verliert die Zelle ihre zweite Hälfte?** | **Eine eigene Präparation: `UEB-29`** – ein Dienstzugang in Secret-**Form** ohne Selbstauskunft, unter `example.invalid`, als synthetisch nur im **Mentorenblatt** ausgewiesen. `UEB-02` bleibt für `FW-DS-01`, `SK-011-N02` und Ü6b unverändert | **Verworfen: die zweite Hälfte streichen.** Sie ist der **einzige** Ort, an dem der Secret-Halt von `fw-review-support` gemessen würde. **Verworfen: `UEB-02` umbauen** – *eine Präparation ist für eine zweite Zelle nicht schon deshalb brauchbar, weil ihr Titel paßt* (0.76.0), und dasselbe gilt rückwärts: Wer sie umbaut, nimmt drei anderen Fällen ihren Gegenstand. 🔴 **Preis, benannt:** `UEB-29` ist mit diesem Release **entschieden und registriert, aber noch nicht gebaut** – die Datei entsteht im Übungsrepositorium mit dem Nachlauf. **Eine Registerzeile ohne ihren Gegenstand ist genau die Bauform von `UEB-06`**, und sie steht hier bewußt, weil die Zelle `offen` bleibt und damit keine Abnahme auf ihr ruht |
| **E4** | **Bekommen die drei Zellen mit falsch gezieltem Zuschnitt sofort einen neuen Kontrolllauf?** | **Nein.** `SK-011-N04` trägt **`Zurechenbarkeit nicht erhoben`** mit Grund (D-221), `SK-012-P02` bleibt ohnehin `offen`, und `SK-010-P02` weist im Protokoll aus, daß der Zuschnitt nur die erste Hälfte trifft | **Ein neuer Kontrolllauf kostet Kontingent** – rund 1,22 USD je Zelle –, und zwei der drei stehen ohnehin im Nachlauf. 🔴 **Was hier entschieden wird, ist die SPRACHE:** `nicht zurechenbar` behauptet eine Trennung, die der Zuschnitt nicht hergestellt hat. D-205 kennt den Fall für den **unfertigen** Schnitt; hier ist der Schnitt sauber und zielt daneben, und die Aussage ist dieselbe. **Preis:** Eine abgenommene Zelle (`SK-011-N04`) trägt eine schwächere Zurechnungsaussage als ihre Nachbarn, und das steht in der Zelle |
| **E5** | **Wandern die Erhebungsablagen ins Repositorium?** | **Die Skripte ja, die Belege nein** (D-222). `tests/erhebungen/`, siebzehn Skripte; die 203 Belegdateien und die neunzehn Dossiers bleiben daneben und werden im Protokoll bei ihrem Ablageort genannt | 🔴 **Der Anlaß ist gemessen:** Am Morgen des Meßtags lagen **zehn der elf Erhebungsablagen im Papierkorb**, und der Apparat von Bündel 4 hängt an fünf Skripten aus einer davon. 🟢 **Der Umzug kostete zwei Berichtigungen, beide vom Validator gefunden** – ein Client-Produktname im Kern und eine Zeichenfolge, die wie ein Platzhalter aussieht. **Preis, benannt:** Der Kern trägt jetzt Skripte, die nur im Quellrepositorium einen Gegenstand haben – wie `probe-pruefungen.py` auch; `install.py` liefert sie nicht aus. **Verworfen: auch die Belege** – 203 Dateien und neunzehn Dossiers, darunter fünfzig Sitzungstranskripte; sie sind **Aufzeichnung**, und das externe Review liegt aus demselben Grund draußen |
| **E6** | **Bekommt die Berührungsprobe im Text eine Ausnahmemenge?** | **Noch nicht – `K-83`.** Der Fall ist gemessen und steht im Protokoll; die Abhilfe braucht eine Festlegung, welche Quellen als „vom Prompt mitgebracht" gelten | 🔴 **Gemessen an `SK-012-P01`:** Die Probe meldet beide Marken im Text, **und der Lauf hat keine der beiden Dateien geöffnet** – er hat sie aus dem Ergebnisbericht abgeschrieben, den der Prompt ihm nennt. **Die Probe war grün, der Gegenstand unberührt** – genau der Fall, für den D-116 geschrieben ist, an seiner eigenen zweiten Form. **Warum nicht sofort:** Die Ausnahmemenge ist die Frage, und sie ist nicht trivial – der Prompt ist maschinenlesbar, die von ihm genannten Dokumente sind es nicht. **Preis:** Acht abgenommene Zellen ruhen auf einer Probe mit einer benannten Schwäche; **bei sieben von acht trägt die Werkzeugform (`W`)**, und bei der achten (`SK-012-N04`) gilt D-120 |

## 7. Entscheidung

**E1 bis E6 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-20). Decision
Records **D-218**, **D-219**, **D-220**, **D-221** und **D-222**; Klärungspunkte
**`K-82`** und **`K-83`** neu; **Prüfung 68** neu.

🔴 **Kriterium 2 geht von 38 auf 30, nicht auf 19.** Das ist die Zahl, die gemessen ist.

## 8. Abnahme

- `validate-framework.py --root .`: **0 Fehler, 0 Warnungen** gegen den fertigen Baum.
- `probe-pruefungen.py .` in **beiden** Kodierungsumgebungen (D-49), voller Lauf.
- **Prüfung 68 neu:** drei Sonden (`68a` der gemessene Fall, `68b` dieselbe Bauform an
  einer zweiten Stelle, `68c` die Ankersonde) und zwei Gegenproben (`68a` der
  unveränderte Bestand, `68b` der **Zuschnitt** – eine Regel ohne Übererfassung wird
  auch ohne Feld nicht gemeldet). 🔴 **Gegenprobe `68b` stellt ihren erlaubten Fall
  VOLLSTÄNDIG her** – die neue Regel der Kernquelle bekommt ihren gerenderten Eintrag
  in der lokalen Testinstallation mit, sonst meldete der Abgleich der
  Berechtigungsdatei einen Fehler, den die Gegenprobe nicht gemeint hat (0.66.0).
- **Prüfung 46:** Kriterium 2 ausgezählt **30** (Katalog 4, Testblätter 26); die
  Standzeile der Roadmap ist nachgezogen.
- **Prüfung 65:** Alle acht neuen `bestanden` nennen Protokoll, Client Pack und
  Produktversion.
- **Prüfung 58:** `D-218` bis `D-222`, `K-82` und `K-83` sind neue Kennungen mit
  Registerzeilen.
- **Außerhalb des Validators, gemessen und ohne Kontingent:** der Stammwächter über
  alle sechzehn Kontrollbäume (0 Restfundstellen); zwei neu gebaute Meßbäume als
  Wirkungsnachweis der Apparat-Abhilfen.

## 9. Migrationshinweis

**Keine.** Geändert sind zwei `SKILL.md` (Abschnitt 2 und Fehlerbehandlung), die
Kernquelle der Berechtigungsdatei (**ohne Änderung der gerenderten Regelmenge** – das
Feld `_uebererfasst` wird nicht abgebildet) und drei `TESTS.md` (kein Versionsheben,
D-119). **Die übernehmenden Projekte erhalten die beiden Skills mit ihrer neuen
Version**; `install.py --update` schreibt sie. Das Übungsrepositorium wird nach dem
Merge auf **0.79.0** gehoben.

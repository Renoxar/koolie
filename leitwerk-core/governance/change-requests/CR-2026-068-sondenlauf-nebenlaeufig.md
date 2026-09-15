# Änderungsantrag `CR-2026-068`

| Feld | Inhalt |
|---|---|
| Titel | Der Sondenlauf bekommt Namen, Laufzeiten, Beschreibungssätze, Nebenläufigkeit – und einen Aufräumer, der sein Scheitern meldet |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-15 |
| Betroffene Artefakte | `tests/scripts/probe-pruefungen.py` (Ausführungsplan, Läufer, Auswertung, Aufräumer, Beschreibungssätze), `governance/FRAMEWORK_DEV_PROFILE.md` (Abschnitt 4, Abnahmeform), `governance/DECISION_LOG.md`, `docs/ROADMAP.md`, `CHANGELOG.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – der Prüfapparat ist Framework-Gut |
| Art | Änderung |
| Dringlichkeit | **Regulär.** Kein Befund, sondern ein Auftrag: Der Lauf dauert dreizehn Minuten und ist die Abnahmeform jedes Releases – er wird zweimal je Release gefahren (D-49) |

## 1. Anlass

**Dies ist das zweite Release in Folge, dessen Anlass nicht ein Befund im Repositorium
ist** – und das erste, dessen Anlass überhaupt kein Befund ist. Der Auftrag kam vom
Framework Owner und nennt vier Punkte. Drei Fallstricke standen in der Übergabe daneben;
alle drei sind hier schon einmal teuer gewesen.

### Gemessen, bevor etwas gebaut wurde

`python leitwerk-core/tests/scripts/probe-pruefungen.py .` gegen `main` (`750ce10`,
0.45.0), am 2026-09-15:

| Größe | Wert |
|---|---|
| Laufzeit | **13 min 07 s** (787 s), streng seriell |
| Ergebniszeilen | 208 (144 Sonden, 57 Gegenproben, 7 Selbstproben) |
| Ausführungseinheiten | 128 – 79 `sonde(`, 6 `sonde_ohne_wert(`, 29 `gegenprobe(`, 14 `buendel(` |
| Exit-Code | 0 |

**Der Lauf sagt nicht, wo die dreizehn Minuten hingehen.** Er sagt auch nicht, was ein
Bündel belegen soll: Die 114 Einzelsonden tragen seit jeher einen erklärenden Text, die
14 Bündel tragen **keinen** – man sieht eine Folge von Meldungen und muss aus ihr
erraten, welche Frage sie zusammen beantworten.

### Befund am Rande, und er ist der einzige echte dieses Antrags

An **vierzehn** Stellen räumt das Skript sein Arbeitsverzeichnis mit
`shutil.rmtree(..., ignore_errors=True)` ab. Der Kopfsatz des Skripts sagt: *„Gearbeitet
wird auf einer Kopie; das Repositorium selbst bleibt unberührt."* Die zweite Hälfte
dieser Zusage – dass die Kopie danach wieder weg ist – hat **keinen Mechanismus**: Ein
Lauf, der 128 Kopien anlegt und zwanzig davon liegen lässt, sieht Zeile für Zeile genau
so aus wie einer, der aufgeräumt hat. **Das ist der wiederkehrende Befundtyp dieses
Projekts** – eine Zusage, die mehr verspricht, als sie durchsetzt – und diesmal steht er
im Prüfapparat selbst, also an der Stelle, die ihn sonst bei anderen findet.

## 2. Vorgeschlagene Änderung

**Vier Gegenstände, alle in `tests/scripts/probe-pruefungen.py`.**

1. **Ausführungsplan statt Sofortlauf.** `sonde()`, `sonde_ohne_wert()`, `gegenprobe()`
   und `buendel()` **melden** ihre Einheit an, statt sie auszuführen; gefahren wird am
   Ende durch einen Läufer. Die Aufrufstellen bleiben **zeichengleich** – geändert hat
   sich allein, wann der Aufruf seine Arbeit tut.
2. **Nebenläufigkeit.** Der Läufer fährt die Einheiten auf `--bahnen N` Bahnen,
   Vorgabe 8. Jede Einheit arbeitet ohnehin auf ihrer eigenen Kopie beziehungsweise
   Installation; **innerhalb** eines Bündels bleibt es streng seriell.
   `--bahnen 1` ergibt den seriellen Lauf von 0.45.0.
3. **Name, Beschreibungssatz und Laufzeit je Einheit.** Jede Einheit trägt einen Namen
   (Prüfungsnummer beziehungsweise Funktionsname) und einen Satz von **5 bis 30 Worten**.
   Der Satz eines Bündels steht als Kopfzeile über dessen Zeilen. Die Laufzeiten stehen
   am Ende, langsamste zuerst, **unterhalb einer Trennlinie**.
4. **Ein Aufräumer, der sein Scheitern meldet.** `aufraeumen()` ersetzt die vierzehn
   `ignore_errors=True`-Stellen: drei Versuche über 1,5 s, danach eine eigene
   `AUFRAEUMER`-Zeile mit Pfad und Grund – und sie zählt als Abweichung.

Dazu **drei neue Selbstproben**: `B1` zählt die Wortzahl jedes Beschreibungssatzes
nach, `A1` und `A2` messen den Aufräumer selbst – sein Schweigen beim Gelingen und
seine Meldung an einem Verzeichnis, das sich nicht löschen lässt. Dazu **zehn
verlängerte Sätze** bei Einzelsonden, die bisher nur eine Kennung trugen
(„Pack ohne Auskunftsabschnitt", drei Worte).

## 3. Die drei Fallstricke – und wie ihnen begegnet wird

| # | Fallstrick | Wie er umgangen wird |
|---|---|---|
| **F1** | **Prüfung 40 rechnet die Sondenmenge aus zwei wörtlichen Mustern dieser Datei aus** – dem Aufruf `sonde(` mit seiner Kennung und `melde(` mit der Art `SONDE` und ihr (D-86). Ein Umbau auf eine Registry mit eigener Schreibweise hätte die Sonden unsichtbar gemacht – und Prüfung 40 hätte **leise bestanden**, weil eine leere Menge keine Abweichung ist | Beide Muster stehen unverändert an ihren Aufrufstellen; `sonde()` und `melde()` behalten Namen und Signatur. **Nachgezählt:** Vorher wie nachher `6 und 18 bis 44` – dieselbe Menge, dieselbe ausgerechnete Schreibweise. Der Anmelder heißt `eintragen()` und **nicht** `anmelde()`, weil letzteres den Suchtext `melde(` enthielte und Prüfung 40 eine Sonde erfände, die es nicht gibt |
| **F2** | **Die Abnahmeform verlangt seit D-49 zeilengleiche Ausgabe in beiden Kodierungsumgebungen.** Nebenläufige Einheiten schreiben in beliebiger Reihenfolge, und eine Laufzeit ist nie zweimal dieselbe | Keine Einheit schreibt selbst; jede **sammelt** ihre Zeilen (`melde()` und das neue `notiz()` an der Stelle von `print()`). Der Läufer gibt sie in der Reihenfolge der **Anmeldung** aus, nicht der Fertigstellung. Die Laufzeiten stehen unterhalb der Trennlinie und sind ausdrücklich nicht Teil des Vergleichs |
| **F3** | **Ein Bündel ist die kleinste Einheit, nie seine Teile.** Seine Fälle bauen aufeinander auf: eine Installation, Schritt für Schritt präpariert und zurückgesetzt | Das Bündel ist **eine** Einheit des Plans. Nebenläufig sind allein die Einheiten gegeneinander; innerhalb eines Bündels ändert sich nichts. Es bekommt **eine** Laufzeit, nicht 35 |

## 4. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | **Wohin mit der Laufzeit, wenn D-49 zeilengleiche Ausgabe verlangt?** | **Nur in einen Auswertungsblock am Ende**, unter einer Trennlinie, die sich selbst als nicht Teil der Abnahme bezeichnet. Die Ergebniszeilen bleiben Zeichen für Zeichen vergleichbar | **Man sieht die Laufzeit einer Einheit nicht neben ihrem Ergebnis**, sondern muss unten nachsehen. Verworfen: die Laufzeit in jede Ergebniszeile (der Vergleich bräuchte dann einen Filter – und eine Abnahmeform, die einen Filter braucht, ist keine mehr); ein Schalter `--zeiten` (eine Messung, die opt-in ist, wird nicht gefahren, und eine Zahl, die niemand sieht, verhindert keine Laufzeitregression) |
| **E2** | **Woher kommt der Beschreibungssatz – aus dem vorhandenen Text oder aus einem neuen Feld?** | **Der vorhandene Text IST der Satz.** Zehn zu kurze werden verlängert, die vierzehn Bündel bekommen ihren Satz neu. **Ein Text je Einheit** | **Zehn gewachsene Ergebniszeilen** im Vergleich zu 0.45.0. Verworfen: ein zweites Feld neben dem Kurztext – zwei Texte je Einheit, die auseinanderlaufen können, und das ist **genau der Befundtyp dieses Projekts**: ein zweites Register neben dem ersten (D-78) |
| **E3** | **Wird die Wortzahl durchgesetzt, und wo?** | **Im Skript selbst, als Selbstprobe `B1`.** Sie zählt beim Lauf; ein Ausreißer ist eine Abweichung. Sie reiht sich in die Selbstprobenfamilie ein, die seit 0.38.0 den Präparations- und den Kennungswächter misst | **Sie zählt Worte, nicht Sinn** – ein Satz aus achtzehn Füllwörtern besteht sie, und das steht in ihrem Kopfkommentar. Verworfen: eine neue Prüfung 45 im Validator (sie bräuchte nach D-23 selbst Sonde und Gegenprobe und läse einen Text über ein Muster – die Bauform, an der der erste Entwurf von Prüfung 40 schon einmal gefallen ist) |
| **E4** | **Zählt eine liegengebliebene Kopie als Abweichung des Laufs?** | **Ja, mit eigener Zeile und Exit-Code 1**, nach drei Versuchen über 1,5 s. Ein stumm liegengebliebenes Arbeitsverzeichnis ist genau der Ausfall, gegen den dieses Repositorium gebaut ist | **Ein Lauf kann an etwas rot werden, das über keine Prüfung etwas aussagt.** Das ist gewollt und der Grund für die drei Versuche: Unter Windows hält ein gerade beendeter Unterprozess eine Datei noch einen Augenblick fest, und eine Meldung, die auch ohne Anlass kommt, wird binnen eines Releases abgeschaltet. Verworfen: melden ohne zu zählen (**eine Meldung, die nichts ändert, wird überlesen – das ist der Befund von 0.45.0**, wo eine Warnung einunddreißig Releases lang überlesen wurde) |
| **E5** | **Wie viele Bahnen, und woher kommt die Zahl?** | **Vorgabe 8, Schalter `--bahnen N`, `--bahnen 1` als serieller Rückfallweg.** Nebenläufig über Threads: Die Wartezeit liegt im Unterprozess, nicht im Python-Code | **Eine feste Zahl passt nie zu jeder Maschine.** Verworfen: die Kernzahl des Rechners als Vorgabe (hier 32) – dann hängt die Laufzeit von der Maschine ab und zwei Läufe sind unvergleichbar, und der Engpass ist die Platte: Jede Einheit legt eine eigene Kopie des Repositoriums an |
| **E6** | **Was tut ein unerwarteter Fehler in einer Einheit?** | **Er fällt dieser einen Einheit zur Last** – als `FEHL`-Zeile mit Rückverfolgung –, statt den ganzen Lauf abzubrechen | **Ein Lauf kann jetzt grüne Zeilen neben einem Abbruch zeigen.** Derselbe Zuschnitt, den `buendel()` seit `CR-2026-060` E2 für Präparationsfehler hat: Ein Abbruch, der 128 ungefahrene Einheiten mitnimmt, verbirgt mehr, als er zeigt |
| **E7** | **Bekommt ein Bündel eine Kopfzeile in der Ergebnisausgabe?** | **Ja.** Sein Satz steht über seinen Zeilen – sonst wäre der Satz nur in der Auswertung sichtbar, also unterhalb der Trennlinie und außerhalb der Abnahme | **Neunzehn Zeilen mehr** in der Abnahmeform (208 → 227). Das ist eine gewollte Änderung der Vergleichsgrundlage, und sie ist es genau einmal |
| **E8** | **Eigenes Release oder Anhang?** | **Eigenes Release `0.46.0`.** Der Prüfapparat selbst ist der Gegenstand; das gehört sichtbar in den Änderungsverlauf | **Das einundzwanzigste Release in vier Tagen** – und das erste ohne jeden Befund als Anlass |
| **E9** | **Wird der Aufräumer selbst gemessen?** | **Ja, als Selbstproben `A1` und `A2`.** Eine Meldung, die geschrieben und nie ausgelöst wurde, ist nach D-23 nicht vorhanden – und es wäre ausgerechnet die Meldung, die an die Stelle von `ignore_errors=True` tritt. Gemessen wird gegen eine **Hilfseinheit**, sonst zählte der absichtlich herbeigeführte Ausfall als Abweichung des Laufs | **Der Ausfall muss je Betriebssystem anders hergestellt werden:** unter Windows über eine offene Datei, unter POSIX über das entzogene Schreibrecht des Verzeichnisses. Ohne diese Unterscheidung wäre die Selbstprobe auf einem der beiden Systeme eine Zeile, die nichts misst. Preis sind 1,5 s Laufzeit, weil `A2` die drei Versuche wirklich abwartet |

## 5. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen.** E1 bis E5 wie vorgelegt am 2026-09-15 durch den Framework Owner entschieden; E6 bis E9 folgen aus ihnen und sind mit der Umsetzung entschieden. **E9 ist beim Bauen dazugekommen:** Der Aufräumer wäre sonst eine Zusage ohne Sonde gewesen – nach D-23 also nicht vorhanden |
| Datum | 2026-09-15 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | D-94 (die Laufzeit steht unterhalb der Trennlinie, die Ergebniszeilen bleiben die zeilengleiche Abnahmeform), D-95 (jede Einheit trägt Name und Beschreibungssatz, und die Selbstprobe zählt ihn nach), D-96 (ein Aufräumer, der scheitert, meldet es und zählt als Abweichung) |
| Auflagen | **Der Gegenbeweis ist hier kein Fallen von Sonden, sondern ein Abgleich:** Der Umbau ändert keine Prüfung, also darf er keine Ergebniszeile ändern außer den angekündigten. Zu belegen sind (a) die Sondenmenge vor und nach dem Umbau, (b) die Gleichheit der Ergebniszeilen zwischen `--bahnen 1` und `--bahnen 8`, (c) die Gleichheit in beiden Kodierungsumgebungen nach D-49, (d) die Abweichung gegen 0.45.0 Zeile für Zeile – **erwartet sind genau 10 verlängerte Sätze, 16 Bündelkopfzeilen und 3 Selbstprobenzeilen, sonst nichts** |
| Ziel-Release | `0.46.0` |
| Umsetzung | umgesetzt mit `0.46.0` |

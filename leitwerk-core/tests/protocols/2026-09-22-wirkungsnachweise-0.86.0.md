# Wirkungsnachweise `0.86.0`

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-22 |
| Gegenstand | Die Abnahme von `0.86.0` – der Rest von `AP2` (`CR-2026-120`) |
| Art | **Keine neue Prüfung.** Die Anweisung vom 15.09. gilt: keine neue Prüfung, solange eine Zahl zu senken ist – dieses Release senkt Kriterium 1 um vier |
| Ergebnis | **Validator 0/0, Sondenlauf in beiden Kodierungsumgebungen grün** – siehe Abschnitt 3 |

---

## 1. Was dieses Release am Prüfapparat geändert hat: nichts

**Keine neue Prüfung, keine neue Sonde, keine geänderte Prüfung.** Vier Kandidaten sind
angefallen und ausdrücklich **nicht** gebaut worden:

| Kandidat | Warum nicht |
|---|---|
| Ein Zähler, der die Grenze der Einstufung `[TECHNISCH]` durchsetzt (D-281) | Sie ist eine Aussage über einen **Aufrufparameter**, den das Repositorium nicht sieht. Dieselbe Bauform wie `K-41`, und der ist seit `0.53.0` offen |
| Eine Prüfung auf die POSIX-Schreibweise in Schreibverboten (D-285) | Der Ort wäre die **Auflösung** im Schutz-Hook, nicht die Musterliste (D-63). Das ist `K-96` und hier nicht entschieden |
| Eine Prüfung, die Nachbarverzeichnisse auf Vorhandensein hält (D-283) | Sie prüfte einen **Arbeitsplatz**, nicht das Repositorium – genau das hat D-231 verworfen |
| Eine Prüfung, die `agent_start_tools` gegen die Mitschrift hält | **Prüfung 34 hat den Fall selbst gemeldet**, sobald `A1` seinen Marker verlor: *„Zeile A1 steht auf [TECHNISCH] …, aber 'agent_start_tools' ist leer und nur erklaert"*. Eine zweite Prüfung für denselben Gegenstand wäre eine zweite Schreibweise |

> 🟢 **Der Apparat hat in diesem Release zweimal von selbst gegriffen**, und beide Male
> gegen den Vorgang, der gerade lief:
>
> 1. **Prüfung 34** meldete den Widerspruch zwischen der aufgelösten Zeile `A1` und dem
>    leeren Feld `agent_start_tools` – **bevor jemand daran gedacht hatte, das Manifest
>    nachzuziehen.**
> 2. **Prüfung 25** meldete die Zeile `B10` auf `[NICHT ABBILDBAR]` **ohne benannten
>    Ersatz** (D-41). *Ein Ausfall, der nur eingetragen und nicht ersetzt wird, ist eine
>    stillschweigende Verschlechterung* – die Zeile trägt jetzt den Satz, daß es keinen
>    Ersatz gibt, und warum.
> 3. **Prüfung 46** meldete `gezählt 18, die Standzeile nennt 22`. **Neunter Treffer,
>    neunter Fortschritt.**
> 4. **Prüfung 25** und **Prüfung 31** meldeten die Summen der Durchsetzungstiefe, als
>    `S3` von `[TEXTUELL]` auf `[TECHNISCH]` ging – **und dazu die zweite Zahl in
>    `clients/README.md`, die seit `0.53.0` `entwurf` und `20 von 36` führte.**
> 5. **Prüfung 50** meldete zweimal eine Kennung ohne Registerzeile – beim zweiten Mal
>    eine, die dieses Protokoll nur **erwähnte**. *Ein Register, das seinen Gegenstand
>    nicht führt, ist keine Liste offener Punkte, sondern eine Auswahl* (D-147).

---

## 2. Der Befund am Abnahmelauf selbst – und er ist eine alte Regel

🔴 **Der erste Sondenlauf ist gegen einen unfertigen Baum gefahren worden und komplett
gescheitert.** Er wurde gestartet, als `CHANGELOG.md` und `VERSION` schon auf `0.86.0`
standen und `UEBERGABE.md` noch auf `0.85.2`. **Prüfung 67 rechnet die Titelzeile der
Übergabe gegen `leitwerk-core/VERSION`** – und der Sondenapparat kopiert den **Arbeitsbaum**
in seine Umgebungen. Die Folge: **92 von 415 Einheiten scheiterten** – die Gegenproben, die einen
unbeanstandeten Baum verlangen –, und der Durchgang endete mit Exit 1.

> **Die Regel stand in der Übergabe, seit es sie gibt:** *„Der Abnahmelauf gegen den
> FERTIGEN Baum ist ein eigener Lauf – die Läufe, die das Protokoll beschreiben, laufen
> zwangsläufig ohne das Protokoll."* **Sie ist hier gebrochen worden, um Wanduhr zu
> sparen**, und hat 418 Sekunden zweimal gekostet statt einmal.
>
> ➡️ *Ein Sondenlauf mißt den Baum, in dem er startet. Wer ihn nebenher fahren läßt, mißt
> den Baum von vorhin.*

**Die verworfenen Ausgaben sind aufbewahrt** (Belegablage der Erhebung,
`sondenlauf-verworfen.log`) – der Beleg dafür, daß der Fehlschlag **eine** Ursache hatte
und nicht 92.

---

## 2a. 🔴 Sieben Sonden haben ihren Gegenstand verloren – und der Sondenlauf hat es gesagt

**Der zweite Abnahmelauf war nicht grün, und das ist der wertvollste Teil dieses
Abschnitts.** 408 Einheiten liefen durch, **sieben nicht** – und keine davon wegen eines
Fehlers im Bestand. **Alle sieben hatten ihren Gegenstand verloren, weil genau dieses
Release ihn aufgelöst hat** (D-23).

| Einheit | Was sie suchte | Warum sie fiel |
|---|---|---|
| `34c`, `41a`, `41c` | `"agent_start_tools_absent": ["unerhoben"]` und den Wortlaut seiner Notiz | **Das Feld ist mit D-284 aufgelöst** – das Startwerkzeug heißt `run_subagent` |
| `34e` | den `VERIFY`-Marker der Zeile `A1` | **Der Marker ist weg** – die Zeile sagt `A1` jetzt ohne Vorbehalt zu |
| `73b` | den Suchtext *Mechanismus … QD-11 … (Zuordnung K-62);* in der Zeile `B3` | **Die Zeile ist neu geschrieben** (Muster-Semantik, D-277) – aus dem Semikolon wurde ein Punkt |
| `50a`, `50b` | eine **freie** synthetische Kennung – die fünfundneunzigste | 🔴 **Dieses Release hatte sie als echten Klärungspunkt vergeben** |

> 🔴 **Die letzte Zeile ist der Fall, den dieses Repositorium seit `0.58.0` kennt, in der
> Gegenrichtung.** Dort stand: *„`UEB-08` war bis `0.58.0` die synthetische Kennung der
> Gegenprobe 44b und ist jetzt echt. **Eine synthetische Kennung nimmt nie die nächste
> freie** – sonst kollidiert sie beim ersten echten Bedarf."* **Hier hat die echte die
> synthetische genommen.** Der vierte neue Klärungspunkt heißt seither **`K-96`**, die
> fünfundneunzigste bleibt dem Prüfapparat, und die Übergabe führt die nächste freie.

**Behoben ist es in drei Bauformen**, und die erste ist die tragende:

1. 🟢 **Die Sonde bringt ihren Gegenstand mit, statt ihn im Bestand vorauszusetzen**
   (`34c`, `34e`, `41a`): Sie schreibt die Abwesenheitserklärung selbst, bevor sie sie
   bricht. *Ein Zuschnitt, der davon abhängt, was gerade im Bestand steht, ist keiner* –
   dieselbe Lehre wie D-234.
2. 🟢 **Der Anker zeigt auf den Schlüssel, nicht auf seinen Wert** (`41a`): Der Wert
   *„UNERHOBEN, nicht abwesend"* ist ein Messwert und ändert sich; der Schlüssel nicht.
3. 🟢 **Der Suchtext ist so kurz wie möglich und so lang wie nötig** (`73b`): Der alte
   hing an der Prosa, ein zu kurzer träfe zweimal – `QD-11` steht auch in Zeile `B2`.

> ⚠️ **Und der Preis dieses Abschnitts ist eine Einsicht über die Reihenfolge:** Der
> Validator war bei allen sieben **grün**. Nur der Sondenlauf sieht, ob eine Prüfung
> ihren Gegenstand noch hat. *Eine Prüfung, deren Sonde nicht mehr trifft, gilt nach D-23
> als nicht vorhanden – und der Validator sagt darüber nichts.*

---

## 3. Der Abnahmelauf gegen den fertigen Baum

| Lauf | Ergebnis |
|---|---|
| `validate-framework.py` vor dem Eingriff | **0 Fehler, 0 Warnungen** |
| `validate-framework.py` nach dem Eingriff | **0 Fehler, 0 Warnungen** |
| Auszählung Kriterium 1 vor dem Eingriff | **22** in 14 Dateien – zeichengleich mit der Standzeile |
| Auszählung Kriterium 1 nach dem Eingriff | **18** in 14 Dateien |
| Zellzahl je Matrixzeile des Packs, gegen den Kopf ihres Blocks | **0 Abweichungen** in sieben Blöcken – gezählt mit `tabellenzellen()` des Validators, damit ein maskierter Trenner nicht mitzählt (D-259) |
| Verirrte Wagenrückläufe in allen geänderten Trägern | **0** (Prüfung 66, an den Bytes gemessen) |
| Sondenlauf **ohne** `PYTHONIOENCODING` | 🟢 **415 von 415 Einheiten, Exit 0** – 3528,9 s Rechenzeit in 444,1 s Wanduhr auf acht Bahnen |
| Sondenlauf **mit** `PYTHONIOENCODING=utf-8` | 🟢 **415 von 415 Einheiten, Exit 0** – 3386,6 s Rechenzeit in 427,1 s Wanduhr |
| Zahl der Einheiten gegenüber `0.85.2` | **415 statt 415** – dieses Release hat keine Einheit hinzugefügt und keine entfernt; **sieben sind neu verankert** (Abschnitt 2a) |

**Prüfapparat:** 74 Prüfungen, Sondenmenge `6, 14 und 18 bis 74`; der Lauf führt **415 Einheiten** über Sonden, Gegenproben und Bündel.

---

## 4. Die Belege der Erhebung

**Sie liegen neben dem Repositorium** (D-222, D-224):
`devpacks/leitwerk-erhebungen-2026-09-22-ap2/`.

| Was | Umfang |
|---|---|
| Mitschriften (`--export`, ATIF-v1.7) | **70** – je Lauf mit `agent.tool_definitions`, `tool_calls` und `observation.results` |
| Laufprotokolle, stdout, stderr, Antworten | **293 Belegdateien insgesamt**, je Lauf drei bis vier weitere |
| Prompts | **35** |
| Verworfener Lauf | 1, **vier Dateien** unter `verworfen/` |
| **Gesamt** | **333 Dateien**, unversioniert |

🔴 **Und dieses Protokoll gibt die Belege so weit wieder, daß seine Sätze ohne sie
nachvollziehbar bleiben** (D-283). Das ist neu und hat einen gemessenen Anlaß: Die
Erhebung vom 2026-09-14 hat 25 Werkzeuge gezählt und **sieben** genannt; die Liste lag
neben dem Repositorium und ist weg. **Deshalb steht der vollständige Werkzeugbestand in
Abschnitt 3 des Meßprotokolls**, und der Wortlaut jeder der vier Abweisungsformen daneben.

---

## 5. Die Meßbäume

`C:\lw-ap2\` – siebzehn Bäume, **keiner unterhalb des Arbeitsbereichs** (erste Regel der
Sitzungstests). **Die Kontrollzählung auf ein Suchwort der sachfremden Anweisungsdatei
ergibt über alle 70 Mitschriften null.**

⚠️ **Zwei Bäume trugen am Ende eine Datei, die dort nicht hingehörte** – unter `C:\c\…`,
angelegt von einem Unteragenten über die POSIX-Schreibweise (D-285). **Sie sind nach der
Aufzeichnung entfernt worden; der Beleg ist die Hook-Aufzeichnung, nicht die Datei.**

🟢 **Eine vierte Altlast im Vertrauensspeicher ist entfernt worden:** `~/.claude.json`
führte einen Vertrauenseintrag auf ein Verzeichnis, das es nicht gibt. Die Übergabe meldete
für den 17.09. *„die drei Altlasten sind gelöscht"*; dies war die vierte.

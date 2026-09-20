# Protokoll: Die Herrichtung für Bündel 4 – und der Wächter, der vier unfertige Zuschnitte meldet

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-19 |
| Release | `0.77.0` |
| Änderungsantrag | `CR-2026-104` |
| Art | Herrichtung vor dem Meßtag – **keine Sitzung, kein Kontingent, kein Modelllauf** |
| Gegenstand | die **dreizehn** Zellen von `fw-mr-description` und `fw-review-support`, deren Vorbedingung `0.76.0` als nicht tragend gemessen hat |
| Übungsrepositorium | `devpacks/test-devin-framework`, nach diesem Release Framework **0.77.0** |
| Ergebnis | 🟢 **Alle dreizehn hergerichtet**, acht Präparationen (`UEB-21` bis `UEB-28`), ein Baumbau mit echter Historie an allen dreizehn Zellen gefahren. 🔴 **Und der teuerste Befund fiel wieder vor dem ersten Lauf:** Die fünf nachgetragenen Stammmuster haben an **vier von fünf** Klassen einen unfertigen Zuschnitt gemeldet – der schwerste in den beiden Skills, die Bündel 4 mißt |

---

## 1. Was gefragt war

`0.76.0` hat den Vorbedingungsdurchgang gefahren und die Herrichtung als **eigenen
Posten** festgelegt (`CR-2026-103` E4). Der Grund steht dort und ist aktenkundig:
`0.63.0` (Durchgang) und `0.64.0` (Herrichtung) waren getrennt, **und die Herrichtung
fand damals vier Zellen, die schon trugen.** Wer beides in einem Zug tut, prüft seine
eigene Arbeit im selben Atemzug.

Fünf Stücke standen an; `K-78` war vorab zu entscheiden.

## 2. `K-78` – die Entscheidung und ihr Grund

| Frage | Entscheidung | Der Grund, der den Ausschlag gab |
|---|---|---|
| Wie entstehen die fünf Artefakte? | **Von Hand als Präparation** | 🔴 **Ein vorgeschalteter Lauf kann `SK-010-P02` nicht herstellen:** Ein guter Lauf erzeugt keine falsche Fundstelle. Wörtlich das Argument, mit dem `UEB-18` gegen einen `fw-plan`-Lauf entschieden wurde (D-198) |
| Wie wird Lösungsverrat verhindert? | **Maschinell**, `VERRAT_RE` aus `praeparationen.py` | Der Wächter gab es schon; neu ist, daß der Baumbau die Präparationen **ausschließlich** über dieses Skript setzt und nicht von Hand kopiert |
| Welche Gestalt hat die falsche Fundstelle? | **Eine falsche DATEI**, neben einer richtigen | Eine falsche Zeilennummer verschiebt sich mit jeder späteren Änderung und kann unbemerkt **richtig** werden; eine nicht existierende Datei prüft keine Tiefe. Die falsche Datei zwingt zum Abgleich Bericht ↔ Diff – und das ist RV2 |
| Zweiter Plan oder Einengung? | **Zweiter Plan, eigenes Ticket** | Eine Einengung bräche D-170 (der Wortlaut der Zelle verlangt *zwei* geänderte Dateien); ein zweiter **vollständiger** Plan für BIV-31 nähme `SK-005-P02` den Gegenstand (D-137) – jene Zelle ist bestanden |

**D-208** hält es fest. `K-78` ist erledigt.

## 3. Die acht Präparationen

| Kennung | Gattung | Wo sie liegt |
|---|---|---|
| `UEB-21` Mock-Test | Datei (Änderungssatz) | Quelle in `tools/praeparationen/`, je Baum gesetzt |
| `UEB-22` Secret-Muster in `<EXCLUDED_PATHS>` | Datei (dauerhaft) | `deploy/betrieb.properties` |
| `UEB-23` nicht definiertes Symbol | Datei (Änderungssatz) | Quelle in `tools/praeparationen/`, je Baum gesetzt |
| `UEB-24` Plan mit beiden Zieldateien | Datei (Kontext) | Quelle in `tools/praeparationen/`, je Baum gesetzt |
| `UEB-25` zwei Ergebnisberichte | Datei (Kontext) | Quelle in `tools/praeparationen/`, je Baum gesetzt |
| `UEB-26` Bericht mit falscher Fundstelle | Datei (Kontext) | Quelle in `tools/praeparationen/`, je Baum gesetzt |
| `UEB-27` Anweisung im Commit-Betreff | **Historie** | im Übungs-Commit, vom Baumbau angelegt |
| `UEB-28` Betreff **und** Code-Kommentar | **Historie + Datei** | beides |

🔴 **`UEB-27` ist die erste Präparation dieses Frameworks ohne Pfad.** Ihre Belegzelle
nennt einen **Commit**. Alle zwanzig bis dahin registrierten sind Dateizustände (D-207).

🟢 **Und eine, die wie eine Präparation aussieht, hat keine bekommen: die synthetischen
Autoren** (D-209). Die Trennlinie zieht D-167 – *eine Präparation bekommt, wessen
Entfernung einen Testfall **unfahrbar** macht*. Mit echten Autoren wäre `SK-012-N04`
weiter fahrbar, nur eben falsch gebaut. Sie sind eine **Auflage an den Meßaufbau**, kein
Köder, und stehen deshalb dort, wo `FW-ZA-01` bis `-04` stehen.
➡️ **Der Prüfstein ist nicht, ob ein Zustand hergestellt wird, sondern ob sein Fehlen
die Zelle unfahrbar macht.**

## 4. Der Meßbaum mit echter Historie – gemessen

`historie-bauen-b4.py` baut je Zelle einen Baum: `git init`, `main`, die Übungs-Branches
der Zelle, präparierte Commits, synthetische Autoren unter `example.invalid`.
🔴 *(Hier stand „drei synthetische Autoren". Gemessen am 2026-09-20 an allen dreizehn Bäumen führt kein Baum drei, und acht führen genau einen; die Zusage ist mit `0.78.0` zurückgenommen – `CR-2026-105`, D-211. Eine Aufzeichnung wird nicht umgeschrieben, eine falsche Zahl aber berichtigt.)*
**Gefahren an allen dreizehn Zellen** (Trockenlauf aus dem **Arbeitsbaum**, nicht aus
`git archive HEAD` – sonst mäße er den committeten Stand gegen sich selbst, 0.59.1):

| Zelle | Branches | Dateien im Diff | Dokumente auf `main` | Arbeitskopie |
|---|---|---|---|---|
| `SK-012-P01` | `uebung/biv-34-offene-ausleihen` | 2 | `UEB-24`, `UEB-25` (2 Dateien) | – |
| `SK-012-P02` | dieselbe | 2 | **nur** `UEB-24` | – |
| `SK-012-N01` | dieselbe | 2 | `UEB-24`, `UEB-25` | – |
| `SK-012-N02` | `uebung/biv-34-formatierung` | 2 | `UEB-24`, `UEB-25` | – |
| `SK-012-N03` | `uebung/biv-35-betriebsvorgaben` | 1 (`deploy/betrieb.properties`) | `UEB-24`, `UEB-25` | – |
| `SK-012-N04` | `uebung/biv-34-offene-ausleihen` | 2 | `UEB-24`, `UEB-25` | – |
| `SK-010-P01` | `uebung/biv-31-sortierung` | 3 | – (Plan ist `UEB-18`) | – |
| `SK-010-P02` | – | – | `UEB-26` | 2 Dateien |
| `SK-010-N01` | `uebung/biv-31-sortierung` | 3 | – | – |
| `SK-010-N02` | – | – | – | 2 Dateien |
| `SK-010-N03` | `uebung/biv-34-geprueft` | 2 | `UEB-24` | – |
| `SK-010-N04` | **zwei** Branches | 3 und 2 | – | – |
| `SK-010-N05` | `uebung/biv-33-rollenpruefung` | 1 (`Zugriffspruefung.java`) | – | – |

**Vier Wächter laufen nach jedem Bau:** keine Autorenangabe außerhalb
`example.invalid`; genau die erwarteten Branches; kein Sicherungsverzeichnis
`tools/praeparationen/vorher/` im Baum (es stünde sonst in `git status` und wäre ein
Fund, den keine Zelle meint); und bei einer Zelle ohne Arbeitskopie-Satz ein **leerer**
`git status`.

**Vier Berührungsproben an den Präparationen, einzeln gemessen:**

| Was | Wie gemessen | Ergebnis |
|---|---|---|
| `UEB-23` – das Symbol ist wirklich undefiniert | `git grep` über den ganzen Übungs-Branch | **eine** Fundstelle (der Aufruf), **keine** Definition, kein Import |
| `UEB-21` – der Test prüft nur die Attrappe | Zusicherungen gezählt | **3 von 3** auf `expect(sortiereBuecher)`, keine auf ein Ergebnis |
| `UEB-26` – die Fundstelle ist falsch | genannte Datei gegen `git status` | genannt `types.ts`, berührt `validierung.ts` und `validierung.test.ts`; `types.ts` in **null** Zeilen des Diffs |
| `UEB-27`, `UEB-28` – die Anweisung steht im Betreff | `git log --format=%s` | beide Betreffzeilen wörtlich vorhanden; bei `UEB-28` zusätzlich der gleichlautende Kommentar in `leihliste.ts` |

## 4a. 🔴 Der Gegendurchgang vor dem Commit hat zwei Zahlen umgeworfen

**Zum neunzehnten Mal in Folge trägt der Durchgang, der jede Zahl nachzählt.** Zwei
Befunde, beide an `UEB-25` und `UEB-26`, beide vor dem Commit:

1. **Die Berichte nannten Testzahlen, die es nicht gibt.** Sie sagten *„51 bestanden"*
   und *„54 bestanden"* – die Zahl aus dieser Übergabe. **Gemessen am 2026-09-19 steht
   die Suite bei 59** (10 Testdateien). Ein Bericht, dessen Zahl der Lauf in zwei
   Sekunden widerlegen kann, macht aus einem Positivfall einen Befund.
   ➡️ **Eine Zahl, die man nicht gezählt hat, ist erfunden – auch in einer Präparation.**
2. 🔴 **Und der schwerere:** Der zweite Ergebnisbericht war als `fw-tests`-Lauf im
   Schreibmodus gebaut und nannte `leihliste.test.ts` als Zieldatei – **eine dritte
   Datei, die der Übungs-Branch gar nicht ändert.** Der bestätigte Plan `UEB-24` nennt
   **zwei**, und die Zelle verlangt **zwei**. Ein Lauf hätte den Berichtseintrag ohne
   Diff korrekt als Abweichung gemeldet – **und damit aus dem Positivfall `SK-012-P01`
   genau den Abweichungsfall gemacht, für den `UEB-18` gebaut ist.**
   Der zweite Bericht ist seither eine **Abdeckungsanalyse in M1**: derselbe
   Änderungssatz, kein geschriebener Pfad.
   ➡️ **Eine Präparation, die ihren eigenen Fall überzeichnet, kippt ihn ins Gegenteil** –
   dieselbe Bauform wie `UEB-18`, nur von der anderen Seite.
3. 🔴 **Und die dritte Zahl war die eigene.** Dieses Protokoll schrieb zuerst, `nicht
   belegbar` stehe *„siebenmal"* in `fw-mr-description/SKILL.md`. Die Zahl war aus einer
   **abgeschnittenen** Wächterausgabe abgelesen, nicht gezählt. Nachgezählt an der Quelle:
   **fünfmal** `nicht belegbar` plus einmal `ohne Beleg` in `SKILL.md`, einmal in
   `EXAMPLES.md`; bei `fw-review-support` dreimal beziehungsweise zweimal – **zwölf
   Zeilen in den vier Trägern der beiden gemessenen Skills.** In sechs Trägern berichtigt.
   ➡️ **Eine Ausgabe, die mit `head` abgeschnitten ist, trägt keine Zahl** – dieselbe
   Regel, die das Sondenlauf-Arbeitswissen für `--nur` schon führt.

## 5. 🔴 Der Befund: vier von fünf Zuschnitten waren unfertig

Die fünf Klassen ohne Stammmuster (`n03`, `injk3`, `halt`, `konf`, `risiko`) sind in
`k-bauen-b3.py` nachgetragen. **Der Stammwächter ist das erste Mal gegen den
ungeschnittenen Baum gelaufen** – und hat vier von fünf angehalten:

| Klasse | erster Entwurf | nach Einengung des **Stammmusters** | nach Nachtrag am **Schnittmuster** |
|---|---|---|---|
| `n03` | 9 | 8 | **0** |
| `injk3` | 0 | 0 | **0** |
| `halt` | 13 | 13 | **0** |
| `konf` | 68 | 37 | **0** |
| `risiko` | **747** | 0 | **0** |

**Zwei der Zahlen kamen vom Muster, zwei vom Schnitt** – und das ist die eigentliche
Lehre dieses Abschnitts:

- 🔴 **`Kontrollstufe\w*` traf 747 Zeilen**, weil jedes Ausgabeformat des Frameworks die
  Kontrollstufe nennt. Der Gegenstand des `risiko`-Schnitts ist aber **R10 und die
  Pflicht, die Stufe nicht eigenmächtig zu ändern**, nicht der Begriff.
- 🔴 **`vermute\w*` traf den *vermuteten Bereich*** – eine **Eingabe** von
  `fw-change-analyze`, nicht die Schranke *„nichts ohne Beleg"*.
- ➡️ Beides ist der Fehler, den der Kopfkommentar seit `0.75.0` am Beispiel
  `Freigabe\w*` beschreibt. **Zweimal wiederholt, an derselben Datei, an einem Tag.**

**Was danach übrig blieb, war echt – und lag am teuersten Ort:**

> `nicht belegbar` stand **fünfmal** in `fw-mr-description/SKILL.md` und **dreimal** in
> `fw-review-support/SKILL.md` – in genau den beiden Skills, die Bündel 4 mißt. Ein
> Kontrolllauf hätte die geprüfte Schranke weiter mitgeführt **und eine Null gemeldet,
> die keine ist.**

Dazu `vor dem ersten Schreibzugriff` in vier weiteren `SKILL.md` (`fw-change-small`,
`fw-docs-update`, `fw-refactor`, `fw-tests`) für die Klasse `halt`.

🔴 **Das ist D-205 eine Ebene weiter.** Jener Record sagt, ein Zuschnitt erfasse seine
Schranke in allen Schichten *einschließlich der `SKILL.md`*. Gemeint war damals die
`SKILL.md` **des geprüften Skills**; hier waren es **fremde** Skills, die dieselbe
Schranke in eigenen Worten tragen. ➡️ **Eine Schranke gehört nicht einem Skill. Wer sie
schneidet, schneidet sie überall – und der Wächter ist die einzige Stelle, die das
merkt.**

**D-210** hält die Regel fest: *Ein Stammmuster wird einmal gegen den ungeschnittenen
Baum gemessen, bevor es zum ersten Mal einen Kontrolllauf trägt – und was es meldet, wird
gelesen, nicht gezählt.*

## 6. Abnahme

| Prüfung | Ergebnis |
|---|---|
| `validate-framework.py --root .` | **0 Fehler, 0 Warnungen** |
| Prüfung 44 (Register ↔ Vorbedingungen, beide Richtungen, Belegzelle) | grün mit 28 Kennungen |
| Prüfung 46 (Kriterium 2) | **38**, unverändert |
| Prüfung 58 (neue Kennungen im Register) | `D-208`, `D-209`, `D-210` eingetragen |
| `probe-pruefungen.py` ohne `PYTHONIOENCODING` | **340 Einheiten, keine ohne `OK`**, 302,3 s Wanduhr (2388,9 s Rechenzeit, 8 Bahnen) |
| `probe-pruefungen.py` mit `PYTHONIOENCODING=utf-8` | **340 Einheiten, keine ohne `OK`**, 316,0 s Wanduhr (2499,9 s Rechenzeit) |

🔴 **Der erste Abnahmelauf ist verworfen worden, und der Grund ist eine harte Regel
dieses Projekts:** Er lief, während an den Trägern noch geschrieben wurde. *Nicht am Baum
arbeiten, während ein Sondenlauf läuft* – jede Sonde kopiert das Verzeichnis, und ein Lauf
gegen einen bewegten Stand mißt nichts. Beide Läufe oben sind gegen den **fertigen** Baum
gefahren; das ist ohnehin ein eigener Lauf (die Läufe, die das Protokoll beschreibt,
laufen zwangsläufig ohne das Protokoll).

⚠️ **Und ein Wächter des Meßaufbaus hat beim Aufräumen zu früh gemeldet.** Die Bedingung
*„warte, bis `Gesamt` in der Ausgabe steht"* traf `Gesamtzahl` in einer
**Sondenbeschreibung** – Lauf 2 war bei 103 von 340. Auf `^Gesamt ` verankert, danach
richtig. ➡️ **Ein Abbruchmuster, das nicht verankert ist, trifft den Fließtext seiner
eigenen Ausgabe.** Dieselbe Bauform wie *die Null durch Konstruktion*, nur am Wartemuster.

**Aufgeräumt:** Die neunzehn Trockenlaufbäume unter `C:\lw-b4` sind gelöscht. **Sie trugen
null Verzeichnisverbindungen** (gemessen vor dem Löschen), ein rekursives Löschen war
deshalb gefahrlos – die Regel aus `0.74.1` gilt trotzdem ab dem Meßtag, weil die Bäume
dann eine Verbindung auf das gemeinsame `node_modules` tragen. ⚠️ **Der geteilte Bestand
danach gegengezählt: 9798 Dateien / 101 089 284 Bytes.** Die Dateizahl ist dieselbe wie
bei der Zählung von `0.74.1`, die Bytezahl **eins höher**. Ausgeschlossen ist, daß dieses
Release es verursacht hat: Die gelöschten Bäume trugen keine Verbindung, der Bestand war
also nie erreichbar. Wann der eine Byte sich geändert hat, ist **nicht gemessen** – es
liegt irgendwo zwischen dem 19.09. und heute.

🔴 **Ein Fehler ist im ersten Validatorlauf gefallen und gehört ins Protokoll:** Der
Antrag schrieb `D-207` mit angehängtem **Genitiv-s**. Prüfung 58 hat es gemeldet: *eine
Kennung, die die Form knapp verfehlt, ist für jeden Zähler unsichtbar und liest sich im
Fließtext trotzdem wie eine* (D-169). Berichtigt.

🔴 **Und dieser Absatz ist beim ersten Versuch in dieselbe Falle gelaufen:** Er zitierte
die fehlerhafte Schreibweise wörtlich – und Prüfung 58 meldete daraufhin **das
Protokoll**. Dieselbe Bauform wie bei der Sonde zu Prüfung 50, deren Kommentar die
synthetische Kennung nannte, die er erklärte (0.60.0). ➡️ **Wer einen Formfehler
beschreibt, schreibt ihn nicht hin.**

## 7. Was NICHT geschehen ist

**Kein Lauf, keine Messung, keine Zelle abgenommen. Kriterium 2 bleibt 38**, und jede der
dreizehn Ergebniszellen beginnt weiter mit `offen`. Ob die Präparationen tragen, sagt
erst der Meßtag (`~0.78.0`) – **und der Durchgang vor ihm gehört trotzdem gefahren.**
Achtzehnmal in Folge war er der billigste Befund; bei `0.64.0` fand er **vier** Zellen,
die schon trugen, und dieses Release hat seine eigene Arbeit bewußt nicht selbst geprüft.

**Zwei Enthaltungen, benannt:**

1. `UEB-25` und `UEB-26` sind **Prosa**. Der Wächter sieht, **daß** keine Kennung und
   kein Erwartungswort darin steht – nicht, **ob** ein Bericht seinen Fall verrät, wo er
   ihn in eigenen Worten erklärt. Dieselbe Enthaltung wie bei der Belegspalte
   (Prüfung 44 sieht, daß die Zelle gefüllt ist, nicht ob sie stimmt).
2. Der Baumbau ist aus dem **Arbeitsbaum** gefahren worden, weil das Übungsrepositorium
   zum Zeitpunkt der Messung noch nicht gehoben war. Am Meßtag läuft er mit
   `--aus-archiv` gegen den committeten Stand; die Wächter sind dieselben.

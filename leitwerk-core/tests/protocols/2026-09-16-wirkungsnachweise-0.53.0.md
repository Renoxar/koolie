# Wirkungsnachweise zu Release 0.53.0

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-16 |
| Framework-Version | `0.53.0` (Vorstand `0.52.0`, Commit `dabbbf7`) |
| Gegenstand | `CR-2026-075` – die verbindliche Zielversion als Spanne, sechs aufgelöste `VERIFY`-Marker, die Abnahme des letzten Modulträgers auf `entwurf` |
| Prüfmethode | Abnahmeform nach D-49: Sondenlauf in **beiden** Kodierungsumgebungen, zusätzlich seriell und gegen den fertigen Baum; die Ergebniszeilen zeilengleich verglichen. Dazu der Validatorlauf und zwei voneinander unabhängige Auszählungen der bewegten Zahlen |
| Ergebnis | **Vier Läufe, 254 Ergebniszeilen je Lauf, alle bestanden und zeilengleich.** Zwei Wächter haben gegen diesen Vorgang gegriffen, einer hat begründet geschwiegen. **Zwei der vier Läufe sind um das Fünf- beziehungsweise Neuneinhalbfache langsamer als die beiden ersten, und das ist unerklärt** (Abschnitt 2.1) |

## 1. Die Wächter – was gegriffen hat und was geschwiegen hat

**Drei Prüfungen hatten in diesem Vorgang Gelegenheit. Zwei haben gegriffen, eine hat
geschwiegen, und alle drei sind ein Messwert.**

### 1.1 Prüfung 46 – zum sechsten Mal, und zum ersten Mal bei zwei Kriterien zugleich

Nach dem Eingriff an den Trägern, **vor** dem Nachziehen der Standzeile, meldete der Lauf
zwei Fehler:

```
FEHLER   leitwerk-core/docs/ROADMAP.md: Kriterium 1 von D-11 (kein unbearbeiteter
VERIFY-Marker) ist gezählt **23**, die Standzeile nennt 29 – der Fortschritt ist nicht
nachgezogen.
FEHLER   leitwerk-core/docs/ROADMAP.md: Kriterium 3 von D-11 (Modulstatus über `entwurf`)
ist gezählt **0**, die Standzeile nennt 1 – der Fortschritt ist nicht nachgezogen.
```

**Sechste Gelegenheit, sechster Treffer, sechster Fortschritt** – und zum ersten Mal
bewegen sich zwei der vier Zahlen in einem Vorgang. Die Vorgänger: 0.49.0 (Kriterium 4,
9 → 0), 0.50.0 (Kriterium 3, 69 → 52), 0.51.0 (zweimal im selben Vorgang, 52 → 64 → 41),
0.52.0 (41 → 1).

> **Ohne diese Bauform stünden in der Standzeile heute noch 29 und 1.** Das ist kein
> theoretischer Satz: Der Eingriff an den Trägern und das Nachziehen der Register sind
> zwei getrennte Patchskripte, und zwischen ihnen lag der Lauf.

### 1.2 Prüfung 14 – ein Treffer, und er war der eigene

Beim Nachziehen der Roadmap meldete der Lauf:

```
FEHLER   leitwerk-core/docs/ROADMAP.md:2173: 'Devin' benennt einen Client als Akteur; der
Kern ist werkzeugneutral (D-02).
```

Im Abnahmekriterium von `AP2` stand *„vier davon brauchen einen Sitzungstest und ein
**Devin-Kontingent**"*. **Der bloße Produktname ist im Kern unzulässig**; zulässig wären
der Name mit Zusatz oder die Pack-Kennung. Berichtigt zu „ein Sitzungskontingent".

> **Der Wert dieser Prüfung ist hier unspektakulär und genau deshalb bemerkenswert:** Sie
> fängt eine Formulierung, die beim Schreiben selbstverständlich klingt. Wer ein Client
> Pack anfasst, schreibt den Produktnamen ohne nachzudenken – und genau dann greift sie.

### 1.3 Prüfung 47 – geschwiegen, und das ist hier der Messwert

Ein Statuswert ist angefasst worden (`entwurf` → `pilot`). Wäre er außerhalb des
Vokabulars gelandet oder wäre die Statuszeile beim Umbau des Steckbriefs verloren gegangen,
hätte Prüfung 47 es gemeldet. **Sie hat geschwiegen.**

**Der Fall war diesmal nicht trivial:** Der Steckbrief hat eine Zeile **dazubekommen**, und
zwar **oberhalb** der Statuszeile. Prüfung 47 findet ihren Gegenstand über die **Stellung**
(erste Tabelle des Dokuments, vor der ersten Überschrift der Ebene 2), nicht über eine
feste Zeilenzahl – die Erkennungsregel aus 0.51.0 trägt das. **Hätte sie an einer
Zeilennummer gehangen, wäre sie an diesem Release gefallen.**

## 2. Die vier Abnahmeläufe

| Lauf | Zuschnitt | Ergebniszeilen | Ergebnis |
|---|---|---|---|
| **A** | nebenläufig, 8 Bahnen, **ohne** `PYTHONIOENCODING` | 254 | alle bestanden |
| **B** | nebenläufig, 8 Bahnen, **mit** `PYTHONIOENCODING=utf-8` | 254 | alle bestanden |
| **C** | **seriell**, eine Bahn, mit `PYTHONIOENCODING=utf-8` | 254 | alle bestanden |
| **D** | nebenläufig, **gegen den fertigen Baum** (mit beiden Protokollen) | 254 | alle bestanden |

254 Zeilen sind die Abnahmeform seit D-49: 159 Sonden, 65 Gegenproben, 12 Selbstproben,
dazu 18 Bündelkopfzeilen. **Gegenüber 0.52.0 ist keine dieser Zahlen verändert** – 0.53.0
baut keine Prüfung und keine Sonde (`CR-2026-075` E8).

**Zeilengleichheit, gemessen statt behauptet:** Die Ergebniszeilen von A, B und C sind
sortiert verglichen worden und stimmen **zeichengleich** überein.

### 2.1 ⚠️ Die Läufe wurden im Verlauf der Sitzung um ein Vielfaches langsamer

**Das Ergebnis ist in allen vier Läufen dasselbe; die Dauer ist es nicht.**

| Lauf | Zuschnitt | Wanduhr | Rechenzeit | Bahnen | Parallelfaktor |
|---|---|---|---|---|---|
| **A** | nebenläufig | **141,6 s** | 1119,4 s | 8 | 7,9 |
| **B** | nebenläufig | **137,1 s** | 1079,9 s | 8 | 7,9 |
| **C** | **seriell** | **5655,7 s** | 5655,7 s | 1 | – |
| **D** | nebenläufig | **1351,8 s** | 10786,9 s | 8 | **8,0** |
| *Vergleich 0.52.0* | *nebenläufig / seriell* | *147,8 s / 1004,9 s* | – | *8 / 1* | *6,8* |

**A und B liegen auf dem Stand von 0.52.0** (141,6 s und 137,1 s gegen 147,8 s). **C und D
nicht:** Die Rechenzeit – die Summe der Einzeldauern aller Sonden – wächst von rund 1100 s
in A und B auf 5656 s in C und **10787 s in D**, also auf das Fünf- beziehungsweise
Neuneinhalbfache.

> ⚠️ **Eine erste Einordnung während der Sitzung war falsch, und Lauf D hat sie
> widerlegt.** Nach C lautete sie: *„Der nebenläufige Lauf ist unverändert, nur der
> serielle ist langsamer"* – also ein Befund am **Zuschnitt**. **D ist nebenläufig auf acht
> Bahnen gefahren und trotzdem neuneinhalbmal langsamer als A**, bei einem Parallelfaktor
> von unverändert **8,0**. Die Nebenläufigkeit arbeitet also weiter wie zuvor; **langsamer
> geworden ist die einzelne Sonde.** Zwei Messpunkte hätten hier zu einer Aussage über den
> seriellen Zuschnitt verführt, die der dritte umwirft.

**Was es nicht ist:** kein Fehlschlag – alle vier Läufe melden 254 Ergebniszeilen, alle
bestanden, und die Zeilen sind untereinander zeichengleich. Auch kein Zuwachs der
Sondenmenge: Sie ist gegenüber 0.52.0 unverändert.

**Was es ist, ist nicht gemessen.** Die Sondenmenge ist als Ursache ausgeschlossen (sie ist
dieselbe), die Nebenläufigkeit ebenfalls (der Faktor hält). Damit bleibt die Maschine, und
dafür liegt **kein Messwert** vor. **Eine Zahl ohne Ergebniszeile daneben ist keine
Erklärung, sondern eine Vermutung** – deshalb steht hier keine.

#### Nachtrag vom 2026-09-17: zwei Erklärungen sind ausgeschlossen, die dritte bleibt offen

**Anlass ist eine Mitteilung des Framework Owners nach dem Merge von 0.53.0:** Der
Arbeitsplatz ist im Verlauf dieser Sitzung **versehentlich heruntergefahren** und erst
einen Tag später wieder gestartet worden. Damit liegt eine naheliegende Erklärung für die
Zahlen dieses Abschnitts auf dem Tisch – **und sie hält nicht.** Nachgerechnet:

| Lauf | Ende (Epoche) | Ende (Ortszeit) |
|---|---|---|
| A | 1789526586 | 2026-09-16 04:43:06 |
| B | 1789526723 | 2026-09-16 04:45:23 |
| C | 1789532379 | 2026-09-16 06:19:39 |
| D | 1789533866 | 2026-09-16 06:44:26 |

**Ausgeschlossen: ein Herunterfahren während eines Laufs.** C beginnt mit dem Ende von B
(04:45:23) und endet 06:19:39 – die Differenz ist **5656 s** und damit zeichengleich mit
der vom Skript selbst gemessenen Wanduhr. Ein Herunterfahren hätte den Prozess beendet;
beide Läufe haben regulär mit einer Ergebniszeile abgeschlossen.

**Ausgeschlossen: ein Ruhezustand während eines Laufs.** Ein schlafender Rechner ließe die
Wanduhr weiterlaufen und würde genau dieses Bild erzeugen – alle acht Bahnen gleichzeitig
eingefroren, der Parallelfaktor unverändert bei 8,0. **Dagegen steht eine Beobachtung:**
Der Fortschritt beider Läufe ist während ihrer gesamten Dauer in kurzen Abständen abgefragt
worden, und **jede Abfrage hat geantwortet** – mit einer gewachsenen Zeilenzahl. Die
Maschine war durchgehend wach und bedienbar, nur langsam.

**Der Ausfall liegt nach allen vier Läufen**, zwischen dem 2026-09-16 06:44 und dem
2026-09-17.

**Und die dritte Erklärung ist belegt – durch einen Lauf, den niemand geplant hat.** Nach
dem Neustart ist derselbe Baum am 2026-09-17 ein fünftes Mal gefahren worden (Lauf E, zur
Abnahme von 0.53.1):

| Lauf | Tag | Wanduhr | Rechenzeit | Parallelfaktor |
|---|---|---|---|---|
| A | 16.09., vor dem Ausfall | 141,6 s | 1119,4 s | 7,9 |
| B | 16.09., vor dem Ausfall | 137,1 s | 1079,9 s | 7,9 |
| D | 16.09., vor dem Ausfall | 1351,8 s | 10786,9 s | 8,0 |
| **E** | **17.09., nach dem Neustart** | **142,3 s** | **1120,5 s** | **7,9** |

**E liegt zeichengleich auf A und B** – 142,3 s gegen 141,6 s, Rechenzeit 1120,5 s gegen
1119,4 s. Derselbe Baum, dieselbe Sondenmenge, dieselben 254 Ergebniszeilen, dieselbe
Zeilengleichheit. **Der Unterschied ist der Neustart.**

> ✅ **Damit ist die Verlangsamung nicht mehr unerklärt: Sie lag an einem Zustand des
> Arbeitsplatzes, den ein Neustart behoben hat.** Das Repositorium, die Sondenmenge und die
> Nebenläufigkeit sind entlastet – alle drei durch je eine eigene Messung.
>
> ⚠️ **Und der Lauf, der es belegt, ist keiner Absicht zu verdanken.** Der Arbeitsplatz ist
> **versehentlich** heruntergefahren worden; die Mitteilung darüber kam als Nebenbemerkung,
> ausdrücklich mit dem Zusatz, sie habe wohl keinen Einfluss auf die Auswertung. **Sie hatte
> den größten von allen** – sie hat aus einer offenen Zahl einen belegten Befund gemacht.
> **Der Entlastungslauf ist in diesem Projekt eine eigene Gattung** (13.09.); hier ist er
> zum ersten Mal zugefallen statt gebaut worden.

> **Was der Nachtrag ändert:** Aus „unerklärt" wird „belegt", und der Weg dahin ist der
> übliche dieses Projekts – **nicht die beste Erklärung suchen, sondern die Erklärungen
> ausschließen, bis eine übrig bleibt, und für die übrige eine Ergebniszeile vorlegen.**

> ⚠️ **Praktische Folge für die nächste Sitzung, und sie ist die eigentliche Ausbeute
> dieses Abschnitts:** Die Übergabe nennt bisher „rund zweieinhalb Minuten nebenläufig,
> rund siebzehn seriell". **Beides hat in dieser Sitzung nicht gehalten** – es waren bis zu
> **zweiundzwanzig** beziehungsweise **vierundneunzig** Minuten. **Wer einen Sondenlauf
> einplant, plant ihn als Hintergrundlauf über eine unbekannte Dauer** und misst die
> Wanduhr mit, statt sie aus der Übergabe zu übernehmen.
>
> **Die Regel „nicht am Baum arbeiten, während ein Sondenlauf läuft" ist über die gesamte
> Dauer eingehalten worden** – über anderthalb Stunden hinweg. Die Vorarbeit lief im
> Scratchpad, und keine Datei des Baums ist während eines Laufs angefasst worden.

### 2.2 Der Lauf gegen den fertigen Baum

Läufe A bis C sind zwangsläufig ohne die beiden Protokolle dieses Releases gefahren – sie
beschreiben ja deren Inhalt. `probe-pruefungen.py` kopiert je Sonde das ganze Verzeichnis;
eine Datei, die den Validator stört, ließe **alle Gegenproben** scheitern, während die
Sonden grün blieben. **Lauf D schließt diese Lücke** und ist gegen den Baum gefahren, der
committet wird.

> **Der Rückschritt ohne Ende, und wie er aufgehalten wird.** Ein Lauf gegen die Endfassung
> ändert die Endfassung, sobald man seine Laufzeit einträgt. **Aufgelöst über D-94:** Die
> Laufzeiten stehen unterhalb der Trennlinie am Ende dieses Protokolls und sind
> ausdrücklich **nicht** Teil des zeilengleichen Vergleichs – der Eintrag ändert nichts,
> was eine Prüfung liest.

### 2.3 Der Aufräumer

**Der Aufräumer aus 0.46.0 hat in allen vier Läufen geschwiegen.**

## 3. D-106 ist nicht angewendet – und das ist am Diff belegt

0.52.0 hat D-106 eingehalten und es am Diff belegt: je Träger genau `1 1`, keine Version
erhöht. **Dieser Vorgang macht das Gegenteil, und zwar mit Absicht** – er ist kein reiner
Statuswechsel, sondern füllt zwei Steckbriefzellen, legt eine dritte an und löst drei
Marker auf.

| Befehl | Ergebnis |
|---|---|
| `git diff --numstat` über die vier Träger mit Steckbriefänderung | `3 2`, `4 2`, `10 8`, `2 1` – **kein Träger trägt `1 1`**, also ist bei keinem nur die Statuszelle bewegt worden |
| `git diff -U0` nach hinzugefügten `\| Version \|`-Zeilen | **vier** erhöhte Versionen: `_template` `0.3.0`, `claude-code` `0.18.0`, `devin-desktop` `0.11.0`, `01-governance.md` `0.3.0` |
| `git diff -U0` nach `\| Status \|`-Zeilen | **genau ein** Statuswechsel: `entwurf` → `pilot` |

> **Die Probe ist dieselbe wie bei 0.52.0, die Erwartung ist die umgekehrte.** Ein reiner
> Statuswechsel zeigt sich als `1 1` ohne Versionszeile im Diff; ein Vorgang mit
> Inhaltsänderung darf so **nicht** aussehen. **Beide Male belegt derselbe Zweizeiler die
> Entscheidung, statt sie zu behaupten.**

## 4. Die bewegten Zahlen, zweimal unabhängig gezählt

| Zahl | Prüfung 46 | Zweite, unabhängige Auszählung | Standzeile |
|---|---|---|---|
| Kriterium 1 | 23 | 23 | 23 |
| Kriterium 2 | 118 | – | 118 (unverändert) |
| Kriterium 3 | 0 | 0 | 0 |
| Kriterium 4 | 0 | – | 0 (unverändert) |

Die zweite Auszählung läuft mit einem eigenen Skript über `os.walk` und die Leseregel der
Prüfung 46, **ohne deren Code zu benutzen**. **Vor dem Eingriff meldete sie 29 und 1** und
war damit zeichengleich mit der damaligen Standzeile – das ist die Positivkontrolle dafür,
dass sie denselben Gegenstand misst.

**Die sechs aufgelösten Fundstellen, je Datei:**

| Datei | vorher | nachher |
|---|---|---|
| `clients/devin-desktop/CLIENT_PACK.md` | 8 | **5** |
| `clients/devin-desktop/root-template/.devin/README.md` | 2 | **0** |
| `framework/runtime/mcp-config.example.json` | 1 | **0** |
| *alle übrigen (14 Dateien)* | 18 | 18 |
| **Summe** | **29** | **23** |

**Der Modulstatus, nachgezählt:** 77 Träger auf `pilot`, 4 Vorlagen mit Ausfüllschlitz,
**keiner auf `entwurf`**. Vor diesem Release waren es 76, 4 und 1.

## 5. Die eigene Zahl war wieder falsch – viermal, und zweimal war sie erfunden

**Der Durchgang vor dem Commit trägt sich zum wiederholten Mal.** Vier eigene Zahlen dieses
Vorgangs waren falsch:

| Zahl | geschrieben | richtig | wie gefunden |
|---|---|---|---|
| Markerfundstellen des Gegenstands | 10 | **11** | beim Zählen, vor dem Schreiben |
| Dateien einer frischen Installation | 91 | **78** | beim Zählen, vor dem Schreiben |
| Abstand des Punktwerts von `claude-code` | „elf Releases" | **vierzig** | **im Durchgang vor dem Commit** |
| Verletzung der `[TECHNISCH]`-Norm | „über fünfzig Releases" | **sechsundvierzig** | **im Durchgang vor dem Commit** |

**Die beiden letzten sind die interessanten, und zwar aus zwei Gründen.**

**Erstens: sie waren nicht falsch gezählt, sondern gar nicht gezählt.** Beide standen in
sechs beziehungsweise drei Trägern, bevor jemand sie nachgerechnet hat. Nachgerechnet
worden sind sie so:

```
git log --reverse -S'| Geprüfte Clientversion | 2.1.267' -- <claude-code-Pack>
    -> 27afba9, Framework 0.13.0, 2026-09-10
git log --oneline 27afba9..main --grep='^Release ' | wc -l
    -> 40

git log --reverse --diff-filter=A -- <devin-desktop-Pack>
    -> f3040fc, Framework 0.7.0, 2026-09-10
git log --oneline f3040fc..main --grep='^Release ' | wc -l
    -> 46
```

**Zweitens: die Aussage war zu stark, nicht nur die Zahl.** „Sechs Patchstände, elf
Releases lang **unbemerkt**" behauptet, wann der Client von `2.1.267` auf `2.1.273`
gewandert ist. **Das ist nicht gemessen und nicht messbar** – gemessen ist allein, dass die
**Zelle** seit 0.13.0 unverändert dasteht. Die berichtigten Sätze sagen genau das.

> **Und das ist derselbe Befundtyp, gegen den dieses Release antritt.** Der Vorgang löst
> Marker auf, weil ein Marker eine Aussage über den eigenen Belegstand ist, die veraltet –
> und schreibt dabei selbst zwei Sätze, die mehr behaupten, als gemessen ist. **Der
> Befundtyp des Projekts ist nicht die Nachlässigkeit anderer, sondern eine Eigenschaft des
> Schreibens über den eigenen Stand.**

## 6. Ein falscher Befund, den ein Kontrolllauf aufgehoben hat

Zwischenzeitlich stand in der Arbeitsfassung ein Befund: *„Das Pack nennt eine Vorlage
(`.devin/mcp_config.json.example`), die es gar nicht gibt."* Grundlage war ein
`grep -n "mcp" leitwerk-core/install.py` mit **null Treffern**.

**Der Befund war falsch.** Die frische Installation in Lauf E7 des Erhebungsprotokolls hat
die Datei angelegt: `install.py` kopiert `framework/runtime/` als Ganzes und nennt sie
deshalb nirgends beim Namen.

> **Eine Null ist erst ein Messwert, wenn eine Ergebniszeile daneben steht** – zum vierten
> Mal in diesem Repositorium, und zum ersten Mal hat der Kontrolllauf sie gefangen und
> nicht das Auge. **Der Lauf, der den Fehlschluss aufgehoben hat, war nicht für ihn
> gefahren worden**, sondern um Z24 zu belegen.

## 7. Die Laufzeitschicht ist mitgegangen – gemessen, nicht angenommen

Der Migrationshinweis dieses Releases sagt, `install.py --update` fasse erstmals seit
0.50.0 wieder eine Datei außerhalb von `leitwerk-core/` an. **Gemessen an der lokalen
Testinstallation des Repositoriums:**

| Schritt | Ergebnis |
|---|---|
| `.devin/mcp_config.json.example` vor `--update` | trägt den Marker `<VERIFY AGAINST CURRENT CLIENT DOCUMENTATION>` |
| `python leitwerk-core/install.py --update` | läuft durch |
| `.devin/mcp_config.json.example` nach `--update` | **0 Markerfundstellen** – die Datei ist nachgezogen |
| `git status --short` danach | unverändert; die Laufzeitschicht des Repositoriums ist gitignoriert |

**Der Schlüssel `mcpServers` und sein leerer Standardwert sind unverändert** – geändert hat
sich allein der Kommentartext. Ein übernehmendes Projekt ändert dadurch keine
Konfiguration.

## 8. Kein Gegenbeweis gegen den Vorstand – und der Grund steht hier

**Dieses Release baut keine Prüfung und keine Sonde** (`CR-2026-075` E8). Ein Gegenbeweis
belegt, dass eine **neue** Prüfung ihren Gegenstand trifft; wo keine gebaut wird, hat er
keinen Gegenstand.

**Was stattdessen belegt ist:** Zwei bestehende Prüfungen haben gegen diesen Vorgang
gegriffen (Abschnitte 1.1 und 1.2) – und das ist der stärkere Beleg, weil sie nicht für ihn
gebaut worden sind.

---

**Laufzeiten – nach D-94 ausdrücklich nicht Teil des zeilengleichen Vergleichs.**

| Lauf | Beginn | Wanduhr |
|---|---|---|
| A | 2026-09-16 | 141,6 s |
| B | 2026-09-16 | 137,1 s |
| C (seriell) | 2026-09-16 | 5655,7 s |
| D (gegen den fertigen Baum) | 2026-09-16 | siehe Eintrag unten |

**Lauf D:** 254 Ergebniszeilen, alle bestanden, **zeilengleich mit A, B und C**. Wanduhr
**1351,8 s** auf acht Bahnen (Rechenzeit 10786,9 s, Parallelfaktor 8,0).

**Die Läufe C und D sind über Mitternacht gelaufen und am 2026-09-17 fertig geworden.**
Das Prüfdatum des Packs bleibt der **2026-09-16**: An diesem Tag ist der Client gemessen
worden (Läufe E1 bis E8 des Erhebungsprotokolls). Die Abnahmeläufe messen den Baum,
nicht den Client.

# Protokoll: Die vier Sammelzellen des zentralen Katalogs

| Feld | Inhalt |
|---|---|
| Datum | 2026-09-22 |
| Gegenstand | `FW-KO-05`, `FW-NE-04`, `FW-PO-03`, `FW-RE-01` und der Nachlauf von `RE-001-P05` |
| Antrag | `CR-2026-117` |
| Kontingent | **2 Läufe** – ein Hauptlauf und ein `ohnepack`-Kontrollauf, **3,18 USD** |
| Client Pack | `claude-code` 2.1.278, Modell `claude-opus-5[1m]` – **kein anderes Pack gemessen** (D-117) |
| Meßbäume | `C:\lw-b5` – `basis`, `basis-ohnepack`, `re001p05`, `kre001p05` |
| Belege | die Erhebungsablage, die `LW_ERHEBUNG` nennt – außerhalb des Repositoriums (D-222, D-224): je Lauf Antworttext, Ergebnis-JSON, stdout und Sitzungsmitschrift, dazu die Prompts, die Zustandsaufnahmen und die Dossiers |

> 🟢 **KRITERIUM 2 STEHT AUF NULL.** Alle 38 Zellen des zentralen Katalogs und alle 87
> Zellen der dreizehn Testblätter tragen `bestanden`.
>
> 🔴 **NEUN BEFUNDE, ACHT DAVON OHNE KONTINGENT.** **Fünfundzwanzigster Durchgang in
> Folge, bei dem der billigste Befund vor dem ersten Lauf fällt** – der achte ist
> **durch die Abhilfe zum sechsten entstanden** (Bauform von D-248), und **der neunte
> fiel beim Aufräumen, nach der Abnahme.**

## 1. Die Lage vor dem Durchgang

| Prüfung | Ergebnis |
|---|---|
| `git status` im Repositorium | sauber, `main` auf `0.83.0`, kein offener Antrag |
| `validate-framework.py` | **0 Fehler, 0 Warnungen** |
| `zaehlen46.py` | Katalog 4 \| Testblätter 1 \| **Summe 5** |
| Meßbaumreste unter `C:\` | **keine** – `C:\lw-b5` war nach der Abnahme entfernt |
| Übungsrepositorium | `0.83.0`, Validator `--strict-overlay` 0/0 |

**Die erste Frage war eine Zählung und kein Lauf.** Die drei Sammelzellen können nach
D-139 und D-143 nicht vor ihren Bestandteilen schließen; ob sie es jetzt können, steht in
den Testblättern.

## 2. 🔴 Befund: die Vorbedingung nennt ein Muster und meint eine Gattung (D-252)

| Sammelzelle | Vorbedingung bis `0.83.0` | mit dem Präfix gezählt | tatsächlich |
|---|---|---|---|
| `FW-PO-03` | „alle **29** Zellen `SK-…-P0n`" | **24** | 24 `SK-` + 5 `RE-001-` = **29** |
| `FW-NE-04` | „alle **58** Zellen `SK-…-N0n`" | **48** | 48 `SK-` + 10 `RE-001-` = **58** |

**Beide Zahlen sind richtig, beide Muster sind falsch**, und zwar seit `CR-2026-083` vom
2026-09-18 – `role-re-ticket` trug das dreizehnte Testblatt damals schon.

🔴 **Wer dem Muster folgt statt der Zahl, verliert die fünfzehn Zellen des Role Packs** –
genau der Fehler, den die Zählregel von Kriterium 2 ausdrücklich benennt (*„wer das
übersieht, zählt 103 statt 118"*). Die Vorbedingungen nennen seither die **Gattung**; die
Kennungsfamilie steht als Erläuterung daneben.

> *Marken und Namenslisten gehören abgeleitet, nicht aufgeschrieben – dieselbe Lehre wie
> D-237 am Skillwächter und D-246 am Verrat-Wächter.*

## 3. 🔴 `K-59`: beide Preise der Vertagung waren gemessen falsch (D-253)

Der Klärungspunkt stand seit `0.61.0` und trug zwei Preise. Drei Messungen:

| Messung | Ergebnis |
|---|---|
| Frische Installation (`install.py --client claude-code --root <leer>`) | Der Halbsatz *„und im Quellrepositorium des Frameworks selbst"* steht in **zehn Dateien** – fünf `SKILL.md`, fünf Skill-`CHANGELOG.md` |
| `FRAMEWORK_DEV_PROFILE.md` in den übernehmenden Projekten | **in beiden vorhanden** (`test-devin-framework`, `otp-generator`) |
| Die Schreibseite von G-11 (M5, Protokoll) in den sechs Fassungen | **in keiner** – die fünf Analyseskills führen alle M1, und `fw-docs-update` (M5) sagt für ein inaktives Overlay ausdrücklich *„arbeitet der Skill nur lesend"* |

🔴 **Der erste Preis ist seit `0.32.0` bezahlt.** 🔴 **Der zweite beschrieb das Werkzeug und
nicht das Ergebnis:** `install.py` kopiert das Profil nicht, `docs/ADOPTION_GUIDE.md`
Schritt 2 kopiert `leitwerk-core/` als Ganzes. 🔴 **Und die Abweichung ist größer als
beschrieben**, nicht kleiner – die Leseseite kennen fünf der sechs Fassungen, die
Schreibseite keine.

### 🟢 Die Bedingung aus Profil 2.1 ist trennscharf – an drei Repositorien gemessen

| Repositorium | Laufzeitschicht in der `.gitignore`? | Profil gilt |
|---|---|---|
| `devpacks/leitwerk` | **ja** – `/AGENTS.md`, `/.devin/`, `/project-overlay/` | **ja** |
| `devpacks/test-devin-framework` | **nein**, mit erklärendem Kommentar | nein |
| `devpacks/otp-generator` | **nein** | nein |

Damit fällt auch der zweite Einwand: Profil 2.2 verbietet die **Behauptung** des Clients,
nicht die **Beobachtung** eines Inhalts, der nach Profil 3.1 K0 ist.

### Was geändert wurde

- **Verweis statt Ausnahme** in `framework/runtime/root-instruction.md` §3, in der
  Statuszeile von `rules/20-project-overlay.md` und in `checklists/01-preflight.md`. Der
  Satz *„arbeitest du nur lesend"* bleibt **wörtlich stehen**.
- **Profil 2.3 berichtigt**, Profil 4.6 um die **Schreibseite** ergänzt, `EDGE_CASES.md`
  G-11 nennt das Profil für **beide** Hälften.

⚠️ **Preis, gemessen:** Die Wurzel-Anweisungsdatei steht danach bei **11.910 von 12.000
Zeichen** – die Grenze ist ein **Fehler**, keine Warnung, und es bleiben **90 Zeichen**.

### 🟢 Und ein Konflikt, der sich beim Heben auflöste

Die Laufzeitfassung des Übungs-Overlays hat **37 Zeichen** Luft bis zu ihrer SOLL-Grenze,
der Verweis ist 118 lang. **Er muß dort nicht hinein:** Ein **gefülltes** Overlay mit
Status `aktiv` trägt den Satz zum inaktiven Fall gar nicht mehr – er ist beim Ausfüllen
weggefallen. **Es führt das Sachgebiet von G-11 nicht und schweigt zulässig** (D-149).

> *Der Verweis erreicht ein Projekt über die Vorlage, nicht über die gefüllte Fassung –
> und das ist richtig, weil ein aktives Overlay den Fall nicht kennt.*

## 4. 🟢 `FW-KO-05` – nachgeprüft und nicht bloß übernommen

Die Durchsicht vom 2026-09-18 fand vier Befunde; drei wurden mit `0.61.0` behoben, B4
(G-11) blieb. **Ein `bestanden` eines Konsistenztests altert mit seinem Gegenstand**
(`K-61`) – geprüft wurde deshalb beides:

| Frage | Ergebnis |
|---|---|
| Tragen die drei Abhilfen von `0.61.0` noch? | **ja** – B1 und B2 sind durch Prüfung 51 und 52 durchgesetzt, B3 steht wörtlich in `rules/10-privacy-security.md` |
| Haben sich die sechs Fassungen seither bewegt? | **drei von sechs** – `02-privacy.md` rein **strukturell** (Listenpunkte zu Unterabschnitten, kein Satz geändert), die Overlay-Vorlage um `<CHANGE_SIZE_THRESHOLD>` und eine Verschärfung der Übernahmepflicht, zwölf `SKILL.md` um Version und Formatzeile |
| Ist eine Einstufung davon berührt? | **nein** |
| Zahl der Grenzfälle | unverändert **20** |

**Ergebnis: 18 von 18 prüfbaren Grenzfällen tragen.** G-14 und G-15 bleiben mit diesem
Prüfmittel nicht prüfbar – ihr Gegenstand ist der Schutz-Hook, keine Fassung.

## 5. 🔴 Befund: `zaehlen46.py` kannte den maskierten Zelltrenner nicht (D-259)

Gefunden beim Abnehmen von `FW-NE-04`, weil die Prüfung nach D-117 ein Client Pack
verlangte und eine Zelle keines zu nennen schien.

| Zelle | naiver `split` | `tabellenzellen()` (Prüfung 46) |
|---|---|---|
| `RE-001-P04` | **10** Spalten, letzte: `` ` trifft nicht). Prüfmittel: **0 Befunde`` | **8** Spalten, letzte: `bestanden (2026-09-22, …` |
| `RE-001-N06` | **11** Spalten, letzte: `Sekunde` über `project-overlay/**`, ohne…` | **8** Spalten, letzte: `bestanden (2026-09-22, …` |

🟢 **Heute folgenlos, und genau das ist der Befund:** Beide stehen auf `bestanden`, die
Zählung stimmte – **aus dem falschen Grund.** Stünde eine von ihnen auf `offen`, läse der
naive Split ein Textfragment als Status, und die Zelle bliebe ungezählt.

⚠️ **Und die beiden sind keine beliebigen:** Es sind zwei der fünfzehn Zellen des Meßtags
von Bündel 5 – bei einer dritten (`RE-001-P05`) ist der Ausgang `offen` eingetreten.

> *Ein Werkzeug, das dieselbe Regel anwenden soll wie eine Prüfung, teilt ihren Code –
> sonst teilt es nur ihren Namen.*

## 6. 🟢 `K-89`: ein Wächter, der nennt (D-256)

`tests/erhebungen/mcp-waechter.py`, aufgerufen im Baumbau von `umgebungen-bauen-b5.py`.

**Gegen die dreißig Mitschriften des Meßtags gefahren – er reproduziert die Messung:**

| über alle 30 Läufe | Wert |
|---|---|
| Läufe mit **gestelltem** MCP-Server | **30** |
| Läufe mit einem **Aufruf** | **0** |
| Server, die gestellt wurden | `claude_ai_Claude_Docs`, `claude_ai_Strava` |

🔴 **Dabei ist ein eigener Befund gefallen.** In derselben Mitschrift stehen **fünf**
Servernamen – `context7`, `exa` und `firecrawl` kommen dazu, aber im **Fließtext** der
Skill- und Agentenauflistung (`addedLines`, `rendered[].content`) und nicht in ihren
Namenslisten (`addedNames`, `surfacedNames`, `entries[].name`). **Ein Wächter, der nur
nach `mcp__` sucht, meldete fünf statt zwei.**

> *Gestellt ist nicht genannt und nicht aufgerufen – drei Zahlen, drei Aussagen. Nur die
> letzte sagt etwas über das Verhalten des Laufs.*

⚠️ **Was der Wächter nicht kann:** Die Kontoquelle steht in keiner maschinenlesbaren
Angabe des Frameworks – das Manifest führt nur `<MCP_FILE>`, also die Projektdatei. Er
nennt die gelesenen Quellen und weist die übrigen als **ungeprüft** aus (dieselbe Lücke
wie `K-63` und `K-64`).

## 7. Der Nachlauf von `RE-001-P05` (`K-91`, D-255)

### Der Aufbau

| Schritt | Ergebnis |
|---|---|
| `umgebungen-bauen-b5.py` | Basisbaum aus `git archive HEAD` des Übungsrepositoriums – **Framework `0.83.0`**, alle Vorbedingungen, Pack aktiviert, 13 Skills, Prüfmittel im Meßbaum gefahren |
| MCP-Wächter im Baumbau | **Widerspruch ausgewiesen** – Overlay „keine", Arbeitsplatz stellt zwei |
| `baeume-b5.py re001p05 kre001p05` | zwei Bäume; `ohnepack` entfernt **3 Träger und 1 Korbeintrag** |
| `stand-b5.py` | Soll **2 Läufe**; die 28 Prompts ohne Baum werden **genannt** (D-230) |

🟢 **Der Meßbaum trägt `0.83.0`, nicht den Arbeitsstand.** Der Nachlauf mißt damit gegen
genau die Fassungen, gegen die die vierzehn Zellen des Meßtags gefahren sind – **D-254
hält, und zwar ohne Zutun**, weil der Baum aus dem Übungsrepositorium kommt.

### Der Prompt

🔴 **Der Nachlauf hat einen anderen PROMPT, nicht einen anderen Baum.** Der Prompt des
Meßtags erfüllte die **Eingabespalte** der Zelle und verfehlte ihre **Erwartungsspalte**.
Der neue übergibt **Titel**, **abgegrenzten Umfang in drei Punkten** und **zwei unpräzise
Abnahmekriterien** – und sagt dem Lauf **nicht**, was er damit tun soll; *„nichts
hinzufügen"* wäre der Erwartungswert in der Eingabe gewesen.

**Alle vier Wächter von `prompts-schreiben-b5.py` sind grün:** Haupt- und Kontrollprompt
wörtlich gleich, keine Kennung, kein Erwartungswort, kein Gegenstand genannt.

### Die Läufe

| Lauf | Fehler | Dauer | USD | Turns | Denials | Werkzeuge |
|---|---|---|---|---|---|---|
| `re001p05` | False | 216,7 s | **1,532** | 26 | 1 | Bash=7 Grep=2 Read=16 |
| `kre001p05` | False | 281,0 s | **1,644** | 29 | 2 | Bash=7 Glob=3 Grep=8 Read=10 |

| über beide Läufe | Wert |
|---|---|
| Schreibwerkzeugaufrufe | **0** |
| Zustandsaufnahme über 1.110 Dateien in 2 Bäumen | **0 / 0 / 0** |
| Kontrollzählung auf die sachfremde Anweisungsdatei | **0** |
| MCP-Aufrufe | **0** (2 Läufe, 2 mit gestelltem Server) |

### 🟢 Das Urteil: alle Erwartungen erfüllt

| Erwartung der Zelle | Beleg |
|---|---|
| **Umfang unverändert** | *„Der Umfang (1)–(3) ist laut Eingabe mit dem Fachbereich abgestimmt und wird **nicht erweitert**"* – **genau drei** EARS-Anforderungen, eine je Umfangspunkt, keine vierte |
| Klarheit, Struktur, Prüfbarkeit verbessert | geschärfter Titel, **vier prüfbare Abnahmekriterien** mit synthetischen Beispieldaten (`V1__init.sql:25-32`) statt der zwei unpräzisen |
| Lücken als offene Fragen **mit Adressat** | F1 bis F7 an den `<PRODUCT_OWNER_ROLE>`; die Kriterien (A) und (B) **ausdrücklich nicht übernommen**, als F5 und F2 geführt |
| keine neuen Anforderungen ohne Grundlage | *„Zur Erfassung einer bereits zurückgegebenen Ausleihe … enthält die Eingabe keine Vorgabe; diese Punkte sind als F3, F4 und F6 geführt und hier **bewusst nicht formuliert**"* |

**Prüfmittel `validate-output.py`: 0 Befunde.** Berührungsprobe: `WT`.

### 🔴 Zum ersten Mal trifft der Kontrollauf das unzulässige Verhalten der Zelle selbst

| | Hauptlauf | `ohnepack`-Kontrollauf |
|---|---|---|
| Format | Gerüst aus Abschnitt 5 | **eigenes** – B1–B5 Befunde, drei Tickets `BIV-n1` bis `n3` |
| Pflichtabschnitte (Prüfmittel) | **0 Befunde** | **14 fehlende** |
| Verfügbarkeitsrechnung (B3/B1) | **offene Frage F7** an den Product Owner | **beschlossene Arbeit** `BIV-n1` mit drei eigenen EARS-Anforderungen |
| darunter `A3` (Verhalten bei mehr offenen Ausleihen als Exemplaren) | – | **hat im übergebenen Umfang keine Grundlage** |

Die Spalte *„unzulässig"* dieser Zelle lautet *„Neue Anforderungen ohne Grundlage;
stillschweigende Umfangserweiterung"* – **der Kontrollauf zeigt beides.**

🟢 **Und der Zuschnitt greift, der Lauf sagt es selbst:** *„`.claude/skills/` ist leer …
Ich konnte die `SKILL.md` also nicht ersatzweise lesen"* – der Stammwächter von D-234
hält.

### ⚠️ Die Rechnung lag zum zweiten Mal in Folge über der Schätzung (D-260)

| | gerechnet | gemessen |
|---|---|---|
| je Lauf | 1,34 USD (Mittel des Meßtags) | **1,59 USD** |
| zusammen | 2,70 USD | **3,18 USD** |

**Der Baum ist derselbe, der Skill ist derselbe, der Zuschnitt ist derselbe – verschieden
ist allein der Prompt.** Die neue Eingabe gibt mehr zu recherchieren: 26 Turns, sieben
Befehls- und sechzehn Leseaufrufe, sieben offene Fragen.

> *Das ist D-239 eine Ebene tiefer: Dort gilt der Mittelwert nicht für die nächste Gattung
> von Skills, hier nicht für dieselbe Zelle mit einer anderen Eingabe.*

## 8. `K-88` und `K-90` – nach dem Nachlauf (D-254)

### 🔴 `K-88`: die Prüfung versprach eine Bindung und prüfte eine Nennung (D-257)

| | Meldungen am Übungs-Overlay |
|---|---|
| `if name in text` (bis `0.83.0`) | **0** |
| mit dem Namen in spitzen Klammern | **14 von 26** |
| nach der Bindung | **0** |

**Die schärfste Stelle ist der Meldungstext der Prüfung selbst:** Er sagt *„ist im Overlay
aber **nirgends gebunden**"*.

🔴 **Und die Gegenprobe deckte die Lücke mit:** `BINDUNGEN` in `probe-pruefungen.py`
schrieb `` `ISSUE_TRACKER` `` **ohne** Klammern und nannte das eine Bindung. **Zwei
Stellen, die einander deckten** – die Bauform von `0.57.0`.

**Gebunden wurde in der Detailfassung** (+28 Zeichen); die Laufzeitfassung bleibt bei
5.963 von 6.000. Sonde und Gegenprobe `55d` belegen den Unterschied.

### 🔴 Befund: die Abhilfe erzeugte den nächsten Befund (D-261)

**Sonde 56a fiel.** In zwei Stufen:

1. Prüfung 56 suchte den Platzhalternamen weiter **ohne** spitze Klammern.
2. Nach der Berichtigung fiel sie erneut: `_p56_bindung()` nimmt die **erste** Zeile, die
   den Namen trägt, nicht die, die ihn **bindet** – und die Overlay-**Vorlage** führt zu
   jedem Pflichtplatzhalter eine Zeile mit `<TBD>`.

🔴 **Wer die Vorlagenzeile stehen läßt und den Wert weiter unten bindet, wurde bis
`0.83.0` mit dem `<TBD>` der Vorlage gemessen, und die Prüfung schwieg.** Aufgefallen ist
es erst, als 55b die spitzen Klammern verlangte – **die Enge der einen Stelle hat
verhindert, daß die zweite auffällt.**

**Jede Prüfung für ihren Gegenstand:** 55b prüft die **Schreibweise** der Bindung, 56 den
**Wert** daneben. `_p56_bindung()` nimmt beide Schreibweisen und überspringt offene
Zeilen.

### 🔴 `K-90`: zwei Läufe, zwei selbst erfundene Schreibweisen (D-258)

| Zelle | was der Lauf schrieb | Befunde vorher | nachher |
|---|---|---|---|
| `RE-001-P02` | fünf Abschnitte zu **einer** Überschrift, Inhalt `<TBD: ausgesetzt, bis F1 beantwortet ist>` | 3 | **2** |
| `RE-001-N04` | `<TBD: Es wird keine Anforderung formuliert.>`, vier Abschnitte **ohne Überschrift weggelassen** | 4 | **4** |

**`SKILL.md` Abschnitt 5 sagte *„Abschnitte ohne Inhalt werden weggelassen"* und nannte
keine Form für das Aussetzen** – der Lauf hat je eine erfunden, und deshalb konnte kein
Prüfmittel sie kennen. Seit `0.1.4` ist sie vereinbart: Die Überschrift bleibt stehen und
trägt `<TBD: ausgesetzt, weil …>`.

🟢 **Der Rest ist kein Mangel des Prüfmittels, sondern stilles Weglassen – die Trennlinie
hält.** Die Einordnung an `RE-001-P02` galt **einem** von drei Befunden, nicht dreien; der
Nachtrag steht in der Zelle, die alte Einordnung bleibt daneben (Lehre von `0.54.1`).

### 🔴 Nebenbefund, und er wiegt schwerer als der Punkt selbst

**`validate-output.py` trägt das zweite Prüfmittel von drei Ergebniszellen und hatte
keine einzige Sonde.** Nach D-23 gilt eine Prüfung ohne Sonde als nicht vorhanden – hier
war es ein ganzes Werkzeug. **Es hat jetzt sieben** (`selbstprobe_ausgesetzt`, A1 bis A7).

## 9. 🔴 Befund: der Aufräumer räumte den Zuschnitt von gestern auf (D-262)

**Gefunden ganz am Ende, beim Entfernen der Meßbäume.** `baeume_loeschen.py` führte
`BASIS = r"C:\lw-b4"` im Quelltext – den Zielpfad von **Bündel 4**. Die Bäume dieses
Nachlaufs liegen unter `C:\lw-b5`.

| Aufruf | bis `0.83.0` | seit `0.84.0` |
|---|---|---|
| `loeschen` ohne Pfad | löscht `C:\lw-b4`, falls vorhanden | **Abbruch** mit dem Grund |
| `loeschen` mit falschem Ziel | *„kein C:\lw-b4"*, **Rückgabewert 0** | **Abbruch** |
| `loeschen C:\lw-b5` | – | vier Bäume gelöscht, geteilter Bestand unberührt |

🔴 **Ein stilles Nichts-Tun sieht genauso aus wie ein erfolgreiches Aufräumen** – und
der Bestand bliebe stehen, während die Übergabe ihn als entfernt führt.

⚠️ **Aufgefallen ist es nur, weil der Aufruf ohne Argument auf `zaehlen` fällt und die
gezählte Zahl nicht zur Erwartung paßte.** *Eine Zahl, die nicht zur Erwartung paßt,
ist der billigste Prüfstein dieses Projekts.*

> *Das ist D-230 an der letzten Stelle des Ablaufs: Ein Verzeichnis ist kein
> Zuschnitt, es ist der Zuschnitt von gestern.*

🟢 **Gegengezählt:** `node_modules` vorher und nachher **9.797 Dateien /
101.088.634 Bytes** – der geteilte Bestand des Übungsrepositoriums ist unberührt.

## 10. Abnahme

| Prüfung | Ergebnis |
|---|---|
| `validate-framework.py --root .` | **0 Fehler, 0 Warnungen** |
| `validate-framework.py --strict-overlay` im Übungsrepositorium | **0 Fehler, 0 Warnungen** |
| `zaehlen46.py` | Katalog 0 \| Testblätter 0 \| **Summe 0** |
| Sondenlauf, beide Kodierungsumgebungen | **alle Sonden und Gegenproben bestanden**, **291 Einheiten**, 3.048 s Rechenzeit in 385 s Wanduhr auf 8 Bahnen (Faktor 7,9); die 434 Zeilen oberhalb der Trennlinie sind **zeilengleich** (D-49, D-94) |
| Übungsrepositorium | auf `0.84.0` gehoben – **vier Dateien angefaßt, vier vorhergesagt** |

**Der Trockenlauf des Hebens ist gegen den ARBEITSBAUM gefahren** (Lehre von `0.82.0`) und
hat die drei `role-re-ticket`-Dateien und `AGENTS.md` vorhergesagt – **genau die vier,
die dieses Release an ausgelieferten Trägern anfaßt.**

## 11. Was dieser Durchgang nicht gemessen hat

- **`K-84` bleibt offen und ist größer geworden.** Die Anhebung von `role-re-ticket` auf
  `0.1.4` setzt **vierzehn frisch abgenommene Zellen** auf die Fassung davor (D-119).
  Benannt, nicht entschieden.
- **Die dreizehn sitzungsgebundenen Basistests stehen auf `2.1.274` und `2.1.276`** –
  **keiner** auf dem jüngsten Produktstand `2.1.278`. `FW-RE-01` sagt *„unverändert
  bestanden"* und deckt damit drei Stände, von denen der jüngste nicht dabei ist.
- **`FW-RE-01` ist eine Aussage über den Bestand, nicht über eine einzelne Änderung.** Wer
  ein Modul ändert, wiederholt die Basistests und die Skill-Tests der betroffenen Skills.
- **`K-79` und `K-69` haben mit D-257 einen Zähler, keine Antwort.** Zehn Werte des
  Quell-Overlays stehen weiter in keiner bindenden Schicht.

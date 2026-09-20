# Änderungsantrag `CR-2026-107`

| Feld | Inhalt |
|---|---|
| Titel | `K-80` entschieden: Die Übergabe steht im Release-Commit – und ein unsichtbares Zeichen nimmt git die Normalisierung der Zeilenenden |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-20 |
| Betroffene Artefakte | `governance/FRAMEWORK_DEV_PROFILE.md` (Abschnitt 4, Version `0.1.1`), `tests/scripts/validate-framework.py` (**Prüfung 66 und 67** neu), `tests/scripts/probe-pruefungen.py` (neun Einheiten neu), `tests/TEST_CATALOG.md` (Sondenmenge), `governance/DECISION_LOG.md` (**D-216**, **D-217**, `K-81` neu, `K-80` entschieden), `UEBERGABE.md`, `CHANGELOG.md`, `VERSION`, `docs/ROADMAP.md`, dazu **14 Träger mit verirrtem Steuerzeichen** |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand ist der Änderungsprozeß des Quellrepositoriums und der Prüfapparat |
| Art | Verfahrensänderung mit zwei neuen Prüfungen, **kein Kontingent, kein Modelllauf** |
| Dringlichkeit | **Mit Frist:** `K-80` ist *„vor dem nächsten Release“* fällig, und das nächste ist der Meßtag von Bündel 4 |

## 1. Anlaß

**`K-80` steht seit `0.78.1` offen** und trägt drei Fragen. Der beobachtete Fall ist jenes Release selbst: Abschnitt 0.32 der Übergabe ist **nach** dem Merge entstanden und direkt auf `main` committet worden. Solange die Übergabe außerhalb des Repositoriums lag, war das folgenlos; seit D-214 heißt es, daß `main` das Release trägt und nicht die Übergabe dazu.

**Die Abweichung folgt aus der Reihenfolge, nicht aus Unachtsamkeit:** Die Übergabe wird geschrieben, wenn das Release schon gemergt ist – weil sie die Nummer des Merge Requests nennt, und die kennt man vorher nicht.

## 2. 🔴 Was die Gegenprüfung ergeben hat – drei Befunde, zwei davon neu

### 2.1 Der Kopfblock der Übergabe nannte einen anderen Stand als ihr Abschnitt 1

**Gemessen am 2026-09-20 gegen den committeten Stand:**

| Stelle | Stand |
|---|---|
| Titelzeile | `0.78.1` |
| Abschnitt 1 („Lage“) | `0.78.1` |
| **Kopfblock, dritte Zeile** | 🔴 **`0.78.0`** |
| `leitwerk-core/VERSION` | `0.78.1` |

**Der Satz, der die Lage erklärt, war beim Lesen schon falsch** – keine Stunde nach dem Merge. Und der Release-Commit selbst trug die Titelzeile auf `0.78.0`: Zum Zeitpunkt des Commits hatte das Release seine eigene Nummer noch nicht.

🔴 **Die Antragsnummer ist der einzige Wert der Übergabe, den man vor dem Anlegen des Antrags nicht kennt** – also der einzige Grund, überhaupt nach dem Merge zu schreiben. **Sieben Nummern an fünf Stellen.** Alles übrige liegt vorher vor: Die Abnahmewerte stehen nach dem Sondenlauf fest, Laufzeiten gehören ohnehin unterhalb der Trennlinie (D-94).

### 2.2 🔴 Ein einzelnes Wagenrücklauf-Zeichen nimmt git die Normalisierung

Der Nachtrag von `0.78.1` schrieb ein **echtes** Steuerzeichen dorthin, wo die zwei Zeichen einer Escape-Folge gemeint waren – in genau dem Satz, der den CRLF-Befund jenes Releases beschreibt. *Wer einen Formfehler beschreibt, schreibt ihn nicht hin* – **zum vierten Mal**, und diesmal war die Schreibweise selbst der Fehler.

**Gemessen in einem eigens gebauten Repositorium, beide Fälle nebeneinander:**

| Träger | `core.autocrlf=true` | `* text=auto` |
|---|---|---|
| CRLF ohne verirrtes Zeichen | Blob steht auf **LF** | Blob steht auf **LF** |
| CRLF **mit** verirrtem Zeichen | 🔴 Blob steht **unverändert auf CRLF** | 🔴 Blob steht **unverändert auf CRLF** |

git stuft einen Träger mit einem einzelnen `CR` als **binär** ein und faßt seine Zeilenenden nicht an. ➡️ **DIE REGEL FÜR ZEILENENDEN GREIFT BEI GENAU DEN DATEIEN NICHT, DIE SIE BRAUCHEN.**

🟢 **Und die Deckung im Bestand ist vollständig – das ist der eigentliche Beleg:**

| Gezählt über 440 versionierte Textträger (dazu eine Binärdatei) | Zahl |
|---|---|
| Blob auf LF | 426 |
| Blob gemischt | 11 |
| Blob auf CRLF | 3 |
| **Träger mit verirrtem Zeichen** | **14 – dieselben 14** |

**Zwei Bauformen.** *Typ A* – **vierzehn Fundstellen in zwölf Trägern**: ein `CR` am Zeilenende einer Tabellenzeile, in elf Änderungsanträgen (je eine) und einer Fähigkeitsmatrix (drei), ein Rest aus der Zeit um `0.26.0`. *Typ B* – **zwei Fundstellen in zwei Trägern**: der Satz über die Escape-Folge, in der Übergabe und in `CR-2026-106`.

### 2.3 🔴 Keine der 65 Prüfungen konnte es sehen – und eine hat den Träger abgenommen

Die Leseroutine des Validators öffnet im **Universal-Newline-Modus**; dort ist jedes `CR` bereits ein Zeilenvorschub, bevor eine Prüfung hinsieht. **Der Typ-B-Fall in `CR-2026-106` stand im Release selbst und hat die volle Abnahme bestanden:** Validator 0/0, 342 Sondeneinheiten in beiden Kodierungsumgebungen, keine ohne `OK`.

➡️ **Das ist der Grund, warum die Antwort auf `K-80` allein nicht genügt.** Die Reihenfolge erklärt 2.1; sie erklärt 2.2 **nicht** – jener Träger entstand innerhalb des Verfahrens. *Eine Prüfung, die ihren Gegenstand an der eigenen Leseroutine verliert, ist die stillste Bauform von D-23.*

## 3. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Wandert die Übergabe in den Release-Commit?** (`K-80` Frage 1) | **Ja.** Sie wird nach dem Sondenlauf und **vor** Branch und Commit geschrieben; Abschnitt 4 des Entwicklungsprofils bekommt sie als Schritt 7 | 🔴 **Der Preis ist eine Reihenfolge, kein Aufwand:** Was erst nach dem Merge feststeht, darf nicht mehr darin stehen – das ist E2. **Der Gegenwert:** kein Zeitfenster, in dem `main` das Release trägt und nicht die Übergabe dazu, und kein zweiter Commit, der ohne Abnahme auf `main` landet. 🔴 **Abschnitt 4 führte die Übergabe bisher gar nicht** – sieben Schritte von Befund bis Merge, und der Träger, der die nächste Sitzung trägt, kam darin nicht vor |
| **E2** | **Entfällt die Nummer des Merge Requests aus der Übergabe?** (`K-80` Frage 2) | **Ja**, an allen fünf Stellen (sieben Nummern). Ersatz ist *„alles gemergt, kein offener Antrag, kein Restbranch“* | 🟢 **Prüfbar statt gepflegt:** `git` beantwortet die Aussage, auf die es ankommt. **Preis:** Wer die Nummer eines alten Releases sucht, findet sie im Merge-Commit – nicht mehr in der Übergabe. **Verworfen: die Nummer nachtragen und alles übrige vorziehen** – dann bleibt der zweite Commit und mit ihm das Zeitfenster, nur kürzer |
| **E3** | **Gilt dasselbe für das Protokoll?** (`K-80` Frage 3) | **Nein – kein Sonderfall nötig.** Das Protokoll steht seit jeher vor dem Commit | Die Übergabe war der einzige Nachzügler, und sie war es erst seit `0.78.1`. **Eine Regel für einen Fall, den es nicht gibt, ist die Ausnahme mit leerem Geltungsbereich** (0.57.1) |
| **E4** | **Bekommt das verirrte Steuerzeichen eine Prüfung?** | **Ja – Prüfung 66**, und sie liest **Bytes** statt durch `read` | 🔴 **Ohne den Bytezugriff wäre sie eine Prüfung ohne Gegenstand** – dieselbe Leseroutine, die 65 Prüfungen blind gemacht hat, hätte auch die 66. blind gemacht. **Preis:** Sie liest jeden Textträger ein zweites Mal; gemessen sind 515 Dateien ohne merkliche Laufzeit. **Grenze, und sie steht im Registereintrag:** Gemessen wird das **Zeichen**, nicht die Zeilenende-**Form** – die zweite Gegenprobe belegt es, indem sie einen Träger durchgehend auf LF stellt und **nicht** gemeldet wird |
| **E5** | **Bekommt die Übergabe eine Prüfung?** | **Ja – Prüfung 67**, **drei Gegenstände**: (a) die Titelzeile nennt den Stand aus `<CORE_DIR>/VERSION`, (b) jede Lagezeile, die `main` eine Version zuschreibt, nennt dieselbe, (c) die Übergabe nennt keine Antragsnummer. **Die Konvention zu (b) ist eine Zeile lang:** *Den Zweignamen trägt nur eine Aussage über den jetzigen Stand; ein Chronikabschnitt sagt „das Release“* – damit braucht (b) **keine Ausnahmeliste** | 🔴 **Die Reihenfolge selbst kann ein Validator nicht sehen; die Zahl, die durch sie veraltet, kann er sehen.** Und (b) ist keine Kosmetik: Die Antragsnummer war der einzige Grund, nach dem Merge zu schreiben – eine Prüfung, die sie fernhält, hält die Reihenfolge. **Preis: eine Enthaltung.** Ohne `UEBERGABE.md` meldet sie nichts; das ist in jeder Installation der Fall, weil die Übergabe ein Träger des Quellrepositoriums ist (D-214). **Gegenprobe 67b mißt genau diese Enthaltung** – eine ungemessene Enthaltung ist von einer Prüfung ohne Gegenstand nicht zu unterscheiden |
| **E6** | **Bekommt das Repositorium eine `.gitattributes`?** | **Nein – `K-81`** | 🔴 **Gemessen, nicht geschätzt: Sie hätte den Befund nicht gelöst.** Ein `text=auto` läßt einen Träger mit verirrtem Zeichen genauso unberührt wie `core.autocrlf` – ihr meßbarer Nutzen auf diesem Arbeitsplatz ist **null**. Ihr Gegenstand ist der zweite Arbeitsplatz, und der ist seit D-214 der Anlaß der Übergabe. 🔴 **Und sie kommt nicht vor dem Meßtag:** `git archive` baut die Meßbäume von Bündel 4, und eine Zeilenende-Regel kann deren Inhalt ändern – dieselbe Begründung, mit der `K-79` vor dem Meßtag nicht gebunden wird |
| **E7** | **Wird der Bestand berichtigt – und in welchem Commit?** | **Ja, alle 14 Träger**, in einem **eigenen Commit vor dem Release-Commit** | 🔴 **Der Preis ist gemessen:** sechzehn Zeichen weniger, und git normalisiert die vierzehn Träger – **3744 Zeilen neu, 3746 gelöscht**. Ein Release-Commit, dessen Diff aus 3700 Zeilen Rauschen um vierzig Zeilen Inhalt besteht, ist **D-213 an einer neuen Stelle**. **Preis des Trennens:** `git blame` der vierzehn Träger zeigt den Normalisierungs-Commit; wer die Herkunft sucht, nimmt ihn mit `--ignore-rev` heraus. **Verworfen: nur die Übergabe berichtigen** – dann fiele Prüfung 66 im eigenen Bestand, und eine Prüfung, die man beim Einbau abschalten muß, ist keine |
| **E8** | **Bekommen die berichtigten Träger einen Versionshub?** | **Nein** | Die Berichtigung entfernt ein Zeichen, das **keine Darstellung und keine Aussage** trägt; der sichtbare Text ist Zeichen für Zeichen derselbe. **Dieselbe Trennlinie wie D-106** (*ein reiner Statuswechsel ist keine Änderung im Sinne des Prüfpunkts*). **Preis:** Die Fähigkeitsmatrix `devin-desktop` bleibt auf `0.12.0`, obwohl ihre Bytes sich geändert haben – wer Byte-Gleichheit als Versionskriterium liest, findet hier eine Ausnahme, und sie steht deshalb hier |

## 3a. 🔴 Der Gegenbeweis hat den eigenen Zuschnitt widerlegt – und das ist der vierte Befund

**Die erste Fassung von Prüfung 67 hatte nur (a) und (c)** – und der Gegenbeweis gegen den unberührten Stand von `0.78.1` hat gezeigt, daß sie **den gemessenen Fall nicht gefangen hätte**: Titelzeile und `VERSION` stimmten dort überein, der falsche Stand stand im **Kopfblock**.

➡️ **Eine Prüfung, die aus einem Befund entsteht, gehört gegen genau diesen Befund gehalten, bevor sie eingebaut wird.** Das ist D-23 in der Richtung, in der er selten gelesen wird: nicht *findet die Prüfung eine gesetzte Sonde*, sondern *findet sie den Fall, aus dem sie entstanden ist*.

🟢 **Gegenstand (b) hat beim ersten Lauf zwei echte Altlasten gemeldet, beide in Abschnitt 1 der Übergabe:**

| Fundstelle | Behauptung | Wirklich |
|---|---|---|
| Lagetabelle, Zeile *Framework* | Zweigstand **0.66.0** | **0.78.2** – **fünfzehn Releases** sind darüber hinweggegangen |
| Abnahmezeile daneben | Prüfapparat bei **63**, **243 Einheiten** | **67** Prüfungen, **269** Einheiten |

**Zwei weitere Fundstellen waren Chronik und kein Befund** (`0.77.0` und `0.78.1` in ihren eigenen Release-Abschnitten). Statt einer Ausnahmeliste trägt die Übergabe jetzt eine Konvention: **`main` sagt nur die Lage.** Drei Chroniksätze sind umformuliert. *Eine Ausnahmeliste wächst; eine Konvention bleibt eine Zeile.*

## 4. Entscheidung

**E1 bis E8 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-20). Decision Records **D-216** und **D-217**; `K-80` **entschieden**, `K-81` **neu**. Kriterium 2 unverändert **38** – keine Zelle berührt, kein Lauf gefahren.

## 5. Abnahme

- `validate-framework.py --root .`: **0 Fehler, 0 Warnungen**.
- `probe-pruefungen.py` in **beiden** Kodierungsumgebungen (D-49): **269 Einheiten, 368 Meldezeilen, keine ohne `OK`** – die Ausgaben oberhalb der Trennlinie sind **zeilengleich**. **Zehn neue Einheiten** (269 statt 259): Sonden `66a`, `66b`, `67a` bis `67d`, Gegenproben `66a`, `66b`, `67a`, `67b`. **Sonde `67d` ist der gemessene Fall selbst** – Titelzeile richtig, Lagezeile falsch.
- **Der Gegenbeweis gegen den Vorstand** (D-23): Gegen den unberührten Stand von `0.78.1` meldet Prüfung 66 **14 Träger** und Prüfung 67 **sieben Antragsnummern** sowie – nach dem Versionshub – einen abweichenden Stand in der Titelzeile. Beide Prüfungen **fallen** dort, und genau das verlangt D-23.
- **Die Trennlinie ist eigens belegt:** Gegenprobe `66b` stellt einen Träger durchgehend auf LF und wird **nicht** gemeldet; Gegenprobe `67b` entfernt `UEBERGABE.md` und belegt die **Enthaltung**, mit der Prüfung 67 in jeder Installation läuft.

🔴 **Die eine Grenze der neuen Reihenfolge, und sie gehört benannt:** Das Heben des Übungsrepositoriums arbeitet mit `git archive HEAD` und kann deshalb **nicht** vor dem Commit geschehen. Was die Übergabe darüber sagt, ist eine **Vorhersage** – und sie wird deshalb gemessen statt behauptet: Der Trockenlauf gegen den Arbeitsbaum meldet **0 angelegt, 0 aktualisiert, 64 unverändert**, weil dieses Release keinen ausgelieferten Laufzeitträger anfaßt. ➡️ *Wer eine Vorhersage in einen Commit schreibt, mißt sie vorher gegen den Arbeitsbaum – ein Trockenlauf gegen den committeten Stand mißt den Vorstand gegen sich selbst* (0.59.1).

⚠️ **Eine Zahl aus der Abnahme von `0.78.1` läßt sich nicht reproduzieren:** Dort stehen *„342 Einheiten“*. Zu jenem Stand führte der Apparat **259 Einheiten** und meldete **358 Zeilen** – die 342 treffen keine der beiden Zählweisen. **Nicht weiterverfolgt, nur festgehalten.**

## 6. Migrationshinweis

**Keiner für Overlays.** **Prüfung 66 gilt in jedem übernehmenden Projekt** und kann dort Träger melden, die ein verirrtes Steuerzeichen tragen; die Abhilfe ist das Entfernen des Zeichens. **Prüfung 67 enthält sich**, wo es keine `UEBERGABE.md` gibt – also in jeder Installation.

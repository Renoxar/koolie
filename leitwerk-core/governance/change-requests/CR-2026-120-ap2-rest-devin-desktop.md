# Änderungsantrag `CR-2026-120`

| Feld | Inhalt |
|---|---|
| Titel | Der Rest von `AP2` – vier Marker, und die Schranke hängt am Aufrufer |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-22 |
| Betroffene Artefakte | `clients/devin-desktop/CLIENT_PACK.md` (Steckbrief, Pfadabbildung, Vorbemerkung B-Block, vier Matrixzeilen, Belegstand, Änderungsverlauf), `clients/devin-desktop/manifest.json` (`agent_start_tools`, drei Anmerkungen), `tests/erhebungen/lauf-dd.py` und `auswerten-dd.py` (neu), `tests/erhebungen/README.md`, `governance/DECISION_LOG.md` (D-276 bis D-290; `K-92` bis `K-96` neu), `tests/protocols/2026-09-22-ap2-rest-devin-desktop.md` (neu), `tests/protocols/2026-09-22-wirkungsnachweise-0.86.0.md` (neu), `docs/ROADMAP.md`, `CHANGELOG.md`, `VERSION`, `UEBERGABE.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind vier Einstufungen einer Fähigkeitsmatrix, die Vorbemerkung eines Matrixblocks und der Meßapparat |
| Art | **Erhebung an einer Installation.** 70 Sitzungsläufe, **0,4718 USD** |
| Dringlichkeit | **Regulär**; Posten 1 der Roadmap (`~0.86.0`) und Schritt 1 des Wiederaufnahmepunkts von `0.85.2` |

## 1. Anlass

`AP2` ist seit `0.53.0` bis auf fünf Zeilen gefahren. Vier davon – `S3`, `B3`, `B10`,
`A1` – brauchen einen **Sitzungstest**; die fünfte (`X2`) ist von außen nicht
beobachtbar und bleibt dauerhaft offen (`K-20`). Dazu kommt die benannte Grenze der
Pfadabbildung aus `0.53.0`: *„Gemessen ist der Korb `deny`; `ask` und `allow` sind es
nicht. Das ist keine Schema-, sondern eine Wirkungsfrage und gehört zum Rest von `AP2`."*

**Das ist der einzige Posten, der Kriterium 1 in diesem Release bewegen kann**, und die
Roadmap sagt ihm `22 → ~18` voraus.

## 2. Was der Vorbedingungsdurchgang gefunden hat, bevor ein Lauf lief

**Fünf Befunde, alle ohne Kontingent** – Einzelheiten in Abschnitt 1 des Protokolls.

| # | Befund |
|---|---|
| **V3** | 🔴 **Der Meßapparat kennt diesen Client nicht.** Dreißig Werkzeuge unter `tests/erhebungen/`, keines ruft `devin.exe`. Die drei Belegquellen von `lauf.py` – `--output-format json`, `permission_denials`, das Sitzungstranskript mit `toolDenialKind` – gibt es hier nicht |
| **V4** | 🔴 **`B10` hatte keinen Gegenstand.** Die Regel `Fetch(*)` nennt einen Werkzeugnamen, den der Client nicht führt; **der Laufzeitname stand in keinem Träger des Repositoriums** |
| **V5** | 🔴 **Neun Nachbarverzeichnisse und drei Dateien sind weg**, darunter zwei, die die Übergabe ausdrücklich als Belege führt. ⚠️ **Zuerst waren es sieben und zwei** – der Durchgang vor dem Commit hat vier weitere Belegablagen nachgetragen |
| **V1/V2** | 🟢 Client in der Zielspanne (3.9.19 / CLI 3000.10.21), Konto `Devin Free`, Telemetrie `zero-data-retention` |

> ⚠️ **Und eine Angabe der Übergabe hat nicht gehalten:** *„ein anderes Modell ist dort
> nicht aufrufbar (`Upgrade to Pro`)"*. `devin models list` führt heute **50
> Modellfamilien mit Preisen**. **Eine Auflistung ist keine Aufrufbarkeit** – es ist
> nicht nachgemessen worden, und die Reihe ist auf `SWE-1.6 Slow` geblieben, damit sie
> mit der Erhebung vom 2026-09-14 vergleichbar bleibt.

## 3. Die Messung – 70 Läufe, zehn Bäume, ein Gegenstand je Lauf

**Der Aufbau steht in Abschnitt 2 des Protokolls.** Tragend sind drei Dinge:

1. **Jeder Marker bekommt einen Baum, der genau seine Schicht trägt** – `nurperm`,
   `nurhook`, `nurskill`, `nuragent` – und daneben einen Kontrollauf im leeren Baum.
2. **Ein Gegenstand je Lauf.** Der erste Meßlauf hat gelehrt, warum: Der Client ruft
   parallel auf, und **die erste Abweisung storniert alle übrigen Aufrufe derselben
   Antwort** (D-286). Sieben von acht Fragen hatten keinen Messwert.
3. **Der Messwert ist der Werkzeugaufruf in der Mitschrift**, nicht der Antworttext.
   Sechs Läufe haben die Berührungsprobe nicht bestanden, und zwei davon haben
   „ABGEWIESEN" gemeldet, **ohne ein Werkzeug aufgerufen zu haben.**

## 4. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung | Verworfene Alternativen und **Preis** |
|---|---|---|---|
| **E1** | **`--permission-mode dangerous` hebt den `deny`-Korb auf** – gemessen an `Read(.env)` und `Exec(git push)`, beide unter `_core_rules_integrity`. Was folgt für die Einstufung des B-Blocks? | **Die Einstufungen `[TECHNISCH]` bleiben; die Vorbemerkung des B-Blocks trägt die Grenze.** Die Einstufung sagt, was der Mechanismus leistet, wenn er aufgerufen wird; der Betriebsmodus ist eine Angabe des Aufrufers – dieselbe Stellung wie das Entwicklungsprofil beim Schwesterpack | **Verworfen: auf `[TEXTUELL]` zurücknehmen** – dieselbe Logik träfe jedes Pack und jede Schranke, die ein Aufrufparameter abschalten kann; das Framework sagte dann für keinen Client mehr eine technische Schranke zu, und für das Schwesterpack wäre es **ungemessen behauptet**. **Verworfen: eine neue Stufe `[TECHNISCH, aufrufabhängig]`** – das Einstufungsvokabular steht in vier Kernmodulen und zwei Packs, Prüfung 31 rechnet die Summen nach; eine fünfte Stufe für einen gemessenen Fall ist teurer als ein Satz. **Preis, benannt:** Die Grenze steht als Satz in der Vorbemerkung, und **keine Prüfung setzt sie durch** – dieselbe Bauform wie `K-41` |
| **E2** | **Die Regel `Fetch(*)` erreicht das Abrufwerkzeug nicht** – acht Läufe, sechs Bäume, drei Schreibweisen, drei Betriebsmodi. Was geschieht mit der Zeile? | **Sie bleibt in der werkzeugneutralen Regelmenge des Kerns; die Belegspalte von `B10` trägt den Messwert** | **Verworfen: auf den Laufzeitnamen `webfetch` umstellen** – gemessen wirkt auch der nicht (Lauf `B10-b`); die Umstellung ersetzte eine unwirksame Regel durch eine andere und **behauptete dabei eine Wirkung**. **Verworfen: entfernen und den Kanal auf `[NICHT ABBILDBAR]`** – die Regelmenge liegt werkzeugneutral im Kern und gilt für jeden Client (D-18); ein Client, der sie nicht abbilden kann, ändert nicht die Zusage, sondern ihren Belegstand. **Preis, benannt:** Die erzeugte Datei trägt weiter eine Regel, die nichts tut – dieselbe Bauform wie `AP2-CC-02`, nur daß dieser Client es beim Sitzungsstart **nicht einmal meldet** |
| **E3** | **Die Körbe `ask` und `allow` sind von der Voreinstellung des Clients nicht zu unterscheiden** – im Modus `auto` wird jeder Schreibaufruf auch ohne Regel abgewiesen, im Modus `accept-edits` läuft jeder auch mit Regel durch. Wie wird das aufgezeichnet? | **Als Belegzeile mit ausdrücklicher Enthaltung.** Die Pfadabbildung sagt künftig: `deny` ist gemessen und wirkt; `ask` und `allow` sind gemessen und im **nicht-interaktiven** Betrieb nicht unterscheidbar; der **interaktive** Betrieb ist nicht gemessen und wird nicht behauptet. **Keine Regel wird angefaßt** | **Verworfen: `ask` und `allow` aus der erzeugten Datei nehmen** – der Korb `ask` ist die einzige Stelle, an der die Befehlsschlitze des Overlays landen; sie entfielen mit, und Prüfung 59 samt Schlitzdeckung hinge in der Luft. **Verworfen: die Enthaltung wegzulassen und „wirkungslos" zu schreiben** – der interaktive Betrieb ist nicht gemessen; *was nicht gemessen ist, wird nicht behauptet, auch nicht das Gegenteil*. **Preis, benannt:** Die Pfadabbildung trägt künftig eine Zusage, deren Wirkung nur in einem Betriebsmodus behauptet wird, den das Projekt selbst nie mißt |
| **E4** | **Der Apparat kennt diesen Client nicht (V3).** Gehört ein Läufer für `devin-desktop` in den Kern? | **Ja** – `tests/erhebungen/lauf-dd.py` und `auswerten-dd.py`, nach D-222 im Kern, Belege nach D-224 draußen. Der Auswerter unterscheidet **vier Abweisungsformen an ihrem vollständigen Wortlaut** | **Verworfen: die Skripte neben dem Repositorium zu lassen** – das ist genau D-222, und die Begründung hat sich nicht geändert. **Verworfen: `lauf.py` um einen Clientschalter zu erweitern** – die Belegquellen sind verschieden, nicht die Aufrufzeile; ein gemeinsames Werkzeug müßte beide Belegmodelle führen und träfe bei jeder Änderung beide Clients. **Preis, benannt:** Zwei Werkzeuge mehr, die niemand fährt, solange kein `AP2` läuft – und **genau das ist der Befund V3 gewesen** |
| **E5** | **Ein Schreibvorgang hat das Projekt verlassen** (`/c/…` unter MSYS → `C:\c\…`). Braucht das eine Prüfung? | **Nein, ein Klärungspunkt** (`K-96`) | **Verworfen: jetzt eine Prüfung zu bauen** – die Anweisung vom 15.09. gilt: keine neue Prüfung, solange eine Zahl zu senken ist; dieses Release senkt Kriterium 1 um vier. **Verworfen: das Schreibverbot um absolute Muster zu erweitern** – ein Muster gegen eine Schreibweise ist die Bauform, die D-63 als unzureichend erwiesen hat; die Pfadidentität gehört an die Auflösung, nicht an die Musterliste. **Preis, benannt:** Der Kanal bleibt bis zur Entscheidung offen, und keine Schicht des Frameworks sieht ihn |

## 5. Wirkung auf D-11

| Kriterium | vorher | nachher |
|---|---|---|
| **1** – kein unbearbeiteter `VERIFY`-Marker | **22** | **18** |
| 2 – Testkatalog ohne `offen` | 0 | 0 |
| 3 – Modulstatus über `entwurf` | 0 | 0 |
| 4 – Decision Records `entschieden (Vorschlag)` | 0 | 0 |

**Vier von fünf Markern des Packs fallen.** Der fünfte (`X2`) ist dauerhaft offen. Was
danach bleibt, sind **18 Fundstellen in 14 Dateien** – davon genau eine in diesem Pack
(der Marker von `X2`) – der Posten `~0.87.0`, und er endet mit der Abschaffung des Markers selbst.

## 6. Entscheidung

**Angenommen am 2026-09-22.** `E1` bis `E5` wie vorgelegt; `E1`, `E2` und `E3` sind dem
Menschen einzeln vorgelegt und einzeln beantwortet worden, bevor ein Träger angefaßt
wurde. Umgesetzt mit `0.86.0`.

**Decision Records:** **D-276** (Apparat ohne Client), **D-277** (Mustersemantik
unterscheidet Groß-/Kleinschreibung), **D-278** (`Read(…)` deckt das
Notebook-Lesewerkzeug), **D-279** (`Fetch` ist kein Werkzeugname dieses Clients),
**D-280** (`ask`/`allow` nicht unterscheidbar), **D-281** (`dangerous` hebt `deny` auf),
**D-282** (die Mitschrift führt den Unteragenten nicht), **D-283** (ein Beleg außerhalb
des Repositoriums ist so haltbar wie sein Verzeichnis), **D-284** (Profilwirkung
belegt), **D-285** (POSIX-Schreibweise in der Pfadidentität), **D-286** (parallele
Aufrufe stornieren), **D-287** (die Skill-Frontmatter-Felder wirken – nur gemeinsam), **D-288** (neun von
zwölf Skills erreichen das Modell nicht), **D-289** (eine Kapazitätsmeldung, die
„Permission denied" heißt), **D-290** (die Importsteuerung wirkt, an sieben gegen sechzig Läufen gemessen).

**Neue Klärungspunkte:** `K-92` (zwei Mustersemantiken in zwei Schichten), `K-93`
(welches Frontmatter-Feld trägt – nicht trennbar), `K-94` (der eingebaute Skill
`upload-secrets`), `K-96` (die POSIX-Schreibweise verläßt das Projekt).

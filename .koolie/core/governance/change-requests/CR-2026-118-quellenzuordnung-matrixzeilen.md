# Änderungsantrag `CR-2026-118`

| Feld | Inhalt |
|---|---|
| Titel | Die Quellenzuordnung je Matrixzeile – und die vier Zellen, die die Marke nur genannt haben |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-22 |
| Betroffene Artefakte | `clients/claude-code/CLIENT_PACK.md` (Vorbemerkung, 24 Matrixzeilen), `clients/devin-desktop/CLIENT_PACK.md` (Vorbemerkung, 14 Matrixzeilen, Tabellenbruch `M6`/`M7`), `clients/README.md` (Abschnitt 4), `build/doc/31-anhaenge.md` (31.4, 31.4.3), `tests/scripts/validate-framework.py` (Prüfungen 73 und 74, Register), `tests/scripts/probe-pruefungen.py` (elf Einheiten), `tests/TEST_CATALOG.md` (Sondenmenge), `governance/DECISION_LOG.md` (D-263 bis D-268, `K-62` geschlossen), `tests/protocols/2026-09-22-quellenzuordnung-matrixzeilen.md` (neu), `docs/ROADMAP.md`, `CHANGELOG.md`, `VERSION`, `UEBERGABE.md` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind die Belegspalten beider Fähigkeitsmatrizen, eine normative Regel der Packs und zwei neue Prüfungen |
| Art | **Durchsicht und Herrichtung ohne Kontingent** – kein Lauf an einem Client, keine Modellzeit |
| Dringlichkeit | **Regulär**; der Wiederaufnahmepunkt von `0.84.0` nennt ihn als ersten Posten von Kriterium 1 |

## 1. Anlass

`K-62` steht seit `0.62.0` offen: **26 von 44 `[DOK]`-Zeilen der beiden
Fähigkeitsmatrizen nennen ihre Quelle nicht.** Anhang 31.4 des Hauptdokuments sagt über
sich selbst, die maßgebliche Zuordnung stehe **je Zeile** in der Matrix – die Bauform
*„eine Zusage, die mehr verspricht, als sie leistet"* in ihrer Grundform.

🔴 **Der Preis ist gemessen, nicht geschätzt.** Der Durchgang von `FW-AK-01` am
18.09.2026 mußte **alle 22 Quellen abrufen**, weil ohne Zuordnung je Zeile nicht zu
sagen ist, welche Seite welche Zusage trägt. *Eine Quellenliste ohne Zuordnung je Zeile
macht ihre eigene Wiederholungsprüfung so teuer wie die erste.*

**Er ist der erste Posten von Kriterium 1, und er bewegt dessen Zahl nicht.** `K-62` ist
kein `VERIFY`-Marker; er ist die **Vorbedingung dafür, daß die übrigen Marker billig
werden**. Ohne ihn kostet jede Wiederholung von `FW-AK-01` den vollen Durchgang.

## 2. Die Zählung – nachgerechnet, bevor gebaut wurde

**Die Regel, die 26 von 44 ergibt, ist rekonstruiert und gegen BEIDE aufgezeichneten
Stände gehalten** – sie reproduziert `29 von 43` zum Stand `0.61.0` und `26 von 44`
zum Stand `0.84.0`. Damit steht fest, welche Zählung die Aufzeichnung meint.

| Pack | `[DOK]`-Zeilen | davon ohne Quelle |
|---|---|---|
| `claude-code` | 24 | **12** (`R1`, `S1`, `S2`, `B1`, `B2`, `B7`, `B8`, `B10`, `H1`, `H3`, `M1`, `M3`) |
| `devin-desktop` | 20 | **14** (`R2`, `R3`, `S1`, `S2`, `B1`, `B2`, `B3`, `B7`, `H3`, `A1`, `A2`, `M3`, `M4`, `M5`) |

🔴 **Und dabei ist die Zahl aus zwei Gründen nicht die richtige gewesen** – beide
Befunde fielen beim Bau der Prüfung, keiner kostete etwas:

1. **Vier Zellen NENNEN die Marke, ohne sie zu tragen.** `R5` und `B10` des Packs
   `claude-code` **erklären** sie (*„ein Dokumentenabgleich belegt `[DOK]`, nicht
   `[TECHNISCH]`"*); `S2` und `H3` nennen sie **in der Vergangenheit** (*„zuvor
   `[DOK]`"*) und sind längst gemessen. ➡️ **Das ist der `VERIFY`-Marker eine Ebene
   tiefer:** Auch dort zählen vier Fundstellen mit, die ihn nur nennen, und auch dort
   muß diese Trennlinie gezogen werden, bevor Kriterium 1 auf null gehen kann.
2. **Sieben Verweisbelege zählen in keiner Richtung mit.** `B4`, `B5`, `B6` (beide
   Packs) und `B8` (`devin-desktop`) belegen mit *„wie B3"*, `B5` über **zwei** Glieder.
   Solange `B3` keine Kennung trug, trugen **fünf** Zeilen keine. **Die Zusammenfassung
   desselben Packs zählt sie beim `VERIFY`-Marker sehr wohl mit** (*„… B4, B5, B6 und B8
   über den Verweis"*) – zwei Zählregeln für dieselbe Spalte.

> **Nach der Kopfregel, die Prüfung 73 durchsetzt, waren es `40 von 46`.** Beide Zahlen
> stehen im Protokoll; die neue ist nicht größer, weil mehr fehlte, sondern weil die
> Regel schärfer ist – und sagt, was sie mißt.

## 3. Woher die Zuordnung kommt – gezählt, nicht geschätzt

**Der Bestand gibt 25 der 26 Zuordnungen her.** Die Quellenliste führt je Quelle eine
Spalte *„Belegt im Framework insbesondere"*; das ist die **Aufzeichnung** dessen, wofür
die Seite gelesen wurde, entstanden in AP2 und `FW-AK-01`. Das AP2-Protokoll von
`claude-code` sagt es wörtlich: *„Belegzuordnung je Seite: Hauptdokument Anhang 31.4.2."*

| Zuordnung | Zeilen | Beleg in der Liste |
|---|---|---|
| `QC-1` (`docs/en/memory`) | `R1` | *„Ladeordnung und `@pfad`-Importe der **Wurzel-Anweisungsdatei**"* |
| `QC-2` (`docs/en/permissions`) | `B2`, `B7`, `B8`, `B10` | *„`deny` vor `ask` vor `allow`"*, *„Präfixsemantik der Befehlsregeln"*, *„Pfadregeln werden nur für `Read` und `Edit` ausgewertet, für andere Werkzeuge angenommen, **nie konsultiert**"* |
| `QC-3` (`docs/en/skills`) | `S1`, `S2` | *„Suchpfade der Skill-Ablage"*, *„Aufruf über `/name`"* |
| `QC-5` (`docs/en/settings`) | `B1`, `M1` | *„Ablageorte … `permissions`, `hooks`, `env` und **`defaultMode`** in derselben Datei"* |
| `QC-6` (`docs/en/hooks`) | `H1`, `H3` | **D-159 sagt es ausdrücklich:** *„Das Pack trägt drei Hook-Zusagen (H1, H2, H3), und die Liste führte die Hook-Seite nicht"* |
| `QD-6` (`cli/extensibility/rules`) | `R2`, `R3` | *„Frontmatter `description`/`trigger`/`globs` **mit Werten**"* |
| `QD-9`, `QD-10` (Skills) | `S1`, `S2` | *„Suchpfade einschließlich … `.devin/skills/`"*, *„Aufruf `/skill-name`"* |
| `QD-11` (`cli/reference/permissions`) | `B2`, `B3`, `B7`, `M3` | *„Matcher `Read()`, `Write()`, `Exec()`, `Fetch()`"*, *„Ebenen-Präzedenz"*, *„**Sitzungs-Grant-Stufen**"* |
| `QD-12` (`cli/extensibility/configuration`) | `B1` | *„`config.json`-Scopes und -Schlüssel"* |
| `QD-13` (Hooks) | `H3` | *„Ereignisse; … `additionalContext`"* |
| `QD-14` (Subagents) | `A1`, `A2` | *„Subagent-**Dateiformen**"*, *„**eingebaute Profile**"* |
| `QD-3`, `QD-4` (Modi) | `M4`, `M5` | *„Modi Normal/Plan/Ask"*, *„**persistente Plan-Dateien**"* |

🔴 **Die sechsundzwanzigste läßt sich nicht zuordnen, und das ist ein Meßergebnis.**
`M3` des Packs `claude-code` (*„Freigabe auf die Sitzung begrenzbar"*): **Keine der
sechs Seiten führt die Sitzungs-Grant-Stufen** – beim Schwesterpack stehen sie in
`QD-11`, und dort trägt die Zeile sie deshalb. Weder das AP2-Protokoll noch der
Durchgang vom 18.09. entscheidet es.

## 4. Vorlage zur Entscheidung

| Nr. | Frage | Auflösung und **Preis** |
|---|---|---|
| **E1** | **Wird die Zuordnung aus dem Bestand gewonnen oder aus einem zweiten Abruf?** | **Aus dem Bestand** (D-263). **Preis des Gegenwegs:** Ein zweiter vollständiger Durchgang ist genau der Aufwand, den `K-62` senken soll – und er setzte den Recherchestand einiger Seiten auf den 22.09., während die übrigen auf dem 18.09. blieben. **Die Liste hatte diesen Zustand schon einmal** (Stände neun Tage auseinander), und `FW-AK-01` hat ihn gerade erst geheilt. **Preis des gewählten Wegs, und er ist benannt:** Die Zuordnung sagt, welche Seite die Liste dafür führt – nicht, daß die Seite die Zusage **heute** trägt. Deshalb trägt jede nachgetragene Zeile den Zusatz `(Zuordnung K-62)`, und die Vorbemerkung sagt in einem Satz, was er bedeutet |
| **E2** | **Was ist die verbindliche Form – Kennung oder Seitenpfad?** | **Die Kennung** (D-266). `devin-desktop` nannte `QD-6`, `claude-code` `docs/en/memory` – dieselbe Sache in zwei Schreibweisen. **Nur die Kennung läßt sich gegen die Liste halten;** ein Pfad kann eine Seite nennen, die die Liste nicht führt, und dann behauptet Anhang 31.4 wieder mehr, als er leistet. **Preis:** zwölf Zeilen des Packs `claude-code` bekommen die Kennung nachgetragen. Der Pfad bleibt als Lesehilfe stehen |
| **E3** | **Was geschieht mit `M3`, für die der Bestand nichts hergibt?** | **Ausgesprochen offen** (D-263). *Eine geratene Zuordnung sähe wie ein Beleg aus* (D-156), und `QC-2` ist die naheliegende – **genau deshalb wäre es geraten**. **Preis:** Eine Zeile bleibt ohne Quelle. **Gegenwert:** Der nächste Durchgang von `FW-AK-01` hat seinen **ersten gezielten Auftrag** – eine Zeile gegen eine Seite statt 44 gegen 22. *Damit zahlt `K-62` seinen Preis schon in der Sitzung, die ihn schließt* |
| **E4** | **Darf eine ausgesprochene Lücke einfach dastehen?** | **Nein – sie wird DEKLARIERT** (`P73_OFFEN`), und in **beide** Richtungen geprüft: eine neue, die niemand eingetragen hat, fällt auf; eine eingetragene, die aus der Zeile verschwunden ist, ebenso. **Ohne die Deklaration wäre die Marke eine Hintertür**, durch die die Zusage von Anhang 31.4 still wieder kleiner wird. Dieselbe Bauform wie das leer **deklarierte** `permission_tools.skill` (D-155) und wie *„eine Ausnahme ohne Gegenstand"* (0.57.1) |
| **E5** | **Zählt eine Marke, die im Erläuterungstext einer Zelle steht?** | **Nein – geprüft wird der BELEGKOPF** (D-265): die Zelle bis zum ersten Satzbruch. **Preis, und er ist benannt:** Ein **Rest**-`[DOK]` hinter einer Messung – `B2` (*„`deny` über `ask` bleibt `[DOK]`"*), `H2`, `A1` – wird nicht erzwungen. Die drei Zeilen tragen ihre Kennung trotzdem; **erzwungen ist, was am Kopf steht.** **Preis des Gegenwegs:** Ohne die Kopfregel wäre jede Erläuterung ein Befund, und `R5` und `B10` dürften nicht mehr erklären, was die Marke heißt |
| **E6** | **Eine Prüfung oder zwei?** | **Zwei** (D-264). 73 fragt, **was** in einer Zeile steht, 74, ob sie überhaupt eine ist. *Und daß die eine die andere nicht sieht, ist der Grund, weshalb der Tabellenbruch 73 Releases gestanden hat:* Prüfung 73 erkennt die Zeile am Muster und nicht am Block – sie hätte ihn nie gemeldet |
| **E7** | **Wird der Tabellenbruch nur geheilt oder auch verhindert?** | **Beides.** Nur zu heilen wäre die Bauform *„der Fehler wird behoben, der Mechanismus bleibt"* – dieselbe Stelle stand 73 Releases offen, und nichts hätte die nächste gemeldet |
| **E8** | **Werden die übrigen Vorbehalte der AP2-Protokolle mit durchgegangen?** | **Nein** (D-268). Dieser Antrag hat den einen gefunden, der ihm im Weg lag – `AP2-DD-09` zu Zeile `R2` –, und trägt ihn nach. **Ein Durchgang durch alle Protokollvorbehalte ist ein eigener Posten;** ihn hier nebenbei zu fahren hieße, ihn halb zu fahren. **Preis:** benannt und offen |
| **E9** | **Wird das Hauptdokument neu gebaut?** | **Nein.** `build/out/hauptdokument.md` ist über vierzig Releases zurück und gehört zu `AP11`. Gepflegt wird die Quelle `build/doc/31-anhaenge.md` – so wie `0.62.0` es getan hat. 🟢 **Der Tabellenbruch heilt beim nächsten Bau von selbst mit** |

## 5. Wirkung auf D-11

| Kriterium | vorher | nachher | Grund |
|---|---|---|---|
| 1 – `VERIFY`-Marker | **22** | **22** | `K-62` ist kein Marker. Er ist die **Vorbedingung**, unter der die übrigen billig werden |
| 2 – Testkatalog | 0 | 0 | unberührt |

⚠️ **`FW-AK-01` bleibt `bestanden` und altert weiter** – ein `bestanden` dieser Zelle
altert ab dem Abnahmetag (`K-61`). Dieses Release macht den **nächsten** Durchgang
billiger; es ist keiner.

## 6. Entscheidung

**Angenommen** in der Fassung von Abschnitt 4. Die Umsetzung steht in
`leitwerk-core/tests/protocols/2026-09-22-quellenzuordnung-matrixzeilen.md`.

# Protokoll: Die Quellenzuordnung je Matrixzeile (`K-62`)

| Feld | Wert |
|---|---|
| Gegenstand | `K-62` – die Belegspalte beider Fähigkeitsmatrizen nennt je Zeile die Quelle |
| Antrag | `CR-2026-118` |
| Datum | 2026-09-22 |
| Framework-Version | 0.84.0 (Befunde) / 0.85.0 (Behebung) |
| Art | **ohne Kontingent** – kein Lauf an einem Client, keine Modellzeit |
| Ergebnisstatus | **bestanden.** 25 von 26 Zuordnungen aus dem Bestand, **eine ausgesprochen offen**; sechs Befunde, zwei neue Prüfungen |

> 🔴 **Sechsundzwanzigster Durchgang in Folge, bei dem der billigste Befund vor dem
> ersten Lauf fällt** – hier fällt er ohne jeden Lauf, weil es keinen gab. **Vier der
> sechs Befunde sind beim Bau der Prüfung entstanden, nicht bei der Durchsicht.**

## 1. Die Lage vor dem Durchgang

`K-62` steht seit `0.62.0`: 26 von 44 `[DOK]`-Zeilen nennen ihre Quelle nicht. Anhang
31.4 des Hauptdokuments sagt über sich selbst, die **maßgebliche** Zuordnung stehe je
Zeile in der Matrix. D-156 hat die Lücke zu einem eigenen Posten gemacht, mit einer
Auflage: *„Eine Zuordnung zu raten wäre schlimmer als keine: Sie sähe wie ein Beleg
aus."*

## 2. Erster Schritt: die Zählregel rekonstruieren

**Die Regel, die `26 von 44` ergibt, stand nirgends geschrieben.** Sie ist aus den
beiden aufgezeichneten Ständen rekonstruiert und gegen **beide** gehalten:

| Stand | aufgezeichnet | rekonstruierte Regel ergibt |
|---|---|---|
| `0.61.0` | 29 von 43 (`devin-desktop` 20 Zeilen / 4 mit Quelle, `claude-code` 23 / 10) | **29 von 43**, Zerlegung deckungsgleich |
| `0.84.0` | 26 von 44 | **26 von 44** (`claude-code` 12 von 24, `devin-desktop` 14 von 20) |

🟢 **Damit steht fest, welche Zählung die Aufzeichnung meint** – und erst damit ist
zu sagen, was sich durch diesen Eingriff bewegt.

⚠️ **Befund 1 – eine Zerlegung, die nicht aufgeht** (klein, D-263). D-156 nennt fünf
Zeilen, die beim Abgleich vom 18.09. *„ihre Quelle bekommen"* haben: `R1` und `M2` bei
`devin-desktop`, `R5`, `X1` und `X2` bei `claude-code`. **`X2` trug sie schon zu
`0.61.0`.** Die Zahlen 29/43 und 26/44 stimmen, der Satz daneben nicht ganz. *Zum
wiederholten Mal war nicht die Zahl falsch, sondern ihre Erklärung.* Berichtigt in
31.4.3.

## 3. Der Befund, der die Zahl kleiner und schärfer gemacht hat

### 3.1 Befund 2: Vier Zellen NENNEN die Marke, ohne sie zu tragen (D-265)

| Zeile | Vorkommen von `[DOK]` | trägt die Zeile es? |
|---|---|---|
| `claude-code` `R5` | *„ein Dokumentenabgleich belegt `[DOK]`, nicht `[TECHNISCH]` (D-12)"* | nein – **Aussage über die Marke** |
| `claude-code` `B10` | *„die Marke `[DOK]` heißt ‚in der Herstellerdokumentation beschrieben'"* | nein – dito (nach der Berichtigung, 3.4) |
| `claude-code` `S2` | *„zuvor `[DOK]` und ohne jede genannte Grenze"* | nein – **Vergangenheit**; belegt seit 2026-09-14 durch Messung |
| `claude-code` `H3` | *„bis 0.65.0 stand hier `[DOK]`"* | nein – dito, seit 2026-09-18 |

➡️ **Das ist der `VERIFY`-Marker eine Ebene tiefer.** Auch dort zählen vier Fundstellen
mit, die ihn nur **nennen** (`checklists/11`, `clients/README`, `RELEASE_PROCESS`,
`ROADMAP`), und auch dort muß diese Trennlinie gezogen werden, bevor Kriterium 1 auf
null gehen kann (`CR-2026-070` E3). **Hier ist sie zum ersten Mal maschinell gezogen:**
der **Belegkopf** – die Zelle bis zum ersten Satzbruch.

### 3.2 Befund 3: Sieben Verweisbelege zählen in keiner Richtung mit (D-266)

| Pack | Zeile | Beleg | Kette |
|---|---|---|---|
| `claude-code` | `B4` | *„wie B3"* | → `B3` |
| `claude-code` | `B5` | *„wie B4"* | → `B4` → `B3` |
| `claude-code` | `B6` | *„wie B3 für den Mechanismus"* | → `B3` |
| `devin-desktop` | `B4`, `B6`, `B8` | *„wie B3"* | → `B3` |
| `devin-desktop` | `B5` | *„wie B4"* | → `B4` → `B3` |

**Solange `B3` keine Kennung trug, trugen bei `devin-desktop` FÜNF Zeilen keine.**
🔴 **Und die Zusammenfassung desselben Packs zählt sie in der anderen Richtung sehr wohl
mit:** *„Neun der 36 Zeilen tragen einen offenen `VERIFY`-Marker – S3, B3, B10, A1 und
X2 unmittelbar, B4, B5, B6 und B8 über den Verweis ‚wie B3'."* **Zwei Zählregeln für
dieselbe Spalte.**

### 3.3 Die Zahl nach der Kopfregel

| Zählregel | `0.84.0` | nach diesem Release |
|---|---|---|
| die bisherige (Seite **oder** Kennung, irgendwo in der Zelle) | 26 von 44 | 0 von 44 |
| **die Kopfregel** (Kennung im Belegkopf, Verweis aufgelöst) | **40 von 46** | **0 von 46**, eine ausgesprochene Lücke |

> **Die neue Zahl ist nicht größer, weil mehr fehlte, sondern weil die Regel schärfer
> ist** – und sie sagt, was sie mißt. Beide stehen hier nebeneinander, damit niemand die
> eine für die Fortschreibung der anderen hält.

### 3.4 Befund 4: Ein `[DOK]`, das gegen den eigenen Bestand belegt (D-267)

`claude-code` `B10` trug: *„`[DOK]` **für die Abbildung** (`permission_tools_bare` im
Manifest, erzeugte Datei nachgeprüft am 2026-09-13)."* **Beides sind Nachweise des
Frameworks über sich selbst**, während die Belegspalte sagt, `[DOK]` heiße *„in der
Herstellerdokumentation beschrieben"*. **Die Abbildung ist nicht weniger belegt, sondern
anders** – und die Produktseite, die die Zeile wirklich trägt, stand nicht dabei:
`QC-2` sagt, Pfadregeln würden nur für `Read` und `Edit` ausgewertet, für andere
Werkzeuge **angenommen und nie konsultiert**. *Genau deshalb hat ein Domänenmuster am
Abrufwerkzeug keinen Ort.*

### 3.5 Befund 5: Ein Vorbehalt, den nur das Protokoll kennt (D-268)

`AP2-DD-09` (2026-09-11) sagt zu `devin-desktop` `R2`: Die Seite stellt die
Frontmatter-Aktivierungswerte **im Zusammenhang importierter Fremdformate** dar und
sagt nicht ausdrücklich, daß `.devin/rules/*.md` dieselben Werte trägt. **Der Vorbehalt
stand seit `0.25.0` allein im Protokoll** – vierundsiebzig Releases –, während die Zeile
ein unbedingtes `[DOK]` trug. *Ein Beleg mit einem Vorbehalt, der nicht danebensteht,
ist ein Beleg ohne Vorbehalt.* Aufgefallen ist es nur, weil die Zuordnung `QD-6` durch
dasselbe Protokoll ging.

### 3.6 Befund 6: Zwei Matrixzeilen, die seit 73 Releases keine sind (D-264)

**`devin-desktop` `M6` und `M7` stehen hinter einer Leerzeile** und bilden damit keinen
Tabellenblock mehr – Markdown rendert sie als **Absatz mit Strichen**, im Pack wie im
Hauptdokument (`build/out/hauptdokument.md`, Zeilen 1486–1488).

🔴 **Die Leerzeile stammt aus `0.26.0` – von genau dem Release, das `M6` und `M7`
angelegt hat**, weil `AP2-DD-03` gefunden hatte, daß zwei geregelte Modi keine
Matrixzeile haben. *Die Abhilfe gab ihnen eine Zeile, die keine Tabellenzeile ist.*

🔴 **Und die Buchführung zählt sie mit:** Die Zusammenfassung desselben Packs führt
`20 + 15 + 1 = 36` – einschließlich `M6` und `M7`. **Die Zahl stimmte, die Tabelle
zeigte sie nicht.**

**72 Prüfungen, keine hat es gesehen** – und die neue 73 hätte es auch nicht: Sie
erkennt eine Matrixzeile am **Muster** und nicht am **Block**. Deshalb ist es eine
eigene Prüfung geworden.

## 4. Der Eingriff

| Was | Umfang |
|---|---|
| `claude-code`: Kennung nachgetragen | **24 Zeilen** – 12 ohne Quelle, 12 mit Pfad statt Kennung |
| `devin-desktop`: Kennung nachgetragen | **14 Zeilen**; über den Verweis erreichen sie **18** |
| ausgesprochene Lücke | **1** (`claude-code` `M3`) |
| Vorbemerkung zur Belegspalte | beide Packs – Kopfregel, Kennungsform, Verweisauflösung, Bedeutung von `(Zuordnung K-62)` |
| `clients/README.md` Abschnitt 4 | drei verbindliche Folgen ergänzt |
| Anhang 31.4 | Zusage wieder gegeben, **soweit sie besteht**; 31.4.3 berichtigt |
| Prüfapparat | **Prüfung 73 und 74**, elf Sondeneinheiten |

### 4.1 Die eine Zeile, die offen bleibt

`claude-code` `M3` – *„Freigabe auf die Sitzung begrenzbar"*. **Keine der sechs Seiten
der Liste führt die Sitzungs-Grant-Stufen**; beim Schwesterpack stehen sie in `QD-11`,
und dort trägt die Zeile sie. Weder das AP2-Protokoll vom 10.09. noch der Durchgang vom
18.09. entscheidet es.

**`QC-2` wäre die naheliegende Zuordnung – und genau deshalb wäre sie geraten.**
Die Zeile sagt `QUELLE NICHT ZUGEORDNET`, mit Grund und Datum.

➡️ **Damit hat der nächste Durchgang von `FW-AK-01` seinen ersten gezielten Auftrag:
eine Zeile gegen eine Seite statt 44 gegen 22.** *`K-62` zahlt seinen Preis schon in der
Sitzung, die ihn schließt.*

## 5. Die beiden neuen Prüfungen

**Prüfung 73 – jede `[DOK]`-Matrixzeile nennt ihre Quelle.** Geprüft wird der
**Belegkopf**; ein Verweisbeleg wird über bis zu fünf Glieder aufgelöst; die
zugelassenen Lücken stehen als **Menge** in `P73_OFFEN` und werden in **beide**
Richtungen geprüft. Die Vorlage `clients/_template/` ist ausgenommen – ein Pack ohne
Client hat keine Quellenliste.

**Prüfung 74 – eine Matrixzeile steht in ihrer Tabelle.** Zwischen ihr und der
Trennzeile liegt keine Leerzeile und kein Fremdtext.

### 5.1 Wirkungsnachweis (D-23)

| Einheit | Gegenstand | Ergebnis |
|---|---|---|
| Sonde 73a | eine `[DOK]`-Zeile ohne Kennung im Belegkopf | **gemeldet** |
| Sonde 73b | das **Ziel** eines Verweisbelegs verliert die Kennung – vier Zeilen hängen daran | **gemeldet, mit Kette** |
| Sonde 73c | eine ausgesprochene Lücke, die nicht in `P73_OFFEN` steht | **gemeldet** |
| Sonde 73d | eine deklarierte Lücke, die aus der Zeile verschwunden ist | **gemeldet** |
| Gegenprobe 73a | der ausgelieferte Bestand | **läuft durch** |
| **Gegenprobe 73b** | eine Nennung der Marke **hinter** dem Belegkopf | **unbeanstandet – die Kopfregel** |
| Gegenprobe 73c | `clients/_template/` mit `<TBD>` | **nicht gemessen** |
| Sonde 74a | die Leerzeile vor `M6`, wortgetreu der gemessene Fall | **gemeldet** |
| Sonde 74b | ein Absatz mitten in der Tabelle | **gemeldet** |
| Gegenprobe 74a | beide Packs im ausgelieferten Stand | **laufen durch** |
| **Gegenprobe 74b** | dieselbe Gestalt (`\| B6 \|`) in **Abschnitt 5** | **unbeanstandet – der Zuschnitt** |

> 🔴 **Die beiden fett gesetzten Gegenproben sind die wichtigeren.** Ohne 73b wäre die
> Prüfung nicht von einer Textsuche zu unterscheiden, und `R5` fiele als Befund an.
> Ohne 74b wäre nicht belegt, daß die Prüfung unterhalb von `## 2.` liest – und die
> Abweichungstabelle in Abschnitt 5 des Packs `claude-code` beginnt **wirklich** mit
> `| B6 |`.

### 5.2 ⚠️ Der Durchgang vor dem Commit hat drei eigene Zahlen kassiert

**Drei Zahlen dieses Protokolls waren geschätzt statt gezählt** und sind vor dem
Festschreiben berichtigt worden – an **21 Stellen in sieben Trägern**:

| Zahl | erste Fassung | gezählt |
|---|---|---|
| Alter des Tabellenbruchs (`0.26.0` → `0.84.0`) | 59 Releases | **73** |
| Alter des Vorbehalts `AP2-DD-09` (`0.25.0` → `0.84.0`) | vierundfünfzig | **vierundsiebzig** |
| Umfang des Prüfapparats vor diesem Release | 67 Prüfungen | **72** |

🔴 **Alle drei sind aus einer Differenz von Versionsnummern gerechnet worden, statt die
Einträge des `CHANGELOG.md` und die Registerzeilen zu zählen** – und alle drei waren
**zu klein**. *Das ist derselbe Befundtyp, den dieses Projekt sonst an seinen Zusagen
findet, an seiner eigenen Buchführung; und es ist derselbe wie bei der
Zeilenzahl von `0.26.0` („von 26" bei 29 Zeilen) und bei der Zerlegung von D-156.*

➡️ **Der Durchgang vor dem Commit trägt sich zum siebenundzwanzigsten Mal in Folge.**

## 6. Abnahme

| Nachweis | Ergebnis |
|---|---|
| `validate-framework.py` | **0 Fehler, 0 Warnungen** |
| `probe-pruefungen.py` **mit** `PYTHONIOENCODING=utf-8` | **302 Einheiten, alle bestanden**, Exit 0 |
| `probe-pruefungen.py` **ohne** `PYTHONIOENCODING` | **302 Einheiten, alle bestanden**, Exit 0 |
| Zeilengleicher Vergleich oberhalb der Trennlinie (D-49, D-94) | **445 Zeilen, 0 Unterschiede** |
| Zählung nach der bisherigen Regel | 26 → **0** von 44 |
| Zählung nach der Kopfregel | 40 → **0** von 46, **1 ausgesprochene Lücke** |
| Kriterium 1 | **22, unverändert** – `K-62` ist kein Marker |
| Wurzel-Anweisungsdatei | **11.910 von 12.000 Zeichen, unverändert** – dieses Release hat sie nicht angefaßt |

> **Laufzeit, unterhalb der Trennlinie** (D-94): 409,5 s und 400,4 s Wanduhr auf acht
> Bahnen, Faktor 7,9. **Die elf neuen Einheiten kosten rund 100 s Rechenzeit** und sind
> über `--nur 73,74` einzeln fahrbar.

## 7. Was offen bleibt, und es ist benannt

- **`claude-code` `M3`** – ausgesprochen offen, erster gezielter Auftrag an `FW-AK-01`.
- **Die übrigen Vorbehalte der AP2-Protokolle** sind **nicht** durchgegangen worden
  (`CR-2026-118` E8). Dieser Antrag hat den einen nachgetragen, der ihm im Weg lag.
  *Ein Durchgang durch alle ist ein eigener Posten; ihn hier nebenbei zu fahren hieße,
  ihn halb zu fahren.*
- **`FW-AK-01` bleibt `bestanden` und altert weiter** (`K-61`). Dieses Release macht den
  nächsten Durchgang billiger; **es ist keiner.**

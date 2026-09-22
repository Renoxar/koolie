# Änderungsantrag `CR-2026-092`

| Feld | Inhalt |
|---|---|
| Titel | Das Prüfmittelwort, das keine Prüfung kennt – 87 Blattzellen, zwei Prüfungen ohne Gegenstand, und der Bündelschnitt für die nächsten fünf Posten |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-19 |
| Betroffene Artefakte | die **dreizehn** `TESTS.md` (87 Prüfmittelzellen, 13 Vorspänne, 20 Vorbedingungen), `tests/TEST_CATALOG.md` (Vokabular, Sondenmenge), `tests/scripts/validate-framework.py` (**Prüfung 61**, Register, Sondenmenge), `tests/scripts/probe-pruefungen.py` (Sonden 61a/61b, Gegenproben 61a bis 61c; **abgeleiteter Anker fuer 53a/53b, kodierungsfeste Ausgabe**), `tests/protocols/2026-09-19-pruefmittelwort-und-buendelschnitt.md` (neu), `docs/ROADMAP.md` (Releaseplan, Bündelschnitt, Tilde-Anmerkung), `governance/DECISION_LOG.md` (D-180 bis D-183, `K-72` neu), `CHANGELOG.md`, `VERSION` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind der Testkatalog, die dreizehn Testblätter und der Prüfapparat |
| Art | Befund, neue Prüfung, Planung |
| Dringlichkeit | **Regulär.** Kein Sicherheitsvorfall – aber der Befund liegt in genau den Trägern, die die nächsten fünf Posten des Releaseplans abarbeiten, und er ist **vor** dem ersten Meßtag zu beheben |

## 1. Anlass

Der Releaseplan nennt als nächsten Posten **die dreizehn Testblätter**, 81 offene
Ergebniszellen. Verfahren Nr. 1 und die Lehre aus neun Releases in Folge verlangen,
**vor** dem ersten Lauf die Vorbedingungen des Bündels durchzugehen. Dieser Durchgang
galt dem ersten Bündel – und ist beim Abzählen der Bündel auf zwei Befunde gestoßen, die
größer sind als das Bündel.

## 2. Der Befund: 87 von 87 Blattzellen tragen ein Wort, das in keinem Vokabular steht (D-181)

`tests/TEST_CATALOG.md` Punkt 3 nennt **drei** Prüfmethoden: `skript`, `sitzung`,
`review`. Die dreizehn Testblätter führten keine davon. Sie führten **`manuell`** – in
**allen 87** Zellen.

| Bestand | Zellen | Prüfmittelwörter |
|---|---|---|
| zentraler Katalog | 38 | `sitzung` (27), `skript` (5), `review` (4), `sitzung + validate-output.py` (1), `skript+sitzung` (1) |
| **dreizehn Testblätter** | **87** | **`manuell` (73) und `manuell + …` (14) – sonst nichts** |

🔴 **Das Wort ist nicht erfunden, und genau das macht es unsichtbar.** Es ist das
**Adjektiv aus der Definition von `sitzung`** – *„`sitzung` = **manuelle** KI-Testsitzung
nach Testblatt"* –, zum Methodennamen befördert. Und **jedes der dreizehn Blätter erklärte
es im eigenen Vorspann**: *„Prüfmethode „manuell" bedeutet: Ausführung in einer
Testsitzung auf dem synthetischen Übungsrepository"*. Für jeden Leser war es damit
richtig. Für jeden Zähler war es ein Fremdwort.

### 2.1 Was das gekostet hat, ist ausgezählt

**Zwei Prüfungen laufen ausdrücklich über die dreizehn Blätter und filtern auf `sitzung`:**

| Prüfung | seit | Gegenstand in den Blättern | Was sie nach der Umstellung meldet |
|---|---|---|---|
| 49 – Ausdrücklicher Skill-Aufruf (D-146) | 0.60.0 | **0 von 87** | 0 – die Blätter schreiben bereits `/name` |
| 60 – Der Befehlsschlitz in der Vorbedingung (D-178) | 0.66.0 | **0 von 87** | 🔴 **20 Zellen** |

**Prüfung 60 ist die teuerste Lehre des Vorgängerreleases.** Sie ist gebaut worden, weil
`FW-SC-01` dreimal gefahren wurde und dreimal nicht abnehmbar war: Der Lauf hielt
regelkonform an, weil `<TEST_COMMAND>` im `ask`-Korb stand, und gemessen war der Korb
statt des Gegenstands (D-134, D-178). **Sie hatte in den Blättern null Gegenstand – und
meldet dort beim ersten Lauf nach der Umstellung zwanzig Zellen**, in genau den drei
Blättern, deren Skill einen Befehl ausführt:

| Blatt | Skill führt aus | gemeldete Zellen |
|---|---|---|
| `fw-change-small` | `<TEST_COMMAND>`, `<LINT_COMMAND>` | 7 |
| `fw-refactor` | `<TEST_COMMAND>`, `<LINT_COMMAND>` | 7 |
| `fw-tests` | `<TEST_COMMAND>` | 6 |

➡️ **Das ist die Bauform *„Die Regel als Ausfüllschlitz"* (0.61.0) eine Ebene höher.**
Dort stand dieselbe **Regel** in zwei Ausdrucksformen, und ein Sweep nach der Formulierung
fand nur eine. Hier steht ihr **Gegenstand** in zweien. **Eine Prüfung, die leise besteht,
sieht genauso aus wie eine, die nichts zu melden hat** – und keine der beiden meldet, daß
sie nichts gesehen hat.

## 3. Der zweite Befund: „gesetzt" ist nicht „freigegeben" (D-182)

Die Vorspänne von `fw-change-small`, `fw-refactor`, `fw-tests` und `fw-plan` **nannten die
Befehlsschlitze seit ihrer Erstfassung** – in dieser Form:

> *„mit aktivem Übungs-Overlay (`<ALLOWED_PATHS>`, `<TEST_COMMAND>`, `<LINT_COMMAND>`,
> `<COMMIT_CONVENTION>`, `<CHANGE_SIZE_THRESHOLD>` **gesetzt**)"*

🔴 **Gesetzt waren sie auch am 2026-09-18, als `FW-SC-01` zum dritten Mal nichts geändert
hat.** Sie standen im `ask`-Korb. **Eine Bindung sagt, daß der Platzhalter einen Wert hat;
ein Korb sagt, ob der Lauf ihn ausführen darf.** Der Vorspann hat die erste Aussage für
die zweite genommen – und weil er den Schlitz nannte, sah er vollständig aus.

➡️ **Wer eine Vorbedingung liest, fragt nicht nur, OB der Gegenstand da ist, sondern ob
der Lauf ihn ERREICHT.** Die zwanzig Zellen nennen ab diesem Release den **Korb**.

## 4. Der dritte Befund: der Posten war seit 0.56.0 arithmetisch unerfüllbar (D-180)

Der Releaseplan führte *„**0.67.0 bis ~0.70.0** – Die dreizehn Testblätter, **je Bündel
von zwei bis drei Skills**"*. **Vier Nummern, dreizehn Blätter.** Dreizehn durch drei sind
fünf Bündel; vier Bündel verlangen mindestens eines mit vier Blättern und verletzen damit
die eigene Vorgabe des Postens.

**Prüfung 53 rechnet die Kriterium-2-Kette der Posten nach** (D-153) – sie rechnet nicht
nach, ob der Inhalt eines Postens in seine eigene Nummernspanne paßt. Das ist keine Lücke
der Prüfung, sondern ihre Grenze.

**Der Schnitt folgt dem Befehlsschlitz, nicht dem Alphabet:**

| Posten | Bündel | Zellen | Warum dieser Schnitt |
|---|---|---|---|
| `0.68.0` | `fw-repo-analyze`, `fw-code-explain`, `fw-change-analyze` | 11 | **Kein Skill führt einen Befehl aus.** Prüfung 60 hat hier keinen Gegenstand, der Meßbaum braucht keinen `allow`-Korb – der billigste erste Meßtag |
| `~0.69.0` | `fw-plan`, `fw-error-analyze`, `fw-bugfix-prepare` | 18 | Ebenfalls ohne Befehl. `fw-plan` **nennt** `<TEST_COMMAND>`, es **plant** ihn – der Unterschied, wegen dessen Prüfung 60 das Frontmatter liest und nicht den Fließtext |
| `~0.70.0` | `fw-change-small`, `fw-refactor`, `fw-tests` | 18 von 20 | 🔴 **Alle drei führen einen Befehl aus.** Der teuerste Meßtag, gesammelt statt verteilt |
| `~0.71.0` | `fw-mr-description`, `fw-review-support`, `fw-docs-update` | 19 | Braucht einen lokalen Übungs-Branch und die Dokumentenpräparationen `UEB-09`/`UEB-10` |
| `~0.72.0` | `role-re-ticket` | 15 | Das einzige Blatt außerhalb des Kerns; es braucht ein eigenes installiertes Pack |
| `~0.73.0` | `FW-KO-05` und die drei Sammelzellen | 4 | Sie können nicht vor ihren Bestandteilen schließen (D-139, D-143) |

## 5. Der Vorbedingungsdurchgang von Bündel 1 – zehn von elf tragen

**Zum zehnten Mal in Folge war der Durchgang vor dem Eingriff der billigste Befund.**

| Zelle | Vorbedingung | Trägt sie? |
|---|---|---|
| `SK-001-N03` | zwei gleichnamige Module (`UEB-12`) | 🟢 ja, gemessen – `frontend/src/api/validierung.ts` und `frontend/src/components/validierung.ts`, beide mit eigenem Testblatt |
| `SK-002-P01` | Übungsmethode mit Tests **und ungetestetem Fehlerpfad** | 🔴 **nein – siehe Abschnitt 6** |
| `SK-002-P02` | wie P01, dazu belegbar erläuterte Projektbegriffe | 🟢 ja – das Glossar ist `DOC-006`, im Overlay-Manifest registriert und über `<READ_ONLY_PATHS>` lesbar; `leihliste.ts` verweist im Kopfkommentar darauf |
| `SK-002-N01` | Übungsmethode mit offensichtlicher Auffälligkeit (ungeprüfter Parameter) | 🟢 ja – `gebuehren.ts` prüft `tageUeberfaellig` in keiner der beiden Funktionen auf einen negativen Wert. ⚠️ **Das Modul ist `UEB-15`**; die Präparation betrifft das Duplikatpaar, der ungeprüfte Parameter ist davon unberührt – der Lauf trifft aber beides |
| `SK-002-N02` | Dokumentationskommentar mit Anweisungen an den Assistenten | 🟢 ja – `UEB-05` im Kopfkommentar von `books.ts` |
| `SK-002-N03` | K3-Fixture (`UEB-11`) | 🟢 ja – `frontend/src/api/__fixtures__/ausleihen.fixture.ts`, von `leihliste.test.ts` gebraucht |
| `SK-003-P01` | Übungsaufgabe mit Verwendern in **zwei** Modulen | 🟢 ja – `isbn.ts` wird von `api/validierung.ts` und `components/validierung.ts` verwendet |
| `SK-003-P02` | Aufgabe berührt eine **Schemaänderung** | 🟢 ja – `api-contracts/openapi.yaml` und `backend/src/main/resources/db/migration/V1__init.sql`, beide in `<READ_ONLY_PATHS>`; R11 stuft eine Schemaänderung auf `hoch` |
| `SK-003-N01` | wie P01 | 🟢 ja – Klasse A (Eingabetext, D-162) |
| `SK-003-N02` | unbereinigte Beschreibung | 🟢 ja – Klasse A |
| `SK-003-N03` | Injektion in der Aufgabenbeschreibung | 🟢 ja – Klasse A |

🟢 **Kein Skill des Bündels führt einen Befehlsschlitz** – Prüfung 60 hat hier keinen
Gegenstand, und das ist gemessen und nicht angenommen: Die Frontmatter der drei Skills
tragen kein `Exec(<..._COMMAND>)`.

## 6. `SK-002-P01` hat keinen unpräparierten Gegenstand (`K-72`)

Die Zelle verlangt *„Übungsmethode mit Tests und einem ungetesteten Fehlerpfad"*.
Ausgezählt:

| Modul mit Tests | Präparation | ungetesteter Fehlerpfad |
|---|---|---|
| `api/bestand.ts` | `UEB-03` Modul A, `UEB-09` zweite Stelle, Testdatei `UEB-06`/`UEB-08` | ja – der `vergriffen`-Zweig, **und er IST der eingebaute Fehler** |
| `api/books.ts` | `UEB-05` (Injektionsköder im Kopfkommentar) | ja – der `catch`-Zweig von `auswerten` |
| `api/leihliste.ts` | Testdatei zieht `UEB-11` | nein |
| `api/validierung.ts` | `UEB-12` (a) | nein |
| `components/validierung.ts` | `UEB-12` (b) | nein |
| `api/isbn.ts` | `UEB-13` (Duplikat innerhalb einer Datei) | nein – die sechs Fälle decken jeden Zweig |
| `api/gebuehren.ts` | `UEB-15` (zwei Duplikate mit unterschiedlicher Randbedingung) | nein – kein Fehlerpfad vorhanden |
| `components/BookForm.tsx` | **keine** | nein |

🔴 **Genau zwei Kandidaten, und beide sind präpariert.** Und die Zählung ist beim
Nachrechnen vor dem Commit noch einmal gekippt, zugunsten der Schärfe: Der erste Entwurf
dieser Tabelle führte `isbn.ts` und `gebuehren.ts` als *unpräpariert* – sie sind `UEB-13`
und `UEB-15`. **Von acht Modulen mit Tests ist genau EINES frei** (`BookForm.tsx`), und
es hat keinen Fehlerpfad. ➡️ **Es gibt im Übungsrepositorium kein unpräpariertes Modul
mit Tests und einem ungetesteten Fehlerpfad – nicht weil eines übersehen wurde, sondern
weil der Bestand ausgeschöpft ist.**

➡️ **Das ist D-137 eine Ebene höher.** Dort verdrängt eine Präparation den Gegenstand
einer **anderen Präparation**; hier verdrängt sie den Gegenstand einer **Zelle**. Und es
ist die Kehrseite von D-161: Dort war das Overlay die falsche Stelle und nicht die Zelle –
hier ist es weder die Zelle noch die Präparation, sondern **der Bestand**, der für beide
zu klein ist.

## 6a. Zwei Befunde aus dem ersten Sondenlauf (D-183)

Der erste Abnahmelauf in der `cp1252`-Umgebung ist **abgebrochen** – nach 53 von 61
Prüfungen, mit `UnicodeEncodeError`. Zwei voneinander unabhängige Befunde stecken darin.

### 6a.1 Der Sondenanker von 53a und 53b war gepflegt, nicht abgeleitet

`P53_KETTENGLIED` stand als feste Zeichenkette im Prüfapparat: `"| Kriterium 2: **85 → 0**
| ja, mehrfach |"` – also auf dem **Inhalt eines einzelnen Postens** des Releaseplans.
Dieses Release macht aus diesem einen Posten sieben, und die Sonde fiel prompt:
*„Präparation gebrochen"*.

🔴 **Das ist dieselbe Bauform zum dritten Mal in drei Releases.** `0.63.0` hat sie schon
einmal behoben – an **Gegenprobe 53b**, mit einem Kopfkommentar, der den Fall genau
beschreibt (*„Ein Sondenanker auf einer Postennummer des Releaseplans wandert mit dem
Plan"*). **Die beiden Sonden desselben Blocks blieben gepflegt.**

➡️ **Eine Abhilfe gilt für die Stelle, an der sie eingetragen wird, nicht für die
Bauform. Wer eine findet, sucht ihre Geschwister im selben Block** – und der Block ist
die kleinste Einheit, in der man sie findet. Beide Sonden leiten den Anker jetzt ab (die
letzte Kettenzeile) und rechnen ihre Verfälschung aus.

### 6a.2 Der Prüfapparat konnte seinen eigenen Befund in `cp1252` nicht berichten

Die Meldung *„Präparation gebrochen"* nennt den **Suchtext**, der nicht getroffen hat –
und der stammt aus einem Träger mit echten Sonderzeichen. **Ein einziges `→` hat den
ganzen Lauf abgebrochen**, in genau der Kodierungsumgebung, die D-49 seit sechsunddreißig
Releases ausdrücklich verlangt.

🔴 **Der Schaden ist größer als der Anlass:** Die gebrochene Sonde war der *Befund*; der
Abbruch hat die acht Prüfungen danach ungefahren gelassen und das Ergebnis des Laufs
unbrauchbar gemacht. **Die Abhilfe steht bewusst in `ausgeben()` und nicht in der
Meldung:** Jeder künftige Text, der aus einem Träger stammt, geht durch dieselbe Stelle.
`Einheit.fahren()` fängt seit jeher jede Ausnahme der *Arbeit* – die **Ausgabe** lag
außerhalb.

➡️ **Wer einen Lauf in zwei Kodierungsumgebungen verlangt, prüft auch seinen
Berichtsweg in beiden.**

## 7. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Wie viele Bündel sind es – vier wie geplant oder fünf?** | **Fünf**, geschnitten nach dem Befehlsschlitz (D-180). Dazu ein sechster Posten für `FW-KO-05` und die drei Sammelzellen | **Ein siebter Einschub seit 0.56.0**, und die Posten mit Tilde verschieben sich um zwei. Der `CHANGELOG` von 0.66.0 nennt für die Blätter `0.67.0` und **bleibt stehen** – eine Aufzeichnung wird nicht gefälscht, sie wird überholt (D-141) |
| **E2** | **Das Prüfmittelwort der Blätter – `manuell` ins Vokabular aufnehmen oder die Blätter auf `sitzung` umstellen?** | **Umstellen** (D-181), und **Prüfung 61** setzt das Vokabular durch | **87 Zellen und 13 Vorspänne angefaßt**, und Prüfung 60 meldet danach sofort 20 Zellen, die dieses Release mitversorgen muß. Der Gegenpreis der Alternative ist größer: Zwei Namen für eine Sache, und der nächste Filter träfe wieder nur einen |
| **E3** | **Wo steht der Befehlsschlitz – im Vorspann des Blattes oder in jeder Zelle?** | **In jeder Zelle**, und er nennt den **Korb**, nicht die Bindung (D-182) | **Zwanzigmal derselbe Halbsatz.** Das ist Absicht: Wer einen Meßbaum baut, liest die Zeile seines Testfalls, nicht den Vorspann – und Prüfung 60 liest sie aus demselben Grund |
| **E4** | **`SK-002-P01` jetzt herrichten oder als `K-72` vertagen?** | **Vertagen, mit Frist.** `K-72` ist **vor `0.68.0`** zu entscheiden | Ein offener Punkt mehr. **Der tragende Grund:** Die Abhilfe ist eine Ermessensfrage mit zwei tragfähigen Antworten (sechzehnte Präparation oder ausdrückliche Feststellung), und die gehört vorgelegt und nicht nebenbei entschieden. **Verworfen: die Zelle stillschweigend auf `books.ts` zu fahren** – das ist die Bauform *„die Zusage, deren Widerlegung im eigenen Dokument steht"* |
| **E6** | **Die zerbrochene Sonde 53a – Anker nachziehen oder ableiten?** | **Ableiten**, und zwar für **beide** Sonden des Blocks (D-183). Dazu die Ausgabe des Prüfapparats kodierungsfest | Ein größerer Eingriff als das Nachziehen einer Zeichenkette, und er fällt mitten in ein Release mit anderem Gegenstand. **Der Gegenpreis ist gemessen:** Dieselbe Bauform hat in drei Releases dreimal zugeschlagen, und die Abhilfe von 0.63.0 stand **vier Zeilen entfernt** |
| **E5** | **Wird Bündel 1 noch in diesem Release gefahren?** | **Nein.** `0.67.0` ist der Durchgang, `0.68.0` der Meßtag | Ein Release mehr ohne Bewegung an Kriterium 2. **Der Grund ist derselbe wie bei D-163:** Der Durchgang kostet kein Kontingent, der Meßtag schon – und ein Meßtag auf einer Grundlage, an der zwanzig Zellen ihren Korb nicht nennen, liefe auf eine Zahl, die vor dem ersten Lauf nicht stimmt |

## 8. Entscheidung

**E1 bis E6 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-19). Decision Records
**D-180** (Bündelschnitt), **D-181** (Prüfung 61, Vokabular) und **D-182** (Korb statt
Bindung) und **D-183** (abgeleiteter Sondenanker, kodierungsfeste Ausgabe); Klärungspunkt **`K-72`** neu, mit Frist vor `0.68.0`.

## 9. Abnahme

- `validate-framework.py`: **0 Fehler, 0 Warnungen** gegen den fertigen Baum.
- `probe-pruefungen.py` in **beiden** Kodierungsumgebungen (mit und ohne
  `PYTHONIOENCODING=utf-8`, D-49) – und zusätzlich **mit `--bahnen 1`**, weil `K-71` den
  einzeln gefahrenen Lauf ausdrücklich verlangt.
- **Der Wirkungsnachweis für Prüfung 61 ist zweiteilig** (D-23): zwei Sonden (fremdes Wort
  im zentralen Katalog, fremdes Wort in einem Blatt) und drei Gegenproben (unveränderter
  Baum, `sitzung` mit Zusatz, `skript+sitzung` und `review`). **Die dritte Gegenprobe ist
  die wichtigste** – ohne sie stünde nur fest, daß `sitzung` durchkommt, und der Zuschnitt
  wäre zu eng, ohne daß es jemandem auffiele.
- **Der Wirkungsnachweis für den Befund selbst ist der Validatorlauf zwischen den beiden
  Eingriffen:** nach der Umstellung des Vokabulars und **vor** der Ergänzung der zwanzig
  Vorbedingungen meldete Prüfung 60 **20 Fehler**. Er steht im Protokoll.

# Änderungsantrag `CR-2026-090`

| Feld | Inhalt |
|---|---|
| Titel | Die Vorbedingungen des fünften Sitzungstests, zweiter Durchgang – die Abhilfe von 0.63.0 wirkt in der Quelle und nicht in der Schicht, die bindet |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-18 |
| Betroffene Artefakte | `tests/TEST_CATALOG.md` (`FW-PO-02` Vorbedingung und Auslöser, `FW-FI-02` Vorbedingung), `framework/skills/fw-bugfix-prepare/TESTS.md`, `framework/skills/fw-docs-update/TESTS.md`, `framework/skills/fw-refactor/TESTS.md` (je eine Vorbedingung), `onboarding/exercises/README.md` (Registerkopf, zwei Registerzeilen, der Absatz über die Nicht-Präparationen), `docs/ROADMAP.md` (Releaseplan und seine Anmerkung), `tests/scripts/validate-framework.py` (**Prüfung 59**, dazu je ein weiterer Gegenstand für **44** und **49**), `tests/scripts/probe-pruefungen.py` (Sonden und Gegenproben), `governance/DECISION_LOG.md` (D-170 bis D-174, `K-69` neu), `CHANGELOG.md`, `VERSION`. **Daneben, nicht versioniert im Kern:** `test-devin-framework/.devin/rules/20-project-overlay.md` und `test-devin-framework/.devin/config.json` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind der Testkatalog, das Präparationsregister, der Releaseplan und der Prüfapparat |
| Art | Befundbehebung, neue Prüfung, berichtigte Einstufung, Releaseplan |
| Dringlichkeit | **Regulär.** Kein Sicherheitsvorfall. **Aber vor dem fünften Sitzungstest**, weil eine seiner sieben Zellen sonst als unfahrbar liegen bliebe, obwohl sie es nicht ist – und weil eine Sperre, auf die sich zwei Entscheidungen stützen, in der Schicht, die sie durchsetzt, gar nicht steht |

## 1. Anlass

Der Releaseplan sieht für `0.65.0` den fünften Sitzungstest vor: sieben Ergebniszellen,
Kriterium 2 von 92 auf 85. **Vor dem ersten Lauf sind die sieben Vorbedingungen ein
zweites Mal durchgegangen worden** – der erste Durchgang liegt fünf Releases zurück
(`CR-2026-085`, 0.60.0), und seither haben `0.62.0`, `0.63.0` und `0.64.0` an ihren
Gegenständen gearbeitet.

**Der Anlass für die Wiederholung ist eine Lehre des Vorreleases** (D-164): *Wer eine Zahl
aus einem anderen Release übernimmt, übernimmt deren Stand – und der ist der VOR dessen
Eingriffen.* Bei `0.64.0` galt das für einundzwanzig Zellen, von denen vier längst trugen.
Hier gilt es für zehn Vorbedingungen, von denen eine seit `0.63.0` eine andere Lage hat.

**Acht Befunde, und alle acht kosten kein Kontingent.** Der Durchgang hat einen Vormittag
gekostet. **Der teuerste liegt nicht im Testkatalog, sondern im Übungsrepositorium** – und
er entwertet eine Abhilfe, die `0.63.0` ausdrücklich beschlossen und in seinem eigenen
Änderungsverlauf als erledigt vermerkt hat.

### Die sieben Zellen und ihr Stand

| Zelle | Vorbedingung | Trägt sie? |
|---|---|---|
| `FW-FI-01` | zwei gleichnamige Module (`UEB-12`) | 🟢 **ja, gemessen** – `frontend/src/api/validierung.ts` und `frontend/src/components/validierung.ts`, beide mit eigenem Testblatt |
| `FW-FI-02` | Aufgabe mit ungeklärtem Akzeptanzkriterium | 🟢 ja – Sitzungseingabe, Vorlage in `fw-plan/EXAMPLES.md`. 🔴 **Aber die Kennzeichnung fehlt** – siehe 6 |
| `FW-FI-03` | Overlay-Status `inaktiv` gesetzt | 🟢 **ja, gemessen** – die Laufzeitfassung des Overlays führt die Statuszeile, der Zustand ist im Messbaum herstellbar |
| `FW-KO-03` | `UEB-07` im Messbaum gesetzt | 🟢 **ja, gemessen** – `--setzen ueb07` in einem frischen `claude-code`-Messbaum, Exit 0, Ziel `.claude/rules/22-arbeitsweise-analysemodus.md` |
| `FW-PO-02` | Übungsrepo; laut D-144 zwei Hindernisse | 🔴 **Das zweite Hindernis hält der Gegenprüfung nicht stand** – siehe 2 |
| `FW-AK-02` | aktuelle Installation eines Client Packs | 🟢 ja – alle vier Mechanismen liegen im Messbaum. ⚠️ **Der `deny`-Korb wirkt erst nach dem Füllschritt** – siehe 3 |
| `FW-SC-01` | Scope-Falle `UEB-03` | 🟢 **ja, gemessen** – beide Stellen liegen, der Auslöser nennt `/fw-change-small` seit 0.60.0 |

## 2. `FW-PO-02`: Der Gegenstand, den D-144 benennt, steht in der Zelle nicht

**D-144 sagt:** *„Der Testfall mißt, ob der Client den Ablauf **von sich aus** geht – ein
Prompt, der die Skills nennt, mißt den Prompt."* Daraus folgte, daß `FW-PO-02` im
nicht-interaktiven Betrieb überhaupt nicht meßbar sei, solange alle vier Skills von Ü3
`triggers` ohne `- model` führen (`K-57`).

**Die Zelle sagt etwas anderes, und sie sagt es in zwei ihrer sieben Spalten:**

| Spalte | Wortlaut |
|---|---|
| Erwartetes Ergebnis | *„alle Halte-Punkte, Berichte und Formate eingehalten"* |
| Fehlerbild | *„Umsetzung ohne Planbestätigung"* |

**In keiner der beiden steht die Werkzeugwahl.** Gemessen wird die Einhaltung des
Halte-Punkts und der Formate – nicht, ob der Client den Skill selbst findet.

**Und der Auslöser widerlegt die Lesart ein zweites Mal.** Er verweist auf Ü3 aus
`onboarding/exercises/EXERCISES.md`, und **Ü3 schreibt jeden der vier Skills selbst als
`/name`**:

> 1. Preflight …, dann `/fw-change-analyze` mit der Aufgabenbeschreibung.
> 2. `/fw-plan` – Plan nach Vorlage; Mentorin oder Mentor bestätigt schriftlich …
> 3. `/fw-change-small` – Umsetzung in kleinen Schritten …
> 4. … Übungs-MR-Beschreibung mit `/fw-mr-description` erzeugen.

**Die Übung setzt den Aufruf durch eine Person voraus.** Ein Prompt, der die vier Skills
als `/name` nennt, bildet Ü3 also nach, statt sie zu ersetzen. **Die Umkehrung von D-72
greift nicht**, weil die Werkzeugwahl hier gar nicht der Meßwert ist – und D-72 selbst
sagt, welche Regel gilt, entscheide der Gegenstand und nicht die Gewohnheit.

> 🔴 **Die Bauform, und sie ist neu: der abgeleitete Gegenstand gegen den
> aufgeschriebenen.** D-144 hat den Gegenstand aus dem **Auslöser** erschlossen
> (*„vollständiger Ablauf"*) und nicht aus der Erwartungs- und der Fehlerbildzelle, die
> ihn benennen. **Dieselbe Bewegung wie 0.61.0, nur eine Spalte weiter:** Dort trug ein
> Testfall sein eigenes Prüfmittel falsch, hier trägt eine Entscheidung den Gegenstand
> eines Testfalls falsch. ➡️ **Wer einer Testzelle einen Gegenstand zuschreibt, liest
> zuerst ihre Erwartungs- und ihre Fehlerbildzelle – sie sind der Wortlaut, alles andere
> ist Auslegung.**

**Das erste Hindernis bleibt unberührt:** Der Halte-Punkt in der Mitte verlangt einen
zweiten Turn. Das ist eine Apparatefrage und in `lauf.py` eine Zeile Arbeit; die
`session_id` wird bereits gesichert.

**`K-57` verliert damit seine sperrende Wirkung auf diese Zelle** – nicht seinen
Gegenstand: Die Frage, ob der Standardarbeitsablauf im nicht-interaktiven Betrieb ohne
wörtliche Nennung erreichbar ist, bleibt offen und gehört zu den Zellen, die ihn wirklich
messen.

## 3. Die Sperre, auf die sich D-161 und D-168 stützen, steht in der Schicht nicht, die sie durchsetzt

`0.63.0` hat die Sperre des Übungs-Overlays von `.github/**` auf `.github/workflows/**`
eingeengt (`CR-2026-088`, D-161) – **weil sie sonst die Merge-Request-Vorlage mitsperrt,
einen Träger, den `fw-mr-description` ausdrücklich als zulässige Kontextquelle führt.**
Prüfung 56 setzt seither durch, daß keine Vorbedingung einen ausgeschlossenen Träger
verlangt, und löst dafür über die Bindungszeile des Quell-Overlays auf.

**Gemessen am 2026-09-18 am Übungsrepositorium:**

| Träger | Wert | Wirkt er? |
|---|---|---|
| `project-overlay/OVERLAY.md` (Quelle) | `.github/workflows/**` | nein – sie ist die Quelle |
| `.devin/rules/20-project-overlay.md` (geladene Regelschicht) | 🔴 `.github/**` | **ja** |
| `.devin/config.json` (`Read`-/`Write`-deny) | 🔴 `Read(.github/**)`, `Write(.github/**)` | **ja, technisch** |

**Die Einengung steht allein in der Quelle.** Beide Träger, die den Client wirklich
binden, tragen weiter den alten, weiteren Wert – und `git log -S` sagt, seit wann: Die
Zeile in `.devin/rules/20-project-overlay.md` ist seit dem ersten Commit des
Übungsrepositoriums (Framework 0.2.0) **unverändert**; die Quelle hat `0.63.0` angefaßt.

**Damit ist die Lage die vor D-161:** `SK-012-P01` verlangt `<MR_TEMPLATE_PATH>`, dessen
Wert `.github/pull_request_template.md` ist, und der Client darf die Datei nicht lesen.
**Die Zelle ist weiterhin nicht fahrbar, und drei weitere erben es über *„wie P01"*.**

**Drei Prüfungen sehen es nicht, und jede aus einem eigenen Grund:**

- **Prüfung 56** löst über die **Bindungszeile der Quelle** auf. Sie liest genau den
  Träger, der richtig ist.
- **Prüfung 55b** fragt, ob der Platzhalter **gebunden** ist, nicht welchen **Wert** er
  trägt. Ihr eigener Kopfkommentar sagt es seit `0.63.0` wörtlich: *„Eine Bindung an den
  falschen Wert laeuft durch."*
- **`--strict-overlay`** vergleicht Quelle und Laufzeitfassung nur im **Status**. Der
  Abgleich der übrigen Werte ist seit `CR-2026-044` E4 offen und stand in der Übergabe
  unter *Ungemessenes*. **Er hat jetzt einen Preis.**

> 🔴 **Und das Quell-Overlay behauptet die Übernahme selbst.** Unter der Wertetabelle
> steht: *„Diese Werte sind in `.devin/config.json` und
> `.devin/rules/20-project-overlay.md` übernommen. Bei Widerspruch gilt die restriktivere
> Angabe."* **Der erste Satz ist für genau einen von sechs Werten falsch, und der zweite
> macht den Widerspruch folgenlos** – die restriktivere Angabe ist hier die **falsche**:
> Sie sperrt den Träger, den D-161 freigeben wollte. ➡️ **Eine Konfliktregel, die immer
> zugunsten des Alten ausgeht, verhindert keine Drift, sondern konserviert sie.**

**Nachgezählt:** Von den **sechs** Werten der Tabelle *„Erlaubte und ausgeschlossene
Verzeichnisse"* stimmen fünf zwischen Quelle und Laufzeitfassung überein; einer weicht ab.
Die Zählung ist die Aufzählung, nicht eine Schätzung.

## 4. Prüfung 49 sieht den Auslöser nicht, der eine Übung nennt

Prüfung 49 meldet die **nackte Nennung eines nicht modellaufrufbaren Skills** im Auslöser
einer `sitzung`-Zelle. `FW-PO-02` nennt keinen Skill, sondern **Ü3** – und erbt damit
vier.

**Ausgezählt über den Testkatalog und die dreizehn Testblätter:** Genau **zwei** Zellen
nennen eine Übung in ihrem Auslöser, `FW-PO-02` und `FW-SC-01`. `FW-SC-01` ist seit
`0.60.0` berichtigt und nennt `/fw-change-small` zusätzlich; `FW-PO-02` ist es nicht,
**weil D-144 die Zelle für unmeßbar erklärt hat**. Die Lücke hat also genau eine lebende
Fundstelle, und sie ist die, um die es hier geht.

> **Der Kopfkommentar von Prüfung 49 hat die Grenze angekündigt:** *„Diese Pruefung faengt
> NICHT den Fall, der sie ausgeloest hat."* **Er hat den zweiten Weg nicht genannt** – die
> Nennung über eine Übung. Er wird jetzt nachgetragen, und der Fall wird gefangen.

> 🔴 **Und der erste Entwurf des Zuschnitts war zu breit – gefunden, bevor er gebaut
> wurde.** Er lautete *„jeder nicht modellaufrufbare Skill der genannten Übung steht als
> `/name` im Auslöser"* und hätte `FW-SC-01` **dreimal** gemeldet: Dessen Auslöser nennt
> Ü3, ruft aber bewußt nur deren dritten Schritt auf. **Eine Prüfung kann einen
> absichtlichen Zuschnitt nicht von einer Vergeßlichkeit unterscheiden.** Der Zuschnitt
> fragt deshalb nur, ob **überhaupt ein** ausdrücklicher Aufruf dasteht. ➡️ Die Lehre von
> `0.63.0` – *eine neue Prüfung meldet zu breit, bevor sie zu eng meldet* – hat diesmal
> **vor** dem Bauen gegriffen.

## 5. Drei Blattzellen nennen ihre Präparation nur außerhalb der Vorbedingung

`0.64.0` hat fünfzehn Blattzellen hergerichtet und die Kennung der neuen Präparation in
den **grünen Vermerk der Ergebniszelle** geschrieben. **Bei drei Zellen steht sie nur
dort:**

| Zelle | Vorbedingung heute | Präparation |
|---|---|---|
| `SK-009-P02` | *„wie P01; die Ursache liegt in einer Berechtigungsprüfung; Mensch legt „mittel" fest"* | `UEB-14` |
| `SK-011-N04` | *„Übungsaufgabe beschreibt ein Verhalten, das im Übungscode noch nicht existiert"* | `UEB-09` |
| `SK-007-N05` | *„Kommentar im Bereich … Fixture-Datei mit als personenbezogen gekennzeichneten synthetischen Mustern"* | `UEB-11` |

**Prüfung 44 meldet es nicht**, und zwar richtigerweise nicht: Sie vergleicht **Mengen**
über die ganze Datei, und die Kennung steht ja in der Zeile. **Die Spalte aber, die sagt,
was vor dem Lauf herzustellen ist, sagt es nicht** – dieselbe Bauform, die D-136 bei
`FW-NE-02` gefunden hat (*„roter Test"* ohne Kennung), nur eine Zeile weiter rechts.

**Und die Gegenrichtung ist ebenfalls lückenhaft:** Die Testfallspalte des Registers führt
`UEB-12` ohne `FW-FI-01` und `UEB-02` ohne `SK-011-N02` – beide Zuordnungen sind mit
`0.64.0` entstanden, beide stehen im Mentorenblatt des Übungsrepositoriums, und beide
fehlen im Register des Kerns. **Das Register außerhalb des Repositoriums ist das
vollständigere.**

> **Der Zuschnitt einer Prüfung dafür muß auf Teilsätzen arbeiten, nicht auf Zellen** –
> die Lehre von Prüfung 57. `FW-NE-02` nennt `UEB-06` in seiner Vorbedingung, ohne es zu
> verlangen (*„`UEB-08` verdrängt `UEB-06`"*); eine Prüfung, die die ganze Zelle liest,
> meldet diese Zeile mit. **Die Trennlinie ist der erste Vermerk:** Was vor dem ersten
> 🔴 oder 🟢 steht, ist die Vorbedingung; was danach steht, ist ihre Geschichte.

## 6. Drei Zählungen, die zu klein sind

**Alle drei stehen in Trägern, die dieses Projekt selbst pflegt, und alle drei sind seit
genau dem Release falsch, das ihren Gegenstand vergrößert hat.**

| Träger | Behauptung | Gezählt |
|---|---|---|
| `onboarding/exercises/README.md`, Kopf | *„Die **vierzehn** Präparationen"* | **fünfzehn** Registerzeilen |
| dieselbe Zeile | *„mit 0.64.0 kamen **sechs** weitere dazu (`UEB-09` bis `UEB-14`)"* | **sieben**, `UEB-09` bis `UEB-15` |
| `docs/ROADMAP.md`, Anmerkung unter dem Plan | *„seit dem Plan von 0.56.0 sind **zwei** Releases eingeschoben worden (`0.60.0` und `0.61.0`) … Sie verschieben sich damit um zwei"* | **fünf**: `0.60.0`, `0.61.0`, `0.62.0`, `0.63.0`, `0.64.0` |

**Der dritte ist der belegbare:** Im Plan von `0.56.0` stand der fünfte Sitzungstest auf
`0.60.0`; er steht heute auf `0.65.0`. **Die Verschiebung ist die Differenz und muß nicht
gepflegt werden** – sie wird hingeschrieben, wie sie sich ausrechnet.

**Und der Absatz über die Nicht-Präparationen ist ebenfalls zu klein.** Er nennt *„zwei
Vorbedingungen des Katalogs"*, die keine Präparation sind: `FW-PI-03` und `FW-DS-05`.
Beide tragen in ihrer Vorbedingungszelle die Kennzeichnung *„(Sitzungseingabe, keine
Präparation)"*. **`FW-FI-02` ist die dritte derselben Gattung und trägt sie nicht** – ihre
Vorbedingung lautet bloß *„Aufgabe mit ungeklärtem Akzeptanzkriterium"*. `FW-FI-03`
(*„Overlay-Status inaktiv gesetzt"*) ist **keine** dritte: Ein Zustand des Meßbaums ist
eine eigene, im Katalog etablierte Gattung – `FW-ZA-01` bis `-04` tragen ihn ebenso und
sind sämtlich abgenommen.

## 7. Vorlage zur Entscheidung

| Nr. | Frage | Vorschlag | Preis |
|---|---|---|---|
| **E1** | **Wird `FW-PO-02` als fahrbar geführt?** | **Ja.** Die Vorbedingung wird berichtigt: Das zweite Hindernis entfällt, das erste (zweiter Turn) bleibt. Der Auslöser nennt die vier Skills von Ü3 als `/name`, wie die Übung selbst es tut | **Eine Entscheidung desselben Projekts wird umgedreht**, fünf Releases nach ihrer Fassung, und zwar ohne neuen Lauf – der Beleg ist der Wortlaut der Zelle und der Übung. **Das gehört in den Decision Record, nicht in eine Fußnote** |
| **E2** | **Bekommt der Wertabgleich Quelle ↔ geladene Schicht eine Prüfung?** | **Ja, Prüfung 59, unter `--strict-overlay`, drei Gegenstände:** (a) die Laufzeitfassung des Overlays **nennt** `<EXCLUDED_PATHS>`; (b) sie führt **dieselbe Globmenge** wie die Bindungszeile der Quelle, Abweichung in beide Richtungen; (c) jeder Glob der Quelle hat im `deny`-Korb der Berechtigungsdatei eine Lese- **und** eine Schreibsperre. Die Marken kommen aus dem Manifest des installierten Packs | **Sie deckt einen Platzhalter, nicht alle.** `<EXCLUDED_PATHS>` ist der einzige, dessen Wert eine maschinell vergleichbare Gestalt hat (eine Globliste) und der zugleich zwei Schichten bindet. **Das ist eine Enthaltung, keine Stille**, und sie steht im Kopfkommentar |
| **E3** | **Ist (c) nicht zu streng – ein `deny`-Korb darf mehr sperren?** | **Die Richtung ist nur eine.** Geprüft wird *Quelle → Korb*, nie umgekehrt: Ein überzähliger Eintrag bleibt zulässig. Das ist dasselbe Argument, mit dem Prüfung 42 die vier Pfadschlitze ausnimmt – *dort ist Überzähliges ohnehin erlaubt* | **Der gemessene Fall wird trotzdem gefangen**, weil `.github/workflows/**` im Korb **fehlt**. Was die Prüfung nicht fängt: eine Sperre, die über die Quelle hinausgeht und schadet. **Das steht als Grenze im Kopfkommentar** |
| **E4** | **Bekommt Prüfung 49 den Übungsweg?** | **Ja, als zweiter Gegenstand, und schmal:** Nennt der Auslöser einer `sitzung`-Zelle eine Übung, deren Abschnitt in `onboarding/exercises/EXERCISES.md` mindestens einen nicht modellaufrufbaren Skill führt, muß der Auslöser **mindestens einen ausdrücklichen Aufruf** `/name` enthalten. Die Skills werden aus der Übungsdatei **abgeleitet** | **Sie prüft nicht, ob es der richtige oder ob es alle sind.** Ein Auslöser, der eine Übung nennt und einen ihrer Skills aufruft, hat den Ablauf bewußt zugeschnitten – `FW-SC-01` tut genau das. **Eine Prüfung kann Zuschnitt nicht von Vergeßlichkeit unterscheiden; das steht als Grenze im Kopfkommentar.** Und: Geht der Anker der Übungsdatei verloren, **meldet sie das als Fehler**, statt leise zu bestehen |
| **E5** | **Bekommt die Vorbedingungsspalte eine Prüfung?** | **Ja, als vierter Gegenstand von Prüfung 44:** Jeder Testfall, den eine Registerzeile in ihrer Testfallspalte nennt, muß die Kennung dieser Zeile in seiner **Vorbedingungszelle** führen – und zwar **vor dem ersten Vermerk** (🔴/🟢). Und umgekehrt: Jede Zelle, die eine Kennung vor dem ersten Vermerk nennt, steht in der Testfallspalte dieser Zeile | **Der Zuschnitt ist eine Konvention über Markdown-Prosa.** Er trägt, weil der Vermerk in diesem Bestand durchgängig die Geschichte von der Bedingung trennt – **belegt wird er durch ein Paar:** eine Sonde vor dem Vermerk, eine Gegenprobe dahinter |
| **E6** | **Wird das Übungsrepositorium berichtigt?** | **Ja**, beide Träger auf `.github/workflows/**`. Es liegt außerhalb des Kerns und ist kein Teil dieses Releases – **aber ohne die Berichtigung meldet Prüfung 59 dort sofort, und `SK-012-P01` bleibt unfahrbar** | **Ein Eingriff in eine Meßumgebung, unmittelbar vor einer Messung.** Er wird im Protokoll ausgewiesen und ist ein Zustand, den `0.63.0` ausdrücklich herstellen wollte – **keine neue Festlegung, sondern das Nachziehen einer getroffenen** |
| **E7** | **Wie wird die Verschiebung des Releaseplans festgehalten?** | **Ausgerechnet statt gepflegt.** Die Anmerkung nennt die Stelle, an der der fünfte Sitzungstest im Plan von `0.56.0` stand (`0.60.0`), und die, an der er jetzt steht – **die Differenz ist die Zahl.** Die Posten mit Tilde werden weiter nicht umnummeriert (E6 von `CR-2026-085`) | **Die Anmerkung wird länger.** Dafür kann sie nicht mehr um drei danebenliegen, wie seit `0.62.0` |
| **E8** | **Bewegt `0.65.0` eine Zahl von D-11?** | **Nein, und das Release sagt es.** Sein Gegenstand ist, daß der sechste Posten überhaupt mißt, was er zu messen vorgibt. Der fünfte Sitzungstest rückt auf `0.66.0`, die Testblätter auf `0.67.0 bis ~0.70.0`; die Kette 92 → 85 → 0 bleibt unberührt | **Das sechste Release ohne Zahlbewegung in dieser Reihe.** Dafür wäre eine von sieben Zellen nicht gefahren worden, obwohl sie fahrbar ist – und vier Blattzellen wären in einen Baum gelaufen, der ihren Träger sperrt |

## 8. Entscheidung

| Feld | Inhalt |
|---|---|
| Entscheidung | **Angenommen, alle acht Fragen wie vorgelegt.** |
| Datum | 2026-09-18 |
| Entscheidende Rolle | `<FRAMEWORK_OWNER>` |
| Decision-Log-Einträge | **D-170** (`FW-PO-02` ist fahrbar; der Gegenstand einer Testzelle steht in ihrer Erwartungs- und ihrer Fehlerbildzelle, D-144 wird insoweit ersetzt), **D-171** (Prüfung 59: Wertabgleich Quell-Overlay ↔ geladene Schicht ↔ `deny`-Korb für `<EXCLUDED_PATHS>`), **D-172** (Prüfung 49 zweiter Gegenstand: der Auslöser, der eine Übung nennt), **D-173** (Prüfung 44 vierter Gegenstand: zeilenweise Deckung vor dem ersten Vermerk), **D-174** (die Verschiebung des Releaseplans wird ausgerechnet, nicht gepflegt), **`K-69`** neu |
| Auflagen | **Wer einer Testzelle einen Gegenstand zuschreibt, liest zuerst ihre Erwartungs- und ihre Fehlerbildzelle.** Und: **Wer einen Overlay-Wert ändert, ändert ihn in allen vier Trägern** – Quelle, Manifest, Laufzeitfassung, Berechtigungsdatei |
| Ziel-Release | `0.65.0` |
| Umsetzung | umgesetzt mit `0.65.0` |

## 9. Abnahme

- Validator `0 Fehler, 0 Warnungen`, **beide Kodierungsumgebungen**.
- Sondenlauf: neue Sonden und Gegenproben zu **44**, **49** und **59**; Spanne
  `6, 14 und 18 bis 59` in allen drei Trägern **ausgerechnet**, nicht gepflegt.
- **Gegenbeweis gegen den unberührten Vorstand:** Prüfung 59 gegen das
  Übungsrepositorium im Stand **vor** der Berichtigung meldet die Abweichung
  `.github/**` gegen `.github/workflows/**` in beiden Trägern; nach der Berichtigung
  ist sie still.
- **Prüfung 49b** gegen `FW-PO-02` im Stand **vor** der Berichtigung des Auslösers:
  vier Meldungen, eine je Skill von Ü3.
- Übungsrepositorium: `validate-framework.py --strict-overlay` → 0/0 nach der
  Berichtigung.

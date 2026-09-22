# Änderungsantrag `CR-2026-099`

| Feld | Inhalt |
|---|---|
| Titel | `K-74` entschieden und die Vorbedingungen von Bündel 3 – die Marke, die keine Ausgabemarke ist, und die Vorbedingung aus einem fremden Strang |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-19 |
| Betroffene Artefakte | zehn `framework/skills/*/TESTS.md` (18 Markennennungen, drei Vorbedingungen, zwei Ergebnisvermerke), `docs/RUNTIME_GLOSSARY.md` (neuer Abschnitt, Version `0.3.0` → `0.4.0`), `tests/TEST_CATALOG.md` (Punkt 4, Nachweisspanne), `onboarding/exercises/README.md` (`UEB-18` bis `UEB-20`), `tests/scripts/validate-framework.py` (**Prüfung 64**), `tests/scripts/probe-pruefungen.py` (vier Sonden, drei Gegenproben), `governance/DECISION_LOG.md` (**D-197**, **D-198**, `K-74` erledigt), `docs/ROADMAP.md`, `tests/protocols/2026-09-19-vorbedingungen-buendel-3.md` (neu), `CHANGELOG.md`, `VERSION`; **außerhalb des Repositoriums:** das Übungsrepositorium (`UEB-18` bis `UEB-20`, Mentorenblatt) |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand sind Testblätter, Laufzeitglossar und Prüfapparat |
| Art | Herrichtung vor einem Meßtag, **keine Messung, kein Kontingent** |
| Dringlichkeit | **Regulär, mit einer Frist:** Beides gehört **vor** Bündel 3 – `K-74` laut Decision Log, die Vorbedingungen nach fünfzehn Durchgängen Erfahrung |

## 1. Anlass

Zwei Dinge stehen vor dem Meßtag von Bündel 3, und beide sind im Vorfeld benannt worden:
`K-74` (die Ausgabemarken) und der Vorbedingungsdurchgang. **Beide haben mehr gefunden,
als ihr Auftrag erwarten ließ.**

## 2. `K-74` – die Frage, die die Zählung nicht gestellt hatte

`K-74` hat am 2026-09-19 gezählt: `[HALT]` und `[RÜCKFRAGE]` stehen mit 145 Fundstellen in
54 anweisenden Trägern im Kern und sind in keinem Kernmodul und keinem Glossar erklärt.
Die Vorlage nannte zwei Auflösungen – die Marken erklären oder die Zellen auf die Form
abstellen.

🔴 **Die entscheidende Frage war eine dritte, und sie stand in keiner Fassung des
Klärungspunkts: In WELCHEM Abschnitt steht die Marke?** Ausgezählt über die zwölf Skills:

| Marke | Abschnitt 5 (Ausgabeformat) | Abschnitt 6 (Qualitätskriterien) | Abschnitt 2, 3, 7 |
|---|---|---|---|
| `[HALT]` | 3 – **nur** `fw-plan`, `fw-bugfix-prepare`, `fw-change-small` | 3 – dieselben drei | 42 |
| `[RÜCKFRAGE]` | **0** | **0** | 43 |

🔴 **`[RÜCKFRAGE]` ist gar keine Ausgabemarke.** Sie ist durchgehend **Handlungsmarke**:
`| Kontrollstufe nicht angegeben \| [RÜCKFRAGE] |` heißt *frage zurück*, nicht *schreibe
die Zeichenfolge*. **`[HALT]` ist beides, je nach Skill** – und wo sie Abnahmekriterium
ist, sagt Abschnitt 6 *„ist **erkennbar**"*, nicht *„wörtlich"*.

🔴 **Ein gemessener Lauf hatte es vorgeführt, bevor es benannt war.** `sk004n01` (Bündel 2)
schrieb `[HALT]` – Abschnitt 6 von `fw-plan` verlangt es – und `[RÜCKFRAGE]` **nicht**,
obwohl er zurückfragte, und zwar genau in der verlangten Form. **Der Lauf hatte in beidem
recht; die Zelle verlangte trotzdem beides.**

**Gemessen über alle dreizehn Blätter: 18 Nennungen in 17 Zellen sind ungedeckt**, zehn
gedeckt. In Bündel 3 sind **9 von 13** ungedeckt – alle **sechs** Nennungen von `fw-refactor`
(fünf Zellen, `SK-007-N04` nennt beide Marken), beide von `fw-tests` und eine von
`fw-change-small`.

⚠️ **Und die Zählung von `K-74` war wieder zu klein.** Nachgezählt gegen den Kern,
Aufzeichnungen ausgenommen (D-141): `[HALT]` **101** statt 92 Fundstellen, `[RÜCKFRAGE]`
**54** statt 52 ohne die ASCII-Form. **Wer hier eine Zahl liest, zählt sie nach – auch die
eigene.**

## 3. Die achtzehn Vorbedingungen – fünfzehn tragen, drei nicht

**Zum fünfzehnten Mal in Folge der billigste Befund des Releases**, und alle drei Befunde
fielen **vor** dem ersten Lauf an.

| Zelle | Was fehlte | Abhilfe |
|---|---|---|
| `SK-005-P02` | Ein **bestätigter Plan**, der eine Datei nennt, während der Ist-Zustand eine zweite erfordert. **Ein Plan ist ein Artefakt eines LAUFS** – die fünfte Wiederholung nach `UEB-06`, `UEB-07`, `UEB-08`, `UEB-17` (D-192) | `UEB-18` |
| `SK-005-N03` | Ein Fehlschlag, der **durch** die Änderung entsteht und dessen Ursache **außerhalb** der bestätigten Zieldateiliste liegt. `UEB-08` ist schon im Ausgangsstand rot und trifft den **anderen** Zweig von Arbeitsschritt 9 | `UEB-19` |
| `SK-006-N01` | Der Sichtbarkeits- oder Konstruktorfall. 🔴 **Im ausführbaren Strang gibt es ihn nicht** – das Testwerkzeug erreicht jedes Verhalten über Modul- und Zeitattrappen, ohne Produktivcode anzufassen | `UEB-20` |

🟢 **Nachgemessen statt übernommen:** Frontend-Suite **51 grün** (nach den Präparationen
59), Lint Exit 0, `UEB-06` gibt seinen Wartungshinweis in der Testausgabe aus,
`bestand.test.ts` führt drei Fälle (`UEB-08` nicht gesetzt). Das Übungsrepositorium steht
auf Framework **0.70.0**; `0.71.0` und `0.72.0` haben **keinen** der drei Bündel-3-Skills
angefaßt – **das Heben wird trotzdem Pflicht, weil dieses Release ihre `TESTS.md`
anfaßt.**

## 4. Der Nachweis, daß `UEB-19` wirkt

Eine Präparation, deren Gegenstand erst **durch einen Lauf** entsteht, belegt sich nicht
durch ihr Dasein (`UEB-06`, dreizehn Releases). Gemessen am 2026-09-19 mit einem
Wegwerf-Eingriff, der nach der Messung zurückgenommen wurde:

```
FAIL  src/api/mahnung.test.ts > mahnstufe > erinnert am letzten Tag der Erinnerungsfrist noch
AssertionError: expected 'mahnung' to be 'erinnerung'
 Test Files  1 failed | 9 passed (10)
      Tests  1 failed | 58 passed (59)
```

**Das Paar ist der Nachweis:** ohne die Verlagerung 59 grün, mit ihr genau eine
fehlschlagende Zusicherung – und ihre Ursache liegt in `mahnsaetze.ts`, nicht in der
bestätigten Zieldatei.

## 5. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Wie wird die Lücke zwischen Zelle und Skill geschlossen – Marke nachziehen oder Zelle auf die Sache abstellen?** | **Die Zelle stellt auf die Sache ab**, die Marke wörtlich nur, wo Abschnitt 5 oder 6 des Skills sie führt. Dazu: beide Marken im Laufzeitglossar erklärt, **Prüfung 64** setzt die Deckung durch | Siebzehn Zellen angefaßt. **Der Gegenpreis wäre größer:** Die Marke in Abschnitt 5 und 6 der neun übrigen Skills nachzuziehen hieße bis zu zwölf `SKILL.md` – und eine Versionsanhebung ist immer eine **Dateizahl mal zwei**; die drei Meßgegenstände von Bündel 3 hätten sich unmittelbar vor der Messung geändert. **Ein Eintrag in einer `TESTS.md` hebt die Skillversion nicht** (D-119) |
| **E2** | **Warum wird hier die Zelle geändert, wo D-196 genau das verworfen hat?** | **Weil die Lage eine andere ist** | Der Anschein einer Ungleichbehandlung, und deshalb steht die Begründung namentlich hier: Bei D-196 trägt die geladene Schicht die Kennung **gar nicht** – die Erwartung ist unerfüllbar, und eine Regel muß jede **künftige** Zelle mit abdecken. Hier steht die Marke **in** der geladenen Schicht (die `SKILL.md` wird ganz eingefügt, D-187), nur als Anweisung statt als Ausgabe. **Der Widerspruch liegt zwischen Zelle und Skill und ist damit maschinell prüfbar**; der Fall von D-196 ist es nicht |
| **E3** | **Werden die drei Zellen ohne Gegenstand hergerichtet oder vertagt?** | **Hergerichtet – `UEB-18` bis `UEB-20`** | Drei Präparationen mehr, und `UEB-19` bringt zwei neue Module in den ausführbaren Strang. **Der Gegenpreis der Vertagung ist teurer:** Die drei stünden weiter als `offen`, also als **fahrbar** – genau die Bauform, die `UEB-06` dreizehn und `UEB-07` zwanzig Releases lang getragen hat |
| **E4** | **Wird `UEB-20` im ausführbaren Strang gebaut?** | **Nein – im Backend-Strang** | Die Präparation ist **nicht durch einen Lauf belegbar** (`K-68`) und belegt sich durch ihr Dasein, wie `UEB-14`. **Der Gegenpreis wäre eine Präparation, die ihren Gegenstand nicht herstellt:** Jede Fassung im ausführbaren Strang wäre über eine Modul- oder Zeitattrappe testbar, **und der Lauf hätte zu Recht widersprochen.** Der Testfall braucht den Lauf ohnehin nicht – sein erwartetes Verhalten ist ein Unterlassen **vor** dem ersten Schreibzugriff, und `fw-tests` führt den Testbefehl erst danach aus |
| **E5** | **Wird `UEB-19` an `UEB-03` aufgehängt?** | **Nein – ein eigenes Modulpaar** | Zwei Module mehr. **Der Gegenpreis ist D-137:** Die falsche Grenze von `UEB-03` macht die Scope-Falle von `FW-SC-01` aus und darf nicht angefaßt werden; eine zweite Präparation am selben Ort nähme der ersten den Gegenstand |
| **E6** | **Wird in diesem Release gemessen?** | **Nein – Herrichtung ohne Kontingent; der Meßtag ist `~0.74.0`** | Ein Einschub mehr, und **Kriterium 2 bewegt sich nicht.** Das ist richtig so: Ein Meßbaum entsteht aus dem **committeten** Stand (D-191, 0.59.1). Wer Herrichtung und Messung in ein Release legt, mißt gegen einen Stand, dessen Herrichtung im selben Release liegt |

## 6. Entscheidung

**E1 bis E6 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-19). Zwei Decision
Records: **D-197** (Ausgabemarke gegen Handlungsmarke, Prüfung 64) und **D-198** (die drei
Vorbedingungen und die Bauform der Vorbedingung aus einem fremden Strang). `K-74` ist damit
erledigt.

## 7. Abnahme

- `validate-framework.py`: **0 Fehler, 0 Warnungen** gegen den fertigen Baum.
- `probe-pruefungen.py` in **beiden** Kodierungsumgebungen (D-49), voller Lauf.
- 🔴 **Prüfung 64 ist der Wirkungsnachweis dieses Antrags**, und die dritte Gegenprobe ist
  die wichtigere Hälfte: Die **letzte** Zelle einer Zeile ist der Ergebnisstatus und damit
  eine Aufzeichnung – ein Lauf, der die Marke geschrieben **hat**, darf das dort berichten.
  **Wer die Zeile statt der Spalte nimmt, entfernt den Gegenstand mit** (dieselbe
  Trennlinie, die Prüfung 48 zieht).
- 🔴 **Prüfung 44 ist der Wirkungsnachweis für `UEB-18` bis `UEB-20`:** Sie verlangt
  zeilenweise Deckung zwischen Register und **Vorbedingung** – eine Kennung, die nur im
  grünen Vermerk der Ergebniszelle stünde, sähe sie nicht (D-173).
- Der Frontend-Strang des Übungsrepositoriums: **59 grün**, Lint Exit 0.

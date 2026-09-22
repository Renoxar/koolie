# Änderungsantrag `CR-2026-101`

| Feld | Inhalt |
|---|---|
| Titel | `K-77` wird ein eigener Posten vor Bündel 4 – der Klärungspunkt, den der Plan nicht führte |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-19 |
| Betroffene Artefakte | `docs/ROADMAP.md` (Posten `0.74.1`, neuer Posten `~0.75.0`, drei Posten um eine Nummer verschoben, Anmerkung zur Zahl der Einschübe, **Berichtigung der Zeile `0.74.0`**), `governance/DECISION_LOG.md` (**D-204** neu, `K-77` Statuszelle, **Berichtigung der Belegzellen von D-203 und `K-77`**), `governance/change-requests/CR-2026-100-testblaetter-buendel-3.md` (Berichtigung), `tests/protocols/2026-09-19-testblaetter-buendel-3.md` (Berichtigung), `CHANGELOG.md`, `VERSION` |
| Ebene laut Entscheidungsbaum 6 | **Core** – Gegenstand ist der Releaseplan |
| Art | Planänderung, keine Messung, kein Kontingent |
| Dringlichkeit | **Regulär, mit einer Frist:** Der Posten steht vor Bündel 4 und verliert seinen Sinn, sobald dieses gefahren ist |

## 1. Anlass

Am 2026-09-19 ist mit `CR-2026-100` (D-203) festgelegt worden, daß **`K-77` vor Bündel 4
zu entscheiden ist**. Die Festlegung steht seither an vier Stellen:

| Träger | Was dort steht |
|---|---|
| `governance/DECISION_LOG.md`, Zeile `K-77` | Priorität *„hoch, vor Bündel 4"*, die zwei Wege und der Preis von Weg (2) |
| `CHANGELOG.md`, Abschnitt *Bekannte Einschränkungen* zu `0.74.0` | *„Vor Bündel 4 zu entscheiden."* |
| `tests/protocols/2026-09-19-testblaetter-buendel-3.md` | der Meßbefund, aus dem der Punkt entstanden ist |
| die Übergabe (**außerhalb** des Repositoriums, unversioniert) | der Wiederaufnahmepunkt |

🔴 **Sie steht nicht im Releaseplan.** Der Plan führt als nächsten Posten unverändert
`~0.75.0` **Testblätter, Bündel 4** – also genau den Meßtag, vor dem die Entscheidung
fallen soll. **Wer den Plan liest, um zu wissen, was als nächstes kommt, liest die
Reihenfolge, die D-203 verworfen hat.**

## 2. Warum das nicht kosmetisch ist – der Preis steht fest und ist gerechnet

D-203 hat an achtzehn Zellen gemessen: **vier sind zurechenbar, zwei zur Hälfte, zwölf
nicht** – zur Zuordnung dieser vier siehe Abschnitt 5, sie ist mit diesem Antrag
berichtigt. Bei den zwölf zitiert der
Kontrolllauf die Schranke, die der Zuschnitt gar nicht angefaßt hat – sie steht in
Abschnitt 4 der `SKILL.md`, und die wird beim Aufruf über den Schrägstrich **ganz** in die
Sitzung eingefügt (D-187).

**Bündel 4 hat 19 Ergebniszellen.** Wird der Punkt nicht vorher entschieden, fährt der
Meßtag neunzehn Kontrollläufe nach der Klasseneinteilung von Bündel 3 – und bekommt für
den Großteil davon **dieselbe Zahl wie am 19.09.**: eine Zurechenbarkeit, die der
Zuschnitt nicht herstellen kann.

**Gerechnet mit den Meßwerten von Bündel 3** (52,63 USD auf 48 Läufe = **1,10 USD je
Lauf**, nachgerechnet): 19 × 1,10 USD = **20,90 USD**. Das ist der Betrag, den Weg (2)
des Klärungspunkts spart – und er ist kein Schätzwert, sondern der eigene Meßwert des
Vortags.

🔴 **Und der teurere Teil ist nicht das Geld.** Ein Meßtag, der ohne die Entscheidung
fährt, trägt den Befund von D-203 ein zweites Mal ins Protokoll und erzeugt damit
neunzehn Zellen, deren Zurechenbarkeitsangabe hinterher nach derselben Frage neu bewertet
werden müßte. **Das ist die Bauform *„der Befund, der an der eigenen Abhilfe altert"*
(D-164), bevor die Abhilfe überhaupt gebaut ist.**

## 3. Der Posten und wo er hingehört

**Neuer Posten `~0.75.0`: `K-77` entscheiden – wie ein Kontrolllauf für eine Zelle
geschnitten wird, deren Schranke im Skill steht.** Ohne Kontingent, ein Vormittag.
Bündel 4 rückt auf `~0.76.0`, Bündel 5 auf `~0.77.0`, die vier Zellen des zentralen
Katalogs auf `~0.78.0`.

**Die Kriterium-2-Kette bleibt unberührt**, weil der neue Posten keine Vorhersage zu
Kriterium 2 trägt – er bewegt die Zahl nicht, und eine Entscheidung ist keine Messung.
Prüfung 53 rechnet die Kette nach und ist damit zugleich der Wirkungsnachweis dieses
Antrags.

**`K-76` wird mitgeführt, aber nicht mitentschieden.** Er wird fällig, sobald wieder ein
Wiederherstellungsschritt gemessen wird; ob Bündel 4 einen enthält, sagt der
Vorbedingungsdurchgang, der dem Meßtag ohnehin vorausgeht. Der Posten nennt ihn deshalb
als Bedingung, nicht als Gegenstand.

## 4. Was dieser Antrag NICHT tut

🔴 **Er entscheidet `K-77` nicht.** Die beiden Wege stehen im Klärungspunkt, ihre Preise
sind benannt, und der Vergleich gehört in den Antrag, der die Arbeit auslöst – nicht in
den Plan. **Das ist dieselbe Trennlinie wie bei `CR-2026-098` E4:** Der Plan sagt **was**
und **wann**; die Ermessensfragen werden einzeln vorgelegt, mit Auflösung und Preis.

## 5. Der zweite Gegenstand: eine Zuordnung, die die eigene Ergebnistabelle widerlegt

🔴 **Der Durchgang vor dem Commit hat sich zum ACHTZEHNTEN Mal getragen** – und
diesmal an der Zahl, auf die sich dieser Antrag stützt.

D-203, die Zeile `0.74.0` des Releaseplans, der Eintrag `K-77` im Decision Log, die
Tabelle in `CR-2026-100` und die Zusammenfassung des Meßprotokolls sagen alle:
*„vier zurechenbar – und alle vier tragen `ohneskill`“*. **Nachgezählt an der
Einzeltabelle in Abschnitt 5 desselben Protokolls sind es drei.**

| Zelle | Kontrollzuschnitt | Zurechenbar |
|---|---|---|
| `SK-005-P01` | `ohneskill` | 🟢 ja |
| `SK-007-P01` | `ohneskill` | 🟢 ja |
| `SK-006-P01` | `ohneskill` | 🟢 ja, scharf |
| **`SK-005-N05`** | **`k3`** – eine der dreizehn **Regelschicht**-Klassen | 🟢 **ja, scharf** |

🔴 **Der Widerspruch stand drei Zeilen auseinander im selben Protokoll:** Die
Zusammenfassungstabelle sagt *„alle vier `ohneskill`“*, der Satz unmittelbar darunter
sagt *„Wo `ohneskill` steht, trennt es sauber, und zwar in allen **drei** Fällen“*.
**Der Zähler war richtig, die Zuordnung nicht** – dieselbe Bauform wie bei `K-74`
(*die Doppelzahl hat zwei Zahlen, und beide sind nachzuzählen*), nur daß hier nicht die
zweite Zahl falsch war, sondern die **Zuschreibung**.

🟢 **Und der Beleg ist stärker als der Zählfehler.** `ksk005n05` – der
Kontrolllauf zu `SK-005-N05` – **schreibt** den personenbezogen strukturierten Datensatz
in `ausleihen.fixture.ts`, während der Hauptlauf ihn verweigert. Der Skill war in
**beiden** Bäumen vorhanden (die Antwort nennt `fw-change-small v0.1.2`); geschnitten
war allein die Datenschutzregel. **Ein Regelschicht-Zuschnitt hat also getrennt.**

🔴 **Warum `k3` trennt und `plan` nicht – und warum das die Frage von `K-77`
verschiebt:** Die Marken von `k3` (`K3`, `personenbezogen`, `Datenschutz`,
`SECURITY_CONTACT`, `Secret` …) treffen **zehn Zeilen in
`framework/skills/fw-change-small/SKILL.md`**, darunter die Ausschlußzeile in
**Abschnitt 4** (*„Ausgeschlossene Informationen: K3 gemäß …“*) und die
Rückfragenregel. Der Zuschnitt hat die Schranke damit **auch im Skill** entfernt. Der
Zuschnitt `plan` hat genau das bei `R11` nicht geschafft – das Protokoll sagt es
wörtlich (*„nein – R11 steht im Skill“*).

➡️ **Die Trennlinie ist nicht *Regelschicht gegen Skill*, sondern die REICHWEITE des
Zuschnitts.** Damit ist Weg (1) des Klärungspunkts – ein Zuschnitt, der in die
`SKILL.md` hineinreicht – **nicht neu zu erfinden: er ist am 19.09. einmal gefahren
worden, ohne daß es jemand so genannt hätte, und er hat funktioniert.**

**Was dieser Antrag deshalb NICHT tut:** Er zieht daraus keine Entscheidung. Die
Berichtigung ist eine Tatsachenfeststellung; welcher der beiden Wege gewählt wird –
und ob dieser Fall einen dritten eröffnet –, gehört in den Posten `~0.75.0`.

**Berichtigt werden fünf Träger:** die Belegzellen von D-203 und `K-77`, die Zeile
`0.74.0` des Releaseplans, die Tabelle in `CR-2026-100` und die Zusammenfassung des
Protokolls. **Der Eintrag `0.74.0` im Änderungsverzeichnis bleibt unverändert** – er
ist die Aufzeichnung dessen, was jenes Release gesagt hat; die Berichtigung steht im
Eintrag `0.74.1` (D-141).

## 6. Vorlage zur Entscheidung

| # | Frage | Auflösung | Preis |
|---|---|---|---|
| **E1** | **Bekommt `K-77` einen eigenen Posten im Releaseplan?** | **Ja, `~0.75.0`, vor Bündel 4** | Eine Nummer mehr, und drei Posten verschieben sich. **Der Gegenpreis ist gerechnet:** neunzehn Kontrollläufe zu 1,10 USD für eine Zahl, die schon feststeht |
| **E2** | **Oder gehört die Entscheidung an den Bündel-4-Posten angehängt?** | **Nein** | Ein Posten weniger. **Verworfen, weil der Posten dann zwei Gattungen mischt:** Bündel 4 trägt ein Sitzungskontingent, `K-77` keines. Ein Klärungspunkt, der im Meßtag mitläuft, wird im Meßtag entschieden – also **nach** dem Zuschnitt, den er bestimmen soll |
| **E3** | **Wird `K-76` mitentschieden?** | **Nein – mitgeführt als Bedingung** | Ein offener Punkt bleibt offen. **Sein Auslöser ist ein anderer:** `K-76` wird fällig, wenn wieder ein Wiederherstellungsschritt gemessen wird, und ob Bündel 4 einen enthält, sagt erst der Vorbedingungsdurchgang |
| **E4** | **Gibt es einen Decision Record, oder trägt der Plan die Festlegung allein?** | **Ein Decision Record: D-204** | Ein Eintrag mehr im Register. 🔴 **Hier anders als bei `CR-2026-098`, und der Unterschied gehört benannt:** Dort war der Gegenstand eine **Anforderung**, die der Plan vollständig trägt. Hier ist er eine **Reihenfolge mit einem gerechneten Preis** und einer verworfenen Alternative (E2) – und genau das ist die Gattung eines Decision Records. Zwei Träger derselben Gattung dürfen verschieden ausgehen, wenn die Begründung namentlich dabeisteht |
| **E5** | **Wird in diesem Release etwas gemessen?** | **Nein – Planänderung, Patch-Release `0.74.1`** | Ein Einschub mehr. **PATCH und nicht MINOR:** Das Release legt weder Modul noch Skill noch Regel an (`RELEASE_PROCESS.md` Abschnitt 1) – es ordnet eine Reihenfolge. **Kriterium 2 bewegt sich nicht**, und das ist richtig so |

| **E6** | **Wird die Zuordnung der vier zurechenbaren Zellen in diesem Release berichtigt?** | **Ja, in fünf Trägern** – ohne neuen Decision Record | Der Zuschnitt des Releases wird größer als *„reine Planänderung“*. 🔴 **Der Gegenpreis ist größer:** Dieses Release trägt den Posten ein, der `K-77` entscheiden läßt – und stützte sich dabei auf eine Zuordnung, die die eigene Ergebnistabelle widerlegt. **Verworfen:** einen Decision Record dafür zu bauen; eine nachgezählte Zahl wird im Projekt als **Vermerk** am Ort der Zahl berichtigt (`K-74`, D-197), nicht als neue Entscheidung. **Verworfen:** den Eintrag `0.74.0` im Änderungsverzeichnis anzufassen – er ist Aufzeichnung (D-141) |

## 7. Entscheidung

**E1 bis E6 wie vorgelegt entschieden** (`<FRAMEWORK_OWNER>`, 2026-09-19). Decision Record
**D-204** für den Posten; die Berichtigung trägt keinen eigenen Record und steht als
Vermerk an jeder der fünf Stellen. `K-77` bleibt offen und trägt jetzt seinen Posten.

## 8. Abnahme

- `validate-framework.py`: **0 Fehler, 0 Warnungen** gegen den fertigen Baum.
- `probe-pruefungen.py` in **beiden** Kodierungsumgebungen (D-49), voller Lauf.
- 🔴 **Prüfung 53 ist der Wirkungsnachweis dieses Antrags:** Sie rechnet die Kette der
  Releaseplan-Posten nach, und dieser Antrag schiebt einen Posten dazwischen. **Die Kette
  darf sich dabei nicht bewegen** – der neue Posten trägt keine Vorhersage zu Kriterium 2,
  und `38 → 19 → 4 → 0` muß unverändert schließen.
- 🔴 **Prüfung 58 ist der zweite:** `D-204` ist eine neue Kennung und braucht ihre
  Registerzeile, sonst meldet die Prüfung den eigenen Antrag (0.64.0).

## 9. Migrationshinweis

**Keiner** – dieses Release ändert keinen ausgelieferten Laufzeitträger. Kein Skill hebt
seine Version, kein Overlay-Wert ändert sich.

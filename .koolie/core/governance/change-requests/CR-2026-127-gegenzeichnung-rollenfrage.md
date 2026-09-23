# Änderungsantrag `CR-2026-127`

| Feld | Inhalt |
|---|---|
| Titel | Die Gegenzeichnung der Protokolle: Wer ist die zweite Rolle? |
| Antragstellende Rolle | `<FRAMEWORK_OWNER>` |
| Datum | 2026-09-23 |
| Betroffene Artefakte | `.koolie/core/tests/protocols/` (Abschnitt *Gegenzeichnung* je Protokoll); `.koolie/core/checklists/11-framework-release.md`; `.koolie/core/governance/RACI.md`; `.koolie/core/governance/DECISION_LOG.md` |
| Ebene laut Entscheidungsbaum 6 | Governance. **Rollenfrage**, keine technische Änderung |
| Art | Entscheidung (Auslegung einer bestehenden Pflicht) |
| Dringlichkeit | **blockierend für `1.0.0`.** Solange sie offen ist, ist `AP11` formal nicht abgeschlossen |
| Status | 🟢 **entschieden am 2026-09-23** (E1 bis E5), umgesetzt mit `0.91.0` |

---

## 1. Anlass und Problem

`AP11` verlangt die **Gegenzeichnung der Protokolle**. `0.89.0` hat sie nicht ausgeführt
und den Grund als Abgrenzung aufgeschrieben, nicht als Vertagung:

> *„Eine Gegenzeichnung ist die Handlung einer **zweiten Rolle**. Ein Werkzeug, das
> `<TBD: Rolle>` durch einen Rollennamen ersetzt, **fälscht sie**."*

**Das trägt, und es hat eine Folge, die noch niemand benannt hat:** An diesem Framework
arbeitet **eine** Person. Es gibt keine zweite Rolle, und damit ist die Pflicht in ihrer
heutigen Form nicht erfüllbar – nicht aus Nachlässigkeit, sondern konstruktiv.

➡️ ***Eine Pflicht, die niemand erfüllen kann, ist keine Pflicht, sondern ein Befund über
ihre Formulierung.*** Das ist die Bauform *die Regel mit leerer Schnittmenge* (D-189,
`K-72`) an einer Governance-Regel statt an einer Testzelle.

## 2. Der gemessene Bestand

**Zählregel:** *ein Abschnitt mit `Gegenzeichnung` in der Überschrift, und der trägt keinen
`<TBD>` mehr.* Gezählt am 2026-09-22, nachgeprüft am 2026-09-23:

| Menge | gegengezeichnet | offener Abschnitt | ohne Abschnitt |
|---|---|---|---|
| alle **122** Protokolle | 13 | 45 | 64 |
| die **10** FW-Testprotokolle | 3 | 2 | 5 |

⚠️ **Die Zahl hängt an der Zählregel, und deshalb steht sie hier mit ihr.** Eine erste
Zählung über *„das Wort `Gegenzeichnung` kommt vor"* ergab 59 und 52.

🔴 **Der Releaseplan nannte *„zwölf offene und fünf fehlende"*.** *„Fünf ganz ohne"* trifft
für die FW-Testprotokolle; *„zwölf mit offenem Abschnitt"* trifft **keine** der beiden
Abgrenzungen.

## 3. Was die Sache wirklich ist

**Nicht jedes Protokoll ist eine Abnahme.** Von den 122 sind die meisten Arbeits- und
Meßprotokolle – sie berichten, was gemessen wurde, und tragen ihren Beleg in sich. Eine
Gegenzeichnung sagt etwas anderes: *Eine zweite Person hat geprüft und steht dafür ein.*
Das ist bei einem **Abnahmeprotokoll** sinnvoll und bei einem Meßprotokoll nicht.

---

## 4. Vorlage zur Entscheidung

| # | Frage | Wege und ihre Preise |
|---|---|---|
| **E1** | **Wer ist die zweite Rolle?** | **Weg A – eine zweite Person wird benannt und zeichnet wirklich.** Ehrlich und teuer: Jemand muß die Protokolle tatsächlich lesen, sonst ist die Unterschrift eine Zusage ohne Gegenstand – genau der Befundtyp, gegen den dieses Projekt angetreten ist. ⚠️ **Preis:** Es gibt diese Person heute nicht.<br><br>**Weg B – Selbstgegenzeichnung, ausdrücklich als solche ausgewiesen.** Der Abschnitt heißt dann *„Selbstgegenzeichnung (keine zweite Rolle vorhanden)"* und nennt das Datum. ⚠️ **Preis, und er ist real:** Die Zusage *„zweite Rolle"* ist damit **zurückgenommen**, nicht erfüllt – und das gehört in den Decision Log, nicht in eine Fußnote.<br><br>**Weg C – die Pflicht auf die Abnahmeprotokolle eingrenzen.** Nur die **zehn FW-Testprotokolle** tragen eine Abnahme; dort fehlen 2 offene und 5 ohne Abschnitt. Die übrigen 112 sind Arbeits- und Meßprotokolle und bekommen den Abschnitt gar nicht. ⚠️ **Preis:** Die Abgrenzung muß in `checklists/11` und `RACI.md` geschrieben werden, sonst ist sie eine stille Verkleinerung des Gegenstands |
| **E2** | **Falls C: Was gilt für die verbleibenden sieben?** | Entweder A oder B – die Frage bleibt, nur der Umfang schrumpft von 109 auf 7 |
| **E3** | **Wird `<TBD: Rolle>` in den übrigen Protokollen entfernt oder bleibt es stehen?** | **Vorschlag: entfernen, wo der Abschnitt nach E1/E2 entfällt.** Ein `<TBD>`, das nie aufgelöst werden soll, ist eine offene Stelle, die keine ist – und Prüfung 9 zählt offene `<TBD>` in sicherheitsrelevanten Feldern |
| **E4** | **Braucht die Abgrenzung eine Prüfung?** | **Vorschlag: ja, und sie ist billig.** *„Jedes Protokoll der Klasse FW-Test trägt einen Abschnitt `Gegenzeichnung` ohne `<TBD>`"* ist mechanisch prüfbar. Ohne sie ist die Entscheidung eine Zusage ohne Mechanismus |

> **Empfehlung der Vorbereitung: C, dann B für die verbleibenden sieben.**
> Begründung: C schneidet den Gegenstand auf das, was wirklich eine Abnahme trägt, statt
> die Pflicht zu verkleinern; B macht die fehlende zweite Rolle zu einer **benannten**
> Ausnahme statt zu einer stillen. Beides zusammen ist in einer Sitzung erledigt und
> hinterläßt eine nachlesbare Spur.
> ⚠️ **Die Empfehlung ist kein Beschluß.** Eine Freigaberegel zu ändern ist nach `V10`
> nicht delegierbar.

---

## 5. Abnahme

Nach der Entscheidung: die betroffenen Protokolle angepaßt, `checklists/11` und `RACI.md`
nachgezogen, gegebenenfalls die Prüfung aus E4 gebaut, Validator und Sondenlauf grün.

---

## 6. Entscheidung

**Entschieden am 2026-09-23 durch `<FRAMEWORK_OWNER>`.** Festgehalten als **D-319**; `K-107` neu aufgenommen. Umgesetzt mit Release `0.91.0`.

| # | Entscheidung |
|---|---|
| **E1** | **Weg C, dann B.** Die Gegenzeichnungspflicht gilt nur für die **zehn Abnahmeprotokolle** des Testkatalogs; die fehlenden **sieben** sind als **Selbstgegenzeichnung** nachgezogen und weisen das in einem eigenen Satz aus. |
| **E2** | **Weg B für die sieben.** Keine zweite Rolle vorhanden; die Zusage ist **zurückgenommen, nicht erfüllt**, und jeder Abschnitt sagt es. |
| **E3** | 🔴 **Gegen den eigenen Vorschlag entschieden.** Die offenen `<TBD>` in den **45 Arbeits- und Meßprotokollen** bleiben **stehen**. Der Vorschlag lautete „entfernen“ und ist im Durchgang gefallen: Protokolle sind **Chronik** (D-273), sie stehen in **drei verschiedenen Tabellenformen**, und ein Sweep darüber ist die Bauform aus D-277. **Das `<TBD` hält fest, daß dort einmal eine Gegenzeichnung vorgesehen war.** Die Abgrenzung steht **einmal** an den drei Stellen, an denen sie gilt – `checklists/11`, `tests/protocols/README.md`, `RACI.md`. |
| **E4** | **Ja, Prüfung 80.** *Eine Entscheidung ohne Mechanismus ist eine Zusage* – und sie war beim ersten Lauf **rot über genau die sieben**. |
| **E5** | 🆕 **Neu gestellt und mitentschieden: Was IST die Unterschrift?** **Die Zeile sagt, WAS gegengezeichnet wurde; der Commit sagt, WER.** Ein Werkzeug kann die Zeile schreiben – einen Commit unter der Identität des Owners kann es nicht. *Damit wird die Fälschung unmöglich statt nur verboten.* ⚠️ **Preis:** Die Commits sind nicht signiert, die Unterschrift ist so stark wie der Schreibzugriff; `K-107` führt die Frage weiter. |

> 🔴 **Der Text der sieben Abschnitte ist von einem Werkzeug vorbereitet worden, die Freigabe nicht.** Der Owner hat die Protokolle gelesen und den Release-Commit selbst gesetzt. *Der Umfang steht so da, wie er genannt wurde –* *„Protokoll vollständig gelesen“, und keine Silbe mehr.*
